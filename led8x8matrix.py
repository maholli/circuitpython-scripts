
import board
from microcontroller import pin
import busio,time
from digitalio import DigitalInOut, Direction, Pull

led      =   DigitalInOut(board.LED)
sd_cs    =   DigitalInOut(board.xSDCS)
rts      =   DigitalInOut(board.RTS)
dtr      =   DigitalInOut(board.DTR)

rts.direction     =  Direction.OUTPUT
dtr.direction     =  Direction.OUTPUT
led.direction     =  Direction.OUTPUT
sd_cs.pull = Pull.UP

led.value       = 0
rts.value       = 0
dtr.value       = 0



# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import matrix

# Create the I2C interface.
# I2C(SCL,SDA)
i2c = busio.I2C(board.A1, board.A0)

matrix = matrix.Matrix8x8x2(i2c)


while True:
	# matrix.fill(0)

	# matrix.pixel(3,4, 2)
	# matrix.pixel(4,4, 2)
	
	# time.sleep(0.3)

	# # matrix.pixel(2,3, 2)
	# matrix.pixel(3,3, 2)
	# matrix.pixel(4,3, 2)
	# # matrix.pixel(5,3, 2)
	# # matrix.pixel(6,3, 2)
	# # matrix.pixel(7,3, 2)

	# # matrix.pixel(0,4, 2)
	# # matrix.pixel(1,4, 2)
	# # matrix.pixel(2,4, 2)
	# matrix.pixel(3,4, 2)
	# matrix.pixel(4,4, 2)
	# # matrix.pixel(5,4, 2)
	# # matrix.pixel(6,4, 2)
	# # matrix.pixel(7,4, 2)

	# # matrix.pixel(0,5, 2)
	# # matrix.pixel(1,5, 2)
	# # matrix.pixel(2,5, 2)
	# # matrix.pixel(3,5, 2)
	# # matrix.pixel(4,5, 2)

	# time.sleep(0.3)

	# # ------------------

	# # matrix.pixel(0,0, 2)
	# # matrix.pixel(1,0, 2)
	# # matrix.pixel(2,0, 2)
	# # matrix.pixel(3,0, 2)
	# # matrix.pixel(4,0, 2)
	# # matrix.pixel(5,0, 2)
	# # matrix.pixel(6,0, 2)
	# # matrix.pixel(7,0, 2)

	# # matrix.pixel(0,1, 2)
	# # matrix.pixel(1,1, 2)
	# # matrix.pixel(2,1, 2)
	# # matrix.pixel(3,1, 2)
	# # matrix.pixel(4,1, 2)
	# # matrix.pixel(5,1, 2)
	# # matrix.pixel(6,1, 2)
	# # matrix.pixel(7,1, 2)

	# # matrix.pixel(0,2, 2)
	# # matrix.pixel(1,2, 2)
	# # matrix.pixel(2,2, 2)
	# # matrix.pixel(3,2, 2)
	# # matrix.pixel(4,2, 2)
	# # matrix.pixel(5,2, 2)
	# # matrix.pixel(6,2, 2)
	# # matrix.pixel(7,2, 2)

	# # matrix.pixel(0,3, 2)
	# # matrix.pixel(1,3, 2)
	# matrix.pixel(2,3, 2)
	# matrix.pixel(3,3, 2)
	# matrix.pixel(4,3, 2)
	# matrix.pixel(5,3, 2)
	# # matrix.pixel(6,3, 2)
	# # matrix.pixel(7,3, 2)

	# # matrix.pixel(0,4, 2)
	# # matrix.pixel(1,4, 2)
	# matrix.pixel(2,4, 2)
	# matrix.pixel(3,4, 2)
	# matrix.pixel(4,4, 2)
	# matrix.pixel(5,4, 2)
	# # matrix.pixel(6,4, 2)
	# # matrix.pixel(7,4, 2)

	# # matrix.pixel(0,5, 2)
	# # matrix.pixel(1,5, 2)
	# # matrix.pixel(2,5, 2)
	# matrix.pixel(3,5, 2)
	# matrix.pixel(4,5, 2)
	# # matrix.pixel(5,5, 2)
	# # matrix.pixel(6,5, 2)
	# # matrix.pixel(7,5, 2)

	# # matrix.pixel(0,6, 2)
	# # matrix.pixel(1,6, 2)
	# # matrix.pixel(2,6, 2)
	# # matrix.pixel(3,6, 2)
	# # matrix.pixel(4,6, 2)
	# # matrix.pixel(5,6, 2)
	# # matrix.pixel(6,6, 2)
	# # matrix.pixel(7,6, 2)

	# # matrix.pixel(0,7, 2)
	# # matrix.pixel(1,7, 2)
	# # matrix.pixel(2,7, 2)
	# # matrix.pixel(3,7, 2)
	# # matrix.pixel(4,7, 2)
	# # matrix.pixel(5,7, 2)
	# # matrix.pixel(6,7, 2)
	# # matrix.pixel(7,7, 2)
	# time.sleep(0.3)
	#---------------------

	# matrix.pixel(0,0, 2)
	# matrix.pixel(1,0, 2)
	# matrix.pixel(2,0, 2)
	# matrix.pixel(3,0, 2)
	# matrix.pixel(4,0, 2)
	# matrix.pixel(5,0, 2)
	# matrix.pixel(6,0, 2)
	# matrix.pixel(7,0, 2)

	# matrix.pixel(0,1, 2)
	# matrix.pixel(1,1, 2)
	# matrix.pixel(2,1, 2)
	# matrix.pixel(3,1, 2)
	# matrix.pixel(4,1, 2)
	# matrix.pixel(5,1, 2)
	# matrix.pixel(6,1, 2)
	# matrix.pixel(7,1, 2)

	# # matrix.pixel(0,2, 2)
	# # matrix.pixel(1,2, 2)
	# matrix.pixel(2,2, 2)
	# # matrix.pixel(3,2, 2)
	# # matrix.pixel(4,2, 2)
	# matrix.pixel(5,2, 2)
	# # matrix.pixel(6,2, 2)
	# # matrix.pixel(7,2, 2)

	# # matrix.pixel(0,3, 2)
	# matrix.pixel(1,3, 2)
	# matrix.pixel(2,3, 2)
	# matrix.pixel(3,3, 2)
	# matrix.pixel(4,3, 2)
	# matrix.pixel(5,3, 2)
	# matrix.pixel(6,3, 2)
	# # matrix.pixel(7,3, 2)

	# # matrix.pixel(0,4, 2)
	# matrix.pixel(1,4, 2)
	# matrix.pixel(2,4, 2)
	# matrix.pixel(3,4, 2)
	# matrix.pixel(4,4, 2)
	# matrix.pixel(5,4, 2)
	# matrix.pixel(6,4, 2)
	# # matrix.pixel(7,4, 2)

	# # matrix.pixel(0,5, 2)
	# # matrix.pixel(1,5, 2)
	# matrix.pixel(2,5, 2)
	# matrix.pixel(3,5, 2)
	# matrix.pixel(4,5, 2)
	# matrix.pixel(5,5, 2)
	# # matrix.pixel(6,5, 2)
	# # matrix.pixel(7,5, 2)

	# # matrix.pixel(0,6, 2)
	# # matrix.pixel(1,6, 2)
	# # matrix.pixel(2,6, 2)
	# matrix.pixel(3,6, 2)
	# matrix.pixel(4,6, 2)
	# # matrix.pixel(5,6, 2)
	# # matrix.pixel(6,6, 2)
	# # matrix.pixel(7,6, 2)

	# # matrix.pixel(0,7, 2)
	# # matrix.pixel(1,7, 2)
	# # matrix.pixel(2,7, 2)
	# # matrix.pixel(3,7, 2)
	# # matrix.pixel(4,7, 2)
	# # matrix.pixel(5,7, 2)
	# # matrix.pixel(6,7, 2)
	# # matrix.pixel(7,7, 2)

	# time.sleep(0.3)
	#---------------------


	# matrix.pixel(0,0, 2)
	# matrix.pixel(1,0, 2)
	# matrix.pixel(2,0, 2)
	# matrix.pixel(3,0, 2)
	# matrix.pixel(4,0, 2)
	# matrix.pixel(5,0, 2)
	# matrix.pixel(6,0, 2)
	# matrix.pixel(7,0, 2)

	# matrix.pixel(0,1, 2)
	# matrix.pixel(1,1, 2)
	# matrix.pixel(2,1, 2)
	# matrix.pixel(3,1, 2)
	# matrix.pixel(4,1, 2)
	# matrix.pixel(5,1, 2)
	# matrix.pixel(6,1, 2)
	# matrix.pixel(7,1, 2)

	# matrix.pixel(0,2, 2)
	matrix.pixel(1,2, 2)
	matrix.pixel(2,2, 2)
	# matrix.pixel(3,2, 2)
	# matrix.pixel(4,2, 2)
	matrix.pixel(5,2, 2)
	matrix.pixel(6,2, 2)
	# matrix.pixel(7,2, 2)

	matrix.pixel(0,3, 2)
	matrix.pixel(1,3, 2)
	matrix.pixel(2,3, 2)
	matrix.pixel(3,3, 2)
	matrix.pixel(4,3, 2)
	matrix.pixel(5,3, 2)
	matrix.pixel(6,3, 2)
	matrix.pixel(7,3, 2)

	matrix.pixel(0,4, 2)
	matrix.pixel(1,4, 2)
	matrix.pixel(2,4, 2)
	matrix.pixel(3,4, 2)
	matrix.pixel(4,4, 2)
	matrix.pixel(5,4, 2)
	matrix.pixel(6,4, 2)
	matrix.pixel(7,4, 2)

	# matrix.pixel(0,5, 2)
	matrix.pixel(1,5, 2)
	matrix.pixel(2,5, 2)
	matrix.pixel(3,5, 2)
	matrix.pixel(4,5, 2)
	matrix.pixel(5,5, 2)
	matrix.pixel(6,5, 2)
	# matrix.pixel(7,5, 2)

	# matrix.pixel(0,6, 2)
	# matrix.pixel(1,6, 2)
	matrix.pixel(2,6, 2)
	matrix.pixel(3,6, 2)
	matrix.pixel(4,6, 2)
	matrix.pixel(5,6, 2)
	# matrix.pixel(6,6, 2)
	# matrix.pixel(7,6, 2)

	# matrix.pixel(0,7, 2)
	# matrix.pixel(1,7, 2)
	# matrix.pixel(2,7, 2)
	matrix.pixel(3,7, 2)
	matrix.pixel(4,7, 2)
	# matrix.pixel(5,7, 2)
	# matrix.pixel(6,7, 2)
	# matrix.pixel(7,7, 2)
	time.sleep(0.3)
	matrix.show()



