# Email

## Announcement / newsletter emails (HTML)

Start from [`templates/email/ucg-announcement-email.html`](../templates/email/ucg-announcement-email.html). It is UCG's working monthly-announcements template (sent through iContact) and its comments explain how to use it. In short:

- Parts marked **FIXED** never change: header logo, base styles, dark-mode rules, sign-off and social links.
- Build the body from the **BLOCKS** between `BODY START` and `BODY END`: hero, feature band, section label, standard item, light card, navy card, two buttons, discipline section, deep band. Copy a block, replace every `[PLACEHOLDER]`, delete what you don't need.
- Keep the sender's wording. Fix only obvious typos.
- Neighboring sections usually get different backgrounds (white, light blue, blue green, navy, dark blue green), so the email reads as separate blocks.
- Small text follows the color pairs ([`color-pairs.md`](color-pairs.md)): on Blue Green it's Dark Blue Green, not Navy; on Navy it's White, Light Blue or Golden Yellow, not Blue Green (DG p42–43).
- Chips: a Red Orange, Golden Yellow or Purple fill with Navy text.
- Every link is https. Buttons for main actions, text links (`Link text →`) for secondary ones.
- Images: only the fixed logo unless an image hosted by the email platform is supplied. Never use white or light images with transparent backgrounds; they vanish in dark mode.
- No unsubscribe link, address or footer below the socials. iContact adds its own.
- Keep every `class="…"` attribute when copying a block. The classes drive dark mode.

**Fonts in email:** most inboxes can't load custom fonts. Headlines use `'Greed Condensed','Saira Condensed','Arial Narrow',Arial,sans-serif` (Saira loads from Google Fonts in Apple Mail and iOS; everyone else sees Arial Narrow or Arial). Body text and buttons are `Arial,Helvetica,sans-serif` (Arial stands in for Suisse Intl, which the guide uses for buttons, DG p76).

**Buttons:** pills, ALL CAPS, `letter-spacing: 0.2em` (DG p76). The template uses Navy with White text, and Light Blue with Navy text.

**What the template uses** (defaults, not rules): hero H1 52px (40px on mobile), section H2 36px, item titles 22px Arial bold, body 16px / 1.55, eyebrows 12–13px bold caps with 0.2em tracking, buttons 15px Arial bold caps with 0.2em tracking, 20px card radius, 600px container. List dividers are 1px, the thinnest line email clients draw reliably (the guide's 0.5pt, DG p77, is for layouts that can render it).

**Contrast in dark mode:** the template remaps backgrounds and text for Apple Mail, iOS and Outlook. If you add a new color pairing, add matching dark-mode classes and check both modes against [`color-pairs.md`](color-pairs.md).

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
