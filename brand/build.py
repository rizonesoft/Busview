#!/usr/bin/env python3
"""Build Busview's brand assets: the icon, its renders, the Windows icon, the wordmarks, both banners and the avatar.

    python brand/build.py            write every asset under brand/
    python brand/build.py --check    exit 1 when a tracked asset differs from what this script builds

The mark was chosen by the owner on 2026-11-17 from three directions: Package, the letter B drawn as a chip package
(a stem, two bowls and three pins down its left side). DESIGN.md section 1 describes it; this file is the drawing.
The fonts are beside this file under the SIL Open Font License, so a render never depends on what a machine has
installed. Needs resvg_py and Pillow (`pip install resvg_py pillow`).
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import resvg_py
from PIL import Image, ImageFont

BRAND = Path(__file__).resolve().parent
FONTS = BRAND / "fonts"
FONT_FILES = [str(p) for p in sorted(FONTS.glob("*.ttf"))]

SLUG, NAME = "busview", "Busview"
TAGLINE = "See what is inside. Know what to do next."
CREDIT = "A Resolute tool by Rizonesoft"
READS = ("SMBIOS", "CPUID", "PCI", "USB", "SMART", "EDID")   # what Busview reads, along the foot of the social preview

# The palette. DESIGN.md section 1 carries the same values.
MINT, EMERALD, PINE = "#5CF0B4", "#12B981", "#0A7F6B"     # the mark: lit face, body, shaded face
GROUND, GROUND_HI, MUTED = "#06120E", "#0C2A20", "#B4DCCB"  # banner ground, its lighter corner, secondary text on it
PAPER, INK = "#F4F7F5", "#0B1512"                           # text on dark, text on light

ICO_SIZES = (16, 20, 24, 32, 40, 48, 64, 96, 128, 256)
SMALL_BELOW = 40   # the size under which the simplified drawing is used
WORD = (("Bus", "Sora-SemiBold.ttf", 600), ("view", "Sora-Light.ttf", 300))   # the name in two weights
TRACKING = -0.035

# The mark's two gradients, in its own 96 units: the lit parts (pins, upper bowl) and the shaded parts (stem, lower bowl).
GRADIENTS = (f'<defs><linearGradient id="lit" gradientUnits="userSpaceOnUse" x1="8" y1="12" x2="74" y2="52">'
             f'<stop offset="0" stop-color="{MINT}"/><stop offset="1" stop-color="{EMERALD}"/></linearGradient>'
             f'<linearGradient id="shade" gradientUnits="userSpaceOnUse" x1="26" y1="16" x2="78" y2="84">'
             f'<stop offset="0" stop-color="{EMERALD}"/><stop offset="1" stop-color="{PINE}"/></linearGradient></defs>')
# The icon on a 96-unit grid, free-standing: it reads on a light and on a dark ground with no tile behind it.
LARGE = (GRADIENTS + '<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M8 30 H16 M8 48 H16 M8 66 H16" stroke="url(#lit)" stroke-width="7"/>'
         '<path d="M32 16 H54 A16 16 0 0 1 54 48 H32" stroke="url(#lit)" stroke-width="11"/>'
         '<path d="M32 48 H60 A16 16 0 0 1 60 80 H32" stroke="url(#shade)" stroke-width="11"/>'
         '<path d="M32 16 V80" stroke="url(#shade)" stroke-width="11"/></g>')
# The drawing used below 40 pixels: no pins, heavier strokes.
SMALL = (GRADIENTS + '<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M24 18 H48 A15 15 0 0 1 48 48 H24" stroke="url(#lit)" stroke-width="15"/>'
         '<path d="M24 48 H54 A15 15 0 0 1 54 78 H24" stroke="url(#shade)" stroke-width="15"/>'
         '<path d="M24 18 V78" stroke="url(#shade)" stroke-width="15"/></g>')


def svg(width: int, height: int, body: str, label: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'role="img" aria-label="{label}">{body}</svg>\n')


def placed(inner: str, x: float, y: float, size: float) -> str:
    """A 96-unit drawing placed at x, y and scaled to `size`."""
    return f'<g transform="translate({x} {y}) scale({size / 96})">{inner}</g>'


def text_width(text: str, font: str, size: float, tracking_em: float = 0.0) -> float:
    face = ImageFont.truetype(str(FONTS / font), 1000)
    return (face.getlength(text) / 1000 + tracking_em * len(text)) * size


def name_text(x: float, baseline: float, size: float, ink: str) -> tuple[str, float]:
    """The name, Bus in semibold and view in light. Returns the markup and its width."""
    spans = "".join(f'<tspan font-weight="{weight}">{text}</tspan>' for text, _, weight in WORD)
    width = sum(text_width(text, file, size, TRACKING) for text, file, _ in WORD)
    return (f'<text x="{x:.1f}" y="{baseline:.1f}" font-family="Sora" font-size="{size}" '
            f'letter-spacing="{TRACKING * size:.2f}" fill="{ink}">{spans}</text>'), width


def render(markup: str, width: int | None = None, zoom: float | None = None) -> bytes:
    return bytes(resvg_py.svg_to_bytes(svg_string=markup, width=width, zoom=zoom, font_files=FONT_FILES, skip_system_fonts=True,
                                       text_rendering="geometric_precision", shape_rendering="geometric_precision"))


def ico(large: str, small: str) -> bytes:
    """Every size rendered from the vector, never scaled from a bitmap: the small drawing below 40 pixels."""
    frames = [Image.open(io.BytesIO(render(small if size < SMALL_BELOW else large, size))).convert("RGBA") for size in ICO_SIZES]
    out = io.BytesIO()
    frames[-1].save(out, format="ICO", sizes=[(s, s) for s in ICO_SIZES], append_images=frames[:-1])
    return out.getvalue()


def ground(width: int, height: int, cx: float, cy: float) -> str:
    """The banner ground: a dark green that lightens toward one corner, a glow behind the mark, and a grid of solder
    pads that fades away from it, a few of them lit."""
    step, pads = 32, []
    for row in range(1, height // step + 1):
        for col in range(width // step + 1):
            lit = (col * 7 + row * 13) % 11 == 0
            pads.append(f'<circle cx="{col * step + 16}" cy="{row * step - 16}" r="{3.5 if lit else 2.2}" fill="{MINT}" '
                        f'opacity="{0.6 if lit else 0.22}"/>')
    reach = height * 1.2
    return (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GROUND}"/>'
            f'<stop offset="1" stop-color="{GROUND_HI}"/></linearGradient>'
            f'<radialGradient id="glow" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{height * 0.95:.0f}">'
            f'<stop offset="0" stop-color="{EMERALD}" stop-opacity="0.34"/><stop offset="0.5" stop-color="{PINE}" stop-opacity="0.12"/>'
            f'<stop offset="1" stop-color="{PINE}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="fade" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{reach:.0f}">'
            f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.3" stop-color="#FFFFFF" stop-opacity="0.9"/>'
            f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>'
            f'<mask id="pads"><rect width="{width}" height="{height}" fill="url(#fade)"/></mask></defs>'
            f'<rect width="{width}" height="{height}" fill="url(#bg)"/><rect width="{width}" height="{height}" fill="url(#glow)"/>'
            f'<g mask="url(#pads)">{"".join(pads)}</g>')


def assets() -> dict[str, bytes]:
    big = svg(96, 96, LARGE, f"{NAME} icon")
    little = svg(96, 96, SMALL, f"{NAME} icon, small sizes")
    files = {f"{SLUG}-icon.svg": big.encode("utf-8"), f"{SLUG}-icon-small.svg": little.encode("utf-8")}
    for size in (512, 256, 192, 64, 48):
        files[f"{SLUG}-icon-{size}.png"] = render(big, size)
    for size in (32, 16):
        files[f"{SLUG}-icon-{size}.png"] = render(little, size)
    files[f"{SLUG}.ico"] = ico(big, little)

    def wordmark(ink: str) -> str:
        text, width = name_text(86, 57, 42, ink)
        return svg(int(86 + width + 12), 80, placed(LARGE, 8, 8, 64) + text, NAME)

    # The README banner: the name and tagline on the left, the mark in its glow on the right.
    text, _ = name_text(88, 160, 68, PAPER)
    banner = svg(1280, 320, ground(1280, 320, 1060, 160) + text
                 + f'<text x="90" y="212" font-family="Inter" font-size="22" fill="{MUTED}">{TAGLINE}</text>'
                 + placed(LARGE, 976, 76, 168), f"{NAME}. {TAGLINE}")
    # The social preview: the same arrangement, with what Busview reads along the foot.
    text, _ = name_text(96, 286, 108, PAPER)
    x, labels = 98.0, []
    for label in READS:
        labels.append(f'<text x="{x:.0f}" y="548" font-family="Inter" font-weight="500" font-size="17" letter-spacing="2.4" '
                      f'fill="{MUTED}" opacity="0.8">{label}</text>')
        x += text_width(label, "Inter-Medium.ttf", 17, 0.141) + 34
    social = svg(1280, 640, ground(1280, 640, 984, 320) + text
                 + f'<text x="98" y="352" font-family="Inter" font-size="30" fill="{MUTED}">{TAGLINE}</text>'
                 + f'<path d="M98 508 H{x - 34:.0f}" stroke="{MUTED}" stroke-width="1" opacity="0.3"/>' + "".join(labels)
                 + f'<text x="98" y="588" font-family="Inter" font-size="18" fill="{MUTED}" opacity="0.65">{CREDIT}</text>'
                 + placed(LARGE, 800, 136, 368), f"{NAME}. {TAGLINE}")
    avatar = svg(512, 512, ground(512, 512, 256, 256) + placed(LARGE, 96, 96, 320), f"{NAME} avatar")
    sources = {f"{SLUG}-wordmark-light.svg": wordmark(INK), f"{SLUG}-wordmark-dark.svg": wordmark(PAPER),
               "readme-banner.svg": banner, "social-preview.svg": social, "avatar.svg": avatar}
    files.update({key: value.encode("utf-8") for key, value in sources.items()})
    files[f"{SLUG}-wordmark-light.png"] = render(sources[f"{SLUG}-wordmark-light.svg"], zoom=3)
    files[f"{SLUG}-wordmark-dark.png"] = render(sources[f"{SLUG}-wordmark-dark.svg"], zoom=3)
    files["readme-banner.png"] = render(banner, 2560)
    files["social-preview.png"] = render(social, 1280)
    files["avatar.png"] = render(avatar, 512)
    return files


def main() -> int:
    """Write the assets under brand/, or with --check say which tracked asset differs from what is built."""
    files = assets()
    if "--check" in sys.argv[1:]:
        stale = [name for name, data in files.items() if not (BRAND / name).is_file() or (BRAND / name).read_bytes() != data]
        for name in stale:
            print(f"brand: {name} is not what brand/build.py builds; run python brand/build.py")
        print(f"brand: {len(files) - len(stale)} of {len(files)} asset(s) current")
        return 1 if stale else 0
    for name, data in files.items():
        (BRAND / name).write_bytes(data)
        print(f"brand: wrote {name} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
