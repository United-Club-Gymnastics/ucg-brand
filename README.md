# UCG brand kit

Brand guidelines and assets for **United Club Gymnastics** (UCG), written so both people and AI coding agents (Claude Code, Codex, Cursor and others) can follow them.

**Start here: [BRAND.md](BRAND.md).** For people, the same guides with visual examples live at **https://united-club-gymnastics.github.io/ucg-brand/**.

## Point your AI agent at it

Paste this into your prompt, or into your project's `CLAUDE.md` / `AGENTS.md`:

```
Follow the UCG brand guidelines: https://united-club-gymnastics.github.io/ucg-brand/BRAND.md
Read the linked references/ file for the medium you are working in before you start.
```

### Claude Code (installs as a skill that loads automatically for UCG work)

```
/plugin marketplace add United-Club-Gymnastics/ucg-brand
/plugin install ucg-brand@ucg
```

### Codex

Add the two lines above to your repo's `AGENTS.md`. (Codex can also load `skills/ucg-brand/SKILL.md` as a skill; on its own, outside this repo, it fetches the guidelines from the URL above.)

## What's here

| Path | What |
|---|---|
| [`BRAND.md`](BRAND.md) | The rules on a few pages: palette, contrast, type, logos, voice, checklist |
| [`references/`](references) | Detail per medium: email, web, Google Slides / Docs / Sheets, social, video, messaging, assets, color pairs |
| [`brand.json`](brand.json) | Machine-readable facts (colors with CMYK/Pantone, type specs, messaging, checklists) |
| [`tokens/ucg.css`](tokens/ucg.css) | CSS variables and helper classes |
| [`templates/email/`](templates/email) | UCG's HTML announcement email template |
| [`assets/logos/`](assets/logos) | All logo lockups in 4 colorways, SVG + PNG |
| [`assets/icons/`](assets/icons) | Event (MAG/WAG/T&T) and apparatus icons, SVG + PNG |
| [`assets/photos/`](assets/photos) | 37 curated 2026 Nationals photos, each in color and B&W, with alt text |
| [`assets/animation/`](assets/animation) | Animated mark loops (MP4) in square, vertical and wide |
| [`assets/social/`](assets/social) | Facebook cover, YouTube banner, Zoom backgrounds, email header |
| [`skills/ucg-brand/`](skills/ucg-brand) | Agent skill (Claude Code plugin / Codex) |
| [`tools/`](tools) | Scripts that build the assets, the color-pair table and the illustrated site |
| `site/`, `guidelines/`, `colors/`, … | The illustrated human site (generated) |

Assets are also served from `https://united-club-gymnastics.github.io/ucg-brand/assets/…` for hotlinking.

## Usage and licensing

These assets are for UCG and its member clubs, volunteers and partners making UCG-related materials. The UCG name, logos and marks are UCG's; don't use them to imply endorsement. Photos are of real UCG athletes: use them respectfully and only for UCG content.

**Fonts are not included.** Greed Condensed and Suisse Intl are licensed to UCG for its own volunteers and website. Everyone else uses the free fallbacks, Saira Condensed Bold (Google Fonts) and Arial.

## Maintaining

The design guides (PDF), source files and full photo sets live in UCG's internal brand toolkit. When something changes, update `brand.json` and the relevant `.md` first, then rerun the tools:

```
python tools/contrast.py                                   # regenerate references/color-pairs.md
python tools/copy_logos.py "<toolkit>/01_Assets/01_Logo"   # refresh logos
python tools/extract_icons.py "<toolkit>/01_Assets/All UCG Assets.svg"
python tools/icon_pngs.py
python tools/build_site.py                                 # rebuild the illustrated pages (<page>/index.html) from the .md files
python tools/test_site.py http://127.0.0.1:8123/ucg-brand/ # check contrast, overflow, links (serve the parent folder first:
                                                           #   python -m http.server 8123, run from the folder above this repo)
```

The illustrated pages are generated: edit the `.md` files (and `tools/site_visuals.py` for the visual examples), never the `<page>/index.html` files directly. Agents should always be pointed at the raw `.md` files.

Questions about the brand, or need a file that isn't here? Contact your team lead or department head.
