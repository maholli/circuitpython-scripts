'''
Working Circuitpython RFID/NFC example with RDM8800 breakout & SAM32

Reads 10-digit ID of NFC card and prints to serial

M.Holliday 2019-05-05   
'''

import board, busio, time
from digitalio import DigitalInOut, Direction, Pull

sd_cs        =   DigitalInOut(board.xSDCS)
rts          =   DigitalInOut(board.RTS)
dtr          =   DigitalInOut(board.DTR)
rfid_rdy     =   DigitalInOut(board.D31)

sd_cs.direction        =  Direction.OUTPUT
rts.direction          =  Direction.OUTPUT
dtr.direction          =  Direction.OUTPUT
rfid_rdy.direction     =  Direction.INPUT

sd_cs.value     = 1
rts.value       = 0
dtr.value       = 0

def checkEqual(val):
   return val[1:] == val[:-1]

try:
    neopix = DigitalInOut(board.NEOPIXEL)
    neopix.direction = Direction.OUTPUT
except Exception as e:
    print(e)

uart = busio.UART(board.TX1, board.RX1, baudrate=9600)

while True:
    
    if uart.in_waiting:
        uart_data = uart.read()
        data_string = ''.join([chr(b) for b in uart_data]) # bytes to string
        id_list = data_string.split('\r\n') # split at CR/LF

        if checkEqual(id_list[:-1]): # see if all id numbers are same 
            print(id_list[0])

        uart.reset_input_buffer