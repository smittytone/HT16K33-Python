# IMPORTS
import time
import board
import busio
from ht16k33 import HT16K33Segment14

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    # Configured for the Raspberry Pi Pico -- update for your own setup
    i2c = busio.I2C(scl=board.GP9, sda=board.GP8, frequency=10000)
    while not i2c.try_lock():
        pass

    display = HT16K33Segment14(i2c,is_ht16k33=True)
    display.set_brightness(2)
    display.clear()

    point_state = True
    while True:
        a = 65
        while (a < 88):
            display.clear()
            display.set_character(chr(a), 0, point_state)
            display.set_character(chr(a + 1), 1, point_state)
            display.set_character(chr(a + 2), 2, point_state)
            display.set_character(chr(a + 3), 3, point_state)
            display.draw()
            a += 1
            time.sleep(0.5)
        time.sleep(5)

        a = 97
        while (a < 120):
            display.clear()
            display.set_character(chr(a), 0, point_state)
            display.set_character(chr(a + 1), 1, point_state)
            display.set_character(chr(a + 2), 2, point_state)
            display.set_character(chr(a + 3), 3, point_state)
            display.draw()
            a += 1
            time.sleep(0.5)
        time.sleep(5)

        a = 0
        while (a < 7):
            display.clear()
            display.set_number(a, 0, point_state)
            display.set_number(a + 1, 1, point_state)
            display.set_number(a + 2, 2, point_state)
            display.set_number(a + 3, 3, point_state)
            display.draw()
            a += 1
            time.sleep(0.5)
        time.sleep(5)

        a = 63
        while (a < 73):
            display.clear()
            display.set_code(a, 0, point_state)
            display.set_code(a + 1, 1, point_state)
            display.set_code(a + 2, 2, point_state)
            display.set_code(a + 3, 3, point_state)
            display.draw()
            a += 1
            time.sleep(0.5)
        time.sleep(5)
        point_state = not point_state
