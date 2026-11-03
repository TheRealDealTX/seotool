# enforceinterest.com — custom HTML/PHP rebuild

A rebuild of [enforceinterest.com](https://enforceinterest.com) — the Rise Public Adjusting site about
Texas prompt-payment (Chapter 542) statutory interest — replacing the WordPress/Elementor install with
static HTML pages behind a small PHP front controller, eleven browser-based calculators and a PHP
contact handler. Hosted on the Hostinger **Agency Growth** plan.

- **Hostinger website UID:** `1WCLLtRIk` (php-fpm 8.3, Phoenix datacenter, order `1008744732`); replaced WordPress website `UXdKlalnO`
- **Search Console:** verified by `static/google9d8d740410b54935.html` (carried over from WordPress)
- **Contact email:** info@enforceinterest.com (Hostinger mailbox; the form sends through it over SMTP)

## Build, check, deploy

```sh
python3 build.py        # writes ./public (pages in ./public/_pages); needs Pillow for share images
python3 validate.py     # links, anchors, assets, titles/descriptions, canonicals, JSON-LD, sitemap,
                        # stale facts, and the homepage "Enforce Interest" count (>= 14)
./deploy.sh [--prune]   # see the header comment for the three upload credentials
```

Local preview: `php -S 127.0.0.1:8000 -t public tools/dev-router.php` (mimics the host's routing).

| Path | What it is |
| --- | --- |
| `lib.py` | Constants (firm, license, email), the **OCCC §304.003 rate table**, shared HTML components |
| `content/home.py` | Homepage |
| `content/guides.py` | Prompt Payment Act pillar, hail/wind, hurricane, fire/smoke, water, post-appraisal, supplements |
| `content/tools.py` | All tool pages (markup + explanatory copy), judgment-rate and prejudgment pages, tools hub |
| `content/posts.py` | Blog posts |
| `content/pages.py` | Qualify quiz, FAQ, about, contact, blog index, legal pages, sitemap, 404 |
| `content/seo.py` | `<title>` / meta description overrides (kept in one place to hold lengths in range) |
| `assets/js/site.js` | Nav, scroll progress, reveal animations, hero accrual meter, scroll-driven 60-day clock, contact form |
| `assets/js/tools.js` | Every calculator (interest engine, Texas business days/holidays, deadlines, quiz, timeline builder) |
| `static/` | `index.php` (front controller + WordPress redirects), `contact.php`, robots, icons, GSC file |
| `backup/wordpress-2026-11-03/` | The old site (see its README; the DB dump and files zip are on the server) |

## Monthly maintenance: the floating rate

§542.060(c) interest = the Finance Code §304.003 rate + 5%. The OCCC publishes next month's rate after the
15th (Texas Credit Letter, <https://occc.texas.gov/publications/interest-rates/>). To update: append the new
monthly value to `OCCC_RATES` in `lib.py`, then build, validate and deploy. Every page, title, calculator
default, chart and table that mentions the current rate updates from that one value. Current data runs
through **November 2026: 7.00% → 12.00%**.

## Pages (36)

**Homepage** — brand/primary keyword "Enforce Interest" (21 uses in body copy) + Texas 60-day rule / 18% interest.

**Kept WordPress URLs** (all had GSC impressions): `/`, `/statutory-damages-calculator/`,
`/post-appraisal-interest-recovery/`, `/long-term-claim-supplements/`, `/hail-wind-claims/`,
`/hurricane-claims/`, `/fire-smoke-damage/`, `/water-plumbing-damage/`, `/does-my-claim-qualify/`, `/faq/`,
`/about-us/`, `/contact/`, `/blog/`, `/blog/18-standard-rate-explained/`, `/blog/act-of-god-floating-rate/`.

**New guides:** `/texas-prompt-payment-act/`, `/texas-judgment-interest-rate/`, `/texas-prejudgment-interest/`
(GSC query "texas prejudgment interest" ranked #4).

**New posts** (several answer GSC queries): Hinojos explained, every claim deadline, how long to file a
freeze claim ("how long do i have to file a freeze claim"), smoke damage claims ("smoke damage
investigations", "smoke claim"), the 542A notice, homeowners cancellation rules ("in texas how long must a
policy be in force").

**Tools (11):** statutory interest calculator (components/supplements, partial payments, shareable link,
CSV, printable memo), claim deadline calculator (business days + Texas holidays, surplus lines, catastrophe,
arson, TWIA), appraisal interest calculator (with shortfall check), qualify quiz, judgment-rate tracker
(chart + full table), prejudgment interest calculator, 542A notice & fee-ratio calculator, claim timeline
builder (localStorage + status-request letter), PA fee calculator, ACV/depreciation calculator, wind/hail
deductible calculator.

## Fact-check corrections versus the WordPress site

- Floating-rate cutoff is the date the **claim was made** (HB 1774 §4(b)), not the date of loss.
- Current floating rate is **12.00%** (Nov 2026 §304.003 = 7.00%), not 11.75%; it is fixed at judgment.
- Chapter 542A pre-suit notice is **61 days**, not 60 (§542A.003).
- Exclusions are in **§542.053**, not §542.052 (which lists covered insurers); reinsurance wasn't listed.
- *Ortiz v. State Farm* held appraisal payment **does** generally bar contract and bad-faith claims (absent
  independent injury); the old site said the opposite. *Barbara Technologies* didn't address document
  requests; the quote attributed to *Hinojos* was removed.
- Added *Rodriguez v. Safeco* (Tex. 2024) on attorney's fees after appraisal; TWIA's separate rules
  (Ch. 2210: 1-year filing, 60-day decision, 10-day payment, prejudgment-interest remedy).
- The "Act of God floating rate" post was about loans and force-majeure clauses; rewritten about §542.060(c).
- Public adjuster fee cap stated precisely: 10% of the settlement (§4102.104).

## Hosting notes

The host serves existing files directly, ignores `.htaccess`, and sends `/` and unknown paths to
`index.php`. Pages live in `public_html/_pages/` (blocked in robots.txt) and every page URL is answered by
`index.php`, which forces `https://enforceinterest.com`, adds trailing slashes, 301s old WordPress URLs
(including `/texas-60-day-rule/`, `/topic/general/`, Yoast sitemaps and old media paths), serves pages with
ETag/Last-Modified, and returns real 404s. Never put an `index.html` or page folders at the root of
`public_html`; `validate.py` checks this.

## Deployment log (2026-11-03)

1. WordPress backed up (see `backup/wordpress-2026-11-03/README.md`); DB dump, files zip and the
   50 form submissions (CSV) are in the new website's `.h5g/` folder (not web-accessible).
2. New php-fpm website `1WCLLtRIk` created and deployed with `./deploy.sh --prune`; verified on its
   temporary domain (all 36 pages 200, redirects, feed, sitemap, 404s, SMTP login and a test form email).
3. enforceinterest.com unlinked from WordPress `UXdKlalnO` and made primary on `1WCLLtRIk`; caches cleared.
4. WordPress website `UXdKlalnO` (and its database) deleted.

The website's storage root is not writable through the File Browser or by PHP, so the SMTP config lives at
`public_html/_private/mail-config.php` and the form log at `public_html/_private/messages.log.php`; both are
PHP files that output nothing (the log returns 404) when requested. `deploy.sh --prune` never touches `_private/`.

`contact.php` validates the form (honeypot, time trap, per-IP rate limit, link/spam filter, PDF/JPG/PNG
attachments up to 5 files / 10 MB), sends it to info@enforceinterest.com over SMTP (smtp.hostinger.com:465)
with a confirmation to the sender, and logs a copy outside the web root. SMTP credentials are read from
`../ei-mail-config.php` (outside `public_html`) or `public_html/_private/mail-config.php` — **never commit
them**. Format:

```php
<?php return ['host' => 'smtp.hostinger.com', 'port' => 465, 'user' => 'info@enforceinterest.com',
              'pass' => '…', 'to' => 'info@enforceinterest.com'];
```
