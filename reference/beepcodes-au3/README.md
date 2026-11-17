# The AutoIt BiosCodes source

This folder is the part of Rizonesoft's AutoIt tool BiosCodes that Busview's beep codes are taken from. It is frozen: read, never edited. Changing a file here changes what the extraction in `tools/extract_beepcodes.py` (D00 T01 §28) has to reproduce.

| Path | What it is |
| --- | --- |
| `src/BiosCodes.au3` | The script. Its display functions (`:783-1263`) map each manufacturer's beep pattern to a text by index |
| `src/Includes/Localization.au3` | The 246 indexed texts and their English defaults (`:119-395`) |
| `Language/en.lng`, `de.lng`, `ko.lng` | The shipped language packs. The English pack is UTF-16 and its `[BeepInformation]` section carries 244 of the 246 texts |

The original holds 177 codes: AMI 15, AST 19, Award 5, Compaq 7, Dell 7, IBM 10 and Phoenix 114.

The scripts cannot be compiled from this folder alone: they include the suite's shared AutoIt framework, which is not here. That does not matter for Busview, which reads them for the data.

BiosCodes was a separate tool of the Resolute suite until 2026-11-17, when it was folded into Busview. The code is Rizonesoft's own, under GPL v3.
