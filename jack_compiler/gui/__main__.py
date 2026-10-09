"""Allow ``python -m jack_compiler.gui``."""

import sys

from .main import main

if __name__ == "__main__":
    sys.exit(main())
