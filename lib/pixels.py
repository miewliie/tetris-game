import math
from rpi_ws281x import PixelStrip, Color as _Color
from lib.color import Color
from lib.sprite import Sprite 

# LED strip configuration:
LED_PIN        = 18        # GPIO pin connected to the pixels (must support PWM!).
LED_DMA        = 5         # DMA channel to use for generating signal (try 5)
MATRIX_HEIGHT  = 8
MATRIX_WIDTH   = 32
LED_COUNT      = MATRIX_HEIGHT * MATRIX_WIDTH # Number of LED pixels.

class Pixels:
    """A beautiful matrix of pixels."""

    _pixel_strip: PixelStrip
    """The stripe of LEDs correspoding to the matrix. Internal use only."""

    def __init__(self, brightness = 30):
        """Set brightness to 0 for darkest and 255 for brightest."""

        self._pixel_strip = PixelStrip(
              num = LED_COUNT,
              pin = LED_PIN,
              dma = LED_DMA,
              brightness = brightness
        )
        self._pixel_strip.begin()

    def __enter__(self):
        self.clear()
        self.show()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.clear()
        self.show()

    def show(self):
        """Flushes all uncommited pixel changes to the pixels."""

        self._pixel_strip.show()

    def fill(self, color: Color):
        """Completely fills the matrix with the given color."""
        
        for i in range(LED_COUNT):
          self._set(i, color)

    def clear(self):
        """Sets the matrix into a clean state."""

        self.fill(color = Color(0, 0, 0))

    def __setitem__(self, index: list[int], value: Color):
         row, col = index
         self.set(x = row, y = col, color = color)

    def set(self, x: int , y: int, color: Color):
        """Set the pixel at the given coordinates with the given color."""
        
        if x < 0 or x >= MATRIX_WIDTH:
            return
        
        if y < 0 or y >= MATRIX_HEIGHT:
            return
          
        led_number: int = x * MATRIX_HEIGHT + y
        if (math.floor(led_number / MATRIX_HEIGHT) % 2) == 1:
          self._set((x + 1) * MATRIX_HEIGHT - y - 1, color) 
        else:
          self._set(led_number, color)

    def _set(self, pos: int, color: Color):
        self._pixel_strip.setPixelColor(pos, _Color(color.r, color.g, color.b))

    def set_sprite(
        self,
        position: list[int],
        sprite: Sprite
    ):
        for row_idx, pixel_row in enumerate(sprite.pixels):
            for col_idx, pixel_value in enumerate(pixel_row):
                if pixel_value in sprite.palette.keys():
                    self.set(
                        x = position[0] + col_idx,
                        y = position[1] + row_idx,
                        color = sprite.palette[pixel_value]
                    )


    def tile(self, pattern: Sprite, position: list[int]):
        """Tiles a pattern matrix onto a canvas matrix."""

        for r in range(position[1], MATRIX_HEIGHT, pattern.height):
            for c in range(position[0], MATRIX_WIDTH, pattern.width):
                self.set_sprite([c,r], sprite = pattern)

