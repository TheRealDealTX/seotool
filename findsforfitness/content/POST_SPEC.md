# findsforfitness.com — article file spec

Each article is ONE file: `findsforfitness/content/posts/<slug>.html`.
The file starts with a JSON front-matter block inside an HTML comment, then the body HTML.

```
<!--
{
  "title": "H1 shown on the page (may be longer, natural)",
  "seo_title": "Title tag, <= 60 chars, contains the keyword",
  "description": "Meta description, 140-158 chars, contains the keyword",
  "keyword": "primary keyword phrase",
  "category": "skin_care | weight_loss | workout | health-tips | product-reviews",
  "published": "YYYY-MM-DD",
  "image": "<unsplash id given in your assignment>",
  "image_alt": "descriptive alt text",
  "excerpt": "1-2 sentence summary for cards (<= 180 chars)",
  "related_tool": "<tool slug or omit>",
  "faq": [ {"q": "Question?", "a": "Plain-text answer, 1-3 sentences."} ]
}
-->
<p>Intro paragraph…</p>
...
```

JSON must be valid (double quotes, no trailing commas). 3-5 FAQ items. FAQ answers plain text (no HTML).

## Body rules
- Do NOT include an H1, the hero image, the FAQ, a byline, or a disclaimer — the build adds those.
- Use `<h2>` for main sections (they become the table of contents) and `<h3>` for sub-sections. 5-9 H2s.
- Primary keyword in the first paragraph, in at least one H2, and naturally 3-6 times total. No stuffing.
- 1,100-1,700 words of body. American English. Friendly, practical, specific, second person. Short paragraphs.
- Do not claim hands-on testing ("we tested"), do not invent named studies, statistics with fake precision, prices, or quotes. General, well-established facts are fine (e.g. "the CDC recommends 150 minutes of moderate activity a week"). Be medically careful: suggest seeing a doctor/dermatologist/podiatrist where appropriate.
- External links: at most 2, only to authoritative sources (cdc.gov, nih.gov, mayoclinic.org, aad.org, heart.org, health.harvard.edu), written as `<a href="..." target="_blank" rel="noopener">`.
- Internal links: 3-6 links to other articles/tools on this site using root-relative URLs from the SLUG LIST below, e.g. `<a href="/healthy-breakfast-foods-for-weight-loss/">healthy breakfast foods</a>`. Only use URLs from the list.

## Components you may use (exact markup)
- Key takeaways box (put one right after the intro):
  `<aside class="takeaways"><p class="takeaways-title">Key takeaways</p><ul><li>…</li></ul></aside>`
- Callouts: `<div class="callout callout-tip"><strong>Tip:</strong> …</div>` — also `callout-warn` ("Heads up:") and `callout-note` ("Good to know:").
- Image (only Unsplash ids listed in your assignment as figures):
  `<figure class="post-figure"><img src="unsplash:<id>" alt="…"><figcaption>…</figcaption></figure>`
- Table: `<div class="table-wrap"><table><thead><tr><th>…</th></tr></thead><tbody><tr><td>…</td></tr></tbody></table></div>`
- Numbered steps: `<ol class="steps"><li><strong>Step name.</strong> Detail…</li></ol>`
- Checklist: `<ul class="checklist"><li>…</li></ul>`
- Tool promo (renders a card linking to an interactive tool): `<div data-tool-cta="calorie-calculator"></div>`
- Product pick card (product-review posts only):
```
<div class="pick">
  <span class="pick-badge">Best overall</span>
  <h3>Product name</h3>
  <ul class="pick-specs"><li><span>Support</span><b>Stability</b></li><li><span>Best for</span><b>Hard courts</b></li></ul>
  <p>Why it suits flat feet…</p>
  <div class="pros-cons"><div class="pros"><p>Pros</p><ul><li>…</li></ul></div><div class="cons"><p>Cons</p><ul><li>…</li></ul></div></div>
</div>
```
- Exercise card (workout posts): `<div class="exercise"><h3>1. Push-up</h3><p class="exercise-meta"><span>Targets: chest, triceps</span><span>3 x 8-12</span></p><p>How to…</p></div>`

No inline styles, no scripts, no other classes.

## SLUG LIST (internal link targets)
Articles:
/best-tennis-shoes-for-flat-feet/
/how-to-choose-running-shoes-for-flat-feet/
/flat-feet-exercises/
/plantar-fasciitis-stretches/
/the-beginners-guide-to-starting-a-running-routine/
/healthy-breakfast-foods-for-weight-loss/
/essential-ways-to-lose-weight-naturally/
/vegan-diet-for-weight-loss-weight-loss-tips/
/apple-cider-vinegar-for-weight-loss/
/how-to-calculate-a-calorie-deficit/
/walking-for-weight-loss/
/benefits-of-beet-juice-for-skin-secret-to-radiant-skin/
/say-goodbye-to-blackheads-with-the-ultimate-blackhead-vacuum/
/how-to-get-rid-of-wrinkles-under-eyes-a-comprehensive-guide/
/natural-ingredients-for-healthy-skin-a-comprehensive-guide/
/essential-benefits-of-charcoal-on-skin/
/how-to-lighten-dark-lips-best-tips/
/the-ultimate-guide-to-nail-care-routine-at-home/
/10-best-glow-up-tips-that-actually-work/
/essential-benefits-of-coconut-water-for-skin/
/daily-skincare-routine-for-glowing-skin/
/how-much-water-should-you-drink-a-day/
/how-much-protein-do-you-need-to-build-muscle/
/10-basic-calisthenics-exercises-for-beginners/
/full-body-home-workout-no-equipment/
/hiit-vs-steady-state-cardio-for-fat-loss/
/beginner-strength-training-guide/
Tools (also valid for data-tool-cta, without slashes/prefix):
/tools/bmi-calculator/  /tools/calorie-calculator/  /tools/protein-calculator/
/tools/water-intake-calculator/  /tools/running-pace-calculator/
/tools/shoe-finder-quiz/  /tools/interval-timer/
