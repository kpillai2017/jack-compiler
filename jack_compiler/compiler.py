"""
Main Jack compiler driver.
Converts Jack source files to Hack VM code.

Usage:
    jackc input.jack -o output.vm
    jackc input_dir -o output_dir
    jackc -r project_dir [--clean] [--dry-run]
    python -m jack_compiler input.jack
"""

import argparse
import os
import sys
import traceback
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Union

from antlr4 import CommonTokenStream, FileStream, Token
from antlr4.error.ErrorListener import ErrorListener

from .antlr_generated.grammar.JackLexer import JackLexer
from .antlr_generated.grammar.JackParser import JackParser
from .checker import check as check_semantics
from .compiler_visitor import JackCompilerVisitor
from .diagnostics import ERROR, WARNING, Diagnostic, Note, friendly_syntax_error, render, summary


class JackSyntaxError(SyntaxError):
    """
    Raised when a Jack source file has lexical or syntax errors.

    ``.diagnostics`` holds every :class:`Diagnostic` (errors, plus any
    warnings found alongside them); ``.errors`` holds the errors' one-line
    ``file:line:col: error: message`` forms.
    """

    kind = "syntax"

    def __init__(self, source: str, diagnostics: Sequence[Union[Diagnostic, str]]):
        self.diagnostics: List[Diagnostic] = [
            d if isinstance(d, Diagnostic) else Diagnostic(source, 0, 0, str(d)) for d in diagnostics
        ]
        self.errors: List[str] = [str(d) for d in self.diagnostics if d.is_error]
        super().__init__(f"{len(self.errors)} {self.kind} error(s) in {source}")
        self.source = source


class JackSemanticError(JackSyntaxError):
    """
    Raised when a file parses but makes no sense: an undeclared variable,
    a method called from a function, a missing return, ... (see checker.py).
    A subclass of JackSyntaxError, so ``except JackSyntaxError`` catches both.
    """

    kind = "semantic"


class CollectingErrorListener(ErrorListener):
    """
    Collects ANTLR lexer/parser errors as :class:`Diagnostic` objects instead
    of printing them to stderr. ANTLR's messages are rewritten into plain
    English, and a missing ';' (or ')' ...) is reported just after the token
    it should follow - where it was forgotten - like GCC and Clang do.
    Columns are 1-based.
    """

    def __init__(self, source: str):
        super().__init__()
        self.source = source
        self.lexer_diagnostics: List[Diagnostic] = []
        self.parser_diagnostics: List[Diagnostic] = []
        self.lexer_lines = set()

    @property
    def errors(self) -> List[str]:
        return [str(d) for d in self.diagnostics]

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        previous = self._previous_token(recognizer, offendingSymbol)
        same_line = previous is None or offendingSymbol is None or previous.line == offendingSymbol.line
        friendly = friendly_syntax_error(msg, f"'{previous.text}'" if previous is not None else None, same_line)

        length = 1
        if offendingSymbol is not None and offendingSymbol.text and offendingSymbol.text != "<EOF>":
            length = len(offendingSymbol.text)
        elif offendingSymbol is None:  # a lexer error: underline the bad text
            length = max(1, len(msg.rsplit(": ", 1)[-1].strip("'")))
        if friendly.after_previous and previous is not None:
            line, column, length = previous.line, previous.column + len(previous.text), 1
        notes = ()
        if offendingSymbol is not None and offendingSymbol.type == Token.EOF:
            brace = self._unclosed_brace(recognizer)
            if brace is not None:
                notes = (Note(brace.line, brace.column + 1, "this '{' is never closed"),)
        diagnostic = Diagnostic(self.source, line, column + 1, friendly.message, ERROR, length, friendly.help, notes)
        if offendingSymbol is None:
            self.lexer_lines.add(line)
            self.lexer_diagnostics.append(diagnostic)
        else:
            self.parser_diagnostics.append(diagnostic)

    @property
    def diagnostics(self) -> List[Diagnostic]:
        """
        Every problem, in source order. A bad character or an unterminated
        string also confuses the parser; those knock-on parser errors on the
        same line are dropped so only the real cause is reported.
        """
        kept = [d for d in self.parser_diagnostics if d.line not in self.lexer_lines]
        return sorted(self.lexer_diagnostics + kept, key=Diagnostic.sort_key)

    @staticmethod
    def _unclosed_brace(recognizer):
        """The innermost '{' that has no matching '}' (for 'unexpected end of file')."""
        if not hasattr(recognizer, "getTokenStream"):
            return None
        stream = recognizer.getTokenStream()
        stream.fill()
        open_braces = []
        for token in stream.tokens:
            if token.type == JackLexer.LBRACE:
                open_braces.append(token)
            elif token.type == JackLexer.RBRACE and open_braces:
                open_braces.pop()
        return open_braces[-1] if open_braces else None

    @staticmethod
    def _previous_token(recognizer, offending):
        """The real token just before the offending one (comments/spaces are skipped)."""
        if offending is None or not hasattr(recognizer, "getTokenStream"):
            return None
        index = getattr(offending, "tokenIndex", -1)
        if index <= 0:
            return None
        try:
            return recognizer.getTokenStream().get(index - 1)
        except Exception:  # pragma: no cover - defensive
            return None


def read_source_lines(path: str) -> List[str]:
    """A file's lines, for showing source snippets in error messages."""
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def _terminal_colour(kind: str, text: str) -> str:
    """Colours for diagnostics, as GCC/Clang use them."""
    if kind == ERROR:
        return Colors.bold(Colors.red(text))
    if kind == WARNING:
        return Colors.bold(Colors.yellow(text))
    if kind == "note":
        return Colors.bold(Colors.cyan(text))
    if kind == "caret":
        return Colors.green(text)
    if kind in ("location", "help"):
        return Colors.bold(text)
    return text


def _colors_enabled() -> bool:
    """Use ANSI colours only on a TTY and when NO_COLOR is not set."""
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

    enabled = _colors_enabled()

    @classmethod
    def _wrap(cls, code: str, text) -> str:
        return f"{code}{text}{cls.RESET}" if cls.enabled else str(text)

    @classmethod
    def green(cls, text):
        return cls._wrap(cls.GREEN, text)

    @classmethod
    def red(cls, text):
        return cls._wrap(cls.RED, text)

    @classmethod
    def yellow(cls, text):
        return cls._wrap(cls.YELLOW, text)

    @classmethod
    def blue(cls, text):
        return cls._wrap(cls.BLUE, text)

    @classmethod
    def cyan(cls, text):
        return cls._wrap(cls.CYAN, text)

    @classmethod
    def bold(cls, text):
        return cls._wrap(cls.BOLD, text)


class JackCompiler:
    """Main compiler class."""

    def __init__(self, verbose: bool = False, warnings: bool = True, werror: bool = False):
        """
        Initialize the compiler.

        Args:
            verbose: Print a full traceback on unexpected internal errors.
            warnings: Print warnings (they never stop compilation by themselves).
            werror: Treat warnings as errors (like ``gcc -Werror``).
        """
        self.visitor = JackCompilerVisitor()
        self.verbose = verbose
        self.show_warnings = warnings
        self.werror = werror
        # Diagnostics (warnings) from the most recent successful compile_source().
        self.diagnostics: List[Diagnostic] = []

    def compile_source(self, input_path: str) -> str:
        """
        Compile a single Jack file and return the generated VM code.

        Raises:
            FileNotFoundError: If the input file does not exist.
            JackSyntaxError: If the source contains lexical or syntax errors;
                ``.errors`` holds ``file:line:col: error: message`` strings
                and ``.diagnostics`` the full :class:`Diagnostic` objects.
            JackSemanticError: (a JackSyntaxError) if it parses but has
                semantic errors, e.g. an undeclared variable.

        Warnings from a successful compile are left in ``self.diagnostics``.
        """
        self.diagnostics = []
        input_stream = FileStream(input_path, encoding='utf-8')
        listener = CollectingErrorListener(input_path)

        lexer = JackLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(listener)

        parser = JackParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(listener)

        tree = parser.program()

        if listener.diagnostics:
            raise JackSyntaxError(input_path, listener.diagnostics)

        diagnostics = check_semantics(tree, input_path)
        if self.werror:
            diagnostics = [
                Diagnostic(d.file, d.line, d.column, d.message + " [-Werror]", ERROR, d.length, d.help, d.notes)
                if d.severity == WARNING else d
                for d in diagnostics
            ]
        if any(d.is_error for d in diagnostics):
            raise JackSemanticError(input_path, diagnostics)
        self.diagnostics = diagnostics

        # Visitor generates both the AST and the VM code.
        self.visitor.compile_program(tree)
        return self.visitor.codegen.get_code()

    def compile_file(self, input_path: str, output_path: str) -> bool:
        """
        Compile a single Jack file to VM code.

        Args:
            input_path: Path to input .jack file
            output_path: Path to output .vm file

        Returns:
            True if compilation succeeded, False otherwise
        """
        try:
            vm_code = self.compile_source(input_path)

            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(vm_code, encoding='utf-8')

            warnings = self.diagnostics if self.show_warnings else []
            note = f" ({summary(warnings)[:-len(' generated.')]})" if warnings else ""
            print(f"{Colors.green('✓ SUCCESS')}{note}: {input_path}")
            print(f"  {Colors.cyan('→')} {output_path}")
            self.print_diagnostics(warnings, input_path)
            return True

        except FileNotFoundError:
            print(f"{Colors.red('✗ FILE NOT FOUND')}: {input_path}")
            return False
        except JackSyntaxError as e:
            print(f"{Colors.red('✗ COMPILATION FAILED')}: {input_path}")
            shown = [d for d in e.diagnostics if d.is_error or self.show_warnings]
            self.print_diagnostics(shown, input_path)
            return False
        except Exception as e:  # pragma: no cover - defensive
            print(f"{Colors.red('✗ COMPILATION ERROR')}: {input_path}")
            print(f"  {Colors.red(str(e))}")
            if self.verbose:
                traceback.print_exc()
            return False

    def print_diagnostics(self, diagnostics: Sequence[Diagnostic], path: str) -> None:
        """Print diagnostics GCC-style: location, message, source line, ^~~~."""
        if not diagnostics:
            return
        lines = read_source_lines(path)
        for diagnostic in diagnostics:
            print(render(diagnostic, lines, colour=_terminal_colour))
        totals = summary(diagnostics)
        print(Colors.red(totals) if any(d.is_error for d in diagnostics) else Colors.yellow(totals))

    def compile_directory(self, input_dir: str, output_dir: str,
                          recursive: bool = False, clean: bool = False,
                          dry_run: bool = False) -> bool:
        """
        Compile all Jack files in a directory.

        Args:
            input_dir: Directory containing .jack files
            output_dir: Directory for output .vm files. With ``recursive``,
                the source sub-directory structure is mirrored beneath it.
            recursive: Also compile .jack files in sub-directories.
            clean: Delete existing .vm files in every output directory that
                will be written to before compiling.
            dry_run: Only report what would be cleaned/compiled.

        Returns:
            True if all compilations succeeded (or, for a dry run, if any
            .jack files were found), False otherwise
        """
        input_path = Path(input_dir)

        if not input_path.is_dir():
            print(f"\n{Colors.red('✗ ERROR')}: Input directory not found: {input_dir}")
            return False

        jobs = plan_jobs(input_path, Path(output_dir), recursive)
        if not jobs:
            where = f"{input_dir} (recursive)" if recursive else input_dir
            print(f"{Colors.yellow('⚠ WARNING')}: No .jack files found in {where}")
            return False

        title = 'JACK COMPILER - BATCH COMPILATION'
        if recursive:
            title += ' (RECURSIVE)'
        return self._run_batch(jobs, title, clean=clean, dry_run=dry_run)

    def _run_batch(self, jobs: List[Tuple[Path, Path]], title: str,
                   clean: bool, dry_run: bool, targets_only: bool = False) -> bool:
        """
        Clean (optionally), then compile each (source, target) job.

        ``targets_only`` limits ``clean`` to the jobs' own target files rather
        than every .vm file in their output directories (used for single files).
        """
        if dry_run:
            title += ' - DRY RUN'

        print(f"\n{Colors.blue('═' * 60)}")
        print(f"{Colors.bold(Colors.blue(title))}")
        print(f"{Colors.blue('═' * 60)}")

        if clean:
            removed = clean_outputs(jobs, dry_run=dry_run, targets_only=targets_only)
            verb = 'Would remove' if dry_run else 'Removed'
            print(f"{Colors.yellow(f'{verb} {len(removed)} existing .vm file(s)')}")
            for vm in removed:
                print(f"  {Colors.yellow('-')} {vm}")

        if dry_run:
            print(f"{Colors.cyan(f'Would compile {len(jobs)} Jack file(s)')}")
            print(f"{Colors.blue('─' * 60)}")
            for src, dst in jobs:
                print(f"  {src} {Colors.cyan('→')} {dst}")
            print(f"{Colors.blue('═' * 60)}\n")
            return True

        print(f"{Colors.cyan(f'Found {len(jobs)} Jack file(s) to compile')}")
        print(f"{Colors.blue('─' * 60)}\n")

        failed: List[Path] = []
        for i, (src, dst) in enumerate(jobs, 1):
            print(f"{Colors.cyan(f'[{i}/{len(jobs)}]')} ", end="")
            if not self.compile_file(str(src), str(dst)):
                failed.append(src)
            print()

        print(f"{Colors.blue('─' * 60)}")
        succeeded = len(jobs) - len(failed)
        print(f"Compiled: {Colors.green(succeeded)}  Failed: "
              f"{Colors.red(len(failed)) if failed else len(failed)}  Total: {len(jobs)}")
        if failed:
            print(f"{Colors.red('✗ SOME COMPILATIONS FAILED')}")
            for src in failed:
                print(f"  {Colors.red('✗')} {src}")
        else:
            print(f"{Colors.green('✓ ALL COMPILATIONS SUCCESSFUL')}")
        print(f"{Colors.blue('═' * 60)}\n")

        return not failed


def find_jack_files(input_dir: Path, recursive: bool = False) -> List[Path]:
    """
    Return the .jack files in ``input_dir``, sorted for deterministic output.

    With ``recursive``, sub-directories are searched too; hidden directories
    (e.g. ``.git``, ``.venv``) are skipped.
    """
    if not recursive:
        return sorted(p for p in input_dir.glob("*.jack") if p.is_file())

    found = []
    for root, dirs, files in os.walk(input_dir):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
        found.extend(Path(root) / f for f in files if f.endswith('.jack'))
    return sorted(found)


def plan_jobs(input_dir: Path, output_dir: Path,
              recursive: bool = False) -> List[Tuple[Path, Path]]:
    """
    Map each source .jack file to its target .vm path.

    Targets mirror the source layout relative to ``input_dir`` beneath
    ``output_dir`` (which may be the same directory for in-place builds).
    """
    return [
        (src, output_dir / src.relative_to(input_dir).with_suffix('.vm'))
        for src in find_jack_files(input_dir, recursive)
    ]


def clean_outputs(jobs: List[Tuple[Path, Path]], dry_run: bool = False,
                  targets_only: bool = False) -> List[Path]:
    """
    Delete every existing .vm file in the output directories used by ``jobs``.

    Only directories that will receive compiled output are touched, and the
    search is not recursive, so unrelated directories are never affected.
    With ``targets_only``, only the jobs' own target .vm files are removed.

    Returns:
        The .vm files that were (or, for a dry run, would be) removed.
    """
    if targets_only:
        candidates = sorted({dst for _, dst in jobs})
    else:
        candidates = [
            vm
            for d in sorted({dst.parent for _, dst in jobs}) if d.is_dir()
            for vm in sorted(d.glob("*.vm"))
        ]

    removed = [vm for vm in candidates if vm.is_file()]
    if not dry_run:
        for vm in removed:
            vm.unlink()
    return removed


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    from . import __version__

    parser = argparse.ArgumentParser(
        prog='jackc',
        description='Jack compiler for nand2tetris Hack computer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compile a single file
  jackc Main.jack -o Main.vm

  # Compile all Jack files in a directory
  jackc src/ -o bin/

  # In-place compilation (output to same directory)
  jackc src/

  # Recursively compile a directory tree (output next to each .jack file)
  jackc -r projects/

  # Preview a clean, recursive rebuild without changing anything
  jackc -r --clean --dry-run projects/
        """
    )
    parser.add_argument('input', help='Input Jack file or directory')
    parser.add_argument(
        '-o', '--output',
        help='Output VM file or directory (default: same as input)',
        default=None,
    )
    parser.add_argument(
        '-r', '--recursive', action='store_true',
        help='Compile .jack files in sub-directories too, mirroring the '
             'directory structure under the output directory',
    )
    parser.add_argument(
        '--clean', action='store_true',
        help='Delete ALL existing .vm files in each output directory before '
             'compiling (for a single file: only its target). Combine with '
             '--dry-run to preview',
    )
    parser.add_argument(
        '-n', '--dry-run', action='store_true',
        help='Show what would be cleaned and compiled without writing anything',
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Show full tracebacks for internal compiler errors',
    )
    parser.add_argument(
        '-w', '--no-warnings', action='store_true',
        help='Do not print warnings (errors are always shown)',
    )
    parser.add_argument(
        '--werror', action='store_true',
        help='Treat warnings as errors: a file with warnings is not compiled',
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    return parser


def main(argv=None):
    """Main entry point."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"{Colors.red('✗ ERROR')}: Input path not found: {args.input}")
        sys.exit(1)

    compiler = JackCompiler(verbose=args.verbose, warnings=not args.no_warnings, werror=args.werror)

    if input_path.is_file():
        if args.recursive:
            parser.error("--recursive requires a directory as input")
        output_path = Path(args.output) if args.output else input_path.with_suffix('.vm')
        if args.clean or args.dry_run:
            success = compiler._run_batch(
                [(input_path, output_path)], 'JACK COMPILER - SINGLE FILE',
                clean=args.clean, dry_run=args.dry_run, targets_only=True,
            )
        else:
            print(f"\n{Colors.bold(Colors.blue('JACK COMPILER - SINGLE FILE'))}\n")
            success = compiler.compile_file(str(input_path), str(output_path))
            print()
    else:
        output_dir = args.output or str(input_path)
        success = compiler.compile_directory(
            str(input_path), output_dir,
            recursive=args.recursive, clean=args.clean, dry_run=args.dry_run,
        )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
