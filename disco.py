import socket
import json
import time
import random

UDP_IP = "192.168.0.255"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:

	state = {'mitr': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'rand': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'cmu': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'stan': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'rand': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'harv': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'case': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'mit': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'mitre': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'rand': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'ames': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'burr': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'linc': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'bbn1': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)],
			 'bbn0': [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)]}
	MESSAGE = json.dumps(state)
	sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
	time.sleep(.5)

