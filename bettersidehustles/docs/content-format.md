# Content file format

Every URL on the site is one PHP file that returns an array. The router
(`index.php`) maps `/{slug}/` to `content/posts/{slug}.php` (articles) or
`content/pages/{slug}.php` (static pages). Adding a file publishes the page and
adds it to the blog index, the sitemaps and the RSS feed — nothing else to edit.

```php
<?php
return [
    'title'       => 'Best Side Hustles in Indianapolis (2026): 21 Ways to Earn',  // <title>, 50–62 chars, primary keyword first
    'description' => '…',            // meta description, 140–160 chars, keyword + a reason to click
    'h1'          => '…',            // one H1, contains the primary keyword
    'kicker'      => 'City Guide',   // small label above the H1
    'dek'         => '…',            // one or two sentences under the H1
    'published'   => '2026-01-09',   // keep the original publish date for existing URLs
    'modified'    => '2026-10-26',
    'image'       => '/wp-content/uploads/2026/01/Best-Side-Hustles-in-Indianapolis.webp',
    'image_alt'   => '…',
    'category'    => 'City Guides',  // City Guides | Platform Guides | Side Hustle Ideas | Money & Taxes
    'keywords'    => ['side hustle indianapolis', '…'],   // internal only: validate.py checks the first one
    'tool'        => 'gig-calculator',   // optional: widget shown in the sidebar (see tool keys)
    'gear'        => ['phone-mount', 'dash-cam', 'book-side-hustle'],  // optional: Amazon gear box at the end
    'related'     => ['best-side-hustles-in-columbus', 'side-hustles-you-can-start-with-just-your-smartphone'],
    'faq'         => [
        ['q' => 'What is the best side hustle in Indianapolis?', 'a' => 'Plain text or light HTML answer, 40–90 words.'],
    ],
    'body'        => <<<'HTML'
<p>Opening paragraph…</p>
<h2 id="why-indianapolis">Why Indianapolis works for side hustles</h2>
…
HTML,
];
```

Pages (`content/pages/`) use the same keys; `kicker`, `image`, `tool`, `gear`,
`faq` and `related` are optional and `'layout' => 'page'` drops the sidebar.

## Body HTML rules

- Start with a `<p>`. No `<h1>` in the body. Every `<h2>` needs a unique,
  short, lowercase-hyphenated `id` — the table of contents is built from them.
  `<h3>` should have an `id` too.
- Do **not** put the FAQ in the body; the `faq` array is rendered as an
  accordion at the end of the article and emitted as FAQPage schema.
- Internal links are root-relative with a trailing slash: `/udemy/`.
- External links: plain `<a href="https://…">`. The renderer adds
  `rel="noopener"` and `target="_blank"`.
- Mention **Better Side Hustles** by name 1–3 times, naturally.

### Components (plain HTML with these classes)

```html
<div class="callout"><strong>Quick tip:</strong> …</div>
<div class="callout callout-warn"><strong>Watch out:</strong> …</div>

<div class="stat-row">
  <div class="stat"><b>$18–$30</b><span>typical hourly pay</span></div>
  <div class="stat"><b>$0</b><span>to start</span></div>
  <div class="stat"><b>1 week</b><span>to first payout</span></div>
</div>

<div class="hustle-grid">
  <div class="hustle-card">
    <h3 id="rideshare">Rideshare driving</h3>
    <p>…</p>
    <ul class="meta"><li><b>Pay:</b> $20–$35/hr</li><li><b>Startup:</b> A car</li><li><b>Best for:</b> Evenings</li></ul>
  </div>
</div>

<ol class="steps"><li><strong>Pick one skill.</strong> …</li></ol>

<table class="data"><thead><tr><th>…</th></tr></thead><tbody><tr><td>…</td></tr></tbody></table>
```

### Shortcodes

| Shortcode | Renders |
| --- | --- |
| `[[tool:KEY]]` | An interactive calculator inline in the article |
| `[[gear:key1,key2,key3\|Optional heading]]` | A box of Amazon product cards |
| `[[amazon:key\|anchor text]]` | Inline Amazon link to a catalog item |
| `[[amazon-search:search words\|anchor text]]` | Inline Amazon search link |

Amazon keys live in `data/amazon.php`; every link gets the
`bettersidehustles-20` tag, `rel="sponsored nofollow noopener"` and the page
automatically shows the Associates disclosure.

### Tool keys

| Key | Tool |
| --- | --- |
| `quiz` | Side Hustle Matcher quiz |
| `income-calculator` | Side hustle income & goal calculator |
| `gig-calculator` | Rideshare/delivery true hourly earnings (gas, mileage) |
| `tax-estimator` | Self-employment tax set-aside estimator |
| `course-calculator` | Online course revenue (Udemy / Skillshare / Thinkific) |
| `freelance-rate` | Freelance rate calculator incl. Fiverr's 20% fee |
| `shopify-profit` | Product margin & break-even calculator |
| `affiliate-calculator` | Affiliate commission projector |
