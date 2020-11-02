# IMPORTS
import time
import board
import busio
from ht16k33matrixcolour import HT16K33MatrixColour

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    while not i2c.try_lock():
        pass
    display = HT16K33MatrixColour(i2c)
    display.set_brightness(2)
    """
    icon = b"\xE4\x9C\xE4\x9C\xE4\x9C\xE4\x9C\xE4\x9C\xE4\x9C\xE4\x9C\xE4\x9C"
    display.set_icon(icon).draw()
    time.sleep(PAUSE)
    display.set_angle(1).draw()
    time.sleep(PAUSE)
    display.set_angle(2).draw()
    time.sleep(PAUSE)
    display.set_angle(3).draw()
    time.sleep(PAUSE)
    """
    icon = b"\x00\x00\x00\x00\x4F\x01\x50\x85\x50\x24\x50\x05\x54\x05\x54\x05"
    display.define_character(icon, 0)
    display.set_angle(0).set_icon(icon).draw()
    time.sleep(PAUSE)

    display.set_blink_rate(1)
    time.sleep(PAUSE)

    display.set_blink_rate(0)
    """
    display.fill(HT16K33MatrixColour.COLOUR_RED).draw()
    time.sleep(PAUSE)
    display.fill(HT16K33MatrixColour.COLOUR_NONE).draw()
    time.sleep(PAUSE)
    display.fill(HT16K33MatrixColour.COLOUR_YELLOW).draw()
    time.sleep(PAUSE)
    """
    display.fill(HT16K33MatrixColour.COLOUR_GREEN).draw()
    time.sleep(PAUSE)

    display.set_character(38, HT16K33MatrixColour.COLOUR_YELLOW, HT16K33MatrixColour.COLOUR_GREEN, True).draw()
    time.sleep(PAUSE)

    s = "abcdefghijklmnopqrstuvwxyz0123456789 \x00"
    display.scroll_text(s, HT16K33MatrixColour.COLOUR_RED, HT16K33MatrixColour.COLOUR_GREEN)
