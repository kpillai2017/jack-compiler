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
from typing import List, Tuple

from antlr4 import CommonTokenStream, FileStream
from antlr4.error.ErrorListener import ErrorListener

from .antlr_generated.grammar.JackLexer import JackLexer
from .antlr_generated.grammar.JackParser import JackParser
from .compiler_visitor import JackCompilerVisitor


class JackSyntaxError(SyntaxError):
    """Raised when a Jack source file has lexical or syntax errors."""

    def __init__(self, source: str, errors: List[str]):
        super().__init__(f"{len(errors)} syntax error(s) in {source}")
        self.source = source
        self.errors = errors


class CollectingErrorListener(ErrorListener):
    """
    Collects ANTLR lexer/parser errors as ``file:line:col: message`` strings
    instead of printing them to stderr, so they can be reported alongside
    the file they belong to. Columns are 1-based.
    """

    def __init__(self, source: str):
        super().__init__()
        self.source = source
        self.errors: List[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"{self.source}:{line}:{column + 1}: {msg}")


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

    def __init__(self, verbose: bool = False):
        """
        Initialize the compiler.

        Args:
            verbose: Print a full traceback on unexpected internal errors.
        """
        self.visitor = JackCompilerVisitor()
        self.verbose = verbose

    def compile_source(self, input_path: str) -> str:
        """
        Compile a single Jack file and return the generated VM code.

        Raises:
            FileNotFoundError: If the input file does not exist.
            JackSyntaxError: If the source contains lexical or syntax errors;
                ``.errors`` holds ``file:line:col: message`` strings.
        """
        input_stream = FileStream(input_path, encoding='utf-8')
        listener = CollectingErrorListener(input_path)

        lexer = JackLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(listener)

        parser = JackParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(listener)

        tree = parser.program()

        if listener.errors:
            raise JackSyntaxError(input_path, listener.errors)

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

            print(f"{Colors.green('✓ SUCCESS')}: {input_path}")
            print(f"  {Colors.cyan('→')} {output_path}")
            return True

        except FileNotFoundError:
            print(f"{Colors.red('✗ FILE NOT FOUND')}: {input_path}")
            return False
        except JackSyntaxError as e:
            print(f"{Colors.red('✗ COMPILATION FAILED')}: {input_path}")
            print(f"  {Colors.red(f'{len(e.errors)} syntax error(s):')}")
            for err in e.errors:
                print(f"  {err}")
            return False
        except Exception as e:  # pragma: no cover - defensive
            print(f"{Colors.red('✗ COMPILATION ERROR')}: {input_path}")
            print(f"  {Colors.red(str(e))}")
            if self.verbose:
                traceback.print_exc()
            return False

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

    compiler = JackCompiler(verbose=args.verbose)

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
