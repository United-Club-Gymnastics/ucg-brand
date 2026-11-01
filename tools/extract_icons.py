"""Extract each icon on the master asset board ("All UCG Assets.svg") into its own
SVG, plus navy / light / white recolors, by reading the vector paths inside each
labelled white tile. Usage:
  python tools/extract_icons.py "<path to All UCG Assets.svg>"
"""
import json
import sys
from pathlib import Path

import fitz

SRC = sys.argv[1]
OUT = Path(__file__).resolve().parent.parent / "assets" / "icons"
NAVY, LIGHT, WHITE = "#1E2B38", "#DBEBEE", "#FFFFFF"

# label -> (slug, set) by x-range of the label's column on the board
def classify(label, x):
    lab = label.upper()
    if x < 960:  # event icons (left half)
        names = {"MAG": "mag", "T&T": "tnt", "WAG": "wag", "MAG 1": "mag-1", "MAG 2": "mag-2", "MAG 3": "mag-3",
                 "T&T 2": "tnt-2", "WAG 1": "wag-1", "GRADWAG": "wag-grad", "CLUB SPIRIT": "club-spirit"}
        return ("event", names.get(lab))
    disc = "mag" if (x % 840) < 1300 % 840 and False else None
    col = None
    for cx, d in [(1175, "mag"), (1430, "tnt"), (1690, "wag"), (2015, "mag"), (2270, "tnt"), (2530, "wag")]:
        if abs(x - cx) < 130:
            col = d
    variant = "solid" if x < 1900 else "duotone"
    slug = {"FLOOR": "floor", "POMMEL HORSE": "pommel-horse", "RINGS": "rings", "VAULT": "vault", "P BARS": "parallel-bars",
            "HIGH BAR": "high-bar", "TRAMPOLINE": "trampoline", "DOUBLE MINI": "double-mini", "POWER TUMBLING": "power-tumbling",
            "SYNCHRO TRAMP": "synchro", "UNEVEN BARS": "uneven-bars", "BALANCE BEAM": "balance-beam"}.get(lab)
    if not slug or not col:
        return (None, None)
    return ("apparatus-" + variant, f"{col}-{slug}")


def hexcol(rgb):
    return "#%02X%02X%02X" % tuple(round(c * 255) for c in rgb)


def path_d(items):
    d, cur = [], None
    for it in items:
        k = it[0]
        if k == "l":
            p1, p2 = it[1], it[2]
            if cur is None or abs(cur.x - p1.x) > 1e-3 or abs(cur.y - p1.y) > 1e-3:
                d.append(f"M{p1.x:.2f} {p1.y:.2f}")
            d.append(f"L{p2.x:.2f} {p2.y:.2f}")
            cur = p2
        elif k == "c":
            p1, c1, c2, p2 = it[1:5]
            if cur is None or abs(cur.x - p1.x) > 1e-3 or abs(cur.y - p1.y) > 1e-3:
                d.append(f"M{p1.x:.2f} {p1.y:.2f}")
            d.append(f"C{c1.x:.2f} {c1.y:.2f} {c2.x:.2f} {c2.y:.2f} {p2.x:.2f} {p2.y:.2f}")
            cur = p2
        elif k == "re":
            r = it[1]
            d.append(f"M{r.x0:.2f} {r.y0:.2f}H{r.x1:.2f}V{r.y1:.2f}H{r.x0:.2f}Z")
            cur = None
        elif k == "qu":
            q = it[1]
            d.append(f"M{q.ul.x:.2f} {q.ul.y:.2f}L{q.ur.x:.2f} {q.ur.y:.2f}L{q.lr.x:.2f} {q.lr.y:.2f}L{q.ll.x:.2f} {q.ll.y:.2f}Z")
            cur = None
    return " ".join(d)


page = fitz.open(SRC)[0]
labels = []
for b in page.get_text("dict")["blocks"]:
    for l in b.get("lines", []):
        t = " ".join(s["text"] for s in l["spans"]).strip()
        x0, y0, x1, y1 = l["bbox"]
        if y0 > 2340 and len(t) < 20:
            labels.append((t, (x0 + x1) / 2, y0))
drawings = page.get_drawings()
tiles = [d for d in drawings if d.get("fill") and hexcol(d["fill"]) == WHITE and d["rect"].width > 150 and d["rect"].y0 > 2400]

manifest = []
for text, cx, ly in labels:
    kind, slug = classify(text, cx)
    if not slug:
        continue
    # the tile directly above the label
    cands = [t for t in tiles if t["rect"].x0 - 5 <= cx <= t["rect"].x1 + 5 and 0 <= ly - t["rect"].y1 <= 60]
    if not cands:  # the primary event icons are labelled above their tiles
        cands = [t for t in tiles if t["rect"].x0 - 5 <= cx <= t["rect"].x1 + 5 and 0 <= t["rect"].y0 - ly <= 120]
    if not cands:
        print("no tile for", text, cx, ly)
        continue
    tile = min(cands, key=lambda t: abs(ly - t["rect"].y1))["rect"]
    def inked(d):  # a non-white fill or stroke (some limbs are stroked lines)
        f = d.get("fill") and hexcol(d["fill"]) != WHITE
        s = d.get("color") and d.get("width") and hexcol(d["color"]) != WHITE and "s" in d["type"]
        return f or s
    parts = [d for d in drawings if inked(d) and d["rect"] in tile and d["rect"] != tile
             and d["rect"].width < tile.width - 4]
    if not parts:
        print("empty", text)
        continue
    bb = None
    for p in parts:
        r = fitz.Rect(p["rect"])
        if "s" in p["type"] and p.get("width"):
            r = r + (-p["width"] / 2, -p["width"] / 2, p["width"] / 2, p["width"] / 2)
        bb = r if bb is None else bb | r
    pad = max(bb.width, bb.height) * 0.04
    vb = (bb.x0 - pad, bb.y0 - pad, bb.width + 2 * pad, bb.height + 2 * pad)
    fills = sorted({hexcol(p[k]) for p in parts for k in ("fill", "color") if p.get(k) and (k == "fill" or "s" in p["type"])})

    def svg(recolor=None):
        recolor = recolor or {}
        body = []
        for p in parts:
            attrs = []
            if p.get("fill") and "f" in p["type"]:
                f = hexcol(p["fill"])
                attrs.append(f'fill="{recolor.get(f, f)}"')
                if p.get("even_odd"):
                    attrs.append('fill-rule="evenodd"')
            else:
                attrs.append('fill="none"')
            if "s" in p["type"] and p.get("color") and p.get("width"):
                s = hexcol(p["color"])
                cap = {0: "butt", 1: "round", 2: "square"}.get((p.get("lineCap") or (0,))[0], "butt")
                attrs.append(f'stroke="{recolor.get(s, s)}" stroke-width="{p["width"]:.2f}" stroke-linecap="{cap}" stroke-linejoin="round"')
            body.append(f'<path {" ".join(attrs)} d="{path_d(p["items"])}"/>')
        label = text.title().replace("&", "&amp;")
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]:.2f} {vb[1]:.2f} {vb[2]:.2f} {vb[3]:.2f}" '
                f'role="img" aria-label="{label} icon">\n' + "\n".join(body) + "\n</svg>\n")

    folder = OUT / kind
    folder.mkdir(parents=True, exist_ok=True)
    files = {}
    if kind == "apparatus-duotone":
        files[f"{slug}-duotone.svg"] = svg()
    else:
        files[f"{slug}-navy.svg"] = svg({c: NAVY for c in fills})
        files[f"{slug}-light.svg"] = svg({c: LIGHT for c in fills})
        files[f"{slug}-white.svg"] = svg({c: WHITE for c in fills})
        if len(fills) > 1:  # keep the designer's multi-color version too
            files[f"{slug}-original.svg"] = svg()
    for name, s in files.items():
        (folder / name).write_text(s, encoding="utf-8")
    manifest.append({"label": text, "set": kind, "slug": slug, "source_fills": fills, "files": [f"{kind}/{n}" for n in files]})

(OUT / "icons.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
print(len(manifest), "icons")
for m in manifest:
    print(m["set"], m["slug"], m["source_fills"])
