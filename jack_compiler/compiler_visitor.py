"""
Parse-tree visitor for the Jack compiler.

Walks the ANTLR parse tree, emitting Hack VM code via :class:`CodeGenerator`
and building an AST whose shape matches the nand2tetris web-ide reference
implementation.
"""

from typing import Any, Dict, List, Optional

from .codegen import CodeGenerator
from .symbols import VarKind


class Span:
    """Source code span information."""
    def __init__(self, start: int = 0, end: int = 0, line: int = 0):
        self.start = start
        self.end = end
        self.line = line
    
    def to_dict(self):
        return {"start": self.start, "end": self.end, "line": self.line}


class JackCompilerVisitor:
    """
    Visitor that emits VM code and builds an AST matching the reference implementation.
    
    AST Structure:
    - Class: { name, varDecs, subroutines }
    - Subroutine: { type, name, returnType, parameters, body }
    - Statement: { statementType, ... }
    - Expression: { nodeType, term, rest }
    - Term: { termType, ... }
    """

    def __init__(self):
        """Initialize the visitor."""
        self.codegen: Optional[CodeGenerator] = None
        self.class_name: Optional[str] = None
        self.current_span: Span = Span()

    def compile_program(self, ctx: Any) -> Dict:
        """
        Compile a program and return AST.
        
        Args:
            ctx: ANTLR parse tree context for program
            
        Returns:
            Class AST node
        """
        class_ast = self.visit_class_declaration(ctx.classDeclaration())
        return class_ast

    def visit_class_declaration(self, ctx: Any) -> Dict:
        """
        Visit class declaration and generate AST.
        
        Returns:
            {
              name: { value: str, span: Span },
              varDecs: ClassVarDec[],
              subroutines: Subroutine[]
            }
        """
        self.class_name = ctx.className().getText()
        self.codegen = CodeGenerator(self.class_name)
        
        # Process class variable declarations
        var_decs = []
        for var_decl in ctx.classVarDeclaration():
            var_decs.extend(self.visit_class_var_declaration(var_decl))
        
        # Process subroutine declarations
        subroutines = []
        for subroutine in ctx.subroutineDeclaration():
            subroutines.append(self.visit_subroutine_declaration(subroutine))
        
        return {
            "name": {
                "value": self.class_name,
                "span": self.current_span.to_dict()
            },
            "varDecs": var_decs,
            "subroutines": subroutines
        }

    def visit_class_var_declaration(self, ctx: Any) -> List[Dict]:
        """
        Visit class variable declaration.
        
        Returns:
            List of {
              varType: "static" | "field",
              type: { value: str, span: Span },
              names: str[]
            }
        """
        kind = VarKind.STATIC if ctx.STATIC() else VarKind.FIELD
        kind_text = kind.value
        type_name = ctx.type_().getText()
        
        var_names = []
        for var_name in ctx.varName():
            var_names.append(var_name.getText())
            self.codegen.symbol_table.define(var_name.getText(), type_name, kind)
        
        return [{
            "varType": kind_text,
            "type": {
                "value": type_name,
                "span": self.current_span.to_dict()
            },
            "names": var_names
        }]

    def visit_subroutine_declaration(self, ctx: Any) -> Dict:
        """
        Visit subroutine declaration.
        
        Returns:
            {
              type: "function" | "method" | "constructor",
              name: { value: str, span: Span },
              returnType: { value: str, span: Span },
              parameters: Parameter[],
              body: SubroutineBody
            }
        """
        self.codegen.symbol_table.start_subroutine()
        
        # Get subroutine type
        if ctx.METHOD():
            subroutine_type = "method"
            self.codegen.symbol_table.define("this", self.class_name, VarKind.ARG)
        elif ctx.CONSTRUCTOR():
            subroutine_type = "constructor"
        else:
            subroutine_type = "function"
        
        subroutine_name = ctx.subroutineName().getText()
        
        # Get return type (void or type_)
        if ctx.VOID():
            return_type_text = "void"
        elif ctx.type_():
            return_type_text = ctx.type_().getText()
        else:
            return_type_text = "void"
        
        # Process parameters
        parameters = []
        param_list = ctx.parameterList()
        if param_list:
            # ANTLR creates parallel arrays for types and varNames
            types = param_list.type_()
            var_names = param_list.varName()
            
            for param_type_ctx, param_name_ctx in zip(types, var_names):
                param_type = param_type_ctx.getText()
                param_name = param_name_ctx.getText()
                
                self.codegen.symbol_table.define(param_name, param_type, VarKind.ARG)
                
                parameters.append({
                    "type": {
                        "value": param_type,
                        "span": self.current_span.to_dict()
                    },
                    "name": param_name
                })
        
        # Process body
        subroutine_body = ctx.subroutineBody()
        
        # Process local variables
        var_decs = []
        for var_decl in subroutine_body.varDeclaration():
            var_decs.extend(self.visit_var_declaration(var_decl))
        
        # Emit function declaration
        full_name = f"{self.class_name}.{subroutine_name}"
        num_locals = self.codegen.symbol_table.var_count(VarKind.LOCAL)
        self.codegen.emit_function(full_name, num_locals)
        
        # Handle constructor memory allocation
        if subroutine_type == "constructor":
            num_fields = self.codegen.symbol_table.var_count(VarKind.FIELD)
            self.codegen.push_constant(num_fields)
            self.codegen.emit_call("Memory.alloc", 1)
            self.codegen.emit("pop pointer 0")
        
        # Handle method this pointer
        if subroutine_type == "method":
            self.codegen.emit("push argument 0")
            self.codegen.emit("pop pointer 0")
        
        # Compile statements
        statements = []
        for statement in subroutine_body.statements().statement():
            statements.append(self.visit_statement(statement))
        
        return {
            "type": subroutine_type,
            "name": {
                "value": subroutine_name,
                "span": self.current_span.to_dict()
            },
            "returnType": {
                "value": return_type_text,
                "span": self.current_span.to_dict()
            },
            "parameters": parameters,
            "body": {
                "varDecs": var_decs,
                "statements": statements
            }
        }

    def visit_var_declaration(self, ctx: Any) -> List[Dict]:
        """
        Visit variable declaration.
        
        Returns:
            [{
              type: { value: str, span: Span },
              names: str[]
            }]
        """
        type_name = ctx.type_().getText()
        
        var_names = []
        for var_name in ctx.varName():
            name = var_name.getText()
            var_names.append(name)
            self.codegen.symbol_table.define(name, type_name, VarKind.LOCAL)
        
        return [{
            "type": {
                "value": type_name,
                "span": self.current_span.to_dict()
            },
            "names": var_names
        }]

    def visit_statement(self, ctx: Any) -> Dict:
        """Visit a statement and return AST node."""
        if ctx.letStatement():
            return self.visit_let_statement(ctx.letStatement())
        elif ctx.ifStatement():
            return self.visit_if_statement(ctx.ifStatement())
        elif ctx.whileStatement():
            return self.visit_while_statement(ctx.whileStatement())
        elif ctx.doStatement():
            return self.visit_do_statement(ctx.doStatement())
        elif ctx.returnStatement():
            return self.visit_return_statement(ctx.returnStatement())
        
        return {}

    def visit_let_statement(self, ctx: Any) -> Dict:
        """
        Visit let statement.
        
        Returns:
            {
              statementType: "letStatement",
              name: { value: str, span: Span } | str,
              arrayIndex?: Expression,
              value: Expression,
              span: Span
            }
        """
        var_name = ctx.varName().getText()
        
        if ctx.LBRACKET():
            # Array assignment: let array[index] = value
            # Stack: need to compute array+index, then store value there
            self.visit_expression_eval(ctx.expression(0))  # Push index
            self.codegen.push_variable(var_name)  # Push array base
            self.codegen.emit("add")  # Stack: [array+index]
            self.visit_expression_eval(ctx.expression(1))  # Push value
            # Stack: [array+index, value]
            self.codegen.emit("pop temp 0")  # temp0 = value, stack: [array+index]
            self.codegen.emit("pop pointer 1")  # THAT = array+index, stack: []
            self.codegen.emit("push temp 0")  # Stack: [value]
            self.codegen.emit("pop that 0")  # that[0] = value
            
            return {
                "statementType": "letStatement",
                "name": var_name,
                "arrayIndex": self.visit_expression(ctx.expression(0)),
                "value": self.visit_expression(ctx.expression(1)),
                "span": self.current_span.to_dict()
            }
        else:
            # Simple assignment
            self.visit_expression_eval(ctx.expression(0))
            self.codegen.pop_variable(var_name)
            
            return {
                "statementType": "letStatement",
                "name": {"value": var_name, "span": self.current_span.to_dict()},
                "value": self.visit_expression(ctx.expression(0)),
                "span": self.current_span.to_dict()
            }

    def visit_if_statement(self, ctx: Any) -> Dict:
        """
        Visit if statement.
        
        Returns:
            {
              statementType: "ifStatement",
              condition: Expression,
              body: Statement[],
              else: Statement[]
            }
        """
        # Generate VM code for if/else
        if_label = self.codegen.new_label("IF")
        else_label = self.codegen.new_label("ELSE")
        end_label = self.codegen.new_label("ENDIF")
        
        self.visit_expression_eval(ctx.expression())
        self.codegen.emit("not")
        self.codegen.emit_if_goto(else_label)
        
        # If block - collect statements while generating code
        if_statements = []
        for stmt in ctx.statements(0).statement():
            if_statements.append(self.visit_statement(stmt))
        self.codegen.emit_goto(end_label)
        
        # Else block
        self.codegen.emit_label(else_label)
        else_statements = []
        if ctx.ELSE():
            for stmt in ctx.statements(1).statement():
                else_statements.append(self.visit_statement(stmt))
        
        self.codegen.emit_label(end_label)
        
        return {
            "statementType": "ifStatement",
            "condition": self.visit_expression(ctx.expression()),
            "body": if_statements,
            "else": else_statements
        }

    def visit_while_statement(self, ctx: Any) -> Dict:
        """
        Visit while statement.
        
        Returns:
            {
              statementType: "whileStatement",
              condition: Expression,
              body: Statement[]
            }
        """
        loop_label = self.codegen.new_label("WHILE")
        end_label = self.codegen.new_label("ENDWHILE")
        
        self.codegen.emit_label(loop_label)
        self.visit_expression_eval(ctx.expression())
        self.codegen.emit("not")
        self.codegen.emit_if_goto(end_label)
        
        # Collect statements for AST while generating code
        statements = []
        for stmt in ctx.statements().statement():
            statements.append(self.visit_statement(stmt))
        
        self.codegen.emit_goto(loop_label)
        self.codegen.emit_label(end_label)
        
        return {
            "statementType": "whileStatement",
            "condition": self.visit_expression(ctx.expression()),
            "body": statements
        }

    def visit_do_statement(self, ctx: Any) -> Dict:
        """
        Visit do statement.
        
        Returns:
            {
              statementType: "doStatement",
              call: SubroutineCall
            }
        """
        call = self.visit_subroutine_call_eval(ctx.subroutineCall())
        self.codegen.emit_pop_temp()
        
        return {
            "statementType": "doStatement",
            "call": self.visit_subroutine_call(ctx.subroutineCall())
        }

    def visit_return_statement(self, ctx: Any) -> Dict:
        """
        Visit return statement.
        
        Returns:
            {
              statementType: "returnStatement",
              value?: Expression,
              span: Span
            }
        """
        if ctx.expression():
            self.visit_expression_eval(ctx.expression())
            ast = {
                "statementType": "returnStatement",
                "value": self.visit_expression(ctx.expression()),
                "span": self.current_span.to_dict()
            }
        else:
            self.codegen.push_constant(0)
            ast = {
                "statementType": "returnStatement",
                "span": self.current_span.to_dict()
            }
        
        self.codegen.emit_return()
        return ast

    def visit_expression(self, ctx: Any) -> Dict:
        """
        Visit expression and return AST (without evaluation).
        
        Returns:
            {
              nodeType: "expression",
              term: Term,
              rest: ExpressionPart[]
            }
        """
        terms = ctx.term()
        ops = ctx.op()
        
        rest = []
        for i, op in enumerate(ops):
            rest.append({
                "op": op.getText(),
                "term": self.visit_term(terms[i + 1])
            })
        
        return {
            "nodeType": "expression",
            "term": self.visit_term(terms[0]),
            "rest": rest
        }

    def visit_expression_eval(self, ctx: Any):
        """Evaluate expression and emit VM code."""
        terms = ctx.term()
        ops = ctx.op()
        
        self.visit_term_eval(terms[0])
        
        for i, op in enumerate(ops):
            self.visit_term_eval(terms[i + 1])
            self.visit_op(op)

    def visit_term(self, ctx: Any) -> Dict:
        """
        Visit term and return AST (without evaluation).
        
        Returns:
            Term AST with termType field
        """
        if ctx.integerConstant():
            return {
                "termType": "numericLiteral",
                "value": int(ctx.integerConstant().getText())
            }
        
        elif ctx.stringConstant():
            string_text = ctx.stringConstant().getText()
            string_value = string_text[1:-1]
            return {
                "termType": "stringLiteral",
                "value": string_value
            }
        
        elif ctx.keywordConstant():
            return {
                "termType": "keywordLiteral",
                "value": ctx.keywordConstant().getText()
            }
        
        elif ctx.varName():
            if ctx.LBRACKET():
                # Array access
                var_name = ctx.varName().getText()
                return {
                    "termType": "arrayAccess",
                    "name": {"value": var_name, "span": self.current_span.to_dict()},
                    "index": self.visit_expression(ctx.expression()),
                    "span": self.current_span.to_dict()
                }
            else:
                # Variable
                var_name = ctx.varName().getText()
                return {
                    "termType": "variable",
                    "name": var_name,
                    "span": self.current_span.to_dict()
                }
        
        elif ctx.subroutineCall():
            return {
                "termType": "subroutineCall",
                **self.visit_subroutine_call(ctx.subroutineCall())
            }
        
        elif ctx.LPAREN():
            return {
                "termType": "groupedExpression",
                "expression": self.visit_expression(ctx.expression())
            }
        
        elif ctx.unaryOp():
            return {
                "termType": "unaryExpression",
                "op": ctx.unaryOp().getText(),
                "term": self.visit_term(ctx.term())
            }
        
        return {"termType": "unknown"}

    def visit_term_eval(self, ctx: Any):
        """Evaluate term and emit VM code."""
        if ctx.integerConstant():
            value = int(ctx.integerConstant().getText())
            self.codegen.push_constant(value)
        
        elif ctx.stringConstant():
            string_text = ctx.stringConstant().getText()
            string_value = string_text[1:-1]
            self.codegen.emit_string_constant(string_value)
        
        elif ctx.keywordConstant():
            keyword = ctx.keywordConstant().getText()
            if keyword == "true":
                self.codegen.push_constant(1)
                self.codegen.emit("neg")
            elif keyword == "false":
                self.codegen.push_constant(0)
            elif keyword == "null":
                self.codegen.push_constant(0)
            elif keyword == "this":
                self.codegen.emit_this_pointer()
        
        elif ctx.varName():
            if ctx.LBRACKET():
                var_name = ctx.varName().getText()
                self.codegen.push_variable(var_name)
                self.visit_expression_eval(ctx.expression())
                self.codegen.emit_array_access()
            else:
                var_name = ctx.varName().getText()
                self.codegen.push_variable(var_name)
        
        elif ctx.subroutineCall():
            self.visit_subroutine_call_eval(ctx.subroutineCall())
        
        elif ctx.LPAREN():
            self.visit_expression_eval(ctx.expression())
        
        elif ctx.unaryOp():
            self.visit_term_eval(ctx.term())
            op = ctx.unaryOp().getText()
            if op == "-":
                self.codegen.emit_negate()
            elif op == "~":
                self.codegen.emit_not()

    def visit_subroutine_call(self, ctx: Any) -> Dict:
        """
        Visit subroutine call and return AST.
        
        Returns:
            {
              name: { value: str, span: Span },
              parameters: Expression[],
              span: Span
            }
        """
        if ctx.DOT():
            # Get receiver - could be className or varName
            receiver = None
            symbol = None
            
            if ctx.varName():
                receiver = ctx.varName().getText()
                symbol = self.codegen.symbol_table.get_symbol(receiver)
            elif ctx.className():
                receiver = ctx.className().getText()
                symbol = self.codegen.symbol_table.get_symbol(receiver)
            
            method_name = ctx.subroutineName().getText()
            
            if symbol:
                full_name = f"{symbol.type}.{method_name}"
            else:
                full_name = f"{receiver}.{method_name}"
        else:
            full_name = f"{self.class_name}.{ctx.subroutineName().getText()}"
        
        parameters = []
        if ctx.expressionList():
            for expr_ctx in ctx.expressionList().expression():
                parameters.append(self.visit_expression(expr_ctx))
        
        return {
            "name": {"value": full_name, "span": self.current_span.to_dict()},
            "parameters": parameters,
            "span": self.current_span.to_dict()
        }

    def visit_subroutine_call_eval(self, ctx: Any):
        """Evaluate subroutine call and emit VM code."""
        num_args = 0
        
        if ctx.DOT():
            # Get receiver - could be className or varName
            # Check varName first, then className
            receiver = None
            symbol = None
            
            if ctx.varName():
                receiver = ctx.varName().getText()
                symbol = self.codegen.symbol_table.get_symbol(receiver)
            elif ctx.className():
                receiver = ctx.className().getText()
                symbol = self.codegen.symbol_table.get_symbol(receiver)
            
            method_name = ctx.subroutineName().getText()
            
            if symbol:
                # It's a variable - push it and use its type as the class name
                self.codegen.push_variable(receiver)
                full_name = f"{symbol.type}.{method_name}"
                num_args = 1
            else:
                # It's a class name - no implicit this
                full_name = f"{receiver}.{method_name}"
                num_args = 0
        else:
            full_name = f"{self.class_name}.{ctx.subroutineName().getText()}"
            self.codegen.emit_this_pointer()
            num_args = 1
        
        if ctx.expressionList():
            num_args += len(ctx.expressionList().expression())
            for expr_ctx in ctx.expressionList().expression():
                self.visit_expression_eval(expr_ctx)
        
        self.codegen.emit_call(full_name, num_args)

    def visit_op(self, ctx: Any):
        """Visit operator and emit VM code."""
        op = ctx.getText()
        
        if op == "+":
            self.codegen.emit_add()
        elif op == "-":
            self.codegen.emit_subtract()
        elif op == "*":
            self.codegen.emit_multiply()
        elif op == "/":
            self.codegen.emit_divide()
        elif op == "&":
            self.codegen.emit_and()
        elif op == "|":
            self.codegen.emit_or()
        elif op == "<":
            self.codegen.emit_lt()
        elif op == ">":
            self.codegen.emit_gt()
        elif op == "=":
            self.codegen.emit_eq()


# Backwards-compatible alias for code written against the old module name.
JackCompilerVisitorV2 = JackCompilerVisitor
