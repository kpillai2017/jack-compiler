"""
theme.py - Fonts and colours shared by every part of the GUI.
============================================================

The palette is the same as jackvm-py's player and debugger, so the compiler
and the VM look like two halves of one tool.
"""

# The first of these monospace fonts that is installed gets used, so the
# columns of code always line up.
MONO_FONTS = "menlo,consolas,dejavusansmono,couriernew,monospace"

# Named text colours. Rows of text say *which kind* they are ("dim",
# "error", ...) and the drawing code looks the colour up here.
COLOURS = {
    "normal": (230, 230, 230),
    "dim": (130, 130, 140),
    "title": (120, 190, 255),
    "highlight": (255, 210, 90),
    "error": (255, 110, 110),
    "ok": (120, 220, 140),
    "warning": (240, 170, 70),
    "note": (120, 200, 210),
    # Extra kinds used only for syntax colouring in the code view.
    "keyword": (120, 190, 255),
    "string": (230, 180, 120),
    "number": (190, 160, 255),
    "comment": (110, 120, 130),
    "symbol": (180, 185, 200),
    "label": (255, 210, 90),
}

BACKGROUND = (30, 30, 36)  # behind everything
BOX = (40, 42, 52)  # inside a box
BOX_HEADER = (50, 54, 70)  # the title strip of a box
BOX_HEADER_FOCUSED = (62, 72, 104)  # the title strip of the focused code pane
BORDER = (88, 96, 120)  # box outlines
FRAME_COLOUR = (150, 160, 190)  # the frame around the code view
ERROR_LINE = (80, 36, 42)  # background of a source line that has an error
WARNING_LINE = (70, 56, 30)  # ...and of one that has a warning
GUTTER = (34, 36, 44)  # behind the line numbers
