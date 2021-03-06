#! /bin/bash
# Copyright (c) 1996-2016 Glou Prods.
# All rights reserved.
#
# Author: Kaci Agoun, 2016
#
# Please send feedback to kagoun@gmail.com
#
# /etc/init.d/maxou-clock.sh
#
### BEGIN INIT INFO
# Provides: testdaemon
# Required-Start:
# Should-Start:
# Required-Stop:
# Should-Stop:
# Default-Start:  3 5
# Default-Stop:   0 1 2 6
# Short-Description: Test daemon process
# Description:    Runs up the test daemon process
### END INIT INFO

# Activate the python virtual environment
    . /path_to_virtualenv/activate

case "$1" in
  start)
    echo "Starting server"
    # Start the daemon
    python /home/pi/maxou-clock/bin/maxou-clock.py start
    ;;
  stop)
    echo "Stopping server"
    # Stop the daemon
    python /home/pi/maxou-clock/bin/maxou-clock.py stop
    ;;
  restart)
    echo "Restarting server"
    python /home/pi/maxou-clock/bin/maxou-clock.py restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/maxou-clock.sh {start|stop|restart}"
    exit 1
    ;;
esac

exit 0