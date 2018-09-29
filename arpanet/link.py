class Link:
    def __init__(self, dest, weight, right_to_left=False):
        self.dest = dest
        self.weight = weight
        self.right_to_left = right_to_left
