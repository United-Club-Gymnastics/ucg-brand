"""Visual examples for the brand site, attached to markdown sections by tools/build_site.py.

Each function returns an HTML fragment. Text that also lives in the markdown (key phrases,
headlines, one-liners) is read from the markdown, so the two can't drift. Paths are relative
to a page one folder deep (prefix "../").
"""
import html
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageOps

import mark_geometry as MG
from contrast import allowed as pair_allowed

E = html.escape
R = "../"
FONTS_DRIVE = "https://drive.google.com/drive/folders/1SUukrVratYo8sd4KxiF5_eztUnhAV-_o"


class Context:
    def __init__(self, root):
        self.root = Path(root)
        self.brand = json.loads((self.root / "brand.json").read_text(encoding="utf-8"))
        self.photos = json.loads((self.root / "assets/photos/photos.json").read_text(encoding="utf-8"))
        self.icons = json.loads((self.root / "assets/icons/icons.json").read_text(encoding="utf-8"))
        cols = {}
        for g in ("primary", "secondary", "neutral"):
            for c in self.brand["colors"][g]:
                cols[c["id"]] = c
        self.colors = cols
        self.pages = []

    def md(self, rel):
        return (self.root / rel).read_text(encoding="utf-8")

    def frames(self):
        """Photo frames: one entry per slug with color + bw files."""
        out = {}
        for p in self.photos:
            slug = re.sub(r"^ucg-(color|bw)-", "", p["file"])[:-4]
            f = out.setdefault(slug, {"slug": slug, "alt": p["alt"], "type": p["type"]})
            f["color" if p["tone"] == "color" else "bw"] = p["file"]
        return list(out.values())


# ---------- media prep (thumbnails, posters, dark email) ----------

ANIMS = [
    ("ucg-mark-flip-v2", "Back flip"), ("ucg-mark-bhs-tuck", "Back handspring tuck"),
    ("ucg-mark-pommel-horse", "Pommel horse"), ("ucg-mark-trampoline", "Trampoline"),
    ("ucg-mark-synchro-tramp", "Synchro trampoline"), ("ucg-mark-ub-dismount", "Uneven bars dismount"),
    ("ucg-mark-three-disciplines", "Three disciplines"), ("ucg-mark-three-disciplines-in-series", "Three disciplines in series"),
    ("ucg-icon-sequence", "Icon sequence"),
]


def anim_main(ctx, stem):
    for cand in (f"{stem}_square_navy.mp4", f"{stem}.mp4"):
        if (ctx.root / "assets/animation" / cand).exists():
            return cand
    raise SystemExit(f"no main video for {stem}")


def prepare_media(ctx):
    th = ctx.root / "site/thumbs/photos"
    th.mkdir(parents=True, exist_ok=True)
    for p in ctx.photos:
        src = ctx.root / "assets/photos" / p["file"]
        dst = th / p["file"]
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            continue
        im = ImageOps.exif_transpose(Image.open(src))
        im.thumbnail((760, 760), Image.LANCZOS)
        im.save(dst, quality=78, optimize=True, progressive=True)
    an = ctx.root / "site/thumbs/anim"
    an.mkdir(parents=True, exist_ok=True)
    for stem, _ in ANIMS:
        mp4 = anim_main(ctx, stem)
        dst = an / (mp4[:-4] + ".jpg")
        src_mp4 = ctx.root / "assets/animation" / mp4
        if not dst.exists() or dst.stat().st_mtime < src_mp4.stat().st_mtime or dst.stat().st_mtime < Path(__file__).stat().st_mtime:
            # poster from near the end of the loop, where the mark is fully formed
            src = str(ctx.root / "assets/animation" / mp4)
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                       capture_output=True, text=True, check=True).stdout.strip())
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{max(dur - 0.4, 0):.2f}", "-i", src,
                            "-frames:v", "1", "-vf", "scale=540:-2", "-q:v", "4", str(dst)], check=True)
    # two copies of the example email with the mode pinned, so the side-by-side preview shows
    # light and dark whatever the viewer's own system setting is
    ex = (ctx.root / "templates/email/example-announcement.html").read_text(encoding="utf-8")
    for mode, query in (("light", "@media not all"), ("dark", "@media all")):
        pinned = ex.replace("@media (prefers-color-scheme: dark)", query)
        if pinned == ex:
            raise SystemExit("dark-mode media query not found in example email")
        pinned = pinned.replace("light dark", mode)  # the color-scheme meta tags and :root rule
        (ctx.root / f"site/email-example-{mode}.html").write_text(
            pinned.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1), encoding="utf-8")


# ---------- helpers ----------

def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    x, y = sorted([lum(a), lum(b)])
    return (y + 0.05) / (x + 0.05)


ORDER = ["navy", "dark-blue-green", "blue-green", "light-blue", "purple", "red-orange", "golden-yellow", "white"]
ON_CLASS = {"navy": "on-navy", "dark-blue-green": "on-dbg", "blue-green": "on-bg", "light-blue": "on-lb",
            "purple": "on-purple", "red-orange": "on-ro", "golden-yellow": "on-yellow", "white": "on-white"}


def readable_on(hexv):
    if hexv.upper() == "#A5C8CF":
        return "#184B56"
    return "#FFFFFF" if ratio("#FFFFFF", hexv) >= ratio("#1E2B38", hexv) else "#1E2B38"


def vis(title, body, note=""):
    t = f'<p class="vis-title">{E(title)}</p>' if title else ""
    n = f'<p class="vis-note">{note}</p>' if note else ""
    return f'<div class="vis">{t}{body}{n}</div>'


def thumb(file):
    return f"{R}site/thumbs/photos/{file}"


def dont(label, inner):
    return f'<div class="verdict-item"><span class="verdict verdict--dont">✗ {E(label)}</span>{inner}</div>'


def do(label, inner):
    return f'<div class="verdict-item"><span class="verdict verdict--do">✓ {E(label)}</span>{inner}</div>'


def pt(v):
    """Slide points -> container width units (slide is 10in wide)."""
    return f"{v * 10 / 72:.3f}cqw"


def px(v, w=1080):
    return f"{v * 100 / w:.3f}cqw"


def md_section(text, heading):
    m = re.search(rf"^##+ {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        raise SystemExit(f"markdown section '{heading}' not found")
    return m.group(1)


# ---------- shared visuals ----------

def palette_cards(ctx):
    uses = {
        "navy": "Most text, dark surfaces, primary buttons.",
        "blue-green": "Signature accent fill, and large type on Navy. Small text on it is Dark Blue Green.",
        "light-blue": "Light surfaces. Text on Navy.",
        "purple": "Accent fills and chips with Navy text. Large type on Navy.",
        "red-orange": "Calls to action and highlights, with Navy text on it. Large type only on White.",
        "dark-blue-green": "Links and accent text on light colors. Dark surface.",
        "golden-yellow": "Accent fills and chips with Navy text. Text on Navy.",
    }
    cards = []
    for g in ("primary", "secondary"):
        for c in ctx.brand["colors"][g]:
            fg = readable_on(c["hex"])
            border = "box-shadow:inset 0 -1px 0 #A5C8CF;" if c["id"] == "light-blue" else ""
            cmyk = ", ".join(str(x) for x in c["cmyk"])
            rgb = ", ".join(str(x) for x in c["rgb"])
            cards.append(f'''<div class="swatch"><div class="swatch-chip" style="background:{c["hex"]};color:{fg};{border}">{E(c["name"])}<span style="margin-left:auto;font-size:12px;letter-spacing:.12em;text-transform:uppercase">{g}</span></div>
<div class="swatch-body"><dl>
<dt>Hex</dt><dd>{c["hex"]}</dd><dd><button class="copy" data-copy="{c["hex"]}">Copy</button></dd>
<dt>RGB</dt><dd>{rgb}</dd><dd><button class="copy" data-copy="{rgb}">Copy</button></dd>
<dt>CMYK</dt><dd>{cmyk}</dd><dd></dd>
<dt>Pantone</dt><dd>{E(c["pantone"])}</dd><dd></dd>
</dl><p class="use">{E(uses[c["id"]])}</p></div></div>''')
    return vis("The palette", f'<div class="grid" style="--min:230px">{"".join(cards)}</div>')


def support_and_expressive(ctx):
    roles = ctx.brand["colors"]["ui_roles"]["values"]
    names = {"text-secondary": "Secondary text", "border": "Borders", "border-input": "Form fields",
             "surface-dark": "Dark surface", "surface-dark-alt": "Dark cards"}
    ui_strip = "".join(f'<div style="background:{ctx.colors[c]["hex"]};color:{readable_on(ctx.colors[c]["hex"])}">{E(names[k])}<br>{E(ctx.colors[c]["name"])}</div>'
                       for k, c in roles.items())
    ex = ctx.brand["colors"]["expressive"]["swatches"]
    ex_strip = "".join(f'<div style="background:{h};color:{readable_on(h)}">{h}</div>' for h in ex)
    return (vis("UI roles", f'<div class="strip">{ui_strip}</div>',
                "Secondary text, borders and dark mode use palette colors. Don't add grays.")
            + vis("Expressive range (merch, campaigns, events only)", f'<div class="strip">{ex_strip}</div>',
                  'Not part of the everyday palette, and not for official communications, lasting signage or anything people rely on to recognize UCG (EDG p4). See <a href="../expressive/">Expressive design</a>.'))


def safe_pairs(ctx, title="Safe text on every background"):
    panels = []
    for bg in ORDER:
        b = ctx.colors[bg]
        lines = []
        for fg in ORDER:
            if fg == bg:
                continue
            f = ctx.colors[fg]
            r = ratio(f["hex"], b["hex"])
            if pair_allowed(fg, bg) == "any":
                lines.append(f'<div style="color:{f["hex"]};font-weight:700;font-size:17px;line-height:1.35">Aa {E(f["name"])} <span style="font-weight:400;font-size:13px">{r:.1f}:1</span></div>')
        border = "border:1px solid #A5C8CF;" if bg in ("white", "light-blue") else ""
        panels.append(f'<div class="panel" style="background:{b["hex"]};{border}"><p class="subhead" style="margin:0 0 10px;font-size:13px;color:{readable_on(b["hex"])}">On {E(b["name"])}</p>{"".join(lines)}</div>')
    return vis(title, f'<div class="grid" style="--min:200px">{"".join(panels)}</div>')


def pillars(ctx, chips=False, title="Messaging themes"):
    text = ctx.md("references/messaging.md")
    phrases = {}
    for m in re.finditer(r"^### (.+?)(?: \(core\))?\n.*?^Key phrases: (.+?)$", text, re.S | re.M):
        phrases[m.group(1).strip()] = [p.strip() for p in m.group(2).split("·")]
    core = ctx.brand["messaging"]["core"]
    def chip_row(name, cls="chip", style=""):
        if not chips:
            return ""
        return '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:14px">' + "".join(
            f'<span class="{cls}" style="{style}text-transform:none;letter-spacing:0;font-size:13px">{E(p)}</span>' for p in phrases.get(name, [])[:4]) + "</div>"
    core_card = f'''<div class="panel on-navy" style="grid-column:1/-1"><p class="eyebrow" style="color:#DBEBEE">Core message</p>
<p class="display" style="font-size:clamp(34px,5vw,56px);margin:0 0 10px;color:#FFFFFF">{E(core["name"])}</p>
<p style="margin:0;color:#DBEBEE;font-size:18px">{E(core["line"])}</p>{chip_row(core["name"])}</div>'''
    sup = []
    for s, cls in zip(ctx.brand["messaging"]["supporting"], ["on-lb", "on-ro", "on-purple", "on-yellow"]):
        sup.append(f'''<div class="panel {cls}"><p class="eyebrow" style="color:#1E2B38">Supporting</p>
<p class="display" style="font-size:30px;margin:0 0 8px">{E(s["name"])}</p><p style="margin:0">{E(s["line"])}</p>{chip_row(s["name"], style="background:#FFFFFF;")}</div>''')
    return vis(title, f'<div class="grid" style="--min:340px">{core_card}{"".join(sup)}</div>')


def logo_strip():
    tiles = [("ucg-primary-navy.svg", "on-lb", "Primary"), ("ucg-secondary-light.svg", "on-navy", "Secondary"),
             ("ucg-logotype-navy.svg", "on-bg", "Logotype"), ("ucg-mark-white.svg", "on-dbg", "Mark")]
    t = "".join(f'<div class="tile {c}"><img src="{R}assets/logos/{f}" alt="{n} logo"></div>' for f, c, n in tiles)
    return vis("", f'<div class="grid" style="--min:200px">{t}</div><p style="margin-top:14px"><a class="btn" href="{R}logos/">All logos and downloads →</a></p>')


def feature_tiles(ctx):
    f = {fr["slug"]: fr for fr in ctx.frames()}
    def photo(slug, tone="bw", pos="center"):
        return f'<img class="photo-fill" src="{thumb(f[slug][tone])}" alt="" style="object-position:{pos}">'
    tiles = [
        ("Color fills", f'<div class="cq square on-bg" style="border-radius:16px"><div class="abs" style="left:8cqw;top:8cqw;right:8cqw"><p class="display" style="font-size:13cqw;margin:0;color:#1E2B38">For the love of the sport.</p></div><img class="abs" src="{R}assets/logos/ucg-mark-navy.svg" alt="" style="width:16cqw;right:8cqw;bottom:8cqw"></div>'),
        ("Strong type", f'<div class="cq square on-white" style="border-radius:16px"><div class="abs" style="left:8cqw;bottom:8cqw;right:8cqw"><p class="subhead" style="font-size:4cqw;margin:0 0 3cqw;color:#184B56">April 2027</p><p class="display" style="font-size:19cqw;margin:0;color:#1E2B38">A guide to Nationals</p></div></div>'),
        ("Black & white photos, white type", f'<div class="cq square" style="border-radius:16px;background:#1E2B38">{photo("beam-pose")}<div class="abs" style="left:0;right:0;bottom:0;background:#1E2B38;padding:5cqw 7cqw"><p class="display" style="font-size:11cqw;margin:0;color:#FFFFFF">Join the club</p></div></div>'),
        ("Dynamic crops", f'<div class="cq square" style="border-radius:16px;background:#1E2B38">{photo("high-bar-swing", pos="60% 30%")}</div>'),
        ("Rounded corners", f'<div class="cq square on-lb" style="border-radius:16px"><div class="abs" style="left:8cqw;right:8cqw;top:12cqw;background:#FFFFFF;border-radius:6cqw;padding:7cqw"><p class="subhead" style="font-size:4.4cqw;margin:0 0 3cqw;color:#184B56">Card title</p><p style="font-size:6cqw;margin:0;color:#1E2B38;font-weight:700;line-height:1.3">Cards, panels and photos all get rounded corners.</p></div></div>'),
        ("Event icons + color overlay", f'<div class="cq square overlay-screen" style="--overlay:#ADBAE9;border-radius:16px">{photo("beam-walkover")}<img class="abs" src="{R}assets/icons/event/wag-navy.svg" alt="WAG icon" style="width:40cqw;left:30cqw;top:30cqw"></div>'),
    ]
    body = "".join(f'<div>{t}<p class="mock-label">{E(n)}</p></div>' for n, t in tiles)
    return vis("The six design features", f'<div class="grid" style="--min:220px">{body}</div>', "Example content.")


def type_specimens(ctx):
    live = '''<div class="card"><p class="eyebrow">Fallback fonts (what this site uses)</p>
<p style="font-family:'Saira Condensed','Arial Narrow',Arial,sans-serif;font-weight:700;font-size:44px;line-height:.95;text-transform:uppercase;margin:0 0 12px">For the love of the sport.</p>
<p style="font-family:Arial,Helvetica,sans-serif;margin:0">Saira Condensed Bold for headlines, Arial for body. Free, and built into Google Docs, Slides, Sheets and most email clients.</p></div>'''
    imgs = (f'<div class="card" style="padding:12px"><img src="{R}site/examples/type/greed-condensed.png" alt="Greed Condensed Bold specimen: FOR THE LOVE OF THE SPORT, alphabet and numerals" style="display:block;width:100%;height:auto"></div>'
            f'<div class="card" style="padding:12px"><img src="{R}site/examples/type/suisse-intl.png" alt="Suisse Intl specimen in Regular and Semibold" style="display:block;width:100%;height:auto"></div>')
    return vis("Brand fonts and fallbacks", f'<div class="grid" style="--min:300px">{imgs}{live}</div>',
               f'The brand fonts are shown as images because the font files are licensed to UCG and never published here. '
               f'UCG volunteers can <a href="{FONTS_DRIVE}">download Greed Condensed and Suisse Intl</a> from the UCG Drive.')


def voice_examples(ctx):
    pairs = re.findall(r'^- Instead of "(.+?)", write "(.+?)"$', md_section(ctx.md("BRAND.md"), "Voice"), re.M)
    if not pairs:
        raise SystemExit("voice examples not found in BRAND.md")
    rows = "".join(f'<div class="dodont">{dont("Instead of", f"<div class=card><p>{E(a)}</p></div>")}{do("Write", f"<div class=card><p>{E(b)}</p></div>")}</div>' for a, b in pairs)
    return vis("Sounds like UCG", f'<div style="display:grid;gap:18px">{rows}</div>')


def medium_cards(ctx):
    cards = "".join(f'<a class="card" href="{R}{slug}/" style="text-decoration:none"><h3 style="color:#184B56">{E(title)}</h3><p class="muted small" style="font-weight:400">{E(blurb)}</p></a>'
                    for slug, title, _md, _s, blurb in ctx.pages if slug != "guidelines")
    return vis("Every guide", f'<div class="grid" style="--min:230px">{cards}</div>')


# ---------- colors page ----------

def contrast_matrix(ctx):
    head = '<div class="mh">Background ↓ / Text →</div>' + "".join(f'<div class="mh">{E(ctx.colors[f]["name"])}</div>' for f in ORDER)
    cells = []
    for bg in ORDER:
        b = ctx.colors[bg]
        cells.append(f'<div class="mh">{E(b["name"])}</div>')
        for fg in ORDER:
            if fg == bg:
                cells.append(f'<div class="cell" style="background:repeating-linear-gradient(45deg,#F1F5F6,#F1F5F6 6px,#FFFFFF 6px,#FFFFFF 12px)" aria-hidden="true"></div>')
                continue
            f = ctx.colors[fg]
            r = ratio(f["hex"], b["hex"])
            a = pair_allowed(fg, bg)
            if a == "any":
                tag, skip = '<span class="tag tag--body">Any text</span>', ""
            elif a == "large":
                tag, skip = '<span class="tag tag--large">Large only</span>', ' data-contrast-skip'
            else:
                tag, skip = '<span class="tag tag--no">Never</span>', ' data-contrast-skip'
            label = readable_on(b["hex"])
            cells.append(f'<div class="cell" style="background:{b["hex"]}"{skip} title="{E(f["name"])} on {E(b["name"])}: {r:.2f}:1">'
                         f'<span class="aa" style="color:{f["hex"]}">Aa</span><span class="ratio" style="color:{label}">{r:.1f}:1</span>{tag}</div>')
    legend = ('<div class="legend"><span><span class="tag tag--body">Any text</span> 4.5:1+ and approved by the guide</span>'
              '<span><span class="tag tag--large">Large only</span> 24px+ text, icons, logos: 3:1+, or the guide approves it for large sizes only</span>'
              '<span><span class="tag tag--no">Never</span> under 3:1, or not approved by the guide</span></div>')
    return vis("Every pairing at a glance", f'<div class="matrix-scroll"><div class="matrix">{head}{"".join(cells)}</div></div>{legend}')


def overlay_demos(ctx):
    f = {fr["slug"]: fr for fr in ctx.frames()}
    a = f'''<div class="cq square overlay-screen" style="--overlay:#DBEBEE;border-radius:16px"><img class="photo-fill" src="{thumb(f["vault-layout"]["bw"])}" alt="">
<div class="abs" style="left:7cqw;right:7cqw;bottom:7cqw;background:#DBEBEE;border-radius:4cqw;padding:5cqw"><p class="display" style="font-size:10cqw;margin:0;color:#1E2B38">Meet us at Nationals</p></div></div>'''
    b = f'''<div class="cq square overlay-dark" style="border-radius:16px"><img class="photo-fill" src="{thumb(f["rings-swing"]["bw"])}" alt="">
<div class="abs" style="left:7cqw;right:7cqw;bottom:7cqw"><p class="display" style="font-size:12cqw;margin:0;color:#FFFFFF">Keep the floor open</p></div></div>'''
    c = f'''<div class="cq square" style="border-radius:16px;background:#1E2B38"><img class="abs" src="{thumb(f["beam-finish"]["bw"])}" alt="" style="top:0;left:0;width:55%;height:100%;object-fit:cover">
<div class="abs" style="left:60%;right:5cqw;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center"><p class="display" style="font-size:9cqw;margin:0 0 3cqw;color:#FFFFFF">One floor. Every story.</p><p style="font-size:3.6cqw;margin:0;color:#DBEBEE">Text on a solid panel beside the photo.</p></div></div>'''
    body = (f'<div>{a}<p class="mock-label">Light: B&amp;W photo screened over Light Blue, Navy text on a Light Blue panel.</p></div>'
            f'<div>{b}<p class="mock-label">Darker: a B&amp;W photo toned down over Navy, White text.</p></div>'
            f'<div>{c}<p class="mock-label">Safest: White text on a solid Navy panel beside the photo.</p></div>')
    return vis("Text over photos", f'<div class="grid" style="--min:230px">{body}</div>')


def palette_files(ctx):
    return vis("", f'''<div class="grid" style="--min:260px"><div class="card"><h3>Swatch files</h3><p class="muted small" style="margin-bottom:12px">For Adobe apps and print vendors.</p>
<div class="btn-row"><a class="btn btn--sm" href="{R}assets/palette/UCG_Colors.ase" download>ASE swatches</a><a class="btn btn--sm btn--ghost" href="{R}assets/palette/UCG_Colors.pdf">Color sheet (PDF)</a></div></div>
<div class="card" style="padding:12px"><img src="{R}assets/palette/ucg-color-wheel.png" alt="UCG color wheel: primary colors on one side, secondary on the other, expressive colors in the inner ring" style="display:block;width:100%;height:auto"></div></div>''')


# ---------- logos ----------

FAMILIES = [("primary", "Primary"), ("secondary", "Secondary"), ("logotype", "Logotype"),
            ("wordmark-full-name", "Wordmark, full name"), ("wordmark-ucg", "Wordmark, UCG"), ("mark", "Mark"),
            ("badge-circle", "Badge, circle"), ("badge-crest", "Badge, crest")]
CW_TILE = {"navy": "on-lb", "light": "on-navy", "white": "on-dbg", "black": "on-white"}
BADGE_TILE = {"navy": "on-white", "light": "on-lb", "white": "on-white", "black": "on-lb"}


def logo_gallery(ctx):
    out = []
    for fam, name in FAMILIES:
        tiles = []
        for cw in ("navy", "light", "white", "black"):
            base = f"{R}assets/logos/ucg-{fam}-{cw}"
            cls = BADGE_TILE[cw] if fam.startswith("badge") else CW_TILE[cw]
            tiles.append(f'''<div class="asset"><div class="tile {cls}" style="border-radius:0"><img src="{base}.svg" alt="{E(name)} logo, {cw}" loading="lazy"></div>
<div class="meta"><b>{cw.title()}</b><span class="dl"><a href="{base}.svg" download>SVG</a><a href="{base}.png" download>PNG</a></span></div></div>''')
        out.append(f'<h3 style="margin:28px 0 12px">{E(name)}</h3><div class="grid" style="--min:200px">{"".join(tiles)}</div>')
    extras = [("ucg-avatar-circle.png", "Avatar, circle", "on-white"), ("ucg-avatar-square.png", "Avatar, square", "on-white"),
              ("ucg-favicon.png", "Favicon", "on-white"), ("ucg-mark-in-circle-light-on-navy.png", "Mark in circle", "on-white"),
              ("ucg-document-header.png", "Document header", "on-white")]
    ex = "".join(f'''<div class="asset"><div class="tile {c}" style="border-radius:0"><img src="{R}assets/logos/{f}" alt="{E(n)}" loading="lazy"></div>
<div class="meta"><b>{E(n)}</b><span class="dl"><a href="{R}assets/logos/{f}" download>PNG</a></span></div></div>''' for f, n, c in extras)
    out.append(f'<h3 style="margin:28px 0 12px">Avatars, favicon and document header</h3><div class="grid" style="--min:200px">{ex}</div>')
    return vis("Every logo, every colorway", "".join(out), "Tiles show each colorway on a background it's meant for. Click SVG for the web, PNG for Google apps.")


def logo_rules(ctx):
    logo = f"{R}assets/logos/ucg-primary-navy.svg"
    clear = f'''<div class="panel on-white" style="display:flex;justify-content:center;padding:40px">
<div style="position:relative;padding:22px;outline:2px dashed #184B56;outline-offset:0"><img src="{logo}" alt="Primary logo with clear space" style="height:84px;display:block">
<span style="position:absolute;top:2px;left:50%;transform:translateX(-50%);font-size:12px;font-weight:700;color:#184B56">x</span>
<span style="position:absolute;left:6px;top:50%;transform:translateY(-50%);font-size:12px;font-weight:700;color:#184B56">x</span></div></div>
<p class="vis-note">x = the height of the "U" in UCG. Recommended: at least that much empty space on every side, and the primary logo at least 1 in wide in print or 120px on screen. (UCG defaults; the design guide doesn't set them.)</p>'''
    f = {fr["slug"]: fr for fr in ctx.frames()}
    def t(style, img=logo, cls="on-white", extra=""):
        return f'<div class="tile {cls}" style="min-height:150px;overflow:hidden;position:relative">{extra}<img src="{img}" alt="" style="max-height:70px;{style}"></div>'
    donts = [
        dont("Don't stretch", t("transform:scaleX(1.5)")),
        dont("Don't use off-palette colors", f'<div class="tile on-white" style="min-height:150px"><span style="display:block;width:240px;max-width:80%;height:70px;background:#2FB34A;-webkit-mask:url({logo}) center/contain no-repeat;mask:url({logo}) center/contain no-repeat"></span></div>'),
        dont("Don't add effects", t("filter:drop-shadow(5px 5px 0 #F6C328) drop-shadow(-2px -2px 0 #ADBAE9)")),
        dont("Don't use low contrast", t("", cls="on-dbg")),
        dont("Don't put it on a busy photo", t("position:relative", img=f"{R}assets/logos/ucg-primary-white.svg", cls="",
             extra=f'<img src="{thumb(f["team-celebration"]["color"])}" alt="" class="photo-fill">')),
    ]
    dos = [
        do("Navy on light", t("", cls="on-lb")),
        do("White or light on navy", t("", img=f"{R}assets/logos/ucg-primary-light.svg", cls="on-navy")),
        do("A palette color in an approved pair", f'<div class="tile on-navy" style="min-height:150px"><span role="img" aria-label="Primary logo in Golden Yellow on Navy" style="display:block;width:240px;max-width:80%;height:70px;background:#F6C328;-webkit-mask:url({logo}) center/contain no-repeat;mask:url({logo}) center/contain no-repeat"></span></div>'),
        do("White on a dark overlay", f'<div class="tile overlay-dark" style="min-height:150px;position:relative;overflow:hidden"><img src="{thumb(f["team-celebration"]["bw"])}" alt="" class="photo-fill"><img src="{R}assets/logos/ucg-primary-white.svg" alt="" style="max-height:70px;position:relative"></div>'),
    ]
    return (vis("Clear space", clear)
            + vis("Do", f'<div class="grid" style="--min:220px">{"".join(dos)}</div>')
            + vis("Don't", f'<div class="grid" style="--min:260px">{"".join(donts)}</div>'))


# ---------- icons ----------

def icon_gallery(ctx):
    groups = {"event": [], "apparatus-solid": []}
    for ic in ctx.icons:
        groups[ic["set"]].append(ic)
    order_app = ["mag-floor", "mag-pommel-horse", "mag-rings", "mag-vault", "mag-parallel-bars", "mag-high-bar",
                 "wag-vault", "wag-uneven-bars", "wag-balance-beam", "wag-floor",
                 "tnt-trampoline", "tnt-double-mini", "tnt-power-tumbling", "tnt-synchro"]
    order_ev = ["mag", "mag-1", "mag-2", "mag-3", "wag", "wag-1", "wag-grad", "tnt", "tnt-2", "club-spirit"]
    def tiles(icons, order):
        icons = sorted(icons, key=lambda i: order.index(i["slug"]) if i["slug"] in order else 99)
        out = []
        for ic in icons:
            base = f'{R}assets/icons/{ic["set"]}/{ic["slug"]}'
            label = ic["slug"].replace("tnt", "T&T").replace("mag", "MAG").replace("wag", "WAG").replace("-", " ")
            out.append(f'''<div class="asset"><div class="tile icon-tile on-white" style="border-radius:0" data-class-navy="tile icon-tile on-white" data-class-light="tile icon-tile on-navy" data-class-white="tile icon-tile on-dbg">
<img src="{base}-navy.svg" data-src-navy="{base}-navy.svg" data-src-light="{base}-light.svg" data-src-white="{base}-white.svg" alt="{E(label)} icon" loading="lazy"></div>
<div class="meta"><b>{E(label)}</b><span class="dl"><a href="{base}-navy.svg" data-href-navy="{base}-navy.svg" data-href-light="{base}-light.svg" data-href-white="{base}-white.svg" download>SVG</a><a href="{base}-navy.png" data-href-navy="{base}-navy.png" data-href-light="{base}-light.png" data-href-white="{base}-white.png" download>PNG</a></span></div></div>''')
        return "".join(out)
    toggle = ('<div class="toggle" data-swap-group="icon-sets" role="group" aria-label="Icon colorway">'
              '<button data-swap="navy" aria-pressed="true">Navy</button><button data-swap="light">Light blue</button><button data-swap="white">White</button></div>')
    body = (f'{toggle}<div id="icon-sets"><h3 style="margin:8px 0 12px">Event icons</h3><div class="grid" style="--min:170px">{tiles(groups["event"], order_ev)}</div>'
            f'<h3 style="margin:28px 0 12px">Apparatus icons</h3><div class="grid" style="--min:170px">{tiles(groups["apparatus-solid"], order_app)}</div></div>')
    return vis("All icons", body)


def icon_usage(ctx):
    f = {fr["slug"]: fr for fr in ctx.frames()}
    chips = "".join(f'<span style="display:inline-flex;align-items:center;gap:10px;background:#FFFFFF;border-radius:999px;padding:8px 16px 8px 10px"><img src="{R}assets/icons/event/{s}-navy.svg" alt="" style="height:28px"><b class="subhead" style="font-size:14px">{n}</b></span>'
                    for s, n in (("mag", "MAG"), ("wag", "WAG"), ("tnt", "T&amp;T")))
    a = f'<div class="panel on-lb" style="display:flex;flex-wrap:wrap;gap:12px;align-items:center">{chips}</div>'
    b = f'''<div class="cq" style="aspect-ratio:16/9;border-radius:16px;background:#1E2B38">
<div class="abs" style="inset:0;display:grid;grid-template-columns:repeat(3,1fr)">
{"".join(f'<div class="cq overlay-screen" style="--overlay:{c};position:relative"><img class="photo-fill" src="{thumb(f[p]["bw"])}" alt=""><img class="abs" src="{R}assets/icons/event/{s}-navy.svg" alt="{n} icon" style="width:50cqw;left:25cqw;top:30cqw"></div>' for c, p, s, n in (("#F6C328", "rings-swing", "mag", "MAG"), ("#ADBAE9", "beam-walkover", "wag", "WAG"), ("#F4694A", "trampoline-straddle", "tnt", "T&amp;T")))}
</div></div>'''
    return vis("In use", f'<div style="display:grid;gap:16px">{a}{b}</div>',
               "Discipline labels on a light panel, and icons over color-overlaid photos (DG p20).")


# ---------- photos ----------

def photo_gallery(ctx):
    frames = ctx.frames()
    items = []
    for fr in frames:
        c, b = fr["color"], fr["bw"]
        items.append(f'''<figure class="photo" data-tags="{fr["type"]}"><img src="{thumb(c)}" data-src-color="{thumb(c)}" data-src-bw="{thumb(b)}" alt="{E(fr["alt"])}" loading="lazy" width="760" height="507">
<figcaption><span class="dl"><a href="{R}assets/photos/{c}" data-href-color="{R}assets/photos/{c}" data-href-bw="{R}assets/photos/{b}" download>Download full size</a></span></figcaption></figure>''')
    controls = ('<div style="display:flex;flex-wrap:wrap;gap:14px;align-items:center">'
                '<div class="toggle" data-swap-group="photo-grid" role="group" aria-label="Tone"><button data-swap="color" aria-pressed="true">Color</button><button data-swap="bw">Black &amp; white</button></div>'
                '<div class="toggle" data-filter-group="photo-grid" role="group" aria-label="Type"><button data-filter="all" aria-pressed="true">All</button><button data-filter="athlete">Athletes</button><button data-filter="movement">Movement</button><button data-filter="community">Community</button></div></div>')
    return vis(f"All {len(frames)} photos", f'{controls}<div class="photo-grid" id="photo-grid">{"".join(items)}</div>')


def photo_treatments(ctx):
    return overlay_demos(ctx)


# ---------- messaging ----------

def tone_cards(ctx):
    cards = "".join(f'<div class="card"><p class="display" style="font-size:34px;margin:0 0 8px">{E(t["name"])}</p><p>{E(t["line"])}</p></div>' for t in ctx.brand["messaging"]["tone"])
    return vis("", f'<div class="grid" style="--min:220px">{cards}</div>')


def headline_posters(ctx, title="Set in caps, they look like this"):
    sec = md_section(ctx.md("references/messaging.md"), "Headlines")
    cats = re.findall(r"^\*\*(.+?):\*\* (.+)$", sec, re.M)
    if len(cats) < 4:
        raise SystemExit("headline categories not parsed")
    styles = ["on-navy", "on-bg", "on-lb", "on-yellow"]
    cards = []
    for (name, lines), cls in zip(cats, styles):
        heads = "".join(f'<li class="display" style="font-size:24px;margin:0 0 8px">{E(h.strip())}</li>' for h in lines.split("·"))
        eyebrow = {"on-navy": "#DBEBEE", "on-bg": "#184B56"}.get(cls, "#1E2B38")
        cards.append(f'<div class="panel {cls}"><p class="eyebrow" style="color:{eyebrow}">{E(name)}</p><ul style="list-style:none;margin:0;padding:0">{heads}</ul></div>')
    return vis(title, f'<div class="grid" style="--min:340px">{"".join(cards)}</div>')


def copy_cards(ctx, heading, title="Copy and paste"):
    sec = md_section(ctx.md("references/messaging.md"), heading)
    items = re.findall(r"^(?:- )?\*\*(.+?)\*\*(?: \([^)]*\))?:?\s*(.+)$", sec, re.M)
    if not items:
        raise SystemExit(f"no copy items in {heading}")
    cards = []
    for label, text in items:
        label = label.rstrip(":")
        text = text.strip()
        cards.append(f'<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px"><span class="eyebrow" style="margin:0">{E(label)}</span><button class="copy" data-copy="{E(text)}">Copy</button></div><p>{E(text)}</p></div>')
    return vis(title, f'<div class="grid" style="--min:340px">{"".join(cards)}</div>')


def caption_mock(ctx, title="As posts"):
    sec = md_section(ctx.md("references/messaging.md"), "Example: social captions")
    quotes = [q for q in re.split(r"\n\s*\n", sec) if q.strip().startswith(">")]
    f = {fr["slug"]: fr for fr in ctx.frames()}
    posts = []
    for q, slug in zip(quotes, ("teammates-react", "beam-finish")):
        lines = [l[1:].strip() for l in q.strip().splitlines()]
        tags = lines[-1] if lines[-1].startswith("#") else ""
        body = " ".join(l for l in lines if l and not l.startswith("#"))
        posts.append(f'''<div class="card" style="padding:0;overflow:hidden;max-width:420px"><div style="display:flex;align-items:center;gap:10px;padding:10px 12px">
<img src="{R}assets/logos/ucg-avatar-circle.png" alt="" style="width:32px;height:32px;border-radius:50%"><b class="small">unitedclubgymnastics</b></div>
<img src="{thumb(f[slug]["color"])}" alt="{E(f[slug]["alt"])}" style="display:block;width:100%;aspect-ratio:4/5;object-fit:cover">
<p class="small" style="padding:12px 14px 4px;margin:0"><b>unitedclubgymnastics</b> {E(body)}</p><p class="small" style="padding:0 14px 14px;margin:0;color:#184B56;font-weight:700">{E(tags)}</p></div>''')
    return vis(title, f'<div class="grid" style="--min:280px">{"".join(posts)}</div>')


# ---------- email ----------

def email_previews(ctx):
    return vis("Example built from the template", f'''<div class="compare">
<div><p class="mock-label" style="margin:0 0 8px"><b>Light mode</b></p><iframe class="email-frame" src="{R}site/email-example-light.html" title="Example UCG announcement email, light mode" loading="lazy"></iframe></div>
<div><p class="mock-label" style="margin:0 0 8px"><b>Dark mode</b> (Apple Mail, iOS Mail, Outlook)</p><iframe class="email-frame" src="{R}site/email-example-dark.html" title="Example UCG announcement email, dark mode" loading="lazy"></iframe></div></div>
<div class="btn-row" style="margin-top:16px"><a class="btn" href="{R}templates/email/ucg-announcement-email.html" download>Download the template</a><a class="btn btn--ghost" href="{R}templates/email/example-announcement.html" download>Download this example</a></div>''',
               "Example content for illustration: the dates and details are placeholders, and every link goes to the UCG homepage.")


def gmail_mock(ctx):
    return vis("A personal email", f'''<div class="card" style="max-width:640px;padding:0;overflow:hidden;font-family:Arial,Helvetica,sans-serif">
<div style="background:#DBEBEE;padding:12px 18px;font-size:14px;color:#1E2B38;border-bottom:1px solid #A5C8CF"><b>To:</b> jordan@example.com<br><b>Subject:</b> Getting involved with UCG</div>
<div style="padding:22px 22px 26px;font-size:16px;line-height:1.55;color:#1E2B38">
<p style="margin:0 0 14px;font-family:'Arial Narrow',Arial,sans-serif;font-weight:700;font-size:18px">Hi Jordan,</p><p style="margin:0 0 14px">Thanks for reaching out about getting involved with UCG. Whether you are coming from a college club, returning after time away, or looking for a new way to stay in the sport, there is a place for you here.</p>
<p style="margin:0 0 22px">See you in the gym,</p>
<p style="margin:0;font-size:16px"><b style="text-transform:uppercase">Jordan Lee</b><br>Events Coordinator, United Club Gymnastics<br><a href="https://unitedclubgymnastics.org" style="color:#184B56">unitedclubgymnastics.org</a></p>
<img src="{R}assets/social/ucg-email-header.png" alt="United Club Gymnastics" style="display:block;width:260px;margin-top:14px;border-radius:6px"></div></div>''')


# ---------- web ----------

def web_layout(ctx):
    bands = "".join(f'<div class="{c}" style="padding:22px 26px;{b}"><span class="subhead" style="font-size:13px">{n}</span></div>'
                    for c, n, b in (("on-white", "White", "border:0;border-bottom:1px solid #A5C8CF;"), ("on-lb", "Light Blue", ""), ("on-bg", "Blue Green", "color:#184B56;"), ("on-navy", "Navy", "")))
    radii = "".join(f'<div style="text-align:center"><div style="height:80px;background:#DBEBEE;border:2px solid #1E2B38;border-radius:{r}"></div><p class="small" style="margin:8px 0 0"><b>{n}</b><br>{r}</p></div>'
                    for n, r in (("Buttons, chips", "999px"), ("Inputs, boxes", "12px"), ("Cards, photos", "20px")))
    return (vis("Section backgrounds", f'<div style="border-radius:16px;overflow:hidden;border:1px solid #A5C8CF">{bands}</div>')
            + vis("Rounded corners (template defaults)", f'<div class="grid" style="--min:130px">{radii}</div>'))


def web_type(ctx):
    rows = [("Display / hero", "clamp(48px, 7vw, 96px), ALL CAPS", '<span class="ucg-display" style="font-size:clamp(44px,6vw,72px)">For the love</span>'),
            ("H1", "clamp(40px, 6vw, 80px)", '<span class="ucg-display" style="font-size:clamp(36px,5vw,56px)">A guide to Nationals</span>'),
            ("H2", "clamp(32px, 4vw, 54px)", '<span class="ucg-display" style="font-size:clamp(28px,3.5vw,40px)">Find your club</span>'),
            ("H3", "20–24px, 600", '<span style="font-weight:700;font-size:22px">Volunteer sign-ups are open</span>'),
            ("Subhead / label", "14–18px, 0.2em tracking", '<span class="ucg-subhead" style="font-size:16px">Sponsorship levels</span>'),
            ("Eyebrow", "12–13px bold caps, 0.2em", '<span class="ucg-eyebrow" style="color:#184B56">New to UCG?</span>'),
            ("Body", "16px / 1.55", '<span>UCG clubs compete in three disciplines. There is a place for you on the floor.</span>')]
    body = "".join(f'<div style="display:grid;grid-template-columns:minmax(120px,180px) 1fr;gap:16px;align-items:baseline;padding:16px 0;border-top:1px solid #A5C8CF"><div class="small"><b>{n}</b><br><span class="muted">{s}</span></div><div style="min-width:0">{x}</div></div>' for n, s, x in rows)
    return vis("Type scale, live", body)


def web_components(ctx):
    buttons = f'''<div class="panel on-white"><p class="vis-title">Buttons</p><div class="btn-row" style="align-items:center">
<a class="ucg-btn" href="#">Register →</a><a class="ucg-btn ucg-btn--cta" href="#">Give</a><a class="ucg-btn ucg-btn--accent" href="#">Learn more</a>
<a href="#" style="font-weight:700;letter-spacing:.2em;text-transform:uppercase;font-size:13px;color:#1E2B38;text-decoration:none">Contact →</a></div>
<div class="panel on-navy" style="margin-top:14px;padding:16px"><a class="ucg-btn ucg-btn--on-dark" href="#">Donate →</a></div>
<details style="margin-top:12px"><summary class="small"><b>HTML</b></summary><pre><code>&lt;a class="ucg-btn" href="…"&gt;Register →&lt;/a&gt;
&lt;a class="ucg-btn ucg-btn--cta" href="…"&gt;Give&lt;/a&gt;
&lt;a class="ucg-btn ucg-btn--accent" href="…"&gt;Learn more&lt;/a&gt;
&lt;a class="ucg-btn ucg-btn--on-dark" href="…"&gt;Donate →&lt;/a&gt;</code></pre></details></div>'''
    chips = '''<div class="panel on-white"><p class="vis-title">Chips and status</p><div class="btn-row">
<span class="chip" style="background:#ADBAE9">New</span><span class="chip" style="background:#F6C328">Nationals</span><span class="chip" style="background:#F4694A">Register now</span><span class="chip">Info</span></div>
<div class="btn-row" style="margin-top:10px"><span class="chip" style="background:#DBEBEE;color:#184B56">✓ On track</span><span class="chip" style="background:#F6C328">● Needs attention</span><span class="chip" style="background:#F4694A">! Closes Jan 15</span></div>
<p class="vis-note">Always pair a status color with a word or symbol.</p></div>'''
    cards = '''<div class="panel on-lb"><p class="vis-title">Cards</p><div class="grid" style="--min:160px">
<div style="background:#FFFFFF;border-radius:20px;padding:18px"><p class="ucg-eyebrow" style="color:#184B56;margin:0 0 6px">Compete</p><p style="font-weight:700;font-size:18px;margin:0 0 6px">Find a meet</p><p class="small" style="margin:0;color:#184B56">Sanctioned events near you.</p></div>
<div style="background:#1E2B38;border-radius:20px;padding:18px"><p class="ucg-eyebrow" style="color:#DBEBEE;margin:0 0 6px">Featured</p><p style="font-weight:700;font-size:18px;margin:0 0 6px;color:#FFFFFF">Nationals 2027</p><p class="small" style="margin:0;color:#DBEBEE">Portland, Oregon.</p></div></div></div>'''
    lst = '''<div class="panel on-white"><p class="vis-title">List with dividers</p><div>
<div style="padding:14px 0"><b>Reach out to UCG</b><br><span class="small muted">Tell us about your club or your situation.</span></div>
<div style="padding:14px 0;border-top:.5pt solid #A5C8CF"><b>Speak with the team</b><br><span class="small muted">We'll answer questions about levels and events.</span></div>
<div style="padding:14px 0;border-top:.5pt solid #A5C8CF"><b>Find your next step</b><br><span class="small muted">Join a club, compete independently or volunteer.</span></div></div>
<p class="vis-note">Dividers between items only, none above the first or below the last.</p></div>'''
    form = '''<div class="panel on-white"><p class="vis-title">Form fields</p>
<label style="display:block;font-weight:700;font-size:14px;margin-bottom:6px" for="demo-club">Club name</label>
<input id="demo-club" value="Example University Gymnastics" style="width:100%;font:inherit;color:#1E2B38;padding:11px 14px;border:1.5px solid #184B56;border-radius:12px;margin-bottom:14px">
<label style="display:block;font-weight:700;font-size:14px;margin-bottom:6px" for="demo-disc">Discipline</label>
<select id="demo-disc" style="width:100%;font:inherit;color:#1E2B38;padding:11px 14px;border:1.5px solid #184B56;border-radius:12px;outline:3px solid rgba(24,75,86,.35);outline-offset:1px;background:#FFFFFF"><option>WAG</option><option>MAG</option><option>T&amp;T</option></select>
<p class="vis-note">The second field shows the focus state: Dark Blue Green border and ring.</p></div>'''
    table = '''<div class="panel on-white" style="grid-column:1/-1"><p class="vis-title">Table</p><div class="table-wrap" style="margin:0"><table>
<thead><tr><th>Club</th><th>Discipline</th><th style="text-align:right">Athletes</th><th>Status</th></tr></thead>
<tbody><tr><td>Example State</td><td>WAG</td><td style="text-align:right">24</td><td>Registered</td></tr>
<tr><td>River City Gym</td><td>MAG</td><td style="text-align:right">12</td><td>Pending</td></tr>
<tr><td>Northside Flyers</td><td>T&amp;T</td><td style="text-align:right">9</td><td>Registered</td></tr></tbody></table></div></div>'''
    return vis("Components, live", f'<div class="grid" style="--min:300px">{buttons}{chips}{cards}{lst}{form}{table}</div>',
               "Example content. Buttons use the classes in tokens/ucg.css.")


def web_dark(ctx):
    return vis("", '''<div class="panel" style="background:#1E2B38;max-width:520px"><p class="ucg-eyebrow" style="color:#DBEBEE;margin:0 0 8px">Dark mode</p>
<p style="font-weight:700;font-size:20px;margin:0 0 6px;color:#FFFFFF">Navy surfaces, white and light blue text</p><p style="margin:0 0 14px;color:#DBEBEE">Golden Yellow or Light Blue for links; Blue Green for large type and rules.</p>
<a class="ucg-btn ucg-btn--on-dark" href="#">Continue →</a> <a href="#" style="color:#F6C328;margin-left:12px">Text link</a></div>''')


# ---------- Google templates (slides, docs, sheets) ----------

# key -> (name, kind, file id, what it's for); previews in site/examples/templates/<key>.png
TEMPLATES = {
    "slides": ("UCG Slides Template", "presentation", "1aJHuTtVjkRVPzteyeOgZdMWxWDLeAFNSvdaMtY3whks", "Branded layouts for New slide, plus an example of every slide type: cover, agenda, cards, section break, numbers, table, sponsors, closing and a working-meeting slide."),
    "policy": ("UCG Policy Template", "document", "1oC-g9xVgEFwP1pCBPfpUfnWDGawBIE3UF858RqZhGG8", "Numbered sections and subsections, amendments and a version history table."),
    "change-proposal": ("UCG Change Proposal Template", "document", "11yKkZv8L44MRprWYa-Ppe_IXf-Wu4KcG2ku_heYfjtU", "Propose a change and plan how it rolls out and who hears about it."),
    "minutes": ("UCG Meeting Minutes Template", "document", "1Yz_r_cHrSBO9s4XeSwUXvlf468QuEn9SxWmLGFZbyE8", "Attendance, agenda and notes, action items, a sign-off block and the minute-taking guidelines from General Counsel."),
    "email-draft": ("UCG Email Draft Template", "document", "13eIZoEsXOzOZCphU0q-_o5OzgLqNAaC8tsz1A0JpJu4", "Draft an announcement email block by block before it's built in the HTML template."),
    "sheets": ("UCG Sheets Template", "spreadsheets", "138BylbdttmkkCohApng-HlhUDbECz8rtueqv_Tp30x0", "UCG theme, frozen header, banded rows, status colors, dropdowns, a chart and a How to use tab."),
    "form": ("UCG Google Form Template", "forms", "1-LLH8MvdZVirtOoXdx1vy83OLZDl11T9zQEAXh3cCGk", "UCG header image, Saira Condensed headings and questions, Arial text and the Navy theme color. Collects respondents' emails."),
}


def template_url(key, action="copy"):
    _, kind, fid, _ = TEMPLATES[key]
    return f"https://docs.google.com/{kind}/d/{fid}/{action}"


def template_cards(ctx, keys, title="Templates"):
    cards = []
    for k in keys:
        name, _, _, what = TEMPLATES[k]
        cards.append(f'''<div class="card template-card"><a href="{template_url(k, "edit")}" class="template-preview"><img src="{R}site/examples/templates/{k}.png" alt="Preview of the {E(name)}" loading="lazy"></a>
<h3>{E(name)}</h3><p class="small">{E(what)}</p>
<div class="btn-row"><a class="btn btn--sm" href="{template_url(k)}">Use template →</a><a class="btn btn--sm btn--ghost" href="{template_url(k, "edit")}">Preview</a></div></div>''')
    layout = "--min:340px" if len(keys) % 2 == 0 else "--min:260px;max-width:440px"  # 2 x 2, or one card not stretched
    return vis(title, f'<div class="grid" style="{layout}">{"".join(cards)}</div>',
               "These are also in the Template gallery in Google Docs, Sheets, Slides and Forms, under United Club Gymnastics. “Use template” gives you your own copy (UCG Google accounts only); the templates themselves stay untouched.")


DOC_STEPS = [
    "In Google Docs, click <b>Template gallery → United Club Gymnastics</b> and pick the template (or click <b>Use template</b> above). Rename it and save it in your team's folder.",
    "Replace every <b>[bracketed]</b> placeholder and delete the guidance lines.",
    "Use the built-in styles (Title, Heading 1, Heading 2, Normal text) from the style menu instead of formatting by hand, so headings stay on brand.",
    "Delete any section you don't need rather than leaving it empty.",
]
SLIDE_STEPS = [
    "In Google Slides, click <b>Template gallery → United Club Gymnastics → UCG Slides Template</b> (or <b>Use template</b> above) and rename the deck.",
    "Delete the example slides you don't need. Duplicate the ones you do (right-click → Duplicate) and replace the text.",
    "For a fresh slide, use <b>New slide</b> and pick a layout: they're already in UCG colors and fonts, with the footers in place.",
    "Type titles in capitals (Slides can't force caps), and keep to Saira Condensed and Arial.",
    "Swap the cover photo for one from the <a href=\"../photos/\">photo library</a> if you like; keep the Navy overlay so the text stays readable.",
]
SHEET_STEPS = [
    "In Google Sheets, click <b>Template gallery → United Club Gymnastics → UCG Sheets Template</b> (or <b>Use template</b> above) and rename the file.",
    "Rename the tab and the column headers. Keep the header row frozen.",
    "Type into the banded rows; extend the banding with Format → Alternating colors if you add rows.",
    "Pick Status and Discipline from the dropdowns. The status words drive the colors.",
    "Charts and new cells pick up the UCG theme (Format → Theme) automatically.",
]

FORM_STEPS = [
    "In Google Forms, click <b>Template gallery → United Club Gymnastics → UCG Google Form Template</b> (or <b>Use template</b> above).",
    "Rename the form and write a short description: what it's for, who should fill it in, and the deadline.",
    "Delete the sample question and add yours. Keep question titles short and put detail in the question description.",
    "Leave the theme as it is (header image, Saira Condensed, Arial, Navy). Swap the header image only for another UCG-branded one.",
    "The form collects respondents' emails. Turn that off in <b>Settings</b> if you don't need them, then <b>Publish</b>.",
]


def how_to_use(steps, title="How to use them"):
    return vis(title, '<ol class="steps">' + "".join(f"<li>{s}</li>" for s in steps) + "</ol>")


# ---------- slides ----------

def slide_theme(ctx):
    slots = [("Dark 1", "#1E2B38", "Navy"), ("Light 1", "#FFFFFF", "White"), ("Dark 2", "#184B56", "Dark Blue Green"),
             ("Light 2", "#DBEBEE", "Light Blue"), ("Accent 1", "#A5C8CF", "Blue Green"), ("Accent 2", "#ADBAE9", "Purple"),
             ("Accent 3", "#F6C328", "Golden Yellow"), ("Accent 4", "#F4694A", "Red Orange")]
    strip = "".join(f'<div style="background:{h};color:{readable_on(h)};{"box-shadow:inset 0 0 0 1px #A5C8CF;" if h in ("#FFFFFF", "#DBEBEE") else ""}">{s}<br><span style="font-weight:400">{n}</span></div>' for s, h, n in slots)
    return vis("Theme colors to set", f'<div class="strip">{strip}</div>')


def slide_gallery(ctx):
    shots = [("cover", "Cover: B&W photo under Navy, huge Saira title"), ("info-cards", "Info cards: one Navy card, the rest light"),
             ("thank-you-band", "Thank-you band: solid Blue Green, big mark"), ("big-numbers", "Big numbers / milestones"),
             ("section-break", "Section break: Navy with apparatus icons"), ("closing", "Closing: solid Golden Yellow, next steps as pills")]
    real = "".join(f'<figure style="margin:0"><img src="{R}site/examples/slides/example-{f}.jpg" alt="{E(c)}" loading="lazy" style="display:block;width:100%;border-radius:10px;box-shadow:0 8px 24px rgba(30,43,56,.16)"><figcaption class="mock-label">{E(c)}</figcaption></figure>' for f, c in shots)
    D = "'Saira Condensed','Arial Narrow',Arial,sans-serif"
    rows = "".join(f'''<div class="abs" style="left:{x}cqw;top:{y}cqw;width:41.3cqw;border-bottom:1px solid #A5C8CF;padding-bottom:1.4cqw;display:flex;gap:2cqw;align-items:baseline">
<span style="font-family:{D};font-weight:700;font-size:{pt(19.5)};color:#184B56">{n}</span><span style="font-family:Arial;font-weight:700;font-size:{pt(14)};color:#1E2B38">{t}</span></div>'''
                   for x, y, n, t in ((6.2, 13, "01", "Eat, buffet is open"), (6.2, 19.7, "02", "Sponsors and volunteers"), (6.2, 26.4, "03", "Judges' awards"),
                                      (52.5, 13, "04", "Individual awards"), (52.5, 19.7, "05", "Team awards"), (52.5, 26.4, "06", "Looking ahead")))
    agenda = f'''<div class="cq slide" style="background:#DBEBEE"><div class="abs display" style="left:6.2cqw;top:5cqw;font-size:{pt(39)};color:#1E2B38">Tonight</div>{rows}
<div class="abs" style="left:3cqw;bottom:1.4cqw;font-family:{D};font-weight:700;font-size:{pt(10)};color:#184B56">@unitedclubgymnastics</div></div>'''
    status = "".join(f'<td style="padding:1cqw 1.4cqw;border:1px solid #A5C8CF;background:{bg};color:{fg};font-family:Arial;font-size:{pt(11)};font-weight:700">{t}</td>'
                     for t, bg, fg in (("On track", "#DBEBEE", "#184B56"), ("At risk", "#F6C328", "#1E2B38"), ("Blocked", "#F4694A", "#1E2B38")))
    work = f'''<div class="cq slide" style="background:#FFFFFF"><div class="abs display" style="left:6.2cqw;top:5cqw;font-size:{pt(30)};color:#1E2B38">Events department</div>
<table class="abs" style="left:6.2cqw;top:13cqw;border-collapse:collapse"><tr>{status}</tr></table>
<ul class="abs" style="left:6.2cqw;top:20cqw;right:6.2cqw;margin:0;padding-left:2.4cqw;font-family:Arial;font-size:{pt(15)};line-height:1.45;color:#1E2B38"><li>Rebrand rollout continues across the org</li><li>Sanctioning is open: 12 events so far</li></ul>
<div class="abs" style="left:0;right:0;bottom:0;height:9cqw;border-top:.4cqw solid #A5C8CF;display:flex;align-items:center;gap:3cqw;padding:0 3cqw"><img src="{R}assets/logos/ucg-primary-navy.svg" alt="" style="height:4cqw"><span style="font-family:Arial;font-weight:700;font-size:{pt(8)};color:#1E2B38">FOR THE LOVE OF THE SPORT.</span></div></div>'''
    rebuilt = (f'<figure style="margin:0">{agenda}<figcaption class="mock-label">Agenda: numbers in Dark Blue Green, never Blue Green, on Light Blue.</figcaption></figure>'
               f'<figure style="margin:0">{work}<figcaption class="mock-label">Working meeting: status cells in brand colors with words.</figcaption></figure>')
    return (vis("Examples", f'<div class="grid" style="--min:300px">{real}</div>')
            + vis("More examples", f'<div class="grid" style="--min:300px">{rebuilt}</div>', "Example content."))


def slide_traps(ctx):
    D = "'Saira Condensed','Arial Narrow',Arial,sans-serif"
    def num(color, skip):
        return f'<div class="panel on-lb" style="display:flex;align-items:center;gap:14px"{skip}><span style="font-family:{D};font-weight:700;font-size:48px;color:{color}">01</span><b style="color:#1E2B38">By level</b></div>'
    def foot(color, skip):
        return f'<div class="panel on-lb"{skip}><span style="font-size:13px;color:{color}">UCG Board of Directors · Nationals 2027</span></div>'
    body = (f'<div class="dodont">{dont("Blue Green on Light Blue (1.4:1)", num("#A5C8CF", " data-contrast-skip"))}{do("Dark Blue Green (7.9:1)", num("#184B56", ""))}</div>'
            f'<div class="dodont" style="margin-top:16px">{dont("Gray #74858F footer (3.1:1)", foot("#74858F", " data-contrast-skip"))}{do("Dark Blue Green (7.9:1)", foot("#184B56", ""))}</div>')
    return vis("Before and after", body)


# ---------- docs ----------

def doc_page(ctx):
    A = "Arial,Helvetica,sans-serif"
    D = "'Saira Condensed','Arial Narrow',Arial,sans-serif"
    p = f'''<div class="paper-bed"><div class="paper">
<img src="{R}assets/logos/ucg-document-header.png" alt="UCG document header" style="display:block;width:100%;margin-bottom:28px">
<p style="font-family:{D};font-weight:700;font-size:32px;line-height:1;text-transform:uppercase;margin:0 0 6px;color:#1E2B38">Event sanctioning policy</p>
<p style="font-size:14px;color:#184B56;margin:0 0 22px">Example document · Effective August 1 · Version 1.2 · Owner: Events Department</p>
<p style="font-size:15px;line-height:1.5;margin:0 0 10px">This policy explains how a club gets a meet sanctioned by UCG, who it applies to, and what hosts need to do before and after the event.</p>
<p style="font-family:{D};font-weight:700;font-size:20px;text-transform:uppercase;margin:24px 0 6px;color:#1E2B38">1. Who this applies to</p>
<p style="font-size:15px;line-height:1.5;margin:0 0 10px">Any member club hosting a competition that counts toward UCG standings.</p>
<p style="font-family:{A};font-weight:700;font-size:16px;margin:18px 0 4px;color:#184B56">1.1 What hosts must do</p>
<ul style="font-size:15px;line-height:1.5;margin:0 0 14px;padding-left:22px"><li>Submit the request at least 30 days before the meet.</li><li>Use approved judges for every session.</li><li>Send results within 48 hours.</li></ul>
<table style="width:100%;border-collapse:collapse;margin:0 0 16px"><tr><td style="background:#DBEBEE;padding:12px 14px;font-size:14px;color:#1E2B38;border-radius:4px"><b>Key rule:</b> results must be sent within 48 hours of the last session.</td></tr></table>
<table style="width:100%;border-collapse:collapse;font-size:13px"><tr><th style="background:#1E2B38;color:#FFFFFF;text-align:left;padding:8px">Meet size</th><th style="background:#1E2B38;color:#FFFFFF;text-align:left;padding:8px">Lead time</th></tr>
<tr><td style="padding:8px;border:.5pt solid #A5C8CF">Under 100 athletes</td><td style="padding:8px;border:.5pt solid #A5C8CF">30 days</td></tr><tr><td style="padding:8px;border:.5pt solid #A5C8CF">100 athletes or more</td><td style="padding:8px;border:.5pt solid #A5C8CF">60 days</td></tr></table>
<div style="display:flex;justify-content:space-between;margin-top:28px;font-size:12px;color:#184B56;border-top:1px solid #A5C8CF;padding-top:8px"><span>Event sanctioning policy · Effective August 1</span><span>Page 1</span></div>
</div></div>'''
    return vis("What a UCG policy looks like", p, "Example document with placeholder content.")


def doc_styles(ctx):
    A = "Arial,Helvetica,sans-serif"
    D = "'Saira Condensed','Arial Narrow',Arial,sans-serif"
    rows = [("Title", f"font-family:{D};font-weight:700;font-size:30px;text-transform:uppercase;color:#1E2B38", "Code of conduct"),
            ("Subtitle", f"font-family:{A};font-size:14px;color:#184B56", "Effective August 1 · Version 2.0"),
            ("Heading 1", f"font-family:{D};font-weight:700;font-size:20px;text-transform:uppercase;color:#1E2B38", "2. Expectations"),
            ("Heading 2", f"font-family:{A};font-weight:700;font-size:16px;color:#184B56", "2.1 At competitions"),
            ("Heading 3", f"font-family:{A};font-weight:700;font-size:14px;color:#1E2B38", "Spectators"),
            ("Normal text", f"font-family:{A};font-size:14px;color:#1E2B38", "Treat athletes, judges and volunteers with respect."),
            ("Link", f"font-family:{A};font-size:14px;color:#184B56;text-decoration:underline", "unitedclubgymnastics.org")]
    body = "".join(f'<div style="display:grid;grid-template-columns:minmax(110px,150px) 1fr;gap:16px;align-items:baseline;padding:12px 0;border-top:1px solid #A5C8CF"><b class="small">{n}</b><span style="{s};line-height:1.2">{E(t)}</span></div>' for n, s, t in rows)
    return vis("The styles, rendered", f'<div class="card">{body}</div>')


def letter_mock(ctx):
    return vis("Letter layout", f'''<div class="paper-bed"><div class="paper" style="max-width:560px;font-size:13px">
<img src="{R}assets/logos/ucg-primary-navy.svg" alt="United Club Gymnastics" style="height:44px;display:block;margin-bottom:22px">
<p style="margin:0;font-size:12px;line-height:1.6"><b>Date:</b> 01.01.27<br><b>From:</b> Jordan Lee<br><b>Subject:</b> Thank you for hosting</p>
<p style="margin:18px 0 10px;line-height:1.55">Thank you for hosting this season's regional meet. Your volunteers kept every session on time, and athletes noticed.</p>
<p style="margin:0 0 18px;line-height:1.55">We'd love to have you back next year.</p>
<p style="margin:0;line-height:1.5">Jordan Lee<br>Events Coordinator<br><span style="color:#184B56;font-weight:700">unitedclubgymnastics.org</span></p></div></div>''', "Example letter.")


# ---------- sheets ----------

def sheet_mock(ctx):
    cols = "".join(f'<th class="ch">{c}</th>' for c in " ABCDE")
    data = [("Example State", "WAG", "#ADBAE9", "24", "Registered", "#DBEBEE", "#184B56", "$1,320.00"),
            ("River City Gym", "MAG", "#A5C8CF", "12", "Pending", "#F6C328", "#1E2B38", "$660.00"),
            ("Northside Flyers", "T&amp;T", "#F6C328", "9", "Missing forms", "#F4694A", "#1E2B38", "$495.00"),
            ("Lakeview Club", "WAG", "#ADBAE9", "17", "Registered", "#DBEBEE", "#184B56", "$935.00")]
    rows = ""
    for i, (club, disc, dc, n, st, sb, sf, fee) in enumerate(data):
        z = "#FFFFFF" if i % 2 == 0 else "#DBEBEE"
        rows += (f'<tr><td class="rh">{i + 3}</td><td style="background:{z};color:#1E2B38">{club}</td><td style="background:{z};color:#1E2B38">{disc}</td>'
                 f'<td style="background:{z};color:#1E2B38;text-align:right">{n}</td><td style="background:{sb};color:{sf};font-weight:700">{st}</td><td style="background:{z};color:#1E2B38;text-align:right">{fee}</td></tr>')
    t = f'''<div class="table-wrap" style="background:#FFFFFF"><table class="sheet"><tr>{cols}</tr>
<tr><td class="rh">1</td><td colspan="5" style="font-family:'Saira Condensed','Arial Narrow',Arial;font-weight:700;font-size:20px;text-transform:uppercase;color:#1E2B38;border-color:transparent">Nationals registrations</td></tr>
<tr><td class="rh">2</td><th style="background:#1E2B38;color:#FFFFFF">Club</th><th style="background:#1E2B38;color:#FFFFFF">Discipline</th><th style="background:#1E2B38;color:#FFFFFF;text-align:right">Athletes</th><th style="background:#1E2B38;color:#FFFFFF">Status</th><th style="background:#1E2B38;color:#FFFFFF;text-align:right">Fees</th></tr>
{rows}<tr><td class="rh">7</td><td style="background:#1E2B38;color:#FFFFFF;font-weight:700">Total</td><td style="background:#1E2B38"></td><td style="background:#1E2B38;color:#FFFFFF;font-weight:700;text-align:right">62</td><td style="background:#1E2B38"></td><td style="background:#1E2B38;color:#FFFFFF;font-weight:700;text-align:right">$3,410.00</td></tr></table></div>'''
    return vis("What a UCG sheet looks like", t, "Example data.")


def sheet_status(ctx, title=""):
    items = [("Good / done / on track", "#DBEBEE", "#184B56"), ("Attention / pending", "#F6C328", "#1E2B38"),
             ("Urgent / error / blocked", "#F4694A", "#1E2B38"), ("Neutral / info", "#ADBAE9", "#1E2B38")]
    chips = "".join(f'<div style="background:{b};color:{f};border-radius:8px;padding:12px 14px;font-weight:700;font-family:Arial">{t}</div>' for t, b, f in items)
    return vis(title, f'<div class="grid" style="--min:190px">{chips}</div>')


def chart_svg(bg, colors, text, muted, grid):
    vals = [(24, 12, 9), (30, 15, 11), (27, 18, 14)]
    years = ["2025", "2026", "2027"]
    w, h, x0, y0 = 520, 300, 56, 250
    bars, labels = [], []
    for gi, (yr, vs) in enumerate(zip(years, vals)):
        gx = x0 + 20 + gi * 150
        for bi, v in enumerate(vs):
            bh = v * 6.4
            bars.append(f'<rect x="{gx + bi * 38}" y="{y0 - bh:.1f}" width="32" height="{bh:.1f}" rx="3" fill="{colors[bi]}"/>')
        labels.append(f'<text x="{gx + 54}" y="{y0 + 22}" text-anchor="middle" fill="{text}" font-size="14" font-family="Arial">{yr}</text>')
    gridl = "".join(f'<line x1="{x0}" x2="{w - 10}" y1="{y0 - t * 64}" y2="{y0 - t * 64}" stroke="{grid}"/><text x="{x0 - 10}" y="{y0 - t * 64 + 4}" text-anchor="end" fill="{muted}" font-size="12" font-family="Arial">{t * 10}</text>' for t in range(4))
    legend = "".join(f'<rect x="{x0 + i * 120}" y="14" width="14" height="14" rx="3" fill="{c}"/><text x="{x0 + 20 + i * 120}" y="26" fill="{text}" font-size="13" font-family="Arial">{n}</text>' for i, (c, n) in enumerate(zip(colors, ["WAG", "MAG", "T&amp;T"])))
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Example bar chart of athletes by discipline" style="width:100%;height:auto;background:{bg};border-radius:16px">'
            f'{gridl}{"".join(bars)}{"".join(labels)}{legend}</svg>')


def sheet_charts(ctx):
    a = chart_svg("#FFFFFF", ["#1E2B38", "#F4694A", "#184B56"], "#1E2B38", "#1E2B38", "#DBEBEE")
    b = chart_svg("#1E2B38", ["#A5C8CF", "#F6C328", "#ADBAE9"], "#FFFFFF", "#DBEBEE", "#184B56")
    return vis("Charts", f'<div class="compare"><div class="card" style="padding:10px">{a}<p class="mock-label">On white: Navy, Red Orange, Dark Blue Green.</p></div><div class="card" style="padding:10px">{b}<p class="mock-label">On Navy: Blue Green, Golden Yellow, Purple.</p></div></div>', "Example data.")


# ---------- social ----------

def social_formats(ctx):
    frames = [("4 / 5", "Feed post", "1080 × 1350"), ("1 / 1", "Square post", "1080 × 1080"), ("9 / 16", "Story / Reel", "1080 × 1920")]
    t = "".join(f'<div style="display:flex;flex-direction:column;align-items:center"><div style="width:100%;max-width:{170 if r != "9 / 16" else 130}px;aspect-ratio:{r};border:2px dashed #184B56;border-radius:12px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:8px"><b class="small">{n}</b><span class="small muted">{s}</span></div></div>' for r, n, s in frames)
    av = f'<div style="display:flex;gap:14px;align-items:center;justify-content:center"><img src="{R}assets/logos/ucg-avatar-circle.png" alt="Circle avatar" style="width:96px"><img src="{R}assets/logos/ucg-avatar-square.png" alt="Square avatar" style="width:96px;border-radius:12px"></div>'
    return vis("Sizes", f'<div class="grid" style="--min:150px;align-items:end">{t}<div>{av}<p class="mock-label" style="text-align:center">Avatars</p></div></div>')


def social_posts(ctx):
    f = {fr["slug"]: fr for fr in ctx.frames()}
    handle = lambda c: f'<div class="abs" style="left:{px(64)};bottom:{px(52)};font-family:Arial;font-weight:700;font-size:{px(36)};color:{c}">@unitedclubgymnastics</div>'
    p1 = f'''<div class="cq post on-bg"><img class="abs" src="{R}assets/logos/ucg-mark-navy.svg" alt="" style="width:{px(110)};right:{px(64)};top:{px(64)}">
<div class="abs display" style="left:{px(64)};right:{px(64)};top:{px(330)};font-size:{px(190)};color:#1E2B38">For the love of the sport.</div>{handle("#184B56")}</div>'''
    p2 = f'''<div class="cq post" style="background:#1E2B38"><img class="abs" src="{thumb(f["vault-layout"]["bw"])}" alt="" style="top:0;left:0;width:100%;height:68%;object-fit:cover">
<div class="abs" style="left:0;right:0;bottom:0;height:34%;background:#1E2B38"></div>
<div class="abs display" style="left:{px(64)};right:{px(64)};top:{px(960)};font-size:{px(150)};color:#FFFFFF">Join the club</div>{handle("#DBEBEE")}</div>'''
    icons = "".join(f'<img src="{R}assets/icons/event/{s}-navy.svg" alt="{n}" style="width:{px(250)}">' for s, n in (("mag", "MAG"), ("wag", "WAG"), ("tnt", "T&amp;T")))
    p3 = f'''<div class="cq post on-purple"><div class="abs" style="left:{px(64)};right:{px(64)};top:{px(330)};display:flex;justify-content:space-between">{icons}</div>
<div class="abs display" style="left:{px(64)};right:{px(64)};top:{px(700)};font-size:{px(120)};color:#1E2B38;text-align:center">MAG · WAG · T&amp;T</div>
<div class="abs" style="left:{px(64)};right:{px(64)};top:{px(860)};font-family:Arial;font-size:{px(46)};color:#1E2B38;text-align:center">Three disciplines. One community.</div>{handle("#1E2B38")}</div>'''
    def car(bg, fg, eyebrow, title, sub, arrow=True):
        return f'''<div class="cq post" style="background:{bg}"><div class="abs" style="left:{px(64)};top:{px(80)};font-family:Arial;font-weight:700;font-size:{px(44)};letter-spacing:.2em;text-transform:uppercase;color:{fg}">{eyebrow}</div>
<div class="abs display" style="left:{px(64)};right:{px(64)};top:{px(420)};font-size:{px(150)};color:{fg}">{title}</div><div class="abs" style="left:{px(64)};right:{px(64)};top:{px(900)};font-family:Arial;font-size:{px(54)};color:{fg}">{sub}</div>
{f'<div class="abs" style="right:{px(64)};bottom:{px(48)};font-family:Arial;font-weight:700;font-size:{px(70)};color:{fg}">→</div>' if arrow else ""}</div>'''
    carousel = (car("#1E2B38", "#FFFFFF", "Nationals 2027", "Everything you need to know", "Swipe for the details")
                + car("#DBEBEE", "#1E2B38", "When?", "April 2027", "Portland, Oregon")
                + car("#F6C328", "#1E2B38", "How to sign up?", "Link in bio", "unitedclubgymnastics.org", arrow=False))
    posts = (f'<div>{p1}<p class="mock-label">Headline post: color fill, big type, small mark.</p></div>'
             f'<div>{p2}<p class="mock-label">Photo post: B&amp;W photo, White type on a Navy band.</p></div>'
             f'<div>{p3}<p class="mock-label">Event post: event icons on a color block.</p></div>')
    return (vis("Post recipes", f'<div class="grid" style="--min:230px">{posts}</div>')
            + vis("Carousel", f'<div class="grid" style="--min:260px">{carousel}</div>', "Example content. One idea per slide, an arrow until the last."))


def event_pattern(ctx):
    base = f"{R}assets/patterns/ucg-event-pattern-2026-27"
    return (f'<img src="{base}.png" alt="Event pattern: rows of the UCG mark, UCG, FOR THE LOVE OF THE SPORT and 2026–2027 NATIONALS in Light Blue on Blue Green" '
            f'style="display:block;width:100%;height:auto;border-radius:16px">'
            f'<div class="btn-row" style="margin-top:12px"><a class="btn btn--sm" href="{base}.svg" download>SVG</a><a class="btn btn--sm btn--ghost" href="{base}.png" download>PNG</a></div>')


# ---------- expressive design page ----------

def mixed_piece(ctx):
    icons = ["mag-rings", "wag-balance-beam", "tnt-trampoline", "mag-pommel-horse"]  # each row shifts one to the right
    mixed = f'''<div class="cq post" style="background:#8BB7E3;width:100%;max-width:360px;flex:1 1 260px">
<div class="abs" style="inset:0;opacity:.5;display:grid;grid-template-columns:repeat(4,1fr);gap:{px(40)};padding:{px(40)}" aria-hidden="true">{"".join(f'<img src="{R}assets/icons/apparatus-solid/{icons[(c - r) % 4]}-white.svg" alt="" style="width:100%">' for r in range(5) for c in range(4))}</div>
<div class="abs" style="left:{px(80)};right:{px(80)};top:{px(380)};background:#1E2B38;border-radius:{px(40)};padding:{px(70)}">
<p style="margin:0 0 {px(20)};font-family:Arial;font-weight:700;font-size:{px(30)};letter-spacing:.2em;text-transform:uppercase;color:#DBEBEE">Nationals 2027</p>
<p class="display" style="margin:0 0 {px(30)};font-size:{px(120)};color:#FFFFFF">Registration opens Dec 1</p>
<p style="margin:0;font-family:Arial;font-size:{px(38)};color:#DBEBEE">unitedclubgymnastics.org</p></div></div>'''
    return vis("A mixed piece", f'<div style="display:flex;flex-wrap:wrap;gap:20px;align-items:center">{mixed}<p class="small" style="max-width:360px">Expressive background and pattern, while the facts (event, date, link) sit on a solid Navy panel in core colors and plain type.</p></div>', "Example content.")


def expression_lights(ctx):
    text = md_section(ctx.md("references/expressive.md"), "Where expression lives")
    def items(label):
        block = re.search(rf"\*\*{label}.*?\*\*\s*\n\n(.*?)(?=\n\n\*\*|\Z)", text, re.S).group(1)
        out = []
        for line in re.findall(r"^- (.+)$", block, re.M):
            m = re.match(r"\*\*(.+?)\*\*\s*(.*)", line)
            head, rest = (m.group(1), m.group(2)) if m else (line, "")
            out.append(f'<li style="margin-bottom:10px"><b>{E(head.rstrip(".,"))}</b>{(" — " + E(rest)) if rest else ""}</li>')
        return "".join(out)
    card = lambda verdict, title, body: (f'<div class="card"><span class="verdict verdict--{verdict}">{title}</span>'
                                         f'<ul style="margin:6px 0 0;padding-left:20px">{body}</ul></div>')
    cards = card("do", "Green light: push it", items("Green light")) + card("dont", "Red light: hold the line", items("Red light"))
    return vis("", f'<div class="grid" style="--min:280px">{cards}</div>') + mixed_piece(ctx)


def anchor_posters(ctx):
    mark = f"{R}assets/logos/ucg-mark-navy.svg"
    # 1. logo locked: the mark as drawn, huge and cropped; color pushed into the expressive range
    p1 = f'''<div class="cq post" style="background:#FF988A"><img class="abs" src="{mark}" alt="" style="width:{px(900)};right:{px(-260)};bottom:{px(-220)}">
<div class="abs display" style="left:{px(64)};right:{px(64)};top:{px(80)};font-size:{px(150)};color:#1E2B38">Nationals<br>2027</div>
<div class="abs" style="left:{px(64)};top:{px(400)};font-family:Arial;font-weight:700;font-size:{px(40)};letter-spacing:.2em;text-transform:uppercase;color:#1E2B38">Portland, OR</div></div>'''
    # 2. color locked: brand palette only; layout and graphics flex
    tiles = [("#A5C8CF", "mag-rings", "navy"), ("#184B56", "wag-balance-beam", "light"),
             ("#ADBAE9", "tnt-trampoline", "navy"), ("#F6C328", "mag-pommel-horse", "navy")]
    grid = "".join(f'<div style="background:{bg};border-radius:{px(30)};display:flex;align-items:center;justify-content:center;padding:{px(40)}">'
                   f'<img src="{R}assets/icons/apparatus-solid/{ic}-{cw}.svg" alt="" style="width:85%"></div>' for bg, ic, cw in tiles)
    p2 = f'''<div class="cq post" style="background:#1E2B38"><div class="abs" style="left:{px(64)};right:{px(64)};top:{px(64)};height:{px(900)};display:grid;grid-template-columns:1fr 1fr;gap:{px(30)}">{grid}</div>
<div class="abs" style="left:{px(64)};right:{px(64)};bottom:{px(150)};font-family:Arial;font-weight:700;font-size:{px(40)};letter-spacing:.2em;text-transform:uppercase;color:#FFFFFF;text-align:center">United Club Gymnastics</div>
<div class="abs" style="left:{px(64)};right:{px(64)};bottom:{px(90)};font-family:Arial;font-size:{px(32)};letter-spacing:.2em;text-transform:uppercase;color:#DBEBEE;text-align:center">For the love of the sport</div></div>'''
    # 3. type locked: big stacked condensed caps; color expressive, no logo needed
    p3 = f'''<div class="cq post" style="background:#504A83"><div class="abs display" style="left:{px(56)};right:{px(40)};top:{px(70)};font-size:{px(255)};line-height:.86;color:#FFFFFF">For<br>the love<br>of the<br>sport.</div></div>'''
    posts = (f'<div>{p1}<p class="mock-label"><b>Logo locked.</b> The mark as drawn, huge and cropped. Color pushed into the expressive range (Coral, Navy text).</p></div>'
             f'<div>{p2}<p class="mock-label"><b>Color locked.</b> Brand palette only. Layout and graphics are free to play.</p></div>'
             f'<div>{p3}<p class="mock-label"><b>Type locked.</b> Big stacked condensed caps. An expressive color (Indigo, White text), no logo needed.</p></div>')
    return vis("One anchor each", f'<div class="grid" style="--min:230px">{posts}</div>', "Example content.")


def mark_moves(ctx):
    def masked(src, color):
        return (f'<div aria-hidden="true" style="width:100%;height:100%;-webkit-mask:url({src}) no-repeat center/contain;'
                f'mask:url({src}) no-repeat center/contain;background:{color}"></div>')
    def outlined(color, width):
        # the mark drawn inline from its construction (tools/mark_geometry.py) as an outline only,
        # with room around it so the stroke is never cropped by the frame
        return f'<div aria-hidden="true" style="width:100%;height:100%">{MG.outline_svg(color, width)}</div>'
    def t(inner, bg, h="150px"):
        cls = "tile on-white" if bg == "#FFFFFF" else "tile"  # white tiles get the card border
        return f'<div class="{cls}" style="background:{bg};min-height:{h};position:relative;overflow:hidden"><div style="width:100%;height:84px">{inner}</div></div>'
    primary = f"{R}assets/logos/ucg-primary-navy.svg"
    mark = f"{R}assets/logos/ucg-mark-navy.svg"
    big_bg = (f'<div class="tile" style="background:#A5C8CF;min-height:150px;position:relative;overflow:hidden">'
              f'<div class="abs" style="width:190px;height:190px;right:-60px;bottom:-70px">{masked(mark, "#DBEBEE")}</div>'
              f'<img src="{primary}" alt="" style="max-height:44px;position:relative"></div>')
    dos = [
        do("Recolor within the palette", t(masked(primary, "#ADBAE9"), "#1E2B38")),
        do("Add a stroke", t(outlined("#DBEBEE", MG.STROKE_GOOD), "#1E2B38")),
        do("Use it huge in the background", big_bg),
    ]
    typed = (f'<div class="tile on-white" style="min-height:150px;gap:12px"><img src="{mark}" alt="" style="max-height:64px">'
             f'<span style="font-family:\'Arial Black\',Arial;font-weight:900;font-size:52px;color:#1E2B38;letter-spacing:-.02em">UCG</span></div>')
    donts = [
        dont("Don't stretch or squash", f'<div class="tile on-white" style="min-height:150px;overflow:hidden"><img src="{primary}" alt="" style="max-height:70px;transform:scale(1.2,.55)"></div>'),
        dont("Don't use off-palette colors", t(masked(primary, "#2FB34A"), "#FFFFFF")),
        dont("Don't retype the wordmark", typed),
        dont("Don't lose contrast", t(masked(primary, "#ADBAE9"), "#DBEBEE")),
        dont("Don't let strokes touch", t(outlined("#DBEBEE", MG.STROKE_TOO_THICK), "#1E2B38")),
    ]
    return (vis("Do", f'<div class="grid" style="--min:220px">{"".join(dos)}</div>')
            + vis("Don't", f'<div class="grid" style="--min:220px">{"".join(donts)}</div>',
                  "Recoloring within the palette works in any material (DG p26, p42). Expressive work adds the six expressive colors, strokes and big crops. See the <a href=\"../logos/\">logo rules</a>."))


def expressive_colors(ctx):
    ex = ctx.brand["colors"]["expressive"]
    sw = "".join(f'''<div style="border-radius:16px;overflow:hidden;border:1px solid #A5C8CF"><div style="background:{h};color:{ex["text_on"][h]};padding:16px 16px 14px;min-height:120px;display:flex;flex-direction:column;justify-content:space-between">
<span style="font-family:Arial;font-weight:700;font-size:32px;line-height:1">Aa</span><span style="font-size:13px;font-weight:700">{"Navy" if ex["text_on"][h] == "#1E2B38" else "White"} text · {ratio(h, ex["text_on"][h]):.1f}:1</span></div>
<div style="background:#FFFFFF;color:#1E2B38;padding:10px 14px;font-size:14px;display:flex;justify-content:space-between;align-items:center"><b>{h}</b><button class="copy" data-copy="{h}">Copy</button></div></div>'''
                 for h in ex["swatches"])
    for h, fg in ex["text_on"].items():  # the page states these pairs pass AA; fail the build if one doesn't
        if ratio(h, fg) < 4.5:
            raise SystemExit(f"expressive text pair {fg} on {h} is below 4.5:1")
    wheel = (f'<div class="card" style="padding:12px;max-width:520px"><img src="{R}assets/palette/ucg-color-wheel.png" alt="UCG color wheel: primary colors on one side, '
             f'secondary on the other, expressive colors in the inner ring" style="display:block;width:100%;height:auto"></div>')
    return (vis("The six, with the text color that works on each", f'<div class="grid" style="--min:136px">{sw}</div>',
                "Only these six. Don't pick shades in between.")
            + vis("How they sit with the brand palette", wheel, "Outer ring: brand primary and secondary colors. Inner ring: the expressive range."))


MERCH = [  # file, alt text, caption (from references/expressive.md "Examples from UCG merch")
    ("merch-logo-recolored-purple.jpg", "Primary logo printed in Purple on a charcoal heather shirt",
     "<b>Recolored.</b> The primary logo, unchanged in shape, printed in Purple (the charcoal is the shirt, not an ink color)."),
    ("merch-badge-distressed.jpg", "Circle badge with a worn, distressed print texture on a charcoal shirt",
     "<b>Textured.</b> A worn print finish over the badge. The shape and type stay as drawn."),
    ("merch-tee-mark-background.jpg", "Blue Green tee with the primary logo on the chest and a huge Light Blue mark cropped off the lower edge",
     "<b>Huge in the background.</b> The mark cropped off the edge, tone on tone, with the primary logo as the anchor."),
    ("merch-crop-top-type.jpg", "Back of a Dark Blue Green crop top with FOR THE LOVE OF THE SPORT. running vertically down the spine",
     "<b>Type does the work.</b> The core message set big and vertical, in condensed caps."),
    ("merch-tee-pattern.jpg", "Tee covered in a repeating pattern of the mark and UCG, with the logotype on the chest",
     "<b>Pattern.</b> An all-over repeat of the mark and UCG, with the logotype on top."),
    ("merch-icons-color-blocks.jpg", "Four palette-color tiles with event icons, a worn texture, and UNITED CLUB GYMNASTICS, FOR THE LOVE OF THE SPORT below",
     "<b>Color blocks.</b> Event icons on four palette tiles. Color and type are the anchors."),
]


def merch_gallery(ctx):
    for f, *_ in MERCH:
        if not (ctx.root / "site/examples/expressive" / f).exists():
            raise SystemExit(f"missing merch example {f}")
    cards = "".join(f'''<figure class="asset" style="margin:0"><img src="{R}site/examples/expressive/{f}" alt="{E(alt)}" loading="lazy" style="display:block;width:100%;aspect-ratio:1;object-fit:cover">
<figcaption class="small" style="padding:12px 14px">{cap}</figcaption></figure>''' for f, alt, cap in MERCH)
    return vis("", f'<div class="grid" style="--min:240px">{cards}</div>',
               "Mockups from UCG's 2026 merch concepts. Each piece keeps at least one anchor and pushes something else.")


def social_print(ctx):
    cards = []
    for g in ("primary", "secondary"):
        for c in ctx.brand["colors"][g]:
            fg = readable_on(c["hex"])
            cards.append(f'<div class="swatch"><div class="swatch-chip" style="background:{c["hex"]};color:{fg};height:80px">PMS {E(c["pantone"])}</div><div class="swatch-body"><b>{E(c["name"])}</b><br><span class="small muted">CMYK {", ".join(str(x) for x in c["cmyk"])}</span></div></div>')
    return vis("Print colors", f'<div class="grid" style="--min:170px">{"".join(cards)}</div>')


def social_banners(ctx):
    items = [("ucg-facebook-cover.png", "Facebook cover", "on-white"), ("ucg-youtube-banner-2048x1152.png", "YouTube banner", "on-white"),
             ("ucg-zoom-background.png", "Zoom background", "on-white"), ("ucg-email-header.png", "Email header (signatures)", "on-navy"),
             ("ucg-email-header-light.png", "Email header (announcements)", "on-white")]
    t = "".join(f'<div class="asset"><div class="{c}" style="padding:14px;display:flex;align-items:center;justify-content:center;min-height:150px"><img src="{R}assets/social/{f}" alt="{n}" loading="lazy" style="max-height:160px"></div><div class="meta"><b>{n}</b><span class="dl"><a href="{R}assets/social/{f}" download>PNG</a></span></div></div>' for f, n, c in items)
    return vis("", f'<div class="grid" style="--min:260px">{t}</div>')


# ---------- video ----------

def anim_gallery(ctx):
    files = sorted(p.name for p in (ctx.root / "assets/animation").glob("*.mp4"))
    tiles = []
    for stem, name in ANIMS:
        main = anim_main(ctx, stem)
        poster = f"{R}site/thumbs/anim/{main[:-4]}.jpg"
        mine = [f for f in files if f == f"{stem}.mp4" or f.startswith(stem + "_")]
        if stem == "ucg-mark-three-disciplines":
            mine = [f for f in mine if not f.startswith("ucg-mark-three-disciplines-in-series")]
        links = "".join(f'<a href="{R}assets/animation/{f}" download>{E(f[len(stem):].strip("_").replace(".mp4", "") or "main").replace("_", " ")}</a>' for f in mine)
        tiles.append(f'''<div class="asset"><video data-autoplay muted loop playsinline preload="none" poster="{poster}" aria-label="{E(name)} animation"><source src="{R}assets/animation/{main}" type="video/mp4"></video>
<div class="meta" style="flex-direction:column;align-items:flex-start"><b>{E(name)}</b><span class="dl" style="flex-wrap:wrap">{links}</span></div></div>''')
    return vis("The animations", f'<div class="grid" style="--min:240px">{"".join(tiles)}</div>',
               "Videos play when they scroll into view. Downloads: square, vertical (9:16), wide (16:9), in navy or light.")


def reel_safe(ctx):
    f = {fr["slug"]: fr for fr in ctx.frames()}
    W = 1080
    s = f'''<div class="cq story overlay-dark" style="width:100%;max-width:300px;flex:1 1 220px"><img class="photo-fill" src="{thumb(f["floor-run"]["bw"])}" alt="">
<div class="abs" style="left:0;right:0;top:0;height:{px(250, W) if False else "13.02%"};background:rgba(244,105,74,.45)" aria-hidden="true"></div>
<div class="abs" style="left:0;right:0;bottom:0;height:19.79%;background:rgba(244,105,74,.45)" aria-hidden="true"></div>
<div class="abs" style="left:0;top:13.02%;bottom:19.79%;width:{px(120)};background:rgba(244,105,74,.3)" aria-hidden="true"></div>
<div class="abs" style="right:0;top:13.02%;bottom:19.79%;width:{px(120)};background:rgba(244,105,74,.3)" aria-hidden="true"></div>
<div class="abs" style="left:{px(140)};right:{px(140)};top:40%"><p style="margin:0 0 {px(20)};font-family:Arial;font-weight:700;font-size:{px(40)};letter-spacing:.2em;text-transform:uppercase;color:#DBEBEE">Nationals 2027</p>
<p class="display" style="margin:0;font-size:{px(112)};color:#FFFFFF">Registration opens Dec 1</p></div></div>'''
    notes = '''<ul class="small" style="max-width:380px"><li>Shaded: where Instagram's buttons and captions sit. Keep text out of it (about 250px top, 380px bottom, 120px sides at 1080 × 1920).</li>
<li>Titles in Saira or Greed caps, White on a darkened photo.</li><li>Burned-in captions on every spoken video.</li></ul>'''
    return vis("Reel safe area", f'<div style="display:flex;flex-wrap:wrap;gap:24px;align-items:center">{s}{notes}</div>', "Example content.")


def lower_third(ctx):
    f = {fr["slug"]: fr for fr in ctx.frames()}
    D = "'Saira Condensed','Arial Narrow',Arial,sans-serif"
    s = f'''<div class="cq" style="aspect-ratio:16/9;border-radius:14px;background:#1E2B38"><img class="photo-fill" src="{thumb(f["pommel-horse-swing"]["color"])}" alt="">
<div class="abs" style="left:5cqw;bottom:7cqw;display:flex;align-items:stretch;box-shadow:0 1cqw 3cqw rgba(0,0,0,.25)">
<div style="background:#A5C8CF;width:.8cqw"></div><div style="background:#1E2B38;padding:1.6cqw 2.6cqw">
<p style="margin:0;font-family:{D};font-weight:700;font-size:3.4cqw;line-height:1;text-transform:uppercase;color:#FFFFFF">Jordan Lee</p>
<p style="margin:.6cqw 0 0;font-family:Arial;font-size:1.6cqw;color:#DBEBEE">Example Club · MAG pommel horse</p></div></div>
<div class="abs" style="right:3cqw;top:3cqw;background:#1E2B38;border-radius:1cqw;padding:1cqw 1.6cqw;display:flex;gap:1.4cqw;align-items:center">
<img src="{R}assets/logos/ucg-mark-light.svg" alt="" style="height:2.6cqw"><span style="font-family:{D};font-weight:700;font-size:2.4cqw;color:#FFFFFF">13.450</span></div></div>'''
    return vis("Lower third and score bug", s, "Saira Condensed + Arial, Navy bars, Blue Green accent. Example content.")


# ---------- registry: page slug -> {section heading or _top/_end: function} ----------

VISUALS = {
    "guidelines": {
        "Who we are": lambda c: pillars(c),
        "Voice": voice_examples,
        "Color": lambda c: palette_cards(c) + safe_pairs(c),
        "Type": type_specimens,
        "Logos": lambda c: logo_strip(),
        "Look and feel": feature_tiles,
        "By medium": medium_cards,
    },
    "colors": {
        "_top": lambda c: palette_cards(c) + support_and_expressive(c),
        "Quick list: safe for body text": lambda c: safe_pairs(c, "See it") + contrast_matrix(c),
        "Palette files — assets/palette/": palette_files,
        "_end": overlay_demos,
    },
    "logos": {"Logos — assets/logos/": lambda c: logo_gallery(c) + logo_rules(c)},
    "icons": {"Icons — assets/icons/": lambda c: icon_gallery(c) + icon_usage(c)},
    "photos": {"Photos — assets/photos/": lambda c: photo_treatments(c) + photo_gallery(c)},
    "messaging": {
        "Messaging themes": lambda c: pillars(c, chips=True, title=""),
        "Tone of voice": tone_cards,
        "Headlines": lambda c: headline_posters(c, title=""),
        "One-liners": lambda c: copy_cards(c, "One-liners", title=""),
        "About us (boilerplate)": lambda c: copy_cards(c, "About us (boilerplate)", title=""),
        "Example: social captions": lambda c: caption_mock(c, title=""),
    },
    "email": {"Announcement / newsletter emails (HTML)": email_previews},
    "web": {
        "Layout": web_layout,
        "Type scale (starting point)": web_type,
        "Components": web_components,
        "Dark mode": web_dark,
    },
    "slides": {
        "_intro": lambda c: template_cards(c, ["slides"], "The template") + how_to_use(SLIDE_STEPS, "How to use it"),
        "Slide types": slide_gallery,
        "Contrast traps seen in real decks": slide_traps,
        "Setup": slide_theme,
    },
    "docs": {"_intro": lambda c: template_cards(c, ["policy", "change-proposal", "minutes", "email-draft"]) + how_to_use(DOC_STEPS),
             "Google Forms": lambda c: template_cards(c, ["form"], "The form template") + how_to_use(FORM_STEPS, "How to use it")},
    "sheets": {
        "_intro": lambda c: template_cards(c, ["sheets"], "The template") + how_to_use(SHEET_STEPS, "How to use it")
                            + sheet_mock(c) + sheet_status(c, "Status colors") + sheet_charts(c),
    },
    "social": {
        "Formats": social_formats,
        "Post recipes (from the design guide)": social_posts,
        "Print": social_print,
        "Social banners — assets/social/": social_banners,
    },
    "expressive": {
        "Where expression lives": expression_lights,
        "The anchor elements": anchor_posters,
        "What you can do with the mark": mark_moves,
        "Expressive colors": expressive_colors,
        "The event pattern": lambda c: vis("", event_pattern(c)),
        "Examples from UCG merch": merch_gallery,
    },
    "video": {
        "Mark animations (ready to use)": anim_gallery,
        "Reels and short videos": reel_safe,
        "Livestream and broadcast graphics": lower_third,
    },
}
