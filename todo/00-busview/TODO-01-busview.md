---
schema_version: 1
id: busview
domain: 00-busview
status: active
title: "TODO-01 -- Busview"
---

# TODO-01 -- Busview

> **Goal:** Busview version 1 ships as one standalone Windows tool of the Resolute suite: it reads the hardware of a real computer from user mode with no kernel driver, gives memory, storage, drive health and Windows 11 advice from what it read, saves and compares snapshots, explains every BIOS beep code, and its window matches `design/SPEC.md` 1:1.

> **Current state:** Measured 2026-11-17. No C++ exists. The repository holds the decisions in `README.md`, the identity under `brand/` (built by `python brand/build.py`), `DESIGN.md`, the interface contract `design/SPEC.md` with the working design `design/busview-interface.html` and 54 captures under `design/captures/`, the AutoIt beep-code source under `reference/beepcodes-au3/` (`src/BiosCodes.au3`, `src/Includes/Localization.au3`, and three language packs), the SDK pin `sdk.json` with `scripts/sdk.ps1`, and the Conclave kits. Resolute-SDK at the pinned commit provides the toolchain under `sdk/reskit/`, the CMake policies under `sdk/cmake/` and, in `sdk/shared/resolute-ui/`, these controls only: `Sidebar`, `Toolbar`, `PopupMenu`, `StatusBar`, `ListView`, `ContentView`, with `Theme`, `Typography`, `Dpi`, `Animation`, `LucideIcons` and `RenderContext`. It has no tool window host, button, tabs, text box, toggle, segmented control, dialog, tooltip, chip or UI Automation yet, and its framework (settings, About, logging, language packs, update, elevation) is planned and not built. Every section here that needs one of those carries the Need `sdk-framework` and waits for it.

## Inputs

- `README.md`: what Busview is, what version 1 holds, and the settled tech stack.
- `design/SPEC.md`: the interface contract. Its Owner column names the section here that builds each control. `design/busview-interface.html` and `design/captures/` are the reference it was written from.
- `DESIGN.md`: the identity and the window's sections, and `sdk/DESIGN.md`, the suite's contract every surface answers to.
- `reference/beepcodes-au3/`: the AutoIt BiosCodes source and language packs. The beep texts are the 246 indexed entries in `src/Includes/Localization.au3:119-395`, and `src/BiosCodes.au3:783-1263` maps each manufacturer's pattern to an entry: 177 codes across AMI (15), AST (19), Award (5), Compaq (7), Dell (7), IBM (10) and Phoenix (114).
- `sdk/cmake/ResoluteSdk.cmake` and `sdk/toolchain.json`: how a tool builds on the SDK.

## Outcome

- `Busview.exe` is one statically linked executable that reads a real computer's memory, processor, board, firmware, drives, graphics, displays, devices, network adapters and battery from user mode, and shows nothing it did not read.
- From that reading and the shipped database it answers four questions with a verdict, a reason and, for memory and storage, the specification to buy: can memory be added, can a drive be added, is a drive wearing out, is the computer ready for Windows 11.
- A snapshot is one versioned JSON file, two snapshots compare to a list of changed values, and a report exports with serial numbers hidden by default.
- All 177 beep codes of the AutoIt original are found by maker and by search, starting on this computer's BIOS maker.
- The window of `design/SPEC.md` works in light, dark and high contrast at every scale, by keyboard alone, and ships as a portable zip and an installer.

**Adjacency:** list=applicable @ D00 T01 §39; document=applicable @ D00 T01 §30; settings=applicable @ D00 T01 §41; reporting=applicable @ D00 T01 §30; notifications=not-applicable (the tool reports on its own surface and in its log and sends nothing to anyone); permissions=applicable @ D00 T01 §36; audit=applicable @ D00 T01 §40; exchange=applicable @ D00 T01 §26; reverse=applicable @ D00 T01 §37

**Adjacency rationale:** The list is the beep-code search and the section list itself, where a person finds a value without knowing its name. The document is the exported report, which is also the reporting surface. Permissions are the standard-user case: drive health needs administrator rights and the refusal says so. Audit is the Activity section, fed by the same record as the log. Exchange is the snapshot file, which leaves the tool and comes back for a comparison. Reverse: Busview changes nothing on the computer; the only things it creates are snapshot and report files, a snapshot is removed by Delete, and Delete has no undo, which the confirmation states before the user commits.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Build Skeleton on the Pinned SDK | -- | [ ] |
| 2 | §2 | Gates and Continuous Integration | §1 | [ ] |
| 3 | §3 | Crash Handler With a Local Minidump | §1 | [ ] |
| 4 | §4 | Bounds-Checked Reader for Firmware Bytes | §1 | [ ] |
| 5 | §5 | Graphics Vendor Library Call Proof | §1 | [ ] |
| 6 | §6 | Inventory Model and Scan Runner | §1 | [ ] |
| 7 | §7 | SMBIOS Table Access and Structure Walk | §4, §6 | [ ] |
| 8 | §8 | Board, BIOS, System and Chassis Values | §7 | [ ] |
| 9 | §9 | Memory Slots and Modules | §7 | [ ] |
| 10 | §10 | Processor Values From CPUID | §6 | [ ] |
| 11 | §11 | Firmware Tables, TPM and Secure Boot | §4, §6 | [ ] |
| 12 | §12 | Drives and Their Connections | §6 | [ ] |
| 13 | §13 | Drive Health With Administrator Rights | §12 | [ ] |
| 14 | §14 | Graphics Adapters and Vendor Detail | §5, §6 | [ ] |
| 15 | §15 | Displays From EDID | §4, §6 | [ ] |
| 16 | §16 | PCI and USB Devices | §6 | [ ] |
| 17 | §17 | Network Adapters and Battery | §6 | [ ] |
| 18 | §18 | Slots and Connectors Model | §9, §12, §14, §16 | [ ] |
| 19 | §19 | Compatibility Database Build | §1 | [ ] |
| 20 | §20 | Database Reader in the Tool | §19 | [ ] |
| 21 | §21 | Processor and Board Specification Data | §19 | [ ] |
| 22 | §22 | Memory Advice | §9, §10, §20, §21 | [ ] |
| 23 | §23 | Storage Advice | §18, §20 | [ ] |
| 24 | §24 | Drive Health Advice | §13 | [ ] |
| 25 | §25 | Windows 11 Readiness | §10, §11, §12, §20 | [ ] |
| 26 | §26 | Snapshot File Format and Writer | §6 | [ ] |
| 27 | §27 | Snapshot Compare Engine | §26 | [ ] |
| 28 | §28 | Beep Code Data in the Database | §19 | [ ] |
| 29 | §29 | Beep Code Lookup and Search | §20, §28 | [ ] |
| 30 | §30 | Report Export and Privacy Masking | §26 | [ ] |
| 31 | §31 | Headless Scan Command | §25, §30 | [ ] |
| 32 | §32 | Window Shell, Sidebar and First Scan | §6 | [ ] |
| 33 | §33 | Overview Section | §22, §23, §24, §25, §32 | [ ] |
| 34 | §34 | Area Sections With Explain and Copy | §22, §23, §32 | [ ] |
| 35 | §35 | Board Section Diagram and Inspector | §18, §32 | [ ] |
| 36 | §36 | Standard User Refusal and Restart | §13, §34 | [ ] |
| 37 | §37 | Snapshots Section | §26, §32 | [ ] |
| 38 | §38 | Compare View | §27, §37 | [ ] |
| 39 | §39 | Beep Codes Section | §29, §32 | [ ] |
| 40 | §40 | Activity Section | §32 | [ ] |
| 41 | §41 | Settings and About Sections | §32 | [ ] |
| 42 | §42 | Accessibility and Fidelity Pass | §33, §35, §36, §38, §39, §40, §41 | [ ] |
| 43 | §43 | Database Update Check | §20 | [ ] |
| 44 | §44 | Language Pack and Strings | §41 | [ ] |
| 45 | §45 | Portable Zip and Installer | §31, §42 | [ ] |
| 46 | §46 | User Guide and Release Documents | §45 | [ ] |
| 47 | §47 | Code Signing of Releases | §45 | [ ] |
| 48 | §48 | Name Clearance Before the First Release | -- | [ ] |

## 1. Build Skeleton on the Pinned SDK

The repository builds an empty Busview window against the pinned SDK with one command, so every later section has somewhere to land and the standalone build is true from the first commit.

**Phase:** 0
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Write `CMakeLists.txt`, `CMakePresets.json` and `scripts/build.ps1` on the SDK's shape. Done when: `pwsh scripts/build.ps1 -Config Debug` produces `Bin\Debug\Busview.exe`.
2. Write `src/main.cpp`, `resources/app.manifest` and `resources/resource.rc` with the icon from `brand/`. Done when: the executable starts and shows an empty window with Busview's icon.

- [ ] Write the root `CMakeLists.txt`: `project(Busview LANGUAGES C CXX RC)`, `include(sdk/cmake/ResoluteSdk.cmake)`, `resolute_sdk_add_libraries()`, the `Busview` target with `resolute_set_warnings` linking `ResoluteUI_static` and `Lucide_static`. Done when: `sdk\reskit\cmake\bin\cmake.exe --preset debug` configures. Cheaper substitute: retyping the language standard, definitions or link flags here, which the SDK owns.
- [ ] Write `CMakePresets.json` with `debug` and `release` presets naming the compilers under `sdk/reskit/llvm-mingw/bin/` and Ninja under `sdk/reskit/ninja/`. Done when: both presets configure from an empty `build/`. Cheaper substitute: compilers found on `PATH`, which makes two machines build differently.
- [ ] Write `scripts/build.ps1` (`-Config Debug|Release`) that runs `scripts/sdk.ps1 -Check` first. Done when: with `sdk/` absent it exits 1 naming `pwsh scripts/sdk.ps1` as the fix.
- [ ] Write `src/main.cpp` opening one empty top-level window through `sdk/shared/resolute-ui`, with `resources/app.manifest` declaring per-monitor DPI v2, the Windows 10 1809 floor and `asInvoker`. Done when: `Bin\Debug\Busview.exe` shows a window that re-lays out when dragged between monitors of different scale.
- [ ] Embed `brand/busview.ico` through `resources/resource.rc` with the version resource. Done when: the executable shows Busview's icon in Explorer and on the taskbar at 100 and 150 percent.
- [ ] Add `tests/CMakeLists.txt` with Catch2 v3 fetched by `FetchContent` at a pinned commit and one case in `tests/smoke_test.cpp`. Done when: `sdk\reskit\cmake\bin\ctest.exe --preset debug` passes with one case.
- [ ] Split the code into a static library target `busview_core` (everything under `src/core`, `src/read`, `src/db`, `src/advice`, `src/snapshot`, `src/beep`) that the executable and the tests link. Done when: the test binary links `busview_core` and no window code.
- [ ] Prove the executable is standalone: copy `Bin\Release\Busview.exe` alone to an empty folder and start it. Done when: it starts, and `sdk\reskit\llvm-mingw\bin\llvm-readobj.exe --coff-imports` lists only Windows system libraries.
- [ ] Commit: `build: an empty window on the pinned SDK, standalone`

**Test checkpoint:** `pwsh scripts/build.ps1 -Config Release` ends with `Busview` built, `sdk\reskit\cmake\bin\ctest.exe --preset debug` passes, and the import table of `Bin\Release\Busview.exe` names no `libc++` or `libunwind` library.

## 2. Gates and Continuous Integration

One command runs every check the repository has, and every push runs it. It comes second so that each later section lands under the gates.

**Phase:** 0
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Write `scripts/check-all.ps1` running the build, the tests and the plan gates in turn. Done when: it ends `check-all: <n> gate(s) ok` and exits 1 naming the first gate that fails.
2. Write `.github/workflows/gates.yml` running it on `windows-latest`. Done when: the run for the commit is green.

- [ ] Write `scripts/check-all.ps1`: `scripts/sdk.ps1 -Check`, `scripts/build.ps1 -Config Release`, `ctest --preset debug`, `python brand/build.py --check`, `python scripts/todo-graph.py validate`, `python scripts/todo-graph.py plan --check` and `node scripts/verify-agent-tiers.mjs`. Done when: each gate prints one line and the script ends `check-all: 7 gate(s) ok`.
- [ ] Make a failing gate stop the run with its name and its last lines. Done when: a deliberately broken test makes `scripts/check-all.ps1` exit 1 naming `tests`. Cheaper substitute: continuing after a failure, which buries the first cause.
- [ ] Write `.github/workflows/gates.yml`: check out, `pwsh scripts/sdk.ps1`, the SDK's `scripts/bootstrap.ps1` for the toolchain with its download cached by `sdk/toolchain.json`'s hash, then `pwsh scripts/check-all.ps1`. Done when: the workflow run for the commit is green on GitHub.
- [ ] Add `scripts/hardening-check.py` to the gates against `Bin\Release\Busview.exe`. Done when: the gate passes and fails when the executable is linked without `/DYNAMICBASE`. Cheaper substitute: trusting the link flags without reading the built file.
- [ ] Commit: `gates: one command for every check, run on every push`

**Test checkpoint:** `pwsh scripts/check-all.ps1` ends `check-all: 8 gate(s) ok`, and exits 1 naming the gate when one test is made to fail.

## 3. Crash Handler With a Local Minidump

The README requires a crash handler from the start. A crash writes a minidump and a short text report beside the program and shows a clear message. Nothing is sent anywhere.

**Phase:** 0
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Implement `src/core/CrashHandler.cpp` installing an unhandled-exception filter that writes the dump and the report. Done when: a forced access violation leaves both files.
2. Prove it with a child-process test in `tests/crash_test.cpp`. Done when: the test finds the files and the child's whole process tree is gone.

- [ ] Implement `CrashHandler::Install()` in `src/core/CrashHandler.cpp` with `SetUnhandledExceptionFilter` and `MiniDumpWriteDump`, writing `Busview-crash-<time>.dmp` and `.txt` to `%LOCALAPPDATA%\Busview\Crashes`. Done when: a forced crash leaves both files and the text names the exception code, the module and Busview's version. Cheaper substitute: a message box with no file, which leaves nothing to diagnose.
- [ ] Add a hidden `--crash-test` argument in `src/main.cpp` that raises an access violation after the handler is installed. Done when: `Busview.exe --crash-test` exits non-zero and leaves one dump.
- [ ] Show one message after the files are written: what happened, where the two files are, and that nothing was sent. Done when: the text matches the wording in `resources/strings/en.json`.
- [ ] Write `tests/crash_test.cpp` starting `Busview.exe --crash-test` in a job object with a 30-second limit and ending the whole job on timeout and teardown. Done when: `ctest --preset debug -L crash` passes, and no `Busview.exe` process is left after a forced timeout. Cheaper substitute: ending only the direct child, which leaves its children running.
- [ ] Keep at most ten crash file pairs, removing the oldest. Done when: a test with twelve fixture pairs leaves the ten newest.
- [ ] Commit: `core: a crash writes a local minidump and says where it is`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L crash` passes: the dump and the report exist after a forced crash, and the test fails when the filter is not installed.

## 4. Bounds-Checked Reader for Firmware Bytes

Firmware tables, EDID blocks and device descriptors are untrusted input. Every parser in Busview reads through one checked reader, so a short, truncated or lying table is refused by name and never read past its end.

**Phase:** 0
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Implement `ByteReader` in `src/core/ByteReader.h`. Done when: every read past the end returns an error and no read touches memory outside the span.
2. Cover it in `tests/bytereader_test.cpp` under AddressSanitizer. Done when: the `asan` preset passes on every malformed input.

- [ ] Implement `ByteReader` over `std::span<const std::byte>` in `src/core/ByteReader.h` with `u8`, `u16`, `u32`, `u64`, `bytes(n)`, `sub(offset, n)` and `cstring()` each returning `std::expected<T, ReadError>`. Done when: reading two bytes from a one-byte span returns `ReadError::PastEnd` with the offset.
- [ ] Add `StringTable` in `src/core/ByteReader.h` for the double-null string sets SMBIOS uses, refusing an index past the last string. Done when: index 3 of a two-string set returns an error, and index 0 returns "no string".
- [ ] Add an `asan` preset to `CMakePresets.json` on the SDK's shape. Done when: `sdk\reskit\cmake\bin\ctest.exe --preset asan -L bytereader` runs the suite under AddressSanitizer.
- [ ] Cover truncated, empty, overlapping and maximum-length inputs in `tests/bytereader_test.cpp`. Done when: the suite passes under `asan`, and fails when one bounds check is removed from `ByteReader`. Cheaper substitute: testing only well-formed input, which proves nothing about the refusals.
- [ ] Commit: `core: one bounds-checked reader for every untrusted table`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset asan -L bytereader` passes, and fails when a bounds check in `src/core/ByteReader.h` is removed.

## 5. Graphics Vendor Library Call Proof

The tech stack reaches NVIDIA and AMD detail by loading the DLLs the graphics driver installs and calling their C interfaces at run time. That is unproven on llvm-mingw and could reopen the toolchain choice, so it is proven before any reader depends on it.

**Phase:** 0
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Write `src/read/VendorLibrary.cpp`, a loader that opens a driver DLL by name from the system directory only. Done when: a missing DLL returns "not installed" and never an error.
2. Call one function of each vendor through it. Done when: the result is recorded in `docs/decisions/graphics-vendor-libraries.md`.

- [ ] Implement `VendorLibrary::Open(name)` in `src/read/VendorLibrary.cpp` with `LoadLibraryExW` and `LOAD_LIBRARY_SEARCH_SYSTEM32`, never the current directory. Done when: a DLL of the same name planted beside the executable is not loaded, asserted in `tests/vendorlibrary_test.cpp`. Cheaper substitute: a plain `LoadLibrary`, which loads a planted file.
- [ ] Call NVAPI through `nvapi64.dll`'s `nvapi_QueryInterface` for `NvAPI_Initialize` and the interface version string. Done when: on a machine with an NVIDIA driver the version string is read, and on one without it the result is "not installed".
- [ ] Call AMD's ADL through `atiadlxx.dll` (`ADL2_Main_Control_Create`, the adapter count, `ADL2_Main_Control_Destroy`). Done when: on a machine with an AMD driver the adapter count is read, and without it the result is "not installed".
- [ ] Record in `docs/decisions/graphics-vendor-libraries.md` what was called, on which driver versions, what a machine without the driver returns, and the verdict: runtime loading works on llvm-mingw, or what must change. Done when: the file states the verdict with the evidence. Cheaper substitute: assuming it works because it compiles.
- [ ] Commit: `read: graphics vendor libraries load and answer from llvm-mingw`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L vendorlibrary` passes: the planted-DLL case is refused and a missing library reports "not installed", and `docs/decisions/graphics-vendor-libraries.md` states the verdict.

## 6. Inventory Model and Scan Runner

Every reader fills one model: areas, groups and values, each value with its reading, whether it is a machine value, where it came from and the key of its explanation. The scan runner calls the readers off the UI thread, reports progress, and records each action once for both the log and the Activity section.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Define the model in `src/core/Inventory.h`. Done when: a test builds an inventory of two areas and reads every value back.
2. Implement `ScanRunner` in `src/core/ScanRunner.cpp`. Done when: two fake readers run, one failing, and the inventory holds the first's values and the second's failure.

- [ ] Define `Value` (key, reading, `machine` flag, `source`, `explainKey`), `Group`, `Area` and `Inventory` in `src/core/Inventory.h`, with the seven areas of `design/SPEC.md` section 4 as an enum. Done when: `tests/inventory_test.cpp` builds and reads back two areas.
- [ ] Define the `Reader` interface in `src/core/Reader.h`: a name, the area it fills, whether it needs administrator rights, and `Read(Inventory&) -> ReadOutcome` (done, skipped, refused or failed, each with a reason). Done when: a fake reader of each outcome compiles against it.
- [ ] Implement `ScanRunner::Run()` in `src/core/ScanRunner.cpp` on a worker thread, calling each reader in a fixed order and reporting `(done, total, readerName)` through a callback. Done when: a test sees one progress call per reader in order.
- [ ] Keep going when a reader fails or throws: record the outcome and the reason on its area. Done when: a throwing fake reader leaves the other areas complete and its own area marked failed with the reason (`design/SPEC.md` S-6). Cheaper substitute: aborting the scan, which loses every other area.
- [ ] Implement `ActivityLog` in `src/core/Activity.cpp`: one record (time, action, detail, outcome) written by one call and read by both the log file and the Activity list. Done when: a test shows one scan of three readers produces exactly five records: started, three readers, finished.
- [ ] Add the English strings for area names, group names and explanations as keyed entries in `resources/strings/en.json`, embedded in the executable. Done when: a test fails for a key the model uses that the file lacks.
- [ ] Commit: `core: the inventory model and the scan that fills it`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L inventory` passes, and fails when `ScanRunner` stops at the first failing reader.

## 7. SMBIOS Table Access and Structure Walk

SMBIOS is the source for the board, the BIOS and the memory slots. This section reads the raw table and walks its structures through the checked reader; the sections after it decode each type.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Read the table with `GetSystemFirmwareTable('RSMB')` in `src/read/smbios/SmbiosTable.cpp`. Done when: the real machine's table is returned with its version.
2. Walk it in `src/read/smbios/SmbiosWalk.cpp`. Done when: each structure's type, handle, formatted area and strings are returned, and a malformed table is refused by offset.

- [ ] Implement `SmbiosTable::ReadSystem()` in `src/read/smbios/SmbiosTable.cpp` and `SmbiosTable::FromBytes()` for fixtures. Done when: on the real machine the version and length are non-zero.
- [ ] Implement `SmbiosWalk` in `src/read/smbios/SmbiosWalk.cpp` over `ByteReader`: header, formatted area, string set, stopping at type 127. Done when: a fixture of three structures yields three, with their strings.
- [ ] Refuse a structure whose length is under four, runs past the table, or whose string set is unterminated, naming the offset. Done when: three malformed fixtures each return an error with the offset and no partial structure. Cheaper substitute: skipping the bad structure silently, which hides a lying table.
- [ ] Commit a real table as `tests/fixtures/smbios/desktop-b550.bin` with every serial number, UUID and asset tag overwritten with zeros or `X`. Done when: `tests/smbios_fixture_test.cpp` asserts no serial-number string in the fixture holds anything but `0` or `X`.
- [ ] Add laptop and brand-name desktop fixtures built in code in `tests/fixtures/smbios/Builders.h` (empty part numbers, a wrong maximum capacity, soldered memory). Done when: each builder produces a table the walk accepts.
- [ ] Commit: `read: the SMBIOS table and a checked walk of its structures`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset asan -L smbios` passes for the real fixture and every malformed one, and fails when the length check is removed.

## 8. Board, BIOS, System and Chassis Values

The Motherboard section's Board and BIOS groups, and the machine line on Overview, come from SMBIOS types 0, 1, 2 and 3.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Decode types 0 to 3 in `src/read/smbios/BoardReader.cpp`. Done when: the fixture returns the board maker, model, BIOS vendor, version and date.
2. Register the reader with the scan. Done when: a scan fills the Motherboard area's Board and BIOS groups.

- [ ] Decode type 0 (BIOS vendor, version, release date, ROM size, UEFI flag) in `src/read/smbios/BoardReader.cpp`. Done when: the desktop fixture returns `American Megatrends Inc.` and its version.
- [ ] Decode types 1 and 2 (system and board maker, product, version) and type 3 (chassis type as a word). Done when: chassis type 3 reads "Desktop" and 10 reads "Notebook", from the table in the SMBIOS specification named in a comment.
- [ ] Treat the filler strings vendors leave (`To Be Filled By O.E.M.`, `Default string`, `System Product Name`, empty) as absent. Done when: a fixture with each returns no value for that field (`design/SPEC.md` X-9). Cheaper substitute: showing the filler text as if it were a model.
- [ ] Read the computer name and the Windows edition and version in `src/read/SystemReader.cpp`. Done when: the values match `GetComputerNameExW` and the registry's `CurrentVersion` on the test machine.
- [ ] Cover it in `tests/boardreader_test.cpp`. Done when: `ctest --preset debug -L board` passes, and fails when the chassis table is shifted by one.
- [ ] Commit: `read: board, BIOS, system and chassis from SMBIOS`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L board` passes for the desktop and laptop fixtures, and filler strings never reach the inventory.

## 9. Memory Slots and Modules

The first use case. SMBIOS types 16 and 17 give the slot count, which slots are empty, and each fitted module's size, type, form factor, speed, voltage, maker and part number.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Decode types 16 and 17 in `src/read/smbios/MemoryReader.cpp`. Done when: the fixture returns four slots, two fitted.
2. Fill the Memory area. Done when: the Summary group and one group per fitted module match `design/SPEC.md` section 4.

- [ ] Decode type 16 (maximum capacity, including the extended field above 2 TB, and the slot count) in `src/read/smbios/MemoryReader.cpp`. Done when: the fixture returns 128 GB and four slots.
- [ ] Decode type 17 per slot: locator, size (including the extended size field), memory type, form factor, configured speed, configured voltage, manufacturer and part number. Done when: slot `DIMM_A2` of the fixture returns 8 GB, DDR4, DIMM, 3200 MT/s and 1.35 V.
- [ ] Mark a slot with size zero as empty and keep its locator. Done when: the fixture's `DIMM_A1` is empty and present.
- [ ] Translate JEDEC manufacturer codes to names from a table in `data/memory-makers.csv`, and trim the padding vendors put in part numbers. Done when: a module reporting a JEDEC code returns its maker's name, and an unknown code returns the code itself.
- [ ] Detect soldered memory from the form factor and the locator. Done when: the laptop fixture's row-of-chips module is marked soldered and an unknown case is marked "may be soldered", never guessed.
- [ ] Fill the Summary group: fitted total, type and form factor, slots used of total, running speed, board maximum with the explanation key that says vendors often fill it in wrongly. Done when: the group matches the design's rows for the fixture.
- [ ] Cover it in `tests/memoryreader_test.cpp` including the fixtures with empty part numbers and a wrong maximum. Done when: `ctest --preset debug -L memory` passes, and fails when the extended size field is ignored.
- [ ] Commit: `read: memory slots and modules from SMBIOS`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L memory` passes for the desktop, laptop and brand-name fixtures.

## 10. Processor Values From CPUID

The Processor section comes from the `CPUID` instruction: the model, family, features, cache and core layout.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Wrap `CPUID` behind an interface in `src/read/cpu/Cpuid.h` so tests can supply leaves. Done when: a fixture of recorded leaves decodes without the instruction.
2. Decode it in `src/read/cpu/ProcessorReader.cpp`. Done when: an AMD and an Intel fixture return their model, cores and cache.

- [ ] Define `CpuidSource` in `src/read/cpu/Cpuid.h` with a real implementation using `__cpuidex` and a fixture implementation reading recorded leaves. Done when: both compile and the real one returns a non-empty vendor string.
- [ ] Decode the brand string, vendor, family, model and stepping in `src/read/cpu/ProcessorReader.cpp`. Done when: the AMD fixture returns `AMD Ryzen 5 5600X 6-Core Processor`, family 19h, model 21h.
- [ ] Decode cores, threads and cache levels from leaf 4 and `0x8000001D`, and the logical layout from `GetLogicalProcessorInformationEx`. Done when: the fixture returns 6 cores, 12 threads and a 32 MB level 3 cache.
- [ ] Decode the feature flags the design lists (SSE4.2, AVX, AVX2, AVX-512, AES, SHA, FMA3, virtualisation). Done when: each flag in the fixtures reads as present or absent correctly.
- [ ] Read the socket from SMBIOS type 4 and the microcode revision from the registry. Done when: the fixture returns `AM4`.
- [ ] Record the leaves of the development machine as `tests/fixtures/cpuid/` files with a small recorder behind `Busview.exe --dump-cpuid`. Done when: the recorded file decodes to the same values as the live read.
- [ ] Cover it in `tests/processor_test.cpp`. Done when: `ctest --preset debug -L processor` passes for one AMD and one Intel fixture, and fails when the family decode drops the extended family.
- [ ] Commit: `read: the processor from CPUID`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L processor` passes for both fixtures.

## 11. Firmware Tables, TPM and Secure Boot

The Motherboard section's Security and Firmware tables groups, and three of the Windows 11 checks: the list of ACPI tables, the TPM's presence and version, UEFI mode and Secure Boot.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Enumerate ACPI tables in `src/read/FirmwareReader.cpp`. Done when: the real machine returns its table signatures.
2. Read TPM and Secure Boot state in `src/read/SecurityReader.cpp`. Done when: both read without administrator rights or say why not.

- [ ] Enumerate ACPI table signatures with `EnumSystemFirmwareTables('ACPI')` in `src/read/FirmwareReader.cpp`, counting repeated signatures. Done when: the result lists `FACP` once and `SSDT` with its count.
- [ ] Read the TPM's presence and specification version through `Tbsi_GetDeviceInfo` in `src/read/SecurityReader.cpp`. Done when: a machine with TPM 2.0 returns "2.0, on" and one without returns "Not present".
- [ ] Read UEFI or legacy mode with `GetFirmwareType` and Secure Boot from the `UEFISecureBootEnabled` registry value, distinguishing off from unsupported. Done when: a legacy-mode fixture returns "Legacy BIOS" and "Not supported".
- [ ] Report a read that Windows refuses as refused with the reason, not as absent. Done when: a fake that returns access denied yields "Not read" with the reason on the value. Cheaper substitute: reporting "Not present", which would fail a Windows 11 check falsely.
- [ ] Cover it in `tests/firmware_test.cpp` behind an interface with fakes. Done when: `ctest --preset debug -L firmware` passes for present, absent and refused.
- [ ] Commit: `read: firmware tables, TPM and Secure Boot`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L firmware` passes, and fails when a refused read is reported as absent.

## 12. Drives and Their Connections

Each drive, its capacity and how it is connected, without administrator rights. Health is the next section.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Enumerate physical drives in `src/read/storage/DriveReader.cpp` with `IOCTL_STORAGE_QUERY_PROPERTY`. Done when: every drive of the test machine is listed with its model and bus type.
2. Fill the Storage area. Done when: one group per drive matches the design's rows that need no rights.

- [ ] Enumerate disk device interfaces with SetupAPI and open each with zero access rights in `src/read/storage/DriveReader.cpp`. Done when: the drives are listed from a standard-user process.
- [ ] Read model, firmware revision, serial number, bus type (NVMe, SATA, USB) and removable flag from `StorageDeviceProperty`, and capacity from `IOCTL_DISK_GET_LENGTH_INFO`. Done when: the values match `Get-PhysicalDisk` on the test machine.
- [ ] Read the negotiated link for NVMe drives (PCIe generation and width) from the device's PCI parent properties. Done when: an NVMe drive returns a value such as "PCIe 3.0 x4", or no value when Windows does not report it.
- [ ] Skip virtual and removable-media devices with no medium, recording why in the outcome. Done when: a card reader with no card adds no drive and one Activity record says it was skipped.
- [ ] Put the drive queries behind `DriveSource` in `src/read/storage/DriveSource.h` with a fake. Done when: `tests/drivereader_test.cpp` runs with three fake drives.
- [ ] Commit: `read: drives and how they are connected`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L drives` passes with the fake source, and a run on the test machine lists the drives `Get-PhysicalDisk` lists.

## 13. Drive Health With Administrator Rights

SMART for SATA drives and the health log for NVMe drives need administrator rights. With them Busview reads health; without them it says exactly what was not read and why.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Read the NVMe health log and SMART attributes in `src/read/storage/HealthReader.cpp`. Done when: an elevated run returns power-on hours and temperature for each drive.
2. Refuse cleanly without rights. Done when: a standard-user run records a refusal naming administrator rights and reads nothing else differently.

- [ ] Read the NVMe SMART/Health log (page 2) with `IOCTL_STORAGE_QUERY_PROPERTY` and `StorageDeviceProtocolSpecificProperty` in `src/read/storage/HealthReader.cpp`. Done when: percentage used, power-on hours, temperature and media errors are returned for an NVMe drive.
- [ ] Read ATA SMART attributes with `IOCTL_ATA_PASS_THROUGH` (SMART READ DATA): reallocated sectors (5), power-on hours (9), temperature (194), pending sectors (197), uncorrectable (198). Done when: the values match `smartctl -A` on the test machine's SATA drive.
- [ ] Parse both through `ByteReader` and refuse a short buffer. Done when: a truncated log fixture returns an error and no values.
- [ ] Return `ReadOutcome::Refused` with "needs administrator rights" when the handle cannot be opened for the pass-through, checked at the action. Done when: the fake source returning access denied yields the refusal and the drive's other values stay (`design/SPEC.md` S-2). Cheaper substitute: reporting health as unknown with no reason.
- [ ] Cover it in `tests/healthreader_test.cpp` with recorded log fixtures under `tests/fixtures/smart/`. Done when: `ctest --preset asan -L health` passes, and fails when attribute 5 is read from the wrong offset.
- [ ] Commit: `read: drive health with administrator rights, and an honest refusal without`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset asan -L health` passes for the NVMe and SATA fixtures, the truncated fixture and the refusal.

## 14. Graphics Adapters and Vendor Detail

Each graphics adapter from DXGI and SetupAPI, with detail from the vendor's driver library where §5 proved it loads.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Enumerate adapters in `src/read/graphics/AdapterReader.cpp`. Done when: each adapter's name, memory and device ID are returned.
2. Add vendor detail through `VendorLibrary`. Done when: a machine with the driver gains its values and one without loses nothing.

- [ ] Enumerate adapters with `IDXGIFactory6::EnumAdapterByGpuPreference`, skipping the software adapter, in `src/read/graphics/AdapterReader.cpp`. Done when: the name, dedicated memory and vendor and device IDs match Device Manager.
- [ ] Read the driver version and date from the adapter's device node. Done when: the values match the driver's properties page.
- [ ] Add NVIDIA detail through NVAPI and AMD detail through ADL, as far as `docs/decisions/graphics-vendor-libraries.md` allows. Done when: the vendor's values appear with their source named, and a missing library records one Skipped activity line saying no such driver is installed.
- [ ] Cover the decode and the missing-library path in `tests/adapter_test.cpp` with a fake adapter source. Done when: `ctest --preset debug -L graphics` passes.
- [ ] Commit: `read: graphics adapters, with vendor detail where the driver offers it`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L graphics` passes, and a run on the test machine lists the adapters Device Manager lists.

## 15. Displays From EDID

Each connected display from its EDID block in the registry: the maker, model, native mode, physical size, when it was made and its serial number.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Read each monitor's EDID from its device node in `src/read/graphics/DisplayReader.cpp`. Done when: the block is returned for each active monitor.
2. Decode it through `ByteReader`. Done when: the fixture returns the model name and the native mode.

- [ ] Enumerate active monitors with SetupAPI and read the `EDID` registry value of each device in `src/read/graphics/DisplayReader.cpp`. Done when: each connected monitor returns a 128-byte block or longer.
- [ ] Decode the header, the three-letter maker ID, the product code, the week and year of manufacture, the physical size, the preferred detailed timing and the name and serial descriptors in `src/read/graphics/Edid.cpp`. Done when: the fixture returns `DELL U2720Q`, 3840 by 2160 at 60 Hz and 597 by 336 mm.
- [ ] Verify the header and the checksum and refuse a block that fails either. Done when: a corrupted fixture returns an error and the display is listed with "EDID not readable".
- [ ] Commit real blocks as `tests/fixtures/edid/` with their serial numbers zeroed and the checksum recomputed. Done when: `tests/edid_test.cpp` decodes each.
- [ ] Commit: `read: displays from their EDID`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset asan -L edid` passes for the real and the corrupted fixtures.

## 16. PCI and USB Devices

The Devices section: every PCI device with its location and IDs, and every USB device with its port, IDs and speed.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Enumerate PCI devices with CfgMgr32 in `src/read/devices/PciReader.cpp`. Done when: each has its bus location, name and vendor and device IDs.
2. Enumerate USB devices in `src/read/devices/UsbReader.cpp`. Done when: each has its port, IDs and speed.

- [ ] Enumerate the `PCI` enumerator with `CM_Get_Device_ID_List` and read each device's location, description and hardware IDs in `src/read/devices/PciReader.cpp`. Done when: the list matches Device Manager's "by connection" PCI devices.
- [ ] Mark a device with no driver or with a problem code, naming the problem in words. Done when: a fake device with problem code 28 reads "No driver installed".
- [ ] Enumerate USB hubs and their ports with `IOCTL_USB_GET_NODE_CONNECTION_INFORMATION_EX_V2` in `src/read/devices/UsbReader.cpp`, reading each device descriptor through `ByteReader`. Done when: each connected device returns its vendor and product IDs and its speed.
- [ ] Name vendors from `data/pci-vendors.csv` and `data/usb-vendors.csv` compiled into the database, falling back to the ID. Done when: `VEN_10DE` reads NVIDIA and an unknown ID is shown as the ID.
- [ ] Cover both in `tests/devices_test.cpp` with fake sources. Done when: `ctest --preset debug -L devices` passes.
- [ ] Commit: `read: PCI and USB devices with their IDs`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L devices` passes with the fakes, and a run on the test machine lists what Device Manager lists.

## 17. Network Adapters and Battery

The Network and power section: each physical network adapter with its state and address, and the battery with its wear.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Read adapters with `GetAdaptersAddresses` in `src/read/NetworkReader.cpp`. Done when: physical adapters are listed and virtual ones are not.
2. Read the battery with the battery IOCTLs in `src/read/BatteryReader.cpp`. Done when: a laptop returns design and full-charge capacity and a desktop returns "No battery".

- [ ] List physical Ethernet and Wi-Fi adapters with their state, link speed and MAC address in `src/read/NetworkReader.cpp`, leaving out loopback, tunnel and virtual adapters. Done when: the list matches the physical adapters in Network Connections.
- [ ] Read `BATTERY_INFORMATION` and `BATTERY_STATUS` through `IOCTL_BATTERY_QUERY_INFORMATION` in `src/read/BatteryReader.cpp`. Done when: a fake battery of 50,000 mWh design and 41,000 mWh full charge reads 18 percent wear.
- [ ] Report a desktop as "No battery (desktop)" using the chassis type from §8. Done when: the desktop fixture returns that one row.
- [ ] Cover both in `tests/network_battery_test.cpp` with fakes. Done when: `ctest --preset debug -L power` passes.
- [ ] Commit: `read: network adapters and the battery`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L power` passes, and fails when wear is computed from the wrong capacity.

## 18. Slots and Connectors Model

The Board section and the storage advice need one list of every slot and connector, with what is in it. It is built from SMBIOS type 9 (system slots), the memory slots of §9, the drives of §12, the adapters of §14 and the devices of §16.

**Phase:** 1
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Build the part list in `src/core/SlotModel.cpp`. Done when: the desktop fixture yields the processor socket, four memory slots, two M.2 slots, three PCIe slots and four SATA ports.
2. Match fitted devices to slots. Done when: the graphics card is in its PCIe slot and each drive in its slot or port.

- [ ] Decode SMBIOS type 9 in `src/read/smbios/SlotReader.cpp`: designation, slot type (PCIe generation and width, M.2 socket), usage and the bus address. Done when: the fixture returns `PCIEX16_1` as PCIe x16, in use.
- [ ] Build `SlotModel` in `src/core/SlotModel.cpp` as a list of parts, each with a kind, a name, a state (fitted, free, needs attention) and its values. Done when: the fixture yields fifteen parts.
- [ ] Match a fitted PCIe or M.2 slot to its device by the bus address type 9 reports. Done when: `PCIEX16_1` holds the graphics adapter and `M.2_1` the NVMe drive in the fixture.
- [ ] Count SATA ports from the AHCI controller's implemented-ports value and match drives to ports by port number. Done when: a four-port fixture with one drive yields one fitted and three free.
- [ ] Fall back when the firmware reports no type 9 slots: keep the memory slots and the drives and mark the model "slots not reported". Done when: the laptop fixture yields memory slots and drives only, with that mark (`design/SPEC.md` section 3). Cheaper substitute: inventing typical slots for the chassis type.
- [ ] Cover it in `tests/slotmodel_test.cpp`. Done when: `ctest --preset debug -L slots` passes for the desktop, laptop and empty fixtures.
- [ ] Commit: `core: one model of every slot and connector and what is in it`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L slots` passes, and fails when a fitted slot is matched by position instead of bus address.

## 19. Compatibility Database Build

The database is one read-only SQLite file shipped beside the executable. Its rows live in the repository as text files, each with its source and the date it was taken, and a Python script compiles them at build time, so every change shows in git.

**Phase:** 2
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Write `tools/build_db.py` compiling `data/*.csv` into `build/busview.db`. Done when: the same inputs always produce the same bytes.
2. Wire it into CMake. Done when: a changed CSV rebuilds the database and nothing else.

- [ ] Write the schema in `data/schema.sql`: a `meta` table (schema version, data version, built date) and one table per CSV, every data table carrying `source` and `taken` columns. Done when: `sqlite3 build/busview.db .schema` shows them.
- [ ] Write `tools/build_db.py` (standard library only) reading each `data/*.csv`, refusing a row with an empty `source` or `taken` or a wrong column count by file and line, and writing the database to a temporary file that replaces the target. Done when: a row with no source makes it exit 1 naming the file and line. Cheaper substitute: loading what parses and skipping the rest, which ships unsourced rows.
- [ ] Make the output reproducible: fixed page size, rows inserted in sorted order, no timestamps but the data version from `data/VERSION`. Done when: two builds produce files with the same SHA-256.
- [ ] Add the `busview_db` custom target to `CMakeLists.txt` depending on every file under `data/`, copying the result beside the executable. Done when: touching one CSV rebuilds only the database.
- [ ] Add `tools/tests/test_build_db.py`. Done when: `python -m unittest discover -s tools/tests` passes, and fails when the source check is removed.
- [ ] Commit: `db: the compatibility database is built from sourced text files`

**Test checkpoint:** `python -m unittest discover -s tools/tests` passes, and two runs of `python tools/build_db.py` give the same SHA-256.

## 20. Database Reader in the Tool

The tool opens the database read-only, checks it is one it understands, and keeps working with a clear message when it is missing or damaged.

**Phase:** 2
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Add SQLite to the build and open the file in `src/db/Database.cpp`. Done when: the version is read from `meta`.
2. Handle a missing, damaged or newer-schema file. Done when: each returns its own reason and the inventory still works.

- [ ] Fetch the SQLite amalgamation by `FetchContent` at a pinned version with its SHA-256 and build it as a static library with `SQLITE_OMIT_LOAD_EXTENSION` and `SQLITE_DQS=0`. Done when: the executable still imports only Windows system libraries.
- [ ] Implement `Database::Open(path)` in `src/db/Database.cpp` with `SQLITE_OPEN_READONLY` and `immutable=1`. Done when: opening the built database returns its data version, and a write attempt fails.
- [ ] Return a distinct reason for a missing file, a file that is not SQLite, a failed `PRAGMA quick_check` and a schema version newer than the tool knows. Done when: four fixtures under `tests/fixtures/db/` each return their reason (`design/SPEC.md` S-7). Cheaper substitute: one generic "database error".
- [ ] Add typed queries in `src/db/Queries.cpp` (`ProcessorLimits`, `BoardSpec`, `VendorName`, `BeepCodes`) using prepared statements with bound parameters only. Done when: no query string is built by concatenation, checked by a test that passes a quote character as input.
- [ ] Cover it in `tests/database_test.cpp`. Done when: `ctest --preset debug -L database` passes.
- [ ] Commit: `db: the tool reads the database read-only and survives a bad one`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L database` passes for the good file and the four bad ones.

## 21. Processor and Board Specification Data

Layer 2 of the database: what a processor supports and what a board supports, keyed on what Busview can read. This section builds the first data set and the rules for adding to it; it does not collect maker-tested kit lists, which the README places after version 1.

**Phase:** 2
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Write `data/processors.csv` keyed on vendor, family and model. Done when: the processors of the fixtures resolve to their memory limits.
2. Write `data/boards.csv` keyed on the SMBIOS board maker and product. Done when: the desktop fixture's board resolves to its slots.

- [ ] Define `data/processors.csv` (vendor, family, model, name pattern, memory types, maximum memory, maximum official speed, on the Windows 11 supported list, source, taken) and fill it for the Intel Core generations 6 to 14 and AMD Ryzen 1000 to 9000 desktop and mobile families from the makers' specification pages. Done when: each row's source is a URL on the maker's site and the fixtures' processors resolve.
- [ ] Define `data/boards.csv` (maker, product, memory slots, maximum memory, maximum speed, M.2 slots with their link, SATA ports, source, taken) and fill it for the boards of the fixtures and the development machines from the makers' specification pages. Done when: the desktop fixture's board resolves to four slots, 128 GB, two M.2 and four SATA.
- [ ] Write `docs/data-sources.md`: which sources are used, that each row records its source and date, and that maker-tested kit lists and proprietary finders are not copied. Done when: the file states the rule for each source type. Cheaper substitute: rows with no stated origin.
- [ ] Add `tools/check_data.py` refusing a duplicate key, an unknown memory type or a `taken` date in the future. Done when: it runs in `scripts/check-all.ps1` and fails on a duplicated row.
- [ ] Cover the lookups in `tests/specdata_test.cpp` against the built database. Done when: `ctest --preset debug -L specdata` passes, and a processor absent from the table returns "not in the database", never a guess.
- [ ] Commit: `data: processor and board specifications, each row sourced and dated`

**Test checkpoint:** `python tools/check_data.py` exits 0 and `sdk\reskit\cmake\bin\ctest.exe --preset debug -L specdata` passes.

## 22. Memory Advice

The answer to "can I add memory, and what do I buy": a verdict, a sentence, the specification to buy and the steps, from the machine's own facts first and the database second.

**Phase:** 2
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Define `Advice` in `src/advice/Advice.h` and implement `MemoryAdvice` in `src/advice/MemoryAdvice.cpp`. Done when: the desktop fixture returns the design's memory advice.
2. Cover every case. Done when: full slots, soldered memory and missing data each return their own advice.

- [ ] Define `Advice` in `src/advice/Advice.h`: an id, the question, a verdict kind (good, watch, problem, information, not known), the verdict, a title, a sentence, an optional specification to buy, the steps, and the area it belongs to. Done when: every field of the design's advice rows and banners has a member.
- [ ] Implement the layer 1 rule in `src/advice/MemoryAdvice.cpp`: with free slots, advise adding modules that match the fitted type, form factor, speed and voltage. Done when: the desktop fixture returns "Add 2 x 8 GB to reach 32 GB" with the specification `DDR4 UDIMM, 3200 MT/s, 1.35 V` and the fitted part number.
- [ ] Bound the advice by the smaller of the firmware's maximum, the board's row and the processor's row, and name which one limited it. Done when: a fixture whose firmware reports 32 GB and whose board row says 128 GB uses 128 GB and says the firmware's figure was overridden by the board's specification.
- [ ] Handle no free slots (advise replacing the pair, with the largest size the limits allow), soldered memory (say it cannot be upgraded), mixed modules (say so and advise matching the faster pair's specification) and an empty part number (give the specification without one). Done when: each fixture returns its case's advice.
- [ ] Return verdict "not known" with the reason when the type or the slot count could not be read. Done when: a fixture with no type 17 structures returns it. Cheaper substitute: advising DDR4 by default.
- [ ] Cover it in `tests/memoryadvice_test.cpp`. Done when: `ctest --preset debug -L memoryadvice` passes for the seven cases, and fails when the limit ignores the processor.
- [ ] Commit: `advice: what memory to buy, from the machine and the database`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L memoryadvice` passes for all seven cases.

## 23. Storage Advice

The answer to "can I add a drive": which M.2 slots and SATA ports are free and what fits them.

**Phase:** 2
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Implement `StorageAdvice` in `src/advice/StorageAdvice.cpp` over the slot model. Done when: the desktop fixture returns "Room for a second NVMe drive".
2. Cover no free connection and slots not reported. Done when: each returns its own advice.

- [ ] List free M.2 slots with their link and length from the slot model and the board's row in `src/advice/StorageAdvice.cpp`. Done when: the fixture returns `M.2_2`, PCIe 3.0 x4, up to 2280, and the specification `M.2 2280 NVMe, PCIe 3.0 x4 or faster`.
- [ ] Count free SATA ports and add them to the sentence. Done when: the fixture's sentence names three free ports.
- [ ] Say when a faster drive would run slower in the slot. Done when: the steps include that a PCIe 4.0 drive runs at PCIe 3.0 speed in a PCIe 3.0 slot.
- [ ] Return "no free connection" advice when none is free, and "not known" when the firmware reported no slots and the board is not in the database. Done when: the two fixtures return those. Cheaper substitute: assuming every desktop has a free SATA port.
- [ ] Cover it in `tests/storageadvice_test.cpp`. Done when: `ctest --preset debug -L storageadvice` passes.
- [ ] Commit: `advice: whether a drive can be added, and what fits`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L storageadvice` passes for the three cases.

## 24. Drive Health Advice

The answer to "is anything wearing out": each drive judged from its own health values by stated rules, and from the change since the last snapshot when there is one.

**Phase:** 2
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Implement the rules in `src/advice/HealthAdvice.cpp`. Done when: each rule has a fixture that triggers it.
2. Handle the unread case. Done when: a refused health read returns "Needs administrator" and no verdict on health.

- [ ] State the rules as data in `src/advice/HealthRules.h`: reallocated, pending or uncorrectable sectors above zero is Watch; NVMe percentage used at or above 90 is Watch; NVMe critical warning bits or media errors above zero is Watch; otherwise Good. Done when: each rule cites the attribute it reads in a comment.
- [ ] Implement `HealthAdvice` in `src/advice/HealthAdvice.cpp` returning one advice naming the drive, the value and what to do. Done when: the fixture with 8 reallocated sectors returns "Back up the 2 TB Seagate drive".
- [ ] Add the earlier value when a previous snapshot holds one. Done when: with a snapshot fixture holding zero, the sentence says it had none on that snapshot's date.
- [ ] Return verdict "Needs administrator" when §13 was refused. Done when: the refusal fixture returns it and no Watch (`design/SPEC.md` S-2). Cheaper substitute: reporting the drive as healthy when its health was never read.
- [ ] Cover it in `tests/healthadvice_test.cpp`. Done when: `ctest --preset debug -L healthadvice` passes, and fails when the pending-sector rule is removed.
- [ ] Commit: `advice: which drive to watch, by stated rules`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L healthadvice` passes for each rule, the good case and the refusal.

## 25. Windows 11 Readiness

The answer to "is it ready for Windows 11": each published requirement checked against what was read, with the one that fails named and why.

**Phase:** 2
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Implement the checks in `src/advice/Windows11Advice.cpp`. Done when: the desktop fixture meets every requirement.
2. Name each failure. Done when: a fixture failing two requirements names both.

- [ ] Check the processor against the supported-list column of `data/processors.csv`, 64-bit and at least two cores. Done when: a seventh-generation Intel fixture fails with "this processor is not on Microsoft's supported list".
- [ ] Check TPM 2.0, UEFI mode and Secure Boot capability from §11, treating Secure Boot off but supported as met and saying it is off. Done when: the desktop fixture reads "Meets every requirement" with the Secure Boot note.
- [ ] Check memory of at least 4 GB and a system drive of at least 64 GB. Done when: a 2 GB fixture fails naming memory.
- [ ] Return "not known" for a requirement whose value was refused or unread, never a failure. Done when: the refused-TPM fixture reads "TPM could not be read" and the verdict is "not known".
- [ ] Record the requirement list with its Microsoft source URL and the date taken in `data/windows11-requirements.csv`. Done when: the checks read their thresholds from the database.
- [ ] Cover it in `tests/windows11_test.cpp`. Done when: `ctest --preset debug -L windows11` passes for pass, two failures and not known.
- [ ] Commit: `advice: Windows 11 readiness, each requirement named`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L windows11` passes for all four fixtures.

## 26. Snapshot File Format and Writer

A snapshot is one versioned JSON document holding the whole inventory, written atomically and read back.

**Phase:** 3
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Define the format in `docs/snapshot-format.md` and write it in `src/snapshot/SnapshotWriter.cpp`. Done when: a snapshot of the fixture inventory matches a committed golden file.
2. Read it in `src/snapshot/SnapshotReader.cpp`. Done when: a written snapshot reads back to an equal inventory.

- [ ] Fetch nlohmann/json by `FetchContent` at a pinned commit as the JSON library. Done when: it builds with the SDK's warnings and the executable's imports are unchanged.
- [ ] Define the document in `docs/snapshot-format.md`: `format` version 1, Busview and database versions, the time taken in UTC, a note, the rights it was taken with, then areas, groups and values with stable keys. Done when: the file lists every field with its type.
- [ ] Implement `SnapshotWriter::Write(inventory, path, note)` in `src/snapshot/SnapshotWriter.cpp`: write to a temporary file in the same folder, flush, replace the target, then read it back and compare. Done when: a test that fails the replace leaves no partial file and the original untouched. Cheaper substitute: writing the target in place, which can leave it half-written.
- [ ] Implement `SnapshotReader::Read(path)` in `src/snapshot/SnapshotReader.cpp`, refusing invalid JSON, a missing field and a newer `format` by name. Done when: three bad fixtures each return their reason.
- [ ] Name files `Busview-<computer>-<yyyy-MM-dd-HHmmss>.json` in the snapshot folder, `Documents\Busview\Snapshots` by default. Done when: two snapshots in the same second get distinct names.
- [ ] Cover it in `tests/snapshot_test.cpp` with a golden file under `tests/fixtures/snapshots/`. Done when: `ctest --preset debug -L snapshot` passes, and fails when a value's key changes.
- [ ] Commit: `snapshot: one versioned JSON file, written atomically and read back`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L snapshot` passes: write, read back, the golden file and the three refusals.

## 27. Snapshot Compare Engine

Two snapshots compare to a list of changed values, each classed as needing attention, changed, or expected.

**Phase:** 3
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Implement `Compare` in `src/snapshot/Compare.cpp`. Done when: the two fixture snapshots yield the six differences of the design.
2. Class each difference. Done when: the reallocated-sector rise is Watch and the power-on hours rise is Expected.

- [ ] Implement `Compare(a, b)` in `src/snapshot/Compare.cpp` matching values by area, group and key, returning changed, added and removed values and the count unchanged. Done when: the fixtures yield six changed and 206 unchanged.
- [ ] Match devices by a stable identity (a drive by serial number, a memory module by slot, a display by its EDID serial) so that a reordered list is not a change. Done when: two snapshots with their drives in a different order yield no differences.
- [ ] Class differences by rules in `src/snapshot/CompareRules.h`: a health counter that rose is Watch, a module or drive that vanished is Watch, a counter that only grows with use is Expected, anything else is Changed. Done when: each rule has a fixture.
- [ ] Refuse to compare snapshots of different computers unless asked, naming both. Done when: fixtures with different system identities return that refusal.
- [ ] Cover it in `tests/compare_test.cpp`. Done when: `ctest --preset debug -L compare` passes, and fails when the Watch rule for a vanished module is removed.
- [ ] Commit: `snapshot: compare two snapshots and class each change`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L compare` passes for the design's pair, the reordered pair and the two-computer refusal.

## 28. Beep Code Data in the Database

The 177 beep codes of the AutoIt BiosCodes become one table of the database, with their texts exactly as the original shows them.

**Phase:** 3
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Extract the codes with `tools/extract_beepcodes.py` into `data/beepcodes.csv`. Done when: the file holds 177 rows across seven makers.
2. Prove the extraction against the source. Done when: a test recomputes it and compares.

- [ ] Write `tools/extract_beepcodes.py` reading the 246 indexed texts and their English defaults from `reference/beepcodes-au3/src/Includes/Localization.au3:119-395` and the pattern-to-index mapping of each maker from `reference/beepcodes-au3/src/BiosCodes.au3:783-1263`. Done when: it writes `data/beepcodes.csv` with maker, pattern, meaning, advice, source and taken.
- [ ] Keep the original's composition: a code's own text and the shared advice text its mapping names, as two columns. Done when: each row's advice is one of the five shared advice texts (entries 1 to 5).
- [ ] Keep Phoenix pattern 2-1-2-4, which the original maps and never lists (`BiosCodes.au3:696`, `:1022-1254`), and list the duplicate 2-1-2-3 once. Done when: Phoenix has 114 rows and each of the two patterns appears once. Cheaper substitute: copying only the patterns the original's list showed, which loses a mapped code.
- [ ] Assert the counts in `tools/tests/test_beepcodes.py`: AMI 15, AST 19, Award 5, Compaq 7, Dell 7, IBM 10, Phoenix 114, 177 in all, and that re-running the extraction reproduces the committed CSV byte for byte. Done when: the test passes, and fails when one text in the CSV is edited.
- [ ] Add the `beepcodes` table to `data/schema.sql` and the general "about beep codes" text (entry 0) to `resources/strings/en.json`. Done when: the built database holds 177 rows.
- [ ] Commit: `data: the 177 beep codes, carried over exactly`

**Test checkpoint:** `python -m unittest discover -s tools/tests -p "test_beepcodes.py"` passes, and fails when a text in `data/beepcodes.csv` is changed by hand.

## 29. Beep Code Lookup and Search

Finding a code: by maker, by a search across every maker, and starting on the maker this computer's BIOS reports.

**Phase:** 3
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Implement `BeepCodes` in `src/beep/BeepCodes.cpp` over the database. Done when: a maker returns its codes in the original's order.
2. Implement the search and the maker match. Done when: `1 long 2 short` finds every maker's entry and `American Megatrends Inc.` matches AMI.

- [ ] Implement `BeepCodes::ByMaker(name)` and `All()` in `src/beep/BeepCodes.cpp`. Done when: `ByMaker("Dell")` returns 7 and `All()` returns 177.
- [ ] Implement `BeepCodes::Search(text)`: read counts and the words long, short, beep and beeps, treat `1L 2S` and `1-3-3-3` forms as patterns, match the meaning text otherwise, and rank pattern matches before meaning matches. Done when: `1 long 2 short` returns the AMI, AST, Award, Compaq and IBM entries first.
- [ ] Implement `MakerMatch(biosVendor)` in `src/beep/MakerMatch.cpp` from a table of normalised substrings for the seven makers. Done when: `American Megatrends Inc.`, `Dell Inc.` and `Phoenix Technologies Ltd.` return AMI, Dell and Phoenix, and an unknown vendor returns none.
- [ ] Return an empty result, not an error, for text nothing matches. Done when: a test searching `zzz` returns zero rows and the reason "no match".
- [ ] Cover it in `tests/beepcodes_test.cpp`. Done when: `ctest --preset debug -L beep` passes, and fails when the ranking is reversed.
- [ ] Commit: `beep: find a code by maker, by search, and by this computer's BIOS`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L beep` passes for a shared pattern, an unknown pattern and three maker matches.

## 30. Report Export and Privacy Masking

The report a person keeps or sends: the whole inventory and the advice as a readable text file or as JSON, with identifying values hidden by default. The comparison exports the same way.

**Phase:** 3
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Implement `Report` in `src/snapshot/Report.cpp`. Done when: the fixture inventory exports to a text file matching a golden file.
2. Implement masking in `src/snapshot/Mask.cpp`. Done when: no serial number, MAC address, computer name or UUID of the fixture appears in a masked export.

- [ ] Implement `Report::WriteText(inventory, advice, path)` and `WriteJson` in `src/snapshot/Report.cpp`, both through the atomic write and readback of §26. Done when: the text export lists every area, group and value and the four pieces of advice.
- [ ] Implement `Report::WriteDifferences(compareResult, path)`. Done when: the design's six differences export with both readings and their class.
- [ ] Mark the values that identify a person or a machine in the model (serial numbers, MAC addresses, computer name, system UUID, asset tags) and implement `Mask` in `src/snapshot/Mask.cpp` replacing each with a stable placeholder of the same kind. Done when: a test greps the masked export for every such value of the fixture and finds none (`design/SPEC.md` X-6). Cheaper substitute: masking by a pattern over the output text, which misses values that do not look like serial numbers.
- [ ] Keep masking on by default and off only by an explicit setting or argument. Done when: an export with no option is masked.
- [ ] Cover it in `tests/report_test.cpp` with golden files. Done when: `ctest --preset debug -L report` passes, and fails when a new identifying value is added to the model without its mark.
- [ ] Commit: `report: export the inventory, the advice and a comparison, masked by default`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L report` passes: the golden files match and the masked export holds no identifying value of the fixture.

## 31. Headless Scan Command

The engine's end-to-end proof before the window exists, and what a technician scripts: one command scans the computer and writes a snapshot or a report, with no window.

**Phase:** 3
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Parse arguments in `src/cli/CommandLine.cpp`. Done when: `Busview.exe --help` prints the options and exits 0 without opening a window.
2. Run the scan and write the file. Done when: `Busview.exe --snapshot out.json` writes a snapshot of the real machine that reads back.

- [ ] Implement `--snapshot <path>`, `--report <path>` (text or JSON by extension), `--compare <a> <b> <out>`, `--unmasked`, `--help` and `--version` in `src/cli/CommandLine.cpp`. Done when: an unknown option exits 2 naming it.
- [ ] Attach to the parent console when started from one, since the executable is a window application. Done when: output appears in the calling PowerShell window and `$LASTEXITCODE` is set.
- [ ] Exit 0 on success, 1 when the file could not be written, 3 when the scan completed with a failed reader, each with one line saying what happened. Done when: a test asserts each code.
- [ ] Add `tests/cli_test.cpp` running the built executable against the real machine in a job object with a 60-second limit, ending the whole job on timeout and teardown and starting it with no console window. Done when: `ctest --preset debug -L cli` passes and the snapshot it wrote holds a Memory area with at least one value.
- [ ] Run the command on the development machine and commit its masked text report as `docs/evidence/first-real-scan.txt`. Done when: the file shows real readings for every area the machine has.
- [ ] Commit: `cli: scan the computer and write a snapshot or a report with no window`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L cli` passes on the real machine, and `Bin\Debug\Busview.exe --snapshot` then `--compare` of the file with itself reports zero differences.

## 32. Window Shell, Sidebar and First Scan

The suite's tool window with Busview's sections, the scan running off the UI thread, and the first-scan state. It waits on the SDK's tool window host, button, tooltip and progress controls.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` section 1 (W-1 to W-10), state S-1 and rule X-8, against `design/captures/overview-*.png` and `state-first-scan-*.png`, in light and dark at 100 and 150 percent.
**Job:** a person starts Busview and sees it read their computer, then moves between sections. Consumer: the rendered window, driven and read back through UI Automation.
**Treatment:** the sidebar in the contract's order with the sliding indicator, the status bar text taken from the content, and the scan's progress in words. Cheaper substitute that fails the checkpoint: a window that blocks until the scan ends.
**Chrome:** the SDK's tool window host, sidebar, content header, status bar and progress control. No control of Busview's own.

**Build order:**

1. Build the window in `src/ui/MainWindow.cpp` from the SDK's tool window host. Done when: every section of W-2 is in the sidebar and Overview is selected at start.
2. Run the scan from `src/ui/ScanController.cpp`. Done when: S-1 shows while it runs and the content appears when it ends.

- [ ] Create `src/ui/MainWindow.cpp` hosting the SDK's tool window with the sections of `design/SPEC.md` W-2 in order, each with its Lucide icon. Done when: selecting each section switches the content and the indicator slides. Cheaper substitute: a private sidebar, which the contract forbids.
- [ ] Add the icons the design uses and the SDK's Lucide set lacks to Resolute-SDK and bump `sdk.json`. Done when: every sidebar entry shows its icon from `LucideIcons`. Cheaper substitute: embedding SVG files in Busview.
- [ ] Implement `src/ui/ScanController.cpp` starting `ScanRunner` on a worker thread and marshalling progress and the result to the UI thread. Done when: the window stays responsive to a section change during a scan slowed by a test hook (X-8).
- [ ] Show the first-scan state S-1 over the content with the icon, the sentence, the progress bar and the name of what is being read. Done when: the driven test reads the sentence and a progress value through UI Automation.
- [ ] Set the status bar: the left text from the current content, the right text from the rights level and the database version (W-7, W-8). Done when: it changes with the section and reads "Standard user" in a non-elevated run.
- [ ] Show the attention dot on Board and Storage from the advice (W-4) with its accessible name. Done when: a fixture with a Watch drive shows both dots and one without shows none.
- [ ] Enforce the minimum size, collapse the sidebar below 600 pixels and restore size and position per monitor (W-9, W-10). Done when: the driven test resizes below 600 and reads the collapsed state, and a restart restores the placement.
- [ ] Add `tests/window_test.cpp` starting the window with a fixture inventory and reading the sidebar through UI Automation. Done when: `ctest --preset debug -L window` passes, and fails when a section is removed.
- [ ] Commit: `ui: the tool window, its sections and the first scan`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L window` passes, and the window stays responsive during a slowed scan.

## 33. Overview Section

The first screen: the computer in eight tiles and the advice as rows, with Rescan, Export report and Take snapshot.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` section 2 (OV-1 to OV-8) and state S-7, against `design/captures/overview-*.png`.
**Job:** a person sees what their computer is and what Busview advises, in one screen. Consumer: the rendered tiles and rows, read back against the inventory and the advice.
**Treatment:** every tile and advice row carries real readings, every verdict an icon and a word, and the primary action is labelled with what it does. Cheaper substitute that fails the checkpoint: tiles with typed-in values.
**Chrome:** the SDK's content header, button, list, chip and tile or list controls. No control of Busview's own.

**Build order:**

1. Build `src/ui/OverviewView.cpp` from the inventory and the advice. Done when: the tiles and rows of the fixture match the design.
2. Wire the three actions. Done when: each does its work off the UI thread and reports in the status bar and Activity.

- [ ] Build the machine line and the rights chip (OV-4, OV-5) in `src/ui/OverviewView.cpp`. Done when: they show the fixture's computer name, board, Windows version and scan time.
- [ ] Build the eight tiles (OV-6) from the inventory, each opening its section. Done when: the driven test activates each tile by keyboard and reads the section it opened.
- [ ] Build the advice list (OV-7, OV-8) from `Advice`, each row opening its section. Done when: the four rows show the fixture's verdicts with an icon and a word.
- [ ] Wire Rescan, Export report and Take snapshot (OV-1 to OV-3). Done when: Take snapshot writes a file that reads back, the status bar names it, and Activity gains one record. Cheaper substitute: updating the list from memory without re-reading the folder.
- [ ] Show the database-missing sentence in place of the advice list (S-7) and keep the tiles. Done when: with the database renamed, the tiles show and the sentence names the file.
- [ ] Extend `tests/window_test.cpp` for the Overview. Done when: `ctest --preset debug -L overview` passes, and fails when a tile's value is forced wrong.
- [ ] Commit: `ui: the Overview section`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L overview` passes: tiles and advice equal the fixture's, and Take snapshot's file reads back.

## 34. Area Sections With Explain and Copy

The seven area sections share one view: advice banners, titled groups of name and reading rows, the Explain toggle and Copy. Memory adds its slots row.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` section 4 (AR-1 to AR-7), state S-6 and rule X-9, against the `memory`, `processor`, `motherboard`, `storage`, `graphics`, `devices`, `network-and-power` and `state-explain-memory` captures.
**Job:** a person reads every value Busview found for one part of the computer and understands the ones that matter. Consumer: the rendered groups, read back against the inventory.
**Treatment:** machine values in monospace and copyable, explanations one line under the value when Explain is on, advice above the values it is about. Cheaper substitute that fails the checkpoint: one long text box of names and values.
**Chrome:** the SDK's content header, toggle, button, grouped list and chip controls. No control of Busview's own.

**Build order:**

1. Build `src/ui/AreaView.cpp` rendering any area of the inventory. Done when: all seven sections show the fixture's groups.
2. Add the banners, the slots row, Explain and Copy. Done when: each matches its capture's content.

- [ ] Build `src/ui/AreaView.cpp` rendering groups and rows (AR-4, AR-5) from `Area`, with machine values monospace, selectable and copyable. Done when: the seven sections show the fixture's values and Ctrl+C on a selected reading copies it.
- [ ] Add the advice banners (AR-3) from `Advice` by area, with Copy specification. Done when: Memory shows the memory advice, Motherboard the Windows 11 advice and Storage the health and storage advice, and Copy specification puts the specification on the clipboard.
- [ ] Add the group chips (AR-6) for drive health. Done when: the fixture's drives show Good and Watch, each with an icon.
- [ ] Add the Memory slots row (AR-7) from the slot model. Done when: four cards show in firmware order, two Fitted and two Free with the dashed outline.
- [ ] Add the Explain toggle (AR-1) bound to the setting of SE-6, showing each value's explanation from the strings. Done when: turning it on shows the lines, the status bar says so, and the setting survives a restart.
- [ ] Add Copy (AR-2) for the whole section as text. Done when: the clipboard holds every group, name and reading of the section.
- [ ] Show a failed or refused reader as one sentence in its section (S-6) and nothing invented (X-9). Done when: a fixture whose graphics reader failed shows the sentence on Graphics and every other section complete.
- [ ] Extend the driven tests in `tests/areaview_test.cpp`. Done when: `ctest --preset debug -L areas` passes for all seven sections, and fails when a group is dropped.
- [ ] Commit: `ui: the seven area sections, with Explain and Copy`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L areas` passes: every section's rows equal the inventory, Explain toggles, and a failed reader shows its sentence.

## 35. Board Section Diagram and Inspector

The Board section: a schematic of the slots and connectors with the selected part's values and advice beside it. The diagram is the one surface the SDK has no control for, so it is Busview's own drawing on the SDK's render context and tokens.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` section 3 (BD-1 to BD-11), against the `board`, `state-board-free-slot` and `state-board-watch` captures.
**Job:** a person sees what is fitted, what is free and what needs attention, and reads one part's detail and advice. Consumer: the rendered diagram and inspector, read back against the slot model.
**Treatment:** fitted, free and needs-attention parts differ by fill, outline style and words, the honesty line is always shown, and every part is reachable by arrow keys and named for screen readers. Cheaper substitute that fails the checkpoint: a bitmap picture of a board with hotspots.
**Chrome:** the SDK's content header, button and grouped list for the inspector; the diagram is Busview's own, drawn with `RenderContext` and theme tokens only.

**Build order:**

1. Lay the parts out in `src/ui/BoardLayout.cpp` by stated rules. Done when: the desktop fixture's fifteen parts are placed without overlap.
2. Draw and drive them in `src/ui/BoardView.cpp`. Done when: selecting a part by mouse or arrow key updates the inspector.

- [ ] Implement `BoardLayout` in `src/ui/BoardLayout.cpp`: the processor socket upper left, memory slots as vertical bars to its right, M.2 and PCIe slots as horizontal bars below in firmware order, SATA ports stacked at the right, in scalable units. Done when: a test places the desktop, a two-slot and a laptop fixture with no two parts overlapping and none outside the board.
- [ ] Draw the diagram (BD-2, BD-3, BD-5, BD-6) in `src/ui/BoardView.cpp` with theme tokens only: fitted filled in the success tokens, free with a dashed outline, needs attention in the warning tokens, the honesty line and the legend. Done when: the rendering in light and dark shows the three states, and no colour literal appears in the file. Cheaper substitute: hardcoded colours, which break in the other theme and in high contrast.
- [ ] Implement selection (BD-4) by click and by arrow keys moving to the nearest part in that direction. Done when: the driven test walks from `DIMM_A1` to `SATA6G_4` by arrow keys.
- [ ] Expose each part to UI Automation as a selectable item named with its slot and what is in it. Done when: a UI Automation walk lists fifteen named items and the selected one reports selected.
- [ ] Build the inspector (BD-7 to BD-11): heading, state chip, values, advice, Copy and Open section. Done when: selecting `M.2_2` shows "Empty M.2 slot", Free, its values and the storage advice, and Open Storage opens that section.
- [ ] Show the single-row fallback and the empty state when the model says slots were not reported. Done when: the laptop fixture shows memory slots and drives in a row, and the empty fixture shows the SDK's empty state with its sentence.
- [ ] Cover it in `tests/boardview_test.cpp`. Done when: `ctest --preset debug -L board-view` passes, and fails when a part loses its accessible name.
- [ ] Commit: `ui: the Board section, a diagram of slots with an inspector`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L board-view` passes: layout without overlap, keyboard selection, fifteen named parts and the inspector's values equal the slot model's.

## 36. Standard User Refusal and Restart

Without administrator rights drive health is not read. The window says exactly that, shows everything else, and offers to restart elevated.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` state S-2, against the `state-standard-user-storage` and `state-standard-user-board` captures.
**Job:** a person running as a standard user understands what is missing and can get it with one action. Consumer: the rendered Storage, Board and Overview sections in a non-elevated run.
**Treatment:** the refusal names what was not read, why, and that the rest is complete; health rows are absent, not blank. Cheaper substitute that fails the checkpoint: showing drives as healthy, or a blanket "run as administrator" banner over the whole window.
**Chrome:** the SDK's banner, button and elevation helper. No control of Busview's own.

**Build order:**

1. Show the refusal in `src/ui/AreaView.cpp` from the reader's outcome. Done when: a non-elevated run shows it on Storage.
2. Wire Restart as administrator through the SDK's elevation helper. Done when: accepting the prompt restarts Busview elevated on the same section.

- [ ] Render the refusal in place of the health banner on Storage, leave out the health, power-on time and temperature rows, and show "Health not read" chips. Done when: the non-elevated driven test reads the refusal text and finds no health row.
- [ ] Remove the Storage and Board attention dots and show "Needs administrator" on the drive health advice row and on the inspector of a drive part. Done when: the three surfaces read so in the non-elevated run.
- [ ] Wire Restart as administrator through the SDK's elevation helper, passing the current section. Done when: the elevated instance opens on Storage and the first instance exits. Cheaper substitute: a private `ShellExecute` of `runas`, which the suite forbids.
- [ ] Keep working when the prompt is declined: say so once in the status bar and Activity. Done when: declining leaves the window as it was with one Refused record.
- [ ] Cover it in `tests/standarduser_test.cpp` with a fake rights level. Done when: `ctest --preset debug -L rights` passes, and fails when a health row is shown without a reading.
- [ ] Commit: `ui: an honest refusal for a standard user, and a restart as administrator`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L rights` passes for the standard-user and administrator fixtures.

## 37. Snapshots Section

The list of saved snapshots: take one, select two, open the folder, delete one after a confirmation that says what is lost.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` section 5 (SN-1 to SN-8, W-5) and states S-3 and S-4, against the `snapshots`, `state-no-snapshots` and `state-delete-confirmation` captures.
**Job:** a person saves the computer's state today and manages what they saved. Consumer: the list, read back against the files in the snapshot folder.
**Treatment:** the list is the folder's real contents, Delete names the file, its size and its note and states it cannot be undone, and Cancel has the focus. Cheaper substitute that fails the checkpoint: a generic "Are you sure?".
**Chrome:** the SDK's list, checkbox, button, dialog and empty state. No control of Busview's own.

**Build order:**

1. Build `src/ui/SnapshotsView.cpp` listing the folder. Done when: the list equals the folder's snapshot files.
2. Wire take, select, open and delete. Done when: each change is read back from the folder.

- [ ] List the snapshot folder's files (SN-4) in `src/ui/SnapshotsView.cpp` with date, note and size, re-read after every change, and show the count in the sidebar (W-5). Done when: adding a file to the folder and refreshing shows it.
- [ ] Implement selection of two (SN-5) and the unavailable Compare selected with its tooltip (SN-2). Done when: selecting a third drops the older and Compare selected is available only with two.
- [ ] Wire Take snapshot (SN-3) with an optional note, and Open folder (SN-1). Done when: the new file appears in the list and reads back.
- [ ] Build the delete confirmation (SN-6, S-4): the snapshot's date, "1 file", its size and note, "This cannot be undone." in bold, Cancel focused, Delete snapshot as the destructive button. Done when: confirming removes the file and the row and adds one Activity record, and cancelling changes nothing. Cheaper substitute: deleting on the first click.
- [ ] Show the empty state (SN-8, S-3) and the folder line (SN-7). Done when: an empty folder shows "No snapshots yet" with Take snapshot.
- [ ] Refuse a file in the folder that is not a readable snapshot with its reason in the row, without hiding it. Done when: a damaged fixture file is listed as "Not readable" and cannot be selected.
- [ ] Cover it in `tests/snapshotsview_test.cpp` with a temporary folder. Done when: `ctest --preset debug -L snapshots-view` passes, and fails when Delete skips the confirmation.
- [ ] Commit: `ui: the Snapshots section, with a confirmation that says what is lost`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L snapshots-view` passes: take, select, delete with confirmation, cancel, and the empty state.

## 38. Compare View

The comparison of two snapshots: a summary and one row per changed value.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` section 5 (CP-1 to CP-4), against the `state-compare` captures.
**Job:** a person sees what changed in their computer between two dates and which change matters. Consumer: the rows, read back against the compare engine's result.
**Treatment:** the old reading struck through and the new in bold, each change classed with an icon and a word, the count unchanged stated. Cheaper substitute that fails the checkpoint: two snapshots shown side by side with no differences marked.
**Chrome:** the SDK's content header, button, list and chip. No control of Busview's own.

**Build order:**

1. Build `src/ui/CompareView.cpp` from `Compare`'s result. Done when: the fixture pair shows the design's six rows.
2. Wire Back and Export differences. Done when: the exported file reads back with six differences.

- [ ] Build the summary (CP-3) and the differences list (CP-4) in `src/ui/CompareView.cpp`, running the comparison off the UI thread. Done when: the rows equal the engine's result for the fixture pair, with Watch, Changed and Expected chips.
- [ ] Wire Back to snapshots (CP-1) keeping the selection, and Export differences (CP-2) through `Report::WriteDifferences`. Done when: the export reads back and the status bar names the file.
- [ ] Show the two-computer refusal as a sentence with a "Compare anyway" action. Done when: the fixtures of two computers show it and the action shows the differences.
- [ ] Show "No differences" with the count unchanged when the two are equal. Done when: comparing a snapshot with a copy of itself shows it.
- [ ] Cover it in `tests/compareview_test.cpp`. Done when: `ctest --preset debug -L compare-view` passes, and fails when a Watch row loses its chip.
- [ ] Commit: `ui: the comparison of two snapshots`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L compare-view` passes for the design's pair, the equal pair and the two-computer pair.

## 39. Beep Codes Section

The beep codes: a search, a maker filter that starts on this computer's BIOS maker, the list, and the meaning with what to try.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` section 6 (BC-1 to BC-6) and state S-5, against the `beep-codes`, `state-beep-all-makers` and `state-beep-no-match` captures.
**Job:** a person who heard beeps at start-up finds the pattern and reads what it means and what to try. Consumer: the list and the panel, read back against the lookup.
**Treatment:** the filter starts on the detected maker and says so, results name their maker, and no match gets a sentence of help and a way back. Cheaper substitute that fails the checkpoint: an empty list with no explanation.
**Chrome:** the SDK's search box, filter, list and button. No control of Busview's own.

**Build order:**

1. Build `src/ui/BeepView.cpp` over `BeepCodes`. Done when: the list shows a maker's codes and the panel the selected code's meaning.
2. Wire the search and the detected maker. Done when: typing narrows the list and the filter starts on the BIOS maker.

- [ ] Build the list (BC-3) and the meaning panel (BC-4, BC-5) in `src/ui/BeepView.cpp`: maker, pattern, meaning, "What to try" as numbered steps, Copy. Done when: selecting AMI "3 short" shows its meaning and steps, and Copy puts them on the clipboard.
- [ ] Build the maker filter (BC-2) starting on `MakerMatch` of the BIOS vendor and marking it "(this computer)", or on All when there is no match. Done when: the AMI fixture starts on AMI with the mark and an unknown vendor starts on All with none.
- [ ] Wire the search box (BC-1) to `BeepCodes::Search` as the user types, with Ctrl+F focusing it. Done when: typing `1 long 2 short` under All lists every maker's entry.
- [ ] Show the no-match state (BC-6, S-5) with the text quoted and Clear search. Done when: `zzz` shows it and Clear search restores the list.
- [ ] Set the status bar to the count shown of the total and the maker. Done when: it reads "15 of 177 codes shown, AMI" for the AMI filter.
- [ ] Cover it in `tests/beepview_test.cpp`. Done when: `ctest --preset debug -L beep-view` passes, and fails when the filter ignores the detected maker.
- [ ] Commit: `ui: the Beep codes section`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L beep-view` passes: filter start, search, selection, copy and no match.

## 40. Activity Section

What the tool did, newest first: the readable face of its log.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` section 7 (AC-1, AC-2), against the `activity` captures.
**Job:** a person sees what Busview did and when, without opening a log file. Consumer: the list, read back against the log.
**Treatment:** one line per action, newest first, the time in monospace and the outcome as an icon and a word. Cheaper substitute that fails the checkpoint: the raw log file in a text box.
**Chrome:** the SDK's list, chip and button, and the framework's log.

**Build order:**

1. Show `ActivityLog`'s records in `src/ui/ActivityView.cpp`. Done when: the list matches the log line for line.
2. Wire Open log file and Copy. Done when: both work on the real log.

- [ ] Build `src/ui/ActivityView.cpp` listing the records newest first with the outcome chips Done, Started, Skipped, Refused and Failed. Done when: after a scan the list shows one line per reader in the right order.
- [ ] Write the same records to the framework's log file from `ActivityLog`. Done when: a test compares the list with the log file and finds them equal. Cheaper substitute: writing the log and the list separately, which lets them disagree.
- [ ] Wire Open log file and Copy (AC-2). Done when: Copy puts every line on the clipboard as text.
- [ ] Show an empty state with one sentence before the first action. Done when: a fixture with no records shows it.
- [ ] Cover it in `tests/activityview_test.cpp`. Done when: `ctest --preset debug -L activity` passes, and fails when a record is dropped from the list.
- [ ] Commit: `ui: the Activity section, the log made readable`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L activity` passes and the list equals the log's lines after a driven run.

## 41. Settings and About Sections

The framework's Settings and About pages hosted in the window, with one page of Busview's own options.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** `design/SPEC.md` section 7 (SE-1 to SE-9, AB-1), against the `settings-general`, `settings-busview`, `settings-logging` and `about` captures.
**Job:** a person changes theme, density, language, logging and Busview's own options, and sees what version they run. Consumer: the framework's settings file, read back.
**Treatment:** the framework's own pages, and Busview's options declared to the framework so it stores them. Cheaper substitute that fails the checkpoint: a private settings page writing its own file.
**Chrome:** the framework's Preferences pages and About page. One page of Busview's own, for the options `design/SPEC.md` names.

**Build order:**

1. Write `src/Descriptor.h` and host the framework's pages in `src/ui/SettingsView.cpp` and `src/ui/AboutView.cpp`. Done when: a changed setting is read back from the framework's file.
2. Declare Busview's page. Done when: each of its options is stored by the framework and consumed.

- [ ] Write `src/Descriptor.h`: the tool's name, tagline, version source, licence (GPL v3), website, source address and update address, and no behaviour. Done when: the framework builds About (AB-1) from it, with the database version, the rights level and "Kernel driver: none" as extra rows.
- [ ] Host the framework's General and Logging pages (SE-1 to SE-5) in `src/ui/SettingsView.cpp`. Done when: changing the theme changes the window and survives a restart. Cheaper substitute: a settings writer in Busview.
- [ ] Declare Busview's page to the framework: Explain each value (SE-6), Sizes (SE-7), Snapshot folder (SE-8) and Hide serial numbers in exports (SE-9, on by default). Done when: each is stored in the framework's file and read back after a restart.
- [ ] Consume each option: Explain in the area sections, Sizes in every capacity reading, the folder in the snapshot writer, masking in every export. Done when: switching Sizes to GiB changes "500 GB" to "465 GiB" in Storage and in a new report.
- [ ] Refuse a snapshot folder that cannot be written, naming it and keeping the old one. Done when: choosing a read-only folder shows the sentence and the setting is unchanged.
- [ ] Cover it in `tests/settings_test.cpp` with a fixture settings file. Done when: `ctest --preset debug -L settings` passes, and fails when an option is stored and not consumed.
- [ ] Commit: `ui: Settings and About from the framework, and Busview's own options`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L settings` passes, and each of Busview's four options is read back and consumed after a restart.

## 42. Accessibility and Fidelity Pass

The whole window against the contract: every control of `design/SPEC.md` accounted for, every action by keyboard, every control named, in both themes and high contrast at every scale.

**Phase:** 4
**Needs:** windows-host, display-session, sdk-framework
**Surface:** yes
**Fidelity:** every ID in `design/SPEC.md` and rules X-1 to X-4 and X-10, against every file in `design/captures/`.
**Job:** a person who uses only a keyboard or a screen reader can do everything, and the built window is the designed one. Consumer: a UI Automation walk and a control-by-control comparison.
**Treatment:** a written inventory of every ID with its state in the built window, and captures of the built window beside the design's. Cheaper substitute that fails the checkpoint: a visual glance at two screenshots.
**Chrome:** no new control; this section fixes what the pass finds in the sections that own it.

**Build order:**

1. Write `tests/spec_coverage_test.cpp` walking the window for every ID. Done when: each ID of `design/SPEC.md` is found or reported missing by name.
2. Capture the built window and fix what differs. Done when: `docs/fidelity.md` lists every ID as built.

- [ ] Give every control an automation ID equal to its `design/SPEC.md` ID and write `tests/spec_coverage_test.cpp` parsing the IDs from `design/SPEC.md` and finding each through UI Automation. Done when: `ctest --preset debug -L spec` passes, and fails naming the ID when a control is removed.
- [ ] Drive every action by keyboard alone in `tests/keyboard_test.cpp`: tab order follows visual order and focus is visible (X-1). Done when: the test completes take snapshot, compare, delete, a beep search and a part selection with no mouse input.
- [ ] Check accessible names and announcements (X-2) and that every chip has an icon and a word (X-3). Done when: a UI Automation walk finds no unnamed control and the scan's end raises a notification event.
- [ ] Capture the built window for every name `python design/capture.py --list` prints to `docs/captures/`, in light, dark and high contrast at 100, 125, 150 and 200 percent (X-10), with a provenance file. Done when: the captures are committed.
- [ ] Compare each built capture with its design capture control by control and record the result per ID in `docs/fidelity.md`, fixing each difference in the section that owns the control. Done when: `docs/fidelity.md` lists every ID as built, or as a deliberate difference with its reason and the contract updated. Cheaper substitute: editing `design/SPEC.md` to match what was built without saying why.
- [ ] Check truncation and tooltips (X-4) at the minimum window size. Done when: no text is clipped without an ellipsis and a tooltip.
- [ ] Commit: `ui: every control of the contract is built, named and keyboard-driven`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L spec` and `-L keyboard` pass, and `docs/fidelity.md` lists every ID of `design/SPEC.md`.

## 43. Database Update Check

The database updates separately from the program. Check for update fetches a small manifest from the Busview repository's releases, downloads a newer database, verifies it and swaps it in.

**Phase:** 5
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Implement `DatabaseUpdate` in `src/db/DatabaseUpdate.cpp`. Done when: a newer manifest on a local test server leads to a verified, swapped database.
2. Refuse every bad case. Done when: a wrong hash, an older version and an offline machine each leave the current database in place.

- [ ] Define the manifest (`busview-db.json`: data version, schema version, size, SHA-256, address) and have `tools/build_db.py` write it beside the database. Done when: the manifest's hash equals the built file's.
- [ ] Implement `DatabaseUpdate::Check()` and `Apply()` in `src/db/DatabaseUpdate.cpp` with WinHTTP over HTTPS only, downloading to a temporary file. Done when: against a local test server the newer file is downloaded.
- [ ] Verify the size and SHA-256, open the file with `Database::Open`, and only then replace the current database, keeping the previous one as `busview.db.previous`. Done when: a file with a wrong hash is deleted and the current database is untouched. Cheaper substitute: replacing first and checking after.
- [ ] Refuse a manifest whose schema version the tool does not know, and report "already up to date", "no connection" and "update failed" each in its own sentence. Done when: four cases return four reasons.
- [ ] Never check without being asked. Done when: a test with a counting test server sees zero requests during start-up and a scan.
- [ ] Cover it in `tests/dbupdate_test.cpp` with a loopback test server ended with its whole process tree at teardown. Done when: `ctest --preset debug -L dbupdate` passes, and fails when the hash check is removed.
- [ ] Commit: `db: check for a newer database, verify it, then swap it in`

**Test checkpoint:** `sdk\reskit\cmake\bin\ctest.exe --preset debug -L dbupdate` passes for the update, the wrong hash, the unknown schema and no connection.

## 44. Language Pack and Strings

Every user-facing string resolves from the suite's language pack. Until the framework exists the strings live in `resources/strings/en.json`; this section moves them to the framework's pack format and proves nothing is typed into the code.

**Phase:** 5
**Needs:** windows-host, sdk-framework
**Surface:** no

**Build order:**

1. Convert `resources/strings/en.json` to the framework's pack and load it through the framework. Done when: every string the window shows comes from the pack.
2. Add a check that no user-facing literal is in the code. Done when: it fails on a typed-in label.

- [ ] Convert `resources/strings/en.json` to the framework's English pack with the same keys. Done when: the window shows the same text as before, loaded by the framework.
- [ ] Write `tools/check_strings.py` listing string literals under `src/ui/` that are not keys, and add it to `scripts/check-all.ps1`. Done when: a label typed into `src/ui/OverviewView.cpp` fails the gate (`design/SPEC.md` X-7). Cheaper substitute: reviewing by eye.
- [ ] Make every sentence with a number or a name a pattern with placeholders, never concatenation. Done when: "2 of 4 slots used" is one pack entry with two placeholders.
- [ ] Prove the pack can be translated: add a pseudo-language pack in tests that brackets every string. Done when: a driven run with it shows no unbracketed text.
- [ ] Commit: `strings: every word the user reads comes from the language pack`

**Test checkpoint:** `python tools/check_strings.py` exits 0, and a driven run with the pseudo-language pack shows no unbracketed text.

## 45. Portable Zip and Installer

What ships: a portable zip of the executable and the database, and an Inno Setup installer, both from one command, with one version.

**Phase:** 5
**Needs:** windows-host
**Surface:** no

**Build order:**

1. Write `scripts/release.ps1` producing the portable folder and its zip. Done when: the zip unpacks to a folder that runs on a machine with nothing else installed.
2. Add the installer from `installer/Busview.iss`. Done when: install, start and uninstall work and leave the user's snapshots.

- [ ] Derive the version from the git tag at build time into the version resource and the descriptor. Done when: the executable's file version, its About page and `--version` agree.
- [ ] Write `scripts/release.ps1` building Release, running `scripts/check-all.ps1`, and writing `dist/Busview-<version>-portable.zip` with `Busview.exe`, `busview.db`, `LICENSE` and the documents, plus SHA-256 sums. Done when: the zip runs from an empty folder on a clean Windows machine. Cheaper substitute: testing from the build tree, which proves it compiles, not that it ships.
- [ ] Write `installer/Busview.iss` for Inno Setup: per-user install by default, a Start menu entry, an uninstaller, no bundled software. Done when: `dist/Busview-<version>-setup.exe` installs and starts.
- [ ] Leave the user's files on uninstall: snapshots, settings and logs stay, and the uninstaller says so. Done when: after uninstall `Documents\Busview\Snapshots` still holds its files.
- [ ] Keep portable mode honest: when a `portable` marker file is beside the executable, settings and crash files stay in that folder. Done when: a portable run writes nothing under `%LOCALAPPDATA%`.
- [ ] Publish the database and its manifest as release assets for §43. Done when: `scripts/release.ps1` writes `busview.db` and `busview-db.json` to `dist/`.
- [ ] Commit: `release: a portable zip and an installer from one command`

**Test checkpoint:** `pwsh scripts/release.ps1` writes the zip, the installer, the database assets and the sums, and the zip's `Busview.exe --snapshot` works from an empty folder.

## 46. User Guide and Release Documents

The documents a release owes: a user guide covering every section, a changelog, and a README that matches what shipped.

**Phase:** 5
**Needs:** none
**Surface:** no

**Build order:**

1. Write `docs/guide.md` from the built window. Done when: every section and action of `design/SPEC.md` has its paragraph.
2. Write `CHANGELOG.md` and bring `README.md` up to date. Done when: no statement in the README is about a plan.

- [ ] Write `docs/guide.md`: one heading per section of the window, each action, each state, what needs administrator rights, where files go, and what Busview never does. Done when: every section name of `design/SPEC.md` W-2 is a heading.
- [ ] Write `CHANGELOG.md` for 1.0.0 from the plan's shipped sections. Done when: each feature of the README's version 1 list has a line.
- [ ] Update `README.md` from "planned" to what shipped: screenshots from `docs/captures/`, the download, and the limits. Done when: the status line names the released version. Cheaper substitute: leaving the planning README beside a released tool.
- [ ] State the limits plainly in the guide: firmware data quality, soldered memory, schematic board positions, no sensors. Done when: each limit of the README's "Known limits" appears in the guide.
- [ ] Commit: `docs: the user guide, the changelog and a README that matches the release`

**Test checkpoint:** `python scripts/todo-graph.py validate` exits 0, and a search of `docs/guide.md` finds a heading for every section name in `design/SPEC.md` W-2.

## 47. Code Signing of Releases

Releases are signed with Rizonesoft's existing certificate and process, the same as other Resolute releases. The certificate is a credential, so the operator does this.

**Phase:** 99
**Needs:** operator
**Surface:** no

**Build order:**

1. Sign `Busview.exe` and the installer in `scripts/release.ps1 -Sign`. Done when: both carry a valid signature naming Rizonesoft.
2. Record the process in `docs/release.md`. Done when: the steps are written without any secret.

- [ ] Add a `-Sign` switch to `scripts/release.ps1` that signs the executable before it is zipped and the installer after it is built, reading the certificate from the store the operator's process already uses. Done when: `Get-AuthenticodeSignature` reports `Valid` for both files. Cheaper substitute: signing only the installer, which leaves the portable executable unsigned.
- [ ] Timestamp both signatures. Done when: the signature shows a timestamp countersignature.
- [ ] Write `docs/release.md`: the release steps in order, where the certificate lives by name only, and how to verify a download. Done when: the file holds no secret value and a reader can verify a signature from it.
- [ ] Commit: `release: signed with Rizonesoft's certificate`

**Test checkpoint:** `Get-AuthenticodeSignature dist\Busview-*-setup.exe` reports `Valid` with a timestamp, and the same for the `Busview.exe` inside the portable zip.

## 48. Name Clearance Before the First Release

The README's search on 2026-11-17 found no current product called Busview in this category and one cancelled United States trademark. That was a search, not a clearance. The owner decides before the first public release whether the name stands.

**Phase:** 99
**Needs:** owner-decision
**Surface:** no

**Build order:**

1. Record what was checked in `docs/decisions/name-clearance.md`. Done when: the trademark, domain and package-name findings are written with their dates.
2. Record the owner's decision there. Done when: the file states the decision and who made it.

- [ ] Record in `docs/decisions/name-clearance.md` the trademark searches (United States, European Union, United Kingdom), the domain availability and the name's use on GitHub, winget and the Microsoft Store, each with its date and source. Done when: each line has a source a reader can open.
- [ ] Record the owner's decision: keep Busview, or the name that replaces it. Done when: the file states it with the date. Cheaper substitute: releasing under the name with the question open.
- [ ] Commit: `decision: the name is cleared for release, or replaced`

**Test checkpoint:** `python scripts/todo-graph.py validate` exits 0 and `docs/decisions/name-clearance.md` states the owner's decision with its date.

## Verification

- On a real computer `Busview.exe` reads every area the machine has, gives its four pieces of advice, takes a snapshot, compares two, and finds a beep code, in light and dark, by keyboard alone.
- `docs/fidelity.md` lists every ID of `design/SPEC.md` as built, and `sdk\reskit\cmake\bin\ctest.exe --preset debug -L spec` passes.
- A masked report of that computer holds none of its serial numbers, MAC addresses, its name or its UUID.
- `pwsh scripts/check-all.ps1` passes, and the portable zip runs from an empty folder on a machine with nothing else installed.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
