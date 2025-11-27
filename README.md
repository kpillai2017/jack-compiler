# Jack Compiler for nand2tetris

A complete, production-ready Jack compiler implementation using ANTLR4 that translates Jack source code to Hack Virtual Machine (VM) code.

## Overview

This compiler implements the full Jack language specification from the nand2tetris course. It is built with Terence Parr's ANTLR4 parser generator and includes:

- **Lexical Analysis**: Tokenization with full comment and string literal support
- **Syntax Analysis**: Complete ANTLR4 grammar with visitor pattern implementation
- **Semantic Analysis**: Symbol table management with class and subroutine scopes, type tracking
- **Code Generation**: Translation to Hack VM bytecode format
- **Comprehensive Testing**: Unit tests for symbol tables and code generation

## Features

✅ **Language Support**
- Variables: static, field, local, and parameter variables
- Data Types: int, boolean, String, and custom class types
- Operators: arithmetic, relational, logical, and unary operators
- Control Flow: if/else statements, while loops, function calls
- Subroutines: functions, methods, and constructors with proper scoping
- Arrays: single-dimensional array operations
- String & Integer Literals: with proper character encoding
- Comments: single-line (//) and block (/* */) comments

✅ **Code Quality**
- Clean separation of concerns (lexer, parser, symbol table, code generation)
- ANTLR4 visitor pattern for AST traversal
- Proper symbol table scoping (class and subroutine levels)
- Comprehensive error handling

✅ **Usability**
- Simple command-line interface
- Single file and batch directory compilation
- Example programs demonstrating all language features
- Detailed documentation and usage guide

## Project Structure

```
jack-compiler/
├── .gitignore                   # Git ignore rules
├── .gitattributes               # Line ending normalization
├── README.md                    # This file
├── USAGE.md                     # Detailed usage guide
├── ARCHITECTURE.md              # Architecture documentation
├── QUICK_REFERENCE.md           # Quick reference guide
├── ERROR_DETECTION.md           # Error handling documentation
├── REFERENCE_COMPATIBILITY.md   # Compatibility information
├── CLEANUP_SUMMARY.md           # Repository cleanup details
│
├── src/                         # SOURCE CODE
│   ├── __init__.py
│   ├── compiler.py              # Main compiler driver (CLI)
│   ├── compiler_visitor_v2.py   # ANTLR visitor for code generation
│   ├── symbols.py               # Symbol table implementation
│   ├── codegen.py               # VM code generator
│   └── antlr_generated/         # ANTLR4-generated files
│       └── grammar/
│           ├── JackLexer.py
│           ├── JackParser.py
│           ├── JackVisitor.py
│           └── JackListener.py
│
├── examples/                    # EXAMPLE PROGRAMS
│   ├── HelloWorld.jack / HelloWorld.vm
│   ├── Math.jack / Math.vm
│   ├── Loop.jack / Loop.vm
│   ├── Point.jack / Point.vm
│   └── Array.jack / Array.vm
│
├── tests/                       # UNIT TESTS
│   └── test_compiler.py
│
├── grammar/                     # GRAMMAR DEFINITION
│   └── Jack.g4                  # ANTLR4 grammar for Jack language
│
├── docs/                        # DOCUMENTATION (HTML)
│   ├── index.html
│   ├── architecture.html
│   ├── usage.html
│   └── [13 more documentation files]
│
├── requirements.txt             # Python dependencies
├── setup.py                     # Python package configuration
└── antlr-4.13.0-complete.jar   # ANTLR4 complete JAR
```

## Quick Start

### 1. Prerequisites

- **Python** 3.8 or higher
- **Java** JDK 11 or later (required for ANTLR4)
- **pip** (Python package manager)
- **ANTLR4** 4.13.0 (included in repository as `antlr-4.13.0-complete.jar`)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Parser and Lexer (One-time Setup)

```bash
java -jar antlr-4.13.0-complete.jar \
    -Dlanguage=Python3 \
    -visitor \
    -o src/antlr_generated \
    grammar/Jack.g4
```

**Note:** The ANTLR4 JAR is already included in the repository. If you modify `grammar/Jack.g4`, you'll need to run this command again.

### 4. Compile a Jack Program

```bash
# Single file
python src/compiler.py examples/HelloWorld.jack -o HelloWorld.vm

# Directory of Jack files
python src/compiler.py examples/ -o output/

# With custom output
python src/compiler.py program.jack -o output/program.vm
```

### 5. Verify Installation

```bash
# Run unit tests (validates all components)
python -m pytest tests/test_compiler.py -v

# Or using unittest
python tests/test_compiler.py

# Compile and check an example
python src/compiler.py examples/Math.jack -o Math.vm
```

## Installation Details

### Full Setup Instructions

#### Step 1: Clone or Download the Repository

```bash
git clone <your-bitbucket-url>
cd jack-compiler
```

#### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Verify ANTLR4 JAR

The repository includes `antlr-4.13.0-complete.jar`. If you need to download it manually:

```bash
# Download if needed (already in repo)
wget https://www.antlr.org/download/antlr-4.13.0-complete.jar -O antlr-4.13.0-complete.jar
```

#### Step 5: Generate Parser and Lexer

```bash
java -jar antlr-4.13.0-complete.jar \
    -Dlanguage=Python3 \
    -visitor \
    -o src/antlr_generated \
    grammar/Jack.g4
```

The generated files will be created in `src/antlr_generated/grammar/`.

#### Step 6: Verify Installation

```bash
python -m pytest tests/test_compiler.py -v
```

### Troubleshooting

#### Issue: "Java not found" or "java: command not found"
**Solution:** Install Java Development Kit (JDK):
- **macOS**: `brew install openjdk@11`
- **Ubuntu/Debian**: `sudo apt-get install openjdk-11-jdk`
- **Windows**: Download from [oracle.com](https://www.oracle.com/java/technologies/downloads/) or use `choco install openjdk`

#### Issue: "ModuleNotFoundError: No module named 'antlr4'"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

#### Issue: ANTLR4 generated files not found
**Solution:** Regenerate the parser:
```bash
java -jar antlr-4.13.0-complete.jar \
    -Dlanguage=Python3 \
    -visitor \
    -o src/antlr_generated \
    grammar/Jack.g4
```

#### Issue: Tests fail with import errors
**Solution:** Ensure you're in the correct directory and the virtual environment is activated:
```bash
cd jack-compiler
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m pytest tests/test_compiler.py -v
```

## Example Programs

### Example 1: Hello World
```jack
class HelloWorld {
    function void main() {
        do Output.printString("Hello, World!");
        do Output.println();
        return;
    }
}
```

### Example 2: Arithmetic & Variables
```jack
class Math {
    function void main() {
        var int x, y, sum;
        let x = 10;
        let y = 20;
        let sum = x + y;
        do Output.printInt(sum);
        return;
    }
}
```

### Example 3: Loops
```jack
class Loop {
    function void main() {
        var int i, sum;
        let i = 0;
        let sum = 0;
        while (i < 10) {
            let i = i + 1;
            let sum = sum + i;
        }
        do Output.printInt(sum);
        return;
    }
}
```

### Example 4: Object-Oriented Programming
```jack
class Point {
    field int x, y;
    
    constructor Point new(int px, int py) {
        let x = px;
        let y = py;
        return this;
    }
    
    method int getX() {
        return x;
    }
    
    method void dispose() {
        do Memory.deAlloc(this);
        return;
    }
}
```

See `USAGE.md` for more detailed examples and advanced usage.

## Architecture

### Compilation Pipeline

```
Jack Source Code
       ↓
[Lexer] (ANTLR4 generated)
       ↓
Token Stream
       ↓
[Parser] (ANTLR4 generated)
       ↓
Parse Tree
       ↓
[Visitor] Traverses tree, manages symbol table
       ↓
[Code Generator] Emits VM instructions
       ↓
Hack VM Code
```

### Symbol Table Design

Two-level scoping:
- **Class Scope**: Static and field variables (persistent across all subroutines)
- **Subroutine Scope**: Local variables and parameters (reset for each subroutine)

Variables are tracked with:
- Name, type, kind (static/field/local/arg), and index
- Proper handling of implicit 'this' pointer for methods

### Code Generation Strategy

- Stack-based VM architecture
- Direct instruction emission for each language construct
- Label generation for control flow (if/while)
- Proper handling of method calls with implicit 'this'
- String literal generation through character appending

## Testing

Run the comprehensive test suite:

```bash
python tests/test_compiler.py
```

Tests cover:
- Symbol table operations (define, lookup, scoping)
- Code generation (arithmetic, jumps, function calls)
- Type tracking and variable indexing
- Label generation

## Command-Line Usage

```bash
python src/compiler.py [-h] [-o OUTPUT] input

Arguments:
  input                 Input Jack file or directory
  -o, --output OUTPUT   Output VM file or directory (default: same as input)
  -h, --help            Show help message
```

## Supported Jack Language Constructs

### Statements
- `let` - Variable assignment (including array elements)
- `if/else` - Conditional execution
- `while` - Loop execution
- `do` - Subroutine call statements
- `return` - Function return

### Expressions
- Arithmetic: `+` `-` `*` `/`
- Relational: `<` `>` `=`
- Logical: `&` `|` `~`
- Unary: `-` `~`

### Declarations
- Class-level: `static`, `field`
- Subroutine-level: `var`
- Parameters: implicit for methods

### Types
- Primitive: `int`, `boolean`, `String`
- User-defined: class names

### Subroutine Types
- `function` - Static method (no 'this')
- `method` - Instance method (implicit 'this')
- `constructor` - Constructor (returns 'this')

## VM Output Format

Generated code follows the Hack VM specification:
- Memory segments: local, argument, static, this, that, constant, pointer, temp
- Arithmetic: add, sub, neg, mul, div
- Comparison: eq, lt, gt
- Logical: and, or, not
- Control flow: label, goto, if-goto
- Functions: function, call, return

## Performance Characteristics

- **Single Pass Compilation**: Parse tree traversal in one pass
- **Memory Efficient**: Symbol table uses minimal memory
- **Fast Generation**: Direct instruction emission
- **Scalability**: Successfully compiles complex programs with multiple classes and methods

## Integration with Nand2Tetris

1. Compile Jack to VM:
   ```bash
   python src/compiler.py program.jack -o program.vm
   ```

2. Compile VM to Hack ASM (using nand2tetris tools):
   ```bash
   java -jar VMTranslator.jar program.vm
   ```

3. Load in Hack Emulator:
   - Open the generated `.asm` file
   - Run simulation

## References

- **nand2tetris Course**: https://www.nand2tetris.org/
- **Jack Language Spec**: http://nand2tetris.org/chapters/chapter09.pdf
- **Hack VM Spec**: http://nand2tetris.org/chapters/chapter07.pdf
- **ANTLR4 Documentation**: https://www.antlr.org/
- **Terence Parr's ANTLR**: Language implementation with ANTLR4

## License

This implementation is provided for educational purposes as part of the nand2tetris curriculum.

## Contributing

Improvements and enhancements are welcome. This project demonstrates best practices in:
- Compiler design with ANTLR4
- Visitor pattern for AST traversal
- Symbol table management
- Code generation for stack-based VMs
