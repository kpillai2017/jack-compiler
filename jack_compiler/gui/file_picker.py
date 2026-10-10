"""
file_picker.py - Choose what to compile with the mouse (or keyboard).
===================================================================

The same little file browser as jackvm-py's, drawn inside the pygame
window, but for Jack sources:

    jackc-gui                 # no path given -> the picker opens
    jackc-gui --gui src/      # start the picker in src/
    Ctrl+O in the window      # pick something else to compile

You can compile either:

  * a single **.jack file**  - click it, or
  * a **folder of .jack files** (one file per Jack class, e.g. a whole
    nand2tetris project) - click "[compile]" next to the folder, or open
    the folder and press the "Compile this folder" button.

What it looks like:

    Choose a .jack file, or a folder of .jack files
    /Users/you/jack-compiler/examples
    -----------------------------------------------------------
     <-  .. (parent folder)
     [+] Square/                              [compile 3 files]
      *  HelloWorld.jack
      *  Math.jack
    -----------------------------------------------------------
     [ Compile this folder (5 files) ]   [ Quit ]   ("Back" when opened from a program)

Choosing where to save
----------------------
Ctrl+Shift+S in the window ("save as") opens the same picker with
`purpose=SAVE`: it lists only folders, Enter opens one, and "[save here]"
next to a folder, Ctrl+Enter, or the "Save here" button picks where the
.vm files go. Ctrl+N / "New folder" makes a folder: type its name, Enter
creates and selects it, Esc stops.

Structure
---------
* `list_entries()` and `PickerState` hold all the *logic* (no pygame), so
  they are easy to test.
* `FilePicker` only *draws* the state and turns mouse/keyboard events into
  calls on `PickerState`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from .session import count_jack_files
from .theme import MONO_FONTS

# What the picker can end with:
CHOSEN = "chosen"  # the user picked a file or folder to compile
CANCEL = "cancel"  # the user pressed Esc / Back / Quit (the caller decides which it means)
QUIT = "quit"  # the user closed the window

# What the picker is choosing:
OPEN = "open"  # something to compile (a .jack file or a folder)
SAVE = "save"  # a folder to save the .vm files in


# ---------------------------------------------------------------------------
# Part 1: logic (no pygame)
# ---------------------------------------------------------------------------
NAME_LIMIT = 100  # longest folder name the "New folder" box takes


def folder_name_problem(name: str) -> str:
    """Why `name` can't be a new folder ("" if it can)."""
    if not name:
        return "Type a name for the new folder"
    if "/" in name or "\\" in name or "\0" in name:
        return "A folder name can't contain / or \\"
    if name in (".", ".."):
        return f"{name} isn't a folder name"
    if name.startswith("."):
        return "Names starting with . are hidden here - choose another"
    return ""


@dataclass(frozen=True)
class Entry:
    """One row in the file list."""

    kind: str  # "parent" (the .. row), "folder" or "jack"
    path: Path
    jack_count: int = 0  # for folders: how many .jack files are directly inside

    @property
    def label(self) -> str:
        if self.kind == "parent":
            return "..  (parent folder)"
        if self.kind == "folder":
            return self.path.name + "/"
        return self.path.name


def list_entries(directory: Path, folders_only: bool = False) -> List[Entry]:
    """
    Everything the picker shows for `directory`, in display order:
    the parent folder first, then sub-folders, then .jack files (unless
    `folders_only`). Hidden items (names starting with ".") and other file
    types are skipped.
    """
    entries: List[Entry] = []
    if directory.parent != directory:  # the top of the disk has no parent
        entries.append(Entry("parent", directory.parent))

    folders, jack_files = [], []
    try:
        children = sorted(directory.iterdir(), key=lambda p: p.name.lower())
    except OSError:
        children = []
    for child in children:
        if child.name.startswith("."):
            continue
        try:
            if child.is_dir():
                folders.append(Entry("folder", child, 0 if folders_only else count_jack_files(child)))
            elif child.suffix.lower() == ".jack" and not folders_only:
                jack_files.append(Entry("jack", child))
        except OSError:
            continue  # unreadable item: just leave it out
    return entries + folders + jack_files


class PickerState:
    """
    Remembers which folder we're in and which row is selected, and decides
    what each action does. Every method that can finish the picker returns
    the Path to compile (a .jack file or a folder), or None to keep browsing.

    With `recursive=True`, a folder counts as compilable when it has .jack
    files anywhere below it (like `jackc -r`), not just directly inside.

    With `purpose=SAVE` it chooses a folder to save into: only folders are
    listed, and any folder can be picked (it needn't hold .jack files).
    """

    def __init__(self, directory: Path, recursive: bool = False, purpose: str = OPEN) -> None:
        self.recursive = recursive
        self.purpose = purpose
        self.naming: Optional[str] = None  # the new folder's name while it's being typed (SAVE only)
        self.message = ""  # feedback shown to the user (e.g. an error)
        self.open_folder(directory)

    # --- navigation -------------------------------------------------------
    def open_folder(self, directory: Path) -> None:
        self.directory = Path(directory).expanduser().resolve()
        self.entries = list_entries(self.directory, folders_only=self.purpose == SAVE)
        # Start on the first real item rather than on "..", if there is one.
        self.selected = 1 if len(self.entries) > 1 and self.entries[0].kind == "parent" else 0
        self.message = ""

    def go_up(self) -> None:
        if self.directory.parent != self.directory:
            child = self.directory
            self.open_folder(self.directory.parent)
            # Re-select the folder we just came out of - feels natural.
            for index, entry in enumerate(self.entries):
                if entry.path == child:
                    self.selected = index

    def move(self, delta: int) -> None:
        """Move the selection up (negative) or down (positive)."""
        if self.entries:
            self.selected = max(0, min(len(self.entries) - 1, self.selected + delta))

    # --- choosing ---------------------------------------------------------
    def activate(self, index: Optional[int] = None) -> Optional[Path]:
        """What Enter / a click does: pick a .jack file, or open a folder."""
        if index is not None:
            self.selected = index
        if not self.entries:
            return None
        entry = self.entries[self.selected]
        if entry.kind == "jack":
            return entry.path
        if entry.kind == "parent":
            self.go_up()
        else:
            self.open_folder(entry.path)
        return None

    def compile_folder_entry(self, index: Optional[int] = None) -> Optional[Path]:
        """Pick the selected (or given) folder row as a whole."""
        if index is not None:
            self.selected = index
        if not self.entries:
            return None
        entry = self.entries[self.selected]
        if entry.kind == "jack":
            return entry.path
        if entry.kind == "folder":
            return self._choose_folder(entry.path)
        return self.compile_current_folder()

    def compile_current_folder(self) -> Optional[Path]:
        """Pick the folder we're looking at."""
        return self._choose_folder(self.directory)

    def _choose_folder(self, folder: Path) -> Optional[Path]:
        if self.purpose == SAVE:
            return folder
        if not count_jack_files(folder, self.recursive):
            where = "inside or below" if self.recursive else "directly inside"
            self.message = f"There are no .jack files {where} {folder.name or folder}/"
            return None
        return folder

    # --- "New folder" (save mode): name a folder, then create it -------------
    def start_new_folder(self) -> None:
        """Ctrl+N / the "New folder" button: start typing a name."""
        self.naming = ""
        self.message = ""

    def type_name(self, text: str) -> None:
        if self.naming is not None:
            self.naming = (self.naming + text.replace("\n", "").replace("\r", ""))[:NAME_LIMIT]

    def erase_name(self) -> None:
        if self.naming:
            self.naming = self.naming[:-1]

    def cancel_new_folder(self) -> None:
        self.naming = None
        self.message = ""

    def create_folder(self) -> Optional[Path]:
        """
        Make the typed folder in the folder being shown and select it.
        Returns its path, or None (with self.message saying why; typing goes on).
        An existing folder of that name is simply selected.
        """
        if self.naming is None:
            return None
        name = self.naming.strip()
        problem = folder_name_problem(name)
        folder = self.directory / name
        if not problem and folder.exists() and not folder.is_dir():
            problem = f"There's already a file called {name}"
        if not problem:
            try:
                folder.mkdir(exist_ok=True)
            except OSError as error:
                problem = f"Can't make {name}/: {error.strerror or error}"
        if problem:
            self.message = problem
            return None
        self.naming = None
        self.open_folder(self.directory)  # list it...
        for index, entry in enumerate(self.entries):
            if entry.path == folder:
                self.selected = index  # ...and select it
        return folder

    def current_folder_jack_count(self) -> int:
        return sum(1 for e in self.entries if e.kind == "jack")

    def folder_is_compilable(self, entry: Entry) -> bool:
        """Show a [compile] (or [save here]) button on this folder row?"""
        return entry.kind == "folder" and (entry.jack_count > 0 or self.recursive or self.purpose == SAVE)


# ---------------------------------------------------------------------------
# Part 2: drawing and input (pygame)
# ---------------------------------------------------------------------------
class FilePicker:
    """Shows a PickerState in a pygame window and handles mouse/keyboard."""

    BACKGROUND = (30, 30, 36)
    TEXT = (230, 230, 230)
    DIM = (130, 130, 140)
    TITLE = (120, 190, 255)
    SELECTED_ROW = (60, 70, 100)
    HOVER_ROW = (45, 48, 60)
    ERROR = (255, 110, 110)
    BUTTON = (70, 110, 170)
    BUTTON_DISABLED = (60, 60, 68)

    MARGIN = 16

    def __init__(
        self, surface, start_directory: Path, message: str = "", recursive: bool = False, back_to: str = "",
        purpose: str = OPEN,
    ) -> None:
        import pygame  # imported here so the logic above works without pygame

        self.pygame = pygame
        self.surface = surface
        # Esc / the second button: back to what was open (e.g. "Square/"), or,
        # in the first picker, there's nothing to go back to - so it quits.
        self.back_to = back_to
        self._esc_needs_release = False  # see run()
        self.state = PickerState(start_directory, recursive, purpose)
        self.saving = purpose == SAVE
        self.state.message = message
        self.font = pygame.font.SysFont(MONO_FONTS, 15)
        self.small = pygame.font.SysFont(MONO_FONTS, 13)
        self.row_height = self.font.get_linesize() + 8
        self.scroll = 0  # index of the first visible row
        # Filled in by draw(), used to work out what the mouse clicked on.
        self._row_rects: List[Tuple[object, int, Optional[object]]] = []
        self._compile_button = None
        self._cancel_button = None
        self._new_folder_button = None

    # --- the picker's own little main loop --------------------------------
    def run(self) -> Tuple[str, Optional[Path]]:
        """
        Show the picker until the user decides.
        Returns (CHOSEN, path), (CANCEL, None) or (QUIT, None).
        """
        pygame = self.pygame
        clock = pygame.time.Clock()
        pygame.key.set_repeat(300, 40)  # hold an arrow key to keep moving
        # Opened by HOLDING Esc? Then its key-repeat isn't a request to go back.
        self._esc_needs_release = bool(pygame.key.get_pressed()[pygame.K_ESCAPE])
        try:
            while True:
                for event in pygame.event.get():
                    result = self._handle_event(event)
                    if result is not None:
                        return result
                self.draw()
                pygame.display.flip()
                clock.tick(30)  # a file list doesn't need 60 frames/s
        finally:
            pygame.key.set_repeat()

    def _handle_event(self, event) -> Optional[Tuple[str, Optional[Path]]]:
        pygame = self.pygame
        state = self.state
        chosen: Optional[Path] = None

        if event.type == pygame.QUIT:
            return QUIT, None

        if state.naming is not None and event.type in (pygame.KEYDOWN, pygame.TEXTINPUT):
            return self._naming_event(event)

        if event.type == pygame.KEYDOWN:
            ctrl = event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META)
            if event.key == pygame.K_ESCAPE:
                return None if self._esc_needs_release else (CANCEL, None)
            if ctrl and event.key == pygame.K_q:
                return QUIT, None
            if ctrl and event.key == pygame.K_n and self.saving:
                self._start_new_folder()
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                chosen = state.compile_folder_entry() if ctrl else state.activate()
            elif event.key in (pygame.K_BACKSPACE, pygame.K_LEFT):
                state.go_up()
            elif event.key == pygame.K_RIGHT:
                if state.entries and state.entries[state.selected].kind == "folder":
                    state.activate()
            elif event.key == pygame.K_UP:
                state.move(-1)
            elif event.key == pygame.K_DOWN:
                state.move(+1)
            elif event.key == pygame.K_PAGEUP:
                state.move(-self._visible_rows())
            elif event.key == pygame.K_PAGEDOWN:
                state.move(+self._visible_rows())
            elif event.key == pygame.K_HOME:
                state.move(-len(state.entries))
            elif event.key == pygame.K_END:
                state.move(+len(state.entries))

        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self._esc_needs_release = False

        elif event.type == pygame.MOUSEWHEEL:
            self.scroll = max(0, self.scroll - event.y * 3)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
            if self._cancel_button and self._cancel_button.collidepoint(event.pos):
                return CANCEL, None
            chosen = self._handle_click(event.pos)

        if chosen is not None:
            return CHOSEN, chosen
        return None

    def _start_new_folder(self) -> None:
        self.state.start_new_folder()
        self.pygame.key.start_text_input()  # so typing arrives as TEXTINPUT events

    def _naming_event(self, event) -> Optional[Tuple[str, Optional[Path]]]:
        """Keys while a new folder's name is typed: Enter creates it, Esc stops."""
        pygame, state = self.pygame, self.state
        if event.type == pygame.TEXTINPUT:
            state.type_name(event.text)
            return None
        ctrl = event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META)
        if ctrl and event.key == pygame.K_q:
            return QUIT, None
        if event.key == pygame.K_ESCAPE:
            state.cancel_new_folder()
            self._esc_needs_release = True  # this press isn't also "go back"
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            state.create_folder()
        elif event.key == pygame.K_BACKSPACE:
            state.erase_name()
        return None

    def _handle_click(self, position) -> Optional[Path]:
        """Work out what is under the mouse and do the matching action."""
        if self._new_folder_button and self._new_folder_button.collidepoint(position):
            if self.state.naming is None:
                self._start_new_folder()
            else:
                self.state.create_folder()
            return None
        if self._compile_button and self._compile_button.collidepoint(position):
            return self.state.compile_current_folder()
        for row_rect, index, compile_rect in self._row_rects:
            if compile_rect is not None and compile_rect.collidepoint(position):
                return self.state.compile_folder_entry(index)
            if row_rect.collidepoint(position):
                return self.state.activate(index)
        return None

    # --- drawing ------------------------------------------------------------
    def _list_area(self):
        """The rectangle (x, y, width, height) where rows are drawn."""
        width, height = self.surface.get_size()
        top = self.MARGIN + 3 * self.font.get_linesize() + 14
        bottom = height - self.MARGIN - 44 - self.small.get_linesize() - 10
        return self.pygame.Rect(self.MARGIN, top, width - 2 * self.MARGIN, max(self.row_height, bottom - top))

    def _visible_rows(self) -> int:
        return max(1, self._list_area().height // self.row_height)

    def _keep_selection_visible(self) -> None:
        rows = self._visible_rows()
        selected = self.state.selected
        if selected < self.scroll:
            self.scroll = selected
        elif selected >= self.scroll + rows:
            self.scroll = selected - rows + 1
        self.scroll = max(0, min(self.scroll, max(0, len(self.state.entries) - rows)))

    def _text(self, text, colour, position, font=None) -> None:
        font = font or self.font
        self.surface.blit(font.render(text, True, colour), position)

    def _fit_left(self, text: str, max_width: int, font) -> str:
        """Shorten long paths from the LEFT: '.../projects/Square' keeps the useful end."""
        if font.size(text)[0] <= max_width:
            return text
        while text and font.size("..." + text)[0] > max_width:
            text = text[1:]
        return "..." + text

    def _button(self, rect, label: str, enabled: bool) -> None:
        pygame = self.pygame
        pygame.draw.rect(self.surface, self.BUTTON if enabled else self.BUTTON_DISABLED, rect, border_radius=6)
        image = self.font.render(label, True, self.TEXT if enabled else self.DIM)
        self.surface.blit(image, image.get_rect(center=rect.center))

    @staticmethod
    def _files(count: int) -> str:
        return f"{count} file{'s' if count != 1 else ''}"

    def draw(self) -> None:
        pygame = self.pygame
        surface, state = self.surface, self.state
        width, height = surface.get_size()
        surface.fill(self.BACKGROUND)
        line = self.font.get_linesize()
        x = self.MARGIN

        # Header: title, current folder, message.
        title = "Choose the folder to save the .vm files in" if self.saving else "Choose a .jack file, or a folder of .jack files"
        if state.recursive and not self.saving:
            title += "  (recursive)"
        self._text(title, self.TITLE, (x, self.MARGIN))
        self._text(self._fit_left(str(state.directory), width - 2 * x, self.font), self.TEXT, (x, self.MARGIN + line))
        if state.naming is not None:
            prompt = f"New folder: {state.naming}_"
            self._text(prompt, self.TITLE, (x, self.MARGIN + 2 * line), self.small)
            hint = state.message or "Enter: create   Esc: cancel"
            self._text(hint, self.ERROR if state.message else self.DIM,
                       (x + self.small.size(prompt)[0] + 16, self.MARGIN + 2 * line), self.small)  # fmt: skip
        elif state.message:
            self._text(state.message, self.ERROR, (x, self.MARGIN + 2 * line), self.small)

        # The list of entries (only the rows that fit).
        area = self._list_area()
        pygame.draw.line(surface, self.DIM, (area.left, area.top - 4), (area.right, area.top - 4))
        self._keep_selection_visible()
        mouse = pygame.mouse.get_pos()
        self._row_rects = []
        visible = state.entries[self.scroll : self.scroll + self._visible_rows()]
        for offset, entry in enumerate(visible):
            index = self.scroll + offset
            row = pygame.Rect(area.left, area.top + offset * self.row_height, area.width, self.row_height)
            if index == state.selected:
                pygame.draw.rect(surface, self.SELECTED_ROW, row, border_radius=4)
            elif row.collidepoint(mouse):
                pygame.draw.rect(surface, self.HOVER_ROW, row, border_radius=4)

            icon = {"parent": "<- ", "folder": "[+]", "jack": " * "}[entry.kind]
            colour = self.TEXT if entry.kind != "folder" or state.folder_is_compilable(entry) else self.DIM
            self._text(f"{icon} {entry.label}", colour, (row.left + 8, row.top + 4))

            compile_rect = None
            if state.folder_is_compilable(entry):
                if self.saving:
                    label = "[save here]"
                else:
                    label = f"[compile {self._files(entry.jack_count)}]" if entry.jack_count else "[compile tree]"
                image = self.font.render(label, True, self.TITLE)
                compile_rect = image.get_rect(right=row.right - 8, top=row.top + 4)
                surface.blit(image, compile_rect)
            self._row_rects.append((row, index, compile_rect))

        if not state.entries:
            self._text("(this folder is empty)", self.DIM, (area.left + 8, area.top + 4))
        if len(state.entries) > self._visible_rows():
            shown = f"{self.scroll + 1}-{self.scroll + len(visible)} of {len(state.entries)}"
            self._text(shown, self.DIM, (area.right - self.small.size(shown)[0], area.bottom + 2), self.small)

        # Footer: help text and buttons.
        help_y = height - self.MARGIN - 44 - self.small.get_linesize() - 4
        pygame.draw.line(surface, self.DIM, (area.left, help_y - 4), (area.right, help_y - 4))
        back_to = self.back_to if len(self.back_to) <= 20 else self.back_to[:19] + "…"
        esc = f"Esc: back to {back_to}" if self.back_to else "Esc: quit"
        if self.saving:  # (Esc always goes back here: the chooser opens from a program)
            keys = "Enter: open   Ctrl+Enter: save in folder   Ctrl+N: new folder   Backspace: up   Esc: back"
        else:
            keys = f"Enter: open   Ctrl+Enter: compile folder   Backspace: up   {esc}   Ctrl+Q: quit"
        self._text(keys, self.DIM, (x, help_y), self.small)
        count = state.current_folder_jack_count()
        enabled = count > 0 or state.recursive or self.saving
        if self.saving:
            label = "Save here"
        else:
            label = f"Compile this folder ({self._files(count)})" if count else "Compile this folder"
        self._compile_button = pygame.Rect(x, height - self.MARGIN - 40, max(300, self.font.size(label)[0] + 30), 40)
        self._cancel_button = pygame.Rect(self._compile_button.right + 12, self._compile_button.top, 120, 40)
        self._button(self._compile_button, label, enabled=enabled)
        self._button(self._cancel_button, "Back" if self.back_to else "Quit", enabled=True)
        self._new_folder_button = None
        if self.saving:
            label = "Create" if state.naming is not None else "New folder"
            self._new_folder_button = pygame.Rect(self._cancel_button.right + 12, self._cancel_button.top, 140, 40)
            self._button(self._new_folder_button, label, enabled=True)
