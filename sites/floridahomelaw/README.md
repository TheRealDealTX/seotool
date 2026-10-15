# floridahomelaw.com — Florida Home Law

Plain-English hub on **Florida homeowner law as it applies to property insurance**,
sponsored by The Lawgical Firm, P.A. (Florida property insurance claims). Guides
cite the Florida Statutes they rely on and carry a "Last reviewed" date. The site
deliberately stays inside property-insurance law; HOA, landlord-tenant and real
estate questions are pointed to the Florida Bar Lawyer Referral Service.

**Hosting:** Hostinger Cloud addon website for https://floridahomelaw.com.
`.htaccess` sends www and http:// to https://floridahomelaw.com (one 301), 404s
`/data/`, and routes unknown URLs to `index.php`, which serves `home.html` for `/`,
adds a trailing slash to real page folders, and returns a real 404 with `404.html`.
Preview hostnames get `X-Robots-Tag: noindex`.

## Keyword targets (one per page)

| Path | Primary keyword |
| --- | --- |
| `/` | Florida home law (+ Florida homeowner law, Florida homeowners insurance law, Florida homeowner rights insurance) |
| `/homeowner-claims-bill-of-rights/` | Florida Homeowner Claims Bill of Rights |
| `/homeowners-insurance-claim-process/` | Florida homeowners insurance claim process |
| `/florida-insurance-law-changes-2023/` | Florida insurance law changes 2023 |
| `/citizens-property-insurance-claim/` | Citizens Property Insurance claim |
| `/roof-and-hurricane-insurance-rules/` | Florida roof insurance law / hurricane deductible |
| `/property-insurance-mediation/` | Florida property insurance mediation |
| `/homeowner-insurance-lawyer/` | Florida homeowner insurance lawyer |
| `/free-case-review/`, `/about-the-firm/`, `/disclaimer/`, `/privacy-policy/`, `/sitemap/`, `404.html` | support pages |

## Design

Sand (#f6efe2) background, palm green (#1d5c4d / #113a31) and sea-foam (#dcefe7),
coral accent (#ef7a5f decorative, #b8442b for text/buttons). Lora headings,
Source Sans 3 body. Home: illustrated hero (inline SVG house, palm, shield),
card-grid topic hub, numbered "know your rights" accordion (`<details>`),
claim-clock timeline with a date-of-loss deadline calculator, before/after
reform table, scope note, lawyer checklist + intake form, FAQ. Guides: header
band with breadcrumb and review date, article + sticky table of contents,
numbered step lists, FAQ accordions. Sticky call/review dock on mobile.

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | Page bodies. Line 1 is a JSON header: path, title, description, crumb, group, `article` (adds Article schema), `help` (false hides the CTA strip), `robots`, `sitemap` |
| `src/static/` | Copied verbatim: CSS, JS, favicon, logos, `index.php`, `.htaccess`, `api/` |
| `src/static/api/lead.php` | Free case review form endpoint. Appends to `public_html/data/leads.php` (first line exits; `/data/` also 404s via `.htaccess`). If `public_html/data/lead-config.php` exists on the server it also emails: `<?php if (!defined('FHL_LEAD')) { http_response_code(404); exit; } return ['to' => ['intake@…'], 'from' => 'leads@floridahomelaw.com'];` (never commit it) |
| `build.py` | Wraps pages in the layout, builds JSON-LD (WebSite, LegalService, WebPage, BreadcrumbList, Article, FAQPage parsed from `<details class="qa">`), writes `public/`, `sitemap.xml`, `robots.txt`. `STAGING = False` |
| `validate.py` | One H1 per page; unique titles/descriptions; canonical = origin + path; internal links and anchors resolve; no `href="#"`; valid JSON-LD; homepage keyword placement and count (6–12 in main content); guide length 900–2000 words with FAQ schema and "Last reviewed" |

Shortcodes in page bodies: `{{FORM}}`, `{{PHONE}}`, `{{TEL}}`, `{{FIRM}}`,
`{{FIRM_LEGAL}}`, `{{FIRM_SITE}}`, `{{REVIEWED}}`, `{{SITEMAP}}`.

## Build & deploy

```sh
python3 build.py && python3 validate.py && ../deploy-cloud.sh floridahomelaw
```

When reviewing content, update `REVIEWED` in `build.py` after re-checking the
statutes cited on each guide.
