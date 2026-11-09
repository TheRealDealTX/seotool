"""City landing-page copy for Missouri Insurance Appraiser.

Each entry feeds one /locations/<slug>/ page. Bodies are HTML fragments that sit under the
page H1 ("Insurance Appraiser in {city}, MO"), so headings start at <h2>.
"""

LOCATIONS = [
    # ------------------------------------------------------------------ Kansas City
    {
        "slug": "kansas-city",
        "city": "Kansas City",
        "geo": "Kansas City",
        "county": "Jackson County",
        "region": "Kansas City Metro",
        "perils": ["Spring hail", "Straight-line wind", "Tornadoes", "Flash flooding"],
        "housing": "Kansas City mixes brick bungalows, shirtwaist houses and Tudor revivals in the older southside neighborhoods with post-war ranches and newer subdivisions across the Northland.",
        "hoods": ["Brookside", "Waldo", "Westport", "Hyde Park", "Crossroads", "Country Club Plaza area", "the Northland"],
        "storms": [
            ("1977", "Plaza flood", "Heavy September rain sent Brush Creek over its banks and flooded the Country Club Plaza and nearby streets."),
            ("2003", "May 4 tornado outbreak", "Tornadoes tore through the Northland, including the Gladstone and Liberty area, damaging homes and businesses."),
            ("Recurring", "Spring hail", "Most springs bring at least one hail event somewhere in the metro that sends roofers door to door."),
        ],
        "near": ["independence", "lees-summit", "st-joseph"],
        "lede": "When a hail or wind claim in Kansas City stalls over the number, an independent appraiser can rebuild the estimate line by line and carry it through your policy’s appraisal clause.",
        "title": "Kansas City Insurance Appraiser | Hail & Wind Claims",
        "desc": "Independent insurance appraiser for Kansas City, MO homes and businesses: hail, wind and water claim estimates, appraisal clause work and umpire help.",
        "body": """<p>Kansas City sits where storm systems coming off the plains tend to organize, and the metro pays for it most springs. Hail that shreds asphalt shingles in Waldo can miss Brookside entirely, and a line of straight-line wind can drop trees across half the Northland in twenty minutes. Those uneven footprints are part of why so many local claims end up as arguments over scope rather than coverage.</p>

<h2>What usually goes wrong with Kansas City claims</h2>
<p>The most common dispute we see is a partial roof approval. An adjuster counts hits on a few test squares, finds the slopes facing the storm damaged and the others “serviceable,” and writes a repair for two slopes. On a 1920s bungalow with a steep pitch, several dormers and discontinued shingles, that partial repair may not be a workable job at all. Gutters, downspouts, window wraps and soft metal on the north side often get left off too.</p>
<p>Wind claims bring a different problem: interior water. A torn roof or a tree limb through a porch leads to ceiling stains and wet insulation that show up days later, after the first inspection is already closed. Getting those items back into the claim, with photos and moisture readings, is a lot of what an estimate review does. Our guide to <a href="/appraisal-help/hail-roof-damage-appraisal/">hail and roof damage appraisal</a> walks through how we document both.</p>

<h2>Old houses, newer code</h2>
<p>South of the Plaza, much of the housing stock went up before World War II. Shirtwaist houses with stone or brick first floors and frame upper stories, Tudor revivals with steep slate-look roofs, and four-squares with deep eaves all cost more to repair than a carrier’s default line items suggest. Plaster walls, built-in cabinetry, old-growth trim and clay tile or slate accents in Hyde Park and around the Plaza do not have cheap like-kind replacements.</p>
<p>Code upgrades matter as well. Re-roofing permits through Kansas City’s planning and development department can trigger requirements such as ice and water shield, drip edge or decking repairs that a bare shingle estimate ignores. Whether your policy pays for those depends on its ordinance or law wording, so we read that section before we price anything.</p>
<p>The metro also crosses four counties. Kansas City reaches into Clay, Platte and Cass counties as well as Jackson, and permit offices, contractor travel and even debris-disposal costs vary by where the house actually sits.</p>

<h2>Floodwater versus storm water</h2>
<p>Brush Creek, Turkey Creek and the Blue River have all flooded neighborhoods in heavy rain. Standard homeowners policies exclude surface flooding, so rising water usually needs a separate NFIP or private flood policy. Water that came in through a storm-damaged roof is a different matter. Sorting out which water did what is often the hinge of a Kansas City claim, and it is a coverage question your policy and, if needed, a Missouri attorney should answer. Appraisal only settles the amount.</p>

<h2>Is appraisal the right next step?</h2>
<p>Appraisal fits when you and your insurer agree something is covered but are far apart on what it costs to fix. It does not fit a flat denial. If you are unsure which side of that line you are on, start with an <a href="/appraisal-help/insurer-estimate-review/">insurer estimate review</a>; it shows where the gaps are before anyone invokes anything.</p>
<p>We serve the whole metro, from the Northland to south Kansas City, and inspect on site rather than working from photos alone.</p>""",
        "faqs": [
            ("My Kansas City neighbors got full roofs after the same hailstorm and I got a repair. Can appraisal fix that?",
             "Possibly. If the insurer agrees there is covered hail damage and the dispute is how much needs replacing, that is an amount-of-loss question appraisal can decide. What your neighbors received does not bind your insurer, so the case rests on documentation of your own roof."),
            ("Do you work on homes in the Northland and in Clay or Platte County?",
             "Yes. We serve the Kansas City metro across Jackson, Clay, Platte and Cass counties and inspect properties in person."),
            ("Brush Creek flooded my basement. Will appraisal help?",
             "Appraisal cannot create coverage for flood if your homeowners policy excludes it. If you carry flood insurance or the water entered through storm damage, appraisal may help resolve a dispute about the amount."),
        ],
    },
    # ------------------------------------------------------------------ St. Louis
    {
        "slug": "st-louis",
        "city": "St. Louis",
        "geo": "St. Louis",
        "county": "Independent city",
        "region": "St. Louis Metro",
        "perils": ["Large hail", "Derecho winds", "Tornadoes", "Sewer backup"],
        "housing": "The city is built largely of brick: two-family flats, row houses and shotgun-style homes in South City, mansard-roofed Victorians in Lafayette Square and large brick homes on private streets in the Central West End.",
        "hoods": ["Soulard", "Tower Grove South", "The Hill", "Lafayette Square", "Central West End", "Dogtown", "Benton Park", "Bevo Mill"],
        "storms": [
            ("1993", "Great Flood", "The Mississippi crested at record levels; the downtown floodwall held, but low-lying areas along the rivers flooded for weeks."),
            ("2001", "April 10 hailstorm", "A hailstorm along the I-70 corridor damaged roofs and vehicles across the north side and into St. Louis County."),
            ("2006", "July windstorms", "Back-to-back July storms with derecho-strength winds knocked out power to much of the region for days."),
            ("2011", "Good Friday tornado", "An April 22 tornado struck Lambert airport and the Bridgeton and Maryland Heights area of St. Louis County."),
        ],
        "near": ["chesterfield", "st-charles", "cape-girardeau"],
        "lede": "St. Louis brick, slate and plaster do not price like a tract home. We help city owners get an estimate that reflects the building they actually own, and handle appraisal when the gap will not close.",
        "title": "St. Louis Insurance Appraiser | Brick, Slate & Storm",
        "desc": "St. Louis, MO insurance appraiser for brick flats, historic homes and storm claims. Estimate review, appraisal clause representation and umpire work.",
        "body": """<h2>A city of brick, and why that matters for your claim</h2>
<p>Few American cities are as thoroughly brick as St. Louis. The soft red brick from local clay works still holds up most of South City, from the two-family flats in Tower Grove South to the narrow shotgun homes around Soulard and Benton Park. Brick walls rarely fail in a storm, but everything attached to them does: slate and tile roofs, box gutters built into the cornice, wood porches, parapet caps and copper flashing.</p>
<p>That is where estimates go sideways. An insurer’s software may price a box gutter as a standard aluminum seamless run, or treat a mansard slate roof in Lafayette Square as if it were architectural shingle. Neither is a like-kind repair. Matching soft brick for a chimney rebuild or tuckpointing around a damaged parapet takes masons who know old mortar, and they charge accordingly.</p>

<h3>Inside the walls</h3>
<p>Plaster on wood or metal lath is the rule in pre-war city housing. Patching it with drywall can leave a visible, uneven wall, and in a multi-room loss the question becomes whether a consistent finish requires more than the stained square footage. Ornate trim, pocket doors and built-ins in the Central West End add more line items that rarely appear in a first-pass estimate.</p>

<h2>Storms, sewers and the rivers</h2>
<p>The region has a long storm record. The April 2001 hailstorm along the I-70 corridor and the July 2006 windstorms that left much of the area without power are still reference points for local roofers. The 2011 Good Friday tornado hit the airport and nearby north county suburbs rather than the city itself, but it shows how far severe weather reaches across the metro.</p>
<p>Water claims are just as common. Many older city sewers are combined systems, and heavy rain can push water back up through basement floor drains. Sewer and drain backup is usually excluded unless you bought a specific endorsement, often with its own limit. Flooding from the Mississippi or River des Peres is a separate exposure again and needs flood insurance. Earthquake damage from the New Madrid seismic zone is normally excluded unless you added earthquake coverage. Coverage questions like these are for your policy and, where needed, a Missouri attorney. Appraisal addresses the dollar amount.</p>

<h2>Local practicalities</h2>
<p>St. Louis is an independent city, separate from St. Louis County, with its own building division and its own permit process. Properties in local historic districts may also need design review before exterior work, which can require specific materials such as real slate or wood windows. If historic review applies to your home, the estimate should account for it, and so should the timeline.</p>
<p>Labor is another factor. Slate roofers, ornamental tin workers and masons who handle historic brick are a smaller pool than general roofers, and their pricing reflects it. An estimate built on generic regional averages tends to come in low.</p>

<h2>Where we fit</h2>
<p>If your insurer accepts the loss but its estimate looks like it was written for a different house, an <a href="/appraisal-help/insurer-estimate-review/">estimate review</a> is the place to start. When a claim is stuck and the policy has an appraisal clause, we can serve as your appraiser; see <a href="/appraisal-help/appraisal-demand-representation/">appraisal demand and representation</a> for how that process runs.</p>
<p>We work throughout the city and inspect in person, on the roof and in the basement.</p>""",
        "faqs": [
            ("My insurer wants to replace my slate roof with shingles. Can appraisal address that?",
             "Appraisal decides the amount of loss, and that often includes what a like-kind repair costs. Whether the policy requires matching materials is ultimately a policy-wording question, so we review the policy before advising."),
            ("Is a basement sewer backup in St. Louis covered?",
             "Usually only if you have a water or sewer backup endorsement, and those often carry a separate limit. If you have the endorsement and dispute the amount, appraisal may help."),
            ("Does it matter that St. Louis is not in St. Louis County?",
             "For your claim it mainly affects permits and code: the City of St. Louis has its own building division and historic district rules, which can change what a proper repair includes."),
        ],
    },
    # ------------------------------------------------------------------ Springfield
    {
        "slug": "springfield",
        "city": "Springfield",
        "geo": "Springfield",
        "county": "Greene County",
        "region": "Ozarks",
        "perils": ["Sinkholes", "Ice storms", "Hail", "Severe thunderstorms"],
        "housing": "Springfield ranges from brick and frame Craftsman homes in Rountree and Phelps Grove to mid-century ranches across the south side and fast-growing subdivisions toward Nixa, Ozark and Republic.",
        "hoods": ["Rountree", "Phelps Grove", "Midtown", "Galloway", "Southern Hills", "Commercial Street", "West Central"],
        "storms": [
            ("2007", "January ice storm", "A heavy mid-January ice storm brought down trees and power lines across Springfield and the Ozarks."),
            ("Recurring", "Spring hail", "Hail-producing storms cross the Springfield plateau most years in spring and early summer."),
            ("Ongoing", "Karst collapse", "Sinkholes and ground subsidence are a long-running issue in the karst bedrock beneath Greene County."),
        ],
        "near": ["joplin", "jefferson-city", "lees-summit"],
        "lede": "Springfield claims run from hail and ice to the ground itself giving way. We help Ozarks property owners sort out what the insurer’s estimate missed and use appraisal when the numbers will not meet.",
        "title": "Springfield MO Insurance Appraiser | Hail, Ice & Karst",
        "desc": "Springfield, MO insurance appraiser for hail, ice storm and ground-collapse claims across Greene County. Estimate reviews and appraisal clause help.",
        "body": """<p>Most of the claims that come out of Springfield fall into three buckets: hail and wind, winter ice, and the ground. The first two are familiar anywhere in Missouri. The third is particular to the Ozarks, and it is the one homeowners are least prepared for.</p>

<h2>Living on karst</h2>
<p>Springfield sits on limestone riddled with caves, springs and solution channels. Greene County has documented a large number of sinkholes, and the city’s stormwater rules treat them as a real planning concern. When a void opens under a slab or a foundation corner drops, the first question is not price. It is coverage.</p>
<p>Most homeowners policies exclude earth movement. Some include limited coverage for “sinkhole collapse,” defined narrowly, and some carriers sell a separate endorsement. Plenty of Springfield owners only learn which version they have after the ground moves. Because the wording decides almost everything here, we read the policy first and suggest a Missouri attorney if coverage is in dispute. Appraisal comes into play only once the insurer agrees there is a covered loss and the fight is about the repair. Our <a href="/appraisal-help/sinkhole-ground-collapse-appraisal/">sinkhole and ground collapse</a> page explains why those repair estimates vary so much, from grouting and underpinning to engineering fees.</p>

<h2>Ice, limbs and long outages</h2>
<p>The January 2007 ice storm is still a reference point in Springfield. Ice-loaded oaks and maples came down on roofs, cars and power lines, and many households went days without heat. Storms like that create layered claims: a limb through the roof, then interior water, then frozen pipes in a cold house. Each piece needs its own documentation, and adjusters working through a backlog sometimes close one piece and forget the others. Our notes on <a href="/appraisal-help/winter-storm-ice-damage-appraisal/">winter storm and ice damage</a> cover how to keep those items connected.</p>

<h2>The houses themselves</h2>
<h3>Older central neighborhoods</h3>
<p>Rountree and Phelps Grove have plenty of 1910s through 1930s Craftsman bungalows and brick homes with plaster walls, original hardwood and deep porches. Repairs there need matched trim and careful plaster work, and those costs are often underpriced in a standard estimate. Around Commercial Street and Midtown, older commercial and mixed-use brick adds its own repair challenges.</p>
<h3>Newer construction south and west</h3>
<p>South Springfield, Galloway and the suburbs toward Nixa and Ozark are mostly newer frame homes with asphalt roofs and vinyl or fiber-cement siding. Here the typical dispute is matching: a hail-hit elevation is replaced, but the siding line has been discontinued and the patch will never blend. Policy wording on matching controls what gets paid, but the cost side is squarely an appraisal issue.</p>

<h2>Before you invoke appraisal</h2>
<p>A few practical points for Greene County owners:</p>
<ul>
<li>Re-roofing and structural work usually needs a permit from the city or, outside city limits, the county. Code items such as underlayment or decking may be required and may be payable under your ordinance or law coverage.</li>
<li>Contractor demand spikes after a big storm. An estimate written in a quiet month may not reflect what a repair actually costs a few weeks after a regional hail event.</li>
<li>Keep photos of anything you remove, including wet drywall or downed limbs, before it goes to the curb.</li>
</ul>
<p>We serve Springfield and the surrounding Ozarks, and we inspect in person.</p>""",
        "faqs": [
            ("Does my homeowners policy cover a sinkhole in Springfield?",
             "It depends entirely on the wording. Many policies exclude earth movement and offer only narrow collapse coverage or a separate endorsement. Check your policy, and talk to a Missouri attorney if coverage is denied; appraisal only applies once a covered loss is accepted."),
            ("Can appraisal be used for ice storm damage?",
             "Yes, if the insurer accepts the damage as covered and the disagreement is about scope or price, such as how much of the roof or how many interior rooms need work."),
            ("Why did my Springfield repair estimate jump after a big hailstorm?",
             "Contractor demand rises sharply after a regional storm, and material and labor pricing can follow. A fair estimate should reflect what the work costs when it is actually done, which is one reason estimates are revisited."),
        ],
    },
    # ------------------------------------------------------------------ Columbia
    {
        "slug": "columbia",
        "city": "Columbia",
        "geo": "Columbia",
        "county": "Boone County",
        "region": "Mid-Missouri",
        "perils": ["Hail", "Wind and fallen trees", "Creek flash floods", "Frozen pipes"],
        "housing": "Columbia combines early twentieth-century homes near downtown and the university, a large stock of student rentals and duplexes, and newer subdivisions spreading south and east of town.",
        "hoods": ["East Campus", "Old Southwest", "Benton-Stephens", "North Village Arts District", "Downtown (The District)", "Grasslands", "Rock Bridge area"],
        "storms": [
            ("Recurring", "Spring hail and wind", "Severe thunderstorms moving across Mid-Missouri regularly bring hail and damaging wind to Boone County."),
            ("Recurring", "Hinkson Creek flash floods", "Heavy rain can send Hinkson Creek and its tributaries out of their banks quickly in low-lying parts of town."),
        ],
        "near": ["jefferson-city", "st-charles", "chesterfield"],
        "lede": "Columbia has owner-occupied homes, student rentals and plenty of newer construction, and each produces a different kind of claim dispute. We help Boone County owners understand the estimate and, when it makes sense, take the claim to appraisal.",
        "title": "Columbia MO Insurance Appraiser | Home & Rental Claims",
        "desc": "Insurance appraiser for Columbia, MO and Boone County: hail, wind and water claims on homes and rentals, estimate reviews and appraisal clause work.",
        "body": """<h2>Three kinds of Columbia properties</h2>
<p>Ask a Columbia roofer about the last big hailstorm and they will tell you the claims split three ways. Owner-occupied homes in Old Southwest and around the parks. Rentals in East Campus, Benton-Stephens and the duplex blocks near the university. And newer houses in the subdivisions south toward Rock Bridge and east along the outer roads. Same storm, very different disputes.</p>

<h3>Older homes near downtown</h3>
<p>Old Southwest and East Campus have brick and frame houses from the early 1900s onward: steep roofs, plaster walls, wood windows and porches that have been rebuilt more than once. When hail or a falling tree damages one of these, the cost of matching trim and plaster is the usual sticking point.</p>

<h3>Rentals and small landlords</h3>
<p>Rental claims bring their own questions. Was the loss under a landlord or dwelling-fire form rather than a homeowners policy? Is there loss of rents coverage while units are empty? Did a tenant’s delay in reporting a leak change anything? Those are policy and coverage questions. Once they are sorted out, we can help with the part appraisal covers: what the repair actually costs, including turnover-season pricing when every contractor in town is booked. Owners of several buildings may also want to read about <a href="/appraisal-help/commercial-hoa-appraisal/">commercial and HOA appraisal</a>.</p>

<h3>Newer subdivisions</h3>
<p>Newer homes usually mean asphalt roofs, vinyl or fiber-cement siding and builder-grade finishes. Disputes tend to center on partial roof approvals and siding that no longer matches once one elevation is replaced.</p>

<h2>Water: creek, pipe, or roof</h2>
<p>Hinkson Creek and its tributaries can rise fast in a heavy rain. Floodwater from a creek is generally excluded from homeowners coverage and needs a separate flood policy. Water from a burst supply line in a cold snap is a different story, and so is rain coming through a storm-torn roof. Our page on <a href="/appraisal-help/burst-pipe-water-damage-appraisal/">burst pipe and water damage appraisal</a> explains how source, timing and drying records feed into the estimate.</p>
<p>Student rentals left empty over winter break are a classic frozen-pipe setup. Many policies have conditions about heat in vacant or unoccupied buildings, so read those before you assume a claim will be paid.</p>

<h2>Permits, pricing and the appraisal decision</h2>
<p>Most structural and roofing work inside city limits goes through the City of Columbia’s building and site development office, and work outside the city goes through Boone County. Code-driven items can be legitimate parts of a repair estimate when your policy includes ordinance or law coverage.</p>
<p>Pricing is the other local factor. Columbia’s contractor pool tightens in late summer, when rental turnover and storm work overlap. An estimate based on off-season pricing can look reasonable on paper and still fail to get the job done.</p>
<p>Appraisal is worth considering when the insurer agrees the loss is covered, you have tried to resolve the difference, and the gap is big enough to justify the cost of an appraiser and a share of the umpire. It decides the amount of loss, not coverage. If you are not sure you are there yet, our <a href="/appraisal-roadmap/">appraisal roadmap</a> lays out the steps.</p>
<p>We serve Columbia and surrounding Boone County and inspect on site.</p>""",
        "faqs": [
            ("I own a rental near campus. Can I use appraisal on a landlord policy?",
             "Many dwelling and landlord policies include an appraisal clause, just as homeowners policies do. Check your specific form; if the clause is there and the dispute is about the amount, appraisal may apply."),
            ("A pipe froze in my vacant rental over winter break. Is that covered?",
             "Possibly, but many policies limit coverage for freezing in vacant or unoccupied buildings unless heat was maintained or the water was shut off. That is a coverage question to resolve before appraisal."),
            ("Do you serve Ashland and the rest of Boone County?",
             "Yes. We serve Columbia and nearby Boone County communities and inspect properties in person."),
        ],
    },
    # ------------------------------------------------------------------ Independence
    {
        "slug": "independence",
        "city": "Independence",
        "geo": "Independence",
        "county": "Jackson County",
        "region": "Kansas City Metro",
        "perils": ["Hail", "Thunderstorm wind", "Tree damage", "Basement water"],
        "housing": "Independence has Victorian and early twentieth-century homes around the Square and the Truman Historic District, modest post-war bungalows and ranches in older neighborhoods, and newer subdivisions toward the east.",
        "hoods": ["Independence Square", "Truman Historic District", "Englewood", "Fairmount", "Little Blue Valley", "Sugar Creek (nearby)", "Blue Springs (nearby)"],
        "storms": [
            ("Recurring", "Spring hail", "Spring hailstorms crossing eastern Jackson County regularly damage roofs, siding and gutters in Independence."),
            ("Recurring", "Severe thunderstorm wind", "Summer thunderstorms bring damaging gusts that drop mature trees onto homes and power lines."),
        ],
        "near": ["kansas-city", "lees-summit", "st-joseph"],
        "lede": "Independence has some of the oldest housing in the metro and plenty of post-war homes too. When a storm claim comes back short, we help owners see why and decide whether appraisal is worth it.",
        "title": "Independence MO Insurance Appraiser | Storm Claims",
        "desc": "Independence, MO insurance appraiser for hail, wind and tree-damage claims on historic and post-war homes. Estimate review and appraisal clause help.",
        "body": """<p>Independence is one of the oldest cities in the Kansas City area, and the age shows in its housing. Around the Square and through the Truman Historic District you find Victorians, four-squares and frame houses with wraparound porches. Farther out, Englewood and Fairmount are full of modest bungalows and post-war homes, and the newer subdivisions east toward the Little Blue Valley look like suburbs anywhere. A single storm can produce a very different claim on each street.</p>

<h2>Storms in eastern Jackson County</h2>
<p>Independence does not need a famous storm to have a busy claim season. Spring hail and summer thunderstorm wind are steady, and the city’s big old trees turn a moderate wind event into roof punctures and crushed porches. A falling oak is rarely a simple claim. There is the roof, the framing it landed on, gutters, siding, interior ceilings, contents and often fence or vehicle damage too.</p>
<p>The most common shortfall we see is an estimate that handles the obvious hole and stops there. Shifted rafters, cracked plaster two rooms away and torn underlayment beyond the impact zone get missed. Our guide to <a href="/appraisal-help/tornado-straight-line-wind-appraisal/">wind and tornado appraisal</a> explains how we trace a load path through the structure.</p>

<h2>Repairing older homes the right way</h2>
<p>Historic and pre-war houses in Independence carry repair costs that generic pricing does not capture:</p>
<ul>
<li><strong>Wood siding and trim.</strong> Clapboard profiles and porch details often have to be milled or sourced from salvage.</li>
<li><strong>Plaster interiors.</strong> Matching texture across a room, or deciding where a repair can stop, is a judgment call that drives the number.</li>
<li><strong>Old wiring and framing.</strong> Opening a wall can expose conditions that code requires be corrected. Whether that is payable depends on your ordinance or law coverage.</li>
<li><strong>Design review.</strong> Exterior work in a designated historic area may need approval, which can limit material choices.</li>
</ul>
<p>Post-war homes have their own issue: discontinued materials. Siding, shingles and even brick from the 1950s and 1960s may no longer be made, and a patch that does not match is an ongoing argument with many carriers. Policy wording on matching decides the coverage side. Appraisal can decide the cost side.</p>

<h2>Water in the basement</h2>
<p>Many Independence homes have full basements, often with block or stone walls. After a heavy storm, owners find water and assume it is covered. It depends on how the water got in. Surface water seeping through a foundation is generally excluded, sump pump overflow and drain backup usually require an endorsement, and floodwater requires a flood policy. Water that came through a storm-damaged roof is typically treated differently. Ask your agent or a Missouri attorney if the coverage answer is unclear.</p>

<h2>When appraisal makes sense here</h2>
<p>Appraisal works best when the insurer has accepted the claim, you have documented the damage, and the remaining dispute is about scope or price. If you want a second opinion first, start with an <a href="/appraisal-help/homeowner-claim-appraisal/">overview of homeowner claim appraisal</a> or <a href="/get-in-touch/">get in touch</a> to talk through your estimate.</p>
<p>We serve Independence, Sugar Creek, Blue Springs and the rest of eastern Jackson County, and inspect on site.</p>""",
        "faqs": [
            ("A tree fell on my Independence house. Will the insurer pay to remove it?",
             "Many policies pay tree removal when a tree damages a covered structure, often with a set limit. If the insurer accepts the claim but you disagree on what the repair and removal cost, appraisal may help."),
            ("My older home’s siding is no longer made. What happens?",
             "Whether the policy pays to replace more than the damaged area depends on its matching wording. The cost of the work, once scope is agreed or decided, is something appraisal can determine."),
            ("Do you work in Blue Springs and Sugar Creek?",
             "Yes. We serve Independence and nearby eastern Jackson County communities and inspect properties in person."),
        ],
    },
    # ------------------------------------------------------------------ Lee's Summit
    {
        "slug": "lees-summit",
        "city": "Lee’s Summit",
        "geo": "Lee's Summit",
        "county": "Jackson County",
        "region": "Kansas City Metro",
        "perils": ["Hail", "Wind", "HOA roof disputes", "Siding mismatch"],
        "housing": "Lee’s Summit is dominated by newer HOA subdivisions and lake communities, alongside a historic downtown with older frame and brick homes nearby.",
        "hoods": ["Downtown Lee’s Summit", "Lakewood", "Raintree Lake", "New Longview", "Lake Lotawana (nearby)", "Greenwood (nearby)"],
        "storms": [
            ("Recurring", "Spring hail", "Hailstorms moving through southeast Jackson County and Cass County routinely hit roofs and siding in Lee’s Summit subdivisions."),
            ("Recurring", "Thunderstorm wind", "Strong summer storms bring wind damage to roofs, fences and trees across the city."),
        ],
        "near": ["independence", "kansas-city", "st-joseph"],
        "lede": "In Lee’s Summit, most claim fights are about newer roofs, matching siding and HOA rules. We help owners and associations get an estimate that reflects all three and pursue appraisal when needed.",
        "title": "Lee’s Summit Insurance Appraiser | Hail & HOA Claims",
        "desc": "Lee’s Summit, MO insurance appraiser for hail and wind claims, siding matching and HOA roof disputes. Estimate reviews and appraisal clause work.",
        "body": """<h2>Newer homes, different arguments</h2>
<p>A lot of Lee’s Summit was built in the last few decades. Neighborhoods like Lakewood, Raintree Lake and the developments around New Longview have newer frame homes, laminated shingle roofs and vinyl, engineered wood or fiber-cement siding. That might sound like the easy kind of claim. In practice, newer homes produce their own disputes, and they look different from what older Kansas City neighborhoods see.</p>

<h3>Hail on newer roofs</h3>
<p>Hail damage to a roof that is only a few years old is sometimes written off as “cosmetic” or as granule loss that does not affect function. Whether cosmetic damage is covered depends on your policy; some carriers now attach cosmetic exclusions or roof payment schedules. Where the damage is covered, the argument becomes how many squares are affected and whether a repair is practical. Our <a href="/appraisal-help/hail-roof-damage-appraisal/">hail and roof damage</a> page goes through how we test and document that.</p>

<h3>The siding problem</h3>
<p>Siding colors and profiles change often. When hail damages one or two elevations, the insurer may offer to replace just those walls. If the product is discontinued or the color has faded, the patched house will not match. The policy’s wording on matching, and any endorsements, control what is covered. The cost of the work, whatever scope is agreed or decided, is an appraisal question.</p>

<h2>HOA rules and the estimate</h2>
<p>Many Lee’s Summit subdivisions have covenants that dictate roof color, siding materials, fencing and even mailbox styles. Those rules do not automatically make your insurer pay more, but they shape what a realistic repair looks like. If the HOA requires a specific shingle line or approval before work begins, that should be documented and reflected in the estimate.</p>
<p>Associations themselves often carry policies on clubhouses, pools, entry monuments and common-area fencing, and townhome or villa associations may insure the roofs. A large hail event can leave a board managing dozens of roofs under one claim. That is a different kind of appraisal; see <a href="/appraisal-help/commercial-hoa-appraisal/">commercial and HOA appraisal</a>.</p>

<h2>Practical notes for Lee’s Summit owners</h2>
<ul>
<li>Most of Lee’s Summit is in Jackson County, with part of the city in Cass County. Re-roofing and structural work generally requires a city permit either way.</li>
<li>Older homes near downtown have plaster, wood windows and older framing, and their repairs price very differently from a newer subdivision house.</li>
<li>Lake communities such as Lakewood and nearby Lake Lotawana have docks and shoreline structures that may be covered differently from the house, or excluded, under your policy.</li>
<li>Storm-chasing contractors arrive quickly after hail. Get your own documentation before you sign anything, and be cautious of anyone offering to handle the claim for you.</li>
</ul>

<h2>Is appraisal the next step?</h2>
<p>Appraisal is designed for one kind of disagreement: you and the insurer agree a loss is covered, but not on its amount. If the insurer has denied the claim outright or says the damage is excluded, that is a coverage dispute and may call for a Missouri attorney instead. If you are in the amount camp, our <a href="/appraisal-roadmap/">appraisal roadmap</a> explains what happens next.</p>
<p>We serve Lee’s Summit, Greenwood and the surrounding lake communities, and inspect in person.</p>""",
        "faqs": [
            ("My insurer says the hail damage on my newer Lee’s Summit roof is cosmetic. What can I do?",
             "First, check whether your policy has a cosmetic damage exclusion. If it does not, or the damage goes beyond cosmetic, a disagreement about how much of the roof is damaged may be resolved through appraisal."),
            ("Does my HOA’s roof color rule mean the insurer must replace the whole roof?",
             "Not automatically. HOA rules can affect what a realistic repair looks like, but your policy wording decides what is covered. Document the rule and include it in the claim."),
            ("Can our homeowners association use appraisal for common-area damage?",
             "Often, yes, if the association’s policy has an appraisal clause and the dispute is about the amount of loss. Larger association claims usually need a more detailed, building-by-building estimate."),
        ],
    },
    # ------------------------------------------------------------------ St. Charles
    {
        "slug": "st-charles",
        "city": "St. Charles",
        "geo": "St. Charles",
        "county": "St. Charles County",
        "region": "St. Louis Metro",
        "perils": ["River flooding", "Tornadoes", "Hail", "Historic-home repairs"],
        "housing": "St. Charles pairs brick and stone buildings in the Main Street historic district and Frenchtown with post-war neighborhoods and large newer subdivisions spreading west through the county.",
        "hoods": ["Historic Main Street", "Frenchtown", "New Town", "Elm Point", "St. Peters (nearby)", "Cottleville (nearby)", "O’Fallon (nearby)"],
        "storms": [
            ("1993", "Great Flood", "The Missouri and Mississippi flooded much of the low ground near their confluence in St. Charles County for weeks."),
            ("2021", "December 10 tornado", "A rare December tornado struck the Defiance area of western St. Charles County, destroying homes."),
            ("Recurring", "Spring hail", "Hailstorms moving across the county regularly damage roofs in St. Charles and its neighboring suburbs."),
        ],
        "near": ["st-louis", "chesterfield", "columbia"],
        "lede": "St. Charles owners deal with two rivers, a historic district and fast-growing subdivisions. We help sort out what a fair estimate looks like for each, and handle appraisal when the insurer will not move.",
        "title": "St. Charles MO Insurance Appraiser | Storm & Water",
        "desc": "St. Charles, MO insurance appraiser for storm, hail and water claims in the historic district and newer subdivisions. Estimate review and appraisal.",
        "body": """<p>St. Charles is the county seat of one of the fastest-growing counties in Missouri, and it sits between two big rivers. That combination shapes almost every claim we look at here, from a 19th-century brick storefront on Main Street to a five-year-old house in a subdivision off Highway 94.</p>

<h2>Rivers on two sides</h2>
<p>The Missouri runs along the city’s eastern edge, and the Mississippi meets it a few miles north at the confluence. The Great Flood of 1993 put much of the low ground near that confluence under water for weeks, and high water has returned in other years. The Missouri bottoms on the north and east sides of town remain floodplain.</p>
<p>The point for policyholders is simple, if unwelcome: river flooding is not covered by a standard homeowners or business policy. It needs flood insurance through the NFIP or a private carrier, and those policies have their own claim process and their own limits on things like basements. When a property has both storm damage and flood damage, separating the two is often the hardest part of the claim, and getting it right is a coverage matter before it is a pricing matter.</p>

<h2>Tornadoes are not just a spring problem</h2>
<p>The December 10, 2021 tornado that hit the Defiance area in western St. Charles County was a reminder that severe weather here does not always follow the calendar. Wind claims after an event like that tend to involve full rebuilds, total loss questions and long fights over the value of what was destroyed. Our page on <a href="/appraisal-help/tornado-straight-line-wind-appraisal/">tornado and straight-line wind appraisal</a> covers how replacement cost, actual cash value and depreciation figure into those disputes.</p>

<h2>From Main Street to the subdivisions</h2>
<h3>Main Street and Frenchtown</h3>
<p>The historic district along Main Street and the Frenchtown neighborhood to the north hold some of the oldest buildings in the region: brick and stone storefronts, frame and brick homes, some dating from the early 1800s. Repairs to these buildings involve:</p>
<ul>
<li>Soft historic brick and lime mortar that should not be patched with modern hard mortar</li>
<li>Wood windows, doors and trim that may need custom milling</li>
<li>Standing-seam metal or other specialty roofing</li>
<li>Historic preservation review for exterior changes in designated districts</li>
</ul>
<p>A standard estimate built on replacement-grade materials usually falls short. Mixed-use buildings with a shop downstairs and apartments upstairs add business income and rental questions on top.</p>

<h3>The subdivisions</h3>
<p>Most St. Charles County housing is newer: frame construction, asphalt shingles, vinyl siding and finished basements. Hail disputes here look like hail disputes everywhere: partial approvals, discontinued siding and roof slopes written as repairs instead of replacements. Finished basements also turn plumbing failures into bigger claims, since flooring, drywall, built-ins and contents all get wet. Sump failures and drain backups usually need a specific endorsement, so check yours.</p>

<h2>Is appraisal right for your claim?</h2>
<p>If the insurer agrees there is covered damage and you are stuck on the amount, appraisal may be a quicker path than continued back-and-forth. It will not decide whether something is covered; your policy and, if needed, a Missouri attorney handle that. Our <a href="/toolkit/">claim toolkit</a> has checklists to get your documentation in order first.</p>
<p>We serve St. Charles, St. Peters, O’Fallon, Cottleville and the rest of St. Charles County, and inspect on site.</p>""",
        "faqs": [
            ("My St. Charles home flooded from the Missouri River. Can appraisal help?",
             "Only if you have flood insurance and dispute the amount; standard homeowners policies exclude river flooding. NFIP policies have their own dispute procedures, so check your flood policy for what applies."),
            ("Do historic district rules on Main Street affect my insurance claim?",
             "They can affect what a proper repair includes, such as required materials or review before exterior work. Whether those added costs are covered depends on your policy, often its ordinance or law section."),
            ("Do you work in St. Peters and O’Fallon too?",
             "Yes. We serve St. Charles and the surrounding St. Charles County communities and inspect properties in person."),
        ],
    },
    # ------------------------------------------------------------------ St. Joseph
    {
        "slug": "st-joseph",
        "city": "St. Joseph",
        "geo": "St. Joseph",
        "county": "Buchanan County",
        "region": "Northwest Missouri",
        "perils": ["Missouri River floods", "Hail", "Wind", "Older-home repairs"],
        "housing": "St. Joseph has an unusually large stock of late 1800s brick mansions and Victorian homes on its hills, plus modest frame houses, post-war ranches and newer homes along the Belt Highway corridor.",
        "hoods": ["Museum Hill", "Hall Street Historic District", "Downtown St. Joseph", "Krug Park area", "Wyatt Park", "Belt Highway corridor", "Savannah (nearby)"],
        "storms": [
            ("2011", "Missouri River flood", "Prolonged high water on the Missouri kept levees around St. Joseph under strain for much of the summer."),
            ("2019", "Missouri River flood", "Spring flooding breached levees north of town and inundated the Rosecrans air base area."),
            ("Recurring", "Spring hail", "Hail and wind storms regularly cross Buchanan County in spring and early summer."),
        ],
        "near": ["kansas-city", "independence", "lees-summit"],
        "lede": "St. Joseph’s brick mansions and Victorian homes are some of the hardest houses in Missouri to estimate correctly. We help owners make sure the insurer prices the real building, and handle appraisal when needed.",
        "title": "St. Joseph MO Insurance Appraiser | Historic Homes",
        "desc": "St. Joseph, MO insurance appraiser for hail, wind and water claims on historic brick homes and newer houses. Estimate review and appraisal help.",
        "body": """<h2>A historic housing stock that defies software</h2>
<p>St. Joseph grew rich in the second half of the 1800s, and the money went into buildings. Museum Hill and the Hall Street Historic District are lined with large brick and stone homes: towers, slate roofs, stained glass, ornate porches and carved woodwork. Even the more modest homes from that era have plaster walls, tall ceilings and trim profiles nobody stocks anymore.</p>
<p>Insurance estimating software is built around average houses. When it meets a three-story Victorian with a slate roof and copper valleys, it tends to underprice. Typical gaps we see:</p>
<ul>
<li>Slate repairs priced as shingle, or slate replacement priced without the extra labor for steep pitches, turrets and hand-formed flashing</li>
<li>Plaster damage written as drywall patching</li>
<li>Box gutters and built-in drainage replaced with standard gutters</li>
<li>Stained or leaded glass written as plain glazing</li>
<li>No allowance for scaffolding on tall masonry walls</li>
</ul>
<p>None of this means the insurer will pay for a museum restoration. It means a fair estimate prices like-kind work on the house that is actually there.</p>

<h2>The river, and the line between flood and everything else</h2>
<p>The Missouri River runs along St. Joseph’s western edge. In 2011, prolonged high water kept levees under strain for much of the summer. In 2019, flooding breached levees north of town and put the Rosecrans air base area under water.</p>
<p>River flooding is excluded by standard homeowners and commercial property policies; it requires separate flood insurance. Neither appraisal nor anyone else can turn a flood loss into a covered homeowners claim. If you have a flood policy, it has its own procedures. If your damage came from wind-driven rain or a burst pipe instead, that is usually a different coverage path, and a dispute about the amount there may be a candidate for appraisal.</p>

<h2>Hail and wind on the hills</h2>
<p>Buchanan County gets its share of spring hail and summer wind. On the bluffs and hilltops where many older homes sit, wind exposure is higher, and large old trees add to the risk. After a storm, roofs are the obvious focus, but don’t forget:</p>
<ul>
<li>Ornamental metalwork and finials</li>
<li>Wood siding, shingles and porch details</li>
<li>Chimneys, which on older homes may need rebuilding with matching brick</li>
<li>Interior water staining that appears days later</li>
</ul>
<p>Our <a href="/appraisal-help/hail-roof-damage-appraisal/">hail and roof damage appraisal</a> page explains how we document those items.</p>

<h2>Local considerations and appraisal</h2>
<p>Work on historic properties may require approval from the city before exterior changes, and contractors who work on slate, masonry and old woodwork are in short supply in northwest Missouri. Both affect cost and timeline, and both belong in a realistic estimate.</p>
<p>Appraisal is for disputes about the amount of a covered loss. It does not resolve coverage denials, and the policy language controls. If your insurer has accepted the loss but undervalued it, an <a href="/appraisal-help/insurer-estimate-review/">insurer estimate review</a> is often the first step.</p>
<p>We serve St. Joseph and surrounding Buchanan County, and inspect on site.</p>""",
        "faqs": [
            ("My insurer priced my St. Joseph slate roof as asphalt shingles. Is that normal?",
             "It happens, especially with software-generated estimates. If the insurer accepts the damage but uses the wrong material or labor, appraisal can be used to resolve the amount of loss."),
            ("Does homeowners insurance cover Missouri River flooding in St. Joseph?",
             "No. Standard homeowners policies exclude flood. You would need a separate NFIP or private flood policy."),
            ("Does living in a historic district change my St. Joseph claim?",
             "It can. Required review or material rules may affect what a proper exterior repair includes; whether the extra cost is covered depends on your policy, often its ordinance or law section."),
        ],
    },
    # ------------------------------------------------------------------ Joplin
    {
        "slug": "joplin",
        "city": "Joplin",
        "geo": "Joplin",
        "county": "Jasper County",
        "region": "Southwest Missouri",
        "perils": ["Tornadoes", "Large hail", "Mine subsidence", "Ice storms"],
        "housing": "Joplin has Victorian-era homes in Murphysburg and near downtown, older frame houses and ranches across the city, and a large share of homes rebuilt after 2011 along the tornado’s path.",
        "hoods": ["Murphysburg Historic District", "Downtown Joplin", "20th Street corridor", "Range Line Road area", "Webb City (nearby)", "Carthage (nearby)", "Duquesne (nearby)"],
        "storms": [
            ("2011", "May 22 EF5 tornado", "A catastrophic EF5 tornado cut across the city, destroying neighborhoods, schools and a hospital."),
            ("Recurring", "Spring hail and wind", "Southwest Missouri sits in an active severe weather corridor that brings hail and damaging wind most years."),
        ],
        "near": ["springfield", "lees-summit", "kansas-city"],
        "lede": "Joplin knows tornado claims better than almost anywhere. We help homeowners and businesses get an accurate estimate on storm losses, and step in as appraiser when the insurer’s number is too low.",
        "title": "Joplin Insurance Appraiser | Tornado & Hail Claims, MO",
        "desc": "Joplin, MO insurance appraiser for tornado, hail and wind claims across Jasper and Newton counties. Estimate review, appraisal clause and umpire work.",
        "body": """<p>Anyone in Joplin can tell you where they were on May 22, 2011. The EF5 tornado that crossed the city that evening changed how residents think about storms, roofs, safe rooms and insurance. More than a decade later, a large share of the homes along that path are newer construction, while the rest of the city still has older housing that has weathered many storms since.</p>

<h2>What tornado and wind claims involve</h2>
<p>A major wind loss is not one claim; it is a dozen. Dwelling, other structures, contents, additional living expense, debris removal, tree removal, code upgrades and sometimes business income all have their own limits and their own disputes. The usual friction points are:</p>
<ul>
<li><strong>Total loss versus repair.</strong> Whether a heavily damaged home can be repaired at a reasonable cost, or should be valued as a total loss.</li>
<li><strong>Depreciation.</strong> How much is held back from actual cash value until the work is done, and whether it was calculated fairly.</li>
<li><strong>Hidden structural damage.</strong> Racked framing, shifted foundations and nail pops that do not show up on a quick inspection.</li>
<li><strong>Contents.</strong> Building an inventory from memory after everything has been scattered.</li>
</ul>
<p>Our page on <a href="/appraisal-help/tornado-straight-line-wind-appraisal/">tornado and straight-line wind appraisal</a> goes deeper on each of those.</p>

<h2>Hail, and roofs rebuilt after 2011</h2>
<p>Southwest Missouri sees regular hail. For homes rebuilt after 2011, many roofs are now reaching the age where carriers start applying more depreciation, or switching to actual-cash-value roof schedules at renewal. If you are not sure how your roof is insured, read your declarations page and endorsements before the next storm, not after. When a covered hail loss is underpaid, appraisal can resolve how much damage there is and what it costs to fix.</p>

<h2>The ground under Joplin</h2>
<p>The Joplin area was the heart of a historic lead and zinc mining district, and old shafts and workings still lie beneath parts of Jasper and Newton counties. Subsidence from old mines is a real, if occasional, problem. Most homeowners policies exclude earth movement, and mine subsidence may be excluded unless you have a specific endorsement. Ask your agent what your policy says, and talk to a Missouri attorney if a claim is denied. If the insurer accepts a ground-related loss and the fight is over repair costs, our <a href="/appraisal-help/sinkhole-ground-collapse-appraisal/">ground collapse appraisal</a> page explains how those estimates are built.</p>

<h2>Local notes</h2>
<p>Joplin spans two counties: most of the city is in Jasper County and the southern part is in Newton County. Permits and code items come from the city. After any big regional storm, demand for roofers and builders jumps, and out-of-town contractors arrive. Get your own documentation, check that anyone you hire holds whatever license or registration the city requires, and be wary of anyone who offers to negotiate your claim for you.</p>
<p>Older homes in Murphysburg and near downtown bring the usual old-house issues: plaster walls, wood windows, original trim and brick that has to be matched.</p>
<p>We serve Joplin and surrounding communities in Jasper and Newton counties, including Webb City, Carthage and Duquesne, and inspect on site.</p>""",
        "faqs": [
            ("My Joplin home was badly damaged by wind. Who decides if it is a total loss?",
             "Initially the insurer, based on its estimate. If you disagree about the amount of loss, including whether repair costs exceed the home’s value, appraisal may be used to resolve that dispute."),
            ("Is damage from old mine collapse covered?",
             "Often not under a standard homeowners policy, which typically excludes earth movement. Some policies or endorsements provide limited coverage, so check your wording and consult a Missouri attorney if your claim is denied."),
            ("Do you work in Webb City and Carthage?",
             "Yes. We serve Joplin and nearby Jasper and Newton County communities and inspect properties in person."),
        ],
    },
    # ------------------------------------------------------------------ Jefferson City
    {
        "slug": "jefferson-city",
        "city": "Jefferson City",
        "geo": "Jefferson City",
        "county": "Cole County",
        "region": "Mid-Missouri",
        "perils": ["Tornadoes", "Missouri River floods", "Hail", "Historic masonry"],
        "housing": "Missouri’s capital has brick rowhouses and 19th-century German-built homes in Old Munichburg and near the Capitol, mid-century neighborhoods on the south side and newer subdivisions on the city’s edges.",
        "hoods": ["Capitol Avenue district", "Old Munichburg", "Downtown", "the Southside", "Ellis Boulevard area", "North Jefferson", "Holts Summit (nearby)"],
        "storms": [
            ("1993", "Great Flood", "The Missouri River flooded North Jefferson and low-lying areas around the capital."),
            ("2019", "May 22 EF3 tornado", "A late-night tornado tore through the city, heavily damaging homes and buildings along a path that included the Ellis Boulevard area and downtown."),
            ("2019", "Missouri River flood", "Prolonged high water in spring and early summer again flooded North Jefferson and the Callaway County side."),
        ],
        "near": ["columbia", "chesterfield", "st-charles"],
        "lede": "Jefferson City has had tornado and flood claims in the same year. We help capital-area property owners make sense of the insurer’s estimate and use the appraisal clause when the amount is wrong.",
        "title": "Jefferson City Insurance Appraiser | Storm & Flood, MO",
        "desc": "Jefferson City, MO insurance appraiser for tornado, hail and storm claims on historic brick and newer homes. Estimate reviews and appraisal help.",
        "body": """<h2>2019, and what it taught capital-area owners</h2>
<p>Late on the night of May 22, 2019, an EF3 tornado moved through Jefferson City, damaging homes and buildings from the south side into downtown. Within weeks, the Missouri River was flooding North Jefferson and the Callaway County side, as it had in 1993. For many owners, that year meant dealing with two very different kinds of loss at once.</p>
<p>The lessons still apply:</p>
<ul>
<li><strong>Wind and flood are separate coverages.</strong> Tornado damage is usually covered under a homeowners or commercial policy. River flooding is not; it needs NFIP or private flood insurance.</li>
<li><strong>Documentation needs to be separated.</strong> If a property had both wind and water damage, photos, moisture readings and timelines need to show which caused what.</li>
<li><strong>Contractor capacity runs out.</strong> After a regional disaster, pricing climbs and timelines stretch. An estimate written right after the storm may not reflect what the work ends up costing.</li>
</ul>
<p>Our <a href="/appraisal-help/tornado-straight-line-wind-appraisal/">tornado and wind appraisal</a> page covers how those claims are measured.</p>

<h2>Old brick in the capital</h2>
<p>Jefferson City has deep German roots, and you can see it in the buildings. Old Munichburg, south of the Capitol, and the streets around Capitol Avenue have brick homes and commercial buildings from the 1800s and early 1900s. These were built with soft brick and lime mortar, and repairing them correctly means:</p>
<ul>
<li>Matching brick size, color and texture, often from salvage</li>
<li>Using compatible mortar rather than modern Portland mixes that can damage old brick</li>
<li>Repairing wood windows, cornices and trim instead of swapping in stock replacements</li>
<li>Planning for any historic review the city requires on exterior work</li>
</ul>
<p>An estimate that treats an 1880s brick building as if it were a modern veneer home will come in low. That is a dispute about amount, which appraisal can address.</p>

<h2>Two counties and a river</h2>
<p>Most of Jefferson City lies in Cole County south of the river. North Jefferson and Holts Summit are across the Missouri in Callaway County, in low ground that has flooded repeatedly. If you own property on that side, find out whether you are in a mapped flood zone and whether you carry flood insurance. Mortgage lenders often require it in high-risk zones, but plenty of owners just outside those zones go without.</p>
<p>Permits come from the city or the county depending on location, and code requirements for re-roofing or structural repairs can add costs. Ordinance or law coverage in your policy may pay some of those.</p>

<h2>When appraisal is the right tool</h2>
<p>Appraisal settles disagreements about the amount of a covered loss. It does not decide whether a loss is covered, and it cannot convert a flood into a wind claim. If the insurer accepts your claim but the estimate is too low, our <a href="/appraisal-roadmap/">appraisal roadmap</a> explains the process from demand to award. For legal questions about coverage, talk to a Missouri attorney.</p>
<p>We serve Jefferson City, Holts Summit and the surrounding Cole and Callaway County area, and inspect in person.</p>""",
        "faqs": [
            ("My Jefferson City home had both tornado and flood damage. How is that handled?",
             "Usually as two separate claims: wind damage under your homeowners policy and flood damage under a flood policy if you have one. Clear documentation of which damage came from which cause is essential."),
            ("Can appraisal be used if the insurer underpaid my old brick building?",
             "Yes, if the insurer accepts the loss as covered and the disagreement is over the cost of a proper repair, including matching brick and compatible mortar."),
            ("I live in North Jefferson. Do I really need flood insurance?",
             "North Jefferson sits in low ground across the river that has flooded in 1993 and 2019, and homeowners policies exclude flood. Whether to buy it is your decision, but without it a river flood is usually uninsured."),
        ],
    },
    # ------------------------------------------------------------------ Cape Girardeau
    {
        "slug": "cape-girardeau",
        "city": "Cape Girardeau",
        "geo": "Cape Girardeau",
        "county": "Cape Girardeau County",
        "region": "Southeast Missouri",
        "perils": ["Mississippi flooding", "Earthquake risk", "Hail and wind", "Ice storms"],
        "housing": "Cape Girardeau has brick commercial blocks and older homes near the downtown riverfront and in historic areas such as Red Star and Haarig, mid-century homes across the middle of town and newer subdivisions to the west toward Jackson.",
        "hoods": ["Downtown riverfront", "Broadway corridor", "Red Star", "Haarig", "Capaha Park area", "Kingshighway corridor", "Jackson (nearby)"],
        "storms": [
            ("1993", "Great Flood", "The Mississippi rose to historic levels; the floodwall protected downtown while low areas outside it flooded."),
            ("2015–16", "Winter record crest", "Heavy December rains pushed the Mississippi to a record crest at Cape Girardeau around the turn of the year."),
            ("Recurring", "Severe storms", "Southeast Missouri regularly sees spring hail, damaging wind and occasional winter ice."),
        ],
        "near": ["st-louis", "chesterfield", "st-charles"],
        "lede": "Cape Girardeau lives with the Mississippi, the New Madrid seismic zone and regular severe storms. We help owners understand what their policy covers, check the estimate and handle appraisal on covered losses.",
        "title": "Cape Girardeau Insurance Appraiser | Storm Claims, MO",
        "desc": "Cape Girardeau, MO insurance appraiser for storm, hail and water claims in Southeast Missouri. Estimate review, appraisal clause and umpire services.",
        "body": """<p>Living in Cape Girardeau means paying attention to the river. The floodwall along downtown has been tested more than once, including during the Great Flood of 1993 and again when the Mississippi reached a record crest around the start of 2016. Add the New Madrid seismic zone to the south and regular spring storms, and Southeast Missouri owners face a set of risks that do not all sit under one policy.</p>

<h2>Know which policy covers what</h2>
<p>Before talking about estimates, it helps to be clear on coverage, because it is easy to assume one policy covers everything:</p>
<ul>
<li><strong>Wind, hail, fire and most sudden water damage</strong> are generally covered under homeowners or commercial property policies, subject to deductibles and exclusions.</li>
<li><strong>Flood</strong> is excluded from those policies. It needs a separate NFIP or private flood policy, and properties outside the floodwall or in low-lying areas should take it seriously.</li>
<li><strong>Earthquake</strong> is usually excluded too, and typically requires a separate endorsement or policy with its own deductible, often a percentage of the dwelling limit.</li>
<li><strong>Sewer and drain backup</strong> usually requires its own endorsement.</li>
</ul>
<p>Appraisal decides the amount of a covered loss. It cannot add coverage you do not have. If you are unsure about coverage, check your declarations page, ask your agent, or talk to a Missouri attorney.</p>

<h2>Storm claims on older and newer homes</h2>
<h3>Near the river and downtown</h3>
<p>Downtown and the historic areas around Red Star and Haarig have brick commercial blocks, older frame homes and houses with plaster walls and original woodwork. Hail and wind damage to these buildings often involves specialty roofing, masonry repairs, wood windows and trim that standard estimates underprice.</p>
<h3>West Cape and Jackson</h3>
<p>Newer subdivisions on the west side and toward Jackson mostly have asphalt roofs, vinyl siding and modern finishes. Disputes there center on roof replacement versus repair, siding that no longer matches and whether all affected elevations were included. Our <a href="/appraisal-help/hail-roof-damage-appraisal/">hail and roof damage</a> page covers how we approach those.</p>
<h3>Winter weather</h3>
<p>Southeast Missouri also gets occasional ice storms, which bring down trees and power lines and can lead to frozen pipes in homes that lose heat. Those claims often combine roof damage, interior water and spoiled food or contents. The <a href="/appraisal-help/winter-storm-ice-damage-appraisal/">winter storm and ice damage</a> page explains how they fit together.</p>

<h2>Local factors in your estimate</h2>
<p>Cape Girardeau is the regional hub for Southeast Missouri, and contractors here often serve a wide rural area. After a major storm, demand stretches across several counties, and prices and timelines move accordingly. Permits and code requirements come from the city or the county depending on where the property sits.</p>
<p>For buildings near the floodwall or in mapped flood zones, any substantial repair may also bring floodplain rules into play, which can affect what a rebuild must include.</p>

<h2>Considering appraisal</h2>
<p>If your insurer has accepted a claim but you believe its estimate is too low, appraisal lets each side choose an appraiser, with an umpire to resolve differences. It is generally quicker than litigation, but it has costs, and it only addresses the amount. Many owners start with an estimate review to see how big the gap really is.</p>
<p>We serve Cape Girardeau, Jackson and surrounding Southeast Missouri, and inspect on site.</p>""",
        "faqs": [
            ("Does my Cape Girardeau homeowners policy cover earthquake damage?",
             "Usually not. Earthquake coverage is typically a separate endorsement or policy with its own deductible. Check your declarations page to see whether you have it."),
            ("My property flooded from the Mississippi. Can appraisal help?",
             "Only if you carry flood insurance and disagree on the amount. Standard homeowners policies exclude flood, and NFIP policies have their own dispute procedures."),
            ("What if I live outside the Cape Girardeau floodwall?",
             "Property outside the floodwall or in mapped low areas carries more river flood exposure. Flood damage needs a separate flood policy, and any substantial repair may also bring local floodplain rules into play."),
        ],
    },
    # ------------------------------------------------------------------ Chesterfield
    {
        "slug": "chesterfield",
        "city": "Chesterfield",
        "geo": "Chesterfield",
        "county": "St. Louis County",
        "region": "St. Louis Metro",
        "perils": ["Hail", "Wind", "Valley flooding", "High-value homes"],
        "housing": "Chesterfield is mostly suburban, with large single-family homes from the 1970s onward, upscale subdivisions with cedar, slate or tile roofs, condos and villas, and commercial development in Chesterfield Valley.",
        "hoods": ["Chesterfield Valley", "Wild Horse Creek Road area", "Baxter Road area", "Clarkson Valley (nearby)", "Town and Country (nearby)", "Wildwood (nearby)", "Ballwin (nearby)"],
        "storms": [
            ("1993", "Chesterfield Valley flood", "A levee failure during the Great Flood put Chesterfield Valley under deep water."),
            ("Recurring", "Spring hail", "Hailstorms crossing west St. Louis County regularly damage roofs, siding and windows in Chesterfield neighborhoods."),
        ],
        "near": ["st-louis", "st-charles", "columbia"],
        "lede": "Chesterfield homes tend to be larger and built with premium materials, which makes underpriced estimates expensive. We help owners and associations get an accurate number and pursue appraisal when needed.",
        "title": "Chesterfield Insurance Appraiser | Hail & Storm, MO",
        "desc": "Chesterfield, MO insurance appraiser for hail and storm claims on larger homes, condos and HOAs in west St. Louis County. Estimates and appraisal.",
        "body": """<h2>Bigger homes, bigger gaps</h2>
<p>Chesterfield’s housing is mostly suburban and mostly substantial. Many homes are large, with complex rooflines, multiple gables and dormers, and premium materials: designer shingles, cedar shakes, slate, concrete or clay tile, stone veneer and custom windows. When a hailstorm crosses west St. Louis County, those features drive up the cost of a proper repair, and they are exactly where insurer estimates tend to fall short.</p>
<p>Common problems we see on Chesterfield claims:</p>
<ul>
<li>Premium roofing priced as standard architectural shingles</li>
<li>Steep-pitch and high-roof labor charges missing or understated</li>
<li>Copper or specialty flashing and gutters swapped for basic aluminum</li>
<li>Custom windows and doors priced as stock units</li>
<li>Interior finishes such as hardwood, millwork and high-end paint systems underpriced</li>
</ul>
<p>Higher-value homes often carry policies with extended replacement cost or guaranteed replacement provisions. Those terms do not change how damage is measured, but they can matter a great deal for large losses. Read them before the claim, not after.</p>

<h2>The valley and the levee</h2>
<p>Chesterfield Valley, the flat land along the Missouri River, was under deep water in 1993 after a levee failed during the Great Flood. Since then the levee system has been improved and the valley has filled with retail, offices and industry. It is still floodplain.</p>
<p>For business owners there, flood insurance is a separate decision from property insurance, and business interruption from a flood is often not covered by a standard commercial policy. For storm claims on commercial buildings, roofs are large and costly, and estimates often miss items such as roof-top equipment, membrane details and insulation. See <a href="/appraisal-help/commercial-hoa-appraisal/">commercial and HOA appraisal</a> for how those claims run.</p>

<h2>Condos, villas and associations</h2>
<p>A lot of Chesterfield residents live in condos, villas or HOA communities. After a storm, the first question is who insures what. The association’s master policy may cover roofs and exteriors, while unit owners cover interiors and improvements. Your declarations and the master policy decide where the line falls. Associations facing a large hail claim across many buildings often benefit from an independent estimate before negotiating.</p>

<h2>Local notes and the appraisal decision</h2>
<p>Chesterfield is a city within St. Louis County, and building permits and code enforcement run through the city and, for some work, the county. Many subdivisions also have trustees or HOAs with architectural rules on roofing and exterior materials, which can shape what a realistic repair looks like.</p>
<p>The western part of the county also has karst ground in places, and sinkholes are not unheard of. As elsewhere, earth movement is generally excluded unless your policy says otherwise.</p>
<p>Appraisal fits when the insurer accepts the loss but you disagree on the amount. It does not decide coverage, and the policy language controls. If you want to know whether your estimate is in the right range before deciding, start with an <a href="/appraisal-help/insurer-estimate-review/">insurer estimate review</a>.</p>
<p>We serve Chesterfield and nearby west county communities, including Clarkson Valley, Town and Country, Wildwood and Ballwin, and inspect on site.</p>""",
        "faqs": [
            ("My Chesterfield home has a tile roof. Will the insurer replace it with tile?",
             "Most replacement cost policies pay for like kind and quality, which would generally mean tile. If the insurer accepts the damage but disputes the amount or material, appraisal may resolve the amount of loss."),
            ("I own a condo. Is the roof my claim or the association’s?",
             "It depends on your association’s governing documents and the master policy. Often the association insures roofs and exteriors, while unit owners insure interiors."),
            ("Is Chesterfield Valley still a flood risk?",
             "It is still floodplain despite levee improvements. Flood damage requires separate flood insurance, which standard property policies do not provide."),
        ],
    },
]
