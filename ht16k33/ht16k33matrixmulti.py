# Import the base class
from ht16k33 import HT16K33Matrix

class HT16K33MatrixMulti:

    matrix_width = 8
    matrix_height = 8
    window_width = 0
    window_height = 8
    
    def __init__(self, i2c, count, addresses=[]):
        assert 0 < count < 9, "ERROR - Invalid matrix count [1-4]"
        assert count != 1, "ERROR - For a single LED use the HT16K33Matrix class"
        assert len(addresses) == 0 or len(addresses) == count, "ERROR - Invalid matrix I2C address count [1-4]"
        
        # Instantiate the required matrix objects, setting their
        # I2C addresses automatically or to those supplied
        self.matrices = []
        baseAddress = 0x70
        for i in range(0, count):
            address = addresses[i] if len(addresses) == count else baseAddress
            self.matrices.append(HT16K33Matrix(i2c, address))
            baseAddress += 1
        self.window_width = self.matrix_width * count

    def set_brightness(self, brightness=15):
        """
        Set the display's brightness (ie. duty cycle).

        Brightness values range from 0 (dim, but not off) to 15 (max. brightness).

        Args:
            brightness (int): The chosen flash rate. Default: 15 (100%).
        """
        if brightness < 0 or brightness > 15: brightness = 15
        for i in range(0, len(self.matrices)):
            self.matrices[i].set_brightness(brightness)

    def clear(self):
        """
        Clear all the matrices.
        """
        for i in range(0, len(self.matrices)):
            self.matrices[i].clear()
        return self

    def draw(self):
        """
        Draw all the matrices.
        """
        for i in range(0, len(self.matrices)):
            self.matrices[i].draw()

    def plot(self, x, y, ink=1, xor=False):
        """
        Plot a point on the display. (0,0) is bottom left as viewed.

        Args:
            x (integer)   X co-ordinate,left to right
            y (integer)   Y co-ordinate, bottom to top
            ink (integer) Pixel color: 1 = 'white', 0 = black. Default: 1
            xor (bool)    Whether an underlying pixel already of color ink should be inverted. Default: False

        Returns:
            The instance (self)
        """
        # Bail on incorrect values
        assert (0 <= x < self.window_width) and (0 <= y < self.window_height), "ERROR - Invalid coordinate set in plot()"

        matrix, mx = self._localise(x)
        matrix.plot(mx, y, ink, xor)
        return self

    def set_icon(self, glyph, column):
        """
        Displays a custom character on the display.

        Args:
            glyph (array) 1-8 8-bit values defining a pixel image. The data is passed as columns
                          0 through 7, left to right. Bit 0 is at the bottom, bit 7 at the top
            column (int)  The column (x co-ordinate) at which to place the glyph

        Returns:
            The instance (self)
        """
        # Bail on incorrect values
        length = len(glyph)
        assert 0 < length <= self.window_width, "ERROR - Invalid glyph set in set_icon()"

        local_column_offset = 0
        display_column = column
        matrix, x = self._localise(display_column)
        for i in range(length):
            local_column = x + local_column_offset
            if local_column > 7:
                # Gone beyond the current matrix, so get the next one
                display_column += local_column_offset
                matrix, x = self._localise(display_column)
                # Break if we've reached the end of the display
                if x == -1: break
                local_column = x
                local_column_offset = 0
            matrix.buffer[local_column] = glyph[i]
            local_column_offset += 1
        return self
    
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
        #assert length >= self.window_width, "ERROR - Invalid image length in scroll_image()"
        assert length > 0, "ERROR - Invalid image length in scroll_image()"

        # Repeat too-small images to the full width (or beyond) of the display
        if length < self.window_width:
            count = int(self.window_width / length)
            if self.window_width % length != 0:
                count += 1
            nu_image = bytearray(count * length)
            for i in range(0, count):
                nu_image[i * length:i * length + length] = the_image
            the_image = nu_image
            length = len(the_image)

        # Animate the image
        cursor = 0
        while True:
            # Iterate over the matrices, setting each one as a window into the image
            for i in range(0, len(self.matrices)):
                window = cursor + (i * self.matrix_width)
                if do_loop:
                    g = bytearray(8)
                    if window > length:
                        # Window doesn't span the image boundary but is beyond it
                        g = the_image[window - length:window - length + 8]
                    elif window + self.matrix_width > length:
                        # Window spans image boundary
                        g[:length - window] = the_image[window:]
                        g[length - window:] = the_image[:self.matrix_width - (length - window)]
                    else:
                        # Window doesn't span the image boundary and is not beyond it
                        g = the_image[window:window + self.matrix_width]
                    self.matrices[i].set_icon(g).draw()
                else:
                    self.matrices[i].set_icon(the_image[window:window + self.matrix_width]).draw()
            # Advance the image cursor and check we've reached its end
            cursor += 1
            if do_loop:
                if cursor >= length:
                    cursor = 0
            else:
                if cursor > length - self.window_width: 
                    break
            time.sleep(speed)

    def _localise(self, x):
        """
        Return the local co-ordinates and matrix for global co-ordinates.
        Return -1 if we are beyond the 
        """
        if x >= self.window_width: return self.matrices[0], -1
        index = int(x / self.matrix_width)
        local_x = x - (index * self.matrix_width)
        if index >= len(self.matrices): return self.matrices[0], -1
        return self.matrices[index], local_x
