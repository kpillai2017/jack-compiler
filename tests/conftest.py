"""
Shared test set-up, loaded by pytest before any test module.

The GUI tests use SDL's "dummy" drivers: pygame draws into memory and no
real window pops up, so they also run on CI machines without a display.
`setdefault` lets you override this from the shell to watch a test draw,
e.g. `SDL_VIDEODRIVER=cocoa pytest tests/test_gui.py`.
"""

import os
import tempfile

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

# Never pick up a real JackVM installed on this machine: tests that need one
# pass a fake (see tests/test_integrations.py). JACKVM=off disables the lookup.
os.environ["JACKVM"] = "off"

# ...and never read or write the real config file (~/.config/jack-tools/config.ini):
# tests that need one make their own (see tests/test_locate_app.py).
os.environ["JACK_TOOLS_CONFIG"] = os.path.join(tempfile.gettempdir(), f"jack-tools-tests-{os.getpid()}", "config.ini")
