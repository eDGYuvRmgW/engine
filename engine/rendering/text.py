"""Implements the `Text` class."""
from dataclasses import dataclass

from engine.component import Component

from engine import assets
from engine.rendering.color import Color
from engine.rendering.font import Font

__all__ = ["Text"]


@dataclass
class Text(Component):
    """Represents text to be rendered."""
    value: str
    font: Font = Font(assets.path("fonts/Moon Light.otf"))
    color: Color = Color(1.0, 1.0, 1.0)
