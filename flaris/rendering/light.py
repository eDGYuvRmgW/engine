"""Implements the `Light` class."""
from dataclasses import dataclass

import glm

from flaris.entity import Component

from .color import Color

__all__ = ["Light", "DirectionalLight", "AmbientLight"]


class Light(Component):

    @property
    def ambient(self) -> glm.vec3:
        raise NotImplementedError

    @property
    def diffuse(self) -> glm.vec3:
        raise NotImplementedError


@dataclass
class DirectionalLight(Light):  # pylint: disable=too-few-public-methods
    color: Color = Color(1, 1, 1)
    intensity: float = 1

    @property
    def ambient(self) -> glm.vec3:
        return glm.vec3(0, 0, 0)

    @property
    def diffuse(self) -> glm.vec3:
        return glm.vec3(self.color.red, self.color.green,
                        self.color.blue) * self.intensity


@dataclass
class AmbientLight(Light):  # pylint: disable=too-few-public-methods
    color: Color = Color(1, 1, 1)
    intensity: float = 0.25

    @property
    def ambient(self) -> glm.vec3:
        return glm.vec3(self.color.red, self.color.green,
                        self.color.blue) * self.intensity

    @property
    def diffuse(self) -> glm.vec3:
        return glm.vec3(0, 0, 0)
