"""Implements the `Light` class."""
from flaris.entity import Entity
from flaris.transform import Vector

__all__ = ["Light"]


class Light(Entity):  # pylint: disable=too-few-public-methods
    """A simple directional light source."""

    def __init__(self, position: Vector, ambient: Vector, diffuse: Vector,
                 specular: Vector):
        """Initialize the light's position and attributes."""
        super().__init__()
        self._position = position
        self._ambient = ambient
        self._diffuse = diffuse
        self._specular = specular

    @property
    def position(self) -> Vector:
        """Return the position of the `Light`."""
        return self._position

    @property
    def ambient(self) -> Vector:
        """Return the ambient value of the `Light`."""
        return self._ambient

    @property
    def diffuse(self) -> Vector:
        """Return the diffuse value of the `Light`."""
        return self._diffuse

    @property
    def specular(self) -> Vector:
        """Return the specular value of the `Light`."""
        return self._specular
