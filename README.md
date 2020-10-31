# HT16K33 Drivers 3.0.0 #

This repo provides Python drivers for the Holtek HT16K33 controller chip and various display devices based upon it, such as the [Adafruit 0.8-inch 8x16 LED Matrix FeatherWing](https://www.adafruit.com/product/3149).

The driver supports both [CircuitPython](https://circuitpython.org) and [MicroPython](https://dmicropython.org) applications. It communicates using I&sup2;C.

## Importing the Drivers ##

The driver package comprises a parent generic HT16K33 driver and child drivers for various displays themselves. All your code needs to do is `import` the latter. For example:

```python
from ht16k33segment import HT16K33Segment
```

You can then instantiate the driver.

You will need both the display driver file and `ht16k33.py` in your project folder.

## Display Drivers ##

| Driver | Example&nbsp;Product |
| --- | --- |
| [4-digit, 7-segment LED](./docs/ht16k33segment.md) | [Adafruit 0.56-inch 4-digit, 7-segment LED display](https://www.adafruit.com/products/878) |
| [8 x 8 matrix LED](./docs/ht16k33matrix.md) | [Adafruit Mini 0.8-inch 8x8 LED Matrix](https://www.adafruit.com/product/872) |
| [16 x 8 FeatherWing matrix LED](./docs/ht16k33matrixfeatherwing.md) | [Adafruit 0.8-inch 8x16 LED Matrix FeatherWing](https://www.adafruit.com/product/3149) |

## License ##

The HTK16K33 driver and subsidiary display drivers are licensed under the [MIT License](LICENSE).
