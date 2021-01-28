"""Implements the Texture class."""
import OpenGL.GL as gl
from PIL import Image

_TEXTURES = {}


class Texture:  # pylint: disable=too-few-public-methods
    """A texture to be mapped onto a mesh.

    The texture is generated lazily.

    Attributes:
        width: An integer representing the width of the texture in pixels.
        height: An integer representing the height of the texture in pixels.
    """

    def __init__(self, path: str):
        """Load data from a given image.

        Args:
            path: The path to the image to load.
        """
        self.path = path

        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        self.width = image.width
        self.height = image.height

        self.data = image.convert("RGBA").tobytes()

    @property
    def name(self):
        """Return an unsigned integer representing the name of the texture."""
        if self.path in _TEXTURES:
            return _TEXTURES[self.path]

        name = gl.glGenTextures(1)
        _TEXTURES[self.path] = name

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.name)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR)

        # NOTE(@bveeramani): Use this for Breakout only.
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_NEAREST)
        # gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
        #                    gl.GL_LINEAR)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width,
                        self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
                        self.data)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        return name

    def __repr__(self):
        """Represent the Texture as a string."""
        return "Texture(path='%s')" % (self.path)
