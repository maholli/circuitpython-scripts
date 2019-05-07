import time
 
from microcontroller import pin
from analogio import AnalogIn
 
analogin = AnalogIn(pin.PA06)
 
 
def getVoltage(pin):  # helper
    return (pin.value * 2 * 3.3) / 65536
 
 
while True:
    print("Analog Voltage: %f" % getVoltage(analogin))
    time.sleep(0.1)