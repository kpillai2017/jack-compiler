"""Extended loops, flow diagnostics, and optional companion-VM integration."""

import itertools

import pytest
from antlr4 import CommonTokenStream, InputStream

from jack_compiler.antlr_generated.grammar.JackLexer import JackLexer
from jack_compiler.antlr_generated.grammar.JackParser import JackParser
from jack_compiler.compiler import JackCompiler, JackSemanticError, JackSyntaxError
from jack_compiler.compiler_visitor import JackCompilerVisitor


def compile_source(tmp_path, source, extensions=True):
    path = tmp_path / "Main.jack"
    path.write_text(source, encoding="utf-8")
    compiler = JackCompiler(extensions=extensions)
    vm = compiler.compile_source(str(path))
    return "\n".join(line.strip() for line in vm.splitlines()), compiler


def compile_body(tmp_path, body, extensions=True):
    return compile_source(tmp_path, "class Main { function void main() { " + body + " } }", extensions)


@pytest.mark.parametrize("init,condition,update", list(itertools.product([False, True], repeat=3)))
def test_optional_for_clauses(tmp_path, init, condition, update):
    header = ";".join(["let i = 0" if init else "", "i < 3" if condition else "", "let i += 1" if update else ""])
    vm, _ = compile_body(tmp_path, "var int i; for (" + header + ") { break; } return;")
    assert "label FOR$" in vm and "label FORUPDATE$" in vm and "label ENDFOR$" in vm
    assert vm.count("pop local 0") == int(init) + int(update)


@pytest.mark.parametrize("let_keyword", ["", "let "])
def test_for_header_accepts_optional_let(tmp_path, let_keyword):
    compile_body(tmp_path, f"var int i; for ({let_keyword}i = 0; i < 3; {let_keyword}i += 1) {{}} return;")


def test_continue_in_for_targets_update(tmp_path):
    vm, _ = compile_body(tmp_path, "var int i; for (i = 0; i < 3; i += 1) { continue; } return;")
    lines = vm.splitlines()
    update = next(line for line in lines if line.startswith("label FORUPDATE$"))
    assert "goto " + update.split()[1] in lines


def test_while_controls_target_condition_and_exit(tmp_path):
    vm, _ = compile_body(tmp_path, "var int i; while (i < 3) { if (i = 1) { break; } continue; } return;")
    lines = vm.splitlines()
    loop = next(line.split()[1] for line in lines if line.startswith("label WHILE$"))
    end = next(line.split()[1] for line in lines if line.startswith("label ENDWHILE$"))
    assert lines.count("goto " + loop) == 2
    assert "goto " + end in lines


@pytest.mark.parametrize("keyword", ["break", "continue"])
def test_control_outside_loop_is_error(tmp_path, keyword):
    with pytest.raises(JackSemanticError) as problem:
        compile_body(tmp_path, f"if (true) {{ {keyword}; }} return;")
    assert any("only valid inside a loop" in d.message for d in problem.value.diagnostics)


@pytest.mark.parametrize("keyword", ["break", "continue"])
def test_loop_scope_does_not_leak_between_subroutines(tmp_path, keyword):
    source = "class Main { function void a() { while (true) { break; } return; } function void b() { " + keyword + "; } }"
    with pytest.raises(JackSemanticError) as problem:
        compile_source(tmp_path, source)
    assert any("only valid inside a loop" in d.message for d in problem.value.diagnostics)


@pytest.mark.parametrize("body", ["for (;;) {}", "while (true) { break; }", "while (true) { continue; }"])
def test_loop_extensions_rejected_in_standard_mode(tmp_path, body):
    with pytest.raises(JackSyntaxError):
        compile_body(tmp_path, body + " return;", extensions=False)


def test_extension_keywords_remain_standard_identifiers(tmp_path):
    compile_body(tmp_path, "var int for, break, continue; let for = 1; let break = for; let continue = break; return;", extensions=False)


@pytest.mark.parametrize("body", [
    "while (true) { break; }",
    "while (true) { if (true) { break; } }",
    "for (;;) { break; }",
    "for (; true;) { if (true) { break; } else { return; } }",
    "for (; false;) {}",
    "while (true) { while (true) { break; } break; }",
])
def test_breakable_loops_require_return_afterwards(tmp_path, body):
    with pytest.raises(JackSemanticError) as problem:
        compile_body(tmp_path, body)
    assert any("can reach its end" in d.message for d in problem.value.diagnostics)


@pytest.mark.parametrize("body", [
    "for (;;) {}",
    "for (;true;) { continue; }",
    "while (true) { while (true) { break; } }",
    "while (true) { continue; break; }",
    "for (;;) { return; break; }",
    "for (;;) { if (true) { return; } else { continue; } break; }",
])
def test_endless_loops_or_returns_need_no_trailing_return(tmp_path, body):
    compile_body(tmp_path, body)


@pytest.mark.parametrize("keyword", ["break", "continue"])
def test_unreachable_code_after_loop_control_is_warned(tmp_path, keyword):
    _, compiler = compile_body(tmp_path, f"while (true) {{ {keyword}; do Output.println(); }} return;")
    assert any("comes after '" + keyword + "'" in d.message for d in compiler.diagnostics)


@pytest.mark.parametrize("header", ["unknown = 0; true;", "; unknown < 3;", "; true; unknown += 1"])
def test_for_clauses_are_semantically_checked(tmp_path, header):
    with pytest.raises(JackSemanticError) as problem:
        compile_body(tmp_path, "for (" + header + ") { break; } return;")
    assert any("unknown" in d.message for d in problem.value.diagnostics)


@pytest.mark.parametrize("body", [
    "for (var int i = 0; i < 3; i += 1) {} return;",
    "for (i = 0 i < 3; i += 1) {} return;",
    "while (true) { break } return;",
    "while (true) { continue } return;",
])
def test_malformed_loops_rejected(tmp_path, body):
    with pytest.raises(JackSyntaxError):
        compile_body(tmp_path, "var int i; " + body)


def test_for_ast(tmp_path):
    source = "class Main { function void main() { var int i; for (i = 0; i < 3; i += 1) { continue; } return; } }"
    lexer = JackLexer(InputStream(source))
    lexer.extensions = True
    parser = JackParser(CommonTokenStream(lexer))
    tree = parser.program()
    assert parser.getNumberOfSyntaxErrors() == 0
    ast = JackCompilerVisitor(extensions=True).compile_program(tree)
    loop = ast["subroutines"][0]["body"]["statements"][0]
    assert loop["statementType"] == "forStatement"
    assert loop["initialiser"]["statementType"] == "letStatement"
    assert loop["update"]["assignmentOperator"] == "+="
    assert loop["body"][0]["statementType"] == "continueStatement"


# These run when jackvm-py is installed or its directory is on PYTHONPATH.
# They remain optional so the compiler does not depend on a companion runtime.
@pytest.fixture
def run_vm(tmp_path):
    vm_module = pytest.importorskip("jackvm.vm")

    def run(body, helpers=""):
        source = "class Main { static int result, calls; function void main() { " + body + " return; } " + helpers + " }"
        code, _ = compile_source(tmp_path, source)
        vm = vm_module.VirtualMachine()
        vm.load_source(code)
        vm.run(300000)
        assert vm.is_halted(), "program did not halt (possible incorrect continue target)"
        base = vm.static_addresses["Main"]
        return vm.peek(base), vm.peek(base + 1)

    return run


@pytest.mark.parametrize("body,expected", [
    ("var int i; for (i = 0; i < 5; i += 1) { let result += i; }", 10),
    ("var int i; for (i = 0; i < 5; i += 1) { if (i = 2) { continue; } let result += i; }", 8),
    ("var int i; for (i = 0; i < 5; i += 1) { if (i = 3) { break; } let result += i; }", 3),
    ("for (;;) { let result += 1; if (result = 4) { break; } }", 4),
    ("var int i = 0; while (i < 5) { let i += 1; if (i = 2) { continue; } if (i = 4) { break; } let result += i; }", 4),
    ("var int i, j; for (i = 0; i < 3; i += 1) { for (j = 0; j < 4; j += 1) { if (j = 1) { break; } let result += 1; } }", 3),
    ("var int i, j; for (i = 0; i < 3; i += 1) { let j = 0; while (j < 3) { let j += 1; if (j = 2) { continue; } let result += 1; } if (i = 1) { continue; } let result += 10; }", 26),
    ("var int i; for (; false; i += 1) { let result = 99; }", 0),
    ("var int i = 0; for (; i < 3;) { let i += 1; let result += i; }", 6),
    ("var Array a = Array.new(1); let a[0] = 0; for (; a[0] < 3; a[0] += 1) { let result += 1; }", 3),
])
def test_runtime_loop_semantics(run_vm, body, expected):
    assert run_vm(body)[0] == expected


def test_runtime_return_inside_loop_skips_update(run_vm):
    body = "let result = Main.compute();"
    helpers = "function int compute() { var int i; for (i = 0; i < 3; i += Main.step()) { if (i = 1) { return 7; } } return 0; } function int step() { let calls += 1; return 1; }"
    assert run_vm(body, helpers) == (7, 1)


def test_runtime_deeply_nested_mixed_loops(run_vm):
    body = "var int i, j; for (i = 0; i < 2; i += 1) { let j = 0; while (j < 2) { let j += 1; for (;;) { let result += 1; break; } if (j = 1) { continue; } let result += 10; } }"
    assert run_vm(body)[0] == 24


def test_runtime_header_calls_and_break_skips_update(run_vm):
    body = "var int i; for (i = Main.start(); i < 4; i += Main.step()) { if (i = 2) { break; } let result += i; }"
    helpers = "function int start() { let calls += 1; return 0; } function int step() { let calls += 1; return 1; }"
    assert run_vm(body, helpers) == (1, 3)
