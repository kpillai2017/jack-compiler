"""
annotate.py - Compiler-style messages under the code (no pygame here).
=====================================================================

Turns a file's lines and its diagnostics into the rows the Jack pane
draws. Each problem gets a ^~~~ marker under the exact spot, and its
message, just like the compiler prints it in a terminal:

      5 |         let x = 1
        |                  ^ error: expected ';' after '1'
        |   = help: every statement and declaration ends with ';'
      6 |         do Output.printInt(x);

Code rows keep their line number; message rows have none (so the gutter
stays blank). Code rows with a problem are "shaded" so the window can give
them a red (error) or amber (warning) background.

`build_rows(..., inline=False)` gives just the code rows (shaded), for
when the messages are switched off with Ctrl+I.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from ..diagnostics import ERROR, NOTE, WARNING, Diagnostic
from .syntax import Span

TAB_SIZE = 4  # the code view expands tabs to this many spaces

# The colour (theme.COLOURS key) of each kind of message.
SEVERITY_COLOURS = {ERROR: "error", WARNING: "warning", NOTE: "note"}


@dataclass
class Row:
    """One row of the Jack pane."""

    number: Optional[int]  # the 1-based source line, or None for a message row
    spans: List[Span]
    shade: Optional[str] = None  # "error" / "warning": the row's background


@dataclass(frozen=True)
class _Marker:
    column: int  # 1-based, in the RAW line (tabs count as 1, like the compiler)
    length: int
    severity: str
    message: str
    help: Optional[str] = None


def display_column(raw_line: str, column: int) -> int:
    """Where 1-based `column` of the raw line lands once tabs are expanded (0-based)."""
    return len(raw_line[: max(0, column - 1)].expandtabs(TAB_SIZE))


def _markers_by_line(diagnostics: Sequence[Diagnostic]) -> Dict[int, List[_Marker]]:
    markers: Dict[int, List[_Marker]] = {}
    for d in diagnostics:
        if d.line > 0:
            markers.setdefault(d.line, []).append(_Marker(d.column, d.length, d.severity, d.message, d.help))
        for note in d.notes:  # e.g. "'x' was first declared here", shown at THAT line
            markers.setdefault(note.line, []).append(_Marker(note.column, note.length, NOTE, note.message))
    for items in markers.values():
        items.sort(key=lambda m: (m.column, m.severity))
    return markers


def message_rows(raw_line: str, marker: _Marker, columns: int) -> List[List[Span]]:
    """The rows for one marker: '^~~~ error: message', then '= help: ...'."""
    kind = SEVERITY_COLOURS.get(marker.severity, "error")
    expanded = raw_line.expandtabs(TAB_SIZE)
    start = min(display_column(raw_line, marker.column), max(0, columns - 1))
    room = max(1, min(marker.length, len(expanded) - start, columns - start))
    caret = "^" + "~" * (room - 1)
    label = f"{marker.severity}: {marker.message}"

    rows: List[List[Span]] = []
    indent = min(start, max(0, columns // 3))  # where wrapped text and help lines start
    if start + len(caret) + 1 + len(label) <= columns:  # it all fits on one row
        rows.append([(" " * start, "normal"), (caret, kind), (" " + label, kind)])
    else:  # caret on its own row, then the message wrapped below it
        rows.append([(" " * start, "normal"), (caret, kind)])
        for piece in textwrap.wrap(label, max(10, columns - indent)) or [label]:
            rows.append([(" " * indent, "normal"), (piece, kind)])
    if marker.help:
        width = max(10, columns - indent - 2)
        for index, piece in enumerate(textwrap.wrap(f"= help: {marker.help}", width)):
            rows.append([(" " * (indent + (0 if index == 0 else 2)), "normal"), (piece, "title")])
    return rows


def build_rows(
    raw_lines: Sequence[str],
    code_spans: Sequence[List[Span]],
    diagnostics: Sequence[Diagnostic],
    columns: int,
    inline: bool = True,
) -> List[Row]:
    """All the rows for the Jack pane: each code line, followed by its messages."""
    markers = _markers_by_line(diagnostics)
    rows: List[Row] = []
    for number, spans in enumerate(code_spans, start=1):
        items = markers.get(number, [])
        severities = {m.severity for m in items}
        shade = "error" if ERROR in severities else ("warning" if WARNING in severities else None)
        rows.append(Row(number, list(spans), shade))
        if inline:
            raw = raw_lines[number - 1] if number <= len(raw_lines) else ""
            for marker in items:
                rows.extend(Row(None, spans_) for spans_ in message_rows(raw, marker, columns))

    # Problems past the last line (rare: e.g. an empty file) go at the end.
    if inline:
        for number in sorted(n for n in markers if n > len(code_spans)):
            for marker in markers[number]:
                rows.extend(Row(None, spans_) for spans_ in message_rows("", marker, columns))
    return rows


def row_of_line(rows: Sequence[Row], line: int) -> int:
    """Index of the row showing source line `line` (0 if there isn't one)."""
    for index, row in enumerate(rows):
        if row.number == line:
            return index
    return 0


def visible_line_range(rows: Sequence[Row], first: int, count: int) -> Tuple[int, int]:
    """The first and last source line numbers among rows[first:first+count]."""
    numbers = [row.number for row in rows[first : first + count] if row.number is not None]
    return (numbers[0], numbers[-1]) if numbers else (0, 0)
