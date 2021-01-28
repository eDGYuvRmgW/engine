"""Implements functions for detecting keyboard input."""
import collections

import glfw

from engine.system import System

__all__ = ["UP", "DOWN", "LEFT", "RIGHT", "ENTER", "is_down", "is_pressed"]

_STATE = collections.defaultdict(lambda: glfw.RELEASE)
_OLD_STATE = collections.defaultdict(lambda: glfw.RELEASE)

UP = glfw.KEY_UP
DOWN = glfw.KEY_DOWN
LEFT = glfw.KEY_LEFT
RIGHT = glfw.KEY_RIGHT
ENTER = glfw.KEY_ENTER


def key_callback(  # pylint: disable=unused-argument
        window, key: int, scancode: int, action: int, mods: int) -> None:
    """Update the internal state on key press.

    See https://www.glfw.org/docs/3.3/input_guide.html#input_key.
    """
    _STATE[key] = action


class KeyboardHandlingSystem(System):
    """System that checks for keyboard input."""

    def start(self) -> None:
        """Get reference to window and set callback function."""
        self.window = glfw.get_current_context()
        glfw.set_key_callback(self.window, key_callback)

    def step(self, delta: float) -> None:
        """Store old states on each frame and update poll events."""
        for key in _STATE:
            _OLD_STATE[key] = _STATE[key]
        glfw.poll_events()


def is_down(key: int) -> bool:
    """Return true if the key is currently pressed.

    Args:
        key: A keyboard key.

    Returns:
        True if the key is pressed and false otherwise.
    """
    return _STATE[key] == glfw.PRESS or _STATE[key] == glfw.REPEAT


def is_pressed(key: int) -> bool:
    """Return true if the key was pressed on the current frame.

    Args:
        key: A keyboard key.

    Returns:
        True if the key was pressed and false otherwise.
    """
    return _STATE[key] == glfw.PRESS and _OLD_STATE[key] == glfw.RELEASE
