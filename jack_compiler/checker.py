"""
Semantic checks: the mistakes the grammar can't catch.

The parser only knows what Jack *looks* like. This pass walks the parse tree
before any VM code is generated and reports, with exact locations, the
mistakes that would otherwise produce broken VM code (or a bare Python
exception):

Errors (the file is not compiled)
    * a variable that was never declared               ("did you mean ...?")
    * a name declared twice in the same scope           (+ note: first declared here)
    * two subroutines with the same name
    * 'this', or a field, used inside a function        (functions have no object)
    * calling a method from a function without an object
    * calling a subroutine this class doesn't have      ("did you mean ...?")
    * calling one of this class's subroutines with the wrong number of arguments
    * calling a method on an int / char / boolean variable
    * an integer constant bigger than 32767
    * a subroutine that can reach its end without 'return'

Warnings (the file still compiles)
    * a local variable that is never used (parameters aren't reported: like
      GCC's -Wall, since a method often has to accept an argument it ignores)
    * statements after 'return' that can never run
    * a void subroutine returning a value, or a non-void one returning nothing
    * a constructor that doesn't 'return this'
    * a class whose name doesn't match its file name (the VM looks functions up by it)
    * 'name.f()' where 'name' isn't a variable and doesn't look like a class name
    * a class name that isn't part of the program: not this class, not a
      Jack OS class, and not another .jack file in the same folder ("did you
      mean ...?"). In nand2tetris one folder is one program.

Apart from which classes exist, only things that can be decided from ONE file
are checked: other classes (including the Jack OS) are compiled separately,
so the subroutines called in them, and their arguments, are trusted.
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set

from .diagnostics import ERROR, WARNING, Diagnostic, Note

MAX_INT = 32767
PRIMITIVE_TYPES = {"int", "char", "boolean"}
# The Jack OS classes. A program class with one of these names mixes its own
# subroutines with the OS's (e.g. examples/Array.jack calls the OS's
# Array.new), so qualified calls into it can't be checked.
OS_CLASSES = {"Array", "Keyboard", "Math", "Memory", "Output", "Screen", "String", "Sys"}


def program_classes(file: str) -> Set[str]:
    """
    The classes of the program `file` belongs to: one per .jack file in its
    folder (nand2tetris names each file after its class). Empty if the
    folder can't be read.
    """
    try:
        return {p.stem for p in Path(file).parent.iterdir() if p.suffix.lower() == ".jack" and p.is_file()}
    except OSError:
        return set()


@dataclass
class Declared:
    """Something with a name and a place in the source."""

    name: str
    kind: str  # static | field | argument | local | constructor | function | method
    type: str
    line: int
    column: int
    used: bool = False
    parameter_count: int = 0  # subroutines only


@dataclass
class _Subroutine:
    kind: str  # constructor | function | method
    name: str
    return_type: str
    scope: Dict[str, Declared] = field(default_factory=dict)


def _where(ctx) -> tuple:
    """(line, 1-based column, length) of a parse-tree node or terminal."""
    token = getattr(ctx, "symbol", None) or ctx.start
    return token.line, token.column + 1, max(1, len(token.text or ""))


def _plural(count: int, word: str) -> str:
    return f"{count} {word}{'s' if count != 1 else ''}"


class SemanticChecker:
    """Run with `check(tree)`; returns every Diagnostic found, sorted by position."""

    def __init__(self, file: str, known_classes: Optional[Iterable[str]] = None) -> None:
        self.file = file
        # Class names that exist: the Jack OS, plus the program's own classes
        # (by default, the .jack files next to this one). This class is added
        # once its name is known.
        program = program_classes(file) if known_classes is None else set(known_classes)
        self.known_classes: Set[str] = OS_CLASSES | program
        self.diagnostics: List[Diagnostic] = []
        self.class_name = ""
        self.class_scope: Dict[str, Declared] = {}
        self.subroutines: Dict[str, Declared] = {}
        self.current: Optional[_Subroutine] = None
        self.shares_os_name = False  # True: trust 'ClassName.f()' calls we can't see

    # --- reporting ------------------------------------------------------------
    def _report(self, severity: str, ctx, message: str, help: Optional[str] = None, notes: Iterable[Note] = ()) -> None:
        line, column, length = _where(ctx)
        self.diagnostics.append(
            Diagnostic(self.file, line, column, message, severity, length, help, tuple(notes))
        )

    def error(self, ctx, message: str, **kwargs) -> None:
        self._report(ERROR, ctx, message, **kwargs)

    def warning(self, ctx, message: str, **kwargs) -> None:
        self._report(WARNING, ctx, message, **kwargs)

    @staticmethod
    def _did_you_mean(name: str, candidates: Iterable[str]) -> Optional[str]:
        close = difflib.get_close_matches(name, list(candidates), n=1, cutoff=0.6)
        return f"did you mean '{close[0]}'?" if close else None

    # --- the walk -------------------------------------------------------------
    def check(self, program_ctx) -> List[Diagnostic]:
        cls = program_ctx.classDeclaration()
        self.class_name = cls.className().getText()
        self.known_classes.add(self.class_name)
        stem = Path(self.file).stem
        if stem and stem != self.class_name:
            self.warning(
                cls.className(),
                f"class '{self.class_name}' is in a file named '{Path(self.file).name}'",
                help=f"rename the file to '{self.class_name}.jack': VM tools find classes by file name",
            )

        if self.class_name in OS_CLASSES:
            self.shares_os_name = True
            # Writing the OS (project 12): Sys.init calls Main.main, and Main
            # belongs to whichever program the OS is later used with.
            self.known_classes.add("Main")
            self.warning(
                cls.className(), f"class '{self.class_name}' has the same name as a Jack OS class",
                help=f"its subroutines will clash with the OS's {self.class_name} class; consider another name",
            )  # fmt: skip

        for var_decl in cls.classVarDeclaration():
            kind = "static" if var_decl.STATIC() else "field"
            type_name = self._check_type(var_decl.type_())
            for name_ctx in var_decl.varName():
                self._declare(self.class_scope, name_ctx, kind, type_name, "in this class")

        # Collect every subroutine first, so calls to ones defined further down are fine.
        for sub in cls.subroutineDeclaration():
            name_ctx = sub.subroutineName()
            name = name_ctx.getText()
            line, column, _ = _where(name_ctx)
            kind = sub.getChild(0).getText()
            params = sub.parameterList()
            count = len(params.varName()) if params else 0
            if name in self.subroutines:
                first = self.subroutines[name]
                self.error(
                    name_ctx, f"subroutine '{name}' is already defined in class '{self.class_name}'",
                    notes=[Note(first.line, first.column, f"'{name}' was first defined here", len(name))],
                )  # fmt: skip
                continue
            self.subroutines[name] = Declared(name, kind, self._return_type(sub), line, column, parameter_count=count)

        for sub in cls.subroutineDeclaration():
            self._check_subroutine(sub)

        self.diagnostics.sort(key=Diagnostic.sort_key)
        return self.diagnostics

    def _return_type(self, sub) -> str:
        return "void" if sub.VOID() else sub.type_().getText()

    def _check_type(self, type_ctx) -> str:
        """Warn if a declared type is a class that isn't in the program. Returns the type's name."""
        type_name = type_ctx.getText()
        if type_name not in PRIMITIVE_TYPES:
            self._check_class_name(type_ctx, type_name)
        return type_name

    def _check_class_name(self, ctx, name: str) -> bool:
        """Warn if `name` (used as a class) isn't a known class. Returns True if it's known."""
        if name in self.known_classes:
            return True
        self.warning(ctx, f"there is no class named '{name}' in this program",
                     help=self._did_you_mean(name, self.known_classes)
                     or f"no {name}.jack in this folder, and it isn't a Jack OS class")  # fmt: skip
        return False

    def _declare(self, scope: Dict[str, Declared], name_ctx, kind: str, type_name: str, where: str) -> None:
        name = name_ctx.getText()
        line, column, length = _where(name_ctx)
        if name in scope:
            first = scope[name]
            self.error(
                name_ctx, f"'{name}' is already declared {where}",
                notes=[Note(first.line, first.column, f"'{name}' was first declared here", length)],
            )  # fmt: skip
            return
        scope[name] = Declared(name, kind, type_name, line, column)

    # --- subroutines ------------------------------------------------------------
    def _check_subroutine(self, sub) -> None:
        kind = sub.getChild(0).getText()
        name = sub.subroutineName().getText()
        self.current = _Subroutine(kind, name, self._return_type(sub))
        if not sub.VOID():
            self._check_type(sub.type_())
        scope = self.current.scope

        params = sub.parameterList()
        if params:
            types = params.type_()
            for type_ctx, name_ctx in zip(types, params.varName()):
                self._declare(scope, name_ctx, "argument", self._check_type(type_ctx), "in this subroutine")
        body = sub.subroutineBody()
        for var_decl in body.varDeclaration():
            type_name = self._check_type(var_decl.type_())
            for name_ctx in var_decl.varName():
                self._declare(scope, name_ctx, "local", type_name, "in this subroutine")

        statements = body.statements()
        self._check_statements(statements)

        if not self._always_returns(statements):
            self.error(
                body.RBRACE(), f"{kind} '{name}' can reach its end without a 'return'",
                help="every Jack subroutine must end with 'return' (use 'return;' in a void one)",
            )  # fmt: skip

        for declared in scope.values():
            if not declared.used and declared.kind == "local":
                self.diagnostics.append(
                    Diagnostic(self.file, declared.line, declared.column, f"unused variable '{declared.name}'",
                               WARNING, len(declared.name))
                )  # fmt: skip
        self.current = None

    def _always_returns(self, statements_ctx) -> bool:
        """Does every path through these statements end in a 'return'?"""
        # Any statement that always returns makes the end unreachable - even if
        # (unreachable) statements follow it; those get their own warning.
        return any(self._statement_always_returns(item) for item in statements_ctx.statement())

    def _statement_always_returns(self, statement) -> bool:
        if statement.returnStatement():
            return True
        node = statement.ifStatement()
        if node is not None and node.ELSE():
            then_branch, else_branch = node.statements()
            return self._always_returns(then_branch) and self._always_returns(else_branch)
        return False

    def _check_statements(self, statements_ctx) -> None:
        items = statements_ctx.statement()
        for index, statement in enumerate(items):
            if index > 0 and items[index - 1].returnStatement():
                self.warning(statement, "this code will never run: it comes after 'return'")
            self._check_statement(statement)

    def _check_statement(self, statement) -> None:
        if statement.letStatement():
            let = statement.letStatement()
            self._use_variable(let.varName())
            for expression in let.expression():
                self._check_expression(expression)
        elif statement.ifStatement():
            node = statement.ifStatement()
            self._check_expression(node.expression())
            for block in node.statements():
                self._check_statements(block)
        elif statement.whileStatement():
            node = statement.whileStatement()
            self._check_expression(node.expression())
            self._check_statements(node.statements())
        elif statement.doStatement():
            self._check_call(statement.doStatement().subroutineCall())
        elif statement.returnStatement():
            self._check_return(statement.returnStatement())

    def _check_return(self, node) -> None:
        sub = self.current
        expression = node.expression()
        if expression is not None:
            self._check_expression(expression)
        if sub.kind == "constructor":
            if expression is None or expression.getText() != "this":
                self.warning(node, f"constructor '{sub.name}' should 'return this;'",
                             help="a constructor hands the new object back to its caller")  # fmt: skip
        elif sub.return_type == "void" and expression is not None:
            self.warning(expression, f"void {sub.kind} '{sub.name}' returns a value",
                         help="callers of a void subroutine ignore it; use 'return;'")  # fmt: skip
        elif sub.return_type != "void" and expression is None:
            self.warning(node, f"{sub.kind} '{sub.name}' should return a {sub.return_type}",
                         help="'return;' here gives the caller 0")  # fmt: skip

    # --- expressions ------------------------------------------------------------
    def _check_expression(self, expression) -> None:
        for term in expression.term():
            self._check_term(term)

    def _check_term(self, term) -> None:
        if term.integerConstant():
            value = int(term.integerConstant().getText())
            if value > MAX_INT:
                self.error(term.integerConstant(), f"integer constant {value} is too large",
                           help=f"the largest Jack integer is {MAX_INT}")  # fmt: skip
        elif term.keywordConstant():
            if term.keywordConstant().getText() == "this" and self.current.kind == "function":
                self.error(term.keywordConstant(), f"'this' can't be used in function '{self.current.name}'",
                           help="only methods and constructors have a 'this' object")  # fmt: skip
        elif term.subroutineCall():
            self._check_call(term.subroutineCall())
        elif term.varName():
            self._use_variable(term.varName())
            if term.expression():
                self._check_expression(term.expression())
        elif term.expression():  # ( expression )
            self._check_expression(term.expression())
        elif term.term():  # unary op
            self._check_term(term.term())

    def _lookup(self, name: str) -> Optional[Declared]:
        if self.current and name in self.current.scope:
            return self.current.scope[name]
        return self.class_scope.get(name)

    def _use_variable(self, name_ctx) -> Optional[Declared]:
        name = name_ctx.getText()
        declared = self._lookup(name)
        if declared is None:
            visible = list(self.class_scope) + (list(self.current.scope) if self.current else [])
            self.error(name_ctx, f"'{name}' is not declared",
                       help=self._did_you_mean(name, visible) or "declare it with 'var', 'field' or 'static'")  # fmt: skip
            return None
        declared.used = True
        if declared.kind == "field" and self.current and self.current.kind == "function":
            self.error(name_ctx, f"field '{name}' can't be used in function '{self.current.name}'",
                       help="a function has no object; make it a method, or use a 'static' variable")  # fmt: skip
        return declared

    def _check_call(self, call) -> None:
        arguments = call.expressionList()
        argument_count = len(arguments.expression()) if arguments else 0
        if arguments:
            for expression in arguments.expression():
                self._check_expression(expression)
        name_ctx = call.subroutineName()
        name = name_ctx.getText()

        if not call.DOT():
            # foo(...) is always a method call on 'this' object.
            target = self.subroutines.get(name)
            if target is None:
                self.error(name_ctx, f"class '{self.class_name}' has no subroutine named '{name}'",
                           help=self._did_you_mean(name, self.subroutines)
                           or f"to call another class's function write 'ClassName.{name}(...)'")  # fmt: skip
                return
            if target.kind != "method":
                self.error(name_ctx, f"'{name}' is a {target.kind}, so call it as '{self.class_name}.{name}(...)'",
                           help="a call without a '.' is a method call on this object")  # fmt: skip
            elif self.current.kind == "function":
                self.error(name_ctx, f"can't call method '{name}' from function '{self.current.name}'",
                           help="a function has no object; call it on one, e.g. 'obj.{0}(...)'".format(name))  # fmt: skip
            self._check_argument_count(name_ctx, target, argument_count)
            return

        receiver_ctx = call.getChild(0)
        receiver = receiver_ctx.getText()
        variable = self._lookup(receiver)
        if variable is not None:
            self._use_variable(receiver_ctx)
            if variable.type in PRIMITIVE_TYPES:
                self.error(receiver_ctx, f"'{receiver}' is a {variable.type}, which has no methods",
                           help=f"'{receiver}.{name}(...)' needs '{receiver}' to be an object")  # fmt: skip
            elif variable.type == self.class_name:
                target = self.subroutines.get(name)
                if target is None:
                    self._no_such_subroutine(name_ctx, name)
                elif target.kind == "method":
                    self._check_argument_count(name_ctx, target, argument_count)
            return

        # ClassName.subroutine(...)
        if receiver == self.class_name:
            target = self.subroutines.get(name)
            if target is None:
                self._no_such_subroutine(name_ctx, name)
            elif target.kind == "method":
                self.error(name_ctx, f"'{name}' is a method, so it needs an object",
                           help=f"call it on an object of class {self.class_name}, not on the class")  # fmt: skip
            else:
                self._check_argument_count(name_ctx, target, argument_count)
        elif receiver in self.known_classes:
            pass  # another class of the program, or the OS: compiled separately, so trusted
        elif receiver[:1].islower():
            visible = list(self.class_scope) + (list(self.current.scope) if self.current else [])
            self.warning(receiver_ctx, f"'{receiver}' is not a variable, so this calls a class named '{receiver}'",
                         help=self._did_you_mean(receiver, [*visible, *self.known_classes])
                         or "class names usually start with a capital letter")  # fmt: skip
        else:
            self._check_class_name(receiver_ctx, receiver)

    def _no_such_subroutine(self, name_ctx, name: str) -> None:
        if self.shares_os_name:
            return  # probably the OS class's subroutine, e.g. Array.new
        self.error(name_ctx, f"class '{self.class_name}' has no subroutine named '{name}'",
                   help=self._did_you_mean(name, self.subroutines))  # fmt: skip

    def _check_argument_count(self, name_ctx, target: Declared, given: int) -> None:
        if given != target.parameter_count:
            self.error(
                name_ctx,
                f"'{target.name}' takes {_plural(target.parameter_count, 'argument')} but {given} {'was' if given == 1 else 'were'} given",
                notes=[Note(target.line, target.column, f"'{target.name}' is declared here", len(target.name))],
            )


def check(tree, file: str, known_classes: Optional[Iterable[str]] = None) -> List[Diagnostic]:
    """
    Run every semantic check on a parsed program. `known_classes` are the
    program's classes; by default, the .jack files in `file`'s folder.
    """
    return SemanticChecker(file, known_classes).check(tree)
