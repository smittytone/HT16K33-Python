from ht16k33 import HT16K33

class HT16K33Segment14(HT16K33):
    """
    Micro/Circuit Python class for the Adafruit 0.54in Quad Alphanumeric Display,
    a four-digit, 14-segment LED displays driven by the HT16K33 controller
    Version:    3.2.0
    Bus:        I2C
    Author:     Tony Smith (@smittytone)
    License:    MIT
    Copyright:  2022
    """

    # *********** CONSTANTS **********

    HT16K33_SEG14_DP_VALUE    = 0x4000
    HT16K33_SEG14_BLANK_CHAR  = 62
    HT16K33_SEG14_DQUOTE_CHAR = 64
    HT16K33_SEG14_QUESTN_CHAR = 65
    HT16K33_SEG14_DOLLAR_CHAR = 66
    HT16K33_SEG14_PRCENT_CHAR = 67
    HT16K33_SEG14_DEGREE_CHAR = 68
    HT16K33_SEG14_STAR_CHAR   = 72
    HT16K33_SEG14_PLUS_CHAR   = 73
    HT16K33_SEG14_MINUS_CHAR  = 74
    HT16K33_SEG14_DIVSN_CHAR  = 75
    HT16K33_SEG14_CHAR_COUNT  = 76

    # CHARSET store character matrices for 0-9, A-Z, a-z, space and various symbols
    CHARSET = b'\x00\x3F\x12\x00\x00\xDB\x00\x8F\x12\xE0\x00\xED\x00\xFD\x14\x01\x00\xFF\x00\xEF\x00\xF7\x12\x8F\x00\x39\x12\x0F\x00\x79\x00\x71\x00\xBD\x00\xF6\x12\x09\x00\x1E\x0C\x70\x00\x38\x05\x36\x09\x36\x00\x3F\x00\xF3\x08\x3F\x08\xF3\x00\xED\x12\x01\x00\x3E\x24\x30\x28\x36\x2D\x00\x15\x00\x24\x09\x10\x58\x08\x78\x00\xD8\x20\x8E\x20\x58\x24\x80\x04\x8E\x10\x70\x10\x00\x08\x06\x1E\x00\x20\x30\x10\xD4\x10\x50\x00\xDC\x01\x70\x04\x86\x00\x50\x08\x88\x00\x78\x00\x1C\x08\x04\x28\x14\x2D\x00\x25\x00\x20\x48\x00\x00\x00\x06\x02\x20\x10\x83\x12\xED\x24\x24\x00\xE3\x04\x00\x09\x00\x20\x00\x3F\xC0\x12\xC0\x00\xC0\x24\x00'


    # *********** CONSTRUCTOR **********

    def __init__(self, i2c, i2c_address=0x70, is_ht16k33=False):
        self.buffer = bytearray(16)
        self.is_ht16k33 = is_ht16k33
        super(HT16K33Segment14, self).__init__(i2c, i2c_address)


    # *********** PUBLIC FUNCTIONS **********

    def set_glyph(self, glyph, digit=0, has_dot=False):
        """
        Puts the input character matrix (a 16-bit integer) into the specified row,
        adding a decimal point if required. Character matrix value is calculated by
        setting the bit(s) representing the segment(s) you want illuminated:

                0                9
                _
            5 |   | 1        8 \ | / 10
              |   |             \|/
                             6  - -  7
            4 |   | 2           /|\
              | _ |         11 / | \ 13    . 14
                3                12
        Bit 14 is the period, but this is set with parameter 3
        Nb. Bit 15 is not read by the display

        Args:
            glyph (int):   The glyph pattern.
            digit (int):   The digit to show the glyph. Default: 0 (leftmost digit).

        Returns:
            The instance (self)
        """

        # Bail on incorrect row numbers or character values
        assert 0 <= digit < 4, "ERROR - Invalid digit (0-3) set in set_glyph()"
        assert 0 <= glyph < 0xFFFF, "ERROR - Invalid glyph (0x0000-0xFFFF) set in set_glyph()"

        # Write the character to the buffer
        if has_dot: glyph |= self.HT16K33_SEG14_DP_VALUE
        self.buffer[digit << 1] = (glyph >> 8) & 0xFF
        self.buffer[(digit << 1 + 1)] = glyph & 0xFF

    def set_number(self, number, digit=0, has_dot=False):
        """
        Present single decimal value (0-9) at the specified digit.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            number (int):  The number to show.
            digit (int):   The digit to show the number. Default: 0 (leftmost digit).

        Returns:
            The instance (self)
        """
        assert 0 <= digit < 4, "ERROR - Invalid digit (0-3) set in set_number()"
        assert 0 <= number < 10, "ERROR - Invalid value (0-9) set in set_number()"
        return self.set_character(str(number), digit)

    def set_character(self, char, digit=0):
        """
        Present single alphanumeric character at the specified digit.

        Only characters from the class' character set are available:
        Other characters can be defined and presented using 'set_glyph()'.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            char (string):  The character to show.
            digit (int):    The digit to show the number. Default: 0 (leftmost digit).

        Returns:
            The instance (self)
        """
        assert 0 <= digit < 4, "ERROR - Invalid digit set in set_character()"
        char_val = 0xFFFF
        if char == '-':
            char_val = self.HT16K33_SEG14_MINUS_CHAR
        elif char == '*':
            char_val = self.HT16K33_SEG14_STAR_CHAR
        elif char == '+':
            char_val = self.HT16K33_SEG14_PLUS_CHAR
        elif char == ' ':
            char_val = self.HT16K33_SEG14_BLANK_CHAR
        elif char == '/':
            char_val = self.HT16K33_SEG14_DIVSN_CHAR
        elif char == '$':
            char_val = self.HT16K33_SEG14_DOLLAR_CHAR
        elif char == ':':
            char_val = self.HT16K33_SEG14_DQUOTE_CHAR
        elif char in '0123456789':
            char_val = ord(char) - 48   # 0-9
        elif char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            char_val = ord(char) - 55   # 10-35
        elif char in 'abcdefghijklmnopqrstuvwxyz':
            char_val = ord(char) - 61   # 36-61
        assert char_val != 0xFFFF, "ERROR - Invalid char string set in set_character() " + char + " (" + str(ord(char)) + ")"
        self._set_digit((self.CHARSET[char_val << 1] << 8) | self.CHARSET[(char_val << 1) + 1], digit)
        return self

    def set_code(self, code, digit):
        """
        Present single alphanumeric character at the specified digit.

        Only characters from the class' character set are available:
        Other characters can be defined and presented using 'set_glyph()'.

        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'update()' to render the buffer on the display.

        Args:
            code (int):     The character's class-specific code.
            digit (int):    The digit to show the number. Default: 0 (leftmost digit).

        Returns:
            The instance (self)
        """
        assert 0 <= digit < 4, "ERROR - Invalid digit (0-3) set in set_code()"
        assert 0 <= code < HT16K33_SEG14_CHAR_COUNT, "ERROR - Invalid code (0-{:d}) set in set_code()".format(self.HT16K33_SEG14_CHAR_COUNT - 1)
        self._set_digit((self.CHARSET[code << 1] << 8) | self.CHARSET[(code << 1) + 1], digit)
        return self


    # *********** PRIVATE FUNCTIONS (DO NOT CALL) **********

    def _set_digit(self, value, digit):
        if self.is_ht16k33:
            # Output for HT16K33: swap bits 11 and 13,
            # and sequence becomes LSB, MSB
            msb = (value >> 8) & 0xFF
            b11 = msb & 0x08
            b13 = msb & 0x20
            msb &= 0xD7
            msb |= (b11 << 2)
            msb |= (b13 >> 2)
            self.buffer[(digit << 1) + 1] = msb
            self.buffer[digit << 1] = value & 0xFF
        else:
            # Output for VK16K33
            a = 0
            d = 1
            for i in range(0, 16):
                if (value & (1 << i)):
                    self.buffer[a] |= (d << digit)
                a += 2
                if i == 6:
                    a = 0
                    d = 16
        return self
