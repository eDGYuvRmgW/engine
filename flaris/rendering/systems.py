"""Implements rendering-related classes that subclass `System`."""
import glfw
import OpenGL.GL as gl

from flaris.entity import Entity

from flaris.system import System, SequentialSystem
from flaris.transform import Transform

from .camera import Camera
from .light import Light
from .sprite import Sprite
from .text import Text
from .renderers import MeshRenderer, SpriteRenderer, TextRenderer


class RenderingSystem(SequentialSystem):
    """System that renders objects in a scene."""

    def __init__(self):
        """Construct and pipeline the systems needed to render a scene."""
        super().__init__([
            WindowClearSystem(),
            MeshRenderingSystem(),
            TextRenderingSystem(),
            SpriteRenderingSystem(),
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

    def __init__(self):
        """Initialize camera field for the system."""
        super().__init__()
        self.camera = None
        self.light = None

    def start(self) -> None:
        """Construct a mesh renderer."""
        if self.camera is None:
            raise RuntimeError(
                "A Camera object must be added to initialize the MeshRenderer.")

        if self.light is None:
            raise RuntimeError(
                "A directional Light object must be added to initialize the MeshRenderer."
            )

        self.renderer = MeshRenderer(self.camera, self.light)

    def step(self, delta: float) -> None:
        """Render each mesh in the scene."""
        for entity in self.entities:
            self.renderer.draw(entity[Transform])

    def add(self, entity: Entity) -> None:
        """Add an entity to the scene."""
        if isinstance(entity, Camera) and not self.camera:
            self.camera = entity
            return

        if isinstance(entity, Camera) and self.camera:
            raise ValueError("MeshRenderer already has a Camera attached.")

        if isinstance(entity, Light):
            self.light = entity
            return

        super().add(entity)

    def remove(self, entity: Entity) -> None:
        """Remove an entity from the scene."""
        if entity is self.camera:
            raise ValueError(
                "Cannot remove a Camera attached to the current MeshRenderer.")

        if entity is self.light:
            raise ValueError(
                "Cannot remove directional light source from the MeshRenderer.")

        super().remove(entity)


class BufferSwapSystem(System):
    """System that swaps buffers."""

    def start(self) -> None:
        """Get a reference to the window."""
        self.window = glfw.get_current_context()

    def step(self, delta: float) -> None:
        """Swap buffers."""
        glfw.swap_buffers(self.window)
