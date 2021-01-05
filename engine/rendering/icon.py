"""Implements the `Icon` class."""
from PIL import Image

from engine import resource

__all__ = ["Icon"]


class Icon:  # pylint: disable=too-few-public-methods
    """Encapsulates a window or file icon.

    The `Icon` constructor loads an image from the provided path and converts
    the image to square images of varying sizes. The specific sizes were
    retrieved from this Stack Overflow thread (https://stackoverflow.com/
    questions/3236115/which-icon-sizes-should-my-windows-applications-icon-
    include), which describes which icon sizes should be provided to a Windows
    application.

    Attributes:
        images: A list of PIL images scaled to the sizes defined by the
            `sizes` class attribute.
        sizes: A list of integers representing the height and width of each
            image in the `images` list.

    Example:
        >>> from engine.rendering import Window
        >>> icon = Icon("textures/icon.png")
        >>> with Window("Untitled Window", 1080, 720, icon=icon) as window:
        ...     pass
    """

    sizes = (16, 24, 32, 40, 48, 64, 96, 128, 256)

    def __init__(self, path: str):
        """Initialize the `images` attribute.

        Arg:
            path: A path to an image. The path should be relative to the assets
                directory.
        """
        self.path = path
        image = Image.open(resource.path(path))
        self.images = [image.resize((size, size)) for size in self.sizes]

    def __repr__(self) -> str:
        """Represent this `Icon` as a string."""
        return f"Icon(path=\"{self.path}\")"
