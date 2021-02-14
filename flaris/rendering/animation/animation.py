"""Do something."""

__all__ = ["Animation"]


class Animation(): # pylint: disable=too-few-public-methods
    """Do something."""

    def __init__(self, length: float, keyframes: list):
        """Do something."""
        self._length = length
        self._keyframes = keyframes

    @property
    def length(self) -> float:
        """Do something."""
        return self._length

    @property
    def keyframes(self) -> list:
        """Do something."""
        return self._keyframes
