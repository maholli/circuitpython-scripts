# KMB-22 cp_demo
# M.Holliday

import board, busio, digitalio, microcontroller
# import adafruit_sdcard, storage
import ads124s08

led      =   digitalio.DigitalInOut(board.LED)
xtb1_cs  =   digitalio.DigitalInOut(microcontroller.pin.PA28)
rfm_cs   =   digitalio.DigitalInOut(microcontroller.pin.PB03)
xtb_rst  =   digitalio.DigitalInOut(board.XTBRST)
sd_cs    =   digitalio.DigitalInOut(board.SDCS)

xtb1_cs.direction =  digitalio.Direction.OUTPUT
rfm_cs.direction  =  digitalio.Direction.OUTPUT
led.direction     =  digitalio.Direction.OUTPUT
xtb_rst.direction =  digitalio.Direction.OUTPUT
sd_cs.direction   =  digitalio.Direction.OUTPUT

xtb1_cs.value   = 1
rfm_cs.value    = 1
led.value       = 1
xtb_rst.value   = 1
sd_cs.value     = 1

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

xtb1 = ads124s08.XTB(spi, xtb_rst, xtb1_cs)
test = []
test.append(xtb1.readtemp())

test.append(xtb1.readpins(1,12, vb=1))
print(test)