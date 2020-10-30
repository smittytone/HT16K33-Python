# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33segmentalpha import HT16K33SegmentAlpha

# CONSTANTS
DELAY = 1

# START
if __name__ == '__main__':
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    print(i2c.scan())

    display = HT16K33SegmentAlpha(i2c, 0x71)
    display.set_brightness(2)
    display.set_number(4,3)
