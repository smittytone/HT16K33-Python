# HT16K33MatrixFeatherWing 3.0.0 #

This is a hardware driver for the [Adafruit 0.8-inch 8x16 LED Matrix FeatherWing](https://www.adafruit.com/product/3149), which is based on the Holtek HT16K33 controller. The driver communicates using I&sup2;C.

It is compatible with [CircuitPython](https://circuitpython.org) and [MicroPython](https://dmicropython.org).

## Importing the Driver ##

The driver comprises a parent generic HT16K33 driver and a child driver for the matrix display itself. All your code needs to do is `import` the latter:

```python
from ht16k33matrixfeatherwing import HT16K33MatrixFeatherWing
```

You can then instantiate the driver.

You will need both the display driver file and `ht16k33.py` in your project folder.

## Characters ##

The class incorporates a full, proportionally spaced Ascii character set. Additionally, you can use Ascii values 0 through 31 for user-definable characters.

## Method Chaining ##

Most methods return a reference to the driver instance (*self*) to allow method chaining with dot syntax:

```python
led.clear().clear().plot(0,1,0).draw()
```

## Class Usage ##

### Constructor: HT16K33MatrixFeatherWing(*i2C_bus[, i2c_address]*) ###

To instantiate a HT16K33MatrixFeatherWing object pass the I&sup2;C bus to which the display is connected and, optionally, its I&sup2;C address. If no address is passed, the default value, `0x70` will be used. Pass an alternative address if you have changed the display’s address using the solder pads on rear of the LED’s circuit board.

The passed I&sup2;C bus must be configured before the HT16K33MatrixFeatherWing object is created.

#### Examples ####

```python
# Micropython
from ht16k33matrixfeatherwing import HT16K33MatrixFeatherWing
from machine import I2C

# Update the pin values for your board
DEVICE_I2C_SCL_PIN = 5
DEVICE_I2C_SDA_PIN = 4

i2c = I2C(scl=Pin(DEVICE_I2C_SCL_PIN), sda=Pin(DEVICE_I2C_SDA_PIN))
led = HT16K33Segment(i2c)
```

```python
# Circuitpython
from ht16k33matrixfeatherwing import HT16K33MatrixFeatherWing
import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass
led = HT16K33Segment(i2c)
```

## Class Methods ##

### set_brightness(*[brightness]*) ###

To set the LED’s brightness (its duty cycle), call *setBrightness()* and pass an integer value between 0 (dim) and 15 (maximum brightness). If you don’t pass a value, the method will default to maximum brightness.

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

### set_icon(*glyph[, col]*) ###

To write a character that is not in the character set at a specified x co-ordinate, call *set_icon()* and pass a glyph-definition pattern and the column of the matrix at which it will be written as its parameters.

The glyph pattern should be a byte array; each byte is a column of image pixels with bit zero at the bottom.

This method returns *self*.

#### Example ####

```python
# Display a smiley in the centre of the display
icon = b"\x3C\x42\xA9\x85\x85\xA9\x42\x3C"
led.set_icon(icon, 4).draw()
```

### set_character(*character[, col]*) ###

To write a character from the display’s character set at a specified x co-ordinate, call *set_character()* and pass the Ascii code of the character to be displayed. You can also specify the column of the matrix at which it will be written.

If you have set any user-definable characters, you can write these by passing their ID value (between 0 and 31) in place of an Ascii code.

If you need other letters or symbols, these can be generated using *set_icon()*.

This method returns *self*.

#### Example ####

```python
# Display 'Boo' on the LED
led.set_character("B", 0).set_char("o", 7)
led.set_character("o", 12).draw()
```

### define_character(*glyph[], ascii_value]*) ###

To record a user-definable character, write its pixel pattern (see [set_icon()](#set_iconglyph-col)) and specify the ID you will use to write the character to the display buffer (using [set_character()](#set_charactercharacter-col)).

This method returns *self*.

#### Example ####

```python
# Define two halves of a space invader
icon = b"\x00\x00\x0E\x18\xBE\x6D\x3D\x3C"
led.define_character(icon, 0)
icon = b"\x3C\x3D\x6D\xBE\x18\x0E\x00\x00"
led.define_character(icon, 1)
```

### scroll_text(*the_line[, speed]*) ###

Call *scroll-text()* to write a line of text to the display and see it scroll right to left until all of the string’s characters have been shown. The method pads the text with spaces so that the text completely clears the screen at the end of the animation.

You can include user-defined graphics in your string by embedding escaped hex characters for the graphics’ ID codes, as the example below shows.

The optional parameter *speed* takes a period in seconds: the pause between animation frames. The smaller the value, the quicker the scroll. Default: 0.1s.

#### Example ####

```python
text = "Eeeek! The Space Invaders are coming... \x00\x01"
led.scroll_text(text)
```

### plot(*x, y[, ink][, xor]*) ###

To set a single pixel on the matrix, call this method and pass in the pixel’s co-ordinates. The *ink* parameter defaults to 1, to set the pixel; specify 0 to unset the pixel. The *xor* parameter is also optional: pass in `True` to cause the target pixel to flip if it already in the specified ink colour.

#### Example ####

```python
# Draw a border at the edge of the matrix
for x in range(16):
    led.plot(x, 0).plot(x, 7)
for y in range(1,7):
    led.plot(0, y).plot(15, y)
led.draw()
```

### is_set(*x, y*) ###

This method returns `True` if the specified pixel is set, otherwise `False`.

### clear() ###

Call *clear()* to wipe the class’ internal display buffer.

*clear()* does not update the display, only the buffer. Call *draw()* to refresh the LED.

This method returns *self*.

#### Example ####

```python
# Clear the display
led.clear().draw()
```

### draw() ###

Call *draw()* after changing any or all of the internal display buffer contents in order to reflect those changes on the display itself.

## Release Notes ##

- 3.0.0 *Unreleased*
    - Initial release.

## License ##

The HT16K33MatrixFeatherWing library is licensed under the [MIT License](./LICENSE).
