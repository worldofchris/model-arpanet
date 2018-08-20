import neopixel
import machine

palette = [(255,0,0),(0,255,0),(0,0,255)]
length = 3
pin = 2

class Display:
    def __init__(self):
        self.np = neopixel.NeoPixel(machine.Pin(pin), length)

    def length(self):
        return length

    def set_light(self, light_index, palette_index):
        self.np[light_index] = palette[palette_index]
        self.np.write()

    def clear(self, write=True):
        for i in range(length):
            self.np[i] = (0, 0, 0)
        if write:
            self.np.write()
