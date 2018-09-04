"""
Node display on Nodemcu
"""

class Wireless:
    """Display"""
    def __init__(self, name, transmitter):
        self.name = name
        self.transmitter = transmitter

    def update(self, state):
        """Enqueue a message at the transmitter to send to the display"""
        message = {self.name: state}
        self.transmitter.enqueue(message)
