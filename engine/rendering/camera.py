"""Implements the camera class."""
import glm
import glfw

from engine import Entity
from engine.transform import Transform

__all__ = ["Camera"]


class Camera(Entity): # pylint: disable=too-few-public-methods
    """An object representing the game's Camera."""

    def __init__(self, transform: Transform):
        """Initialize Camera attributes."""
        self.transform = transform

    @property
    def view(self) -> glm.mat4:
        """Return the Camera's view matrix."""
        position = glm.vec3(self.transform.x, self.transform.y, self.transform.z)
        front = glm.vec3(0.0, 0.0, -1.0)
        up = glm.vec3(0.0, 1.0, 0.0)
        return glm.lookAt(position, position + front, up)

    @property
    def projection(self):
        """Return the Camera's projection matrix."""
        window = glfw.get_current_context()
        window_width, window_height = glfw.get_window_size(window)
        return glm.ortho(0.0, window_width, 0.0, window_height, -100.0, 100.0)

    @property
    def position(self) -> glm.vec3:
        """Return the Camera's position."""
        return self.camera_pos
