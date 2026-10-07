# Generated from grammar/Jack.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .JackParser import JackParser
else:
    from JackParser import JackParser

# This class defines a complete listener for a parse tree produced by JackParser.
class JackListener(ParseTreeListener):

    # Enter a parse tree produced by JackParser#program.
    def enterProgram(self, ctx:JackParser.ProgramContext):
        pass

    # Exit a parse tree produced by JackParser#program.
    def exitProgram(self, ctx:JackParser.ProgramContext):
        pass


    # Enter a parse tree produced by JackParser#classDeclaration.
    def enterClassDeclaration(self, ctx:JackParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by JackParser#classDeclaration.
    def exitClassDeclaration(self, ctx:JackParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by JackParser#classVarDeclaration.
    def enterClassVarDeclaration(self, ctx:JackParser.ClassVarDeclarationContext):
        pass

    # Exit a parse tree produced by JackParser#classVarDeclaration.
    def exitClassVarDeclaration(self, ctx:JackParser.ClassVarDeclarationContext):
        pass


    # Enter a parse tree produced by JackParser#type.
    def enterType(self, ctx:JackParser.TypeContext):
        pass

    # Exit a parse tree produced by JackParser#type.
    def exitType(self, ctx:JackParser.TypeContext):
        pass


    # Enter a parse tree produced by JackParser#subroutineDeclaration.
    def enterSubroutineDeclaration(self, ctx:JackParser.SubroutineDeclarationContext):
        pass

    # Exit a parse tree produced by JackParser#subroutineDeclaration.
    def exitSubroutineDeclaration(self, ctx:JackParser.SubroutineDeclarationContext):
        pass


    # Enter a parse tree produced by JackParser#parameterList.
    def enterParameterList(self, ctx:JackParser.ParameterListContext):
        pass

    # Exit a parse tree produced by JackParser#parameterList.
    def exitParameterList(self, ctx:JackParser.ParameterListContext):
        pass


    # Enter a parse tree produced by JackParser#subroutineBody.
    def enterSubroutineBody(self, ctx:JackParser.SubroutineBodyContext):
        pass

    # Exit a parse tree produced by JackParser#subroutineBody.
    def exitSubroutineBody(self, ctx:JackParser.SubroutineBodyContext):
        pass


    # Enter a parse tree produced by JackParser#varDeclaration.
    def enterVarDeclaration(self, ctx:JackParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by JackParser#varDeclaration.
    def exitVarDeclaration(self, ctx:JackParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by JackParser#statements.
    def enterStatements(self, ctx:JackParser.StatementsContext):
        pass

    # Exit a parse tree produced by JackParser#statements.
    def exitStatements(self, ctx:JackParser.StatementsContext):
        pass


    # Enter a parse tree produced by JackParser#statement.
    def enterStatement(self, ctx:JackParser.StatementContext):
        pass

    # Exit a parse tree produced by JackParser#statement.
    def exitStatement(self, ctx:JackParser.StatementContext):
        pass


    # Enter a parse tree produced by JackParser#letStatement.
    def enterLetStatement(self, ctx:JackParser.LetStatementContext):
        pass

    # Exit a parse tree produced by JackParser#letStatement.
    def exitLetStatement(self, ctx:JackParser.LetStatementContext):
        pass


    # Enter a parse tree produced by JackParser#ifStatement.
    def enterIfStatement(self, ctx:JackParser.IfStatementContext):
        pass

    # Exit a parse tree produced by JackParser#ifStatement.
    def exitIfStatement(self, ctx:JackParser.IfStatementContext):
        pass


    # Enter a parse tree produced by JackParser#whileStatement.
    def enterWhileStatement(self, ctx:JackParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by JackParser#whileStatement.
    def exitWhileStatement(self, ctx:JackParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by JackParser#doStatement.
    def enterDoStatement(self, ctx:JackParser.DoStatementContext):
        pass

    # Exit a parse tree produced by JackParser#doStatement.
    def exitDoStatement(self, ctx:JackParser.DoStatementContext):
        pass


    # Enter a parse tree produced by JackParser#returnStatement.
    def enterReturnStatement(self, ctx:JackParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by JackParser#returnStatement.
    def exitReturnStatement(self, ctx:JackParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by JackParser#expression.
    def enterExpression(self, ctx:JackParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JackParser#expression.
    def exitExpression(self, ctx:JackParser.ExpressionContext):
        pass


    # Enter a parse tree produced by JackParser#term.
    def enterTerm(self, ctx:JackParser.TermContext):
        pass

    # Exit a parse tree produced by JackParser#term.
    def exitTerm(self, ctx:JackParser.TermContext):
        pass


    # Enter a parse tree produced by JackParser#subroutineCall.
    def enterSubroutineCall(self, ctx:JackParser.SubroutineCallContext):
        pass

    # Exit a parse tree produced by JackParser#subroutineCall.
    def exitSubroutineCall(self, ctx:JackParser.SubroutineCallContext):
        pass


    # Enter a parse tree produced by JackParser#expressionList.
    def enterExpressionList(self, ctx:JackParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by JackParser#expressionList.
    def exitExpressionList(self, ctx:JackParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by JackParser#op.
    def enterOp(self, ctx:JackParser.OpContext):
        pass

    # Exit a parse tree produced by JackParser#op.
    def exitOp(self, ctx:JackParser.OpContext):
        pass


    # Enter a parse tree produced by JackParser#unaryOp.
    def enterUnaryOp(self, ctx:JackParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by JackParser#unaryOp.
    def exitUnaryOp(self, ctx:JackParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by JackParser#keywordConstant.
    def enterKeywordConstant(self, ctx:JackParser.KeywordConstantContext):
        pass

    # Exit a parse tree produced by JackParser#keywordConstant.
    def exitKeywordConstant(self, ctx:JackParser.KeywordConstantContext):
        pass


    # Enter a parse tree produced by JackParser#className.
    def enterClassName(self, ctx:JackParser.ClassNameContext):
        pass

    # Exit a parse tree produced by JackParser#className.
    def exitClassName(self, ctx:JackParser.ClassNameContext):
        pass


    # Enter a parse tree produced by JackParser#subroutineName.
    def enterSubroutineName(self, ctx:JackParser.SubroutineNameContext):
        pass

    # Exit a parse tree produced by JackParser#subroutineName.
    def exitSubroutineName(self, ctx:JackParser.SubroutineNameContext):
        pass


    # Enter a parse tree produced by JackParser#varName.
    def enterVarName(self, ctx:JackParser.VarNameContext):
        pass

    # Exit a parse tree produced by JackParser#varName.
    def exitVarName(self, ctx:JackParser.VarNameContext):
        pass


    # Enter a parse tree produced by JackParser#integerConstant.
    def enterIntegerConstant(self, ctx:JackParser.IntegerConstantContext):
        pass

    # Exit a parse tree produced by JackParser#integerConstant.
    def exitIntegerConstant(self, ctx:JackParser.IntegerConstantContext):
        pass


    # Enter a parse tree produced by JackParser#stringConstant.
    def enterStringConstant(self, ctx:JackParser.StringConstantContext):
        pass

    # Exit a parse tree produced by JackParser#stringConstant.
    def exitStringConstant(self, ctx:JackParser.StringConstantContext):
        pass



del JackParser