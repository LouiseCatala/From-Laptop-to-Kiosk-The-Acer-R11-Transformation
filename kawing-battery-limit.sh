#!/bin/bash

BAT="/sys/class/power_supply/BAT0"

while true; do

    CAPACITY=$(cat "$BAT/capacity")

    if [ "$CAPACITY" -ge 80 ]; then

        echo inhibit-charge > "$BAT/charge_behaviour"

    elif [ "$CAPACITY" -le 75 ]; then

        echo auto > "$BAT/charge_behaviour"

    fi

    sleep 60

done
