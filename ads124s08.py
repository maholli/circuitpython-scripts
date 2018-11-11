import time
from adafruit_bus_device import spi_device

default = bytes([0x42, 0x08, 0xCC, 0x08, 0x1D, 0x39, 0x00, 0xFF, 0x00, 0x10])
registers = [
                    "(ID):        ",
                    "(STATUS):    ",
                    "(INPMUX):    ",
                    "(PGA):       ",
                    "(DATARATE):  ",
                    "(REF):       ",
                    "(IDACMAG):   ",
                    "(IDACMUX):   ",
                    "(VBIAS):     ",
                    "(SYS):       ",
                    "(OFCAL0):    ",
                    "(OFCAL1):    ",
                    "(OFCAL2):    ",
                    "(FSCAL0):    ",
                    "(FSCAL1):    ",
                    "(FSCAL2):    ",
                    "(GPIODAT):   ",
                    "(GPIOCON):   "]

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
        with self.spi_device as spi:
            spi.write(bytes(0x0A))
            self.reset_pin.value = 0
            time.sleep(1e-6)
            self.reset_pin.value = 1
            spi.write(default)

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
        for i, j in enumerate(readOut):
            print(registers[i], hex(j))
        print("-------------------------------")
    
    def GPIO(self, GPIODAT, GPIOCON):
    	with self.spi_device as spi:
            spi.write(bytes([0x50, 0x01, GPIODAT, GPIOCON]))

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
            time.sleep(0.01)
            spi.write(bytes([0x00,0x12]))
            spi.readinto(buffer)
            spi.write(bytes([0x49, 0x00, 0x10]))
        data = self.dataconvert(buffer)*1000
        output = (-1*((129.00-data)*0.403)+25)
        return output

    def IVcurve(self, inn, inp, start=0x00, stop=0x0A, idacMux=15):
            buffer = []
            for idacMag in range(start, stop):
                buffer.append((hex(idacMag), self.readpins(inn, inp, idacMag=idacMag, idacMux=idacMux, delayT=0.05)))
            return buffer
            
    def readpins(self, inp, inn, idacMag=0, idacMux=15, vb=None, delayT=0.01, hall=False):
        if vb:
            vapp = (idacMux << 4) | vb
            if   (vb == None):
                vbPin = 0x80
            elif (vb == 0):
                vbPin = 0x81
            elif (vb == 1):
                vbPin = 0x82
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
        else:
            vbPin = 0x80
        
        inpMux  = (inp << 4) | inn        
        bufferA = bytearray(3)
        bufferB = bytearray(3)
        cmd     = bytes([0x42,0x06, inpMux, 0x08, 0x1D, 0x39, idacMag, (0xF0 | idacMux), vbPin])
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
                vapplied = self.dataconvert(bufferB)
        output = self.dataconvert(bufferA)
        return output

class XTB(_ADS124S08):
    # XTB class from ADS124S08    
    def __init__(self, spi, xtb_rst, xtb_cs, baudrate=8000000, phase=1, polarity=0):
        self.spi_device = spi_device.SPIDevice(spi, xtb_cs, baudrate=baudrate, phase=phase, polarity=polarity)
        super().__init__(xtb_rst)
    
    def ZnO(self):
        buffer = []
        buffer.append(super().readpins(6, 12, idacMag=0x01, idacMux=6, delayT=0.05))
        time.sleep(0.01)
        buffer.append(super().readpins(3, 12, idacMag=0x01, idacMux=3, delayT=0.05))
        time.sleep(0.01)
        buffer.append(super().readpins(2, 12, idacMag=0x01, idacMux=2, delayT=0.05))
        time.sleep(0.01)
        buffer.append(super().readpins(5, 12, idacMag=0x01, idacMux=5, delayT=0.05))
        time.sleep(0.01)
        super().GPIO(0x00, 0x04)
        time.sleep(0.01)
        buffer.append(super().readpins(1, 10, idacMag=0x01, idacMux=1, delayT=0.05))
        time.sleep(0.01)
        super().GPIO(0x00, 0x01)

        buffer.append(super().readpins(7, 8,  idacMag=0x01, idacMux=7, delayT=0.05)) 
        time.sleep(0.01)
        super().readpins(6, 12)
        super().GPIO(0x00, 0x00)

        # super().GPIO(0x00, 0x08)
        # time.sleep(0.01)
        # buffer.append(super().readpins(0, 11, idacMag=0x01, idacMux=0, delayT=0.05))
        
        
        return buffer