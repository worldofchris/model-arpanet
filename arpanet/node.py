class Node:
    def __init__(self, name):
        self.name = name
        self.links = {}

    def add_link(self, destination):
        self.links[destination.name] = destination

    def route(self, destination):
        try:
            return[self.links[destination].name, self.name]
        except KeyError:
            for link in self.links:
                rest = self.links[link].route(destination)
                rest.append(self.name)
                return rest
