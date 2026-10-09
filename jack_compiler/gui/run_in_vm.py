"""
run_in_vm.py - Ctrl+J: run the compiled program in JackVM (no pygame here).
=========================================================================

JackVM (https://github.com/kpillai2017/jackvm-py) is a separate app in its
own repository. If it's installed (see ../integrations.py for how it is
found), Ctrl+J in the compiler window starts it in a second window with the
program you are looking at:

  * "The program" is every .jack file in the SAME FOLDER as the selected
    tab - one folder = one Jack program, as in nand2tetris. (A recursive
    session can hold many programs; you run the one you're looking at.)
  * It only runs when all of those files compiled without errors.
  * The VM code is written to a fresh temporary folder, so it works in
    preview mode (--no-write) too and never mixes with old .vm files.
    Other .vm files already next to the output (classes this session
    didn't compile, e.g. Ball.vm when only Main.jack was opened) are
    copied in as well. JackVM brings its own Jack OS (Math, Screen, ...).
  * Pressing Ctrl+J again closes the previous JackVM window first.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from ..integrations import JACKVM, Companion, find
from .session import OK, CompileSession, FileResult

LOG_NAME = "jackvm.log"  # what JackVM printed, kept in the run folder


def program_results(session: CompileSession, index: int) -> List[FileResult]:
    """The files that make up the program of tab `index`: its whole folder."""
    folder = session.results[index].source.parent
    return [r for r in session.results if r.source.parent == folder]


class VMLauncher:
    """Starts (and restarts) JackVM on the compiler's output."""

    def __init__(self, finder: Callable[[], Optional[Companion]] = lambda: find(JACKVM)) -> None:
        self.companion = finder()
        self.process: Optional[subprocess.Popen] = None
        self.folder: Optional[Path] = None
        self._reported = True  # has the current process's failure been shown?

    @property
    def available(self) -> bool:
        return self.companion is not None

    def not_found_message(self) -> str:
        return f"JackVM not found. Install it: {JACKVM.install_hint}"

    def launch(self, session: CompileSession, index: int) -> Tuple[bool, str]:
        """Try to run tab `index`'s program. Returns (started?, message for the user)."""
        if self.companion is None:
            return False, self.not_found_message()
        if not session.finished:
            return False, "Still compiling - try again when it's done"
        results = program_results(session, index)
        broken = [r for r in results if r.status != OK]
        if broken:
            more = f" (+{len(broken) - 1} more)" if len(broken) > 1 else ""
            return False, f"Fix the errors in {broken[0].source.name}{more} first"

        self.stop()
        self.folder = Path(tempfile.mkdtemp(prefix="jackc-run-"))
        names = set()
        for result in results:
            name = result.source.stem + ".vm"
            (self.folder / name).write_text(result.vm_text, encoding="utf-8")
            names.add(name.lower())
        for extra in sorted(results[0].target.parent.glob("*.vm")):  # classes compiled earlier
            if extra.name.lower() not in names and extra.is_file():
                shutil.copy(extra, self.folder / extra.name)
                names.add(extra.name.lower())

        log = open(self.folder / LOG_NAME, "w", encoding="utf-8")
        try:
            self.process = self.companion.launch([str(self.folder)], stdout=log, stderr=subprocess.STDOUT)
        except OSError as problem:
            self.process = None
            return False, f"Couldn't start JackVM: {problem}"
        finally:
            log.close()  # the child process keeps its own copy of the file
        self._reported = False
        return True, f"Running {len(names)} file{'s' if len(names) != 1 else ''} in JackVM"

    def poll_failure(self) -> Optional[str]:
        """
        Called every frame: if JackVM has just exited with an error (e.g. a
        runtime error, or it couldn't load the program), return what it
        said - once. Otherwise None.
        """
        if self.process is None or self._reported or self.process.poll() is None:
            return None
        self._reported = True
        if self.process.returncode == 0:
            return None
        said = ""
        if self.folder is not None:
            try:
                lines = (self.folder / LOG_NAME).read_text(encoding="utf-8", errors="replace").strip().splitlines()
                said = lines[-1] if lines else ""
            except OSError:
                pass
        return f"JackVM stopped (exit {self.process.returncode})" + (f": {said}" if said else "")

    def stop(self) -> None:
        """Close the JackVM window we started (if it's still open) and tidy up."""
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.process = None
        if self.folder is not None:
            shutil.rmtree(self.folder, ignore_errors=True)
            self.folder = None
