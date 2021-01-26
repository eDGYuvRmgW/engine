"""Implements a simple light source."""
import ctypes
import glfw
import glm
import numpy as np
import OpenGL.GL as gl

from engine.rendering.camera import Camera
from engine.rendering.shader import Shader

__all__ = ["Lamp"]

DEFAULT_VERTEX_SHADER = """
    #version 410 core
    layout (location = 0) in vec3 aPos;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main()
    {
        gl_Position = projection * view * model * vec4(aPos, 1.0);
    }
    """

DEFAULT_FRAGMENT_SHADER = """
    #version 410 core
    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(1.0);
    }
    """

DEFAULT_LAMP_SHADER = Shader.compile(vertex=DEFAULT_VERTEX_SHADER,
                                       fragment=DEFAULT_FRAGMENT_SHADER)

class Lamp:  # pylint: disable=too-few-public-methods
    """A simple light."""

    def __init__(self, camera: Camera, shader: Shader = DEFAULT_LAMP_SHADER):
        """Initialize OpenGL buffer data."""
        self.camera = camera

        vertices = np.array([
            -0.5, -0.5, -0.5,  0.0, 0.0,
            0.5, -0.5, -0.5,  1.0, 0.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 0.0,

            -0.5, -0.5,  0.5,  0.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,

            -0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5,  0.5,  1.0, 0.0,

             0.5,  0.5,  0.5,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5,  0.5,  0.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 0.0,

            -0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5, -0.5,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,

            -0.5,  0.5, -0.5,  0.0, 1.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0
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
                                 20, ctypes.c_void_p(0))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def draw(self):
        """Draw the lamp on the screen."""
        gl.glUseProgram(self.shader.program)

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(450.0, 450.0, 0.0))
        model = glm.rotate(model, float(glfw.get_time() * glm.radians(50.0)),
                           glm.vec3(0.5, 1.0, 0.0))
        model = glm.scale(model, glm.vec3(25.0))

        projection = glm.ortho(0.0, 800.0, 0.0, 600.0, -100.0, 100.0)

        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.shader.program, "model"), 1, gl.GL_FALSE, glm.value_ptr(model))
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.shader.program, "view"), 1, gl.GL_FALSE, glm.value_ptr(self.camera.get_view()))
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.shader.program, "projection"), 1, gl.GL_FALSE, glm.value_ptr(projection))

        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
        gl.glBindVertexArray(0)
