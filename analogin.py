
import time
import board
from analogio import AnalogIn

analogin = AnalogIn(board.A6)


def getVoltage(pin):  # helper
    return (pin.value * 3.3) / 65536


while True:
    print("Analog Voltage: %f" % getVoltage(analogin))
    time.sleep(0.1)
