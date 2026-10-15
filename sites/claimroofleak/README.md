# claimroofleak.com — Claim Roof Leak

Lead-generation and information site for **The Lawgical Firm, P.A.** (Florida
property insurance claims law firm, https://thelawgicalfirm.com/). It explains
how a Florida **roof leak claim** works — coverage, Florida roof statutes,
interior water damage and mold, contractor/AOB limits, and what to do when the
claim is denied or underpaid — and routes visitors to a free case review.
Phone on the site: (407) 433-4131.

Hosting: Hostinger Cloud addon website (claimroofleak.com). Canonical host is
`https://claimroofleak.com`; `.htaccess` + `index.php` send www/http to the apex,
serve `home.html` for `/`, and return a real 404 (`404.html`) for unknown URLs.

## Keyword targets (one primary keyword per page)

| Path | Primary keyword |
| --- | --- |
| `/` | roof leak claim (exact match; title front, H1, first paragraph, H2, meta description, 6–10 visible uses — checked by `validate.py`) |
| `/is-a-roof-leak-covered-by-homeowners-insurance-florida/` | is a roof leak covered by homeowners insurance Florida |
| `/roof-leak-insurance-claim-florida/` | roof leak insurance claim Florida |
| `/roof-leak-claim-denied/` | roof leak claim denied |
| `/roof-damage-insurance-claim-florida/` | roof damage insurance claim Florida |
| `/wear-and-tear-roof-denial/` | wear and tear roof denial |
| `/florida-25-percent-roof-rule/` | Florida 25% roof rule |
| `/roof-leak-water-damage-mold-claim/` | roof leak water damage and mold claim |
| `/free-case-review/`, `/about-the-firm/`, `/disclaimer/`, `/privacy-policy/`, `/sitemap/`, `404.html` | support pages |

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | Page bodies. Line 1 is a JSON header: `path`, `title`, `description`, `crumb`, `group`, `nav`; guides add `kind: "guide"`, `h1`, `kicker`, `lede`. |
| `src/static/` | Copied verbatim: `assets/roof.css`, `assets/roof.js`, logos, `favicon.svg`, `index.php`, `.htaccess`, `api/` |
| `src/static/api/lead.php` | Case review form endpoint. Appends to `public_html/data/leads.php` (first line exits, so it 404s on the web). If `public_html/data/lead-config.php` exists on the server (never commit it), leads are also emailed — see the header comment in `lead.php`. |
| `build.py` | Wraps pages in the shared layout (header, breadcrumbs, guide shell with auto "On this page" list, footer disclosures, mobile call dock), builds JSON-LD (WebSite, LegalService, WebPage, BreadcrumbList, Article on guides, FAQPage from `<details class="qa">`), writes `public/`, `sitemap.xml`, `robots.txt`. `STAGING = False`. |
| `validate.py` | One H1, unique title/description, canonical = origin + path, internal links/anchors resolve, no `href="#"`, footer disclosures present, banned ad words, guide length 900–2000 words + FAQ/Article schema + "Last reviewed", homepage keyword placement/count. |

Shortcodes in pages: `{{PHONE}}`, `{{TEL}}`, `{{FIRM}}`, `{{LEGAL}}`, `{{FIRM_SITE}}`, `{{FIRM_ROOF}}`, `{{REVIEWED}}`, `{{FORM}}` (lead form), `{{SITEMAP}}`.

Design: clay/terracotta (#a5482a), slate (#2e3a46) and sky blue (#2f86c4 / #7cc4ee) on a warm sand background; Nunito headings with Plus Jakarta Sans body; roofline SVG hero with dripping-leak illustration, an interactive "covered or not?" helper (runs in the browser only), numbered checklist cards, a slate "Florida rules" ladder, and an eave-edged guide header with a sticky table of contents.

Legal content was checked against the 2026 Florida Statutes (ss. 95.11, 489.147, 553.844, 624.155, 626.9744, 627.701, 627.7011, 627.70131, 627.70132, 627.70152, 627.7015, 627.7142, 627.7152). Re-review guides when the Legislature amends these sections and update `REVIEWED` in `build.py`.

## Build & deploy

```sh
python3 build.py && python3 validate.py && ../deploy-cloud.sh claimroofleak
```
