"""Unit tests for the `flaris.rendering.shader` module."""
import pytest

from flaris.rendering import Shader


class TestShader:
    """Unit tests for `Shader` class."""

    def testInit_InvalidPath_RaisesValueError(self):
        with pytest.raises(ValueError):
            Shader("some-non-existant-vertex-shader.glsl",
                   "some-non-existant-fragment-shader.glsl")
