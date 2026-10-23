# Content spec — dogearcleaner.com rebuild

Every post/page body lives in `content/posts/<slug>.html` or `content/pages/<slug>.html`.
`build.py` wraps it in the site layout (header, breadcrumbs, hero image, sidebar,
author box, related posts, footer, JSON-LD). **Write only the article body.**

## File format

```html
<!--meta
{
  "title": "SEO <title> tag, 50-62 chars, keyword first",
  "description": "Meta description, 140-158 chars, keyword in first 80 chars",
  "h1": "On-page H1 (can be longer than title, must contain the keyword)",
  "keyword": "primary keyword",
  "secondary": ["secondary keyword", "..."],
  "category": "reviews | how-to | guides",
  "image": "Virbac-Epi-Otic-Flush-Review.webp",
  "image_alt": "descriptive alt text",
  "published": "2026-05-06",
  "excerpt": "1-2 sentence card summary (max ~160 chars)",
  "faq": [["Question?", "Answer in 2-4 plain sentences (no HTML)."]],
  "review": {                       // ONLY on product review posts
    "product": "epi-otic",          // product key, see below
    "rating": 4.7,                  // Dog Ear Cleaner's own score out of 5
    "verdict": "One-sentence bottom line.",
    "pros": ["...", "..."],
    "cons": ["...", "..."]
  }
}
-->
<p class="lead">Opening paragraph...</p>
...
```

`build.py` renders the FAQ list as an `<h2>` FAQ section with FAQPage schema at
the end of the article, and the `review` object as a verdict box under the H1
with Review schema — so **do not** write an FAQ section or a pros/cons box
yourself. Do not write the H1. Start with `<p class="lead">`.

## Shortcodes (expanded by build.py)

| Shortcode | Renders |
| --- | --- |
| `[[product:KEY]]` | Product card: name, "best for" line, Amazon button, link to our review |
| `[[amazon:KEY\|anchor text]]` | Inline affiliate text link to that product |
| `[[amazon-search:ACCESSORY_KEY\|anchor text]]` | Inline affiliate link to an Amazon search (accessories) |
| `[[compare:KEY,KEY,KEY]]` | Comparison table of those products with Amazon buttons |
| `[[tool:schedule]]` | Interactive "How often should I clean my dog's ears?" calculator |
| `[[tool:symptoms]]` | Interactive ear symptom checker (home care vs vet) |
| `[[tool:finder]]` | Interactive "which ear cleaner fits my dog" quiz |
| `[[tool:bottle]]` | Interactive "how much cleaner per flush / how long a bottle lasts" calculator |
| `[[cta]]` | "Shop our top pick" banner linking to Epi-Otic + /best-dog-ear-cleaner/ |

Product keys (from `products.py`): `epi-otic`, `epi-otic-8oz`, `zymox-cleanser`,
`zymox-otic`, `vetericyn-plus`, `vetericyn-triple`, `petmd-tris-flush`,
`petmd-otic-clean`, `petmd-wipes`, `zymox-wipes`, `epiklean`, `ear-therapy`,
`nutri-vet`, `vets-best`, `pet-honesty`, `skouts-honor`.

Accessory keys: `cotton-rounds`, `gauze`, `ear-powder`, `lick-mat`, `dog-towel`,
`dog-dryer`, `otoscope`, `treats`, `swim-ear`, `snood`, `slicker-brush`,
`deshedding-tool`.

Shortcodes must sit on their own line (block ones: product, compare, tool, cta)
or inline inside a `<p>`/`<li>` (amazon, amazon-search).

## Allowed HTML / classes

Plain semantic HTML: `h2`, `h3`, `p`, `ul`, `ol`, `li`, `strong`, `em`, `a`,
`table` (`<table class="data">` with `thead`/`tbody`), `blockquote`.
Components:

- `<div class="callout tip"><p><strong>Tip:</strong> ...</p></div>` (also `callout vet` for "see a vet" warnings, `callout note`)
- `<div class="key-takeaways"><h2>Key takeaways</h2><ul>...</ul></div>` — put right after the lead
- `<ol class="steps"><li><h3>Step title</h3><p>...</p></li></ol>` — numbered how-to steps
- Internal links: root-relative, trailing slash, e.g. `<a href="/ear-infection-signs/">`

No inline styles, no scripts, no images (the hero image is added automatically).

## Site URLs (keep links to these exact paths)

- `/` — homepage
- `/best-dog-ear-cleaner/` — NEW roundup of the best dog ear cleaners
- `/virbac-epi-otic-flush-review/` — Virbac Epi-Otic review (site's #1 page in Search Console)
- `/zymox-ear-cleanser-review/`, `/pet-md-ear-flush-review/`, `/vetericyn-plus-ear-rinse-review/`
- `/how-to-clean-dog-earss-matters/` — how to clean dog ears (yes, the slug has the typo — keep it)
- `/ear-infection-signs/`, `/cleaning-routines/`, `/floppy-ear-breeds/`, `/after-bath-care/`
- `/tools/` — NEW interactive tools hub; tools: `/tools/ear-cleaning-schedule/`,
  `/tools/ear-symptom-checker/`, `/tools/ear-cleaner-finder/`, `/tools/ear-cleaner-dose-calculator/`
- `/resources/` (all articles), `/topic/reviews/`, `/topic/how-to/`, `/topic/guides/`
- `/about-us/`, `/contact-us/`, `/affiliate-disclosure/`, `/disclaimer/`

## Writing rules

- Brand name is **Dog Ear Cleaner** (use it naturally 2-4 times per article, e.g. "At Dog Ear Cleaner we...").
- US English. Short paragraphs (1-3 sentences). Scannable H2/H3s that contain
  keyword variants people actually search.
- Primary keyword in: the first 100 words, at least two H2s, and naturally
  ~1 per 200 words. No stuffing.
- Be honest about evidence. Do **not** claim hands-on lab testing or invent
  testers, dogs, quotes, statistics or studies. Frame as research: label
  ingredients, manufacturer directions, veterinary guidance, and patterns in
  owner reviews. Never quote Amazon star ratings, review counts or prices
  (Amazon policy) — say "check the current price on Amazon".
- Ingredient and product facts must be correct. Verify with web search when
  unsure; if you can't verify a detail, leave it out.
- Medical caution: cleaners are not medication; red-flag symptoms go to a vet.
- Every article: at least 4 affiliate touchpoints (product cards and/or inline
  links), at least one interactive `[[tool:...]]`, 4+ internal links to other
  site pages, a `key-takeaways` box, and 5-7 FAQ entries in meta.
