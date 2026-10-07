"""
Main Jack compiler driver.
Converts Jack source files to Hack VM code.

Usage:
    jackc input.jack -o output.vm
    jackc input_dir -o output_dir
    python -m jack_compiler input.jack
"""

import argparse
import os
import sys
import traceback
from pathlib import Path

from antlr4 import CommonTokenStream, FileStream

from .antlr_generated.grammar.JackLexer import JackLexer
from .antlr_generated.grammar.JackParser import JackParser
from .compiler_visitor import JackCompilerVisitor


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
            SyntaxError: If the source contains syntax errors.
        """
        input_stream = FileStream(input_path, encoding='utf-8')
        parser = JackParser(CommonTokenStream(JackLexer(input_stream)))
        tree = parser.program()

        if parser.getNumberOfSyntaxErrors() > 0:
            raise SyntaxError(
                f"{parser.getNumberOfSyntaxErrors()} syntax error(s) in {input_path}"
            )

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
            print(f"\n{Colors.red('✗ FILE NOT FOUND')}: {input_path}")
            return False
        except SyntaxError:
            print(f"\n{Colors.red('✗ COMPILATION FAILED')}: {input_path}")
            print(f"  {Colors.red('Syntax errors detected')}")
            return False
        except Exception as e:  # pragma: no cover - defensive
            print(f"\n{Colors.red('✗ COMPILATION ERROR')}: {input_path}")
            print(f"  {Colors.red(str(e))}")
            if self.verbose:
                traceback.print_exc()
            return False

    def compile_directory(self, input_dir: str, output_dir: str) -> bool:
        """
        Compile all Jack files in a directory.

        Args:
            input_dir: Directory containing .jack files
            output_dir: Directory for output .vm files

        Returns:
            True if all compilations succeeded, False otherwise
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        if not input_path.is_dir():
            print(f"\n{Colors.red('✗ ERROR')}: Input directory not found: {input_dir}")
            return False

        jack_files = sorted(input_path.glob("*.jack"))

        if not jack_files:
            print(f"{Colors.yellow('⚠ WARNING')}: No .jack files found in {input_dir}")
            return False

        print(f"\n{Colors.blue('═' * 60)}")
        print(f"{Colors.bold(Colors.blue('JACK COMPILER - BATCH COMPILATION'))}")
        print(f"{Colors.blue('═' * 60)}")
        print(f"{Colors.cyan(f'Found {len(jack_files)} Jack file(s) to compile')}")
        print(f"{Colors.blue('─' * 60)}\n")

        all_succeeded = True
        for i, jack_file in enumerate(jack_files, 1):
            vm_file = output_path / f"{jack_file.stem}.vm"
            print(f"{Colors.cyan(f'[{i}/{len(jack_files)}]')} ", end="")
            if not self.compile_file(str(jack_file), str(vm_file)):
                all_succeeded = False
            print()

        print(f"{Colors.blue('─' * 60)}")
        if all_succeeded:
            print(f"{Colors.green('✓ ALL COMPILATIONS SUCCESSFUL')}")
        else:
            print(f"{Colors.red('✗ SOME COMPILATIONS FAILED')}")
        print(f"{Colors.blue('═' * 60)}\n")

        return all_succeeded


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
        """
    )
    parser.add_argument('input', help='Input Jack file or directory')
    parser.add_argument(
        '-o', '--output',
        help='Output VM file or directory (default: same as input)',
        default=None,
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
    args = build_arg_parser().parse_args(argv)
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"{Colors.red('✗ ERROR')}: Input path not found: {args.input}")
        sys.exit(1)

    compiler = JackCompiler(verbose=args.verbose)

    if input_path.is_file():
        output_path = args.output or str(input_path.with_suffix('.vm'))
        print(f"\n{Colors.bold(Colors.blue('JACK COMPILER - SINGLE FILE'))}\n")
        success = compiler.compile_file(str(input_path), output_path)
        print()
    else:
        output_dir = args.output or str(input_path)
        success = compiler.compile_directory(str(input_path), output_dir)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
