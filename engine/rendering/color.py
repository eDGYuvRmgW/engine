"""Implements the `Color` class."""
from dataclasses import dataclass

__all__ = ["Color"]


@dataclass(frozen=True)
class Color:  # pylint: disable=too-few-public-methods
    """Encapsulates a color in the RGB color space.

    Each color component is a floating point value in the range from 0 to 1.

    Attributes:
        red: The red component of the color.
        green: The green component of the color.
        blue: The blue component of the color.
        alpha: The alpha component of the color.
    """

    red: float
    green: float
    blue: float
    alpha: float = 1.0

    def __post_init__(self):
        """Check validity of constructor arguments."""
        for component in "red", "green", "blue", "alpha":
            value = getattr(self, component)
            if value < 0 or value > 1:
                raise ValueError(f"Expected argument '{component}' to be "
                                 f"between 0 and 1 but got {value}.")
