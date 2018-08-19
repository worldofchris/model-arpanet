import network

from arpa import Node, Display

net = network.WLAN(network.STA_IF)
display = Display()
n = Node("utah", net, display)
n.connect()
n.listen()
