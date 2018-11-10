from board import SCL, SDA
import busio
#import adafruit_ssd1306

#i2c = busio.I2C(SCL, SDA)
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

databuf = bytearray(0)

def read_le(s):
    # as of this writting, int.from_bytes does not have LE support, DIY!
    result = 0
    shift = 0
    for byte in bytearray(s):
        result += byte << shift
        shift += 8
    return result

#display.fill(0)
#display.show()

# Set a pixel in the origin 0,0 position.
#display.pixel(0, 0, 1)
# Set a pixel in the middle 64, 16 position.
#display.pixel(64, 16, 1)
# Set a pixel in the opposite 127, 31 position.
#display.pixel(127, 31, 1)
#display.show()
class BMPError(Exception):
    pass


with open("lab64_b.bmp", "rb") as f:
    print("File opened")
    if f.read(2) != b'BM':  # check signature
        raise BMPError("Not BitMap file")

    bmpFileSize = read_le(f.read(4))
    f.read(4)  # Read & ignore creator bytes

    bmpImageoffset = read_le(f.read(4))  # Start of image data
    headerSize = read_le(f.read(4))
    bmpWidth = read_le(f.read(4))
    bmpHeight = read_le(f.read(4))
    flip = True

    print("Size: %d\nImage offset: %d\nHeader size: %d" %
          (bmpFileSize, bmpImageoffset, headerSize))
    print("Width: %d\nHeight: %d" % (bmpWidth, bmpHeight))
    
    if read_le(f.read(2)) != 1:
        raise BMPError("Not singleplane")
    bmpDepth = read_le(f.read(2))  # bits per pixel
    print("Bit depth: %d" % (bmpDepth))
    if bmpDepth != 1:
        raise BMPError("Not monochrome")
    if read_le(f.read(2)) != 0:
        raise BMPError("Compressed file")

    print("Image OK!")
    rowSize = int((bmpWidth * 1 + 31)/32)*4 
    
    print("RowSize: %d" % rowSize)
    
    
        
    for row in range(bmpHeight):  # For each scanline...
        if flip:  # Bitmap is stored bottom-to-top order (normal BMP)
            pos = bmpImageoffset + (bmpHeight - 1 - row) * rowSize
        else:  # Bitmap is stored top-to-bottom
            pos = bmpImageoffset + row * rowSize
        f.seek(pos)
        for col in range(bmpWidth):
            if (read_le(f.read(1)) == 255):  # monochrome
                pix = 1
            else:
                pix = 0
            
            #print("row: %d  col: %d  val: %d" % (row,col,pix))
            print(pix, end=''), print(' ', end=''),
        print('')
            
     