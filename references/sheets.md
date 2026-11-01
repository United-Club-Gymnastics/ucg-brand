# Google Sheets

Sheets are working tools first. Brand them lightly so they look like UCG and stay easy to read.

**Start from the [UCG Sheets template](https://docs.google.com/spreadsheets/d/138BylbdttmkkCohApng-HlhUDbECz8rtueqv_Tp30x0/copy)** (the link makes your own copy; UCG Google accounts only). It has the UCG theme (Arial, brand colors), a frozen Navy header row, banded rows, Status and Discipline dropdowns that color themselves, a totals row and an example chart. Google doesn't let an organization change what a new *blank* sheet looks like, so copying the template is the way to get these defaults.

The details below are for building or fixing a sheet by hand (agents: copy the template with Drive `files.copy` on `138BylbdttmkkCohApng-HlhUDbECz8rtueqv_Tp30x0`).

## Defaults

- Font: **Arial 10pt** for data (Sheets' default theme font may be something else; set it in Format → Theme → Font to Arial). Saira Condensed Bold for a title row only.
- Theme colors (Format → Theme → Customize): Text Navy `#1E2B38`, Background White, Accent 1 Blue Green `#A5C8CF`, Accent 2 Purple `#ADBAE9`, Accent 3 Golden Yellow `#F6C328`, Accent 4 Red Orange `#F4694A`, Accent 5 Dark Blue Green `#184B56`, Accent 6 Light Blue `#DBEBEE`, Links Dark Blue Green.

## Layout

| Row / area | Style |
|---|---|
| Title row (optional, row 1) | Saira Condensed Bold 18pt, ALL CAPS, Navy text, no fill; merged across the table width |
| Header row | Navy `#1E2B38` fill, White Arial Bold 10pt, frozen, wrap text, vertical-align middle |
| Data rows | Alternating White / Light Blue `#DBEBEE` (Format → Alternating colors → custom), Navy text |
| Borders | `#BFD5D9` thin, horizontal only, or none |
| Totals row | Arial Bold, Light Blue or Blue Green fill, Navy text |

- Freeze the header row and any identifier column.
- Right-align numbers, left-align text, consistent decimals (scores to 3 decimals, money to 2).
- Use dates as real dates, formatted `Apr 8, 2027` or ISO `2027-04-08` consistently.

## Status and conditional formatting

Use fills with Navy text, never colored text on white:

| Meaning | Fill | Text |
|---|---|---|
| Good / done / on track | Light Blue `#DBEBEE` or Blue Green `#A5C8CF` | Dark Blue Green or Navy |
| Attention / pending | Golden Yellow `#F6C328` | Navy |
| Urgent / error / blocked | Red Orange `#F4694A` | Navy |
| Neutral / info | Purple `#ADBAE9` | Navy |

Discipline tags, if color-coded: WAG Purple, MAG Blue Green, T&T Golden Yellow (Navy text on all three).

## Charts

Chart marks need 3:1 against the background. On a white chart, series colors in this order: Navy, Red Orange, Dark Blue Green. Purple, Golden Yellow and Blue Green are too pale on white (under 2:1), so only use them for bars with a Navy outline or on a Navy chart background (where Blue Green, Golden Yellow, Purple, Red Orange and White all pass). Light Blue only for backgrounds or gridlines. Arial for all chart text; no 3D, no gradients; label directly instead of a legend when there are few series.
