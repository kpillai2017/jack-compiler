# Jack Compiler - Quick Reference

## Installation

```bash
cd jack-compiler
pip install -e ".[dev]"
```

## Basic Usage

```bash
# Compile single file
jackc input.jack -o output.vm

# Compile directory
jackc src_dir/ -o out_dir/

# In-place compilation
jackc src_dir/
```

## Compiler Window (`jackc-gui`)

```bash
pip install -e ".[gui]"          # adds pygame
jackc-gui                        # pick a file or folder in a window
jackc-gui src_dir/               # compile and show Jack + VM side by side
jackc-gui --no-write src_dir/    # preview only
```

| Key | Action |
|-----|--------|
| Ctrl+E | Next error or warning |
| Ctrl+R | Recompile (after saving in your editor) |
| Ctrl+I | Show / hide messages under the code |
| Ctrl+W | Warnings count as errors (`--werror`) on / off |
| Ctrl+Tab, 1–9, click a tab | Switch file |
| Tab | Switch pane (Jack / VM) |
| Ctrl+J | Run the program in JackVM ([jackvm-py](https://github.com/kpillai2017/jackvm-py), if installed) |
| Ctrl+O | Open something else |
| Ctrl+D | Show / hide info panel |
| Ctrl+Q, or Esc (hold 1 s while compiling) | Quit |

Full guide: [docs/gui.html](docs/gui.html)

## Run Tests

```bash
pytest -v
```

## Jack Language Syntax

### Variable Declaration

```jack
var int x;              // Local variable
var int x, y, z;        // Multiple declaration

field int x;            // Instance variable
field String name;      // Field with type

static int count;       // Class variable
static boolean flag;    // Static variable
```

### Data Types

```jack
int         // 16-bit integer
boolean     // true or false
String      // String literal
ClassName   // Custom class type
```

### Statements

```jack
let x = 5;                      // Assignment
let arr[i] = x + 1;             // Array assignment

if (x > 0) {                    // If statement
    do Output.printInt(x);
} else {
    do Output.printString("neg");
}

while (i < 10) {                // While loop
    let i = i + 1;
}

do Output.printInt(x);          // Subroutine call

return;                         // Return (no value)
return x + 1;                   // Return (with value)
```

### Expressions

```jack
x + y                   // Addition
x - y                   // Subtraction
x * y                   // Multiplication
x / y                   // Division
x & y                   // Bitwise AND
x | y                   // Bitwise OR
x < y                   // Less than
x > y                   // Greater than
x = y                   // Equal
~x                      // Bitwise NOT
-x                      // Negation
```

### Subroutines

```jack
// Function (static method)
function void doSomething() {
    var int x;
    let x = 5;
    return;
}

// Method (instance method)
method void doSomething() {
    let x = 5;          // Access fields via implicit 'this'
    return;
}

// Constructor
constructor Point new(int px, int py) {
    let x = px;
    let y = py;
    return this;
}

// Subroutine call
do Output.printInt(42);
do point.setX(10);
let result = Math.abs(-5);
```

### Classes

```jack
class Point {
    field int x, y;
    static int count;
    
    constructor Point new(int px, int py) {
        let x = px;
        let y = py;
        let count = count + 1;
        return this;
    }
    
    method int getX() {
        return x;
    }
    
    function int distance(Point p1, Point p2) {
        // Static method
        return 0;
    }
}
```

### Arrays

```jack
var Array arr;
let arr = Array.new(10);        // Create array
let arr[0] = 42;                // Set element
let x = arr[0];                 // Get element
do arr.dispose();               // Free memory
```

### Strings

```jack
var String msg;
let msg = "Hello, World!";
do Output.printString(msg);
do Output.println();
```

### Comments

```jack
// Single-line comment

/* Multi-line
   comment */
```

## Operator Precedence

(Highest to Lowest)
1. Unary: `-`, `~`
2. Multiplicative: `*`, `/`
3. Additive: `+`, `-`
4. Relational: `<`, `>`, `=`
5. Logical AND: `&`
6. Logical OR: `|`

Use parentheses for clarity:
```jack
let x = (a + b) * (c - d);
```

## Common Patterns

### Loop with Counter

```jack
var int i;
let i = 0;
while (i < 10) {
    do Output.printInt(i);
    let i = i + 1;
}
```

### Method Call Chain

```jack
let point = Point.new(5, 10);
do point.setX(20);
let x = point.getX();
do point.dispose();
```

### Array Processing

```jack
var Array arr;
var int i, sum;

let arr = Array.new(5);
let i = 0;
let sum = 0;

while (i < 5) {
    let sum = sum + arr[i];
    let i = i + 1;
}

do Output.printInt(sum);
```

### Conditional Logic

```jack
if (x > 0) {
    if (x < 10) {
        do Output.printString("small");
    } else {
        do Output.printString("large");
    }
} else {
    do Output.printString("non-positive");
}
```

### Memory Management

```jack
// Create object
let point = Point.new(1, 2);

// Use object
do point.setX(5);

// Free memory
do point.dispose();
```

## Built-in Classes (Standard Library)

The Hack OS provides these classes:

### Math
```jack
Math.abs(x)
Math.multiply(x, y)
Math.divide(x, y)
Math.min(x, y)
Math.max(x, y)
Math.sqrt(x)
```

### String
```jack
String.new(length)
str.appendChar(char)
str.length()
str.charAt(i)
str.setCharAt(i, c)
String.backSpace()
String.doubleQuote()
```

### Array
```jack
Array.new(size)
arr.length()      // Via indexing, use external tracking
arr.dispose()
```

### Output
```jack
Output.printChar(char)
Output.printString(str)
Output.printInt(i)
Output.println()
Output.backSpace()
```

### Screen
```jack
Screen.clearScreen()
Screen.setColor(isBlack)
Screen.drawPixel(x, y)
Screen.drawLine(x1, y1, x2, y2)
Screen.drawRectangle(x1, y1, x2, y2)
Screen.drawCircle(x, y, r)
```

### Memory
```jack
Memory.alloc(size)
Memory.deAlloc(obj)
Memory.peek(address)
Memory.poke(address, value)
```

### Keyboard
```jack
Keyboard.keyPressed()
Keyboard.readChar()
Keyboard.readLine(msg)
Keyboard.readInt(msg)
```

### Sys
```jack
Sys.init()
Sys.halt()
Sys.wait(duration)
Sys.error(code)
```

## Symbol Table Scopes

### Class Scope
- **static** variables: persistent across methods
- **field** variables: instance variables (one per object)

### Method Scope
- **var** variables: local variables
- **argument** variables: parameters
- **this** implicit pointer: current object

## Memory Segments

```
local       - Subroutine local variables
argument    - Function parameters
static      - Class-level static variables
this        - Current object (field variables via this[i])
that        - Auxiliary (array elements)
temp        - Temporary storage
constant    - Constant values
pointer     - Pointer 0 (this), Pointer 1 (that)
```

## Common Errors

```
File.jack:LINE:COL: error: expected ';' after ')'
 LINE |         do Output.printInt(1)
      |                              ^
→ The ^ marks the exact spot; add the missing ';' there

File.jack:LINE:COL: error: 'x' is not declared
      = help: did you mean 'y'?
→ Declare the variable with var, field, or static (or fix the typo)

File.jack:LINE:COL: error: invalid character '@' in program / unterminated string
→ Remove the invalid character / close the string literal

File.jack:LINE:COL: warning: unused variable 'y'
→ Compiles anyway; -w hides warnings, --werror makes them errors
```

See ERROR_DETECTION.md for every error and warning.

Not detected at compile time (Jack is weakly typed, and the program's other
classes are compiled separately): type mismatches, and wrong subroutine names
or argument counts in calls to the program's *other* classes. Calls within a
class and calls into the Jack OS are checked. The rest surface when the
program runs in the VM Emulator. See [ERROR_DETECTION.md](ERROR_DETECTION.md).

## File Organization

```
project/
├── Main.jack          // Entry point
├── Point.jack         // Other classes
└── Util.jack
```

Compile all at once:
```bash
jackc project/ -o output/
```

## VM Output Format

Jack compiles to Hack VM code:

```vm
function ClassName.methodName numLocals
push constant 5
pop local 0
push local 0
call Output.printInt 1
pop temp 0
push constant 0
return
```

## Testing Your Programs

1. **Syntax Check**: Compiler will report syntax errors
2. **Logic Check**: Manually test with Output.printInt()
3. **Full Test**: Run in Hack Emulator after VM translation

## Integration with nand2tetris Tools

```bash
# 1. Compile Jack to VM
jackc program.jack -o program.vm

# 2. Translate VM to Hack Assembly
java -jar VMTranslator.jar program.vm

# 3. Run in Hack Emulator
# Open program.asm in the emulator
```

## Performance Tips

- Use `static` for class-level constants
- Minimize variable scope (local vs field)
- Cache frequently accessed values
- Use arrays for bulk data

## More Resources

- Full Documentation: See README.md
- Usage Guide: See USAGE.md
- Error messages: See [ERROR_DETECTION.md](ERROR_DETECTION.md)
- Compiler window: See [docs/gui.html](docs/gui.html)
- Architecture: See ARCHITECTURE.md
- Examples: See examples/ directory

---

**Quick Command Reference**

| Task | Command |
|------|---------|
| Setup | `pip install -e ".[dev]"` |
| Compile file | `jackc in.jack -o out.vm` |
| Compile dir | `jackc src/ -o bin/` |
| Run tests | `pytest -v` |
| View help | `jackc -h` |
| Compile in a window | `jackc-gui src/` |
