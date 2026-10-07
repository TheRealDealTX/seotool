# Cebu-Davao content guide (for writers)

Each post is one Markdown file: `content/posts/<slug>.md`, where `<slug>` is the
last segment of its path (e.g. `/food/pinoy-barbecue-recipe/` -> `pinoy-barbecue-recipe.md`).

## Front matter (required, exact format: `key: value`, one per line)

```
---
title: Cebu Lechon Recipe: The Secret Stuffing That Needs No Sauce
path: /food/secret-ingredients-of-cebu-lechon-revealed/
category: food
places: cebu
keyword: cebu lechon recipe
description: 140-158 character meta description that contains the primary keyword and makes people click.
image: cebu-lechon
image_alt: Whole Cebu lechon with crisp golden skin on a banana-leaf tray
type: recipe
excerpt: One or two sentences (max ~200 chars) shown on cards and category pages.
recipe_yield: 6 servings
recipe_prep: PT30M
recipe_cook: PT2H
---
```

- `title`: the SEO title / H1. 45-65 characters, primary keyword near the start. No site name (added automatically).
- `path`: exactly as given in your brief. Never change it.
- `category`: one of `news, travel, food, culture, lifestyle, entertainment, sports, money, tech` (as given in brief).
- `places`: comma list from `cebu, davao, other` (as given).
- `keyword`: primary keyword (as given, lowercase). It MUST appear in title, description, the first paragraph and at least one `##` heading.
- `type`: `article` (default), `guide`, `listicle`, or `recipe`.
- Recipes: add `recipe_yield`, `recipe_prep`, `recipe_cook` (ISO-8601 durations) and the body MUST contain `## Ingredients` (a `-` list) and `## Instructions` (a `1.` list). These become Recipe schema.
- `image`: one key from the photo list below (pick the most relevant). `image_alt`: specific, descriptive alt text.

## Body (Markdown subset — nothing else is supported)

- `## Heading` and `### Subheading` (no `#` H1 — the title is the H1)
- Paragraphs separated by a blank line. Keep them 2-4 sentences.
- `- item` bullet lists, `1. item` numbered lists (one level only, no nesting)
- `**bold**`, `*italic*`, `[link text](/internal/path/)` or `[text](https://external.example)`
- Tables: header row, `|---|---|` separator, rows. Keep 2-5 columns.
- `> **Tip:** text` callouts (single paragraph blockquotes)
- Widgets, on their own line: `{{widget:NAME}}` — available: `weather-cebu`, `weather-davao`,
  `fish-translator`, `bisaya-dictionary`, `distance`, `currency`, `budget`, `quiz-destinations`,
  `festival-countdown`, `news-wire-cebu`, `news-wire-davao`. Use only where a brief suggests it
  or it clearly helps the reader (max 1-2 per post).
- End every post with `## Frequently Asked Questions` containing 3-5 `### Question?` subheadings,
  each followed by a 1-3 sentence answer paragraph. These become FAQPage schema.

## Length and structure

- 1,000-1,600 words of body text (recipes 800-1,300). Quality over padding.
- Open with a 2-3 sentence answer-first intro that uses the primary keyword naturally.
- Use the secondary keywords from the brief naturally in headings/body where they fit. Never stuff.
- Include a quick-facts table or comparison table when it helps.
- Add 3-6 internal links to other posts on this site (paths listed in `content/briefs/ALL_PATHS.md`)
  and to tools: `/weather/`, `/tools/`, `/tools/bisaya-dictionary/`, `/tools/fish-names/`,
  `/tools/currency-converter/`, `/tools/trip-budget-calculator/`, `/tools/festival-calendar/`,
  `/travel/mileage-from-to-distance-between-cities/`, `/cebu/`, `/davao/`, `/news/`.
- 1-3 external links to authoritative/official sources where relevant (PAGASA, DFA, DOT, official LGU
  or company sites). Use homepages or obvious stable URLs only — never guess deep URLs.

## Accuracy rules (critical — this is a news/travel site)

- Today is October 2026. Do not describe news events after mid-2026 or invent recent events.
- NEVER invent statistics, quotes, people, prices, schedules, phone numbers, addresses or opening hours.
- Prices and fares: give approximate ranges and say they are approximate and change; tell readers to confirm.
- Only name businesses, bands, people and places you are confident exist(ed). When unsure, leave it out.
- Neutral and non-partisan on politics. No gossip, no sexualised content, no defamation.
- Health topics: factual, cautious, add "This article is for general information, not medical advice" and suggest seeing a doctor.
- Write in clear international English with a warm local voice; Bisaya/Tagalog terms in *italics* with meaning.
- Do not mention that content is AI-written, and do not mention the old site or 2017.

## Photo keys (for `image:`)

cebu-skyline, cebu-it-park, magellans-cross, santo-nino-basilica, fort-san-pedro, taoist-temple-cebu,
temple-of-leah, sinulog, kawasan-falls, moalboal, oslob-whale-shark, bantayan-island, malapascua,
mactan-beach, cclex-bridge, simala-shrine, cebu-lechon, lechon-roasting, puso-rice, siomai, cebu-guitar,
davao-city, davao-peoples-park, mount-apo, philippine-eagle, samal-beach, pearl-farm, talikud-island,
durian, kadayawan, eden-nature-park, davao-river, marilog, kinilaw, tuna-gensan, bangus, adobo, sinigang,
halo-halo, barbecue-pinoy, boodle-fight, batchoy, pancit, dried-fish, fish-market, basil, chocolate-hills,
tarsier, boracay, siargao, el-nido, coron, banaue, vigan, intramuros, manila-skyline, camiguin, siquijor,
jeepney, ferry, mactan-airport, davao-airport, airplane-philippines, passport, basketball-court, boxing,
football-philippines, pickleball, surfing, running-race, esports, smartphone, gecko-tuko, chinese-new-year,
edsa, rizal, concert, guitar-band, cinema, books, typhoon-satellite, rain-street, spratly, mall, bpo-office,
condo-cebu, market-carbon, coffee, money-peso, atm, hospital, hands-palm, face-portrait, batman, rice-field,
coconut-trees, mangrove, plantation-bay, lapu-lapu-shrine, tops-lookout, bohol-loboc, camotes, iloilo,
bacolod-masskara, cagayan-de-oro, baguio, sunset-beach, island-hopping, snorkel-reef, tribal-davao, church-cebu
