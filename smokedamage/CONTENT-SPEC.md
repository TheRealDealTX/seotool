# SmokeDamage.com — content format & editorial rules

Every page body lives in `content/` as a Markdown-lite file. `build.py` renders
it into the shared layout. No HTML is needed in content files (inline HTML is
passed through, but avoid it).

## Front matter

Each file starts with a front-matter block. One `key: value` per line.

```
---
path: /smoke-damage-claims/
title: Smoke Damage Insurance Claims in Texas | Smoke Damage PA      (SEO title, ~50-60 chars)
description: Meta description, MAX 150 characters including spaces.
h1: Smoke Damage Insurance Claims in Texas
eyebrow: Smoke Damage Claims
lead: One or two sentences shown under the H1 in the page hero.
keyword: smoke damage insurance claim
image: hero-smoke-interior
breadcrumb: Smoke Damage Claims
parent: /claims/                       (optional; breadcrumb parent path, omit for top level)
schema: Service                        (Service | Article | WebPage | AboutPage | ContactPage)
updated: 2026-09-28
related: /soot-damage-claims/, /hvac-smoke-damage/, /smoke-damaged-contents/
---
```

Blog posts add: `published: 2026-09-28`, `author: Joseph Dittman`,
`category: Claim Documentation`, `status: published` (or `draft`).
Location pages add: `city: Houston`, `county: Harris County`,
`region: Gulf Coast`, `nearby: Pasadena, Pearland, Katy, Sugar Land`,
`lat: 29.7604`, `lng: -95.3698`.
Events add: `event_date`, `county`, `area`, `event_type`, `status`,
`acreage` (only if verified), `structures` (only if verified), `last_updated`.

## Body syntax

- `## Heading` (H2) and `### Heading` (H3). Never use `#` (H1 comes from front matter).
- Blank line separates paragraphs.
- `- item` bullets, `1. item` numbered lists.
- Pipe tables (`| a | b |` + `|---|---|` separator row).
- `**bold**`, `*italic*`, `[link text](/internal-path/)`, external links `[TDI](https://www.tdi.texas.gov/...)`.
- `{{phone}}` renders the clickable phone number; `{{email}}` the email link;
  `{{review}}` renders a "Request a Free Claim Review" link to /contact/.

Blocks (open with `:::name`, close with a line containing only `:::`):

| Block | Use |
|---|---|
| `:::cta Optional headline` | Conversion banner (phone + free claim review buttons). Optional body text inside. Use 1-3 per long page, between major sections. |
| `:::note Title` | Callout box (e.g. "Policy language matters"). |
| `:::faq` | FAQ accordion. Inside: `### Question?` followed by answer paragraph(s). Generates FAQPage schema. One per page max, usually near the end. |
| `:::cards` | Card grid. Inside: `### Card title`, paragraph, optional last line `-> /path/` to make the card a link. |
| `:::steps` | Numbered process timeline. Inside: `### Step title` + paragraph. |
| `:::checklist Title` | Styled checklist; inside is a `- ` list. |
| `:::sources` | "Sources" box; inside is a `- [Title](url)` list. Required on any page citing law, regulation, or events. |
| `:::figure image-key` | Full-width image; inside is the caption text (one line). |

## Image keys (use only these)

hero-fire-house, burned-house, smoke-interior, soot-ceiling, smoke-kitchen,
smoke-hallway, contents-damage, electronics, hvac-vent, ductwork,
commercial-fire, adjuster-documenting, inspection, contents-inventory,
paperwork-review, texas-home, texas-business, wildfire, attic-insulation,
burned-furniture, office-interior, restaurant, warehouse, multifamily,
houston, dallas, austin, san-antonio, texas-landscape

## Business facts (use exactly)

- Brand: Smoke Damage Public Adjuster (site: SmokeDamage.com)
- Operated by: Rise Public Adjusting LLC — Texas Department of Insurance License #3356839
- Phone: +1 (844) 537-1427 (use `{{phone}}`), email info@smokedamage.com
- Service area: all of Texas. Author of articles: Joseph Dittman.
- There are NO verified years in business, claim counts, settlement totals, success
  rates, awards, certifications, offices, staff bios, testimonials, or case studies.
  Never invent any of these.

## Editorial rules (non-negotiable)

We represent policyholders in property insurance claims. We are NOT a restoration
contractor — never imply we clean, remediate, demolish, repair or rebuild. We
document, prepare, present and negotiate claims. No result is guaranteed. Coverage
depends on the policy and the facts of the loss.

DO: document the full scope of the loss; understand what is and is not in the
carrier's estimate; present the claim with organized supporting information;
request a closer review. Explain concepts plainly. Short paragraphs. Helpful H2/H3s.
Tables only where they genuinely help. Internal links to related pages.

DON'T: promise maximum/larger settlements or claim increases; say "fight the
insurance company", "every penny", "insurance companies always underpay"; call
carriers or their adjusters dishonest; give legal, medical, health or
hazardous-cleanup advice; give HVAC repair instructions; invent statistics,
laws, deadlines, court cases, events, customer stories; answer coverage
questions categorically ("yes, that's covered") — always explain that policy
language and facts matter. No hype, clichés, filler or obvious AI phrasing
("In today's world", "navigating the complexities", "it's important to note",
"delve", "comprehensive guide", "rest assured", "peace of mind").

Texas law statements must come from `research/compliance.md` (verified against
TDI / Texas Insurance Code ch. 4102 / 28 TAC). If it is not there, don't state it.

Keyword use: natural language, never stuffed. The phrase "Smoke Damage Public
Adjuster" can appear a few times per page where natural.

## Internal URL map (link only to these)

/ · /about/ · /smoke-damage-claims/ · /fire-damage-claims/ · /soot-damage-claims/ ·
/smoke-odor-claims/ · /hvac-smoke-damage/ · /smoke-damaged-contents/ ·
/residential-smoke-damage-claims/ · /commercial-smoke-damage-claims/ ·
/denied-smoke-damage-claims/ · /underpaid-smoke-damage-claims/ ·
/delayed-smoke-damage-claims/ · /smoke-damage-claim-process/ ·
/texas-smoke-damage-public-adjuster/ · /texas-public-adjuster-rules/ ·
/texas-fire-smoke-events/ · /texas-fire-smoke-history/ · /tools/ ·
/tools/smoke-damage-scope-calculator/ · /tools/contents-rcv-acv-calculator/ ·
/texas/ · /texas/<city-slug>/ · /blog/ · /faq/ · /contact/ · /privacy-policy/ ·
/terms-of-use/ · /disclaimer/ · /sitemap/
