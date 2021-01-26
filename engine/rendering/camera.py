"""Implements the camera class."""
import glm

__all__ = ["Camera"]


class Camera: # pylint: disable=too-few-public-methods
    """An object representing the game's camera."""

    def __init__(self):
        """Initialize camera attributes."""
        self.camera_pos = glm.vec3(0.0, 0.0, 3.0)
        self.camera_front = glm.vec3(0.0, 0.0, -1.0)
        self.camera_up = glm.vec3(0.0, 1.0, 0.0)

    def get_view(self) -> glm.mat4:
        """Return the camera's view matrix."""
        return glm.lookAt(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def get_position(self) -> glm.vec3:
        """Return the camera's position."""
        return self.camera_pos
