import time
from adafruit_bus_device import spi_device

class _ADS124S08:
    def __init__(self, reset, refV=2.5, pgaGain=1):
        self.LSBsize = ((refV*2)/pgaGain)/pow(2,24)
        self.reset_pin = reset
        if self.reset_pin:
            self.reset_pin.switch_to_output(value=1)
        self.init_adc()

    def init_adc(self):
        self.reset()
        self.start()
        self.regreadout()

    def reset(self):
        commands = bytes([0x42, 0x08, 0xCC, 0x08, 0x1C, 0x39, 0x00, 0xFF, 0x00, 0x10])
        with self.spi_device as spi:
            spi.write(bytes(0x0A))
            self.reset_pin.value = 0
            time.sleep(1e-6)
            self.reset_pin.value = 1
            spi.write(commands)

    def start(self):
        with self.spi_device as spi:
            spi.write(bytes([0x0A, 0x08]))
        time.sleep(0.1)
    
    def stop(self):
        with self.spi_device as spi:
            spi.write(bytes(0x0A))

    def wake(self):
        with self.spi_device as spi:
            spi.write(bytes(0x02))

    def wreg(self,start,cmd): #xtb.wreg(0x42,[0xCC])
        length = len(cmd) - 1
        with self.spi_device as spi:
            spi.write(bytes([start]+[length]+cmd))
    
    def regreadout(self):
        readOut = bytearray(18)
        with self.spi_device as spi:
            spi.write(bytes([0x20, 0x12]))
            spi.readinto(readOut)
        print("-------------------------------")
        print("Register 0x00 (ID):        ", end=''), print(hex(readOut[0]))
        print("Register 0x01 (STATUS):    ", end=''), print(hex(readOut[1]))
        print("Register 0x02 (INPMUX):    ", end=''), print(hex(readOut[2]))
        print("Register 0x03 (PGA):       ", end=''), print(hex(readOut[3]))
        print("Register 0x04 (DATARATE):  ", end=''), print(hex(readOut[4]))
        print("Register 0x05 (REF):       ", end=''), print(hex(readOut[5]))
        print("Register 0x06 (IDACMAG):   ", end=''), print(hex(readOut[6]))
        print("Register 0x07 (IDACMUX):   ", end=''), print(hex(readOut[7]))
        print("Register 0x08 (VBIAS):     ", end=''), print(hex(readOut[8]))
        print("Register 0x09 (SYS):       ", end=''), print(hex(readOut[9]))
        print("Register 0x0A (OFCAL0):    ", end=''), print(hex(readOut[10]))
        print("Register 0x0B (OFCAL1):    ", end=''), print(hex(readOut[11]))
        print("Register 0x0C (OFCAL2):    ", end=''), print(hex(readOut[12]))
        print("Register 0x0D (FSCAL0):    ", end=''), print(hex(readOut[13]))
        print("Register 0x0E (FSCAL1):    ", end=''), print(hex(readOut[14]))
        print("Register 0x0F (FSCAL2):    ", end=''), print(hex(readOut[15]))
        print("Register 0x10 (GPIODAT):   ", end=''), print(hex(readOut[16]))
        print("Register 0x11 (GPIOCON):   ", end=''), print(hex(readOut[17]))
        print("-------------------------------")
    
    def dataconvert(self, raw):
        rawDataIN = 0 | raw[0]
        rawDataIN = (rawDataIN << 8) | raw[1]
        rawDataIN = (rawDataIN << 8) | raw[2]
        if (((1 << 23) & rawDataIN) != 0):
            maskIN = (1 << 24) - 1
            rawDataIN = ((~rawDataIN) & maskIN) + 1
            dataOUT = rawDataIN * self.LSBsize * -1
        else:
            dataOUT = rawDataIN*self.LSBsize
        return dataOUT

    def readtemp(self):
        buffer = bytearray(3)
        with self.spi_device as spi:
            spi.write(bytes([0x49, 0x00, 0x50]))
            time.sleep(0.005)
            spi.write(bytes([0x00,0x12]))
            spi.readinto(buffer)
            spi.write(bytes([0x49, 0x00, 0x10]))
        data = self.dataconvert(buffer)*1000
        output = (-1*((129.00-data)*0.403)+25)
        return output
    
    def readpins(self, inp, inn, idacMag=0, idacMux=15, vb=0, delayT=0.01, hall=False):
        inpMux  = (inp << 4) | inn
        vapp    = (idacMux << 4) | vb
        bufferA = bytearray(3)
        bufferB = bytearray(3)
        output=[]
        if (vb == 0):
            vbPin = 0x80
        elif (vb <= 1):
            vbPin = 0x80 | (vb+1)
        elif (vb == 2):
            vbPin = 0x84
        elif (vb == 3):
            vbPin = 0x88
        elif (vb == 4):
            vbPin = 0x90
        elif (vb == 5):
            vbPin = 0xA0
        elif (vb > 5):
            vbPin = 0x80
        cmd = bytes([0x42,0x06, inpMux, 0x08, 0x1D, 0x39, idacMag, (0xF0 | idacMux), vbPin])
        with self.spi_device as spi:
            spi.write(cmd)
            time.sleep(delayT)
            spi.write(bytes([0x00,0x12]))
            spi.readinto(bufferA)
            if hall:
                time.sleep(0.001)
                spi.write(bytes([0x42,0x00,vapp]))
                time.sleep(0.01)
                spi.write(bytes([0x00,0x12]))
                spi.readinto(bufferB)
                output.append(self.dataconvert(bufferB))
        output.append(self.dataconvert(bufferA))
        return output



class XTB(_ADS124S08):
    # XTB class from ADS124S08    
    def __init__(self, spi, xtb_rst, xtb_cs, baudrate=8000000, phase=1, polarity=0):
        self.spi_device = spi_device.SPIDevice(spi, xtb_cs, baudrate=baudrate, phase=phase, polarity=polarity)
        super().__init__(xtb_rst)
    



    
