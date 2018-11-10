# KMB-22 cp_demo
# M.Holliday
# reads SD card contents and prints out files names

import os, board, time, busio, digitalio, microcontroller
import adafruit_sdcard, storage

led = digitalio.DigitalInOut(board.LED)
xtb1  = digitalio.DigitalInOut(microcontroller.pin.PA28)
rfm = digitalio.DigitalInOut(microcontroller.pin.PB03)

xtb1.direction = digitalio.Direction.OUTPUT
rfm.direction = digitalio.Direction.OUTPUT
led.direction = digitalio.Direction.OUTPUT

xtb1.value = 1
rfm.value = 1
led.value = 1

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(microcontroller.pin.PA20)
cs.direction = digitalio.Direction.OUTPUT

sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

######################### MAIN LOOP ##############################
delay = 0.5
i = 0

def print_directory(path, tabs=0):
    for file in os.listdir(path):
        try:
            stats = os.statvfs(path + "/" + file)
            filesize = stats[6]
            isdir = stats[0] & 0x4000
     
            if filesize < 1000:
                sizestr = str(filesize) + " by"
            elif filesize < 1000000:
                sizestr = "%0.1f KB" % (filesize / 1000)
            else:
                sizestr = "%0.1f MB" % (filesize / 1000000)
     
            prettyprintname = ""
            for _ in range(tabs):
                prettyprintname += "   "
            prettyprintname += file
            if isdir:
                prettyprintname += "/"
            print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))
     
            #recursively print directory contents
            if isdir:
                print_directory(path + "/" + file, tabs + 1)
        except:
            print('error')
            pass
 
 
print("Files on filesystem:")
print_directory("/sd")

while True:
  print(i)
  led.value = 1
  time.sleep(delay) 
  led.value = 0
  time.sleep(delay)
  i += 1