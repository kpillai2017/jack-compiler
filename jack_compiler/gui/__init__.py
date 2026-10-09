"""
A pygame front end for the Jack compiler (``jackc-gui``).

Modules:
    session      compile a file/folder in the background (no pygame)
    syntax       colour Jack and VM code line by line (no pygame)
    annotate     compiler-style ^~~~ error messages under the code (no pygame)
    panel        the STATUS / FILES / PROBLEMS / OUTPUT boxes
    file_picker  choose a .jack file or folder inside the window
    window       the main window: code view, Esc-to-quit, shortcuts
    main         command line entry point

Only `panel`, `file_picker` and `window` need pygame, and they import it
lazily or are only imported when the window opens, so ``import
jack_compiler`` keeps working without it.
"""

from .session import CompileSession, FileResult

__all__ = ["CompileSession", "FileResult"]
