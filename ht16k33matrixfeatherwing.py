# Import the base class
from ht16k33 import HT16K33

class HT16K33MatrixFeatherWing(HT16K33):
    """
    Micro/Circuit Python class for the Adafruit 0.8-in
    16x8 LED matrix FeatherWing.

    Version:    3.0.0
    Bus:        I2C
    Author:     Tony Smith (@smittytone)
    License:    MIT
    """

    # *********** CONSTANTS **********

    CHARSET = [
        b"\x00\x00",              # space - Ascii 32
        b"\xfa",                  # !
        b"\xc0\x00\xc0",          # "
        b"\x24\x7e\x24\x7e\x24",  # #
        b"\x24\xd4\x56\x48",      # $
        b"\xc6\xc8\x10\x26\xc6",  # %
        b"\x6c\x92\x6a\x04\x0a",  # &
        b"\xc0",                  # '
        b"\x7c\x82",              # (
        b"\x82\x7c",              # )
        b"\x10\x7c\x38\x7c\x10",  # *
        b"\x10\x10\x7c\x10\x10",  # +
        b"\x06\x07",              # ,
        b"\x10\x10\x10\x10",      # -
        b"\x06\x06",              # .
        b"\x04\x08\x10\x20\x40",  # /
        b"\x7c\x8a\x92\xa2\x7c",  # 0 - Ascii 48
        b"\x42\xfe\x02",          # 1
        b"\x46\x8a\x92\x92\x62",  # 2
        b"\x44\x92\x92\x92\x6c",  # 3
        b"\x18\x28\x48\xfe\x08",  # 4
        b"\xf4\x92\x92\x92\x8c",  # 5
        b"\x3c\x52\x92\x92\x8c",  # 6
        b"\x80\x8e\x90\xa0\xc0",  # 7
        b"\x6c\x92\x92\x92\x6c",  # 8
        b"\x60\x92\x92\x94\x78",  # 9
        b"\x36\x36",              # : - Ascii 58
        b"\x36\x37",              #
        b"\x10\x28\x44\x82",      # <
        b"\x24\x24\x24\x24\x24",  # =
        b"\x82\x44\x28\x10",      # >
        b"\x60\x80\x9a\x90\x60",  # ?
        b"\x7c\x82\xba\xaa\x78",  # @
        b"\x7e\x90\x90\x90\x7e",  # A - Ascii 65
        b"\xfe\x92\x92\x92\x6c",  # B
        b"\x7c\x82\x82\x82\x44",  # C
        b"\xfe\x82\x82\x82\x7c",  # D
        b"\xfe\x92\x92\x92\x82",  # E
        b"\xfe\x90\x90\x90\x80",  # F
        b"\x7c\x82\x92\x92\x5c",  # G
        b"\xfe\x10\x10\x10\xfe",  # H
        b"\x82\xfe\x82",          # I
        b"\x0c\x02\x02\x02\xfc",  # J
        b"\xfe\x10\x28\x44\x82",  # K
        b"\xfe\x02\x02\x02",      # L
        b"\xfe\x40\x20\x40\xfe",  # M
        b"\xfe\x40\x20\x10\xfe",  # N
        b"\x7c\x82\x82\x82\x7c",  # O
        b"\xfe\x90\x90\x90\x60",  # P
        b"\x7c\x82\x92\x8c\x7a",  # Q
        b"\xfe\x90\x90\x98\x66",  # R
        b"\x64\x92\x92\x92\x4c",  # S
        b"\x80\x80\xfe\x80\x80",  # T
        b"\xfc\x02\x02\x02\xfc",  # U
        b"\xf8\x04\x02\x04\xf8",  # V
        b"\xfc\x02\x3c\x02\xfc",  # W
        b"\xc6\x28\x10\x28\xc6",  # X
        b"\xe0\x10\x0e\x10\xe0",  # Y
        b"\x86\x8a\x92\xa2\xc2",  # Z - Ascii 90
        b"\xfe\x82\x82",          # [
        b"\x40\x20\x10\x08\x04",  # \
        b"\x82\x82\xfe",          # ]
        b"\x20\x40\x80\x40\x20",  # ^
        b"\x02\x02\x02\x02\x02",  # _
        b"\xc0\xe0",              # '
        b"\x04\x2a\x2a\x1e",      # a - Ascii 97
        b"\xfe\x22\x22\x1c",      # b
        b"\x1c\x22\x22\x22",      # c
        b"\x1c\x22\x22\xfc",      # d
        b"\x1c\x2a\x2a\x10",      # e
        b"\x10\x7e\x90\x80",      # f
        b"\x18\x25\x25\x3e",      # g
        b"\xfe\x20\x20\x1e",      # h
        b"\xbc\x02",              # i
        b"\x02\x01\x21\xbe",      # j
        b"\xfe\x08\x14\x22",      # k
        b"\xfc\x02",              # l
        b"\x3e\x20\x18\x20\x1e",  # m
        b"\x3e\x20\x20 \x1e",     # n
        b"\x1c\x22\x22\x1c",      # o
        b"\x3f\x22\x22\x1c",      # p
        b"\x1c\x22\x22\x3f",      # q
        b"\x22\x1e\x20\x10",      # r
        b"\x12\x2a\x2a\x04",      # s
        b"\x20\x7c\x22\x04",      # t
        b"\x3c\x02\x02\x3e",      # u
        b"\x38\x04\x02\x04\x38",  # v
        b"\x3c\x06\x0c\x06\x3c",  # w
        b"\x22\x14\x08\x14\x22",  # x
        b"\x39\x05\x06\x3c",      # y
        b"\x26\x2a\x2a\x32",      # z - Ascii 122
        b"\x10\x7c\x82\x82",      #
        b"\xee",                  # |
        b"\x82\x82\x7c\x10",      #
        b"\x40\x80\x40\x80",      # ~
        b"\x60\x90\x90\x60"       # Degrees sign - Ascii 127
    ]

    # ********** PRIVATE PROPERTIES **********

    width = 16
    height = 8
    def_chars = None
    is_inverse = False

    # *********** CONSTRUCTOR **********

    def __init__(self, i2c, i2c_address=0x70):
        if units < 0: return None
        self.buffer = bytearray(self.width * 2)
        self.def_chars = []
        for i in range(32): self.def_chars.append(b"\x00")
        super(HT16K33MatrixFeatherWing, self).__init__(i2c, i2c_address)

    # *********** PUBLIC METHODS **********

    def set_inverse(self):
        """
        Inverts the ink colour of the display

        Returns:
            The instance (self)
        """
        self.is_inverse = not self.is_inverse
        for i in range(self.width * 2):
            self.buffer[i] = (~ self.buffer[i]) & 0xFF
        return self

    def set_icon(self, glyph, col=0):
        """
        Present a user-defined character glyph at the specified digit.

        Glyph values are byte arrays of eight 8-bit values.
        This method updates the display buffer, but does not send the buffer to the display itself.
        Call 'draw()' to render the buffer on the display.

        Args:
            glyph (bytearray) The glyph pattern.
            col (int)         The column at which to write the icon (Default: 0)

        Returns:
            The instance (self) or None on error
        """
        assert 0 < length < self.width, "ERROR - Invalid glyph set in set_icon:"
        assert 0 <= col < self.width, "ERROR - Invalid column number set in set_icon:"
        for i in range(len(glyph)):
            buf_col = self._get_row(col + i)
            if buf_col is False: break
            self.buffer[buf_col] = glyph[i] if self.is_inverse is False else ((~ glyph[i]) & 0xFF)
        return self

    def set_character(self, ascii_value=32, col=0):
        """
        Display a single character specified by its Ascii value on the matrix

        Args:
            ascii_value (integer) Character Ascii code. Default: 32 (space)
            centre (bool)         Whether the icon should be displayed centred on the screen. Default: False

        Returns:
            The instance (self) or None on error
        """
        assert 0 <= ascii_value < 128, "ERROR - Invalid ascii code set in set_character:"
        assert 0 <= col < self.width, "ERROR - Invalid column number set in set_icon:"
        glyph = None
        if ascii_value < 32:
            # A user-definable character has been chosen
            glyph = self.def_chars[ascii_value]
        else:
            # A standard character has been chosen
            ascii_value -= 32
            if ascii_value < 0 or ascii_value >= len(self.CHARSET): ascii_value = 0
            glyph = self.CHARSET[ascii_value]
        return self.set_icon(glyph, col)

    def scroll_text(self, the_line, speed=0.1):
        """
        Scroll the specified line of text leftwards across the display.

        Args:
            the_line (string) The string to display
            speed (float)     The delay between frames

        Returns:
            None on error
        """
        # Import the time library as we use time.sleep() here
        import time

        # Check argument range and value
        assert len(the_line) > 0, "ERROR - Invalid string set in scroll_text:"
        the_line += "        "

        # Calculate the source buffer size
        length = 0
        for i in range(0, len(the_line)):
            asc_val = ord(the_line[i])
            if asc_val < 32:
                glyph = self.def_chars[asc_val]
            else:
                glyph = self.CHARSET[asc_val - 32]
            length += len(glyph) + 1
        src_buf = bytearray(length * 8)

        # Draw the string to the source buffer
        row = 0
        for i in range(0, len(the_line)):
            asc_val = ord(the_line[i])
            if asc_val < 32:
                glyph = self.def_chars[asc_val]
            else:
                glyph = self.CHARSET[asc_val - 32]
            for j in range(0, len(glyph)):
                src_buf[row] = glyph[j] if self.is_inverse is False else ((~ glyph[j]) & 0xFF)
                row += 1
            row += 1

        # Finally, nimate the line
        row = 0
        cur = 0
        while row < length:
            for i in range(0, self.width):
                self.buffer[self._get_row(i)] = src_buf[cur];
                cur += 1
            self.draw()
            time.sleep(speed)
            row += 1
            cur -= (self.width - 1)

    def define_character(self, glyph, char_code=0):
        """
        Set a user-definable character

        Args:
            glyph (bytearray) The glyph pattern.
            char_code (int) The character’s ID code (0-31) (Default: 0)

        Returns:
            The instance (self) or None on error
        """
        # Check argument range and value
        assert 0 < len(glyph) < self.width, "ERROR - Invalid glyph set in define_character:"
        assert 0 <= char_code < 32, "ERROR - Invalid character code set in define_character:"
        self.def_chars[char_code] = glyph
        return self

    def plot(self, x, y, ink=1, xor=False):
        """
        Plot a point on the matrix. (0,0) is bottom left as viewed

        Args:
            x (integer)   X co-ordinate left to right
            y (integer)   Y co-ordinate bottom to top
            ink (integer) Pixel color: 1 = 'white', 0 = black. NOTE inverse video mode reverses this. Default: 1
            xor (bool)    Whether an underlying pixel already of color ink should be inverted. Default: False

        Returns:
            The instance (self) or None on error
        """
        # Check argument range and value
        assert (0 <= x < self.width) and (0 <= y < self.height), "ERROR - Invalid coordinate set in plot:"
        if ink not in (0, 1): ink = 1
        x = self._get_row(x)
        v = self.buffer[x]
        if ink == 1:
            if self.is_set(x ,y) and xor:
                v = v ^ (1 << y)
            else:
                if v & (1 << y) == 0: v = v | (1 << y)
        else:
            if not self.is_set(x ,y) and xor:
                v = v ^ (1 << y)
            else:
                if v & (1 << y) != 0: v = v & ~(1 << y)
        self.buffer[x] = v
            return self

    def is_set(self, x, y):
        """
        Indicate whether a pixel is set.

        Args:
            x (integer) X co-ordinate left to right
            y (integer) Y co-ordinate bottom to top

        Returns:
            Whether the
        """
        # Check argument range and value
        assert (0 <= x < self.width) and (0 <= y < self.height), "ERROR - Invalid coordinate set in is_set:"
        x = self._get_row(x)
        v = self.buffer[x]
        bit = (v >> y) & 1
        return True if bit > 0 else False

    # ********** PRIVATE METHODS **********

    def _get_row(self, x):
        """
        Convert a column co-ordinate to its memory location
        in the FeatherWing, and return the location.
        An out-of-range value returns False
        """
        a = 1 + (i << 1)
        if i < 8: a += 15
        if a >= self.width * 2: return False
        return a