"""Implements rendering objects."""
import ctypes
import glfw
import glm  # pytype: disable=import-error
import numpy as np
import OpenGL.GL as gl

from engine.transform import Transform

from engine.rendering.shader import Shader
from engine.rendering.sprite import Sprite

__all__ = ["SpriteRenderer"]

DEFAULT_VERTEX_SHADER = """
    #version 410 core
    layout (location = 0) in vec4 vertex;

    out vec2 TexCoords;

    uniform mat4 model;
    uniform mat4 projection;

    void main()
    {
        TexCoords = vertex.zw;
        gl_Position = projection * model * vec4(vertex.xy, 0.0, 1.0);
    }
    """

DEFAULT_FRAGMENT_SHADER = """
    #version 410 core
    in vec2 TexCoords;
    out vec4 color;

    uniform sampler2D image;
    uniform vec3 spriteColor;

    void main()
    {
        color = vec4(spriteColor, 1.0) * texture(image, TexCoords);
    }
    """

DEFAULT_SPRITE_SHADER = Shader.compile(vertex=DEFAULT_VERTEX_SHADER,
                                       fragment=DEFAULT_FRAGMENT_SHADER)


class SpriteRenderer:  # pylint: disable=too-few-public-methods
    """A renderer for drawing sprites on the screen."""

    def __init__(self, shader: Shader = DEFAULT_SPRITE_SHADER):
        """Initialize OpenGL buffer data."""
        vertices = np.array([
            0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0
        ], dtype=np.float32)

        self.shader = shader

        self.vao = gl.glGenVertexArrays(1)
        vbo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices,
                        gl.GL_STATIC_DRAW)

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 4, gl.GL_FLOAT, gl.GL_FALSE,
                                 vertices.itemsize * 4, ctypes.c_void_p(0))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def __del__(self):
        """Delete VAO."""
        # NOTE(@bveeramani): Seems like there's some issue with PyOpenGL that's
        # causing this to bug out. See https://rb.gy/g4cj2k.
        # gl.glDeleteVertexArrays(1, self.vao);

    def draw(self, sprite: Sprite, transform: Transform) -> None:
        """Draw a sprite on the screen.

        Args:
            sprite: The sprite to draw.
            transform: The position, rotation, and scale of the sprite.
        """
        # pylint: disable=c-extension-no-member, no-member
        gl.glUseProgram(self.shader.program)
        gl.glBindTexture(gl.GL_TEXTURE_2D, sprite.texture.name)

        window = glfw.get_current_context()
        window_width, window_height = glfw.get_window_size(window)
        projection = glm.ortho(0.0, window_width, window_height, 0.0, -1.0, 1.0)

        width = sprite.texture.width * transform.scale.x
        height = sprite.texture.height * transform.scale.y

        gl.glUniform1i(gl.glGetUniformLocation(self.shader.program, "image"), 0)
        gl.glUniformMatrix4fv(
            gl.glGetUniformLocation(self.shader.program, "projection"), 1,
            gl.GL_FALSE, glm.value_ptr(projection))

        model = glm.mat4(1.0)
        model = glm.translate(
            model, glm.vec3(transform.position.x, transform.position.y, 0.0))

        model = glm.translate(model, glm.vec3(0.5 * width, 0.5 * height, 0.0))
        model = glm.rotate(model, glm.radians(180.0), glm.vec3(0.0, 0.0, 1.0))
        model = glm.translate(model, glm.vec3(-0.5 * width, -0.5 * height, 0.0))

        model = glm.scale(model, glm.vec3(width, height, 1.0))

        gl.glUniformMatrix4fv(
            gl.glGetUniformLocation(self.shader.program, "model"), 1,
            gl.GL_FALSE, glm.value_ptr(model))
        # TODO(@bveeramani): Add support for color alpha.
        gl.glUniform3f(
            gl.glGetUniformLocation(self.shader.program, "spriteColor"),
            sprite.color.red, sprite.color.green, sprite.color.blue)

        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
        gl.glBindVertexArray(0)
