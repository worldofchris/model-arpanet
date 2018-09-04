"""
Transmitter for sending state of LEDs to nodemcu wireless nodes
"""

class Transmitter:
    """Transmitter"""

    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.messages = []

    def enqueue(self, message):
        """
        Enqueue messages for transmission
        """
        pass
