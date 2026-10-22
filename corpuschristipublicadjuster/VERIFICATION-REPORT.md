# Verification report — CorpusChristiPublicAdjuster.com rebuild

Checked 2026-10-22 against the local PHP 8.3 dev server (`tools/test/serve.sh`).

## Results

| Check | Result |
|---|---|
| `python3 tools/test/crawl.py` — 71 HTML pages, 172 internal link targets: status 200, one H1, unique titles/descriptions, canonical, JSON-LD parses, img alt, no PHP warnings, only approved email addresses | **No problems found** |
| Homepage visible-text count of "Corpus Christi Public Adjuster" (requirement: at least 14) | **28** (22 in the main content, the rest in header/footer) |
| Original WordPress URLs (7 articles, 6 pages, `/blog/`) return 200 | **Pass** |
| Legacy archive/sitemap/author/shortlink URLs return 301 to the right target | **Pass** |
| `node tools/test/functional.js` — popup timing (opens after 5 s, Escape/dismiss, not on contact), popup + page form submission over SMTP, calculator math, checklist, storm history + lookup, mobile nav, no JS errors | **29/29 pass** |
| Form mail captured by a local SMTP sink | `To: info@corpuschristipublicadjuster.com` |
| Hurricane deductible + claim deadline calculators (browser) | Correct values; deadlines match Tex. Ins. Code §§542.055–.057, 2210.573–.577 |
| Desktop (1366px) + phone (390px) screenshots of 10 key pages | No horizontal overflow, no console errors |

## Preserved URLs

Pages: `/`, `/about-us/`, `/services/`, `/blog/`, `/contact/`, `/privacy-policy/`, `/terms-of-use/`.
All 207 files the old site served from `/wp-content/uploads/` are kept at the same paths.

301 redirects: `/category/general/` → `/blog/`; `/author/infohoustonpublicadjusting-com/` → `/author/joseph-dittman/`;
`/sitemap_index.xml`, `/post-sitemap.xml`, `/page-sitemap.xml`, `/category-sitemap.xml`, `/wp-sitemap.xml` → `/sitemap.xml`;
`/?p=` and `/?page_id=` shortlinks for every original post and page; `http://` and `www.` → `https://corpuschristipublicadjuster.com`.

## Content

* 21 articles (7 rewritten at their original URLs + 14 new), about 36,000 words, all by Joseph Dittman, Licensed Public Adjuster.
* 19 claim service pages (about 20,000 words), including new TWIA windstorm, flood, and mold pages.
* 31 pages: home, about, contact, free claim review, FAQ (24 Q&As), author, services hub, blog, sitemap, privacy, terms,
  local building codes, hurricane season guide, service areas hub + 8 area pages (Portland, Rockport, Port Aransas,
  Aransas Pass, Ingleside, Padre Island, Robstown, Kingsville), weather, weather events, storm history, storm lookup,
  claim tools, settlement calculator, documentation checklist, hurricane deductible calculator, claim deadline calculator.
* Facts come only from `tools/notes/local-facts.md` (sourced, verified 2026-10-22) and `tools/notes/storm-facts.md` (NOAA NCEI).

### Articles

| URL | Title |
|---|---|
| `/water-damage-vs-flood-damage-corpus-christi/` | Water Damage vs. Flood Damage in Corpus Christi: What’s Covered |
| `/wind-damage-insurance-claims-corpus-christi-tx/` | Wind Damage Insurance Claims in Corpus Christi, TX |
| `/windstorm-certificate-wpi-8-insurance-claims/` | Windstorm Certificates (WPI-8) and Insurance Claim Repairs |
| `/named-storm-hurricane-deductibles-texas/` | Named-Storm and Hurricane Deductibles in Texas, Explained |
| `/wind-vs-storm-surge-damage-claims-texas-coast/` | Wind vs. Storm Surge Damage Claims on the Texas Coast |
| `/twia-claim-process-corpus-christi/` | The TWIA Claim Process in Corpus Christi, Step by Step |
| `/hurricane-damage-claims-corpus-christi-guide/` | Corpus Christi Hurricane Damage Claims: A Homeowner’s Guide |
| `/corpus-christi-storm-history-hail-wind-hurricanes/` | Corpus Christi Storm History: Hail, Wind, Tornadoes, and Hurricanes |
| `/noaa-weather-records-document-property-damage-corpus-christi/` | Using NOAA Weather Records to Document Property Damage in Corpus Christi |
| `/freeze-damage-burst-pipe-claims-corpus-christi/` | Freeze Damage and Burst Pipe Insurance Claims in Corpus Christi |
| `/document-commercial-property-damage-after-storm/` | How to Document Commercial Property Damage After a Storm |
| `/how-to-review-underpaid-roof-insurance-estimate/` | How to Review an Underpaid Roof Insurance Estimate |
| `/why-property-insurance-claims-are-delayed-texas/` | Why Property Insurance Claims Are Delayed in Texas (and What to Do) |
| `/replacement-cost-vs-actual-cash-value-texas/` | Replacement Cost vs. Actual Cash Value in Texas Property Claims |
| `/fire-insurance-adjuster/` | Fire Insurance Adjuster: What They Do and How They Help in Corpus Christi |
| `/public-adjuster-vs-insurance-adjuster-for-hail-claims-in-texas/` | Public Adjuster vs. Insurance Adjuster for Hail Claims in Texas |
| `/document-hail-damage-for-an-insurance-claim/` | How to Document Hail Damage for an Insurance Claim in Corpus Christi |
| `/hail-claim-was-denied-in-texas/` | What to Do If Your Hail Claim Was Denied in Texas |
| `/hail-damage-claim-supplements-what-carriers-miss-in-their-scope/` | Hail Damage Claim Supplements: What Carriers Miss in Their Scope |
| `/hail-damage-roof-insurance-claim/` | Hail Damage Roof Insurance Claim: A Corpus Christi Homeowner’s Guide |
| `/questions-about-public-adjusters/` | Top Questions About Public Adjusters: What Corpus Christi Property Owners Need to Know |

## Email

* Every form (homepage hero + section, contact, free claim review, 5-second popup) → **info@corpuschristipublicadjuster.com**.
* Joseph Dittman's direct address **jditt@risepublicadjusting.com** is shown on the homepage, contact, free claim review,
  author page, footer, author boxes, and in the Person schema.
* SMTP password must be set in `ccpa-config.php` above `public_html` (see INSTALL-HOSTINGER.md §4).

## Data

* NOAA NCEI Storm Events 1950–2026 for Nueces, San Patricio, Aransas, Kleberg: 1,869 events.
* NWS Local Storm Reports (CRP), last ~3 years: 182 reports.
* Live (cached, refreshed by cron): NWS KCRP conditions, hourly + 7-day forecast, alerts; NOAA CO-OPS tides
  (8775296, 8775792, 8775237); NHC active storms; IEM NEXRAD radar tiles (browser).
