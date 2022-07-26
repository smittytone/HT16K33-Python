# HT16K33Segment14 3.2.0 #

This is a hardware driver for the [SparkFun Qwiic Alphanumeric Display](https://www.sparkfun.com/products/16916)., which is based on the Freenove VK16K33, a clone of the Holtek HT16K33 controller. The driver communicates using I&sup2;C.

It also supports the HT16K33-based [Adafruit 0.54in Alphanumeric Display](https://www.adafruit.com/product/1911) (version 3.2.0 and up).

It is compatible with [CircuitPython](https://circuitpython.org) and [MicroPython](https://micropython.org).

## Importing the Driver ##

The driver comprises a parent generic HT16K33 driver and a child driver for the 14-segment display itself. All your code needs to do is `import` the latter:

```python
from HT16K33segment14 import HT16K33Segment14
```

You can then instantiate the driver — see [Class Usage](#class-usage), below.

You will need both the display driver file and `ht16k33.py` in your project folder.

## Characters ##

The class incorporates its own (limited) character set, accessed through the following codes:

- Digits 0 through 9: codes 0 through 9
- Characters A through Z: codes 10 through 35
- Characters a through z: codes 36 through 61
- Space character: code 62
- Symbol characters: codes 63 through 75 `| " ? $ % ° ' \ , * + - /`

## Display Digits ##

The display’s digits are numbered 0 to 3, from left to right.

## Method Chaining ##

Most methods return a reference to the driver instance (*self*) to allow method chaining with dot syntax:

```python
led.clear().set_number(4, 0).set_number(3, 1).draw()
```

## Class Usage ##

### Constructor: HT16K33Segment14(*i2C_bus[, i2c_address][, is_ht16k33]*) ###

To instantiate a HT16K33Segment14 object pass the I&sup2;C bus to which the display is connected and, optionally, its I&sup2;C address. If no address is passed, the default value, `0x70` will be used. Pass an alternative address if you have changed the display’s address using the solder pads on rear of the LED’s circuit board.

A second optional parameter, *is_ht16k33*, allows you to specify the Adafruit 0.54in Alphanumeric Display: pass `True` to use this display. The default value is `False`, which implies you are using a VK16K33-based display.

The passed I&sup2;C bus must be configured before the HT16K33Segment object is created.

#### Examples ####

```python
# Micropython
from HT16K33segment14 import HT16K33Segment14
from machine import I2C

# Update the pin values for your board
DEVICE_I2C_SCL_PIN = 5
DEVICE_I2C_SDA_PIN = 4

i2c = I2C(scl=Pin(DEVICE_I2C_SCL_PIN), sda=Pin(DEVICE_I2C_SDA_PIN))
led = HT16K33Segment14(i2c)
```

```python
# Circuitpython - VK16K33 device
from HT16K33segment14 import HT16K33Segment14
import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass
led = HT16K33Segment14(i2c)
```

```python
# Circuitpython - HT16K33 device
from HT16K33segment14 import HT16K33Segment14
import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass
led = HT16K33Segment14(i2c, is_ht16k33=True)
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

### set_colon(*[is_set]*) ###

Call *set_colon()* to specify whether the display’s center colon symbol is illuminated (`True`) or not (`False`). The call defaults to `True`.

This method returns *self*.

#### Example ####

```python
# Set the display to --:--
led.set_char("-", 0).set_char("-", 1).set_char("-", 2).set_char("-", 3)
led.set_colon().draw()
```

### set_glyph(*glyph[, digit]*) ###

To write a character that is not in the character set (see [**Characters**](#characters)) to a single digit, call *set_glyph()* and pass a glyph-definition pattern and the digit number (0, 1, 2 or 3, left to right) as its parameters.

Calculate the glyph pattern value using the following chart. The segment number is the bit that must be set to illuminate it (or unset to keep it unlit):

```
    0			    9
    _
5 |   | 1		8 \ | / 10
  |   |			   \|/
                6  - -  7
4 |   | 2		   /|\
  | _ |		   13 / | \ 11		. 14
    3			    12

Bit 14 is the period, but this is set with parameter 3
Nb. Bit 15 is not read by the display
```

For example, to define the letter `P`, we need to set segments 0, 1, 4, 5 and 6. In bit form that makes `0x73`, and this is the value passed into *glyph*.

**Important** This is the encoding for the VK16K33. For the HT16K33, bits 11 and 13 are swapped. For pre-defined characters, the driver swaps these bits this for you.

This method returns *self*.

### set_number(*number[, digit]*) ###

To write a number to a single digit, call *set_number()* and pass the digit number (0, 1, 2 or 4, left to right) and the number to be displayed (0 to 9, A to F) as its parameters.

This method returns *self*.

#### Example ####

```python
# Display '42 42' on the LED
led.set_number(4, 0).set_number(2, 1)
led.set_number(4, 2).set_number(2, 3).draw()
```

### set_character(*character[, digit]*) ###

To write a character from the display’s hexadecimal character set to a single digit, call *set_character()* and pass the the letter to be displayed (`"0"` to `"9"`, `"A"` to `"Z"`, `"`a`"` to `"z"`) and the digit number (0, 1, 2 or 3, left to right) as its parameters. You can pass the string `"deg"` for a degree symbol.

If you need other letters or symbols, these can be generated using [*set_glyph()*](#set_glyphglyph-digit-has_dot).

This method returns *self*.

#### Example ####

```python
# Display 'bEEF' on the LED
led.set_character("b", 0).set_character("e", 1)
led.set_character("e", 2).set_character("f", 3).draw()
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
