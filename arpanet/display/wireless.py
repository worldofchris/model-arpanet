"""
Node display on Nodemcu
"""
from time import sleep

class Wireless:
    """Display"""
    def __init__(self, transmitter):
        self.transmitter = transmitter

    def update(self, node_name, light_state):
        """Enqueue a message at the transmitter to send to the display"""
        message = {node_name: light_state}
        self.transmitter.enqueue(message)
        for i in range(5):
	        self.transmitter.transmit()
	        sleep(.001)