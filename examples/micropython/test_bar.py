# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33Bar

# CONSTANTS
DELAY = 0.1
PAUSE = 3
SUB_PAUSE = 1

# START
if __name__ == '__main__':
    # Configured for the Raspberry Pi Pico -- update for your own setup
    i2c = I2C(0, scl=Pin(9), sda=Pin(8))
    display = HT16K33Bar(i2c, i2c_address=0x74)
    display.set_brightness(8)

    while True:
        display.clear().draw()
        for i in range(0,24):
            display.set(i, HT16K33Bar.BAR_COLOUR_RED).draw()
            time.sleep(DELAY)
            display.set(i, HT16K33Bar.BAR_COLOUR_OFF).draw()
            time.sleep(DELAY)
        time.sleep(SUB_PAUSE)

        for i in range(0,24):
            display.set(i, HT16K33Bar.BAR_COLOUR_GREEN).draw()
            time.sleep(DELAY)
            display.set(i, HT16K33Bar.BAR_COLOUR_CLEAR).draw()
            time.sleep(DELAY)
        time.sleep(SUB_PAUSE)

        for i in range(0,24):
            display.set(i, HT16K33Bar.BAR_COLOUR_AMBER).draw()
            time.sleep(DELAY)
            display.set(i, HT16K33Bar.BAR_COLOUR_CLEAR).draw()
            time.sleep(DELAY)
        time.sleep(PAUSE)

        display.clear().draw()
        for i in range(0,24):
            display.fill(i, HT16K33Bar.BAR_COLOUR_RED).draw()
            time.sleep(DELAY)
        time.sleep(SUB_PAUSE)

        display.clear().draw()
        for i in range(0,24):
            display.fill(i, HT16K33Bar.BAR_COLOUR_GREEN).draw()
            time.sleep(DELAY)
        time.sleep(SUB_PAUSE)

        display.clear().draw()
        for i in range(0,24):
            display.fill(i, HT16K33Bar.BAR_COLOUR_AMBER).draw()
            time.sleep(DELAY)
        time.sleep(SUB_PAUSE)

        display.clear().draw()
        c = 1
        for i in range(0,24):
            display.fill(i, c).draw()
            c += 1
            if c > 3:
                c = 1
            time.sleep(DELAY)
        time.sleep(SUB_PAUSE)

        display.clear().draw()
        c = 1
        for i in range(0,24):
            display.set(i, c).draw()
            c += 1
            if c > 3:
                c = 1
            time.sleep(DELAY)
        time.sleep(PAUSE)
