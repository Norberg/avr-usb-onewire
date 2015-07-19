import usb
import usb.util

def match_manufacturer(dev):
	if usb.util.get_string(dev, dev.iManufacturer) == "pthread.se":
		return True
	return False


dev = usb.core.find(idVendor=0x16c0, custom_match=match_manufacturer)
dev.set_configuration()
print(usb.util.get_string(dev, dev.iManufacturer))

