# United Club Gymnastics (UCG) brand guidelines

Short rules for anyone, person or AI agent, making UCG materials: emails, web pages and tools, slides, docs, sheets, social graphics and video. Follow them exactly. Details per medium live in `references/`; assets live in `assets/`.

- Repo: https://github.com/United-Club-Gymnastics/ucg-brand
- Assets base URL: `https://united-club-gymnastics.github.io/ucg-brand/assets/`
- Machine-readable facts: [`brand.json`](brand.json) · CSS tokens: [`tokens/ucg.css`](tokens/ucg.css)

## Who we are

United Club Gymnastics (UCG, formerly NAIGC) is a nonprofit, volunteer-run organization for adult club gymnastics (ages 18+), with collegiate and community clubs competing in WAG, MAG and Trampoline & Tumbling (T&T). Website: https://unitedclubgymnastics.org. Instagram: @unitedclubgymnastics. Write "UCG" or "United Club Gymnastics"; use "NAIGC" only when talking about history.

**Core message: For the Love of the Sport.** Healthy competition fueled by joy, passion and personal drive. As a sign-off or tagline it is written `For the Love of the Sport.` (with the period).

Supporting messages: **A Place to Land** (a long-term competitive home beyond traditional pathways) · **Open Gym** (anyone can belong and compete) · **On the Same Team** (camaraderie across clubs) · **Good Spot** (structure that keeps competition safe, fair and organized). See [`references/messaging.md`](references/messaging.md) for approved headlines, one-liners and boilerplate.

## Voice

Welcoming, credible, joyful, practical. Write like people who know the sport and care about the people in it.

- Speak to the reader ("you"); UCG is "we".
- Short, clear, conversational sentences. Lead with what matters, then make the next step obvious (join, compete, register, volunteer, connect).
- Encouraging even when sharing rules or deadlines.
- No jargon, buzzwords ("world-class", "innovative solutions"), stiff institutional language, or acronym soup. Spell out a term the first time if a newcomer wouldn't know it.
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

- Navy carries most text and dark surfaces. Light Blue, White and Blue Green are the main light surfaces. Secondary colors are accents: chips, highlights, data, one bold slide.
- UI roles use palette colors only, never extra greys: secondary text in Dark Blue Green (or Navy), dividers and card outlines in Blue Green, form-field borders in Dark Blue Green (they need 3:1), and dark surfaces in Navy with Dark Blue Green for cards and bands.
- No gradients, no off-palette colors. Six extra "expressive" colors exist only for merch, campaigns and event graphics, and only those six (see [`references/expressive.md`](references/expressive.md)).

### Contrast is a hard rule (WCAG AA everywhere)

Body text needs **4.5:1**, large text (24px+, or 18.5px+ bold), icons and logos need **3:1**.

**Safe text pairs:**

- Text on **Navy** or **Dark Blue Green** backgrounds: White, Light Blue, Blue Green, Golden Yellow or Purple. Red Orange works on Navy only.
- Text on **White, Light Blue, Blue Green, Purple or Golden Yellow** backgrounds: Navy or Dark Blue Green.
- Text on **Red Orange** backgrounds: Navy only.

**Never:** Golden Yellow, Purple, Blue Green or Light Blue text on White or Light Blue; Red Orange text on White (3.0:1) or Light Blue (2.5:1); Navy on Dark Blue Green; anything on a busy photo without a solid or overlay behind it. Full table: [`references/color-pairs.md`](references/color-pairs.md).

## Type

| Use | Brand font | Fallback (Google / no license) | System fallback |
|---|---|---|---|
| Headlines, subheads, big numbers | **Greed Condensed Bold**, ALL CAPS | **Saira Condensed Bold** | Arial Narrow Bold |
| Body, buttons, captions | **Suisse Intl** Regular / Semibold | **Arial** | Arial |

- Headlines are ALL CAPS, short and tight (line-height ~0.92, tracking ~0). Condensed subheads and labels use 20% tracking (`letter-spacing: 0.2em`).
- Body copy is sentence case. Avoid Title Case for anything but proper names.
- Buttons: Suisse Intl or Arial, ALL CAPS, `letter-spacing: 0.2em`, short verb labels ("Register", "Join the club").
- Greed and Suisse are licensed to UCG. Only UCG volunteers making UCG materials may use them, and only UCG-owned websites may self-host them. Volunteers download them from the [UCG fonts folder](https://drive.google.com/drive/folders/1SUukrVratYo8sd4KxiF5_eztUnhAV-_o) (UCG Google accounts only). **Never copy or re-share the font files anywhere else.** If you don't have them, use Saira Condensed Bold + Arial.

| Surface | Fonts |
|---|---|
| Google Slides, Docs, Sheets | Saira Condensed Bold + Arial |
| Email | Saira Condensed (Google Fonts link) → Arial Narrow for headlines, Arial for body |
| UCG websites and tools | Greed + Suisse self-hosted on UCG's domain, falling back to Saira Condensed + Arial |
| Print, social graphics, Reels | Greed + Suisse (licensed volunteers), else Saira + Arial |
| Livestream / broadcast graphics | Saira Condensed + Arial (Greed's license doesn't cover broadcast video) |

## Logos

Use the files exactly as drawn. Recolor only to the four supplied colorways. **Never** stretch, rotate, redraw, outline, add effects, retype the wordmark, or place on a low-contrast background. (Expressive pieces like merch may also recolor within the palette, add a stroke or crop the mark big in the background, but never redraw it: [`references/expressive.md`](references/expressive.md).)

| Logo | Use it for | Files (`assets/logos/`) |
|---|---|---|
| **Primary** (mark + UNITED CLUB GYMNASTICS) | Default, headers, documents | `ucg-primary-{navy,light,black,white}.{svg,png}` |
| **Secondary** (mark + UCG) | Compact horizontal spaces | `ucg-secondary-…` |
| **Logotype** (big UCG + full name) | Covers, signage, big moments | `ucg-logotype-…` |
| **Mark** (the burst) | Avatars, favicons, small spaces, watermarks | `ucg-mark-…` |
| Badges (circle, crest) | Merch, medals, stickers, social | `ucg-badge-circle-…`, `ucg-badge-crest-…` |
| Wordmarks | Footers, tight horizontal strips | `ucg-wordmark-full-name-…`, `ucg-wordmark-ucg-…` |

Colorways: **navy** on light backgrounds, **light** (Light Blue) or **white** on navy, dark blue green or dark photos, **black** only for one-color print. Leave clear space around a logo at least the height of the "U" in UCG, and don't shrink the primary logo below 120px (1 in) wide. Social avatars: `ucg-avatar-circle.png` / `ucg-avatar-square.png`. More: [`references/assets.md`](references/assets.md).

## Look and feel

The six design features:

1. **Color fills**: solid brand-color blocks behind type.
2. **Strong type**: big ALL CAPS condensed headlines.
3. **Black-and-white photography** with white type and graphics.
4. **Dynamic crops** that show the angle and movement of the sport.
5. **Rounded corners** on cards, panels and photos (8px buttons, 12px small boxes, 20px cards, pills for chips).
6. **Event icons** (MAG, WAG, T&T and apparatus) and **color overlays** on photos.

- Less is more: show only the critical information, with plenty of white space and a clear reading order.
- Left-align to a grid. Center only short content.
- Alternate section backgrounds (White → Light Blue → Blue Green → Navy) so neighbors differ.
- Color overlays: a black-and-white photo with a solid brand color behind it, photo blend mode Screen (guide recipe). Screen makes the image lighter, so use it with light colors (Blue Green, Light Blue, Purple, Golden Yellow) and put **Navy** text on it. For White text over a photo, darken instead: a Navy or Dark Blue Green duotone (or Multiply) dark enough that White stays at 4.5:1, or put the text on a solid Navy panel beside the photo.
- Photos: real UCG athletes, documentary style, shown with dignity. Never use photos showing old NAIGC branding. Curated set with alt text: `assets/photos/photos.json`.
- Icons: the UCG event and apparatus icons in `assets/icons/`. For general UI icons (arrows, menus) use a simple line set at a consistent stroke and keep them in brand colors. Use `→` for links and buttons.

## Before anything ships

1. Is it visually on-brand: right logo file, palette colors, fonts, alignment?
2. Does it sound like UCG: welcoming, credible, joyful, clear?
3. Does it show gymnasts, clubs and families with dignity, respect and belonging?
4. Is the next step clear?
5. Does every text/background pair meet AA contrast, including hover states and dark mode wherever it applies (email clients always apply it; websites only if you support it)?

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

*Based on the 2026 UCG Design, Messaging and Expressive Design guides by Build Design Studio, with later UCG decisions: For the Love of the Sport is the core message; Saira Condensed and Arial are the fallbacks; AA contrast everywhere.*
