"""Implements rendering meshes."""
import ctypes
import numpy as np
import OpenGL.GL as gl
import glm

from flaris.transform import Transform

from flaris.rendering.camera import Camera
from flaris.rendering.shader import Shader

from ..light import Light
from ..material import Material
from ..mesh import Mesh

__all__ = ["MeshRenderer"]

DEFAULT_VERTEX_SHADER = """
    #version 410 core
    layout (location = 0) in vec3 aPos;
    layout (location = 1) in vec3 aNormal;
    layout (location = 2) in vec2 aTexCoords;

    out vec3 FragPos;
    out vec3 Normal;
    out vec2 TexCoords;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main()
    {
        FragPos = vec3(model * vec4(aPos, 1.0));
        Normal = mat3(transpose(inverse(model))) * aNormal;
        TexCoords = aTexCoords;

        gl_Position = projection * view * vec4(FragPos, 1.0);
    }
"""

DEFAULT_FRAGMENT_SHADER = """
    #version 330 core
    out vec4 FragColor;

    struct Material {
        sampler2D ambient;
        sampler2D diffuse;
        vec3 albedo;
    };

    struct Light {
        vec3 direction;
        vec3 ambient;
        vec3 diffuse;
    };

    in vec3 FragPos;
    in vec3 Normal;
    in vec2 TexCoords;

    uniform vec3 viewPos;
    uniform Material material;
    uniform Light light;

    void main()
    {
        // ambient
        vec3 ambient = material.albedo * light.ambient *
            texture(material.ambient, TexCoords).rgb;

        // diffuse
        vec3 norm = normalize(Normal);
        vec3 lightDir = light.direction;
        float diff = max(dot(norm, -lightDir), 0.0);
        vec3 diffuse = material.albedo * light.diffuse *
            (diff * texture(material.diffuse, TexCoords).rgb);

        vec3 result = ambient + diffuse;
        FragColor = vec4(result, 1.0);
    }
"""

DEFAULT_MESH_SHADER = Shader.compile(vertex=DEFAULT_VERTEX_SHADER,
                                     fragment=DEFAULT_FRAGMENT_SHADER)


class MeshRenderer:  # pylint: disable=too-few-public-methods
    """A renderer for drawing meshes on the screen."""

    def __init__(self, camera: Camera, shader: Shader = DEFAULT_MESH_SHADER):
        """Initialize OpenGL buffer data."""
        self.camera = camera

        # TODO(@nspevacek): replace with vertices from loaded model once
        # implemented
        # yapf: disable
        vertices = np.array([
            -0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 0.0, 0.0, 0.5, -0.5, -0.5, 0.0,
            0.0, -1.0, 1.0, 0.0, 0.5, 0.5, -0.5, 0.0, 0.0, -1.0, 1.0, 1.0, 0.5,
            0.5, -0.5, 0.0, 0.0, -1.0, 1.0, 1.0, -0.5, 0.5, -0.5, 0.0, 0.0,
            -1.0, 0.0, 1.0, -0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 0.0, 0.0, -0.5,
            -0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0, 0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
            1.0, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5,
            0.0, 0.0, 1.0, 1.0, 1.0, -0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0, -0.5, 0.5, 0.5, -1.0, 0.0,
            0.0, 1.0, 0.0, -0.5, 0.5, -0.5, -1.0, 0.0, 0.0, 1.0, 1.0, -0.5,
            -0.5, -0.5, -1.0, 0.0, 0.0, 0.0, 1.0, -0.5, -0.5, -0.5, -1.0, 0.0,
            0.0, 0.0, 1.0, -0.5, -0.5, 0.5, -1.0, 0.0, 0.0, 0.0, 0.0, -0.5, 0.5,
            0.5, -1.0, 0.0, 0.0, 1.0, 0.0, 0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0,
            0.0, 0.5, 0.5, -0.5, 1.0, 0.0, 0.0, 1.0, 1.0, 0.5, -0.5, -0.5, 1.0,
            0.0, 0.0, 0.0, 1.0, 0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0, 0.5,
            -0.5, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 1.0, 0.0, 0.0,
            1.0, 0.0, -0.5, -0.5, -0.5, 0.0, -1.0, 0.0, 0.0, 1.0, 0.5, -0.5,
            -0.5, 0.0, -1.0, 0.0, 1.0, 1.0, 0.5, -0.5, 0.5, 0.0, -1.0, 0.0, 1.0,
            0.0, 0.5, -0.5, 0.5, 0.0, -1.0, 0.0, 1.0, 0.0, -0.5, -0.5, 0.5, 0.0,
            -1.0, 0.0, 0.0, 0.0, -0.5, -0.5, -0.5, 0.0, -1.0, 0.0, 0.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 0.5, 0.5, -0.5, 0.0, 1.0,
            0.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 1.0, 0.0, 0.5, 0.5,
            0.5, 0.0, 1.0, 0.0, 1.0, 0.0, -0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 0.0,
            0.0, -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 1.0
        ], dtype=np.float32)
        # yapf: enable

        self.shader = shader

        self.vao = gl.glGenVertexArrays(1)
        vbo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices,
                        gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 32,
                                 ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 32,
                                 ctypes.c_void_p(12))
        gl.glEnableVertexAttribArray(1)

        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 32,
                                 ctypes.c_void_p(24))
        gl.glEnableVertexAttribArray(2)

    def draw(self, mesh: Mesh, transform: Transform, light: Light) -> None:  # pylint: disable=unused-argument  # noqa: E501
        """Draw a mesh on the screen.

        Args:
            mesh: The mesh to draw.
            transform: The position, rotation, and scale of the mesh.
            light: The light to draw.
        """
        gl.glUseProgram(self.shader.program)
        gl.glBindVertexArray(self.vao)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, mesh.entity[Material].ambient)

        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, mesh.entity[Material].diffuse)

        self.shader.set_int("material.ambient", 0)
        self.shader.set_int("material.diffuse", 1)

        model = glm.mat4(1.0)
        model = glm.translate(
            model,
            glm.vec3(transform.position.x, transform.position.y,
                     transform.position.z))

        model = glm.rotate(model, glm.radians(transform.rotation.x),
                           glm.vec3(1.0, 0.0, 0.0))
        model = glm.rotate(model, glm.radians(transform.rotation.y),
                           glm.vec3(0.0, 1.0, 0.0))
        model = glm.rotate(model, glm.radians(transform.rotation.z),
                           glm.vec3(0.0, 0.0, 1.0))

        model = glm.scale(
            model,
            glm.vec3(transform.scale.x, transform.scale.y, transform.scale.z))

        gl.glUniformMatrix4fv(
            gl.glGetUniformLocation(self.shader.program, "model"), 1,
            gl.GL_FALSE, glm.value_ptr(model))
        gl.glUniformMatrix4fv(
            gl.glGetUniformLocation(self.shader.program, "view"), 1,
            gl.GL_FALSE, glm.value_ptr(self.camera.view))
        gl.glUniformMatrix4fv(
            gl.glGetUniformLocation(self.shader.program, "projection"), 1,
            gl.GL_FALSE, glm.value_ptr(self.camera.projection))

        angles = light.entity[Transform].rotation * 3.14159 / 180
        rotation = glm.quat(glm.vec3(angles.x, angles.y, angles.z))
        forwards = glm.vec3(0, 0, 1)
        self.shader.set_vec3("light.direction", rotation * forwards)
        self.shader.set_vec3("viewPos", self.camera.entity[Transform].position)
        albedo = mesh.entity[Material].albedo
        self.shader.set_vec3("material.albedo",
                             glm.vec3(albedo.red, albedo.green, albedo.blue))
        self.shader.set_vec3("light.diffuse", light.diffuse)
        self.shader.set_vec3("light.ambient", light.ambient)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
        gl.glBindVertexArray(0)
