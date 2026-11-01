# Google Slides

Reference deck: **Nationals 2027 Awards Banquet** (UCG Drive). It is the best current example of the brand in Slides. Measurements below come from it.

## Setup

- **Size:** 16:9, 10 × 5.625 in (Google's default widescreen).
- **Fonts:** Saira Condensed Bold (700) for headlines, labels and numbers, always ALL CAPS. Arial for everything else. Both are built into Google Slides. Never leave Calibri or the theme default in a text box.
- **Palette:** set the theme colors to the brand palette (Slide → Edit theme → Colors): Dark 1 Navy `#1E2B38`, Light 1 White, Dark 2 Dark Blue Green `#184B56`, Light 2 Light Blue `#DBEBEE`, Accent 1 Blue Green `#A5C8CF`, Accent 2 Purple `#ADBAE9`, Accent 3 Golden Yellow `#F6C328`, Accent 4 Red Orange `#F4694A`, Hyperlink Dark Blue Green.
- **Images:** Slides can't insert SVG. Use the PNG versions of logos and icons from `assets/` (all have transparent backgrounds).

## Grid and type (from the banquet deck)

| Element | Font | Size | Color | Position |
|---|---|---|---|---|
| Margins | | | | 0.62 in left/right, title top at 0.5 in |
| Eyebrow above title | Arial Bold, ALL CAPS | 9.75–10.5pt | Dark Blue Green (light bg) / Blue Green (dark bg) | directly above the title |
| Slide title | Saira Condensed Bold | 34–39pt | Navy (light bg) / White (dark bg) | y 0.5 in |
| Intro line under title | Arial | 12pt | `#4A5A66` | ~0.5 in below title top |
| Cover / section title | Saira Condensed Bold | 60–84pt | White on Navy or photo | left-aligned, stacked lines |
| Card label | Saira Condensed Bold | 9–10pt | Dark Blue Green | top of card |
| Card heading | Arial Bold | 15–20pt | Navy, or White on Navy cards | |
| Body text in cards | Arial | 11–12pt | Navy / `#4A5A66`; Light Blue on Navy | |
| Big numbers | Saira Condensed Bold | 33pt+ | Navy on light, Blue Green on Navy | |
| Footer handles | Saira Condensed Bold | 10pt | Dark Blue Green (light) / Light Blue (dark) | bottom corners, y 5.3 in: `@unitedclubgymnastics` left, event hashtag right |

- **Cards:** rounded rectangles in Light Blue, Blue Green or Navy with ~0.25 in inner padding, 0.15–0.2 in gaps. Use one Navy card for the item you want noticed.
- **Chips:** small rounded rectangle in a secondary color with Saira caps label in Navy (e.g. Golden Yellow "GLUTEN FREE").
- **Dividers:** thin `#BFD5D9` lines between list rows; numbered rows use a Saira number then an Arial Bold label.
- **Tables:** Navy or Blue Green header row, alternating White / Light Blue rows, Arial 9–10pt body, Saira caps for column headers.

## Slide types

1. **Cover:** full-bleed B&W photo with a Navy overlay (or solid Navy), white mark top-left, eyebrow (org · event), huge Saira title, date and place in Arial 12pt, tagline `FOR THE LOVE OF THE SPORT.` small in Blue Green.
2. **Agenda / list:** two columns of numbered rows with dividers.
3. **Info cards:** title + 3–4 cards (one Navy, others Light Blue / Blue Green).
4. **Section break:** solid Navy, Blue Green, or Golden Yellow fill with a huge Saira headline; apparatus icons scattered around the edges are a good expressive touch.
5. **Big numbers / milestones:** row of cards with Saira numbers.
6. **Results tables:** Light Blue slide, title in a Navy band, white rounded rows.
7. **Sponsors:** grid of equal white rounded tiles, logos all the same visual weight.
8. **Closing:** solid color slide with the next step (register, party time, link) and the handles.

Leadership or working-meeting decks can be simpler: White slides, Saira title, Arial bullets 14–16pt, and a footer with the primary logo and `FOR THE LOVE OF THE SPORT.` on a thin Blue Green rule. Status cells use brand colors with a word ("On track" in Dark Blue Green text on Light Blue, "At risk" Navy on Golden Yellow, "Blocked" Navy on Red Orange). Don't use Google's default mint or green fills.

## Contrast traps seen in real decks

- Blue Green numbers or text on Light Blue or White backgrounds (about 1.4:1 and 1.8:1). Use Dark Blue Green or Navy instead; keep Blue Green for text on Navy.
- Grey `#74858F` footer text on Light Blue (3.1:1). Use `#4A5A66` or Dark Blue Green.
- Pale placeholder text such as `#9FB4BB` on white. Fine to delete before presenting, never for real content.
- White or Light Blue text on a photo without a Navy overlay behind it.

## Building decks with the API (for agents)

Use a UCG Google Workspace account, not a personal one, so files land in UCG's Drive. Easiest path: duplicate the banquet deck (Drive `files.copy`), delete the slides you don't need, and replace text, so geometry and styles stay right. When creating shapes, set `fontFamily` to `Saira Condensed` with `weightedFontFamily.weight: 700` for headlines and `Arial` for body, and pass colors as RGB from the palette.
