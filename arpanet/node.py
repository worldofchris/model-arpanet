class Node:
    def __init__(self, name):
        self.name = name
        self.links = {}
        self.load = 0

    def add_link(self, link):
        self.links[link.dest.name] = link

    def route(self, destination):
        try:
            return[[self.links[destination].dest, self]]
        except KeyError:
            routes = []
            for link in self.links:
                # These variable names are terrible
                rest = self.links[link].dest.route(destination)
                for r in rest:
                    r.append(self)
                    routes.append(r)
            return routes
