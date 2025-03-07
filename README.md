# HT16K33 Drivers 4.2.0 #

This repo provides Python drivers for the Holtek HT16K33 controller chip and various display devices based upon it, such as the [Adafruit 0.8-inch 8x16 LED Matrix FeatherWing](https://www.adafruit.com/product/3149) and the [SparkFun Qwiic Alphanumeric Display](https://www.sparkfun.com/products/16916).

The drivers support both [CircuitPython](https://circuitpython.org) and [MicroPython](https://micropython.org) applications. They communicate using I&sup2;C.

The library also supports generic seven-segment displays wired up to an HT16K33, which can drive up to eight these LEDs. The HT16K33 may be on a board of your own design, or on a third-party one, such as the [Adafruit 16x8 LED Matrix Driver Backpack ](https://www.adafruit.com/product/1427). LED units you can connect range from [single digits](https://www.sparkfun.com/products/8546) up to combinations of [multi-digit units](https://www.sparkfun.com/products/11409).

Connect your HT16K33 column pins to each LED's digit selection pin, and its row pins to the LED's segment selection pins.

## Major Changes ##

### 4.2.0 ###

A new component has been added: `ht16k33matrixmulti.py`. This provides horizontal message scrolling across two or more matrix LEDs. Up to eight matrix LEDs can be connected, based on the range of unique I&sup2;C addresses that the HT16K33 provides. The message can be a text string or a byte array containing an 'image' comprising column-by-column bit data of the kind you might present on a single matrix LED using the `HT16K33Matrix.set_icon()` function.

For example, with MicroPython:

```python
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33MatrixMulti

i2c = I2C(0, scl=Pin(9), sda=Pin(8))
display = HT16K33MatrixMulti(i2c)
display.set_brightness(2)
display.clear()

image = [0x01,0x03,0x07,0x0F,0x1D,0x3F,0x7F,0xEB,0xFF,0x77,0x3E,0x1F,0x0D,0x07,0x03,0x01,0x01,0x03,0x07,0x0D,0x0F,0x07,0x03,0x01,0x01,0x03,0x07,0x0F,0x1D,0x3F,0x7F,0xEB,0xFF,0x77,0x3E,0x1F,0x0D,0x07,0x03,0x01,0x01,0x03,0x07,0x0D,0x0F,0x07,0x03,0x01,0xC1,0xC3,0x07,0x0F,0x0F,0x07,0x03,0x01]
image_bytes = bytes(image)
display.scroll_image(image_bytes)
```

or for text:

```python
display.scroll_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
```

The constructor takes a pre-configured I&sup2;C instance (via CircuitPython or MicroPython) and the number of matrix LEDs in your custom display panel. By default, these are assumed to be oriented left to right, with the left-most matrix using the address `0x70` and each subsequent matrix using the next sequential address. Alternatively, you can pass in an array of addresses in the sequence in which they are mounted left to right. For example, my test rig has displays with the addresses `0x70`, `0x71`, `0x74` and, `0x72`.

The key functions, `scroll_text()` and `scroll_image()` take a string and a byte array, respectively (see the examples above). Both have two optional parameters. First, a speed value: a float that provides the pause duration in seconds between each animation frame (the default is 0.1 seconds). Second, a boolean that determines whether the image or text auto-repeats once it has completely scrolled across the face of the display (default: `False`). `True` should be used carefully as it will cause the code to block infinitely.

The new driver also includes the functions `set_text()` and `set_image()`, which take, respectively, a text string and a byte array, and a column on the display at which to draw them. `set_character()` works the same way, but takes an Ascii value rather than a string or a byte array. `define_character()` allows you to store user-defined characters in Ascii values 0 through 31.

And `plot()` sets or unsets a pixel on the display: pass the pixel's x and y co-ordinates ((0,0) is at the bottom left) and the ink colour (1 to set, 0 to clear). Optionally, pass `True` to reverse the target pixel if it is already set.

Finally, `clear()` and `set_brightness()` functions are provided which affect all the matrix LEDs in the display.

## Display Drivers ##

| Driver<br />(Click for docs) | Example&nbsp;Product |
| :-- | :-- |
| [Small 4-digit, 7-segment LED](https://smittytone.net/docs/ht16k33_segment.html) | [Adafruit 0.56-inch 4-digit, 7-segment LED display](https://www.adafruit.com/products/878) |
| [Large 4-digit, 7-segment LED](https://smittytone.net/docs/ht16k33_segmentbig.html) | [Adafruit 1.2-inch 4-digit, 7-segment LED display](https://www.adafruit.com/product/1270) |
| [Small 4-digit, 14-segment LED](https://smittytone.net/docs/ht16k33_segment14.html) | [SparkFun Qwiic Alphanumeric Display](https://www.sparkfun.com/products/16916),<br />[Adafruit 0.54in Alphanumeric Display](https://www.adafruit.com/product/1911),<br />[EC Buying 0.54-inch HT16K33 Digital Tube Module](https://www.amazon.com/EC-Buying-Digital-Display-Segment/dp/B0C1C6LKDB) |
| [8x8 monochrome matrix LED](https://smittytone.net/docs/ht16k33_matrix.html) | [Adafruit Mini 0.8-inch 8x8 LED Matrix](https://www.adafruit.com/product/872) |
| [Multiple 8x8 monochrome matrix LEDs](https://smittytone.net/docs/ht16k33_matrix_multi.html) | [Adafruit Mini 0.8-inch 8x8 LED Matrix](https://www.adafruit.com/product/872) |
| [8x8 bi-colour matrix LED](https://smittytone.net/docs/ht16k33_matrixcolour.html) | [Adafruit 1.2-inch 8x8 bi-color LED matrix backpack](https://www.adafruit.com/product/902) |
| [16x8 FeatherWing matrix LED](https://smittytone.net/docs/ht16k33_matrixfeatherwing.html) | [Adafruit 0.8-inch 8x16 LED Matrix FeatherWing](https://www.adafruit.com/product/3149) |
| [Standalone HT16K33](https://smittytone.net/docs/ht16k33_segmentgen.html) | [Adafruit 16x8 LED Matrix Driver Backpack ](https://www.adafruit.com/product/1427) |
| [Bar graph LED](https://smittytone.net/docs/ht16k33_bar.html) | [Adafruit Bi-Color 24-Bar Bargraph w/I2C Backpack](https://www.adafruit.com/product/1721) |

Further drivers may be added in due course.

## Import the Drivers ##

The driver package comprises a parent generic HT16K33 class and child classes for various displays themselves. All your code needs to do is `import` the latter. For example:

```python
from ht16k33 import HT16K33Segment
```

You can then instantiate the driver object. This requires a **configured** I2C bus object.

You will need at least one display driver file, eg. `ht16k33segmentgen.py` and `ht16k33.py` in your project folder.

## Install the Drivers ##

### MicroPython Manual Install ###

Use the [`pyboard`](https://github.com/micropython/micropython/blob/master/tools/pyboard.py) or [`mpremote`](https://github.com/micropython/micropython/tree/master/tools/mpremote) command line tools to copy the `ht16k33` directory to your board's `lib` directory.

### MicroPython MIP Install ###

You can install the drivers using [MicroPython's MIP system](https://docs.micropython.org/en/v1.21.0/reference/packages.html). This requires a board running MicroPython 1.20 or above and connected to the Internet. Add the following to your code:

```python
import mip
mip.install('github:smittytone/HT16K33-Python')
```

If your board is not Internet-capable, you can install locally using [the `mpremote` tool](https://docs.micropython.org/en/latest/reference/mpremote.html):

```python
mpremote mip install github:smittytone/HT16K33-Python
```

#### Install Script ####

Alternatively, use our convenient installer script:

```shell
./tools/mpinstall.sh
```

To install pre-compiled versions of the library files, run:

```shell
./tools/mpinstall.sh mpy
```

This requires MicroPython's `mpy-cross` tool installed on your computer.

### CircuitPython Manual Install ###

Copy `ht16k33` directory to the mounted board's `lib` folder.

## Reducing Memory Usage ##

Adding the driver code may prove too much for certain CircuitPython devices which have limited amounts of memory. To overcome this, [use MicroPython’s `mpy-cross` compiler](https://github.com/micropython/micropython/tree/master/mpy-cross). This will compile the raw Python into a highly compact form as a `.mpy` file. Copy `ht16k33.mpy` and the device-specific `.mpy` file to your device in place of the `.py` versions.

For MicroPython boards, I recommend you use the [`mpinstall.sh` script](#install-script) to compile and install `.mpy` versions if the library files all in one go.

## Documentation

You can find documentation for all of the drivers [at smittytone.net](https://smittytone.net/docs/ht16k33.html).

## Python Package Index

This code is now available [via the Python Package Index](https://pypi.org/project/ht16k33-python/) for folks using Thonny and other code-pulling IDEs.

## Release Notes

- 4.2.0 *Unreleased*
    - Add multi-matrix scrolling enabler class.
    - Code clean.
- 4.1.0 *2 January 2025*
    - Add `HT16K33Bar.py` bar graph driver.
    - Add alternative, all-capitals character set for `ht16k33Segment.py`.
    - Support EC Buying 0.54in 4-digit, 14-segment display in `ht16k33Segment14.py`.
    - Support new board selection mode in `ht16k33Segment14.py`.
    - Fix decimal point clearing `ht16k33Segment14.py`.
- 4.0.3 *18 December 2024*
    - Fix typo breaking `mpremote` usage  — thanks, `@sebromero`.
- 4.0.2 *16 December 2024*
    - Fixed a character set indexing bug in `ht16k33Segmentbig.py` — thanks, `@jonhp`.
- 4.0.1 *16 August 2024*
    - Minor fixes/improvements.
    - Add **experimental** `rotate()` method to `ht16k33Segmentbig.py`.
- 4.0.0 *8 May 2024*
    - Completely reorganise the library files into their own directory.
    - Add device installation script for MicroPython users - thanks, `@ubidefeo`.
    - Add `HT16K33SegmentGen` CircuitPython examples.
    - Use Raspberry Pi Pico for all examples.
- 3.5.3 *15 January 2024*
    - Remove the `.mpy` versions and provide instructions instead.
    - Fix incorrect selection of blink rate 0.5Hz — thanks, [`@Karrp`](https://github.com/Karrp).
- 3.5.2 *11 December 2023*
    - Add `mip` support — thanks, [`@ubidefeo`](https://github.com/ubidefeo) (no code changes).
- 3.5.1 *30 October 2023*
    - Add provisional [PyPI](https://pypi.org/) support (no code changes).
- 3.5.0 *2 September 2023*
    - Add `HT16K33SegmentGen` a generic, 1-8 digit 7-segment driver — thanks, [`@vader7071`](https://github.com/vader7071).
- 3.4.2 *14 February 2023*
    - Fix an error when a space is shown as a zero — thanks, [`@asasine`](https://github.com/asasine).
- 3.4.1 *14 November 2022*
    - Correct VK16K33 naming.
    - Fix VK16K33 colon setting and unsetting — thanks, Dietmar Schüller.
- 3.4.0 *6 October 2022*
    - Allow the colon and decimal point on [SparkFun Qwiic Alphanumeric Display](https://www.sparkfun.com/products/16916)).
- 3.3.1 *13 September 2022*
    - 14-segment character-set numerals now match 7-segment equivalents.
    - Assorted code tweaks.
    - Wrangle and extend examples.
    - Remove old docs.
    - Big thanks to [`@akbiocca`](https://github.com/akbiocca) for assistance with this release.
- 3.3.0 *5 August 2022*
    - Add `rotate()` method to HT16K33Segment.
- 3.2.0 *26 July 2022*
    - Support the [Adafruit 0.54in Alphanumeric Display](https://www.adafruit.com/product/1911) via `ht16k33segment14.py`.
    - Bug fixes.
- 3.1.0 *16 February 2022*
    - Add `ht16k33segment14.py` to support the [SparkFun Qwiic Alphanumeric Display](https://www.sparkfun.com/products/16916).
- 3.0.2 *23 November 2020*
    - Refactor out some `ht16k33matrix.py` code.
- 3.0.1 *7 November 2020*
    - Correct variable name in `ht16k33matrix.py`.
- 3.0.0 *6 November 2020*
    - Initial public release.

## Licence and Copyright

This repository’s source code and documentation is copyright © 2025, Tony Smith (@smittytone).

The HTK16K33 driver and subsidiary display drivers are licensed under the [MIT License](LICENSE.md).
