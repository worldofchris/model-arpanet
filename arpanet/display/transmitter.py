"""
Transmitter for sending state of LEDs to nodemcu wireless nodes
"""
import socket
import json

class Transmitter:
    """Transmitter"""

    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.messages = {}
        self.sock = socket.socket(socket.AF_INET, # Internet
                                  socket.SOCK_DGRAM) # UDP

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def enqueue(self, message):
        """
        Enqueue messages for transmission
        """
        self.messages.update(message)

    def transmit(self):
        """
        Transmit messages to the IMPs
        """
        message = json.dumps(self.messages)
        self.sock.sendto(message.encode('utf-8'), (self.udp_ip, self.udp_port))
