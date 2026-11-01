# Websites and web tools

Applies to unitedclubgymnastics.org, UCG web apps (registration, scoring, planners, check-in) and any HTML page made for UCG.

## Setup

```html
<link href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@700&display=swap" rel="stylesheet">
<link href="https://united-club-gymnastics.github.io/ucg-brand/tokens/ucg.css" rel="stylesheet">
```

`tokens/ucg.css` defines every color, font stack, radius and spacing step as CSS variables (`--ucg-navy`, `--ucg-font-display`, `--ucg-radius-card` …) plus a few helper classes (`.ucg-display`, `.ucg-subhead`, `.ucg-eyebrow`, `.ucg-btn`). Copy it into your project if you prefer not to hotlink.

**Brand fonts on UCG-owned sites:** UCG's license allows self-hosting Greed Condensed and Suisse Intl as woff2 via `@font-face` on UCG's own domains only. Get the files from the UCG brand toolkit (not from this repo; they are never published). On any other site, the stacks fall back to Saira Condensed and Arial automatically.

## Layout

- Light page (`#FFFFFF` or `#DBEBEE`), Navy text. Full-bleed Navy for heroes, footers and feature bands.
- Alternate section backgrounds White → Light Blue → Blue Green → Navy so neighbors differ.
- Content max width about 1240px; 4px spacing grid (8, 12, 16, 24, 32, 48, 64). Generous white space; cut content before cramming.
- Left-align to a grid. Center only short content (a hero line, a single call to action).
- Rounded corners: 8px buttons, 12px inputs and small boxes, 20px cards and photos, pills (999px) for chips and tags.
- Black-and-white photography with white type; color overlays use a B&W photo on a brand color with `mix-blend-mode: screen`. Keep text on a solid or overlaid area that meets contrast.

## Type scale (starting point)

| Element | Font | Size | Notes |
|---|---|---|---|
| Display / hero | display stack | clamp(48px, 7vw, 96px) | ALL CAPS, line-height 0.92 |
| H1 | display | clamp(40px, 6vw, 80px) | ALL CAPS |
| H2 | display | clamp(32px, 4vw, 54px) | ALL CAPS |
| H3 and below | body stack, 600 | 20–24px | Sentence case |
| Subhead / label | display | 14–18px | ALL CAPS, letter-spacing 0.2em |
| Eyebrow | body, 700 | 12–13px | ALL CAPS, letter-spacing 0.16em, Dark Blue Green on light, Blue Green on dark |
| Body | body | 16px, line-height 1.55 | Navy or `#4A5A66` for secondary text |

## Components

- **Buttons** (DG p76): Suisse Intl / Arial, ALL CAPS, `letter-spacing: 0.2em`, short labels. Primary = Navy background + White text; on dark backgrounds = Blue Green background + Navy text. Text-only buttons are Navy (or White on dark). Add `→` for "go somewhere" actions.
- **Chips / tags**: pill shape, a secondary color fill with Navy text. Red Orange chips only for deadlines or urgent states.
- **Lists** (DG p77): thin 1px dividers between items (none above the first or below the last), about 15px between text and divider, 30px between a heading and the list. Bullets for unordered items; numbers only for sequences, rankings or counts.
- **Cards**: 20px radius, White on Light Blue pages (or Light Blue on White), optional 1px `#CFE1E4` border. Navy cards for the one thing you want noticed.
- **Forms**: 12px radius inputs, 1.5px `#BFD5D9` border, Navy text, visible focus ring in Dark Blue Green (3:1+ against the background). Labels above fields, sentence case.
- **Tables / data**: Navy header row with White text or Light Blue header with Navy text; zebra rows in White / Light Blue. Use the discipline colors consistently: WAG Purple, MAG Blue Green, T&T Golden Yellow, always with Navy text.
- **Icons**: UCG event and apparatus icons for discipline and apparatus (see [`assets.md`](assets.md)); a simple line icon set for UI controls, in Navy or the current text color.
- **Status colors**: Dark Blue Green for good / on track, Golden Yellow for attention, Red Orange for urgent or error. Always pair color with a word or icon.

## Dark mode

Optional. If you support it, use Navy `#1E2B38` / `#141E27` surfaces, White and Light Blue text, Blue Green accents and links, and recheck every pair. Swap logos to the `-light` or `-white` colorway.

## Accessibility checklist

- AA contrast for all text and UI (see [`color-pairs.md`](color-pairs.md)), including hover, focus, disabled and dark-mode states.
- Never Golden Yellow, Purple, Blue Green or Red Orange text on White or Light Blue.
- Meaningful `alt` text on photos (`assets/photos/photos.json` has some ready to use); `aria-label` on icon-only buttons.
- Logos: `<img src="…/ucg-primary-navy.svg" alt="United Club Gymnastics">`.
