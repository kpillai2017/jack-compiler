"""Opt-in comparisons and literals, with standard Jack compatibility."""

import pytest
from antlr4 import CommonTokenStream, InputStream

from jack_compiler.antlr_generated.grammar.JackLexer import JackLexer
from jack_compiler.antlr_generated.grammar.JackParser import JackParser
from jack_compiler.compiler import JackCompiler, JackSemanticError, JackSyntaxError, main
from jack_compiler.compiler_visitor import JackCompilerVisitor
from jack_compiler.literals import ESCAPES, quoted_value


def compile_expression(tmp_path, expression, extensions=True):
    path = tmp_path / "Main.jack"
    path.write_text("class Main { function int value() { return " + expression + "; } }", encoding="utf-8")
    vm = JackCompiler(extensions=extensions).compile_source(str(path))
    return "\n".join(line.strip() for line in vm.splitlines())


@pytest.mark.parametrize("op,instruction", [("<=", "gt"), (">=", "lt"), ("!=", "eq")])
def test_comparison_lowering(tmp_path, op, instruction):
    assert compile_expression(tmp_path, "3 " + op + " 4").splitlines() == [
        "function Main.value 0", "push constant 3", "push constant 4", instruction, "not", "return"
    ]


@pytest.mark.parametrize("literal,value", [
    ("0xFF", 255), ("0X7fFf", 32767), ("0b1010", 10), ("0B111", 7),
    ("0x0", 0), ("0b0", 0), ("0007", 7), ("'A'", 65), ("' '", 32), ("'é'", 233),
])
def test_numeric_and_character_literals(tmp_path, literal, value):
    assert "push constant " + str(value) + "\nreturn" in compile_expression(tmp_path, literal)


@pytest.mark.parametrize("escape,decoded", list(ESCAPES.items()))
def test_character_escapes(tmp_path, escape, decoded):
    vm = compile_expression(tmp_path, "'\\" + escape + "'")
    assert "push constant " + str(ord(decoded)) + "\nreturn" in vm


@pytest.mark.parametrize("escape,decoded", list(ESCAPES.items()))
def test_string_escapes(tmp_path, escape, decoded):
    vm = compile_expression(tmp_path, '"\\' + escape + '"')
    assert vm.splitlines() == [
        "function Main.value 0", "push constant 1", "call String.new 1",
        "push constant " + str(ord(decoded)), "call String.appendChar 2", "return"
    ]


def test_string_decoded_length_and_empty_string(tmp_path):
    vm = compile_expression(tmp_path, r'"a\n\"\\b"')
    assert "push constant 5\ncall String.new 1" in vm
    assert "push constant 10\ncall String.appendChar 2" in vm
    assert "push constant 0\ncall String.new 1\nreturn" in compile_expression(tmp_path, '""')


@pytest.mark.parametrize("expression", ["1 <= 2", "1 >= 2", "1 != 2", "0x10", "0b10", "'A'"])
def test_extensions_are_opt_in(tmp_path, expression):
    with pytest.raises(JackSemanticError) as problem:
        compile_expression(tmp_path, expression, extensions=False)
    assert any("requires extension mode" in d.message for d in problem.value.diagnostics)
    assert any("--extensions" in (d.help or "") for d in problem.value.diagnostics)


@pytest.mark.parametrize("expression", ["0x8000", "0b1000000000000000", "32768"])
def test_literal_range(tmp_path, expression):
    with pytest.raises(JackSemanticError) as problem:
        compile_expression(tmp_path, expression)
    assert any("too large" in d.message for d in problem.value.diagnostics)


@pytest.mark.parametrize("expression", [r'"\q"', r"'\q'", '"😀"', "'😀'"])
def test_invalid_decoded_literals(tmp_path, expression):
    with pytest.raises(JackSemanticError) as problem:
        compile_expression(tmp_path, expression)
    assert all(d.line == 1 and d.column > 0 for d in problem.value.diagnostics)


@pytest.mark.parametrize("expression", [
    "0x", "0xGG", "0b", "0b102", "0x1G", "''", "'ab'", "'a", '"a',
    '"a\nb"', "'\n'", '"ends\\',
])
def test_malformed_literals(tmp_path, expression):
    with pytest.raises(JackSyntaxError):
        compile_expression(tmp_path, expression)


def test_standard_backslashes_remain_verbatim(tmp_path):
    vm = compile_expression(tmp_path, r'"\n\q"', extensions=False)
    assert "push constant 4\ncall String.new 1" in vm
    assert vm.count("push constant 92\ncall String.appendChar 2") == 2
    # A backslash immediately before the closing quote is valid standard Jack.
    vm = compile_expression(tmp_path, '"tail\\"', extensions=False)
    assert "push constant 5\ncall String.new 1" in vm


def test_expression_order_is_unchanged(tmp_path):
    assert compile_expression(tmp_path, "2 + 3 * 4").splitlines() == [
        "function Main.value 0", "push constant 2", "push constant 3", "add",
        "push constant 4", "call Math.multiply 2", "return"
    ]


@pytest.mark.parametrize("literal,value", [("0x2A", 42), ("'A'", 65), (r'"\n"', "\n")])
def test_ast_literal_values(literal, value):
    lexer = JackLexer(InputStream(literal))
    lexer.extensions = True
    parser = JackParser(CommonTokenStream(lexer))
    term = parser.term()
    assert parser.getNumberOfSyntaxErrors() == 0
    assert JackCompilerVisitor(extensions=True).visit_term(term)["value"] == value


def test_string_size_validation():
    with pytest.raises(ValueError, match="too long"):
        quoted_value('"' + "a" * 32768 + '"', extensions=True)


@pytest.mark.parametrize("directory", [False, True])
def test_cli_extension_flag(tmp_path, directory):
    source = tmp_path / "Main.jack"
    source.write_text("class Main { function int value() { return 0x2A; } }")
    with pytest.raises(SystemExit) as problem:
        main([str(tmp_path if directory else source), "--extensions"])
    assert problem.value.code == 0
    assert "push constant 42" in source.with_suffix(".vm").read_text()


@pytest.mark.parametrize("expression", ["0", "0007", "2 + 3 * 4", "~false", '"Hello"'])
def test_standard_vm_is_identical_in_extension_mode(tmp_path, expression):
    standard = compile_expression(tmp_path, expression, extensions=False)
    assert compile_expression(tmp_path, expression, extensions=True) == standard


def test_standard_cli_rejects_extensions(tmp_path):
    source = tmp_path / "Main.jack"
    source.write_text("class Main { function int value() { return 0x2A; } }")
    with pytest.raises(SystemExit) as problem:
        main([str(source)])
    assert problem.value.code == 1
    assert not source.with_suffix(".vm").exists()
