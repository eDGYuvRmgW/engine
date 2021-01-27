"""Implements the Window class."""
from typing import Optional

import glfw
import OpenGL.GL as gl

from framework.rendering.icon import Icon

__all__ = ["Window"]


class Window:  # pylint: disable=too-few-public-methods
    """An object that encapsulates both a window and a context."""

    def __init__(self, name, width, height, icon: Optional[Icon] = None):
        """Open a window.

        Args:
            name: The title of the window.
            width: The width of the window.
            height: The height of the window.
            icon: The window icon. If no icon is provided, then the default icon
                for the operating system is used (default: None).
        """
        self.name = name
        self.width = width
        self.height = height
        self.icon = icon

        self.window = None
        self.shader = None

    def __enter__(self):
        """Do something."""
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW.")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(self.width, self.height, self.name,
                                         None, None)

        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create window.")

        if self.icon:
            glfw.set_window_icon(self.window, len(self.icon.images),
                                 self.icon.images)

        glfw.make_context_current(self.window)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        glfw.set_framebuffer_size_callback(self.window,
                                           framebuffer_size_callback)

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Do something."""
        glfw.terminate()

    @property
    def should_close(self) -> bool:
        """Do something."""
        return glfw.window_should_close(self.window)


def framebuffer_size_callback(window, width: int, height: int) -> None:  # noqa: E501  # pylint: disable=unused-argument
    """Update the OpenGL viewport.

    Args:
        window: A GLFW window.
        width: The width of the framebuffer.
        height: The height of the framebuffer.
    """
    gl.glViewport(0, 0, width, height)
