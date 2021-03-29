"""Implements the `Component` class and the `ComponentError` exception."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flaris.entity import Entity

__all__ = ["Component", "ComponentError"]


class Component:  # pylint: disable=too-few-public-methods
    """Raw data for one aspect of an entity."""

    @property
    def entity(self) -> Entity:
        """Return the entity that this component is attached to."""
        if not hasattr(self, "_entity"):
            self._entity = None
        return self._entity

    @entity.setter
    def entity(self, value) -> None:
        """Set the entity that this component is attached to."""
        self._entity = value


class ComponentError(Exception):
    """An exception raised when an entity lacks an expected component."""
