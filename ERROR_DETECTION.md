# Error Detection & Handling Guide

> **Note:** This guide describes the standalone `compile_all.sh` batch script, which is **not
> included in this repository**. For batch compilation use the built-in directory mode:
> `jackc <dir> [-o <outdir>]` (non-recursive; exits non-zero if any file fails). The error
> categories and CI patterns below still apply to `jackc`.

## Overview

**Yes, the batch compilation script thoroughly checks for compilation errors!** Errors are detected at multiple levels and reported clearly so you always know exactly what went wrong.

## How Errors Are Detected

### 1. **Environment Validation** (Before Compilation Starts)

The script checks:
- ✅ Compiler script exists (`jack_compiler/compiler.py`)
- ✅ Python 3 is installed
- ✅ Input directory exists
- ✅ Directory is readable

If any of these fail, the script exits immediately with a clear error message.

### 2. **Compilation Error Capture** (During Compilation)

For each Jack file, the script:
1. Runs the compiler
2. Captures the return code (exit status)
3. Checks if return code indicates success (0) or failure (non-zero)
4. If failure detected, marks file as failed and continues

### 3. **Error Tracking** (Throughout Compilation)

Variables track:
- `COMPILED_FILES` - Successfully compiled files
- `FAILED_FILES` - Files with errors
- `TOTAL_FILES` - Total files processed
- `error_files` - Array of failed filenames

### 4. **Error Reporting** (At Completion)

The script reports:
- Visual indicators (✓ success, ✗ failure)
- Summary statistics (success/failure counts)
- Detailed list of failed files
- Proper exit code (0 for success, 1 for failure)

## How You'll Know If There Are Errors

### Method 1: Visual Indicators in Output

**Success (all files compiled):**
```
ℹ Compiling: .....
✓ All files compiled successfully!
```

**Failure (some files had errors):**
```
ℹ Compiling: .✗..✓.
             ↑
             Red X indicates failed file

✗ Failed to compile: src/broken.jack
```

### Method 2: Summary Section

Always printed at the end:

**Success:**
```
╔════════════════════════════════════════════════════════════════╗
║  Total Files Found:    5                                       ║
║  Successfully Compiled: 5                                       ║
║  Time Elapsed:         1s                                      ║
╚════════════════════════════════════════════════════════════════╝
```

**Failure:**
```
╔════════════════════════════════════════════════════════════════╗
║  Total Files Found:    6                                       ║
║  Successfully Compiled: 5                                       ║
║  Failed:               1                                       ║
║  Time Elapsed:         1s                                      ║
╚════════════════════════════════════════════════════════════════╝
```

### Method 3: Failed Files List

If any compilation fails:

```
✗ The following files failed to compile:
  - src/broken.jack
  - src/invalid.jack
```

### Method 4: Exit Code

Check the shell exit code:

```bash
$ ./compile_all.sh .
$ echo $?
0  ← All files compiled successfully

$ ./compile_all.sh .
$ echo $?
1  ← Some files failed
```

Use in scripts:
```bash
if ./compile_all.sh .; then
    echo "Build successful"
else
    echo "Build failed"
    exit 1
fi
```

### Method 5: Verbose Mode

Use `--verbose` to see each file's status:

```bash
$ ./compile_all.sh . --verbose

ℹ Compiling: src/Main.jack
✓ Compiled: src/Main.jack → src/Main.vm

ℹ Compiling: src/broken.jack
line 4:8 mismatched input 'let' expecting {',', ';'}
Error: Syntax errors in src/broken.jack
✗ Failed to compile: src/broken.jack

ℹ Compiling: src/Game.jack
✓ Compiled: src/Game.jack → src/Game.vm
```

This shows exactly which file fails and often displays the error message from the compiler.

## Types of Errors Detected

### Environment Errors (Before Compilation)

These stop the script immediately:

| Error | Message | Solution |
|-------|---------|----------|
| Compiler missing | `✗ Compiler script not found: jack_compiler/compiler.py` | Install the package (`pip install -e .`) |
| Python missing | `✗ Python 3 is not installed or not in PATH` | Install Python 3 |
| Directory missing | `✗ Directory not found: src/` | Check directory path |

### Jack Syntax Errors (During Compilation)

Caught by the ANTLR4 parser:

```
line 4:8 mismatched input 'let' expecting {',', ';'}
Error: Syntax errors in examples/broken.jack
✗ Failed to compile: examples/broken.jack
```

### Semantic Errors (During Compilation)

Caught during code generation:

```
Error: Undefined variable: unknownVar
Error: Type mismatch in assignment
Error: Invalid operation
```

### File Access Errors (During Compilation)

```
Error: Cannot read input file
Error: Cannot write output file
Error: Permission denied
```

## Practical Examples

### Example 1: Detect Missing Semicolon

**File: broken.jack**
```jack
class Test {
    function void main() {
        var int x     // ← Missing semicolon
        return;
    }
}
```

**Command:**
```bash
$ ./compile_all.sh . --verbose
```

**Output:**
```
ℹ Compiling: examples/broken.jack
line 4:8 mismatched input 'return' expecting {',', ';'}
Error: Syntax errors in examples/broken.jack
✗ Failed to compile: examples/broken.jack
```

### Example 2: Multiple Errors - Find Which Files Fail

**Command:**
```bash
$ ./compile_all.sh .
```

**Output:**
```
ℹ Compiling: .✗.✓.✗.

✗ Failed to compile: src/file1.jack
✗ Failed to compile: src/file3.jack

╔════════════════════════════════════════════════════════════════╗
║  Total Files Found:    6                                       ║
║  Successfully Compiled: 4                                       ║
║  Failed:               2                                       ║
╚════════════════════════════════════════════════════════════════╝

✗ The following files failed to compile:
  - src/file1.jack
  - src/file3.jack
```

Now you know exactly which files to fix!

### Example 3: Check Exit Code in Script

```bash
#!/bin/bash

if ./compile_all.sh src/; then
    echo "✓ Build successful"
    exit 0
else
    echo "✗ Build failed - check errors above"
    exit 1
fi
```

### Example 4: Log to File for Later Review

```bash
$ ./compile_all.sh . --verbose > build.log 2>&1

$ # Check what failed
$ grep "Failed to compile" build.log
Failed to compile: src/broken.jack

$ # See the error
$ grep -A 2 "Failed to compile: src/broken.jack" build.log
```

## Troubleshooting Errors

### Step 1: Identify the Problem

Run with verbose mode to see which file fails:
```bash
./compile_all.sh . --verbose
```

Look for lines like:
```
✗ Failed to compile: src/broken.jack
```

### Step 2: Examine the Error Message

The script shows the compiler's error message:
```
line 4:8 mismatched input 'let' expecting {',', ';'}
```

This tells you:
- **line 4, column 8** - Where the error is
- **Expected `{',', ';'}`** - What was expected
- **Found `'let'`** - What was actually there

### Step 3: Check the File

Look at the problematic file around that line:
```bash
$ cat -n src/broken.jack | grep -A 2 "4"
     3     function void main() {
     4         var int x
     5         let x = 5;
```

The error says a semicolon is expected after `var int x`

### Step 4: Fix the Syntax

Add the missing semicolon:
```jack
var int x;  // ← Added semicolon
```

### Step 5: Recompile

```bash
$ ./compile_all.sh .
```

If fixed, you'll see:
```
✓ All files compiled successfully!
```

## Common Jack Syntax Errors

### Missing Semicolon
```jack
var int x       // ✗ Missing semicolon
var int x;      // ✓ Correct
```

### Unmatched Braces
```jack
function void test() {
    return;
}               // ✗ Missing closing brace

function void test() {
    return;
}               // ✓ Correct
```

### Invalid Variable Name
```jack
let 123x = 5;   // ✗ Variable name can't start with number
let x123 = 5;   // ✓ Correct
```

### Missing Type
```jack
var x;          // ✗ Missing type
var int x;      // ✓ Correct
```

### Invalid Operator
```jack
let x = 5 ** 2;     // ✗ ** is not valid
let x = 5 * 2;      // ✓ Use single *
```

## Error Detection in the Script (Code Reference)

### Return Code Capture
```bash
if python3 "$COMPILER_SCRIPT" "$jack_file" -o "$vm_file" 2>&1; then
    ((COMPILED_FILES++))  # Success
else
    ((FAILED_FILES++))    # Failure
    error_files+=("$jack_file")
fi
```

### Summary Generation
```bash
║  Total Files Found:    $TOTAL_FILES
║  Successfully Compiled: $COMPILED_FILES
║  Failed:               $FAILED_FILES
```

### Exit Code
```bash
if [ ${#error_files[@]} -gt 0 ]; then
    exit 1  # Failure
else
    exit 0  # Success
fi
```

## Integration with Build Systems

### With Make

```makefile
compile:
	./compile_all.sh src/
	@if [ $$? -ne 0 ]; then \
		echo "Compilation failed"; \
		exit 1; \
	fi
```

### With GitHub Actions

```yaml
- name: Compile Jack Files
  run: |
    ./compile_all.sh src/
    if [ $? -ne 0 ]; then
      echo "Compilation failed"
      exit 1
    fi
```

### With Shell Scripts

```bash
#!/bin/bash
set -e  # Exit on first error

echo "Compiling..."
./compile_all.sh src/ --clean

echo "Build successful!"
```

## FAQ

**Q: Will the script stop on first error?**
A: No, it continues compiling all files and reports all errors at the end. This way you see all problems at once.

**Q: How do I see the actual error message?**
A: Use `--verbose` flag to see each file and its error message.

**Q: Can I check if compilation succeeded in a script?**
A: Yes, check the exit code:
```bash
if ./compile_all.sh .; then
    echo "Success"
else
    echo "Failed"
fi
```

**Q: What if one file fails but others succeed?**
A: The script generates .vm files for successful compilations. The summary shows how many failed. You can fix the broken files and recompile.

**Q: How do I get detailed error information?**
A: Run the single file directly with the compiler:
```bash
jackc src/broken.jack -o test.vm
```

**Q: Where are the error messages coming from?**
A: The Jack compiler itself (ANTLR4 parser + visitor) reports syntax and semantic errors. The batch script captures and displays them.

## Summary

✅ **Error Detection: Comprehensive**
- Environment validation
- Return code capture
- Error tracking and reporting
- Clear error messages
- Proper exit codes

✅ **How You Know About Errors:**
1. Visual red X (✗) in output
2. "Failed to compile" messages
3. Summary section shows failed count
4. List of failed files at end
5. Exit code 1 (can check with $?)

✅ **Error Details Available:**
- Run with `--verbose` for each file
- Check exit code with `echo $?`
- Save to log file for review
- Run single file directly for full details

**The script won't hide errors - they're clearly reported!**
