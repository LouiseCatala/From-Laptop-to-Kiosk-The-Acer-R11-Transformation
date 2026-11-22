# Installation History — Acer Chromebook R11 KAWING Kiosk

**Device:** Acer Chromebook R11 CB5-132T-C9KK (CYAN)  
**Original OS:** ChromeOS  
**Documented installed OS:** Debian GNU/Linux 13 (Trixie), 64-bit, XFCE (X11)  
**Firmware identified in snapshot:** MrChromebox UEFI  
**Archived configuration date:** November 10, 2026

> This document combines the creator's account of the conversion, the saved kiosk configuration, and official public instructions. **It is not a verified keystroke-by-keystroke log of the original installation.** No claim is made about the exact original Debian point-release ISO.

## 1. Preparing the laptop

I decided to repurpose an existing Acer R11 to provide an affordable shared access device for KAWING. Before changing the original firmware, I removed the CYAN motherboard's hardware write-protection screw.

- [Write-protection photo for the CYAN board (MrChromebox)](https://docs.mrchromebox.tech/images/wp/cyan_wp.jpg)
- [R11 disassembly reference with photos (Sudaraka)](https://sudaraka.org/how-to/chromebook-r11-archlinux-installation-guide/)

**Warning:** Opening the laptop and flashing its firmware can permanently damage or render it unbootable. Consult the device-specific MrChromebox documentation and back up important data before attempting this.

## 2. Replacing the stock firmware

I used the MrChromebox Firmware Utility Script to prepare the Chromebook for a regular Linux operating system. The **official** current invocation documented by MrChromebox is:

```bash
cd; curl -LOf https://mrchromebox.tech/firmware-util.sh && sudo bash firmware-util.sh
```

The exact firmware menu number may change: follow the **on-screen item labeled `Install/Update UEFI (Full ROM) Firmware`**, not a memorized number. Check the exact device's support before running the tool. Back up the stock firmware as prompted.

Official instructions: [MrChromebox Getting Started](https://docs.mrchromebox.tech/docs/getting-started.html), [Firmware Utility Script](https://docs.mrchromebox.tech/docs/fwscript.html).

## 3. Installing Debian 13

I replaced ChromeOS with **Debian 13 (Trixie)** and used **XFCE** for the desktop session. The original archived handoff confirms the installed OS but not the precise ISO filename used during installation.

- [Official Debian 13 installer images](https://www.debian.org/releases/trixie/debian-installer/)
- [Official Debian 13 installation guide](https://www.debian.org/releases/trixie/amd64/index.en.html)
- [Debian ISO reference for this project](DEBIAN-13-ISO.md)

## 4. Configuring kiosk mode

After administrator login, XFCE starts the autostart desktop entry (`Configurations/Autostart/kawing-kiosk.desktop`), which calls the resume and kiosk scripts.

- **Chrome:** kiosk/fullscreen display
- **Onboard:** custom phone-style touch keyboard
- **Offline handling:** local KAWING connection page when server checks fail
- **Maintenance:** a script to restore desktop access for servicing

See [Scripts](Scripts/README.md), [Keyboard](Keyboard/README.md), and [Configurations](Configurations/README.md).

## 5. Restricting shutdown

The archived project uses a GTK dialog that requests the administrator's username and password before issuing a shutdown command. The script checks credentials with `pamtester` and then invokes `sudo systemctl poweroff`.

This is one **user-interface control**, not proof that power buttons or alternative system paths are blocked. A full kiosk security review is required before deployment.

## 6. Battery charge thresholds (experimental)

A saved systemd service and shell script were configured to try to pause charging at 80% and resume at 75%. Operation depends on kernel/hardware support and was not independently verified in this snapshot.

## Original purpose

I wanted farmers with limited access to personal devices to be able to use KAWING via a shared touchscreen kiosk. Because my own thesis budget was limited, I reused the Chromebook instead of purchasing kiosk hardware.
