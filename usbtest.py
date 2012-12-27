import sys
import usb.core
import usb.util
from CtrlMsg import CtrlMsg

REQUEST_TYPE_IN = usb.util.build_request_type(usb.util.CTRL_IN,
                                                   usb.util.CTRL_TYPE_VENDOR,
                                                   usb.util.CTRL_RECIPIENT_DEVICE)
REQUEST_TYPE_OUT = usb.util.build_request_type(usb.util.CTRL_OUT,
                                                   usb.util.CTRL_TYPE_VENDOR,
                                                   usb.util.CTRL_RECIPIENT_DEVICE)
def match_manufacturer(dev):
	if usb.util.get_string(dev,126, dev.iManufacturer) == "pthread.se":
		return True
	return False

def main():
	dev = usb.core.find(idVendor=0x16c0, idProduct=0x05dc, custom_match=match_manufacturer)
	if dev == None:
		print "No device found, exiting.."
		return
	dev.set_configuration()
	if len(sys.argv) < 1:
		print "usage: python usbtest.py <on/off/read/write>"
	elif sys.argv[1] == "on":
		dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_LED_ON)
	elif sys.argv[1] == "off":
		dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_LED_OFF)
	elif sys.argv[1] == "read":
		print dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_READ_EEPROM, data_or_wLength=32).tostring()
	elif sys.argv[1] == "write":
		dev.ctrl_transfer(REQUEST_TYPE_OUT, CtrlMsg.USB_WRITE_EEPROM, data_or_wLength=sys.argv[2])

if __name__ == "__main__":
	main()
