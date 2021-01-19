"""Implements rendering meshes."""
import ctypes
import glfw
import glm
import numpy as np
import OpenGL.GL as gl

#from engine.transform import Transform

from engine.rendering.shader import Shader
from engine.rendering.texture import Texture

__all__ = ["MeshRenderer"]

# https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/7.4.camera_class/7.4.camera.vs
DEFAULT_VERTEX_SHADER = """
    #version 410 core
    layout (location = 0) in vec3 aPos;
    layout (location = 1) in vec2 aTexCoord;

    out vec2 TexCoord;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main()
    {
        gl_Position = projection * view * model * vec4(aPos, 1.0f);
        TexCoord = vec2(aTexCoord.x, aTexCoord.y);
    }
    """

# use https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/7.4.camera_class/7.4.camera.fs ?
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

DEFAULT_MESH_SHADER = Shader.compile(vertex=DEFAULT_VERTEX_SHADER,
                                       fragment=DEFAULT_FRAGMENT_SHADER)

class MeshRenderer: # pylint: disable=too-few-public-methods
    """A renderer for drawing meshes on the screen."""

    def __init__(self, shader: Shader = DEFAULT_MESH_SHADER):
        #https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/6.1.coordinate_systems/coordinate_systems.cpp
        """Initialize OpenGL buffer data."""
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

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 20,
                                 ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 20,
                                 ctypes.c_void_p(12))
        gl.glEnableVertexAttribArray(1)

    # https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/7.4.camera_class/camera_class.cpp
    def draw(self) -> None:
        """Draw a mesh on the screen.

        Args:
            transform: The position, rotation, and scale of the mesh.
        """
        gl.glUseProgram(self.shader.program)
        texture = Texture("textures/ike.jpg")
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture.name)

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(400.0, 300.0, 0.0))
        model = glm.rotate(model, float(glfw.get_time() * glm.radians(50.0)), glm.vec3(0.5, 1.0, 0.0))
        model = glm.scale(model, glm.vec3(100.0, 100.0, 100.0))

        view = glm.mat4(1.0)
        view = glm.translate(view, glm.vec3(0.0, 0.0, -3.0))

        #projection = glm.perspective(glm.radians(45.0), 800.0 / 600.0, 0.1, 100.0)
        projection = glm.ortho(0.0, 800.0, 600.0, 0.0, -50.0, 1000.0)

        model_loc = gl.glGetUniformLocation(self.shader.program, "model")
        gl.glUniformMatrix4fv(model_loc, 1, gl.GL_FALSE, glm.value_ptr(model))

        view_loc = gl.glGetUniformLocation(self.shader.program, "view")
        gl.glUniformMatrix4fv(view_loc, 1, gl.GL_FALSE, glm.value_ptr(view))

        proj_loc = gl.glGetUniformLocation(self.shader.program, "projection")
        gl.glUniformMatrix4fv(proj_loc, 1, gl.GL_FALSE, glm.value_ptr(projection))

        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
        gl.glBindVertexArray(0)
