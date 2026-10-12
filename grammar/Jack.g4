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
    : CLASS className LBRACE (classVarDeclaration | constDeclaration | enumDeclaration)* subroutineDeclaration* RBRACE
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
    : LBRACE (varDeclaration | constDeclaration)* statements RBRACE
    ;

varDeclaration
    : VAR type localVariable (COMMA localVariable)* SEMICOLON
    ;

localVariable
    : varName (EQUAL expression)?
    ;

constDeclaration
    : CONST type constEntry (COMMA constEntry)* SEMICOLON
    ;

constEntry
    : varName EQUAL expression
    ;

enumDeclaration
    : ENUM className LBRACE enumMember (COMMA enumMember)* COMMA? RBRACE SEMICOLON?
    ;

enumMember
    : varName (EQUAL expression)?
    ;

qualifiedConstant
    : varName DOT varName
    ;

statements
    : statement*
    ;

statement
    : letStatement
    | ifStatement
    | whileStatement
    | forStatement
    | breakStatement
    | continueStatement
    | doStatement
    | returnStatement
    ;

letStatement
    : LET varName (LBRACKET expression RBRACKET)? assignmentOperator expression SEMICOLON
    ;

assignmentOperator
    : EQUAL
    | PLUS_ASSIGN
    | MINUS_ASSIGN
    | MUL_ASSIGN
    | DIV_ASSIGN
    | AND_ASSIGN
    | OR_ASSIGN
    ;

ifStatement
    : IF LPAREN expression RPAREN LBRACE statements RBRACE (ELSE LBRACE statements RBRACE)?
    ;

whileStatement
    : WHILE LPAREN expression RPAREN LBRACE statements RBRACE
    ;

forStatement
    : FOR LPAREN init=forAssignment? SEMICOLON condition=expression? SEMICOLON update=forAssignment? RPAREN LBRACE statements RBRACE
    ;

forAssignment
    : LET? varName (LBRACKET expression RBRACKET)? assignmentOperator expression
    ;

breakStatement
    : BREAK SEMICOLON
    ;

continueStatement
    : CONTINUE SEMICOLON
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
    | characterConstant
    | keywordConstant
    | varName
    | varName LBRACKET expression RBRACKET
    | subroutineCall
    | qualifiedConstant
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
    | LE
    | GE
    | NE
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

characterConstant
    : CHAR_LITERAL
    ;

// Extension keywords remain valid identifiers in standard mode.
CONST       : {getattr(self, 'extensions', False)}? 'const';
ENUM        : {getattr(self, 'extensions', False)}? 'enum';
FOR         : {getattr(self, 'extensions', False)}? 'for';
BREAK       : {getattr(self, 'extensions', False)}? 'break';
CONTINUE    : {getattr(self, 'extensions', False)}? 'continue';

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
PLUS_ASSIGN : '+=';
MINUS_ASSIGN: '-=';
MUL_ASSIGN  : '*=';
DIV_ASSIGN  : '/=';
AND_ASSIGN  : '&=';
OR_ASSIGN   : '|=';
PLUS        : '+';
MINUS       : '-';
MUL         : '*';
DIV         : '/';
AND         : '&';
OR          : '|';
NOT         : '~';
LE          : '<=';
GE          : '>=';
NE          : '!=';
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
    | '0' [xX] [0-9a-fA-F]+
    | '0' [bB] [01]+
    ;

STRING_LITERAL
    : {not getattr(self, 'extensions', False)}? '"' (~["\r\n])* '"'
    | {getattr(self, 'extensions', False)}? '"' ('\\' ~[\r\n] | ~["\\\r\n])* '"'
    ;

CHAR_LITERAL
    : '\'' ('\\' ~[\r\n] | ~['\\\r\n]) '\''
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
