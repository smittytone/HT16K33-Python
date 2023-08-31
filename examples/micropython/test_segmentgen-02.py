class HT16K33:
    """
    A simple, generic driver for the I2C-connected Holtek HT16K33 controller chip.
    This release supports MicroPython and CircuitPython

    Version:    3.5.0
    Bus:        I2C
    Author:     Tony Smith (@smittytone)
    License:    MIT
    Copyright:  2023
    """

    # *********** CONSTANTS **********

    HT16K33_GENERIC_DISPLAY_ON = 0x81
    HT16K33_GENERIC_DISPLAY_OFF = 0x80
    HT16K33_GENERIC_SYSTEM_ON = 0x21
    HT16K33_GENERIC_SYSTEM_OFF = 0x20
    HT16K33_GENERIC_DISPLAY_ADDRESS = 0x00
    HT16K33_GENERIC_CMD_BRIGHTNESS = 0xE0
    HT16K33_GENERIC_CMD_BLINK = 0x81

    # *********** PRIVATE PROPERTIES **********

    i2c = None
    address = 0
    brightness = 15
    flash_rate = 0

    # *********** CONSTRUCTOR **********

    def __init__(self, i2c, i2c_address):
        assert 0x00 <= i2c_address < 0x80, "ERROR - Invalid I2C address in HT16K33()"
        self.i2c = i2c
        self.address = i2c_address
        self.power_on()

    # *********** PUBLIC METHODS **********

    def set_blink_rate(self, rate=0):
        """
        Set the display's flash rate.

        Only four values (in Hz) are permitted: 0, 2, 1, and 0,5.

        Args:
            rate (int): The chosen flash rate. Default: 0Hz (no flash).
        """
        assert rate in (0, 0.5, 1, 2), "ERROR - Invalid blink rate set in set_blink_rate()"
        self.blink_rate = rate & 0x03
        self._write_cmd(self.HT16K33_GENERIC_CMD_BLINK | rate << 1)

    def set_brightness(self, brightness=15):
        """
        Set the display's brightness (ie. duty cycle).

        Brightness values range from 0 (dim, but not off) to 15 (max. brightness).

        Args:
            brightness (int): The chosen flash rate. Default: 15 (100%).
        """
        if brightness < 0 or brightness > 15: brightness = 15
        self.brightness = brightness
        self._write_cmd(self.HT16K33_GENERIC_CMD_BRIGHTNESS | brightness)

    def draw(self):
        """
        Writes the current display buffer to the display itself.

        Call this method after updating the buffer to update
        the LED itself.
        """
        self._render()

    def update(self):
        """
        Alternative for draw() for backwards compatibility
        """
        self._render()

    def clear(self):
        """
        Clear the buffer.

        Returns:
            The instance (self)
        """
        for i in range(0, len(self.buffer)): self.buffer[i] = 0x00
        return self

    def power_on(self):
        """
        Power on the controller and display.
        """
        self._write_cmd(self.HT16K33_GENERIC_SYSTEM_ON)
        self._write_cmd(self.HT16K33_GENERIC_DISPLAY_ON)

    def power_off(self):
        """
        Power on the controller and display.
        """
        self._write_cmd(self.HT16K33_GENERIC_DISPLAY_OFF)
        self._write_cmd(self.HT16K33_GENERIC_SYSTEM_OFF)

    # ********** PRIVATE METHODS **********

    def _render(self):
        """
        Write the display buffer out to I2C
        """
        buffer = bytearray(len(self.buffer) + 1)
        buffer[1:] = self.buffer
        buffer[0] = 0x00
        self.i2c.writeto(self.address, bytes(buffer))

    def _write_cmd(self, byte):
        """
        Writes a single command to the HT16K33. A private method.
        """
        self.i2c.writeto(self.address, bytes([byte]))
        
class HT16K33SegmentGen(HT16K33):
    """
    Micro/Circuit Python class for a generic 1-8-digit, 7-segment display.
    It assumes each digit has a decimal point, but there are no other
    symbol LEDs included.

    Version:    3.5.0
    Bus:        I2C
    Author:     Tony Smith (@smittytone)
    License:    MIT
    Copyright:  2023
    """

    # *********** CONSTANTS **********

    HT16K33_SEGMENT_MINUS_CHAR = 0x10
    HT16K33_SEGMENT_DEGREE_CHAR = 0x11
    HT16K33_SEGMENT_SPACE_CHAR = 0x12

    # Bytearray of the key alphanumeric characters we can show:
    # 0-9, A-F, minus, degree, space
    CHARSET = b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x5F\x7C\x58\x5E\x7B\x71\x40\x63\x00'

    # *********** CONSTRUCTOR **********

    def __init__(self, i2c, i2c_address=0x70, digits=8):
        self.buffer = bytearray(16)
        self.is_rotated = False
        # Check digits specified (must be 1 - 8)
        assert 0 < digits < 9, "ERROR - Invalid number of digits (1-8) in HT16K33Segment8()"
        self.max_digits = digits
        super(HT16K33SegmentGen, self).__init__(i2c, i2c_address)

    # *********** PUBLIC METHODS **********

    def rotate(self):
        """
        Rotate/flip the segment display.

        Returns:
            The instance (self)
        """
        self.is_rotated = not self.is_rotated
        return self

    def set_glyph(self, glyph, digit=0, has_dot=False):
        """
        Present a user-defined character glyph at the specified digit.

        Glyph values are 8-bit integers representing a pattern of set LED segments.
        The value is calculated by setting the bit(s) representing the segment(s) you want illuminated.
        Bit-to-segment mapping runs clockwise from the top around the outside of the matrix; the inner segment is bit 6:

                0
                _
            5 |   | 1
              |   |
                - <----- 6
            4 |   | 2
              | _ |
                3

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            glyph (int):   The glyph pattern.
            digit (int):   The digit to show the glyph. Default: 0 (leftmost digit).
            has_dot (bool): Whether the decimal point to the right of the digit should be lit. Default: False.

        Returns:
            The instance (self)
        """
        # Bail on incorrect row numbers or character values
        assert 0 <= digit < self.max_digits, "ERROR - Invalid digit set in set_glyph()"
        assert 0 <= glyph < 0x80, "ERROR - Invalid glyph (0x00-0x80) set in set_glyph()"

        self.buffer[digit << 1] = glyph
        if has_dot is True: self.buffer[digit << 1] |= 0x80
        return self

    def set_number(self, number, digit=0, has_dot=False):
        """
        Present single decimal value (0-9) at the specified digit.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            number (int):  The number to show.
            digit (int):   The digit to show the number. Default: 0 (leftmost digit).
            has_dot (bool): Whether the decimal point to the right of the digit should be lit. Default: False.

        Returns:
            The instance (self)
        """
        # Bail on incorrect row numbers or character values
        assert 0 <= digit < self.max_digits, "ERROR - Invalid digit set in set_number()"
        assert 0 <= number < 10, "ERROR - Invalid value (0-9) set in set_number()"

        return self.set_character(str(number), digit, has_dot)

    def set_character(self, char, digit=0, has_dot=False):
        """
        Present single alphanumeric character at the specified digit.

        Only characters from the class' character set are available:
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d ,e, f, -.
        Other characters can be defined and presented using 'set_glyph()'.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            char (string):  The character to show.
            digit (int):    The digit to show the number. Default: 0 (leftmost digit).
            has_dot (bool): Whether the decimal point to the right of the digit should be lit. Default: False.

        Returns:
            The instance (self)
        """
        # Bail on incorrect row numbers
        assert 0 <= digit < self.max_digits, "ERROR - Invalid digit set in set_character()"

        char = char.lower()
        char_val = 0xFF
        if char == "deg":
            char_val = self.HT16K33_SEGMENT_DEGREE_CHAR
        elif char == '-':
            char_val = self.HT16K33_SEGMENT_MINUS_CHAR
        elif char == ' ':
            char_val = self.HT16K33_SEGMENT_SPACE_CHAR
        elif char in 'abcdef':
            char_val = ord(char) - 87
        elif char in '0123456789':
            char_val = ord(char) - 48

        # Bail on incorrect character values
        assert char_val != 0xFF, "ERROR - Invalid char string set in set_character()"

        self.buffer[digit << 1] = self.CHARSET[char_val]
        if has_dot is True: self.buffer[digit << 1] |= 0x80
        return self

    def draw(self):
        """
        Writes the current display buffer to the display itself.

        Call this method after updating the buffer to update
        the LED itself. Rotation handled here.
        """
        if self.is_rotated:
            # Swap digits 0,(max - 1), 1,(max - 2) etc
            if self.max_digits > 1:
                for i in range(0, self.max_digits):
                    swap = self.max_digits - i - 1
                    if i != swap:
                        a = self.buffer[i << 1]
                        self.buffer[i << i] = self.buffer[swap << 1]
                        self.buffer[swap << 1] = a

            # Flip each digit
            for i in range(0, self.max_digits):
                a = self.buffer[i << 1]
                b = (a & 0x07) << 3
                c = (a & 0x38) >> 3
                a &= 0xC0
                self.buffer[i << 1] = (a | b | c)
        self._render()
        
 # IMPORTS
import utime as time
from machine import I2C, Pin, RTC

# CONSTANTS
DELAY = 0.01
PAUSE = 3

def clear(d): 
    for i in range(0,8):
        d.set_number(0, i, False)

# START
if __name__ == '__main__':
    # Delete or comment out all but one of the following i2c instantiations
    i2c = I2C(1, scl=Pin(3), sda=Pin(2))  # Adafruit QTPy RP2040

    display = HT16K33SegmentGen(i2c)
    display.set_brightness(2)

    while True:
        count = 1
        while True:
            # Convert 'count' into Binary-Coded Decimal (BCD)
            bcd = int(str(count), 16)
            display.clear().set_glyph(0x5E, 0)
            display.set_number((bcd & 0x0F00) >> 8, 5)
            display.set_number((bcd & 0xF0) >> 4, 6)
            display.set_number((bcd & 0x0F), 7)
            display.update()
            time.sleep(1)
            
            hs = f'{count:02x}'
            display.clear().set_glyph(0x74, 0)
            display.set_character(hs[0], 6)
            display.set_character(hs[1], 7)
            display.update()
            time.sleep(1)

            clear(display)
            for i in range(0,8):
                if count & (1 << i) != 0:
                    display.set_number(1, 7 - i)
            display.update()
            time.sleep(1)

            count += 1
            if count > 255: break

        # Pause for breath
        time.sleep(3)

