# Busview interface contract

This file is the contract for building Busview's window 1:1 with the design the owner chose on 2026-11-17: one section per part of the computer (direction A, "Ledger") with a Board view that draws the slots and connectors (from direction C). Every screen, control, state and string below is owned by one section of `todo/00-busview/TODO-01-busview.md`, named in the Owner column. A control with no working owner is a defect in the plan.

## How this binds

- **The reference is `design/busview-interface.html`.** Open it in a browser: it is the whole window, working, in both themes, with every state. `design/captures/` holds one capture per screen and state per theme, written by `python design/capture.py`.
- **1:1 means:** the same sections in the same order, the same controls in the same places with the same labels, the same states, the same words, and the same behaviour on click and on key. It does not mean the same pixels: geometry, colour, type and spacing come from the suite's tokens in `sdk/DESIGN.md`, which the design already uses (4px grid, the type ramp, the token set).
- **The suite's contract wins on shared surfaces.** The caption, sidebar, content header, status bar, Activity, Settings and About are the SDK's (`sdk/DESIGN.md` section 16). Busview never draws a control the SDK provides. What is Busview's own is the list of sections and what each contains.
- **The accent is the Windows accent.** The design shows Amber, the suite's fallback. Busview's green is its icon, never an interface colour.
- **The machine in the design is example data.** The built window shows the real machine. Every count, name and reading in the design is replaced by what the scan found, and a part of the design that has no real value behind it is not shown (rule X-9).
- **Where this file and the design disagree, this file wins** and the design is corrected in the same commit, with its captures.
- **Changing the contract** takes a commit that edits this file, the design and the captures together and says why.

## 1. The window

Captures: every file in `design/captures/`.

| ID | Element | What it is | Owner |
| --- | --- | --- | --- |
| W-1 | Caption | The SDK's caption: Busview's icon, the name "Busview", minimise, maximise, close | §32 |
| W-2 | Sidebar | Overview, Board, Memory, Processor, Motherboard, Storage, Graphics, Devices, Network and power, a separator, Snapshots, Beep codes, then Activity, Settings, About at the foot | §32 |
| W-3 | Selection indicator | The accent bar on the selected section, which slides between positions | §32 |
| W-4 | Attention dot | A dot on Board and Storage when a part needs attention; its tooltip and accessible name say "Needs attention" | §32 |
| W-5 | Count | The number of snapshots on Snapshots, shown when there is at least one | §37 |
| W-6 | Content header | The section's title, an optional secondary line (the board model on Board), then the section's actions with the primary action last | §32 |
| W-7 | Status bar, left | One sentence saying what the content shows, from the content itself | §32 |
| W-8 | Status bar, right | "Administrator" or "Standard user", then "Database" and its version | §32 |
| W-9 | Sidebar collapse | Below 600 pixels of width the sidebar shows icons only | §32 |
| W-10 | Window size | Opens at 1180 by 748 at 100 percent, has a minimum size, and remembers size and position per monitor | §32 |

Section order and names are fixed. Overview opens selected.

## 2. Overview

Captures: `overview-light.png`, `overview-dark.png`, `state-first-scan-*.png`.

| ID | Element | What it is | Owner |
| --- | --- | --- | --- |
| OV-1 | Rescan | Reads the machine again; the content updates from the new scan | §33 |
| OV-2 | Export report | Writes the report file (X-5) | §33 |
| OV-3 | Take snapshot | The primary action: saves a snapshot and says so in the status bar and in Activity | §33 |
| OV-4 | Machine line | Busview's icon, the computer name, then board model, Windows edition and version, and when it was scanned | §33 |
| OV-5 | Rights chip | "Administrator" or "Standard user", with an icon | §33 |
| OV-6 | Eight tiles | Memory, Processor, Motherboard, Storage, Graphics, Devices, Network, Windows 11: each a label with an icon, a headline value and one line of detail. Selecting a tile opens its section (Windows 11 opens Motherboard) | §33 |
| OV-7 | Advice list | One row per piece of advice: an icon, the advice as a title, the question it answers, and a verdict chip. Selecting a row opens the section the advice is about | §33 |
| OV-8 | Advice count | "4 answers" style count in the list's heading | §33 |

Status bar: how many values were read and how many pieces of advice there are.

## 3. Board

Captures: `board-*.png`, `state-board-free-slot-*.png`, `state-board-watch-*.png`, `state-standard-user-board-*.png`.

| ID | Element | What it is | Owner |
| --- | --- | --- | --- |
| BD-1 | Rescan | As OV-1 | §35 |
| BD-2 | Diagram | A schematic of the slots and connectors the firmware reports: the processor socket, each memory slot, each M.2 slot, each PCIe slot, each SATA port and the wireless card. Fixed blocks (rear ports, chipset) are drawn unlabelled as parts and are not selectable | §35 |
| BD-3 | Part | A box with the slot's name and what is in it. Fitted, free and needs-attention parts differ by fill, by outline style (free is dashed) and by the words in the inspector, never by colour alone | §35 |
| BD-4 | Selection | The selected part has the accent outline. One part is always selected; the first fitted memory slot at start | §35 |
| BD-5 | Honesty line | "A diagram of what the firmware reports, not a picture of the board: positions are schematic." Always shown | §35 |
| BD-6 | Legend | Fitted, Free, Needs attention, and "Arrow keys move between parts" | §35 |
| BD-7 | Inspector heading | The slot's name, what is in it, and a state chip: Fitted, Free or Watch | §35 |
| BD-8 | Inspector values | The part's values as name and reading rows; machine values in monospace | §35 |
| BD-9 | Inspector advice | The advice for this part under an "Advice" label, when there is any | §35 |
| BD-10 | Copy | Copies the part's name, state, values and advice as text | §35 |
| BD-11 | Open section | "Open Memory", "Open Storage" and so on: opens the section the part belongs to | §35 |

Keyboard: Tab reaches the diagram, arrow keys move the selection to the nearest part in that direction, and the inspector follows. Status bar: how many slots and connectors, how many fitted, free and to watch.

A machine whose firmware reports no slots (many laptops) shows the memory slots and drives it does report in a single row, with the same inspector. A machine that reports nothing usable shows the SDK's empty state with one sentence saying the firmware gave no slot information, and the other sections are unaffected.

## 4. The seven area sections

Memory, Processor, Motherboard, Storage, Graphics, Devices, and Network and power share one layout. Captures: `memory-*.png`, `processor-*.png`, `motherboard-*.png`, `storage-*.png`, `graphics-*.png`, `devices-*.png`, `network-and-power-*.png`, `state-explain-memory-*.png`.

| ID | Element | What it is | Owner |
| --- | --- | --- | --- |
| AR-1 | Explain | A toggle in the header. On, each value that has an explanation shows one plain line under it saying what it means and whether it matters. It is the same setting as SE-6 | §34 |
| AR-2 | Copy | Copies the whole section as text: group, name, reading | §34 |
| AR-3 | Advice banner | The advice that belongs to this section, above the values: a title, a sentence, the specification to buy in monospace where there is one, and Copy specification. A warning banner (drive health) is drawn in the warning tokens with a warning icon | §34 |
| AR-4 | Group | A titled box of rows, one per device or topic (a memory module, a drive, "Cache") | §34 |
| AR-5 | Row | A name on the left and its reading on the right. Machine values (part numbers, serial numbers, device IDs, versions, addresses) are monospace, selectable and copyable | §34 |
| AR-6 | Group chip | A state chip in a group's heading where the group has a state: a drive's health as Good, Watch or "Health not read" | §34 |
| AR-7 | Memory slots row | On Memory only: one card per slot in firmware order, showing the slot name, the size or "Empty", a line of detail, and a Fitted or Free chip. Free slots have a dashed outline | §34 |

What each section holds:

| Section | Banners | Groups |
| --- | --- | --- |
| Memory | Memory advice | Summary (fitted, type, slots, running speed, board maximum), then one group per fitted module (size, maker, part number, speed, voltage, serial number) |
| Processor | none | Processor (model, socket, cores and threads, family model stepping, microcode), Cache (levels 1 to 3), Features (instruction sets, virtualisation, supported memory) |
| Motherboard | Windows 11 readiness | Board (maker, model, version, chassis), BIOS (vendor, version, date, mode), Security (TPM, Secure Boot), Firmware tables (ACPI tables, SMBIOS version) |
| Storage | Drive health, storage advice | One group per drive (slot or port, capacity, health, power-on time, temperature, firmware), Free connections |
| Graphics | none | One group per adapter (memory, slot, driver, device ID), one per display (connection, native mode, size, made, serial number) |
| Devices | none | PCI (location, name and IDs), USB (port, name, IDs and speed) |
| Network and power | none | One group per adapter (state, MAC address), Battery (state, and on a laptop design capacity, full charge capacity, wear and cycle count) |

Status bar: how many values the section holds, and "explanations shown" when Explain is on.

## 5. Snapshots

Captures: `snapshots-*.png`, `state-no-snapshots-*.png`, `state-delete-confirmation-*.png`, `state-compare-*.png`.

| ID | Element | What it is | Owner |
| --- | --- | --- | --- |
| SN-1 | Open folder | Opens the snapshot folder in Explorer | §37 |
| SN-2 | Compare selected | Opens the compare view for the two selected snapshots; unavailable, with a tooltip saying why, unless exactly two are selected | §37 |
| SN-3 | Take snapshot | The primary action, as OV-3 | §37 |
| SN-4 | List | One row per snapshot, newest last: a checkbox, the date and time taken, its note, its size, and Delete. "Select two to compare" in the heading | §37 |
| SN-5 | Selection | Selecting a third snapshot drops the older of the two already selected | §37 |
| SN-6 | Delete | Opens the confirmation S-4 for that snapshot | §37 |
| SN-7 | Folder line | Where snapshots are kept and that they stay on this computer | §37 |
| SN-8 | Empty state | S-3 | §37 |
| CP-1 | Back to snapshots | Returns to the list with the selection kept | §38 |
| CP-2 | Export differences | Writes the differences as a file (X-5) | §38 |
| CP-3 | Summary | The two dates, how many values changed and how many are the same, and a chip when a change needs attention | §38 |
| CP-4 | Differences | One row per changed value: area, value, the old reading struck through, the new reading in bold, and a chip: Watch, Changed or Expected | §38 |

Status bar: how many snapshots and how many are selected; in compare, how many differences and how many values are unchanged.

## 6. Beep codes

Captures: `beep-codes-*.png`, `state-beep-all-makers-*.png`, `state-beep-no-match-*.png`.

| ID | Element | What it is | Owner |
| --- | --- | --- | --- |
| BC-1 | Search | A search box: narrows the list to codes whose pattern or meaning matches as the user types. Ctrl+F focuses it | §39 |
| BC-2 | Maker filter | All, AMI, AST, Award, Compaq, Dell, IBM, Phoenix. The maker this computer's BIOS reports is marked "(this computer)" and is selected at start; All when it is not one of the seven | §39 |
| BC-3 | List | Pattern, meaning and BIOS maker, one row per code | §39 |
| BC-4 | Meaning panel | For the selected code: the maker, the pattern, the meaning, "What to try" as numbered steps, and Copy | §39 |
| BC-5 | Nothing selected | The panel explains what beep codes are and names this computer's BIOS maker | §39 |
| BC-6 | No match | S-5 | §39 |

Status bar: how many codes are shown out of the total, and which maker.

## 7. Activity, Settings and About

Captures: `activity-*.png`, `settings-general-*.png`, `settings-busview-*.png`, `settings-logging-*.png`, `about-*.png`.

| ID | Element | What it is | Owner |
| --- | --- | --- | --- |
| AC-1 | Activity list | What Busview did, newest first: the time in monospace, the action, its detail, and an outcome chip (Done, Started, Skipped, Refused, Failed) | §40 |
| AC-2 | Open log file, Copy | Opens the log file; copies the list as text | §40 |
| SE-1 | Pages | General, Busview, Logging. General and Logging are the SDK framework's pages | §41 |
| SE-2 | Theme | Follow system, Light, Dark | §41 |
| SE-3 | Density | Compact, Normal, Spacious | §41 |
| SE-4 | Language | The current language and Change | §41 |
| SE-5 | Log | Keep a log file, and the log folder with Open | §41 |
| SE-6 | Explain each value | The same setting as AR-1 | §41 |
| SE-7 | Sizes | GB, as drive makers count, or GiB, as Windows counts | §41 |
| SE-8 | Snapshot folder | The folder and Change | §41 |
| SE-9 | Hide serial numbers in exports | On by default (X-6) | §41 |
| SE-10 | Compatibility database | Its version, what it holds, and Check for update | §43 |
| AB-1 | About | The SDK framework's About page from Busview's descriptor: icon, name, tagline, version, database version, running as, "Kernel driver: none", website, source, and where crash reports are written | §41 |

Settings are saved as they are changed, and the status bar says so.

## 8. States

| ID | State | What the window shows | Owner |
| --- | --- | --- | --- |
| S-1 | First scan | Over the content: Busview's icon, "Reading this computer", a progress bar, what is being read now, and "Nothing is changed and nothing leaves this computer." The status bar counts values read. The sidebar stays usable | §32 |
| S-2 | Standard user | Drive health is not read. Storage shows a refusal in place of the health banner: what was not read, why, that the rest of the page is complete, and Restart as administrator. Health, power-on time and temperature rows are absent, the drive chips say "Health not read", the Storage and Board attention dots are absent, and the drive health advice row says "Needs administrator" | §36 |
| S-3 | No snapshots | The SDK's empty state: an icon, "No snapshots yet", what a snapshot is for, and Take snapshot | §37 |
| S-4 | Delete confirmation | A dialog naming the snapshot by date, what is deleted (1 file, its size, its note), "This cannot be undone." in bold, and Cancel and Delete snapshot. Delete snapshot is the destructive button; Cancel has the focus | §37 |
| S-5 | No match | An icon, the search text quoted, one sentence of help, and Clear search | §39 |
| S-6 | Scan failed in part | A reader that fails shows one sentence in its section naming what could not be read and why, and every other section is complete. It is recorded in Activity as Failed or Refused | §34 |
| S-7 | Database missing or damaged | Advice, explanations and beep codes need the database. Their places show one sentence naming the file and what to do; the inventory itself still works | §33 |

## 9. Rules for every screen

| ID | Rule | Owner |
| --- | --- | --- |
| X-1 | Every action is reachable by keyboard, tab order follows visual order, and focus is always visible | §42 |
| X-2 | Every control has an accessible name and exposes UI Automation; status changes are announced | §42 |
| X-3 | State is never colour alone: every chip has an icon and a word | §42 |
| X-4 | Text that is cut off ends in an ellipsis and has a tooltip with the full text | §42 |
| X-5 | Report, snapshot and differences files are written atomically, read back, and the status bar and Activity say where the file went | §30 |
| X-6 | With SE-9 on, serial numbers, MAC addresses, the computer name and the system UUID are replaced in every exported file | §30 |
| X-7 | Every string comes from the language pack. No user-facing text is typed into the code | §44 |
| X-8 | The UI thread never blocks: scanning, exporting and comparing run off it and report progress | §32 |
| X-9 | Nothing invented: a value the machine did not report is absent, and a reading known to be unreliable (the firmware's memory maximum) says so in its explanation | §34 |
| X-10 | Light, dark and high contrast all work, at 100, 125, 150 and 200 percent | §42 |

## 10. Not in this design

These are decided as later work and have no control in version 1: live sensors (temperatures, fans, voltages, which need a kernel driver), memory timings and XMP or EXPO profiles, processor upgrade suggestions, maker-tested memory kits, opt-in reports from users, the used-PC report, hand-off to retailers' and makers' finders, and WinPE support.
