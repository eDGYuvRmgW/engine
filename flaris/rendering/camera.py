"""Implements the `Camera` class."""
from dataclasses import dataclass
import math

import glfw
import glm
import OpenGL.GL as gl

from flaris import Entity
from flaris.component import Component
from flaris.transform import Transform

from .color import Color

__all__ = ["Camera", "OrthographicCamera"]


class Camera(Component):

    @property
    def view(self) -> glm.mat4:
        raise NotImplementedError

    @property
    def projection(self) -> glm.mat4:
        raise NotImplementedError


@dataclass
class OrthographicCamera(Camera):

    background: Color = Color(1, 0, 0)
    size: float = 5
    near: float = 0.001
    far: float = 10000

    @property
    def view(self) -> glm.mat4:
        """Return the `Camera` view matrix."""
        position = glm.vec3(self.entity.transform.position.x,
                            self.entity.transform.position.y,
                            self.entity.transform.position.z)
        front = glm.vec3(0.0, 0.0, -1.0)
        upwards = glm.vec3(0.0, 1.0, 0.0)
        angles = self.entity.transform.rotation * math.pi / 180
        rotation = glm.quat(glm.vec3(angles.x, angles.y, angles.z))
        return glm.lookAt(position, position + rotation * front,
                          rotation * upwards)

    @property
    def projection(self) -> glm.mat4:
        """Return the `Camera` projection matrix."""
        window = glfw.get_current_context()
        width, height = glfw.get_window_size(window)
        left, right = -width / height * self.size, width / height * self.size
        bottom, top = -1 * self.size, 1 * self.size
        return glm.ortho(left, right, bottom, top, self.near, self.far)
