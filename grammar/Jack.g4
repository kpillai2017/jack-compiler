grammar Jack;

/**
 * Jack Grammar for nand2tetris
 * Based on Chapter 9 specification
 * Converted to ANTLR4 format
 */

// Program structure
program
    : classDeclaration EOF
    ;

classDeclaration
    : CLASS className LBRACE classVarDeclaration* subroutineDeclaration* RBRACE
    ;

classVarDeclaration
    : (STATIC | FIELD) type varName (COMMA varName)* SEMICOLON
    ;

type
    : INT
    | BOOLEAN
    | CHAR
    | className   // String and Array are ordinary classes, not keywords
    ;

subroutineDeclaration
    : (CONSTRUCTOR | FUNCTION | METHOD) (VOID | type) subroutineName LPAREN parameterList? RPAREN subroutineBody
    ;

parameterList
    : type varName (COMMA type varName)*
    ;

subroutineBody
    : LBRACE varDeclaration* statements RBRACE
    ;

varDeclaration
    : VAR type varName (COMMA varName)* SEMICOLON
    ;

statements
    : statement*
    ;

statement
    : letStatement
    | ifStatement
    | whileStatement
    | doStatement
    | returnStatement
    ;

letStatement
    : LET varName (LBRACKET expression RBRACKET)? EQUAL expression SEMICOLON
    ;

ifStatement
    : IF LPAREN expression RPAREN LBRACE statements RBRACE (ELSE LBRACE statements RBRACE)?
    ;

whileStatement
    : WHILE LPAREN expression RPAREN LBRACE statements RBRACE
    ;

doStatement
    : DO subroutineCall SEMICOLON
    ;

returnStatement
    : RETURN expression? SEMICOLON
    ;

expression
    : term (op term)*
    ;

term
    : integerConstant
    | stringConstant
    | keywordConstant
    | varName
    | varName LBRACKET expression RBRACKET
    | subroutineCall
    | LPAREN expression RPAREN
    | unaryOp term
    ;

subroutineCall
    : subroutineName LPAREN expressionList? RPAREN
    | (className | varName) DOT subroutineName LPAREN expressionList? RPAREN
    ;

expressionList
    : expression (COMMA expression)*
    ;

op
    : PLUS
    | MINUS
    | MUL
    | DIV
    | AND
    | OR
    | LT
    | GT
    | EQUAL
    ;

unaryOp
    : MINUS
    | NOT
    ;

keywordConstant
    : TRUE
    | FALSE
    | NULL
    | THIS
    ;

// Identifiers and constants
className
    : IDENTIFIER
    ;

subroutineName
    : IDENTIFIER
    ;

varName
    : IDENTIFIER
    ;

integerConstant
    : INTEGER
    ;

stringConstant
    : STRING_LITERAL
    ;

// Keywords
CLASS       : 'class';
CONSTRUCTOR : 'constructor';
FUNCTION    : 'function';
METHOD      : 'method';
FIELD       : 'field';
STATIC      : 'static';
VAR         : 'var';
INT         : 'int';
BOOLEAN     : 'boolean';
CHAR        : 'char';
VOID        : 'void';
TRUE        : 'true';
FALSE       : 'false';
NULL        : 'null';
THIS        : 'this';
LET         : 'let';
DO          : 'do';
IF          : 'if';
ELSE        : 'else';
WHILE       : 'while';
RETURN      : 'return';

// Operators and symbols
PLUS        : '+';
MINUS       : '-';
MUL         : '*';
DIV         : '/';
AND         : '&';
OR          : '|';
NOT         : '~';
LT          : '<';
GT          : '>';
EQUAL       : '=';
DOT         : '.';
COMMA       : ',';
SEMICOLON   : ';';
LPAREN      : '(';
RPAREN      : ')';
LBRACKET    : '[';
RBRACKET    : ']';
LBRACE      : '{';
RBRACE      : '}';

// Literals
INTEGER
    : [0-9]+
    ;

STRING_LITERAL
    : '"' (~["\r\n])* '"'
    ;

IDENTIFIER
    : [a-zA-Z_][a-zA-Z0-9_]*
    ;

// Whitespace and comments
WS
    : [ \t\r\n]+ -> skip
    ;

LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;
