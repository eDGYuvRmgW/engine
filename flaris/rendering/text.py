"""Implements the `Text` class."""
from dataclasses import dataclass

from flaris.component import Component

from flaris import assets
from flaris.rendering.color import Color
from flaris.rendering.font import Font

__all__ = ["Text"]


@dataclass
class Text(Component):
    """Represents text to be rendered."""
    value: str
    font: Font = Font(assets.path("fonts/Moon Light.otf"))
    color: Color = Color(1.0, 1.0, 1.0)
