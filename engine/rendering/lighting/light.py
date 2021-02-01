"""Implements a simple Light source."""
from dataclasses import dataclass
import glm

from engine import Component

__all__ = ["Light"]


@dataclass(frozen=True)
class Light(Component):  # pylint: disable=too-few-public-methods
    """Describes the Light's position, ambient, diffuse, and specular attributes."""
    position: glm.vec3
    ambient: glm.vec3
    diffuse: glm.vec3
    specular: glm.vec3
