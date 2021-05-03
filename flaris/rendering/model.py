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
      

class Mesh:

    def __init__(self, primitive) -> None:
        self._vao = 0

        if not len(primitive.vertex):
            raise ValueError("Foo")

        vertex_indices = np.array(primitive.vertex_index).flatten()
        vertices = primitive.vertex[vertex_indices]

        if primitive.normal is not None:
            normal_indices = np.array(primitive.normal_index).flatten()
            normals = primitive.normal[normal_indices]
        else:
            normals = np.zeros(vertices.shape)

        if len(primitive.texcoordset) == 0:
            texture_coordinates = np.zeros((len(vertices), 2), dtype=np.float32)
        else:
            if primitive.texcoord_indexset:
                texture_coordinates = primitive.texcoordset[0][primitive.texcoord_indexset[0]]
            else:
                texture_coordinates = primitive.texcoordset[0]
                    
        self.array = np.concatenate([vertices, normals, texture_coordinates], axis=1)

    @property
    def vao(self) -> None:
        if self._vao:
            return self._vao

        self._vao = gl.glGenVertexArrays(1)
        vbo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self._vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.array.nbytes, self.array,
                                    gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 32,
                                    ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 32,
                                ctypes.c_void_p(12))
        gl.glEnableVertexAttribArray(1)

        gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, gl.GL_FALSE, 32,
                                ctypes.c_void_p(24))
        gl.glEnableVertexAttribArray(2)

        gl.glBindVertexArray(0)

        return self._vao

    @property
    def size(self) -> int:
        return len(self.array)


class Model(Component):

    def __init__(self, path: str):
        mesh = collada.Collada(path)

        self.meshes = []
        for geometry in mesh.geometries:
            for primitive in geometry.primitives:
                self.meshes.append(Mesh(primitive))

    def __iter__(self):
        return iter(self.meshes)