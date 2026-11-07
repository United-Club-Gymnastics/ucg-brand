# United Club Gymnastics (UCG) brand guidelines

Short rules for anyone, person or AI agent, making UCG materials: emails, web pages and tools, slides, docs, sheets, social graphics and video. The rules come from the 2026 guides by Build Design Studio (cited as DG, EDG, MG with page numbers) plus a short list of [UCG decisions](#ucg-decisions). Sizes, spacing and layouts labeled as template defaults or suggestions are starting points, not rules. Details per medium live in `references/`; assets live in `assets/`.

- Repo: https://github.com/United-Club-Gymnastics/ucg-brand
- Assets base URL: `https://united-club-gymnastics.github.io/ucg-brand/assets/`
- Machine-readable facts: [`brand.json`](brand.json) · CSS tokens: [`tokens/ucg.css`](tokens/ucg.css)

## Who we are

United Club Gymnastics (UCG, formerly NAIGC) is a nonprofit, volunteer-run organization for adult club gymnastics (ages 18+), with collegiate and community clubs competing in WAG, MAG and Trampoline & Tumbling (T&T). Website: https://unitedclubgymnastics.org. Instagram: @unitedclubgymnastics. Write "UCG" or "United Club Gymnastics"; use "NAIGC" only when talking about history.

**Core message: For the Love of the Sport.** Healthy competition fueled by joy, passion and personal drive. As a sign-off or tagline it is written `For the Love of the Sport.` (with the period).

Supporting messages: **A Place to Land** (a long-term competitive home beyond traditional pathways) · **Open Gym** (anyone can belong and compete) · **On the Same Team** (camaraderie across clubs) · **Good Spot** (structure that keeps competition safe, fair and organized). See [`references/messaging.md`](references/messaging.md) for the approved headlines, one-liners and boilerplate.

## Voice

Welcoming, credible, joyful, practical (MG p29). Write like people who know the sport and care about the people in it.

- Speak to the reader ("you"); UCG is "we".
- Short, clear, conversational sentences. Lead with what matters, then make the next step obvious (join, compete, register, volunteer, connect).
- Encouraging even when sharing rules or deadlines.
- No jargon, buzzwords ("world-class", "innovative solutions"), stiff institutional language, or acronym soup (MG p38). Spelling out a term the first time helps newcomers.
- No emoji in official communications.
- Dates: `April 1–4, 2027` (en dash, no spaces); short form `Apr 1–4`; with a place, `April 1–4, 2027 · Portland, OR`. Times: `10:30 AM`, `7–9 PM ET`. Numbers: numerals for scores, dates and counts (`3 events`, `9.650`).
- Use real links. If you don't have the exact URL (registration, a course page), use https://unitedclubgymnastics.org and flag it for the person to fix; never invent a URL.

Examples:

- Instead of "We are a leading provider of innovative solutions that drive operational excellence.", write "We help gymnasts stay connected to the sport by bringing clubs and independent athletes together."
- Instead of "Registration for the aforementioned competition shall commence on 12/01.", write "Registration opens December 1. Here's how to sign up."
- Instead of "Athletes failing to submit paperwork will be disqualified.", write "Send your paperwork by Friday so you're cleared to compete."

## Color

| Role | Name | Hex |
|---|---|---|
| Primary | **Navy Blue** | `#1E2B38` |
| Primary | **Blue Green** | `#A5C8CF` |
| Primary | **Light Blue** | `#DBEBEE` |
| Secondary | Purple | `#ADBAE9` |
| Secondary | Red Orange | `#F4694A` |
| Secondary | Dark Blue Green | `#184B56` |
| Secondary | Golden Yellow | `#F6C328` |
| Neutral | White | `#FFFFFF` |

- Navy carries most text and dark surfaces. Light Blue, White and Blue Green are the main light surfaces. Secondary colors are accents: chips, highlights, calls to action (the guide's GIVE button is Red Orange, DG p76), data.
- UI roles use palette colors only, never extra grays: secondary text in Dark Blue Green (or Navy), dividers and card outlines in Blue Green, form-field borders in Dark Blue Green (they need 3:1), and dark surfaces in Navy with Dark Blue Green for cards and bands.
- No off-palette colors (EDG p4–6). Six extra "expressive" colors exist for merch, campaigns and event graphics, and only those six (see [`references/expressive.md`](references/expressive.md)).

### Color pairs: the guide's approved pairs, at WCAG AA

A text/background pair is allowed when it is approved in the design guide (DG p42–43) **and** meets WCAG AA at that size: **4.5:1** for body text, **3:1** for large text (24px+, or 18.66px+ bold), icons and logos. Where the guide is silent, AA decides.

**Safe at any size:**

- On **Navy**: White, Light Blue, Golden Yellow, Red Orange.
- On **Dark Blue Green**: White, Light Blue, Blue Green, Purple, Golden Yellow.
- On **White, Light Blue, Purple or Golden Yellow**: Navy or Dark Blue Green.
- On **Red Orange**: Navy.
- On **Blue Green**: Dark Blue Green.

**Large text, icons and logos only:** Blue Green or Purple on Navy (DG p42); Navy on Blue Green (DG p43); Red Orange on White or Dark Blue Green; White on Red Orange.

**Never:** Golden Yellow, Purple, Blue Green or Light Blue on White or Light Blue; Navy on Dark Blue Green (or the reverse); Dark Blue Green on Red Orange (DG p43); text on a busy part of a photo where it doesn't meet the ratio. Full table: [`references/color-pairs.md`](references/color-pairs.md).

## Type

| Use | Brand font | Fallback (Google / no license) | System fallback |
|---|---|---|---|
| Headlines, subheads, big numbers | **Greed Condensed Bold**, ALL CAPS | **Saira Condensed Bold** | Arial Narrow Bold |
| Body, buttons, captions | **Suisse Intl** Regular / Semibold | **Arial** | Arial |

- Headlines are ALL CAPS (DG p16, p32). The guide suggests around 36–60pt for print headlines, 10–24pt for subheads and 9–14pt for body copy (DG p34).
- Condensed subheads and labels use 20% tracking (`letter-spacing: 0.2em`, DG p34).
- Buttons and pills: Suisse Intl or Arial, ALL CAPS, 20% tracking (`letter-spacing: 0.2em`). Keep labels clear, short and legible (DG p76).
- Greed and Suisse are licensed to UCG. Only UCG volunteers making UCG materials may use them, and only UCG-owned websites may self-host them. Volunteers download them from the [UCG fonts folder](https://drive.google.com/drive/folders/1SUukrVratYo8sd4KxiF5_eztUnhAV-_o) (UCG Google accounts only). **Never copy or re-share the font files anywhere else.** If you don't have them, use Saira Condensed Bold + Arial.

| Surface | Fonts |
|---|---|
| Google Slides, Docs, Sheets | Saira Condensed Bold + Arial |
| Email | Saira Condensed (Google Fonts link) → Arial Narrow for headlines, Arial for body and buttons |
| UCG websites and tools | Greed + Suisse self-hosted on UCG's domain, falling back to Saira Condensed + Arial |
| Print, social graphics, Reels | Greed + Suisse (licensed volunteers), else Saira + Arial |
| Livestream / broadcast graphics | Saira Condensed + Arial (Greed's license doesn't cover broadcast video) |

## Logos

Use the supplied files. Color variations are permitted, but the structure and proportions of the logo never change (DG p26). **Never** stretch, redraw, retype the wordmark, add shadows or other effects, or place a logo where it doesn't meet 3:1 against its background. Expressive pieces like merch can also use the six expressive colors, add a stroke or crop the mark big in the background: [`references/expressive.md`](references/expressive.md).

**Colors:** the files come in four colorways: **navy** for light backgrounds, **light** (Light Blue) or **white** for Navy, Dark Blue Green and dark photos, and **black**, which suits one-color print. You can also recolor a logo in any palette color that is an approved pair for its background (DG p42): for example Golden Yellow, Red Orange, Purple or Blue Green on Navy, or Red Orange or Dark Blue Green on White. Seasonal and event recolors of the avatars are fine within the palette (DG p66).

| Logo | Typical use | Files (`assets/logos/`) |
|---|---|---|
| **Primary** (mark + UNITED CLUB GYMNASTICS) | The default | `ucg-primary-{navy,light,black,white}.{svg,png}` |
| **Secondary** (mark + UCG) | Horizontal spaces | `ucg-secondary-…` |
| **Logotype** (big UCG + full name) | Covers, signage, big moments | `ucg-logotype-…` |
| **Mark** (the burst) | Avatars, favicons, small spaces, watermarks | `ucg-mark-…` |
| Badges (circle, crest) | Merch, medals, stickers, social | `ucg-badge-circle-…`, `ucg-badge-crest-…` |
| Wordmarks | Footers, thin horizontal strips | `ucg-wordmark-full-name-…`, `ucg-wordmark-ucg-…` |

Recommended (UCG defaults; the guide doesn't set them): clear space around a logo of about the height of the "U" in UCG, and the primary logo at least 1 in wide in print or 120px on screen. Social avatars: `ucg-avatar-circle.png` / `ucg-avatar-square.png`. More: [`references/assets.md`](references/assets.md).

## Look and feel

The six design features (DG p15–21):

1. **Color fills**: solid brand-color blocks behind type.
2. **Strong type**: big ALL CAPS condensed headlines.
3. **Black-and-white photography** with white type and graphics.
4. **Dynamic crops** that show the angle and movement of the sport.
5. **Rounded corners** on cards, panels and photos, and pill-shaped buttons and chips (DG p76).
6. **Event icons** (MAG, WAG, T&T and apparatus) and **color overlays** on photos.

- Less is more: show only the critical information, with plenty of white space and a clear reading order (DG p89).
- Color overlays: a black-and-white photo over a solid brand color, photo blend mode Screen (DG p44; the guide's example uses Navy). Text on top still follows the color pairs; if it doesn't meet them, put it on a solid panel.
- Photos: real UCG athletes, documentary style, shown with dignity. The guide shows athletes and community/team photos in black and white (DG p17, p47). Don't use photos showing old NAIGC branding. Curated set with alt text: `assets/photos/photos.json`.
- Icons: the UCG event and apparatus icons in `assets/icons/`. For general UI icons (arrows, menus), a simple line set in brand colors works well.

## Before anything ships

1. Is it visually on-brand: right logo file, palette colors, fonts, alignment?
2. Does it sound like UCG: welcoming, credible, joyful, clear?
3. Does it show gymnasts, clubs and families with dignity, respect and belonging?
4. Is the next step clear?
5. Does every text/background pair meet the color pairs above, including hover states and dark mode wherever it applies (email clients always apply it; websites only if you support it)?

## UCG decisions

Made by UCG after the guides were delivered. Where they differ from the guides, they win.

- **For the Love of the Sport** is the core message (the guide lists A Place to Land as core).
- **Fallback fonts** are Saira Condensed Bold and Arial.
- **WCAG AA** on top of the guide's approved pairs, everywhere.
- **unitedclubgymnastics.org** is the web address (the guides say unitedgymnastics.org).
- **Palette-only UI**: no extra grays or navies.
- **Expressive colors** are exactly the six swatches, no in-between shades.
- **The mark** is the clean, constructed version in `assets/logos/`; any outline stays thinner than the gap between its V's.
- **House style:** no emoji in official communications; "UCG", with "NAIGC" only for history; the date and time formats above; numbered policies use one automatic decimal list ([`references/docs.md`](references/docs.md)).
- **Accessibility:** alt text on every image, captions on every video with speech, and color never the only signal (pair it with a word or icon).
- **Photos** in this kit are for UCG materials only, with no photographer credit needed.
- **Brand questions** go to your team lead or department head.

## By medium

- Email: [`references/email.md`](references/email.md) + [`templates/email/ucg-announcement-email.html`](templates/email/ucg-announcement-email.html)
- Websites and web tools: [`references/web.md`](references/web.md)
- Google Slides: [`references/slides.md`](references/slides.md)
- Google Docs and Forms (policies, letters, forms): [`references/docs.md`](references/docs.md)
- Google Sheets: [`references/sheets.md`](references/sheets.md)
- Social graphics and print: [`references/social.md`](references/social.md)
- Merch, campaigns, event graphics (expressive design): [`references/expressive.md`](references/expressive.md)
- Video and Reels: [`references/video.md`](references/video.md)
- Messaging and copy library: [`references/messaging.md`](references/messaging.md)
- Logos, icons, photos: [`references/assets.md`](references/assets.md)

*Based on the 2026 UCG Design, Messaging and Expressive Design guides by Build Design Studio, with the UCG decisions above.*
