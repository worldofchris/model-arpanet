import network

from arpa import Node, Display

net = network.WLAN(network.STA_IF)
display = Display()
nodename = open('nodename.txt')
name = nodename.read().rstrip()
nodename.close()
n = Node(name, net, display)
n.connect()
n.listen()
