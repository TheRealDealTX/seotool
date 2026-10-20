# Verification Report — PortArthurPublicAdjuster.com rebuild

Prepared October 20, 2026.

## 1. Original URLs (all preserved)

Crawled from the live WordPress site (Yoast sitemaps + REST API): 6 pages, 1 post, 1 category, 26 media files.

| Original URL | New site |
|---|---|
| `/` | 200 — rebuilt homepage |
| `/about-us/` | 200 — rewritten |
| `/services/` | 200 — rewritten hub for 19 service pages |
| `/blog/` | 200 — blog index with search + categories |
| `/contact/` | 200 — rewritten, full form |
| `/privacy-policy/` | 200 — updated (forms, uploads, weather data) |
| `/terms-of-use/` | 200 — updated |
| `/are-insurance-adjusters-honest/` | 200 — rewritten and expanded (2,101 words) |
| `/category/general/` | 200 — kept as a live archive page (noindex, follow) |
| `/wp-content/uploads/2026/02/*` | 200 — all 26 original image files at the same paths |
| `/sitemap_index.xml`, `/post-sitemap.xml`, `/page-sitemap.xml`, `/category-sitemap.xml` | 301 → `/sitemap.xml` |
| `/feed/` | 200 (RSS); `/comments/feed/`, `/category/general/feed/` 301 → `/feed/` |
| `/?p=251`, `/?page_id=N` | 301 → matching page |
| `/wp-admin/`, `/wp-login.php`, `/xmlrpc.php`, `/wp-json/` | 410 Gone |

## 2. Content removed from the old copy

Unsupported or risky claims were removed: "We fight insurance companies", "You pay nothing unless we increase
your settlement", "No upfront fees — we only get paid if we recover", "Texas insurance policy loopholes",
"relentless advocacy", "pursued aggressively", "team of licensed public adjusters". The old article also said
hurricane wind is covered under homeowners policies; it now explains the homeowners / TWIA / flood split
used in Jefferson County. Fee wording everywhere: written contract, capped at 10% by Texas law.

## 3. Pages

| URL | Words | FAQs | Title tag |
|---|---|---|---|
| `/about-us/` | 1191 | 6 | About Port Arthur Public Adjuster | Licensed Texas Adjusting |
| `/service-areas/` | 703 | 4 | Service Areas | Jefferson County Public Adjuster for SETX |
| `/contact/` | 257 | 4 | Contact a Port Arthur Public Adjuster | Insurance Claim Help |
| `/claim-tools/` | 470 | 3 | Free Insurance Claim Tools for Port Arthur Property Owners |
| `/category/general/` | 0 | 0 | General Insurance Claim Articles | Port Arthur Public Adjuster |
| `/hurricane-deductible-calculator/` | 223 | 5 | Hurricane Deductible Calculator for Texas Homeowners |
| `/claim-calculator/` | 713 | 5 | Insurance Claim Settlement Calculator (RCV, ACV, Depreciation) |
| `/author/joseph-dittman/` | 410 | 4 | Joseph Dittman, Texas Public Adjuster | Author Bio |
| `/hurricane-tracker/` | 343 | 4 | Port Arthur Hurricane Tracker | Live NHC Storm Map |
| `/weather/` | 726 | 5 | Port Arthur Weather Today: Live Conditions, Forecast & Alerts |
| `/storm-history/` | 895 | 5 | Port Arthur Storm History | Jefferson County NOAA Records |
| `/local-building-codes/` | 1306 | 6 | Port Arthur Building Codes & Insurance Claims | WPI-8 Guide |
| `/` | 0 | 7 | Port Arthur Public Adjuster | Hurricane & TWIA Claim Help |
| `/faq/` | 102 | 23 | Port Arthur Public Adjuster FAQs | TWIA, Flood & Fees |
| `/privacy-policy/` | 1139 | 3 | Privacy Policy | Port Arthur Public Adjuster |
| `/blog/` | 0 | 0 | Port Arthur Insurance Claim Blog | Hurricane, TWIA & Flood |
| `/claim-documentation-checklist/` | 613 | 5 | Insurance Claim Documentation Checklist | Free Printable Tool |
| `/services/` | 1071 | 6 | Port Arthur Public Adjuster Services | Property Claim Help |
| `/service-areas/beaumont/` | 858 | 5 | Public Adjuster in Beaumont, TX | Hurricane & Flood Claims |
| `/service-areas/groves/` | 760 | 5 | Public Adjuster in Groves, TX | Hurricane & Flood Claim Help |
| `/service-areas/nederland/` | 754 | 4 | Public Adjuster in Nederland, TX | Storm & Flood Claim Help |
| `/service-areas/orange/` | 753 | 5 | Public Adjuster in Orange, TX | Hurricane, Wind & Flood Claims |
| `/service-areas/port-neches/` | 783 | 4 | Public Adjuster in Port Neches, TX | Storm & Fire Claim Help |
| `/service-areas/sabine-pass/` | 790 | 5 | Public Adjuster in Sabine Pass, TX | Hurricane & TWIA Claims |
| `/weather-events/` | 605 | 4 | Recent Port Arthur Storm Reports | Jefferson County Weather |
| `/free-claim-review/` | 304 | 4 | Free Claim Review | Port Arthur Public Adjuster |
| `/sitemap/` | 0 | 0 | Sitemap | Port Arthur Public Adjuster Pages, Services & Articles |
| `/storm-lookup/` | 574 | 4 | Storm Event Lookup | Storm Reports Near Port Arthur ZIP Codes |
| `/terms-of-use/` | 965 | 3 | Terms of Use | Port Arthur Public Adjuster |

## 4. Services (19)

| URL | Words | FAQs | Title tag |
|---|---|---|---|
| `/services/hurricane-damage-claims/` | 1043 | 6 | Port Arthur Hurricane Damage Claims | Public Adjuster |
| `/services/twia-windstorm-claims/` | 904 | 6 | TWIA Claim Port Arthur | Windstorm Claim Public Adjuster |
| `/services/wind-damage-claims/` | 973 | 5 | Port Arthur Wind Damage Claims | Public Adjuster Help |
| `/services/flood-damage-claims/` | 912 | 6 | Port Arthur Flood Damage Claims | NFIP & Private Flood |
| `/services/storm-damage-claims/` | 946 | 6 | Port Arthur Storm Damage Claims | Public Adjuster Help |
| `/services/roof-damage-insurance-claims/` | 910 | 6 | Port Arthur Roof Damage Insurance Claims | Public Adjuster |
| `/services/hail-damage-claims/` | 933 | 6 | Port Arthur Hail Damage Claims | Public Adjuster Help |
| `/services/water-damage-claims/` | 938 | 5 | Port Arthur Water Damage Claims | Public Adjuster Help |
| `/services/mold-damage-claims/` | 927 | 5 | Port Arthur Mold Damage Claims | Public Adjuster Help |
| `/services/fire-damage-claims/` | 932 | 6 | Port Arthur Fire Damage Claims | Public Adjuster Help |
| `/services/smoke-damage-claims/` | 1113 | 6 | Smoke Damage Claims Port Arthur, TX | Public Adjuster |
| `/services/residential-property-claims/` | 1022 | 6 | Residential Property Claims Port Arthur | Public Adjuster |
| `/services/commercial-property-claims/` | 1024 | 7 | Commercial Property Claims Port Arthur, TX | Public Adjuster |
| `/services/denied-insurance-claims/` | 1044 | 6 | Denied Insurance Claim Port Arthur | Public Adjuster Help |
| `/services/underpaid-insurance-claims/` | 982 | 6 | Underpaid Insurance Claim Port Arthur | Public Adjuster |
| `/services/delayed-insurance-claims/` | 1008 | 6 | Delayed Insurance Claim Port Arthur | Prompt Payment Help |
| `/services/insurance-claim-supplements/` | 983 | 6 | Insurance Claim Supplements Port Arthur | Reopen Claims |
| `/services/insurance-appraisal/` | 990 | 6 | Insurance Appraisal Port Arthur, TX | Claim Amount Disputes |
| `/services/insurance-estimate-review/` | 1018 | 6 | Insurance Estimate Review Port Arthur | Xactimate Check |

## 5. Articles (10, author Joseph Dittman, licensed public adjuster)

| URL | Words | FAQs | Title tag |
|---|---|---|---|
| `/denied-insurance-claim-port-arthur/` | 1723 | 6 | Denied Insurance Claim in Port Arthur? What to Do Next |
| `/how-to-document-storm-damage-port-arthur/` | 1758 | 5 | How to Document Storm Damage in Port Arthur, TX |
| `/hurricane-damage-insurance-claim-port-arthur/` | 1805 | 6 | Port Arthur Hurricane Damage Claim: Step-by-Step Guide |
| `/hurricane-deductible-texas-explained/` | 1668 | 6 | Texas Hurricane Deductibles Explained: TWIA & Named Storm |
| `/port-arthur-hurricane-history-insurance-lessons/` | 1974 | 6 | Port Arthur Hurricane History & Insurance Lessons |
| `/public-adjuster-pros-and-cons/` | 1747 | 6 | Public Adjuster Pros and Cons | Port Arthur Public Adjuster |
| `/twia-windstorm-claim-guide-port-arthur/` | 1835 | 7 | TWIA Windstorm Claim Guide for Port Arthur Homeowners |
| `/when-is-it-too-late-to-hire-a-public-adjuster/` | 1747 | 6 | When Is It Too Late to Hire a Public Adjuster? Texas Guide |
| `/wind-vs-flood-damage-port-arthur-insurance/` | 2181 | 6 | Wind vs. Flood Damage Claims in Port Arthur, TX |
| `/are-insurance-adjusters-honest/` | 2101 | 6 | Are Insurance Adjusters Honest? Port Arthur Homeowner Guide |

## 6. Tools and live data

| Tool | URL | Data |
|---|---|---|
| Live hurricane tracker | `/hurricane-tracker/` | NHC CurrentStorms.json (cached 15 min), NWS alerts, NHC 7-day outlook image, Leaflet map with 200/400/800-mile rings |
| Live weather | `/weather/` | NWS API: KBPT observations, LCH 7-day forecast, alerts; KLCH radar loop |
| Hurricane deductible calculator | `/hurricane-deductible-calculator/` | In-browser; 1/2/3/5/10% or custom of Coverage A |
| Claim settlement calculator | `/claim-calculator/` | In-browser RCV/ACV/depreciation math |
| Documentation checklist | `/claim-documentation-checklist/` | In-browser, printable, optional local save |
| Storm event lookup | `/storm-lookup/` | NOAA NCEI + NWS LSR, Jefferson County cities/ZIPs (Census Gazetteer) |
| Storm history | `/storm-history/` | NOAA NCEI Storm Events, Jefferson County, 697 events 1955–2026 |
| Recent weather events | `/weather-events/` | NWS Lake Charles Local Storm Reports (+ IEM archive) |

## 7. Forms

* Free Claim Review form on `/free-claim-review/`, `/contact/`, the homepage (hero + section), and the popup.
* The popup opens **5 seconds** after page load (not on contact, free-claim-review, privacy, terms, or noindex pages);
  dismissing it snoozes it for 7 days, submitting for 90 days.
* All submissions are emailed to **info@portarthurpublicadjuster.com** via authenticated SMTP (PHPMailer),
  with CSRF token, honeypot, minimum fill time, rate limit, and up to 3 attachments × 8 MB.
* Verified locally against an SMTP sink: test submissions were addressed `To: info@portarthurpublicadjuster.com`
  with `Reply-To` set to the visitor. **Live delivery requires the mailbox password** (INSTALL-HOSTINGER.md §4).

## 8. SEO

* Homepage: "Port Arthur Public Adjuster" appears **20 times** in main visible content (26 counting header/footer);
  title "Port Arthur Public Adjuster | Hurricane & TWIA Claim Help".
* Unique title + meta description on every page; canonical URLs; Open Graph/Twitter tags; geo meta.
* JSON-LD: WebSite, ProfessionalService/LocalBusiness (Jefferson + Orange counties and 14 cities),
  BreadcrumbList, BlogPosting with author Person (Joseph Dittman, Licensed Public Adjuster), Service, FAQPage.
* XML sitemap (57 URLs) and RSS feed generated automatically.

## 9. Test results (local, PHP 8.3 built-in server)

* `tools/test/crawl.py`: 57 HTML pages, 145 internal link targets — **no problems found** (status codes, one H1,
  unique titles/descriptions, description length, canonical, JSON-LD, image alt text, internal links).
* `tools/test/functional.js` (Playwright/Chromium): **all passed** — popup timing (hidden at 3.5 s, open by 5 s),
  Escape/dismiss, phone layout, popup + contact form submissions, settlement calculator math, checklist,
  storm history filters, storm lookup (ZIP 77640), deductible calculator, hurricane tracker map, mobile nav,
  no JavaScript errors.
* `php -l` on every PHP file; no McAllen/Hidalgo/Rio Grande text remains in the site.

## 10. Before launch

1. Create the SMTP override file with the info@portarthurpublicadjuster.com mailbox password, then send a live test.
2. Set up the cron job (INSTALL-HOSTINGER.md §6) so weather, tropics, and storm reports stay current.
3. Confirm TDI license #3356839 and the business details in `includes/config.php`.
4. Submit `/sitemap.xml` in Google Search Console.
