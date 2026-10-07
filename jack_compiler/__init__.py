"""Jack compiler for the nand2tetris Hack platform."""

__version__ = "1.1.0"

from .codegen import CodeGenerator
from .compiler import JackCompiler, JackSyntaxError
from .compiler_visitor import JackCompilerVisitor
from .symbols import SymbolInfo, SymbolTable, VarKind

__all__ = [
    "__version__",
    "JackCompiler",
    "JackSyntaxError",
    "JackCompilerVisitor",
    "CodeGenerator",
    "SymbolTable",
    "VarKind",
    "SymbolInfo",
]
