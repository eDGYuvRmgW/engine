"""Unit tests for the `flaris.rendering.font` module."""
import pytest

from flaris.rendering import Font


class TestFont:
    """Unit tests for the `Font` class."""

    def testInit_InvalidPath_RaisesValueError(self):
        with pytest.raises(ValueError):
            Font("some-non-existant-image.png")
