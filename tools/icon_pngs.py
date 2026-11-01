"""Render every icon SVG in assets/icons to a 512px-tall transparent PNG next to it
(Google Slides, Docs and Sheets can't insert SVG). Usage: python tools/icon_pngs.py"""
from pathlib import Path
import fitz

ICONS = Path(__file__).resolve().parent.parent / "assets" / "icons"
n = 0
for svg in sorted(ICONS.glob("*/*.svg")):
    if svg.name.startswith("club-spirit"):  # uses SVG masks; tools/club_spirit.py renders these
        continue
    page = fitz.open(svg)[0]
    z = 512 / page.rect.height
    page.get_pixmap(matrix=fitz.Matrix(z, z), alpha=True).save(svg.with_suffix(".png"))
    n += 1
print("rendered", n, "PNGs")
