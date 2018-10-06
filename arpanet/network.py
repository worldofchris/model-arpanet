"""
A collection of nodes
"""
from arpanet.node import Node
from arpanet.link import Link
from arpanet.display.wireless import Wireless


class Network:
    """
    Group nodes into a network and provide a way of stepping messages
    through the network
    """

    def __init__(self, network, transmitter=None):
        self.nodes = {}
        self.transmitter = transmitter
        if self.transmitter is None:
            display = None
        else:
            display = Wireless(self.transmitter)
        for node in network:
            if not node['from'] in self.nodes:
                from_node = Node(node['from'], display)
                self.nodes[from_node.name] = from_node
            else:
                from_node = self.nodes[node['from']]
            if not node['to'] in self.nodes:
                to_node = Node(node['to'], display)
                self.nodes[to_node.name] = to_node
            else:
                to_node = self.nodes[node['to']]
            self.nodes[node['from']].add_link(Link(to_node, node['weight'], node['r2l']))
            if node['bidirectional']:
                self.nodes[node['to']].add_link(Link(from_node, node['weight'], not node['r2l']))

    def process(self):
        """
        Process all the messages in the network
        """
        processed = []
        for node in self.nodes:
            for i in range(2): # MAGIC
                messages = self.nodes[node].messages(i)
                if not any(message in messages for message in processed):
                    self.nodes[node].process(i)
                    processed.extend(messages)
                self.nodes[node].update_display()


    def ascii_art(self):
        """
        ASCII art representation of network
        """
        ascii_art = ''
        for node in self.nodes:
            ascii_art += node + ':' + self.nodes[node].ascii_art() + ' '

        return ascii_art.strip()
