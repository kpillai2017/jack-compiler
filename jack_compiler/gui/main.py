"""
main.py - Start the compiler GUI from the command line.
======================================================

    jackc-gui                        # choose a .jack file or folder in a window
    jackc-gui examples/              # compile a folder straight away
    jackc-gui examples/Math.jack     # ...or a single file
    jackc-gui --gui projects/        # open the picker in projects/
    jackc-gui -r projects/           # compile a whole tree (like jackc -r)
    jackc-gui src/ -o bin/           # write the .vm files to bin/
    jackc-gui -o bin/                # choose in a window; the .vm files go to bin/
    jackc-gui --no-write src/        # preview only: never write .vm files
    python -m jack_compiler.gui ...  # the same, without installing

The .vm files go where `jackc` would put them, unless --no-write is given.
In the window, Ctrl+S saves them (even with --no-write) and Ctrl+Shift+S
chooses another folder to save them in.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence


def build_argument_parser() -> argparse.ArgumentParser:
    from .. import __version__

    parser = argparse.ArgumentParser(
        prog="jackc-gui",
        description="A window for compiling Jack (.jack) programs to Hack VM code and browsing the result.",
    )
    parser.add_argument(
        "input", nargs="?",
        help="a .jack file or a folder of .jack files. Leave it out to choose in a window.",
    )  # fmt: skip
    parser.add_argument(
        "--gui", action="store_true",
        help="choose what to compile in a window (starts in the given folder, or the current one)",
    )  # fmt: skip
    parser.add_argument(
        "-o", "--output",
        help="output .vm file or folder (default: next to the sources; Ctrl+Shift+S in the window chooses another)",
    )  # fmt: skip
    parser.add_argument("-r", "--recursive", action="store_true", help="compile .jack files in sub-folders too")
    parser.add_argument("--no-write", action="store_true", help="compile and show the VM code, but don't write .vm files")
    parser.add_argument(
        "--werror", action="store_true",
        help="treat warnings as errors, like jackc --werror (Ctrl+W switches it in the window)",
    )
    parser.add_argument("--rows", type=int, default=34, metavar="N", help="lines of code shown in each pane (default: 34)")
    parser.add_argument("--font-size", type=int, default=13, metavar="PT", help="text size (default: 13)")
    parser.add_argument("--no-panel", action="store_true", help="hide the info panel (Ctrl+D shows it)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def pygame_missing_message(executable: str = sys.executable) -> str:
    """
    What to say when pygame isn't installed. jack-compiler isn't on PyPI,
    so the fix is the [gui] extra of the checkout this code runs from (when
    it does), installed into THIS Python - often a fresh, empty venv.
    """
    root = Path(__file__).resolve().parent.parent.parent
    if (root / "pyproject.toml").is_file():
        fix = f'pip install -e "{root}[gui]"   (or just: pip install pygame)'
    else:
        fix = "pip install pygame"
    return f"jackc-gui needs pygame, which this Python ({executable}) doesn't have.\nInstall it with:  {fix}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    write = not args.no_write

    try:
        import pygame  # noqa: F401
    except ImportError:
        print(pygame_missing_message(), file=sys.stderr)
        return 1

    from .session import CompileSession
    from .window import CompilerWindow, open_picker_window

    use_picker = args.gui or args.input is None
    output = Path(args.output) if args.output else None
    if use_picker:
        start = Path(args.input).expanduser() if args.input else Path.cwd()
        session = open_picker_window(
            start if start.is_dir() else Path.cwd(), args.recursive, write, args.werror, output=output,
        )  # fmt: skip
        if session is None:
            return 0  # the user cancelled or closed the window
    else:
        input_path = Path(args.input)
        if input_path.is_file() and args.recursive:
            parser.error("--recursive requires a directory as input")
        try:
            session = CompileSession(input_path, output, args.recursive, write, werror=args.werror)
        except FileNotFoundError as problem:
            print(problem, file=sys.stderr)
            return 1

    CompilerWindow(
        session,
        font_size=args.font_size,
        code_rows=args.rows,
        show_panel=not args.no_panel,
        output=output,
    ).run()
    if session.finished:
        print(f"Compiled {session.ok_count} of {session.total} file(s); {session.failed_count} failed.")
        return 1 if session.failed_count else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
