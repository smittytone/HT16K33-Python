# HT16K33 Drivers 3.5.3 #

This repo provides Python drivers for the Holtek HT16K33 controller chip and various display devices based upon it, such as the [Adafruit 0.8-inch 8x16 LED Matrix FeatherWing](https://www.adafruit.com/product/3149) and the [Raspberry Pi Pico](https://www.raspberrypi.org/documentation/pico/getting-started/).

The library also supports generic seven-segment displays wired up to an HT16K33, which can drive up to eight these LEDs. The HT16K33 may be on a board of your own design, or on a third-part one, such as the [Adafruit 16x8 LED Matrix Driver Backpack ](https://www.adafruit.com/product/1427). LED units you can connect range from [single digits](https://www.sparkfun.com/products/8546) up to combinations of [multi-digit units](https://www.sparkfun.com/products/11409).

Connect your HT16K33 column pins to each LED's digit selection pin, and its row pins to the LED's segment selection pins.

The drivers support both [CircuitPython](https://circuitpython.org) and [MicroPython](https://micropython.org) applications. They communicate using I&sup2;C.

## Display Drivers ##

| Driver<br />(Click for docs) | Example&nbsp;Product |
| --- | --- |
| [Small 4-digit, 7-segment LED](https://smittytone.net/docs/ht16k33_segment.html) | [Adafruit 0.56-inch 4-digit, 7-segment LED display](https://www.adafruit.com/products/878) |
| [Large 4-digit, 7-segment LED](https://smittytone.net/docs/ht16k33_segmentbig.html) | [Adafruit 1.2-inch 4-digit, 7-segment LED display](https://www.adafruit.com/product/1270) |
| [Small 4-digit, 14-segment LED](https://smittytone.net/docs/ht16k33_segment14.html) | [SparkFun Qwiic Alphanumeric Display](https://www.sparkfun.com/products/16916),<br />[Adafruit 0.54in Alphanumeric Display](https://www.adafruit.com/product/1911) |
| [8x8 monochrome matrix LED](https://smittytone.net/docs/ht16k33_matrix.html) | [Adafruit Mini 0.8-inch 8x8 LED Matrix](https://www.adafruit.com/product/872) |
| [8x8 bi-colour matrix LED](https://smittytone.net/docs/ht16k33_matrixcolour.html) | [Adafruit 1.2-inch 8x8 bi-color LED matrix backpack](https://www.adafruit.com/product/902) |
| [16x8 FeatherWing matrix LED](https://smittytone.net/docs/ht16k33_matrixfeatherwing.html) | [Adafruit 0.8-inch 8x16 LED Matrix FeatherWing](https://www.adafruit.com/product/3149) |
| [Standalone HT16K33](https://smittytone.net/docs/ht16k33_segmentgen.html) | [Adafruit 16x8 LED Matrix Driver Backpack ](https://www.adafruit.com/product/1427) |

Further drivers may be added in due course.

## Import the Drivers ##

The driver package comprises a parent generic HT16K33 class and child classes for various displays themselves. All your code needs to do is `import` the latter. For example:

```python
from ht16k33segment import HT16K33Segment
```

You can then instantiate the driver object. This requires a **configured** I2C bus object.

You will need both the display driver file and `ht16k33.py` in your project folder.

## Install the Drivers ##

### MicroPython Manual ###

Use the [`pyboard`](https://github.com/micropython/micropython/blob/master/tools/pyboard.py) or [`mpremote`](https://github.com/micropython/micropython/tree/master/tools/mpremote) command line tools to copy the `ht16k33.py` and your required device-specific driver to your board.

### MicroPython MIP Install ###

From version 3.5.2, you can install the drivers using [MicroPython's MIP module](https://docs.micropython.org/en/v1.21.0/reference/packages.html). This requires a board running MicroPython 1.20 or above and connected to the Internet. Add the following to your code:

```python
import mip
mip.install('github:smittytone/HT16K33-Python')
```

If your board is not Internet-capable, you can install locally using [the `mpremote` tool](https://docs.micropython.org/en/latest/reference/mpremote.html):

```python
mpremote mip install github:smittytone/HT16K33-Python
```

### CircuitPython Install ###

Copy `ht16k33.py` and your required driver `.py` file(s) to the mounted board's `lib` folder.

## Reducing Memory Usage ##

Adding the driver code may prove too much for certain CircuitPython devices which have limited amounts of memory. To overcome this, [use MicroPython’s `mpy-cross` compiler](https://github.com/micropython/micropython/tree/master/mpy-cross). This will compile the raw Python into a highly compact form as a `.mpy` file. Copy `ht16k33.mpy` and the device-specific `.mpy` file to your device in place of the `.py` versions.

#### Example ####

```shell
./mpy-cross ht16k33.py ht16k33matrixcolour.py
```

## Documentation

You can find documentation for all of the drivers [at smittytone.net](https://smittytone.net/docs/ht16k33.html).

## Python Package Index

This code is now available [via the Python Package Index](https://pypi.org/project/ht16k33-python/) for folks using Thonny and other code-pulling IDEs.

## Release Notes

- 3.5.3 *Unreleased*
    - Remove the `.mpy` versions and provide instructions instead.
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

This repository’s source code and documentation is copyright 2024, Tony Smith (@smittytone).

The HTK16K33 driver and subsidiary display drivers are licensed under the [MIT License](LICENSE.md).
