# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33matrix import HT16K33Matrix

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    display = HT16K33Matrix(i2c)
    display.set_brightness(2)

    icon = b"\x3C\x42\xA9\x85\x85\xA9\x42\x3C"
    display.set_icon(icon).draw()

    time.sleep(PAUSE)
    display.set_angle(900).draw()

    time.sleep(PAUSE)
    display.clear().draw()

    icon = b"\x0E\x18\xBE\x6D\x3D\x3C"
    display.define_character(icon, 0)
    icon = b"\x3C\x3D\x6D\xBE\x18\x0E"
    display.define_character(icon, 1)

    text = "0123456789 abcdefghijklmnopqrstuvwxyz !$%&*() \x00\x01"
    display.scroll_text(text)

    time.sleep(PAUSE)
    display.set_character(0, True).draw()

    time.sleep(PAUSE)
    display.set_inverse().draw()

    time.sleep(PAUSE)
    display.set_inverse().draw()

    time.sleep(PAUSE)
    display.clear().draw()

    for i in range(4):
        display.plot(i, i).plot(7 - i, i).plot(i, 7 - i).plot(7 - i, 7 - i)
    display.draw()
    display.set_blink_rate(1)