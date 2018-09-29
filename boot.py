"""
Listen for messages at boot
"""

from imp.display import Display
from imp.node import Node
import network

net = network.WLAN(network.STA_IF)
display = Display()
nodename = open('nodename.txt')
name = nodename.read().rstrip()
nodename.close()
wifi_creds = open('wifi.txt')
wifi = wifi_creds.read().rstrip().split(',')
wifi_creds.close()
n = Node(name, wifi, net, display)
print("Connecting to the model arpanet as:", name)
n.connect()
n.listen()
