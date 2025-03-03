# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33MatrixMulti

# CONSTANTS
DELAY = 0.01
PAUSE = 3
DISPLAY_COUNT = 4

# START
if __name__ == '__main__':
    # Configured for the Raspberry Pi Pico -- update for your own setup
    i2c = I2C(0, scl=Pin(9), sda=Pin(8))
    
    # Assume four displays arranged left to right with addresses 0x70-0x73
    display = HT16K33MatrixMulti(i2c, DISPLAY_COUNT)
    display.set_brightness(2)
    display.clear()

    # Scroll
    image_ints = [0x01,0x03,0x07,0x0F,0x1D,0x3F,0x7F,0xEB,0xFF,0x77,0x3E,0x1F,0x0D,0x07,0x03,0x01,0x01,0x03,0x07,0x0D,0x0F,0x07,0x03,0x01,0x01,0x03,0x07,0x0F,0x1D,0x3F,0x7F,0xEB,0xFF,0x77,0x3E,0x1F,0x0D,0x07,0x03,0x01,0x01,0x03,0x07,0x0D,0x0F,0x07,0x03,0x01,0xC1,0xC3,0x07,0x0F,0x0F,0x07,0x03,0x01]
    image_bytes = bytes(image_ints)

    # Show an animation
    display.scroll_image(image_bytes, 0.05, True)
    #display.scroll_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ", 0.05, True)
