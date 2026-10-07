"""
Code generator for Jack compiler.
Converts parsed Jack AST to Hack VM code.
"""

from typing import List

from .symbols import SymbolTable, VarKind


class CodeGenerator:
    """
    Generates Hack VM code from Jack programs.
    Handles expression evaluation, statements, and subroutine calls.
    """

    def __init__(self, class_name: str):
        """
        Initialize code generator.

        Args:
            class_name: Name of the current class being compiled
        """
        self.class_name = class_name
        self.symbol_table = SymbolTable()
        self.code: List[str] = []
        self.label_counter = 0
        self.current_subroutine = None

    def emit(self, line: str):
        """Emit a line of VM code."""
        # Add indentation (4 spaces) for all non-function/label lines
        if line.startswith("function ") or line.startswith("label "):
            self.code.append(line)
        else:
            self.code.append("    " + line)

    def get_code(self) -> str:
        """Get all generated VM code as a string."""
        return "\n".join(self.code)

    def new_label(self, prefix: str = "LABEL") -> str:
        """
        Generate a unique label.

        Args:
            prefix: Label prefix (e.g., "WHILE", "IF", "ELSE")

        Returns:
            Unique label name in format PREFIX$counter
        """
        label = f"{prefix}${self.label_counter}"
        self.label_counter += 1
        return label

    # Variable access operations
    def push_constant(self, value: int):
        """Push a constant value onto the stack."""
        self.emit(f"push constant {value}")

    def push_variable(self, name: str):
        """Push a variable onto the stack."""
        symbol = self.symbol_table.get_symbol(name)
        if symbol is None:
            raise ValueError(f"Undefined variable: {name}")
        self._push_segment(symbol.kind, symbol.index)

    def pop_variable(self, name: str):
        """Pop the stack into a variable."""
        symbol = self.symbol_table.get_symbol(name)
        if symbol is None:
            raise ValueError(f"Undefined variable: {name}")
        self._pop_segment(symbol.kind, symbol.index)

    def _push_segment(self, kind: VarKind, index: int):
        """Push a value from memory segment onto the stack."""
        segment = self._kind_to_segment(kind)
        self.emit(f"push {segment} {index}")

    def _pop_segment(self, kind: VarKind, index: int):
        """Pop the stack into a memory segment."""
        segment = self._kind_to_segment(kind)
        self.emit(f"pop {segment} {index}")

    def _kind_to_segment(self, kind: VarKind) -> str:
        """Convert variable kind to VM memory segment."""
        mapping = {
            VarKind.STATIC: "static",
            VarKind.FIELD: "this",
            VarKind.ARG: "argument",
            VarKind.LOCAL: "local",
        }
        return mapping.get(kind, "local")

    # Arithmetic and logical operations
    def emit_add(self):
        """Emit addition operation."""
        self.emit("add")

    def emit_subtract(self):
        """Emit subtraction operation."""
        self.emit("sub")

    def emit_multiply(self):
        """Emit multiplication operation."""
        self.emit("call Math.multiply 2")

    def emit_divide(self):
        """Emit division operation."""
        self.emit("call Math.divide 2")

    def emit_negate(self):
        """Emit negation operation."""
        self.emit("neg")

    def emit_and(self):
        """Emit bitwise AND operation."""
        self.emit("and")

    def emit_or(self):
        """Emit bitwise OR operation."""
        self.emit("or")

    def emit_not(self):
        """Emit bitwise NOT operation."""
        self.emit("not")

    def emit_lt(self):
        """Emit less-than comparison."""
        self.emit("lt")

    def emit_gt(self):
        """Emit greater-than comparison."""
        self.emit("gt")

    def emit_eq(self):
        """Emit equality comparison."""
        self.emit("eq")

    # Control flow
    def emit_label(self, label: str):
        """Emit a label."""
        self.emit(f"label {label}")

    def emit_goto(self, label: str):
        """Emit an unconditional jump."""
        self.emit(f"goto {label}")

    def emit_if_goto(self, label: str):
        """Emit a conditional jump (jump if top of stack is true)."""
        self.emit(f"if-goto {label}")

    def emit_if_else(self, if_label: str, else_label: str, end_label: str):
        """
        Emit if-else branching.
        Assumes condition is on top of stack.
        """
        self.emit_if_goto(if_label)
        self.emit_goto(else_label)

    # Subroutine calls
    def emit_call(self, function_name: str, num_args: int):
        """
        Emit a subroutine call.

        Args:
            function_name: Fully qualified function name (ClassName.methodName)
            num_args: Number of arguments
        """
        self.emit(f"call {function_name} {num_args}")

    def emit_return(self):
        """Emit a return statement."""
        self.emit("return")

    # Function definition
    def emit_function(self, function_name: str, num_locals: int):
        """
        Emit function declaration.

        Args:
            function_name: Fully qualified function name
            num_locals: Number of local variables
        """
        self.emit(f"function {function_name} {num_locals}")

    # Memory operations
    def emit_array_access(self):
        """
        Handle array access.
        Assumes base address and index are on stack.
        Pushes the value at base address + index.
        """
        self.emit("add")
        self.emit("pop pointer 1")
        self.emit("push that 0")

    def emit_array_assignment(self):
        """
        Handle array assignment.
        Assumes base address, index, and value are on stack (in that order).
        """
        self.emit("pop temp 0")  # Save value
        self.emit("add")  # Add base + index
        self.emit("pop pointer 1")  # pointer 1 = base + index
        self.emit("push temp 0")  # Restore value
        self.emit("pop that 0")  # Store value at that[0]

    # String handling
    def emit_string_constant(self, string_value: str):
        """
        Emit code to create a string constant.

        Args:
            string_value: The string value (without quotes)
        """
        # Call String.new with length
        length = len(string_value)
        self.emit(f"push constant {length}")
        self.emit("call String.new 1")

        # Append each character
        for char in string_value:
            char_code = ord(char)
            self.emit(f"push constant {char_code}")
            self.emit("call String.appendChar 2")

    # Utility
    def emit_pop_temp(self):
        """Pop stack into temp 0 (used to discard return values)."""
        self.emit("pop temp 0")

    def emit_this_pointer(self):
        """Push the this pointer."""
        self.emit("push pointer 0")

    def emit_that_pointer(self):
        """Push the that pointer."""
        self.emit("push pointer 1")
