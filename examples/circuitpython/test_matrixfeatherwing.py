# IMPORTS
import time
import board
import busio
from random import randint
from ht16k33matrixfeatherwing import HT16K33MatrixFeatherWing

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    while not i2c.try_lock():
        pass
    display = HT16K33MatrixFeatherWing(i2c)
    display.set_brightness(2)

    # Show some charset characters on the LED
    sync_text = "BOO"
    col = 0
    for i in range(len(sync_text)):
        display.set_character(ord(sync_text[i]), col)
        col += 5
    display.draw()
    time.sleep(PAUSE)

    # Store custom characters
    icon = b"\x3C\x42\xA9\x85\x85\xA9\x42\x3C"
    display.clear().set_icon(icon, 4).draw()
    time.sleep(PAUSE)

    # Store custom characters
    icon = b"\x00\x00\x0E\x18\xBE\x6D\x3D\x3C"
    display.define_character(icon, 0)
    icon = b"\x3C\x3D\x6D\xBE\x18\x0E\x00\x00"
    display.define_character(icon, 1)
    display.clear().set_character(0, 0).set_character(1, 8).draw()
    time.sleep(PAUSE)

    # Scroll text
    display.clear().draw()
    text = "        0123456789 abcdefghijklmnopqrstuvwxyz !$%&*() \x00\x01        "
    display.scroll_text(text)
    time.sleep(PAUSE)

    # Plot random spots
    display.clear().draw()
    for i in range(32):
        while True:
            x = randint(0, 15)
            y = randint(0, 7)
            if not display.is_set(x, y): break
        display.plot(x, y).draw()
        time.sleep(0.5)
    time.sleep(PAUSE)

    # Invert the LED
    display.set_inverse().draw()
    time.sleep(PAUSE)

    # De-invert the LED
    display.set_inverse().draw()

    # And flash the display
    display.set_blink_rate(1)