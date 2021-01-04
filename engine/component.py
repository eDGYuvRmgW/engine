"""Implements the `Component` class and the `ComponentError` exception."""

__all__ = ["Component", "ComponentError"]


class Component:
    """Raw data for one aspect of an entity."""


class ComponentError(Exception):
    """An exception raised when an entity lacks an expected component."""
