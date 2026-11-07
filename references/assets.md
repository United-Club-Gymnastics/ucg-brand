# Logos, icons, photos and other assets

Every file below is served at `https://united-club-gymnastics.github.io/ucg-brand/assets/<path>`, e.g. `https://united-club-gymnastics.github.io/ucg-brand/assets/logos/ucg-primary-navy.svg`. You can also download the whole repo. Use SVG on the web, PNG in Google apps (Slides, Docs and Sheets can't insert SVG), and the toolkit's AI/EPS/PDF masters for professional print.

## Logos — `assets/logos/`

Pattern: `ucg-<logo>-<colorway>.<svg|png>` (PNGs are 2400px wide, transparent).

| `<logo>` | What it is |
|---|---|
| `primary` | Mark + "UNITED CLUB GYMNASTICS" on two lines. The default. |
| `secondary` | Mark + "UCG". Compact horizontal. |
| `logotype` | Big "UCG" letters with "UNITED CLUB GYMNASTICS" underneath. |
| `wordmark-full-name` | "UNITED CLUB GYMNASTICS" on one line, no mark. Footers, thin strips. |
| `wordmark-ucg` | The "UCG" letters alone. |
| `mark` | The burst symbol alone (a gymnast in a starburst). Avatars, favicons, small spaces. |
| `badge-circle` | Mark inside a ring reading "UNITED CLUB GYMNASTICS · FOR THE LOVE OF THE SPORT". Merch, medals, stickers. |
| `badge-crest` | "UCG" and the gymnast figure in a shield. Merch, apparel. |

| `<colorway>` | Color | Use on |
|---|---|---|
| `navy` | Navy `#1E2B38` | White, Light Blue, Blue Green, Purple, Golden Yellow, Red Orange backgrounds |
| `light` | Light Blue `#DBEBEE` | Navy, Dark Blue Green, dark photos |
| `white` | White | Navy, Dark Blue Green, dark photos and overlays |
| `black` | Black | One-color print |

Badges are two-tone: `badge-circle-navy` and `badge-crest-navy` are Navy art on a Light Blue disc/shield; `-light` is Light Blue art on Navy; `-white` is White on black; `-black` is black on White.

Also in `assets/logos/`: `ucg-avatar-circle` / `ucg-avatar-square` (social profile images, White mark on Dark Blue Green), `ucg-favicon.png`, `ucg-mark-in-circle-*`, `ucg-document-header` (Navy header band for documents).

**How the mark is built** (every file uses this exact geometry, from `tools/mark_geometry.py`): six identical V's at exactly 60° steps around a round dot. Each V is two straight legs at 22.5° either side of its axis; the rounded base is a circle centered on the V's inner point with radius equal to the leg width; each leg ends square to the leg with a slight outward arc. Each V has 8 nodes. If you need the mark as a shape (for a stroke, a cut file, an embroidery file), start from these files, not a trace.

**Rules:** color variations are allowed, but the structure and proportions never change (DG p26). Don't stretch, redraw, add shadows or other effects, or rebuild the wordmark in a font. Other colors: recolor the SVG in a palette color that is an approved pair for its background (DG p42; see [`color-pairs.md`](color-pairs.md)), for example Golden Yellow, Red Orange, Purple, Blue Green or Light Blue on Navy. Off-palette colors, strokes and the expressive colors: see [`expressive.md`](expressive.md). The mark can be cropped by the edge of a layout, as on the guide's lanyard (DG p86).

**Recommended** (UCG defaults; the design guide doesn't set clear space or minimum sizes): clear space of about the height of the "U" in UCG; primary logo at least 1 in wide in print or 120px on screen; mark at least 0.25 in or 24px.

## Icons — `assets/icons/`

UCG's own pictograms (simple, bold gymnast figures with a ball-shaped head). Every icon comes in `-navy`, `-light` and `-white` SVG + PNG versions. Index with labels: `assets/icons/icons.json`.

**Event icons** (`event/`): one figure per discipline, used to label MAG, WAG and T&T content.

| File stem | Meaning |
|---|---|
| `mag`, `mag-1`, `mag-2`, `mag-3` | Men's artistic gymnastics (primary + alternates) |
| `wag`, `wag-1`, `wag-grad` | Women's artistic gymnastics (primary + alternates; `wag-grad` wears a grad cap) |
| `tnt`, `tnt-2` | Trampoline & tumbling (primary + alternate) |
| `club-spirit` | A cheering crowd, for spirit awards and community. The one-color versions are line art: each figure is outlined so the crowd doesn't merge into a blob. `club-spirit-original` is the two-tone version (Light Blue figures with Navy outlines). |

**Apparatus icons** (`apparatus-solid/`), named `<discipline>-<apparatus>`:

- MAG: `mag-floor`, `mag-pommel-horse`, `mag-rings`, `mag-vault`, `mag-parallel-bars`, `mag-high-bar`
- WAG: `wag-vault`, `wag-uneven-bars`, `wag-balance-beam`, `wag-floor`
- T&T: `tnt-trampoline`, `tnt-double-mini`, `tnt-power-tumbling`, `tnt-synchro`

Icons are graphics, so each needs 3:1 against its background and an approved pair (Navy on light colors, White or Light Blue on dark ones; DG p20 mixes both in one layout). They work best at a consistent size in a layout.

## Photos — `assets/photos/`

163 photos from 2026 UCG Nationals by photographer Bryan Johnson, each in a color and a black-and-white edit (326 files), 2000px on the long edge, metadata stripped. `photos.json` lists each file with ready-to-use alt text, its tone, and its type:

- `athlete`: a single athlete, often B&W, for heroes and quotes
- `movement`: skills in motion, dynamic crops
- `community`: teams, coaches, judges, volunteers, fans

File names: `ucg-<color|bw>-<what's in it>.jpg`. The design guide uses black-and-white photos with white type and graphics, for athletes and for community and team shots alike (DG p17, p47); the color edits are there when a piece needs color. Use them for UCG materials only, and crop rather than distort. The full Nationals sets live in the [UCG brand toolkit](https://drive.google.com/drive/folders/1M7wFuZvl7AUGmU7Rzh3bu_vErSauU2ZZ) (UCG volunteers only).

## Social banners — `assets/social/`

Facebook cover, YouTube banner, Zoom backgrounds and the email header logo (`ucg-email-header.png`, navy background baked in so it survives dark mode). Their editable sources are the "05 Social & Digital" artboards in the toolkit's `All UCG Assets.svg` (live text in Greed and Suisse; each artboard remembers its export file name and size). The mirrored Zoom background is a clone of the regular one, so edit that one.

## Patterns — `assets/patterns/`

`ucg-event-pattern-2026-27.svg` / `.png`: the 2026–27 Nationals event pattern from the design guide (p54). See [`expressive.md`](expressive.md).

## Palette files — `assets/palette/`

`UCG_Colors.ase` (Adobe swatches), `UCG_Colors.pdf`, `ucg-color-wheel.png`. Values in `brand.json` and `tokens/ucg.css`.

## Not in this repo

- **Fonts.** Greed Condensed and Suisse Intl are licensed to UCG and are never published here. UCG volunteers can download them from the [UCG fonts folder](https://drive.google.com/drive/folders/1SUukrVratYo8sd4KxiF5_eztUnhAV-_o) (UCG Google accounts only). Everyone else uses Saira Condensed Bold + Arial.
- **Masters and source files** (AI, EPS, the Figma templates, full-resolution photos, alpha-channel animations): in UCG's internal brand toolkit. Ask your team lead or department head.
