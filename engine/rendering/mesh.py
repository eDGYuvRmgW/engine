"""Implements the `Mesh` class."""
from dataclasses import dataclass

from engine.component import Component

from .color import Color
from .texture import Texture

__all__ = ["Mesh"]


@dataclass(frozen=True)
class Mesh(Component):
    """Encapsulates a mesh.

    Attributes:
        texture: The mesh's texture.
        color: The mesh's color.
    """

    color: Color = Color(1.0, 1.0, 1.0)
