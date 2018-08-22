class Message:
    def __init__(self, dest, body):
        self.dest = dest
        self.body = body
        self.location = None
        self.route = None

    def send(self, origin):
        routes = origin.route(self.dest)
        weights = []  

        for route in routes:
            steps = list(reversed(route))
            weight = 0
            for i in range(len(steps)-1):
                weight = weight + steps[i].links[steps[i+1].name].weight
            weights.append(weight)
        lowest = (weights.index(min(weights)))
        self.route = routes[lowest]
        self.location = self.route[0].name
        return self.route
