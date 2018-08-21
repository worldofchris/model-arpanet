# a message can be sent to a destination node via the network

# you can tell where a message is in the network

import unittest
from arpanet.node import Node
from arpanet.message import Message
# from unittest.mock import MagicMock, patch

class test_message(unittest.TestCase):

    def setUp(self):
        self.ucla = Node('ucla')
        self.sri = Node('sri')

        self.ucla.add_link(self.sri)

        self.utah = Node('utah')
        self.sri.add_link(self.utah)

    def test_send_message_to_peer(self):
        message = Message('sri', 1)
        message.send(self.ucla)
        assert message.location == 'sri', message.location

    def test_send_message_to_non_peer(self):
        message = Message('utah', 1)
        route = message.send(self.ucla)
        assert message.location == 'utah', message.location

    def test_send_with_two_routes(self):
        ucsb = Node('ucsb')
        self.ucla.add_link(ucsb)
        ucsb.add_link(self.sri)

        message = Message('utah', 1)
        route = message.send(self.ucla)
        assert message.location == 'utah', message.location
