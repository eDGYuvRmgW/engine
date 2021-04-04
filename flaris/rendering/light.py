"""Implements the `Light` class."""
from dataclasses import dataclass

import glm

from flaris.entity import Component

from .color import Color

__all__ = ["Light", "DirectionalLight", "AmbientLight"]


class Light(Component):
    pass

@dataclass
class DirectionalLight(Light):  # pylint: disable=too-few-public-methods
    color: Color = Color(1, 1, 1)
    intensity: float = 1

    def __post_init__(self):
        self.ambient = glm.vec3(0, 0, 0)
        self.diffuse = glm.vec3(self.color.red, self.color.green, self.color.blue) * self.intensity


@dataclass
class AmbientLight(Light):  # pylint: disable=too-few-public-methods
    color: Color = Color(1, 1, 1)
    intensity: float = 0.25

    def __post_init__(self):
        self.ambient = glm.vec3(self.color.red, self.color.green, self.color.blue) * self.intensity
        self.diffuse = glm.vec3(0, 0, 0)
