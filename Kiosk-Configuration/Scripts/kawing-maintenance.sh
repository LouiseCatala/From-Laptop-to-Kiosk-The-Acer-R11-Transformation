#!/bin/bash

MAINTENANCE_FLAG="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/kawing-maintenance"

# Enter maintenance mode
touch "$MAINTENANCE_FLAG"

# Stop kiosk launcher
pkill -f "/home/kawing/kawing-kiosk.sh" 2>/dev/null


# Stop kiosk Chrome
pkill -TERM -f -- "--user-data-dir=/home/kawing/.config/kawing-chrome" 2>/dev/null


# Restore mouse cursor
pkill -x unclutter 2>/dev/null


# Restore XFCE desktop
if ! pgrep -x xfdesktop >/dev/null; then

    nohup xfdesktop \
        >/tmp/xfdesktop.log 2>&1 &

fi


# Restore XFCE panel
if ! pgrep -x xfce4-panel >/dev/null; then

    nohup xfce4-panel \
        >/tmp/xfce4-panel.log 2>&1 &

fi
