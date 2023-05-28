from lib.color import Color

class Sprite:

    @property
    def width(self) -> int:
        """Width of the sprite."""
        return len(self.pixels[0])

    @property
    def height(self) -> int:
        """Height of the sprite."""
        return len(self.pixels)

    pixels: list[list[str]]
    """The matrix of pixels representing the sprite."""

    palette: dict[str, Color]
    """The colors associated to each symbol listed in the pixels attribute."""

    def __init__(self, pixels: list[list[str]], palette: dict[str, Color]):
        self.pixels = pixels
        self.palette = palette
