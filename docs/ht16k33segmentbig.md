# HT16K33SegmentBig 3.3.0 #

This is a hardware driver for the [Adafruit 1.2-inch 4-digit, 7-segment LED display](http://www.adafruit.com/products/1270), which is based on the Holtek HT16K33 controller. The driver communicates using I&sup2;C.

It is compatible with [CircuitPython](https://circuitpython.org) and [MicroPython](https://micropython.org).

**Note** This display requires a 5V input in addition to the IO driver voltage (3V3 or 5V). Please check that your MCU board can deliver this.

## Importing the Driver ##

The driver comprises a parent generic HT16K33 driver and a child driver for the 7-segment display itself. All your code needs to do is `import` the latter:

```python
from ht16k33segmentbig import HT16K33SegmentBig
```

You can then instantiate the driver.

You will need both the display driver file and `ht16k33.py` in your project folder.

## Characters ##

The class incorporates its own (limited) character set, accessed through the following codes:

- Digits 0 through 9: codes 0 through 9
- Characters A through F: codes 10 through 15
- Space character: code 16
- Minus character: code 17
- Degree character: code 18

## Display Digits ##

The display’s digits are numbered 0 to 3, from left to right.

## Method Chaining ##

Most methods return a reference to the driver instance (*self*) to allow method chaining with dot syntax:

```python
led.clear().set_number(4, 0).set_number(3, 1).draw()
```

## Class Usage ##

### Constructor: HT16K33SegmentBig(*i2C_bus[, i2c_address]*) ###

To instantiate a HT16K33SegmentBig object pass the I&sup2;C bus to which the display is connected and, optionally, its I&sup2;C address. If no address is passed, the default value, `0x70` will be used. Pass an alternative address if you have changed the display’s address using the solder pads on rear of the LED’s circuit board.

The passed I&sup2;C bus must be configured before the HT16K33SegmentBig object is created.

#### Examples ####

```python
# Micropython
from ht16k33segmentbig import HT16K33SegmentBig
from machine import I2C

# Update the pin values for your board
DEVICE_I2C_SCL_PIN = 5
DEVICE_I2C_SDA_PIN = 4

i2c = I2C(scl=Pin(DEVICE_I2C_SCL_PIN), sda=Pin(DEVICE_I2C_SDA_PIN))
led = HT16K33SegmentBig(i2c)
```

```python
# Circuitpython
from ht16k33segmentbig import HT16K33SegmentBig
import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass
led = HT16K33SegmentBig(i2c)
```

## Class Methods ##

### set_brightness(*[brightness]*) ###

To set the LED’s brightness (its duty cycle), call *set_brightness()* and pass an integer value between 0 (dim) and 15 (maximum brightness). If you don’t pass a value, the method will default to maximum brightness.

#### Example ####

```python
# Turn down the display brightness
led.set_brightness(1)
```

### set_blink_rate(*rate*) ###

This method can be used to flash the display. The value passed into *rate* is the flash rate in Hertz. This value must be one of the following values, fixed by the HT16K33 controller: 0.5Hz, 1Hz or 2Hz. You can also pass in 0 to disable flashing, and this is the default value.

#### Example ####

```python
# Blink the display every second
led.set_blink_rate(1)
```

### set_colon(*[pattern]*) ###

Call *set_colon()* to specify whether the display’s center and left-side colon symbols and upper point (between digits 2 and 3) are illuminated. Pass in an integer bit patten which determines which symbols are lit:

* `0x00` — no colon
* `0x02` — centre colon
* `0x04` — left colon, lower dot
* `0x08` — left colon, upper dot
* `0x10` — decimal point (upper)

This method returns *self*.

#### Example ####

```python
# Set the centre : and the left :
pattern = 0x02 | 0x04 | 0x08
led.set_colon(pattern).draw()
```

### set_glyph(*glyph[, digit]*) ###

To write a character that is not in the character set (see [**Characters**](#characters)) to a single digit, call *set_glyph()* and pass a glyph-definition pattern and the digit number (0, 1, 2 or 3, left to right) as its parameters.

Calculate the glyph pattern value using the following chart. The segment number is the bit that must be set to illuminate it (or unset to keep it unlit):

```
    0
    _
5 |   | 1
  |   |
    - <----- 6
4 |   | 2
  | _ |
    3
```

For example, to define the letter `P`, we need to set segments 0, 1, 4, 5 and 6. In bit form that makes `0x73`, and this is the value passed into *glyph*.

This method returns *self*.

#### Example ####

```python
# Display 'SYNC' on the LED
letters = [0x6D, 0x6E, 0x37, 0x39]
for index in range(0, len(letters)):
    led.set_glyph(letters[index], index)
led.draw()
```

### set_number(*number[, digit]*) ###

To write a number to a single digit, call *set_number()* and pass the digit number (0, 1, 2 or 4, left to right) and the number to be displayed (0 to 9, A to F) as its parameters.

This method returns *self*.

#### Example ####

```python
# Display '42.42' on the LED
led.set_number(4, 0).set_number(2, 1, True)
led.set_number(4, 2).set_number(2, 3).draw()
```

### set_character(*character[, digit]*) ###

To write a character from the display’s hexadecimal character set to a single digit, call *set_character()* and pass the the letter to be displayed (`"0"` to `"9"`, `"A"` to `"F"`, `"-"` or `" "`) and the digit number (0, 1, 2 or 3, left to right) as its parameters. You can pass the string `"deg"` for a degree symbol.

If you need other letters or symbols, these can be generated using [*set_glyph()*](#set_glyphglyph-digit).

This method returns *self*.

#### Example ####

```python
# Display 'bEEF' on the LED
led.set_char("b", 0).set_char("e", 1)
led.set_char("e", 2).set_char("f", 3).draw()
```

### clear() ###

Call *clear()* to wipe the class’ internal display buffer.

*clear()* does not update the display, only the buffer. Call [*draw()*](#draw) to refresh the LED.

This method returns *self*.

#### Example ####

```python
# Clear the display
led.clear().draw()
```

### draw() ###

Call *draw()* after changing any or all of the internal display buffer contents in order to reflect those changes on the display itself.
