#!/bin/bash

# the date format on the panel
d=$(date "+%H:%M\n %Y-%m-%d ")

# the date format in the tooltip
t=$(date "+%A %Y-%m-%d %H:%M 第%U周")

# the app to run when the data is clicked
a="/home/${USER}/.xfce-lunar/lunar.py"

# the genmon command
echo -e "<txt>$d</txt><txtclick>$a</txtclick><tool>$t</tool>"
