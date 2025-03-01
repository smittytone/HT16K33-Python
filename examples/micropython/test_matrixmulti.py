# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33MatrixMulti

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    # Configured for the Raspberry Pi Pico -- update for your own setup
    i2c = I2C(0, scl=Pin(9), sda=Pin(8))
    display = HT16K33MatrixMulti(i2c, 2)
    display.set_brightness(2)
    display.clear()

    # Scroll
    image_ints = [0x01,0x03,0x07,0x0F,0x1D,0x3F,0x7F,0xEB,0xFF,0x77,0x3E,0x1F,0x0D,0x07,0x03,0x01,0x01,0x03,0x07,0x0D,0x0F,0x07,0x03,0x01,0x01,0x03,0x07,0x0F,0x1D,0x3F,0x7F,0xEB,0xFF,0x77,0x3E,0x1F,0x0D,0x07,0x03,0x01,0x01,0x03,0x07,0x0D,0x0F,0x07,0x03,0x01,0xC1,0xC3,0x07,0x0F,0x0F,0x07,0x03,0x01]
    #image_ints = [0x01,0x03,0x07,0x0F,0x1D]
    image_bytes = bytes(image_ints)

    # Show an animation
    display.scroll_image(image_bytes, 0.1, True)
    #display.scroll_text("Rename an imported class using the as keyword. ", do_loop=True)
