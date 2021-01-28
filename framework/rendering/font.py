"""Implements the `Font` class."""
from typing import Dict

import freetype
import glm  # pytype: disable=import-error
import OpenGL.GL as gl

from engine import resource
from engine.rendering.character import Character

__all__ = ["Font"]


class Font:  # pylint: disable=too-few-public-methods
    """Represents a font.

    The character map is lazily loaded at runtime.

    Attributes:
        characters: A dictionary that maps ASCII characters to `Character`
            objects.
    """

    def __init__(self, path: str, size: int = 100):
        """Save constructor arguments.

        Args:
            path: Path to a font file relative to the assets directory.
            size: The font size in points.
        """
        self.path = path
        self.size = size
        self._characters = {}

    @property
    def characters(self) -> Dict[str, Character]:
        """Return a `dict` that maps ASCII characters to `Character` objects."""
        if self._characters:
            return self._characters

        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        print(resource.path(self.path))
        face = freetype.Face(resource.path(self.path))
        face.set_char_size(self.size * 64)

        for i in range(128):
            face.load_char(chr(i))

            texture = gl.glGenTextures(1)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RED,
                            face.glyph.bitmap.width, face.glyph.bitmap.rows, 0,
                            gl.GL_RED, gl.GL_UNSIGNED_BYTE,
                            face.glyph.bitmap.buffer)

            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,
                               gl.GL_CLAMP_TO_EDGE)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,
                               gl.GL_CLAMP_TO_EDGE)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                               gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                               gl.GL_LINEAR)

            character = Character(
                texture,
                glm.ivec2(face.glyph.bitmap.width, face.glyph.bitmap.rows),
                glm.ivec2(face.glyph.bitmap_left, face.glyph.bitmap_top),
                face.glyph.advance.x)
            self._characters[chr(i)] = character

        return self._characters
