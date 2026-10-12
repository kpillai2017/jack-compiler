"""Literal conversion shared by semantic checking and VM generation."""

ESCAPES = {
    "n": "\n", "r": "\r", "t": "\t", "b": "\b", "f": "\f",
    "0": "\0", "\\": "\\", '"': '"', "'": "'",
}


def integer_value(text: str) -> int:
    """Parse decimal (including leading zeros), hexadecimal, or binary."""
    if text.lower().startswith("0x"):
        return int(text[2:], 16)
    if text.lower().startswith("0b"):
        return int(text[2:], 2)
    return int(text, 10)


def quoted_value(text: str, extensions: bool = False) -> str:
    """Decode a quoted literal; standard Jack keeps backslashes verbatim."""
    body = text[1:-1]
    if not extensions:
        return body
    result = []
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\":
            index += 1
            if index == len(body) or body[index] not in ESCAPES:
                escape = body[index] if index < len(body) else ""
                raise ValueError("unsupported escape sequence: " + "\\" + escape)
            char = ESCAPES[body[index]]
        if ord(char) > 32767:
            raise ValueError("literal characters must have codes between 0 and 32767")
        result.append(char)
        index += 1
    if len(result) > 32767:
        raise ValueError("string literal is too long (maximum 32767 characters)")
    return "".join(result)
