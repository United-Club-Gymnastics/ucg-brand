# Email

## Announcement / newsletter emails (HTML)

Start from [`templates/email/ucg-announcement-email.html`](../templates/email/ucg-announcement-email.html). It is UCG's working monthly-announcements template (sent through iContact) and its comments explain the rules. In short:

- Parts marked **FIXED** never change: header logo, base styles, dark-mode rules, sign-off and social links.
- Build the body from the **BLOCKS** between `BODY START` and `BODY END`: hero, feature band, section label, standard item, light card, navy card, two buttons, discipline section, deep band. Copy a block, replace every `[PLACEHOLDER]`, delete what you don't need.
- Keep the sender's wording. Fix only obvious typos.
- Alternate section backgrounds so neighbors differ: white → light blue → blue green → navy → dark blue green.
- Red Orange chips only for deadlines and urgent items, always with Navy text on them.
- Discipline chips: WAG Purple `#ADBAE9`, MAG Blue Green `#A5C8CF`, T&T Golden Yellow `#F6C328`, all with Navy text.
- Every link is https. Buttons for main actions, text links (`Link text →`) for secondary ones.
- Images: only the fixed logo unless an image hosted by the email platform is supplied. Never use white or light images with transparent backgrounds; they vanish in dark mode.
- No unsubscribe link, address or footer below the socials. iContact adds its own.
- Keep every `class="…"` attribute when copying a block. The classes drive dark mode.

**Fonts in email:** most inboxes can't load custom fonts. Headlines use `'Greed Condensed','Saira Condensed','Arial Narrow',Arial,sans-serif` (Saira loads from Google Fonts in Apple Mail and iOS; everyone else sees Arial Narrow or Arial). Body text is always `Arial,Helvetica,sans-serif`.

**Sizes used by the template:** hero H1 52px (40px on mobile), section H2 36px, item titles 22px Arial bold, body 16px / 1.55, eyebrows 12–13px bold caps with 0.16em tracking, buttons 16px caps with 0.2em tracking, 8px button radius, 20px card radius, 600px container.

**Contrast in dark mode:** the template remaps backgrounds and text for Apple Mail, iOS and Outlook. If you add a new color pairing, add matching dark-mode classes and check both modes against [`color-pairs.md`](color-pairs.md).

## Plain-text and personal emails (Gmail, replies)

From the design guide (DG p37): when brand fonts aren't available, use Arial.

- Greeting and body: Arial 12pt, Navy or black.
- A short headline, if any: Arial Narrow 14pt bold, ALL CAPS.
- Signature: name and title in Arial 12pt, then `unitedclubgymnastics.org`. Optionally the email header logo (`assets/social/ucg-email-header.png`, navy background baked in) at 260px wide.

Example signature:

```
Ilana Shushansky
Director of Operations, United Club Gymnastics
unitedclubgymnastics.org
```

Write like [`messaging.md`](messaging.md) shows: warm opener, the key information first, one clear next step, friendly sign-off ("See you in the gym," / "The UCG Team").
