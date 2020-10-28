# IMPORTS
import time
import board
import busio
from ht16k33segmentalpha import HT16K33SegmentAlpha

# CONSTANTS
DELAY = 1

# START
if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    while not i2c.try_lock():
        pass
    display = HT16K33SegmentAlpha(i2c, 0x70)
    display.set_brightness(2)

    display.set_number(4,3)
