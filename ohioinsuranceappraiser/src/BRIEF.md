# Ohio Insurance Appraiser — content brief (shared by all writers)

Site: https://ohioinsuranceappraiser.com — "Ohio Insurance Appraiser", an independent property-insurance
appraisal practice (party appraiser under the policy's appraisal clause, estimate review, umpire work).
Phone +1 (844) 537-1427 · info@ohioinsuranceappraiser.com · Mon–Fri 8am–6pm ET · statewide.

## Hard rules
- Python 3 data files only, stdlib, must import cleanly (`python3 -c "import services"` from src/).
- Write ALL copy fresh and specific to Ohio. `src/ref/*.py` is copy from a sister site (another state):
  read it ONLY to see the data shape. Do not reuse its sentences, headings or structure of arguments.
- NEVER write any of these words anywhere (the build fails): Alabama, Arizona, Delaware, Florida, Georgia,
  Kentucky, Maine, Maryland, Massachusetts, Missouri, Montana, Nevada, New York, North Carolina,
  West Virginia, Wyoming. (So: no "Delaware County", no "Wyoming, Ohio", no "Covington KY",
  say "across the Ohio River" / "neighboring states" instead.)
- No reviews, testimonials, client stories, "we recovered $X", years-in-business, license numbers,
  certifications or team bios. Any example dollar figures must be labelled "illustrative" / "for example".
- Legal caution: we are not attorneys or public adjusters; say "commonly", "many policies", "check your policy",
  "talk to an Ohio attorney". Bad faith in Ohio: describe only generally — Ohio has no first-party bad-faith
  statute giving policyholders a private claim; the Ohio Supreme Court recognizes a common-law bad-faith tort
  against insurers that lack reasonable justification for how they handle or pay a claim; claim-handling
  standards are set by the Ohio Department of Insurance's unfair claims settlement practices rule
  (Ohio Administrative Code 3901-1-54). Don't cite case names or penalty figures.
- Typography: curly apostrophes/quotes (’ “ ”), en dash for ranges (45–120), em dash sparingly.
- HTML bodies: start with <h2>; allowed tags h2, h3 (h3 only under an h2), p, ul, ol, li, strong, em, a,
  and callouts `<div class="note"><b class="h">Heading</b>Text…</div>`. No h1, no h4+, no images, no inline style.
  Internal links only to the URLs listed below. FAQ answers are PLAIN TEXT (no HTML) — they go into JSON-LD.
- SEO: every page has ONE main keyword (field "kw"); use it in the title, h1, desc and naturally in the body.
  `title` ≤ 55 characters (hard max 60; avoid many capital W/M), unique across the site.
  `desc` (meta description) MUST be 110–150 characters — count them with Python before finishing.
  The phrase "Ohio Insurance Appraiser" may appear but don't stuff it.

## Vetted Ohio facts you may use (stay inside these; if unsure of a figure, leave it out)
- 88 counties. Regulator: Ohio Department of Insurance (ODI), Columbus; consumer hotline exists — don't give a number.
- FAIR plan: Ohio FAIR Plan Underwriting Association (insurer of last resort for property). No wind pool.
- Regions: Northeast (Cleveland, Akron, Canton, Youngstown, Lake Erie snowbelt in Lake/Geauga/Ashtabula),
  Northwest (Toledo, Sandusky, Lima, flat Great Black Swamp farmland), Central (Columbus, Franklin County
  suburbs), Southwest (Cincinnati, Dayton, Miami Valley, Xenia), Southeast/Appalachian Ohio (Zanesville,
  Athens, Marietta, hills, Ohio River towns).
- Perils: hail (spring–summer), severe thunderstorms and straight-line wind, tornadoes, derechos,
  remnants of Gulf hurricanes, lake-effect snow (snowbelt east of Cleveland), ice dams, frozen/burst pipes,
  snow load, ice storms, basement water and sewer/drain backup (needs an endorsement, usually with a sublimit),
  river flooding (flood is excluded from homeowners policies; NFIP/flood policy), fallen trees, fire, lightning.
  Old housing stock: many pre-1940 homes, slate roofs, plaster walls, brick doubles, basements nearly everywhere.
- Storms: Great Flood of March 1913 (Dayton, Miami River, Columbus Scioto, Zanesville Muskingum);
  1924 Lorain–Sandusky tornado (June 28, 1924, deadliest in Ohio history); 1937 Ohio River flood (Cincinnati);
  April 3, 1974 Xenia tornado (F5, part of the 1974 Super Outbreak); Great Blizzard of January 1978;
  May 31, 1985 Niles–Wheatland F5 tornado (Mahoning Valley); April 9, 1999 Blue Ash/Montgomery F4 tornado
  (Cincinnati suburbs); September 14, 2008 remnants of Hurricane Ike — hurricane-force gusts across Ohio,
  widespread roof and tree damage, about two million customers lost power, one of the costliest insured
  events in Ohio history; June 5, 2010 Lake Township EF4 tornado (Wood County near Toledo);
  June 29, 2012 derecho (Columbus and central/southern Ohio, roughly a million without power);
  Memorial Day 2019 tornado outbreak in the Dayton area (EF4 through Trotwood/Harrison Township/Brookville,
  EF3 Beavercreek); March 14, 2024 Indian Lake EF3 tornado (Logan County).
- Many Ohio homeowner policies contain a contractual suit-limitation clause — often one year from the
  date of loss (some two); Ohio courts generally enforce such clauses. Always say "check your policy" and
  "talk to an Ohio attorney". Appraisal clause: written demand, each side picks a competent and impartial/
  independent appraiser (often within 20 days), appraisers pick an umpire (court can appoint if they can’t agree),
  agreement of any two sets the amount of loss; each side pays its appraiser and splits the umpire.
- Wind/hail percentage deductibles (1%–5% of Coverage A) appear on some Ohio policies.

## Site URLs you may link to
/ · /meet-the-firm/ · /contact-our-team/ · /appraisal-timeline/ (process guide) · /appraisal-q-and-a/ (FAQ)
· /appraisal-lexicon/ (glossary) · /appraisal-briefings/ (guides index)
Services (/appraisal-practice/<slug>/): appraisal-demand-representation, home-insurance-appraisal,
commercial-hoa-appraisal, hail-roof-appraisal, tornado-windstorm-appraisal, derecho-remnant-storm-appraisal,
water-damage-appraisal, fire-smoke-appraisal, ice-dam-frozen-pipe-appraisal, estimate-audit, neutral-umpire-services
Cities (/service-cities/<slug>-ohio/): columbus, cleveland, cincinnati, toledo, akron, dayton, canton,
youngstown, sandusky, lima, xenia, zanesville
Tools (/appraisal-workbench/<slug>/): claim-gap-fee-estimator, rcv-acv-holdback-calculator,
roof-area-pitch-calculator, percentage-deductible-calculator, claim-calendar-builder,
appraisal-readiness-checkup, basement-backup-sublimit-calculator
