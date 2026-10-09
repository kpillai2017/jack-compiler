"""
Shared test set-up, loaded by pytest before any test module.

The GUI tests use SDL's "dummy" drivers: pygame draws into memory and no
real window pops up, so they also run on CI machines without a display.
`setdefault` lets you override this from the shell to watch a test draw,
e.g. `SDL_VIDEODRIVER=cocoa pytest tests/test_gui.py`.
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
