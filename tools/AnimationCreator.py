#!/usr/local/bin/python3

"""
Read an excel animation file and convert it to an hex pic for the LED matrix 


Take a glyph input line-by-line as colour values (r, g, y)
and convert to the HT16K33MatrixColour library's buffer
format: two bytes per pixel column
"""

import math
import pandas as pd



def CreateSmileyBitsHex(_icon):
    """
    Create the smiley hey code my list of color
    """
    spaces = ".........."
    output = bytearray()
    for column in range(8):
        byte_left = 0
        byte_right = 0
        row = 7
        for bit in range(8):
            line = _icon[row].lower()
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
    _hexStr = "b\""
    for i in range(len(output)):
        _hexStr += "\\x{:02X}".format(output[i])
    print("_icon = " + _hexStr + "\"")
    print("self.__drawIcon(_icon)")
    print("time.sleep(_sleepTime)")



# Read the animation file
df = pd.read_excel("./Animation.xlsx", sheet_name="RolingFace")

#create the needed objects
smiley = []


#go threw every line in the excel file
for index, row in df.iterrows():
    
    #Read the complete line
    _line = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
    _lineStr = ""

    #Replace the non string values and create a single string
    for i, _value in enumerate(_line):

        #Replace the nan entries 
        if not isinstance(_value, str):
            _line[i] = "-"

        _lineStr = _lineStr + _line[i]
        
    #Add the Line to the Smiley
    smiley.append(_lineStr)    

    if (len(smiley) > 7):
        CreateSmileyBitsHex(smiley)
        smiley = []

