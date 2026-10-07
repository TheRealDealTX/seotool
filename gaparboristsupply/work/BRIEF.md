# Content brief — Gap Arborist Supply rebuild

gaparboristsupply.com was an arborist / tree-care gear e-commerce store (climbing,
rigging, rope, saws, Husqvarna power equipment, safety gear, clothing). It expired.
The new owner is rebuilding it as **their own** independent store and buying guide
under the same name. Products will be sold through **affiliate links** that are
added later, so the site shows a *typical price*, an "Add to cart" button and a
"Check price" button.

## Voice
Written by working tree people for working tree people: plain, practical, specific,
confident. US English. Short paragraphs. Talk about how the gear is used on a real
job (climb, rig, buck, chip, haul brush). No fluff ("in today's fast-paced world"),
no exclamation marks, no emoji.

## Hard rules
- **Not a copy of the old site.** Write fresh copy. Do not claim a physical address,
  phone number, years in business, staff names, or "authorized dealer" status.
- **No invented reviews, star ratings, testimonials, or sales counts.**
- **Specs:** include only figures you are confident are correct for that product
  (displacement, bar length, weight, diameter, MBS, length). If unsure, leave that
  spec out. Never guess a certification. Prefer "about" for weights.
- **Prices:** `price` is a realistic typical US street price in whole dollars
  (what a buyer would see in 2025–2026). It is shown as "Typical price".
- **Safety:** where relevant, remind readers that life-support gear must meet the
  applicable standard (ANSI Z133 / manufacturer instructions) and be inspected,
  and that they should be trained. Don't give instructions that would be unsafe.
- Use the primary keyword (highest-volume relevant keyword in the input) naturally
  in `title`, `h1`, `meta`, and the first paragraph of `summary`. Weave secondary
  keywords in naturally. Ignore junk/irrelevant keywords (e.g. "did garou break his
  limiter", "how tall is powerhouse hobbs") — never use those.
- Output must be **valid JSON** (UTF-8, straight quotes inside strings escaped). Use
  plain text in strings — no HTML, no Markdown — except that `body` paragraphs may
  contain `<a href="/path/">anchor</a>` links to other site paths you were given
  (category paths or product paths in your input) — at most 2 links per product.
- `title` ≤ 60 characters and must not include the site name (it is appended).
  `meta` 140–160 characters.

## Product JSON schema (array of objects, one per input product, same order)
```json
{
  "path": "/exact/input/path/",
  "category": "/exact/input/category/",
  "name": "Husqvarna 372XP Chainsaw",
  "brand": "husqvarna",              // brand slug, see list below
  "brand_name": "Husqvarna",
  "kind": "chainsaw",                 // one of the KIND list below
  "price": 1099,                      // integer USD typical street price
  "keyword": "husqvarna 372xp",       // primary keyword
  "title": "Husqvarna 372XP Chainsaw: Specs, Bars & Buying Guide",
  "h1": "Husqvarna 372XP Chainsaw",
  "meta": "…140-160 chars…",
  "tagline": "One line, ≤ 90 chars, what it is and who it's for.",
  "summary": "2–3 sentences. First sentence contains the keyword.",
  "highlights": ["4–6 short bullet strings"],
  "specs": [["Displacement", "70.7 cc"], ["Weight", "about 13.6 lb (powerhead)"]],
  "body": [ {"h": "Section heading", "p": ["paragraph", "paragraph"]} ],
  "faq": [ {"q": "Question?", "a": "Answer."} ],
  "use": ["climbing", "rigging", "felling", "ground", "pruning", "bucket", "plant-health", "safety", "maintenance", "apparel"], // 1–3 tags that apply
  "level": "pro" | "all" | "beginner"
}
```
Length by `tier`:
- `full`: `body` 3–4 sections, ~450–650 words total; `faq` 3–4 entries; 5–8 specs.
- `standard`: `body` 2 sections, ~200–300 words total; `faq` 2 entries; 3–6 specs.

## Category JSON schema (array of objects, one per input category, same order)
```json
{
  "path": "/exact/input/path/",
  "name": "Carabiners & Hardware",        // short nav label
  "h1": "Arborist Carabiners & Climbing Hardware",
  "keyword": "carabiners",
  "title": "≤ 60 chars, no site name",
  "meta": "140–160 chars",
  "kind": "carabiner",                    // KIND for the category art
  "intro": "2–3 sentences shown above the product grid. Contains the keyword.",
  "guide": [ {"h": "heading", "p": ["paragraph", "…"]} ],  // buying-guide below grid
  "faq": [ {"q": "…", "a": "…"} ]
}
```
Length: categories with `traffic` ≥ 1 or `backlinks` > 0 or that are top-level
(one path segment) get `guide` 3–4 sections (~450–700 words) and 3–4 FAQs. All others:
`guide` 1–2 sections (~150–250 words) and 1–2 FAQs.

## KIND list (pick the closest; it selects the product illustration)
chainsaw, top-handle, pole-saw, hand-saw, pruner, chain-bar, spark-plug, parts, fluid,
wedge-axe, log-tool, wrench-file, case-bag, chaps-pants, boot, apparel, helmet, eye-ear,
gloves, first-aid, traffic, carabiner, pulley, ascender, friction-device, lanyard, saddle,
spur, rope, throw-line, sling, rigging-device, cable-hardware, power-tool, battery, book, jobsite

## Brand slugs (use these exact slugs; if a product's brand isn't listed, make a
lowercase-hyphenated slug from the brand name, e.g. "ngk", "clogger", "cmi", "haix")
3m, all-gear, alliance-equipment, arbortec, arborwear, arbpro, art, buckingham, camp,
climb-right, climbing-innovations, climbing-technology, corona, courant, distel, dmm,
eagle-safety, echo, edelrid, fanno, felco, forester, ftc, good-rigging,
green-manufacturing, hasegawa, husqvarna, irwin, isc, jameson, k-h-distributing, kask,
klein, kong, logrite, marlow, marvin, notch-equipment, oregon, petzl, pfanner, pferd,
pro-climb, pullr-holdings, rock-exotica, safetree-products, safewaze, samson-rope,
sawpod, sena, silky, simonds, smc, stein, sterling-rope, teufelberger, weaver,
wesco-boots, westcoast-saw, yale-cordage, ngk, clogger, cmi
Unbranded / house items: use "gap" with brand_name "Gap Arborist Supply" only for
generic items (e.g. "steel locking rope snap", "chafe sleeve", "wheel chock").
