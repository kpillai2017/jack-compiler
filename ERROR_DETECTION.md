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
characters, unterminated strings, missing or unexpected tokens. All of them are
collected and printed beneath the failing file as:

```
<file>:<line>:<column>: <message>
```

Lines and columns are 1-based, so most editors and terminals can jump straight
to the location.

### 3. Semantic errors (while generating code)

Some errors are only found while generating VM code — for example using a
variable that was never declared. These are reported as
`✗ COMPILATION ERROR` with a short message. Add `-v` to also print a Python
traceback, which is useful when reporting a compiler bug.

### 4. Reporting (after compiling)

- Every file is attempted — one failure does not stop the build
- A summary shows compiled / failed / total counts and lists each failed file
- No `.vm` file is written for a file that fails
- The exit status is non-zero if anything failed

## How You'll Know If There Are Errors

### Per-file result

```
[2/4] ✗ COMPILATION FAILED: src/game/Broken.jack
  2 syntax error(s):
  src/game/Broken.jack:3:17: mismatched input ';' expecting {'true', 'false', 'null', 'this', '-', '~', '(', INTEGER, STRING_LITERAL, IDENTIFIER}
  src/game/Broken.jack:5:5: mismatched input '}' expecting {'true', 'false', 'null', 'this', '-', '~', ';', '(', INTEGER, STRING_LITERAL, IDENTIFIER}
```

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
| Lexical | `token recognition error at: ...` | `@`, `#`, unterminated string |
| Syntax | `mismatched input ...`, `missing ... at ...`, `extraneous input ...` | Missing `;`, `(`, `}`; keyword used as a name |
| Semantic | `✗ COMPILATION ERROR` + message | Undeclared variable |
| Internal | `✗ COMPILATION ERROR` + message (`-v` for traceback) | Compiler bug |

### What is *not* detected

`jackc` follows the Jack grammar, which does not require every subroutine to end
with `return`. A missing `return` therefore compiles, and only fails when the
program runs in the VM Emulator. Type mismatches are likewise not checked —
Jack is weakly typed.

## Common Jack Syntax Errors

All messages below are real `jackc` output.

### Missing semicolon

```jack
do Output.printInt(1)
return;
```

```
errs/MissingSemi.jack:4:9: extraneous input 'return' expecting ';'
```

The error is reported at the *next* token, so look at the end of the previous line.

### Missing parentheses around a condition

```jack
if x { let x = 1; }
```

```
errs/IfNoParens.jack:4:12: missing '(' at 'x'
errs/IfNoParens.jack:4:14: missing ')' at '{'
```

### Unclosed class or subroutine body

```
errs/Unclosed.jack:5:1: extraneous input '<EOF>' expecting {'constructor', 'function', 'method', '}'}
```

`<EOF>` (end of file) in a message usually means a missing `}`.

### Keyword used as a name

```jack
var int class;
```

```
errs/KeywordName.jack:3:17: mismatched input 'class' expecting IDENTIFIER
```

### Unterminated string

```jack
do Output.printString("oops);
```

```
errs/BadString.jack:3:31: token recognition error at: '"oops);\n'
errs/BadString.jack:4:9: mismatched input 'return' expecting {...}
```

Fix the first error first — later ones are often a knock-on effect.

### Undeclared variable

```jack
let y = 1;     // y was never declared with var/field/static
```

```
✗ COMPILATION ERROR: errs/Undeclared.jack
  Undefined variable: y
```

### Empty file

```
errs/Missing.jack:1:1: mismatched input '<EOF>' expecting 'class'
```

## Troubleshooting Errors

1. **Read the first error for each file first.** Later errors are often caused by it.
2. **Check the line before** the reported position for missing `;` or `)`.
3. **Compile the one file** to focus on it: `jackc src/game/Broken.jack`.
4. **Use `--clean`** so a failed file can't leave an old `.vm` behind that the VM Emulator would still load.
5. **Use `-v`** if you see `✗ COMPILATION ERROR` with an unexpected message, and include the traceback in a bug report.

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
from jack_compiler import JackCompiler, JackSyntaxError

try:
    vm_code = JackCompiler().compile_source("Main.jack")
except JackSyntaxError as e:
    for err in e.errors:          # "file:line:col: message"
        print(err)
```

**Q: Where do the messages come from?**
A: Lexical and syntax errors come from the ANTLR4-generated lexer and parser
(`grammar/Jack.g4`); semantic errors come from the code-generating visitor.

## See Also

- [Batch Compilation Guide](docs/batch-compilation.html)
- [Batch Compilation Examples](docs/batch-examples.html)
- [Usage Guide](USAGE.md)
- [README](README.md)
