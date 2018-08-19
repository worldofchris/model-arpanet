import unittest
from arpa import Display
import neopixel
from unittest.mock import MagicMock, patch

class test_node(unittest.TestCase):
    # It sets LED on based on palette and light index
    @patch('neopixel.NeoPixel')
    def test_set_display(self, NeoPixel):
        display = Display()
        display.set_light(0,1)
        assert display.np.__setitem__.call_count == 1
        assert display.np.write.call_count == 1

# It clears the display
    @patch('neopixel.NeoPixel')
    def test_clear_display(self, NeoPixel):
        display = Display()
        display.clear()
        assert display.np.__setitem__.call_count == 3 # MAGIC
        assert display.np.write.call_count == 1