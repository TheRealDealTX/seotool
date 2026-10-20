# roofestimatepro.com — static rebuild

A static rebuild of [roofestimatepro.com](https://roofestimatepro.com) as a **free roof-estimating tools site**
that also sells professional estimates. It replaces the WordPress/Elementor site: no database, no plugins, just HTML,
one stylesheet, a small JS engine for the calculators and a PHP form handler.

Texas is the primary market (every region of the state); the tools and copy also cover other U.S. states.

## What's here

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, schema, page builders, `sitemap.xml`, `robots.txt`, `index.php` (front controller + 301s) |
| `siteconfig.py` | Business details, tool registry, services, Texas/U.S. regions, steep-slope unit prices and waste factors |
| `content/home.py` | Homepage |
| `content/tools/*.py` | One module per calculator: meta, form (built with `content/ui.py`), explainer article, FAQs |
| `content/services.py`, `content/pages.py` | Services hub + 4 service pages; about, how-it-works, FAQs, areas, legal |
| `content/blog/*.py` | Blog posts, one module each, at their original WordPress URLs |
| `static/` | Copied into the build as-is: CSS, JS, fonts, images, favicons, `api/contact.php`, legacy `wp-content/uploads/` |
| `static/assets/js/tools-core.js` | Calculator engine: live results, saved inputs, share links, print sheet, estimator hand-off |
| `static/assets/js/tools/<slug>.js` | Each calculator's math |
| `validate.py` | Post-build checks (run after every build) |
| `serve.py` | Local preview that mimics the host (`/` → `home.html`, real 404s) |
| `deploy.sh` | Upload `public/` to the Hostinger website |

`public/` is the build output and is not committed.

## Building

```sh
python3 build.py              # production build (indexable)
python3 build.py --staging    # temporary domain: noindex everywhere + robots.txt Disallow: /
python3 validate.py
python3 serve.py 8000         # preview at http://localhost:8000
```

Python 3 standard library only.

## The tools

Twelve calculators under `/tools/`: replacement cost, square footage, pitch, shingle materials, metal roof, flat &
commercial roof, insurance claim, depreciation, repair cost, gutters, attic ventilation, bid & profit. Every one:

- recalculates live, with every unit price editable in an *Edit unit prices* panel (Texas 2026 defaults);
- saves inputs in the visitor's browser and can **copy a share link** that reopens the same estimate;
- prints a clean **estimate sheet** (Print / Save as PDF);
- has a **"Have a pro estimator review this"** button that carries the results into the `/get-estimate/` form.

Steep-slope material prices live in `siteconfig.MATERIALS` and regional labor factors in `TEXAS_REGIONS`/`US_REGIONS`;
`build.py` writes them to `assets/js/data.js` so the calculators and the homepage quick estimate share one source.

To add a tool: add it to `siteconfig.TOOLS`, create `content/tools/<slug_with_underscores>.py` exporting `TOOL`
(see the replacement-cost module, which is documented as the reference), and `static/assets/js/tools/<slug>.js`
calling `REP.tool({...})` (the result format is documented at the top of `tools-core.js`).

## Forms

`/get-estimate/`, `/claim/` ($50 claim estimate review) and `/get-a-scope/` ($200 scope) post to `/api/contact.php`,
which emails the submission with attachments (photos, PDF, ESX, XLSX, ZIP, 20 MB total) to `contact@roofestimatepro.com`,
keeps a copy outside the web root, and has a honeypot, a minimum fill time and a per-IP rate limit.

**To take payment online**, create two Stripe Payment Links and paste them into `STRIPE_CLAIM` and `STRIPE_SCOPE` at
the top of `static/api/contact.php`; visitors are then sent to checkout after submitting. Until then the success
message says a secure payment link will follow.

## SEO

- Unique title/description, one H1, canonical (always `https://roofestimatepro.com/...`), Open Graph and JSON-LD on every
  page: `ProfessionalService` organization (areaServed Texas + United States), `WebApplication` + `FAQPage` on tools,
  `Service` on service pages, `BlogPosting` on posts, `BreadcrumbList` everywhere.
- The 288 thin city pages (`/areas/<city>-roof-estimates-services/` and `/helotes-roof-estimates-services/`) are gone and
  **301 to `/areas/`** via `index.php`; the category archive, feeds, old sitemap files and WordPress paths redirect too.
- Blog posts keep their original URLs and publish dates; the content was rewritten around estimating and the tools.
- Old media URLs under `/wp-content/uploads/` still resolve (files are kept in `static/wp-content/uploads/`).

## Hosting

Hostinger Agency plan, plain php-fpm website (no WordPress). The platform serves existing files directly, ignores
`.htaccess`, and sends `/` and unknown paths to `index.php` — unless an `index.html` exists at the root, so the
homepage is built as `home.html` and served by `index.php`. `index.php` also does the 301s and returns `404.html`
with a real 404 status. Canonical host/HTTPS redirects only fire when the request is for roofestimatepro.com, so the
site also works on its temporary `*.hostingersite.com` domain.

- Website UID `tZQpRue3o`, temporary domain **https://cyan-goose-654464.hostingersite.com/** (staging build: noindex).

### Going live on roofestimatepro.com

1. Connect `roofestimatepro.com` to website `tZQpRue3o` in hPanel (Domains → Connect domain), or point the domain's
   DNS at it. Remove it from the old WordPress hosting.
2. `python3 build.py && python3 validate.py && ./deploy.sh` — the **production** build (without `--staging`) removes
   the noindex tags and the blocking `robots.txt`.
3. Clear the site cache. In Google Search Console, submit `https://roofestimatepro.com/sitemap.xml` and upload the
   disavow file.
4. Set up the `contact@roofestimatepro.com` mailbox (or change `TO_EMAIL` in `api/contact.php`) and send a test form.
