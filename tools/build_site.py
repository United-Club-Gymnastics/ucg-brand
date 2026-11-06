"""Build the human-friendly brand site from the same markdown the agents read.

Each page = one markdown file (or some of its H2 sections) rendered to HTML,
plus visual examples from tools/site_visuals.py attached to named sections.
The .md files are never modified. Output: <slug>/index.html for each page,
site/email-example-dark.html, and photo/animation thumbnails in site/thumbs/.

Usage (from the repo root):  python tools/build_site.py
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_visuals as V  # noqa: E402

# slug, nav title, markdown file, H2 sections to include (None = all), one-line blurb
PAGES = [
    ("guidelines", "Brand guidelines", "BRAND.md", None,
     "The core rules on one page: who we are, voice, color, type, logos, look and feel, and the pre-publish checklist."),
    ("colors", "Color & contrast", "references/color-pairs.md", None,
     "The palette, every approved text pairing, and how to keep everything readable."),
    ("logos", "Logos", "references/assets.md", ["Logos — assets/logos/", "Not in this repo"],
     "Every UCG logo in every colorway, ready to download, and how to use them."),
    ("icons", "Icons", "references/assets.md", ["Icons — assets/icons/"],
     "UCG's event and apparatus pictograms in navy, light blue and white."),
    ("photos", "Photos", "references/assets.md", ["Photos — assets/photos/"],
     "Curated 2026 Nationals photos, in color and black-and-white, with alt text."),
    ("messaging", "Messaging & voice", "references/messaging.md", None,
     "How UCG sounds: messaging themes, tone, approved headlines and copy you can use."),
    ("email", "Email", "references/email.md", None,
     "The announcement email template and fonts that work in inboxes."),
    ("web", "Websites & tools", "references/web.md", None,
     "CSS tokens, type scale and components for UCG websites and web apps."),
    ("slides", "Google Slides", "references/slides.md", None,
     "Start every deck from the UCG Slides template, with guidance for going beyond it."),
    ("docs", "Google Docs & Forms", "references/docs.md", None,
     "Templates for policies, change proposals, meeting minutes, email drafts and forms."),
    ("sheets", "Google Sheets", "references/sheets.md", None,
     "Start from the UCG Sheets template: header rows, status colors and charts that stay readable."),
    ("social", "Social & print", "references/social.md", ["Formats", "Post recipes (from the design guide)", "Captions", "Print"],
     "Post recipes, captions, banners and print colors."),
    ("expressive", "Expressive design", "references/expressive.md", None,
     "Merch, campaigns, event graphics and Nationals: how far to push, and the anchors that keep it UCG."),
    ("video", "Video & Reels", "references/video.md", None,
     "Animated mark loops, Reel safe areas and livestream graphics."),
]
# H2 sections deliberately shown on a different page than their markdown file
EXTRA_SECTIONS = {
    ("references/assets.md", "Social banners — assets/social/"): "social",
    ("references/assets.md", "Patterns — assets/patterns/"): "expressive",  # hidden there: "The event pattern" covers it
    ("references/assets.md", "Palette files — assets/palette/"): "colors",
}
RESERVED = {"assets", "templates", "tokens", "tools", "skills", "references", "site"}

MD_TO_PAGE = {
    "BRAND.md": "guidelines", "color-pairs.md": "colors", "messaging.md": "messaging", "email.md": "email",
    "web.md": "web", "slides.md": "slides", "docs.md": "docs", "sheets.md": "sheets", "social.md": "social",
    "expressive.md": "expressive", "video.md": "video", "assets.md": "logos",
}
DIR_TO_PAGE = {"assets/logos": "logos", "assets/icons": "icons", "assets/photos": "photos",
               "assets/animation": "video", "assets/social": "social", "references": "guidelines"}

GITHUB = "https://github.com/United-Club-Gymnastics/ucg-brand"
RAW = "https://united-club-gymnastics.github.io/ucg-brand"
FONTS_DRIVE = "https://drive.google.com/drive/folders/1SUukrVratYo8sd4KxiF5_eztUnhAV-_o"
PHOTOS_DRIVE = "https://drive.google.com/drive/folders/1M7wFuZvl7AUGmU7Rzh3bu_vErSauU2ZZ"


# ---------- human-page edits: what people see differs from what agents read ----------
# Text that only helps agents (setup code, file tables, prose the visuals already show) is
# hidden on the illustrated pages; the markdown keeps all of it.

def visual_only(frag):
    """Keep only the section heading; the section's visual carries the content."""
    m = re.match(r"\s*(<h2[^>]*>.*?</h2>)", frag, re.S)
    return m.group(1) if m else ""


def drop_text(*starts):
    """Remove paragraphs and list items whose text starts with one of `starts`."""
    def edit(frag):
        soup = BeautifulSoup(frag, "html.parser")
        for el in soup.find_all(["p", "li"]):
            if el.get_text(" ", strip=True).startswith(starts):
                el.decompose()
        return str(soup)
    return edit


def drop_lists(frag):
    soup = BeautifulSoup(frag, "html.parser")
    for el in soup.find_all(["ul", "ol"]):
        el.decompose()
    return str(soup)


def replace_prose(new_html):
    return lambda frag: visual_only(frag) + new_html


def first_paragraph(frag):
    m = re.search(r"<p>.*?</p>", frag, re.S)
    return m.group(0) if m else ""


def colors_intro(frag):
    # these sentences describe the full table, which the page doesn't show
    return re.sub(r"\s*The 'Guide' column.*?(</p>)", lambda m: m.group(1), frag, count=1, flags=re.S)


PHOTOS_INTRO = ('<p>163 photos from 2026 UCG Nationals by photographer Bryan Johnson, each in a color and a '
                'black-and-white edit (326 files), 2000px on the long edge. Pick the B&amp;W edit for athlete features with white type, and the color edit for community and '
                'belonging. Use them for UCG materials only, and crop rather than distort. The full Nationals sets '
                f'<a href="{PHOTOS_DRIVE}">live in the UCG brand toolkit</a>.</p>')

# slug -> {"hide": sections not shown, "edit": {section or "_intro": fn(html) -> html}, "order": sections to put first}
HUMAN = {
    "colors": {"hide": ["Full table"], "edit": {"_intro": colors_intro}},
    "logos": {"edit": {"Logos — assets/logos/": drop_text("Badges are two-tone", "Also in")}},
    "icons": {"edit": {"Icons — assets/icons/": visual_only}},
    "photos": {"edit": {"Photos — assets/photos/": replace_prose(PHOTOS_INTRO)}},
    "messaging": {"edit": {"Messaging themes": visual_only, "Tone of voice": drop_lists, "Headlines": visual_only,
                           "One-liners": visual_only, "About us (boilerplate)": visual_only,
                           "Example: social captions": visual_only}},
    "email": {"hide": ["Plain-text and personal emails (Gmail, replies)"]},
    "web": {"hide": ["Setup"]},
    "slides": {"hide": ["Grid and type", "Building decks with the API (for agents)"]},
    "docs": {"hide": ["Page setup", "Styles", "Writing policies", "Letters and memos", "Building docs with the API (for agents)"],
             "edit": {"_intro": first_paragraph,  # the template cards replace the link list
                      "Google Forms": visual_only}},
    "sheets": {"edit": {"_intro": drop_text("The details below")}},
    "expressive": {"hide": ["Patterns — assets/patterns/"],
                   "edit": {"Where expression lives": visual_only,
                            "Expressive colors": replace_prose("<p>Six extra colors for expressive work only, on top of the brand palette. "
                                                               "Never use them in official communications, wayfinding, UI, Google Docs, Slides or Sheets.</p>"),
                            "Examples from UCG merch": visual_only}},
}

CONTRAST_RULE = "text needs a contrast ratio of at least 4.5:1 against its background, large text 3:1"
TERMS = {  # first mention on each page gets a short definition and a link: term -> (link, definition)
    "WCAG": ("https://www.w3.org/WAI/standards-guidelines/wcag/",
             "the Web Content Accessibility Guidelines, the international standard for accessible web content"),
    "AA": ("https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum",
           f"the standard level of WCAG, the Web Content Accessibility Guidelines. In short, {CONTRAST_RULE}"),
    "WCAG AA": ("https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum",
                f"the standard level of the Web Content Accessibility Guidelines: {CONTRAST_RULE}"),
}
SKIP_TERM_IN = {"code", "pre", "a", "button", "script", "style", "summary", "th", "label"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


def explain_terms(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    todo = {"WCAG", "AA"}
    for node in list(soup.find_all(string=re.compile(r"\b(WCAG|AA)\b"))):
        if not todo:
            break
        parents = [p for p in node.parents if p.name]
        if any(p.name in SKIP_TERM_IN or {"vis-title", "tag", "mh"} & set(p.get("class") or []) for p in parents):
            continue
        m = re.search(r"\bWCAG AA\b|\bWCAG\b|\bAA\b", node)
        if not m or not todo & set(m.group(0).split()):
            continue
        term = m.group(0)
        link, note = TERMS[term]
        if term == "AA" and "WCAG" not in todo:
            note = f"WCAG's standard level: {CONTRAST_RULE}"
        todo -={"WCAG", "AA"} if term != "WCAG" else {"WCAG"}  # the AA definition spells out WCAG too
        heading = next((p for p in parents if p.name in HEADINGS), None)
        if heading:  # define it in a line under the heading rather than inside it
            heading.insert_after(BeautifulSoup(f'<p class="term-def"><a class="term" href="{link}">{term}</a> is {html.escape(note)}.</p>', "html.parser"))
            continue
        node.replace_with(BeautifulSoup(f'{html.escape(node[:m.start()])}<a class="term" href="{link}">{term}</a>'
                                        f'<span class="term-def"> ({html.escape(note)})</span>{html.escape(node[m.end():])}', "html.parser"))
    return str(soup)


LOGO_TILE = {"navy": "on-lb", "light": "on-navy", "white": "on-dbg", "black": "on-white"}


def table_examples(html_text):
    """Add a visual column to tables of colors and logos."""
    soup = BeautifulSoup(html_text, "html.parser")
    for table in soup.find_all("table"):
        heads = [th.get_text(" ", strip=True) for th in table.find_all("th")]
        rows = table.find("tbody").find_all("tr") if table.find("tbody") else []

        def add(label, cell_for):
            th = soup.new_tag("th")
            th.string = label
            table.find("tr").insert(0, th)
            for tr in rows:
                td = BeautifulSoup(f'<td class="ex-cell">{cell_for(tr)}</td>', "html.parser")
                tr.insert(0, td)

        if "Hex" in heads:
            i = heads.index("Hex")

            def swatch(tr):
                hexv = tr.find_all("td")[i].get_text(strip=True)
                return f'<span class="mini-swatch" style="background:{hexv}" role="img" aria-label="{hexv} swatch"></span>'
            add("Swatch", swatch)
        elif any(h.startswith("Files") for h in heads) or heads[:1] == ["<logo>"]:
            col = next(k for k, h in enumerate(heads) if h.startswith("Files") or h == "<logo>")

            def logo(tr):
                m = re.search(r"ucg-([a-z-]+?)-(?:\{|…)", tr.find_all("td")[col].get_text()) or \
                    re.fullmatch(r"([a-z-]+)", tr.find_all("td")[col].get_text(strip=True))
                fam = m.group(1)
                return f'<span class="mini-logo on-white"><img src="../assets/logos/ucg-{fam}-navy.svg" alt="{fam.replace("-", " ")} logo"></span>'
            add("Example", logo)
        elif heads[:1] == ["<colorway>"]:
            def colorway(tr):
                cw = tr.find_all("td")[0].get_text(strip=True)
                return f'<span class="mini-logo {LOGO_TILE[cw]}"><img src="../assets/logos/ucg-primary-{cw}.svg" alt="Primary logo, {cw}"></span>'
            add("Example", colorway)
    return str(soup)


def enhance(html_text):
    return explain_terms(table_examples(html_text))


def render_md(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    # "#hashtag" lines (no space) are not headings; Python-Markdown would treat them as one
    text = re.sub(r"^(\s*>?\s*)#(?=[A-Za-z])", lambda m: m.group(1) + r"\#", text, flags=re.M)
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "attr_list", "toc"],
                             extension_configs={"toc": {"permalink": False}})
    soup = BeautifulSoup(body, "html.parser")
    h1 = soup.find("h1")
    title = h1.get_text() if h1 else ""
    if h1:
        h1.decompose()
    sections, cur = [("_intro", [])], None
    for node in list(soup.contents):
        if getattr(node, "name", None) == "h2":
            sections.append((node.get_text(), [node]))
        else:
            sections[-1][1].append(node)
    return title, [(name, "".join(str(n) for n in nodes)) for name, nodes in sections]


def rewrite_links(fragment, md_path):
    """Point .md links at human pages and fix relative asset paths for pages one level deep."""
    soup = BeautifulSoup(fragment, "html.parser")
    md_dir = (ROOT / md_path).parent
    for tag, attr in (("a", "href"), ("img", "src")):
        for el in soup.find_all(tag):
            url = el.get(attr)
            if not url or re.match(r"^(https?:|mailto:|#)", url):
                continue
            path, _, anchor = url.partition("#")
            target = (md_dir / path).resolve()
            try:
                rel = target.relative_to(ROOT).as_posix()
            except ValueError:
                continue
            name = Path(rel).name
            if name.endswith(".md") and name in MD_TO_PAGE:
                new = f"../{MD_TO_PAGE[name]}/"
            elif rel.rstrip("/") in DIR_TO_PAGE:
                new = f"../{DIR_TO_PAGE[rel.rstrip('/')]}/"
            else:
                new = "../" + rel
            el[attr] = new + (f"#{anchor}" if anchor else "")
    for table in soup.find_all("table"):
        wrap = soup.new_tag("div", attrs={"class": "table-wrap"})
        if len(table.find_all("th")) >= 4:  # wide tables scroll sideways on phones instead of squashing
            table["class"] = "wide"
        table.wrap(wrap)
    return str(soup)


def slug_id(text):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"`[^`]*`", "", text).lower()).strip("-")


def nav_html(active):
    items = ['<a class="nav-link{}" href="../">Overview</a>'.format("")]
    for slug, title, *_ in PAGES:
        cls = " is-active" if slug == active else ""
        cur = ' aria-current="page"' if slug == active else ""
        items.append(f'<a class="nav-link{cls}" href="../{slug}/"{cur}>{html.escape(title)}</a>')
    return "\n".join(items)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} · UCG Brand Kit</title>
<meta name="description" content="{blurb}">
<link rel="icon" href="../assets/logos/ucg-favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@700&display=swap" rel="stylesheet">
<link href="../tokens/ucg.css" rel="stylesheet">
<link href="../site/site.css" rel="stylesheet">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="../"><img src="../assets/logos/ucg-primary-white.svg" alt="United Club Gymnastics"><span>Brand kit</span></a>
    <nav class="header-links" aria-label="Kit links">
      <a href="{raw_url}">Raw markdown</a>
      <a href="{github}">GitHub</a>
    </nav>
  </div>
</header>
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">UCG brand kit</p>
    <h1>{title}</h1>
    <p class="lead">{blurb}</p>
    {toc}
  </div>
</section>
<div class="wrap layout">
  <aside class="sidenav">
    <details class="nav-details" open>
      <summary>All guides</summary>
      <nav aria-label="Guides">
{nav}
      </nav>
    </details>
  </aside>
  <main id="main" class="content">
{content}
    <aside class="agent-note">
      <p class="eyebrow">For AI agents</p>
      <p>This page is generated from <a href="{raw_url}"><code>{md_path}</code></a>. Point AI tools at the raw markdown, not this page.</p>
    </aside>
  </main>
</div>
<footer class="site-footer">
  <div class="wrap">
    <p class="tag">For the Love of the Sport.</p>
    <p>United Club Gymnastics · <a href="https://unitedclubgymnastics.org">unitedclubgymnastics.org</a> · Fonts are licensed to UCG and not included; this site uses Saira Condensed and Arial. UCG volunteers can <a href="{fonts}">download the brand fonts</a>.</p>
  </div>
</footer>
<script src="../site/site.js"></script>
</body>
</html>
"""


def build():
    for slug, *_ in PAGES:
        if slug in RESERVED:
            raise SystemExit(f"page slug '{slug}' collides with a repo folder")
    ctx = V.Context(ROOT)
    ctx.pages = PAGES
    V.prepare_media(ctx)  # thumbnails, posters, dark email copy

    # every H2 of every markdown file must land on exactly one page
    claimed = {}
    for slug, title, md, sections, blurb in PAGES:
        _, secs = render_md(md)
        names = [n for n, _ in secs if n != "_intro"]
        for n in (names if sections is None else sections):
            if n not in names:
                raise SystemExit(f"{slug}: section '{n}' not found in {md}; have {names}")
            claimed[(md, n)] = slug
    claimed.update(EXTRA_SECTIONS)
    for md in {p[2] for p in PAGES}:
        _, secs = render_md(md)
        for n, _ in secs:
            if n != "_intro" and (md, n) not in claimed:
                raise SystemExit(f"section '{n}' of {md} is on no page")

    built = []
    for slug, title, md, sections, blurb in PAGES:
        md_title, secs = render_md(md)
        visuals = V.VISUALS.get(slug, {})
        chosen = [(n, h) for n, h in secs if (n == "_intro" and sections is None) or
                  (n != "_intro" and claimed.get((md, n)) == slug)]
        for (emd, en), eslug in EXTRA_SECTIONS.items():
            if eslug == slug:
                chosen += [(n, h) for n, h in render_md(emd)[1] if n == en]
        names = [n for n, _ in chosen]
        human_names = list(HUMAN.get(slug, {}).get("hide", [])) + [k for k in HUMAN.get(slug, {}).get("edit", {}) if k != "_intro"]
        for key in human_names:
            if key not in names:
                raise SystemExit(f"{slug}: HUMAN edit names missing section '{key}'; have {names}")
        for key in visuals:
            if key not in names and key not in ("_top", "_end"):
                raise SystemExit(f"{slug}: visual attached to missing section '{key}'; have {names}")
        parts = []
        if "_top" in visuals:
            parts.append(visuals["_top"](ctx))
        toc_items = []
        human = HUMAN.get(slug, {})
        for n, h in chosen:
            if n in human.get("hide", ()):
                continue
            src_md = next((emd for (emd, en) in EXTRA_SECTIONS if en == n), md)
            frag = rewrite_links(h, src_md)
            sid = slug_id(n) if n != "_intro" else "intro"
            if n != "_intro":
                frag = re.sub(r"<h2[^>]*>", f'<h2 id="{sid}">', frag, count=1)
                frag = re.sub(r"(<h2[^>]*>.*?) — <code>[^<]*</code>(</h2>)", lambda m: m.group(1) + m.group(2), frag, count=1)  # drop file paths from page headings
                toc_items.append(f'<a href="#{sid}">{html.escape(re.sub(r" — .*$", "", re.sub(r"`", "", n)))}</a>')
            if n in human.get("edit", {}):
                frag = human["edit"][n](frag)
            extra = visuals[n](ctx) if n in visuals else ""
            parts.append(f'<section class="doc-section" id="sec-{sid}">\n<div class="prose">{frag}</div>\n{extra}\n</section>')
        if "_end" in visuals:
            parts.append(visuals["_end"](ctx))
        toc = ('<nav class="toc" aria-label="On this page">' + "".join(toc_items) + "</nav>") if len(toc_items) > 1 else ""
        page = TEMPLATE.format(title=html.escape(title), blurb=html.escape(blurb), toc=toc, nav=nav_html(slug),
                               content=enhance("\n".join(parts)), fonts=FONTS_DRIVE, raw_url=f"{RAW}/{md}", md_path=md, github=GITHUB)
        if any(ord(ch) < 32 and ch not in "\t\n\r" for ch in page):
            raise SystemExit(f"{slug}: control characters in output (a bad regex replacement?)")
        out = ROOT / slug / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page, encoding="utf-8")
        built.append(slug)
    print("built", len(built), "pages:", ", ".join(built))


if __name__ == "__main__":
    build()
