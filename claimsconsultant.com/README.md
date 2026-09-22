# claimsconsultant.com

A 57-page static SEO authority site for **Claims Consultant**, a Texas public
insurance adjusting firm working large commercial and institutional property
losses — churches, school districts, cities, campuses, hospitals and
portfolios.

No CMS, no database, no build toolchain beyond Python 3. Upload the contents of
this folder to any web host and it runs.

---

## Before you go live

Everything a human needs to change is in **`siteconfig.py`**, marked `TODO`:

| Key | Current value | Notes |
| --- | --- | --- |
| `phone_display` / `phone_href` | `(512) 555-0100` | **Placeholder.** 555-01xx is the range reserved for fiction — it rings nowhere. Replace with the real tracking number. |
| `email` | `claims@claimsconsultant.com` | Confirm the mailbox exists; the contact form sends here. |
| `legal_name` | `Claims Consultant` | The registered entity name for the footer and schema. |
| `founded` | `2009` | **Placeholder.** Set the real year or delete the key. |
| `license` | *(empty)* | Add e.g. `TDI #1234567`. While empty, the copy reads "licensed under Chapter 4102" with no number — which is accurate but weaker. Add it. |
| `city` / `latitude` / `longitude` | Austin | Change if the office is elsewhere. |

Then rebuild:

```sh
python3 build.py      # regenerates every HTML file
python3 validate.py   # 0 errors, 0 warnings is the passing state
```

**Deliberately not included:** no client names, no testimonials, no case
results, no dollar figures attributed to past settlements, no physical street
address. Everything on the site is either verifiable law, published industry
convention, or a description of method. Add real credentials and results when
you have them and can substantiate them — do not let anyone fill those gaps
with invented numbers.

---

## What's here

| Path | What it is |
| --- | --- |
| `index.html` and the `*/index.html` files | The generated site — this is the deliverable |
| `build.py` | Generator: layout, chrome, schema builders, sitemap, robots, icons |
| `siteconfig.py` | Firm details, statute constants, navigation |
| `content/` | All page copy, written in a small block vocabulary |
| `validate.py` | Post-build checks — run it every time |
| `assets/css/site.css` | The single stylesheet |
| `assets/js/site.js` | The single script: nav, accordions, seven calculators |
| `.htaccess` | HTTPS + non-www canonical, trailing slashes, compression, cache, security headers |
| `sitemap.xml`, `robots.txt`, `site.webmanifest`, `favicon.svg`, `apple-touch-icon.png` | Generated |

### Page inventory — 57 pages

**Homepage** — `texas commercial public adjuster`

**Who we serve** (`/who-we-serve/`) — 9 property types, one hub:
churches & faith organizations · school districts & ISDs · cities &
municipalities · universities & colleges · hospitals & healthcare ·
multifamily & apartments · hotels & hospitality · industrial & manufacturing ·
retail & shopping centers

**Services** (`/services/`) — 9 services, one hub. Five by cause of loss
(commercial property damage, hurricane & windstorm, hail, fire & smoke, water &
freeze), four by claim stage (business interruption, appraisal & disputes,
denied & underpaid, policy review & pre-loss).

**Tools** (`/tools/`) — 7 working calculators, one hub:

| Tool | What it computes |
| --- | --- |
| Commercial claim value estimator | RCV, contents, code work, depreciation, deductible, holdback |
| Business interruption calculator | Gross earnings, continuing expenses, waiting period, extra expense |
| Coinsurance penalty calculator | Required limit, recovery ratio, penalty, net |
| RCV vs ACV depreciation calculator | Effective age, depreciable base, ACV, recoverable depreciation |
| Texas claim deadline calculator | Ch. 542 acknowledgement / accept-reject / payment, 542A pre-suit, limitation |
| Commercial roof replacement estimator | By system, with tear-off, insulation, deck, flashing, curbs, O&P |
| Public adjuster fee calculator | Net recovery, break-even settlement, fee as a share of the improvement |

**Service areas** (`/service-areas/`) — Austin · Houston · Dallas–Fort Worth ·
San Antonio · Corpus Christi & the Coastal Bend · Rio Grande Valley, plus a hub.
Each is written from the perils and policy problems specific to that metro.

**Insights** (`/blog/`) — 8 long-form articles (1,300–1,750 words) plus a hub.

**Firm** — `/about/`, `/how-we-work/`, `/fees/`, `/faq/`, `/glossary/`
(30 terms), `/contact/`.

**Legal** — `/privacy-policy/`, `/terms/`, `/disclaimer/`, `/accessibility/`,
`/sitemap/`, `/404.html`.

---

## SEO

- Unique title (≤65 chars) and meta description (70–175 chars) on every page —
  `validate.py` enforces both and fails the build on duplicates.
- Canonical, Open Graph and Twitter tags throughout.
- One JSON-LD `@graph` per page: `ProfessionalService` + `LocalBusiness`
  organization node, `WebSite`, `BreadcrumbList`, plus `Service`, `FAQPage`,
  `Article`, `WebApplication` or `ItemList` as the page type warrants.
- Breadcrumbs rendered and marked up on every interior page.
- Dense internal linking: hub↔spoke, plus contextual cross-links that rotate
  deterministically so no two pages carry the same related-links block.
- `sitemap.xml` with per-page priority and changefreq; `robots.txt`.
- Trailing-slash directory URLs, 301s to `https://` non-`www` via `.htaccess`.

## Accessibility

Built to WCAG 2.1 AA as a working target: one `h1` and one `main` per page
(enforced by the validator), skip link, visible focus rings, labelled form
controls, captioned tables with `scope`, `prefers-reduced-motion` respected, no
horizontal scroll at 360px, contrast checked in both the light and dark bands.

## The calculators

All seven run entirely client-side. Nothing is transmitted, stored or logged.
Each is a `<form data-calc="name">`; inputs are read by `name` and results
written into every `[data-out="key"]`. The maths lives in one `CALC` table in
`assets/js/site.js` — add a calculator by adding a function there and a page
entry in `content/tools.py`.

## Notes on the copy

Written to be defensible. The statutory references (Tex. Ins. Code ch. 542,
542A, 4102), the coinsurance and O&P conventions, the FEMA duplication-of-
benefits point and the storm references are all real and checkable. Where a
question is legal rather than adjusting, the copy says so and recommends
counsel — deliberately, and it should stay that way.

US spelling throughout.
