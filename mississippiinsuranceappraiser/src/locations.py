# -*- coding: utf-8 -*-
"""City / location pages for mississippiinsuranceappraiser.com."""

LOCATIONS = [
    # 1 ─────────────────────────────────────────────────────────────
    {
        "slug": "jackson-hinds-county",
        "city": "Jackson",
        "county": "Hinds County",
        "region": "Capital Region",
        "kw": "insurance appraiser jackson ms",
        "title": "Insurance Appraiser in Jackson, MS | Hinds County Claims",
        "desc": "Independent insurance appraiser in Jackson, MS for disputed home and business claims in Hinds, Madison and Rankin counties.",
        "h1": "Jackson Insurance Appraiser for Disputed Property Claims",
        "lede": "When your carrier’s number doesn’t match what it will cost to repair your Jackson home or building, the appraisal clause in your policy gives you a way to settle the amount without a lawsuit. We work Jackson-area claims from Belhaven to South Jackson and out into the suburbs.",
        "perils": [
            "Frozen and burst pipes after hard freezes",
            "Water losses tied to municipal pressure loss and boil-water events",
            "Pearl River and creek flooding",
            "Tree fall on older, shaded lots",
            "Hail and straight-line wind on roofs",
        ],
        "neighborhoods": ["Belhaven", "Fondren", "Eastover", "North Jackson", "South Jackson", "West Jackson"],
        "housing": "Jackson mixes early-1900s homes in Belhaven and Fondren, large custom homes in Eastover, mid-century brick ranches across North and South Jackson, and newer slab-on-grade subdivisions in the Madison and Rankin County suburbs.",
        "storms": [
            ("Feb 2020", "Pearl River flooding in the Jackson metro"),
            ("Feb 2021", "Statewide winter storm and freeze, with widespread burst pipes"),
            ("2022", "Jackson water-system failures, pressure loss and boil-water notices"),
            ("Dec 2022", "Hard freeze and another round of frozen-pipe losses"),
        ],
        "near": ["vicksburg-warren-county", "hattiesburg-forrest-county", "meridian-lauderdale-county"],
        "body": """<h2>Property claims in the capital city</h2>
<p>Jackson is Mississippi’s capital and largest city. It sits mostly in Hinds County, which is unusual in having two county seats, Jackson and Raymond, and the city limits also reach into Madison and Rankin counties. That matters on a claim: your address, your county and sometimes your carrier’s local adjuster pool all shape how a loss gets handled.</p>
<p>We also work claims across the metro, including Brandon, Madison, Ridgeland, Clinton, Pearl and Flowood. Many of those suburbs were built out more recently, so the homes and the disputes look different from the older neighborhoods inside the city.</p>

<h2>What recent Jackson losses have looked like</h2>
<p>Jackson’s claim history over the last several years has been driven as much by water and cold as by wind:</p>
<ul>
<li><strong>February 2020:</strong> the Pearl River rose into neighborhoods in northeast Jackson and nearby areas. Flood damage generally falls under a separate flood policy, not your homeowners policy.</li>
<li><strong>February 2021:</strong> the statewide freeze split pipes in attics, crawlspaces and exterior walls.</li>
<li><strong>2022:</strong> the city’s water-system failures brought pressure loss and boil-water notices. Some owners later found plumbing and fixture damage that carriers questioned.</li>
<li><strong>December 2022:</strong> another hard freeze, and another round of frozen-pipe claims.</li>
</ul>
<p>On a water loss, the cause question (sudden pipe failure versus long-term leak, or surface water versus plumbing) is usually a coverage issue. Appraisal decides the amount of loss, not coverage. Once coverage is accepted, though, the scope of drying, tear-out and rebuild is where most Jackson water disputes live. Our <a href="/our-appraisal-services/water-plumbing-loss-appraisal/">water and plumbing loss appraisal</a> page explains how we handle those.</p>

<h2>Belhaven, Fondren, Eastover and older Jackson homes</h2>
<p>Belhaven and Fondren hold many early-twentieth-century homes with plaster walls, original wood floors, tall ceilings and detailed trim. Eastover has large custom homes with high-end finishes. North, South and West Jackson have a lot of brick ranches from the 1960s through the 1980s.</p>
<h3>Where estimates come apart</h3>
<ul>
<li><strong>Plaster and trim:</strong> carrier estimates often price drywall patching where the house has plaster and site-built moldings.</li>
<li><strong>Flooring continuity:</strong> water reaches one room of continuous hardwood, and the estimate replaces only that room.</li>
<li><strong>Matching:</strong> older brick, tile and shingles may no longer be made, so a “repair” that can’t match is not a real repair.</li>
<li><strong>Tree fall:</strong> mature oaks and pines shade many of these lots. Many policies cap debris removal per tree and per occurrence.</li>
</ul>

<div class="callout"><b class="callout-t">A note on Yazoo clay</b><p>Much of the Jackson metro sits on Yazoo clay, an expansive soil that swells and shrinks. Foundation movement from soil is usually excluded. Where a covered event, such as a pipe burst or a tree strike, causes the damage, the cost of that damage is a fair subject for appraisal.</p></div>

<h2>How we help Jackson owners</h2>
<p>We start by reading your carrier’s estimate line by line against the actual house: measurements, materials, labor, overhead and profit, and code items. If the gap is real and your policy has an appraisal clause, we can represent you through the demand, the appraiser exchange and, if needed, the umpire. See how that works in our <a href="/appraisal-roadmap/">appraisal roadmap</a>, or start with a <a href="/our-appraisal-services/carrier-estimate-review/">carrier estimate review</a>.</p>
<p>Deadlines in your policy and under state law still apply while you talk to your carrier, so confirm yours with a Mississippi attorney.</p>""",
        "faqs": [
            ("Does appraisal cover damage from Jackson’s water-system problems?", "Appraisal does not decide whether a loss is covered. If your carrier accepts that a water loss is covered but disagrees on the cost of repairs, appraisal can settle that amount. Whether pressure-related damage is covered depends on your policy wording and the facts."),
            ("Do you work claims in Madison and Rankin County suburbs?", "Yes. We work claims across the Jackson metro, including Brandon, Madison, Ridgeland, Clinton, Pearl and Flowood, and throughout Mississippi."),
            ("My foundation cracked. Can appraisal help?", "Foundation movement from expansive Yazoo clay is usually excluded. If a covered event such as a plumbing leak or tree strike caused the damage and the carrier accepts coverage, appraisal can address the amount of that loss."),
        ],
    },
    # 2 ─────────────────────────────────────────────────────────────
    {
        "slug": "gulfport-harrison-county",
        "city": "Gulfport",
        "county": "Harrison County",
        "region": "Gulf Coast",
        "kw": "insurance appraiser gulfport ms",
        "title": "Insurance Appraiser Gulfport, MS | Wind & Hurricane Claims",
        "desc": "Insurance appraiser in Gulfport, MS for hurricane, wind and MWUA claim disputes across Harrison County and the Coast.",
        "h1": "Gulfport Hurricane and Wind Claim Appraisal",
        "lede": "On the Coast, one storm can mean two or three policies, a percentage deductible and a fight over wind versus water. If you and your carrier can’t agree on the amount of your Gulfport loss, appraisal is one way to settle it.",
        "perils": [
            "Hurricane wind and storm surge",
            "Split homeowners and MWUA wind policies",
            "Named-storm percentage deductibles",
            "Roof and siding damage from tropical storms",
            "Flood losses under separate NFIP policies",
        ],
        "neighborhoods": ["Downtown Gulfport", "Handsboro", "Orange Grove", "Bayou View", "North Gulfport", "Long Beach"],
        "housing": "Gulfport has raised and elevated homes rebuilt to post-Katrina standards near the beach, older cottages and brick homes in established neighborhoods, and newer subdivisions to the north toward Interstate 10.",
        "storms": [
            ("Aug 17, 1969", "Hurricane Camille’s Category 5 landfall to the west near Pass Christian"),
            ("Aug 29, 2005", "Hurricane Katrina’s surge and wind"),
            ("Aug 2012", "Hurricane Isaac’s rain and surge"),
            ("Oct 28, 2020", "Hurricane Zeta’s strong wind across the Coast"),
        ],
        "near": ["biloxi-harrison-county", "pascagoula-jackson-county", "hattiesburg-forrest-county"],
        "body": """<h2>Gulfport, Harrison County and the split-policy problem</h2>
<p>Gulfport is one of Harrison County’s two county seats (Biloxi is the other) and home to the state port. Harrison County is one of the six southernmost counties where the Mississippi Windstorm Underwriting Association (MWUA) writes wind and hail coverage. Many Gulfport owners carry a homeowners policy that excludes wind, an MWUA wind policy, and a separate flood policy, usually through the NFIP.</p>
<p>That arrangement shapes every storm claim. Each carrier writes its own estimate, applies its own deductible and tends to point at the other policy for the damage in between.</p>

<h2>Katrina, Zeta and what the Coast learned</h2>
<p>Hurricane Katrina’s surge on August 29, 2005 pushed far inland across Gulfport, Long Beach and Pass Christian, and wind damage reached well past the surge line. It produced years of wind-versus-water disputes and arguments over anti-concurrent-causation clauses. Our guide on <a href="/claim-advice/wind-vs-water-after-katrina/">wind vs. water after Katrina</a> walks through that history.</p>
<p>More recent storms have been smaller but still costly. Hurricane Isaac in August 2012 brought heavy rain and surge. Hurricane Zeta made landfall in Louisiana on October 28, 2020, but drove strong wind across the Mississippi Coast, tearing shingles, soffits and fences in Gulfport neighborhoods.</p>
<div class="callout"><b class="callout-t">Coverage vs. amount</b><p>Whether damage was caused by wind or by water is often a coverage question, and appraisal does not decide coverage. Appraisal can, however, set the dollar amount of the wind damage, or of each part of a loss, when the policy allows it.</p></div>

<h2>Gulfport homes and the estimates they produce</h2>
<p>Areas like Handsboro, Orange Grove, Bayou View and Downtown Gulfport show the whole range: historic cottages, mid-century brick homes, and the raised homes built after 2005 on piers or pilings. North Gulfport and the subdivisions along the Interstate 10 corridor are newer and mostly slab-on-grade.</p>
<p>The disputes we see most often on Gulfport claims:</p>
<ul>
<li><strong>Deductible math:</strong> a 2% to 5% named-storm deductible on Coverage A can wipe out a partial-roof estimate. Our <a href="/claim-calculator-suite/named-storm-deductible-calculator/">named-storm deductible calculator</a> shows where your number lands.</li>
<li><strong>Elevated-home access:</strong> raised homes need lifts, scaffolding and longer labor time. Carrier estimates often price them like a one-story slab house.</li>
<li><strong>Code upgrades:</strong> repairs may trigger current wind-load and elevation requirements. Ordinance or law coverage, if you have it, may pay for those.</li>
<li><strong>Partial roof replacement:</strong> when matching shingles aren’t available, a patch leaves a roof that doesn’t match.</li>
<li><strong>Allocation:</strong> interior damage gets assigned to flood when the roof opening says wind.</li>
</ul>

<h2>When appraisal fits a Gulfport claim</h2>
<p>Appraisal is most useful when coverage is accepted and the fight is over price and scope. Each policy has its own appraisal clause, so a wind-policy appraisal and a homeowners-policy appraisal can be separate tracks. Read the clause first. Our <a href="/our-appraisal-services/hurricane-named-storm-appraisal/">hurricane and named-storm appraisal</a> service covers how we handle split-policy claims.</p>
<p>We serve Long Beach and Pass Christian as well, and the rest of Harrison County. Policy and legal deadlines keep running during a dispute, so confirm yours with a Mississippi attorney.</p>""",
        "faqs": [
            ("Can I demand appraisal on my MWUA wind policy?", "If your MWUA policy contains an appraisal clause, you can generally use it for a dispute over the amount of a covered wind loss. Read the clause for its exact steps and deadlines, and keep in mind that each policy is handled separately."),
            ("Does appraisal decide whether my Gulfport damage was wind or flood?", "No. Whether wind or water caused a loss is generally a coverage question. Appraisal sets the amount of loss, and in some cases the amount of each part of a loss, which can still help narrow a wind-versus-water dispute."),
        ],
    },
    # 3 ─────────────────────────────────────────────────────────────
    {
        "slug": "biloxi-harrison-county",
        "city": "Biloxi",
        "county": "Harrison County",
        "region": "Gulf Coast",
        "kw": "biloxi insurance appraiser",
        "title": "Biloxi Insurance Appraiser | Harrison County Storm Claims",
        "desc": "Biloxi insurance appraiser for homeowners, rental owners and businesses with disputed hurricane, wind and water claims.",
        "h1": "Biloxi Property Claim Appraisal, From Point Cadet to Woolmarket",
        "lede": "Biloxi has taken direct hits from Camille, Katrina and Nate, and every one left behind arguments over what repairs really cost. If your carrier’s estimate is short, appraisal may be the quickest fair way to settle it.",
        "perils": [
            "Hurricane surge and wind along the beachfront and Back Bay",
            "Wind-driven rain through roofs and windows",
            "Split wind and homeowners policy disputes",
            "Commercial and hospitality property losses",
            "Mold after delayed water mitigation",
        ],
        "neighborhoods": ["East Biloxi", "Point Cadet", "Back Bay", "West Biloxi", "Woolmarket", "Downtown Biloxi"],
        "housing": "Biloxi’s housing ranges from historic cottages and shotgun houses in East Biloxi to raised post-Katrina rebuilds, mid-century homes near Keesler, and newer subdivisions north of the Back Bay in Woolmarket.",
        "storms": [
            ("Aug 17, 1969", "Hurricane Camille’s Category 5 landfall to the west"),
            ("Aug 29, 2005", "Hurricane Katrina’s catastrophic surge and wind"),
            ("Oct 2017", "Hurricane Nate’s Category 1 landfall near Biloxi"),
            ("Oct 28, 2020", "Hurricane Zeta’s wind across the Coast"),
        ],
        "near": ["gulfport-harrison-county", "pascagoula-jackson-county", "hattiesburg-forrest-county"],
        "body": """<h2>Biloxi’s storm record</h2>
<p>Biloxi shares county-seat status in Harrison County with Gulfport and sits on a peninsula between the Mississippi Sound and the Back Bay. Water on two sides means storms hit from more than one direction.</p>
<ul>
<li><strong>Hurricane Camille, August 17, 1969:</strong> a Category 5 landfall to the west near Pass Christian and Bay St. Louis, with heavy damage in Biloxi.</li>
<li><strong>Hurricane Katrina, August 29, 2005:</strong> surge swept East Biloxi and Point Cadet and pushed into the Back Bay, while wind damaged roofs across the city.</li>
<li><strong>Hurricane Nate, October 2017:</strong> a Category 1 landfall near Biloxi, with surge along the beachfront and wind damage to roofs and signs.</li>
<li><strong>Hurricane Zeta, October 28, 2020:</strong> landfall in Louisiana, but strong wind across the whole Mississippi Coast.</li>
</ul>
<p>Katrina in particular left a long trail of wind-versus-water fights. Those coverage questions are outside what appraisal decides, but the dollar amount of each piece of damage is not.</p>

<h2>East Biloxi, Point Cadet and the rest of the city</h2>
<p>East Biloxi and Point Cadet are the city’s oldest neighborhoods, with cottages, shotgun houses and seafood-industry roots. Many lots there were rebuilt after 2005, often raised. West Biloxi and the areas around Keesler Air Force Base hold a lot of mid-century homes and rentals. Woolmarket, north of the Back Bay, is newer and more suburban. Downtown Biloxi mixes older commercial buildings with newer construction.</p>
<p>Biloxi is also a hospitality city. The casino resorts and hotels along the beach and the Back Bay, plus the restaurants, shops and rental property that serve them, produce large commercial claims. For those, see our <a href="/our-appraisal-services/commercial-hoa-appraisal/">commercial and HOA appraisal</a> service.</p>

<h2>Common estimate gaps on Biloxi claims</h2>
<h3>Homes and rentals</h3>
<ul>
<li>Raised homes priced without the lifts, staging and extra labor they require.</li>
<li>Wind-driven rain damage written as a small ceiling patch when insulation, drywall and flooring were soaked.</li>
<li>Mold remediation limited by a policy sublimit, with the remaining tear-out left out of the estimate.</li>
<li>Older cottages with wood siding and trim profiles that standard pricing doesn’t match.</li>
</ul>
<h3>Commercial and hospitality property</h3>
<ul>
<li>Roof systems on large flat or low-slope buildings measured short or repaired in patches.</li>
<li>Exterior finishes and signage on storm-exposed buildings left off the estimate.</li>
<li>Disputes over how many units, rooms or floors a loss actually reached.</li>
</ul>
<div class="callout"><b class="callout-t">Two policies, two deductibles</b><p>Biloxi is inside the MWUA territory. If your wind coverage is separate, expect a separate wind deductible, often a percentage of Coverage A. Run your numbers before you decide whether appraisal is worth it.</p></div>

<h2>Working a Biloxi claim through appraisal</h2>
<p>We review the carrier’s estimate, build a line-by-line scope and, if your policy has an appraisal clause and the dispute is about amount, represent you through the process. The <a href="/claim-advice/coast-hurricane-deductibles-explained/">Coast hurricane deductibles guide</a> is a good place to start before you file a demand.</p>
<p>We also serve D’Iberville and Ocean Springs across the Back Bay and the bay bridge. Confirm any deadline with a Mississippi attorney.</p>""",
        "faqs": [
            ("Do you handle casino, hotel and commercial claims in Biloxi?", "Yes. We work commercial, HOA and condominium claims as well as homeowner claims. Larger losses often involve more complex roof systems, multiple buildings and business owners with their own appraisal clause terms."),
            ("I live near Keesler and rent my house out. Can I still use appraisal?", "If your landlord or dwelling policy has an appraisal clause and you and your carrier disagree on the amount of a covered loss, you can generally invoke it. Check the clause wording for notice and timing requirements."),
        ],
    },
    # 4 ─────────────────────────────────────────────────────────────
    {
        "slug": "hattiesburg-forrest-county",
        "city": "Hattiesburg",
        "county": "Forrest County",
        "region": "Pine Belt",
        "kw": "hattiesburg insurance appraisal",
        "title": "Hattiesburg Insurance Appraisal | Forrest & Lamar County",
        "desc": "Hattiesburg insurance appraisal for tornado, wind and tree-fall claim disputes in Forrest and Lamar counties and the Pine Belt.",
        "h1": "Insurance Appraisal for Hattiesburg and the Pine Belt",
        "lede": "Hattiesburg sits in tornado country and in pine country, a combination that keeps roofers and adjusters busy. When your carrier underpays a Hattiesburg wind or tree claim, appraisal is a way to resolve the amount.",
        "perils": [
            "Tornadoes and spring severe storms",
            "Pine trees falling on roofs, cars and outbuildings",
            "Inland hurricane wind",
            "Hail on shingle and metal roofs",
            "Water losses after roof openings",
        ],
        "neighborhoods": ["The Avenues", "Downtown Hattiesburg", "Midtown", "West Hattiesburg", "Oak Grove", "Petal"],
        "housing": "Hattiesburg has early-1900s homes in The Avenues historic district, brick ranches near the university, student rentals, and newer slab-on-grade subdivisions in Lamar County and Oak Grove.",
        "storms": [
            ("Aug 29, 2005", "Hurricane Katrina’s inland wind and widespread pine fall"),
            ("Feb 10, 2013", "EF4 tornado across Oak Grove, the university and Hattiesburg"),
            ("Apr 12, 2020", "Easter Sunday outbreak with wide damage in the Pine Belt"),
        ],
        "near": ["gulfport-harrison-county", "jackson-hinds-county", "meridian-lauderdale-county"],
        "body": """<h2>Hattiesburg at a glance</h2>
<p>Hattiesburg is the county seat of Forrest County, and the city extends west into Lamar County. It is the hub of the Pine Belt and home to the University of Southern Mississippi. Petal sits just across the Leaf River, and Oak Grove spreads out to the west in Lamar County.</p>
<p>For property claims, the defining features are tall pines, an active tornado season and a location close enough to the Coast to catch hurricane wind. Hattiesburg is north of the MWUA territory, so wind is usually covered under the homeowners policy itself, though some policies carry a separate wind or hurricane deductible. Read your declarations page before you compare numbers.</p>

<h2>Storms that shaped Hattiesburg claims</h2>
<h3>Hurricane Katrina, 2005</h3>
<p>Katrina’s wind on August 29, 2005 stayed strong well inland. In Hattiesburg it snapped and uprooted pines across the city, punching holes in roofs and crushing carports and sheds. Many of those claims turned on tree removal limits and on whether interior water damage was fully scoped.</p>
<h3>February 10, 2013 tornado</h3>
<p>An EF4 tornado tracked through Oak Grove, across the University of Southern Mississippi campus and into Hattiesburg neighborhoods. Damage ranged from total losses to roofs and siding peeled back blocks away from the center of the path.</p>
<h3>Easter Sunday, April 12, 2020</h3>
<p>The Easter outbreak produced an EF4 near Bassfield and Soso and caused wide damage across the Pine Belt, including the Hattiesburg area.</p>

<h2>Neighborhoods and housing</h2>
<p>The Avenues historic district, near downtown, has large early-1900s homes with wood siding, porches and plaster interiors. Downtown Hattiesburg and Midtown mix older homes with commercial buildings. West Hattiesburg, along the busy commercial corridors toward the university, has brick ranches and rental property. Oak Grove and the Lamar County side are mostly newer subdivisions on slabs.</p>
<p>Those differences show up in the estimates:</p>
<ul>
<li><strong>Historic homes in The Avenues:</strong> wood siding, trim and plaster priced as vinyl and drywall.</li>
<li><strong>Tree strikes:</strong> many policies limit debris removal per tree and per occurrence, and estimates sometimes skip the framing repair under the impact point.</li>
<li><strong>Tornado damage on newer homes:</strong> partial roof and siding replacements that leave mismatched elevations.</li>
<li><strong>Student rentals:</strong> contents and loss-of-rent disputes on top of the building claim.</li>
</ul>
<div class="callout"><b class="callout-t">Photograph before cleanup</b><p>After a tornado or tree strike, document everything before debris moves: the tree, the roof, the attic, every room. Our <a href="/claim-advice/documenting-tornado-damage/">tornado documentation guide</a> lists what an appraiser will want to see.</p></div>

<h2>How appraisal helps in the Pine Belt</h2>
<p>If coverage is accepted and the disagreement is about how much the repair costs, the appraisal clause lets each side name an independent appraiser, with an umpire to break a tie. We handle <a href="/our-appraisal-services/tornado-wind-damage-appraisal/">tornado and wind damage appraisal</a> and <a href="/our-appraisal-services/fallen-tree-claim-appraisal/">fallen tree claims</a> across Hattiesburg, Petal and the surrounding counties.</p>
<p>Policy deadlines still run while you negotiate. Confirm yours with a Mississippi attorney.</p>""",
        "faqs": [
            ("A pine fell on my Hattiesburg house. Why is the tree removal payment so low?", "Many homeowners policies cap debris removal for trees, often per tree and per occurrence. The repair of the house itself is a separate part of the claim, and if the carrier’s repair estimate is short, that amount can be disputed through appraisal."),
            ("Do you cover Oak Grove and Petal?", "Yes. We work claims in Hattiesburg, Oak Grove, Petal and across Forrest and Lamar counties, and throughout the Pine Belt."),
        ],
    },
    # 5 ─────────────────────────────────────────────────────────────
    {
        "slug": "southaven-desoto-county",
        "city": "Southaven",
        "county": "DeSoto County",
        "region": "North Mississippi",
        "kw": "insurance appraiser southaven ms",
        "title": "Insurance Appraiser Southaven, MS | DeSoto County Claims",
        "desc": "Insurance appraiser in Southaven, MS for hail, wind and ice storm claim disputes in DeSoto County, from Horn Lake to Olive Branch.",
        "h1": "Southaven and DeSoto County Claim Appraisal",
        "lede": "DeSoto County grew fast, and so did its roofs. When hail, straight-line wind or ice damages your Southaven home and the carrier’s estimate falls short, appraisal can settle the amount.",
        "perils": [
            "Hail on architectural shingles",
            "Straight-line wind from spring and summer storms",
            "Ice storms and tree limb damage",
            "Frozen pipes during hard freezes",
            "Siding and gutter damage",
        ],
        "neighborhoods": ["Greenbrook", "Goodman Road corridor", "Stateline Road area", "Horn Lake", "Olive Branch", "Hernando"],
        "housing": "Southaven is mostly brick-front and vinyl-sided subdivision homes built from the 1980s through the 2000s, with newer construction spreading south and east across DeSoto County.",
        "storms": [
            ("Feb 1994", "North Mississippi ice storm with heavy tree and power-line damage"),
            ("Feb 2021", "Winter storm and statewide freeze, with burst pipes"),
            ("Dec 2022", "Hard freeze and frozen-pipe losses"),
        ],
        "near": ["oxford-lafayette-county", "tupelo-lee-county", "greenville-washington-county"],
        "body": """<h2>Southaven in DeSoto County</h2>
<p>Southaven sits at the top of the state, just across the line from Memphis, Tennessee, and is one of Mississippi’s largest cities. DeSoto County’s seat is Hernando, a few miles south. Along with Olive Branch and Horn Lake, Southaven has grown into the Mississippi side of the Memphis metro.</p>
<p>Because so many homes here were built in the same era with similar materials, a single storm can damage many similar roofs at once. Carriers often bring in out-of-area adjusters after a large hail event, and their estimates can vary widely from street to street.</p>
<p>Two roads frame much of the city. Stateline Road runs along the northern edge, and Goodman Road carries most of the retail and traffic east and west. Interstate 55 runs through the middle.</p>

<h2>What damages Southaven homes</h2>
<p>Southaven doesn’t see hurricanes, but it sees almost everything else:</p>
<ul>
<li><strong>Hail:</strong> spring storms drop hail that bruises and cracks architectural shingles, dents gutters and splits vinyl siding.</li>
<li><strong>Straight-line wind:</strong> severe thunderstorms push wind strong enough to lift shingles, topple fences and drop limbs.</li>
<li><strong>Ice:</strong> the February 1994 ice storm brought down trees and power lines across North Mississippi. The February 2021 winter storm added ice, snow and burst pipes.</li>
<li><strong>Freeze:</strong> the December 2022 hard freeze caught plumbing in attics and outside walls.</li>
</ul>

<h2>The subdivision roof dispute</h2>
<p>Most of Southaven was built between the 1980s and the 2000s, in subdivisions like Greenbrook and the neighborhoods along Goodman Road and Stateline Road. Those homes tend to share the same builder-grade materials. That creates a predictable set of arguments after a hail or wind storm.</p>
<h3>Repair or replace</h3>
<p>Carriers often approve a few slopes or a set number of shingles. If the shingle line is discontinued or the color has faded, a partial repair won’t match. Whether matching is owed depends on your policy, but the cost of a proper repair is the kind of amount dispute appraisal handles.</p>
<h3>Measurements and waste</h3>
<p>Roof square counts, pitch and waste factor drive the whole roof estimate. Short measurements carry through every line. Our <a href="/claim-calculator-suite/roof-pitch-squares-calculator/">roof pitch and squares calculator</a> helps you check the carrier’s numbers.</p>
<h3>Hail on soft metals and siding</h3>
<p>Estimates sometimes include gutters and downspouts but leave off vents, flashing, window wraps or vinyl siding on the storm-facing side.</p>
<div class="callout"><b class="callout-t">Depreciation and holdback</b><p>Many DeSoto County roof claims are paid on an actual cash value basis first, with depreciation held back until the work is done. Track deadlines for recovering that holdback; they are often in your policy.</p></div>

<h2>Getting a fair number</h2>
<p>If your carrier accepts the claim but the estimate doesn’t cover a real repair, we can review it and, where your policy allows, represent you in appraisal. Our <a href="/our-appraisal-services/roof-hail-claim-appraisal/">roof and hail claim appraisal</a> service is built around exactly these subdivision roof disputes.</p>
<p>We work across DeSoto County, including Olive Branch, Horn Lake and Hernando. Confirm any filing deadline with a Mississippi attorney.</p>""",
        "faqs": [
            ("My carrier will only replace part of my Southaven roof. Is that appraisal?", "It can be. If the carrier accepts that hail or wind damaged the roof but disagrees on how much repair is needed or what it costs, that is an amount-of-loss dispute. Whether matching is required depends on your policy language."),
            ("Do you serve Olive Branch, Horn Lake and Hernando?", "Yes. We work claims throughout DeSoto County and the rest of Mississippi."),
        ],
    },
    # 6 ─────────────────────────────────────────────────────────────
    {
        "slug": "tupelo-lee-county",
        "city": "Tupelo",
        "county": "Lee County",
        "region": "North Mississippi",
        "kw": "tupelo insurance appraiser",
        "title": "Tupelo Insurance Appraiser | Lee County Tornado & Hail",
        "desc": "Tupelo insurance appraiser for tornado, hail and wind claim disputes on homes and businesses across Lee County.",
        "h1": "Tupelo Tornado, Wind and Hail Claim Appraisal",
        "lede": "Tupelo knows tornadoes, from 1936 to 2014. If your Tupelo home or business was damaged and your carrier’s estimate won’t cover the repair, appraisal can resolve the amount.",
        "perils": [
            "Tornadoes and spring severe weather",
            "Hail on shingle and metal roofs",
            "Ice and tree damage in winter storms",
            "Commercial and industrial roof losses",
        ],
        "neighborhoods": ["Downtown Tupelo", "Fairpark", "East Tupelo", "Joyner", "Mill Village", "Saltillo"],
        "housing": "Tupelo has older homes near downtown, a large stock of post-war and mid-century brick ranches, newer subdivisions on the edges of town, and commercial and manufacturing buildings tied to the furniture industry.",
        "storms": [
            ("Apr 5, 1936", "Tupelo tornado, one of the deadliest in US history"),
            ("Feb 1994", "North Mississippi ice storm"),
            ("Apr 28, 2014", "EF3 tornado through Tupelo"),
            ("Feb 2021", "Winter storm and statewide freeze"),
        ],
        "near": ["oxford-lafayette-county", "columbus-lowndes-county", "southaven-desoto-county"],
        "body": """<h2>A city rebuilt by storms</h2>
<p>Tupelo is the county seat of Lee County and the commercial center of northeast Mississippi. It is known for the Elvis Presley birthplace in East Tupelo, for the Natchez Trace Parkway, and for a long run as a center of upholstered furniture manufacturing.</p>
<p>Tupelo’s mix of older neighborhoods, post-war housing, retail corridors and industrial buildings means a single storm can produce very different claims within a few blocks: a homeowner arguing over brick and decking, and a plant owner arguing over a large roof system.</p>
<p>It is also known for tornadoes. On April 5, 1936, a tornado tore through the city and became one of the deadliest in US history. Much of what was rebuilt after that storm, and the post-war neighborhoods that followed, still stands.</p>
<p>On April 28, 2014, the same day an EF4 struck Louisville in Winston County, an EF3 tornado crossed Tupelo, damaging homes, businesses and trees along its path.</p>

<h2>Where Tupelo claims come from</h2>
<ul>
<li><strong>Tornadoes and straight-line wind:</strong> spring storms remain the biggest single source of large claims.</li>
<li><strong>Hail:</strong> storms tracking across northeast Mississippi damage shingle and metal roofs alike.</li>
<li><strong>Ice and freeze:</strong> the February 1994 ice storm and the February 2021 winter storm both brought down limbs and burst pipes.</li>
<li><strong>Commercial losses:</strong> large low-slope and metal roofs on manufacturing, warehouse and retail buildings.</li>
</ul>

<h2>Tupelo homes and the gaps in their estimates</h2>
<p>Downtown Tupelo and the Fairpark district hold the city’s older core. East Tupelo, Joyner and the Mill Village area include older and mid-century houses on established lots. Newer subdivisions have spread outward toward Saltillo and other parts of Lee County.</p>
<p>The post-war and mid-century brick ranch is the most common house we see in Tupelo claims. On those homes, the recurring problems are:</p>
<ul>
<li><strong>Brick repair:</strong> estimates assume matching brick is available when the original brick has long been discontinued.</li>
<li><strong>Roof decking:</strong> older plank decking under a tornado-damaged roof is often left out of the scope.</li>
<li><strong>Code items:</strong> a re-roof or partial rebuild may trigger current code requirements that the estimate ignores.</li>
<li><strong>Interior water:</strong> rain through a tornado-damaged roof, scoped as a few ceiling stains.</li>
</ul>
<h3>Commercial and industrial property</h3>
<p>For furniture plants, warehouses and retail buildings, the disputes are larger but similar in kind: roof area, system type, and whether a section can be repaired or must be replaced. Our <a href="/our-appraisal-services/commercial-hoa-appraisal/">commercial and HOA appraisal</a> service covers those claims.</p>

<h2>Starting the process in Tupelo</h2>
<p>Before you demand appraisal, gather your policy, the carrier’s estimate, photos and any contractor bids. Our <a href="/claim-calculator-suite/appraisal-readiness-checkup/">appraisal readiness checkup</a> walks through what you need. If the gap is real, we can represent you through the appraisal clause, from the written demand to the award. See our <a href="/our-appraisal-services/tornado-wind-damage-appraisal/">tornado and wind damage appraisal</a> service for details.</p>
<p>Policy and legal deadlines keep running, so confirm yours with a Mississippi attorney.</p>""",
        "faqs": [
            ("Can appraisal help with a commercial or manufacturing building in Tupelo?", "Yes, if the commercial policy has an appraisal clause and the dispute is about the amount of a covered loss. Large roof systems and multi-building sites are common subjects of commercial appraisal."),
            ("Do you work claims outside the Tupelo city limits?", "Yes. We work claims across Lee County, including Saltillo, and throughout Mississippi."),
        ],
    },
    # 7 ─────────────────────────────────────────────────────────────
    {
        "slug": "meridian-lauderdale-county",
        "city": "Meridian",
        "county": "Lauderdale County",
        "region": "East Central",
        "kw": "insurance appraiser meridian ms",
        "title": "Insurance Appraiser in Meridian, MS | Lauderdale County",
        "desc": "Insurance appraiser in Meridian, MS for wind, tornado, tree and water claim disputes on homes and businesses in Lauderdale County.",
        "h1": "Meridian Property Insurance Appraiser",
        "lede": "Meridian’s older homes and tall trees make for complicated claims when spring storms roll through. If your carrier’s estimate doesn’t match the real repair cost, appraisal is one way to settle it.",
        "perils": [
            "Spring severe storms and tornadoes",
            "Trees falling on older homes",
            "Inland hurricane wind",
            "Hail on roofs",
            "Frozen pipes in older plumbing",
        ],
        "neighborhoods": ["Downtown Meridian", "Highland Park", "Poplar Springs", "East End", "Marion", "Collinsville"],
        "housing": "Meridian has a historic downtown and early-twentieth-century homes in its older neighborhoods, mid-century brick ranches across the city, and newer homes in the outlying parts of Lauderdale County.",
        "storms": [
            ("Aug 29, 2005", "Hurricane Katrina’s inland wind and tree damage"),
            ("Feb 2021", "Winter storm and statewide freeze"),
            ("Dec 2022", "Hard freeze and frozen-pipe losses"),
        ],
        "near": ["jackson-hinds-county", "hattiesburg-forrest-county", "columbus-lowndes-county"],
        "body": """<h2>Meridian and Lauderdale County</h2>
<p>Meridian is the county seat of Lauderdale County and the largest city in East Central Mississippi, near the eastern state line. Interstates 20 and 59 meet here, and Naval Air Station Meridian, a Navy jet training base, sits northeast of the city. The base brings a steady flow of military families, many of them renting or buying for a few years at a time.</p>
<p>Meridian is far from the Coast, but not far enough to escape hurricanes. When Katrina came ashore on August 29, 2005, its wind was still strong as it reached the Meridian area, bringing down trees and power lines and damaging roofs across the county.</p>

<h2>The older side of Meridian</h2>
<p>Downtown Meridian has a collection of historic commercial buildings from the city’s railroad era. Neighborhoods such as Highland Park, Poplar Springs and the East End include early-twentieth-century homes with wood siding, porches, plaster and hardwood floors. Elsewhere in the city and out toward Marion and Collinsville, brick ranches and newer homes are more common.</p>
<p>Older homes raise their own estimate problems:</p>
<ul>
<li><strong>Plaster walls and ceilings</strong> priced as drywall, without the labor and materials a true plaster repair takes.</li>
<li><strong>Wood siding and trim</strong> that can’t be bought off the shelf and has to be milled or matched.</li>
<li><strong>Old-growth framing</strong> and plank roof decking left out of the scope after a tree strike.</li>
<li><strong>Older plumbing</strong> where a freeze-related break leads to water damage through several rooms.</li>
<li><strong>Code upgrades</strong> on electrical or framing when a large section is opened up.</li>
</ul>

<h2>Storm seasons in East Central Mississippi</h2>
<h3>Spring and fall severe weather</h3>
<p>Most of Meridian’s wind and hail claims come from spring storm systems, with a smaller second season in late fall. Tornadoes, straight-line wind and hail can all appear in the same event.</p>
<h3>Trees</h3>
<p>Mature oaks and pines line many Meridian streets. When they fall, the claim usually has two parts: removing the tree, which many policies limit per tree and per occurrence, and repairing the house, which has no such small cap. Our <a href="/our-appraisal-services/fallen-tree-claim-appraisal/">fallen tree claim appraisal</a> page covers both.</p>
<h3>Freeze</h3>
<p>The February 2021 winter storm and the December 2022 hard freeze both brought frozen-pipe claims, especially in older homes with plumbing in crawlspaces and exterior walls.</p>
<div class="callout"><b class="callout-t">For military households</b><p>If you are transferring away from NAS Meridian while a claim is open, keep copies of your policy, estimates and photos, and note every deadline before you move. An appraisal can generally continue after you relocate.</p></div>

<h2>Our role on a Meridian claim</h2>
<p>We review the carrier’s estimate line by line, build a scope that matches your home and, when coverage is accepted and the dispute is about amount, represent you through the policy’s appraisal clause. The <a href="/claim-advice/line-by-line-estimate-reading/">line-by-line estimate reading guide</a> shows what we look for.</p>
<p>Confirm your claim deadlines with a Mississippi attorney.</p>""",
        "faqs": [
            ("Was Meridian affected by Hurricane Katrina?", "Yes. Katrina’s wind remained strong far inland and caused tree and roof damage in the Meridian area. Inland hurricane claims often involve tree fall and wind-driven rain rather than surge."),
            ("Can you help with an older or historic Meridian home?", "Yes. Older homes often have plaster, wood siding, plank decking and trim that standard estimates underprice. We build a scope that reflects how the house was actually built."),
        ],
    },
    # 8 ─────────────────────────────────────────────────────────────
    {
        "slug": "oxford-lafayette-county",
        "city": "Oxford",
        "county": "Lafayette County",
        "region": "North Mississippi",
        "kw": "oxford ms insurance appraiser",
        "title": "Oxford, MS Insurance Appraiser | Lafayette County Claims",
        "desc": "Oxford MS insurance appraiser for homeowners, condo and student rental owners with disputed hail, wind, ice and water claims.",
        "h1": "Claim Appraisal for Oxford Homes, Condos and Rentals",
        "lede": "Oxford has grown fast around the University of Mississippi, and a lot of its newer property is condos and rentals. When hail, wind or ice damages your Oxford property and the carrier underpays, appraisal can help settle the amount.",
        "perils": [
            "Hail and straight-line wind",
            "Tornadoes in spring storm systems",
            "Ice storms and tree limb damage",
            "Frozen pipes in rentals left empty over breaks",
            "Water damage spreading between condo units",
        ],
        "neighborhoods": ["The Square", "North Lamar", "South Lamar", "University Avenue", "Grand Oaks", "Taylor"],
        "housing": "Oxford mixes older homes near the Square and campus, condo complexes and student rentals, newer single-family subdivisions, and rural homes across Lafayette County.",
        "storms": [
            ("Feb 1994", "North Mississippi ice storm with massive tree and power-line damage"),
            ("Feb 2021", "Winter storm with ice, snow and burst pipes"),
            ("Dec 2022", "Hard freeze and frozen-pipe losses"),
        ],
        "near": ["southaven-desoto-county", "tupelo-lee-county", "greenville-washington-county"],
        "body": """<h2>Oxford, Lafayette County and Ole Miss</h2>
<p>Oxford is the county seat of Lafayette County and home to the University of Mississippi. The courthouse Square sits at the center of town, with older homes along North and South Lamar and the streets running toward campus on University Avenue. Beyond that core, Oxford has added condo complexes, apartment-style rentals and subdivisions like Grand Oaks, while small communities such as Taylor sit just outside town.</p>
<p>That mix of property, much of it owned by people who don’t live in it full time, shapes the claims we see.</p>

<h2>Weather that drives Oxford claims</h2>
<ul>
<li><strong>Ice:</strong> the February 1994 ice storm coated North Mississippi and brought down trees and power lines for weeks. The February 2021 winter storm brought ice, snow and frozen pipes.</li>
<li><strong>Freeze:</strong> the December 2022 hard freeze hit during winter break, when many rentals and condos were empty.</li>
<li><strong>Hail and wind:</strong> spring storms bring hail, straight-line wind and occasional tornadoes across Lafayette County.</li>
</ul>
<p>Our guide to <a href="/claim-advice/ice-storm-tree-claims-north-mississippi/">ice storm and tree claims in North Mississippi</a> covers how those losses are usually handled.</p>

<h2>Condos, rentals and student housing</h2>
<h3>Who owns what</h3>
<p>In a condo, the association’s master policy and your unit-owner policy each cover part of the building. Read your declarations and bylaws to see where the line falls for walls, floors, cabinets and fixtures. When a pipe bursts upstairs and water runs through three units, each policy may produce its own estimate and its own dispute.</p>
<h3>Empty units and frozen pipes</h3>
<p>Many policies include conditions about maintaining heat in a vacant or unoccupied unit. Whether a freeze loss is covered is a coverage question, not an appraisal question. Once coverage is accepted, the scope of drying, tear-out and rebuild is fair game.</p>
<h3>Loss of rent and contents</h3>
<p>Landlord policies often include fair rental value coverage. Furnished rentals add a contents claim. Both can be underestimated when repairs drag on.</p>

<h2>Common estimate disputes in Oxford</h2>
<ul>
<li>Hail damage on condo roofs written as spot repairs across buildings that share one roof system.</li>
<li>Water losses scoped for one unit when moisture readings show it reached the units below.</li>
<li>Older homes near the Square priced with modern materials that don’t match the original trim and finishes.</li>
<li>Ice-related limb damage where the roof repair is approved but the gutter, fascia and siding work is left out.</li>
</ul>
<div class="callout"><b class="callout-t">HOAs and associations</b><p>An association disputing a master-policy claim follows its own policy’s appraisal clause. Our <a href="/our-appraisal-services/commercial-hoa-appraisal/">commercial and HOA appraisal</a> service handles association claims.</p></div>

<h2>How we can help</h2>
<p>Whether you live in Oxford year-round or own a rental from out of town, we can review your carrier’s estimate and, where your policy allows, represent you through appraisal. Start with the <a href="/our-appraisal-services/ice-storm-freeze-appraisal/">ice storm and freeze appraisal</a> service if your loss came from cold weather. Confirm any deadline with a Mississippi attorney.</p>""",
        "faqs": [
            ("I own a student rental in Oxford and live out of town. Can you still help?", "Yes. We can review the carrier’s estimate and handle the appraisal process with you remotely, coordinating access to the property as needed."),
            ("A burst pipe damaged several condo units. Whose policy pays?", "That depends on the association’s master policy, your unit-owner policy and the condo documents. Appraisal does not decide which policy covers what, but it can settle the amount of loss under a policy once coverage is accepted."),
        ],
    },
    # 9 ─────────────────────────────────────────────────────────────
    {
        "slug": "pascagoula-jackson-county",
        "city": "Pascagoula",
        "county": "Jackson County",
        "region": "Gulf Coast",
        "kw": "pascagoula insurance appraiser",
        "title": "Pascagoula Insurance Appraiser | Jackson County Coast",
        "desc": "Pascagoula insurance appraiser for hurricane, wind and MWUA claim disputes in coastal Jackson County, Moss Point and Gautier.",
        "h1": "Pascagoula and Coastal Jackson County Claim Appraisal",
        "lede": "Pascagoula sits on the eastern end of the Mississippi Coast, where surge, wind and split policies all meet. If your carrier’s estimate won’t pay for a proper repair, appraisal can settle the amount.",
        "perils": [
            "Hurricane surge and wind",
            "MWUA wind policy disputes",
            "Named-storm percentage deductibles",
            "River and bayou flooding",
            "Wind-driven rain and roof damage",
        ],
        "neighborhoods": ["Downtown Pascagoula", "Beach Boulevard", "Moss Point", "Gautier", "Escatawpa", "Vancleave"],
        "housing": "Coastal Jackson County has raised homes rebuilt after Katrina, older brick and frame homes from the shipyard boom years, manufactured homes in rural areas, and newer subdivisions inland.",
        "storms": [
            ("Aug 29, 2005", "Hurricane Katrina’s storm surge and wind"),
            ("Aug 2012", "Hurricane Isaac’s rain and surge"),
            ("Oct 28, 2020", "Hurricane Zeta’s strong wind across the Coast"),
        ],
        "near": ["biloxi-harrison-county", "gulfport-harrison-county", "hattiesburg-forrest-county"],
        "body": """<h2>Jackson County, not the city of Jackson</h2>
<p>A quick clarification first: Jackson County is the easternmost coastal county in Mississippi. It is not the city of Jackson, which sits in Hinds County in the middle of the state. Pascagoula is the county seat of Jackson County, at the mouth of the Pascagoula River near the eastern state line.</p>
<p>Pascagoula is a shipbuilding town. The shipyard has been the area’s largest employer for generations, and much of the housing in Pascagoula, Moss Point and Gautier was built to house its workforce. Ocean Springs sits at the western end of the county.</p>

<h2>Hurricanes on the eastern Coast</h2>
<p>Hurricane Katrina’s surge on August 29, 2005 flooded large parts of Pascagoula and pushed up the river and bayous into Moss Point and Gautier. Wind damage followed far beyond the surge line. The claim fights that followed, over wind versus water and anti-concurrent-causation clauses, lasted for years.</p>
<p>Since then, Hurricane Isaac in August 2012 brought heavy rain and surge, and Hurricane Zeta, which made landfall in Louisiana on October 28, 2020, sent strong wind across the Coast, including Jackson County.</p>

<h2>Split policies in the MWUA territory</h2>
<p>Jackson County is one of the six southernmost counties served by the Mississippi Windstorm Underwriting Association. Many Pascagoula owners have:</p>
<ul>
<li>a homeowners policy that excludes wind,</li>
<li>an MWUA policy for wind and hail, and</li>
<li>a separate flood policy, usually through the NFIP.</li>
</ul>
<p>Each policy has its own deductible and, often, its own appraisal clause. Wind deductibles on the Coast are frequently a percentage of Coverage A. Our <a href="/claim-calculator-suite/wind-water-split-estimator/">wind and water split estimator</a> can help you think through how a loss might be divided.</p>
<div class="callout"><b class="callout-t">What appraisal can and can’t do here</b><p>Appraisal won’t decide whether wind or water caused a loss; that is generally a coverage question. It can set the amount of the wind damage, or of each part of a loss, once coverage is accepted.</p></div>

<h2>Homes in Pascagoula, Moss Point and Gautier</h2>
<p>Older neighborhoods near Downtown Pascagoula and along Beach Boulevard have brick and frame homes from the shipyard boom years, many of them repaired or raised after 2005. Moss Point and Escatawpa mix older homes with rural property along the rivers. Gautier and Vancleave include newer subdivisions and manufactured homes.</p>
<h3>Disputes we see often</h3>
<ul>
<li>Raised homes priced without the access equipment and labor they need.</li>
<li>Roof estimates that ignore code requirements for wind resistance on a full replacement.</li>
<li>Manufactured homes with roof and skirting damage written as minor repairs.</li>
<li>Interior water damage assigned to flood when the roof was opened by wind.</li>
</ul>

<h2>Next steps</h2>
<p>If you and your carrier agree the loss is covered but not on what it costs, we can review the estimate and, where your policy allows, represent you through appraisal. See our <a href="/our-appraisal-services/hurricane-named-storm-appraisal/">hurricane and named-storm appraisal</a> service. We serve Pascagoula, Moss Point, Gautier, Ocean Springs and the rest of Jackson County. Confirm your deadlines with a Mississippi attorney.</p>""",
        "faqs": [
            ("Is Jackson County the same as the city of Jackson?", "No. Jackson County is on the Gulf Coast, with Pascagoula as its county seat. The city of Jackson is the state capital, mostly in Hinds County."),
            ("Do I need separate appraisals for my wind policy and my homeowners policy?", "Often, yes. Each policy has its own appraisal clause and carrier. If both policies are disputed, they may proceed separately, though the same facts and photos usually support both."),
        ],
    },
    # 10 ────────────────────────────────────────────────────────────
    {
        "slug": "vicksburg-warren-county",
        "city": "Vicksburg",
        "county": "Warren County",
        "region": "Southwest Mississippi",
        "kw": "insurance appraisal vicksburg ms",
        "title": "Insurance Appraisal in Vicksburg, MS | Warren County",
        "desc": "Insurance appraisal in Vicksburg, MS for historic homes and newer properties with disputed wind, tree and water claims.",
        "h1": "Vicksburg Insurance Appraisal for Historic and Hillside Homes",
        "lede": "Vicksburg’s bluffs, ravines and historic homes make property claims harder to estimate than most. When your carrier’s number doesn’t reflect the real repair, appraisal can settle the amount.",
        "perils": [
            "Tornadoes and spring severe storms",
            "Tree fall on hillside lots",
            "Water losses in older homes",
            "Mississippi River and backwater flooding",
            "Inland hurricane wind",
        ],
        "neighborhoods": ["Historic Downtown Vicksburg", "Clay Street corridor", "Halls Ferry Road area", "Culkin", "Bovina", "Redwood"],
        "housing": "Vicksburg has antebellum and Victorian homes in its historic core, early-twentieth-century and mid-century homes on hilly streets, and newer subdivisions and rural homes across Warren County.",
        "storms": [
            ("Dec 5, 1953", "Vicksburg tornado through the downtown area"),
            ("2011", "Mississippi River flooding and backwater"),
            ("Aug 2021", "Hurricane Ida’s wind and tree damage in southwest Mississippi"),
        ],
        "near": ["jackson-hinds-county", "greenville-washington-county", "hattiesburg-forrest-county"],
        "body": """<h2>Vicksburg on the bluffs</h2>
<p>Vicksburg is the county seat of Warren County, set on high bluffs above the Mississippi River where it meets the Yazoo River. The Vicksburg National Military Park wraps around the north and east sides of the city, and Interstate 20 crosses the river into Louisiana here. The U.S. Army Corps of Engineers has a large presence in town.</p>
<p>Many of the city’s historic homes are still private residences, and some operate as inns, which can mean a mix of homeowners and commercial coverage on one property.</p>
<p>The terrain is the first thing to understand about a Vicksburg claim. Streets climb and drop through ravines, many homes sit on slopes, and big trees grow on hillsides above and below houses.</p>

<h2>Storms and floods in Vicksburg’s history</h2>
<p>On December 5, 1953, a tornado struck Vicksburg, causing heavy loss of life and destroying buildings in and around downtown. In 2011, the Mississippi River rose to major flood levels, and backwater pushed into low-lying areas of Warren County. In August 2021, Hurricane Ida came ashore in Louisiana and brought wind and tree damage to southwest Mississippi.</p>
<p>Flood damage is generally covered under a separate flood policy, not a homeowners policy. Wind, tree fall and sudden water losses inside the home are the claims that more often end up in appraisal.</p>

<h2>Historic homes and hillside lots</h2>
<p>Historic Downtown Vicksburg and the older streets around it hold antebellum and Victorian homes, many of them restored. Farther out along the Clay Street corridor and the Halls Ferry Road area, mid-century homes and newer subdivisions are common. Culkin, Bovina and Redwood add rural and suburban property across the county.</p>
<h3>Estimate problems on historic homes</h3>
<ul>
<li>Plaster, ornate trim, heart-pine floors and tall windows priced as standard modern materials.</li>
<li>Slate, metal or other specialty roofing written as asphalt shingles.</li>
<li>Repairs that can’t meet the original look without custom millwork, left out of the scope.</li>
<li>Ordinance or law costs when a large repair triggers current code requirements.</li>
</ul>
<h3>Estimate problems on hillside property</h3>
<ul>
<li>Access costs for steep lots: equipment, staging and hand-carrying materials.</li>
<li>Tree removal on slopes, where many policies limit debris removal per tree and per occurrence.</li>
<li>Damage to retaining structures, decks and steps that the estimate treats as separate or excluded.</li>
</ul>
<div class="callout"><b class="callout-t">Earth movement</b><p>Damage from soil movement or erosion on a slope is usually excluded. If a covered event, like a tree strike or a burst pipe, caused the damage, the cost of repairing it can be appraised once coverage is accepted.</p></div>

<h2>Appraisal for Vicksburg owners</h2>
<p>When coverage isn’t in question and the problem is the number, the appraisal clause in your policy lets each side name an independent appraiser, with an umpire if needed. Our <a href="/claim-advice/mississippi-appraisal-clause-guide/">Mississippi appraisal clause guide</a> explains the steps, and our <a href="/our-appraisal-services/home-insurance-appraisal/">home insurance appraisal</a> service covers how we represent homeowners.</p>
<p>Confirm any deadline in your policy, and under state law, with a Mississippi attorney.</p>""",
        "faqs": [
            ("My historic Vicksburg home needs custom trim. Will appraisal account for that?", "Appraisal sets the amount needed to repair the covered damage. If your home’s original materials require custom work to repair properly, that cost belongs in the scope and can be part of the appraisal."),
            ("Does my homeowners policy cover Mississippi River flooding?", "Generally no. Flood is usually covered by a separate flood policy. Appraisal under a homeowners policy addresses covered losses such as wind, tree fall and sudden water damage from plumbing."),
        ],
    },
    # 11 ────────────────────────────────────────────────────────────
    {
        "slug": "columbus-lowndes-county",
        "city": "Columbus",
        "county": "Lowndes County",
        "region": "North Mississippi",
        "kw": "insurance appraiser columbus ms",
        "title": "Insurance Appraiser Columbus, MS | Lowndes County Claims",
        "desc": "Insurance appraiser in Columbus, MS for tornado, wind and hail claim disputes on historic homes and newer property in Lowndes County.",
        "h1": "Columbus Claim Appraisal for Historic and Newer Homes",
        "lede": "Columbus pairs antebellum homes with Air Force families and a recent EF3 tornado. If the carrier’s estimate on your Columbus property falls short, appraisal can settle the amount.",
        "perils": [
            "Tornadoes and spring severe weather",
            "Hail and straight-line wind",
            "Tree fall on large historic lots",
            "Frozen pipes in older homes",
        ],
        "neighborhoods": ["Downtown Columbus", "Southside", "Caledonia", "New Hope", "Steens"],
        "housing": "Columbus has antebellum and Victorian homes in its historic districts, mid-century brick ranches, rental housing near the university and the Air Force base, and newer subdivisions in eastern Lowndes County.",
        "storms": [
            ("Feb 23, 2019", "EF3 tornado through Columbus"),
            ("Feb 2021", "Winter storm and statewide freeze"),
            ("Dec 2022", "Hard freeze and frozen-pipe losses"),
        ],
        "near": ["tupelo-lee-county", "meridian-lauderdale-county", "oxford-lafayette-county"],
        "body": """<h2>Columbus and Lowndes County</h2>
<p>Columbus is the county seat of Lowndes County, on the Tombigbee River near the eastern state line. It is home to Mississippi University for Women and to Columbus Air Force Base, a pilot training base north of the city. Starkville and Mississippi State University are a short drive west.</p>
<p>Columbus is also one of Mississippi’s well-known historic towns. Its spring Pilgrimage opens antebellum and Victorian homes to visitors, and many of those houses are still lived in.</p>

<h2>The February 2019 tornado</h2>
<p>On February 23, 2019, an EF3 tornado moved through Columbus, damaging homes, businesses and trees along its path. Claims from that storm included total losses, roofs torn open, and long fights over interior water damage after rain followed through the openings.</p>
<p>Many of those claims also raised questions about tree removal, fences and outbuildings, and additional living expenses for families who could not stay in their homes during repairs.</p>
<p>Beyond that event, Columbus sees the same severe weather as the rest of North Mississippi: spring storm systems with hail, straight-line wind and tornadoes, plus the occasional hard freeze like the February 2021 winter storm.</p>

<h2>Historic homes and Pilgrimage houses</h2>
<p>Downtown Columbus and the Southside historic district hold many of the city’s antebellum and Victorian homes. Claims on these houses rarely fit a standard estimate.</p>
<table>
<thead><tr><th>Feature</th><th>Common carrier approach</th><th>What a proper repair may need</th></tr></thead>
<tbody>
<tr><td>Plaster walls and ceilings</td><td>Drywall patch and paint</td><td>Plaster repair by a skilled trade</td></tr>
<tr><td>Wood siding and trim</td><td>Stock lumber</td><td>Custom-milled profiles to match</td></tr>
<tr><td>Heart-pine flooring</td><td>Replace damaged boards only</td><td>Matching reclaimed boards and refinishing a continuous area</td></tr>
<tr><td>Tall windows and doors</td><td>Standard-size replacements</td><td>Restoration or custom units</td></tr>
</tbody>
</table>
<p>Whether a policy pays to match original materials depends on its wording. The cost of repairing covered damage properly is the core question appraisal answers.</p>

<h2>Newer homes, rentals and base housing</h2>
<p>Mid-century brick ranches fill much of the city. Rentals cluster near MUW and serve families stationed at the base. Areas such as Caledonia, New Hope and Steens have newer subdivisions and rural homes. On these properties, the typical disputes are:</p>
<ul>
<li>Partial roof replacements after hail or wind that leave mismatched shingles.</li>
<li>Short roof measurements and missing items like drip edge, starter and ridge.</li>
<li>Tornado-damaged siding replaced on one wall when the color no longer matches.</li>
<li>Tree removal capped by policy limits while the framing repair is underestimated.</li>
</ul>
<div class="callout"><b class="callout-t">Starting point</b><p>Read your carrier’s estimate line by line before you respond. Our <a href="/claim-advice/line-by-line-estimate-reading/">estimate reading guide</a> shows how.</p></div>

<h2>Our work in Columbus</h2>
<p>We work claims across Lowndes County and nearby Starkville. When coverage is accepted and the disagreement is about amount, we can represent you through your policy’s appraisal clause. See our <a href="/our-appraisal-services/tornado-wind-damage-appraisal/">tornado and wind damage appraisal</a> service, and confirm your deadlines with a Mississippi attorney.</p>""",
        "faqs": [
            ("Can appraisal help with a Pilgrimage home in Columbus?", "Yes, if the dispute is about the cost to repair covered damage. Historic homes often need specialty trades and materials, and those costs belong in a proper scope of repair."),
            ("Do you also work claims in Starkville?", "Yes. We work claims in Starkville, across Lowndes and Oktibbeha counties, and throughout Mississippi."),
        ],
    },
    # 12 ────────────────────────────────────────────────────────────
    {
        "slug": "greenville-washington-county",
        "city": "Greenville",
        "county": "Washington County",
        "region": "The Delta",
        "kw": "greenville ms insurance appraiser",
        "title": "Greenville, MS Insurance Appraiser | Delta Property Claims",
        "desc": "Greenville MS insurance appraiser for homes, farm buildings and businesses with disputed wind and tornado claims in Washington County.",
        "h1": "Greenville and Delta Property Claim Appraisal",
        "lede": "In the Delta, a single storm can damage a house, a metal shop building and a grain bin on the same property. If your carrier’s estimate on your Greenville-area loss falls short, appraisal can settle the amount.",
        "perils": [
            "Tornadoes and straight-line wind across open farmland",
            "Metal building and farm structure damage",
            "Hail on roofs and equipment sheds",
            "Mississippi River and backwater flooding",
            "Frozen pipes during hard freezes",
        ],
        "neighborhoods": ["Downtown Greenville", "Lake Ferguson area", "Leland", "Metcalfe", "Arcola", "Hollandale"],
        "housing": "Greenville and Washington County have older homes in town, mid-century brick ranches, manufactured homes in rural areas, and metal farm and shop buildings across the surrounding farmland.",
        "storms": [
            ("1927", "Great Mississippi Flood across the Delta"),
            ("2011", "Mississippi River flooding"),
            ("Mar 24, 2023", "Rolling Fork EF4 tornado to the south in Sharkey County"),
        ],
        "near": ["vicksburg-warren-county", "oxford-lafayette-county", "jackson-hinds-county"],
        "body": """<h2>Greenville, Washington County and the Delta</h2>
<p>Greenville is the county seat of Washington County and the largest city in the Mississippi Delta. It sits on Lake Ferguson, an oxbow off the Mississippi River, behind the levee system that protects the town. Leland lies a few miles east, and Indianola is farther east in Sunflower County. Smaller towns such as Metcalfe, Arcola and Hollandale round out Washington County.</p>
<p>The Delta is flat, open farmland, and Greenville’s economy is tied to agriculture and the river. Many owners in and around town hold a homeowners policy on the house and a farm or commercial policy on the operation, each with its own terms. Wind travels a long way with little to slow it, and farms carry a mix of houses, shops, barns and bins that all need to be scoped after a storm.</p>

<h2>Floods and storms in Delta history</h2>
<ul>
<li><strong>1927:</strong> the Great Mississippi Flood broke the levee north of Greenville and covered much of the Delta. It shaped the levee system Greenville relies on today.</li>
<li><strong>2011:</strong> the Mississippi River rose to major flood stage, testing those levees again.</li>
<li><strong>March 24, 2023:</strong> an EF4 tornado devastated Rolling Fork in Sharkey County, south of Washington County, and Silver City in Humphreys County.</li>
</ul>
<p>River and surface flooding is usually covered by a separate flood policy, not by homeowners or farm property coverage. Wind, tornado and hail losses are where appraisal most often comes in.</p>

<h2>Farm buildings, metal structures and Delta homes</h2>
<p>Downtown Greenville and the neighborhoods near Lake Ferguson include older homes and commercial buildings. Brick ranches from the 1960s through the 1980s are common across town, and manufactured homes are widespread in rural Washington County. On farms, metal shop buildings, equipment sheds, barns and grain bins are part of nearly every claim.</p>
<h3>Metal buildings</h3>
<p>Metal building claims are often underpriced. Common gaps include:</p>
<ul>
<li>Replacing a few damaged panels when the panel profile or color is no longer available.</li>
<li>Leaving out bent purlins, girts or framing hidden behind intact sheeting.</li>
<li>Ignoring the crane, lift and crew time needed on tall structures.</li>
<li>Missing doors, trim, gutters and insulation.</li>
</ul>
<h3>Homes and manufactured homes</h3>
<p>On houses, the usual disputes are roof measurements, partial replacements that won’t match, and interior water damage after a roof opening. On manufactured homes, roof coatings, skirting, tie-downs and interior panels are often left off the estimate.</p>
<div class="callout"><b class="callout-t">Farm and commercial policies</b><p>Farm and commercial policies have their own appraisal clauses, schedules and limits. Read yours, including any coverage for outbuildings, before you demand appraisal.</p></div>

<h2>Working with us from the Delta</h2>
<p>We work claims throughout Washington County and the wider Delta. If coverage is accepted and the problem is the amount, we can represent you through appraisal. See our <a href="/our-appraisal-services/tornado-wind-damage-appraisal/">tornado and wind damage appraisal</a> service, or our <a href="/our-appraisal-services/commercial-hoa-appraisal/">commercial appraisal</a> page for farm and business property. Confirm your deadlines with a Mississippi attorney.</p>""",
        "faqs": [
            ("Can appraisal cover metal shop buildings and barns in Washington County?", "Yes, if those structures are covered under your policy and the dispute is about the amount of loss. Farm and commercial policies often schedule outbuildings separately, so check how each structure is listed."),
            ("Does my policy cover flooding from the Mississippi River?", "Usually not. River and surface flooding is generally covered by a separate flood policy. Appraisal under your property policy addresses covered perils such as wind, tornado and hail."),
        ],
    },
]
