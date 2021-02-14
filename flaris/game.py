"""Implements the `Game` class."""
from __future__ import annotations

from timeit import default_timer as timer
from typing import Optional, TYPE_CHECKING

from .system import SequentialSystem, UpdateSystem
from .rendering import Window, RenderingSystem
from .inputs import InputSystem

if TYPE_CHECKING:
    from .rendering import Icon

__all__ = ["Game"]


class Game(SequentialSystem):
    """Base class for all games."""

    _HAS_DYNAMIC_ATTRIBUTES = True

    def __init__(self, name: str, icon: Optional[Icon] = None):
        """Initialize the game.

        Args:
            name: The title of the game.
            icon: The window icon (default: None).
        """
        super().__init__([InputSystem(), UpdateSystem(), RenderingSystem()])
        self.name = name
        self.icon = icon

    def run(self, width: int, height: int) -> None:
        """Run the game.

        Args:
            width: The width of the window.
            height: The height of the window.
        """
        with Window(self.name, width, height, self.icon) as window:
            self.start()

            delta = 0
            while not window.should_close:
                start_time = timer()
                self.step(delta)
                end_time = timer()
                delta = end_time - start_time

            self.exit()
