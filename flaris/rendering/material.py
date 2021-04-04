from dataclasses import dataclass

import glm

from flaris.component import Component

from .color import Color
from .texture import Texture


@dataclass
class Material(Component):
    albedo: Color = Color(1, 1, 1)
    shininess: float = 32.0
    
    @property
    def ambient(self):
        return self.entity[Texture].name

    @property
    def diffuse(self):
        return self.entity[Texture].name
        
