"""Implements the `InputSystem` class."""
from flaris.system import PipelinedSystem

from .key import KeyboardHandlingSystem

__all__ = ["InputSystem"]


class InputSystem(PipelinedSystem):
    """A system that checks for user input."""

    def __init__(self):
        """Construct and pipeline the systems needed to check for user input."""
        super().__init__([KeyboardHandlingSystem()])
