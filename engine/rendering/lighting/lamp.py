"""Implements a simple light source."""
from dataclasses import dataclass
import glm

__all__ = ["Lamp"]


@dataclass(frozen=True)
class Lamp(Component):  # pylint: disable=too-few-public-methods
    """Do something."""

    position: glm.vec3
    ambient: glm.vec3
    diffuse: glm.vec3
    specular: glm.vec3
