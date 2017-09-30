#!/usr/bin/python
# -*- coding: utf-8 -*-

from fonts import SUPER_TINY_FONT
import max7219.led as led
from max7219.font import proportional, SINCLAIR_FONT, TINY_FONT, CP437_FONT, LCD_FONT

device = led.matrix(cascaded=2);
device.orientation(270);
device.brightness(1);
device.show_message("123", font=proportional(SUPER_TINY_FONT));
