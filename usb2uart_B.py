# input: UART, print to serial

import board, supervisor, busio
uart = busio.UART(board.TX, board.RX, baudrate=9600)

while True:
	if uart.in_waiting:
		try:
			data = uart.read()
			print(data, end=''), print('    string:',end='')
			data_string = ''.join([chr(b) for b in data])
			print(data_string)
			uart.reset_input_buffer
		except:
			pass


