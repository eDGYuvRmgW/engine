"""Implements the `Mesh` class."""
from flaris.component import Component

__all__ = ["Mesh"]


class Mesh(Component):
    """A collection of primitives defining three-dimensional geometry."""

    def __init__(self, path: str):
        """Initialize instance attributes.

        Arguments:
            path: Path to a COLLADA model.
        """
        raise NotImplementedError