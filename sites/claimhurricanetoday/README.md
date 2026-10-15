# claimhurricanetoday.com

Lead-generation and information site for **The Lawgical Firm, P.A.** (Florida property
insurance claims law firm). Angle: an urgent "file your hurricane claim today" guide for
Florida homeowners, with a notice-deadline countdown calculator (s. 627.70132) and a
progress checklist. Hosted as an addon website on the Hostinger Cloud plan.

- Live origin: https://claimhurricanetoday.com (apex is canonical; www and http 301 to it)
- Phone on site: (407) 433-4131 (`+14074334131`)
- `STAGING = False` in `build.py` (pages indexable). Set `True` to noindex everything.

## Keyword targets (one primary per page)

| Page | Primary keyword |
|---|---|
| `/` | hurricane claim (exact match; also "claim hurricane today", "file a hurricane claim") |
| `/how-to-file-a-hurricane-claim/` | how to file a hurricane claim (+ "how to file a hurricane insurance claim Florida") |
| `/hurricane-claim-deadline-florida/` | hurricane claim deadline Florida (calculator) |
| `/hurricane-claim-checklist/` | hurricane claim checklist (interactive) |
| `/hurricane-claim-delayed/` | hurricane claim delayed |
| `/hurricane-claim-underpaid/` | hurricane claim underpaid |
| `/hurricane-claim-denied/` | hurricane claim denied |
| `/hurricane-deductible-florida/` | hurricane deductible Florida |
| `/additional-living-expenses-hurricane-claim/` | additional living expenses hurricane claim |
| `/free-case-review/`, `/about-the-firm/`, `/disclaimer/`, `/privacy-policy/`, `/sitemap/`, `/404.html` | utility pages |

## Layout

```
build.py            stdlib-only generator: src/ -> public/
validate.py         post-build checks (H1, title/description unique, canonicals,
                    internal links + anchors, no href="#", keyword placement and
                    homepage count 6-10, guide word counts 900-2000, FAQPage schema)
src/pages/*.html    page bodies; line 1 is a JSON header comment (path, kind, title,
                    description, h1, lede, crumb, ...). kind=home|guide|page.
                    FAQ schema is generated from <details><summary>..</summary><div>..</div></details>.
                    Shortcodes: {{LEAD_FORM}} {{CALC}} {{PHONE}} {{TEL}} {{FIRM_SITE}} {{FIRM_PRACTICE}} {{SITEMAP}}
src/static/         copied as-is: index.php (front controller, real 404s), .htaccess,
                    api/lead.php + api/_lib.php (lead endpoint), assets/, favicon.svg
```

Leads are appended to `data/leads.php` next to `api/` (first line exits; `.htaccess`
also 404s `/data`). To email leads, create `data/lead-config.php` on the server only
(see the header comment in `api/lead.php`).

Design: white canvas, safety orange (`#c2410c` / `#ea580c`) and deep navy (`#0a1a33`),
Archivo (wide, 800-900) headings with Public Sans body, hazard-stripe accents, a navy
countdown calculator card, numbered step rails, statute "rule cards", sticky mobile
call bar. Vanilla JS only (`assets/js/main.js`); localStorage use is wrapped in try/catch.

## Build and deploy

```
python3 build.py && python3 validate.py && ../deploy-cloud.sh claimhurricanetoday
```

Legal content was last reviewed October 2026 against the Florida Statutes
(ss. 627.70131, 627.70132, 627.701, 627.4025, 627.7011, 627.7015, 627.70152,
627.7142, 627.7152, 626.854, 626.9744, 624.155, 95.11). Re-check after each
legislative session.
