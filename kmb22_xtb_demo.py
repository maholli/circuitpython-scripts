# KMB-22 cp_demo
# M.Holliday
# reads SD card contents and prints out files names

import os, board, time, busio, digitalio, microcontroller
import adafruit_sdcard, storage
from adafruit_bus_device.spi_device import SPIDevice

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
xtb = SPIDevice(spi, xtb1_cs, baudrate=8000000, phase=1, polarity=0)

def startADC():
    print("------Starting ADC 1----")
    with xtb as device:
        device.write(bytes([0x0A, 0x08]))
    time.sleep(0.1)


def resetADC():
    commands = bytes([0x42, 0x08, 0xCC, 0x08, 0x1C, 0x39, 0x00, 0xFF, 0x00, 0x10])
    print("------Resetting ADC 1----")
    with xtb as device:
        device.write(bytes(0x0A))
        xtb_rst.value = 0
        time.sleep(1e-6)
        xtb_rst.value = 1
        device.write(commands)

def regReadout():
    readOut = bytearray(18)
    print("------regReadout ADC 1----")
    with xtb as device:
        device.write(bytes([0x20, 0x12]))
        device.readinto(readOut)
    print("Register 0x00 (ID):        ", end=''), print(hex(readOut[0]))
    print("Register 0x01 (STATUS):    ", end=''), print(hex(readOut[1]))
    print("Register 0x02 (INPMUX):    ", end=''), print(hex(readOut[2]))
    print("Register 0x03 (PGA):       ", end=''), print(hex(readOut[3]))
    print("Register 0x04 (DATARATE):  ", end=''), print(hex(readOut[4]))
    print("Register 0x05 (REF):       ", end=''), print(hex(readOut[5]))
    print("Register 0x06 (IDACMAG):   ", end=''), print(hex(readOut[6]))
    print("Register 0x07 (IDACMUX):   ", end=''), print(hex(readOut[7]))
    print("Register 0x08 (VBIAS):     ", end=''), print(hex(readOut[8]))
    print("Register 0x09 (SYS):       ", end=''), print(hex(readOut[9]))
    print("Register 0x0A (OFCAL0):    ", end=''), print(hex(readOut[10]))
    print("Register 0x0B (OFCAL1):    ", end=''), print(hex(readOut[11]))
    print("Register 0x0C (OFCAL2):    ", end=''), print(hex(readOut[12]))
    print("Register 0x0D (FSCAL0):    ", end=''), print(hex(readOut[13]))
    print("Register 0x0E (FSCAL1):    ", end=''), print(hex(readOut[14]))
    print("Register 0x0F (FSCAL2):    ", end=''), print(hex(readOut[15]))
    print("Register 0x10 (GPIODAT):   ", end=''), print(hex(readOut[16]))
    print("Register 0x11 (GPIOCON):   ", end=''), print(hex(readOut[17]))
    print("-----------------------------")
    spi.unlock()

resetADC()
startADC()
regReadout()
