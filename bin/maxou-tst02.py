#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, TINY_FONT, SINCLAIR_FONT

import argparse
import atexit
from daemon import runner
from datetime import datetime
import logging
import os
import sys
import time

def stop_clean(device):
  logger.info("Exiting message") 
  if not args.quick:
    show_message(device, "    Good bye commander !!      ", fill="white", font=proportional(LCD_FONT))
  else:
    show_message(device, "      ", fill="white", font=proportional(LCD_FONT))

class MaxouClock():
    def __init__(self):
      self.stdin_path = '/dev/null'
      self.stdout_path = '/dev/tty'
      self.stderr_path = '/dev/tty'
      pidpath = os.path.realpath(os.path.dirname(__file__))+'/../run'
      if not os.path.exists(pidpath):
        os.makedirs(pidpath)
      self.pidfile_path =  pidpath+'/maxou-clock.pid'
      self.pidfile_timeout = 5
    def run(self):
      logger.info("Initializing device") 
      # create matrix device
      serial = spi(port=0, device=0, gpio=noop())
      device = max7219(serial, cascaded=2, block_orientation=0, rotate=0)
      device.contrast(64)
      virtual = viewport(device, width=16, height=8)

      atexit.register(stop_clean, device)

      logger.info("Welcome message")
      if not args.quick:
        show_message(device, "    Welcome commander !! Maxou's clock has been launched !!    ", fill="white", font=proportional(LCD_FONT))
      before = 15;
      x = 0;
      #for _ in range(60):
      while True:
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        dot = second % 2 == 0  # calculate blinking dot
        # Set hours & minutes
        words=[str(int(hour / 10))+str(hour % 10)+str(int(minute / 10))+str(minute % 10)]
        with canvas(virtual) as draw:
          for i, word in enumerate(words):
            text(draw, (0, i * 8), word, fill="white", font=TINY_FONT)

        time.sleep(1);
        x += 1;

if __name__ == "__main__":
  # setting arguments of the program
  parser = argparse.ArgumentParser(prog=__file__, description="Run Maxime's Clock & Alarm",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('action', choices=('start', 'stop', 'restart'), help='starts/stops/restarts %(prog)s daemon')
  parser.add_argument('-q', '--quick', dest='quick', action='store_true', help='Skip messages when starting and exiting', default=False)
  parser.add_argument('--debug', dest='debug', action='store_true', help='Show debug information', default=False)
  parser.add_argument('--no-debug', dest='debug', action='store_false', help='No debug information (default)', default=False)
  # parsing arguments
  args = parser.parse_args()

  logpath = os.path.realpath(os.path.dirname(__file__))+"/../log"
  if not os.path.exists(logpath):
    os.makedirs(logpath)

  logger = logging.getLogger("MaxouClock")
  if args.debug:
    logger.setLevel(logging.DEBUG)
  else:
    logger.setLevel(logging.INFO)

  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler = logging.FileHandler(logpath+"/maxou-clock.log")
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  app = MaxouClock()
  daemon_runner = runner.DaemonRunner(app)
  #This ensures that the logger file handle does not get closed during daemonization
  daemon_runner.daemon_context.files_preserve=[handler.stream]
  daemon_runner.do_action()
