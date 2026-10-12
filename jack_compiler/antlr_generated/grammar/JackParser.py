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
        4,1,61,390,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,1,0,1,0,1,
        0,1,1,1,1,1,1,1,1,1,1,1,1,5,1,88,8,1,10,1,12,1,91,9,1,1,1,5,1,94,
        8,1,10,1,12,1,97,9,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,5,2,106,8,2,10,
        2,12,2,109,9,2,1,2,1,2,1,3,1,3,1,3,1,3,3,3,117,8,3,1,4,1,4,1,4,3,
        4,122,8,4,1,4,1,4,1,4,3,4,127,8,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,
        5,1,5,5,5,138,8,5,10,5,12,5,141,9,5,1,6,1,6,1,6,5,6,146,8,6,10,6,
        12,6,149,9,6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,5,7,159,8,7,10,7,12,
        7,162,9,7,1,7,1,7,1,8,1,8,1,8,3,8,169,8,8,1,9,1,9,1,9,1,9,1,9,5,
        9,176,8,9,10,9,12,9,179,9,9,1,9,1,9,1,10,1,10,1,10,1,10,1,11,1,11,
        1,11,1,11,1,11,1,11,5,11,193,8,11,10,11,12,11,196,9,11,1,11,3,11,
        199,8,11,1,11,1,11,3,11,203,8,11,1,12,1,12,1,12,3,12,208,8,12,1,
        13,1,13,1,13,1,13,1,14,5,14,215,8,14,10,14,12,14,218,9,14,1,15,1,
        15,1,15,1,15,1,15,1,15,1,15,1,15,3,15,228,8,15,1,16,1,16,1,16,1,
        16,1,16,1,16,3,16,236,8,16,1,16,1,16,1,16,1,16,1,17,1,17,1,18,1,
        18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,3,18,256,8,
        18,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,20,1,20,1,20,3,20,269,
        8,20,1,20,1,20,3,20,273,8,20,1,20,1,20,3,20,277,8,20,1,20,1,20,1,
        20,1,20,1,20,1,21,3,21,285,8,21,1,21,1,21,1,21,1,21,1,21,3,21,292,
        8,21,1,21,1,21,1,21,1,22,1,22,1,22,1,23,1,23,1,23,1,24,1,24,1,24,
        1,24,1,25,1,25,3,25,309,8,25,1,25,1,25,1,26,1,26,1,26,1,26,5,26,
        317,8,26,10,26,12,26,320,9,26,1,27,1,27,1,27,1,27,1,27,1,27,1,27,
        1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,3,27,
        341,8,27,1,28,1,28,1,28,3,28,346,8,28,1,28,1,28,1,28,1,28,3,28,352,
        8,28,1,28,1,28,1,28,1,28,3,28,358,8,28,1,28,1,28,3,28,362,8,28,1,
        29,1,29,1,29,5,29,367,8,29,10,29,12,29,370,9,29,1,30,1,30,1,31,1,
        31,1,32,1,32,1,33,1,33,1,34,1,34,1,35,1,35,1,36,1,36,1,37,1,37,1,
        38,1,38,1,38,0,0,39,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,
        34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,
        0,6,1,0,10,11,1,0,7,9,2,0,27,32,45,45,2,0,33,38,40,45,2,0,34,34,
        39,39,1,0,17,20,401,0,78,1,0,0,0,2,81,1,0,0,0,4,100,1,0,0,0,6,116,
        1,0,0,0,8,118,1,0,0,0,10,131,1,0,0,0,12,142,1,0,0,0,14,153,1,0,0,
        0,16,165,1,0,0,0,18,170,1,0,0,0,20,182,1,0,0,0,22,186,1,0,0,0,24,
        204,1,0,0,0,26,209,1,0,0,0,28,216,1,0,0,0,30,227,1,0,0,0,32,229,
        1,0,0,0,34,241,1,0,0,0,36,243,1,0,0,0,38,257,1,0,0,0,40,265,1,0,
        0,0,42,284,1,0,0,0,44,296,1,0,0,0,46,299,1,0,0,0,48,302,1,0,0,0,
        50,306,1,0,0,0,52,312,1,0,0,0,54,340,1,0,0,0,56,361,1,0,0,0,58,363,
        1,0,0,0,60,371,1,0,0,0,62,373,1,0,0,0,64,375,1,0,0,0,66,377,1,0,
        0,0,68,379,1,0,0,0,70,381,1,0,0,0,72,383,1,0,0,0,74,385,1,0,0,0,
        76,387,1,0,0,0,78,79,3,2,1,0,79,80,5,0,0,1,80,1,1,0,0,0,81,82,5,
        6,0,0,82,83,3,66,33,0,83,89,5,53,0,0,84,88,3,4,2,0,85,88,3,18,9,
        0,86,88,3,22,11,0,87,84,1,0,0,0,87,85,1,0,0,0,87,86,1,0,0,0,88,91,
        1,0,0,0,89,87,1,0,0,0,89,90,1,0,0,0,90,95,1,0,0,0,91,89,1,0,0,0,
        92,94,3,8,4,0,93,92,1,0,0,0,94,97,1,0,0,0,95,93,1,0,0,0,95,96,1,
        0,0,0,96,98,1,0,0,0,97,95,1,0,0,0,98,99,5,54,0,0,99,3,1,0,0,0,100,
        101,7,0,0,0,101,102,3,6,3,0,102,107,3,70,35,0,103,104,5,47,0,0,104,
        106,3,70,35,0,105,103,1,0,0,0,106,109,1,0,0,0,107,105,1,0,0,0,107,
        108,1,0,0,0,108,110,1,0,0,0,109,107,1,0,0,0,110,111,5,48,0,0,111,
        5,1,0,0,0,112,117,5,13,0,0,113,117,5,14,0,0,114,117,5,15,0,0,115,
        117,3,66,33,0,116,112,1,0,0,0,116,113,1,0,0,0,116,114,1,0,0,0,116,
        115,1,0,0,0,117,7,1,0,0,0,118,121,7,1,0,0,119,122,5,16,0,0,120,122,
        3,6,3,0,121,119,1,0,0,0,121,120,1,0,0,0,122,123,1,0,0,0,123,124,
        3,68,34,0,124,126,5,49,0,0,125,127,3,10,5,0,126,125,1,0,0,0,126,
        127,1,0,0,0,127,128,1,0,0,0,128,129,5,50,0,0,129,130,3,12,6,0,130,
        9,1,0,0,0,131,132,3,6,3,0,132,139,3,70,35,0,133,134,5,47,0,0,134,
        135,3,6,3,0,135,136,3,70,35,0,136,138,1,0,0,0,137,133,1,0,0,0,138,
        141,1,0,0,0,139,137,1,0,0,0,139,140,1,0,0,0,140,11,1,0,0,0,141,139,
        1,0,0,0,142,147,5,53,0,0,143,146,3,14,7,0,144,146,3,18,9,0,145,143,
        1,0,0,0,145,144,1,0,0,0,146,149,1,0,0,0,147,145,1,0,0,0,147,148,
        1,0,0,0,148,150,1,0,0,0,149,147,1,0,0,0,150,151,3,28,14,0,151,152,
        5,54,0,0,152,13,1,0,0,0,153,154,5,12,0,0,154,155,3,6,3,0,155,160,
        3,16,8,0,156,157,5,47,0,0,157,159,3,16,8,0,158,156,1,0,0,0,159,162,
        1,0,0,0,160,158,1,0,0,0,160,161,1,0,0,0,161,163,1,0,0,0,162,160,
        1,0,0,0,163,164,5,48,0,0,164,15,1,0,0,0,165,168,3,70,35,0,166,167,
        5,45,0,0,167,169,3,52,26,0,168,166,1,0,0,0,168,169,1,0,0,0,169,17,
        1,0,0,0,170,171,5,1,0,0,171,172,3,6,3,0,172,177,3,20,10,0,173,174,
        5,47,0,0,174,176,3,20,10,0,175,173,1,0,0,0,176,179,1,0,0,0,177,175,
        1,0,0,0,177,178,1,0,0,0,178,180,1,0,0,0,179,177,1,0,0,0,180,181,
        5,48,0,0,181,19,1,0,0,0,182,183,3,70,35,0,183,184,5,45,0,0,184,185,
        3,52,26,0,185,21,1,0,0,0,186,187,5,2,0,0,187,188,3,66,33,0,188,189,
        5,53,0,0,189,194,3,24,12,0,190,191,5,47,0,0,191,193,3,24,12,0,192,
        190,1,0,0,0,193,196,1,0,0,0,194,192,1,0,0,0,194,195,1,0,0,0,195,
        198,1,0,0,0,196,194,1,0,0,0,197,199,5,47,0,0,198,197,1,0,0,0,198,
        199,1,0,0,0,199,200,1,0,0,0,200,202,5,54,0,0,201,203,5,48,0,0,202,
        201,1,0,0,0,202,203,1,0,0,0,203,23,1,0,0,0,204,207,3,70,35,0,205,
        206,5,45,0,0,206,208,3,52,26,0,207,205,1,0,0,0,207,208,1,0,0,0,208,
        25,1,0,0,0,209,210,3,70,35,0,210,211,5,46,0,0,211,212,3,70,35,0,
        212,27,1,0,0,0,213,215,3,30,15,0,214,213,1,0,0,0,215,218,1,0,0,0,
        216,214,1,0,0,0,216,217,1,0,0,0,217,29,1,0,0,0,218,216,1,0,0,0,219,
        228,3,32,16,0,220,228,3,36,18,0,221,228,3,38,19,0,222,228,3,40,20,
        0,223,228,3,44,22,0,224,228,3,46,23,0,225,228,3,48,24,0,226,228,
        3,50,25,0,227,219,1,0,0,0,227,220,1,0,0,0,227,221,1,0,0,0,227,222,
        1,0,0,0,227,223,1,0,0,0,227,224,1,0,0,0,227,225,1,0,0,0,227,226,
        1,0,0,0,228,31,1,0,0,0,229,230,5,21,0,0,230,235,3,70,35,0,231,232,
        5,51,0,0,232,233,3,52,26,0,233,234,5,52,0,0,234,236,1,0,0,0,235,
        231,1,0,0,0,235,236,1,0,0,0,236,237,1,0,0,0,237,238,3,34,17,0,238,
        239,3,52,26,0,239,240,5,48,0,0,240,33,1,0,0,0,241,242,7,2,0,0,242,
        35,1,0,0,0,243,244,5,23,0,0,244,245,5,49,0,0,245,246,3,52,26,0,246,
        247,5,50,0,0,247,248,5,53,0,0,248,249,3,28,14,0,249,255,5,54,0,0,
        250,251,5,24,0,0,251,252,5,53,0,0,252,253,3,28,14,0,253,254,5,54,
        0,0,254,256,1,0,0,0,255,250,1,0,0,0,255,256,1,0,0,0,256,37,1,0,0,
        0,257,258,5,25,0,0,258,259,5,49,0,0,259,260,3,52,26,0,260,261,5,
        50,0,0,261,262,5,53,0,0,262,263,3,28,14,0,263,264,5,54,0,0,264,39,
        1,0,0,0,265,266,5,3,0,0,266,268,5,49,0,0,267,269,3,42,21,0,268,267,
        1,0,0,0,268,269,1,0,0,0,269,270,1,0,0,0,270,272,5,48,0,0,271,273,
        3,52,26,0,272,271,1,0,0,0,272,273,1,0,0,0,273,274,1,0,0,0,274,276,
        5,48,0,0,275,277,3,42,21,0,276,275,1,0,0,0,276,277,1,0,0,0,277,278,
        1,0,0,0,278,279,5,50,0,0,279,280,5,53,0,0,280,281,3,28,14,0,281,
        282,5,54,0,0,282,41,1,0,0,0,283,285,5,21,0,0,284,283,1,0,0,0,284,
        285,1,0,0,0,285,286,1,0,0,0,286,291,3,70,35,0,287,288,5,51,0,0,288,
        289,3,52,26,0,289,290,5,52,0,0,290,292,1,0,0,0,291,287,1,0,0,0,291,
        292,1,0,0,0,292,293,1,0,0,0,293,294,3,34,17,0,294,295,3,52,26,0,
        295,43,1,0,0,0,296,297,5,4,0,0,297,298,5,48,0,0,298,45,1,0,0,0,299,
        300,5,5,0,0,300,301,5,48,0,0,301,47,1,0,0,0,302,303,5,22,0,0,303,
        304,3,56,28,0,304,305,5,48,0,0,305,49,1,0,0,0,306,308,5,26,0,0,307,
        309,3,52,26,0,308,307,1,0,0,0,308,309,1,0,0,0,309,310,1,0,0,0,310,
        311,5,48,0,0,311,51,1,0,0,0,312,318,3,54,27,0,313,314,3,60,30,0,
        314,315,3,54,27,0,315,317,1,0,0,0,316,313,1,0,0,0,317,320,1,0,0,
        0,318,316,1,0,0,0,318,319,1,0,0,0,319,53,1,0,0,0,320,318,1,0,0,0,
        321,341,3,72,36,0,322,341,3,74,37,0,323,341,3,76,38,0,324,341,3,
        64,32,0,325,341,3,70,35,0,326,327,3,70,35,0,327,328,5,51,0,0,328,
        329,3,52,26,0,329,330,5,52,0,0,330,341,1,0,0,0,331,341,3,56,28,0,
        332,341,3,26,13,0,333,334,5,49,0,0,334,335,3,52,26,0,335,336,5,50,
        0,0,336,341,1,0,0,0,337,338,3,62,31,0,338,339,3,54,27,0,339,341,
        1,0,0,0,340,321,1,0,0,0,340,322,1,0,0,0,340,323,1,0,0,0,340,324,
        1,0,0,0,340,325,1,0,0,0,340,326,1,0,0,0,340,331,1,0,0,0,340,332,
        1,0,0,0,340,333,1,0,0,0,340,337,1,0,0,0,341,55,1,0,0,0,342,343,3,
        68,34,0,343,345,5,49,0,0,344,346,3,58,29,0,345,344,1,0,0,0,345,346,
        1,0,0,0,346,347,1,0,0,0,347,348,5,50,0,0,348,362,1,0,0,0,349,352,
        3,66,33,0,350,352,3,70,35,0,351,349,1,0,0,0,351,350,1,0,0,0,352,
        353,1,0,0,0,353,354,5,46,0,0,354,355,3,68,34,0,355,357,5,49,0,0,
        356,358,3,58,29,0,357,356,1,0,0,0,357,358,1,0,0,0,358,359,1,0,0,
        0,359,360,5,50,0,0,360,362,1,0,0,0,361,342,1,0,0,0,361,351,1,0,0,
        0,362,57,1,0,0,0,363,368,3,52,26,0,364,365,5,47,0,0,365,367,3,52,
        26,0,366,364,1,0,0,0,367,370,1,0,0,0,368,366,1,0,0,0,368,369,1,0,
        0,0,369,59,1,0,0,0,370,368,1,0,0,0,371,372,7,3,0,0,372,61,1,0,0,
        0,373,374,7,4,0,0,374,63,1,0,0,0,375,376,7,5,0,0,376,65,1,0,0,0,
        377,378,5,58,0,0,378,67,1,0,0,0,379,380,5,58,0,0,380,69,1,0,0,0,
        381,382,5,58,0,0,382,71,1,0,0,0,383,384,5,55,0,0,384,73,1,0,0,0,
        385,386,5,56,0,0,386,75,1,0,0,0,387,388,5,57,0,0,388,77,1,0,0,0,
        34,87,89,95,107,116,121,126,139,145,147,160,168,177,194,198,202,
        207,216,227,235,255,268,272,276,284,291,308,318,340,345,351,357,
        361,368
    ]

class JackParser ( Parser ):

    grammarFileName = "Jack.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'class'", "'constructor'", 
                     "'function'", "'method'", "'field'", "'static'", "'var'", 
                     "'int'", "'boolean'", "'char'", "'void'", "'true'", 
                     "'false'", "'null'", "'this'", "'let'", "'do'", "'if'", 
                     "'else'", "'while'", "'return'", "'+='", "'-='", "'*='", 
                     "'/='", "'&='", "'|='", "'+'", "'-'", "'*'", "'/'", 
                     "'&'", "'|'", "'~'", "'<='", "'>='", "'!='", "'<'", 
                     "'>'", "'='", "'.'", "','", "';'", "'('", "')'", "'['", 
                     "']'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>", "CONST", "ENUM", "FOR", "BREAK", "CONTINUE", 
                      "CLASS", "CONSTRUCTOR", "FUNCTION", "METHOD", "FIELD", 
                      "STATIC", "VAR", "INT", "BOOLEAN", "CHAR", "VOID", 
                      "TRUE", "FALSE", "NULL", "THIS", "LET", "DO", "IF", 
                      "ELSE", "WHILE", "RETURN", "PLUS_ASSIGN", "MINUS_ASSIGN", 
                      "MUL_ASSIGN", "DIV_ASSIGN", "AND_ASSIGN", "OR_ASSIGN", 
                      "PLUS", "MINUS", "MUL", "DIV", "AND", "OR", "NOT", 
                      "LE", "GE", "NE", "LT", "GT", "EQUAL", "DOT", "COMMA", 
                      "SEMICOLON", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", 
                      "LBRACE", "RBRACE", "INTEGER", "STRING_LITERAL", "CHAR_LITERAL", 
                      "IDENTIFIER", "WS", "LINE_COMMENT", "BLOCK_COMMENT" ]

    RULE_program = 0
    RULE_classDeclaration = 1
    RULE_classVarDeclaration = 2
    RULE_type = 3
    RULE_subroutineDeclaration = 4
    RULE_parameterList = 5
    RULE_subroutineBody = 6
    RULE_varDeclaration = 7
    RULE_localVariable = 8
    RULE_constDeclaration = 9
    RULE_constEntry = 10
    RULE_enumDeclaration = 11
    RULE_enumMember = 12
    RULE_qualifiedConstant = 13
    RULE_statements = 14
    RULE_statement = 15
    RULE_letStatement = 16
    RULE_assignmentOperator = 17
    RULE_ifStatement = 18
    RULE_whileStatement = 19
    RULE_forStatement = 20
    RULE_forAssignment = 21
    RULE_breakStatement = 22
    RULE_continueStatement = 23
    RULE_doStatement = 24
    RULE_returnStatement = 25
    RULE_expression = 26
    RULE_term = 27
    RULE_subroutineCall = 28
    RULE_expressionList = 29
    RULE_op = 30
    RULE_unaryOp = 31
    RULE_keywordConstant = 32
    RULE_className = 33
    RULE_subroutineName = 34
    RULE_varName = 35
    RULE_integerConstant = 36
    RULE_stringConstant = 37
    RULE_characterConstant = 38

    ruleNames =  [ "program", "classDeclaration", "classVarDeclaration", 
                   "type", "subroutineDeclaration", "parameterList", "subroutineBody", 
                   "varDeclaration", "localVariable", "constDeclaration", 
                   "constEntry", "enumDeclaration", "enumMember", "qualifiedConstant", 
                   "statements", "statement", "letStatement", "assignmentOperator", 
                   "ifStatement", "whileStatement", "forStatement", "forAssignment", 
                   "breakStatement", "continueStatement", "doStatement", 
                   "returnStatement", "expression", "term", "subroutineCall", 
                   "expressionList", "op", "unaryOp", "keywordConstant", 
                   "className", "subroutineName", "varName", "integerConstant", 
                   "stringConstant", "characterConstant" ]

    EOF = Token.EOF
    CONST=1
    ENUM=2
    FOR=3
    BREAK=4
    CONTINUE=5
    CLASS=6
    CONSTRUCTOR=7
    FUNCTION=8
    METHOD=9
    FIELD=10
    STATIC=11
    VAR=12
    INT=13
    BOOLEAN=14
    CHAR=15
    VOID=16
    TRUE=17
    FALSE=18
    NULL=19
    THIS=20
    LET=21
    DO=22
    IF=23
    ELSE=24
    WHILE=25
    RETURN=26
    PLUS_ASSIGN=27
    MINUS_ASSIGN=28
    MUL_ASSIGN=29
    DIV_ASSIGN=30
    AND_ASSIGN=31
    OR_ASSIGN=32
    PLUS=33
    MINUS=34
    MUL=35
    DIV=36
    AND=37
    OR=38
    NOT=39
    LE=40
    GE=41
    NE=42
    LT=43
    GT=44
    EQUAL=45
    DOT=46
    COMMA=47
    SEMICOLON=48
    LPAREN=49
    RPAREN=50
    LBRACKET=51
    RBRACKET=52
    LBRACE=53
    RBRACE=54
    INTEGER=55
    STRING_LITERAL=56
    CHAR_LITERAL=57
    IDENTIFIER=58
    WS=59
    LINE_COMMENT=60
    BLOCK_COMMENT=61

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
            self.state = 78
            self.classDeclaration()
            self.state = 79
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


        def constDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.ConstDeclarationContext)
            else:
                return self.getTypedRuleContext(JackParser.ConstDeclarationContext,i)


        def enumDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.EnumDeclarationContext)
            else:
                return self.getTypedRuleContext(JackParser.EnumDeclarationContext,i)


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
            self.state = 81
            self.match(JackParser.CLASS)
            self.state = 82
            self.className()
            self.state = 83
            self.match(JackParser.LBRACE)
            self.state = 89
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3078) != 0):
                self.state = 87
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [10, 11]:
                    self.state = 84
                    self.classVarDeclaration()
                    pass
                elif token in [1]:
                    self.state = 85
                    self.constDeclaration()
                    pass
                elif token in [2]:
                    self.state = 86
                    self.enumDeclaration()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 91
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 95
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 896) != 0):
                self.state = 92
                self.subroutineDeclaration()
                self.state = 97
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 98
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
            self.state = 100
            _la = self._input.LA(1)
            if not(_la==10 or _la==11):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 101
            self.type_()
            self.state = 102
            self.varName()
            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47:
                self.state = 103
                self.match(JackParser.COMMA)
                self.state = 104
                self.varName()
                self.state = 109
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 110
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
            self.state = 116
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [13]:
                self.enterOuterAlt(localctx, 1)
                self.state = 112
                self.match(JackParser.INT)
                pass
            elif token in [14]:
                self.enterOuterAlt(localctx, 2)
                self.state = 113
                self.match(JackParser.BOOLEAN)
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 3)
                self.state = 114
                self.match(JackParser.CHAR)
                pass
            elif token in [58]:
                self.enterOuterAlt(localctx, 4)
                self.state = 115
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
            self.state = 118
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 896) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 121
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16]:
                self.state = 119
                self.match(JackParser.VOID)
                pass
            elif token in [13, 14, 15, 58]:
                self.state = 120
                self.type_()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 123
            self.subroutineName()
            self.state = 124
            self.match(JackParser.LPAREN)
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 288230376151769088) != 0):
                self.state = 125
                self.parameterList()


            self.state = 128
            self.match(JackParser.RPAREN)
            self.state = 129
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
            self.state = 131
            self.type_()
            self.state = 132
            self.varName()
            self.state = 139
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47:
                self.state = 133
                self.match(JackParser.COMMA)
                self.state = 134
                self.type_()
                self.state = 135
                self.varName()
                self.state = 141
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


        def constDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.ConstDeclarationContext)
            else:
                return self.getTypedRuleContext(JackParser.ConstDeclarationContext,i)


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
            self.state = 142
            self.match(JackParser.LBRACE)
            self.state = 147
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==12:
                self.state = 145
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [12]:
                    self.state = 143
                    self.varDeclaration()
                    pass
                elif token in [1]:
                    self.state = 144
                    self.constDeclaration()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 149
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 150
            self.statements()
            self.state = 151
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


        def localVariable(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.LocalVariableContext)
            else:
                return self.getTypedRuleContext(JackParser.LocalVariableContext,i)


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
            self.state = 153
            self.match(JackParser.VAR)
            self.state = 154
            self.type_()
            self.state = 155
            self.localVariable()
            self.state = 160
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47:
                self.state = 156
                self.match(JackParser.COMMA)
                self.state = 157
                self.localVariable()
                self.state = 162
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 163
            self.match(JackParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LocalVariableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varName(self):
            return self.getTypedRuleContext(JackParser.VarNameContext,0)


        def EQUAL(self):
            return self.getToken(JackParser.EQUAL, 0)

        def expression(self):
            return self.getTypedRuleContext(JackParser.ExpressionContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_localVariable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLocalVariable" ):
                listener.enterLocalVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLocalVariable" ):
                listener.exitLocalVariable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLocalVariable" ):
                return visitor.visitLocalVariable(self)
            else:
                return visitor.visitChildren(self)




    def localVariable(self):

        localctx = JackParser.LocalVariableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_localVariable)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 165
            self.varName()
            self.state = 168
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 166
                self.match(JackParser.EQUAL)
                self.state = 167
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONST(self):
            return self.getToken(JackParser.CONST, 0)

        def type_(self):
            return self.getTypedRuleContext(JackParser.TypeContext,0)


        def constEntry(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.ConstEntryContext)
            else:
                return self.getTypedRuleContext(JackParser.ConstEntryContext,i)


        def SEMICOLON(self):
            return self.getToken(JackParser.SEMICOLON, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JackParser.COMMA)
            else:
                return self.getToken(JackParser.COMMA, i)

        def getRuleIndex(self):
            return JackParser.RULE_constDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstDeclaration" ):
                listener.enterConstDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstDeclaration" ):
                listener.exitConstDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstDeclaration" ):
                return visitor.visitConstDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def constDeclaration(self):

        localctx = JackParser.ConstDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_constDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            self.match(JackParser.CONST)
            self.state = 171
            self.type_()
            self.state = 172
            self.constEntry()
            self.state = 177
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47:
                self.state = 173
                self.match(JackParser.COMMA)
                self.state = 174
                self.constEntry()
                self.state = 179
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 180
            self.match(JackParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstEntryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varName(self):
            return self.getTypedRuleContext(JackParser.VarNameContext,0)


        def EQUAL(self):
            return self.getToken(JackParser.EQUAL, 0)

        def expression(self):
            return self.getTypedRuleContext(JackParser.ExpressionContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_constEntry

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstEntry" ):
                listener.enterConstEntry(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstEntry" ):
                listener.exitConstEntry(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstEntry" ):
                return visitor.visitConstEntry(self)
            else:
                return visitor.visitChildren(self)




    def constEntry(self):

        localctx = JackParser.ConstEntryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_constEntry)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 182
            self.varName()
            self.state = 183
            self.match(JackParser.EQUAL)
            self.state = 184
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnumDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENUM(self):
            return self.getToken(JackParser.ENUM, 0)

        def className(self):
            return self.getTypedRuleContext(JackParser.ClassNameContext,0)


        def LBRACE(self):
            return self.getToken(JackParser.LBRACE, 0)

        def enumMember(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.EnumMemberContext)
            else:
                return self.getTypedRuleContext(JackParser.EnumMemberContext,i)


        def RBRACE(self):
            return self.getToken(JackParser.RBRACE, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JackParser.COMMA)
            else:
                return self.getToken(JackParser.COMMA, i)

        def SEMICOLON(self):
            return self.getToken(JackParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return JackParser.RULE_enumDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnumDeclaration" ):
                listener.enterEnumDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnumDeclaration" ):
                listener.exitEnumDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnumDeclaration" ):
                return visitor.visitEnumDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def enumDeclaration(self):

        localctx = JackParser.EnumDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_enumDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.match(JackParser.ENUM)
            self.state = 187
            self.className()
            self.state = 188
            self.match(JackParser.LBRACE)
            self.state = 189
            self.enumMember()
            self.state = 194
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,13,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 190
                    self.match(JackParser.COMMA)
                    self.state = 191
                    self.enumMember() 
                self.state = 196
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,13,self._ctx)

            self.state = 198
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 197
                self.match(JackParser.COMMA)


            self.state = 200
            self.match(JackParser.RBRACE)
            self.state = 202
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==48:
                self.state = 201
                self.match(JackParser.SEMICOLON)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnumMemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varName(self):
            return self.getTypedRuleContext(JackParser.VarNameContext,0)


        def EQUAL(self):
            return self.getToken(JackParser.EQUAL, 0)

        def expression(self):
            return self.getTypedRuleContext(JackParser.ExpressionContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_enumMember

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnumMember" ):
                listener.enterEnumMember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnumMember" ):
                listener.exitEnumMember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnumMember" ):
                return visitor.visitEnumMember(self)
            else:
                return visitor.visitChildren(self)




    def enumMember(self):

        localctx = JackParser.EnumMemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_enumMember)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
            self.varName()
            self.state = 207
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 205
                self.match(JackParser.EQUAL)
                self.state = 206
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QualifiedConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.VarNameContext)
            else:
                return self.getTypedRuleContext(JackParser.VarNameContext,i)


        def DOT(self):
            return self.getToken(JackParser.DOT, 0)

        def getRuleIndex(self):
            return JackParser.RULE_qualifiedConstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQualifiedConstant" ):
                listener.enterQualifiedConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQualifiedConstant" ):
                listener.exitQualifiedConstant(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQualifiedConstant" ):
                return visitor.visitQualifiedConstant(self)
            else:
                return visitor.visitChildren(self)




    def qualifiedConstant(self):

        localctx = JackParser.QualifiedConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_qualifiedConstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 209
            self.varName()
            self.state = 210
            self.match(JackParser.DOT)
            self.state = 211
            self.varName()
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
        self.enterRule(localctx, 28, self.RULE_statements)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 216
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 115343416) != 0):
                self.state = 213
                self.statement()
                self.state = 218
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


        def forStatement(self):
            return self.getTypedRuleContext(JackParser.ForStatementContext,0)


        def breakStatement(self):
            return self.getTypedRuleContext(JackParser.BreakStatementContext,0)


        def continueStatement(self):
            return self.getTypedRuleContext(JackParser.ContinueStatementContext,0)


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
        self.enterRule(localctx, 30, self.RULE_statement)
        try:
            self.state = 227
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [21]:
                self.enterOuterAlt(localctx, 1)
                self.state = 219
                self.letStatement()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 2)
                self.state = 220
                self.ifStatement()
                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 3)
                self.state = 221
                self.whileStatement()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 4)
                self.state = 222
                self.forStatement()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 5)
                self.state = 223
                self.breakStatement()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 6)
                self.state = 224
                self.continueStatement()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 7)
                self.state = 225
                self.doStatement()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 8)
                self.state = 226
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


        def assignmentOperator(self):
            return self.getTypedRuleContext(JackParser.AssignmentOperatorContext,0)


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
        self.enterRule(localctx, 32, self.RULE_letStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 229
            self.match(JackParser.LET)
            self.state = 230
            self.varName()
            self.state = 235
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==51:
                self.state = 231
                self.match(JackParser.LBRACKET)
                self.state = 232
                self.expression()
                self.state = 233
                self.match(JackParser.RBRACKET)


            self.state = 237
            self.assignmentOperator()
            self.state = 238
            self.expression()
            self.state = 239
            self.match(JackParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQUAL(self):
            return self.getToken(JackParser.EQUAL, 0)

        def PLUS_ASSIGN(self):
            return self.getToken(JackParser.PLUS_ASSIGN, 0)

        def MINUS_ASSIGN(self):
            return self.getToken(JackParser.MINUS_ASSIGN, 0)

        def MUL_ASSIGN(self):
            return self.getToken(JackParser.MUL_ASSIGN, 0)

        def DIV_ASSIGN(self):
            return self.getToken(JackParser.DIV_ASSIGN, 0)

        def AND_ASSIGN(self):
            return self.getToken(JackParser.AND_ASSIGN, 0)

        def OR_ASSIGN(self):
            return self.getToken(JackParser.OR_ASSIGN, 0)

        def getRuleIndex(self):
            return JackParser.RULE_assignmentOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignmentOperator" ):
                listener.enterAssignmentOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignmentOperator" ):
                listener.exitAssignmentOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentOperator" ):
                return visitor.visitAssignmentOperator(self)
            else:
                return visitor.visitChildren(self)




    def assignmentOperator(self):

        localctx = JackParser.AssignmentOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_assignmentOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 241
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 35192827805696) != 0)):
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
        self.enterRule(localctx, 36, self.RULE_ifStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 243
            self.match(JackParser.IF)
            self.state = 244
            self.match(JackParser.LPAREN)
            self.state = 245
            self.expression()
            self.state = 246
            self.match(JackParser.RPAREN)
            self.state = 247
            self.match(JackParser.LBRACE)
            self.state = 248
            self.statements()
            self.state = 249
            self.match(JackParser.RBRACE)
            self.state = 255
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==24:
                self.state = 250
                self.match(JackParser.ELSE)
                self.state = 251
                self.match(JackParser.LBRACE)
                self.state = 252
                self.statements()
                self.state = 253
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
        self.enterRule(localctx, 38, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            self.match(JackParser.WHILE)
            self.state = 258
            self.match(JackParser.LPAREN)
            self.state = 259
            self.expression()
            self.state = 260
            self.match(JackParser.RPAREN)
            self.state = 261
            self.match(JackParser.LBRACE)
            self.state = 262
            self.statements()
            self.state = 263
            self.match(JackParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.init = None # ForAssignmentContext
            self.condition = None # ExpressionContext
            self.update = None # ForAssignmentContext

        def FOR(self):
            return self.getToken(JackParser.FOR, 0)

        def LPAREN(self):
            return self.getToken(JackParser.LPAREN, 0)

        def SEMICOLON(self, i:int=None):
            if i is None:
                return self.getTokens(JackParser.SEMICOLON)
            else:
                return self.getToken(JackParser.SEMICOLON, i)

        def RPAREN(self):
            return self.getToken(JackParser.RPAREN, 0)

        def LBRACE(self):
            return self.getToken(JackParser.LBRACE, 0)

        def statements(self):
            return self.getTypedRuleContext(JackParser.StatementsContext,0)


        def RBRACE(self):
            return self.getToken(JackParser.RBRACE, 0)

        def forAssignment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.ForAssignmentContext)
            else:
                return self.getTypedRuleContext(JackParser.ForAssignmentContext,i)


        def expression(self):
            return self.getTypedRuleContext(JackParser.ExpressionContext,0)


        def getRuleIndex(self):
            return JackParser.RULE_forStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStatement" ):
                listener.enterForStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStatement" ):
                listener.exitForStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStatement" ):
                return visitor.visitForStatement(self)
            else:
                return visitor.visitChildren(self)




    def forStatement(self):

        localctx = JackParser.ForStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 265
            self.match(JackParser.FOR)
            self.state = 266
            self.match(JackParser.LPAREN)
            self.state = 268
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21 or _la==58:
                self.state = 267
                localctx.init = self.forAssignment()


            self.state = 270
            self.match(JackParser.SEMICOLON)
            self.state = 272
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540995472175529984) != 0):
                self.state = 271
                localctx.condition = self.expression()


            self.state = 274
            self.match(JackParser.SEMICOLON)
            self.state = 276
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21 or _la==58:
                self.state = 275
                localctx.update = self.forAssignment()


            self.state = 278
            self.match(JackParser.RPAREN)
            self.state = 279
            self.match(JackParser.LBRACE)
            self.state = 280
            self.statements()
            self.state = 281
            self.match(JackParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForAssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varName(self):
            return self.getTypedRuleContext(JackParser.VarNameContext,0)


        def assignmentOperator(self):
            return self.getTypedRuleContext(JackParser.AssignmentOperatorContext,0)


        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JackParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(JackParser.ExpressionContext,i)


        def LET(self):
            return self.getToken(JackParser.LET, 0)

        def LBRACKET(self):
            return self.getToken(JackParser.LBRACKET, 0)

        def RBRACKET(self):
            return self.getToken(JackParser.RBRACKET, 0)

        def getRuleIndex(self):
            return JackParser.RULE_forAssignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForAssignment" ):
                listener.enterForAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForAssignment" ):
                listener.exitForAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForAssignment" ):
                return visitor.visitForAssignment(self)
            else:
                return visitor.visitChildren(self)




    def forAssignment(self):

        localctx = JackParser.ForAssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_forAssignment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 284
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21:
                self.state = 283
                self.match(JackParser.LET)


            self.state = 286
            self.varName()
            self.state = 291
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==51:
                self.state = 287
                self.match(JackParser.LBRACKET)
                self.state = 288
                self.expression()
                self.state = 289
                self.match(JackParser.RBRACKET)


            self.state = 293
            self.assignmentOperator()
            self.state = 294
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BREAK(self):
            return self.getToken(JackParser.BREAK, 0)

        def SEMICOLON(self):
            return self.getToken(JackParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return JackParser.RULE_breakStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreakStatement" ):
                listener.enterBreakStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreakStatement" ):
                listener.exitBreakStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStatement" ):
                return visitor.visitBreakStatement(self)
            else:
                return visitor.visitChildren(self)




    def breakStatement(self):

        localctx = JackParser.BreakStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_breakStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 296
            self.match(JackParser.BREAK)
            self.state = 297
            self.match(JackParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinueStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTINUE(self):
            return self.getToken(JackParser.CONTINUE, 0)

        def SEMICOLON(self):
            return self.getToken(JackParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return JackParser.RULE_continueStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinueStatement" ):
                listener.enterContinueStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinueStatement" ):
                listener.exitContinueStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinueStatement" ):
                return visitor.visitContinueStatement(self)
            else:
                return visitor.visitChildren(self)




    def continueStatement(self):

        localctx = JackParser.ContinueStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_continueStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 299
            self.match(JackParser.CONTINUE)
            self.state = 300
            self.match(JackParser.SEMICOLON)
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
        self.enterRule(localctx, 48, self.RULE_doStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 302
            self.match(JackParser.DO)
            self.state = 303
            self.subroutineCall()
            self.state = 304
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
        self.enterRule(localctx, 50, self.RULE_returnStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 306
            self.match(JackParser.RETURN)
            self.state = 308
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540995472175529984) != 0):
                self.state = 307
                self.expression()


            self.state = 310
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
        self.enterRule(localctx, 52, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 312
            self.term()
            self.state = 318
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 69810398429184) != 0):
                self.state = 313
                self.op()
                self.state = 314
                self.term()
                self.state = 320
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


        def characterConstant(self):
            return self.getTypedRuleContext(JackParser.CharacterConstantContext,0)


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


        def qualifiedConstant(self):
            return self.getTypedRuleContext(JackParser.QualifiedConstantContext,0)


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
        self.enterRule(localctx, 54, self.RULE_term)
        try:
            self.state = 340
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 321
                self.integerConstant()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 322
                self.stringConstant()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 323
                self.characterConstant()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 324
                self.keywordConstant()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 325
                self.varName()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 326
                self.varName()
                self.state = 327
                self.match(JackParser.LBRACKET)
                self.state = 328
                self.expression()
                self.state = 329
                self.match(JackParser.RBRACKET)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 331
                self.subroutineCall()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 332
                self.qualifiedConstant()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 333
                self.match(JackParser.LPAREN)
                self.state = 334
                self.expression()
                self.state = 335
                self.match(JackParser.RPAREN)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 337
                self.unaryOp()
                self.state = 338
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
        self.enterRule(localctx, 56, self.RULE_subroutineCall)
        self._la = 0 # Token type
        try:
            self.state = 361
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 342
                self.subroutineName()
                self.state = 343
                self.match(JackParser.LPAREN)
                self.state = 345
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540995472175529984) != 0):
                    self.state = 344
                    self.expressionList()


                self.state = 347
                self.match(JackParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 351
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
                if la_ == 1:
                    self.state = 349
                    self.className()
                    pass

                elif la_ == 2:
                    self.state = 350
                    self.varName()
                    pass


                self.state = 353
                self.match(JackParser.DOT)
                self.state = 354
                self.subroutineName()
                self.state = 355
                self.match(JackParser.LPAREN)
                self.state = 357
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540995472175529984) != 0):
                    self.state = 356
                    self.expressionList()


                self.state = 359
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
        self.enterRule(localctx, 58, self.RULE_expressionList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 363
            self.expression()
            self.state = 368
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47:
                self.state = 364
                self.match(JackParser.COMMA)
                self.state = 365
                self.expression()
                self.state = 370
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

        def LE(self):
            return self.getToken(JackParser.LE, 0)

        def GE(self):
            return self.getToken(JackParser.GE, 0)

        def NE(self):
            return self.getToken(JackParser.NE, 0)

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
        self.enterRule(localctx, 60, self.RULE_op)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 371
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 69810398429184) != 0)):
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
        self.enterRule(localctx, 62, self.RULE_unaryOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 373
            _la = self._input.LA(1)
            if not(_la==34 or _la==39):
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
        self.enterRule(localctx, 64, self.RULE_keywordConstant)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 375
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1966080) != 0)):
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
        self.enterRule(localctx, 66, self.RULE_className)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 377
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
        self.enterRule(localctx, 68, self.RULE_subroutineName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 379
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
        self.enterRule(localctx, 70, self.RULE_varName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 381
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
        self.enterRule(localctx, 72, self.RULE_integerConstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 383
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
        self.enterRule(localctx, 74, self.RULE_stringConstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 385
            self.match(JackParser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHAR_LITERAL(self):
            return self.getToken(JackParser.CHAR_LITERAL, 0)

        def getRuleIndex(self):
            return JackParser.RULE_characterConstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterConstant" ):
                listener.enterCharacterConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterConstant" ):
                listener.exitCharacterConstant(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharacterConstant" ):
                return visitor.visitCharacterConstant(self)
            else:
                return visitor.visitChildren(self)




    def characterConstant(self):

        localctx = JackParser.CharacterConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_characterConstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 387
            self.match(JackParser.CHAR_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





