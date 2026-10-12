"""Dependency graphs must not be limited by Python's recursion depth."""

import pytest

from jack_compiler.compiler import JackCompiler, JackSemanticError


def compile_declarations(tmp_path, declarations, body="return C0;", local=False):
    path = tmp_path / "Main.jack"
    if local:
        source = "class Main { function int value() { " + declarations + body + " } }"
    else:
        source = "class Main { " + declarations + " function int value() { " + body + " } }"
    path.write_text(source, encoding="utf-8")
    compiler = JackCompiler(extensions=True)
    return compiler.compile_source(str(path)), compiler


def chain(length, ending="7", qualified=False):
    prefix = "Main." if qualified else ""
    return "\n".join(
        [f"const int C{i} = {prefix}C{i + 1};" for i in range(length)]
        + [f"const int C{length} = {ending};"]
    )


@pytest.mark.parametrize("local,qualified", [(False, False), (False, True), (True, False)])
def test_long_forward_dependency_chain(tmp_path, local, qualified):
    code, _ = compile_declarations(tmp_path, chain(2000, qualified=qualified), local=local)
    assert "push constant 7" in code
    assert "function Main.value 0" in code


@pytest.mark.parametrize("local", [False, True])
def test_long_cycle_produces_semantic_diagnostics(tmp_path, local):
    with pytest.raises(JackSemanticError) as problem:
        compile_declarations(tmp_path, chain(2000, ending="C0"), local=local)
    assert any("cyclic constant definition" in d.message for d in problem.value.diagnostics)
    assert all(d.line >= 1 for d in problem.value.diagnostics)


def test_long_enum_dependency_chain(tmp_path):
    members = ", ".join([f"V{i} = E.V{i + 1}" for i in range(2000)] + ["V2000 = 7"])
    code, _ = compile_declarations(tmp_path, "enum E { " + members + " }", "return E.V0;")
    assert "push constant 7" in code


def test_shared_dependencies_and_diamond_graph(tmp_path):
    declarations = "const int C0 = A + B, A = BASE * 2, B = BASE * 3, BASE = 4;"
    code, _ = compile_declarations(tmp_path, declarations)
    assert "push constant 20" in code


def test_invalid_dependency_does_not_poison_independent_definitions(tmp_path):
    from antlr4 import CommonTokenStream, InputStream
    from jack_compiler.antlr_generated.grammar.JackLexer import JackLexer
    from jack_compiler.antlr_generated.grammar.JackParser import JackParser
    from jack_compiler.constants import collect_constants

    source = "class Main { const int A = B, B = A, GOOD = 7, OTHER = GOOD + 2; }"
    lexer = JackLexer(InputStream(source))
    lexer.extensions = True
    parser = JackParser(CommonTokenStream(lexer))
    cls = parser.classDeclaration()
    assert parser.getNumberOfSyntaxErrors() == 0
    diagnostics = []
    values = collect_constants(cls, "Main", report=lambda ctx, message: diagnostics.append(message))
    assert values["GOOD"].value == 7
    assert values["OTHER"].value == 9
    assert any("cyclic" in message for message in diagnostics)


def test_unknown_dependency_terminates_with_diagnostic(tmp_path):
    with pytest.raises(JackSemanticError) as problem:
        compile_declarations(tmp_path, chain(2000, ending="MISSING"))
    assert any("unknown compile-time constant 'MISSING'" in d.message for d in problem.value.diagnostics)
