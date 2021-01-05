"""Implements the `Sprite` class."""
from dataclasses import dataclass

from engine.component import Component

from .color import Color
from .texture import Texture

__all__ = ["Sprite"]


@dataclass(frozen=True)
class Sprite(Component):
    """Encapsulates a sprite.

    Attributes:
        texture: The sprite's texture.
        color: The sprite's color.
    """

    texture: Texture
    color: Color = Color(1.0, 1.0, 1.0)
