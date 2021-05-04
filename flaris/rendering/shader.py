"""Implements the `Shader` class."""
from __future__ import annotations

import tempfile
import os
import glm

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
        if not os.path.exists(vertex):
            raise ValueError(
                f"Expected to find a vertex shader at \"{vertex}\", but a file "
                f"does not exist at that path.")
        if not os.path.exists(fragment):
            raise ValueError(
                f"Expected to find a fragment shader at \"{fragment}\", but a "
                f"file does not exist at that path.")

        self.vertex_path = vertex
        with open(self.vertex_path) as file:
            self.vertex_source = file.read()

        self.fragment_path = fragment
        with open(self.fragment_path) as file:
            self.fragment_source = file.read()

    def set_int(self, name: str, value: int) -> None:
        """Set the value of an int uniform.

        Args:
            name: The name of the uniform.
            value: The int to assign to the uniform.
        """
        gl.glUniform1i(gl.glGetUniformLocation(self.program, name), value)

    def set_float(self, name: str, value: float) -> None:
        """Set the value of a float uniform.

        Args:
            name: The name of the uniform.
            value: The float to assign to the uniform.
        """
        gl.glUniform1f(gl.glGetUniformLocation(self.program, name), value)

    def set_vec3(self, name: str, vector: glm.vec3) -> None:
        """Set the value of a vec3 uniform."""
        gl.glUniform3f(gl.glGetUniformLocation(self.program, name), vector.x,
                       vector.y, vector.z)

    def set_mat4(self, name: str, value: glm.mat4) -> None:
        """Set the value of a mat4 uniform.

        Args:
            name: The name of the uniform.
            value: The mat4 to assign to the uniform.
        """
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.program, name), 1,
                              gl.GL_FALSE, glm.value_ptr(value))

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
        # NOTE(@bveeramani): I don't remeber why, but there was some reason why
        # I didn't want to use with statements here.
        # pylint: disable=consider-using-with
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
