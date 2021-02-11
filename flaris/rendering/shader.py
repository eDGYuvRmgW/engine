"""Implements the `Shader` class."""
from __future__ import annotations

import tempfile
import os

import OpenGL.GL as gl
import OpenGL.GL.shaders as gls

__all__ = ["Shader"]

_SHADERS = {}


class Shader:  # pylint: disable=too-few-public-methods
    """Encapsulates an OpenGL shader.

    The shader program is compiled lazily.

    Attributes:
        program: An OpenGL shader program.
    """

    def __init__(self, vertex: str, fragment: str):
        """Initialize the vertex and fragment attributes.

        Args:
            vertex: Path to the vertex shader relative to the assets directory.
            fragment: Path to the fragment shader relative to the assets
                directory.
        """
        self.vertex_path = vertex
        with open(self.vertex_path) as file:
            self.vertex_source = file.read()

        self.fragment_path = fragment
        with open(self.fragment_path) as file:
            self.fragment_source = file.read()

    @property
    def program(self):
        """Return the OpenGL shader program."""
        if (self.vertex_path, self.fragment_path) in _SHADERS:
            return _SHADERS[(self.vertex_path, self.fragment_path)]

        _SHADERS[(self.vertex_path, self.fragment_path)] = gls.compileProgram(
            gls.compileShader(self.vertex_source, gl.GL_VERTEX_SHADER),
            gls.compileShader(self.fragment_source, gl.GL_FRAGMENT_SHADER))

        return _SHADERS[(self.vertex_path, self.fragment_path)]

    @staticmethod
    def compile(vertex: str, fragment: str) -> Shader:
        """Construct a shader from source.

        Args:
            vertex: The source code for the vertex shader.
            fragment: The source code for the fragment shader.

        Returns:
            A Shader instance.
        """
        vertex_shader = tempfile.NamedTemporaryFile(mode="w", delete=False)
        fragment_shader = tempfile.NamedTemporaryFile(mode="w", delete=False)

        vertex_shader.write(vertex)
        fragment_shader.write(fragment)

        vertex_shader.close()
        fragment_shader.close()

        shader = Shader(vertex_shader.name, fragment_shader.name)

        os.unlink(vertex_shader.name)
        os.unlink(fragment_shader.name)

        return shader
