"""Jack compiler for the nand2tetris Hack platform."""

__version__ = "1.2.0"

from .codegen import CodeGenerator
from .compiler import JackCompiler, JackSemanticError, JackSyntaxError
from .diagnostics import Diagnostic, render as render_diagnostic
from .compiler_visitor import JackCompilerVisitor
from .symbols import SymbolInfo, SymbolTable, VarKind

__all__ = [
    "__version__",
    "JackCompiler",
    "JackSyntaxError",
    "JackSemanticError",
    "Diagnostic",
    "render_diagnostic",
    "JackCompilerVisitor",
    "CodeGenerator",
    "SymbolTable",
    "VarKind",
    "SymbolInfo",
]
