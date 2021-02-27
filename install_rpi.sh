#!/usr/bin/env bash

echo "Installing the Adafruit TFT display"

sudo pip3 install adafruit-python-shell click

git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd Raspberry-Pi-Installer-Scripts
sudo python3 adafruit-pitft.py --display=28r --rotation=0 --install-type=console
#sudo python3 adafruit-pitft.py --display=28r --rotation=0 --install-type=fbcp


