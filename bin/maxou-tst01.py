#!/usr/bin/python

import os
from daemon import runner
from datetime import datetime
import sys
import time
import max7219.led as led
from max7219.font import proportional, SINCLAIR_FONT, TINY_FONT, CP437_FONT, LCD_FONT

class MaxouClock():
    def __init__(self):
      self.stdin_path = '/dev/null'
      self.stdout_path = '/dev/tty'
      self.stderr_path = '/dev/tty'
      self.pidfile_path =  os.path.realpath(os.path.dirname(__file__))+'/../run/maxou-clock.pid'
      self.pidfile_timeout = 5
    def run(self):
      device = led.matrix(cascaded=2);
      device.orientation(270);
      device.brightness(1);
      #device.show_message("Maxou's clock launched !", font=proportional(LCD_FONT));
      before = 15;
      x = 0;
      #for _ in range(60):
      while True:
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        dot = second % 2 == 0                # calculate blinking dot
        # Set hours
        device.show_message(str(int(hour / 10))+str(hour % 10)+str(int(minute / 10))+str(minute % 10), font=proportional(TINY_FONT))

        if (x > 15):
          x = 0;
        if (x == 0):
          before = 15;
        else:
          before = x - 1;

        device._buffer[before] |= (1 << 7);
        device._buffer[x] &= ~(1 << 7);
        device.flush();
        time.sleep(1);
        x += 1;

app = MaxouClock()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()