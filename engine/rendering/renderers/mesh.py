"""Implements rendering meshes."""
import ctypes
import glfw
import glm
import math
import numpy as np
import OpenGL.GL as gl

#from engine.transform import Transform

from engine.rendering.shader import Shader
from engine.rendering.texture import Texture

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
    out vec4 FragColor;

    in vec2 TexCoord;
    in vec3 FragPos;
    in vec3 Normal;

    uniform vec3 lightPos;

    void main()
    {
        FragColor = texture(aTexture, TexCoord);
    }
    """

DEFAULT_LIGHTING_SHADER = """
    #version 410 core
    struct Material {
        vec3 ambient;
        vec3 diffuse;
        vec3 specular;
        float shininess;
    };

    struct Light {
        vec3 position;

        vec3 ambient;
        vec3 diffuse;
        vec3 specular;

        float constant;
        float linear;
        float quadratic;
    };

    out vec4 FragColor;

    in vec3 FragPos;
    in vec3 Normal;

    uniform vec3 viewPos;
    uniform vec3 lightPos;
    uniform vec3 objectColor;
    uniform Material material;
    uniform Light light;
    
    void main()
    {
        vec3 ambient = light.ambient * material.ambient;
  	
        vec3 norm = normalize(Normal);
        vec3 lightDir = normalize(light.position - FragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = light.diffuse * (diff * material.diffuse);
    
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-lightDir, norm);  
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
        vec3 specular = light.specular * (spec * material.specular); 

        float distance = length(light.position - FragPos);
        float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));
        
        ambient *= attenuation;
        diffuse *= attenuation;
        specular *= attenuation;
        
        vec3 result = ambient + diffuse + specular;
        FragColor = vec4(result, 1.0);
    }
    """

DEFAULT_MESH_SHADER = Shader.compile(vertex=DEFAULT_VERTEX_SHADER,
                                       fragment=DEFAULT_LIGHTING_SHADER)

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
    def draw(self, view: glm.mat4) -> None:
        """Draw a mesh on the screen.

        Args:
            transform: The position, rotation, and scale of the mesh.
        """
        gl.glUseProgram(self.shader.program)
        gl.glBindVertexArray(self.vao)
        #texture = Texture("textures/ike.jpg")
        #gl.glBindTexture(gl.GL_TEXTURE_2D, texture.name)

        cube_positions = [
            glm.vec3(0.0, 0.0, 0.0),
            glm.vec3(2.0, 5.0, -15.0),
            glm.vec3(-1.5, -2.2, -2.5),
            glm.vec3(-3.8, -2.0, -12.3),
            glm.vec3(2.4, -0.4, -3.5),
            glm.vec3(-1.7, 3.0, -7.5),
            glm.vec3(1.3, -2.0, -2.5),
            glm.vec3(1.5, 2.0, -2.5),
            glm.vec3(1.5, 0.2, -1.5),
            glm.vec3(-1.3, 1.0, -1.5)
        ]

        for i in range(0, 10):
            model = glm.mat4(1.0)
            model = glm.translate(model, cube_positions[i])
            model = glm.rotate(model, float(glfw.get_time() * glm.radians(50.0)), glm.vec3(0.5, 1.0, 0.0))
            #model = glm.rotate(model, glm.radians(45.0), glm.vec3(1.0, 1.0, 0.0))
            model = glm.scale(model, glm.vec3(0.5, 0.5, 0.5))
            model_loc = gl.glGetUniformLocation(self.shader.program, "model")
            gl.glUniformMatrix4fv(model_loc, 1, gl.GL_FALSE, glm.value_ptr(model))
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

        #view = glm.mat4(1.0)
        #view = glm.translate(view, glm.vec3(0.0, 0.0, -3.0))

        #projection = glm.ortho(0.0, 800.0, 600.0, 0.0, 0.001, 1000.0)
        projection = glm.perspective(glm.radians(45.0), 800.0 / 600.0, 0.1, 100.0)

        

        view_loc = gl.glGetUniformLocation(self.shader.program, "view")
        gl.glUniformMatrix4fv(view_loc, 1, gl.GL_FALSE, glm.value_ptr(view))

        proj_loc = gl.glGetUniformLocation(self.shader.program, "projection")
        gl.glUniformMatrix4fv(proj_loc, 1, gl.GL_FALSE, glm.value_ptr(projection))

        object_color = gl.glGetUniformLocation(self.shader.program, "objectColor")
        gl.glUniform3f(object_color, 1.0, 0.5, 0.31)

        #light_color = gl.glGetUniformLocation(self.shader.program, "lightColor")
        #gl.glUniform3f(light_color, 1.0, 1.0, 1.0)

        #light_pos = gl.glGetUniformLocation(self.shader.program, "lightPos")
        #gl.glUniform3f(light_pos, 0.5, 0.5, 0.6)

        view_pos = gl.glGetUniformLocation(self.shader.program, "viewPos")
        gl.glUniform3f(view_pos, 0.0, 0.0, 3.0)

        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "material.ambient"), 1.0, 0.5, 0.31)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "material.diffuse"), 1.0, 0.5, 0.31)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "material.specular"), 0.5, 0.5, 0.5)
        gl.glUniform1f(gl.glGetUniformLocation(self.shader.program, "material.shininess"), 32.0)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "light.specular"), 0.5, 0.5, 0.5)

        light_color = glm.vec3(math.sin(glfw.get_time() * 2.0), math.sin(glfw.get_time() * 0.7), math.sin(glfw.get_time() * 1.3))

        diffuse_color = light_color * glm.vec3(0.5)
        ambient_color = diffuse_color * glm.vec3(0.2)

        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "light.ambient"), ambient_color.x, ambient_color.y, ambient_color.z)
        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "light.diffuse"), diffuse_color.x, diffuse_color.y, diffuse_color.z)

        gl.glUniform3f(gl.glGetUniformLocation(self.shader.program, "light.position"), 0.5, 0.5, 0.6)

        gl.glUniform1f(gl.glGetUniformLocation(self.shader.program, "light.constant"), 1.0)
        gl.glUniform1f(gl.glGetUniformLocation(self.shader.program, "light.linear"), 0.09)
        gl.glUniform1f(gl.glGetUniformLocation(self.shader.program, "light.quadratic"), 0.032)

        
        gl.glBindVertexArray(0)
