# Content guide — landscapelightingtexas.com

How page and post content files are written. Read this before adding or editing
a page.

## How a page is rendered

`index.php` looks up the URL in `inc/registry.php`, which gives the page's
`title`, `h1`, `description`, `image` and the content `file`. The content file
is `include`d **inside** `render_page()`, so it can read and set keys on `$P`
before any HTML is sent. Whatever it echoes becomes the page body.

- **Pages** (`pages/…`, types page/service/area/tool): the layout prints the
  header, then a hero (breadcrumbs, `$P['eyebrow']`, the H1 from the registry,
  `$P['lead']`, and Quote/Call buttons), then your body, then the footer. Your
  body is a series of full-width `<section>`s. Do not print an `<h1>`.
- **Posts** (`posts/…`): the layout prints the post hero (H1, date, reading
  time), a sticky table of contents built from your `<h2>`s, and wraps your
  body in `.prose`. Your body is plain article HTML: `<p>`, `<h2>`, `<h3>`,
  `<ul>`, `<ol>`, tables, plus the helpers below. No `<section>` wrappers, no
  `<h1>`. Related posts and a CTA are appended automatically.

Every file starts with:

```php
<?php defined('LLT') or exit;
$P['eyebrow'] = 'Short label above the H1';          // pages only
$P['lead'] = 'One or two sentences under the H1.';   // pages only, HTML allowed
// $P['tools_js'] = true;   // only if the page embeds an interactive widget
?>
```

## Helpers (inc/components.php)

All echo directly unless marked "returns".

| Helper | Use |
| --- | --- |
| `section_head($eyebrow, $titleHtml, $leadHtml = '', $align = 'center'\|'left')` | Section heading (renders an `<h2>`) |
| `faqs([[q, answerHtml], …], $title = 'Frequently Asked Questions')` | Accordion section **and** FAQPage schema. Put it near the end of a page as its own top-level call (it prints its own `<section>`). In posts, don't call it — write a normal `<h2>FAQ</h2>` with `<h3>` questions instead. |
| `cta_band($titleHtml = default, $text = default)` | Full-width photo CTA. End every page with it (posts get one automatically). |
| `service_cards($excludeSlug = '', $limit = 99)` | Grid of service cards with photos |
| `area_cards($excludeSlug = '')` | Grid of region cards |
| `tool_cards($excludeHref = '')` | Grid of interactive tool cards |
| `related_posts($excludePath = '', $n = 3, $title)` | Prints its own section |
| `stats([[number, suffix, label], …])` | Animated counters, e.g. `[['1400','+','Projects completed']]` |
| `split($imgKey, $alt, $html, $reverse = false)` | Photo + text, two columns |
| `before_after($imgKey, $alt)` | Drag slider: unlit vs lit |
| `testimonials()` | Review carousel (the business's real reviews) |
| `quote_form($heading, $sourceLabel)` | The quote form |
| `checklist([html, …])` | returns `<ul>` with gold check icons |
| `figure($imgKey, $alt, $captionHtml = '')` | returns a figure (use in posts) |
| `callout($html, 'tip'\|'note'\|'warn', $title = '')` | returns an aside box (use in posts) |
| `tool_promo($href)` | returns an inline link card to one of the tools, `$href` is a key of `$TOOLS` in `inc/config.php` |
| `icon($name, $size)` | returns an inline SVG; names in `components.php` |
| `e($text)` | HTML-escape |

**Image keys** (all real night photos, 3:2): `architectural-uplighting`,
`oak-tree-uplighting`, `garden-pathway-lighting`, `driveway-lighting`,
`pool-lighting`, `patio-lighting`, `landscape-lighting-texas-home`,
`cost-calculator`. Use `img_url($key, 800|1600)` if you need a raw URL.

**Constants**: `SITE_NAME`, `PHONE`, `PHONE_HREF`, `EMAIL`, `HOURS`.
**Arrays**: `$SERVICES`, `$AREAS`, `$TOOLS` (see `inc/config.php`).
Inside a content file, globals are not automatically in scope — use
`global $AREAS;` first if you need one.

## Layout classes (assets/css/site.css)

```html
<section class="section">            <!-- standard vertical rhythm -->
<section class="section alt">        <!-- slightly lighter night-blue band -->
  <div class="container">            <!-- max width 1240px -->
  <div class="container narrow">     <!-- max width 820px, for reading -->
    <div class="prose">…</div>       <!-- long-form typography for p/h2/h3/ul/ol/table -->
    <div class="grid-2">…</div>      <!-- two columns, stacks on mobile -->
    <div class="grid-3">…</div>      <!-- three columns -->
    <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('bulb') ?></span><h3>…</h3><p>…</p></div>
    <ol class="steps"><li><h3>…</h3><p>…</p></li>…</ol>   <!-- numbered timeline -->
    <ul class="pill-list"><li>Austin</li>…</ul>           <!-- city/tag chips -->
    <div class="table-wrap"><table>…</table></div>        <!-- responsive table -->
    <p class="lead-p">…</p>                               <!-- larger intro paragraph -->
    <span class="highlight">…</span>                      <!-- gold emphasis -->
```

Add `reveal` to any block that should fade up on scroll (cards, figures,
headings); the helpers already do this.

## Writing rules

- US spelling. Confident, specific, warm; written for Texas homeowners.
  No filler ("in today's world", "look no further"), no exclamation marks.
- Use real lighting knowledge: color temperature (2700K/3000K), beam angles,
  lumens, low-voltage 12V systems, transformers, multi-tap, 12/10-gauge wire,
  voltage drop, hub wiring, brass/copper fixtures, IP ratings, astronomical
  timers, glare control, dark-sky practice, live oaks, crape myrtles, palms,
  limestone, Austin stone, brick. Texas specifics: heat, hail, humidity,
  coastal salt, caliche/clay soil, HOA rules, long outdoor-living season.
- Never invent facts about the business beyond what it already states:
  1,400+ projects, 5+ years, 4.9★ average rating, 5-year workmanship warranty,
  licensed & insured, free consultations/estimates, statewide service, phone
  `+1 (281) 704-7210`, email `info@landscapelightingtexas.com`,
  Mon–Fri 8am–6pm CT. Do not invent street addresses, staff names, license
  numbers, awards, or customer names/reviews.
- Prices are planning ranges, stated as such. Typical residential projects run
  $2,500–$12,000; starter $2,500–$5,000; estates can exceed $20,000; roughly
  $250–$450 per installed fixture professionally. LEDs use ~75–80% less energy
  than halogen; a whole-property LED system typically costs $10–$25/month to run.
- Mention the brand "Landscape Lighting Texas" naturally 2–4 times per page.
- Link internally where useful: services `/services/<slug>/`, areas
  `/areas/<slug>/`, tools (keys of `$TOOLS`), posts (paths in the registry),
  `/quote/`, `/gallery/`, `/faq/`.
- Every page must be valid PHP: run `php -l <file>` and render it with
  `php tests/render.php /path/` (prints the page or the error).
