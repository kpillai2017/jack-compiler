"""
syntax.py - Colour Jack and VM code, one line at a time (no pygame here).
========================================================================

Each line becomes a list of "spans": (text, kind) pairs, where kind is a
name from theme.COLOURS ("keyword", "string", "comment", ...). Joining the
texts of a line's spans gives back exactly the original line.

    jack_spans(['let x = 1; // one'])
    -> [[('let', 'keyword'), (' x ', 'normal'), ('=', 'symbol'), (' ', 'normal'),
         ('1', 'number'), (';', 'symbol'), (' ', 'normal'), ('// one', 'comment')]]

Jack's /* block comments */ can span many lines, so the colouring of one
line depends on the lines before it. That's why these functions take the
whole file at once.
"""

from __future__ import annotations

import re
from typing import List, Tuple

Span = Tuple[str, str]

JACK_KEYWORDS = frozenset(
    "class constructor function method field static var int char boolean void "
    "true false null this let do if else while return".split()
)
JACK_SYMBOLS = frozenset("{}()[].,;+-*/&|<>=~")

_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_NUMBER = re.compile(r"[0-9]+")


def _add(spans: List[Span], text: str, kind: str) -> None:
    """Append, merging with the previous span when it has the same kind."""
    if not text:
        return
    if spans and spans[-1][1] == kind:
        spans[-1] = (spans[-1][0] + text, kind)
    else:
        spans.append((text, kind))


def jack_spans(lines: List[str]) -> List[List[Span]]:
    """Syntax-colour Jack source lines."""
    result: List[List[Span]] = []
    in_block_comment = False
    for line in lines:
        spans: List[Span] = []
        i = 0
        while i < len(line):
            if in_block_comment:
                end = line.find("*/", i)
                if end < 0:
                    _add(spans, line[i:], "comment")
                    break
                _add(spans, line[i : end + 2], "comment")
                i = end + 2
                in_block_comment = False
                continue
            if line.startswith("//", i):
                _add(spans, line[i:], "comment")
                break
            if line.startswith("/*", i):
                in_block_comment = True
                _add(spans, "/*", "comment")
                i += 2
                continue
            char = line[i]
            if char == '"':
                end = line.find('"', i + 1)
                end = len(line) if end < 0 else end + 1
                _add(spans, line[i:end], "string")
                i = end
                continue
            word = _WORD.match(line, i)
            if word:
                text = word.group()
                _add(spans, text, "keyword" if text in JACK_KEYWORDS else "normal")
                i = word.end()
                continue
            number = _NUMBER.match(line, i)
            if number:
                _add(spans, number.group(), "number")
                i = number.end()
                continue
            _add(spans, char, "symbol" if char in JACK_SYMBOLS else "normal")
            i += 1
        result.append(spans)
    return result


# VM commands, grouped by how they're coloured.
_VM_FLOW = {"label", "goto", "if-goto"}
_VM_FUNCTIONS = {"function", "call", "return"}
_PIECES = re.compile(r"\s+|\S+")  # runs of spaces, and the words between them


def vm_spans(lines: List[str]) -> List[List[Span]]:
    """Syntax-colour VM code lines: function/call/return and labels stand out."""
    result: List[List[Span]] = []
    for line in lines:
        spans: List[Span] = []
        code, comment = line, ""
        if "//" in line:
            cut = line.index("//")
            code, comment = line[:cut], line[cut:]
        command_kind = None  # set once we've seen the first word
        for piece in _PIECES.findall(code):
            if piece.isspace():
                _add(spans, piece, "normal")
            elif command_kind is None:
                command_kind = "keyword" if piece in _VM_FUNCTIONS else ("label" if piece in _VM_FLOW else "normal")
                _add(spans, piece, command_kind)
            else:
                _add(spans, piece, "number" if piece.isdigit() else ("label" if command_kind == "label" else "dim"))
        _add(spans, comment, "comment")
        result.append(spans)
    return result
