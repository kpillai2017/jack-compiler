"""Independent contracts for every added public extended-OS routine.

Core tests need only the compiler. Source consistency is optional when the
companion VM (which packages its Jack OS sources) is importable.
"""

import re
from pathlib import Path

import pytest

from jack_compiler.checker import OS_SUBROUTINES
from test_diagnostics import diagnose, in_main

# class: routine name, kind (f=function, m=method, c=constructor), arity.
# Keep expectations independent of the checker's signature parser.
CONTRACTS = {
    "Memory": "fill:f:3 copy:f:3 move:f:3",
    "Screen": "drawBitmap:f:5 drawSprite:f:6 captureBitmap:f:5 drawVertical:f:3",
    "Output": "cursorRow:f:0 cursorColumn:f:0",
    "String": "capacity:m:0 clear:m:0 hasCapacity:m:1 appendString:m:1 equals:m:1 indexOf:m:1 substring:m:2 copy:m:0 isInteger:m:0",
    "Math": "clamp:f:3 sign:f:1 mod:f:2 shiftLeft:f:2 shiftRight:f:2 shiftRightUnsigned:f:2",
    "Input": "init:f:0 update:f:0 key:f:0 pressed:f:0 released:f:0",
    "Random": "new:c:1 next:m:0 range:m:1 dispose:m:0",
    "IntQueue": "new:c:1 enqueue:m:1 dequeue:m:0 isEmpty:m:0 isFull:m:0 length:m:0 clear:m:0 dispose:m:0",
    "IntStack": "new:c:1 push:m:1 pop:m:0 peek:m:0 isEmpty:m:0 isFull:m:0 length:m:0 clear:m:0 dispose:m:0",
    "Console": "printAt:f:3 clearLine:f:1 clearRegion:f:4 scrollUp:f:1 printPaddedInt:f:2",
    "Timer": "new:c:1 tick:m:0 advance:m:1 remaining:m:0 expired:m:0 reset:m:0 restart:m:1 dispose:m:0",
    "Clock": "supported:f:0 now:f:0 elapsed:f:1",
}
KINDS = {"f": "function", "m": "method", "c": "constructor"}
CASES = [(cls, name, KINDS[kind], int(count))
         for cls, entries in CONTRACTS.items()
         for name, kind, count in (entry.split(":") for entry in entries.split())]
IDS = [cls + "." + name for cls, name, _, _ in CASES]


def call_source(cls, name, kind, count, wrong_receiver=False):
    on_object = (kind == "method") != wrong_receiver
    receiver = "object" if on_object else cls
    declaration = "var " + cls + " object;" if on_object else ""
    arguments = ", ".join("0" for _ in range(count))
    return in_main(declaration + f" do {receiver}.{name}({arguments});")


@pytest.mark.parametrize("cls,name,kind,count", CASES, ids=IDS)
def test_extended_contract_and_valid_call(tmp_path, cls, name, kind, count):
    routine = OS_SUBROUTINES[cls][name]
    assert (routine.kind, routine.parameter_count) == (kind, count)
    code, diagnostics = diagnose(tmp_path, call_source(cls, name, kind, count))
    assert code is not None and not diagnostics
    assert f"call {cls}.{name} {count + int(kind == 'method')}" in code


@pytest.mark.parametrize("cls,name,kind,count", CASES, ids=IDS)
def test_every_extended_routine_rejects_wrong_arity(tmp_path, cls, name, kind, count):
    _, diagnostics = diagnose(tmp_path, call_source(cls, name, kind, count + 1))
    assert any(f"takes {count} argument" in d.message for d in diagnostics)


@pytest.mark.parametrize("cls,name,kind,count", CASES, ids=IDS)
def test_every_extended_routine_rejects_wrong_receiver(tmp_path, cls, name, kind, count):
    _, diagnostics = diagnose(tmp_path, call_source(cls, name, kind, count, wrong_receiver=True))
    message = "needs an object" if kind == "method" else "call it as"
    assert any(message in d.message for d in diagnostics)


@pytest.mark.parametrize("cls,name,kind,count", CASES, ids=IDS)
def test_companion_source_matches_extended_signature(cls, name, kind, count):
    companion = pytest.importorskip("jackvm")
    source = Path(companion.__file__).parent / "os" / (cls + ".jack")
    assert source.is_file(), f"companion runtime does not provide {source.name}"
    # Ignore comments before finding declarations, not references or examples.
    text = re.sub(r"/\*.*?\*/|//[^\n]*", "", source.read_text(), flags=re.S)
    declarations = list(re.finditer(
        r"\b(function|method|constructor)\s+(\w+)\s+(\w+)\s*\(([^)]*)\)", text))
    matches = [m for m in declarations if m[3] == name]
    assert len(matches) == 1, f"expected one declaration of {cls}.{name}"
    declaration = matches[0]
    signature = OS_SUBROUTINES[cls][name]
    parameter_count = len([p for p in declaration[4].split(",") if p.strip()])
    assert (declaration[1], declaration[2], parameter_count) == (kind, signature.type, count)
