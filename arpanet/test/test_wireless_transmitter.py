"""
Broadcast UDP messages to the wireless nodemcu IMPs
"""
import unittest
from unittest.mock import patch, MagicMock
from arpanet.display.transmitter import Transmitter

PORT = 5005
ADDR = "172.20.10.15"

class TestWirelessTransmitter(unittest.TestCase):
    """Test wireless transmitter"""
    def setUp(self):
        self.transmitter = Transmitter(ADDR, PORT)

    def test_enqueue_messages(self):
        """
        Nodes can enqueue messages which are then broadcast in one
        go by the transmitter.
        """
        message = {'ucla': [1, 2, 3]}
        self.transmitter.enqueue(message)
        assert self.transmitter.messages['ucla'] == message['ucla'], self.transmitter.messages['ucla']

    @patch('socket.socket')
    def test_broadcast_enqueued(self, socket):
        """
        Transmit enqueued messsages in one go
        """
        mock_socket = MagicMock()
        socket.return_value = mock_socket

        messages = [{'ucla': [1, 2, 3]},
                    {'sri':  [4, 5, 6]},
                    {'ucla': [7, 8, 9]}]

        mocked_socket_transmitter = Transmitter(ADDR, PORT)


        for message in messages:
            mocked_socket_transmitter.enqueue(message)

        mocked_socket_transmitter.transmit()
        transmission = b'{"ucla": [7, 8, 9], "sri": [4, 5, 6]}'
        ip = ('172.20.10.15', 5005)
        mock_socket.sendto.assert_called_with(transmission, ip)
