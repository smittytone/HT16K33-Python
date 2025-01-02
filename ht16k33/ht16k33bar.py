# Import the base class
from .ht16k33 import HT16K33

class HT16K33Bar(HT16K33):
    """
    Micro/Circuit Python class for the Adafruit bar graph
    (https://www.adafruit.com/product/1721)

    Bus:        I2C
    Author:     Tony Smith (@smittytone)
    License:    MIT
    Copyright:  2025
    """

    # *********** CONSTANTS **********

    BAR_I2C_ADDRESS             = 0x70
    BAR_DISPLAY_ADDRESS         = 0
    BAR_COUNT                   = 24
    # Convenience constants for bar colours
    BAR_COLOUR_OFF              = 0
    BAR_COLOUR_CLEAR            = 0
    BAR_COLOUR_RED              = 1
    BAR_COLOUR_YELLOW           = 2
    BAR_COLOUR_AMBER            = 2
    BAR_COLOUR_GREEN            = 3
    # Convenience constants for bar orientation (see docs)
    BAR_ZERO_ALONGSIDE_CHIP     = 0
    BAR_ZERO_FURTHEST_FROM_CHIP = 1

    # *********** CONSTRUCTOR **********

    def __init__(self, i2c, i2c_address=BAR_I2C_ADDRESS, orientation=BAR_ZERO_ALONGSIDE_CHIP):
        self.buffer = bytearray(6)
        self.zero_by_chip = (orientation is self.BAR_ZERO_ALONGSIDE_CHIP)
        super(HT16K33Bar, self).__init__(i2c, i2c_address)

    # *********** PUBLIC METHODS **********

    def set(self, bar, colour):
        """
        Set a specific bar to the specified color.

        NOTE Off is a colour. Colours listed above.

        Args:
            bar (int):    The index of the bar to colour.
            colour (int): The colour of the bar.

        Returns: The instance (self)
        """
        self._check_values(bar, colour)
        if self.zero_by_chip:
            bar = self.BAR_COUNT - 1 - bar
        return self._set_bar(bar, colour)

    def fill(self, bar, colour):
        """
        Fill the graph up to the specific bar with the specified color.

        NOTE Off is a colour. Colours listed above.

        Args:
            bar (int):    The index of the bar to colour.
            colour (int): The colour of the bar.

        Returns: The instance (self)
        """
        self._check_values(bar, colour)
        if self.zero_by_chip:
            bar = self.BAR_COUNT - 1 - bar
            i = 23
            while i >= bar:
                self._set_bar(i, colour)
                i -= 1
        else:
            for i in range(0, bar + 1):
                self._set_bar(i, colour)
        return self

    def clear(self):
        """
        Clear the buffer.

        Returns:
            The instance (self)
        """
        self.buffer = bytearray(6)
        return self

    def draw(self):
        """
        Writes the current display buffer to the display itself.

        Call this method after updating the buffer in order to update
        the LED itself.
        """
        output = bytearray(7)
        output[0] = self.BAR_DISPLAY_ADDRESS
        output[1:] = self.buffer
        self.i2c.writeto(self.address, bytes(output))

    # ********** PRIVATE METHODS **********

    def _check_values(self, bar, colour):
        """
        Assert supplied values are in range.

        Args:
            bar (int):    The index of the bar to colour.
            colour (int): The colour of the bar.
        """
        assert 0 <= bar < self.BAR_COUNT, f"[ERROR] Requested bar out of range 0-{self.BAR_COUNT - 1:d} ({bar:d})"
        assert self.BAR_COLOUR_OFF <= colour <= self.BAR_COLOUR_GREEN, f"[ERROR] Requested bar colour out of range 0-{self.BAR_COLOUR_GREEN:d} ({colour:d})"

    def _set_bar(self, bar, colour):
        """
        Generic function to colour a specific bar on the graph.

        Args:
            bar (int):    The index of the bar to colour.
            colour (int): The colour of the bar.

        Returns: The instance (self).
        """
        red_index = 2 * int(bar / 4 if bar < 12 else (bar - 12) / 4)
        grn_index = red_index + 1

        bit = bar % 4
        if bar >= 12:
            bit += 4
        bit = (1 << bit)

        if colour is self.BAR_COLOUR_RED:
            # Turn red LED on, green off
            self.buffer[red_index] |= bit
            self.buffer[grn_index] &= ~bit
        elif colour is self.BAR_COLOUR_GREEN:
            # Turn green LED on, red off
            self.buffer[grn_index] |= bit
            self.buffer[red_index] &= ~bit
        elif colour is self.BAR_COLOUR_YELLOW:
            # Turn red and green LEDs on
            self.buffer[red_index] |= bit
            self.buffer[grn_index] |= bit
        else:
            # Turn red and green LEDs off
            self.buffer[red_index] &= ~bit
            self.buffer[grn_index] &= ~bit
        return self
