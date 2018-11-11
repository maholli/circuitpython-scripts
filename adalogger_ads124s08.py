import adafruit_sdcard, board
from sys import path
from busio import SPI
from digitalio import DigitalInOut, Direction
from storage import mount, VfsFat
from time import sleep

led      =   DigitalInOut(board.D8)
xtb_cs   =   DigitalInOut(board.A2)
xtb_rst  =   DigitalInOut(board.A1)
sd_cs    =   DigitalInOut(board.SD_CS)

led.direction     =  Direction.OUTPUT
xtb_cs.direction  =  Direction.OUTPUT
xtb_rst.direction =  Direction.OUTPUT
sd_cs.direction   =  Direction.OUTPUT

led.value       = 0
xtb_cs.value    = 1
xtb_rst.value   = 1
sd_cs.value     = 1

spi = SPI(board.SCK, board.MOSI, board.MISO)

sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
vfs = VfsFat(sdcard)
mount(vfs, "/sd")
path.append("/sd")

import ads124s08

xtb = ads124s08.XTB(spi, xtb_rst, xtb_cs)

while True:
    with open("/sd/xtb_test1.txt", "a") as f:
        led.value = 1
        t = xtb.readtemp()
        print("Temperature = %0.3f" % t)
        f.write("%0.3f\n" % t)
        led.value = 0
    time.sleep(1)