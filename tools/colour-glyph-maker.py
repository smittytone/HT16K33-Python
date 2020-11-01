#!/usr/local/bin/python3

"""
Take a glyph input line-by-line as colour values (r, g, y)
and convert to the HT16K33MatrixColour library's internal
format (two bits per pixel)
"""
lines = []
print("  Bits: 01234567")
for i in range(8):
    lines.append(input("Line " + str(i) + ": "))

output = bytearray()
l = 0
for i in range(8):
    for j in range(0,2):
        row = 4 * j
        byte_value = 0
        for k in range(0,4):
            line = lines[7 - row].lower()
            if len(line) < 8: line = "........"
            colour_value = line[l]
            if colour_value == "r": byte_value |= (0x02 << (k * 2))
            if colour_value == "g": byte_value |= (0x01 << (k * 2))
            if colour_value == "y": byte_value |= (0x03 << (k * 2))
            row += 1
            #print(l, j, k, k * 2, colour_value, byte_value)
        output.append(byte_value)
    l += 1

# Output the glyph bytearray as a string, ie.
# b"\x00\x00"
# ready to be copied and pasted into your code
s = "b\""
for i in range(len(output)):
    s += "\\x{:02X}".format(output[i])
print(s + "\"")