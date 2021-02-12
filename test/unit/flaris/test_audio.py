"""Unit tests for the `flaris.audio` module."""
import pytest

from flaris.audio import AudioSource


class TestAudioSource:
    """Unit tests for `AudioSource` class."""

    def testInit_InvalidPath_RaisesValueError(self):
        with pytest.raises(ValueError):
            AudioSource("some-non-existant-sound.mp3")
