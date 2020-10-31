# IMPORTS
import time
import board
import busio
from ht16k33matrixcolour import HT16K33MatrixColour

# CONSTANTS
DELAY = 0.01
PAUSE = 5

# START
if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    while not i2c.try_lock():
        pass
    display = HT16K33MatrixColour(i2c)
    display.set_brightness(2)

    #icon = b"\x3C\x42\xA9\x85\x85\xA9\x42\x3C"
    #display.set_icon(icon, 1).draw()

    display.plot(1, 1, HT16K33MatrixColour.COLOUR_YELLOW).plot(3, 4, HT16K33MatrixColour.COLOUR_GREEN).plot(6, 6, HT16K33MatrixColour.COLOUR_RED).draw()
    time.sleep(PAUSE)
    display.set_angle(1).draw()
    time.sleep(PAUSE)
    display.set_angle(2).draw()
    time.sleep(PAUSE)
    display.set_angle(3).draw()