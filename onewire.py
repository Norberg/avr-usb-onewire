import time
from CtrlMsg import CtrlMsg
from constants import *

class OneWire():
	DELAY = 0.01
	
	def __init__(self, dev):
		self.dev = dev
		self.search_state = SearchState()

	def delay(self, delay=DELAY):
		time.sleep(delay)

	def reset(self):
		self.delay()
		return self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_ONEWIRE_RESET)

	def write_byte(self, byte):
		self.delay()
		self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_ONEWIRE_WRITE, byte)
	
	def write_bit(self, bit):
		self.delay()
		if bit > 0:
			bit = 0xff
		else:
			bit = 0x00
		self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_ONEWIRE_WRITE_BIT, bit)

	def read_bytes(self, count):
		self.delay()
		self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_ONEWIRE_READ, data_or_wLength=9)
		return self.read_result(count)

	def read_bit(self):
		self.delay()
		self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_ONEWIRE_READ_BIT)
		res = self.read_result(1)
		if res > 0:
			return 1
		else:
			return 0

	def read_result(self, count):
		self.delay()
		res = self.dev.ctrl_transfer(REQUEST_TYPE_IN, CtrlMsg.USB_READ_RESULT, data_or_wLength=count)
		l =  res.tolist()
		if len(l) == 1:
			return l[0]

	def search(self):
		self.reset()
		self.write_byte(0xf0)
		new_deviation = 0
		for rom_index in xrange(64):
			b = self.read_bit()
			b_comp = self.read_bit()
			print "B" + str(rom_index), b
			print "^B" + str(rom_index), b_comp
			if b == 1 and b_comp == 1:
				continue
				#no device participating in search
				print self.search_state.rom
				raise Exception("Error, No device participating in search")
			elif b !=  b_comp:
				#devices have same bit value in current position
				self.search_state.rom[rom_index] = b	
			elif b == 0 and b_comp == 0:
				#devices have both 0 and 1 in current position
				if rom_index == self.search_state.last_deviation:
					self.search_state.rom[rom_index] = 1
				else:
					if rom_index > self.search_state.last_deviation:
						self.search_state.rom[rom_index] = 0
					elif self.search_state.rom[rom_index] == 0:
						new_deviation = rom_index
			print "Writing bit:", self.search_state.rom[rom_index]					
			self.write_bit(self.search_state.rom[rom_index])
		self.reset()
			
class SearchState():
	def __init__(self):
		self.rom = [0]*64
		self.last_deviation = 0
				

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

