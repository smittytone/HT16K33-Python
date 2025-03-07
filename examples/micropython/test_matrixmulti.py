# IMPORTS
import utime as time
from urandom import randrange
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
    display.set_brightness(2).clear().draw()

    # Scroll
    image_ints = [0x01,0x03,0x07,0x0F,0x1D,0x3F,0x7F,0xEB,0xFF,0x77,0x3E,0x1F,0x0D,0x07,0x03,0x01,0x01,0x03,0x07,0x0D,0x0F,0x07,0x03,0x01,0x01,0x03,0x07,0x0F,0x1D,0x3F,0x7F,0xEB,0xFF,0x77,0x3E,0x1F,0x0D,0x07,0x03,0x01,0x01,0x03,0x07,0x0D,0x0F,0x07,0x03,0x01,0xC1,0xC3,0x07,0x0F,0x0F,0x07,0x03,0x01]
    image_bytes = bytes(image_ints)

    # Random plots across the display
    for i in range (0,33):    
        display.plot(randrange(0, 8 * DISPLAY_COUNT),randrange(0, 8))
    display.draw()
    time.sleep(PAUSE)

    # Show an image
    display.clear().draw()
    image = [0x3F,0x7e,0xcf,0xfe,0xcf,0x7e,0x3f]
    display.set_image(bytes(image), 6).draw()
    time.sleep(PAUSE)

    # Set and show a user-defined character
    image = [0x42,0x66,0xff,0xff,0x3c,0x18]
    display.define_character(bytes(image)).set_character(0,20).draw()
    time.sleep(PAUSE)

    # Test printing partially off the screen
    display.clear().draw()
    display.set_character(48,3).set_text("TEST", 17).draw()
    time.sleep(PAUSE)

    # Animation
    xor = False
    for i in range(0,4):
        x = DISPLAY_COUNT * 8 -1
        y = 0
        dx = 0
        dy = 1
        mx = DISPLAY_COUNT * 8 - 2
        my = 7
        nx = 0
        ny = 0

        for i in range(0, 64*DISPLAY_COUNT):
            display.plot(x, y, 1, xor).draw()

            if dx == 1 and x == mx:
                dy = 1
                dx = 0
                mx -= 1
            elif dx == -1 and x == nx:
                nx += 1
                dy = -1
                dx = 0
            elif dy == 1 and y == my:
                dy = 0
                dx = -1
                my -= 1
            elif dy == -1 and y == ny:
                dx = 1
                dy = 0
                ny += 1

            x += dx
            y += dy

            time.sleep(DELAY)
        xor = not xor

    time.sleep(DELAY)

    # Infinite scroll
    display.set_inverse().scroll_image(image_bytes, 0.05, True)
    #display.scroll_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ", 0.05, True)
