from imp.node import Node
from imp.display import Display
import socket
import unittest
import json
from unittest.mock import MagicMock, patch

class test_node(unittest.TestCase):

    @patch('socket.socket')
    def test_connect_to_network(self, socket):
        # it searches for a network to connect to

        network = MagicMock()
        network.active = MagicMock()
        network.connect = MagicMock()
        network.isconnected = MagicMock()
        connection_status = [False, False, True]
        network.isconnected.side_effect = connection_status
        display = Display()
        display.set_light = MagicMock()
        display.clear = MagicMock()
        mock_socket = MagicMock()
        socket.return_value = mock_socket

        node = Node('utah', network, display)
        assert node.display.clear.call_count == 1
        node.connect()
        assert network.active.call_count == 1
        assert network.connect.call_count == 1
        assert network.isconnected.call_count == len(connection_status)
        assert node.display.set_light.call_count == len(connection_status)
        assert mock_socket.bind.call_count == 1

    # it recognises itself in a broadcast message
    @patch('socket.socket')
    def test_recv(self, socket):

        state = {'utah': [1,2,3]}
        message = json.dumps(state)

        network = MagicMock()
        display = MagicMock()
        mock_socket = MagicMock()
        mock_socket.recvfrom = MagicMock(return_value=(message, None))
        socket.return_value = mock_socket

        node = Node('utah', network, display)
        node.connected = MagicMock()
        node.connected.side_effect = [True, False]
        node.connect()
        node.listen()
        assert node.display.set_light.call_count == 4, node.display.set_light.call_count

    # it ignores messages that it doesn't figure in
    @patch('socket.socket')
    def test_recv(self, socket):

        state = {'sri': [1,2,3]}
        message = json.dumps(state)

        network = MagicMock()
        display = MagicMock()
        mock_socket = MagicMock()
        mock_socket.recvfrom = MagicMock(return_value=(message, None))
        socket.return_value = mock_socket

        node = Node('utah', network, display)
        node.connected = MagicMock()
        node.connected.side_effect = [True, False]
        node.connect()
        node.listen()
        assert node.display.set_light.call_count == 1, node.display.set_light.call_count

if __name__ == '__main__':
    unittest.main()