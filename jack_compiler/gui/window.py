"""
window.py - The compiler window: compile, then browse source and VM code.
========================================================================

A pygame front end for the Jack compiler, built like jackvm-py's player
(same colours, framed main view, shortcuts box and info panel).

Window layout
-------------
    +-------------------------------------------------------------------+
    |  margin                                                            |
    |   #=====================================#   +-- STATUS --------+  |
    |   # [Main.jack] [Ball.jack] [Bat.jack]  #   |                  |  |
    |   # +- JACK SOURCE ----+ +- VM CODE ---+ #   +-- FILES ---------+  |
    |   # | 1 class Main {   | | function .. | #   |                  |  |
    |   # | 2   function ... | | push ...    | #   +-- PROBLEMS ------+  |
    |   # +------------------+ +-------------+ #   +-- OUTPUT --------+  |
    |   #=====================================#   +------------------+  |
    |   +-- SHORTCUTS ------------------------+                          |
    +-------------------------------------------------------------------+

When a folder is compiled, the tab bar along the top has one tab per .jack
file: pick a tab (click it, Ctrl+Tab / Ctrl+Shift+Tab, Left / Right, or the
number keys 1-9) to switch BOTH panes to that file. The left pane shows the
selected .jack file; the right pane shows the VM code it compiled to.

Errors and warnings are shown the way a compiler prints them: the line is
shaded (red = error, amber = warning) and a ^~~~ marker under the exact
spot carries the message, with any "help:" suggestion and "note:" (e.g.
where a name was first declared) beneath it. Ctrl+E jumps from problem to
problem; Ctrl+I hides/shows the messages; Ctrl+W makes warnings count as
errors (like jackc --werror) and recompiles. Tabs are coloured like the
FILES box: red for files with errors. The
right-hand column (Ctrl+D hides it) shows how the compilation went.

If JackVM (https://github.com/kpillai2017/jackvm-py) is installed, Ctrl+J
runs the program you're looking at in a second window - see run_in_vm.py.

Compiling runs on a background thread (see session.py), so the window
stays responsive while a big folder compiles. Edit your .jack files in any
editor, then press Ctrl+R here to recompile them.

Esc goes back to the file picker - the same rules as the jackvm player
---------------------------------------------------------------------
  * While a compilation is running, a stray tap of Esc must not throw the
    work away: hold Esc for ESC_HOLD_SECONDS (1 s) to go back. A "keep
    holding" bar appears after ESC_SHOW_BAR_AFTER (0.25 s), so normal
    taps never flash it. Letting go early cancels.
  * Once the compilation has finished, there's nothing left to protect -
    so a single Esc press goes back at once.
  * In the picker, Esc (or "Back") returns to this compilation; the very
    first picker has nothing to return to, so there Esc quits.
  * Ctrl+Q (or closing the window) always quits at once.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pygame

from . import theme
from .file_picker import CHOSEN, QUIT, FilePicker
from .run_in_vm import VMLauncher
from .panel import InfoPanel, build_sections, display_name, largest_sections
from .session import COMPILING, FAILED, IDLE, OK, PENDING, CompileSession
from .annotate import Row, build_rows, row_of_line, visible_line_range
from .syntax import Span, jack_spans, vm_spans

FRAMES_PER_SECOND = 30  # a code viewer doesn't need more

ESC_HOLD_SECONDS = 1.0  # hold Esc this long (while compiling) to go back to the picker
ESC_SHOW_BAR_AFTER = 0.25  # ...and show the "keep holding" bar after this long
FINISHED_HINT_SECONDS = 3.0  # how long "finished - press Esc" shows over the code
NOTICE_SECONDS = 5.0  # how long a message such as "Running in JackVM" shows

# Layout (pixels, or characters where it says so).
MARGIN = 16  # empty space around the code view and the panel
FRAME_WIDTH = 3  # thickness of the border around the code view
FRAME_GAP = 3  # space between the code view and its border
FRAME_EXTENT = FRAME_GAP + FRAME_WIDTH  # how far the frame sticks out
PANE_GAP = 8  # space between the two code panes
PANE_PADDING = 6
GUTTER_CHARS = 5  # line numbers: 4 digits and a space
JACK_COLUMNS = 60  # characters of Jack code shown per line
VM_COLUMNS = 30  # characters of VM code shown per line (VM lines are short)
DEFAULT_CODE_ROWS = 34
SCROLLBAR_WIDTH = 4
TAB_GAP = 4  # space between file tabs
TAB_PADDING = 10  # space either side of a tab's name
TAB_MAX_CHARS = 28  # longer file names are shortened on their tab
TAB_ARROW_WIDTH = 22  # the "<" / ">" buttons shown when the tabs don't all fit

JACK, VM = 0, 1  # the two panes


def tab_window(widths: List[int], available: int, selected: int, first: int = 0, gap: int = TAB_GAP) -> Tuple[int, int]:
    """
    Which tabs fit in `available` pixels: returns (first, stop) so that tabs
    first..stop-1 are drawn. The selected tab is always included, and the
    strip only scrolls when it has to (so tabs don't jump around on every
    click). `first` is where the strip started last time.
    """
    count = len(widths)
    if count == 0:
        return 0, 0
    selected = max(0, min(selected, count - 1))

    def fits(start: int, stop: int) -> bool:
        return sum(widths[start:stop]) + gap * (stop - start - 1) <= available

    first = max(0, min(first, selected))
    while first < selected and not fits(first, selected + 1):
        first += 1  # scroll right until the selected tab fits
    stop = first + 1
    while stop < count and fits(first, stop + 1):
        stop += 1
    while first > 0 and fits(first - 1, stop):
        first -= 1  # room to spare at the end: show more on the left
    return first, max(stop, selected + 1)


class CompilerWindow:
    def __init__(
        self,
        session: CompileSession,
        font_size: int = 13,
        code_rows: int = DEFAULT_CODE_ROWS,
        show_panel: bool = True,
        launcher: Optional[VMLauncher] = None,
    ) -> None:
        self.session = session
        # Ctrl+J: run in JackVM. Looked up once, when the window is made.
        self.launcher = launcher if launcher is not None else VMLauncher()
        self._notice: Optional[Tuple[str, str, float]] = None  # (text, colour, shown until)
        self.font_size = font_size
        self.code_rows = max(5, code_rows)
        self.show_panel = show_panel

        self.selected = 0  # index of the file shown in the code panes
        self.focus = JACK  # which pane the scroll keys move
        self.scroll = [0, 0]  # first visible line of each pane
        self._error_cursor: Optional[int] = None  # line Ctrl+E last jumped to

        # The clock we read. It's an attribute so tests can replace it with a
        # fake clock and "hold" Esc for exactly 1 second without waiting.
        self.now = time.perf_counter
        self._esc_pressed_at: Optional[float] = None  # None = Esc not held
        self._esc_needs_release = False  # True = ignore Esc until it's let go (see go_back)
        self._finished_hint_until: Optional[float] = None
        self._was_compiling = False

        self.inline_messages = True  # show ^~~~ messages under the code (Ctrl+I)
        self._rows: Dict[Tuple[int, int], Tuple[tuple, List[Row]]] = {}
        self._text_cache: Dict[Tuple[str, str], object] = {}
        self._file_rows: List[Tuple[object, int]] = []  # clickable FILES rows
        self._tab_first = 0  # first tab shown in the tab bar
        self._tab_hits: List[Tuple[object, int]] = []  # clickable tabs / arrows -> file index

    # ------------------------------------------------------------------
    # Window setup and layout
    # ------------------------------------------------------------------
    def _open_window(self) -> None:
        pygame.init()
        pygame.display.set_caption(self._title())
        self.panel = InfoPanel(self.font_size)
        self.font = self.panel.font
        self.char_width = self.font.size("M")[0]
        self.line_height = self.font.get_linesize()
        self._resize_window()

    def _resize_window(self) -> None:
        """
        Work out where everything goes, then size the window to fit:

          left column:  the framed code view, and the SHORTCUTS box below it
          right column: the info boxes (if shown)
          MARGIN pixels of empty space around everything
        """
        header = self.panel.header_height
        pane_height = header + PANE_PADDING + self.code_rows * self.line_height + PANE_PADDING
        jack_width = (GUTTER_CHARS + JACK_COLUMNS) * self.char_width + 2 * PANE_PADDING + SCROLLBAR_WIDTH
        vm_width = (GUTTER_CHARS + VM_COLUMNS) * self.char_width + 2 * PANE_PADDING + SCROLLBAR_WIDTH
        tab_height = self.line_height + 10
        # code_rect = the tab bar plus the two panes below it (the frame goes round it).
        self.code_rect = pygame.Rect(MARGIN, MARGIN, jack_width + PANE_GAP + vm_width, tab_height + PANE_GAP + pane_height)
        self.tabs_rect = pygame.Rect(self.code_rect.left, self.code_rect.top, self.code_rect.width, tab_height)
        panes_top = self.tabs_rect.bottom + PANE_GAP
        self.pane_rects = [
            pygame.Rect(self.code_rect.left, panes_top, jack_width, pane_height),
            pygame.Rect(self.code_rect.left + jack_width + PANE_GAP, panes_top, vm_width, pane_height),
        ]

        # The shortcuts box lines up with the outside edges of the frame.
        frame = self.code_rect.inflate(2 * FRAME_EXTENT, 2 * FRAME_EXTENT)
        jackvm = "Ctrl+J run in JackVM" if self.launcher.available else "Ctrl+J JackVM (not installed)"
        self.shortcuts = self.panel.shortcuts_section(frame.width, [jackvm])
        self.shortcuts_rect = pygame.Rect(
            frame.left, frame.bottom + InfoPanel.GAP + 4,
            frame.width, self.panel.box_height(self.shortcuts.row_count),
        )  # fmt: skip

        width = self.code_rect.right + MARGIN
        height = self.shortcuts_rect.bottom + MARGIN
        if self.show_panel:
            width += InfoPanel.WIDTH + MARGIN
            panel_height = self.panel.required_height(largest_sections(self.session))
            height = max(height, MARGIN + panel_height + MARGIN)
        self.window = pygame.display.set_mode((width, height))

    def _title(self) -> str:
        target = self.session.target
        name = target.name + ("/" if target.is_dir() else "")
        files = self.session.total
        return f"Jack Compiler - {name} ({files} file{'s' if files != 1 else ''})"

    # ------------------------------------------------------------------
    # The main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Open the window, compile, and stay open until the user quits."""
        self._open_window()
        if self.session.state == IDLE:
            self.session.start()
        pygame.key.set_repeat(300, 40)  # hold an arrow key to keep scrolling
        clock = pygame.time.Clock()
        try:
            while self._handle_events():
                if self._esc_held_long_enough() and not self.go_back():
                    break  # the user closed the window from the picker
                self._update()
                self._draw()
                clock.tick(FRAMES_PER_SECOND)
        finally:
            pygame.quit()

    # 1. Events -------------------------------------------------------------
    def _handle_events(self) -> bool:
        """Process all waiting events. Returns False when we should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # Ctrl (or Cmd on a Mac) + key = a shortcut.
                if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META):
                    if not self._handle_shortcut(event.key, bool(event.mod & pygame.KMOD_SHIFT)):
                        return False
                    continue
                if event.key == pygame.K_ESCAPE:
                    if self._esc_needs_release:
                        continue  # still the Esc that was held in the picker
                    if self.compilation_finished():
                        if not self.go_back():  # nothing left to protect: back to the picker now
                            return False
                        continue
                    if self._esc_pressed_at is None:  # (ignore key-repeat events)
                        self._esc_pressed_at = self.now()  # start the hold timer
                    continue
                self._handle_key(event.key)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self._esc_pressed_at = None  # let go early: don't go back
                    self._esc_needs_release = False

            elif event.type == pygame.WINDOWFOCUSLOST:
                # Otherwise Esc held while switching windows would "stick".
                self._esc_pressed_at = None
                self._esc_needs_release = False

            elif event.type == pygame.MOUSEWHEEL:
                position = pygame.mouse.get_pos()
                if self.tabs_rect.collidepoint(position):
                    self.select_next(-1 if event.y > 0 else +1)  # wheel over tabs: switch file
                    continue
                pane = self._pane_at(position)
                if pane is not None:
                    self._scroll_by(pane, -3 * event.y)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
        return True

    def compilation_finished(self) -> bool:
        """True once every file has been compiled (successfully or not)."""
        return self.session.finished

    def esc_hold_progress(self) -> float:
        """How far through the 'hold Esc to go back' countdown we are: 0.0 .. 1.0."""
        if self._esc_pressed_at is None:
            return 0.0
        held_for = self.now() - self._esc_pressed_at
        return min(1.0, held_for / ESC_HOLD_SECONDS)

    def _esc_held_long_enough(self) -> bool:
        return self.esc_hold_progress() >= 1.0

    def _handle_shortcut(self, key: int, shift: bool = False) -> bool:
        """React to Ctrl+<key>. Returns False if the user asked to quit."""
        if key == pygame.K_q:
            return False
        if key == pygame.K_TAB:  # Ctrl+Tab / Ctrl+Shift+Tab: next / previous file
            self.select_next(-1 if shift else +1)
        elif key == pygame.K_PAGEDOWN:  # like browser tabs
            self.select_next(+1)
        elif key == pygame.K_PAGEUP:
            self.select_next(-1)
        elif key == pygame.K_r:
            self.recompile()
        elif key == pygame.K_e:
            self.next_problem()
        elif key == pygame.K_i:
            self.toggle_inline_messages()
        elif key == pygame.K_w:
            self.toggle_werror()
        elif key == pygame.K_d:
            self.show_panel = not self.show_panel
            self._resize_window()
        elif key == pygame.K_j:
            self.run_in_vm()
        elif key == pygame.K_o:
            return self._open_something_else()
        return True

    def _handle_key(self, key: int) -> None:
        """Plain (non-Ctrl) keys: scrolling and choosing files."""
        page = self.code_rows - 1
        moves = {
            pygame.K_UP: -1, pygame.K_DOWN: +1,
            pygame.K_PAGEUP: -page, pygame.K_PAGEDOWN: +page,
            pygame.K_HOME: -10**9, pygame.K_END: +10**9,
        }  # fmt: skip
        if key in moves:
            self._scroll_by(self.focus, moves[key])
        elif key == pygame.K_TAB:
            self.focus = VM if self.focus == JACK else JACK
        elif key in (pygame.K_LEFT, pygame.K_LEFTBRACKET):
            self.select(self.selected - 1)
        elif key in (pygame.K_RIGHT, pygame.K_RIGHTBRACKET):
            self.select(self.selected + 1)
        elif pygame.K_1 <= key <= pygame.K_9:  # 1-9: jump straight to that tab
            self.select(key - pygame.K_1)

    def _handle_click(self, position) -> None:
        for rect, index in self._tab_hits:
            if rect.collidepoint(position):
                self.select(index)
                return
        pane = self._pane_at(position)
        if pane is not None:
            self.focus = pane
            return
        for rect, index in self._file_rows:
            if rect.collidepoint(position):
                self.select(index)
                return

    def _pane_at(self, position) -> Optional[int]:
        for pane, rect in enumerate(self.pane_rects):
            if rect.collidepoint(position):
                return pane
        return None

    # --- actions ------------------------------------------------------------
    def select(self, index: int) -> None:
        """Show file `index` (clamped to the list) from the top."""
        index = max(0, min(index, self.session.total - 1))
        if index != self.selected:
            self.selected = index
            self.scroll = [0, 0]
            self._error_cursor = None

    def select_next(self, step: int) -> None:
        """Move `step` files along the tabs, wrapping round at either end."""
        if self.session.total:
            self.select((self.selected + step) % self.session.total)

    def recompile(self) -> bool:
        """Ctrl+R: compile everything again (re-reading the files from disk)."""
        if not self.session.start():
            return False  # already compiling
        self._esc_pressed_at = None
        self._finished_hint_until = None
        return True

    def toggle_werror(self) -> bool:
        """
        Ctrl+W: treat warnings as errors (like jackc --werror), or stop
        doing so, and recompile. Not while compiling: each run reads the
        setting once, so changing it half-way would mix the two.
        Returns True if the setting changed.
        """
        if self.session.state == COMPILING:
            self.notify("Still compiling - press Ctrl+W again when it's finished", "warning")
            return False
        self.session.werror = not self.session.werror
        if self.session.werror:
            self.notify("Warnings now count as errors (--werror): recompiling", "warning")
        else:
            self.notify("Warnings are only warnings again: recompiling")
        self._error_cursor = None
        self.recompile()
        return True

    def run_in_vm(self) -> bool:
        """Ctrl+J: run the selected file's program in JackVM (if it compiled)."""
        started, message = self.launcher.launch(self.session, self.selected)
        self.notify(message, "normal" if started else "error")
        return started

    def notify(self, text: str, colour: str = "normal") -> None:
        """
        Show a short message over the bottom of the code view for a few
        seconds. Only its first line fits; the terminal gets all of it.
        """
        print(text)
        self._notice = (text.split("\n")[0], colour, self.now() + NOTICE_SECONDS)

    def next_problem(self, errors_only: bool = False) -> bool:
        """
        Ctrl+E: jump to the next error or warning, moving on to the next file
        (and wrapping around to the first) when this file has no more.
        Returns False if there are none at all.
        """
        stops: List[Tuple[int, int]] = []  # (file index, line) for every problem
        for index, result in enumerate(self.session.results):
            if result.status == PENDING:
                continue
            problems = result.errors if errors_only else result.diagnostics
            lines = sorted({d.line for d in problems})  # 0 = a problem with no line number
            stops.extend((index, line) for line in lines)
        if not stops:
            return False
        here = (self.selected, self._error_cursor if self._error_cursor is not None else -1)
        index, line = next((stop for stop in stops if stop > here), stops[0])
        self.select(index)
        self.focus = JACK
        self._error_cursor = line
        self.show_line(JACK, line)
        return True

    next_error = next_problem  # the old name

    def toggle_inline_messages(self) -> None:
        """Ctrl+I: show or hide the messages under the code, keeping the same line in view."""
        rows = self._pane_lines(JACK)
        top = visible_line_range(rows, self.scroll[JACK], self.code_rows)[0]
        self.inline_messages = not self.inline_messages
        self.scroll[JACK] = 0
        if top:
            self._scroll_by(JACK, row_of_line(self._pane_lines(JACK), top))

    def show_line(self, pane: int, line: int) -> None:
        """Scroll so 1-based `line` sits about a third of the way down the pane."""
        self.scroll[pane] = 0
        row = row_of_line(self._pane_lines(pane), line) if line > 0 else 0
        self._scroll_by(pane, max(0, row - self.code_rows // 3))

    def _scroll_by(self, pane: int, delta: int) -> None:
        lines = len(self._pane_lines(pane))
        biggest = max(0, lines - self.code_rows)
        self.scroll[pane] = max(0, min(biggest, self.scroll[pane] + delta))

    def go_back(self) -> bool:
        """Esc: back to the file picker (see _open_something_else)."""
        return self._open_something_else()

    def _open_something_else(self) -> bool:
        """
        Ctrl+O (or Esc): show the file picker inside our window. If the user
        picks something, compile it; if they go back, carry on as before.
        Returns False if the user quit from the picker (Ctrl+Q / closed the window).
        """
        self._esc_pressed_at = None  # Esc in the picker means "back here", not "quit"
        target = self.session.target
        start = target if target.is_dir() else target.parent
        width, height = self.window.get_size()
        if width < 800 or height < 560:
            self.window = pygame.display.set_mode((max(width, 800), max(height, 560)))

        outcome, session = choose_target(
            self.window, start, recursive=self.session.recursive, write=self.session.write,
            werror=self.session.werror, back_to=target.name + ("/" if target.is_dir() else ""),
        )
        # If Esc is still down (it was held to get here), its key-repeat must
        # not send us straight back to the picker: wait until it's let go.
        self._esc_needs_release = bool(pygame.key.get_pressed()[pygame.K_ESCAPE])
        if session is not None:
            self.session = session
            self.selected = 0
            self._tab_first = 0
            self.scroll = [0, 0]
            self._error_cursor = None
            self._finished_hint_until = None
            self._rows.clear()
            pygame.display.set_caption(self._title())
            session.start()
        pygame.key.set_repeat(300, 40)  # the picker turned key repeat off
        self._resize_window()  # back to the normal size (the panel may have changed)
        return outcome != QUIT

    # 2. Keep up with the compiler -------------------------------------------
    def _update(self) -> None:
        failure = self.launcher.poll_failure()  # did the JackVM we started crash?
        if failure:
            self.notify(failure, "error")
        compiling = self.session.state == COMPILING
        if self._was_compiling and not compiling:
            self._on_compilation_finished()
        self._was_compiling = compiling

    def _on_compilation_finished(self) -> None:
        self._finished_hint_until = self.now() + FINISHED_HINT_SECONDS
        # Show the first problem straight away, if there is one.
        first_failed = self.session.first_failed_index()
        if first_failed is not None and self.session.results[self.selected].status != FAILED:
            self.select(first_failed)
        if self.session.results[self.selected].status == FAILED:
            self._error_cursor = None
            self.next_problem(errors_only=True)
        else:
            for pane in (JACK, VM):
                self._scroll_by(pane, 0)  # keep scroll positions in range

    # 3. Draw ---------------------------------------------------------------
    def _pane_lines(self, pane: int) -> List[Row]:
        """
        The rows of one pane for the selected file (cached): syntax-coloured
        code, and - in the Jack pane - the compiler's messages under it.
        """
        result = self.session.results[self.selected]
        text = result.source_text if pane == JACK else result.vm_text
        # Rebuild when the text, the diagnostics or the Ctrl+I setting change.
        # (Keeping the objects themselves - not their id()s - means a recompile
        # can never be mistaken for the old text.)
        version = (text, result.diagnostics, self.inline_messages)
        cached = self._rows.get((self.selected, pane))
        if cached is None or not (cached[0][0] is text and cached[0][1] is result.diagnostics
                                  and cached[0][2] == self.inline_messages):  # fmt: skip
            if pane == JACK:
                raw = text.splitlines()
                spans = jack_spans([line.expandtabs(4) for line in raw])
                rows = build_rows(raw, spans, result.diagnostics, JACK_COLUMNS, self.inline_messages)
            else:
                rows = [Row(n, spans) for n, spans in enumerate(vm_spans(text.splitlines()), start=1)]
            cached = (version, rows)
            self._rows[(self.selected, pane)] = cached
        return cached[1]

    def _render(self, text: str, kind: str):
        """font.render, remembered: the same words show up again and again."""
        key = (text, kind)
        image = self._text_cache.get(key)
        if image is None:
            if len(self._text_cache) > 5000:
                self._text_cache.clear()
            image = self.font.render(text, True, theme.COLOURS[kind])
            self._text_cache[key] = image
        return image

    def _draw(self) -> None:
        self.window.fill(theme.BACKGROUND)
        self._draw_tabs()
        for pane in (JACK, VM):
            self._draw_pane(pane)
        frame = self.code_rect.inflate(2 * FRAME_EXTENT, 2 * FRAME_EXTENT)
        pygame.draw.rect(self.window, theme.FRAME_COLOUR, frame, width=FRAME_WIDTH, border_radius=4)
        self.panel.draw_box(self.window, self.shortcuts_rect.x, self.shortcuts_rect.y, self.shortcuts, self.shortcuts_rect.width)
        self._file_rows = []
        if self.show_panel:
            sections = build_sections(self.session, self.selected)
            self._file_rows = self.panel.draw(self.window, self.code_rect.right + FRAME_EXTENT + MARGIN, MARGIN, sections)
        self._draw_quit_hints()
        pygame.display.flip()  # show everything we just drew

    def _tab_label(self, index: int) -> str:
        name = display_name(self.session, self.session.results[index].source)
        if len(name) > TAB_MAX_CHARS:
            name = "..." + name[-(TAB_MAX_CHARS - 3) :]
        return f"{index + 1} {name}" if index < 9 else name  # the number = its 1-9 key

    def _draw_tabs(self) -> None:
        """One tab per file; the selected one is bright and joined to the panes."""
        window, bar = self.window, self.tabs_rect
        labels = [self._tab_label(i) for i in range(self.session.total)]
        widths = [self.font.size(label)[0] + 2 * TAB_PADDING for label in labels]
        overflow = sum(widths) + TAB_GAP * (len(widths) - 1) > bar.width
        left = bar.left + (TAB_ARROW_WIDTH + TAB_GAP if overflow else 0)
        right = bar.right - (TAB_ARROW_WIDTH + TAB_GAP if overflow else 0)
        self._tab_first, stop = tab_window(widths, right - left, self.selected, self._tab_first)
        self._tab_hits = []

        x = left
        for index in range(self._tab_first, stop):
            width = min(widths[index], right - x)
            rect = pygame.Rect(x, bar.top, width, bar.height)
            result = self.session.results[index]
            is_selected = index == self.selected
            fill = theme.BOX_HEADER_FOCUSED if is_selected else theme.BOX_HEADER
            pygame.draw.rect(window, fill, rect, border_top_left_radius=6, border_top_right_radius=6)
            pygame.draw.rect(window, theme.FRAME_COLOUR if is_selected else theme.BORDER, rect, width=1,
                             border_top_left_radius=6, border_top_right_radius=6)  # fmt: skip
            if result.status == FAILED:
                kind = "error"
            elif result.status == OK and result.warnings:
                kind = "warning"
            elif is_selected:
                kind = "highlight"
            else:
                kind = "dim" if result.status == PENDING else "normal"
            clip = window.get_clip()
            window.set_clip(rect.inflate(-4, 0))  # never draw a name outside its tab
            window.blit(self._render(labels[index], kind), (rect.left + TAB_PADDING, rect.top + 5))
            window.set_clip(clip)
            self._tab_hits.append((rect, index))
            x = rect.right + TAB_GAP

        if overflow:  # "<" and ">" step through the files when not all tabs fit
            for label, rect, step in (
                ("<", pygame.Rect(bar.left, bar.top, TAB_ARROW_WIDTH, bar.height), -1),
                (">", pygame.Rect(bar.right - TAB_ARROW_WIDTH, bar.top, TAB_ARROW_WIDTH, bar.height), +1),
            ):
                pygame.draw.rect(window, theme.BOX_HEADER, rect, border_radius=4)
                image = self._render(label, "title")
                window.blit(image, image.get_rect(center=rect.center))
                self._tab_hits.append((rect, (self.selected + step) % self.session.total))

    def _draw_pane(self, pane: int) -> None:
        window, panel = self.window, self.panel
        rect = self.pane_rects[pane]
        result = self.session.results[self.selected]
        rows = self._pane_lines(pane)
        first = self.scroll[pane]

        # Box, title strip (brighter when this pane has the focus) and border.
        pygame.draw.rect(window, theme.BOX, rect, border_radius=InfoPanel.RADIUS)
        header = pygame.Rect(rect.left, rect.top, rect.width, panel.header_height)
        strip = theme.BOX_HEADER_FOCUSED if pane == self.focus else theme.BOX_HEADER
        pygame.draw.rect(
            window, strip, header,
            border_top_left_radius=InfoPanel.RADIUS, border_top_right_radius=InfoPanel.RADIUS,
        )  # fmt: skip
        gutter_width = GUTTER_CHARS * self.char_width + PANE_PADDING
        body = pygame.Rect(rect.left, header.bottom, rect.width, rect.height - panel.header_height)
        pygame.draw.rect(window, theme.GUTTER, (body.left + 1, body.top, gutter_width, body.height - 1))
        pygame.draw.line(window, theme.BORDER, (rect.left, header.bottom), (rect.right - 1, header.bottom))
        pygame.draw.rect(window, theme.BORDER, rect, width=1, border_radius=InfoPanel.RADIUS)

        # Title: what this pane shows, and which lines are visible.
        path = result.source if pane == JACK else result.target
        title = ("JACK  " if pane == JACK else "VM  ") + display_name(self.session, path)
        total_lines = sum(1 for row in rows if row.number is not None)
        if len(rows) > self.code_rows:
            top, bottom = visible_line_range(rows, first, self.code_rows)
            title += f"   {top}-{bottom}/{total_lines}" if top else f"   -/{total_lines}"
        columns = JACK_COLUMNS if pane == JACK else VM_COLUMNS
        title = title if len(title) <= GUTTER_CHARS + columns else title[: GUTTER_CHARS + columns - 3] + "..."
        window.blit(self._render(title, "title"), (rect.left + PANE_PADDING, rect.top + 3))

        # The code itself.
        text_x = rect.left + PANE_PADDING + GUTTER_CHARS * self.char_width
        y = header.bottom + PANE_PADDING
        shades = {"error": theme.ERROR_LINE, "warning": theme.WARNING_LINE}
        for row in rows[first : first + self.code_rows]:
            if row.shade:
                pygame.draw.rect(window, shades[row.shade], (body.left + 1, y, body.width - 2, self.line_height))
            if row.number is not None:  # message rows leave the gutter blank
                label = f"{row.number:>{GUTTER_CHARS - 1}}"
                window.blit(self._render(label, row.shade or "dim"), (rect.left + PANE_PADDING, y))
            self._draw_spans(row.spans, text_x, y, columns)
            y += self.line_height

        if not rows:
            window.blit(self._render(self._empty_message(pane), "dim"), (text_x, y))
        self._draw_scrollbar(body, len(rows), first)

    def _empty_message(self, pane: int) -> str:
        result = self.session.results[self.selected]
        if result.status == PENDING:
            return "(compiling...)"
        if pane == VM and result.status == FAILED:
            return "(no VM code - see PROBLEMS)"
        return "(empty file)"

    def _draw_spans(self, spans: List[Span], x: int, y: int, columns: int) -> None:
        """Draw one coloured line, cutting it off (with a dim ») at `columns`."""
        column = 0
        for text, kind in spans:
            if column >= columns:
                break
            room = columns - column
            if len(text) > room:
                text = text[: room - 1]
                self.window.blit(self._render("»", "dim"), (x + (columns - 1) * self.char_width, y))
                columns = column  # stop after this piece
            if text:
                self.window.blit(self._render(text, kind), (x + column * self.char_width, y))
            column += len(text)

    def _draw_scrollbar(self, body, total: int, first: int) -> None:
        if total <= self.code_rows:
            return
        track = pygame.Rect(body.right - SCROLLBAR_WIDTH - 3, body.top + 4, SCROLLBAR_WIDTH, body.height - 8)
        thumb_height = max(12, track.height * self.code_rows // total)
        thumb_top = track.top + (track.height - thumb_height) * first // max(1, total - self.code_rows)
        pygame.draw.rect(self.window, theme.BOX_HEADER, track, border_radius=2)
        pygame.draw.rect(self.window, theme.BORDER, (track.left, thumb_top, track.width, thumb_height), border_radius=2)

    def _draw_quit_hints(self) -> None:
        """The 'keep holding Esc' bar, or (briefly) a 'press Esc to go back' note."""
        progress = self.esc_hold_progress()
        if self._esc_pressed_at is not None and progress * ESC_HOLD_SECONDS >= ESC_SHOW_BAR_AFTER:
            self._draw_banner("Keep holding Esc to go back...", progress)
        elif self._notice is not None and self.now() < self._notice[2]:
            self._draw_banner(self._notice[0], None, self._notice[1])
        elif self.compilation_finished() and self._finished_hint_until is not None and self.now() < self._finished_hint_until:
            self._draw_banner("Compilation finished - press Esc to go back, Ctrl+Q to quit", None)

    def _draw_banner(self, text: str, progress: Optional[float], colour: str = "normal") -> None:
        """A dark, see-through box over the bottom of the code view."""
        height = 44 if progress is not None else 28
        widest = self.code_rect.width - 20
        while len(text) > 4 and self.font.size(text)[0] + 24 > widest:
            text = text[:-4] + "..."  # too long for the box: cut it short
        box = pygame.Rect(0, 0, min(widest, max(380, self.font.size(text)[0] + 24)), height)
        box.midbottom = (self.code_rect.centerx, self.code_rect.bottom - 10)

        overlay = pygame.Surface(box.size, pygame.SRCALPHA)  # SRCALPHA = allows see-through
        overlay.fill((20, 20, 26, 220))  # the 4th number is opacity (0..255)
        self.window.blit(overlay, box)
        pygame.draw.rect(self.window, theme.FRAME_COLOUR, box, width=1, border_radius=4)

        label = self.font.render(text, True, theme.COLOURS["error"] if colour == "error" else (235, 235, 235))
        self.window.blit(label, label.get_rect(midtop=(box.centerx, box.top + 6)))
        if progress is not None:
            bar = pygame.Rect(box.left + 12, box.bottom - 14, box.width - 24, 6)
            pygame.draw.rect(self.window, (70, 70, 85), bar, border_radius=3)
            filled = bar.copy()
            filled.width = int(bar.width * progress)
            pygame.draw.rect(self.window, theme.COLOURS["error"], filled, border_radius=3)


# ---------------------------------------------------------------------------
# Choosing what to compile with the GUI file picker
# ---------------------------------------------------------------------------
def choose_target(
    surface, start_directory: Path, recursive: bool = False, write: bool = True, message: str = "",
    werror: bool = False, back_to: str = "",
) -> Tuple[str, Optional[CompileSession]]:
    """
    Show the file picker on `surface` until the user picks something that
    can be compiled (or gives up). If the choice can't be used, the picker
    opens again with the problem shown at the top. `back_to` names what Esc
    returns to ("" in the first picker, where Esc quits).

    Returns (outcome, session) - session is None unless outcome is "chosen".
    The session has not been started yet.
    """
    while True:
        outcome, path = FilePicker(surface, start_directory, message, recursive, back_to).run()
        if outcome != CHOSEN or path is None:
            return outcome, None
        try:
            return CHOSEN, CompileSession(path, recursive=recursive, write=write, werror=werror)
        except (FileNotFoundError, OSError) as problem:
            message = str(problem)
            print(message)
            start_directory = path if path.is_dir() else path.parent


def open_picker_window(
    start_directory: Path, recursive: bool = False, write: bool = True, werror: bool = False
) -> Optional[CompileSession]:
    """
    Used when jackc-gui is started without a path: open a window just for
    the picker. Returns the chosen session, or None if the user gave up.
    (The CompilerWindow then reuses and resizes this same window.)
    """
    pygame.init()
    pygame.display.set_caption("Jack Compiler - choose what to compile")
    surface = pygame.display.set_mode((900, 620))
    outcome, session = choose_target(surface, start_directory, recursive, write, werror=werror)
    if session is None:
        pygame.quit()
    return session
