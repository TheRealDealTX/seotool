# claimsconsultant.com

A 65-page static SEO authority site for **Claims Consultant**, a Texas
**expert witness and damage consulting** firm working large commercial and
institutional property losses — churches, school districts, cities, campuses, hospitals and
portfolios.

**Positioning:** primarily expert witness and damage consulting. The firm is
*not* a policyholder-side advocate — it is retained by either party
(policyholders, insurers, TPAs, risk pools, brokers and counsel). Expert and
consulting work is billed hourly or fixed fee and is **never contingent**;
public adjusting is the one capacity where a percentage basis may apply, capped
at 10% by §4102.104, and it is disclosed separately. That distinction is
load-bearing: a contingent expert is impeachable on that ground alone. See
`/who-we-work-for/`, `/services/public-adjusting/` and `/disclaimer/`.

**Information architecture** — three axes, deliberately separated:

| Section | Answers |
| --- | --- |
| `/services/` | What we are retained to *do* (9 pages) |
| `/loss-types/` | What we are retained to do it *on* (6 pages) |
| `/who-we-serve/` | *Whose* property it is (9 pages) |

Mixing these back together is the main way this structure degrades. A peril
(hail, fire) is a loss type, not a service.

No CMS, no database, no build toolchain beyond Python 3. Upload the contents of
this folder to any web host and it runs.

---

## Before you go live

Everything a human needs to change is in **`siteconfig.py`**, marked `TODO`:

| Key | Current value | Notes |
| --- | --- | --- |
| `phone_display` / `phone_href` | `(832) 503-5866` | Live. |
| `city` / `latitude` / `longitude` | Houston | Set to Houston to match the area code. Change if the office is elsewhere — local SEO keys off it. |
| `email` | `info@claimsconsultant.com` | Confirm the mailbox exists; the contact form sends here. |
| `legal_name` | `Claims Consultant` | The registered entity name for the footer and schema. |
| `license_ia` | *(empty)* | Texas adjuster licence no. (Tex. Ins. Code ch. 4101). |
| `license_pa` | *(empty)* | Texas public insurance adjuster licence no. (ch. 4102). |
| `credential` | *(empty)* | Optional, e.g. `HAAG certified`. |
| `founded` | *(empty)* | Omitted from the schema while blank, so no invented founding date is published. |

The two licence numbers render automatically in the top bar and the footer via
`license_line()` once filled, and the site reads correctly while they are
blank. Holding both an IA and a PA licence is what the copy relies on to
explain how one firm can be retained by either side — see `/about/` and
`/faq/`.

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

**One thing to confirm with counsel:** the copy describes assessment,
estimating, quantification, appraisal and expert work, and states that the firm
acts in one licensed capacity per matter. Where the line falls between
consulting and licensed adjusting for a given activity is a regulatory
question, not a copywriting one.

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

### Page inventory — 65 pages

**Homepage** — `texas claims consultant` / `commercial property loss consultant`

**Who we serve** (`/who-we-serve/`) — 9 property types, one hub:
churches & faith organizations · school districts & ISDs · cities &
municipalities · universities & colleges · hospitals & healthcare ·
multifamily & apartments · hotels & hospitality · industrial & manufacturing ·
retail & shopping centers

**Services** (`/services/`) — 9 services, one hub: expert witness & litigation
support · causation determinations · construction cost estimating · appraisal &
umpire service · soot, smoke & mold testing and reporting · cabinet
repairability reports · contents itemizing & pricing disputes · public
adjusting · policy review & pre-loss consulting.

**Loss types** (`/loss-types/`) — 6 pages plus a hub: commercial property
damage, hurricane & windstorm, hail, fire & smoke, water & freeze, business
interruption. These were previously under `/services/`; they are causes of
loss, not services.

**Tools** (`/tools/`) — 7 working calculators, one hub:

| Tool | What it computes |
| --- | --- |
| Commercial claim value estimator | RCV, contents, code work, depreciation, deductible, holdback |
| Business interruption calculator | Gross earnings, continuing expenses, waiting period, extra expense |
| Coinsurance penalty calculator | Required limit, recovery ratio, penalty, net |
| RCV vs ACV depreciation calculator | Effective age, depreciable base, ACV, recoverable depreciation |
| Texas claim deadline calculator | Ch. 542 acknowledgement / accept-reject / payment, 542A pre-suit, limitation |
| Commercial roof replacement estimator | By system, with tear-off, insulation, deck, flashing, curbs, O&P |
| Overhead, profit & general conditions | O&P, general conditions, occupied-building premium, bond, and the three-trade test |

**Service areas** (`/service-areas/`) — Austin · Houston · Dallas–Fort Worth ·
San Antonio · Corpus Christi & the Coastal Bend · Rio Grande Valley, plus a hub.
Each is written from the perils and policy problems specific to that metro.

**Insights** (`/blog/`) — 8 long-form articles (1,300–1,750 words) plus a hub.

**Firm** — `/about/`, `/who-we-work-for/`, `/how-we-work/`, `/fees/`, `/faq/`,
`/glossary/` (33 terms), `/contact/`.

Two pages were retired in the restructure: `/services/denied-and-underpaid-
claims/` (covered by expert witness, appraisal and cost estimating) and the old
`/services/appraisal-and-claim-disputes/` (now `/services/insurance-appraisal/`).
Nothing was ever published at those URLs, so no redirects were added.

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

Written to be defensible, and written neutrally. The statutory references
(Tex. Ins. Code ch. 542, 542A, 4101, 4102), the coinsurance and O&P
conventions, the FEMA duplication-of-benefits point and the storm references
are all real and checkable. Where a question is legal rather than technical,
the copy says so and recommends counsel — deliberately, and it should stay
that way.

The copy never assumes the reader is the policyholder. Tables that set out
competing positions give both, and the claim throughout is that the analysis
does not change with the client. That is the firm's whole differentiator, so
edits should preserve it.

US spelling throughout.
