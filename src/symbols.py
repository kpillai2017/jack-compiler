"""
Symbol Table management for Jack compiler.
Handles variable scope (class, method, local) and maintains type information.
"""

from enum import Enum
from typing import Dict, Optional, Tuple


class VarKind(Enum):
    """Variable kind classification."""
    STATIC = "static"
    FIELD = "field"
    ARG = "argument"
    LOCAL = "local"
    NONE = "none"


class SymbolInfo:
    """Information about a symbol (variable)."""

    def __init__(self, name: str, type_: str, kind: VarKind, index: int):
        self.name = name
        self.type = type_
        self.kind = kind
        self.index = index

    def __repr__(self):
        return f"SymbolInfo({self.name}, {self.type}, {self.kind.value}, {self.index})"


class SymbolTable:
    """
    Symbol table for Jack compiler.
    Manages class-level (static, field) and subroutine-level (local, argument) scopes.
    """

    def __init__(self):
        """Initialize class and subroutine-level symbol tables."""
        self.class_symbols: Dict[str, SymbolInfo] = {}
        self.subroutine_symbols: Dict[str, SymbolInfo] = {}

        # Counters for each kind
        self.static_count = 0
        self.field_count = 0
        self.arg_count = 0
        self.local_count = 0

    def start_subroutine(self):
        """Start a new subroutine scope (reset subroutine-level symbols)."""
        self.subroutine_symbols.clear()
        self.arg_count = 0
        self.local_count = 0

    def define(self, name: str, type_: str, kind: VarKind):
        """
        Define a new variable in the appropriate scope.

        Args:
            name: Variable name
            type_: Variable type (int, boolean, String, or class name)
            kind: Variable kind (STATIC, FIELD, ARG, or LOCAL)
        """
        if kind == VarKind.STATIC:
            index = self.static_count
            self.static_count += 1
            self.class_symbols[name] = SymbolInfo(name, type_, kind, index)
        elif kind == VarKind.FIELD:
            index = self.field_count
            self.field_count += 1
            self.class_symbols[name] = SymbolInfo(name, type_, kind, index)
        elif kind == VarKind.ARG:
            index = self.arg_count
            self.arg_count += 1
            self.subroutine_symbols[name] = SymbolInfo(name, type_, kind, index)
        elif kind == VarKind.LOCAL:
            index = self.local_count
            self.local_count += 1
            self.subroutine_symbols[name] = SymbolInfo(name, type_, kind, index)

    def kind_of(self, name: str) -> VarKind:
        """
        Return the kind of the named identifier.

        Args:
            name: Variable name to look up

        Returns:
            VarKind of the variable, or NONE if not found
        """
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name].kind
        if name in self.class_symbols:
            return self.class_symbols[name].kind
        return VarKind.NONE

    def type_of(self, name: str) -> Optional[str]:
        """
        Return the type of the named identifier.

        Args:
            name: Variable name to look up

        Returns:
            Type of the variable, or None if not found
        """
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name].type
        if name in self.class_symbols:
            return self.class_symbols[name].type
        return None

    def index_of(self, name: str) -> Optional[int]:
        """
        Return the index of the named identifier.

        Args:
            name: Variable name to look up

        Returns:
            Index of the variable, or None if not found
        """
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name].index
        if name in self.class_symbols:
            return self.class_symbols[name].index
        return None

    def var_count(self, kind: VarKind) -> int:
        """
        Return the count of variables of the given kind.

        Args:
            kind: Variable kind to count

        Returns:
            Number of variables of the given kind
        """
        if kind == VarKind.STATIC:
            return self.static_count
        elif kind == VarKind.FIELD:
            return self.field_count
        elif kind == VarKind.ARG:
            return self.arg_count
        elif kind == VarKind.LOCAL:
            return self.local_count
        return 0

    def get_symbol(self, name: str) -> Optional[SymbolInfo]:
        """
        Get the complete symbol information.

        Args:
            name: Variable name to look up

        Returns:
            SymbolInfo object, or None if not found
        """
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name]
        if name in self.class_symbols:
            return self.class_symbols[name]
        return None
