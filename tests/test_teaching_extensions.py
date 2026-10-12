"""Keep the combined teaching source, explanations, and runtime results aligned."""

from pathlib import Path

import pytest

from jack_compiler.compiler import JackCompiler, JackSyntaxError

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "teaching" / "extensions"
SOURCE = LESSON / "Main.jack"


def test_teaching_example_compiles_without_warnings():
    code = JackCompiler(extensions=True, werror=True).compile_source(str(SOURCE))
    assert "function Main.main 4" in code
    assert code.count("call Main.countIndex 1") == 1
    for instruction in ("call Math.multiply 2", "call Math.divide 2", "and", "or"):
        assert instruction in code


def test_teaching_example_requires_extension_mode():
    with pytest.raises(JackSyntaxError):
        JackCompiler().compile_source(str(SOURCE))


def test_teaching_doc_links_and_expected_results():
    readme = (LESSON / "README.md").read_text()
    html = (ROOT / "docs" / "language-extensions.html").read_text()
    assert (LESSON / "Main.jack").exists()
    for text in (readme, html):
        for line in ("total = 31", "processed = 5", "index calls = 5", "flags = 3", "state = 6"):
            assert line in text
        assert "--extensions" in text
        assert "build/extensions/Main.vm" in text
        assert "test_teaching_extensions.py" in text
    assert "language-extensions.html" in (ROOT / "docs" / "examples.html").read_text()
    assert "teaching/extensions/README.md" in (ROOT / "README.md").read_text()


@pytest.mark.parametrize("replacement,expected", [
    (None, (31, 5, 5, 3, 6)),
    (("SKIP_AT = 2", "SKIP_AT = 3"), (29, 5, 5, 3, 6)),
    (("STOP_AT = 6", "STOP_AT = 4"), (11, 3, 3, 3, 6)),
    (("if (i = SKIP_AT) { continue; }", ""), (36, 6, 6, 3, 6)),
    (("ACTIVE = 5", "ACTIVE = 10"), (31, 5, 5, 3, 11)),
])
def test_teaching_runtime_and_exercises(tmp_path, replacement, expected):
    vm_module = pytest.importorskip("jackvm.vm")
    source = SOURCE.read_text()
    if replacement:
        assert replacement[0] in source
        source = source.replace(*replacement)
    path = tmp_path / "Main.jack"
    path.write_text(source)
    code = JackCompiler(extensions=True, werror=True).compile_source(str(path))
    vm = vm_module.VirtualMachine()
    vm.load_source(code)
    vm.run(300000)
    assert vm.is_halted(), "teaching program should finish within the tick budget"
    base = vm.static_addresses["Main"]
    assert tuple(vm.peek(base + index) for index in range(5)) == expected
