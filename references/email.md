# Email

## Announcement / newsletter emails (HTML)

Start from [`templates/email/ucg-announcement-email.html`](../templates/email/ucg-announcement-email.html). It is UCG's working monthly-announcements template (sent through iContact) and its comments explain how to use it. In short:

- Parts marked **FIXED** never change: header logo, base styles, dark-mode rules, sign-off and social links.
- **Dark text on light backgrounds** (UCG decision, 2026-11-10): readers found light text on dark sections harder to read. Sections and cards are White, Light Blue or Blue Green; Navy is for text and buttons only. The header is a White strip with the Navy logo, and the sign-off sits on Blue Green.
- Build the body from the **BLOCKS** between `BODY START` and `BODY END`: hero, feature band, section label, standard item, light card, action card, two buttons, discipline section, feature article. Copy a block, replace every `[PLACEHOLDER]`, delete what you don't need.
- Keep the sender's wording. Fix only obvious typos.
- Neighboring sections usually get different backgrounds (white, light blue, blue green), so the email reads as separate blocks. A feature article on White after another White section gets its Blue Green top rule as the divider.
- Small text follows the color pairs ([`color-pairs.md`](color-pairs.md)): on Blue Green it's Dark Blue Green, not Navy (DG p42–43).
- Chips: a Red Orange, Golden Yellow or Purple fill with Navy text.
- Every link is https. Buttons for main actions, text links (`Link text →`) for secondary ones.
- Images: only the fixed logo unless an image hosted by the email platform is supplied. The logo is `assets/social/ucg-email-header-light.png` (Navy logo with White baked in, shown 360px wide); the header strip stays White in dark mode so the image never shows as a white box. Never use images with transparent backgrounds; they vanish in dark mode.
- No unsubscribe link, address or footer below the socials. iContact adds its own.
- Keep every `class="…"` attribute when copying a block. The classes drive dark mode.

**Fonts in email:** most inboxes can't load custom fonts. Headlines use `'Greed Condensed','Saira Condensed','Arial Narrow',Arial,sans-serif` (Saira loads from Google Fonts in Apple Mail and iOS; everyone else sees Arial Narrow or Arial). Body text and buttons are `Arial,Helvetica,sans-serif` (Arial stands in for Suisse Intl, which the guide uses for buttons, DG p76).

**Buttons:** pills, ALL CAPS, `letter-spacing: 0.2em` (DG p76). The template uses Navy with White text (short bold labels, the one light-on-dark element), and Light Blue with Navy text for a second button.

**What the template uses** (defaults, not rules): hero H1 52px (40px on mobile), section H2 36px, item titles 22px Arial bold, body 16px / 1.55, eyebrows 12–13px bold caps with 0.2em tracking, buttons 15px Arial bold caps with 0.2em tracking, 20px card radius, 600px container. List dividers are 1px, the thinnest line email clients draw reliably (the guide's 0.5pt, DG p77, is for layouts that can render it).

**Contrast in dark mode:** when a reader's device is in dark mode, the template remaps sections to Navy and Dark Blue Green with White and Light Blue text, for Apple Mail, iOS and Outlook. That's the reader's choice, so it stays. If you add a new color pairing, add matching dark-mode classes and check both modes against [`color-pairs.md`](color-pairs.md).

## Plain-text and personal emails (Gmail, replies)

From the design guide's email example (DG p37), when brand fonts aren't available:

- Greeting ("Dear Simone,"): Arial Narrow 14pt bold.
- Body: Arial 12pt, Navy or black.
- Signature: name in bold caps, then title, in Arial 12pt, then `unitedclubgymnastics.org`. Optionally the email header logo (`assets/social/ucg-email-header.png`, navy background baked in) at 260px wide.

Example signature:

```
JORDAN LEE
Events Coordinator, United Club Gymnastics
unitedclubgymnastics.org
```

Write like [`messaging.md`](messaging.md) shows: warm opener, the key information first, one clear next step, friendly sign-off ("See you in the gym," / "The UCG Team").
