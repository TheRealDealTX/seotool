# Content brief — Maryland Insurance Appraiser (marylandinsuranceappraiser.com)

Brand / main keyword: **Maryland Insurance Appraiser**. Phone +1 (844) 537-1427. Email info@marylandinsuranceappraiser.com.
An independent insurance appraisal firm (appraisal clause representation, estimate review, umpire work) for disputed
property claims anywhere in Maryland. Not a law firm, not a public adjuster.

## Hard rules
- All copy must be **new and Maryland-specific**. Do not copy phrasing from other sites in this repo.
- **Never write these words anywhere** (build fails): Alabama, Arizona, Florida, Georgia, Massachusetts, Missouri,
  Montana, Nevada, North Carolina, West Virginia, Wyoming. (Plain "Virginia" and "Delaware" are fine. Say "across the
  Potomac" or "the panhandle state to the west" if needed — better to avoid neighbour-state talk.)
- No fabricated reviews, testimonials, client results, case wins, staff names, years in business, licences or
  credentials. Any dollar example must be labelled illustrative ("an illustrative example", "hypothetical").
- Be factual and cautious on law. Describe statutes only generally; recommend a Maryland attorney for legal questions.
- Use curly apostrophes/quotes (’ “ ”) and en dashes (–) like normal typography. HTML entities like `&amp;` in HTML.
- Body HTML: start with `<h2>`; `<h3>` only directly under an `<h2>`; never `<h1>`, never skip a level, never h4+.
  Allowed blocks: p, ul/ol/li, strong, em, a, h2, h3, table (with thead/tbody, wrapped in `<div class="table-wrap">`),
  `<div class="note"><b class="h">Label</b>Text…</div>`.
- Internal links only to paths that will exist (listed below). Do not invent other internal URLs.
- SEO: every `title` ≤ 60 characters (and not wider than ~580px in Arial 20px — roughly avoid >56 chars if many
  capitals/W/M), every `desc` 110–150 characters, all unique. Check lengths with Python before finishing.
- Each page has a single main keyword (e.g. "Hail Damage Appraisal Maryland"); use it in title, h1, first paragraph.

## Maryland facts you may use (stay within these; don’t invent numbers)
- 23 counties plus Baltimore City (an independent city) = 24 local jurisdictions.
- Regions: Western Maryland (Garrett, Allegany, Washington), Capital Region (Montgomery, Prince George’s, Frederick),
  Central Maryland (Baltimore City, Baltimore County, Howard, Anne Arundel, Harford, Carroll), Southern Maryland
  (Charles, Calvert, St. Mary’s), Eastern Shore (Cecil, Kent, Queen Anne’s, Talbot, Caroline, Dorchester, Wicomico,
  Somerset, Worcester).
- Regulator: **Maryland Insurance Administration (MIA)**, led by the Maryland Insurance Commissioner; takes consumer
  complaints. Claims-handling standards appear in Maryland regulations (COMAR Title 31) and the unfair claim settlement
  practices law (Insurance Article §27-303) — describe generally.
- Residual market: **Maryland Joint Insurance Association (MJIA)** – the state’s FAIR-plan-style insurer of last resort
  for property owners who can’t get coverage in the regular market. Maryland has no separate wind pool.
- Bad faith (describe only generally): Maryland law (Insurance Article §27-1001 together with Courts & Judicial
  Proceedings §3-1701) lets first-party property and certain other policyholders pursue an insurer’s failure to act in
  good faith; it generally begins with a complaint filed with the MIA before going to court, and remedies can include
  actual damages plus certain expenses and fees. Appraisers don’t handle this — refer to an attorney.
- Suit time limits: Maryland’s general contract limitations period is three years, and Maryland law generally does not
  let property policies shorten the time to sue below that — but when the clock starts can be disputed; tell readers to
  check the policy and ask an attorney.
- Percentage hurricane / named-storm / windstorm deductibles are common near the Chesapeake Bay and Atlantic coast
  (Eastern Shore, Southern Maryland, Anne Arundel); trigger definitions vary by insurer.
- Perils: nor’easters; tropical storms and hurricane remnants; derechos and straight-line wind; severe thunderstorms
  with hail (mainly central and western counties, spring–summer); tornadoes (usually brief, EF0–EF2, sometimes
  stronger); flash flooding in stream valleys; tidal/“nuisance” flooding around Annapolis and the Bay; heavy snow,
  ice dams and frozen pipes (worst in Garrett and Allegany, where seasonal snowfall can far exceed the rest of the
  state); falling oaks and tulip poplars; rowhouse fires that spread across party walls.
- Well-known events: Hurricane Isabel (Sept 2003 – record storm surge in the Bay, flooding Fells Point, Annapolis’
  City Dock and many shoreline communities); Tropical Storm Agnes (June 1972 – statewide river flooding); the La Plata
  tornado (April 28, 2002 – an F4 through Charles County); the June 29, 2012 derecho (widespread tree and roof damage,
  long power outages); Superstorm Sandy (Oct 2012 – coastal flooding in Crisfield and Ocean City, blizzard conditions in
  Garrett County); the February 2010 back-to-back blizzards (“Snowmageddon”, roof collapses); the January 2016 blizzard;
  Ellicott City flash floods (July 30, 2016 and May 27, 2018); a tornado through Annapolis and Edgewater on Sept 1, 2021
  from Ida’s remnants; the 1933 Chesapeake–Potomac hurricane that cut the Ocean City inlet; the 1962 Ash Wednesday
  nor’easter; Cumberland’s 1936 St. Patrick’s Day flood (which led to its flood-control project) and the January 1996
  flood in Western Maryland.
- Housing mix: Baltimore brick rowhouses (often 1880s–1920s, low-slope membrane or built-up roofs, shared party walls,
  plaster interiors); 1930s–60s colonials and Cape Cods in Towson/Catonsville; planned-community townhouses in Columbia;
  Levitt-built 1960s homes in Bowie; colonial-era and 18th/19th-century buildings in Annapolis and Frederick historic
  districts; high-rise condos in Ocean City, Silver Spring, Rockville and Baltimore’s Harbor East; newer vinyl-sided
  subdivisions in Waldorf, Frederick County and Harford County; hillside frame houses in Cumberland; lake cabins at
  Deep Creek Lake (Garrett County).

## Internal paths that will exist
/  /about-the-firm/  /start-a-claim-review/
/property-claim-services/ and /property-claim-services/<service-slug>/ for:
  appraisal-demand-representation, home-insurance-appraisal, commercial-hoa-appraisal, roof-hail-damage-appraisal,
  windstorm-tornado-appraisal, hurricane-noreaster-appraisal, water-damage-appraisal, fire-smoke-damage-appraisal,
  snow-ice-dam-freeze-appraisal, tree-impact-claim-appraisal, carrier-estimate-review, neutral-umpire-services
/service-locations/ and /service-locations/<slug>/ for: baltimore, towson, ellicott-city, annapolis, frederick,
  rockville, bowie, waldorf, hagerstown, cumberland, salisbury, ocean-city
/appraisal-calculators/ and /appraisal-calculators/<slug>/ for: claim-gap-fee-estimator, rcv-acv-holdback-worksheet,
  roof-square-pitch-calculator, hurricane-deductible-calculator, claim-timeline-planner, appraisal-readiness-checklist,
  snow-load-roof-estimator
/the-appraisal-process/  /common-questions/  /appraisal-glossary/
/knowledge-base/ and /knowledge-base/<slug>/ for: maryland-appraisal-clause-guide, mia-complaint-or-appraisal,
  baltimore-rowhouse-roof-claims, bay-hurricane-deductibles, western-maryland-ice-dam-claims,
  choosing-an-independent-appraiser
/privacy-practices/  /site-terms/  /important-disclaimer/  /photo-credits/  /all-pages/
