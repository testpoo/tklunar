#!/bin/bash

rm -rf ~/.xfce-lunar
mkdir ~/.xfce-lunar
cp ../xfce-lunar/*.py ~/.xfce-lunar
cp ../xfce-lunar/clock.png ~/.xfce-lunar
cp ../xfce-lunar/lunar.sh ~/.xfce-lunar
chmod +x ~/.xfce-lunar/*
