# Google Slides

**Start every new deck from the [UCG Slides template](https://docs.google.com/presentation/d/1aJHuTtVjkRVPzteyeOgZdMWxWDLeAFNSvdaMtY3whks/copy)** (in the Google Slides **Template gallery** under United Club Gymnastics, or the link opens your own copy; UCG Google accounts only). It already has the theme colors, fonts, footers and an example of every slide type below: delete the slides you don't need and duplicate the ones you do.

If you need to go well beyond the template or make a new kind of slide, use the guidance below. The fonts, palette and color pairs are rules; the sizes and layouts are what the template uses, so treat them as starting points.

## Setup

- **Size:** 16:9, 10 × 5.625 in (Google's default widescreen).
- **Fonts:** Saira Condensed Bold (700) for headlines, labels and numbers, always ALL CAPS. Arial for everything else. Both are built into Google Slides. Never leave Calibri or the theme default in a text box.
- **Palette:** set the theme colors to the brand palette (Slide → Edit theme → Colors): Dark 1 Navy `#1E2B38`, Light 1 White, Dark 2 Dark Blue Green `#184B56`, Light 2 Light Blue `#DBEBEE`, Accent 1 Blue Green `#A5C8CF`, Accent 2 Purple `#ADBAE9`, Accent 3 Golden Yellow `#F6C328`, Accent 4 Red Orange `#F4694A`, Hyperlink Dark Blue Green.
- **Images:** Slides can't insert SVG. Use the PNG versions of logos and icons from `assets/` (all have transparent backgrounds).

## Grid and type

What the template uses:

| Element | Font | Size | Color | Position |
|---|---|---|---|---|
| Margins | | | | 0.62 in left/right, title top at 0.5 in |
| Eyebrow above title | Arial Bold, ALL CAPS | 9.75–10.5pt | Dark Blue Green (light bg) / Light Blue (dark bg) | directly above the title |
| Slide title | Saira Condensed Bold | 34–39pt | Navy (light bg) / White (dark bg) | y 0.5 in |
| Intro line under title | Arial | 12pt | Dark Blue Green `#184B56` | ~0.5 in below title top |
| Cover / section title | Saira Condensed Bold | 60–84pt | White on Navy or photo | left-aligned, stacked lines |
| Card label | Saira Condensed Bold | 9–10pt | Dark Blue Green | top of card |
| Card heading | Arial Bold | 15–20pt | Navy, or White on Navy cards | |
| Body text in cards | Arial | 11–12pt | Navy; Light Blue on Navy; Dark Blue Green on Blue Green | |
| Big numbers | Saira Condensed Bold | 33pt+ | Navy on light, Blue Green or Golden Yellow on Navy | |
| Footer handles | Saira Condensed Bold | 10pt | Dark Blue Green (light) / Light Blue (dark) | bottom corners, y 5.3 in: `@unitedclubgymnastics` left, event hashtag right |

The design guide suggests around 36–60pt for headlines (DG p34), so the template's titles sit at the small end of that range.

- **Cards:** rounded rectangles in Light Blue, Blue Green or Navy with ~0.25 in inner padding, 0.15–0.2 in gaps. A Navy card stands out from light ones. Small text on a Blue Green card is Dark Blue Green; Navy on Blue Green is for large text only (DG p43).
- **Chips:** small rounded rectangle in Purple, Golden Yellow or Red Orange with a Saira caps label in Navy (e.g. Golden Yellow "GLUTEN FREE").
- **Dividers:** thin Blue Green `#A5C8CF` lines between list rows; numbered rows use a Saira number then an Arial Bold label.
- **Tables:** Navy header row with White text, or Light Blue with Navy text; alternating White / Light Blue rows; Arial 9–10pt body, Saira caps for column headers.

## Slide types

1. **Cover:** full-bleed B&W photo with a Navy overlay (or solid Navy), white mark top-left, eyebrow (org · event), huge Saira title, date and place in Arial 12pt, tagline `FOR THE LOVE OF THE SPORT.` small in Light Blue.
2. **Agenda / list:** two columns of numbered rows with dividers.
3. **Info cards:** title + 3–4 cards (one Navy, others Light Blue / Blue Green).
4. **Section break:** solid Navy, Blue Green, or Golden Yellow fill with a huge Saira headline; apparatus icons scattered around the edges are a good expressive touch.
5. **Big numbers / milestones:** row of cards with Saira numbers.
6. **Results tables:** Light Blue slide, title in a Navy band, white rounded rows.
7. **Sponsors:** grid of equal white rounded tiles, logos all the same visual weight.
8. **Closing:** solid color slide with the next step (register, party time, link) and the handles.

Leadership or working-meeting decks can be simpler: White slides, Saira title, Arial bullets 14–16pt, and a footer with the primary logo and `FOR THE LOVE OF THE SPORT.` on a thin Blue Green rule. Status cells can use brand colors with a word ("On track" in Dark Blue Green text on Light Blue, "At risk" Navy on Golden Yellow, "Blocked" Navy on Red Orange) instead of Google's default mint or green fills.

## Contrast traps seen in real decks

- Blue Green numbers or text on Light Blue or White backgrounds (about 1.4:1 and 1.8:1). Use Dark Blue Green or Navy instead; keep Blue Green for large text on Navy.
- Small Navy text on Blue Green cards (fine for big numbers and headings, but the guide doesn't approve it at small sizes). Use Dark Blue Green.
- Gray `#74858F` footer text on Light Blue (3.1:1). Use Dark Blue Green or Navy.
- Pale placeholder text such as `#9FB4BB` on white. Fine to delete before presenting, never for real content.
- White or Light Blue text over a light or busy part of a photo. Place it where the photo is dark enough, or add a Navy overlay or band behind it.

## Building decks with the API (for agents)

Use a UCG Google Workspace account, not a personal one, so files land in UCG's Drive. Easiest path: copy the UCG Slides template (Drive `files.copy` on `1aJHuTtVjkRVPzteyeOgZdMWxWDLeAFNSvdaMtY3whks`), delete the slides you don't need, and replace text, so geometry and styles stay right. When creating shapes, set `fontFamily` to `Saira Condensed` with `weightedFontFamily.weight: 700` for headlines and `Arial` for body, and pass colors as RGB from the palette.
