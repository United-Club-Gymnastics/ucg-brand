"""Rebuild the Club Spirit icon so every figure keeps its outline.

The asset board draws the crowd as overlapping figures with an outline around each one.
A plain one-color recolor (what extract_icons.py does) merges them into a blob, so this
script redraws them from the extracted geometry:

- club-spirit-original: Light Blue figures with Navy outlines, Light Blue rays and base
  (the toolkit's Team_Spirit_Icon.png look).
- club-spirit-navy / -light / -white: one-color line art. Each figure is an outline with a
  see-through middle that still hides the figures behind it; rays and base are solid.

PNGs are rendered with Chrome (Playwright) because PyMuPDF ignores SVG masks.
Run after extract_icons.py:  python tools/club_spirit.py
"""
import re
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

DIR = Path(__file__).resolve().parent.parent / "assets" / "icons" / "event"
INKS = {"navy": "#1E2B38", "light": "#DBEBEE", "white": "#FFFFFF"}
NAVY, LIGHT = "#1E2B38", "#DBEBEE"

src = (DIR / "club-spirit-navy.svg").read_text(encoding="utf-8")
src = re.sub(r"<defs>.*?</defs>", "", src, flags=re.S)  # a rebuilt file: read its visible paths (rerunnable)
head = re.match(r"<svg[^>]*>", src).group(0)
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', head).group(1).split()]
paths = []
for m in re.finditer(r"<path ([^>]*?) d=\"([^\"]*)\"[^>]*/>", src):
    attrs, d = m.group(1), m.group(2)
    w = re.search(r'stroke-width="([^"]+)"', attrs)
    cap = re.search(r'stroke-linecap="([^"]+)"', attrs)
    paths.append({"d": d, "w": float(w.group(1)) if w else 0, "cap": cap.group(1) if cap else "butt",
                  "evenodd": "evenodd" in attrs})
# board order: the base, then the figures back to front, then the rays (stroked lines)
base, figures, rays = paths[0], [p for p in paths[1:] if p["w"] < 9], [p for p in paths[1:] if p["w"] >= 9]
if len(figures) != 15 or len(rays) != 8:
    raise SystemExit(f"unexpected club-spirit geometry: {len(figures)} figure parts, {len(rays)} rays")


def rule(p):
    return ' fill-rule="evenodd"' if p["evenodd"] else ""


def ray_paths(color):
    return "".join(f'<path fill="none" stroke="{color}" stroke-width="{p["w"]:.2f}" stroke-linecap="{p["cap"]}" d="{p["d"]}"/>' for p in rays)


def original():
    figs = "".join(f'<path fill="{LIGHT}"{rule(p)} stroke="{NAVY}" stroke-width="{p["w"]:.2f}" stroke-linejoin="round" d="{p["d"]}"/>' for p in figures)
    return f'{head}\n<path fill="{LIGHT}" d="{base["d"]}"/>{figs}{ray_paths(LIGHT)}\n</svg>\n'


def line_art(ink):
    x, y, w, h = vb
    defs, body = [], []
    # everything in front of part i hides part i (mask cs0 is the base's)
    for i in range(len(figures) + 1):
        front = figures[i:]
        if not front:
            break
        # cut inside the front part's outline (not at its outer edge) so no hairline seam shows
        cut = 0 if i == 0 else 0.6
        uses = "".join(f'<path fill="#000"{rule(p)} stroke="#000" stroke-width="{p["w"] * cut:.2f}" stroke-linejoin="round" d="{p["d"]}"/>' for p in front)
        defs.append(f'<mask id="cs{i}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/>{uses}</mask>')
    body.append(f'<path fill="{ink}" d="{base["d"]}" mask="url(#cs0)"/>')
    for i, p in enumerate(figures):
        m = f' mask="url(#cs{i + 1})"' if i + 1 < len(figures) else ""
        body.append(f'<path fill="none"{rule(p)} stroke="{ink}" stroke-width="{p["w"]:.2f}" stroke-linejoin="round" d="{p["d"]}"{m}/>')
    return f'{head}\n<defs>{"".join(defs)}</defs>\n{"".join(body)}{ray_paths(ink)}\n</svg>\n'


files = {"club-spirit-original.svg": original()}
for name, ink in INKS.items():
    files[f"club-spirit-{name}.svg"] = line_art(ink)
for name, svg in files.items():
    (DIR / name).write_text(svg, encoding="utf-8")

# 512px-tall transparent PNGs, matching tools/icon_pngs.py
with sync_playwright() as pw, tempfile.TemporaryDirectory() as tmp:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 512})
    for name in files:
        html = Path(tmp) / "p.html"
        html.write_text(f'<body style="margin:0;background:transparent"><img id="i" src="{(DIR / name).as_uri()}" style="height:512px;display:block">', encoding="utf-8")
        pg.goto(html.as_uri())
        pg.wait_for_function("document.getElementById('i').complete")
        pg.locator("#i").screenshot(path=str(DIR / name.replace(".svg", ".png")), omit_background=True)
    b.close()
print("rebuilt", len(files), "club-spirit SVG + PNG pairs")
