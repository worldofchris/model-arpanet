"""
Script for the Arpanet talk
"""
from time import sleep

from arpanet.message import Message
from arpanet.network import Network

from arpanet.display.transmitter import Transmitter

UDP_IP = "192.168.0.255"
UDP_PORT = 5005

TRANS = Transmitter(UDP_IP, UDP_PORT)

NETWORK = Network([{'from':'ucla', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True},
                   {'from':'ucla', 'to': 'sig7', 'weight': 1, 'r2l': False, 'bidirectional': True},
                   {'from':'ucla', 'to': 'ucsb', 'weight': 1, 'r2l': False, 'bidirectional': True},
                   {'from':'ucsb', 'to': 'sri', 'weight': 1, 'r2l': False, 'bidirectional': True},
                   {'from':'sri', 'to': 'sds', 'weight': 1, 'r2l': False, 'bidirectional': True},
                   {'from':'sri', 'to': 'utah', 'weight': 1, 'r2l': False, 'bidirectional': True}],
                  TRANS)

NETWORK.nodes['sds'].host = True

input("Send L")
input("Are you sure?")

M = Message('sds', 5)
NETWORK.nodes['sig7'].add_message(M)
sleep(.4)
for i in range(4):
    print(i)
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)

input("Send O")
input("Are you sure?")

M = Message('sds', 5)
NETWORK.nodes['sig7'].add_message(M)
sleep(.4)
for i in range(4):
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)

input("Send G")
input("Are you sure?")

M = Message('sds', 5)
NETWORK.nodes['sig7'].add_message(M)
sleep(.4)
for i in range(4):
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)

for i in range(5):
    flash = [[3, 3, 3], [None, None, None]]
    for f in flash:
        TRANS.enqueue({'sri': f})
        TRANS.enqueue({'ucla': f})
        for j in range(5):
            TRANS.transmit()
            sleep(.01)
        sleep(.2)

# ADD UCSB

input("Add UCSB to the NETWORK")
input("Are you sure?")

NETWORK.nodes['ucla'].links['sri'].weight = 10

M = Message('sds', 4)
NETWORK.nodes['sig7'].add_message(M)
sleep(.4)
for i in range(4):
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)

input("Add UTAH to the NETWORK")
input("Are you sure?")

for j in range(3):
    m = Message('utah', j+20)
    NETWORK.nodes['sig7'].add_message(m)
    sleep(.4)
    for i in range(4):
        print(i)
        NETWORK.process()
        sleep(.4)
        NETWORK.process()
        sleep(.4)
        NETWORK.process()
        sleep(.4)
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)
    NETWORK.process()
    sleep(.4)

input("Lots of messages")
input("Are you sure?")

NETWORK.nodes['ucla'].links['sri'].weight = 1

MESSAGES = [["ucla", "utah", 4],
            ["utah", "ucla", 5],
            ["ucsb", "sri", 6],
            ["utah", "ucsb", 7]]

S = .4
for j in range(4):
    for mess in MESSAGES:
        print(mess)
        NETWORK.nodes[mess[0]].add_message(Message(mess[1], mess[2]))
        NETWORK.process()
        sleep(S)

    for i in range(3):
        NETWORK.process()
        sleep(S)
        NETWORK.process()
        sleep(S)
        NETWORK.process()
        sleep(S)
    S = S - .1

for i in range(5):
    flash = [[3, 3, 3], [None, None, None]]
    for f in flash:
        TRANS.enqueue({'sri': f})
        TRANS.enqueue({'ucla': f})
        TRANS.enqueue({'ucsb': f})
        TRANS.enqueue({'utah': f})
        for j in range(5):
            TRANS.transmit()
            sleep(.01)
        sleep(.2)
