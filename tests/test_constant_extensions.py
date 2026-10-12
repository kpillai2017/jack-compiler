"""Compile-time named values, enum numbering, and runtime integration."""

import pytest
from antlr4 import CommonTokenStream, InputStream

from jack_compiler.antlr_generated.grammar.JackLexer import JackLexer
from jack_compiler.antlr_generated.grammar.JackParser import JackParser
from jack_compiler.compiler import JackCompiler, JackSemanticError, JackSyntaxError
from jack_compiler.compiler_visitor import JackCompilerVisitor


def compile_class(tmp_path, declarations="", body="return 0;", extensions=True, parameters=""):
    source = "class Main { " + declarations + " function int value(" + parameters + ") { " + body + " } }"
    path = tmp_path / "Main.jack"
    path.write_text(source, encoding="utf-8")
    code = JackCompiler(extensions=extensions).compile_source(str(path))
    return "\n".join(line.strip() for line in code.splitlines())


@pytest.mark.parametrize("expression,value", [
    ("2 + 3 * 4", 20), ("2 + (3 * 4)", 14), ("-7 / 2", -3),
    ("7 / -2", -3), ("-7 / -2", 3), ("32767 + 1", -32768),
    ("-32767 - 1", -32768), ("32767 * 2", -2), ("~0", -1),
    ("0xFF & 0b1010", 10), ("4 | 1", 5), ("3 < 4", -1),
    ("3 > 4", 0), ("3 = 3", -1), ("3 <= 3", -1), ("3 >= 4", 0),
    ("3 != 4", -1), ("'A' + 1", 66), ("false", 0), ("true", -1),
    ("(32767 & 32767) + 1", -32768), ("(-32767 - 1) / -1", -32768),
])
def test_constant_expression_values(tmp_path, expression, value):
    code = compile_class(tmp_path, "const int X = " + expression + ";", "return X;")
    if value >= 0:
        expected = ["push constant " + str(value)]
    elif value == -32768:
        expected = ["push constant 32767", "not"]
    else:
        expected = ["push constant " + str(-value), "neg"]
    assert code.splitlines() == ["function Main.value 0", *expected, "return"]


def test_forward_references_and_class_qualification(tmp_path):
    code = compile_class(tmp_path, "const int A = B + 1, B = 4;", "const int C = Main.A + B; return C;")
    assert "push constant 9\nreturn" in code


def test_class_constant_used_in_local_initialiser(tmp_path):
    code = compile_class(tmp_path, "const int LIMIT = 5;", "var int x = LIMIT; return x;")
    assert code.splitlines() == ["function Main.value 1", "push constant 5", "pop local 0", "push local 0", "return"]


def test_constants_allocate_no_fields_statics_or_locals(tmp_path):
    code = compile_class(tmp_path, "const int A = 4; enum E { X, Y }", "const int B = A; return B + E.Y;")
    assert "function Main.value 0" in code
    assert "static" not in code and "this" not in code and "local" not in code


@pytest.mark.parametrize("declaration,value", [
    ("enum E { A, B, C }", 2), ("enum E { A = 10, B, C }", 12),
    ("enum E { A = -2, B, C }", 0), ("enum E { A, B = 7, C, };", 8),
    ("enum E { A = E.C - 2, B, C = 5 }", 5),
    ("const int BASE = 4; enum E { A = BASE, B, C }", 6),
])
def test_enum_values(tmp_path, declaration, value):
    code = compile_class(tmp_path, declaration, "return E.C;")
    assert "push constant " + str(value) + "\nreturn" in code


def test_enum_members_are_scoped(tmp_path):
    code = compile_class(tmp_path, "enum First { X = 3 } enum Second { X = 7 }", "return First.X + Second.X;")
    assert "push constant 3\npush constant 7\nadd" in code


@pytest.mark.parametrize("body,parameters,fragment", [
    ("const int X = 8; return X + Main.X;", "", "push constant 8\npush constant 3"),
    ("var int X = 8; return X + Main.X;", "", "push local 0\npush constant 3"),
    ("return X + Main.X;", "int X", "push argument 0\npush constant 3"),
])
def test_local_shadowing(tmp_path, body, parameters, fragment):
    assert fragment in compile_class(tmp_path, "const int X = 3;", body, parameters=parameters)


@pytest.mark.parametrize("declarations,body,message", [
    ("const int A = B, B = A;", "return 0;", "cyclic"),
    ("const int A = A;", "return 0;", "cyclic"),
    ("enum E { A = E.B, B }", "return 0;", "cyclic"),
    ("const int X = 1 / 0;", "return 0;", "division by zero"),
    ("const int X = unknown;", "return 0;", "unknown compile-time"),
    ("const int X = Main.value();", "return 0;", "constant expressions"),
    ('const int X = "hello";', "return 0;", "constant expressions"),
    ("const int X = null;", "return 0;", "constant expressions"),
    ("const int X = this;", "return 0;", "constant expressions"),
    ("const String X = 1;", "return 0;", "must have type"),
    ("const boolean X = 1;", "return 0;", "boolean constants"),
    ("const char X = -1;", "return 0;", "char constants"),
    ("const int X = 32768;", "return 0;", "too large"),
    ("enum E { A = 32767, B }", "return 0;", "outside"),
    ("static int x; const int C = x;", "return 0;", "variable"),
    ("", "var int x; const int C = x; return C;", "variable"),
    ("const int X = 1;", "let X = 2; return X;", "cannot assign"),
    ("const int X = 1;", "let X += 2; return X;", "cannot assign"),
    ("", "const int X = 1; let X = 2; return X;", "cannot assign"),
    ("const int X = 1;", "return X[0];", "cannot be indexed"),
    ("enum E { A }", "return E.MISSING;", "unknown compile-time"),
    ("", "const int X = 1; return Main.X;", "unknown compile-time"),
    ("", "return Other.X;", "unknown compile-time"),
    ("const int X = 1, X = 2;", "return 0;", "already declared"),
    ("static int X; const int X = 1;", "return 0;", "already declared"),
    ("enum E { A, A }", "return 0;", "already declared"),
    ("enum E { A } enum E { B }", "return 0;", "conflicts"),
    ("enum E { A } const int E = 1;", "return 0;", "conflicts"),
    ("enum Main { A }", "return 0;", "conflicts"),
    ("", "var int X; const int X = 1; return X;", "already declared"),
])
def test_invalid_constants_and_enums(tmp_path, declarations, body, message):
    with pytest.raises(JackSemanticError) as problem:
        compile_class(tmp_path, declarations, body)
    assert any(message in d.message for d in problem.value.diagnostics), [d.message for d in problem.value.diagnostics]


def test_local_variable_shadow_blocks_constant_expression(tmp_path):
    with pytest.raises(JackSemanticError):
        compile_class(tmp_path, "const int X = 3;", "var int X; const int Y = X; return Y;")


def test_qualified_class_constant_bypasses_variable_shadow(tmp_path):
    code = compile_class(tmp_path, "const int X = 3;", "var int X; const int Y = Main.X; return Y;")
    assert "push constant 3\nreturn" in code


def test_constants_do_not_affect_constructor_allocation(tmp_path):
    path = tmp_path / "Main.jack"
    path.write_text("class Main { const int X = 5; enum E { A, B } field int value; constructor Main new() { const int N = E.B; var int x = X; let value = x + N; return this; } }")
    code = JackCompiler(extensions=True).compile_source(str(path))
    assert "push constant 1\n    call Memory.alloc 1" in code
    assert "function Main.new 1" in code


def test_constants_do_not_leak_between_subroutines(tmp_path):
    path = tmp_path / "Main.jack"
    path.write_text("class Main { function int a() { const int X = 5; return X; } function int b() { return X; } }")
    with pytest.raises(JackSemanticError):
        JackCompiler(extensions=True).compile_source(str(path))


@pytest.mark.parametrize("declaration", ["const int X = 1;", "enum E { A }"])
def test_declarations_are_opt_in(tmp_path, declaration):
    with pytest.raises(JackSyntaxError):
        compile_class(tmp_path, declaration, extensions=False)


def test_keyword_identifiers_preserved_in_standard_mode(tmp_path):
    compile_class(tmp_path, body="var int const, enum; let const = 2; let enum = const; return enum;", extensions=False)


def test_constant_boolean_endless_loop_return_analysis(tmp_path):
    compile_class(tmp_path, "const boolean FOREVER = true;", "while (FOREVER) {}")
    with pytest.raises(JackSemanticError):
        compile_class(tmp_path, "const boolean FOREVER = true;", "while (FOREVER) { break; }")


def test_typed_char_and_boolean_constants(tmp_path):
    code = compile_class(tmp_path, r"const char LETTER = '\n'; const boolean READY = 2 <= 3;", "return LETTER + READY;")
    assert "push constant 10\npush constant 1\nneg\nadd" in code


@pytest.mark.parametrize("body,parameters", [
    ("var int E; return 0;", ""), ("const int E = 1; return 0;", ""),
    ("return 0;", "int E"), ("return E.A();", ""),
])
def test_enum_namespace_collisions_and_calls(tmp_path, body, parameters):
    with pytest.raises(JackSemanticError):
        compile_class(tmp_path, "enum E { A }", body, parameters=parameters)


def test_parameter_constant_name_conflict_is_diagnosed(tmp_path):
    with pytest.raises(JackSemanticError):
        compile_class(tmp_path, body="const int X = 1; return X;", parameters="int X")


def test_constant_ast(tmp_path):
    lexer = JackLexer(InputStream("class Main { const int X = 2; enum E { A = 3 } function int value() { return X + E.A; } }"))
    lexer.extensions = True
    parser = JackParser(CommonTokenStream(lexer))
    tree = parser.program()
    visitor = JackCompilerVisitor(extensions=True)
    ast = visitor.compile_program(tree)
    expression = ast["subroutines"][0]["body"]["statements"][0]["value"]
    assert expression["term"]["value"] == 2
    assert expression["rest"][0]["term"]["value"] == 3


@pytest.mark.parametrize("value,expected", [("32767 + 1", -32768), ("-7 / 2", -3), ("2 + 3 * 4", 20)])
def test_constant_runtime(tmp_path, value, expected):
    vm_module = pytest.importorskip("jackvm.vm")
    path = tmp_path / "Main.jack"
    path.write_text("class Main { static int result; const int X = " + value + "; enum E { A = 3, B } function void main() { const int N = E.B; var int i; for (i = 0; i < N; i += 1) { let result = X; } return; } }")
    vm = vm_module.VirtualMachine()
    vm.load_source(JackCompiler(extensions=True).compile_source(str(path)))
    vm.run(300000)
    assert vm.is_halted()
    assert vm.peek(vm.static_addresses["Main"]) == expected
