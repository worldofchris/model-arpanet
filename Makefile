SRC := arpa.py boot.py
PORT := /dev/tty.SLAB_USBtoUART

install: $(SRC)
	for FILE in $(SRC) ; do \
		ampy --port $(PORT) put $$FILE ; \
	done
