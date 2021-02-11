"""Unit tests for the flaris.rendering.icon module."""
from flaris.rendering import Icon


class TestIcon:
    """Unit tests for flaris.rendering.Icon class."""

    def testInit(self):
        icon = Icon("textures/icon.png")
        for image, size in zip(icon.images, icon.sizes):
            assert image.height == size and image.width == size

    def testRepr(self):
        icon = Icon("textures/icon.png")
        assert repr(icon) == "Icon(path=\"textures/icon.png\")"
