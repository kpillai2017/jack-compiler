# Extended Jack: one program, four lessons

This lesson uses [Main.jack](Main.jack) to connect syntax, execution order, and VM
behaviour. First read standard Jack's five statements (`let`, `if`, `while`, `do`,
`return`); the extensions are conveniences built on that foundation, not a change
to the Hack VM instruction set.

## 1. Compile and run

From the **jack-compiler repository root**, with the package installed:

```bash
jackc --extensions teaching/extensions/Main.jack -o build/extensions/Main.vm
```

If the companion `jackvm-py` is installed, run the generated VM (not the Jack
source, since automatic source compilation may use standard mode):

```bash
jackvm build/extensions/Main.vm
# Alternatively, display an ASCII rendering of the pixel screen:
jackvm --headless --ticks 300000 build/extensions/Main.vm
```

Headless output is a pixel-screen rendering plus execution status, not a plain
text transcription of `Output.printString`. The graphical VM is easiest for
reading the displayed lesson output.

The Python equivalent is:

```python
from jack_compiler.compiler import JackCompiler

JackCompiler(extensions=True).compile_file(
    "teaching/extensions/Main.jack", "build/extensions/Main.vm"
)
```

The compiler GUI currently uses standard mode. Without `--extensions` the source
is intentionally rejected. This lesson lives outside `examples/` so the standard
example batch remains valid.

## 2. Predict the result before running

The screen should show:

```text
Extensions "lab" \ A
total = 31
processed = 5
index calls = 5
flags = 3
state = 6
finished
```

The first loop clears the array. The scoring loop then behaves as follows:

| `i` | Action | Score added | Running total | Processed |
|---:|---|---:|---:|---:|
| 0 | process | 1 | 1 | 1 |
| 1 | process | 3 | 4 | 2 |
| 2 | `continue` | — | 4 | 2 |
| 3 | process | 7 | 11 | 3 |
| 4 | process | 9 | 20 | 4 |
| 5 | process | 11 | 31 | 5 |
| 6 | `break` | — | 31 | 5 |
| 7 | never reached | — | 31 | 5 |

`countIndex(i)` increments a counter and returns `i`. Five processed rows mean
five calls. If a compiler naively translated `a[f()] += x` into an assignment
that called `f()` twice, this count would be ten: a concrete reason to preserve
single evaluation.

## 3. Group 1 — literals and comparisons

- `0x0F` is hexadecimal 15; `0b0010` is binary 2. These are alternate spellings of
  integer literals, not different numeric types. Literal magnitudes remain
  0–32767; negative values use unary minus.
- `'A'` is the character code 65. A character literal represents one character;
  `"A"` allocates a String object instead.
- `\"` places a quote in a string and `\\` places a backslash. `\n`, `\r`, `\t`,
  `\b`, `\f`, `\0`, and `\'` are also decoded in extension mode. Unknown escapes
  are errors. Use `Output.println()` for line breaks in this lesson: decoding
  `\n` does not guarantee an OS will display it as a newline.
- `<=`, `>=`, and `!=` produce Jack booleans: true is **-1**, false is **0**.

**Precedence trap:** Jack still evaluates binary operators left to right.
`1 + 2 * 3` means `(1 + 2) * 3`, yielding 9, not 7. Group explicitly when needed.
The score `(i * 2) + BONUS` makes the intent visible.

**Standard-mode distinction:** backslashes in strings are literal in standard
Jack. Enabling extensions can therefore change the meaning of an existing
string containing backslashes; review such strings before switching modes.

## 4. Group 2 — initialisers and compound assignment

`var Array scores = Array.new(CAPACITY);` declares a local and executes its
initialiser once on entry. Local initialisers run in source order, after method
`this` setup or constructor allocation, and before the statements. Constants
are resolved at compile time and have no initialisation side effects.

Locals retain subroutine scope and must be declared at its start. All local slots
start at zero; an initialiser that reads a later local sees zero, not that local's
eventual initialiser. Prefer earlier declarations for dependencies. This does
**not** mean newly allocated array contents are zeroed: the example clears them.

| Extended assignment | Meaning for a simple variable |
|---|---|
| `let total += x;` | `let total = total + x;` |
| `let total -= x;` | `let total = total - x;` |
| `let total *= x;` | `let total = total * x;` |
| `let total /= x;` | `let total = total / x;` |
| `let flags &= mask;` | `let flags = flags & mask;` |
| `let flags |= bits;` | `let flags = flags | bits;` |

For arrays, that textual expansion is unsafe if it duplicates an index call.
The implementation evaluates the target address once, reads the old value, then
evaluates the right-hand side. It preserves the address and old value on the VM
stack, since a right-hand-side call can overwrite temporary/pointer segments.

Here `2 | 1` becomes 3, then `3 & 15` remains 3. `&` and `|` are bitwise,
**not short-circuit** operators. Multiplication/division use existing OS calls.

## 5. Group 3 — loops and control flow

```jack
for (let i = 0; i < limit; let i += 1) {
    // body
}
```

Execution is **initialise once → test → body → update → test again**.
The header's `let` keywords are optional. Each header assignment is a single
assignment, not a declaration or comma-separated list. Declare `i` beforehand.
Any clause may be empty; `for (;;) { ... }` has no condition and repeats until a
`break` or `return` (if any).

- `continue` in a `for` loop jumps to its update, then tests the condition.
- `continue` in a `while` loop jumps straight to its condition.
- `break` leaves the innermost loop without running a for-loop update.
- `return` leaves the subroutine; it is not another spelling of `break`.
- Nested controls target only the innermost loop. Controls outside loops are
  errors; unreachable statements after them are warned about in extension mode.

The countdown loop goes 3 → 2 (`continue`) → 1 → 0 (`break`). Its decrement must
come before the skip, otherwise a skipped iteration can prevent progress.
Conditions use Jack booleans, not an arbitrary-integer truthiness convention.
An endless loop with a reachable break needs a return on paths after the loop;
an endless loop without an exit cannot reach the subroutine's end.

## 6. Group 4 — constants and enums

```jack
const int CAPACITY = 8, STOP_AT = 6;
enum State { READY, ACTIVE = 5, DONE }
```

Constants have `int`, `char`, or `boolean` type and cannot be assigned or indexed.
Class constants and subroutine constants consume no field, static, or local
slots. References are compiled into literal pushes. `Main.CAPACITY` explicitly
selects a class constant if a local shadows its bare name.

Enum members are scoped integer names: `State.READY = 0`, `State.ACTIVE = 5`,
`State.DONE = 6`. An explicit value resets numbering; later members increment.
Enums are **not distinct types**, and members must be qualified (`State.DONE`,
not `DONE`). They are not objects or callable methods.

Compile-time expressions support grouping, unary `-`/`~`, existing binary
operators, characters, booleans, and other constants/members. Forward references
are allowed; cycles, runtime values/calls, strings, `null`, `this`, and division
by zero are rejected. Arithmetic follows left-to-right signed 16-bit wrapping;
division truncates toward zero. Booleans must be 0/-1, chars 0–32767. An implicit
enum increment past 32767 is an error.

Scope limits: declarations and references are in the current source class only;
there are no cross-file exports or enum types. `const` and `enum` (like `for`,
`break`, and `continue`) are reserved only in extension mode.

## 7. Connect the lesson to VM code

Inspect `build/extensions/Main.vm`:

- Constant/enum references become `push constant` instructions. Negative values
  additionally use `neg` or `not`; no constant storage is allocated.
- `<=` becomes `gt` followed by `not`; `>=` becomes `lt` then `not`; `!=` becomes
  `eq` then `not`.
- A `for` loop has condition, update, and end labels. `continue` targets the update
  label, while `break` targets the end label.
- Array compound updates retain the address beneath the value on the stack.
- Initialisers are assignments following the `function` entry/prologue.

No VM instruction was added. Allocation and disposal still use the ordinary OS:
`Array.new` and `scores.dispose()`.

## 8. Exercises (with checkpoints)

1. Set `SKIP_AT` to 3. Predict first, then run: total **29**, processed **5**, index
   calls **5**. Explain why the removed score is 7 rather than 5.
2. Set `STOP_AT` to 4 (leave `SKIP_AT = 2`): total **11**, processed **3**, calls
   **3**. Why does the update not run when `i = 4` breaks?
3. Remove the `continue` condition: total **36**, processed **6**, calls **6**.
4. Change `ACTIVE = 5` to `ACTIVE = 10`: `DONE` and the final state become **11**.
5. Attempt `let CAPACITY = 9;`, `const int BAD = Main.countIndex(0);`, or put
   `break;` outside a loop. Identify why each must be a compile-time error.
6. Translate the scoring loop into standard `while` plus flags. Compare the
   boilerplate, especially the update needed on the skipped path.

## 9. Verification

From the compiler repository root:

```bash
python3 -m pytest tests/test_teaching_extensions.py -q
```

The compilation, standard-mode rejection, and documentation/source consistency
checks always run. Runtime checks require the optional companion `jackvm-py`:

```bash
# When the sibling repository is present:
PYTHONPATH="../jackvm-py" python3 -m pytest tests/test_teaching_extensions.py -q
```

Runtime tests read the five `Main` static results after the VM halts. Do not use
the stack top as `Main.main`'s result: `Sys.init` discards the return value and
then halts. The lesson prints the same checked values for a human reader.
