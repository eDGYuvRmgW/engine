"""Implements rendering-related classes that subclass `System`."""
import glfw
import OpenGL.GL as gl

from engine.system import System, PipelinedSystem
from engine.transform import Transform

from .camera import Camera
from .lighting import Lamp
from .sprite import Sprite
from .text import Text
from .renderers import MeshRenderer, SpriteRenderer, TextRenderer


class RenderingSystem(PipelinedSystem):
    """System that renders objects in a scene."""

    def __init__(self):
        """Construct and pipeline the systems needed to render a scene."""
        self.camera = Camera()

        super().__init__([
            WindowClearSystem(),
            TextRenderingSystem(),
            SpriteRenderingSystem(),
            MeshRenderingSystem(self.camera.get_view()),
            LightSystem(self.camera.get_view()),
            BufferSwapSystem()
        ])


class WindowClearSystem(System):
    """System that clears the pixels on the screen."""

    def step(self, delta: float) -> None:
        """Clear the pixels on the screen."""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


class TextRenderingSystem(System):
    """System that renders text."""

    REQUIRED_COMPONENTS = Transform, Text

    def start(self) -> None:
        """Construct a text renderer."""
        self.renderer = TextRenderer()

    def step(self, delta: float) -> None:
        """Render text in the scene."""
        for entity in self.entities:
            self.renderer.draw(entity[Text], entity[Transform])


class SpriteRenderingSystem(System):
    """System that renders sprite."""

    REQUIRED_COMPONENTS = Transform, Sprite

    def start(self) -> None:
        """Construct a sprite renderer."""
        self.renderer = SpriteRenderer()

    def step(self, delta: float) -> None:
        """Render each sprite in the scene."""
        for entity in self.entities:
            self.renderer.draw(entity[Sprite], entity[Transform])


class MeshRenderingSystem(System):
    """System that renders a mesh."""

    def __init__(self, view):
        """Do something."""
        self.view = view

    def start(self) -> None:
        """Construct a mesh renderer."""
        self.renderer = MeshRenderer()

    def step(self, delta: float) -> None:
        """Render each mesh in the scene."""
        self.renderer.draw(self.view)


class LightSystem(System):
    """System that renders a light."""

    def __init__(self, view):
        """Do something."""
        self.view = view

    def start(self) -> None:
        """Construct a lamp."""
        self.renderer = Lamp()

    def step(self, delta: float) -> None:
        """Render each lamp in the scene."""
        self.renderer.draw(self.view)


class BufferSwapSystem(System):
    """System that swaps buffers."""

    def start(self) -> None:
        """Get a reference to the window."""
        self.window = glfw.get_current_context()

    def step(self, delta: float) -> None:
        """Swap buffers."""
        glfw.swap_buffers(self.window)
