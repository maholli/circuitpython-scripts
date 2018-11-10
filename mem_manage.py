import adafruit_sdcard, board
from sys import path
from busio import SPI
from digitalio import DigitalInOut
from storage import mount, VfsFat

# Connect to the card and mount the filesystem.
spi = SPI(board.SCK, board.MOSI, board.MISO)
cs = DigitalInOut(board.D4)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = VfsFat(sdcard)
mount(vfs, "/sd")
path.append("/sd")

import ads124s08
