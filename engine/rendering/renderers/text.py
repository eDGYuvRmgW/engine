"""Implements the `TextRenderer` class."""
from __future__ import annotations

import ctypes
from typing import TYPE_CHECKING

import glm  # pytype: disable=import-error
import OpenGL.GL as gl
import numpy as np

from engine.rendering.shader import Shader

if TYPE_CHECKING:
    from engine.transform import Transform
    from engine.rendering.text import Text

__all__ = ["TextRenderer"]

DEFAULT_VERTEX_SHADER = """
    #version 330 core
    layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
    out vec2 TexCoords;

    uniform mat4 projection;

    void main()
    {
        gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
        TexCoords = vertex.zw;
    }
    """
    
DEFAULT_FRAGMENT_SHADER = """
    #version 330 core
    in vec2 TexCoords;
    out vec4 color;

    uniform sampler2D text;
    uniform vec3 textColor;

    void main()
    {
        vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
        color = vec4(textColor, 1.0) * sampled;
    }
    """

DEFAULT_TEXT_SHADER = Shader.compile(
    vertex=DEFAULT_VERTEX_SHADER,
    fragment=DEFAULT_FRAGMENT_SHADER)


class TextRenderer:  # noqa: E241  # pylint: disable=too-few-public-methods
    """A renderer for rendering text on the screen."""

    def __init__(self, shader: Shader = DEFAULT_TEXT_SHADER):
        """Initialize this renderer.

        Args:
            shader: The shader to use for rendering text.
        """
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        ctypes.sizeof(ctypes.c_float) * 6 * 4, None,
                        gl.GL_DYNAMIC_DRAW)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

        self.shader = shader

    def draw(self, text: Text, transform: Transform) -> None:
        """Render text on the screen.

        Args:
            text: The text to render.
            transform: The `Transform` that specifies the position of the text.
        """
        gl.glUseProgram(self.shader.program)
        projection = glm.ortho(0.0, 800, 0, 600)
        gl.glUniformMatrix4fv(
            gl.glGetUniformLocation(self.shader.program, "projection"), 1,
            gl.GL_FALSE, glm.value_ptr(projection))

        gl.glUniform3f(
            gl.glGetUniformLocation(self.shader.program, "textColor"),
            text.color.red, text.color.blue, text.color.green)

        gl.glActiveTexture(gl.GL_TEXTURE0)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glBindVertexArray(self.vao)

        x, y, _ = transform.position

        for c in text.value:
            character = text.font.characters[c]

            xpos = x + character.bearing.x
            ypos = y - (character.size.y - character.bearing.y)

            width = character.size.x
            height = character.size.y

            vertices = np.array(
                [
                    xpos,
                    ypos + height,
                    0.0,
                    0.0,  # noqa: E241
                    xpos,
                    ypos,
                    0.0,
                    1.0,  # noqa: E241
                    xpos + width,
                    ypos,
                    1.0,
                    1.0,  # noqa: E241
                    xpos,
                    ypos + height,
                    0.0,
                    0.0,  # noqa: E241
                    xpos + width,
                    ypos,
                    1.0,
                    1.0,  # noqa: E241
                    xpos + width,
                    ypos + height,
                    1.0,
                    0.0,  # noqa: E241
                ],
                dtype=np.float32)

            gl.glBindTexture(gl.GL_TEXTURE_2D, character.texture)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
            x += (character.advance >> 6)

        gl.glBindVertexArray(0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
