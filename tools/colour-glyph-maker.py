#!/usr/local/bin/python3

"""
Take a glyph input line-by-line as colour values (r, g, y)
and convert to the HT16K33MatrixColour library's buffer
format: two bytes per pixel column
"""
lines = []
print("  Bits: 01234567")
for i in range(8):
    lines.append(input("Line " + str(i) + ": "))

spaces = ".........."
output = bytearray()
for column in range(8):
    byte_left = 0
    byte_right = 0
    row = 7
    for bit in range(8):
        line = lines[row].lower()
        length = len(line)
        if length < 8: line += spaces[:8 - len(line)]
        colour_value = line[column]
        if colour_value == "r":
            byte_right |= (1 << bit)
        if colour_value == "g":
            byte_left |= (1 << bit)
        if colour_value == "y":
            byte_left |= (1 << bit)
            byte_right |= (1 << bit)
        row -= 1
        #print(l, j, k, k * 2, colour_value, byte_value)
    output.append(byte_left)
    output.append(byte_right)

# Output the glyph bytearray as a string, ie.
# b"\x00\x00"
# ready to be copied and pasted into your code
s = "b\""
for i in range(len(output)):
    s += "\\x{:02X}".format(output[i])
print(s + "\"")