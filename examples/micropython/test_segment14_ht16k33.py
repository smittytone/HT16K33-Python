# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33segment14 import HT16K33Segment14

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    # Delete or comment out all but one of the following i2c instantiations
    i2c = I2C(0, scl=Pin(9), sda=Pin(8))    # Raspberry Pi Pico
    i2c = I2C(0, scl=Pin(5), sda=Pin(4))    # Adafruit Feather Huzzah ESP8256
    i2c = I2C(0, scl=Pin(17), sda=Pin(16))  # SparkFun ProMicro 2040
    display = HT16K33Segment14(i2c, is_ht16k33=True)
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