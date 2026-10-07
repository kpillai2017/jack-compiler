# Jack Compiler Usage Guide

## Quick Start

### 1. Installation

```bash
# Navigate to the jack-compiler directory
cd jack-compiler

# Run setup script (downloads ANTLR4 and generates parser)
pip install -e ".[dev]"

# Or manually install dependencies
pip install -r requirements.txt
```

### 2. Compile a Single File

```bash
jackc program.jack -o program.vm
```

### 3. Compile a Directory

```bash
jackc src_dir/ -o bin_dir/
```

### 4. In-place Compilation

```bash
jackc src_dir/
```

This will generate `.vm` files in the same directory as the `.jack` files.

## Command Line Options

```
usage: jackc [-h] [-o OUTPUT] [-v] [--version] input

Jack compiler for nand2tetris Hack computer

positional arguments:
  input                 Input Jack file or directory

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output VM file or directory (default: same as input)
```

## Examples

### Example 1: Simple Function

**Input (main.jack):**
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

**Output (main.vm):**
```vm
function Main.main 1
push constant 5
pop local 0
push local 0
call Output.printInt 1
pop temp 0
push constant 0
return
```

### Example 2: Variable Declaration and Arithmetic

**Input (calc.jack):**
```jack
class Calc {
    function void main() {
        var int a, b, sum;
        let a = 10;
        let b = 20;
        let sum = a + b;
        do Output.printInt(sum);
        return;
    }
}
```

**Output (calc.vm):**
```vm
function Calc.main 3
push constant 10
pop local 0
push constant 20
pop local 1
push local 0
push local 1
add
pop local 2
push local 2
call Output.printInt 1
pop temp 0
push constant 0
return
```

### Example 3: Control Flow - While Loop

**Input (loop.jack):**
```jack
class Loop {
    function void main() {
        var int i;
        let i = 0;
        while (i < 10) {
            do Output.printInt(i);
            let i = i + 1;
        }
        return;
    }
}
```

**Output (loop.vm):**
```vm
function Loop.main 1
push constant 0
pop local 0
label WHILE$0
push local 0
push constant 10
lt
not
if-goto ENDWHILE$1
push local 0
call Output.printInt 1
pop temp 0
push local 0
push constant 1
add
pop local 0
goto WHILE$0
label ENDWHILE$1
push constant 0
return
```

### Example 4: Control Flow - If Statement

**Input (conditional.jack):**
```jack
class Conditional {
    function void main() {
        var int x;
        let x = 5;
        if (x > 0) {
            do Output.printString("positive");
        } else {
            do Output.printString("non-positive");
        }
        return;
    }
}
```

### Example 5: Class with Methods and Fields

**Input (point.jack):**
```jack
class Point {
    field int x, y;
    
    constructor Point new(int px, int py) {
        let x = px;
        let y = py;
        return this;
    }
    
    method void setX(int val) {
        let x = val;
        return;
    }
    
    method int getX() {
        return x;
    }
}
```

### Example 6: Arrays

**Input (array.jack):**
```jack
class Array {
    function void main() {
        var Array arr;
        var int i;
        
        let arr = Array.new(10);
        let arr[0] = 42;
        let i = arr[0];
        
        do Output.printInt(i);
        return;
    }
}
```

### Example 7: String Literals

**Input (strings.jack):**
```jack
class Strings {
    function void main() {
        var String msg;
        let msg = "Hello, World!";
        do Output.printString(msg);
        do Output.println();
        return;
    }
}
```

## Supported Jack Language Features

### Data Types
- `int` - 16-bit integer
- `boolean` - true or false
- `String` - string literals
- Custom class types (user-defined classes)

### Variable Kinds
- `static` - class-level static variables
- `field` - instance variables
- `var` - local variables (in methods/functions)
- Implicit parameters for methods

### Operators
- Arithmetic: `+`, `-`, `*`, `/`
- Comparison: `<`, `>`, `=`
- Logical: `&`, `|`, `~`
- Unary: `-`, `~`

### Statements
- `let` - variable assignment and array element assignment
- `if/else` - conditional execution
- `while` - loops
- `do` - subroutine calls (statements)
- `return` - function return

### Subroutines
- `function` - static method (no implicit this)
- `method` - instance method (implicit this as first parameter)
- `constructor` - constructor method (returns new instance)

### Other Features
- Single-dimensional arrays with `[]` notation
- String literals with escape sequences (basic support)
- Comments: `//` and `/* */`
- Field and local variable declarations

## Compilation Process

1. **Lexical Analysis**: ANTLR4 tokenizes the input
2. **Syntax Analysis**: ANTLR4 parses tokens according to the grammar
3. **Semantic Analysis**: Symbol table tracks variable definitions and scopes
4. **Code Generation**: Converts parse tree to VM instructions

## Symbol Table Management

The compiler maintains two symbol tables:
- **Class scope**: Static and field variables
- **Subroutine scope**: Local variables and parameters

When a new subroutine is encountered, the subroutine-level scope is reset while class-level scope persists.

## VM Code Output Format

The generated VM code follows the Hack Virtual Machine specification:
- `push [segment] [index]` - Push value onto stack
- `pop [segment] [index]` - Pop stack into memory
- `add`, `sub`, `neg`, `mul`, `div` - Arithmetic
- `eq`, `lt`, `gt` - Comparisons
- `and`, `or`, `not` - Logical operations
- `label [name]` - Label definition
- `goto [label]` - Unconditional jump
- `if-goto [label]` - Conditional jump
- `call [function] [num_args]` - Subroutine call
- `return` - Function return
- `function [name] [num_locals]` - Function definition

## Troubleshooting

### "No module named jack_compiler.antlr_generated..."
Solution: The generated parser is committed to the repo. If it was deleted, regenerate it:
`java -jar antlr-4.13.0-complete.jar -Dlanguage=Python3 -visitor -o jack_compiler/antlr_generated grammar/Jack.g4`

### Syntax Errors
The compiler will report syntax errors from the ANTLR parser. Check your Jack code for:
- Missing semicolons
- Unmatched braces
- Invalid keywords
- Type mismatches

### Undefined Variable Errors
Ensure variables are declared before use in the appropriate scope:
- Use `var` for local variables
- Use `field` for instance variables
- Use `static` for class variables

### File Not Found
Ensure the input file path is correct and the file exists

## Testing

Run the included test suite:

```bash
pytest -v
```

This tests:
- Symbol table operations
- Code generation
- Variable scoping
- Type tracking

## Integration with Hack Emulator

1. Compile your Jack program to VM code:
   ```bash
   jackc myprogram.jack -o myprogram.vm
   ```

2. Use the Hack VM translator to convert VM code to machine code:
   ```bash
   java -jar VMTranslator.jar myprogram.vm
   ```

3. Load the resulting `.asm` file into the Hack Emulator and run

## Advanced Usage

### Processing Multiple Files

```bash
# Compile all Jack files in a directory
jackc src/ -o compiled/

# This will preserve the directory structure
```

### Using as a Library

```python
from jack_compiler import JackCompiler

compiler = JackCompiler()
compiler.compile_file("input.jack", "output.vm")
```

## References

- nand2tetris Course: https://www.nand2tetris.org/
- Jack Language Specification: http://nand2tetris.org/chapters/chapter09.pdf
- Hack Virtual Machine: http://nand2tetris.org/chapters/chapter07.pdf
- ANTLR4 Documentation: https://www.antlr.org/

## License

This implementation is provided as-is for educational purposes in the nand2tetris course.
