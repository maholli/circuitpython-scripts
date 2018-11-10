# feather M0 adalogger demo 
# M.Holliday

import board
import time
from digitalio import DigitalInOut, Direction, Pull

# Built in LEDs
led1 = DigitalInOut(board.D13)
led1.direction = Direction.OUTPUT
led2 = DigitalInOut(board.D8)
led2.direction = Direction.OUTPUT


######################### MAIN LOOP ##############################
delay = 0.5
i = 0
while True:
  print(i)
  led1.value = 1
  time.sleep(delay) # make bigger to slow down
  led1.value = 0
  time.sleep(delay) # make bigger to slow down
  
  led2.value = 1
  time.sleep(delay) # make bigger to slow down
  led2.value = 0
  time.sleep(delay) # make bigger to slow down
  i += 1