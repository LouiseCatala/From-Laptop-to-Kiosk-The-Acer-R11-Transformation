# From Laptop to Kiosk — Acer R11 Touchscreen Transformation

An Acer Chromebook R11 repurposing project for KAWING, with an AutoCAD enclosure concept and a documented Debian touchscreen kiosk configuration.

I started this project because I needed a shared access device for my thesis without the cost of buying a dedicated kiosk. The repository brings together the physical design study and the software configuration used to explore that idea.

## Explore the project

| Part | Documentation |
| --- | --- |
| Enclosure concept, component arrangement, and CAD previews | [CAD design and assembly](CAD/README.md) |
| Debian, XFCE, Chrome kiosk mode, and touchscreen keyboard | [Kiosk configuration](Kiosk-Configuration/README.md) |
| Setup walkthrough | [Installation notes](Kiosk-Configuration/INSTALLATION.md) |
| Startup and shutdown flow | [System flow](Kiosk-Configuration/SYSTEM-FLOW.md) |
| Third-party sources | [Credits](Kiosk-Configuration/CREDITS.md) |

## Project status

The CAD files are conceptual visualizations. Some dimensions, component geometries, and mounting positions are approximate and need physical verification before fabrication.

The kiosk package is a historical configuration snapshot. Its documentation reports user tests of the browser, keyboard, and shutdown confirmation, but identifies remaining checks for cold boot, public touch-only operation, session privacy, and kiosk escape protection. It is not a security-audited deployment package.

## Related work

- [KAWING — Post-Harvest Coordination Platform](https://github.com/LouiseCatala/KAWING--IoT-Integrated-Post-Harvest-Coordination-Platform)
- [Orland Louise Catala's portfolio](https://catala-portfolio.vercel.app/)

## Author and use

Orland Louise Catala · [GitHub](https://github.com/LouiseCatala)

See the existing CAD and kiosk documentation for copyright, permission requirements, and third-party credits. This index does not change those terms.
