"""Implements the `Camera` class."""
from dataclasses import dataclass
import math

import glfw
import glm

from flaris.component import Component, ComponentError
from flaris.transform import Transform

__all__ = ["Camera", "OrthographicCamera"]


class Camera(Component):
    """Base class for cameras."""

    @property
    def view(self) -> glm.mat4:
        """Return the camera view matrix."""
        if not self.entity or Transform not in self.entity:
            raise ComponentError(
                "Expected camera to be attached to an entity with a transform "
                "component.")

        position = glm.vec3(self.entity.transform.position.x,
                            self.entity.transform.position.y,
                            self.entity.transform.position.z)
        front = glm.vec3(0.0, 0.0, -1.0)
        upwards = glm.vec3(0.0, 1.0, 0.0)
        angles = self.entity[Transform].rotation * math.pi / 180
        rotation = glm.quat(glm.vec3(angles.x, angles.y, angles.z))
        return glm.lookAt(position, position + rotation * front,
                          rotation * upwards)

    @property
    def projection(self) -> glm.mat4:
        """Return a projection matrix."""
        raise NotImplementedError


@dataclass
class OrthographicCamera(Camera):
    """An orthographic camera.

    Attributes:
        size: A float specifying the height of the screen in Flaris units.
        near: A float specifying the near clipping plane.
        far: A float specifying the far clipping plane.
    """

    size: float = 10
    near: float = 0.001
    far: float = 10000

    @property
    def projection(self) -> glm.mat4:
        """Return an orthographic projection matrix."""
        window = glfw.get_current_context()
        width, height = glfw.get_window_size(window)
        aspect_ratio = width / height
        left, right = (-aspect_ratio * self.size / 2,
                       aspect_ratio * self.size / 2)
        bottom, top = -self.size / 2, self.size / 2
        return glm.ortho(left, right, bottom, top, self.near, self.far)
