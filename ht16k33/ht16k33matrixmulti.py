# Import the base class
from ht16k33 import HT16K33Matrix

class HT16K33MatrixMulti:

    width = 8
    buffer_width = 0
    brightness = 15
    
    def __init__(self, i2c, count):
        assert 0 < count < 5, "ERROR - Invalid matrix count [1-4]"
        self.matrix_count = count
        self.matrices = []
        baseAddress = 0x70
        for i in range(0, count):
            self.matrices.append(HT16K33Matrix(i2c, baseAddress))
            baseAddress += 1
        self.buffer_width = self.width * count

    def set_brightness(self, brightness=15):
        """
        Set the display's brightness (ie. duty cycle).

        Brightness values range from 0 (dim, but not off) to 15 (max. brightness).

        Args:
            brightness (int): The chosen flash rate. Default: 15 (100%).
        """
        if brightness < 0 or brightness > 15: brightness = 15
        self.brightness = brightness
        for i in range(0, len(self.matrices)):
            self.matrices[i].set_brightness(brightness)

    def clear(self):
        """
        Set the display's brightness (ie. duty cycle).

        Brightness values range from 0 (dim, but not off) to 15 (max. brightness).

        Args:
            brightness (int): The chosen flash rate. Default: 15 (100%).
        """
        for i in range(0, len(self.matrices)):
            self.matrices[i].clear().draw()

    def scroll_text(self, the_line, speed=0.1, do_loop=False):
        """
        Scroll the specified line of text leftwards across the display.

        Args:
            the_line (string) The string to display
            speed (float)     The delay between frames
            do_loop (bool)    Should the scroll loop to the start
        Returns:
            The instance (self)
        """
        # Just in case it hasn't yet been imported
        import time

        # Bail on incorrect values
        assert len(the_line) > 0, "ERROR - Invalid string set in scroll_text()"

        # Calculate the source buffer size
        length = 0
        for i in range(0, len(the_line)):
            asc_val = ord(the_line[i])
            assert 31 < asc_val < 128, "ERROR - Character out of range"
            glyph = self.matrices[0].CHARSET[asc_val - 32]
            length += len(glyph)
            if asc_val > 32: length += 1

        # Draw the string to the source buffer
        src_buffer = bytearray(length)
        row = 0
        for i in range(0, len(the_line)):
            asc_val = ord(the_line[i])
            glyph = self.matrices[0].CHARSET[asc_val - 32]
            for j in range(0, len(glyph)):
                src_buffer[row] = glyph[j]
                row += 1
            if asc_val > 32: row += 1
        assert row == length, "ERROR - Mismatched lengths in scroll_text()"

        # Finally, animate the line
        self.scroll_image(src_buffer, speed, do_loop)

    def scroll_image(self, the_image, speed=0.1, do_loop=False):
        """
        Scroll the specified image leftwards across the display.
        Here 'image' means an array of arbitrary row values together
        comprising a graphic to scroll across the multi-matrix display.

        Args:
            the_image (byte array) The image data to display
            speed (float)          The delay between frames
            do_loop (bool)         Should the scroll loop to the start

        Returns:
            The instance (self)
        """
        # Just in case it hasn't yet been imported
        import time

        # Bail on incorrect values
        length = len(the_image)
        assert length > 0, "ERROR - Invalid image length in scroll_image()"

        # Finally, animate the image
        cursor = 0
        window_width = self.width * len(self.matrices)
        while True:
            # Iterate over the matrices, setting each one as a window into the image
            for i in range(0, len(self.matrices)):
                window = cursor + (i * self.width)
                if do_loop:
                    g = bytearray(8)
                    if window > length:
                        # Window doesn't span the image boundary but is beyond it
                        g = the_image[window - length:window - length + 8]
                    elif window + self.width > length:
                        # Window spans image boundary
                        g[:length - window] = the_image[window:]
                        g[length - window:] = the_image[:self.width - (length - window)]
                    else:
                        # Window doesn't span the image boundary and is not beyond it
                        g = the_image[window:window + self.width]
                    self.matrices[i].set_icon(g).draw()
                else:
                    self.matrices[i].set_icon(the_image[window:window + self.width]).draw()
            # Advance the image cursor and check we've reached its end
            cursor += 1
            if do_loop:
                if cursor >= length:
                    cursor = 0
            else:
                if cursor > length - window_width: 
                    break
            time.sleep(speed)
