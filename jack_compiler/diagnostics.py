"""
Compiler diagnostics: errors, warnings and notes with a source location.

Diagnostics are reported the way GCC, Clang and rustc do it - the location,
the severity, a plain-English message, then the offending source line with
the problem underlined::

    Broken.jack:6:16: error: expected an expression, found ';'
        6 |         let x = ;
          |                 ^
    Broken.jack:9:15: error: expected ';' after 'return'
        9 |         return
          |               ^
          = help: every statement ends with ';'
    Main.jack:4:13: error: 'x' is already declared in this subroutine
        4 |     var int x;
          |             ^
    Main.jack:3:13: note: 'x' was first declared here
        3 |     var int x;
          |             ^

The first line of each diagnostic is always ``file:line:column: severity:
message`` so editors and terminals can jump to it. Lines and columns are
1-based; a line of 0 means "no particular place in the file".

This module also turns ANTLR's raw parser messages, such as::

    mismatched input ';' expecting {'true', 'false', 'null', 'this', '-',
    '~', '(', INTEGER, STRING_LITERAL, IDENTIFIER}

into what a person would say: ``expected an expression, found ';'``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence, Tuple

ERROR = "error"
WARNING = "warning"
NOTE = "note"


@dataclass(frozen=True)
class Note:
    """Extra information that points at another place, e.g. an earlier declaration."""

    line: int
    column: int
    message: str
    length: int = 1


@dataclass(frozen=True)
class Diagnostic:
    """One problem found in one source file."""

    file: str
    line: int  # 1-based; 0 = not tied to a line
    column: int  # 1-based
    message: str
    severity: str = ERROR
    length: int = 1  # how many characters to underline
    help: Optional[str] = None  # a suggestion: "did you mean 'count'?"
    notes: Tuple[Note, ...] = field(default_factory=tuple)

    @property
    def is_error(self) -> bool:
        return self.severity == ERROR

    def location(self) -> str:
        if self.line <= 0:
            return self.file
        return f"{self.file}:{self.line}:{self.column}"

    def __str__(self) -> str:
        """The one-line form: ``file:line:col: error: message``."""
        return f"{self.location()}: {self.severity}: {self.message}"

    def sort_key(self) -> Tuple[int, int]:
        return (self.line, self.column)


def _no_colour(kind: str, text: str) -> str:
    return text


def caret_padding(source_line: str, column: int) -> str:
    """
    Spaces that line a caret up under `column` (1-based). Tabs in the source
    are copied, so the caret still lines up whatever the tab width is.
    """
    prefix = source_line[: max(0, column - 1)]
    return "".join("\t" if char == "\t" else " " for char in prefix)


def render(
    diagnostic: Diagnostic,
    source_lines: Optional[Sequence[str]] = None,
    colour: Callable[[str, str], str] = _no_colour,
) -> str:
    """
    The full, multi-line report for one diagnostic (see the module docstring).

    `source_lines` are the lines of the file (without newlines); leave it out
    to get just the headline(s). `colour(kind, text)` may wrap pieces in
    terminal colours; kind is a severity, "location", "caret" or "help".
    """
    out: List[str] = []
    width = max([len(str(diagnostic.line))] + [len(str(n.line)) for n in diagnostic.notes])

    def headline(line: int, column: int, severity: str, message: str) -> None:
        where = diagnostic.file if line <= 0 else f"{diagnostic.file}:{line}:{column}"
        out.append(f"{colour('location', where + ':')} {colour(severity, severity + ':')} {message}")

    def snippet(line: int, column: int, length: int) -> None:
        if not source_lines or not 1 <= line <= len(source_lines):
            return
        text = source_lines[line - 1].rstrip("\r\n")
        gutter = " " * width
        length = max(1, min(length, len(text) - column + 1))  # never underline past the line
        marker = "^" + "~" * (length - 1)
        out.append(f" {line:>{width}} | {text}")
        out.append(f" {gutter} | {caret_padding(text, column)}{colour('caret', marker)}")

    headline(diagnostic.line, diagnostic.column, diagnostic.severity, diagnostic.message)
    snippet(diagnostic.line, diagnostic.column, diagnostic.length)
    if diagnostic.help:
        out.append(f" {' ' * width} = {colour('help', 'help:')} {diagnostic.help}")
    for note in diagnostic.notes:
        headline(note.line, note.column, NOTE, note.message)
        snippet(note.line, note.column, note.length)
    return "\n".join(out)


def summary(diagnostics: Sequence[Diagnostic]) -> str:
    """'2 errors and 1 warning generated.' (empty string if there are none)."""
    errors = sum(1 for d in diagnostics if d.severity == ERROR)
    warnings = sum(1 for d in diagnostics if d.severity == WARNING)
    parts = []
    if errors:
        parts.append(f"{errors} error{'s' if errors != 1 else ''}")
    if warnings:
        parts.append(f"{warnings} warning{'s' if warnings != 1 else ''}")
    return f"{' and '.join(parts)} generated." if parts else ""


# ---------------------------------------------------------------------------
# Turning ANTLR's messages into friendly ones
# ---------------------------------------------------------------------------
# Groups of tokens that ANTLR lists one by one, and how a person names them.
_EXPRESSION_START = {"'true'", "'false'", "'null'", "'this'", "'-'", "'~'", "'('", "INTEGER", "STRING_LITERAL", "IDENTIFIER"}
_STATEMENT_START = {"'let'", "'if'", "'while'", "'do'", "'return'"}
_TYPE = {"'int'", "'boolean'", "'char'", "'String'", "IDENTIFIER"}
_OPERATOR = {"'+'", "'-'", "'*'", "'/'", "'&'", "'|'", "'<'", "'>'", "'='"}
_SUBROUTINE_KIND = {"'constructor'", "'function'", "'method'"}
_CLASS_VAR_KIND = {"'static'", "'field'"}
_SINGLE_NAMES = {
    "IDENTIFIER": "a name",
    "INTEGER": "a number",
    "STRING_LITERAL": "a string",
    "'<EOF>'": "the end of the file",
    "<EOF>": "the end of the file",
}

_MISMATCHED = re.compile(r"^mismatched input (.+?) expecting (.+)$", re.DOTALL)
_MISSING = re.compile(r"^missing (.+?) at (.+)$", re.DOTALL)
_EXTRANEOUS = re.compile(r"^extraneous input (.+?) expecting (.+)$", re.DOTALL)
_NO_VIABLE = re.compile(r"^no viable alternative at input (.+)$", re.DOTALL)
_TOKEN_ERROR = re.compile(r"^token recognition error at: (.+)$", re.DOTALL)


def _split_expected(text: str) -> List[str]:
    """"{'a', 'b', X}" or "'a'" -> ["'a'", "'b'", "X"]."""
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        text = text[1:-1]
    return [item.strip() for item in re.findall(r"'(?:[^'\\]|\\.)*'|[^,\s]+", text) if item.strip()]


def describe_expected(items: Sequence[str]) -> str:
    """Name a set of expected tokens: "';' or an operator", "an expression", ..."""
    remaining = list(dict.fromkeys(items))  # keep order, drop repeats
    phrases: List[str] = []

    def take(group: set, phrase: str) -> None:
        if group <= set(remaining):
            phrases.append(phrase)
            for item in group:
                remaining.remove(item)

    take(_EXPRESSION_START, "an expression")
    take(_STATEMENT_START, "a statement")
    take(_OPERATOR, "an operator")
    take(_SUBROUTINE_KIND, "a subroutine declaration")
    take(_CLASS_VAR_KIND, "a 'static' or 'field' declaration")
    take(_TYPE, "a type")
    simple = [_SINGLE_NAMES.get(item, item) for item in remaining]
    # Punctuation such as ';' reads best first: "';' or an expression".
    words = simple + phrases
    if not words:
        return "something else"
    if len(words) > 5:
        return "one of " + ", ".join(words)
    return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " or " + words[-1]


def _found(token_text: str) -> str:
    return "the end of the file" if token_text in ("'<EOF>'", "<EOF>") else token_text


@dataclass
class FriendlySyntaxError:
    """A rewritten parser message, and whether to point after the previous token."""

    message: str
    after_previous: bool = False  # True: the problem is really at the end of the previous token
    help: Optional[str] = None


def _help_for(expected: Sequence[str]) -> Optional[str]:
    if "';'" in expected:
        return "every statement and declaration ends with ';'"
    if "'}'" in expected:
        return "check that every '{' has a matching '}'"
    return None


def _unexpected_end(expected: Sequence[str]) -> FriendlySyntaxError:
    """The file stopped too soon - usually a missing '}'. Point at the last real token."""
    return FriendlySyntaxError(
        f"unexpected end of file: expected {describe_expected(expected)}", after_previous=True, help=_help_for(expected)
    )


def friendly_syntax_error(message: str, previous_token: Optional[str] = None, same_line: bool = True) -> FriendlySyntaxError:
    """
    Rewrite one ANTLR error message.

    `previous_token` is the text of the token before the problem, and
    `same_line` says whether the offending token is on the same line as it.
    A missing ';' or ')' is reported "after the previous token" - where the
    programmer forgot it - like real compilers do.
    """
    after = f" after {previous_token}" if previous_token else ""

    match = _MISSING.match(message)
    if match:
        missing = match.group(1)
        return FriendlySyntaxError(
            f"expected {describe_expected([missing])}{after}", after_previous=True, help=_help_for([missing])
        )

    match = _MISMATCHED.match(message)
    if match:
        found, expected = _found(match.group(1)), _split_expected(match.group(2))
        closing = [t for t in ("';'", "')'", "']'") if t in expected]
        if closing and (not same_line or found == "the end of the file"):
            # e.g. "return" at the end of a line with no ';': say so at the end of that line.
            return FriendlySyntaxError(
                f"expected {describe_expected(closing)}{after}", after_previous=True, help=_help_for(closing)
            )
        if found == "the end of the file":
            return _unexpected_end(expected)
        return FriendlySyntaxError(f"expected {describe_expected(expected)}, found {found}", help=_help_for(expected))

    match = _EXTRANEOUS.match(message)
    if match:
        found, expected = _found(match.group(1)), _split_expected(match.group(2))
        if found == "the end of the file":
            return _unexpected_end(expected)
        closing = [t for t in ("';'", "')'", "']'") if t in expected]
        if closing and not same_line:  # "do f()\n return;" - the ';' was forgotten on the line above
            return FriendlySyntaxError(
                f"expected {describe_expected(closing)}{after}", after_previous=True, help=_help_for(closing)
            )
        return FriendlySyntaxError(f"unexpected {found} (expected {describe_expected(expected)})")

    match = _NO_VIABLE.match(message)
    if match:
        return FriendlySyntaxError("this doesn't form a valid statement or expression")

    match = _TOKEN_ERROR.match(message)
    if match:
        text = match.group(1)
        inner = text[1:-1] if len(text) >= 2 and text[0] == text[-1] == "'" else text
        if inner.startswith('"'):
            return FriendlySyntaxError(
                "unterminated string", help="a string must end with '\"' on the same line"
            )
        return FriendlySyntaxError(f"invalid character '{inner}' in program")

    return FriendlySyntaxError(message)
