"""Implements the `Component` class and the `ComponentError` exception."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flaris.entity import Entity

__all__ = ["Component", "ComponentError"]


class Component:  # pylint: disable=too-few-public-methods
    """Raw data for one aspect of an entity."""

    def __init__(self):
        self._entity = None

    @property
    def entity(self) -> Entity:
        if not hasattr(self, "_entity"):
            raise AttributeError("Cannot attach component before"
                                 "Component.__init__() call.")
        return self._entity

    @entity.setter
    def entity(self, value) -> None:
        if not hasattr(self, "_entity"):
            raise AttributeError("Cannot attach component before"
                                 "Component.__init__() call.")
        self._entity = value


class ComponentError(Exception):
    """An exception raised when an entity lacks an expected component."""
