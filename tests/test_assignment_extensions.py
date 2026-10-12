"""Opt-in local initialisers and compound assignment."""

import pytest

from jack_compiler.compiler import JackCompiler, JackSemanticError, JackSyntaxError


def compile_main(tmp_path, body, extensions=True):
    path = tmp_path / "Main.jack"
    path.write_text("class Main { function void main() { " + body + " } }", encoding="utf-8")
    vm = JackCompiler(extensions=extensions).compile_source(str(path))
    return "\n".join(line.strip() for line in vm.splitlines())


# --- local initialisers -------------------------------------------------

def test_single_initialiser(tmp_path):
    vm = compile_main(tmp_path, "var int x = 5; return;")
    assert vm.splitlines() == [
        "function Main.main 1", "push constant 5", "pop local 0", "push constant 0", "return"
    ]


def test_mixed_initialised_and_plain_locals(tmp_path):
    vm = compile_main(tmp_path, "var int x = 1, y, z = 2; let y = x + z; return;")
    assert vm.splitlines() == [
        "function Main.main 3",
        "push constant 1", "pop local 0",
        "push constant 2", "pop local 2",
        "push local 0", "push local 2", "add", "pop local 1",
        "push constant 0", "return",
    ]


def test_initialiser_may_reference_earlier_sibling(tmp_path):
    vm = compile_main(tmp_path, "var int x = 1, y = x + 1; return y;")
    assert vm.splitlines() == [
        "function Main.main 2",
        "push constant 1", "pop local 0",
        "push local 0", "push constant 1", "add", "pop local 1",
        "push local 1", "return",
    ]


def test_initialisers_run_in_source_order_for_side_effects(tmp_path):
    # Calls inside initialisers must run in source order, not reverse.
    path = tmp_path / "Main.jack"
    path.write_text(
        "class Main {"
        "  function int main() {"
        "    var int a, b;"
        "    let a = Main.mark(1);"
        "    let b = Main.mark(2);"
        "    return 0;"
        "  }"
        "  function int mark(int n) { return n; }"
        "}", encoding="utf-8")
    vm = "\n".join(line.strip() for line in JackCompiler(extensions=True).compile_source(str(path)).splitlines())
    first_call = vm.index("call Main.mark")
    second_call = vm.index("call Main.mark", first_call + 1)
    assert "push constant 1" in vm[:first_call + 40]
    assert first_call < second_call


def test_initialiser_in_method_runs_after_this_pointer_is_set(tmp_path):
    path = tmp_path / "Main.jack"
    path.write_text(
        "class Main {"
        "  field int value;"
        "  method int get() {"
        "    var int copy = value;"
        "    return copy;"
        "  }"
        "}", encoding="utf-8")
    vm = "\n".join(line.strip() for line in JackCompiler(extensions=True).compile_source(str(path)).splitlines())
    assert vm.splitlines() == [
        "function Main.get 1",
        "push argument 0", "pop pointer 0",
        "push this 0", "pop local 0",
        "push local 0", "return",
    ]


def test_initialiser_in_constructor_runs_after_allocation(tmp_path):
    path = tmp_path / "Main.jack"
    path.write_text(
        "class Main {"
        "  field int value;"
        "  constructor Main new() {"
        "    var int copy = 7;"
        "    let value = copy;"
        "    return this;"
        "  }"
        "}", encoding="utf-8")
    vm = "\n".join(line.strip() for line in JackCompiler(extensions=True).compile_source(str(path)).splitlines())
    assert vm.splitlines()[:5] == [
        "function Main.new 1", "push constant 1", "call Memory.alloc 1", "pop pointer 0",
        "push constant 7",
    ]


def test_initialisers_are_opt_in(tmp_path):
    with pytest.raises(JackSemanticError) as problem:
        compile_main(tmp_path, "var int x = 5; return;", extensions=False)
    assert any("requires extension mode" in d.message for d in problem.value.diagnostics)


def test_initialiser_type_errors_are_still_reported(tmp_path):
    with pytest.raises(JackSemanticError) as problem:
        compile_main(tmp_path, "var int x = undeclaredThing; return;")
    assert any("undeclaredThing" in d.message for d in problem.value.diagnostics)


# --- compound assignment -------------------------------------------------

@pytest.mark.parametrize("op,instr", [
    ("+=", "add"), ("-=", "sub"), ("*=", "call Math.multiply 2"),
    ("/=", "call Math.divide 2"), ("&=", "and"), ("|=", "or"),
])
def test_scalar_compound_assignment(tmp_path, op, instr):
    vm = compile_main(tmp_path, f"var int x; let x {op} 3; return;")
    assert vm.splitlines() == [
        "function Main.main 1", "push local 0", "push constant 3", instr, "pop local 0",
        "push constant 0", "return",
    ]


def test_array_compound_assignment_evaluates_index_once(tmp_path):
    path = tmp_path / "Main.jack"
    path.write_text(
        "class Main {"
        "  static int calls;"
        "  function int index() { let calls = calls + 1; return 0; }"
        "  function void main() {"
        "    var Array data;"
        "    let data = Array.new(1);"
        "    let data[Main.index()] += 5;"
        "    return;"
        "  }"
        "}", encoding="utf-8")
    vm = "\n".join(line.strip() for line in JackCompiler(extensions=True).compile_source(str(path)).splitlines())
    assert vm.count("call Main.index") == 1


def test_array_compound_assignment_lowering(tmp_path):
    vm = compile_main(tmp_path, "var Array a; let a[1] += 2; return;")
    assert vm.splitlines() == [
        "function Main.main 1",
        "push constant 1", "push local 0", "add",
        "pop pointer 1", "push pointer 1", "push that 0",
        "push constant 2", "add",
        "pop temp 0", "pop pointer 1", "push temp 0", "pop that 0",
        "push constant 0", "return",
    ]


def test_compound_assignment_is_opt_in(tmp_path):
    with pytest.raises(JackSemanticError) as problem:
        compile_main(tmp_path, "var int x; let x += 1; return;", extensions=False)
    assert any("requires extension mode" in d.message for d in problem.value.diagnostics)


def test_compound_assignment_marks_variable_as_used(tmp_path):
    # Reading via += must not trigger an "unused variable" warning.
    path = tmp_path / "Main.jack"
    path.write_text("class Main { function void main() { var int x; let x += 1; return; } }")
    JackCompiler(extensions=True, werror=True).compile_source(str(path))  # must not raise


def test_division_by_compound_preserves_integer_semantics(tmp_path):
    vm = compile_main(tmp_path, "var int x; let x /= 2; return;")
    assert "call Math.divide 2" in vm


# --- standard-mode compatibility -----------------------------------------

@pytest.mark.parametrize("body", [
    "var int x, y; let x = 1; let y = x; return;",
    "var Array a; let a[0] = 9; return;",
])
def test_standard_syntax_unaffected_in_extension_mode(tmp_path, body):
    assert compile_main(tmp_path, body, extensions=False) == compile_main(tmp_path, body, extensions=True)


def test_malformed_assignment_operator_is_a_syntax_error(tmp_path):
    with pytest.raises(JackSyntaxError):
        compile_main(tmp_path, "var int x; let x =+ 1; return;")
