#!/usr/bin/env python3
"""Capture every screen and state of the interface design to design/captures/, in light and dark.

    python design/capture.py            write every capture
    python design/capture.py --list     print the capture names and the address each is taken from

Each capture is the application window alone, 1180 by 748, taken from design/busview-interface.html in headless
Microsoft Edge (or Chrome). design/SPEC.md names these files screen by screen. Standard library only.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DESIGN = Path(__file__).resolve().parent
PAGE = DESIGN / "busview-interface.html"
OUT = DESIGN / "captures"
SIZE = "1180,748"
TIMEOUT = 60

# name -> query. Every section, then every state SPEC.md describes.
SECTIONS = {
    "overview": "view=overview", "board": "view=map", "memory": "view=memory", "processor": "view=processor",
    "motherboard": "view=board", "storage": "view=storage", "graphics": "view=graphics", "devices": "view=devices",
    "network-and-power": "view=network", "snapshots": "view=snapshots", "beep-codes": "view=beeps",
    "activity": "view=activity", "settings-general": "view=settings&page=general",
    "settings-busview": "view=settings&page=busview", "settings-logging": "view=settings&page=logging", "about": "view=about",
}
STATES = {
    "state-first-scan": "view=overview&state=scan",
    "state-standard-user-storage": "view=storage&state=user",
    "state-standard-user-board": "view=map&part=sata1&state=user",
    "state-no-snapshots": "view=snapshots&state=nosnap",
    "state-delete-confirmation": "view=snapshots&state=dialog",
    "state-compare": "view=snapshots&compare=1",
    "state-beep-no-match": "view=beeps&state=nomatch",
    "state-beep-all-makers": "view=beeps&maker=All",
    "state-explain-memory": "view=memory&explain=1",
    "state-board-free-slot": "view=map&part=m2-2",
    "state-board-watch": "view=map&part=sata1",
}


def browser() -> str:
    for path in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                 r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        if Path(path).is_file():
            return path
    found = shutil.which("msedge") or shutil.which("chrome") or shutil.which("chromium")
    if not found:
        sys.exit("capture: Microsoft Edge or Chrome is needed and neither was found")
    return found


def captures() -> dict[str, str]:
    shots = {}
    for theme in ("light", "dark"):
        for name, query in {**SECTIONS, **STATES}.items():
            shots[f"{name}-{theme}.png"] = f"{PAGE.as_uri()}?{query}&theme={theme}&capture=1"
    return shots


def shoot(exe: str, url: str, target: Path, profile: str) -> None:
    command = [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={SIZE}", "--force-device-scale-factor=1",
               f"--user-data-dir={profile}", "--virtual-time-budget=4000", f"--screenshot={target}", url]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        process.wait(timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        # The browser starts children of its own: end the whole tree, never only the process started here.
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            process.kill()
        sys.exit(f"capture: the browser did not finish {target.name} in {TIMEOUT} seconds")
    if not target.is_file() or target.stat().st_size < 2000:
        sys.exit(f"capture: {target.name} was not written")


def main() -> int:
    shots = captures()
    if "--list" in sys.argv[1:]:
        for name, url in shots.items():
            print(f"{name}\t{url.split('?', 1)[1]}")
        return 0
    exe = browser()
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="busview-capture-") as profile:
        for name, url in shots.items():
            shoot(exe, url, OUT / name, profile)
            print(f"capture: wrote {name}")
    print(f"capture: {len(shots)} capture(s) in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
