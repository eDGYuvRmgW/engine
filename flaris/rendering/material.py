"""Implements the `Material` class."""
from dataclasses import dataclass

from flaris.component import Component

from .color import Color
from .texture import Texture

__all__ = ["Material"]


@dataclass
class Material(Component):
    """An abstraction that specifies how a model should be shaded.

    Attributes:
        albedo: A Color representing the base color of a model.
        shininess: A float that determines the amount of specular effects.
    """
    albedo: Color = Color(1, 1, 1)
    shininess: float = 32.0

    @property
    def ambient(self):
        """Return a texture specifying the ambient coefficients."""
        return self.entity[Texture].name

    @property
    def diffuse(self):
        """Return a texture specifying the diffuse coefficients."""
        return self.entity[Texture].name
