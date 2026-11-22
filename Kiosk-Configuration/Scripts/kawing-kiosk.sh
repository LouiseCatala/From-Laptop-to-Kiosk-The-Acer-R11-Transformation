# Public archive only: internal server addresses were replaced with placeholder .example hosts.
#!/bin/bash

CHROME_PROFILE="/home/kawing/.config/kawing-chrome"

KAWING_URLS=(
    "http://kawing-server-1.example:3000/"
    "http://kawing-server-2.example:3000/"
)
KAWING_URL=""
OFFLINE_PAGE="file:///home/kawing/kawing-offline.html"
MAINTENANCE_FLAG="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/kawing-maintenance"
sleep 3


# Start touchscreen keyboard
pkill onboard 2>/dev/null

onboard \
  --layout=/home/kawing/.local/share/onboard/layouts/KAWING-Phone.onboard \
  --theme=/usr/share/onboard/themes/Blackboard.theme \
  >/tmp/onboard.log 2>&1 &

# ---------------------------------------------------
# HIDE XFCE
# ---------------------------------------------------

pkill -x xfce4-panel 2>/dev/null
pkill -x xfdesktop 2>/dev/null


# ---------------------------------------------------
# PREVENT SCREEN BLANKING
# ---------------------------------------------------

xset s off
xset s noblank
xset -dpms


# ---------------------------------------------------
# HIDE CURSOR
# ---------------------------------------------------

pkill -x unclutter 2>/dev/null

unclutter \
    --timeout 2 \
    --hide-on-touch \
    --start-hidden \
    --fork


# ---------------------------------------------------
# CHROME CONTROL
# ---------------------------------------------------

chrome_running() {

    pgrep -f -- "--user-data-dir=$CHROME_PROFILE" >/dev/null 2>&1

}


stop_chrome() {

    pkill -TERM -f -- "--user-data-dir=$CHROME_PROFILE" 2>/dev/null

    sleep 2

}


show_offline() {

    stop_chrome

    google-chrome-stable --user-data-dir="$CHROME_PROFILE" --no-first-run --no-default-browser-check --force-renderer-accessibility=complete --kiosk "$OFFLINE_PAGE" \
        >/tmp/kawing-chrome.log 2>&1 &

    sleep 2

}


show_kawing() {

    stop_chrome

    google-chrome-stable --user-data-dir="$CHROME_PROFILE" --no-first-run --no-default-browser-check --force-renderer-accessibility=complete --kiosk "$KAWING_URL" \
        >/tmp/kawing-chrome.log 2>&1 &

    sleep 2

}


# ---------------------------------------------------
# KIOSK LOOP
# ---------------------------------------------------

CURRENT_MODE=""

while [ ! -f "$MAINTENANCE_FLAG" ]; do

    AVAILABLE_URL=""

    for url in "${KAWING_URLS[@]}"; do
        if curl -fsS --connect-timeout 3 "$url" >/dev/null 2>&1; then
            AVAILABLE_URL="$url"
            break
        fi
    done

    if [ -n "$AVAILABLE_URL" ]; then
        if [ "$KAWING_URL" != "$AVAILABLE_URL" ]; then
            KAWING_URL="$AVAILABLE_URL"
            CURRENT_MODE=""
        fi

        # Server is ONLINE

        if [ "$CURRENT_MODE" != "online" ]; then

            show_kawing
            CURRENT_MODE="online"

        elif ! chrome_running; then

            show_kawing

        fi

    else

        # Server is OFFLINE

        if [ "$CURRENT_MODE" != "offline" ]; then

            show_offline
            CURRENT_MODE="offline"

        elif ! chrome_running; then

            show_offline

        fi

    fi

    sleep 5

done
