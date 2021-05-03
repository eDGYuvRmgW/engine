import ctypes
from dataclasses import dataclass
from typing import List

import collada
import glm
import numpy as np
import OpenGL.GL as gl

from flaris.component import Component
from .texture import Texture

__all__ = ["Model"]


@dataclass(frozen=True)
class Vertex:
    position: glm.vec3
    normal: glm.vec3
    texture_coordinates: glm.vec2        

class Model(Component):

    def __init__(self, path: str):
        mesh = collada.Collada(path)

        vertices = np.empty((0, 3), dtype=np.float32)
        normals = np.empty((0, 3), dtype=np.float32)

        for geometry in mesh.geometries:
            for primitive in geometry.primitives:
                vertices = np.concatenate([vertices, primitive.vertex[np.array(primitive.vertex_index).flatten()]])
                normals = np.concatenate([normals, primitive.normal[np.array(primitive.normal_index).flatten()]])

        self._vertices = np.concatenate([vertices, normals], axis=1)
        self._vao = 0

    def init(self) -> None:
        if self._vao:
            return

        self._vao = gl.glGenVertexArrays(1)
        vbo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self._vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

        gl.glBufferData(gl.GL_ARRAY_BUFFER, self._vertices.nbytes, self._vertices,
                                    gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 24,
                                    ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 24,
                                ctypes.c_void_p(12))
        gl.glEnableVertexAttribArray(1)

        gl.glBindVertexArray(0)

    @property
    def vao(self) -> int:
        self.init()
        return self._vao