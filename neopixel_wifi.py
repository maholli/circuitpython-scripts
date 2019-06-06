"""
Example of turning on and off a LED
from an Adafruit IO Dashboard.
"""
import time
import board
import busio, neopixel
from digitalio import DigitalInOut, Direction
from random import randint
# ESP32 SPI
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Setup on-board Neopixel
ORDER = neopixel.GRB
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.5, auto_write=False,pixel_order=ORDER)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b)

def rainbow_cycle(wait):
    for j in range(255):
        pixel_index = (256 // 1) + j
        pixel[0] = wheel(pixel_index & 255)
        pixel.show()
        time.sleep(wait)

# SAM32 board ESP32 Setup
dtr = DigitalInOut(board.DTR)
esp32_cs = DigitalInOut(board.TMS) #GPIO14
esp32_ready = DigitalInOut(board.TCK) #GPIO13
esp32_reset = DigitalInOut(board.RTS)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# Requires ESP32 is flashed with ESP32SPI firmware
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset, gpio0_pin=dtr, debug=False)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_pixel=None)
 
aio_username = secrets['aio_username']
aio_key = secrets['aio_key']

# Import Adafruit IO REST Client
from adafruit_io.adafruit_io import RESTClient, AdafruitIO_RequestError

# Create an instance of the Adafruit IO REST client
io = RESTClient(aio_username, aio_key, wifi)

prev_color = '#000000'

while True:
    if io.receive_data('digital')['value']=='ON':
        rainbow_cycle(0.1)
    else: # grab the `color` feed
        color_val = io.receive_data('color')['value'][1:]        
        if color_val != prev_color:
            rgb = tuple(int(color_val[i:i+2], 16) for i in (0, 2, 4))
            print('Received New Color:',color_val,rgb)
            pixel.fill(rgb)
            pixel.show()
            prev_color=color_val
    time.sleep(.2)

