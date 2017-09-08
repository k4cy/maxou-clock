#/bin/bash

SPI=$(lsmod | grep -i spi | wc -l)
if [ 0 -eq ${SPI} ] ; then
  echo "ERR You must activate SPI with raspi-config"
  exit 1
fi

PIP=$(which pip | wc -l)
if [ 0 -eq ${PIP} ] ; then
  echo "ERR You must activate SPI with raspi-config"
  exit 1
fi

GRPS=$(id | egrep "spi|gpio" | wc -l)
if [ 0 -eq ${GRPS} ] ; then
  echo "ERR You must add groups to user : gpio & spi"
  exit 1
fi
echo "Everything seems OK :)"
