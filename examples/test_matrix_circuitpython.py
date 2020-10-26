# IMPORTS
import time
import board
import busio
from random import randint
from ht16k33matrixfeatherwing import HT16K33MatrixFeatherWing

# CONSTANTS
DELAY = 0.01
PAUSE = 4

# START
if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    while not i2c.try_lock():
        pass
    display = HT16K33MatrixFeatherWing(i2c)
    display.set_brightness(2)

    sync_text = "ABC"
    col = 0
    for i in range(len(sync_text)):
        display.set_character(ord(sync_text[i]), col)
        col += 6
    display.draw()

    time.sleep(PAUSE)
    display.clear().draw()

    icon = b"\x3C\x42\xA9\x85\x85\xA9\x42\x3C"
    display.set_icon(icon, 4).draw()

    time.sleep(PAUSE)
    display.clear().draw()

    icon = b"\x00\x00\x0E\x18\xBE\x6D\x3D\x3C"
    display.define_character(icon, 0)
    icon = b"\x3C\x3D\x6D\xBE\x18\x0E\x00\x00"
    display.define_character(icon, 1)
    display.set_character(0, 0).set_character(1, 8).draw()

    time.sleep(PAUSE)
    display.clear().draw()

    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 abcdefghijklmnopqrstuvwxyz !$%&*() \x00\x01"
    display.scroll_text(text)

    time.sleep(PAUSE)
    display.clear().draw()

    for i in range(64):
        while True:
            x = randint(0, 15)
            y = randint(0, 7)
            if not display.is_set(x, y): break
        display.plot(x, y).draw()
        time.sleep(0.5)

    display.set_blink_rate(1)