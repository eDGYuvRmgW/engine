"""Implements rendering meshes."""
import ctypes
import math
import glfw
import glm
import numpy as np
import OpenGL.GL as gl

from engine.rendering.camera import Camera
from engine.rendering.shader import Shader

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

        // TODO(@nspevacek): costly, calculate matrix on CPU instead (like model)
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
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
        vec3 specular = light.specular * (spec * material.specular);

        vec3 result = ambient + diffuse + specular;
        FragColor = vec4(result, 1.0);
    }
"""

DEFAULT_MESH_SHADER = Shader.compile(vertex=DEFAULT_VERTEX_SHADER,
                                       fragment=DEFAULT_FRAGMENT_SHADER)

class MeshRenderer: # pylint: disable=too-few-public-methods
    """A renderer for drawing meshes on the screen."""

    def __init__(self, camera: Camera, shader: Shader = DEFAULT_MESH_SHADER):
        """Initialize OpenGL buffer data."""
        self.camera = camera

        # TODO(@nspevacek): replace with vertices from loaded model once implemented
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

    def draw(self) -> None:
        """Draw a mesh on the screen.

        Args:
            transform: The position, rotation, and scale of the mesh.
        """
        gl.glUseProgram(self.shader.program)
        gl.glBindVertexArray(self.vao)

        cube_positions = [
            glm.vec3(50.0, 0.0, 0.0),
            glm.vec3(200.0, 500.0, 0.0),
            glm.vec3(150.0, 220.0, 0.0),
            glm.vec3(380.0, 20.0, 0.0),
            glm.vec3(240.0, 40.0, 0.0),
            glm.vec3(500.0, 300.0, 0.0),
            glm.vec3(350.0, 200.0, 0.0),
            glm.vec3(400.0, 200.0, 0.0),
            glm.vec3(600.0, 600.0, 0.0),
            glm.vec3(130.0, 100.0, 0.0)
        ]

        for i in range(0, 10):
            model = glm.mat4(1.0)
            model = glm.translate(model, cube_positions[i])
            model = glm.rotate(model, float(glfw.get_time() * glm.radians(50.0)), glm.vec3(0.5, 1.0, 0.0))
            model = glm.scale(model, glm.vec3(25.0))
            gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.shader.program, "model"), 1, gl.GL_FALSE, glm.value_ptr(model))
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.shader.program, "view"), 1, gl.GL_FALSE, glm.value_ptr(self.camera.get_view()))
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.shader.program, "projection"), 1, gl.GL_FALSE, glm.value_ptr(self.camera.get_projection()))

        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "lightPos"), 450.0, 450.0, 0.0)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "viewPos"), 0.0, 0.0, 3.0)

        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "material.ambient"), 1.0, 0.5, 0.31)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "material.diffuse"), 1.0, 0.5, 0.31)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "material.specular"), 0.5, 0.5, 0.5)
        gl.glUniform1f(gl.glGetUniformLocation(self.shader.program, "material.shininess"), 32.0)
        
        light_color = glm.vec3(math.sin(glfw.get_time() * 2.0), math.sin(glfw.get_time() * 0.7), math.sin(glfw.get_time() * 1.3))
        diffuse_color = light_color * glm.vec3(0.5)
        ambient_color = diffuse_color * glm.vec3(0.2)

        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "light.direction"), -450.0, -450.0, 0.0)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "light.ambient"), ambient_color.x, ambient_color.y, ambient_color.z)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "light.diffuse"), diffuse_color.x, diffuse_color.y, diffuse_color.z)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "light.specular"), 0.5, 0.5, 0.5)
        
        gl.glBindVertexArray(0)
