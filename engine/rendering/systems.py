import glfw
import OpenGL.GL as gl

from engine.system import System, PipelinedSystem
from engine.transform import Transform

from .sprite import Sprite
from .text import Text
from .renderers import SpriteRenderer, TextRenderer


class RenderingSystem(PipelinedSystem):

    def __init__(self):
        super().__init__([
            WindowClearSystem(),
            TextRenderingSystem(),
            SpriteRenderingSystem(),
            BufferSwapSystem()
        ])


class WindowClearSystem(System):

    def step(self, delta: float) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)


class TextRenderingSystem(System):

    REQUIRED_COMPONENTS = Transform, Text

    def start(self) -> None:
        self.renderer = TextRenderer()

    def step(self, delta: float) -> None:
        for entity in self.entities:
            self.renderer.draw(entity[Text], entity[Transform])


class SpriteRenderingSystem(System):

    REQUIRED_COMPONENTS = Transform, Sprite

    def start(self) -> None:
        self.renderer = SpriteRenderer()

    def step(self, delta: float) -> None:
        for entity in self.entities:
            self.renderer.draw(entity[Sprite], entity[Transform])


class BufferSwapSystem(System):

    def start(self) -> None:
        self.window = glfw.get_current_context()

    def step(self, delta: float) -> None:
        glfw.swap_buffers(self.window)
