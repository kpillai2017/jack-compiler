# Generated from grammar/Jack.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .JackParser import JackParser
else:
    from JackParser import JackParser

# This class defines a complete generic visitor for a parse tree produced by JackParser.

class JackVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JackParser#program.
    def visitProgram(self, ctx:JackParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#classDeclaration.
    def visitClassDeclaration(self, ctx:JackParser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#classVarDeclaration.
    def visitClassVarDeclaration(self, ctx:JackParser.ClassVarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#type.
    def visitType(self, ctx:JackParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#subroutineDeclaration.
    def visitSubroutineDeclaration(self, ctx:JackParser.SubroutineDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#parameterList.
    def visitParameterList(self, ctx:JackParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#subroutineBody.
    def visitSubroutineBody(self, ctx:JackParser.SubroutineBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#varDeclaration.
    def visitVarDeclaration(self, ctx:JackParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#localVariable.
    def visitLocalVariable(self, ctx:JackParser.LocalVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#constDeclaration.
    def visitConstDeclaration(self, ctx:JackParser.ConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#constEntry.
    def visitConstEntry(self, ctx:JackParser.ConstEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#enumDeclaration.
    def visitEnumDeclaration(self, ctx:JackParser.EnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#enumMember.
    def visitEnumMember(self, ctx:JackParser.EnumMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#qualifiedConstant.
    def visitQualifiedConstant(self, ctx:JackParser.QualifiedConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#statements.
    def visitStatements(self, ctx:JackParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#statement.
    def visitStatement(self, ctx:JackParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#letStatement.
    def visitLetStatement(self, ctx:JackParser.LetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:JackParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#ifStatement.
    def visitIfStatement(self, ctx:JackParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#whileStatement.
    def visitWhileStatement(self, ctx:JackParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#forStatement.
    def visitForStatement(self, ctx:JackParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#forAssignment.
    def visitForAssignment(self, ctx:JackParser.ForAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#breakStatement.
    def visitBreakStatement(self, ctx:JackParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#continueStatement.
    def visitContinueStatement(self, ctx:JackParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#doStatement.
    def visitDoStatement(self, ctx:JackParser.DoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#returnStatement.
    def visitReturnStatement(self, ctx:JackParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#expression.
    def visitExpression(self, ctx:JackParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#term.
    def visitTerm(self, ctx:JackParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#subroutineCall.
    def visitSubroutineCall(self, ctx:JackParser.SubroutineCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#expressionList.
    def visitExpressionList(self, ctx:JackParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#op.
    def visitOp(self, ctx:JackParser.OpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#unaryOp.
    def visitUnaryOp(self, ctx:JackParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#keywordConstant.
    def visitKeywordConstant(self, ctx:JackParser.KeywordConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#className.
    def visitClassName(self, ctx:JackParser.ClassNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#subroutineName.
    def visitSubroutineName(self, ctx:JackParser.SubroutineNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#varName.
    def visitVarName(self, ctx:JackParser.VarNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#integerConstant.
    def visitIntegerConstant(self, ctx:JackParser.IntegerConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#stringConstant.
    def visitStringConstant(self, ctx:JackParser.StringConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JackParser#characterConstant.
    def visitCharacterConstant(self, ctx:JackParser.CharacterConstantContext):
        return self.visitChildren(ctx)



del JackParser