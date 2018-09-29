"""
A node on the model network.
"""

from collections import deque
from operator import add

class Node:
    """ A node on the model network """
    def __init__(self, name, display=None):
        self.name = name
        self.links = {}
        self.load = 0
        self.buffer_length = 3
        self.buffer = [deque([None] * (self.buffer_length + 1)),
                       deque([None] * (self.buffer_length + 1))]
        self.display = display

    def __unicode__(self):
        return '{}-->{}'.format(self.name, list(self.links.keys()))

    def __str__(self):
        return self.__unicode__()

    def add_link(self, link):
        """Add a link to a peer node"""
        self.links[link.dest.name] = link

    def add_message(self, message, buffer=0):
        """
        Add a message to the buffer for processing
        """
        message.route(self)
        if self.buffer[buffer][0] is not None:
            return False
        self.buffer[buffer][0] = message
        self.update_display()
        return True

    def buffer_contents(self, buffer_index):
        """
        What's in the buffer?  We have two, one for showing
        messages going one way, and one for going the other.
        """
        return list(self.buffer[buffer_index])[0:self.buffer_length]

    def process(self):
        """
        Process any messages in the buffer
        """

        for i, buffer in enumerate(self.buffer):
            buffer.rotate()
            message = buffer[-1]
            if message is not None:
                try:
                    location = message.route_nodes.index(self)-1
                except ValueError:
                    location = 0
                if location >= 0:
                    right_to_left = int(self.links[message.route_nodes[location].name].right_to_left)
                    if message.route_nodes[location].add_message(message, right_to_left):
                        buffer[-1] = None
                    else:
                        buffer.rotate(-1)
                else:
                    buffer[-1] = None
        self.update_display()

    def update_display(self):

        def light(message):
            if message is None:
                return 0
            return message.body

        lights_1 = [light(i) for i in self.buffer_contents(0)]
        lights_2 = list(reversed([light(i) for i in self.buffer_contents(1)]))
        all_lights = list(map(add, lights_1, lights_2))

        if self.display is not None:
            self.display.update(self.name, [None if l == 0 else l for l in all_lights])

    def route(self, destination, depth=0):
        """
        Find all routes to a destination
        """
        depth += 1
        if depth > 10:
            """
            The routing algorthim will get stuck in an endless loop so until
            it is re-written to be less dumb I'm just cutting it off after a fixed
            number of recurrsions.
            """
            return[[]]
        if destination == self.name:
            return[[self]]
        try:
            return[[self.links[destination].dest, self]]
        except KeyError:
            routes = []
            for link in self.links:
                # These variable names are terrible
                rest = self.links[link].dest.route(destination, depth)
                for r in rest:
                    r.append(self)
                    routes.append(r)
            return routes

    def ascii_art(self):
        """
        ASCII art representation of buffers
        """
        ascii_art = ''
        for i in range(2):
            ascii_art += '['
            buffer = self.buffer_contents(i)
            for message in buffer:
                if message is None:
                    ascii_art += '-'
                else:
                    ascii_art += message.ascii_art()
            ascii_art += ']'
        return ascii_art

    def messages(self):
        """
        Get messages on node
        """
        messages = []
        for i in range(2):
            for message in self.buffer_contents(i):
                if message is not None:
                    messages.append(message)

        return messages
