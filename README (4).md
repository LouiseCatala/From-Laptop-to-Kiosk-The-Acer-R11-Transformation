# KAWING Kiosk Scripts

These are scripts from the **November 10, 2026 configuration archive** supplied for this project. Most script content is preserved; the private server IP addresses in `kawing-kiosk.sh` have been replaced with `.example` hostnames before publication.

| File | Purpose |
|:--|:--|
| `kawing-kiosk.sh` | Starts the Onboard keyboard and Chrome kiosk; chooses online/offline view |
| `kawing-resume.sh` | Resumes kiosk mode after maintenance |
| `kawing-maintenance.sh` | Restores XFCE desktop for servicing |
| `kawing-offline.html` | Local page when configured KAWING server is unreachable |
| `kawing-shutdown-ui.py` | GTK password-confirmation window for shutdown |
| `kawing-shutdown.sh` | Launches the shutdown dialog |
| `kawing-battery-limit.sh` | Experimental battery threshold handling |

**Important:** These are archival examples, not turnkey, tested installation scripts. They contain paths configured for Linux user `kawing`. The current archived kiosk script points to **nonfunctional example servers**; adjust it to the correct trusted deployment if reproducing the setup. Actual public KAWING website: https://kawingph.com/.

**Security:** The shutdown dialog uses PAM authentication, then passes a password to `sudo -S`. Do not treat that design as a hardened public-kiosk security boundary. Inspect `/etc/sudoers` permissions and audit all exits, recovery paths and maintenance methods before deployment. The charge-control script depends on hardware support for `charge_behaviour`; confirm functionality on the real device. No authentication secrets are intentionally included here.
