"""Interface for accessing files in the standard assets directory."""
import os


def path(path: str) -> str:
    """Return the absolute path to a file in the standard assets directory.

    Args:
        path: Path to an asset relative to the standard assets directory.

    Returns:
        The absolute path to the specified file.
    """
    return os.path.join(os.path.dirname(__file__), path)
