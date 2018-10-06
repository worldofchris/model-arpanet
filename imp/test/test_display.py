"""
Test LED display for Nodemcu IMPs
"""
import unittest
from unittest.mock import patch
from imp.display import Display, PALETTE

class TestDisplay(unittest.TestCase):
    """Test IMP Display"""
    @patch('neopixel.NeoPixel')
    def test_set_display(self, NeoPixel):
        """It sets LED on based on palette and light index"""
        display = Display()
        display.set_light(0, 1)
        assert display.neo_pixel.__setitem__.call_count == 1
        assert display.neo_pixel.write.call_count == 1

    @patch('neopixel.NeoPixel')
    def test_set_display_to_none(self, NeoPixel):
        """It sets LED on based on palette and light index"""
        display = Display()
        display.set_light(0, None)
        assert display.neo_pixel.__setitem__.call_count == 1
        # assert display.neo_pixel.__setitem__.assert_called_with(0, (0, 0, 0))
        assert display.neo_pixel.write.call_count == 1

    @patch('neopixel.NeoPixel')
    def test_clear_display(self, NeoPixel):
        """It clears the display """
        display = Display()
        display.clear()
        assert display.neo_pixel.__setitem__.call_count == 3 # MAGIC
        assert display.neo_pixel.write.call_count == 1
