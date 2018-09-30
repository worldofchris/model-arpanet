"""
A network can be created out of nodes and links
e.g ucla can be linked to sri

A node can have one or more links
e.g. ucla can be linked to ucsb and sri
"""
import unittest
from unittest.mock import MagicMock

from arpanet.node import Node
from arpanet.link import Link
from arpanet.message import Message

class TestNode(unittest.TestCase):
    """Test Node"""
    def setUp(self):
        self.ucla = Node('ucla')
        self.sri = Node('sri')

    def test_create_network(self):
        """Test create network"""

        assert self.ucla.__str__() == 'ucla-->[]', self.ucla.__str__()
        self.ucla.add_link(Link(self.sri, 0))
        assert self.ucla.links['sri'].dest.name == 'sri'
        assert self.ucla.__str__() == "ucla-->['sri']", self.ucla.__str__()

    def test_add_message_to_buffer(self):
        """
        Add a message to the three slot buffer on the node.
        The slots correspond to LEDS on the IMP models.
        """

        message = Message('utah', 1)
        self.ucla.add_message(message)
        assert self.ucla.buffer_contents(0) == [message, None, None], self.ucla.buffer_contents(0)

    def test_move_message_through_buffer(self):
        """
        A message moves from left to right through the buffer
        as messages to its right are processed.
        """

        message = Message('utah', 1)
        self.ucla.add_message(message)
        message_2 = Message('utah', 2)
        self.ucla.add_message(message_2, 1)
        self.ucla.process()
        assert self.ucla.buffer_contents(0) == [None, message, None], self.ucla.buffer_contents(0)
        assert self.ucla.buffer_contents(1) == [None, message_2, None], self.ucla.buffer_contents(1)

    def test_add_message_to_rl_buffer(self):
        """
        When we have messages going in opposite directions the effect is a bit meh if they
        always go right to left on the node.  So I'm adding a second buffer for messages
        going the other way which can then be ORed together onto the LEDs.
        """

        message = Message('utah', 1)
        self.ucla.add_message(message, 1)
        assert self.ucla.buffer_contents(1) == [message, None, None], self.ucla.buffer_contents(1)

    def test_message_gets_sent_when_leaves_buffer(self):
        """
        When a message gets to the end of the buffer it should be sent to the
        next node on its route

        Unless this is the last node on the route...
        """

        self.ucla.add_link(Link(self.sri, 0))
        message = Message('sri', 1)
        message.route(self.ucla)
        self.sri.add_message = MagicMock()
        self.ucla.add_message(message)
        for _ in range(self.ucla.buffer_length):
            self.ucla.process()
        assert self.sri.add_message.call_count == 1
        assert self.ucla.buffer_contents(0) == [None, None, None], self.ucla.buffer_contents(0)

    def test_message_leaves_destination_node(self):
        """
        Messages should be passed off (to the host?) once they reach their destination
        """
        message = Message('ucla', 1)
        self.ucla.add_message(message)

        for _ in range(self.ucla.buffer_length):
            self.ucla.process()
        assert self.ucla.buffer_contents(0) == [None, None, None], self.ucla.buffer_contents(0)
        assert message.route_nodes is not None

    def test_add_message_to_buffer_when_full(self):
        """
        Adding a message to the buffer when it is full will fail
        Want some way of showing this so we can update the display
        accordingly - e.g. turn the LEDs red.

        Sending node can then decide to route the message a different way.
        """
        message = Message('ucla', 1)
        message.route(self.ucla)
        assert self.ucla.add_message(message) == True
        assert self.ucla.add_message(message) == False

    def test_display_state_change(self):
        """
        When state changes let the display know so it can be updated
        """
        display = MagicMock()
        self.ucla.display = display
        self.ucla.process()
        self.ucla.display.update.assert_called_with('ucla', [None, None, None])

    def test_combine_both_buffers_in_display(self):
        """
        The display should show messages travelling in both directions
        """
        display = MagicMock()
        self.ucla.display = display
        message = Message('utah', 1)
        self.ucla.add_message(message)
        message_2 = Message('utah', 2)
        self.ucla.add_message(message_2, 1)
        self.ucla.display.update.assert_called_with('ucla', [1, None, 2])

    def test_link_to_rl_buffer(self):
        """
        Links can indicate whether messages sent via them should be
        added to the right to left or the left to right buffer.
        """
        message = Message('sri', 1)
        self.sri.add_message = MagicMock()
        self.ucla.add_link(Link(self.sri, 0, True))
        self.ucla.add_message(message)
        for _ in range(self.ucla.buffer_length):
            self.ucla.process()
        self.sri.add_message.assert_called_with(message, 1)

    def test_send_to_non_existent_node(self):
        """
        Fail gracefully if there is nowhere to route the message
        """
        message = Message('foo', 1)
        message.route(self.ucla)
        assert message.route_nodes == None, message.route_nodes

    def test_dont_go_round_in_circles(self):
        """
        If there is a route back to the origin, check we don't end up going round in circles
        """
        NODES = ['ucla',
                 'ucsb',
                 'sri',
                 'utah']

        LINKS = [('ucla', 'sri', 1),
                 ('ucla', 'ucsb', 1),
                 ('ucsb', 'sri', 1),
                 ('sri', 'utah', 1),
                 ('utah', 'sri', 1),
                 ('sri', 'ucsb', 1),
                 ('sri', 'ucla', 1),
                 ('ucsb', 'ucla', 1)]

        network = {}
        for node in NODES:
            network[node] = Node(node)

        for link in LINKS:
            network[link[0]].add_link(Link(network[link[1]], link[2]))

        message = Message('utah', 1)
        message.route(network['ucla'])
        assert message.route_nodes[0] == network['utah']

    def test_ascii_version_of_node(self):
        """
        To make it easier to inspect the network we want to be able to see what the
        contents of each node's buffers is
        """
        self.ucla.add_message(Message('foo', 1))
        assert self.ucla.ascii_art() == "[1--][---]", self.ucla.ascii_art()

    def test_get_messages(self):
        messages = [Message('foo', 1),
                    Message('foo', 2),
                    Message('foo', 3)]
        self.ucla.add_message(messages[0])
        self.ucla.add_message(messages[1], 1)
        self.ucla.process()
        self.ucla.add_message(messages[2])

        for message in self.ucla.messages():
            assert message in messages

        assert messages[0] in self.ucla.messages(0)
        assert messages[1] in self.ucla.messages(1)
