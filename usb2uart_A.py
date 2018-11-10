# input: usb, send: UART

import board, supervisor, busio
uart = busio.UART(board.TX, board.RX, baudrate=9600)

while True:
	if supervisor.runtime.serial_bytes_available:
		uart.write(str(input()))