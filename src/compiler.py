#!/usr/bin/env python3
"""
Main Jack compiler driver.
Converts Jack source files to Hack VM code.

Usage:
    python compiler.py input.jack -o output.vm
    python compiler.py input_dir -o output_dir
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional

from antlr4 import (
    FileStream,
    CommonTokenStream,
    ParseTreeWalker,
    InputStream,
)

# ANSI color codes for terminal output
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    
    @staticmethod
    def green(text):
        return f"{Colors.GREEN}{text}{Colors.RESET}"
    
    @staticmethod
    def red(text):
        return f"{Colors.RED}{text}{Colors.RESET}"
    
    @staticmethod
    def yellow(text):
        return f"{Colors.YELLOW}{text}{Colors.RESET}"
    
    @staticmethod
    def blue(text):
        return f"{Colors.BLUE}{text}{Colors.RESET}"
    
    @staticmethod
    def cyan(text):
        return f"{Colors.CYAN}{text}{Colors.RESET}"
    
    @staticmethod
    def bold(text):
        return f"{Colors.BOLD}{text}{Colors.RESET}"

# Import ANTLR-generated lexer and parser
try:
    from antlr_generated.grammar.JackLexer import JackLexer
    from antlr_generated.grammar.JackParser import JackParser
except ImportError:
    print(Colors.red("ERROR: ANTLR-generated files not found."))
    print(Colors.yellow("Please run:"))
    print("  java -jar antlr-4.13.0-complete.jar -Dlanguage=Python3 grammar/Jack.g4 -visitor -o src/antlr_generated")
    sys.exit(1)

from compiler_visitor_v2 import JackCompilerVisitorV2


class JackCompiler:
    """Main compiler class."""

    def __init__(self):
        """Initialize the compiler."""
        self.visitor = JackCompilerVisitorV2()

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
            # Create input stream from file
            input_stream = FileStream(input_path, encoding='utf-8')

            # Create lexer and token stream
            lexer = JackLexer(input_stream)
            stream = CommonTokenStream(lexer)

            # Create parser
            parser = JackParser(stream)

            # Add error listener (optional, for better error messages)
            # parser.removeErrorListeners()
            # parser.addErrorListener(CustomErrorListener())

            # Parse the program
            tree = parser.program()

            # Check for syntax errors
            if parser.getNumberOfSyntaxErrors() > 0:
                print(f"\n{Colors.red('✗ COMPILATION FAILED')}: {input_path}")
                print(f"  {Colors.red('Syntax errors detected')}")
                return False

            # Compile using visitor - generates AST and VM code
            ast = self.visitor.compile_program(tree)
            
            # Get VM code from code generator
            vm_code = self.visitor.codegen.get_code()

            # Write VM output
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(vm_code)

            print(f"{Colors.green('✓ SUCCESS')}: {input_path}")
            print(f"  {Colors.cyan('→')} {output_path}")
            return True

        except FileNotFoundError:
            print(f"\n{Colors.red('✗ FILE NOT FOUND')}: {input_path}")
            return False
        except Exception as e:
            print(f"\n{Colors.red('✗ COMPILATION ERROR')}: {input_path}")
            print(f"  {Colors.red(str(e))}")
            import traceback
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

        # Find all .jack files
        jack_files = list(input_path.glob("*.jack"))

        if not jack_files:
            print(f"{Colors.yellow('⚠ WARNING')}: No .jack files found in {input_dir}")
            return False

        print(f"\n{Colors.blue('═' * 60)}")
        print(f"{Colors.bold(Colors.blue('JACK COMPILER - BATCH COMPILATION'))}")
        print(f"{Colors.blue('═' * 60)}")
        print(f"{Colors.cyan(f'Found {len(jack_files)} Jack file(s) to compile')}")
        print(f"{Colors.blue('─' * 60)}\n")

        all_succeeded = True
        for i, jack_file in enumerate(sorted(jack_files), 1):
            vm_file = output_path / jack_file.stem
            vm_file = vm_file.with_suffix('.vm')
            
            print(f"{Colors.cyan(f'[{i}/{len(jack_files)}]')} ", end="")

            if not self.compile_file(str(jack_file), str(vm_file)):
                all_succeeded = False
            print()  # Add spacing between compilations

        # Print summary
        print(f"{Colors.blue('─' * 60)}")
        if all_succeeded:
            print(f"{Colors.green('✓ ALL COMPILATIONS SUCCESSFUL')}")
        else:
            print(f"{Colors.red('✗ SOME COMPILATIONS FAILED')}")
        print(f"{Colors.blue('═' * 60)}\n")

        return all_succeeded


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Jack compiler for nand2tetris Hack computer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compile a single file
  python compiler.py main.jack -o main.vm

  # Compile all Jack files in a directory
  python compiler.py src/ -o bin/

  # In-place compilation (output to same directory)
  python compiler.py src/
        """
    )

    parser.add_argument(
        'input',
        help='Input Jack file or directory'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output VM file or directory (default: same as input)',
        default=None
    )

    args = parser.parse_args()

    # Determine if input is file or directory
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"{Colors.red('✗ ERROR')}: Input path not found: {args.input}")
        sys.exit(1)

    compiler = JackCompiler()

    if input_path.is_file():
        # Single file compilation
        if not args.output:
            output_path = input_path.with_suffix('.vm')
        else:
            output_path = args.output

        print(f"\n{Colors.bold(Colors.blue('JACK COMPILER - SINGLE FILE'))}\n")
        success = compiler.compile_file(str(input_path), str(output_path))
        print()
        sys.exit(0 if success else 1)

    else:
        # Directory compilation
        if not args.output:
            output_dir = input_path
        else:
            output_dir = args.output

        success = compiler.compile_directory(str(input_path), str(output_dir))
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
