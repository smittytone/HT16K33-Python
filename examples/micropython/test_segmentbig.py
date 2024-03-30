# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33SegmentBig

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    # Delete or comment out all but one of the following i2c instantiations
    i2c = I2C(0, scl=Pin(9), sda=Pin(8))    # Raspberry Pi Pico
    i2c = I2C(0, scl=Pin(5), sda=Pin(4))    # Adafruit Feather Huzzah ESP8256
    i2c = I2C(0, scl=Pin(17), sda=Pin(16))  # SparkFun ProMicro 2040
    i2c = I2C(1, scl=Pin(23), sda=Pin(22))  # Adafruit QTPy RP2040

    display = HT16K33SegmentBig(i2c)
    display.set_brightness(2)

    # Write 'SYNC' to the LED using custom glyphs
    sync_text = b"\x6D\x6E\x37\x39"
    for i in range(len(sync_text)):
        display.set_glyph(sync_text[i], i)
    display.draw()
    time.sleep(PAUSE)

    # Write 'SYNC' to the LED -- this time with decimal points
    for i in range(len(sync_text)):
        display.set_glyph(sync_text[i], i)
    display.set_colon(display.COLON_CENTRE | display.COLON_LEFT | display.DECIMAL_POINT).draw()
    time.sleep(PAUSE)

    # Write 'BEEF' to the display using the charset characters
    display.set_character("B", 0).set_character("E", 1)
    display.set_character("E", 2).set_character("F", 3)
    display.set_colon(0).draw()
    time.sleep(PAUSE)

    display.set_character(" ", 0).set_character(" ", 3).draw()
    time.sleep(PAUSE)

    # Show a countdown using the charset numbers
    # (also uses 'set_colon()')
    count = 9999
    colon_state = True
    while True:
        # Convert 'count' into Binary-Coded Decimal (BCD)
        bcd = int(str(count), 16)

        # Display 'count' as decimal digits
        display.set_number((bcd & 0xF000) >> 12, 0)
        display.set_number((bcd & 0x0F00) >> 8, 1)
        display.set_number((bcd & 0xF0) >> 4, 2)
        display.set_number((bcd & 0x0F), 3)

        if count % 10 == 0: colon_state = not colon_state
        display.set_colon(0x02 if colon_state else 0x00).draw()

        count -= 1
        if count < 0: break

        # Pause for breath
        time.sleep(DELAY)

    # Flash the LED
    display.set_blink_rate(1)
