import time, neopixel_write, board
from digitalio import DigitalInOut, Direction, Pull

blink1_time = time.monotonic()
blink1_int = 1

blink2_time = time.monotonic()
blink2_int = 5

try:
    neopix = DigitalInOut(board.NEOPIXEL)
    neopix.direction = Direction.OUTPUT
except Exception as e:
    print(e)

payload = []

while True:
    now = time.monotonic()

    if now >= blink1_time:
        blink1_time = now + blink1_int
        test = (0.00000000000000012356,7,8,9)
        payload.append((now, '{:E}, {}, {}, {}'.format(*test)))
        neopixel_write.neopixel_write(neopix, bytearray([0,255,0]))
        time.sleep(0.1)
        neopixel_write.neopixel_write(neopix, bytearray([0,0,0]))

    if now >= blink2_time:
        blink2_time = now + blink2_int
        print(payload)
        neopixel_write.neopixel_write(neopix, bytearray([0,0,255]))
        time.sleep(0.1)
        neopixel_write.neopixel_write(neopix, bytearray([0,0,0]))
        payload = []
