# Import the base class
from ht16k33 import HT16K33

class HT16K33SegmentAlpha(HT16K33):
    """
    Micro/Circuit Python class for the Adafruit 0.54-in 4-digit,
    16-segment LED matrix backpack.

    Version:    3.0.0
    Bus:        I2C
    Author:     Tony Smith (@smittytone)
    License:    MIT
    """

    # *********** CONSTANTS **********

    HT16K33_SEGMENT_COLON_ROW = 0x04
    HT16K33_SEGMENT_MINUS_CHAR = 0x10
    HT16K33_SEGMENT_DEGREE_CHAR = 0x11

    # Bytearray of the key alphanumeric characters we can show:
    # 0-9, A-F, minus, degree
    CHARSET = b'\x00\x3F\x12\x00\x00\xDB\x00\x8F\x12\xE0\x00\xED\x00\xFD\x0C\x01\x00\xFF\x00\xEF\x00\xF7\x12\x8F\x00\x39\x12\x0F\x00\x79\x00\x71\x00\xBD\x00\xF6\x12\x00\x00\x1E\x24\x70\x00\x38\x05\x36\x21\x36\x00\x3F\x00\xF3\x20\x3F\x20\xF3\x00\xED\x12\x01\x00\x3E\x0C\x30\x28\x36\x2D\x00\x15\x00\x0C\x09\x10\x58\x20\x78\x00\xD8\x08\x8E\x08\x58\x0C\x80\x04\x8E\x10\x70\x10\x00\x00\x0E\x36\x00\x00\x30\x10\xD4\x10\x50\x00\xDC\x01\x70\x04\x86\x00\x50\x20\x88\x00\x78\x00\x1C\x20\x04\x28\x14\x28\xC0\x20\x0C\x08\x48\x00\x00\x00\x06\x02\x20\x12\xCE\x12\xED\x0C\x24\x23\x5D\x04\x00\x24\x00\x09\x00\x3F\xC0\x12\xC0\x08\x00\x00\xC0\x00\x00\x0C\x00'

    # *********** CONSTRUCTOR **********

    def __init__(self, i2c, i2c_address=0x70):
        if i2c_address < 0 or i2c_address > 255: return None
        self.buffer = bytearray(8)
        super(HT16K33SegmentAlpha, self).__init__(i2c, i2c_address)

    # *********** PUBLIC METHODS **********

    def set_colon(self, is_set=True):
        """
        Set or unset the display's central colon symbol.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            isSet (bool): Whether the colon is lit (True) or not (False). Default: True.
        """
        self.buffer[self.HT16K33_SEGMENT_COLON_ROW] = 0x02 if is_set is True else 0x00
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
        """
        if not 0 <= digit <= 3: return None
        self.buffer[digit] = glyph
        if has_dot is True: self.buffer[digit] |= 0x4000
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
        """
        return self.set_char(str(number), digit, has_dot)

    def set_character(self, char, digit=0, has_dot=False):
        """
        Present single alphanumeric character at the specified digit.

        Only characters from the class' character set are available:
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d ,e, f, -, degree symbol.
        Other characters can be defined and presented using 'set_glyph()'.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            char (string): The character to show.
            digit (int):   The digit to show the number. Default: 0 (leftmost digit).
            has_dot (bool): Whether the decimal point to the right of the digit should be lit. Default: False.
        """
        if not 0 <= digit <= 3: return None
        digit *= digit
        char = char.lower()
        if char in 'abcdef':
            char_val = ord(char) - 87
        elif char == '-':
            char_val = self.HT16K33_SEGMENT_MINUS_CHAR
        elif char in '0123456789':
            char_val = ord(char) - 48
        elif char == ' ':
            char_val = 0x00
        else:
            return

        self.buffer[digit] = self.CHARSET[char_val]
        self.buffer[digit + 1] = self.CHARSET[char_val + 1]
        if has_dot is True: self.buffer[digit] |= 0x40
        return self
