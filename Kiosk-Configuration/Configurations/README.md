# Desktop, Login and Service Configuration

This folder contains actual text configuration files from the November 10, 2026 handoff. The directory names group original system locations for readability; **they are not drop-in installer folders**.

| Folder | Original path / purpose |
|:--|:--|
| `LightDM/` | `/etc/lightdm/` login manager and custom keyboard mapping |
| `Autostart/` | `~/.config/autostart/` kiosk session launcher |
| `XFCE/` | XFCE shortcuts, session, power management, helpers and MIME default settings |
| `Desktop/` | Desktop shortcuts to launch the kiosk or request shutdown |
| `Systemd/` | System service for charge-control experiment |

**Public repository warning:** Do not paste credentials, real kiosk network addresses, browser profiles, device identifiers or private diagnostics into public repositories. Back up and review all current files before applying any old snapshot. This archive isn't a security audit, and does not certify kiosk escape prevention.
