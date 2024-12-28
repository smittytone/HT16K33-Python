# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33Segment14

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    # Configured for the Raspberry Pi Pico -- update for your own setup
    i2c = I2C(0,scl=Pin(9),sda=Pin(8))
    display = HT16K33Segment14(i2c,board=HT16K33Segment14.SPARKFUN_ALPHA)
    display.set_brightness(2)
    display.clear()

    while True:
        a = 65
        while (a < 88):
            display.clear()
            display.set_character(chr(a), 0)
            display.set_character(chr(a + 1), 1)
            display.set_character(chr(a + 2), 2)
            display.set_character(chr(a + 3), 3)
            display.draw()
            a += 1
            time.sleep(0.5)
        time.sleep(5)

        a = 97
        while (a < 120):
            display.clear()
            display.set_character(chr(a), 0)
            display.set_character(chr(a + 1), 1)
            display.set_character(chr(a + 2), 2)
            display.set_character(chr(a + 3), 3)
            display.draw()
            a += 1
            time.sleep(0.5)
        time.sleep(5)

        a = 0
        while (a < 7):
            display.clear()
            display.set_number(a, 0)
            display.set_number(a + 1, 1)
            display.set_number(a + 2, 2)
            display.set_number(a + 3, 3)
            display.draw()
            a += 1
            time.sleep(0.5)
        time.sleep(5)

        a = 63
        while (a < 73):
            display.clear()
            display.set_code(a, 0)
            display.set_code(a + 1, 1)
            display.set_code(a + 2, 2)
            display.set_code(a + 3, 3)
            display.draw()
            a += 1
            time.sleep(0.5)
        time.sleep(5)

        state = True
        display.clear()
        display.set_number(0, 0).set_number(0, 1)
        display.set_number(0, 2).set_number(0, 3)
        for i in range(0, 21):
            display.set_colon(state).set_decimal(not state).draw()
            time.sleep(0.5)
            state = not state
        time.sleep(5)
