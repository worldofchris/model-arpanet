"""
Broadcast UDP messages to the wireless nodemcu IMPs
"""
import unittest
from arpanet.display.transmitter import Transmitter

class TestWirelessTransmitter(unittest.TestCase):
    """Test wireless transmitter"""
    def setUp(self):
        self.transmitter = Transmitter(5005, "172.20.10.15")

    def test_enqueue_messages(self):
        """
        Nodes can enqueue messages which are then broadcast in one
        go by the transmitter.
        """
        message = {'ucla': [1, 2, 3]}
        self.transmitter.enqueue(message)

    def test_broadcast_enqueued(self):
        """
        Enqueued messsages broadcast in one go
        """
        pass
