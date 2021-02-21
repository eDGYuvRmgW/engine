"""Implements the `Scene` class."""
from typing import Iterator

from .camera import Camera
from .light import Light

__all__ = ["Scene"]


class Scene():  # pylint: disable=too-few-public-methods
    """A collection of objects to be rendered."""

    def __init__(self, camera: Camera):
        """Initialize the scene's camera and directional light."""
        self._camera = camera
        self._lights = []

    def add(self, component: Light) -> None:
        """Add a component to the scene."""
        if component is Light:
            self._lights.append(component)

    @property
    def camera(self) -> Camera:
        """Return the camera in this scene."""
        return self._camera

    @property
    def lights(self) -> Iterator[Light]
        """Return a list of lights in this scene."""
        return self._lights