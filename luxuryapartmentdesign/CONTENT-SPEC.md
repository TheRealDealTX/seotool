# Luxury Apartment Design — content spec

The site is a custom PHP site (no WordPress). Every article is two files in
`content/articles/`:

- `<slug>.json` — metadata (schema below), UTF-8, valid JSON.
- `<slug>.html` — the article body as an HTML fragment.

The PHP layout renders the H1, hero image, byline/dates, table of contents
(built from the body's `<h2>` tags), key takeaways box, the tool call-to-action,
the FAQ section (with FAQPage schema), related articles, and all schema. **Do not
put any of those in the body.**

## `<slug>.json`

```json
{
  "slug": "how-to-hang-wall-art",
  "title": "How to Hang Wall Art: Heights, Spacing & Layouts",
  "h1": "How to Hang Wall Art: The Complete Guide to Height, Spacing and Layout",
  "description": "Learn how to hang wall art like a designer: the 57-inch rule, spacing over sofas and beds, gallery wall layouts, and the right hardware for every wall.",
  "keyword": "how to hang wall art",
  "secondary_keywords": ["how high to hang art", "gallery wall spacing"],
  "category": "living-tips",
  "excerpt": "One or two sentences used on cards and listing pages (max ~170 chars).",
  "image": "how-to-hang-wall-art",
  "image_alt": "Descriptive alt text of the hero image that includes the topic naturally",
  "published": "2025-09-15",
  "updated": "2026-10-28",
  "key_takeaways": ["3 to 5 short, concrete takeaways"],
  "faq": [{"q": "Question people actually search?", "a": "40–80 word direct answer, plain text."}],
  "related": ["slug-one", "slug-two", "slug-three"],
  "tool": "art-hanging-calculator"
}
```

Rules:
- `title` ≤ 60 characters, keyword near the front. The layout does NOT append the brand.
- `description` 140–158 characters, includes the keyword, reads like an invitation.
- `h1` contains the keyword (can be longer than the title).
- `image`: use the value given in your assignment exactly (a file stem in `assets/img/articles/`).
- `published`: use the date given in your assignment. `updated`: `2026-10-28`.
- `faq`: 4–6 items, questions phrased the way people search (People Also Ask style). Plain text answers, no HTML.
- `related`: exactly 3 slugs from the article list below (not itself).
- `tool`: one tool slug from the tool list below, or `null`.

## `<slug>.html` body

- Start with a 2–3 paragraph intro (`<p>`) that answers the search intent fast and uses the primary keyword in the first 100 words. No heading before the intro.
- Then 6–10 `<h2>` sections, with `<h3>` subsections where useful. Write H2s that match sub-queries people search ("How High Should You Hang Art Above a Sofa?").
- Allowed tags: `p h2 h3 h4 ul ol li strong em a table thead tbody tr th td blockquote div span br`.
- Allowed components (use 2–4 per article, they make pages scannable):
  - `<div class="callout"><p><strong>Designer tip:</strong> …</p></div>`
  - `<div class="callout callout--warn"><p><strong>Renter note:</strong> …</p></div>`
  - `<table class="data-table">…</table>` with `<thead>` — use at least one table of real, useful numbers/comparisons per article.
  - `<div class="checklist"><ul><li>…</li></ul></div>` for step lists / checklists.
  - `<div class="pull-quote"><p>…</p></div>` sparingly (one line of opinion, no fake attributions).
- **No** `<h1>`, `<img>`, `<script>`, `<style>`, inline `style=""`, FAQ section, "Conclusion"-titled heading (use a meaningful final H2 like "Putting It All Together" or a next-steps section), or key-takeaways box.
- Internal links: 4–8 per article, root-relative with trailing slash (`/small-apartment-ideas/`, `/tools/rug-size-calculator/`). Link only to slugs in the lists below. Use descriptive anchor text.
- No external links.
- Length: rewritten articles 1,500–2,200 words; new pillar articles 2,200–3,000 words.
- Voice: confident, warm, specific, written for apartment dwellers and renters who want a high-end look. Concrete measurements, materials, finishes, budgets, and step-by-step instructions. Address the reader as "you".
- Mention the brand "Luxury Apartment Design" naturally at most once per article (optional).
- Accuracy: no invented statistics, studies, surveys, quotes, named experts, or product claims. Standard design guidelines (e.g. art centered at 57–60 in., 8–10 in. above a sofa, rugs 12–18 in. from walls, 2/3 rule) are fine.
- US spelling and imperial units first, metric in parentheses where helpful.
- Avoid filler phrases ("In today's fast-paced world", "Look no further", "elevate your space" more than once, "game-changer", "delve").

## Categories (`category` value)

| slug | name |
| --- | --- |
| `apartment-design-inspiration` | Design Inspiration |
| `living-tips` | Decor & Styling |
| `space-optimization-storage` | Small Spaces & Storage |
| `renovations-makeovers` | Renovations & Makeovers |
| `color-paint` | Color & Paint |
| `balcony-outdoor` | Balcony & Outdoor Living |

## Tools (`/tools/<slug>/`)

| slug | what it does |
| --- | --- |
| `interior-design-style-quiz` | 8-question quiz that tells you your interior design style (Quiet Luxury, Japandi, Modern Minimalist, Warm Contemporary, Art Deco Glam, Organic Modern, Classic Parisian, Mid-Century Modern) |
| `room-color-palette-generator` | Pick a base color and a harmony; get a 60-30-10 palette with hex codes, preview room |
| `rug-size-calculator` | Enter room type and dimensions; get the recommended rug size and placement |
| `art-hanging-calculator` | Enter ceiling height, art height, furniture height; get nail height and spacing, gallery wall spacing |
| `paint-calculator` | Room dimensions, doors, windows, coats; gallons of paint and primer needed, cost estimate |
| `room-lighting-calculator` | Room type and size; lumens needed, number of bulbs, layered lighting plan |
| `curtain-size-calculator` | Window width/height and style; panel width, length, rod length and mounting height |
| `decorating-budget-planner` | Total budget and room; allocates spend by category with priorities |
| `room-layout-planner` | Drag-and-drop furniture onto a scaled floor plan of your room, checks walkway clearances |

## Article list (all slugs)

| slug | primary keyword | category |
| --- | --- | --- |
| `luxury-apartment-interior-design` | luxury apartment interior design | apartment-design-inspiration |
| `apartment-decorating-ideas` | apartment decorating ideas | apartment-design-inspiration |
| `small-apartment-ideas` | small apartment ideas | space-optimization-storage |
| `apartment-living-room-ideas` | apartment living room ideas | apartment-design-inspiration |
| `apartment-bedroom-ideas` | apartment bedroom ideas | apartment-design-inspiration |
| `how-to-make-your-apartment-look-expensive` | how to make your apartment look expensive | apartment-design-inspiration |
| `quiet-luxury-interior-design` | quiet luxury interior design | apartment-design-inspiration |
| `renter-friendly-upgrades` | renter friendly upgrades | renovations-makeovers |
| `apartment-kitchen-ideas` | apartment kitchen ideas | renovations-makeovers |
| `studio-apartment-design-ideas-layouts-decor-tips` | studio apartment ideas | apartment-design-inspiration |
| `japandi-rug-the-perfect-blend-of-minimalism-and-warmth` | japandi rug | apartment-design-inspiration |
| `types-of-minimalism` | types of minimalism | apartment-design-inspiration |
| `how-to-hang-wall-art` | how to hang wall art | living-tips |
| `how-to-style-pillows-on-a-couch` | how to style pillows on a couch | living-tips |
| `living-room-fairy-lights` | fairy lights living room | living-tips |
| `diy-bedroom-fairy-lights` | fairy lights bedroom | living-tips |
| `easy-home-decor-ideas` | easy home decor ideas | living-tips |
| `diy-home-decor-ideas` | diy home decor ideas | living-tips |
| `home-refresh` | home refresh ideas | living-tips |
| `declutter-checklist` | declutter checklist | space-optimization-storage |
| `spare-bedroom-ideas` | spare bedroom ideas | space-optimization-storage |
| `organized-mudroom` | mudroom organization | space-optimization-storage |
| `guest-quarters-laundry-room` | small laundry room ideas | space-optimization-storage |
| `double-layered-sliding-bathroom-drawers-for-toiletries` | bathroom drawer organizer | space-optimization-storage |
| `hidden-key-cabinet-in-the-kitchen` | hidden key cabinet | space-optimization-storage |
| `home-gym-decor` | home gym decor | space-optimization-storage |
| `small-bathroom-design` | small bathroom design | renovations-makeovers |
| `sliding-shower-doors` | sliding shower doors | renovations-makeovers |
| `repair-drywall-after-removing-wallpaper` | repair drywall after removing wallpaper | renovations-makeovers |
| `trim-around-front-door` | front door trim ideas | renovations-makeovers |
| `pastel-colors-for-home` | pastel colors for home | color-paint |
| `warm-pastel-bedroom-paint-colors` | warm pastel bedroom paint colors | color-paint |
| `what-color-goes-with-lavender` | what color goes with lavender | color-paint |
| `luxury-small-garden-ideas` | luxury small garden ideas | balcony-outdoor |
| `how-to-arrange-garden-pots` | how to arrange potted plants | balcony-outdoor |
| `decorate-your-patio` | patio decorating ideas | balcony-outdoor |
