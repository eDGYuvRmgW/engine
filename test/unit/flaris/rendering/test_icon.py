"""Unit tests for the `flaris.rendering.icon` module."""
import os

import pytest

from flaris.rendering import Icon


class TestIcon:
    """Unit tests for the `Icon` class."""

    path = os.path.join(os.path.dirname(__file__), "icon.jpg")

    def testInit(self):
        icon = Icon(self.path)
        for image, size in zip(icon.images, icon.sizes):
            assert image.height == size and image.width == size

    def testInit_InvalidPath_RaisesValueError(self):
        with pytest.raises(ValueError):
            Icon("some-non-existant-icon.png")

    def testRepr(self):
        assert repr(Icon(self.path)) == f"Icon(path=\"{self.path}\")"
