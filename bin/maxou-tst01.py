#!/usr/bin/python

import argparse
import atexit
from daemon import runner
from datetime import datetime
import max7219.led as led
from max7219.font import proportional, SINCLAIR_FONT, TINY_FONT, CP437_FONT, LCD_FONT
import logging
import os
import sys
import time

def stop_clean(device):
  logger.info("Exiting message") 
  if not args.quick:
    device.show_message("    Good bye commander !!      ", font=proportional(LCD_FONT));
  else:
    device.show_message("      ", font=proportional(LCD_FONT));

class MaxouClock():
    def __init__(self):
      self.stdin_path = '/dev/null'
      self.stdout_path = '/dev/tty'
      self.stderr_path = '/dev/tty'
      self.pidfile_path =  os.path.realpath(os.path.dirname(__file__))+'/../run/maxou-clock.pid'
      self.pidfile_timeout = 5
    def run(self):
      logger.info("Initializing device") 
      device = led.matrix(cascaded=2);
      device.orientation(270);
      device.brightness(1);

      atexit.register(stop_clean, device)

      logger.info("Welcome message") 
      if not args.quick:
        device.show_message("    Welcome commander !! Maxou's clock has been launched !!    ", font=proportional(LCD_FONT));
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
        device.show_message(str(int(hour / 10))+str(hour % 10)+str(int(minute / 10))+str(minute % 10), font=proportional(TINY_FONT))

        if (x > 15):
          x = 0;
        if (x == 0):
          before = 15;
        else:
          before = x - 1;

        if dot:
          device._buffer[7] &= ~(1 << 2);
          device._buffer[7] &= ~(1 << 4);
        else:
          device._buffer[7] |= (1 << 2);
          device._buffer[7] |= (1 << 4);

        device._buffer[before] |= (1 << 7);
        device._buffer[x] &= ~(1 << 7);
        device.flush();
        time.sleep(1);
        x += 1;

# setting arguments of the program
parser = argparse.ArgumentParser(prog=__file__, description="Run Maxime's Clock & Alarm")
parser.add_argument('action', choices=('start', 'stop', 'restart'), help='starts/stops/restarts %(prog)s daemon')
parser.add_argument('-q', '--quick', dest='quick', action='store_true', help='Skip messages when starting and exiting', default=False)
parser.add_argument('--debug', dest='debug', action='store_true', help='Show debug information', default=False)
parser.add_argument('--no-debug', dest='debug', action='store_false', help='No debug information (default)', default=False)
# parsing arguments
args = parser.parse_args()

logger = logging.getLogger("MaxouClock")
if args.debug:
  logger.setLevel(logging.DEBUG)
else:
  logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(os.path.realpath(os.path.dirname(__file__))+"/../log/maxou-clock.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = MaxouClock()
daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
