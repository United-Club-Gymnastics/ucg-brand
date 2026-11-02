# Google Docs and Forms (policies, guides, letters, forms)

Policies and official documents are "core system" work: clarity beats flair. Keep them calm, consistent and easy to scan.

**Start from a template** (in the Google Docs **Template gallery** under United Club Gymnastics, or the link opens your own copy; UCG Google accounts only):

- [Policy](https://docs.google.com/document/d/1oC-g9xVgEFwP1pCBPfpUfnWDGawBIE3UF858RqZhGG8/copy): numbered sections and subsections, amendments, version history
- [Change proposal](https://docs.google.com/document/d/11yKkZv8L44MRprWYa-Ppe_IXf-Wu4KcG2ku_heYfjtU/copy): the proposal, rollout and communication plan
- [Meeting minutes](https://docs.google.com/document/d/1Yz_r_cHrSBO9s4XeSwUXvlf468QuEn9SxWmLGFZbyE8/copy): attendance, agenda and notes, action items, sign-off, minute-taking guidelines
- [Email draft](https://docs.google.com/document/d/13eIZoEsXOzOZCphU0q-_o5OzgLqNAaC8tsz1A0JpJu4/copy): draft an announcement block by block before it's built in the [HTML email template](email.md)

Replace every `[bracketed]` placeholder, delete the guidance lines, and use the built-in styles (Title, Heading 1, Heading 2, Normal text). The rest of this page is for building something the templates don't cover.

## Page setup

- US Letter, portrait, 1 in margins (0.75 in is fine for long reference guides).
- **Header:** the UCG document header image (`assets/logos/ucg-document-header.png`, a Navy band with the mark, "UCG" and the web address) full width at the top of page 1, or the primary logo (`ucg-primary-navy.png`, about 2.2 in wide) top-left.
- **Footer:** document title and effective date left, page number right, Arial 9pt Dark Blue Green `#184B56`.

## Styles

Set these once with Format → Paragraph styles → "Update to match", then Options → "Save as my default styles".

| Style | Font | Size | Color | Spacing |
|---|---|---|---|---|
| Title | Saira Condensed Bold, ALL CAPS | 28–32pt | Navy `#1E2B38` | 0 before, 6pt after |
| Subtitle | Arial | 12pt | Dark Blue Green `#184B56` | 0 before, 18pt after (effective date, version, owner) |
| Heading 1 | Saira Condensed Bold, ALL CAPS | 18pt | Navy | 18pt before, 6pt after |
| Heading 2 | Arial Bold | 13pt | Dark Blue Green `#184B56` | 14pt before, 4pt after |
| Heading 3 | Arial Bold | 11pt | Navy | 10pt before, 2pt after |
| Normal text | Arial | 11pt | Navy (or black) | line spacing 1.15, 8pt after |
| Links | | | Dark Blue Green, underlined | |

- Sentence case for Heading 2 and below; ALL CAPS only for Title and Heading 1.
- Number policy sections (1, 1.1, 1.2) when people will cite them; otherwise use plain headings.
- Bullets for unordered items, numbers for steps or ranked items. Keep list items short.
- Tables: header row Navy fill with White Arial Bold text, or Light Blue fill with Navy text; body Arial 10pt; borders Blue Green `#A5C8CF` at 0.5pt.
- Callouts (key rule, deadline, definition): a one-cell table with Light Blue `#DBEBEE` fill, no border, Navy text. Use Golden Yellow fill + Navy text only for warnings.
- Never colored text other than Navy, and Dark Blue Green for links and secondary notes.

## Writing policies

- Open with a two- or three-sentence purpose statement: what this policy is, who it applies to, and when it takes effect.
- Put what people must do before background and rationale.
- Plain language: "must", "may", "should" used consistently; define terms once in a short definitions section.
- Warm but credible (the "Good Spot" voice): structure that supports people, not legalese that shuts them out.
- End with contacts: who to ask, and how (e.g. an email address on unitedclubgymnastics.org).
- Include a version history table at the end for policies that change.

## Letters and memos

Follow the design guide letterhead: logo top-left, then `Date`, `From`, `Subject` lines in Arial 10pt, body Arial 11pt, sign-off with name, title and `unitedclubgymnastics.org`.

## Google Forms

Start from the [UCG Google Form template](https://docs.google.com/forms/d/1-LLH8MvdZVirtOoXdx1vy83OLZDl11T9zQEAXh3cCGk/copy) (in the Google Forms **Template gallery** under United Club Gymnastics). Its theme is already set: the UCG header image, Saira Condensed for the header (24) and questions (14), Arial 11 for text, Navy as the theme color, and email collection on. Give the form a clear title and a one-line description (what, who, deadline), keep question titles short, and turn off email collection if you don't need it.

## Building docs with the API (for agents)

Use a UCG Google Workspace account so files land in UCG's Drive. Copy the matching template (Drive `files.copy`) instead of building from scratch: policy `1oC-g9xVgEFwP1pCBPfpUfnWDGawBIE3UF858RqZhGG8`, change proposal `11yKkZv8L44MRprWYa-Ppe_IXf-Wu4KcG2ku_heYfjtU`, meeting minutes `1Yz_r_cHrSBO9s4XeSwUXvlf468QuEn9SxWmLGFZbyE8`, email draft `13eIZoEsXOzOZCphU0q-_o5OzgLqNAaC8tsz1A0JpJu4`, form `1-LLH8MvdZVirtOoXdx1vy83OLZDl11T9zQEAXh3cCGk` (the Forms API can't set themes, so copy this one rather than creating a form). Their named styles are already set, so apply `namedStyleType` (TITLE, HEADING_1 …) rather than formatting text by hand. Google Docs styles can't force capitals, so type Title and Heading 1 text in capitals.
