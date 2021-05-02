"""Implements the `Light` class."""
from dataclasses import dataclass

import glm

from flaris.entity import Component

from .color import Color

__all__ = ["Light", "DirectionalLight", "AmbientLight"]


class Light(Component):
    """Base class for all lights."""

    @property
    def ambient(self) -> glm.vec3:
        """Return a vector reprsenting the color of ambient light."""
        raise NotImplementedError

    @property
    def diffuse(self) -> glm.vec3:
        """Return a vector representing the color of diffuse light."""
        raise NotImplementedError


@dataclass
class DirectionalLight(Light):  # pylint: disable=too-few-public-methods
    """A directional light.
    
    Attributes:
        color: A Color representing the color of the light.
        intensity: A float representing the intensity of the light.
    """

    color: Color = Color(1, 1, 1)
    intensity: float = 1

    @property
    def ambient(self) -> glm.vec3:
        """Return a vector reprsenting the color of ambient light."""
        return glm.vec3(0, 0, 0)

    @property
    def diffuse(self) -> glm.vec3:
        """Return a vector representing the color of diffuse light."""
        return glm.vec3(self.color.red, self.color.green,
                        self.color.blue) * self.intensity


@dataclass
class AmbientLight(Light):  # pylint: disable=too-few-public-methods
    """An ambient light.
    
    Attributes:
        color: A Color representing the color of the light.
        intensity: A float representing the intensity of the light.
    """

    color: Color = Color(1, 1, 1)
    intensity: float = 0.25

    @property
    def ambient(self) -> glm.vec3:
        """Return a vector reprsenting the color of ambient light."""
        return glm.vec3(self.color.red, self.color.green,
                        self.color.blue) * self.intensity

    @property
    def diffuse(self) -> glm.vec3:
        """Return a vector representing the color of diffuse light."""
        return glm.vec3(0, 0, 0)
