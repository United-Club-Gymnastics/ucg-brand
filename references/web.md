# Websites and web tools

Applies to unitedclubgymnastics.org, UCG web apps (registration, scoring, planners, check-in) and any HTML page made for UCG.

## Setup

```html
<link href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@700&display=swap" rel="stylesheet">
<link href="https://united-club-gymnastics.github.io/ucg-brand/tokens/ucg.css" rel="stylesheet">
```

`tokens/ucg.css` defines every color, font stack, radius and spacing step as CSS variables (`--ucg-navy`, `--ucg-font-display`, `--ucg-radius-card` …) plus a few helper classes (`.ucg-display`, `.ucg-subhead`, `.ucg-eyebrow`, `.ucg-btn`). Copy it into your project if you prefer not to hotlink.

**Brand fonts on UCG-owned sites:** UCG's license allows self-hosting Greed Condensed and Suisse Intl as woff2 via `@font-face` on UCG's own domains only. UCG volunteers get the files from the [UCG fonts folder](https://drive.google.com/drive/folders/1SUukrVratYo8sd4KxiF5_eztUnhAV-_o) (not from this repo; they are never published). On any other site, the stacks fall back to Saira Condensed and Arial automatically.

## Layout

Suggestions and the defaults in `tokens/ucg.css`; the design guide sets the look, not these numbers.

- Light page (`#FFFFFF` or `#DBEBEE`), Navy text. Full-bleed Navy for heroes, footers and feature bands.
- Neighboring sections read best with different backgrounds (White, Light Blue, Blue Green, Navy).
- Content max width about 1240px; spacing in steps of 4px (8, 12, 16, 24, 32, 48, 64). Generous white space; cut content before cramming (DG p89).
- Left-align to a grid. Center only short content (a hero line, a single call to action).
- Rounded corners on cards, panels and photos (DG p19); pills for buttons, chips and tags (DG p76). Defaults: 12px inputs and small boxes, 20px cards and photos, 999px pills.
- Black-and-white photography with white type (DG p17). Color overlays: a B&W photo on a brand color with `mix-blend-mode: screen` (DG p44). Keep text on a solid or overlaid area that meets the color pairs.

## Type scale (starting point)

| Element | Font | Size | Notes |
|---|---|---|---|
| Display / hero | display stack | clamp(48px, 7vw, 96px) | ALL CAPS, line-height about 0.92 |
| H1 | display | clamp(40px, 6vw, 80px) | ALL CAPS |
| H2 | display | clamp(32px, 4vw, 54px) | ALL CAPS |
| H3 and below | body stack, 600 | 20–24px | |
| Subhead / label | display | 14–18px | ALL CAPS, letter-spacing 0.2em (DG p34) |
| Eyebrow | body, 700 | 12–13px | ALL CAPS, letter-spacing 0.2em, Dark Blue Green on light, Light Blue on dark |
| Body | body | 16px, line-height 1.55 | Navy; Dark Blue Green for secondary text |

## Components

- **Buttons** (DG p76): pills in Suisse Intl / Arial, ALL CAPS, `letter-spacing: 0.2em`, clear short labels. The guide's examples: Navy with White text, Red Orange for a call to action like GIVE (use Navy text on it: White on Red Orange is only 3:1), and Light Blue with Navy text. On dark backgrounds use Light Blue with Navy text. Text-only buttons are Navy or a secondary color, or White on a dark background or image. `→` works well for "go somewhere" actions.
- **Chips / tags**: pills with a secondary color or Light Blue fill and Navy text. Not Blue Green with Navy text at chip sizes (DG p43).
- **Lists** (DG p77): thin 0.5pt dividers between items (none above the first or below the last), 15pt between text and divider, 30pt between a heading above the list and the first item. Bullets for options and grouped ideas; numbers only for sequences, rankings or counts.
- **Cards**: rounded, White on Light Blue pages (or Light Blue on White), optionally outlined in Blue Green `#A5C8CF`. A Navy card stands out from light ones.
- **Forms**: 1.5px Dark Blue Green `#184B56` border (form fields need 3:1), Navy text, visible focus ring in Dark Blue Green. Labels above fields.
- **Tables / data**: Navy header row with White text or Light Blue header with Navy text; zebra rows in White / Light Blue.
- **Icons**: UCG event and apparatus icons for discipline and apparatus (see [`assets.md`](assets.md)); a simple line icon set for UI controls, in Navy or the current text color.
- **Status colors** (a suggestion): Dark Blue Green for good / on track, Golden Yellow for attention, Red Orange for urgent or error. Always pair color with a word or icon.

## Dark mode

Optional. If you support it, use Navy `#1E2B38` surfaces with Dark Blue Green `#184B56` for cards and bands, White and Light Blue text, Golden Yellow or Light Blue links, and Blue Green only for large type, rules and icons on Navy (DG p42). Recheck every pair. Swap logos to the `-light` or `-white` colorway.

## Accessibility checklist

- Every text and UI pair follows [`color-pairs.md`](color-pairs.md) (the guide's approved pairs, at WCAG AA), including hover, focus, disabled and dark-mode states.
- Never small Golden Yellow, Purple, Blue Green, Light Blue or Red Orange text on White or Light Blue; Red Orange on White only for large text.
- Meaningful `alt` text on photos (`assets/photos/photos.json` has some ready to use); `aria-label` on icon-only buttons.
- Logos: `<img src="…/ucg-primary-navy.svg" alt="United Club Gymnastics">`.
