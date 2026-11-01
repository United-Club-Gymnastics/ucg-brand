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
     "The announcement email template, fonts that work in inboxes, and signatures."),
    ("web", "Websites & tools", "references/web.md", None,
     "CSS tokens, type scale and components for UCG websites and web apps."),
    ("slides", "Google Slides", "references/slides.md", None,
     "Grid, type sizes and slide types, from the Nationals 2027 Banquet deck."),
    ("docs", "Google Docs", "references/docs.md", None,
     "Paragraph styles and layout for policies, guides and letters."),
    ("sheets", "Google Sheets", "references/sheets.md", None,
     "Header rows, status colors and charts that stay readable."),
    ("social", "Social & print", "references/social.md", ["Formats", "Post recipes (from the design guide)", "Expressive design (merch, campaigns, Nationals, big moments)", "Captions", "Print"],
     "Post recipes, expressive design, banners and print colors."),
    ("video", "Video & Reels", "references/video.md", None,
     "Animated mark loops, Reel safe areas and livestream graphics."),
]
# H2 sections deliberately shown on a different page than their markdown file
EXTRA_SECTIONS = {
    ("references/assets.md", "Social banners — assets/social/"): "social",
    ("references/assets.md", "Palette files — assets/palette/"): "colors",
}
RESERVED = {"assets", "templates", "tokens", "tools", "skills", "references", "site"}

MD_TO_PAGE = {
    "BRAND.md": "guidelines", "color-pairs.md": "colors", "messaging.md": "messaging", "email.md": "email",
    "web.md": "web", "slides.md": "slides", "docs.md": "docs", "sheets.md": "sheets", "social.md": "social",
    "video.md": "video", "assets.md": "logos",
}
DIR_TO_PAGE = {"assets/logos": "logos", "assets/icons": "icons", "assets/photos": "photos",
               "assets/animation": "video", "assets/social": "social", "references": "guidelines"}

GITHUB = "https://github.com/United-Club-Gymnastics/ucg-brand"
RAW = "https://united-club-gymnastics.github.io/ucg-brand"


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
    <p>United Club Gymnastics · <a href="https://unitedclubgymnastics.org">unitedclubgymnastics.org</a> · Fonts are licensed to UCG and not included; this site uses Saira Condensed and Arial.</p>
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
        for key in visuals:
            if key not in names and key not in ("_top", "_end"):
                raise SystemExit(f"{slug}: visual attached to missing section '{key}'; have {names}")
        parts = []
        if "_top" in visuals:
            parts.append(visuals["_top"](ctx))
        toc_items = []
        for n, h in chosen:
            src_md = next((emd for (emd, en) in EXTRA_SECTIONS if en == n), md)
            frag = rewrite_links(h, src_md)
            sid = slug_id(n) if n != "_intro" else "intro"
            if n != "_intro":
                frag = re.sub(r"<h2[^>]*>", f'<h2 id="{sid}">', frag, count=1)
                frag = re.sub(r"(<h2[^>]*>.*?) — <code>[^<]*</code>(</h2>)", r"", frag, count=1)  # drop file paths from page headings
                toc_items.append(f'<a href="#{sid}">{html.escape(re.sub(r" — .*$", "", re.sub(r"`", "", n)))}</a>')
            extra = visuals[n](ctx) if n in visuals else ""
            parts.append(f'<section class="doc-section" id="sec-{sid}">\n<div class="prose">{frag}</div>\n{extra}\n</section>')
        if "_end" in visuals:
            parts.append(visuals["_end"](ctx))
        toc = ('<nav class="toc" aria-label="On this page">' + "".join(toc_items) + "</nav>") if len(toc_items) > 1 else ""
        page = TEMPLATE.format(title=html.escape(title), blurb=html.escape(blurb), toc=toc, nav=nav_html(slug),
                               content="\n".join(parts), raw_url=f"{RAW}/{md}", md_path=md, github=GITHUB)
        out = ROOT / slug / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page, encoding="utf-8")
        built.append(slug)
    print("built", len(built), "pages:", ", ".join(built))


if __name__ == "__main__":
    build()
