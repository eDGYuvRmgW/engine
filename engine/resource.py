"""Functions for accessing game assets."""
import os
import sys


def path(relative_path: str):
    """Return the absolute path to a file in the assets directory.

    Args:
        relative_path: A file path relative to the assets directory.
    """
    try:
        # NOTE(@bveeramani): Using getattr here to appease linters.
        base_path = getattr(sys, "_MEIPASS")
    except AttributeError:
        # TODO(@bveeramani): Make the base path the top-level directory rather
        # than the current working directory.
        base_path = os.path.abspath(".")
    return os.path.join(os.path.dirname(__file__), "assets", relative_path)
