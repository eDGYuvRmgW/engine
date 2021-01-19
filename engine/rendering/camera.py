"""Implements the camera class."""
import glm

__all__ = ["Camera"]


class Camera: # pylint: disable=too-few-public-methods
    """An object representing the game's camera."""

    def __init__(self):
        """Do something."""
        camera_pos = glm.vec3(0.0, 0.0, 3.0)

        camera_target = glm.vec3(0.0, 0.0, 0.0)
        camera_direction = glm.normalize(camera_pos - camera_target)

        up_vector = glm.vec3(0.0, 1.0, 0.0)
        camera_right = glm.normalize(glm.cross(up_vector, camera_direction))

        camera_up = glm.cross(camera_direction, camera_right)

        self.view = glm.lookAt(glm.vec3(0.0, 0.0, 3.0),
                          glm.vec3(0.0, 0.0, 0.0),
                          glm.vec3(0.0, 1.0, 0.0))

    def get_view(self) -> glm.mat4:
        """Return the camera's view matrix."""
        return self.view
