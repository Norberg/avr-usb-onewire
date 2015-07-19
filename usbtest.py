import time, sys
import usb.core
import usb.util
from CtrlMsg import CtrlMsg
from constants import *
import onewire

def match_manufacturer(dev):
	if usb.util.get_string(dev, dev.iManufacturer) == "pthread.se":
		return True
	return False

def connect():
	dev = usb.core.find(idVendor=0x16c0, idProduct=0x05dc, custom_match=match_manufacturer)
	if dev == None:
		print("No device found, exiting..")
		return
	dev.set_configuration()
	return dev

def handleInput(dev):
	ow = onewire.OneWire(dev)
	sensor = onewire.DS18S20(ow)
	if len(sys.argv) < 1:
		print_usage()
	elif sys.argv[1] == "on":
		dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_LED_ON)
	elif sys.argv[1] == "off":
		dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_LED_OFF)
	elif sys.argv[1] == "read":
		print(dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_READ_EEPROM, data_or_wLength=32).tostring())
	elif sys.argv[1] == "write":
		dev.ctrl_transfer(REQUEST_TYPE_OUT, CtrlMsg.USB_WRITE_EEPROM, data_or_wLength=sys.argv[2])
	elif sys.argv[1] == "onewire" and sys.argv[2] == "write":
		dev.ctrl_transfer(REQUEST_TYPE_OUT, CtrlMsg.USB_ONEWIRE_WRITE, int(sys.argv[3]))
	elif sys.argv[1] == "onewire" and sys.argv[2] == "get_temp":
		print(sensor.read_temp())
	elif sys.argv[1] == "onewire" and sys.argv[2] == "search":
		print(ow.search())
	else:
		print_usage()

def print_usage():
		print("usage: python usbtest.py <on/off/read/write/onewire>")


def main():
	dev = connect()
	handleInput(dev)


if __name__ == "__main__":
	main()
