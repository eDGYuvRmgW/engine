"""Implements the `Light` class."""
from dataclasses import dataclass

from flaris.entity import Component
from flaris.transform import Vector

__all__ = ["Light"]


@dataclass
class Light(Component):  # pylint: disable=too-few-public-methods
    """A simple light source.

    Attributes:
        position: The position of the `Light`.
        ambient: The ambient value of the `Light`.
        diffuse: The diffuse value of the `Light`.
        specular: The specular value of the `Light`.
    """

    position: Vector
    ambient: Vector = Vector(0.2, 0.2, 0.2)
    diffuse: Vector = Vector(0.5, 0.5, 0.5)
    specular: Vector = Vector(1.0, 1.0, 1.0)
