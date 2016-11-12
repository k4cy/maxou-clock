#!/bin/bash

/usr/bin/dtc -@ -I dts -O dtb -o pwm-audio-pi-zero-overlay.dtb pwm-audio-pi-zero-overlay.dts
sudo cp pwm-audio-pi-zero-overlay.dtb /boot
