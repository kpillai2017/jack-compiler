# Jack Compiler Architecture

## Overview

This document describes the architecture and design of the Jack compiler, which translates Jack source code to Hack Virtual Machine bytecode.

## System Architecture

### High-Level Pipeline

```
┌─────────────────┐
│  Jack Source    │
│     Code        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Lexical Analysis (ANTLR4)       │
│  - Tokenization                         │
│  - Keyword/operator recognition         │
│  - Comment stripping                    │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Syntax Analysis (ANTLR4)        │
│  - Grammar-based parsing                │
│  - Parse tree construction              │
│  - Error detection                      │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│        Semantic Analysis & Code Gen     │
│  - Symbol table management              │
│  - Type checking                        │
│  - Code generation                      │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│      Hack Virtual Machine Code          │
│  (.vm bytecode)                         │
└─────────────────────────────────────────┘
```

## Component Architecture

### 1. Grammar & Parser Generation (ANTLR4 v4.13.0)

**File**: `grammar/Jack.g4`

The ANTLR4 v4.13.0 grammar defines the complete syntax of the Jack language:

```
Program
  ├── ClassDeclaration
  │   ├── ClassVarDeclaration (static/field)
  │   └── SubroutineDeclaration
  │       ├── Function
  │       ├── Method
  │       └── Constructor
  │
  └── Statements
      ├── LetStatement (assignment)
      ├── IfStatement (conditional)
      ├── WhileStatement (loops)
      ├── DoStatement (calls)
      └── ReturnStatement
```

**ANTLR4 Generates**:
- `JackLexer.py` - Tokenizer implementation
- `JackParser.py` - Parse tree builder
- `JackVisitor.py` - Base visitor class

### 2. Symbol Table Management

**File**: `jack_compiler/symbols.py`

Implements a two-level symbol table:

```python
SymbolTable
├── Class Scope
│   ├── Static Variables (index 0+)
│   └── Field Variables (index 0+)
│
└── Subroutine Scope (reset per function)
    ├── Parameters/Arguments (index 0+)
    └── Local Variables (index 0+)
```

**Data Structure**:
```python
SymbolInfo:
  - name: str
  - type: str
  - kind: VarKind (STATIC, FIELD, ARG, LOCAL)
  - index: int
```

**Operations**:
- `define(name, type, kind)` - Add symbol
- `kind_of(name)` - Get variable kind
- `type_of(name)` - Get variable type
- `index_of(name)` - Get variable index
- `start_subroutine()` - Reset subroutine scope

### 3. Code Generator

**File**: `jack_compiler/codegen.py`

Emits Hack VM instructions during code generation:

```python
CodeGenerator
├── Arithmetic Operations
│   ├── emit_add()
│   ├── emit_subtract()
│   ├── emit_multiply()
│   └── emit_divide()
│
├── Comparison Operations
│   ├── emit_lt()
│   ├── emit_gt()
│   └── emit_eq()
│
├── Logical Operations
│   ├── emit_and()
│   ├── emit_or()
│   └── emit_not()
│
├── Memory Operations
│   ├── push_variable()
│   ├── pop_variable()
│   ├── emit_array_access()
│   └── emit_string_constant()
│
├── Control Flow
│   ├── emit_label()
│   ├── emit_goto()
│   └── emit_if_goto()
│
└── Function Management
    ├── emit_function()
    ├── emit_call()
    └── emit_return()
```

### 4. Compiler Visitor

**File**: `jack_compiler/compiler_visitor.py`

Implements the ANTLR visitor pattern to traverse the parse tree:

```python
JackCompilerVisitor
├── visit_class_declaration()
├── visit_subroutine_declaration()
├── visit_statements()
├── visit_let_statement()
├── visit_if_statement()
├── visit_while_statement()
├── visit_do_statement()
├── visit_return_statement()
├── visit_expression()
├── visit_term()
├── visit_subroutine_call()
└── visit_operator()
```

**Workflow**:
1. Visit class declaration - initialize class-level symbol table
2. For each subroutine:
   - Reset subroutine-level symbol table
   - Emit function declaration
   - Compile statements
3. For each statement:
   - Update symbol table as needed
   - Generate appropriate VM code

### 5. Main Compiler Driver

**File**: `jack_compiler/compiler.py`

Command-line interface and file handling:

```python
JackCompiler
├── compile_file(input_path, output_path)
│   ├── Create input stream
│   ├── Tokenize (Lexer)
│   ├── Parse (Parser)
│   ├── Generate code (Visitor)
│   └── Write output
│
└── compile_directory(input_dir, output_dir)
    └── Process all .jack files
```

## Data Flow Example

### Input Program:
```jack
class Main {
    function void main() {
        var int x;
        let x = 5;
        do Output.printInt(x);
        return;
    }
}
```

### Processing Steps:

**1. Lexical Analysis**
```
Tokens: CLASS, IDENTIFIER(Main), LBRACE, FUNCTION, VOID, ...
```

**2. Parsing**
```
ClassDeclaration
└── SubroutineDeclaration (function Main.main)
    └── Statements
        ├── VarDeclaration (x: int)
        ├── LetStatement (let x = 5)
        ├── DoStatement (do Output.printInt(x))
        └── ReturnStatement
```

**3. Symbol Table after processing declarations**
```
Subroutine Scope:
  x: int, LOCAL, index=0
```

**4. Code Generation**
```
function Main.main 1          // 1 local variable
push constant 5               // Compile: let x = 5
pop local 0
push local 0                  // Compile: printInt(x)
call Output.printInt 1
pop temp 0                    // Discard return value
push constant 0               // Compile: return
return
```

## Memory Model

The Hack VM uses these memory segments:

```
┌──────────────────────────────────────────┐
│  Memory Segments in Hack VM              │
├──────────────────────────────────────────┤
│  local   - Subroutine local variables    │
│  argument- Function parameters           │
│  static  - Class-level static variables  │
│  field   - Object instance fields        │
│  this    - Current object (via pointer 0)│
│  that    - Auxiliary pointer (via pointer 1) │
│  temp    - Temporary storage             │
│  constant- Constant values               │
└──────────────────────────────────────────┘
```

**Variable Kind to Memory Segment Mapping**:
```
VarKind.STATIC  → memory segment "static"
VarKind.FIELD   → memory segment "this"
VarKind.LOCAL   → memory segment "local"
VarKind.ARG     → memory segment "argument"
```

## Control Flow Implementation

### If-Else Statement

```jack
if (x > 0) {
    // block 1
} else {
    // block 2
}
```

**Generated VM Code**:
```vm
push x              // Evaluate condition
push 0
gt
not                 // Negate for false case
if-goto ELSE$0      // Jump if false
                    // Block 1 code
goto ENDIF$0        // Jump over else
label ELSE$0        // Else block
                    // Block 2 code
label ENDIF$0       // End
```

### While Loop

```jack
while (i < 10) {
    // loop body
}
```

**Generated VM Code**:
```vm
label WHILE$0       // Loop start
push i              // Evaluate condition
push 10
lt
not                 // Negate for exit condition
if-goto ENDWHILE$0  // Exit if false
                    // Loop body code
goto WHILE$0        // Jump to condition
label ENDWHILE$0    // After loop
```

## Method and Constructor Handling

### Method Calls

Methods include an implicit `this` pointer as the first argument:

```jack
point.setX(5);  // Equivalent to: Point.setX(point, 5)
```

**Compilation**:
1. Push receiver object (point) onto stack
2. Push arguments (5)
3. Call Point.setX with 2 arguments
4. Handle return value

### Constructor Calls

Constructors allocate memory and initialize the object:

```jack
let p = Point.new(1, 2);
```

**Generated Code**:
```vm
push constant 2         // Allocate 2 fields
call Memory.alloc 1     // VM call
pop pointer 0           // Set this = new object
push argument 0         // Set field values
pop this 0
push argument 1
pop this 1
push pointer 0          // Return this
return
```

## String Literal Handling

Jack string literals are compiled to a sequence of VM calls:

```jack
let s = "Hi";
```

**Generated VM Code**:
```vm
push constant 2         // String length
call String.new 1       // Create string object
push constant 72        // ASCII code for 'H'
call String.appendChar 2// Append character
push constant 105       // ASCII code for 'i'
call String.appendChar 2// Append character
```

## Array Implementation

Arrays are allocated as Jack objects and accessed via memory indirection:

```jack
let arr[2] = 5;
```

**Generated Code**:
```vm
push arr                // Base address
push constant 2         // Index
push constant 5         // Value
pop temp 0              // Save value
add                     // Compute address
pop pointer 1           // Set that = address
push temp 0             // Restore value
pop that 0              // Store in array
```

## Error Handling

The compiler handles errors at multiple levels:

1. **Lexical Errors**: Invalid characters, unterminated strings (ANTLR4 lexer)
2. **Syntax Errors**: Invalid grammar (ANTLR4 parser)
3. **Semantic Errors and Warnings**: Undeclared names, bad calls, missing `return`s and more
   (`checker.py`, before any code is generated)
4. **I/O Errors**: File not found, write permission denied

Lexer and parser errors are captured by `CollectingErrorListener`
(`jack_compiler/compiler.py`) rather than ANTLR's default console listener,
and raised as `JackSyntaxError`, whose `.errors` list holds
`file:line:col: message` strings (1-based). The driver prints them beneath the
failing file, and no `.vm` file is written for it. The semantic checker
(`jack_compiler/checker.py`) checks calls within a class and calls into the
Jack OS (against its API), but not types, nor calls into the program's other
classes: those are compiled separately and resolved by the VM at run time.
See [ERROR_DETECTION.md](ERROR_DETECTION.md).

## Performance Considerations

### Time Complexity
- **Lexical Analysis**: O(n) - single pass through input
- **Parsing**: O(n) - single pass through tokens
- **Code Generation**: O(n) - single pass through parse tree

Overall: **O(n)** where n is the input size

### Space Complexity
- **Symbol Table**: O(s) where s = number of unique symbols
- **Parse Tree**: O(d) where d = maximum nesting depth
- **Generated Code**: O(n) - proportional to input

## Design Patterns Used

1. **Visitor Pattern**: AST traversal and code generation
2. **Symbol Table Pattern**: Scoped variable management
3. **Builder Pattern**: Incremental code generation
4. **Factory Pattern**: Code instruction creation

## Extension Points

The compiler can be extended with:

1. **Additional operators**: Add to grammar and visitor
2. **New built-in types**: Modify symbol table type checking
3. **Optimizations**: Post-processing on generated VM code
4. **More semantic checks**: e.g. check calls between the program's own classes

## References

- ANTLR4 Documentation: https://www.antlr.org/
- Visitor Pattern: Gang of Four Design Patterns
- Compiler Design: "Compilers: Principles, Techniques, and Tools" (Dragon Book)
- Hack Virtual Machine: nand2tetris course materials
