import socket
import json
import time
import random

UDP_IP = "172.20.10.15"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:

	state = {'utah': [random.randint(0,2), random.randint(0,2), random.randint(0,2)]}
	MESSAGE = json.dumps(state)
	sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
	time.sleep(.5)