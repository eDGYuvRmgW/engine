"""Implements rendering meshes."""
from typing import List

import ctypes
import numpy as np
import OpenGL.GL as gl
import glm

from flaris.transform import Transform

from flaris.rendering.camera import Camera
from flaris.rendering.light import Light
from flaris.rendering.shader import Shader

__all__ = ["MeshRenderer"]

DEFAULT_VERTEX_SHADER = """
    #version 410 core
    layout (location = 0) in vec3 aPos;
    layout (location = 1) in vec3 aNormal;

    out vec3 FragPos;
    out vec3 Normal;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main()
    {
        gl_Position = projection * view * model * vec4(aPos, 1.0);
        FragPos = vec3(model * vec4(aPos, 1.0));

        // TODO(@nspevacek): costly, calculate matrix on CPU instead
        Normal = mat3(transpose(inverse(model))) * aNormal;
    }
"""

DEFAULT_FRAGMENT_SHADER = """
    #version 410 core
    struct Material {
        vec3 ambient;
        vec3 diffuse;
        vec3 specular;
        float shininess;
    };

    struct Light {
        vec3 direction;
        vec3 ambient;
        vec3 diffuse;
        vec3 specular;
    };

    out vec4 FragColor;

    in vec3 Normal;
    in vec3 FragPos;

    uniform Material material;
    uniform Light light;
    uniform vec3 lightPos;
    uniform vec3 viewPos;

    void main() {
        vec3 ambient = light.ambient * material.ambient;

        vec3 norm = normalize(Normal);
        vec3 lightDir = normalize(-light.direction);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = light.diffuse * (diff * material.diffuse);

        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir,reflectDir), 0.0), material.shininess);
        vec3 specular = light.specular * (spec * material.specular);

        vec3 result = ambient + diffuse + specular;
        FragColor = vec4(result, 1.0);
    }
"""

DEFAULT_MESH_SHADER = Shader.compile(vertex=DEFAULT_VERTEX_SHADER,
                                     fragment=DEFAULT_FRAGMENT_SHADER)


class MeshRenderer:  # pylint: disable=too-few-public-methods
    """A renderer for drawing meshes on the screen."""

    def __init__(self,
                 camera: Camera,
                 shader: Shader = DEFAULT_MESH_SHADER):
        """Initialize OpenGL buffer data."""
        self.camera = camera

        # TODO(@nspevacek): replace with vertices from loaded model once
        # implemented
        vertices = np.array([
            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, -0.5, -0.5, 0.0, 1.0,
            0.5, -0.5, -0.5, 0.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 0.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,
            0.5, -0.5, -0.5, 1.0, 1.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 0.0, 1.0
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

    def draw(self, transform: Transform, lights: List[Light]) -> None:
        """Draw a mesh on the screen.

        Args:
            transform: The position, rotation, and scale of the mesh.
        """
        gl.glUseProgram(self.shader.program)
        gl.glBindVertexArray(self.vao)

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

        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "viewPos"),
                       self.camera.transform.position.x,
                       self.camera.transform.position.y,
                       self.camera.transform.position.z)

        light = lights[0]

        gl.glUniform3f(
            gl.glGetUniformLocation(self.shader.program, "material.ambient"),
            1.0, 0.5, 0.31)
        gl.glUniform3f(
            gl.glGetUniformLocation(self.shader.program, "material.diffuse"),
            1.0, 0.5, 0.31)
        gl.glUniform3f(
            gl.glGetUniformLocation(self.shader.program, "material.specular"),
            0.5, 0.5, 0.5)
        gl.glUniform1f(
            gl.glGetUniformLocation(self.shader.program, "material.shininess"),
            32.0)

        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "lightPos"),
                       light.position.x, light.position.y,
                       light.position.z)
        gl.glUniform3f(
            gl.glGetUniformLocation(self.shader.program, "light.direction"), 
            -light.position.x, -light.position.y, -light.position.z)
        gl.glUniform3f(
            gl.glGetUniformLocation(self.shader.program, "light.ambient"),
            light.ambient.x, light.ambient.y, light.ambient.z)
        gl.glUniform3f(
            gl.glGetUniformLocation(self.shader.program, "light.diffuse"),
            light.diffuse.x, light.diffuse.y, light.diffuse.z)
        gl.glUniform3f(
            gl.glGetUniformLocation(self.shader.program, "light.specular"),
            light.diffuse.x, light.diffuse.y, light.diffuse.z)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
        gl.glBindVertexArray(0)
