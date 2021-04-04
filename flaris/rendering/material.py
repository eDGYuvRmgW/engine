from dataclasses import dataclass

import glm

from flaris.component import Component

from .color import Color


@dataclass
class Material(Component):
    albedo: Color = Color(1, 1, 1)
    shininess: float = 32.0

    def __post_init__(self):
        self.ambient = glm.vec3(self.albedo.red, self.albedo.green, self.albedo.blue)
        self.diffuse = glm.vec3(self.albedo.red, self.albedo.green, self.albedo.blue)
