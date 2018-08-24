"""
A node on the model network.
"""

from collections import deque

class Node:
    """ A node on the model network """
    def __init__(self, name):
        self.name = name
        self.links = {}
        self.load = 0
        self.buffer_length = 3
        self.buffer = deque([None] * (self.buffer_length + 1))

    def add_link(self, link):
        """Add a link to a peer node"""
        self.links[link.dest.name] = link

    def add_message(self, message):
        """
        Add a message to the buffer for processing
        """
        if self.buffer[0] is not None:
            return False
        self.buffer[0] = message
        return True

    def buffer_contents(self):
        """
        What's in the buffer?
        """
        return list(self.buffer)[0:self.buffer_length]

    def process(self):
        """
        Process any messages in the buffer
        """
        self.buffer.rotate()
        message = self.buffer[-1]
        if message is not None:
            location = message.route_nodes.index(self)-1
            if location >= 0:
                message.route_nodes[location].add_message(message)
            self.buffer[-1] = None

    def route(self, destination):
        """
        Find all routes to a destination
        """
        if destination == self.name:
            return[[self]]
        try:
            return[[self.links[destination].dest, self]]
        except KeyError:
            routes = []
            for link in self.links:
                # These variable names are terrible
                rest = self.links[link].dest.route(destination)
                for r in rest:
                    r.append(self)
                    routes.append(r)
            return routes
