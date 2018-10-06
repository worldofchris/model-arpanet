"""
Wireless display for node
"""

import unittest
from unittest.mock import MagicMock
from arpanet.display.wireless import Wireless

class TestWirelessDisplay(unittest.TestCase):
    """Test a Nodemcu based Wireless Display"""

    def setUp(self):
        self.transmitter = MagicMock()

    def test_update_display(self):
        """Update the display with the state of a node"""
        self.transmitter.enqueue = MagicMock()

        display = Wireless(self.transmitter)
        display.update('ucla', [None, None, None])
        # Display doesn't know anything about messages.  It just knows about
        # Palette Indicies.
        display.update('ucla', [1, 2, 3])
        expected = {'ucla': [1, 2, 3]}
        self.transmitter.enqueue.assert_called_with(expected)
