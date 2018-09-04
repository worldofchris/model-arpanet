PALETTE = [(  0,   0,   0),
           (255,   0,   0),
           (  0, 255,   0),
           (  0,   0, 255)]

class Wired:
    def __init__(self, data_pin, palette=PALETTE):
        self.data_pin = data_pin
        self.nodes = {}
        self.strip = []
        self.palette = palette
        self.hss_on = False

    def __unicode__(self):
        chars = ""
        for light in self.strip:
            i = self.palette.index(light)
            chars += str(i)
        return chars

    def __str__(self):
        return self.__unicode__()

    def add_node(self, node_name, offset, hss_offset):
        """
        Define where in the Neopixel strip the Blinkenlights
        for a node appear.
        """
        self.nodes[node_name] = (offset, hss_offset)
        highest = max(offset, hss_offset)
        self.strip += [self.palette[0]] * (highest - len(self.strip) + 3) # MAGIC

    def set_hss_on(self, state):
        """
        Switch the High Side Switch on the wired display to route the Neopixel
        data line when the network is extended to include UCSB
        """
        self.hss_on = state
        self.strip = [self.palette[0]] * len(self.strip)

    def update(self, node_name, light_state):
        """
        Set state of lights for a given node
        """
        for i, light in enumerate(light_state):
            x = int(light or 0)
            self.strip[(self.nodes[node_name][0+int(self.hss_on)])+ i] = self.palette[x]
