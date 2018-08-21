class Node:
    def __init__(self, name):
        self.name = name
        self.links = {}

    def add_link(self, destination):
        self.links[destination.name] = destination

    def route(self, destination):
        return[self.links[destination].name, self.name]
