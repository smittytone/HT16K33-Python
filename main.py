# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33SegmentGen

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    # Configured for the Raspberry Pi Pico -- update for your own setup
    i2c = I2C(0, scl=Pin(9), sda=Pin(8))

    display = HT16K33SegmentGen(i2c)
    display.set_brightness(2)

    sync_text = b"\x6D\x6E\x37\x39"
    runs = 2
    while True:
        # Write 'SYNC' to the LED using custom glyphs
        display.clear()
        for i in range(len(sync_text)):
            display.set_glyph(sync_text[i], i)
            display.set_glyph(sync_text[i], i + 4)
        display.draw()
        time.sleep(PAUSE)

        # Write 'SYNC' to the LED -- this time with decimal points
        for i in range(len(sync_text)):
            display.set_glyph(sync_text[i], i, True)
            display.set_glyph(sync_text[i], i + 4, True)
        display.draw()
        time.sleep(PAUSE)

        # Write 'BEEF' to the display using the charset characters
        display.set_character("B", 0).set_character("E", 1)
        display.set_character("E", 2).set_character("F", 3)
        display.set_character("B", 4).set_character("E", 5)
        display.set_character("E", 6).set_character("F", 7)
        display.draw()
        time.sleep(PAUSE)

        display.set_character(" ", 2).set_character(" ", 3)
        display.set_character(" ", 6).set_character(" ", 7)
        display.draw()
        time.sleep(PAUSE)

        # Show a countdown using the charset numbers
        # (also uses 'set_colon()')
        count = 0
        while True:
            # Convert 'count' into Binary-Coded Decimal (BCD)
            bcd = int(str(count), 16)

            # Display 'count' as decimal digits
            display.set_number((bcd & 0xF0000000) >> 28, 0)
            display.set_number((bcd & 0x0F000000) >> 24, 1)
            display.set_number((bcd & 0x00F00000) >> 20, 2)
            display.set_number((bcd & 0x000F0000) >> 16, 3)

            #bcd = int(str(0000 - count), 16)
            display.set_number((bcd & 0x0000F000) >> 12, 4)
            display.set_number((bcd & 0x00000F00) >> 8, 5, True)
            display.set_number((bcd & 0x000000F0) >> 4, 6)
            display.set_number((bcd & 0x0000000F), 7)
            display.draw()

            count += 100
            if count >= 99999999: break

        # Pause for breath
        time.sleep(DELAY)

        # Flash the LED
        display.set_blink_rate(1)
        time.sleep(PAUSE)
        display.set_blink_rate(0)
        time.sleep(PAUSE)

        runs -= 1
        if runs < 1:
            break

