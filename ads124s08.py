from time import sleep
from adafruit_bus_device import spi_device


default = bytes([0x42, 0x08, 0xCC, 0x08, 0x1C, 0x3A, 0x00, 0xFF, 0x00, 0x18])
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
        self.pgaGain = pgaGain
        self.LSBsize = refV/(pgaGain*pow(2,23))
        self.xtb_rst = reset
        self.init_adc()
        self.startTrig = True

    def LSBSIZE(self, refV=2.5):
        pgaGain = self.pgaGain
        val = refV/(pgaGain*pow(2,23))
        self.LSBsize = val
        return val

    def init_adc(self):
        self.reset()
        self.start()
        self.regreadout()

    def readValue(self):
        zzz = bytearray(3)
        with self.spi_device as spi:
            spi.write(bytes([0x12]))
            spi.readinto(zzz)
            return self.dataconvert(zzz)

    def reset(self):
        with self.spi_device as spi:
            spi.write(bytes(0x0A))
            sleep(0.1)
            spi.write(default)

    def start(self):
        with self.spi_device as spi:
            spi.write(bytes([0x0A, 0x08]))
        sleep(0.1)
    
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
    
    def calibrate(self):
        with self.spi_device as spi:
            spi.write(bytes([0x19]))

    def dataconvert(self, raw):
        self.LSBSIZE()
        rawDataIN = 0 | raw[0]
        rawDataIN = (rawDataIN << 8) | raw[1]
        rawDataIN = (rawDataIN << 8) | raw[2]
        # if (((1 << 23) & rawDataIN) != 0):
        if (rawDataIN > 8.38861e6):
            dataOUT = (((~rawDataIN) & ((1 << 24) - 1)) + 1) * self.LSBsize * -1
        else:
            dataOUT = rawDataIN*self.LSBsize
        return dataOUT
 

    def readtemp(self):
        with self.spi_device as spi:
            spi.write(bytes([0x49, 0x00, 0x58]))
        sleep(1)
        data = self.readValue()*1000
        with self.spi_device as spi:
            spi.write(bytes([0x49, 0x00, 0x18]))        
        output = (-1*((129.00-data)*0.403)+25)
        print(output)
        return output

    def test(self):
        zeroBuf = []    
        pgaOLD = self.pgaGain
        self.pgaGain = 4
        with self.spi_device as spi:
            spi.write(bytes([0x42, 0x08, 0x20, 0x0A, 0x1C, 0x3A, 0x00, 0xFF, 0x90, 0x38]))
        for i in range(30):
            zeroBuf.append(abs(self.readValue()))
        b = [abs(x[1] - x[0]) for x in zip(zeroBuf[1:], zeroBuf)]
        test = sum(b)/30 
        print('Self-test Result:', test, 'PGA gain:', self.pgaGain)
        return test
        self.pgaGain = pgaOLD 
    
    def IVsweep(self, inn, inp, start=0x00, stop=0x0A, idacMux=15):
            buffer = []
            for idacMag in range(start, stop):
                buffer.append((hex(idacMag), self.readpins(inn, inp, idacMag=idacMag, idacMux=idacMux, delayT=0.05)))
            return buffer

    def readpins(self, inp, inn, idacMag=0, idacMux=15, vb='off', pga=0xA8, datarate=0x18, delayT=0.01, hall=False):
        vbPin = 0x80
        if vb != 'off' and vb < 6:
            vbPin = (0x80 | 1<<vb)     
        inpMux  = (inp << 4) | inn               
        bufferA = bytearray(3)
        bufferB = bytearray(3)
        cmd     = bytes([0x42,0x06, inpMux, pga, datarate, 0x39, idacMag, (0xF0 | idacMux), vbPin])
        with self.spi_device as spi:
            spi.write(cmd)
            sleep(delayT)
            spi.write(bytes([0x00,0x12]))
            spi.readinto(bufferA)
            if hall:
                vapp = (idacMux << 4) | vb 
                sleep(0.001)
                spi.write(bytes([0x42,0x00,vapp]))
                sleep(0.1)
                spi.write(bytes([0x00,0x12]))
                spi.readinto(bufferB)
                vapplied = self.dataconvert(bufferB)
                print(vapplied,end=''), print(',',end='')
        output = self.dataconvert(bufferA)
        return output
    


class XTB(_ADS124S08):
    # XTB class from ADS124S08    
    def __init__(self, spi, xtb_rst, xtb_cs, baudrate=8000000, phase=1, polarity=0):
        self.spi_device = spi_device.SPIDevice(spi, xtb_cs, baudrate=baudrate, phase=phase, polarity=polarity)
        super().__init__(xtb_rst)
    
    # def ZnO(self):
    #     buffer = []
    #     buffer.append(super().readpins(6, 12, idacMag=0x01, idacMux=6, delayT=0.05))
    #     sleep(0.01)
    #     buffer.append(super().readpins(3, 12, idacMag=0x01, idacMux=3, delayT=0.05))
    #     sleep(0.01)
    #     buffer.append(super().readpins(2, 12, idacMag=0x01, idacMux=2, delayT=0.05))
    #     sleep(0.01)
    #     buffer.append(super().readpins(5, 12, idacMag=0x01, idacMux=5, delayT=0.05))
    #     sleep(0.01)
    #     super().GPIO(0x00, 0x04)
    #     sleep(0.01)
    #     buffer.append(super().readpins(1, 10, idacMag=0x01, idacMux=1, delayT=0.05))
    #     sleep(0.01)
    #     super().GPIO(0x00, 0x01)
    #     buffer.append(super().readpins(7, 8,  idacMag=0x01, idacMux=7, delayT=0.05)) 
    #     sleep(0.01)
    #     super().readpins(6, 12)
    #     super().GPIO(0x00, 0x00)
    #     # super().GPIO(0x00, 0x08)
    #     # sleep(0.01)
    #     # buffer.append(super().readpins(0, 11, idacMag=0x01, idacMux=0, delayT=0.05))           
    #     return buffer