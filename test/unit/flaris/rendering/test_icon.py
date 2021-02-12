"""Unit tests for the flaris.rendering.icon module."""
import pytest

from flaris.rendering import Icon


class TestIcon:
    """Unit tests for flaris.rendering.Icon class."""

    def testInit(self):
        icon = Icon("textures/icon.png")
        for image, size in zip(icon.images, icon.sizes):
            assert image.height == size and image.width == size

    def testInit_InvalidPath_RaisesValueError(self):
        with pytest.raises(ValueError):
            Icon("some-non-existant-icon.otf")

    def testRepr(self):
        icon = Icon("textures/icon.png")
        assert repr(icon) == "Icon(path=\"textures/icon.png\")"
