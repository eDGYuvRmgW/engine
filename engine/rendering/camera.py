"""Implements the `Camera` class."""
import glfw
import glm

from engine import Entity
from engine.transform import Transform

__all__ = ["Camera"]


class Camera(Entity):  # pylint: disable=too-few-public-methods
    """An object representing the game's `Camera`."""

    def __init__(self, transform: Transform):
        """Initialize `Camera` attributes.

        Components:
            transform: The transform of the `Camera` object.
        """
        super().__init__()
        self.transform = transform

    @property
    def view(self) -> glm.mat4:
        """Return the `Camera` view matrix."""
        position = glm.vec3(self.transform.x, self.transform.y,
                            self.transform.z)
        front = glm.vec3(0.0, 0.0, -1.0)
        upwards = glm.vec3(0.0, 1.0, 0.0)
        return glm.lookAt(position, position + front, upwards)

    @property
    def projection(self):
        """Return the `Camera` projection matrix."""
        window = glfw.get_current_context()
        window_width, window_height = glfw.get_window_size(window)
        return glm.ortho(0.0, window_width, 0.0, window_height, -100.0, 100.0)
