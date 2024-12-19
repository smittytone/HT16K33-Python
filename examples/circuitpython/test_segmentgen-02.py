# IMPORTS
import time
import board
import busio
from ht16k33 import HT16K33SegmentGen

# CONSTANTS
DELAY = 0.01
PAUSE = 3

def clear(d):
    for i in range(0,8):
        d.set_number(0, i, False)

# START
if __name__ == '__main__':
    # Configured for the Raspberry Pi Pico -- update for your own setup
    i2c = busio.I2C(scl=board.GP9, sda=board.GP8, frequency=10000)
    while not i2c.try_lock():
        pass

    display = HT16K33SegmentGen(i2c)
    display.set_brightness(2)

    count = 1
    while True:
        # Convert 'count' into Binary-Coded Decimal (BCD)
        bcd = int(str(count), 16)
        display.clear().set_glyph(0x5E, 0)
        display.set_number((bcd & 0x0F00) >> 8, 5)
        display.set_number((bcd & 0xF0) >> 4, 6)
        display.set_number((bcd & 0x0F), 7)
        display.update()
        time.sleep(1)

        hs = f'{count:02x}'
        display.clear().set_glyph(0x74, 0)
        display.set_character(hs[0], 6, (hs[0] > '9'))
        display.set_character(hs[1], 7, (hs[1] > '9'))
        display.update()
        time.sleep(1)

        clear(display)
        for i in range(0,8):
            if count & (1 << i) != 0:
                display.set_number(1, 7 - i)
        display.update()
        time.sleep(1)

        count += 1
        if count > 255: break

    # Pause for breath
    time.sleep(3)
