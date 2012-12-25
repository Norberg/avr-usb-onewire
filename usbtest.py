import sys
import usb.core
from CtrlMsg import CtrlMsg

DEFAULT_REQUEST_TYPE = 0x40


def main():
	dev = usb.core.find(idProduct=0x05dc)
	dev.set_configuration()
	if len(sys.argv) < 1:
		print "usage: python usbtest.py <on/off>"
	elif sys.argv[1] == "on":
		dev.ctrl_transfer(DEFAULT_REQUEST_TYPE, CtrlMsg.USB_LED_ON)
	elif sys.argv[1] == "off":
		dev.ctrl_transfer(DEFAULT_REQUEST_TYPE, CtrlMsg.USB_LED_OFF)

if __name__ == "__main__":
	main()
