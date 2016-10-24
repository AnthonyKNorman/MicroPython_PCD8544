#  PCD8544.py

from machine import Pin, SPI
from array import array
import time

class PCD8544():
	def __init__(self, rst=14, ce=13, dc=12, dout=0, din=5, clk=4):
		self._rst = Pin(rst, Pin.OUT)   	# 14
		self._ce = Pin(ce, Pin.OUT)    		# 13
		self._ce.high()
		self._dc = Pin(dc, Pin.OUT)    		# 12
		self._dc.high()	
		
		self._dout = dout					# 0	MISO - not connected
		self._din = din						# 5 MOSI
		self._clk = clk						# 4 SCLK
		self._row = 0
		self._col = 0
		self._x = 0
		self._y = 0
		self.clear()

		# SPI

		self._spi = SPI(baudrate=100000, polarity=1, phase=0, sck=Pin(self._clk), mosi=Pin(self._din), miso=Pin(self._dout))
		self._spi.init(baudrate=200000) # set the baudrate

	def command(self,c):
		b = bytearray(1)
		b[0] = c
		self._dc.low()
		self._ce.low()
		self._spi.write(b)     # write 1 byte on MOSI
		self._ce.high()


	def data(self, data):
		b = bytearray(1)
		b[0] = c
		self._dc.high()
		self._ce.low()
		self._spi.write(b)     # write 1 byte on MOSI
		self._ce.high()
		
	def reset(self):
		self._rst.low()
		time.sleep_ms(50)        # sleep for 50 milliseconds
		self._rst.high()

	# begin
	def begin(self):
		self.reset()
		self.command(0x21)	# extended command
		self.command(0xB1)	# set contrast
		self.command(0x13)	# bias
		self.command(0x04)	# temp coeff
		self.command(0x20)	# normal moded._x
		self.command(0x0C)	# not inverted
		self.display()

	# display
	def display(self):
		self.command(0x40)
		self.command(0x80)
		self._dc.high()
		self._ce.low()
		self._spi.write(self._buf)
		self._ce.high
		
	def p_char(self, ch):
		fp = (ord(ch)-0x20) * 5
		char_buf = array('b',[0,0,0,0,0])
		f = open('font5x7.fnt','rb')
		f.seek(fp)
		char_buf = f.read(5)
		bp = 84*self._row + 6*self._col
		for x in range (0,5):
			self._buf[bp+x] = char_buf[x]
			self._buf[bp+5] = 0 # put in inter char space
		self._col += 1
		if (self._col>13):
			self._col = 0
			self._row += 1
			if (self._row>5):
				self._row = 0	

	def p_string(self, str):
		for ch in (str):
			self.p_char(ch)

	def clear(self):
		self._buf= bytearray(84 * int(48 / 8))
		self._row = 0
		self._col = 0
				
	def pixel(self,x,y,fill):
		r = int(y/8)
		i = r * 84 + x
		b = y % 8
		self._buf[i] = self._buf[i] | ( 1 << b )
		
