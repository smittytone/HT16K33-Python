# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33segment import HT16K33Segment

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# START
if __name__ == '__main__':
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    display = HT16K33Segment(i2c)
    display.set_brightness(2)

    sync_text = b"\x6D\x6E\x37\x39"
    for i in range(len(sync_text)):
        display.set_glyph(sync_text[i], i)
    display.draw()

    time.sleep(PAUSE)
    display.clear().draw()

    sync_text = b"\x6D\x6E\x37\x39"
    for i in range(len(sync_text)):
        display.set_glyph(sync_text[i], i, True)
    display.draw()

    time.sleep(PAUSE)
    display.set_character("B", 0).set_character("E", 1)
    display.set_character("E", 2).set_character("F", 3)
    display.draw()

    time.sleep(PAUSE)
    display.clear().draw()

    count = 1100
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
        display.set_colon(colon_state).update()

        count -= 1
        if count < 0: break

        # Pause for breath
        time.sleep(DELAY)

    display.set_blink_rate(1)