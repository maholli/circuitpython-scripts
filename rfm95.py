import board
from busio import SPI
from digitalio import DigitalInOut, Direction, Pull
import time, neopixel_write

led      =   DigitalInOut(board.LED)
cs       =   DigitalInOut(board.D59)
reset    =   DigitalInOut(board.D60)
rts      =   DigitalInOut(board.RTS)
dtr      =   DigitalInOut(board.DTR)

rts.direction     =  Direction.OUTPUT
dtr.direction     =  Direction.OUTPUT
led.direction     =  Direction.OUTPUT
cs.direction      =  Direction.OUTPUT
reset.direction   =  Direction.OUTPUT

led.value       = 0
rts.value       = 0
dtr.value       = 0

spi = SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

try:
    neopix = DigitalInOut(board.NEOPIXEL)
    neopix.direction = Direction.OUTPUT
except Exception as e:
    print(e)

import adafruit_rfm9x
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)
print('sleeping')
time.sleep(2)
print('waking')
print('chirping')

while True:
	rfm9x.send('Hello world!')
	time.sleep(2)