#!/usr/bin/env python3

import gi
import subprocess
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


CSS = b"""
window {
    background: transparent;
}

#card {
    background: #ffffff;
    border-radius: 18px;
    border: 1px solid #d9e1d5;
}

#header {
    background: #254b32;
    border-radius: 18px 18px 0 0;
    padding: 18px;
}

#title {
    color: white;
    font-size: 24px;
    font-weight: bold;
}

#subtitle {
    color: #dce8df;
    font-size: 13px;
}

#body {
    padding: 25px;
}

label {
    color: #25332a;
    font-size: 14px;
}

entry {
    min-height: 42px;
    padding: 6px 12px;
    border-radius: 9px;
    border: 1px solid #b9c5bc;
    font-size: 17px;
    background: #ffffff;
}

entry:focus {
    border-color: #39734b;
}

#error {
    color: #b42318;
    font-size: 13px;
}

#cancel {
    min-height: 42px;
    border-radius: 9px;
    padding: 0 22px;
}

#shutdown {
    min-height: 42px;
    border-radius: 9px;
    padding: 0 22px;
    background: #a83232;
    color: white;
    font-weight: bold;
}

#shutdown:hover {
    background: #922b2b;
}
"""


class ShutdownWindow(Gtk.Window):

    def __init__(self):
        super().__init__()

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)

        self.set_default_size(520, 340)

        # Fixed position on 1366x768 R11 display
        self.move(423, 55)

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)

        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        card = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )
        card.set_name("card")
        self.add(card)

        # HEADER
        header = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=4
        )
        header.set_name("header")

        title = Gtk.Label(label="KAWING Secure Shutdown")
        title.set_name("title")
        title.set_xalign(0)

        subtitle = Gtk.Label(
            label="Authentication is required before powering off this kiosk."
        )
        subtitle.set_name("subtitle")
        subtitle.set_xalign(0)

        header.pack_start(title, False, False, 0)
        header.pack_start(subtitle, False, False, 0)

        card.pack_start(header, False, False, 0)

        # BODY
        body = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )
        body.set_name("body")

        username_label = Gtk.Label(label="Username")
        username_label.set_xalign(0)

        self.username = Gtk.Entry()
        self.username.set_placeholder_text("Enter username")

        password_label = Gtk.Label(label="Password")
        password_label.set_xalign(0)

        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        self.password.set_placeholder_text("Enter password")
        self.password.set_activates_default(True)

        for entry in (self.username, self.password):
            entry.connect("focus-in-event", self.show_keyboard)
            entry.connect("button-press-event", self.show_keyboard)

        self.error = Gtk.Label()
        self.error.set_name("error")
        self.error.set_xalign(0)

        body.pack_start(username_label, False, False, 0)
        body.pack_start(self.username, False, False, 0)

        body.pack_start(password_label, False, False, 4)
        body.pack_start(self.password, False, False, 0)

        body.pack_start(self.error, False, False, 2)

        buttons = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )

        cancel = Gtk.Button(label="Cancel")
        cancel.set_name("cancel")
        cancel.connect("clicked", self.cancel)

        shutdown = Gtk.Button(label="Shut Down")
        shutdown.set_name("shutdown")
        shutdown.connect("clicked", self.authenticate)

        self.set_default(shutdown)

        buttons.pack_end(shutdown, False, False, 0)
        buttons.pack_end(cancel, False, False, 0)

        body.pack_end(buttons, False, False, 4)

        card.pack_start(body, True, True, 0)

        self.connect("destroy", Gtk.main_quit)

    @staticmethod
    def raise_keyboard():
        try:
            subprocess.Popen(
                [
                    "dbus-send",
                    "--session",
                    "--dest=org.onboard.Onboard",
                    "--type=method_call",
                    "/org/onboard/Onboard/Keyboard",
                    "org.onboard.Onboard.Keyboard.Show"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except OSError:
            pass
        return False

    def show_keyboard(self, *args):
        self.raise_keyboard()
        GLib.timeout_add(250, self.raise_keyboard)
        return False

    def cancel(self, button):
        # Close the keyboard explicitly opened by this dialog.
        try:
            subprocess.run(
                ["dbus-send", "--session", "--dest=org.onboard.Onboard",
                 "--type=method_call", "--print-reply", "--reply-timeout=1000",
                 "/org/onboard/Onboard/Keyboard",
                 "org.onboard.Onboard.Keyboard.Hide"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
        except (OSError, subprocess.TimeoutExpired):
            pass
        Gtk.main_quit()

    def authenticate(self, button):
        username = self.username.get_text().strip()
        password = self.password.get_text()

        if username != "kawing":
            self.error.set_text("Incorrect username or password.")
            self.password.set_text("")
            return

        try:
            result = subprocess.run(
                ["pamtester", "login", username, "authenticate"],
                input=password + "\n",
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            self.error.set_text("Authentication service unavailable.")
            return

        if result.returncode != 0:
            self.error.set_text("Incorrect username or password.")
            self.password.set_text("")
            self.password.grab_focus()
            return

        # Correct credentials
        subprocess.Popen(
            ["sudo", "-S", "-k", "-p", "",
             "/usr/bin/systemctl", "poweroff"],
            stdin=subprocess.PIPE,
            text=True
        ).communicate(password + "\n")


window = ShutdownWindow()
window.show_all()
window.username.grab_focus()
window.show_keyboard()
Gtk.main()
