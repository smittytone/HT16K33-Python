# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33Bar

# CONSTANTS
DELAY = 0.1
PAUSE = 3
SUB_PAUSE = 1

# FUNCTIONS
def tests(display):
        # Run a single bar up the display in each colour
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

        # Run a fill up the display in each colour
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

        # Fill and change the fill colour
        display.clear().draw()
        c = 1
        for i in range(0,24):
            display.fill(i, c).draw()
            c += 1
            if c > 3:
                c = 1
            time.sleep(DELAY)
        time.sleep(SUB_PAUSE)

        # Fill using set() to alternate colours
        display.clear().draw()
        c = 1
        for i in range(0,24):
            display.set(i, c).draw()
            c += 1
            if c > 3:
                c = 1
            time.sleep(DELAY)
        time.sleep(PAUSE)

        # Flash the display and reset
        display.set_blink_rate(2)
        time.sleep(PAUSE)
        display.set_blink_rate(0)
        time.sleep(PAUSE)

# START
if __name__ == '__main__':
    # Configured for the Raspberry Pi Pico -- update for your own setup
    i2c = I2C(0, scl=Pin(9), sda=Pin(8))

    while True:
        # Orient bar with zero alongside the HT16K33
        graph = HT16K33Bar(i2c)
        graph.set_brightness(8)
        tests(graph)

        # Orient bar with zero as the furthest segment from the HT16K33
        graph = HT16K33Bar(i2c, orientation=HT16K33Bar.BAR_ZERO_FURTHEST_FROM_CHIP)
        graph.set_brightness(8)
        tests(graph)
