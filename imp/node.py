import socket
import ujson

ssid = '-'
password = '-'
UDP_PORT = 5005
delay = 2000

class Node:
    def __init__(self, name, network=None, display=None):
        self.name = name
        self.connection_status = False
        if network is not None:
            self.network = network
        else:
            self.network = network.WLAN(network.STA_IF)

        self.network.active(True)
        self.network.connect(ssid, password)

        if display is not None:
            self.display = display
        else:
            self.display = Display()

        self.display.clear()

    def connect(self):

        i = 0
        j = 0
        while not self.network.isconnected():
            j+= 1
            if j >= delay:
                j = 0
                self.display.clear(False)
                self.display.set_light(i, 0)
                i+= 1
                if i >= self.display.length():
                    i = 0

        UDP_IP = self.network.ifconfig()[0]
        self.sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, UDP_PORT))

        for i in range(self.display.length()):
            self.display.set_light(i, 0)

        self.connection_status = True

    def connected(self):
        return self.connection_status

    def listen(self):

        while self.connected():
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            print ("received message:", data)
            try:
                body = ujson.loads(data)
                lights = (body[self.name])
                for i in range(len(lights)):
                    self.display.set_light(i, lights[i])
            except KeyError:
                pass
