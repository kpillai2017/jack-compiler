# Generated from grammar/Jack.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,47,270,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        1,0,1,0,1,0,1,1,1,1,1,1,1,1,5,1,62,8,1,10,1,12,1,65,9,1,1,1,5,1,
        68,8,1,10,1,12,1,71,9,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,5,2,80,8,2,10,
        2,12,2,83,9,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,3,3,92,8,3,1,4,1,4,1,4,
        3,4,97,8,4,1,4,1,4,1,4,3,4,102,8,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,
        5,1,5,5,5,113,8,5,10,5,12,5,116,9,5,1,6,1,6,5,6,120,8,6,10,6,12,
        6,123,9,6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,5,7,133,8,7,10,7,12,7,
        136,9,7,1,7,1,7,1,8,5,8,141,8,8,10,8,12,8,144,9,8,1,9,1,9,1,9,1,
        9,1,9,3,9,151,8,9,1,10,1,10,1,10,1,10,1,10,1,10,3,10,159,8,10,1,
        10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,
        11,1,11,1,11,3,11,177,8,11,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,
        12,1,13,1,13,1,13,1,13,1,14,1,14,3,14,193,8,14,1,14,1,14,1,15,1,
        15,1,15,1,15,5,15,201,8,15,10,15,12,15,204,9,15,1,16,1,16,1,16,1,
        16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,
        16,3,16,223,8,16,1,17,1,17,1,17,3,17,228,8,17,1,17,1,17,1,17,1,17,
        3,17,234,8,17,1,17,1,17,1,17,1,17,3,17,240,8,17,1,17,1,17,3,17,244,
        8,17,1,18,1,18,1,18,5,18,249,8,18,10,18,12,18,252,9,18,1,19,1,19,
        1,20,1,20,1,21,1,21,1,22,1,22,1,23,1,23,1,24,1,24,1,25,1,25,1,26,
        1,26,1,26,0,0,27,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,
        36,38,40,42,44,46,48,50,52,0,5,1,0,5,6,1,0,2,4,2,0,23,28,30,32,2,
        0,24,24,29,29,1,0,13,16,275,0,54,1,0,0,0,2,57,1,0,0,0,4,74,1,0,0,
        0,6,91,1,0,0,0,8,93,1,0,0,0,10,106,1,0,0,0,12,117,1,0,0,0,14,127,
        1,0,0,0,16,142,1,0,0,0,18,150,1,0,0,0,20,152,1,0,0,0,22,164,1,0,
        0,0,24,178,1,0,0,0,26,186,1,0,0,0,28,190,1,0,0,0,30,196,1,0,0,0,
        32,222,1,0,0,0,34,243,1,0,0,0,36,245,1,0,0,0,38,253,1,0,0,0,40,255,
        1,0,0,0,42,257,1,0,0,0,44,259,1,0,0,0,46,261,1,0,0,0,48,263,1,0,
        0,0,50,265,1,0,0,0,52,267,1,0,0,0,54,55,3,2,1,0,55,56,5,0,0,1,56,
        1,1,0,0,0,57,58,5,1,0,0,58,59,3,44,22,0,59,63,5,40,0,0,60,62,3,4,
        2,0,61,60,1,0,0,0,62,65,1,0,0,0,63,61,1,0,0,0,63,64,1,0,0,0,64,69,
        1,0,0,0,65,63,1,0,0,0,66,68,3,8,4,0,67,66,1,0,0,0,68,71,1,0,0,0,
        69,67,1,0,0,0,69,70,1,0,0,0,70,72,1,0,0,0,71,69,1,0,0,0,72,73,5,
        41,0,0,73,3,1,0,0,0,74,75,7,0,0,0,75,76,3,6,3,0,76,81,3,48,24,0,
        77,78,5,34,0,0,78,80,3,48,24,0,79,77,1,0,0,0,80,83,1,0,0,0,81,79,
        1,0,0,0,81,82,1,0,0,0,82,84,1,0,0,0,83,81,1,0,0,0,84,85,5,35,0,0,
        85,5,1,0,0,0,86,92,5,8,0,0,87,92,5,9,0,0,88,92,5,10,0,0,89,92,5,
        11,0,0,90,92,3,44,22,0,91,86,1,0,0,0,91,87,1,0,0,0,91,88,1,0,0,0,
        91,89,1,0,0,0,91,90,1,0,0,0,92,7,1,0,0,0,93,96,7,1,0,0,94,97,5,12,
        0,0,95,97,3,6,3,0,96,94,1,0,0,0,96,95,1,0,0,0,97,98,1,0,0,0,98,99,
        3,46,23,0,99,101,5,36,0,0,100,102,3,10,5,0,101,100,1,0,0,0,101,102,
        1,0,0,0,102,103,1,0,0,0,103,104,5,37,0,0,104,105,3,12,6,0,105,9,
        1,0,0,0,106,107,3,6,3,0,107,114,3,48,24,0,108,109,5,34,0,0,109,110,
        3,6,3,0,110,111,3,48,24,0,111,113,1,0,0,0,112,108,1,0,0,0,113,116,
        1,0,0,0,114,112,1,0,0,0,114,115,1,0,0,0,115,11,1,0,0,0,116,114,1,
        0,0,0,117,121,5,40,0,0,118,120,3,14,7,0,119,118,1,0,0,0,120,123,
        1,0,0,0,121,119,1,0,0,0,121,122,1,0,0,0,122,124,1,0,0,0,123,121,
        1,0,0,0,124,125,3,16,8,0,125,126,5,41,0,0,126,13,1,0,0,0,127,128,
        5,7,0,0,128,129,3,6,3,0,129,134,3,48,24,0,130,131,5,34,0,0,131,133,
        3,48,24,0,132,130,1,0,0,0,133,136,1,0,0,0,134,132,1,0,0,0,134,135,
        1,0,0,0,135,137,1,0,0,0,136,134,1,0,0,0,137,138,5,35,0,0,138,15,
        1,0,0,0,139,141,3,18,9,0,140,139,1,0,0,0,141,144,1,0,0,0,142,140,
        1,0,0,0,142,143,1,0,0,0,143,17,1,0,0,0,144,142,1,0,0,0,145,151,3,
        20,10,0,146,151,3,22,11,0,147,151,3,24,12,0,148,151,3,26,13,0,149,
        151,3,28,14,0,150,145,1,0,0,0,150,146,1,0,0,0,150,147,1,0,0,0,150,
        148,1,0,0,0,150,149,1,0,0,0,151,19,1,0,0,0,152,153,5,17,0,0,153,
        158,3,48,24,0,154,155,5,38,0,0,155,156,3,30,15,0,156,157,5,39,0,
        0,157,159,1,0,0,0,158,154,1,0,0,0,158,159,1,0,0,0,159,160,1,0,0,
        0,160,161,5,32,0,0,161,162,3,30,15,0,162,163,5,35,0,0,163,21,1,0,
        0,0,164,165,5,19,0,0,165,166,5,36,0,0,166,167,3,30,15,0,167,168,
        5,37,0,0,168,169,5,40,0,0,169,170,3,16,8,0,170,176,5,41,0,0,171,
        172,5,20,0,0,172,173,5,40,0,0,173,174,3,16,8,0,174,175,5,41,0,0,
        175,177,1,0,0,0,176,171,1,0,0,0,176,177,1,0,0,0,177,23,1,0,0,0,178,
        179,5,21,0,0,179,180,5,36,0,0,180,181,3,30,15,0,181,182,5,37,0,0,
        182,183,5,40,0,0,183,184,3,16,8,0,184,185,5,41,0,0,185,25,1,0,0,
        0,186,187,5,18,0,0,187,188,3,34,17,0,188,189,5,35,0,0,189,27,1,0,
        0,0,190,192,5,22,0,0,191,193,3,30,15,0,192,191,1,0,0,0,192,193,1,
        0,0,0,193,194,1,0,0,0,194,195,5,35,0,0,195,29,1,0,0,0,196,202,3,
        32,16,0,197,198,3,38,19,0,198,199,3,32,16,0,199,201,1,0,0,0,200,
        197,1,0,0,0,201,204,1,0,0,0,202,200,1,0,0,0,202,203,1,0,0,0,203,
        31,1,0,0,0,204,202,1,0,0,0,205,223,3,50,25,0,206,223,3,52,26,0,207,
        223,3,42,21,0,208,223,3,48,24,0,209,210,3,48,24,0,210,211,5,38,0,
        0,211,212,3,30,15,0,212,213,5,39,0,0,213,223,1,0,0,0,214,223,3,34,
        17,0,215,216,5,36,0,0,216,217,3,30,15,0,217,218,5,37,0,0,218,223,
        1,0,0,0,219,220,3,40,20,0,220,221,3,32,16,0,221,223,1,0,0,0,222,
        205,1,0,0,0,222,206,1,0,0,0,222,207,1,0,0,0,222,208,1,0,0,0,222,
        209,1,0,0,0,222,214,1,0,0,0,222,215,1,0,0,0,222,219,1,0,0,0,223,
        33,1,0,0,0,224,225,3,46,23,0,225,227,5,36,0,0,226,228,3,36,18,0,
        227,226,1,0,0,0,227,228,1,0,0,0,228,229,1,0,0,0,229,230,5,37,0,0,
        230,244,1,0,0,0,231,234,3,44,22,0,232,234,3,48,24,0,233,231,1,0,
        0,0,233,232,1,0,0,0,234,235,1,0,0,0,235,236,5,33,0,0,236,237,3,46,
        23,0,237,239,5,36,0,0,238,240,3,36,18,0,239,238,1,0,0,0,239,240,
        1,0,0,0,240,241,1,0,0,0,241,242,5,37,0,0,242,244,1,0,0,0,243,224,
        1,0,0,0,243,233,1,0,0,0,244,35,1,0,0,0,245,250,3,30,15,0,246,247,
        5,34,0,0,247,249,3,30,15,0,248,246,1,0,0,0,249,252,1,0,0,0,250,248,
        1,0,0,0,250,251,1,0,0,0,251,37,1,0,0,0,252,250,1,0,0,0,253,254,7,
        2,0,0,254,39,1,0,0,0,255,256,7,3,0,0,256,41,1,0,0,0,257,258,7,4,
        0,0,258,43,1,0,0,0,259,260,5,44,0,0,260,45,1,0,0,0,261,262,5,44,
        0,0,262,47,1,0,0,0,263,264,5,44,0,0,264,49,1,0,0,0,265,266,5,42,
        0,0,266,51,1,0,0,0,267,268,5,43,0,0,268,53,1,0,0,0,21,63,69,81,91,
        96,101,114,121,134,142,150,158,176,192,202,222,227,233,239,243,250
    ]

class JackParser ( Parser ):

    grammarFileName = "Jack.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'class'", "'constructor'", "'function'", 
                     "'method'", "'field'", "'static'", "'var'", "'int'", 
                     "'boolean'", "'char'", "'String'", "'void'", "'true'", 
                     "'false'", "'null'", "'this'", "'let'", "'do'", "'if'", 
                     "'else'", "'while'", "'return'", "'+'", "'-'", "'*'", 
                     "'/'", "'&'", "'|'", "'~'", "'<'", "'>'", "'='", "'.'", 
                     "','", "';'", "'('", "')'", "'['", "']'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>", "CLASS", "CONSTRUCTOR", "FUNCTION", "METHOD", 
                      "FIELD", "STATIC", "VAR", "INT", "BOOLEAN", "CHAR", 
                      "STRING", "VOID", "TRUE", "FALSE", "NULL", "THIS", 
                      "LET", "DO", "IF", "ELSE", "WHILE", "RETURN", "PLUS", 
                      "MINUS", "MUL", "DIV", "AND", "OR", "NOT", "LT", "GT", 
                      "EQUAL", "DOT", "COMMA", "SEMICOLON", "LPAREN", "RPAREN", 
                      "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", "INTEGER", 
                      "STRING_LITERAL", "IDENTIFIER", "WS", "LINE_COMMENT", 
                      "BLOCK_COMMENT" ]

    RULE_program = 0
    RULE_classDeclaration = 1
    RULE_classVarDeclaration = 2
    RULE_type = 3
    RULE_subroutineDeclaration = 4
    RULE_parameterList = 5
    RULE_subroutineBody = 6
    RULE_varDeclaration = 7
    RULE_statements = 8
    RULE_statement = 9
    RULE_letStatement = 10
    RULE_ifStatement = 11
    RULE_whileStatement = 12
    RULE_doStatement = 13
    RULE_returnStatement = 14
    RULE_expression = 15
    RULE_term = 16
    RULE_subroutineCall = 17
    RULE_expressionList = 18
    RULE_op = 19
    RULE_unaryOp = 20
    RULE_keywordConstant = 21
    RULE_className = 22
    RULE_subroutineName = 23
    RULE_varName = 24
    RULE_integerConstant = 25
    RULE_stringConstant = 26

    ruleNames =  [ "program", "classDeclaration", "classVarDeclaration", 
                   "type", "subroutineDeclaration", "parameterList", "subroutineBody", 
                   "varDeclaration", "statements", "statement", "letStatement", 
                   "ifStatement", "whileStatement", "doStatement", "returnStatement", 
                   "expression", "term", "subroutineCall", "expressionList", 
                   "op", "unaryOp", "keywordConstant", "className", "subroutineName", 
                   "varName", "integerConstant", "stringConstant" ]

    EOF = Token.EOF
    CLASS=1
    CONSTRUCTOR=2
    FUNCTION=3
    METHOD=4
    FIELD=5
    STATIC=6
    VAR=7
    INT=8
    BOOLEAN=9
    CHAR=10
    STRING=11
    VOID=12
    TRUE=13
    FALSE=14
    NULL=15
    THIS=16
    LET=17
    DO=18
    IF=19
    ELSE=20
    WHILE=21
    RETURN=22
    PLUS=23
    MINUS=24
    MUL=25
    DIV=26
    AND=27
    OR=28
    NOT=29
    LT=30
    GT=31
    EQUAL=32
    DOT=33
    COMMA=34
    SEMICOLON=35
    LPAREN=36
    RPAREN=37
    LBRACKET=38
    RBRACKET=39
    LBRACE=40
    RBRACE=41
    INTEGER=42
    STRING_LITERAL=43
    IDENTIFIER=44
    WS=45
    LINE_COMMENT=46
    BLOCK_COMMENT=47

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classDeclaration(self):
            return self.getTypedRuleContext(JackParser.ClassDeclarationContext,0)


        def EOF(self):
            return self.getToken(JackParser.EOF, 0)

        def getRuleIndex(self):
            return JackParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = JackParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.classDeclaration()
            self.state = 55
            self.match(JackParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CLASS(self):
            return self.getToken(JackParser.CLASS, 0)

        def className(self):
            return self.getTypedRuleContext(JackParser.ClassNameContext,0)


        def LBRACE(self):
            return self.getToken(JackParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(JackParser.RBRACE, 0)

        def classVarDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.ClassVarDeclarationContext)
            else:
                return self.getTypedRuleContext(JackParser.ClassVarDeclarationContext,i)


        def subroutineDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.SubroutineDeclarationContext)
            else:
                return self.getTypedRuleContext(JackParser.SubroutineDeclarationContext,i)


        def getRuleIndex(self):
            return JackParser.RULE_classDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassDeclaration" ):
                listener.enterClassDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassDeclaration" ):
                listener.exitClassDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassDeclaration" ):
                return visitor.visitClassDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def classDeclaration(self):

        localctx = JackParser.ClassDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_classDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.match(JackParser.CLASS)
            self.state = 58
            self.className()
            self.state = 59
            self.match(JackParser.LBRACE)
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5 or _la==6:
                self.state = 60
                self.classVarDeclaration()
                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 69
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 28) != 0):
                self.state = 66
                self.subroutineDeclaration()
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 72
            self.match(JackParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassVarDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(JackParser.TypeContext,0)


        def varName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.VarNameContext)
            else:
                return self.getTypedRuleContext(JackParser.VarNameContext,i)


        def SEMICOLON(self):
            return self.getToken(JackParser.SEMICOLON, 0)

        def STATIC(self):
            return self.getToken(JackParser.STATIC, 0)

        def FIELD(self):
            return self.getToken(JackParser.FIELD, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JackParser.COMMA)
            else:
                return self.getToken(JackParser.COMMA, i)

        def getRuleIndex(self):
            return JackParser.RULE_classVarDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassVarDeclaration" ):
                listener.enterClassVarDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassVarDeclaration" ):
                listener.exitClassVarDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassVarDeclaration" ):
                return visitor.visitClassVarDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def classVarDeclaration(self):

        localctx = JackParser.ClassVarDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_classVarDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            _la = self._input.LA(1)
            if not(_la==5 or _la==6):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 75
            self.type_()
            self.state = 76
            self.varName()
            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 77
                self.match(JackParser.COMMA)
                self.state = 78
                self.varName()
                self.state = 83
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 84
            self.match(JackParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(JackParser.INT, 0)

        def BOOLEAN(self):
            return self.getToken(JackParser.BOOLEAN, 0)

        def CHAR(self):
            return self.getToken(JackParser.CHAR, 0)

        def STRING(self):
            return self.getToken(JackParser.STRING, 0)

        def className(self):
            return self.getTypedRuleContext(JackParser.ClassNameContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)




    def type_(self):

        localctx = JackParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_type)
        try:
            self.state = 91
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 86
                self.match(JackParser.INT)
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.match(JackParser.BOOLEAN)
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 3)
                self.state = 88
                self.match(JackParser.CHAR)
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 4)
                self.state = 89
                self.match(JackParser.STRING)
                pass
            elif token in [44]:
                self.enterOuterAlt(localctx, 5)
                self.state = 90
                self.className()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubroutineDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subroutineName(self):
            return self.getTypedRuleContext(JackParser.SubroutineNameContext,0)


        def LPAREN(self):
            return self.getToken(JackParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(JackParser.RPAREN, 0)

        def subroutineBody(self):
            return self.getTypedRuleContext(JackParser.SubroutineBodyContext,0)


        def CONSTRUCTOR(self):
            return self.getToken(JackParser.CONSTRUCTOR, 0)

        def FUNCTION(self):
            return self.getToken(JackParser.FUNCTION, 0)

        def METHOD(self):
            return self.getToken(JackParser.METHOD, 0)

        def VOID(self):
            return self.getToken(JackParser.VOID, 0)

        def type_(self):
            return self.getTypedRuleContext(JackParser.TypeContext,0)


        def parameterList(self):
            return self.getTypedRuleContext(JackParser.ParameterListContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_subroutineDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubroutineDeclaration" ):
                listener.enterSubroutineDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubroutineDeclaration" ):
                listener.exitSubroutineDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubroutineDeclaration" ):
                return visitor.visitSubroutineDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def subroutineDeclaration(self):

        localctx = JackParser.SubroutineDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_subroutineDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 28) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 96
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [12]:
                self.state = 94
                self.match(JackParser.VOID)
                pass
            elif token in [8, 9, 10, 11, 44]:
                self.state = 95
                self.type_()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 98
            self.subroutineName()
            self.state = 99
            self.match(JackParser.LPAREN)
            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17592186048256) != 0):
                self.state = 100
                self.parameterList()


            self.state = 103
            self.match(JackParser.RPAREN)
            self.state = 104
            self.subroutineBody()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.TypeContext)
            else:
                return self.getTypedRuleContext(JackParser.TypeContext,i)


        def varName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.VarNameContext)
            else:
                return self.getTypedRuleContext(JackParser.VarNameContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JackParser.COMMA)
            else:
                return self.getToken(JackParser.COMMA, i)

        def getRuleIndex(self):
            return JackParser.RULE_parameterList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterList" ):
                listener.enterParameterList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterList" ):
                listener.exitParameterList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameterList" ):
                return visitor.visitParameterList(self)
            else:
                return visitor.visitChildren(self)




    def parameterList(self):

        localctx = JackParser.ParameterListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_parameterList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 106
            self.type_()
            self.state = 107
            self.varName()
            self.state = 114
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 108
                self.match(JackParser.COMMA)
                self.state = 109
                self.type_()
                self.state = 110
                self.varName()
                self.state = 116
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubroutineBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(JackParser.LBRACE, 0)

        def statements(self):
            return self.getTypedRuleContext(JackParser.StatementsContext,0)


        def RBRACE(self):
            return self.getToken(JackParser.RBRACE, 0)

        def varDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.VarDeclarationContext)
            else:
                return self.getTypedRuleContext(JackParser.VarDeclarationContext,i)


        def getRuleIndex(self):
            return JackParser.RULE_subroutineBody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubroutineBody" ):
                listener.enterSubroutineBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubroutineBody" ):
                listener.exitSubroutineBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubroutineBody" ):
                return visitor.visitSubroutineBody(self)
            else:
                return visitor.visitChildren(self)




    def subroutineBody(self):

        localctx = JackParser.SubroutineBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_subroutineBody)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            self.match(JackParser.LBRACE)
            self.state = 121
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==7:
                self.state = 118
                self.varDeclaration()
                self.state = 123
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 124
            self.statements()
            self.state = 125
            self.match(JackParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(JackParser.VAR, 0)

        def type_(self):
            return self.getTypedRuleContext(JackParser.TypeContext,0)


        def varName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.VarNameContext)
            else:
                return self.getTypedRuleContext(JackParser.VarNameContext,i)


        def SEMICOLON(self):
            return self.getToken(JackParser.SEMICOLON, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JackParser.COMMA)
            else:
                return self.getToken(JackParser.COMMA, i)

        def getRuleIndex(self):
            return JackParser.RULE_varDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDeclaration" ):
                listener.enterVarDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDeclaration" ):
                listener.exitVarDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDeclaration" ):
                return visitor.visitVarDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def varDeclaration(self):

        localctx = JackParser.VarDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_varDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.match(JackParser.VAR)
            self.state = 128
            self.type_()
            self.state = 129
            self.varName()
            self.state = 134
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 130
                self.match(JackParser.COMMA)
                self.state = 131
                self.varName()
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 137
            self.match(JackParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.StatementContext)
            else:
                return self.getTypedRuleContext(JackParser.StatementContext,i)


        def getRuleIndex(self):
            return JackParser.RULE_statements

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatements" ):
                listener.enterStatements(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatements" ):
                listener.exitStatements(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatements" ):
                return visitor.visitStatements(self)
            else:
                return visitor.visitChildren(self)




    def statements(self):

        localctx = JackParser.StatementsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_statements)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 7208960) != 0):
                self.state = 139
                self.statement()
                self.state = 144
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def letStatement(self):
            return self.getTypedRuleContext(JackParser.LetStatementContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(JackParser.IfStatementContext,0)


        def whileStatement(self):
            return self.getTypedRuleContext(JackParser.WhileStatementContext,0)


        def doStatement(self):
            return self.getTypedRuleContext(JackParser.DoStatementContext,0)


        def returnStatement(self):
            return self.getTypedRuleContext(JackParser.ReturnStatementContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = JackParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_statement)
        try:
            self.state = 150
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 145
                self.letStatement()
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 2)
                self.state = 146
                self.ifStatement()
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 3)
                self.state = 147
                self.whileStatement()
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 4)
                self.state = 148
                self.doStatement()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 5)
                self.state = 149
                self.returnStatement()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LetStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LET(self):
            return self.getToken(JackParser.LET, 0)

        def varName(self):
            return self.getTypedRuleContext(JackParser.VarNameContext,0)


        def EQUAL(self):
            return self.getToken(JackParser.EQUAL, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(JackParser.ExpressionContext,i)


        def SEMICOLON(self):
            return self.getToken(JackParser.SEMICOLON, 0)

        def LBRACKET(self):
            return self.getToken(JackParser.LBRACKET, 0)

        def RBRACKET(self):
            return self.getToken(JackParser.RBRACKET, 0)

        def getRuleIndex(self):
            return JackParser.RULE_letStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetStatement" ):
                listener.enterLetStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetStatement" ):
                listener.exitLetStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetStatement" ):
                return visitor.visitLetStatement(self)
            else:
                return visitor.visitChildren(self)




    def letStatement(self):

        localctx = JackParser.LetStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_letStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self.match(JackParser.LET)
            self.state = 153
            self.varName()
            self.state = 158
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==38:
                self.state = 154
                self.match(JackParser.LBRACKET)
                self.state = 155
                self.expression()
                self.state = 156
                self.match(JackParser.RBRACKET)


            self.state = 160
            self.match(JackParser.EQUAL)
            self.state = 161
            self.expression()
            self.state = 162
            self.match(JackParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(JackParser.IF, 0)

        def LPAREN(self):
            return self.getToken(JackParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(JackParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(JackParser.RPAREN, 0)

        def LBRACE(self, i:int=None):
            if i is None:
                return self.getTokens(JackParser.LBRACE)
            else:
                return self.getToken(JackParser.LBRACE, i)

        def statements(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.StatementsContext)
            else:
                return self.getTypedRuleContext(JackParser.StatementsContext,i)


        def RBRACE(self, i:int=None):
            if i is None:
                return self.getTokens(JackParser.RBRACE)
            else:
                return self.getToken(JackParser.RBRACE, i)

        def ELSE(self):
            return self.getToken(JackParser.ELSE, 0)

        def getRuleIndex(self):
            return JackParser.RULE_ifStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = JackParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_ifStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.match(JackParser.IF)
            self.state = 165
            self.match(JackParser.LPAREN)
            self.state = 166
            self.expression()
            self.state = 167
            self.match(JackParser.RPAREN)
            self.state = 168
            self.match(JackParser.LBRACE)
            self.state = 169
            self.statements()
            self.state = 170
            self.match(JackParser.RBRACE)
            self.state = 176
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 171
                self.match(JackParser.ELSE)
                self.state = 172
                self.match(JackParser.LBRACE)
                self.state = 173
                self.statements()
                self.state = 174
                self.match(JackParser.RBRACE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(JackParser.WHILE, 0)

        def LPAREN(self):
            return self.getToken(JackParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(JackParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(JackParser.RPAREN, 0)

        def LBRACE(self):
            return self.getToken(JackParser.LBRACE, 0)

        def statements(self):
            return self.getTypedRuleContext(JackParser.StatementsContext,0)


        def RBRACE(self):
            return self.getToken(JackParser.RBRACE, 0)

        def getRuleIndex(self):
            return JackParser.RULE_whileStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStatement" ):
                listener.enterWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStatement" ):
                listener.exitWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStatement" ):
                return visitor.visitWhileStatement(self)
            else:
                return visitor.visitChildren(self)




    def whileStatement(self):

        localctx = JackParser.WhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.match(JackParser.WHILE)
            self.state = 179
            self.match(JackParser.LPAREN)
            self.state = 180
            self.expression()
            self.state = 181
            self.match(JackParser.RPAREN)
            self.state = 182
            self.match(JackParser.LBRACE)
            self.state = 183
            self.statements()
            self.state = 184
            self.match(JackParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DO(self):
            return self.getToken(JackParser.DO, 0)

        def subroutineCall(self):
            return self.getTypedRuleContext(JackParser.SubroutineCallContext,0)


        def SEMICOLON(self):
            return self.getToken(JackParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return JackParser.RULE_doStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoStatement" ):
                listener.enterDoStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoStatement" ):
                listener.exitDoStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoStatement" ):
                return visitor.visitDoStatement(self)
            else:
                return visitor.visitChildren(self)




    def doStatement(self):

        localctx = JackParser.DoStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_doStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.match(JackParser.DO)
            self.state = 187
            self.subroutineCall()
            self.state = 188
            self.match(JackParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(JackParser.RETURN, 0)

        def SEMICOLON(self):
            return self.getToken(JackParser.SEMICOLON, 0)

        def expression(self):
            return self.getTypedRuleContext(JackParser.ExpressionContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_returnStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStatement" ):
                listener.enterReturnStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStatement" ):
                listener.exitReturnStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStatement" ):
                return visitor.visitReturnStatement(self)
            else:
                return visitor.visitChildren(self)




    def returnStatement(self):

        localctx = JackParser.ReturnStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_returnStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            self.match(JackParser.RETURN)
            self.state = 192
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 30855598825472) != 0):
                self.state = 191
                self.expression()


            self.state = 194
            self.match(JackParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.TermContext)
            else:
                return self.getTypedRuleContext(JackParser.TermContext,i)


        def op(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.OpContext)
            else:
                return self.getTypedRuleContext(JackParser.OpContext,i)


        def getRuleIndex(self):
            return JackParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = JackParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            self.term()
            self.state = 202
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 8044675072) != 0):
                self.state = 197
                self.op()
                self.state = 198
                self.term()
                self.state = 204
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def integerConstant(self):
            return self.getTypedRuleContext(JackParser.IntegerConstantContext,0)


        def stringConstant(self):
            return self.getTypedRuleContext(JackParser.StringConstantContext,0)


        def keywordConstant(self):
            return self.getTypedRuleContext(JackParser.KeywordConstantContext,0)


        def varName(self):
            return self.getTypedRuleContext(JackParser.VarNameContext,0)


        def LBRACKET(self):
            return self.getToken(JackParser.LBRACKET, 0)

        def expression(self):
            return self.getTypedRuleContext(JackParser.ExpressionContext,0)


        def RBRACKET(self):
            return self.getToken(JackParser.RBRACKET, 0)

        def subroutineCall(self):
            return self.getTypedRuleContext(JackParser.SubroutineCallContext,0)


        def LPAREN(self):
            return self.getToken(JackParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(JackParser.RPAREN, 0)

        def unaryOp(self):
            return self.getTypedRuleContext(JackParser.UnaryOpContext,0)


        def term(self):
            return self.getTypedRuleContext(JackParser.TermContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = JackParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_term)
        try:
            self.state = 222
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 205
                self.integerConstant()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 206
                self.stringConstant()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 207
                self.keywordConstant()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 208
                self.varName()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 209
                self.varName()
                self.state = 210
                self.match(JackParser.LBRACKET)
                self.state = 211
                self.expression()
                self.state = 212
                self.match(JackParser.RBRACKET)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 214
                self.subroutineCall()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 215
                self.match(JackParser.LPAREN)
                self.state = 216
                self.expression()
                self.state = 217
                self.match(JackParser.RPAREN)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 219
                self.unaryOp()
                self.state = 220
                self.term()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubroutineCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subroutineName(self):
            return self.getTypedRuleContext(JackParser.SubroutineNameContext,0)


        def LPAREN(self):
            return self.getToken(JackParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(JackParser.RPAREN, 0)

        def expressionList(self):
            return self.getTypedRuleContext(JackParser.ExpressionListContext,0)


        def DOT(self):
            return self.getToken(JackParser.DOT, 0)

        def className(self):
            return self.getTypedRuleContext(JackParser.ClassNameContext,0)


        def varName(self):
            return self.getTypedRuleContext(JackParser.VarNameContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_subroutineCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubroutineCall" ):
                listener.enterSubroutineCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubroutineCall" ):
                listener.exitSubroutineCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubroutineCall" ):
                return visitor.visitSubroutineCall(self)
            else:
                return visitor.visitChildren(self)




    def subroutineCall(self):

        localctx = JackParser.SubroutineCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_subroutineCall)
        self._la = 0 # Token type
        try:
            self.state = 243
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 224
                self.subroutineName()
                self.state = 225
                self.match(JackParser.LPAREN)
                self.state = 227
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 30855598825472) != 0):
                    self.state = 226
                    self.expressionList()


                self.state = 229
                self.match(JackParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 233
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
                if la_ == 1:
                    self.state = 231
                    self.className()
                    pass

                elif la_ == 2:
                    self.state = 232
                    self.varName()
                    pass


                self.state = 235
                self.match(JackParser.DOT)
                self.state = 236
                self.subroutineName()
                self.state = 237
                self.match(JackParser.LPAREN)
                self.state = 239
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 30855598825472) != 0):
                    self.state = 238
                    self.expressionList()


                self.state = 241
                self.match(JackParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(JackParser.ExpressionContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JackParser.COMMA)
            else:
                return self.getToken(JackParser.COMMA, i)

        def getRuleIndex(self):
            return JackParser.RULE_expressionList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpressionList" ):
                listener.enterExpressionList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpressionList" ):
                listener.exitExpressionList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionList" ):
                return visitor.visitExpressionList(self)
            else:
                return visitor.visitChildren(self)




    def expressionList(self):

        localctx = JackParser.ExpressionListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_expressionList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 245
            self.expression()
            self.state = 250
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 246
                self.match(JackParser.COMMA)
                self.state = 247
                self.expression()
                self.state = 252
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(JackParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(JackParser.MINUS, 0)

        def MUL(self):
            return self.getToken(JackParser.MUL, 0)

        def DIV(self):
            return self.getToken(JackParser.DIV, 0)

        def AND(self):
            return self.getToken(JackParser.AND, 0)

        def OR(self):
            return self.getToken(JackParser.OR, 0)

        def LT(self):
            return self.getToken(JackParser.LT, 0)

        def GT(self):
            return self.getToken(JackParser.GT, 0)

        def EQUAL(self):
            return self.getToken(JackParser.EQUAL, 0)

        def getRuleIndex(self):
            return JackParser.RULE_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOp" ):
                listener.enterOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOp" ):
                listener.exitOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOp" ):
                return visitor.visitOp(self)
            else:
                return visitor.visitChildren(self)




    def op(self):

        localctx = JackParser.OpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_op)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 253
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8044675072) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MINUS(self):
            return self.getToken(JackParser.MINUS, 0)

        def NOT(self):
            return self.getToken(JackParser.NOT, 0)

        def getRuleIndex(self):
            return JackParser.RULE_unaryOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryOp" ):
                listener.enterUnaryOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryOp" ):
                listener.exitUnaryOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryOp" ):
                return visitor.visitUnaryOp(self)
            else:
                return visitor.visitChildren(self)




    def unaryOp(self):

        localctx = JackParser.UnaryOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_unaryOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 255
            _la = self._input.LA(1)
            if not(_la==24 or _la==29):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeywordConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(JackParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(JackParser.FALSE, 0)

        def NULL(self):
            return self.getToken(JackParser.NULL, 0)

        def THIS(self):
            return self.getToken(JackParser.THIS, 0)

        def getRuleIndex(self):
            return JackParser.RULE_keywordConstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKeywordConstant" ):
                listener.enterKeywordConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKeywordConstant" ):
                listener.exitKeywordConstant(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeywordConstant" ):
                return visitor.visitKeywordConstant(self)
            else:
                return visitor.visitChildren(self)




    def keywordConstant(self):

        localctx = JackParser.KeywordConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_keywordConstant)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 122880) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(JackParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return JackParser.RULE_className

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassName" ):
                listener.enterClassName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassName" ):
                listener.exitClassName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassName" ):
                return visitor.visitClassName(self)
            else:
                return visitor.visitChildren(self)




    def className(self):

        localctx = JackParser.ClassNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_className)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 259
            self.match(JackParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubroutineNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(JackParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return JackParser.RULE_subroutineName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubroutineName" ):
                listener.enterSubroutineName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubroutineName" ):
                listener.exitSubroutineName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubroutineName" ):
                return visitor.visitSubroutineName(self)
            else:
                return visitor.visitChildren(self)




    def subroutineName(self):

        localctx = JackParser.SubroutineNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_subroutineName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 261
            self.match(JackParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(JackParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return JackParser.RULE_varName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarName" ):
                listener.enterVarName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarName" ):
                listener.exitVarName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarName" ):
                return visitor.visitVarName(self)
            else:
                return visitor.visitChildren(self)




    def varName(self):

        localctx = JackParser.VarNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_varName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 263
            self.match(JackParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntegerConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(JackParser.INTEGER, 0)

        def getRuleIndex(self):
            return JackParser.RULE_integerConstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntegerConstant" ):
                listener.enterIntegerConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntegerConstant" ):
                listener.exitIntegerConstant(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntegerConstant" ):
                return visitor.visitIntegerConstant(self)
            else:
                return visitor.visitChildren(self)




    def integerConstant(self):

        localctx = JackParser.IntegerConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_integerConstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 265
            self.match(JackParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self):
            return self.getToken(JackParser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return JackParser.RULE_stringConstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringConstant" ):
                listener.enterStringConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringConstant" ):
                listener.exitStringConstant(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringConstant" ):
                return visitor.visitStringConstant(self)
            else:
                return visitor.visitChildren(self)




    def stringConstant(self):

        localctx = JackParser.StringConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_stringConstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 267
            self.match(JackParser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





