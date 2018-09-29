"""
A message can be sent to a destination node via the network
You can tell where a message is in the network
"""

import unittest
from arpanet.node import Node
from arpanet.message import Message
from arpanet.link import Link
# from unittest.mock import MagicMock, patch

class TestMessage(unittest.TestCase):
    """Test Message"""
    def setUp(self):
        self.ucla = Node('ucla')
        self.sri = Node('sri')

        self.ucla.add_link(Link(self.sri, 1))

        self.utah = Node('utah')
        self.sri.add_link(Link(self.utah, 1))

    def test_send_message_to_origin(self):
        """Test a node can send a message to itself"""
        message = Message('ucla', 1)
        message.send(self.ucla)
        assert message.location().name == 'ucla', message.location

    def test_send_message_to_peer(self):
        """Test send message to peer"""
        message = Message('sri', 1)
        message.send(self.ucla)
        assert message.location().name == 'sri', message.location

    def test_send_message_to_non_peer(self):
        """Test send message to non peer"""
        message = Message('utah', 1)
        message.send(self.ucla)
        assert message.location().name == 'utah', message.location

    def test_send_with_two_routes(self):
        """Test send with two routes"""
        ucsb = Node('ucsb')
        self.ucla.add_link(Link(ucsb, 1))
        ucsb.add_link(Link(self.sri, 1))

        message = Message('utah', 1)
        message.send(self.ucla)
        assert message.location().name == 'utah', message.location

    def test_send_by_least_busy_route(self):
        """Test send by least busy route"""
        ucsb = Node('ucsb')
        self.ucla.add_link(Link(ucsb, 1))
        ucsb.add_link(Link(self.sri, 1))
        self.ucla.links['sri'].weight = 10

        message = Message('utah', 1)
        message.send(self.ucla)
        assert message.route_nodes == [self.utah, self.sri, ucsb, self.ucla]

    def test_send_back_from_peer(self):
        """Test send back from peer"""
        message = Message('ucla', 1)
        self.sri.add_link(Link(self.ucla, 1))
        message.send(self.sri)
        assert message.location().name == 'ucla', message.location

    def test_send_back_from_non_peer(self):
        """Test send back from non peer"""
        message = Message('ucla', 1)
        self.sri.add_link(Link(self.ucla, 1))
        self.utah.add_link(Link(self.sri, 1))
        message.send(self.utah)
        assert message.location().name == 'ucla', message.location

    def test_step_message_along_route(self):
        """
        In order to display the progress of a message on Blinkenlights etc
        we want to be able to move the message along the route a step (node/light) at a time
        updating the display as we go
        """
        message = Message('utah', 1)
        message.route(self.ucla)
        message.step()
        location = message.location()
        assert location.name == 'sri'

    def test_ascii_representation_of_message(self):

        message = Message('utah', 1)
        assert message.ascii_art() == '1'
