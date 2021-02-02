"""Implements a simple `Light` source."""
from dataclasses import dataclass

from engine import Component, Transform, Vector

__all__ = ["Light"]


@dataclass(frozen=True)
class Light(Component):  # pylint: disable=too-few-public-methods
    """Describes the `Light` position, ambient, diffuse, and specular attributes.
    
    Attributes:
        position: The position of the `Light.
        ambient: The ambient component of the `Light`.
        diffuse: The diffuse component of the `Light`.
        specular: The specular component of the `Light`.
    """
    position: Transform
    ambient: Vector
    diffuse: Vector
    specular: Vector
