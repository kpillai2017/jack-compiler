# Extended OS compatibility

The compiler recognises the public routines of the extended Jack OS supplied by
[the companion jackvm-py runtime](https://github.com/kpillai2017/jackvm-py).
It checks their names, argument counts, and whether a call requires an object.
It does **not** perform full argument-type checking or bundle/link an OS into
its generated VM output.

## Language extensions and OS extensions are different

- `--extensions` enables extra **language syntax**: literals/operators,
  initialisers, compound assignment, loop controls, constants, and enums.
- Extended **OS calls** use ordinary Jack syntax and are recognised even without
  `--extensions`. The flag neither installs the OS nor verifies runtime support.
- Stock nand2tetris programs keep their original OS signatures and behaviour.
  Stock nand2tetris OS implementations generally do **not** supply the routines
  below: compilation succeeding does not make such a program portable to them.

## Available additions

| Class | Added public routines |
|---|---|
| `Memory` | `fill`, `copy`, `move` |
| `Screen` | `drawBitmap`, `drawSprite`, `captureBitmap`, `drawVertical` |
| `Output` | `cursorRow`, `cursorColumn` |
| `String` | `capacity`, `clear`, `hasCapacity`, `appendString`, `equals`, `indexOf`, `substring`, `copy`, `isInteger` |
| `Math` | `clamp`, `sign`, `mod`, `shiftLeft`, `shiftRight`, `shiftRightUnsigned` |
| `Input` | `init`, `update`, `key`, `pressed`, `released` |
| `Random` | `new`, `next`, `range`, `dispose` |
| `IntQueue` | `new`, `enqueue`, `dequeue`, `isEmpty`, `isFull`, `length`, `clear`, `dispose` |
| `IntStack` | `new`, `push`, `pop`, `peek`, `isEmpty`, `isFull`, `length`, `clear`, `dispose` |
| `Console` | `printAt`, `clearLine`, `clearRegion`, `scrollUp`, `printPaddedInt` |
| `Timer` | `new`, `tick`, `advance`, `remaining`, `expired`, `reset`, `restart`, `dispose` |
| `Clock` | `supported`, `now`, `elapsed` |

Use the companion OS API documentation/source for parameter meanings, valid
ranges, memory ownership, and timing semantics. Private implementation helpers
remain outside the compiler's public API catalogue.

## Example: ordinary Jack syntax, extended runtime

```jack
class Main {
    function void main() {
        var IntStack stack;
        let stack = IntStack.new(4);
        do stack.push(42);
        do Output.printInt(stack.pop());
        do Output.println();
        do stack.dispose();
        return;
    }
}
```

Compile normally with `jackc Main.jack`, then run the resulting VM with a version
of `jackvm-py` providing `IntStack`. A stock OS without `IntStack` cannot execute
it. When using another VM, supply a compatible compiled extended OS yourself.
Do not substitute a game-local class for a public OS class; use distinct names
(e.g. `GameConsole`) to avoid collisions.

`Clock` also needs host-runtime clock support. Call `Clock.supported()` before
using `Clock.now()`/`Clock.elapsed()`; a runtime lacking the host facility may
reject clock access even when the Jack routines are present. `Timer` is a
manually advanced counter, not an automatically running host clock.

## Tests

From the compiler repository root:

```bash
python3 -m pytest tests/test_os_extensions.py tests/test_os_api_contract.py -q
# Optional companion source consistency check, for sibling checkouts:
PYTHONPATH="../jackvm-py" python3 -m pytest tests/test_os_api_contract.py -q
```

The compiler-only tests cover all 66 added public signatures, valid calls,
wrong argument counts, and wrong receiver kinds. When `jackvm` is importable,
additional tests compare each signature (kind, return type, argument count)
against its packaged Jack source. These consistency checks skip without the
optional companion; the compiler has no runtime dependency on it.
