"""
Tests for the compiler GUI (jackc-gui).

* session / syntax / panel text: plain Python, no window needed.
* The window, picker and Esc handling: SDL's dummy video driver (see
  conftest.py) and a FAKE CLOCK, so a test can "hold Esc for exactly one
  second" without waiting.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from jack_compiler.gui.panel import build_sections, file_window  # noqa: E402
from jack_compiler.gui.session import (  # noqa: E402
    COMPILING,
    DONE,
    FAILED,
    OK,
    CompileSession,
    plan_session_jobs,
)
from jack_compiler.gui.syntax import jack_spans, vm_spans  # noqa: E402

EXAMPLES_DIR = ROOT / "examples"
EXPECTED_DIR = ROOT / "tests" / "expected"

BROKEN = """class Broken {
    function void main() {
        let x = ;
        return;
    }
}
"""


@pytest.fixture
def project(tmp_path):
    """A folder with two good classes and one broken one."""
    for name in ("HelloWorld", "Math"):
        (tmp_path / f"{name}.jack").write_text((EXAMPLES_DIR / f"{name}.jack").read_text())
    (tmp_path / "Broken.jack").write_text(BROKEN)
    return tmp_path


# --- session ---------------------------------------------------------------------
def test_jobs_follow_the_jackc_rules(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "A.jack").write_text("")
    (tmp_path / "sub" / "B.jack").write_text("")
    assert plan_session_jobs(tmp_path / "A.jack") == [(tmp_path / "A.jack", tmp_path / "A.vm")]
    assert [s.name for s, _ in plan_session_jobs(tmp_path)] == ["A.jack"]
    assert [d for _, d in plan_session_jobs(tmp_path, tmp_path / "out", recursive=True)] == [
        tmp_path / "out" / "A.vm",
        tmp_path / "out" / "sub" / "B.vm",
    ]


def test_a_folder_compiles_writes_good_files_and_reports_errors(project):
    session = CompileSession(project)
    session.run()
    assert session.state == DONE and session.finished
    by_name = {r.source.name: r for r in session.results}
    assert by_name["HelloWorld.jack"].status == OK
    assert by_name["HelloWorld.jack"].written
    assert (project / "HelloWorld.vm").read_text() == (EXPECTED_DIR / "HelloWorld.vm").read_text()

    broken = by_name["Broken.jack"]
    assert broken.status == FAILED and not broken.written
    assert not (project / "Broken.vm").exists()
    assert broken.error_lines == [3]
    assert broken.source_text == BROKEN
    assert (session.ok_count, session.failed_count) == (2, 1)
    assert session.first_failed_index() == session.results.index(broken)


def test_no_write_never_touches_the_disk(project):
    session = CompileSession(project, write=False)
    session.run()
    assert session.ok_count == 2
    assert not list(project.glob("*.vm"))
    assert "preview" in session.describe_output()


def test_background_compile_and_recompile_after_an_edit(project):
    session = CompileSession(project / "Broken.jack")
    assert session.start()
    assert session.wait(10)
    assert session.results[0].status == FAILED
    (project / "Broken.jack").write_text(BROKEN.replace("let x = ;", "do Output.printInt(1);"))
    assert session.start()
    assert session.wait(10)
    assert session.results[0].status == OK and (project / "Broken.vm").exists()


def test_empty_or_missing_inputs_are_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        CompileSession(tmp_path)  # no .jack files
    with pytest.raises(FileNotFoundError):
        CompileSession(tmp_path / "nope.jack")


# --- syntax colouring -------------------------------------------------------------
def test_spans_rebuild_each_line_exactly():
    jack = ['  let s = "a // b"; // note', "/* start", " still */ return 12;", "\tdo x.y();"]
    vm = ["function Main.main 2", "    push   constant 7   // seven", "label L1", ""]
    for lines, spans in ((jack, jack_spans(jack)), (vm, vm_spans(vm))):
        assert ["".join(text for text, _ in line) for line in spans] == lines


def test_jack_colouring_handles_strings_comments_and_keywords():
    spans = jack_spans(['let s = "a // b"; // note', "/* start", " still */ return 12;"])
    assert ("let", "keyword") in spans[0]
    assert ('"a // b"', "string") in spans[0]
    assert ("// note", "comment") in spans[0]
    assert spans[1] == [("/* start", "comment")]
    assert spans[2][0] == (" still */", "comment")
    assert ("return", "keyword") in spans[2] and ("12", "number") in spans[2]


def test_vm_colouring_picks_out_functions_and_labels():
    spans = vm_spans(["function Main.main 2", "if-goto LOOP", "push constant 7"])
    assert spans[0][0] == ("function", "keyword")
    assert ("LOOP", "label") in spans[1]
    assert ("7", "number") in spans[2]


# --- panel text -----------------------------------------------------------------
def test_panel_describes_the_session_and_selected_file(project):
    session = CompileSession(project)
    session.run()
    broken = next(i for i, r in enumerate(session.results) if r.status == FAILED)
    status, files, errors, output = build_sections(session, broken)
    assert status.rows[0] == ("FAILED - 1 of 3 with errors", "error")
    assert any("press Esc to quit" in text for text, _ in status.rows)
    assert files.targets == [0, 1, 2]
    assert files.rows[broken][0].startswith("> ERR")
    assert errors.title == "PROBLEMS: Broken.jack"
    assert errors.rows[0][0].startswith("3:17 error: expected an expression")
    assert errors.rows[0][1] == "error"
    assert "not saved" in output.rows[1][0]


def test_boxes_keep_their_height_while_compiling_and_when_done(project):
    session = CompileSession(project)
    before = [s.row_count for s in build_sections(session, 0)]
    session.run()
    assert [s.row_count for s in build_sections(session, 0)] == before


def test_file_window_keeps_the_selection_visible():
    assert file_window(5, 3, rows=10) == range(5)
    assert 25 in file_window(40, 25, rows=10)
    assert file_window(40, 39, rows=10) == range(30, 40)


# --- the window (pygame, dummy video driver) ------------------------------------------
pygame = pytest.importorskip("pygame")

from jack_compiler.gui import window as window_module  # noqa: E402
from jack_compiler.gui.file_picker import CANCEL, CHOSEN, FilePicker, PickerState  # noqa: E402
from jack_compiler.gui.window import ESC_HOLD_SECONDS, JACK, VM, CompilerWindow  # noqa: E402


class FakeClock:
    """Stands in for time.perf_counter(); we move time forward by hand."""

    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t


def make_window(session):
    w = CompilerWindow(session, code_rows=10)
    w.now = FakeClock()
    w._open_window()
    return w


@pytest.fixture
def busy_window(project):
    """A window whose session is (pretend) still compiling."""
    session = CompileSession(project)
    session.state = COMPILING
    w = make_window(session)
    yield w
    pygame.quit()


@pytest.fixture
def done_window(project):
    session = CompileSession(project)
    session.run()
    w = make_window(session)
    yield w
    pygame.quit()


def send(w, *events):
    """Put events in pygame's queue and let the window handle them."""
    for event in events:
        pygame.event.post(event)
    return w._handle_events()


def key_down(key, mod=0):
    return pygame.event.Event(pygame.KEYDOWN, key=key, mod=mod, unicode="")


def key_up(key):
    return pygame.event.Event(pygame.KEYUP, key=key, mod=0)


# Esc while compiling: the same rules as jackvm's player.
def test_a_quick_esc_tap_while_compiling_does_not_quit(busy_window):
    w = busy_window
    assert send(w, key_down(pygame.K_ESCAPE)) is True
    w.now.t += 0.2
    assert send(w, key_up(pygame.K_ESCAPE)) is True
    assert w.esc_hold_progress() == 0.0
    assert not w._esc_held_long_enough()


def test_holding_esc_for_one_second_quits_while_compiling(busy_window):
    w = busy_window
    send(w, key_down(pygame.K_ESCAPE))
    w.now.t += ESC_HOLD_SECONDS / 2
    assert w.esc_hold_progress() == pytest.approx(0.5)
    # Key-repeat sends more KEYDOWNs while held: they must not restart the timer.
    send(w, key_down(pygame.K_ESCAPE))
    w.now.t += ESC_HOLD_SECONDS / 2
    assert w._esc_held_long_enough()


def test_letting_go_or_switching_windows_cancels(busy_window):
    w = busy_window
    send(w, key_down(pygame.K_ESCAPE))
    w.now.t += 0.9
    send(w, key_up(pygame.K_ESCAPE))
    w.now.t += 0.5
    assert not w._esc_held_long_enough()
    send(w, key_down(pygame.K_ESCAPE))
    w.now.t += 0.5
    send(w, pygame.event.Event(pygame.WINDOWFOCUSLOST))
    w.now.t += 0.6
    assert w.esc_hold_progress() == 0.0


def test_the_keep_holding_bar_is_drawn(busy_window):
    w = busy_window
    send(w, key_down(pygame.K_ESCAPE))
    w.now.t += 0.5
    w._draw()
    x = w.code_rect.centerx - 100  # inside the filled (left) half of the bar
    reds = [y for y in range(w.code_rect.top, w.code_rect.bottom) if w.window.get_at((x, y))[:3] == (255, 110, 110)]
    assert reds, "the red progress bar should be on screen"


def test_one_esc_press_quits_once_compilation_has_finished(done_window):
    assert send(done_window, key_down(pygame.K_ESCAPE)) is False


def test_ctrl_q_quits_and_other_shortcuts_dont(busy_window):
    w = busy_window
    assert send(w, key_down(pygame.K_d, pygame.KMOD_CTRL)) is True
    assert send(w, key_down(pygame.K_q, pygame.KMOD_CTRL)) is False


# Browsing the results.
def test_finishing_jumps_to_the_first_error(project):
    session = CompileSession(project)
    w = make_window(session)
    session.start()
    w._update()  # notices it is compiling
    session.wait(10)
    w._update()  # notices it has finished
    assert session.results[w.selected].status == FAILED
    assert w._error_cursor == 3 and w.focus == JACK
    w._draw()
    pygame.quit()


def test_scrolling_tab_and_choosing_files(done_window, project):
    w = done_window
    w.session.results[0].source_text = "\n".join(f"// line {n}" for n in range(1, 61))
    w.session.results[0].vm_text = "\n".join(f"push constant {n}" for n in range(1, 61))
    w.select(1)
    w.select(0)
    send(w, key_down(pygame.K_PAGEDOWN))
    assert w.scroll[JACK] == w.code_rows - 1
    send(w, key_down(pygame.K_END))
    lines = len(w._pane_lines(JACK))
    assert w.scroll[JACK] == lines - w.code_rows
    send(w, key_down(pygame.K_HOME), key_down(pygame.K_TAB), key_down(pygame.K_DOWN))
    assert w.scroll == [0, 1] and w.focus == VM
    selected = w.selected
    send(w, key_down(pygame.K_RIGHT))
    assert w.selected == min(selected + 1, w.session.total - 1) and w.scroll == [0, 0]
    send(w, key_down(pygame.K_LEFT), key_down(pygame.K_LEFT), key_down(pygame.K_LEFT), key_down(pygame.K_LEFT))
    assert w.selected == 0


def test_clicking_a_file_in_the_panel_selects_it(done_window):
    w = done_window
    w._draw()
    rect, index = w._file_rows[2]
    send(w, pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert w.selected == index == 2


def test_ctrl_e_cycles_through_errors_and_warnings(done_window):
    w = done_window
    name = lambda: w.session.results[w.selected].source.name  # noqa: E731
    assert w.next_problem()
    assert (name(), w._error_cursor) == ("Broken.jack", 3)
    assert w.next_problem()  # Math.jack: "same name as a Jack OS class" warning
    assert (name(), w._error_cursor) == ("Math.jack", 4)
    assert w.next_problem()  # wraps round
    assert (name(), w._error_cursor) == ("Broken.jack", 3)
    assert w.next_problem(errors_only=True) and (name(), w._error_cursor) == ("Broken.jack", 3)


def test_ctrl_r_recompiles_after_an_edit(done_window, project):
    w = done_window
    (project / "Broken.jack").write_text(BROKEN.replace("let x = ;", "do Output.printInt(1);"))
    assert send(w, key_down(pygame.K_r, pygame.KMOD_CTRL)) is True
    w.session.wait(10)
    assert w.session.failed_count == 0


def test_layout_has_margins_two_panes_and_the_panel(done_window):
    w = done_window
    w._draw()
    width, height = w.window.get_size()
    jack, vm = w.pane_rects
    assert jack.right < vm.left and vm.right == w.code_rect.right
    assert w.shortcuts_rect.bottom <= height - 16
    assert width >= w.code_rect.right + 16 + 360 + 16
    send(w, key_down(pygame.K_d, pygame.KMOD_CTRL))
    assert w.window.get_size()[0] < width


def test_long_lines_are_cut_off_with_a_marker(tmp_path):
    (tmp_path / "Long.jack").write_text("class Long { // " + "x" * 200 + "\n}\n")
    session = CompileSession(tmp_path, write=False)
    session.run()
    w = make_window(session)
    w._draw()  # must not draw past the pane (or crash)
    pygame.quit()


# The picker.
def test_picker_lists_folders_and_jack_files(project):
    (project / "sub").mkdir()
    (project / "sub" / "A.jack").write_text("class A {}")
    (project / "notes.txt").write_text("")
    state = PickerState(project)
    kinds = [(e.kind, e.path.name) for e in state.entries]
    assert kinds[0][0] == "parent"
    assert ("folder", "sub") in kinds and ("jack", "Broken.jack") in kinds
    assert all(name != "notes.txt" for _, name in kinds)
    folder = next(i for i, e in enumerate(state.entries) if e.kind == "folder")
    assert state.entries[folder].jack_count == 1
    assert state.compile_folder_entry(folder) == project / "sub"
    assert state.compile_current_folder() == project.resolve()


def test_picker_explains_folders_without_jack_files(tmp_path):
    (tmp_path / "empty").mkdir()
    state = PickerState(tmp_path)
    assert state.compile_current_folder() is None
    assert "no .jack files" in state.message


def test_picker_keyboard_and_esc(project):
    pygame.init()
    surface = pygame.display.set_mode((900, 620))
    picker = FilePicker(surface, project)
    picker.draw()
    jack_row = next(i for i, e in enumerate(picker.state.entries) if e.kind == "jack")
    picker.state.selected = jack_row
    outcome, path = picker._handle_event(key_down(pygame.K_RETURN))
    assert outcome == CHOSEN and path.suffix == ".jack"
    assert picker._handle_event(key_down(pygame.K_ESCAPE)) == (CANCEL, None)
    pygame.quit()


def test_ctrl_o_switches_to_a_new_target_or_keeps_the_old_one(done_window, project, monkeypatch):
    w = done_window
    old = w.session
    monkeypatch.setattr(window_module, "choose_target", lambda *a, **k: (CANCEL, None))
    assert send(w, key_down(pygame.K_o, pygame.KMOD_CTRL)) is True
    assert w.session is old

    new = CompileSession(project / "Math.jack", write=False)
    monkeypatch.setattr(window_module, "choose_target", lambda *a, **k: (CHOSEN, new))
    assert send(w, key_down(pygame.K_o, pygame.KMOD_CTRL)) is True
    assert w.session is new and new.wait(10) and new.ok_count == 1


# The file tabs above the code panes.
from jack_compiler.gui.window import tab_window  # noqa: E402


def test_tab_window_keeps_the_selected_tab_visible_and_scrolls_lazily():
    widths = [100] * 10
    assert tab_window(widths, 10 * 100 + 9 * 4, 0) == (0, 10)  # everything fits (tabs + gaps)
    first, stop = tab_window(widths, 350, 7, first=0)  # 3 tabs fit
    assert first <= 7 < stop and stop - first == 3
    assert tab_window(widths, 350, 6, first=first) == (first, stop)  # still visible: don't move
    assert tab_window(widths, 350, 0, first=first)[0] == 0
    assert tab_window([500], 100, 0) == (0, 1)  # an over-wide tab still shows


def test_clicking_a_tab_switches_both_panes(done_window):
    w = done_window
    w._draw()
    assert [index for _, index in w._tab_hits] == list(range(w.session.total))
    good = next(i for i, r in enumerate(w.session.results) if r.status == OK and i != w.selected)
    rect, index = w._tab_hits[good]
    send(w, pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert w.selected == index == good
    result = w.session.results[good]
    assert "".join(t for t, _ in w._pane_lines(JACK)[0].spans) == result.source_text.expandtabs(4).splitlines()[0]
    assert "".join(t for t, _ in w._pane_lines(VM)[0].spans) == result.vm_text.splitlines()[0]


def test_ctrl_tab_number_keys_and_wheel_switch_files(done_window):
    w = done_window
    w._draw()
    last = w.session.total - 1
    send(w, key_down(pygame.K_TAB, pygame.KMOD_CTRL | pygame.KMOD_SHIFT))
    assert w.selected == last  # wraps round backwards
    send(w, key_down(pygame.K_TAB, pygame.KMOD_CTRL))
    assert w.selected == 0  # ...and forwards
    send(w, key_down(pygame.K_PAGEDOWN, pygame.KMOD_CTRL))
    assert w.selected == 1
    send(w, key_down(pygame.K_3))
    assert w.selected == 2
    pygame.mouse.set_pos(w.tabs_rect.center)
    if pygame.mouse.get_pos() == w.tabs_rect.center:  # some dummy drivers can't move the mouse
        send(w, pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=1, flipped=False))
        assert w.selected == 1


def test_many_files_get_arrows_and_the_selected_tab_stays_on_screen(tmp_path):
    for n in range(30):
        (tmp_path / f"VeryLongClassName{n:02}.jack").write_text(f"class VeryLongClassName{n:02} {{}}\n")
    session = CompileSession(tmp_path, write=False)
    session.run()
    w = make_window(session)
    w.select(25)
    w._draw()
    tabs = [(rect, i) for rect, i in w._tab_hits if rect.width > 30]
    assert 25 in [i for _, i in tabs]
    assert all(w.tabs_rect.contains(rect) for rect, _ in w._tab_hits)
    arrows = [(rect, i) for rect, i in w._tab_hits if rect.width <= 30]
    assert [i for _, i in arrows] == [24, 26]  # "<" and ">"
    send(w, pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=arrows[1][0].center))
    assert w.selected == 26
    pygame.quit()


# Compiler-style messages under the code.
from jack_compiler.diagnostics import Diagnostic, Note  # noqa: E402
from jack_compiler.gui.annotate import build_rows, message_rows, row_of_line  # noqa: E402


def _text(row):
    return "".join(t for t, _ in row.spans)


def test_messages_go_under_their_line_with_a_caret():
    raw = ["class A {", "\tlet x = ;", "}"]
    spans = jack_spans([line.expandtabs(4) for line in raw])
    error = Diagnostic("A.jack", 2, 10, "expected an expression, found ';'", help="add one")
    rows = build_rows(raw, spans, [error], columns=60)
    assert [r.number for r in rows] == [1, 2, None, None, 3]
    assert rows[1].shade == "error"
    # Column 10 of "\tlet x = ;" is the ';' - 12 characters in once the tab is expanded.
    assert _text(rows[2]) == " " * 12 + "^ error: expected an expression, found ';'"
    assert _text(rows[3]).strip() == "= help: add one"
    assert row_of_line(rows, 3) == 4
    assert [r.number for r in build_rows(raw, spans, [error], 60, inline=False)] == [1, 2, 3]


def test_long_messages_wrap_and_notes_appear_at_their_own_line():
    raw = ["var int x;", "var int x;"]
    spans = jack_spans(raw)
    duplicate = Diagnostic("A.jack", 2, 9, "'x' is already declared in this subroutine",
                           notes=(Note(1, 9, "'x' was first declared here"),))  # fmt: skip
    rows = build_rows(raw, spans, [duplicate], columns=30)
    line_two = rows.index(next(r for r in rows if r.number == 2))
    note_text = " ".join(_text(r).strip() for r in rows[1:line_two])
    assert rows[0].number == 1 and "note:" in note_text
    assert "'x' was first declared here" in " ".join(note_text.split())
    caret_row = line_two + 1
    assert _text(rows[caret_row]).strip() == "^"  # message too long: it wraps below the caret
    assert all(len(_text(r)) <= 30 for r in rows)
    assert message_rows("", Diagnostic("A", 1, 1, "x", "warning"), 20)[0][1] == ("^", "warning")


def test_warnings_shade_amber_and_ctrl_i_hides_the_messages(tmp_path):
    (tmp_path / "Main.jack").write_text(
        "class Main {\n    function void main() {\n        var int unused;\n        return;\n    }\n}\n"
    )
    session = CompileSession(tmp_path, write=False)
    session.run()
    w = make_window(session)
    rows = w._pane_lines(JACK)
    assert rows[2].shade == "warning" and rows[3].number is None
    assert "warning: unused variable 'unused'" in _text(rows[3])
    send(w, key_down(pygame.K_i, pygame.KMOD_CTRL))
    assert [r.number for r in w._pane_lines(JACK)] == [1, 2, 3, 4, 5, 6]
    status, files, problems, output = build_sections(session, 0)
    assert status.rows[0] == ("DONE - all 1 compiled, 1 warning", "warning")
    assert files.rows[0][0].startswith("> warn")
    assert problems.rows[0] == ("3:17 warning: unused variable 'unused'", "warning")
    w._draw()
    pygame.quit()


# --- warnings as errors (--werror / Ctrl+W) ---------------------------------------
WARNS = """class Warns {
    function void main() {
        var int unused;
        return;
    }
}
"""


@pytest.fixture
def warning_project(tmp_path):
    (tmp_path / "Warns.jack").write_text(WARNS)
    return tmp_path


def test_werror_makes_a_file_with_warnings_fail_like_jackc(warning_project):
    session = CompileSession(warning_project)
    session.run()
    assert session.failed_count == 0 and session.warning_count == 1
    (warning_project / "Warns.vm").unlink()

    session = CompileSession(warning_project, werror=True)
    session.run()
    result = session.results[0]
    assert result.status == FAILED and not result.written
    assert [d.message for d in result.errors] == ["unused variable 'unused' [-Werror]"]
    assert not (warning_project / "Warns.vm").exists()


def status_lines(session):
    return [text for text, _ in build_sections(session, 0)[0].rows]


def test_ctrl_w_switches_werror_and_recompiles(warning_project):
    session = CompileSession(warning_project, write=False)
    session.run()
    w = make_window(session)
    try:
        assert "warnings don't stop a file (Ctrl+W)" in status_lines(session)
        rows_before = build_sections(session, 0)[0].row_count

        assert send(w, key_down(pygame.K_w, pygame.KMOD_CTRL)) is True
        assert session.werror and session.wait(10)
        assert session.failed_count == 1
        assert "warnings count as errors (--werror)" in status_lines(session)
        assert build_sections(session, 0)[0].row_count == rows_before  # the box doesn't change size
        assert "--werror" in w._notice[0]

        send(w, key_down(pygame.K_w, pygame.KMOD_CTRL))
        assert not session.werror and session.wait(10)
        assert session.failed_count == 0 and session.warning_count == 1
    finally:
        pygame.quit()


def test_ctrl_w_waits_while_compiling(busy_window):
    w = busy_window
    assert w.toggle_werror() is False
    assert w.session.werror is False and "Still compiling" in w._notice[0]


def test_ctrl_w_is_listed_in_the_shortcuts(done_window):
    assert any("Ctrl+W" in text for text, _ in done_window.shortcuts.rows)


def test_ctrl_o_keeps_the_werror_setting(done_window, monkeypatch):
    w = done_window
    w.session.werror = True
    seen = {}

    def fake_choose_target(*args, **kwargs):
        seen.update(kwargs)
        return CANCEL, None

    monkeypatch.setattr(window_module, "choose_target", fake_choose_target)
    send(w, key_down(pygame.K_o, pygame.KMOD_CTRL))
    assert seen["werror"] is True


def test_jackc_gui_werror_option(warning_project, monkeypatch):
    from jack_compiler.gui import main as gui_main

    opened = []
    monkeypatch.setattr(window_module.CompilerWindow, "run", lambda self: opened.append(self.session))
    assert gui_main.main(["--werror", "--no-write", str(warning_project)]) == 0
    assert opened[0].werror is True
    assert gui_main.main(["--no-write", str(warning_project)]) == 0
    assert opened[1].werror is False
