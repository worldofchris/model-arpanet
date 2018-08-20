# Model ARPANET IMPs

Blinkenlights for the nodemcu model ARPANET IMPs

## Dependencies

The model ARPANET IMPs code requires [Python 3](https://www.python.org/), tested with Python 3.6.5 for the host and [MicroPython](https://micropython.org/) for the [nodemcu](http://nodemcu.com/index_en.html) IMPs. 

The IMP is wired up to three [neopixels](https://www.adafruit.com/product/1938):  

![Nodemcu IMPs](assets/imps.jpg)

L-R Prototype breadboard build, build soldered on to protoboard, soldered build mounted in an ABS project box.

To get started, install the Python dependencies with:

	make develop

## Configuring the IMP

First erase the flash on the nodemcu:


	make erase

Then flash with the [MicroPython firmware](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#getting-the-firmware):

	make flash
	
## Running the tests

	make test

## Deploying to a nodemcu

	make deploy
