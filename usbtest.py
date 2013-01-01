import time, sys
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

def connect():
	dev = usb.core.find(idVendor=0x16c0, idProduct=0x05dc, custom_match=match_manufacturer)
	if dev == None:
		print "No device found, exiting.."
		return
	dev.set_configuration()
	return dev

def handleInput(dev):
	if len(sys.argv) < 1:
		print "usage: python usbtest.py <on/off/read/write/onewire>"
	elif sys.argv[1] == "on":
		dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_LED_ON)
	elif sys.argv[1] == "off":
		dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_LED_OFF)
	elif sys.argv[1] == "read":
		print dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_READ_EEPROM, data_or_wLength=32).tostring()
	elif sys.argv[1] == "write":
		dev.ctrl_transfer(REQUEST_TYPE_OUT, CtrlMsg.USB_WRITE_EEPROM, data_or_wLength=sys.argv[2])
	elif sys.argv[1] == "onewire" and sys.argv[2] == "write":
		dev.ctrl_transfer(REQUEST_TYPE_OUT, CtrlMsg.USB_ONEWIRE_WRITE, int(sys.argv[3]))
def reset(dev):
	onewire_send(dev, CtrlMsg.USB_ONEWIRE_RESET)
	onewire_send(dev, CtrlMsg.USB_ONEWIRE_WRITE, 0xcc)
	onewire_send(dev, CtrlMsg.USB_ONEWIRE_WRITE, 0x44)
	time.sleep(1)
	onewire_send(dev, CtrlMsg.USB_ONEWIRE_RESET)
	onewire_send(dev, CtrlMsg.USB_ONEWIRE_WRITE, 0xcc)
	onewire_send(dev, CtrlMsg.USB_ONEWIRE_WRITE, 0xbe)
	print "Reading scratchpad"
	for i in range(9):
		onewire_send(dev, CtrlMsg.USB_ONEWIRE_READ)
	print "Reset"
	onewire_send(dev, CtrlMsg.USB_ONEWIRE_RESET)

def onewire_send(dev, msg, value = None):
	if value != None:
		dev.ctrl_transfer(REQUEST_TYPE_OUT, msg, value)
	else:
		dev.ctrl_transfer(REQUEST_TYPE_OUT, msg)
		
	time.sleep(0.01)
	res = None
	if msg in (CtrlMsg.USB_ONEWIRE_READ, CtrlMsg.USB_ONEWIRE_READ_BIT, CtrlMsg.USB_ONEWIRE_RESET):
		res = dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_READ_RESULT, data_or_wLength=32)
		print hex(res.tolist()[0])
		#time.sleep(0.01)
	return res
			
def main():
	dev = connect()
	handleInput(dev)

		
if __name__ == "__main__":
	main()
