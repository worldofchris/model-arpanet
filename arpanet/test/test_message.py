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

    def test_send_message_to_peer(self):
        message = Message('sri', 1)
        message.send(self.ucla)
        assert message.location == 'sri', message.location
