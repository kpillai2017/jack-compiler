"""
panel.py - The info boxes on the right of the window.
====================================================

The same idea as jackvm-py's debugger panel: `build_sections()` describes
what to show as plain data (a list of Sections - titled boxes holding rows
of text), and `InfoPanel` draws them as bordered boxes.

    +-- STATUS ------------------+
    | DONE - 4 ok, 1 failed      |
    | examples/  (5 files)       |
    +-- FILES (4 ok, 1 failed) --+
    | > ERR  Broken.jack         |
    |   ok   HelloWorld.jack     |
    +-- PROBLEMS: Broken.jack ---+
    | 3:17 error: expected an    |
    |   expression, found ';'    |
    +-- OUTPUT ------------------+
    | Broken.vm                  |
    +----------------------------+

Keeping "what to show" apart from "how to draw it" means the text can be
tested without opening a window.

Every box reserves a fixed number of rows (`min_rows`), so the boxes never
jump up and down as files compile or you select another file.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from . import theme
from .session import COMPILING, DONE, FAILED, OK, PENDING, CompileSession

# Each row of a section is (text, colour-name). Colours are chosen in draw().
Line = Tuple[str, str]

PANEL_CHARS = 42  # characters that fit across a box
FILE_ROWS = 10  # how many files the FILES box lists at once
ERROR_ROWS = 7  # rows in the PROBLEMS box (longer lists are cut short)

# Shown in the SHORTCUTS box under the code view. The items are laid out
# left to right and wrap onto a new row when the box is full ("flow layout").
HELP_ITEMS = [
    "Up/Down/PgUp/PgDn scroll",
    "Tab switch pane",
    "Ctrl+Tab / Left/Right / 1-9 switch file",
    "Ctrl+E next problem",
    "Ctrl+I messages",
    "Ctrl+R recompile",
    "Ctrl+W warnings=errors",
    "Ctrl+O open",
    "Ctrl+D panel",
    "Ctrl+Q quit",
    "Esc back to picker (hold 1 s if busy)",
]
HELP_SEPARATOR = "   "

STATUS_MARKS = {PENDING: "..  ", OK: "ok  ", FAILED: "ERR "}
STATUS_COLOURS = {PENDING: "dim", OK: "normal", FAILED: "error"}


def file_mark(result) -> Tuple[str, str]:
    """(4-character mark, colour) for a file in the FILES box."""
    if result.status == OK and result.warnings:
        return "warn", "warning"
    return STATUS_MARKS[result.status], STATUS_COLOURS[result.status]


def counted(count: int, word: str) -> str:
    return f"{count} {word}{'s' if count != 1 else ''}"


def describe_problem(diagnostic) -> str:
    """'3:17 error: expected ...' (or just 'error: ...' when not on a line)."""
    where = f"{diagnostic.line}:{diagnostic.column} " if diagnostic.line > 0 else ""
    return f"{where}{diagnostic.severity}: {diagnostic.message}"


@dataclass
class Section:
    """One box of the panel: a title and some rows of text."""

    title: str
    rows: List[Line] = field(default_factory=list)
    # Always reserve at least this many rows, so the boxes below don't jump.
    min_rows: int = 0
    # Optional: for each row, the index of the file that clicking it selects.
    targets: List[Optional[int]] = field(default_factory=list)

    def add(self, text: str = "", colour: str = "normal", target: Optional[int] = None) -> None:
        self.rows.append((text, colour))
        self.targets.append(target)

    @property
    def row_count(self) -> int:
        return max(len(self.rows), self.min_rows)


def fit_left(text: str, width: int = PANEL_CHARS) -> str:
    """Shorten from the LEFT, keeping the useful end: '...projects/Square'."""
    return text if len(text) <= width else "..." + text[-(width - 3) :]


def wrap(text: str, width: int = PANEL_CHARS) -> List[str]:
    """Break text between words so it fits across a box."""
    return textwrap.wrap(text, width) or [""]


def display_name(session: CompileSession, path: Path) -> str:
    """A file's name as shown in lists: relative to the folder being compiled."""
    base = session.target if session.target.is_dir() else session.target.parent
    try:
        return str(path.relative_to(base))
    except ValueError:
        return path.name


def file_window(total: int, selected: int, rows: int = FILE_ROWS) -> range:
    """Which file indexes to list so the selected one is always visible."""
    if total <= rows:
        return range(total)
    first = max(0, min(selected - rows // 2, total - rows))
    return range(first, first + rows)


def build_sections(session: CompileSession, selected: int) -> List[Section]:
    """Describe the session (and the selected file) as Sections, top to bottom."""
    sections: List[Section] = []
    results = session.results
    selected = max(0, min(selected, len(results) - 1))
    current = results[selected]

    # --- status -----------------------------------------------------------
    output_lines = wrap(session.describe_output())
    # state + target + output + warnings + time + "press Esc" hint (only once finished)
    box = Section("STATUS", min_rows=5 + len(output_lines))
    if session.state == COMPILING:
        box.add(f"COMPILING {session.completed}/{session.total}", "highlight")
    elif session.state == DONE and session.failed_count:
        box.add(f"FAILED - {session.failed_count} of {session.total} with errors", "error")
    elif session.state == DONE and session.warning_count:
        box.add(f"DONE - all {session.total} compiled, {counted(session.warning_count, 'warning')}", "warning")
    elif session.state == DONE:
        box.add(f"DONE - all {session.total} compiled", "ok")
    else:
        box.add("READY", "normal")
    kind = "folder" if session.target.is_dir() else "file"
    box.add(fit_left(f"{kind}: {session.target.name or session.target}"))
    for line in output_lines:
        box.add(line, "dim")
    # Always one line, so switching it (Ctrl+W) doesn't change the box's size.
    if session.werror:
        box.add("warnings count as errors (--werror)", "warning")
    else:
        box.add("warnings don't stop a file (Ctrl+W)", "dim")
    box.add(f"time   {session.elapsed:.2f} s", "dim")
    if session.finished:
        box.add("Compilation finished: Esc to go back", "dim")
    sections.append(box)

    # --- files --------------------------------------------------------------
    title = f"FILES ({session.ok_count} ok, {session.failed_count} failed, {session.total} total)"
    box = Section(title, min_rows=min(FILE_ROWS, session.total) + (1 if session.total > FILE_ROWS else 0))
    shown = file_window(session.total, selected)
    for index in shown:
        result = results[index]
        pointer = ">" if index == selected else " "
        mark, colour = file_mark(result)
        colour = "highlight" if index == selected else colour
        text = f"{pointer} {mark}{display_name(session, result.source)}"
        box.add(fit_left(text), colour, target=index)
    if session.total > FILE_ROWS:
        box.add(f"  {shown.start + 1}-{shown.stop} of {session.total}  (Ctrl+Tab)", "dim")
    sections.append(box)

    # --- errors and warnings in the selected file ---------------------------------
    box = Section(fit_left(f"PROBLEMS: {current.source.name}"), min_rows=ERROR_ROWS)
    if current.status == PENDING:
        box.add("(not compiled yet)", "dim")
    elif not current.diagnostics:
        box.add("(none)", "dim")
    else:
        lines: List[Line] = []
        for problem in current.diagnostics:
            colour = "error" if problem.is_error else "warning"
            for index, piece in enumerate(wrap(describe_problem(problem), PANEL_CHARS - 2)):
                lines.append((piece if index == 0 else "  " + piece, colour))
        if len(lines) > ERROR_ROWS:
            totals = [counted(len(current.errors), "error"), counted(len(current.warnings), "warning")]
            lines = lines[: ERROR_ROWS - 1] + [(f"... {' and '.join(totals)} (Ctrl+E)", "dim")]
        for text, colour in lines:
            box.add(text, colour)
    sections.append(box)

    # --- output of the selected file -------------------------------------------
    box = Section("OUTPUT", min_rows=3)
    box.add(fit_left(display_name(session, current.target)))
    if current.status == OK:
        functions = current.function_count
        box.add(f"{current.vm_line_count} VM lines, {functions} function{'s' if functions != 1 else ''}")
        warned = f" ({counted(len(current.warnings), 'warning')})" if current.warnings else ""
        if current.written:
            box.add("saved" + warned, "warning" if warned else "ok")
        else:
            box.add("not saved (preview only)" + warned, "dim")
    elif current.status == FAILED:
        box.add("not saved: fix the errors, then Ctrl+R", "error")
    else:
        box.add("waiting...", "dim")
    sections.append(box)
    return sections


def largest_sections(session: CompileSession) -> List[Section]:
    """
    The sections as TALL as they can ever get. Every box reserves a fixed
    number of rows (min_rows), so this is simply the current layout - the
    window is sized from it, and nothing ever gets cut off the bottom.
    """
    return build_sections(session, 0)


class InfoPanel:
    """Draws `build_sections()` onto a pygame surface as bordered boxes."""

    WIDTH = 360  # pixels
    PADDING = 6  # space between a box's border and its text
    GAP = 8  # space between boxes
    RADIUS = 6  # rounded corners

    def __init__(self, font_size: int = 13) -> None:
        import pygame  # imported here so build_sections() works without pygame

        self.pygame = pygame
        self.font = pygame.font.SysFont(theme.MONO_FONTS, font_size)
        self.line_height = self.font.get_linesize()
        self.header_height = self.line_height + 6

    # --- sizes ----------------------------------------------------------------
    def box_height(self, n_rows: int) -> int:
        return self.header_height + self.PADDING + n_rows * self.line_height + self.PADDING

    def required_height(self, sections: Sequence[Section]) -> int:
        """Pixels needed to stack these sections one below the other."""
        total = sum(self.box_height(s.row_count) for s in sections)
        return total + self.GAP * max(0, len(sections) - 1)

    def shortcuts_section(self, width: int, extra: Sequence[str] = ()) -> Section:
        """
        Arrange HELP_ITEMS into rows that fit inside a box `width` pixels
        wide. `extra` items (e.g. "Ctrl+J run in JackVM") go before quitting.
        """
        usable = width - 2 * self.PADDING
        rows: List[str] = []
        current = ""
        quit_at = HELP_ITEMS.index("Ctrl+Q quit")
        for item in [*HELP_ITEMS[:quit_at], *extra, *HELP_ITEMS[quit_at:]]:
            candidate = item if not current else current + HELP_SEPARATOR + item
            if current and self.font.size(candidate)[0] > usable:
                rows.append(current)  # row is full: start a new one
                current = item
            else:
                current = candidate
        if current:
            rows.append(current)
        section = Section("SHORTCUTS")
        for row in rows:
            section.add(row, "dim")
        return section

    # --- drawing ----------------------------------------------------------------
    def draw_box(self, target, x: int, y: int, section: Section, width: int = WIDTH, clickable=None) -> int:
        """
        Draw one section as a box at (x, y). Returns the y below the box.
        If `clickable` is a list, (row rectangle, file index) pairs are added
        to it for rows that select a file when clicked.
        """
        pygame = self.pygame
        height = self.box_height(section.row_count)
        outline = pygame.Rect(x, y, width, height)

        # Body, then the title strip, then the border on top of both.
        pygame.draw.rect(target, theme.BOX, outline, border_radius=self.RADIUS)
        header = pygame.Rect(x, y, width, self.header_height)
        pygame.draw.rect(
            target, theme.BOX_HEADER, header,
            border_top_left_radius=self.RADIUS, border_top_right_radius=self.RADIUS,
        )  # fmt: skip
        pygame.draw.line(target, theme.BORDER, (x, header.bottom), (outline.right - 1, header.bottom))
        pygame.draw.rect(target, theme.BORDER, outline, width=1, border_radius=self.RADIUS)

        target.blit(self.font.render(section.title, True, theme.COLOURS["title"]), (x + self.PADDING, y + 3))
        text_y = header.bottom + self.PADDING
        for (text, colour), file_index in zip(section.rows, section.targets):
            if text:
                target.blit(self.font.render(text, True, theme.COLOURS[colour]), (x + self.PADDING, text_y))
            if clickable is not None and file_index is not None:
                clickable.append((pygame.Rect(x, text_y, width, self.line_height), file_index))
            text_y += self.line_height
        return y + height

    def draw(self, target, x: int, y: int, sections: Sequence[Section]) -> List[Tuple[object, int]]:
        """Draw the boxes stacked downward from (x, y); return the clickable rows."""
        clickable: List[Tuple[object, int]] = []
        for section in sections:
            y = self.draw_box(target, x, y, section, clickable=clickable) + self.GAP
        return clickable
