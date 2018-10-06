"""
Message sent across network
"""

class Message:
    """
    Message
    """
    def __init__(self, dest, body):
        self.dest = dest
        self.body = body
        self.location_index = None
        self.route_nodes = None

    def send(self, origin):
        """
        Send the message from an origin node on the network.
        """
        self.route(origin)
        self.location_index = 0

    def location(self):
        """
        Get location of message on route
        """
        return self.route_nodes[self.location_index]

    def route(self, origin):
        """
        Work out the route for the message to take.  I was in two minds
        about whether to make this the responsibility of the nodes or the messages
        It's a bit of a halfway house at the moment.
        """
        routes = origin.route(self.dest)
        weights = []
        if routes:
            for route in routes:
                steps = list(reversed(route))
                weight = 0
                for i in range(len(steps)-1):
                    weight = weight + steps[i].links[steps[i+1].name].weight
                weights.append(weight)
            lowest = (weights.index(min(weights)))
            self.route_nodes = routes[lowest]

    def step(self):
        """
        Step through the route
        """
        if self.location_index is None:
            self.location_index = 0
        self.location_index += 1

    def ascii_art(self):
        """
        ASCII art representation of message
        """
        return str(self.body)
