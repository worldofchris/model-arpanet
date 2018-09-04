"""
Test display made up of wired connection to neopixel strip.
"""
import unittest
from arpanet.display.wired import Wired

class TestWiredDisplay(unittest.TestCase):
    """
    Test receiept of messages and updating of the neopixel
    strip for wired IMPs
    """
    def setUp(self):
        self.data_pin = 18
        self.wired = Wired(self.data_pin)
        self.palette = [(255, 0, 0)]

    def test_set_neopixels_for_node(self):
        """
        Set the neopixels for a specific node
        """
        self.wired.add_node('ucla', 0, 0)
        assert self.wired.strip == [self.wired.palette[0],
                                    self.wired.palette[0],
                                    self.wired.palette[0]], self.wired.strip

    def test_set_neopixels_with_hss_on(self):
        """
        If the High Side Switch that switches the neopixel
        data wire on the model is on then neopixel offsets
        change
        """
        self.wired.add_node('sri', 3, 6)

        self.wired.update('sri', [1, 2, 3])

        assert self.wired.strip == [self.wired.palette[0],
                                    self.wired.palette[0],
                                    self.wired.palette[0],
                                    self.wired.palette[1],
                                    self.wired.palette[2],
                                    self.wired.palette[3],
                                    self.wired.palette[0],
                                    self.wired.palette[0],
                                    self.wired.palette[0]]

        self.wired.set_hss_on(True)
        self.wired.update('sri', [1, 2, 3])

        assert self.wired.strip == [self.wired.palette[0],
                                    self.wired.palette[0],
                                    self.wired.palette[0],
                                    self.wired.palette[0],
                                    self.wired.palette[0],
                                    self.wired.palette[0],
                                    self.wired.palette[1],
                                    self.wired.palette[2],
                                    self.wired.palette[3]], self.wired.strip

    def test_ascify_display(self):
        """
        Ascii version of the display
        """
        self.wired.strip = [self.wired.palette[0],
                            self.wired.palette[1],
                            self.wired.palette[2],
                            self.wired.palette[3],
                            self.wired.palette[0],
                            self.wired.palette[1],
                            self.wired.palette[2],
                            self.wired.palette[3],
                            self.wired.palette[0]]

        assert str(self.wired) == "012301230", str(self.wired)
