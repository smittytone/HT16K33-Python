# IMPORTS
import time
import board
import busio
from ht16k33segment import HT16K33Segment

# CONSTANTS
DELAY = 0.01
PAUSE = 3

# FUNCTIONS
def run_tests(display=None):
    if display == None:
        assert display != None, "ERROR = No display supplied"

    # Write 'SYNC' to the LED using custom glyphs
    sync_text = b"\x6D\x6E\x37\x39"
    for i in range(len(sync_text)):
        display.set_glyph(sync_text[i], i)
    display.draw()
    time.sleep(PAUSE)

    # Write 'SYNC' to the LED -- this time with decimal points
    sync_text = b"\x6D\x6E\x37\x39"
    for i in range(len(sync_text)):
        display.set_glyph(sync_text[i], i, True)
    display.draw()
    time.sleep(PAUSE)

    # Write 'BEEF' to the display using the charset characters
    display.set_character("B", 0).set_character("E", 1)
    display.set_character("E", 2).set_character("F", 3)
    display.draw()
    time.sleep(PAUSE)

    display.set_character(" ", 0).set_character(" ", 3).draw()
    time.sleep(PAUSE)

    # Show a countdown using the charset numbers
    # (also uses 'set_colon()')
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
        display.set_colon(colon_state).draw()

        count -= 1
        if count < 0: break

        # Pause for breath
        time.sleep(DELAY)

# START
if __name__ == '__main__':
    # For any supported board's default I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    while not i2c.try_lock():
        pass
    display = HT16K33Segment(i2c)
    display.set_brightness(2)

    # Test pass 1
    run_tests(display)
    time.sleep(2)

    # Test pass 2
    display.rotate()
    run_tests(display)

    # Flash the LED
    display.set_blink_rate(1)
