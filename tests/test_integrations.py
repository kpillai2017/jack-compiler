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
    JACKC_GUI,
    JACKVM,
    Companion,
    config_path,
    entry_point_command,
    find,
    not_found_message,
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


# --- the config file ----------------------------------------------------------
def executable(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\n")
    path.chmod(0o755)
    return path


def config(tmp_path, text):
    """A fake home folder with ~/.config/jack-tools/config.ini; returns its environ."""
    path = tmp_path / "home" / ".config" / "jack-tools" / "config.ini"
    path.parent.mkdir(parents=True)
    path.write_text(text)
    return {"HOME": str(tmp_path / "home")}


def test_where_the_config_file_is():
    assert config_path({}) is None  # no home folder: no config file
    assert config_path({"HOME": "/h"}) == Path("/h/.config/jack-tools/config.ini")
    assert config_path({"HOME": "/h", "XDG_CONFIG_HOME": "/x"}) == Path("/x/jack-tools/config.ini")
    assert config_path({"HOME": "/h", "JACK_TOOLS_CONFIG": "/y/my.ini"}) == Path("/y/my.ini")


@pytest.mark.parametrize("venv", ["", "bin", ".venv/bin", "venv/bin", "env/bin", ".direnv/python-3.13/bin"])
def test_a_configured_folder_is_searched_for_the_command(tmp_path, venv):
    command = executable(tmp_path / "anywhere" / "jackvm-py" / venv / "jackvm")
    environ = config(tmp_path, f"[apps]\njackvm = {tmp_path / 'anywhere' / 'jackvm-py'}\n")
    found = find(JACKVM, environ=environ, entry_points=[point("vm", "json.tool:main")], which=lambda n: "/bin/jackvm")
    assert found.command == [str(command)] and found.found_by.startswith("config file ")


def test_a_configured_command_and_off(tmp_path):
    found = find(JACKVM, environ=config(tmp_path, "[apps]\njackvm = python3 -m jackvm\n"), entry_points=[], which=nothing_on_path)
    assert found.command == ["python3", "-m", "jackvm"]
    off = config(tmp_path / "2", "[apps]\njackvm = off\n")
    assert find(JACKVM, environ=off, entry_points=[], which=lambda n: "/bin/jackvm") is None
    assert not_found_message(JACKVM, off).startswith("JackVM is switched off in ~/.config/jack-tools/config.ini")


def test_the_environment_variable_beats_the_config_file(tmp_path):
    environ = {**config(tmp_path, "[apps]\njackvm = python3 -m jackvm\n"), "JACKVM": "/opt/jackvm"}
    assert find(JACKVM, environ=environ, entry_points=[], which=nothing_on_path).command == ["/opt/jackvm"]


def test_jackc_gui_is_found_where_jackc_is(tmp_path):
    gui = executable(tmp_path / "jack-compiler" / ".venv" / "bin" / "jackc-gui")
    executable(gui.parent / "jackc")
    for value in (tmp_path / "jack-compiler", gui.parent / "jackc"):  # its folder, or its command
        environ = config(tmp_path / str(len(str(value))), f"[apps]\njackc = {value}\n")
        assert find(JACKC_GUI, environ=environ, entry_points=[], which=nothing_on_path).command == [str(gui)]


def test_a_folder_without_the_command_falls_back_and_says_why(tmp_path):
    (tmp_path / "empty").mkdir()
    environ = config(tmp_path, f"[apps]\njackvm = {tmp_path / 'empty'}\n")
    assert find(JACKVM, environ=environ, entry_points=[], which=lambda n: "/bin/jackvm").found_by == "PATH"
    assert find(JACKVM, environ=environ, entry_points=[], which=nothing_on_path) is None
    message = not_found_message(JACKVM, environ)
    assert message.startswith(f"No jackvm command in {tmp_path / 'empty'} (set in ~/.config/jack-tools/config.ini)")


@pytest.mark.parametrize("text", ["jackvm = /x\n", "[apps\n", "[apps]\njackvm = 'unclosed\n", "\xff\xfe"])
def test_a_broken_config_file_never_stops_the_lookup(tmp_path, text):
    environ = config(tmp_path, text)
    assert find(JACKVM, environ=environ, entry_points=[], which=lambda n: "/bin/jackvm").found_by == "PATH"


def test_not_found_message_says_how_to_configure_it(tmp_path):
    message = not_found_message(JACKVM, {"HOME": str(tmp_path)})
    first, *rest = message.split("\n")
    assert first == "JackVM not found: set jackvm = <its folder> under [apps] in ~/.config/jack-tools/config.ini"
    assert rest == [f"Or install it here: {JACKVM.install_hint}"]
    assert "couldn't be read" in not_found_message(JACKVM, config(tmp_path / "b", "[apps\n"))


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
    assert not started and message == not_found_message(JACKVM)  # (what it says depends on the setup)


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
