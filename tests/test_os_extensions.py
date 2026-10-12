"""Extended OS signatures retain method-kind and argument validation."""
import pytest
from test_diagnostics import diagnose, in_main


def test_extended_os_public_calls_compile(tmp_path):
    source = in_main("""
        var String s; var Array a; var Random r; var IntQueue q; var IntStack stack; var Timer timer;
        let s = String.new(8); let a = Array.new(16);
        do Memory.fill(a, 16, 0); do Memory.copy(a, a, 16); do Memory.move(a, a, 16);
        do s.clear(); do s.appendString(s); do s.equals(s); do s.capacity();
        do s.hasCapacity(1); do s.indexOf(65); do s.substring(0, 0); do s.copy(); do s.isInteger();
        do Screen.drawBitmap(0, 0, 16, 1, a); do Screen.drawSprite(0, 0, 16, 1, a, a);
        do Screen.captureBitmap(0, 0, 16, 1, a);
        do Input.init(); do Input.update(); do Input.key(); do Input.pressed(); do Input.released();
        let r = Random.new(1); do r.next(); do r.range(7); do r.dispose();
        let q = IntQueue.new(2); do q.enqueue(1); do q.dequeue(); do q.dispose();
        let stack = IntStack.new(2); do stack.push(1); do stack.pop(); do stack.dispose();
        do Math.clamp(1, 0, 2); do Math.sign(-1); do Math.mod(7, 3);
        do Math.shiftLeft(1, 1); do Math.shiftRight(-1, 1); do Math.shiftRightUnsigned(-1, 1);
        do Console.printAt(0, 0, s); do Console.clearLine(0); do Console.clearRegion(0, 0, 1, 1);
        do Console.scrollUp(1); do Console.printPaddedInt(1, 3); do Output.cursorRow(); do Output.cursorColumn();
        let timer = Timer.new(3); do timer.tick(); do timer.advance(1); do timer.remaining();
        do timer.expired(); do timer.reset(); do timer.restart(0); do timer.dispose();
        do Clock.supported(); do Clock.now(); do Clock.elapsed(0);
        do s.dispose(); do a.dispose();
    """)
    vm, diagnostics = diagnose(tmp_path, source)
    assert vm is not None
    assert not diagnostics


@pytest.mark.parametrize("body,expected", [
    ("do Memory.fill(100, 1);", "takes 3 arguments"),
    ("do Input.pressed(1);", "takes 0 arguments"),
    ("do Random.next();", "needs an object"),
    ("do Clock.now(1);", "takes 0 arguments"),
    ("do Timer.tick();", "needs an object"),
    ("do Screen.captureBitmap(0, 0, 1, 1);", "takes 5 arguments"),
    ("do Console.scrolUp(1);", "no subroutine named"),
    ("do Screen.blit(0, 0, 1, 1, 0, 0, false);", "no subroutine named")])
def test_extended_os_calls_still_validate(tmp_path, body, expected):
    _, diagnostics = diagnose(tmp_path, in_main(body))
    assert any(expected in diagnostic.message for diagnostic in diagnostics)
