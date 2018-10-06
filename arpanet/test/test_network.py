"""
Test behaviour of nodes and messages routed through them when combined
together into a network
"""

import unittest
from unittest.mock import MagicMock

from arpanet.network import Network
from arpanet.message import Message

class TestNetwork(unittest.TestCase):
    """
    Test the network
    """
    @staticmethod
    def test_two_node_network():
        """
        Make a simple two node network with a bidirectional link
        """
        net = Network(
            [{'from':'ucla', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True}])
        assert net.nodes['ucla'].name == 'ucla'
        assert net.nodes['sri'].name == 'sri'
        assert net.nodes['ucla'].links['sri'].dest.name == 'sri'
        assert net.nodes['ucla'].links['sri'].right_to_left is False
        assert net.nodes['ucla'].links['sri'].weight == 1
        assert net.nodes['sri'].links['ucla'].dest.name == 'ucla'
        assert net.nodes['sri'].links['ucla'].right_to_left is True
        assert net.nodes['sri'].links['ucla'].weight == 1

    @staticmethod
    def test_one_to_many_links():
        """
        Add more than one link to a node
        """
        net = Network(
            [{'from':'ucla', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True},
             {'from':'ucla', 'to': 'ucsb', 'weight': 1, 'r2l': False, 'bidirectional': True}])
        assert net.nodes['ucla'].__str__() == "ucla-->['sri', 'ucsb']", net.nodes['ucla'].__str__()
        assert net.nodes['sri'].__str__() == "sri-->['ucla']", net.nodes['sri'].__str__()

    @staticmethod
    def test_process_message():
        """
        So that the lights representing messages appear to move one light at a time
        we don't want them to get processed twice in one go.

        e.g. if a message bound for utah is on ucla [_ _ M] and it gets processed off to sri
        [M _ _] if ucla is does its processing before sri then when it's sri's turn then it will
        move again [_ M _] and the message will appear to have jumped two steps and not one
        """
        net = Network(
            [{'from':'ucla', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True}])
        net.nodes['ucla'].add_message(Message('sri', 1))
        for i in range(5):
            net.process()
        assert net.nodes['sri'].ascii_art() == '[--1][---]', net.nodes['sri'].ascii_art()

    @staticmethod
    def test_ascii_art():
        """
        ASCII art representation of the network state
        """
        net = Network(
            [{'from':'ucla', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True},
             {'from':'ucsb', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True}])
        net.nodes['ucla'].add_message(Message('sri', 1))
        net.nodes['ucsb'].add_message(Message('sri', 1))
        assert net.ascii_art() == 'ucla:[1--][---] sri:[---][---] ucsb:[1--][---]', net.ascii_art()

    @staticmethod
    def test_process_messages():
        net = Network(
            [{'from':'ucla', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True},
             {'from':'ucsb', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True}])
        net.nodes['ucla'].add_message(Message('sri', 1))
        net.nodes['ucsb'].add_message(Message('sri', 2))
        for i in range(5):
            net.process()
        assert net.ascii_art() == 'ucla:[---][---] sri:[-21][---] ucsb:[---][---]', net.ascii_art()

    @staticmethod
    def test_process_messages_to_ways():
        net = Network(
            [{'from':'ucla', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True},
             {'from':'ucsb', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True}])
        net.nodes['ucla'].add_message(Message('sri', 1))
        # net.nodes['ucsb'].add_message(Message('sri', 2))
        net.nodes['sri'].add_message(Message('ucla', 3), 1)
        for i in range(5):
            net.process()
        assert net.ascii_art() == 'ucla:[---][--3] sri:[--1][---] ucsb:[---][---]', net.ascii_art()

    @staticmethod
    def test_network_with_wireless_displays():
        """
        Can we attach wireless displays to the network?
        """
        trans = MagicMock()
        net = Network(
            [{'from':'ucla', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True}],
            trans)
        