"""
Tests for finding the companion app (integrations.py) and for Ctrl+J
"run in JackVM" (gui/run_in_vm.py). No real JackVM is needed: a tiny Python
script stands in for it, and the lookup is given fake environments.
"""

import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from jack_compiler.gui.run_in_vm import LOG_NAME, VMLauncher, program_results  # noqa: E402
from jack_compiler.gui.session import CompileSession  # noqa: E402
from jack_compiler.integrations import (  # noqa: E402
    JACKC,
    JACKVM,
    Companion,
    entry_point_command,
    find,
)

GOOD = "class Main {\n    function void main() {\n        do Output.printInt(1);\n        return;\n    }\n}\n"
BAD = "class Main {\n    function void main() {\n        let x = 1;\n        return;\n    }\n}\n"


def point(name, value):
    return SimpleNamespace(name=name, value=value)


def nothing_on_path(_name):
    return None


# --- finding the other app ----------------------------------------------------
def test_an_environment_variable_wins_and_can_switch_it_off():
    found = find(JACKVM, environ={"JACKVM": "python3 -m jackvm"}, entry_points=[], which=lambda n: "/bin/jackvm")
    assert found.command == ["python3", "-m", "jackvm"] and found.found_by == "$JACKVM"
    assert find(JACKVM, environ={"JACKVM": "off"}, entry_points=[], which=lambda n: "/bin/jackvm") is None


def test_the_same_python_environment_comes_before_the_path():
    found = find(JACKVM, environ={}, entry_points=[point("vm", "json.tool:main")], which=lambda n: "/bin/jackvm")
    assert found.found_by == "same Python environment"
    assert found.command[0] == sys.executable and "from json.tool import main" in found.command[-1]


def test_stale_installs_and_other_apps_entry_points_are_ignored():
    points = [point("vm", "no_such_module_xyz.main:main"), point("compiler", "json.tool:main")]
    found = find(JACKVM, environ={}, entry_points=points, which=lambda n: f"/usr/local/bin/{n}")
    assert found.command == ["/usr/local/bin/jackvm"] and found.found_by == "PATH"
    assert find(JACKC, environ={}, entry_points=points, which=nothing_on_path).found_by == "same Python environment"


def test_nothing_found_returns_none():
    assert find(JACKVM, environ={}, entry_points=[], which=nothing_on_path) is None


def test_entry_point_commands_really_run():
    # json.tool.main() takes no parameters and reads sys.argv on every Python from 3.8
    command = entry_point_command("json.tool:main", "jsontool")
    done = subprocess.run([*command, "--sort-keys"], input='{"b": 1, "a": 2}', capture_output=True, text=True)
    assert done.returncode == 0 and done.stdout.index('"a"') < done.stdout.index('"b"')


def test_this_package_advertises_itself_for_jackvm_py_to_find():
    found = find(JACKC, environ={}, which=nothing_on_path)
    assert found is not None and found.found_by == "same Python environment"
    assert "jack_compiler.compiler" in found.command[-1]
    done = found.run(["--version"], timeout=60)
    assert done.returncode == 0 and "jackc" in done.stdout


# --- Ctrl+J: running the compiled program ---------------------------------------
FAKE_VM = """
import pathlib, sys
folder = pathlib.Path(sys.argv[1])
names = sorted(p.name for p in folder.glob('*.vm'))
(pathlib.Path(sys.argv[2]) / 'ran.txt').write_text(' '.join(names))
if 'Crash.vm' in names:
    print('Runtime error: stack overflow')
    sys.exit(3)
"""


@pytest.fixture
def fake_vm(tmp_path):
    """A stand-in for jackvm: lists the .vm files it was given, then exits."""
    script = tmp_path / "fake_jackvm.py"
    script.write_text(FAKE_VM)
    marker = tmp_path / "out"
    marker.mkdir()

    class FakeCompanion(Companion):
        def launch(self, args, **options):  # add where to leave ran.txt
            return super().launch([*args, str(marker)], **options)

    return FakeCompanion(JACKVM, [sys.executable, str(script)], "test"), marker


def finished(folder, write=False):
    session = CompileSession(folder, write=write)
    session.run()
    return session


def test_the_program_is_every_file_in_the_selected_tabs_folder(tmp_path):
    for game in ("pong", "tetris"):
        (tmp_path / game).mkdir()
        (tmp_path / game / "Main.jack").write_text(GOOD)
    (tmp_path / "pong" / "Ball.jack").write_text(GOOD.replace("Main", "Ball"))
    session = CompileSession(tmp_path, recursive=True, write=False)
    pong = [i for i, r in enumerate(session.results) if r.source.parent.name == "pong"]
    assert [r.source.name for r in program_results(session, pong[0])] == ["Ball.jack", "Main.jack"]


def test_ctrl_j_runs_the_program_from_a_temporary_folder(tmp_path, fake_vm):
    companion, marker = fake_vm
    src = tmp_path / "src"
    src.mkdir()
    (src / "Main.jack").write_text(GOOD)
    (src / "Old.vm").write_text("function Old.f 0\npush constant 0\nreturn\n")  # compiled earlier
    launcher = VMLauncher(lambda: companion)
    started, message = launcher.launch(finished(src), 0)
    assert started and message == "Running 2 files in JackVM"
    launcher.process.wait(timeout=30)
    assert (marker / "ran.txt").read_text() == "Main.vm Old.vm"
    assert not (src / "Main.vm").exists()  # preview mode: nothing written next to the sources
    assert launcher.poll_failure() is None  # exited cleanly
    folder = launcher.folder
    launcher.stop()
    assert not folder.exists()  # the temporary folder is tidied away


def test_a_crash_is_reported_once_with_what_jackvm_said(tmp_path, fake_vm):
    companion, _ = fake_vm
    (tmp_path / "Crash.jack").write_text(GOOD.replace("Main", "Crash"))
    launcher = VMLauncher(lambda: companion)
    assert launcher.launch(finished(tmp_path), 0)[0]
    launcher.process.wait(timeout=30)
    assert launcher.poll_failure() == "JackVM stopped (exit 3): Runtime error: stack overflow"
    assert launcher.poll_failure() is None
    assert (launcher.folder / LOG_NAME).exists()
    launcher.stop()


def test_ctrl_j_refuses_broken_programs_and_explains_a_missing_jackvm(tmp_path, fake_vm):
    (tmp_path / "Main.jack").write_text(BAD)
    session = finished(tmp_path)
    started, message = VMLauncher(lambda: fake_vm[0]).launch(session, 0)
    assert not started and message == "Fix the errors in Main.jack first"
    missing = VMLauncher(lambda: None)
    assert not missing.available
    started, message = missing.launch(session, 0)
    assert not started and message.startswith("JackVM not found. Install it: git clone")


def test_ctrl_j_waits_for_compiling_to_finish(tmp_path, fake_vm):
    (tmp_path / "Main.jack").write_text(GOOD)
    session = CompileSession(tmp_path, write=False)  # not compiled yet
    assert VMLauncher(lambda: fake_vm[0]).launch(session, 0) == (False, "Still compiling - try again when it's done")


def test_the_default_lookup_respects_jackvm_off():
    assert os.environ["JACKVM"] == "off"  # set by conftest.py
    assert not VMLauncher().available


# --- in the window ----------------------------------------------------------------
pygame = pytest.importorskip("pygame")


def test_window_shortcut_and_notice(tmp_path, fake_vm):
    from jack_compiler.gui.window import CompilerWindow

    (tmp_path / "Main.jack").write_text(GOOD)
    session = finished(tmp_path)
    w = CompilerWindow(session, code_rows=10, launcher=VMLauncher(lambda: fake_vm[0]))
    w._open_window()
    assert any("Ctrl+J run in JackVM" in row for row, _ in w.shortcuts.rows)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_j, mod=pygame.KMOD_CTRL, unicode=""))
    assert w._handle_events()
    assert w._notice[0] == "Running 1 file in JackVM"
    w.launcher.process.wait(timeout=30)
    w._update()
    w._draw()
    w.launcher.stop()

    plain = CompilerWindow(session, code_rows=10, launcher=VMLauncher(lambda: None))
    plain._open_window()
    assert any("Ctrl+J JackVM (not installed)" in row for row, _ in plain.shortcuts.rows)
    assert not plain.run_in_vm() and plain._notice[1] == "error"
    plain._draw()  # a long notice is cut to fit
    pygame.quit()
