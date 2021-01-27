"""Implements the `Mesh` class."""
from dataclasses import dataclass

from engine.component import Component

__all__ = ["Mesh"]


@dataclass(frozen=True)
class Mesh(Component):
    """Encapsulates a mesh.

    Placeholder until model loading is implemented.
    """
