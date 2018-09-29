"""
WIFI part of the Model Arpanet
"""

from imp.display import Display
import socket
import ujson

UDP_PORT = 5005
DELAY = 2000

class Node:
    """
    A wifi model of an Arpanet IMP
    """
    def __init__(self, name, wifi, network=None, display=None):
        self.name = name
        self.connection_status = False
        self.ssid = wifi[0]
        self.password = wifi[1]
        self.sock = None
        if network is not None:
            self.network = network
        else:
            self.network = network.WLAN(network.STA_IF)

        self.network.active(True)
        self.network.config(dhcp_hostname=self.name)
        self.network.connect(self.ssid, self.password)

        if display is not None:
            self.display = display
        else:
            self.display = Display()

        self.display.clear()

    def connect(self):
        """
        Connect to the WIFI network
        """
        print("connect")
        i = 0
        j = 0
        while not self.network.isconnected():
            j += 1
            if j >= DELAY:
                print("connecting...")
                j = 0
                self.display.clear(False)
                self.display.set_light(i, 0)
                i += 1
                if i >= self.display.length():
                    i = 0

        udp_ip = self.network.ifconfig()[0]
        self.sock = socket.socket(socket.AF_INET, # Internet
                                  socket.SOCK_DGRAM) # UDP
        self.sock.bind((udp_ip, UDP_PORT))

        for i in range(self.display.length()):
            self.display.set_light(i, 0)

        self.connection_status = True

    def connected(self):
        """
        Are we connected to the WIFI network?
        """
        return self.connection_status

    def listen(self):
        """
        Listen for updates to the blinkenlights
        """
        while self.connected():
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            print("received message:", data)
            try:
                body = ujson.loads(data)
                lights = (body[self.name])
                for i in range(len(lights)):
                    print("setting light {0} to {1}".format(i, lights[i]))
                    self.display.set_light(i, lights[i])
            except KeyError:
                print("hostname {0} not found in message".format(self.name))
