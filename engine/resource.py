"""Functions for accessing game assets."""
import os


def path(relative_path: str):
    """Return the absolute path to a file in the assets directory.

    Args:
        relative_path: A file path relative to the assets directory.
    """
    return os.path.join(os.path.dirname(__file__), "assets", relative_path)
