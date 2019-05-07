"""
Sending data to Adafruit IO and receiving it.
"""

import board, time, busio, supervisor, os
import adafruit_sdcard, storage
from digitalio import DigitalInOut, Direction

# Setup pins
led = DigitalInOut(board.LED)
rts = DigitalInOut(board.RTS)
dtr = DigitalInOut(board.DTR)
led.direction = Direction.OUTPUT
rts.direction = Direction.OUTPUT
dtr.direction = Direction.OUTPUT

led.value = 0
rts.value = 1
dtr.value = 1
from random import randint


# ESP32 SPI
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager

# Import NeoPixel Library
import neopixel

# Import Adafruit IO REST Client
from adafruit_io.adafruit_io import RESTClient, AdafruitIO_RequestError

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# ESP32 Setup
esp32_cs = DigitalInOut(board.TMS) #GPIO14
esp32_ready = DigitalInOut(board.TCK) #GPIO13
esp32_reset = DigitalInOut(board.RTS)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
"""Use below for Most Boards"""
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2) # Uncomment for Most Boards
"""Uncomment below for ItsyBitsy M4"""
#status_light = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

"""
# PyPortal ESP32 Setup
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)
"""

# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = secrets['aio_username']
aio_key = secrets['aio_key']

# Create an instance of the Adafruit IO REST client
io = RESTClient(aio_username, aio_key, wifi)

try:
    # Get the 'temperature' feed from Adafruit IO
    temperature_feed = io.get_feed('temperature')
except AdafruitIO_RequestError:
    # If no 'temperature' feed exists, create one
    temperature_feed = io.create_new_feed('temperature')

# Send random integer values to the feed
random_value = randint(0, 50)
print('Sending {0} to temperature feed...'.format(random_value))
io.send_data(temperature_feed['key'], random_value)
print('Data sent!')

# Retrieve data value from the feed
print('Retrieving data from temperature feed...')
received_data = io.receive_data(temperature_feed['key'])
print('Data from temperature feed: ', received_data['value'])
