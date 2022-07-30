# HT16K33 Drivers 3.2.0 #

This repo provides Python drivers for the Holtek HT16K33 controller chip and various display devices based upon it, such as the [Adafruit 0.8-inch 8x16 LED Matrix FeatherWing](https://www.adafruit.com/product/3149) and the [Raspberry Pi Pico](https://www.raspberrypi.org/documentation/pico/getting-started/).

The drivers supports both [CircuitPython](https://circuitpython.org) and [MicroPython](https://micropython.org) applications. They communicate using I&sup2;C.

## Importing the Drivers ##

The driver package comprises a parent generic HT16K33 class and child classes for various displays themselves. All your code needs to do is `import` the latter. For example:

```python
from ht16k33segment import HT16K33Segment
```

You can then instantiate the driver object. This requires a configured I2C bus object.

You will need both the display driver file and `ht16k33.py` in your project folder.

## Reducing Memory Usage ##

Adding the driver code may prove too much for certain CircuitPython devices which have limited amounts of memory. To overcome this, run the `mpy-cross` compiler. This will compile the raw Python into a highly compact form in a `.mpy` file. Copy `ht16k33.mpy` and the device-specific `.mpy` file to your device in place of the `.py` versions.

The repo’s `mpy` directory contains pre-compiled versions for CircuitPython applications.

## Display Drivers ##

| Driver<br />(Click for docs) | Example&nbsp;Product |
| --- | --- |
| [Small 4-digit, 7-segment LED](https://smittytone.net/docs/ht16k33_segment.html) | [Adafruit 0.56-inch 4-digit, 7-segment LED display](https://www.adafruit.com/products/878) |
| [Large 4-digit, 7-segment LED](https://smittytone.net/docs/ht16k33_segmentbig.html) | [Adafruit 1.2-inch 4-digit, 7-segment LED display](https://www.adafruit.com/product/1270) |
| [Small 4-digit, 14-segment LED](https://smittytone.net/docs/ht16k33_segment14.html) | [SparkFun Qwiic Alphanumeric Display](https://www.sparkfun.com/products/16916),<br />[Adafruit 0.54in Alphanumeric Display](https://www.adafruit.com/product/1911) |
| [8x8 monochrome matrix LED](https://smittytone.net/docs/ht16k33_matrix.html) | [Adafruit Mini 0.8-inch 8x8 LED Matrix](https://www.adafruit.com/product/872) |
| [8x8 bi-colour matrix LED](https://smittytone.net/docs/ht16k33_matrixcolour.html) | [Adafruit 1.2-inch 8x8 bi-color LED matrix backpack](https://www.adafruit.com/product/902) |
| [16x8 FeatherWing matrix LED](https://smittytone.net/docs/ht16k33_matrixfeatherwing.html) | [Adafruit 0.8-inch 8x16 LED Matrix FeatherWing](https://www.adafruit.com/product/3149) |

Further drivers may be added in due course.

## Release Notes

- 3.2.0 *26 July 2022*
    - Support the [Adafruit 0.54in Alphanumeric Display](https://www.adafruit.com/product/1911) via `ht16k33segment14.py`.
    - Bug fixes.
- 3.2.0 *16 February 2022*
    - Add `ht16k33segment14.py` to support the [SparkFun Qwiic Alphanumeric Display](https://www.sparkfun.com/products/16916).
- 3.0.2 *23 November 2020*
    - Refactor out some `ht16k33matrix.py` code.
- 3.0.1 *7 November 2020*
    - Correct variable name in `ht16k33matrix.py`.
- 3.0.0 *6 November 2020*
    - Initial public release.

## Licence and Copyright

This repository’s source code and documentation is copyright 2022, Tony Smith (@smittytone).

The HTK16K33 driver and subsidiary display drivers are licensed under the [MIT License](LICENSE.md).
