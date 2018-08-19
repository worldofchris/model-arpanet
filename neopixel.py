# Dummy library to stand in for the micropython neopixel lib so we can test calls to it

class NeoPixel:
	def __init__(self, pin, length):
		pass

	def __setitem__(self, key):
		pass
