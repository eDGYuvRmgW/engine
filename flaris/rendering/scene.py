"""Implements the `Scene` class."""
from typing import List

from .camera import Camera
from .light import Light

__all__ = ["Scene"]


class Scene():  # pylint: disable=too-few-public-methods
    """A collection of objects to be rendered."""

    def __init__(self):
        """Initialize the scene's camera and lights."""
        self._camera = None
        self._lights = []

    def add(self, component: Light) -> None:
        """Add a component to the scene."""
        if isinstance(component, Light):
            self._lights.append(component)

    @property
    def camera(self) -> Camera:
        """Return the camera in this scene."""
        return self._camera

    @camera.setter
    def camera(self, camera: Camera):
        """Assign a camera to the scene."""
        self._camera = camera

    @property
    def lights(self) -> List[Light]:
        """Return a list of lights in this scene."""
        return self._lights
