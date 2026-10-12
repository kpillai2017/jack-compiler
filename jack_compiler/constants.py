"""Compile-time expression evaluation for constants and integer-valued enums."""

from dataclasses import dataclass

from .literals import integer_value, quoted_value


@dataclass(frozen=True)
class Constant:
    value: int
    type: str


class ConstantError(ValueError):
    pass


def signed_word(value):
    return ((value + 32768) % 65536) - 32768


def evaluate(expression, resolve):
    """Evaluate with Jack's left-to-right order and signed 16-bit arithmetic."""
    def term(node):
        if node.integerConstant():
            value = integer_value(node.integerConstant().getText())
            if value > 32767:
                raise ConstantError("integer literal is too large (maximum 32767)")
            return value
        if node.characterConstant():
            return ord(quoted_value(node.characterConstant().getText(), True))
        if node.keywordConstant():
            text = node.keywordConstant().getText()
            if text in {"true", "false"}:
                return -1 if text == "true" else 0
        if node.qualifiedConstant():
            return resolve(node.qualifiedConstant().getText()).value
        if node.varName() and not node.LBRACKET():
            return resolve(node.varName().getText()).value
        if node.LPAREN():
            return evaluate(node.expression(), resolve)
        if node.unaryOp():
            value = term(node.term())
            return signed_word(-value if node.unaryOp().getText() == "-" else ~value)
        raise ConstantError("constant expressions allow only integers, characters, booleans, constants, and operators")

    value = term(expression.term(0))
    for op, right in zip(expression.op(), expression.term()[1:]):
        rhs = term(right)
        text = op.getText()
        if text == "+": value += rhs
        elif text == "-": value -= rhs
        elif text == "*": value *= rhs
        elif text == "/":
            if rhs == 0:
                raise ConstantError("division by zero in constant expression")
            value = (abs(value) // abs(rhs)) * (-1 if (value < 0) != (rhs < 0) else 1)
        elif text == "&": value &= rhs
        elif text == "|": value |= rhs
        elif text == "<": value = -1 if value < rhs else 0
        elif text == ">": value = -1 if value > rhs else 0
        elif text == "=": value = -1 if value == rhs else 0
        elif text == "<=": value = -1 if value <= rhs else 0
        elif text == ">=": value = -1 if value >= rhs else 0
        elif text == "!=": value = -1 if value != rhs else 0
        value = signed_word(value)
    return value


def collect_constants(container, class_name, parent=None, blocked=(), report=None):
    """Resolve a declaration section, including forward references and cycles.

    Returns an environment keyed by bare constant names and Enum.member names.
    ClassName.CONSTANT aliases only refer to class-scope constants.
    """
    local_section = parent is not None
    parent = parent or {}
    blocked = set(blocked)
    definitions = {}
    values = {}
    active = set()
    failed = set()
    enum_names = set()

    def error(ctx, message):
        if report is None:
            raise ConstantError(message)
        report(ctx, message)

    def add(name, ctx, type_name, expression, previous=None):
        if name in definitions or name in blocked:
            error(ctx, f"'{name}' is already declared in this scope")
            return
        definitions[name] = (ctx, type_name, expression, previous)

    for child in container.children or []:
        rule = type(child).__name__
        if rule == "ConstDeclarationContext":
            type_name = child.type_().getText()
            for entry in child.constEntry():
                add(entry.varName().getText(), entry, type_name, entry.expression())
        elif rule == "EnumDeclarationContext":
            enum_name = child.className().getText()
            if enum_name in enum_names or enum_name in blocked or enum_name == class_name:
                error(child, f"enum name '{enum_name}' conflicts with another declaration")
            enum_names.add(enum_name)
            previous = None
            for member in child.enumMember():
                name = enum_name + "." + member.varName().getText()
                add(name, member, "int", member.expression(), previous)
                previous = name
    for enum_name in enum_names:
        if enum_name in definitions:
            error(definitions[enum_name][0], f"constant '{enum_name}' conflicts with an enum name")

    if local_section:
        inherited_enums = {name.split(".")[0] for name in parent if "." in name}
        for name in (blocked | set(definitions)) & inherited_enums:
            error(container, f"'{name}' conflicts with an enum namespace")

    def resolve(name):
        if name.startswith(class_name + "."):
            bare = name[len(class_name) + 1:]
            # Parent is present for local sections; otherwise resolve this class.
            if local_section:
                if bare in parent and "." not in bare:
                    return parent[bare]
                raise ConstantError(f"unknown class constant '{name}'")
            if "." in bare:
                raise ConstantError(f"unknown class constant '{name}'")
            name = bare
        if name in values:
            return values[name]
        if name in definitions:
            if name in active:
                raise ConstantError(f"cyclic constant definition involving '{name}'")
            if name in failed:
                raise ConstantError(f"constant '{name}' has an invalid definition")
            ctx, type_name, expression, previous = definitions[name]
            if type_name not in {"int", "char", "boolean"}:
                raise ConstantError("constants must have type int, char, or boolean")
            active.add(name)
            try:
                value = evaluate(expression, resolve) if expression is not None else (resolve(previous).value + 1 if previous else 0)
                if not -32768 <= value <= 32767:
                    raise ConstantError("enum value is outside the signed 16-bit range")
                if type_name == "char" and value < 0:
                    raise ConstantError("char constants must be between 0 and 32767")
                if type_name == "boolean" and value not in {-1, 0}:
                    raise ConstantError("boolean constants must evaluate to true (-1) or false (0)")
                values[name] = Constant(value, type_name)
                return values[name]
            finally:
                active.remove(name)
        if name in blocked:
            raise ConstantError(f"'{name}' is a variable, not a compile-time constant")
        if name in parent:
            return parent[name]
        raise ConstantError(f"unknown compile-time constant '{name}'")

    for name, definition in definitions.items():
        try:
            resolve(name)
        except ValueError as problem:
            failed.add(name)
            error(definition[0], str(problem))
    return {**parent, **values}


def lookup_constant(name, environment, class_environment, class_name, blocked=()):
    if name.startswith(class_name + "."):
        name = name[len(class_name) + 1:]
        return class_environment.get(name) if "." not in name else None
    return None if name in blocked else environment.get(name)
