# deniedfloodclaim.com — Denied Flood Claim (Florida)

Lead-generation and information site for **The Lawgical Firm, P.A.** (Florida
property insurance claims law firm, https://thelawgicalfirm.com/). It explains
what Florida property owners can do after a flood insurance claim is denied or
underpaid: NFIP Standard Flood Insurance Policy rules (60-day proof of loss,
60-day FEMA appeal under 44 CFR 62.20, one-year federal suit limit under SFIP
VII.O / 42 U.S.C. 4072, coverage limits and exclusions), private flood
policies under Florida law (s. 627.715 and the claim statutes), and wind vs.
water disputes after hurricanes.

**Scope note:** the firm's website (checked 2026-10-15) lists residential and
commercial property insurance claims (hurricane/windstorm, water damage, roof,
mold, plumbing, sinkhole, fire, hail, theft, construction defect) but **not**
NFIP flood claims. The site therefore never claims NFIP representation; it
frames the firm's role around the homeowners/windstorm side of wind-vs-flood
disputes and invites a free case review to see whether a given claim fits.
Fee wording mirrors the firm's own: "No upfront fees" / no fee unless there is
a recovery.

Phone: (407) 433-4131 (`+14074334131`). Firm details live in `FIRM` in `build.py`.

## Keyword targets (one primary per page)

| Path | Primary keyword |
| --- | --- |
| `/` | denied flood claim (exact match; also "flood insurance claim denied Florida") |
| `/nfip-claim-denied/` | NFIP claim denied |
| `/flood-insurance-appeal-fema/` | flood insurance appeal FEMA |
| `/flood-proof-of-loss-deadline/` | flood proof of loss deadline |
| `/what-nfip-flood-insurance-covers/` | what NFIP flood insurance covers |
| `/wind-vs-flood-damage-claim/` | wind vs flood damage claim |
| `/private-flood-insurance-claim-denied-florida/` | private flood insurance claim denied Florida |
| `/flood-claim-underpaid/` | flood claim underpaid |
| `/free-case-review/`, `/about-the-firm/`, `/disclaimer/`, `/privacy-policy/`, `/sitemap/`, `/404.html` | utility pages |

## Design

Calm water / data look: deep teal-to-slate gradients (`#0b2a35`, `#0e4f5c`,
`#1d3b52`), bright aqua accent (`#35e0d0`), warning amber (`#f5a524`) reserved
for deadlines. Sora headings, Public Sans body (Google Fonts). Contour-line
SVG hero, wave dividers, a 5-step deadline timeline component (horizontal on
desktop, vertical on mobile), a client-side NFIP date calculator, sticky
in-page table of contents on guides, mobile call/review dock.

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | Page bodies; line 1 is a JSON header (path, title, description, crumb, article, group, band) |
| `src/static/` | Copied verbatim: `index.php` front controller, `.htaccess`, `favicon.svg`, CSS, JS, logos, `api/` |
| `src/static/api/lead.php` | Free case review endpoint. Appends to `public_html/data/leads.php` (first line exits → 404 on the web) and, if `public_html/data/lead-config.php` exists on the server (never committed), emails the lead |
| `build.py` | Wraps pages in the shared layout; adds TOC, FAQPage/Article/Breadcrumb/LegalService schema; writes `public/`, `sitemap.xml`, `robots.txt` |
| `validate.py` | One H1, unique title/description, canonicals, internal links/anchors, no `href="#"`, banned ad words, guide word counts 900–2000 + FAQ schema, homepage keyword placement and count (6–10) |

Shortcodes in pages: `{{LEAD_FORM}}`, `{{TOC}}`, `{{REVIEWED_LINE}}`, `{{PHONE}}`, `{{TEL}}`, `{{FIRM_LEGAL}}`, `{{FIRM_SITE}}`, `{{SITEMAP}}`.

## Build & deploy

Hostinger Cloud addon website (deniedfloodclaim.com).

```sh
python3 build.py && python3 validate.py && ../deploy-cloud.sh deniedfloodclaim
```

`deploy-cloud.sh` needs `FB_URL`, `FB_AUTH`, `FB_REST` from `hosting_files_generate-upload-url` for the domain.
Legal content last reviewed October 2026; re-check FEMA bulletins and Florida statutes each hurricane season.
