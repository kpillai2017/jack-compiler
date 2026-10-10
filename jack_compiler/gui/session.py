"""
session.py - What the GUI compiles, and what came out (no pygame here).
=====================================================================

A `CompileSession` is one "compile this" request from the user: a single
.jack file, or a folder of them. It works out the (source, target) pairs
with the very same rules as the `jackc` command line tool:

    jackc Main.jack            ->  Main.vm next to Main.jack
    jackc src/                 ->  src/*.vm next to each .jack file
    jackc src/ -o bin/         ->  bin/*.vm
    jackc -r projects/         ->  every .jack file in the tree

The output can be changed later: set_output() points every target at
another folder (the window's Ctrl+Shift+S, "save as"), and save() writes
the VM code that has already been compiled (Ctrl+S) - no recompiling.

then compiles each file and keeps a `FileResult` for it: the Jack source,
the generated VM code and every diagnostic (errors and warnings, each with
a line and column, see jack_compiler/diagnostics.py) so the window can mark
the exact spot, compiler-style.

Compiling runs on a background thread, so the window keeps redrawing (and
can show progress) while a big folder compiles. The window only ever
*reads* the results; the worker thread is the only one that writes them.

Keeping this free of pygame makes it easy to test - see tests/test_gui.py.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from ..compiler import JackCompiler, JackSyntaxError, find_jack_files, plan_jobs
from ..diagnostics import ERROR, WARNING, Diagnostic

# The life of a session...
IDLE = "idle"  # created, nothing compiled yet
COMPILING = "compiling"  # the worker thread is busy
DONE = "done"  # every file has been tried

# ...and of each file in it.
PENDING = "pending"
OK = "ok"
FAILED = "failed"

@dataclass
class FileResult:
    """Everything the window shows about one .jack file."""

    source: Path
    target: Path
    status: str = PENDING
    source_text: str = ""
    vm_text: str = ""
    diagnostics: List[Diagnostic] = field(default_factory=list)  # errors AND warnings
    written: bool = False  # True once the .vm file has been saved

    @property
    def errors(self) -> List[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == ERROR]

    @property
    def warnings(self) -> List[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == WARNING]

    @property
    def error_lines(self) -> List[int]:
        """Source line numbers that have at least one error (sorted, unique)."""
        return sorted({e.line for e in self.errors if e.line > 0})

    @property
    def problem_lines(self) -> List[int]:
        """Lines with an error or a warning (sorted, unique)."""
        return sorted({d.line for d in self.diagnostics if d.line > 0})

    @property
    def vm_line_count(self) -> int:
        return len(self.vm_text.splitlines())

    @property
    def function_count(self) -> int:
        return sum(1 for line in self.vm_text.splitlines() if line.lstrip().startswith("function "))


def output_is_folder(output: Path) -> bool:
    """Is a single file's -o output a folder (an existing one, or a name without .vm)?"""
    return output.is_dir() or output.suffix.lower() != ".vm"


def plan_session_jobs(
    target: Path, output: Optional[Path] = None, recursive: bool = False
) -> List[Tuple[Path, Path]]:
    """
    (source .jack, target .vm) pairs for a file or a folder, as
    `jackc target [-o output] [-r]` would compile them. For a single file,
    an `output` folder (see output_is_folder) means output/<Name>.vm.
    """
    target = Path(target)
    if target.is_file():
        if output is None:
            return [(target, target.with_suffix(".vm"))]
        output = Path(output)
        return [(target, output / target.with_suffix(".vm").name if output_is_folder(output) else output)]
    if target.is_dir():
        return plan_jobs(target, Path(output) if output else target, recursive)
    raise FileNotFoundError(f"Input path not found: {target}")


def count_jack_files(folder: Path, recursive: bool = False) -> int:
    """How many .jack files `folder` holds (0 if it can't be read)."""
    try:
        return len(find_jack_files(Path(folder), recursive))
    except OSError:
        return 0


class CompileSession:
    """Compile a file or folder and collect one FileResult per .jack file."""

    def __init__(
        self,
        target: Path,
        output: Optional[Path] = None,
        recursive: bool = False,
        write: bool = True,
        werror: bool = False,
    ) -> None:
        self.target = Path(target).expanduser().resolve()
        self.output = Path(output).expanduser().resolve() if output else None
        self.recursive = recursive
        self.write = write  # False = preview only: compiling never writes (Ctrl+S still can, see save())
        # True = warnings count as errors (like jackc --werror). Read once at
        # the start of each run, so change it only between runs.
        self.werror = werror

        jobs = plan_session_jobs(self.target, self.output, recursive)
        if not jobs:
            where = f"{self.target} (and its sub-folders)" if recursive else str(self.target)
            raise FileNotFoundError(f"No .jack files found in {where}")
        self.results = [FileResult(src, dst) for src, dst in jobs]

        self.state = IDLE
        self.completed = 0  # files tried so far in the current run
        self.started_at: Optional[float] = None
        self.finished_at: Optional[float] = None
        self._thread: Optional[threading.Thread] = None

    # --- running ------------------------------------------------------------
    def start(self) -> bool:
        """
        Compile everything on a background thread. Returns False (and does
        nothing) if a run is already in progress.
        """
        if self.state == COMPILING:
            return False
        self._begin()
        self._thread = threading.Thread(target=self._compile_all, name="jackc-gui", daemon=True)
        self._thread.start()
        return True

    def run(self) -> None:
        """Compile everything right now, on this thread (handy for tests)."""
        if self.state == COMPILING:
            raise RuntimeError("a compilation is already running")
        self._begin()
        self._compile_all()

    def wait(self, timeout: Optional[float] = None) -> bool:
        """Wait for a background run to end. Returns True if it has."""
        if self._thread is not None:
            self._thread.join(timeout)
        return self.state != COMPILING

    def _begin(self) -> None:
        for result in self.results:
            result.status = PENDING
        self.completed = 0
        self.started_at = time.perf_counter()
        self.finished_at = None
        self.state = COMPILING

    def _compile_all(self) -> None:
        compiler = JackCompiler(werror=self.werror)  # one per run: the compiler isn't thread-safe
        try:
            for result in self.results:
                self._compile_one(compiler, result)
                self.completed += 1
        finally:
            self.finished_at = time.perf_counter()
            self.state = DONE

    def _compile_one(self, compiler: JackCompiler, result: FileResult) -> None:
        diagnostics: List[Diagnostic] = []
        vm_text = ""
        written = False
        path = str(result.source)

        def fail(message: str) -> None:  # a problem that isn't on any one line
            diagnostics.append(Diagnostic(path, 0, 0, message))

        try:
            source_text = result.source.read_text(encoding="utf-8", errors="replace")
        except OSError as problem:
            source_text = ""
            fail(f"can't read file: {problem}")
        else:
            try:
                vm_text = compiler.compile_source(path)
                diagnostics.extend(compiler.diagnostics)  # warnings
            except JackSyntaxError as problem:  # syntax or semantic errors
                diagnostics.extend(problem.diagnostics)
            except Exception as problem:  # an internal compiler bug: show it, don't crash
                fail(f"internal compiler error: {type(problem).__name__}: {problem}")

        failed = any(d.is_error for d in diagnostics)
        if not failed and self.write:
            try:
                result.target.parent.mkdir(parents=True, exist_ok=True)
                result.target.write_text(vm_text, encoding="utf-8")
                written = True
            except OSError as problem:
                fail(f"can't write {result.target.name}: {problem}")

        # Fill in the details first and the status LAST: the window treats
        # "status is not PENDING" as "this result is complete".
        result.source_text = source_text
        result.vm_text = vm_text
        result.diagnostics = sorted(diagnostics, key=Diagnostic.sort_key)
        result.written = written
        result.status = FAILED if any(d.is_error for d in diagnostics) else OK

    # --- questions the window asks ------------------------------------------
    @property
    def finished(self) -> bool:
        return self.state == DONE

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def ok_count(self) -> int:
        return sum(1 for r in self.results if r.status == OK)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if r.status == FAILED)

    @property
    def warning_count(self) -> int:
        return sum(len(r.warnings) for r in self.results)

    @property
    def elapsed(self) -> float:
        """Seconds the current (or last) run took so far."""
        if self.started_at is None:
            return 0.0
        end = self.finished_at if self.finished_at is not None else time.perf_counter()
        return end - self.started_at

    # --- where the .vm files go -------------------------------------------------
    def set_output(self, output: Optional[Path]) -> None:
        """
        Send the .vm files somewhere else (None = next to the sources). The
        results are kept; only their targets change - call save() to write
        them there. From now on every (re)compile writes there too.
        """
        if self.state == COMPILING:
            raise RuntimeError("can't change the output while compiling")
        output = Path(output).expanduser().resolve() if output else None
        targets = dict(plan_session_jobs(self.target, output, self.recursive))
        for result in self.results:
            # A .jack file added since the session started isn't in self.results
            # (Ctrl+O picks it up); one deleted since keeps a target by the same rule.
            if result.source not in targets:
                base = output or (self.target if self.target.is_dir() else self.target.parent)
                if result.source != self.target and self.target in result.source.parents:
                    relative = result.source.relative_to(self.target)
                else:  # a single-file session
                    relative = Path(result.source.name)
                targets[result.source] = base / relative.with_suffix(".vm")
            result.target = targets[result.source]
            result.written = False
        self.output = output
        self.write = True

    def save(self) -> Tuple[List[Path], List[str]]:
        """
        Write the VM code of every file that compiled to its target (even in
        a preview-only session). Returns (paths written, problems).
        """
        if self.state == COMPILING:
            raise RuntimeError("can't save while compiling")
        written: List[Path] = []
        problems: List[str] = []
        for result in self.results:
            if result.status != OK:
                continue
            try:
                result.target.parent.mkdir(parents=True, exist_ok=True)
                result.target.write_text(result.vm_text, encoding="utf-8")
            except OSError as problem:
                problems.append(f"can't write {result.target}: {problem}")
                continue
            result.written = True
            written.append(result.target)
        return written, problems

    def output_folder(self) -> Path:
        """The folder the .vm files go to (for a single file, the folder its .vm file is in)."""
        if self.output is not None:
            return self.output.parent if self.target.is_file() and not output_is_folder(self.output) else self.output
        return self.target if self.target.is_dir() else self.target.parent

    def first_failed_index(self) -> Optional[int]:
        return next((i for i, r in enumerate(self.results) if r.status == FAILED), None)

    def describe_output(self) -> str:
        """Where the .vm files go, in words."""
        if not self.write:
            return "preview only (.vm files not written)"
        if self.output is None:
            return ".vm files written next to sources"
        return f".vm files written to {self.output}"
