import supervisor, time

buffer = []
i=0
while True:
    while (supervisor.runtime.serial_bytes_available):
        buffer.append(input())
        i += 1
        if i == 20:
            print(buffer)
            i = 0