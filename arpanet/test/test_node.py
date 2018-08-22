"""
A network can be created out of nodes and links
e.g ucla can be linked to sri

A node can have one or more links
e.g. ucla can be linked to ucsb and sri
"""
import unittest
from arpanet.node import Node
from arpanet.link import Link

class TestNode(unittest.TestCase):
    """Test Node"""
    def setUp(self):
        self.ucla = Node('ucla')
        self.sri = Node('sri')

    def test_create_network(self):
        """Test create network"""

        self.ucla.add_link(Link(self.sri, 0))
        assert self.ucla.links['sri'].dest.name == 'sri'
