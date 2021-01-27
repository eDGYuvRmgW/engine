"""Implements input handling.

Example:
    >>> from framework.inputs import key
    >>> if key.is_down(key.UP):
    ...     print("Up arrow pressed!")
"""
from . import key  # noqa: F401
from .systems import *  # noqa: F401,F403
