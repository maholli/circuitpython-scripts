from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from math import pi

FDC2214_I2C_ADDR_0   =const(0x2A)
FDC2214_I2C_ADDR_1   =const(0x2B)
# Address is 0x2A (default) or 0x2B (if ADDR is high)

#bitmasks
FDC2214_CH0_UNREADCONV =const(0x0008)         #denotes unread CH0 reading in STATUS register
FDC2214_CH1_UNREADCONV =const(0x0004)         #denotes unread CH1 reading in STATUS register
FDC2214_CH2_UNREADCONV =const(0x0002)         #denotes unread CH2 reading in STATUS register
FDC2214_CH3_UNREADCONV =const(0x0001)         #denotes unread CH3 reading in STATUS register


#registers
FDC2214_DEVICE_ID            =const(0x7F)
FDC2214_MUX_CONFIG           =const(0x1B)
FDC2214_CONFIG               =const(0x1A)
FDC2214_RCOUNT_CH0           =const(0x08)
FDC2214_RCOUNT_CH1           =const(0x09)
FDC2214_RCOUNT_CH2           =const(0x0A)
FDC2214_RCOUNT_CH3           =const(0x0B)
FDC2214_OFFSET_CH0           =const(0x0C)
FDC2214_OFFSET_CH1           =const(0x0D)
FDC2214_OFFSET_CH2           =const(0x0E)
FDC2214_OFFSET_CH3           =const(0x0F)
FDC2214_SETTLECOUNT_CH0      =const(0x10)
FDC2214_SETTLECOUNT_CH1      =const(0x11)
FDC2214_SETTLECOUNT_CH2      =const(0x12)
FDC2214_SETTLECOUNT_CH3      =const(0x13)
FDC2214_CLOCK_DIVIDERS_CH0   =const(0x14)
FDC2214_CLOCK_DIVIDERS_CH1   =const(0x15)
FDC2214_CLOCK_DIVIDERS_CH2   =const(0x16)
FDC2214_CLOCK_DIVIDERS_CH3   =const(0x17)
FDC2214_STATUS               =const(0x18)
FDC2214_DATA_CH0_MSB         =const(0x00)
FDC2214_DATA_CH0_LSB         =const(0x01)
FDC2214_DATA_CH1_MSB         =const(0x02)
FDC2214_DATA_CH1_LSB         =const(0x03)
FDC2214_DATA_CH2_MSB         =const(0x04)
FDC2214_DATA_CH2_LSB         =const(0x05)
FDC2214_DATA_CH3_MSB         =const(0x06)
FDC2214_DATA_CH3_LSB         =const(0x07)
FDC2214_DRIVE_CH0            =const(0x1E)
FDC2214_DRIVE_CH1            =const(0x1F)
FDC2214_DRIVE_CH2            =const(0x20)
FDC2214_DRIVE_CH3            =const(0x21)

# mask for 28bit data to filter out flag bits
FDC2214_DATA_CHx_MASK_DATA          =const(0x0FFF) 
FDC2214_DATA_CHx_MASK_ERRAW         =const(0x1000) 
FDC2214_DATA_CHx_MASK_ERRWD         =const(0x2000) 

class FDC2214(object):
    """
    :param i2c: The `busio.I2C` object to use. This is the only required parameter.
    :param 
    # Class-level buffer to reduce allocations and fragmentation.
    # Note this is NOT thread-safe or re-entrant by design!   
    """
    _BUFFER = bytearray(8)
    def __init__(self, i2c, *, address=FDC2214_I2C_ADDR_0):
        self._device = I2CDevice(i2c, address)
        # Check for valid chip ID
        if self._read16(FDC2214_DEVICE_ID) not in (0x3055,0x3054):
            raise RuntimeError('Failed to find FD2214, check wiring!')

        self._write16(FDC2214_MUX_CONFIG,         0x220D)
        self._write16(FDC2214_CONFIG,             0x9E01)
        self._write16(FDC2214_RCOUNT_CH0,         0xFFFF)
        self._write16(FDC2214_RCOUNT_CH1,         0xFFFF)
        self._write16(FDC2214_RCOUNT_CH2,         0xFFFF)
        self._write16(FDC2214_RCOUNT_CH3,         0xFFFF)
        self._write16(FDC2214_OFFSET_CH0,         0x0000)
        self._write16(FDC2214_OFFSET_CH1,         0x0000)
        self._write16(FDC2214_OFFSET_CH2,         0x0000)
        self._write16(FDC2214_OFFSET_CH3,         0x0000)
        self._write16(FDC2214_SETTLECOUNT_CH0,    0x0400)
        self._write16(FDC2214_SETTLECOUNT_CH1,    0x0400)
        self._write16(FDC2214_SETTLECOUNT_CH2,    0x0400)
        self._write16(FDC2214_SETTLECOUNT_CH3,    0x0400)
        self._write16(FDC2214_CLOCK_DIVIDERS_CH0, 0x1001)
        self._write16(FDC2214_CLOCK_DIVIDERS_CH1, 0x1001)
        self._write16(FDC2214_CLOCK_DIVIDERS_CH2, 0x1001)
        self._write16(FDC2214_CLOCK_DIVIDERS_CH3, 0x1001)
        self._write16(FDC2214_DRIVE_CH0,          0x8C40)
        self._write16(FDC2214_DRIVE_CH1,          0x8C40)
        self._write16(FDC2214_DRIVE_CH2,          0x8C40)
        self._write16(FDC2214_DRIVE_CH3,          0x8800)
        self._Fsense = self._Csense = 0
        self._channel = 2
        self._MSB = FDC2214_DATA_CH2_MSB
        self._LSB = FDC2214_DATA_CH2_LSB

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel=2):
        if channel not in (0,1,2,3):
            raise ValueError("Unsupported channel.")
        if channel == 0:
            self._write16(FDC2214_MUX_CONFIG, 0x020D)
            self._write16(FDC2214_CONFIG,     0x1E01)
            self._MSB = FDC2214_DATA_CH0_MSB
            self._LSB = FDC2214_DATA_CH0_LSB
        if channel == 1:
            self._write16(FDC2214_MUX_CONFIG, 0x020D)
            self._write16(FDC2214_CONFIG,     0x5E01)
            self._MSB = FDC2214_DATA_CH1_MSB
            self._LSB = FDC2214_DATA_CH1_LSB
        if channel == 2:
            self._write16(FDC2214_MUX_CONFIG, 0x220D)
            self._write16(FDC2214_CONFIG,     0x9E01)
            self._MSB = FDC2214_DATA_CH2_MSB
            self._LSB = FDC2214_DATA_CH2_LSB
        if channel == 3:
            self._write16(FDC2214_MUX_CONFIG, 0x420D)
            self._write16(FDC2214_CONFIG,     0xDE01)
            self._MSB = FDC2214_DATA_CH3_MSB
            self._LSB = FDC2214_DATA_CH3_LSB
        self._channel = channel

    def _read_into(self, address, buf, count=None):
        # Read bytes from the specified address into the provided buffer.
        # If count is not specified (the default) the entire buffer is filled,
        # otherwise only count bytes are copied in.
        assert len(buf) > 0
        if count is None:
            count = len(buf)
        with self._device as i2c:
            i2c.write_then_readinto(bytes([address & 0xFF]), buf,
                                    in_end=count, stop=False)    
    def _read16(self, address):
        # Read a 16-bit unsigned value for from the specified address.
        self._read_into(address, self._BUFFER, count=2)
        return self._BUFFER[0] << 8 | self._BUFFER[1]

    def _write16(self, address, value):
        # Rrite a 16-bit unsigned value to the specified address.
        with self._device as i2c:
            self._BUFFER[0] = address & 0xFF
            self._BUFFER[1] = (value >> 8) & 0xFF
            i2c.write(self._BUFFER, end=2)

    def _read_raw(self):
        _reading = (self._read16(self._MSB) & FDC2214_DATA_CHx_MASK_DATA) << 16
        _reading |= self._read16(self._LSB)
        return _reading

    def read(self):
        _reading = self._read_raw()
        try:
            # calculate fsensor (40MHz external ref)
            self._Fsense=_reading*(40e6)/(2**28)
            # calculate Csensor (18uF and 33pF LC tank)
            self._Csense = (1e12)*((1/((18e-6)*(2*pi*self._Fsense)**2))-(33e-12))
        except:
            print('error on read')
        return self._Csense
