# Content brief — southcarolinainsuranceappraiser.com

Brand / homepage keyword: **South Carolina Insurance Appraiser**. Phone +1 (844) 537-1427, email info@southcarolinainsuranceappraiser.com.
An independent insurance appraisal practice (appraiser, estimate review, umpire) for disputed property claims statewide.
Not a law firm, not a public adjuster. No fabricated reviews, testimonials, client results, years-in-business, licenses or credentials.
Any example dollar figure must be labelled illustrative ("for example", "illustrative figures").

## Hard rules (a validator enforces them)
- Python 3 module, stdlib only, data as plain lists/dicts. HTML bodies are triple-quoted strings.
- Body HTML: only `<h2>`/`<h3>` headings (never h1, and never jump h2→h4; an h3 must follow an h2), `<p>`, `<ul>/<ol>/<li>`, `<strong>`, `<em>`, `<a href>`, `<div class="note"><b class="h">Label</b>text</div>`, `<div class="table-wrap"><table>…</table></div>`. No `<?`, no inline styles, no scripts.
- Use typographic apostrophes/quotes (’ “ ”) in copy. Escape `&` as `&amp;` inside HTML strings. Plain-text fields (title, desc, short, summary, FAQ strings) may use a raw `&` — they get escaped later — EXCEPT FAQ answers, which are inserted as HTML: use `&amp;` there.
- **Banned words anywhere** (case-insensitive, whole word): Alabama, Arizona, Florida, Georgia, Missouri, Montana, Nevada, North Carolina, Wyoming, West Virginia, Massachusetts, Maryland, Maine, Delaware, New York, Kentucky. (Georgetown SC and Hurricane Florence/Florence SC are fine. Say “across the Savannah River” rather than naming the neighbouring state; say “the state line” / “the border” for the north.)
- `title` (the HTML <title>): ≤ 60 characters AND ≤ 580px using this estimator (run it!):
  ```python
  _W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500]))
  _W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611]))
  _W.update({c: 556 for c in "0123456789"}); _W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})
  px = lambda t: sum(_W.get(c, 556) for c in t) * 20 / 1000
  ```
- `desc` (meta description): 110–150 characters, unique, contains the page’s main keyword.
- Every page has ONE main keyword (field `kw`); it appears in title, h1, desc and the first paragraph.
- Be factual and cautious on law: describe statutes only generally, recommend a South Carolina attorney for legal questions, never promise outcomes.

## Internal URLs you may link to (only these)
- `/` home, `/about-the-firm/`, `/contact-an-appraiser/`
- Services index `/claim-dispute-services/` + `/claim-dispute-services/<slug>/` for: appraisal-demand-representation, home-insurance-appraisal, commercial-hoa-appraisal, roof-hail-damage-appraisal, wind-tornado-claim-appraisal, hurricane-claim-appraisal, water-damage-claim-appraisal, fire-smoke-damage-appraisal, tree-fall-ice-storm-appraisal, earthquake-claim-appraisal, claim-estimate-review, umpire-neutral-appraiser
- Locations index `/locations-served/` + `/locations-served/<slug>/` for: charleston, columbia, greenville, myrtle-beach, spartanburg, mount-pleasant, summerville, rock-hill, hilton-head-island, florence, beaufort, aiken
- Tools index `/free-claim-tools/` + `/free-claim-tools/<slug>/` for: claim-gap-fee-estimator, rcv-acv-holdback-calculator, roof-area-pitch-estimator, hurricane-deductible-calculator, claim-timeline-builder, appraisal-readiness-checkup, wind-flood-damage-splitter
- `/appraisal-process-explained/`, `/insurance-appraisal-faq/`, `/appraisal-glossary/`, guides index `/appraisal-guides/` + `/appraisal-guides/<slug>/` for: hurricane-deductibles-explained, when-a-tree-falls-on-your-house, wind-pool-claims-and-appraisal, appraisal-versus-lawsuit, storm-damage-photo-checklist, how-umpires-decide-line-items

## South Carolina facts (use; don’t invent beyond widely documented facts)
- 46 counties; capital Columbia. Regions: **Upstate** (Greenville, Spartanburg, Anderson; Rock Hill/York County in the north-central Piedmont), **Midlands** (Columbia, Lexington, Aiken, Sumter, Orangeburg), **Pee Dee** (Florence, Darlington, Marion, Dillon), **Grand Strand** (Myrtle Beach, North Myrtle Beach, Conway, Surfside Beach, Georgetown), **Lowcountry** (Charleston, Mount Pleasant, Summerville, Beaufort, Hilton Head Island, Bluffton).
- Regulator: **South Carolina Department of Insurance (SCDOI)**, which handles consumer complaints and licenses adjusters.
- Coastal wind pool: **South Carolina Wind and Hail Underwriting Association (SCWHUA)** — the insurer of last resort for wind and hail in designated coastal areas; homeowners there often pair an SCWHUA wind policy with a homeowners policy that excludes wind, plus separate flood insurance (NFIP or private). Do not mention a FAIR plan.
- 2007 Omnibus Coastal Property Insurance Reform Act: created catastrophe savings accounts, hurricane-deductible disclosure rules and the **SC Safe Home** mitigation grant program. Mention lightly, not as legal advice.
- Bad faith (describe only generally): South Carolina courts recognize a claim against an insurer that unreasonably refuses to pay benefits under its policy, and a provision of Title 38 of the state insurance code can allow attorney’s fees in some cases where an insurer refuses payment without reasonable cause. The state also has unfair claims practices rules. Appraisal does not decide bad faith; refer to a South Carolina attorney.
- Suit limits: contract actions in SC generally have a three-year statute of limitations, but policy wording and other rules matter — always “confirm with a South Carolina attorney”.
- Umpire appointment if appraisers can’t agree: a court of record in the county where the property is located (in SC, the circuit court).
- Notable events: Hurricane Hazel (Oct 1954, devastating Grand Strand); Hurricane Gracie (1959, Beaufort area); **Hurricane Hugo** (Sept 21–22, 1989, Category 4 landfall near Charleston/Sullivan’s Island, damage far inland to Sumter and the Midlands); Hurricane Gaston (2004, near McClellanville); the **October 2015 “thousand-year” flood** (Columbia and the Midlands, dam failures, Gills Creek); **Hurricane Matthew** (Oct 8, 2016, Category 1 landfall near McClellanville; heavy tree loss on Hilton Head and Beaufort, inland flooding); Irma (2017, Charleston surge flooding); **Hurricane Florence** (Sept 2018, record river flooding in the Pee Dee and Horry County — Conway, Waccamaw River); Dorian (2019, brushed the coast); **Hurricane Ian** (Sept 30, 2022, landfall near Georgetown); Idalia (Aug 2023, Charleston tidal flooding); Debby (Aug 2024, heavy Lowcountry rain); **Hurricane Helene** (Sept 26–27, 2024, severe wind and widespread tree fall across the Upstate and Aiken County, very long power outages); the **February 2014 ice storm** (Aiken, Midlands, Pee Dee); the **April 13, 2020 Easter tornado outbreak** (an EF3 in Seneca/Oconee County and strong tornadoes in Hampton County); the **1886 Charleston earthquake** (epicenter near Summerville/Middleton Place) and the **2021–22 Elgin/Lugoff earthquake swarm** in Kershaw County. Earthquake is usually excluded from homeowners policies unless an earthquake endorsement or policy was bought.
- Housing: Charleston single houses with piazzas and historic masonry/stucco, elevated coastal homes, high-rise and mid-rise condos on the Grand Strand, mill villages in the Upstate, 1920s–40s bungalows in Columbia, fast-growing new subdivisions around Summerville, Rock Hill/Fort Mill and Greenville; manufactured homes in rural counties; pine and live-oak canopies.
- Perils: hurricanes and tropical storms, wind-driven rain, storm surge (flood — separate policy), tornadoes, hail (Upstate/Midlands spring), tree fall, ice storms, freeze/burst pipes, lightning and fire, earthquake (if endorsed), mold after water losses.

## Tone
Plain-spoken, specific, useful. Short paragraphs. US spelling. Explain *how appraisal applies* to the topic in SC, what documentation helps, common estimate disputes (e.g. matching, code upgrades, O&P, steep/high charges, tree removal sub-limits, wind-vs-flood causation, hurricane deductible triggers), and when appraisal is the wrong tool.
