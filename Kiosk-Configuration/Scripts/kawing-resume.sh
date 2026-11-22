#!/bin/bash

MAINTENANCE_FLAG="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/kawing-maintenance"

rm -f "$MAINTENANCE_FLAG"

if ! pgrep -f '/home/kawing/[k]awing-kiosk.sh' >/dev/null; then
    nohup /home/kawing/kawing-kiosk.sh \
      >/tmp/kawing-kiosk.log 2>&1 &
fi
