# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33segmentgen import HT16K33SegmentGen

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    # Delete or comment out all but one of the following i2c instantiations
    i2c = I2C(1, scl=Pin(3), sda=Pin(2))  # Adafruit QTPy RP2040

    display = HT16K33SegmentGen(i2c)
    display.set_brightness(2)
    #display.rotate()

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
        count = 1100
        while True:
            # Convert 'count' into Binary-Coded Decimal (BCD)
            bcd = int(str(count), 16)

            # Display 'count' as decimal digits
            display.set_number((bcd & 0xF000) >> 12, 0)
            display.set_number((bcd & 0x0F00) >> 8, 1)
            display.set_number((bcd & 0xF0) >> 4, 2)
            display.set_number((bcd & 0x0F), 3)

            bcd = int(str(1100 - count), 16)
            display.set_number((bcd & 0xF000) >> 12, 4)
            display.set_number((bcd & 0x0F00) >> 8, 5)
            display.set_number((bcd & 0xF0) >> 4, 6)
            display.set_number((bcd & 0x0F), 7)
            display.draw()

            count -= 1
            if count < 0: break

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

