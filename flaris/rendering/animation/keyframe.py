"""Do something."""

__all__ = ["Keyframe"]


class Keyframe(): # pylint: disable=too-few-public-methods
    """Do something."""

    def __init__(self, timestamp: float, pose: dict):
        """Do something."""
        self._timestamp = timestamp
        self._pose = pose

    @property
    def timestamp(self) -> float:
        """Do something."""
        return self._timestamp

    @property
    def pose(self) -> dict:
        """Do something."""
        return self._pose
