# a network can be created out of nodes and links
# e.g ucla can be linked to sri

# a node can have one or more links
# e.g. ucla can be linked to ucsb and sri

import unittest
from arpanet.node import Node
from arpanet.link import Link
# from unittest.mock import MagicMock, patch

class test_node(unittest.TestCase):

    def test_create_network(self):
        ucla = Node('ucla')
        sri = Node('sri')

        ucla.add_link(Link(sri, 0))
        assert ucla.links['sri'].dest.name == 'sri'
