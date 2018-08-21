class Message:
    def __init__(self, dest, body):
        self.dest = dest
        self.body = body
        self.location = None
        self.route = None

    def send(self, origin):
        self.route = origin.route(self.dest)
        self.location = self.route[0]
