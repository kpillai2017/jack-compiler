"""
Tests for compiler diagnostics: friendly syntax errors, the semantic
checker, the GCC-style renderer, and the -w / --werror options.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from jack_compiler import JackCompiler, JackSemanticError, JackSyntaxError  # noqa: E402
from jack_compiler.compiler import main  # noqa: E402
from jack_compiler.diagnostics import (  # noqa: E402
    Diagnostic,
    Note,
    caret_padding,
    describe_expected,
    friendly_syntax_error,
    render,
    summary,
)

EXAMPLES_DIR = ROOT / "examples"
SQUARE_DIR = ROOT / "tests" / "fixtures" / "square"


def diagnose(tmp_path, source, name="Main"):
    """Compile `source` as <name>.jack; return (vm or None, diagnostics)."""
    path = tmp_path / f"{name}.jack"
    path.write_text(source)
    compiler = JackCompiler()
    try:
        return compiler.compile_source(str(path)), compiler.diagnostics
    except JackSyntaxError as problem:
        return None, problem.diagnostics


def in_main(body, decls="", name="Main"):
    """A class with one 'function void main()' holding `body`."""
    return f"class {name} {{\n{decls}    function void main() {{\n{body}\n        return;\n    }}\n}}\n"


def only(diagnostics, severity="error"):
    found = [d for d in diagnostics if d.severity == severity]
    assert len(found) == 1, [str(d) for d in diagnostics]
    return found[0]


# --- rewriting ANTLR's messages ------------------------------------------------------
def test_expected_token_sets_get_names():
    expression = ["'true'", "'false'", "'null'", "'this'", "'-'", "'~'", "'('", "INTEGER", "STRING_LITERAL", "IDENTIFIER"]
    assert describe_expected(expression) == "an expression"
    assert describe_expected(expression + ["';'"]) == "';' or an expression"
    assert describe_expected(["IDENTIFIER"]) == "a name"
    assert describe_expected(["'}'", "'constructor'", "'function'", "'method'"]) == "'}' or a subroutine declaration"


def test_friendly_messages():
    assert friendly_syntax_error("mismatched input ';' expecting {'true', 'false', 'null', 'this', '-', '~', '(', "
                                 "INTEGER, STRING_LITERAL, IDENTIFIER}").message == "expected an expression, found ';'"  # fmt: skip
    missing = friendly_syntax_error("missing ';' at '}'", "'x'")
    assert (missing.message, missing.after_previous) == ("expected ';' after 'x'", True)
    assert friendly_syntax_error("token recognition error at: '@'").message == "invalid character '@' in program"
    assert friendly_syntax_error("token recognition error at: '\"abc'").message == "unterminated string"
    assert friendly_syntax_error("something new").message == "something new"  # unknown: passed through


def test_missing_semicolon_points_after_the_previous_token(tmp_path):
    _, diagnostics = diagnose(tmp_path, in_main("        do Output.printInt(1)"))
    error = only(diagnostics)
    assert (error.line, error.column, error.message) == (3, 30, "expected ';' after ')'")
    assert error.help and "';'" in error.help


def test_missing_semicolon_after_return_at_end_of_line(tmp_path):
    source = "class Main {\n    function void main() {\n        return\n    }\n}\n"
    error = only(diagnose(tmp_path, source)[1])
    assert (error.line, error.column, error.message) == (3, 15, "expected ';' after 'return'")


def test_unexpected_end_of_file_notes_the_unclosed_brace(tmp_path):
    error = only(diagnose(tmp_path, "class Main {\n    function void main() {\n        return;\n    }\n")[1])
    assert error.message.startswith("unexpected end of file: expected '}'")
    assert (error.line, error.column) == (4, 6)  # right after the last '}'
    assert error.notes == (Note(1, 12, "this '{' is never closed"),)


def test_a_bad_string_is_reported_once_without_knock_on_errors(tmp_path):
    _, diagnostics = diagnose(tmp_path, in_main('        do Output.printString("oops);'))
    error = only(diagnostics)
    assert error.message == "unterminated string" and (error.line, error.column) == (3, 31)


def test_keyword_used_as_a_name(tmp_path):
    error = only(diagnose(tmp_path, in_main("        var int class;"))[1])
    assert error.message == "expected a name, found 'class'" and error.length == 5


def test_syntax_errors_keep_the_old_api(tmp_path):
    bad = tmp_path / "Bad.jack"
    bad.write_text("class Bad {\n    function void f() {\n        let x = ;\n    }\n}\n")
    with pytest.raises(JackSyntaxError) as problem:
        JackCompiler().compile_source(str(bad))
    assert not isinstance(problem.value, JackSemanticError)
    assert problem.value.errors == [f"{bad}:3:17: error: expected an expression, found ';'"]


# --- semantic errors ----------------------------------------------------------------
@pytest.mark.parametrize(
    "body, decls, message, line, column",
    [
        ("        let cuont = 1;", "    static int count;\n", "'cuont' is not declared", 4, 13),
        ("        var int x;\n        var int x;\n        let x = 1;", "", "'x' is already declared in this subroutine", 4, 17),
        ("        do Output.printInt(40000);", "", "integer constant 40000 is too large", 3, 28),
        ("        do Output.printInt(this);", "", "'this' can't be used in function 'main'", 3, 28),
        ("        let size = 1;", "    field int size;\n", "field 'size' can't be used in function 'main'", 4, 13),
        ("        do nope();", "", "class 'Main' has no subroutine named 'nope'", 3, 12),
        ("        do Main.nope();", "", "class 'Main' has no subroutine named 'nope'", 3, 17),
        ("        var boolean flag;\n        let flag = true;\n        do flag.run();", "", "'flag' is a boolean, which has no methods", 5, 12),
    ],
)
def test_semantic_errors_are_located(tmp_path, body, decls, message, line, column):
    vm, diagnostics = diagnose(tmp_path, in_main(body, decls))
    assert vm is None
    error = only(diagnostics)
    assert (error.message, error.line, error.column) == (message, line, column)


def test_semantic_errors_raise_a_semantic_error(tmp_path):
    path = tmp_path / "Main.jack"
    path.write_text(in_main("        let y = 1;"))
    with pytest.raises(JackSemanticError) as problem:
        JackCompiler().compile_source(str(path))
    assert "1 semantic error(s)" in str(problem.value)


def test_did_you_mean(tmp_path):
    error = only(diagnose(tmp_path, in_main("        let cuont = 1;", "    static int count;\n"))[1])
    assert error.help == "did you mean 'count'?"


def test_duplicates_point_back_at_the_first_declaration(tmp_path):
    source = "class Main {\n    function void f() { return; }\n    function void f() { return; }\n}\n"
    error = only(diagnose(tmp_path, source)[1])
    assert error.message == "subroutine 'f' is already defined in class 'Main'"
    assert error.notes == (Note(2, 19, "'f' was first defined here", 1),)


METHODS = """class Main {
    method void draw(int size) { do Output.printInt(size); return; }
    function int twice(int n) { return n + n; }
    function void main() {
        %s
        return;
    }
}
"""


@pytest.mark.parametrize(
    "call, message",
    [
        ("do draw(5);", "can't call method 'draw' from function 'main'"),
        ("do Main.draw(5);", "'draw' is a method, so it needs an object"),
        ("do twice(1);", "'twice' is a function, so call it as 'Main.twice(...)'"),
        ("do Main.twice(1, 2);", "'twice' takes 1 argument but 2 were given"),
    ],
)
def test_calls_within_the_class_are_checked(tmp_path, call, message):
    error = only(diagnose(tmp_path, METHODS % call)[1])
    assert error.message == message


def test_wrong_argument_count_notes_the_declaration(tmp_path):
    error = only(diagnose(tmp_path, METHODS % "do Main.twice();")[1])
    assert error.message == "'twice' takes 1 argument but 0 were given"
    assert error.notes[0].line == 3 and error.notes[0].message == "'twice' is declared here"


def test_missing_return_is_an_error_but_if_else_returns_count(tmp_path):
    source = "class Main {\n    function int f(int a) {\n        if (a) { return 1; }\n    }\n}\n"
    error = only(diagnose(tmp_path, source)[1])
    assert error.message == "function 'f' can reach its end without a 'return'" and error.line == 4
    ok = "class Main {\n    function int f(int a) {\n        if (a) { return 1; } else { return 2; }\n    }\n}\n"
    vm, diagnostics = diagnose(tmp_path, ok)
    assert vm is not None and not diagnostics


# --- warnings --------------------------------------------------------------------
@pytest.mark.parametrize(
    "source, message",
    [
        (in_main("        var int unused;"), "unused variable 'unused'"),
        ("class Main {\n    function void main() {\n        return;\n        do Output.println();\n    }\n}\n",
         "this code will never run: it comes after 'return'"),
        ("class Main {\n    function void main() {\n        return 1;\n    }\n}\n", "void function 'main' returns a value"),
        ("class Main {\n    function int f() {\n        return;\n    }\n}\n", "function 'f' should return a int"),
        ("class Main {\n    constructor Main new() {\n        return 0;\n    }\n}\n", "constructor 'new' should 'return this;'"),
        (in_main("        do output.printInt(1);"), "'output' is not a variable, so this calls a class named 'output'"),
    ],
)
def test_warnings_do_not_stop_compilation(tmp_path, source, message):
    vm, diagnostics = diagnose(tmp_path, source)
    assert vm is not None, [str(d) for d in diagnostics]
    assert only(diagnostics, "warning").message == message


def test_class_and_file_names_should_match(tmp_path):
    vm, diagnostics = diagnose(tmp_path, in_main(""), name="Other")
    assert vm is not None
    assert only(diagnostics, "warning").message == "class 'Main' is in a file named 'Other.jack'"


def test_unused_parameters_are_not_reported(tmp_path):
    vm, diagnostics = diagnose(tmp_path, "class Main {\n    function void f(int a) {\n        return;\n    }\n}\n")
    assert vm is not None and diagnostics == []


# --- no false alarms on real programs ---------------------------------------------------
@pytest.mark.parametrize("path", sorted(SQUARE_DIR.glob("*.jack")), ids=lambda p: p.name)
def test_the_square_game_compiles_without_any_diagnostics(path):
    compiler = JackCompiler()
    compiler.compile_source(str(path))
    assert compiler.diagnostics == []


@pytest.mark.parametrize("path", sorted(EXAMPLES_DIR.glob("*.jack")), ids=lambda p: p.name)
def test_the_examples_have_no_errors(path):
    compiler = JackCompiler()
    compiler.compile_source(str(path))
    # Only "same name as an OS class" (Array.jack, Math.jack) is expected.
    assert all("Jack OS class" in d.message for d in compiler.diagnostics), [str(d) for d in compiler.diagnostics]


# --- rendering --------------------------------------------------------------------
def test_render_shows_the_line_a_caret_help_and_notes():
    diagnostic = Diagnostic(
        "Main.jack", 3, 13, "'x' is already declared", length=1, help="rename one of them",
        notes=(Note(2, 13, "'x' was first declared here"),),
    )  # fmt: skip
    lines = ["class Main {", "    var int x;", "    var int x;"]
    assert render(diagnostic, lines) == "\n".join([
        "Main.jack:3:13: error: 'x' is already declared",
        " 3 |     var int x;",
        "   |             ^",
        "   = help: rename one of them",
        "Main.jack:2:13: note: 'x' was first declared here",
        " 2 |     var int x;",
        "   |             ^",
    ])  # fmt: skip


def test_render_underlines_and_keeps_tabs_aligned():
    assert caret_padding("\tlet x", 6) == "\t    "
    text = render(Diagnostic("A.jack", 1, 2, "bad", length=99), ["\tcount"])
    assert text.splitlines()[-1] == "   | \t^~~~~"  # never past the end of the line


def test_render_without_a_location():
    assert render(Diagnostic("A.jack", 0, 0, "can't read file")) == "A.jack: error: can't read file"


def test_summary():
    assert summary([]) == ""
    errors = [Diagnostic("a", 1, 1, "x"), Diagnostic("a", 1, 1, "y"), Diagnostic("a", 1, 1, "z", "warning")]
    assert summary(errors) == "2 errors and 1 warning generated."


# --- command line ---------------------------------------------------------------------
def _cli(*args):
    with pytest.raises(SystemExit) as done:
        main([str(a) for a in args])
    return done.value.code


def test_cli_prints_compiler_style_errors(tmp_path, capsys):
    bad = tmp_path / "Main.jack"
    bad.write_text(in_main("        let cuont = 1;", "    static int count;\n"))
    assert _cli(bad, "-o", tmp_path / "Main.vm") == 1
    out = capsys.readouterr().out
    assert f"{bad}:4:13: error: 'cuont' is not declared" in out
    assert " 4 |         let cuont = 1;\n   |             ^~~~~" in out
    assert "help: did you mean 'count'?" in out
    assert "1 error generated." in out


def test_cli_warnings_no_warnings_and_werror(tmp_path, capsys):
    source = tmp_path / "Main.jack"
    source.write_text(in_main("        var int unused;"))
    assert _cli(source) == 0
    out = capsys.readouterr().out
    assert "SUCCESS (1 warning)" in out and "warning: unused variable 'unused'" in out

    assert _cli(source, "-w") == 0
    assert "unused" not in capsys.readouterr().out

    (tmp_path / "Main.vm").unlink()
    assert _cli(source, "--werror") == 1
    assert "error: unused variable 'unused' [-Werror]" in capsys.readouterr().out
    assert not (tmp_path / "Main.vm").exists()
