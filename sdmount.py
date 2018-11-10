import os 
import adafruit_sdcard, sys
import board
import busio
import digitalio
import storage
 
# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D4)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
sys.path.append("/sd")
 
# Use the filesystem as normal! Our files are under /sd
 
# This helper function will print the contents of the SD
 
 
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
print("====================")
print_directory("/sd")