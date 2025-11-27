"""
Unit tests for Jack compiler.
Tests lexing, parsing, and code generation functionality.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from symbols import SymbolTable, VarKind, SymbolInfo
from codegen import CodeGenerator


class TestSymbolTable:
    """Test symbol table functionality."""

    def test_define_and_lookup(self):
        """Test defining and looking up symbols."""
        table = SymbolTable()

        # Define a static variable
        table.define("count", "int", VarKind.STATIC)
        assert table.kind_of("count") == VarKind.STATIC
        assert table.type_of("count") == "int"
        assert table.index_of("count") == 0

    def test_class_scope(self):
        """Test class-level symbol table."""
        table = SymbolTable()

        table.define("x", "int", VarKind.FIELD)
        table.define("y", "int", VarKind.FIELD)
        table.define("count", "int", VarKind.STATIC)

        assert table.field_count == 2
        assert table.static_count == 1
        assert table.index_of("x") == 0
        assert table.index_of("y") == 1
        assert table.index_of("count") == 0

    def test_subroutine_scope(self):
        """Test subroutine-level symbol table."""
        table = SymbolTable()

        # Define class-level variables
        table.define("x", "int", VarKind.FIELD)

        # Start subroutine
        table.start_subroutine()

        # Define subroutine-level variables
        table.define("sum", "int", VarKind.LOCAL)
        table.define("i", "int", VarKind.ARG)

        assert table.var_count(VarKind.LOCAL) == 1
        assert table.var_count(VarKind.ARG) == 1

        # Verify x is still accessible
        assert table.type_of("x") == "int"

        # Start new subroutine (scope reset)
        table.start_subroutine()
        assert table.var_count(VarKind.LOCAL) == 0
        assert table.var_count(VarKind.ARG) == 0

    def test_undefined_variable(self):
        """Test looking up undefined variables."""
        table = SymbolTable()

        assert table.kind_of("undefined") == VarKind.NONE
        assert table.type_of("undefined") is None
        assert table.index_of("undefined") is None


class TestCodeGenerator:
    """Test code generator functionality."""

    def test_push_pop_constant(self):
        """Test pushing constants."""
        gen = CodeGenerator("TestClass")

        gen.push_constant(42)
        code = gen.get_code()

        assert "push constant 42" in code

    def test_arithmetic_operations(self):
        """Test arithmetic operations."""
        gen = CodeGenerator("TestClass")

        gen.emit_add()
        gen.emit_subtract()
        gen.emit_multiply()
        gen.emit_divide()

        code = gen.get_code()
        assert "add" in code
        assert "sub" in code
        assert "call Math.multiply 2" in code
        assert "call Math.divide 2" in code

    def test_labels_and_jumps(self):
        """Test label and jump generation."""
        gen = CodeGenerator("TestClass")

        label1 = gen.new_label("TEST")
        label2 = gen.new_label("TEST")

        gen.emit_label(label1)
        gen.emit_goto(label2)
        gen.emit_label(label2)

        code = gen.get_code()
        assert "label TEST$0" in code
        assert "label TEST$1" in code
        assert "goto TEST$1" in code

    def test_function_declaration(self):
        """Test function declaration."""
        gen = CodeGenerator("TestClass")

        gen.emit_function("TestClass.main", 2)
        code = gen.get_code()

        assert "function TestClass.main 2" in code

    def test_subroutine_call(self):
        """Test subroutine call generation."""
        gen = CodeGenerator("TestClass")

        gen.emit_call("Output.printInt", 1)
        code = gen.get_code()

        assert "call Output.printInt 1" in code

    def test_string_constant(self):
        """Test string constant generation."""
        gen = CodeGenerator("TestClass")

        gen.emit_string_constant("Hi")
        code = gen.get_code()

        # Should create string and append characters
        assert "push constant 2" in code  # Length
        assert "call String.new 1" in code
        assert "push constant 72" in code  # 'H'
        assert "push constant 105" in code  # 'i'
        assert "call String.appendChar 2" in code


def run_tests():
    """Run all tests."""
    print("Running Symbol Table Tests...")
    test_table = TestSymbolTable()
    test_table.test_define_and_lookup()
    test_table.test_class_scope()
    test_table.test_subroutine_scope()
    test_table.test_undefined_variable()
    print("✓ Symbol table tests passed")

    print("\nRunning Code Generator Tests...")
    test_gen = TestCodeGenerator()
    test_gen.test_push_pop_constant()
    test_gen.test_arithmetic_operations()
    test_gen.test_labels_and_jumps()
    test_gen.test_function_declaration()
    test_gen.test_subroutine_call()
    test_gen.test_string_constant()
    print("✓ Code generator tests passed")

    print("\n✓ All tests passed!")


if __name__ == '__main__':
    run_tests()
