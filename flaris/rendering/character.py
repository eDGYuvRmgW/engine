"""Implements the `Character` class."""
from dataclasses import dataclass

import glm  # pytype: disable=import-error

__all__ = ["Character"]


# TODO(@bveeramani): Refactor the `Character` and `Font` classes so that `glm`
# isn't exposed.
@dataclass(frozen=True)
class Character:
    """Represents a character in a font."""
    texture: int
    size: glm.vec2
    bearing: glm.vec2
    advance: int
