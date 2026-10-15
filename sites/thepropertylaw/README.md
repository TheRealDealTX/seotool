# thepropertylaw.com — The Property Law

A structured legal-information resource on **Florida property insurance law** for
homeowners, condo owners and small commercial property owners, sponsored by
The Lawgical Firm, P.A. (lead generation for its Florida property insurance
claims practice). Phone on the site: (407) 433-4131 (`+14074334131`).

**Hosting:** Hostinger Cloud addon website for thepropertylaw.com. DNS was not
yet pointed at Hostinger when the site was built. `.htaccess` + `index.php`
send www and http:// to `https://thepropertylaw.com`, serve `home.html` for `/`
and return a real 404 (`404.html`) for unknown URLs; previews on
`*.hostingersite.com` get `X-Robots-Tag: noindex`.

## Keyword targets (one primary keyword per page)

| Page | Primary keyword |
| --- | --- |
| `/` | property law (exact match; 6-10 visible uses, enforced by `validate.py`) |
| `/florida-property-insurance-law/` | Florida property insurance law |
| `/property-insurance-lawyer-florida/` | property insurance lawyer Florida |
| `/property-damage-claim/` | property damage claim |
| `/insurance-policy-exclusions/` | insurance policy exclusions explained |
| `/sinkhole-claim-florida/` | sinkhole claim Florida |
| `/fire-damage-insurance-claim-florida/` | fire damage insurance claim Florida |
| `/commercial-property-insurance-claim/` | commercial property insurance claim (the firm lists commercial claims) |

Support pages: `/free-case-review/`, `/about-the-firm/`, `/disclaimer/`,
`/privacy-policy/`, `/sitemap/`, `404.html`.

Legal content cites the 2026 Florida Statutes (ss. 627.70131, 627.70132,
627.7015, 627.70152, 624.155, 624.1551, 627.706, 627.707, 627.7074, 627.701,
627.7011, 627.702, 627.7152, 95.11) and shows "Last reviewed: October 2026".
Change `REVIEWED`/`MODIFIED` in `build.py` after the next review.

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | Page bodies. Line 1 is a JSON header: `path`, `kind` (`guide`/`page`/`home`), `title`, `description`, and for guides `h1`, `lede`, `keyword`, `crumb`, `cites`, `related` |
| `src/static/` | Copied verbatim: `index.php`, `.htaccess`, `favicon.svg`, `assets/` (CSS, JS, firm logo), `api/` |
| `src/static/api/lead.php` | Free case review endpoint. Appends to `public_html/data/leads.php` (404 on the web); emails too if `public_html/data/lead-config.php` exists on the server (see header comment; never commit it) |
| `build.py` | Wraps pages in the layout. Guides get a hero, sticky table of contents built from `<h2 id>`, Article + FAQPage schema (FAQs parsed from `<details class="faq">`) and related links. Writes `public/`, `sitemap.xml`, `robots.txt` |
| `validate.py` | One H1, unique title/description, canonical URLs, internal links and anchors, no `href="#"`, guide word counts (900-2000) + FAQ schema, homepage keyword placement and count, Florida Bar barred words, footer disclosures |

Design: near-white (`#fafafb`) with graphite text (`#1c1e22`) and one
indigo-violet accent (`#5b3fd9`), Inter throughout, hairline rules and a faint
44px grid on hero areas; the home page is a filterable A-Z glossary index.

## Build & deploy

```sh
python3 build.py && python3 validate.py && ../deploy-cloud.sh thepropertylaw
```
