# deniedclaimlaw.com — Denied Claim Law

Attorney lead-generation site for The Lawgical Firm, P.A. (Florida property
insurance claims law firm, https://thelawgicalfirm.com/), built as a plain-English
legal reference to the Florida law behind denied property insurance claims:
s. 627.70131 insurer timelines, s. 627.70132 notice limits, s. 627.70152 pre-suit
notice, s. 624.155 bad faith / Civil Remedy Notice, appraisal (s. 627.70151),
DFS mediation (s. 627.7015), the 2022–2023 fee reforms (SB 2-A, HB 837) and
contingency representation. Statutes are linked to Online Sunshine
(leg.state.fl.us) via the `{{S:627.70131}}` shortcode. Guides carry
"Last reviewed: October 2026".

Phone: (407) 433-4131 (`+14074334131`). Firm details live in `FIRM` in `build.py`;
the masthead, footer attorney-advertising disclosures, counsel band and lead form
render from it.

**Hosting:** Hostinger Cloud addon website for https://deniedclaimlaw.com.
`.htaccess` + `index.php` send www and http:// to https://deniedclaimlaw.com,
serve `home.html` for `/`, and return real 404s (`404.html`) for unknown URLs.

## Keyword targets (one primary keyword per page)

| Path | Target keyword |
| --- | --- |
| `/` | denied claim law (exact match; 6–10 visible uses enforced by validate.py) |
| `/denied-claim-lawyer-florida/` | denied claim lawyer Florida |
| `/florida-claim-deadlines/` | Florida claim deadlines (includes a date-of-loss calculator) |
| `/pre-suit-notice-florida-property-insurance/` | pre-suit notice Florida property insurance |
| `/insurance-appraisal-florida/` | insurance appraisal Florida |
| `/florida-insurance-bad-faith-law/` | Florida insurance bad faith law |
| `/florida-insurance-attorney-fees/` | Florida insurance attorney fees after HB 837 |
| `/do-i-need-a-lawyer-for-a-denied-insurance-claim/` | do I need a lawyer for a denied insurance claim |
| `/free-case-review/`, `/about-the-firm/`, `/disclaimer/`, `/privacy-policy/`, `/sitemap/`, `/404.html` | support pages |

## Design

Law-library look: deep forest green (#173326 / #21473a), parchment (#f3ecdb) and
paper (#fbf8f0) with brass accents (#c9a356, text-safe #6f531a) and an oxblood
highlight; Libre Baskerville headings, Source Sans 3 body. Components: § seal
wordmark, numbered "volume index" nav, statute citation cards, an insurer-duties
vs policyholder-rights ledger, a Roman-numeral procedural path, and guide pages
with a sticky table of contents built from each `<h2 id>`. Mobile sticky call bar.

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | Page bodies; line 1 is a JSON header (`path`, `kind` home/guide/page, `title`, `description`, `h1`/`dek` for guides, `crumb`, `group`) |
| `src/static/` | Copied verbatim: CSS, JS, favicon, logos, `.htaccess`, `index.php`, `api/` |
| `src/static/api/lead.php` | Free case review form. Appends leads to `public_html/data/leads.php` (first line exits, so it 404s on the web; download via hPanel File Manager). If `public_html/data/lead-config.php` exists on the server it also emails each lead: `<?php if (!defined('DC_LEAD')) { http_response_code(404); exit; } return ['to' => ['intake@…'], 'from' => 'leads@deniedclaimlaw.com'];` (never commit that file) |
| `build.py` | Wraps pages in the layout, builds TOC, schema (WebSite, LegalService, WebPage, BreadcrumbList, Article, FAQPage from `<details class="faq">`) → `public/` + sitemap.xml + robots.txt |
| `validate.py` | One H1, unique titles/descriptions, canonicals, internal links/anchors, no `href="#"`, footer disclosures, banned ad words, guide word counts (900–2000) + FAQ schema + Last reviewed, homepage keyword placement and count |

## Build & deploy

```sh
python3 build.py && python3 validate.py && ../deploy-cloud.sh deniedclaimlaw
```
