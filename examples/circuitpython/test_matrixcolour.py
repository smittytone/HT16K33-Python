# IMPORTS
import time
import board
import busio
from random import randint
from ht16k33 import HT16K33MatrixColour

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    # Configured for the Raspberry Pi Pico -- update for your own setup
    i2c = busio.I2C(scl=board.GP1, sda=board.GP0, frequency=10000)
    while not i2c.try_lock():
        pass

    display = HT16K33MatrixColour(i2c)
    display.set_brightness(2)

    # Display a custom on the LED and rotate it
    icon = b"\xC3\x3C\xC3\x3D\xC3\x6D\xC3\xBE\xE7\x18\xF1\x0E\xFF\x00\xFF\x00"
    display.set_icon(icon).draw()
    time.sleep(PAUSE)
    display.set_angle(1).draw()
    time.sleep(PAUSE)
    display.set_angle(2).draw()
    time.sleep(PAUSE)
    display.set_angle(3).draw()
    time.sleep(PAUSE)

    # Store the custom icon and another
    display.define_character(icon, 1)
    icon = b"\xFF\x00\xFF\x00\xF1\x0E\xE7\x18\xC3\xBE\xC3\x6D\xC3\x3D\xC3\x3C"
    display.define_character(icon, 0)
    display.set_angle(0).set_icon(icon).draw()

    # Blink the display
    display.set_blink_rate(1)
    time.sleep(PAUSE)

    # Fill the LED with each of the colours
    display.set_blink_rate(0)
    display.fill(display.COLOUR_RED).draw()
    time.sleep(PAUSE)
    display.fill(display.COLOUR_NONE).draw()
    time.sleep(PAUSE)
    display.fill(display.COLOUR_YELLOW).draw()
    time.sleep(PAUSE)
    display.fill(display.COLOUR_GREEN).draw()
    time.sleep(PAUSE)

    # Display a charset character
    display.fill(display.COLOUR_RED)
    display.set_character(36, display.COLOUR_GREEN, display.COLOUR_RED, True).draw()
    time.sleep(PAUSE)

    # Scroll some text
    s = "    abcdefghijklmnopqrstuvwxyz 0123456789 $%&!\"# \x00\x01    "
    display.scroll_text(s, display.COLOUR_RED, display.COLOUR_GREEN)
    time.sleep(1)

    # Plot an X
    display.fill(display.COLOUR_NONE).draw()
    for i in range(4):
        display.plot(i, i, display.COLOUR_RED).plot(7 - i, i, display.COLOUR_RED)
        display.plot(i, 7 - i, display.COLOUR_RED).plot(7 - i, 7 - i, display.COLOUR_RED)
    display.draw()
    time.sleep(PAUSE)
    assert (display.is_set(0, 0) is True) and (display.is_set(0, 1) is False)
    display.clear().draw()

    # Show an animation
    while True:
        x = 7
        y = 0;
        dx = 0
        dy = 1;
        mx = 6
        my = 7;
        nx = 0
        ny = 0;
        colour = randint(0,3) + 1
        for i in range(0,64):
            display.plot(x, y, colour).draw();

            if dx == 1 and x == mx:
                dy = 1;
                dx = 0;
                mx -= 1;
            elif dx == -1 and x == nx:
                nx += 1;
                dy = -1;
                dx = 0;
            elif dy == 1 and y == my:
                dy = 0;
                dx = -1;
                my -= 1;
            elif dy == -1 and y == ny:
                dx = 1;
                dy = 0;
                ny += 1;

            x += dx;
            y += dy

            time.sleep(DELAY)

        x = 4
        y = 3
        dx = -1
        dy = 0
        mx = 5
        my = 4
        nx = 3
        ny = 2
        for i in range(0, 64):
            display.plot(x, y, 0).draw()

            if dx == 1 and x == mx:
                dy = -1;
                dx = 0;
                mx += 1;
            elif dx == -1 and x == nx:
                nx -= 1;
                dy = 1;
                dx = 0;
            elif dy == 1 and y == my:
                dy = 0;
                dx = 1;
                my += 1;
            elif dy == -1 and y == ny:
                dx = -1;
                dy = 0;
                ny -= 1;

            x += dx;
            y += dy

            time.sleep(DELAY)
