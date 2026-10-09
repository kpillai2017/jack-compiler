# Error Detection & Handling Guide

## Overview

`jackc` checks every file it compiles and reports problems clearly — per file,
in a final summary, and through its exit status — so scripts, Make and CI can
rely on it. This applies to single files, directories and recursive (`-r`)
builds alike.

## How Errors Are Detected

### 1. Input checks (before compiling)

- The input path must exist, otherwise: `✗ ERROR: Input path not found: <path>`
- A directory must contain `.jack` files (searching sub-directories only with `-r`),
  otherwise: `⚠ WARNING: No .jack files found in <dir>`
- Invalid option combinations are rejected, e.g.
  `jackc: error: --recursive requires a directory as input`

### 2. Lexical and syntax errors (while parsing)

The ANTLR4 lexer and parser report every problem they find in a file — invalid
characters, unterminated strings, missing or unexpected tokens. Their raw
messages are rewritten in plain English, and each one is printed the way GCC,
Clang and rustc do it:

```
<file>:<line>:<column>: error: <message>
 <line> | <the source line>
        |        ^~~~
        = help: <a suggestion, when there is one>
```

Lines and columns are 1-based, so most editors and terminals can jump straight
to the location. A forgotten `;`, `)` or `]` is reported **just after the
token it should follow**, where it was forgotten, not at the start of the next
line. A bad character or unterminated string is reported once; the knock-on
parser errors it causes on the same line are dropped.

### 3. Semantic errors and warnings (after parsing, before generating code)

A file can be grammatically fine and still make no sense. A semantic pass
(`jack_compiler/checker.py`) checks every file before any VM code is generated.

**Errors** stop the file from being compiled:

| Problem | Message |
|---------|---------|
| Undeclared variable | `'cuont' is not declared` + `help: did you mean 'count'?` |
| Declared twice in one scope | `'x' is already declared in this subroutine` + `note: 'x' was first declared here` |
| Two subroutines with one name | `subroutine 'bump' is already defined in class 'Sem'` + note |
| `this` in a function | `'this' can't be used in function 'main'` |
| A field in a function | `field 'count' can't be used in function 'main'` |
| Method called without an object | `can't call method 'draw' from function 'main'` |
| Method called on the class | `'bump' is a method, so it needs an object` |
| Function called like a method (`helper()` or `obj.helper()`) | `'helper' is a function, so call it as 'Main.helper(...)'` |
| Unknown subroutine in this class | `class 'Sem' has no subroutine named 'nope'` |
| Unknown Jack OS subroutine | `the Jack OS class 'Output' has no subroutine named 'printSting'` + `help: did you mean 'printString'?` |
| Wrong number of arguments | `'helper' takes 1 argument but 2 were given` + `note: 'helper' is declared here` (for the OS: `help: the Jack OS declares it as '...'`) |
| Method call on a primitive | `'flag' is a boolean, which has no methods` |
| Integer too big | `integer constant 40000 is too large` + `help: the largest Jack integer is 32767` |
| No `return` at the end | `function 'main' can reach its end without a 'return'` |

The call checks cover this class's own subroutines and the Jack OS (the API
in the book; private helpers of a particular OS, such as `Output.initMap`,
aren't part of it). If the folder has its own `Output.jack`, `Math.jack` etc.
(project 12), that class replaces the OS's and calls into it aren't checked.

A `while` loop whose condition is always true (`true`, `~false`, `~0`, `-1`)
never ends except by `return`, since Jack has no `break`, so nothing is
needed after it: `function void halt() { while (true) {} }` is fine.

**Warnings** are printed but the file still compiles (`-w` hides them,
`--werror` turns them into errors):

| Problem | Message |
|---------|---------|
| Local never used | `unused variable 'y'` |
| Code after `return` | `this code will never run: it comes after 'return'` |
| Void subroutine returns a value | `void method 'bump' returns a value` |
| Non-void subroutine returns nothing | `function 'f' should return a int` |
| Constructor doesn't return `this` | `constructor 'new' should 'return this;'` |
| Class name ≠ file name | `class 'Foo' is in a file named 'Bar.jack'` |
| Class named like an OS class | `class 'Math' has the same name as a Jack OS class` |
| `lowercase.f()` and `lowercase` isn't a variable | `'output' is not a variable, so this calls a class named 'output'` |
| Unknown class name | `there is no class named 'Outptu' in this program` + `help: did you mean 'Output'?` |

A class name (in a type, or before `.` in a call) is known if it is a Jack OS
class or there is a matching `.jack` file in the same folder. Calls into the
program's *other* classes are trusted: their subroutine names and argument
counts aren't checked, because those classes are compiled separately.

Internal compiler bugs are reported as `✗ COMPILATION ERROR`; add `-v` for a
Python traceback to include in a bug report.

### 4. Reporting (after compiling)

- Every file is attempted — one failure does not stop the build
- A summary shows compiled / failed / total counts and lists each failed file
- No `.vm` file is written for a file that fails
- The exit status is non-zero if anything failed

## How You'll Know If There Are Errors

### Per-file result

```
[2/4] ✗ COMPILATION FAILED: src/game/Broken.jack
src/game/Broken.jack:3:17: error: expected an expression, found ';'
 3 |         let x = ;
   |                 ^
src/game/Broken.jack:5:15: error: expected ';' after 'return'
 5 |         return
   |               ^
   = help: every statement and declaration ends with ';'
2 errors generated.
```

A file that compiles with warnings says so, and lists them:

```
✓ SUCCESS (1 warning): src/Main.jack
  → src/Main.vm
src/Main.jack:3:20: warning: unused variable 'y'
 3 |         var int x, y;
   |                    ^
1 warning generated.
```

On a terminal, errors are red, warnings yellow, notes cyan and the `^~~~`
marker green, as in GCC. Colour is off when output is redirected or
`NO_COLOR` is set.

### Summary

**All files compiled:**

```
────────────────────────────────────────────────────────────
Compiled: 3  Failed: 0  Total: 3
✓ ALL COMPILATIONS SUCCESSFUL
════════════════════════════════════════════════════════════
```

**Some files failed:**

```
────────────────────────────────────────────────────────────
Compiled: 3  Failed: 1  Total: 4
✗ SOME COMPILATIONS FAILED
  ✗ src/game/Broken.jack
════════════════════════════════════════════════════════════
```

### Exit status

| Code | Meaning |
|------|---------|
| `0` | Every file compiled successfully (dry run: `.jack` files were found) |
| `1` | A file failed to compile, the input does not exist, or no `.jack` files were found |
| `2` | Invalid command line |

```bash
jackc -r src/
echo $?        # 0 = success, non-zero = failure
```

## Types of Errors

| Category | Reported as | Example cause |
|----------|-------------|---------------|
| Input | `✗ ERROR: Input path not found` | Typo in the path |
| Input | `⚠ WARNING: No .jack files found` | Wrong directory, or forgot `-r` |
| Lexical | `error: invalid character '@' in program`, `error: unterminated string` | `@`, `#`, a string without its closing `"` |
| Syntax | `error: expected ';' after ')'`, `error: expected an expression, found ';'`, `error: unexpected end of file` | Missing `;`, `(`, `}`; keyword used as a name |
| Semantic | `error: 'y' is not declared`, `error: can't call method ...` | See the tables above |
| Warning | `warning: unused variable 'y'` | See the tables above |
| Internal | `✗ COMPILATION ERROR` + message (`-v` for traceback) | Compiler bug |

### What is *not* detected

Jack is weakly typed, so type mismatches (`let x = "text";` for an `int x`)
are not errors. Class names are checked against the folder and the Jack OS,
and calls against this class and the Jack OS API, but calls into the
program's other classes aren't: they are compiled separately, so a wrong
subroutine name or argument count there (`Game.strat()`) shows up when the
program runs in the VM.

## Common Jack Errors

All messages below are real `jackc` output.

### Missing semicolon

```jack
do Output.printInt(1)
return;
```

```
errs/MissingSemi.jack:4:30: error: expected ';' after ')'
 4 |         do Output.printInt(1)
   |                              ^
   = help: every statement and declaration ends with ';'
```

### Missing parentheses around a condition

```jack
if x { let x = 1; }
```

```
errs/IfNoParens.jack:4:11: error: expected '(' after 'if'
 4 |         if x { let x = 1; }
   |           ^
errs/IfNoParens.jack:4:13: error: expected ')' after 'x'
 4 |         if x { let x = 1; }
   |             ^
```

### Unclosed class or subroutine body

```
errs/Unclosed.jack:4:6: error: unexpected end of file: expected '}' or a subroutine declaration
 4 |     }
   |      ^
   = help: check that every '{' has a matching '}'
errs/Unclosed.jack:1:16: note: this '{' is never closed
 1 | class Unclosed {
   |                ^
```

### Keyword used as a name

```
errs/KeywordName.jack:4:17: error: expected a name, found 'class'
 4 |         var int class;
   |                 ^~~~~
```

### Unterminated string

```
errs/BadString.jack:4:31: error: unterminated string
 4 |         do Output.printString("oops);
   |                               ^~~~~~~
   = help: a string must end with '"' on the same line
```

### Undeclared variable (with a suggestion)

```
errs/Sem.jack:14:13: error: 'cuont' is not declared
 14 |         let cuont = 1;
    |             ^~~~~
    = help: did you mean 'count'?
```

### Declared twice

```
errs/Sem.jack:12:17: error: 'x' is already declared in this subroutine
 12 |         var int x;
    |                 ^
errs/Sem.jack:11:17: note: 'x' was first declared here
 11 |         var int x, y;
    |                 ^
```

### Calling a method from a function

```
errs/Calls.jack:4:12: error: can't call method 'draw' from function 'main'
 4 |         do draw(5);
   |            ^~~~
   = help: a function has no object; call it on one, e.g. 'obj.draw(...)'
```

### Wrong number of arguments

```
errs/Sem.jack:18:16: error: 'helper' takes 1 argument but 2 were given
 18 |         do Sem.helper(1, 2);
    |                ^~~~~~
errs/Sem.jack:27:18: note: 'helper' is declared here
 27 |     function int helper(int a) {
    |                  ^~~~~~
```

### Calling the Jack OS wrongly

```
Main.jack:3:19: error: the Jack OS class 'Output' has no subroutine named 'printSting'
 3 |         do Output.printSting("Hi");
   |                   ^~~~~~~~~~
   = help: did you mean 'printString'?
Main.jack:4:19: error: 'drawLine' takes 4 arguments but 3 were given
 4 |         do Screen.drawLine(0, 0, 10);
   |                   ^~~~~~~~
   = help: the Jack OS declares it as 'function void Screen.drawLine(int x1, int y1, int x2, int y2)'
```

### Missing return

```
errs/Sem.jack:29:5: error: function 'helper' can reach its end without a 'return'
 29 |     }
    |     ^
    = help: every Jack subroutine must end with 'return' (use 'return;' in a void one)
```

### Misspelt class name

A warning, so the file still compiles; the VM fails when it reaches the call.
Use `--werror` to make it stop the build.

```
Main.jack:3:12: warning: there is no class named 'Outptu' in this program
 3 |         do Outptu.printInt(1);
   |            ^~~~~~
   = help: did you mean 'Output'?
```

### Empty file

```
errs/Missing.jack:1:1: error: unexpected end of file: expected 'class'
```

## Troubleshooting Errors

1. **Read the first error for each file first.** Later errors are often caused by it.
2. **Follow the `help:` and `note:` lines**: they point at the fix, or at the other place involved (e.g. the first declaration).
3. **Missing `;` or `)`** is reported right after the token it should follow.
4. **Compile the one file** to focus on it: `jackc src/game/Broken.jack`.
5. **Use `--clean`** so a failed file can't leave an old `.vm` behind that the VM Emulator would still load.
6. **Use `-v`** if you see `✗ COMPILATION ERROR` with an unexpected message, and include the traceback in a bug report.
7. **Use `jackc-gui`** to work through many errors: it opens on the first one, Ctrl+E jumps to the next, and Ctrl+R recompiles after you save. See the [compiler window guide](docs/gui.html).

## Integration with Build Systems

Because `jackc` exits non-zero on any failure, no extra checks are needed.

### Make

```makefile
build:
	jackc -r --clean src/ -o build/
```

### GitHub Actions

```yaml
- name: Compile Jack sources
  run: jackc -r --clean src/ -o build/
```

### Shell scripts

```bash
#!/bin/bash
set -e                      # stop the script if jackc fails
jackc -r --clean src/
echo "Build successful!"
```

### Saving a log

```bash
jackc -r src/ > build.log 2>&1
```

All diagnostics go to standard output, and colour is turned off automatically
when output is redirected (or when the `NO_COLOR` environment variable is set).

## FAQ

**Q: Does compilation stop at the first error?**
A: No. Every file is compiled and every error reported, so you can fix them all in one pass.

**Q: Is a `.vm` file produced for a file with errors?**
A: No. If a previous `.vm` exists it is left untouched — use `--clean` to remove it.

**Q: How do I check for success in a script?**
A:

```bash
if jackc -r src/; then
    echo "Success"
else
    echo "Failed"
fi
```

**Q: Can I use the compiler from Python and get the errors?**
A: Yes:

```python
from jack_compiler import JackCompiler, JackSyntaxError, render_diagnostic

compiler = JackCompiler()
try:
    vm_code = compiler.compile_source("Main.jack")
    warnings = compiler.diagnostics           # warnings from a successful compile
except JackSyntaxError as e:                  # also catches JackSemanticError
    for err in e.errors:                      # "file:line:col: error: message"
        print(err)
    for d in e.diagnostics:                   # Diagnostic: .line .column .severity .message .help .notes
        print(render_diagnostic(d, open("Main.jack").read().splitlines()))
```

**Q: Can warnings fail the build?**
A: Yes: `jackc --werror src/` treats every warning as an error. `jackc -w` hides warnings instead.
In the compiler window, start it with `jackc-gui --werror` or press Ctrl+W to switch it on and off;
the STATUS box shows which is in use.

**Q: Where do the messages come from?**
A: Lexical and syntax errors come from the ANTLR4-generated lexer and parser
(`grammar/Jack.g4`), turned into friendlier wording by
`jack_compiler/diagnostics.py`. Semantic errors and warnings come from the
checker (`jack_compiler/checker.py`), which runs before any VM code is
generated.

**Q: Can I see the errors in a window?**
A: Yes: `jackc-gui src/` shows each file with its errors and warnings marked
under the line, the same way `jackc` prints them. Ctrl+E jumps from one to the
next and Ctrl+R recompiles. See the [compiler window guide](docs/gui.html).

## See Also

- [Batch Compilation Guide](docs/batch-compilation.html)
- [Batch Compilation Examples](docs/batch-examples.html)
- [The Compiler Window (`jackc-gui`)](docs/gui.html)
- [Quick Reference](QUICK_REFERENCE.md)
- [Usage Guide](USAGE.md)
- [README](README.md)
