# DESIGN.md

Busview's design guide: what is its own, and where the rest comes from.

**Everything not said here is the suite's.** Colour tokens, type ramp, spacing, motion, window chrome, accessibility floor, every control and the tool window's layout come from the suite's design contract, `sdk/DESIGN.md` (Resolute-SDK at the commit `sdk.json` pins). Busview never draws a control the shared library provides and never hardcodes a colour, a size or a spacing value. This file holds only what the contract leaves to a tool: its identity, and what its window's sections contain.

Both were chosen by the owner on 2026-11-17, each from three directions.

## 1. Identity

**Package: the letter B drawn as a chip package.** A stem, two bowls and three pins down its left side.

- Free-standing with no tile, and every stroke has rounded ends.
- The pins and the upper bowl are the lit face; the stem and the lower bowl are the shaded face. Each face carries a gradient within the one green hue.
- The small drawing, used below 40 pixels, is the B alone with heavier strokes and no pins.
- A letter is an exception to the suite's icon rules, approved for Busview by the owner and recorded in `sdk/DESIGN.md` section 14.

| Name | Value | Use |
| --- | --- | --- |
| Mint | `#5CF0B4` | The lit face, at its lightest |
| Emerald | `#12B981` | Where the two faces meet |
| Pine | `#0A7F6B` | The shaded face, at its darkest |
| Ground | `#06120E` | The banners' ground |
| Ground high | `#0C2A20` | The ground's lighter corner |
| Muted | `#B4DCCB` | Secondary text on that ground |
| Paper, Ink | `#F4F7F5`, `#0B1512` | Text on dark and on light |

Type: the name is Sora in two weights, "Bus" in SemiBold and "view" in Light, and a tagline is Inter. Inside the tool, text is the system font, as the contract says.

Tagline: "See what is inside. Know what to do next."

The assets are in `brand/`, all written by `python brand/build.py` from the description in that file (`--check` fails when one differs from what the script builds). The fonts are in `brand/fonts/` under the SIL Open Font License. Busview's banners carry a glow and a field of solder pads that the suite's shared `brandkit.py` does not draw, so the script is Busview's own.

| File | What it is |
| --- | --- |
| `busview-icon.svg`, `-512.png`, `-256.png`, `-192.png`, `-64.png`, `-48.png` | The icon, detailed drawing |
| `busview-icon-small.svg`, `-32.png`, `-16.png` | The icon's small drawing |
| `busview.ico` | The Windows icon, ten sizes from 16 to 256 |
| `busview-wordmark-light.svg`, `.png`, `-dark.svg`, `.png` | The icon with the name |
| `readme-banner.svg`, `.png` | The README banner, 1280 by 320 |
| `social-preview.svg`, `.png` | The repository's social preview, 1280 by 640 |
| `avatar.svg`, `.png` | The icon on the ground, 512 by 512 |

Rules: the icon is never recoloured, outlined, stretched or set on a tile. Green is the icon's colour only: the interface's accent is the Windows accent, as in every tool of the suite.

## 2. The window

**The suite's tool window** (`sdk/DESIGN.md` section 16): sections on the left, the selected section's content on the right with its title and actions in a header, a status bar under both. What is Busview's own is the list of sections and what each shows.

**The full contract is `design/SPEC.md`**, written from the working design in `design/busview-interface.html` and its captures in `design/captures/`. This section is the summary; where the two differ, `design/SPEC.md` is right.

### Sections

| Section | What it holds |
| --- | --- |
| Overview | The computer in one screen: eight tiles, one per area, and the advice Busview has for it |
| Board | A diagram of the slots and connectors the firmware reports (fitted, free, needs attention) with the selected part's values and advice beside it |
| Memory | The advice on what to buy, the slots, and every fitted module |
| Processor | The processor, its cache and its features |
| Motherboard | The board, the BIOS, TPM and Secure Boot, the firmware tables, and whether the computer is ready for Windows 11 |
| Storage | Each drive with its health, and the free M.2 slots and SATA ports |
| Graphics | Each graphics adapter and each display |
| Devices | PCI and USB devices with their IDs |
| Network and power | Network adapters and the battery |
| Snapshots | Saved states of the computer, and the comparison of any two |
| Beep codes | What a BIOS beep pattern means and what to try, starting on this computer's BIOS maker |
| Activity | What the tool did, newest first |
| Settings | The suite's settings pages from the framework, and one page of Busview's own |
| About | The framework's About page for this tool |

### The first screen

Overview opens selected. It shows the thing the tool acts on, the computer, as eight tiles and the advice as rows, each with its state as an icon and a word. The primary action is Take snapshot: it is the one action that changes anything, and what it changes is a file in the user's own folder.

### Busview's own drawing

The Board diagram is the one surface the SDK has no control for. It is drawn with the SDK's render context and tokens, exposes each part to UI Automation, and is driven by keyboard. It is a diagram of what the firmware reports and says so on its face: Busview does not know where a slot sits on a real board.

### What the window does not have

No menu bar, no splash screen, no live sensor graphs (version 1 reads no sensors), no advertising and no account. Nothing Busview shows leaves the computer.
