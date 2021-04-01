"""Implements rendering-related classes that subclass `System`."""
import glfw
import OpenGL.GL as gl

from flaris.entity import Entity

from flaris.system import System, SequentialSystem
from flaris.transform import Transform

from .camera import OrthographicCamera
from .mesh import Mesh
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

    REQUIRED_COMPONENTS = Transform, Mesh

    def __init__(self):
        """Initialize the scene."""
        super().__init__()
        self.camera = None
        self.renderer = None

    def start(self) -> None:
        self.renderer = MeshRenderer(self.camera)

    def step(self, delta: float) -> None:
        """Render each mesh in the scene."""
        for entity in self.entities:
            self.renderer.draw(entity[Mesh], entity[Transform])

    def add(self, entity: Entity) -> None:
        """Add an entity to the scene."""
        # TODO: Add inheritance for component keys
        if OrthographicCamera in entity and not self.camera:
            self.camera = entity[OrthographicCamera]

        super().add(entity)


class BufferSwapSystem(System):
    """System that swaps buffers."""

    def start(self) -> None:
        """Get a reference to the window."""
        self.window = glfw.get_current_context()

    def step(self, delta: float) -> None:
        """Swap buffers."""
        glfw.swap_buffers(self.window)
