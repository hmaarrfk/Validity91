permissions:
	lsusb -d 138a: | awk -F '[^0-9]+' '{ print "/dev/bus/usb/" $$2 "/" $$3 }' | xargs -r sudo chmod a+rw

.PHONY: permissions
