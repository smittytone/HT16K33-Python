# IMPORTS
import time
import board
import busio
from ht16k33quad import HT16K33Quad

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    while not i2c.try_lock():
        pass
    display = HT16K33Quad(i2c)
    display.set_brightness(2)
    display.clear()
    #display.set_digit(0x003F,3)

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
    while (a < 75):
        display.clear()
        display.set_code(a, 0)
        display.set_code(a + 1, 1)
        display.set_code(a + 2, 2)
        display.set_code(a + 3, 3)
        display.draw()
        a += 1
        time.sleep(0.5)
    time.sleep(5)