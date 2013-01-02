import time
from CtrlMsg import CtrlMsg
from constants import *

class OneWire():
	DELAY = 0.01
	def __init__(self, dev):
		self.dev = dev

	def delay(self, delay=DELAY):
		time.sleep(delay)

	def reset(self):
		self.delay()
		return self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_ONEWIRE_RESET)

	def write_byte(self, byte):
		self.delay()
		self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_ONEWIRE_WRITE, byte)

	def read_bytes(self, count):
		self.delay()
		self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_ONEWIRE_READ, data_or_wLength=9)
		return self.read_result(count)

	def read_result(self, count):
		self.delay()
		res = self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_READ_RESULT, data_or_wLength=count)
		return res.tolist()

	def search(self):
		pass

class DS18S20():
	def __init__(self, onewire):
		self.onewire = onewire

	def read_temp(self):
		self.onewire.reset()
		self.onewire.write_byte(0xcc)
		self.onewire.write_byte(0x44)
		time.sleep(0.750)
		self.onewire.reset()
		self.onewire.write_byte(0xcc)
		self.onewire.write_byte(0xbe)
		scratchpad = self.onewire.read_bytes(9)
		self.onewire.reset()
		low = scratchpad[0]
		high = scratchpad[1]
		count_remain = scratchpad[6]
		return self.calc_temp(low, high, count_remain)
		
	def calc_temp(self, low, hi, remain):
		sign = 1
		if hi == 0xff:
			#- needed since python lack a unsigned type
			low = -(low ^ 0xff + 1) 
			sign = -1
		temp_read = (low & 0xfe) *0.5
		return sign * (temp_read - 0.25 + (16.0-remain)/16)

