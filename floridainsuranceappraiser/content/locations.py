"""City / location pages for floridainsuranceappraiser.com.

Each record follows content/SCHEMA.md plus location-specific fields:
city, county, region, lat, lng, neighborhoods, storms, claim_issues, nearby.
"""

_PART_A = [
    # ------------------------------------------------------------------ MIAMI
    {
        "slug": "miami-fl",
        "city": "Miami",
        "county": "Miami-Dade County",
        "region": "South Florida",
        "lat": "25.7617",
        "lng": "-80.1918",
        "title": "Miami Insurance Appraiser | Property Claim Appraisal",
        "description": "Independent insurance appraiser for Miami and Miami-Dade County homes, condos and businesses. Resolve hurricane, roof and water claim disputes by appraisal.",
        "h1": "Insurance Appraiser in Miami, FL",
        "kicker": "Miami-Dade claim appraisal",
        "lead": "When you and your insurer agree a Miami loss is covered but cannot agree on what it costs to fix, the appraisal clause gives you a way to settle the number without a lawsuit. We prepare independent, line-item valuations built around Miami-Dade’s building rules and pricing.",
        "neighborhoods": ["Brickell", "Coconut Grove", "Little Havana", "Coral Gables", "Kendall", "Doral", "Miami Beach", "Homestead"],
        "storms": [
            (1992, "Hurricane Andrew", "Andrew’s landfall in south Miami-Dade flattened large parts of Homestead and Cutler Bay and led directly to the county’s stricter product-approval rules."),
            (2005, "Hurricane Wilma", "Wilma crossed the peninsula and broke windows and damaged facades in downtown and Brickell high-rises, along with widespread roof and fence damage."),
            (2017, "Hurricane Irma", "Irma brought storm surge into Brickell Avenue and coastal neighborhoods and hurricane-force gusts across much of the county."),
        ],
        "claim_issues": [
            "High-rise condo water intrusion through windows, sliders and balconies",
            "Code-upgrade costs under High-Velocity Hurricane Zone rules",
            "Concrete tile and flat-roof membrane disputes",
            "Pipe and AC-line leaks in older garden-style condos",
            "Mixed condo association vs. unit-owner scope questions",
        ],
        "sections": [
            ("Why Miami claims are priced differently",
             '<p>Miami-Dade sits inside Florida’s High-Velocity Hurricane Zone (HVHZ), and that single fact shapes almost every repair estimate in the county. Roofing, windows, doors and shutters generally need product approvals and installation methods that go beyond what much of the state requires, permitting is more involved, and qualified labor is in steady demand. An estimate written from statewide or national pricing tables can miss those costs entirely.</p>'
             '<p>When we value a Miami loss, we look at what a licensed contractor would actually need to do to put the property back to code-compliant condition: the approved materials, the inspections, the tear-off and disposal, and whether your policy’s ordinance-or-law provisions may come into play. Coverage questions belong to you, your insurer and, if needed, your attorney; our job is to make sure the dollar figure reflects real Miami-Dade conditions.</p>'),
            ("Condos, towers and the water that gets in",
             '<p>From Brickell and Edgewater to Miami Beach and Sunny Isles, a large share of the county lives in multi-story concrete buildings. The common claim pattern we see is wind-driven rain entering through window systems, sliding doors and balcony thresholds, then traveling through drywall, flooring and the units below. These losses often involve two policies, the association’s master policy and the unit owner’s HO-6, and disputes over where one scope ends and the other begins.</p>'
             '<p>Appraisal does not decide which policy pays for what, but it can fix the amount of loss for each scope once coverage is settled. Our <a href="/appraisal-services/condo-hoa-claim-appraisal/">condo and HOA claim appraisal</a> work focuses on documenting moisture paths, matching finishes in shared areas, and separating unit-level damage from building components.</p>'),
            ("Single-family homes from the Gables to Homestead",
             '<p>Outside the towers, Miami’s housing stock runs from 1920s Mediterranean Revival homes in Coral Gables and Coconut Grove to mid-century ranch homes in Westchester and Kendall and newer construction in Doral and the Redland. Older homes raise questions about matching discontinued barrel tile, plaster walls and original wood floors. Post-Andrew homes in south Miami-Dade were often built or rebuilt to tougher standards, but their roofs and openings are now reaching the age where carriers argue wear and tear.</p>'
             '<p>Our <a href="/appraisal-services/roof-claim-appraisal/">roof claim appraisal</a> service looks at tile breakage patterns, underlayment condition and the true cost of a compliant re-roof rather than a patch that cannot be permitted.</p>'),
            ("How we work a Miami appraisal",
             '<p>Florida Insurance Appraiser is an independent appraisal firm that serves Miami-Dade as part of our statewide coverage. If your policy contains an appraisal clause and you invoke it, each side typically names its own appraiser, and the two appraisers try to agree on the amount of loss; if they cannot, an umpire decides the disputed items. The exact wording varies by policy, so read yours closely.</p>'
             '<ul><li>We inspect, photograph and measure the damage ourselves.</li><li>We build an itemized estimate using current South Florida pricing.</li><li>We negotiate the numbers with the carrier’s appraiser and present them to the umpire if needed.</li></ul>'
             '<p>You can read a step-by-step overview on our <a href="/appraisal-process/">appraisal process</a> page, or try the <a href="/claim-tools/appraisal-worth-it-calculator/">appraisal worth-it calculator</a> to see whether the gap in your claim justifies the cost.</p>'),
        ],
        "faqs": [
            ("Does appraisal decide whether my Miami claim is covered?",
             "No. Appraisal sets the amount of loss for damage that is covered. If your insurer denied coverage outright, that is usually a question for a public adjuster or attorney rather than an appraiser."),
            ("Do HVHZ code requirements affect my claim value?",
             "They can. Repairs in Miami-Dade often have to meet High-Velocity Hurricane Zone standards, and whether those upgrade costs are payable depends on your policy’s ordinance-or-law coverage. We price the work as it would actually need to be done."),
            ("Can you handle both the condo association and individual unit claims?",
             "Florida Insurance Appraiser can be retained by an association or by a unit owner, though not by both sides of the same dispute. We will confirm there is no conflict before taking the assignment."),
        ],
        "nearby": ["fort-lauderdale-fl", "west-palm-beach-fl", "naples-fl"],
    },
    # ------------------------------------------------------------------ TAMPA
    {
        "slug": "tampa-fl",
        "city": "Tampa",
        "county": "Hillsborough County",
        "region": "Tampa Bay",
        "lat": "27.9506",
        "lng": "-82.4572",
        "title": "Tampa Insurance Appraiser | Claim Appraisal Help",
        "description": "Independent insurance appraisal for Tampa and Hillsborough County property claims, from storm surge and wind damage to sinkholes, roofs and water losses.",
        "h1": "Insurance Appraiser in Tampa, FL",
        "kicker": "Hillsborough County appraisal",
        "lead": "Tampa’s recent hurricane seasons, combined with the ground conditions in Florida’s sinkhole belt, have produced a lot of claims where the insurer and the owner are far apart on price. We help Tampa property owners use the appraisal clause to resolve that gap on the numbers.",
        "neighborhoods": ["South Tampa", "Hyde Park", "Davis Islands", "Seminole Heights", "Carrollwood", "Westchase", "Brandon", "New Tampa"],
        "storms": [
            (2017, "Hurricane Irma", "Irma weakened as it passed east of the bay but still downed oaks, damaged roofs and knocked out power across Hillsborough County."),
            (2023, "Hurricane Idalia", "Idalia stayed offshore but pushed surge onto Bayshore Boulevard and low-lying South Tampa streets."),
            (2024, "Hurricane Helene", "Helene’s surge flooded Davis Islands, Harbour Island and other bayfront areas well beyond previous high-water marks."),
            (2024, "Hurricane Milton", "Two weeks after Helene, Milton brought damaging winds, heavy rain and tornadoes across the Tampa Bay area."),
        ],
        "claim_issues": [
            "Wind vs. surge allocation on bayfront homes",
            "Sinkhole and ground-cover collapse claims",
            "Tree-fall roof and structural damage",
            "Back-to-back storm losses on the same property",
            "Shingle roof replacement vs. repair disputes",
        ],
        "sections": [
            ("Two storms, one property: a Tampa problem",
             '<p>The 2024 season left many Tampa owners with something insurers and policyholders rarely plan for: two major events on the same house within weeks. Helene’s surge soaked first floors in South Tampa and on the islands, and Milton’s wind and rain followed before many repairs had begun. That creates hard questions about which damage came from which storm, which deductible applies, and how much of the loss falls under a flood policy rather than the homeowners policy.</p>'
             '<p>Allocation and coverage are not decided in appraisal, but once those lines are drawn, the dollar value of each piece still has to be measured. Documenting the property carefully, storm by storm, matters. Our <a href="/appraisal-services/hurricane-claim-appraisal/">hurricane claim appraisal</a> work is built around that kind of layered loss.</p>'),
            ("Sinkhole country",
             '<p>Hillsborough, along with neighboring Pasco and Hernando counties, sits in the part of Florida often called “sinkhole alley,” where limestone below the surface can dissolve and leave voids. Cracked slabs, separating walls, sticking doors and sloping floors can point to ground movement, though they can also come from ordinary settlement. Florida policies treat catastrophic ground cover collapse and broader sinkhole loss differently, and coverage often depends on what you purchased.</p>'
             '<p>Where a sinkhole loss is accepted but the repair method or cost is in dispute, for example grouting and underpinning versus a more limited approach, appraisal may help settle the amount. See our <a href="/appraisal-services/sinkhole-claim-appraisal/">sinkhole claim appraisal</a> page for how we approach engineering reports and repair scopes.</p>'),
            ("Tampa’s housing stock and what it means for estimates",
             '<p>Tampa mixes 1920s bungalows in Seminole Heights and Hyde Park, block ranch homes from the post-war decades, and large master-planned subdivisions in Westchase, New Tampa and Brandon. Old-growth live oaks are part of the city’s character and a frequent source of roof and structural claims when limbs come down. Older wood-frame homes raise matching and plaster questions; newer stucco-over-block homes raise questions about hidden moisture after wind-driven rain.</p>'
             '<p>We price each of these with the local labor and material costs Tampa contractors are actually charging, not a generic statewide average.</p>'),
            ("Working with Florida Insurance Appraiser in Tampa",
             '<p>Florida Insurance Appraiser serves Tampa and the rest of the bay area as part of our statewide practice. We are appraisers, not public adjusters or attorneys: we do not negotiate coverage or give legal advice. What we do is inspect, document and value the damage, then work the numbers with the insurer’s appraiser and, if needed, an umpire.</p>'
             '<p>If you are not sure whether appraisal is the right move, start with our <a href="/claim-tools/appraisal-readiness-quiz/">appraisal readiness quiz</a> or review the <a href="/appraisal-process/">appraisal process</a> from demand letter to award.</p>'),
        ],
        "faqs": [
            ("Can appraisal separate Helene damage from Milton damage?",
             "Appraisers can value the damage observed and, where the evidence allows, describe it by cause, but whether a policy covers a given cause is a coverage question. Strong photo and date documentation helps any later allocation."),
            ("Is my Tampa sinkhole claim a good fit for appraisal?",
             "It can be when the insurer accepts the loss but disputes the repair cost or method. If the dispute is whether there is a sinkhole at all, or whether you bought sinkhole coverage, that is usually outside appraisal."),
            ("Do you charge Tampa homeowners for an initial conversation?",
             "Call us and we will talk through your claim and whether appraisal fits before any engagement. Fee arrangements are explained in writing up front."),
        ],
        "nearby": ["st-petersburg-fl", "sarasota-fl", "orlando-fl"],
    },
    # ---------------------------------------------------------------- ORLANDO
    {
        "slug": "orlando-fl",
        "city": "Orlando",
        "county": "Orange County",
        "region": "Central Florida",
        "lat": "28.5383",
        "lng": "-81.3792",
        "title": "Orlando Insurance Appraiser | Claim Appraisal Help",
        "description": "Independent property claim appraisal for Orlando and Central Florida homes and businesses: hurricane wind, hail, roof, water and inland flooding disputes.",
        "h1": "Insurance Appraiser in Orlando, FL",
        "kicker": "Central Florida appraisal",
        "lead": "Inland doesn’t mean safe from storms. Orlando property owners deal with hurricanes that arrive still strong, summer thunderstorms that drop hail, and heavy rain that overwhelms neighborhoods, and we help them settle underpaid claims through appraisal.",
        "neighborhoods": ["Winter Park", "College Park", "Dr. Phillips", "Lake Nona", "Kissimmee", "Winter Garden", "Altamonte Springs", "Oviedo"],
        "storms": [
            (2004, "Hurricane Charley", "Charley raced inland from Punta Gorda and crossed Orlando as a hurricane, toppling trees and damaging roofs across Orange County."),
            (2017, "Hurricane Irma", "Irma’s wind and rain caused widespread tree damage, roof losses and long power outages throughout the metro area."),
            (2022, "Hurricane Ian", "Ian stalled over Central Florida and its rainfall flooded neighborhoods such as Orlo Vista and areas along the Little Wekiva River."),
        ],
        "claim_issues": [
            "Hail and wind damage from summer thunderstorms",
            "Shingle roofs on 1990s-2000s subdivision homes",
            "Rain intrusion vs. long-term leak disputes",
            "Pool enclosure and screen cage losses",
            "Small commercial and hospitality property claims",
        ],
        "sections": [
            ("Orlando’s inland storm profile",
             '<p>Because Orlando sits in the middle of the peninsula, people often assume hurricanes lose their punch before they get there. Charley in 2004 and Ian in 2022 proved otherwise in different ways: Charley with fast-moving wind, Ian with slow, extraordinary rainfall. Add the near-daily summer thunderstorms that can bring hail, microbursts and lightning, and Central Florida produces a steady stream of roof, window and interior water claims.</p>'
             '<p>The common dispute is not whether something happened but how much damage it caused. Insurers may approve a handful of shingles where an owner sees a roof that cannot be repaired without replacement, or approve drying where the owner sees ruined cabinets and flooring.</p>'),
            ("Subdivision roofs and the repair-or-replace question",
             '<p>Much of metro Orlando, from Winter Garden and Ocoee to Oviedo, Lake Nona and Kissimmee, was built out in large subdivisions from the 1980s onward, overwhelmingly with asphalt shingle roofs. Many of those roofs are now old enough that carriers push back on replacement, arguing that damage is wear and tear or that a repair is enough. Matching discontinued shingle colors and profiles is a frequent sticking point.</p>'
             '<p>Our <a href="/appraisal-services/roof-claim-appraisal/">roof claim appraisal</a> looks at hail and wind indicators, brittleness, repairability and what a code-compliant repair would really require. The <a href="/claim-tools/roof-measurement-calculator/">roof measurement calculator</a> is a quick way to sanity-check the square footage in your carrier’s estimate.</p>'),
            ("Water inside the house",
             '<p>Heavy rain finds its way through flashing, around windows and under doors, and in Orlando it often arrives with enough volume to saturate walls before anyone notices. Many policies treat sudden water damage very differently from long-term seepage, and Florida policies have increasingly added limits or exclusions in this area, so the wording of your policy matters. Where the event is accepted and only the scope or pricing is in dispute, appraisal can be a practical path.</p>'
             '<p>See <a href="/appraisal-services/water-damage-claim-appraisal/">water damage claim appraisal</a> for how we document moisture readings, materials and drying versus replacement.</p>'),
            ("Florida Insurance Appraiser in Central Florida",
             '<p>Florida Insurance Appraiser works throughout Orange, Seminole, Osceola and Lake counties as part of our statewide service. Clients range from homeowners in College Park and Winter Park to owners of rental homes, small offices and hospitality properties near the tourist corridor. We do not represent you on coverage and we are not lawyers; we are retained to prepare and defend a fair, documented amount of loss through the appraisal process.</p>'),
        ],
        "faqs": [
            ("Does hail really happen in Orlando?",
             "Yes. Central Florida thunderstorms can produce hail, especially in spring and early summer. Hail damage on shingles and screen enclosures is a common appraisal topic."),
            ("Can appraisal help if my Orlando home flooded from rain during Ian?",
             "It depends on the policy. Rising water is usually covered under a separate flood policy, not homeowners coverage. If a covered claim has a dispute over price, appraisal may apply under whichever policy contains the clause."),
            ("How long does an Orlando appraisal take?",
             "It varies with the size of the loss and how quickly the other appraiser engages. Smaller residential disputes may resolve in weeks; complex or commercial claims, or those that go to an umpire, can take longer."),
        ],
        "nearby": ["tampa-fl", "jacksonville-fl", "st-petersburg-fl"],
    },
    # ----------------------------------------------------------- JACKSONVILLE
    {
        "slug": "jacksonville-fl",
        "city": "Jacksonville",
        "county": "Duval County",
        "region": "Northeast Florida",
        "lat": "30.3322",
        "lng": "-81.6557",
        "title": "Jacksonville Insurance Appraiser | Claim Appraisal",
        "description": "Independent insurance appraiser for Jacksonville and Northeast Florida property claims, including river flooding, wind, roof, tree-fall and water losses.",
        "h1": "Insurance Appraiser in Jacksonville, FL",
        "kicker": "Northeast Florida appraisal",
        "lead": "Jacksonville covers more ground than any other city in the continental U.S., and its claims are just as varied, from riverfront homes in San Marco to beach condos and inland subdivisions. We give Duval County owners an independent valuation when their insurer’s number falls short.",
        "neighborhoods": ["Riverside", "Avondale", "San Marco", "Mandarin", "Arlington", "Southside", "Jacksonville Beach", "Ponte Vedra Beach"],
        "storms": [
            (1964, "Hurricane Dora", "Dora came ashore near St. Augustine and remains the benchmark direct hurricane strike for the Jacksonville area."),
            (2016, "Hurricane Matthew", "Matthew stayed just offshore but brought surge, beach erosion and wind damage to the beaches and along the St. Johns River."),
            (2017, "Hurricane Irma", "Irma pushed the St. Johns River to record levels, flooding downtown, San Marco and Riverside streets far from the ocean."),
        ],
        "claim_issues": [
            "St. Johns River and tidal flooding vs. wind damage",
            "Historic homes in Riverside, Avondale and Springfield",
            "Fallen oak and pine trees on roofs",
            "Beach condo and townhome wind-driven rain",
            "Hip-and-gable shingle roof disputes",
        ],
        "sections": [
            ("The river changes the claim",
             '<p>Many people think of Jacksonville’s storm risk as an oceanfront issue, but Irma showed that the St. Johns River can carry surge and rainfall deep into the city. Homes in San Marco, Riverside, Ortega and along the tributaries saw water that had nothing to do with the beach. That makes the line between flood damage, usually covered under a separate flood policy, and wind or rain damage under a homeowners policy especially important in Duval County.</p>'
             '<p>Appraisal does not redraw that line; it measures the cost of the damage on each side of it once the coverage picture is clear. A careful inspection that records water lines, roof and window damage, and interior conditions gives everyone a better starting point.</p>'),
            ("Historic neighborhoods, older materials",
             '<p>Riverside, Avondale, Springfield and parts of San Marco hold some of the oldest housing stock in Florida, with heart-pine floors, plaster walls, original wood windows and slate, tile or specialty shingle roofs. Insurers sometimes price those homes as if they were built last year with stock materials. Repairing them properly can mean specialty trades, matching profiles and longer timelines.</p>'
             '<p>Our <a href="/appraisal-services/homeowners-claim-appraisal/">homeowners claim appraisal</a> service accounts for like-kind-and-quality materials and the labor older homes actually require, and our <a href="/appraisal-services/xactimate-estimate-review/">Xactimate estimate review</a> can show where a carrier estimate has substituted cheaper line items.</p>'),
            ("Trees, wind and the suburbs",
             '<p>Further out, in Mandarin, Arlington, the Southside and into Clay and St. Johns counties, the typical home is a block or frame house with a shingle roof under a canopy of oaks and pines. Northeast Florida also gets strong summer storms and the occasional nor’easter. A large limb through a roof can cause structural framing damage, ceiling collapse and water damage that spreads well past the impact point, and the initial estimate often captures only the obvious hole.</p>'),
            ("How Florida Insurance Appraiser helps in Jacksonville",
             '<p>Florida Insurance Appraiser serves Jacksonville, the Beaches and surrounding counties as part of our statewide work. When your policy has an appraisal provision and you decide to use it, we act as your appraiser: we inspect, build an itemized estimate, and work with the insurer’s appraiser to reach an agreed amount. If the two of us cannot agree, the umpire decides the items in dispute.</p>'
             '<p>Timing matters in Florida, where notice and filing deadlines have shortened in recent years. Our <a href="/claim-tools/claim-deadline-calculator/">claim deadline calculator</a> gives a general sense of the timelines, but confirm your specific deadlines with your policy or an attorney.</p>'),
        ],
        "faqs": [
            ("Is river flooding covered by my Jacksonville homeowners policy?",
             "Typically not. Rising water from rivers or surge is usually covered under a separate flood policy. Wind and wind-driven rain damage may fall under homeowners coverage. Your policy language controls."),
            ("Can appraisal help with a historic home in Riverside or Avondale?",
             "Yes, if the dispute is about the cost to repair covered damage. Appraisal is often useful when an estimate ignores the materials and craftsmanship an older home needs."),
            ("Do you travel to the Beaches and St. Johns County?",
             "Yes. We serve all of Northeast Florida, including Jacksonville Beach, Neptune Beach, Atlantic Beach, Ponte Vedra and St. Augustine."),
        ],
        "nearby": ["tallahassee-fl", "orlando-fl", "pensacola-fl"],
    },
    # -------------------------------------------------------- FORT LAUDERDALE
    {
        "slug": "fort-lauderdale-fl",
        "city": "Fort Lauderdale",
        "county": "Broward County",
        "region": "South Florida",
        "lat": "26.1224",
        "lng": "-80.1373",
        "title": "Fort Lauderdale Insurance Appraiser | Claim Appraisal",
        "description": "Independent insurance appraisal for Fort Lauderdale and Broward County condos, homes and businesses facing underpaid wind, water, roof or flood-related claims",
        "h1": "Insurance Appraiser in Fort Lauderdale, FL",
        "kicker": "Broward County appraisal",
        "lead": "Fort Lauderdale combines dense oceanfront condos, waterfront homes along miles of canals, and inland suburbs, all inside the High-Velocity Hurricane Zone. We help Broward owners resolve price disputes on covered claims through the appraisal clause.",
        "neighborhoods": ["Las Olas", "Victoria Park", "Coral Ridge", "Rio Vista", "Wilton Manors", "Lauderdale-by-the-Sea", "Plantation", "Pompano Beach"],
        "storms": [
            (2005, "Hurricane Wilma", "Wilma caused some of the worst wind damage in Broward’s modern history, shattering high-rise windows and stripping roofs countywide."),
            (2017, "Hurricane Irma", "Irma brought hurricane-force gusts, downed trees and long outages across Broward County."),
            (2023, "April 2023 Rain Event", "A slow-moving storm system dropped more than two feet of rain on Fort Lauderdale in about a day, flooding homes, cars and streets."),
        ],
        "claim_issues": [
            "Condo window, slider and balcony water intrusion",
            "Plumbing and AC-line leaks in older mid-rise buildings",
            "HVHZ roofing and code-upgrade costs",
            "Rain flooding vs. covered water damage",
            "Waterfront seawall-adjacent home damage",
        ],
        "sections": [
            ("Broward’s building code backdrop",
             '<p>Like Miami-Dade, Broward County is part of Florida’s High-Velocity Hurricane Zone. Roof coverings, windows, doors and shutters generally have to meet stricter testing and installation standards, and permitting and inspections reflect that. When a carrier’s estimate treats a Broward roof like one in a lower wind zone, the shortfall can be significant.</p>'
             '<p>Whether code-driven upgrade costs are payable depends on your ordinance-or-law coverage, which is a coverage question. What we can do is make sure the repair is priced the way a Broward contractor would actually have to perform it.</p>'),
            ("Condo country along A1A",
             '<p>Fort Lauderdale’s beach, the Galt Ocean Mile, Lauderdale-by-the-Sea and Pompano Beach are lined with condominium towers and mid-rise buildings, many dating to the 1960s through the 1980s. Common claims include water through aging window systems and balcony doors, failed plumbing stacks and AC lines, and roof leaks that travel through several floors. Recent Florida condo safety laws have also put many associations under pressure on structural repairs, which can complicate the claim picture.</p>'
             '<p>Our <a href="/appraisal-services/condo-hoa-claim-appraisal/">condo and HOA claim appraisal</a> work helps associations and unit owners document scope by unit and common element so the amount of loss can be fixed fairly.</p>'),
            ("When the rain came in 2023",
             '<p>The April 2023 rain event dropped extraordinary rainfall on Fort Lauderdale in a short time, and many homeowners found water inside their homes without any hurricane in sight. How those losses are covered depends heavily on the source of the water: rising surface water is generally a flood policy matter, while water entering through a damaged roof or opening may fall under a homeowners policy. Where coverage is accepted and the dispute is about scope or pricing, appraisal may be an option.</p>'
             '<p>Our <a href="/appraisal-services/water-damage-claim-appraisal/">water damage claim appraisal</a> page explains how we document moisture, materials and drying.</p>'),
            ("Working with Florida Insurance Appraiser in Broward",
             '<p>Florida Insurance Appraiser serves Fort Lauderdale and all of Broward County, from Hollywood and Hallandale to Coral Springs and Weston, as part of our statewide practice. We act as your appraiser under the policy’s appraisal clause, not as a public adjuster or attorney. That means we focus on measurement, pricing and documentation, and we work toward an agreed figure with the insurer’s appraiser or an umpire’s decision.</p>'
             '<p>Before you invoke appraisal, our <a href="/claim-tools/appraisal-worth-it-calculator/">appraisal worth-it calculator</a> can help you estimate whether the gap justifies the cost.</p>'),
        ],
        "faqs": [
            ("Are Fort Lauderdale roofs held to a higher standard than the rest of Florida?",
             "Broward is part of the High-Velocity Hurricane Zone, so roofing and openings generally must meet stricter requirements than much of the state. That can raise repair costs, and how those costs are covered depends on your policy."),
            ("Can appraisal resolve my condo association’s claim?",
             "It can resolve disputes over the amount of a covered loss on the master policy. Questions about which policy covers a component, or whether an exclusion applies, are coverage issues outside appraisal."),
            ("Was the April 2023 flood covered by homeowners insurance?",
             "That depends on how water entered and what policies you carry. Rising surface water is usually a flood policy matter. Talk to your agent or an attorney about coverage; we can help once the dispute is about value."),
        ],
        "nearby": ["miami-fl", "west-palm-beach-fl", "naples-fl"],
    },
    # -------------------------------------------------------- WEST PALM BEACH
    {
        "slug": "west-palm-beach-fl",
        "city": "West Palm Beach",
        "county": "Palm Beach County",
        "region": "South Florida",
        "lat": "26.7153",
        "lng": "-80.0534",
        "title": "West Palm Beach Insurance Appraiser | Claim Appraisal",
        "description": "Independent claim appraisal for West Palm Beach and Palm Beach County homes, estates, condos and businesses with underpaid hurricane, roof or water claims.",
        "h1": "Insurance Appraiser in West Palm Beach, FL",
        "kicker": "Palm Beach County appraisal",
        "lead": "Palm Beach County’s property ranges from historic bungalows and island estates to coastal condos and western suburban subdivisions. We help West Palm Beach owners value covered losses accurately and use appraisal when the insurer’s offer doesn’t add up.",
        "neighborhoods": ["Northwood", "El Cid", "Flamingo Park", "Palm Beach", "Palm Beach Gardens", "Jupiter", "Wellington", "Delray Beach"],
        "storms": [
            (1928, "Okeechobee Hurricane", "The 1928 hurricane made landfall near Palm Beach and devastated the coast before its catastrophic flooding around Lake Okeechobee."),
            (2004, "Hurricane Frances", "Frances made landfall near Stuart and its slow crawl brought prolonged wind and rain damage to northern Palm Beach County."),
            (2004, "Hurricane Jeanne", "Jeanne struck almost the same stretch of coast three weeks later, adding new roof and interior damage to homes still awaiting repair."),
            (2005, "Hurricane Wilma", "Wilma crossed from the Gulf and caused widespread roof, window and tree damage across Palm Beach County."),
        ],
        "claim_issues": [
            "High-value homes with custom finishes and materials",
            "Clay and concrete tile roof matching",
            "Coastal condo wind-driven rain intrusion",
            "Contents and fine-furnishing valuation",
            "Commercial and mixed-use building claims",
        ],
        "sections": [
            ("High-value property, higher stakes",
             '<p>Palm Beach and the waterfront stretches of West Palm Beach, Jupiter and Manalapan include some of the most valuable homes in the country. Custom millwork, imported stone, specialty roofing and high-end systems mean a modest-sounding loss can carry a large repair cost, and insurers sometimes price these homes using standard-grade line items. The difference between “like kind and quality” and “close enough” can be substantial.</p><p>Historic West Palm Beach neighborhoods such as Flamingo Park, Grandview Heights and Old Northwood add another layer. Many of their 1920s homes have wood windows, plaster, cypress trim and original floors, and repairs may need to respect local historic preservation review. Those requirements can lengthen timelines and narrow material choices, and we factor them into a realistic scope.</p>'
             '<p>Our <a href="/appraisal-services/homeowners-claim-appraisal/">homeowners claim appraisal</a> work documents finish levels, sources for matching materials and the specialty trades the repair actually requires.</p>'),
            ("Tile roofs and the matching problem",
             '<p>Barrel and flat concrete and clay tile are common across Palm Beach County, from historic Northwood and El Cid homes to newer communities in Wellington and Palm Beach Gardens. When a storm breaks a section of tile, finding an exact match for an older or discontinued profile is often difficult, and a patchwork repair can leave a roof that doesn’t look or perform like the original. How your policy treats matching is a coverage question, but the cost of the realistic options is a valuation question appraisal can address.</p>'
             '<p>See <a href="/appraisal-services/roof-claim-appraisal/">roof claim appraisal</a> for how we evaluate tile damage, underlayment and replacement scope.</p>'),
            ("From the coast to the western communities",
             '<p>Palm Beach County is not all oceanfront. Western communities such as Wellington, Royal Palm Beach and Loxahatchee have equestrian properties, larger lots and outbuildings, while the coastal cities from Boca Raton to Tequesta are dense with condominiums. Commercial property is concentrated downtown and along the I-95 corridor. Each brings its own claim patterns, and our <a href="/appraisal-services/commercial-claim-appraisal/">commercial claim appraisal</a> service covers offices, retail and mixed-use buildings.</p>'),
            ("Florida Insurance Appraiser in Palm Beach County",
             '<p>Florida Insurance Appraiser covers West Palm Beach and the entire county as part of our statewide practice. We are independent appraisers retained to value the loss, not public adjusters or attorneys, and appraisal does not decide whether a loss is covered. When the appraisal clause is invoked, we inspect, estimate and work the numbers with the carrier’s appraiser, with an umpire resolving anything we cannot agree on.</p>'
             '<p>Contents can be a large part of a high-value claim; our <a href="/claim-tools/contents-inventory-builder/">contents inventory builder</a> helps you organize items before the appraisal begins.</p>'),
        ],
        "faqs": [
            ("Is appraisal appropriate for a high-value Palm Beach home?",
             "It can be, especially where the dispute centers on finish quality, materials or specialty labor. The larger and more detailed the loss, the more thorough documentation matters."),
            ("Can appraisal include contents and personal property?",
             "Often yes, if the policy’s appraisal clause applies to the contents claim and the dispute is about value. A detailed inventory with photos and receipts makes that much easier."),
            ("Do you work with condo associations in Palm Beach County?",
             "Yes. We work with associations and unit owners on master policy and HO-6 disputes over the amount of loss."),
        ],
        "nearby": ["fort-lauderdale-fl", "miami-fl", "orlando-fl"],
    },
]

_PART_B = [
    # ------------------------------------------------------------- FORT MYERS
    {
        "slug": "fort-myers-fl",
        "city": "Fort Myers",
        "county": "Lee County",
        "region": "Southwest Florida",
        "lat": "26.6406",
        "lng": "-81.8723",
        "title": "Fort Myers Insurance Appraiser | Claim Appraisal",
        "description": "Independent insurance appraisal for Fort Myers, Cape Coral and Lee County property claims, including wind vs. surge disputes, roofs, water and rebuild costs.",
        "h1": "Insurance Appraiser in Fort Myers, FL",
        "kicker": "Lee County claim appraisal",
        "lead": "Few places in Florida have been tested by storms like Lee County. If your Fort Myers or Cape Coral claim was accepted but the insurer’s number won’t cover the repair, appraisal may give you a path to a fair amount of loss.",
        "neighborhoods": ["Downtown Fort Myers", "McGregor Boulevard corridor", "Cape Coral", "Fort Myers Beach", "Sanibel", "Lehigh Acres", "Estero", "North Fort Myers"],
        "storms": [
            (2004, "Hurricane Charley", "Charley came ashore at Cayo Costa and Punta Gorda just north of Lee County, damaging Captiva, Pine Island and northern Lee communities."),
            (2017, "Hurricane Irma", "Irma made its Florida mainland landfall at Marco Island and brought widespread wind and tree damage to Lee County."),
            (2022, "Hurricane Ian", "Ian made landfall near Cayo Costa as a strong Category 4, and its storm surge devastated Fort Myers Beach, Sanibel, Pine Island and riverfront Fort Myers."),
        ],
        "claim_issues": [
            "Wind vs. storm surge allocation after Ian",
            "Cape Coral canal-front block homes",
            "Rebuild costs vs. repair estimates on heavily damaged homes",
            "Roofs damaged by wind then exposed to months of rain",
            "Supplemental damage found during repairs",
        ],
        "sections": [
            ("After Ian: the wind-versus-water question",
             '<p>Hurricane Ian changed the claim landscape in Southwest Florida. On Fort Myers Beach, Sanibel, Pine Island, Matlacha and along the Caloosahatchee, many homes were hit by both extreme wind and storm surge. Homeowners policies generally cover wind and exclude flood, while flood policies, often through the NFIP, cover surge with their own limits. The result is a long list of claims where the insurer attributes most of the damage to water and the owner believes wind did much of it first.</p>'
             '<p>Deciding cause is often a coverage matter outside appraisal, and courts and policies differ on how far appraisers may go. But once the scope is defined, the cost of wind-damaged roofs, windows, soffits and interiors still has to be measured accurately. Our <a href="/appraisal-services/hurricane-claim-appraisal/">hurricane claim appraisal</a> work is built around documenting those layers.</p>'),
            ("Cape Coral and the canal-front block home",
             '<p>Cape Coral was built out over decades as a grid of canals lined with single-story concrete block homes, many with tile or shingle roofs, pool cages and docks. Ian’s wind tore pool enclosures and roofs across the city, and water got into homes through damaged openings. Many of these houses are similar in layout, which can tempt insurers toward template estimates that miss what is actually in a particular home.</p>'
             '<p>We inspect each property on its own terms. The <a href="/claim-tools/roof-measurement-calculator/">roof measurement calculator</a> can help you check whether your carrier’s roof area is in the right range before we even arrive.</p>'),
            ("Repair, rebuild and the 50 percent conversation",
             '<p>In flood zones, local floodplain rules generally require a heavily damaged structure to be brought into compliance, often by elevating it, when repair costs reach a set share of the building’s value. That “substantial damage” determination is made by the local building official, not by an appraiser, and it can change what a realistic repair looks like. We take any such determination into account when building a scope, and we price what a contractor would actually need to do.</p>'
             '<p>Lee County’s post-Ian construction market also pushed labor and material costs well above normal, which is one reason older estimates often fall short. Our <a href="/appraisal-services/xactimate-estimate-review/">Xactimate estimate review</a> compares a carrier’s pricing line by line against current conditions.</p>'),
            ("How Florida Insurance Appraiser works in Lee County",
             '<p>Florida Insurance Appraiser serves Fort Myers, Cape Coral, the islands and the rest of Lee County as part of our statewide practice. We are appraisers, not public adjusters or attorneys: our work is to value covered damage and defend that valuation in the appraisal process, with an umpire resolving any items the two appraisers cannot settle. Florida deadlines for reporting and reopening claims have tightened in recent years, so check yours promptly.</p>'),
        ],
        "faqs": [
            ("Can appraisal decide how much of my Ian loss was wind vs. surge?",
             "Practice varies, and many causation questions are treated as coverage issues outside appraisal. Appraisal reliably sets the cost of the damage once the covered scope is identified. If causation is the main fight, consider talking to an attorney."),
            ("Is it too late to use appraisal on an older Lee County claim?",
             "Possibly not, but Florida law and your policy set deadlines for supplemental and reopened claims. Check your policy, and use our claim deadline calculator as a general guide, then confirm with an attorney if you are close."),
            ("Do you work on Sanibel, Captiva and Fort Myers Beach?",
             "Yes. We serve the barrier islands and all of Lee County, including Bonita Springs, Estero and Lehigh Acres."),
        ],
        "nearby": ["naples-fl", "sarasota-fl", "tampa-fl"],
    },
    # ------------------------------------------------------------------ NAPLES
    {
        "slug": "naples-fl",
        "city": "Naples",
        "county": "Collier County",
        "region": "Southwest Florida",
        "lat": "26.1420",
        "lng": "-81.7948",
        "title": "Naples Insurance Appraiser | Property Claim Appraisal",
        "description": "Independent insurance appraiser for Naples, Marco Island and Collier County homes, condos and HOAs with disputed hurricane, surge, roof and water claims.",
        "h1": "Insurance Appraiser in Naples, FL",
        "kicker": "Collier County appraisal",
        "lead": "Naples and Collier County mix luxury Gulf-front homes, gated golf communities and a large number of condominium associations, and all of them have been tested by recent hurricanes. We help owners and associations resolve disputes over the cost of covered damage through appraisal.",
        "neighborhoods": ["Old Naples", "Port Royal", "Park Shore", "Pelican Bay", "Vanderbilt Beach", "Golden Gate", "Marco Island", "Naples Park"],
        "storms": [
            (1960, "Hurricane Donna", "Donna’s surge swept through Naples and remains a historical benchmark for flooding in the city."),
            (2005, "Hurricane Wilma", "Wilma made landfall at Cape Romano just south of Marco Island and caused widespread roof and tree damage across Collier County."),
            (2017, "Hurricane Irma", "Irma made landfall at Marco Island, bringing strong winds, roof damage and surge to coastal Collier County."),
            (2022, "Hurricane Ian", "Although Ian’s eye came ashore farther north, its surge flooded Old Naples, Vanderbilt Beach and parts of Naples Park to record levels."),
        ],
        "claim_issues": [
            "HOA and gated-community master policy disputes",
            "Gulf-front surge vs. wind damage",
            "High-end interior finishes and matching",
            "Tile and metal roof replacement scope",
            "Seasonal-resident losses discovered late",
        ],
        "sections": [
            ("A community of associations",
             '<p>A large share of Collier County homeowners live in a condominium or homeowners association, from Gulf-front towers on Park Shore and Pelican Bay to golf communities east of US-41. That means many claims involve a master policy covering roofs, exterior walls and common elements, plus individual policies for unit interiors. When a hurricane damages an entire community, the association’s claim can be large and complex, and boards are often asked to make decisions under time pressure.</p>'
             '<p>Our <a href="/appraisal-services/condo-hoa-claim-appraisal/">condo and HOA claim appraisal</a> work helps boards document building-by-building damage and present a defensible amount of loss, while unit owners can retain us separately for interior claims.</p>'),
            ("Surge, wind and the Gulf-front home",
             '<p>Ian’s surge reached deep into Old Naples, Aqualane Shores and Vanderbilt Beach, flooding homes that had never taken water before. Many of those properties also had wind damage to roofs, windows and lanais. As elsewhere in Southwest Florida, flood losses usually fall under a separate flood policy and wind losses under the homeowners policy, so the allocation can drive the outcome. Appraisal values the damage; which policy pays for it is a coverage determination.</p>'
             '<p>See our <a href="/appraisal-services/hurricane-claim-appraisal/">hurricane claim appraisal</a> page for how we document mixed-cause losses.</p>'),
            ("Pricing the finishes Naples homes actually have",
             '<p>Custom cabinetry, natural stone, impact-rated window systems, metal and tile roofs, and outdoor living spaces are standard in much of Naples. An estimate that uses builder-grade line items can understate a loss significantly. We document finish levels during the inspection and price repairs with materials of like kind and quality, sourcing specialty items where needed.</p><p>Lanais, screen enclosures, outdoor kitchens, docks and boat lifts are also part of many Naples claims. Some of these items have their own sublimits or exclusions under the policy, which is a coverage matter, but where they are covered, their repair cost deserves the same careful measurement as the house itself.</p>'
             '<p>Seasonal residents also face a timing problem: damage may go unnoticed until an owner returns months later. Florida claim notice deadlines have become stricter, so it is worth checking the <a href="/claim-tools/claim-deadline-calculator/">claim deadline calculator</a> and your policy as soon as you learn of damage.</p>'),
            ("Florida Insurance Appraiser in Collier County",
             '<p>Florida Insurance Appraiser serves Naples, Marco Island, Golden Gate, Immokalee and the rest of Collier County as part of our statewide coverage. We are independent appraisers, not public adjusters or attorneys, and we don’t argue coverage. Once appraisal is invoked under your policy, we inspect, build an itemized estimate, and work toward an agreed figure with the insurer’s appraiser, with an umpire deciding any unresolved items.</p>'),
        ],
        "faqs": [
            ("Can an HOA board invoke appraisal on a master policy claim?",
             "If the master policy contains an appraisal clause, the association, as the insured, can generally invoke it. Boards should follow their governing documents and may want counsel involved for large claims."),
            ("I live in Naples seasonally. What if I found damage months after the storm?",
             "Report it right away. Florida law and many policies set notice deadlines, and late notice can complicate a claim. Once the claim is open and the dispute is about value, appraisal may still be available."),
            ("Do you serve Marco Island?",
             "Yes. We cover Marco Island, Isles of Capri, Everglades City and all of Collier County."),
        ],
        "nearby": ["fort-myers-fl", "miami-fl", "sarasota-fl"],
    },
    # --------------------------------------------------------------- SARASOTA
    {
        "slug": "sarasota-fl",
        "city": "Sarasota",
        "county": "Sarasota County",
        "region": "Southwest Florida",
        "lat": "27.3364",
        "lng": "-82.5307",
        "title": "Sarasota Insurance Appraiser | Claim Appraisal Help",
        "description": "Independent property claim appraisal for Sarasota, the barrier keys, Venice and North Port. Settle underpaid hurricane, roof, surge and water claims fairly.",
        "h1": "Insurance Appraiser in Sarasota, FL",
        "kicker": "Sarasota County appraisal",
        "lead": "Sarasota went years without a direct hit, then took Ian’s damage in the south county in 2022 and Helene and Milton within two weeks in 2024. We help Sarasota-area owners resolve disputes over what covered damage really costs to repair.",
        "neighborhoods": ["Downtown Sarasota", "Siesta Key", "Lido Key", "Longboat Key", "Lakewood Ranch", "Osprey", "Venice", "North Port"],
        "storms": [
            (2004, "Hurricane Charley", "Charley’s landfall at Punta Gorda brought damaging winds into southern Sarasota County and North Port."),
            (2022, "Hurricane Ian", "Ian’s eyewall winds hit Venice and North Port hard, and the Myakka River flooded neighborhoods for days afterward."),
            (2024, "Hurricane Helene", "Helene passed well offshore but pushed storm surge over Siesta Key, Lido Key and Longboat Key."),
            (2024, "Hurricane Milton", "Milton made landfall near Siesta Key two weeks later, bringing hurricane-force wind across the county."),
        ],
        "claim_issues": [
            "Back-to-back Helene and Milton losses",
            "Barrier-island surge vs. wind disputes",
            "Mid-century modern homes with unusual construction",
            "Manufactured and older homes in Venice and North Port",
            "Inland river flooding after Ian",
        ],
        "sections": [
            ("A county with very different claim zones",
             '<p>Sarasota County stretches from the high-rise and estate properties on Longboat, Lido and Siesta keys to the older neighborhoods around downtown, the planned communities of Lakewood Ranch and Palmer Ranch, and the fast-growing grid of North Port. The same storm can produce entirely different losses in each: surge on the keys, roof and window damage downtown, and freshwater flooding along the Myakka River inland.</p>'
             '<p>That variety is why we start every engagement with a full on-site inspection rather than relying on the carrier’s photos.</p><p>We also look at what was already repaired. After back-to-back storms, many owners hired emergency contractors for tarping, water extraction and demolition before an adjuster ever arrived. Those invoices, along with dated photos and moisture logs, are part of the loss and belong in the valuation. Keeping them organized makes the appraisal faster and more persuasive.</p>'),
            ("Helene, then Milton",
             '<p>In late September 2024, Helene’s surge pushed water into homes and businesses on the barrier islands. Before many owners had even finished mucking out, Milton came ashore near Siesta Key with strong winds. For many properties, that means two dates of loss, possibly two deductibles, and a mix of flood and wind damage. Sorting out which policy and which event apply is a coverage exercise, but each piece still has to be valued correctly.</p>'
             '<p>Our <a href="/appraisal-services/hurricane-claim-appraisal/">hurricane claim appraisal</a> page covers how we handle multi-event losses, and the <a href="/claim-tools/hurricane-deductible-calculator/">hurricane deductible calculator</a> shows how percentage deductibles can change what you actually receive.</p>'),
            ("Mid-century modern and older homes",
             '<p>Sarasota is known for its mid-century modern architecture, with flat or low-slope roofs, large expanses of glass and unconventional framing. Venice and parts of North Port also have older block homes and manufactured housing. These buildings can be tricky to estimate: low-slope roofing systems, custom glazing and non-standard materials don’t fit neatly into default pricing. Our <a href="/appraisal-services/roof-claim-appraisal/">roof claim appraisal</a> service works through those systems item by item.</p>'),
            ("Florida Insurance Appraiser in Sarasota County",
             '<p>Florida Insurance Appraiser serves Sarasota, Venice, North Port, Englewood and the keys as part of our statewide practice. If your policy has an appraisal clause and you choose to use it, we serve as your appraiser: we inspect, document, estimate and negotiate the amount of loss with the insurer’s appraiser, and present the disputed items to an umpire if needed. We are not public adjusters or attorneys and appraisal does not resolve coverage disputes.</p>'
             '<p>Read the <a href="/appraisal-process/">appraisal process</a> page for a step-by-step overview.</p>'),
        ],
        "faqs": [
            ("Do I have two claims if Helene and Milton both damaged my Sarasota home?",
             "Often the insurer treats them as separate events with separate dates of loss, which can affect deductibles and documentation. Your policy and adjuster determine how they are handled; appraisal can value each once that is settled."),
            ("Can appraisal help with my North Port home damaged by Ian?",
             "Yes, if the claim was accepted and the dispute is over the cost of repairs. River flooding is usually a flood policy matter, while wind damage typically falls under homeowners coverage."),
            ("Do you cover Manatee County and Lakewood Ranch too?",
             "Yes. We serve Sarasota and Manatee counties, including Lakewood Ranch, Bradenton and Anna Maria Island."),
        ],
        "nearby": ["st-petersburg-fl", "tampa-fl", "fort-myers-fl"],
    },
    # --------------------------------------------------------- ST. PETERSBURG
    {
        "slug": "st-petersburg-fl",
        "city": "St. Petersburg",
        "county": "Pinellas County",
        "region": "Tampa Bay",
        "lat": "27.7676",
        "lng": "-82.6403",
        "title": "St. Petersburg Insurance Appraiser | Claim Appraisal",
        "description": "Independent insurance appraisal for St. Petersburg and Pinellas County homes, condos and businesses facing disputed surge, wind, roof and water damage claims.",
        "h1": "Insurance Appraiser in St. Petersburg, FL",
        "kicker": "Pinellas County appraisal",
        "lead": "Pinellas is a densely built peninsula surrounded by water, with much of its housing dating from before modern building codes. After the 2024 storms, many St. Petersburg owners are disputing what their insurer paid, and we help them settle the amount through appraisal.",
        "neighborhoods": ["Old Northeast", "Snell Isle", "Shore Acres", "Kenwood", "Gulfport", "St. Pete Beach", "Treasure Island", "Clearwater"],
        "storms": [
            (1921, "Tampa Bay Hurricane", "The 1921 hurricane, the last major hurricane to make landfall in the Tampa Bay area for a century, flooded much of the Pinellas shoreline."),
            (2023, "Hurricane Idalia", "Idalia passed offshore but its surge flooded low-lying streets and homes in Shore Acres and along the Pinellas beaches."),
            (2024, "Hurricane Helene", "Helene’s record surge flooded thousands of homes in Shore Acres, Snell Isle, Gulfport and the barrier-island beach towns."),
            (2024, "Hurricane Milton", "Milton tore much of the fabric roof off Tropicana Field, dropped extreme rainfall on the city and caused widespread wind damage."),
        ],
        "claim_issues": [
            "Surge-flooded slab homes vs. wind damage",
            "Pre-1970s homes and code-upgrade costs",
            "Beach-town condos and motels",
            "Roofs damaged by Milton after Helene flooding",
            "Substantial-damage rules in flood zones",
        ],
        "sections": [
            ("Older homes in low places",
             '<p>Much of St. Petersburg was built out between the 1920s and the 1960s, long before today’s Florida Building Code. Neighborhoods like Shore Acres, Venetian Isles and parts of Gulfport sit only a few feet above sea level, with slab-on-grade ranch homes that were never designed for the water Helene brought in 2024. Historic neighborhoods such as the Old Northeast and Kenwood have bungalows and revival-style homes with materials that are difficult to match.</p>'
             '<p>Those conditions mean repair estimates often have to account for older wiring and plumbing exposed during demolition, code upgrades and specialty materials. Whether code-upgrade costs are payable depends on your ordinance-or-law coverage.</p><p>Pinellas is also Florida’s most densely populated county, so lots are small and access is tight. Staging, debris removal and permit-related delays can all add cost that a desk estimate overlooks. We price those practical realities alongside the materials themselves.</p>'),
            ("Helene’s water, Milton’s wind",
             '<p>Many Pinellas owners experienced Helene and Milton as one long disaster, but insurers generally treat them as separate events. Helene’s surge typically falls under flood coverage, while Milton’s wind and wind-driven rain damage typically falls under homeowners coverage, each with its own deductible and documentation. When a roof damaged by Milton sits over a house already gutted by Helene, sorting out scope gets complicated.</p>'
             '<p>Our <a href="/appraisal-services/hurricane-claim-appraisal/">hurricane claim appraisal</a> work documents each event’s damage as clearly as the evidence allows, so the amount of loss for each covered part can be fixed.</p>'),
            ("Substantial damage and rebuilding in flood zones",
             '<p>In flood zones, when repairs reach a set share of a structure’s value, local floodplain rules generally require bringing the building into compliance, which may mean elevation or even demolition. St. Petersburg and the beach communities handled a large number of those reviews after 2024. Those determinations come from local officials, not appraisers, but they shape what a realistic repair scope and price look like.</p>'
             '<p>Before invoking appraisal, our <a href="/claim-tools/appraisal-worth-it-calculator/">appraisal worth-it calculator</a> can help you gauge whether the dispute is large enough to justify the process.</p>'),
            ("Florida Insurance Appraiser in Pinellas County",
             '<p>Florida Insurance Appraiser serves St. Petersburg, Clearwater, Largo, Dunedin and the beach towns from Tierra Verde to Clearwater Beach as part of our statewide service. We work as your appraiser under the policy’s appraisal clause, not as a public adjuster or attorney, so coverage and legal questions stay with you and your counsel. Our focus is a documented, defensible amount of loss, agreed with the insurer’s appraiser or decided by an umpire.</p>'
             '<p>Commercial owners, including motel, retail and small office properties, can learn more on our <a href="/appraisal-services/commercial-claim-appraisal/">commercial claim appraisal</a> page.</p>'),
        ],
        "faqs": [
            ("Does appraisal apply to my flood policy as well as homeowners?",
             "Some flood policies, including the NFIP standard policy, contain their own appraisal provision limited to the amount of loss. The terms differ from homeowners policies, so review the specific policy."),
            ("My St. Pete home is older. Will code upgrades be included?",
             "Only if your policy provides ordinance-or-law coverage and the upgrades are required for the repair. We price the work as it must be done; the policy decides what is payable."),
            ("Do you serve the Pinellas beach towns?",
             "Yes, including St. Pete Beach, Treasure Island, Madeira Beach, Indian Rocks Beach and Clearwater Beach."),
        ],
        "nearby": ["tampa-fl", "sarasota-fl", "orlando-fl"],
    },
    # ------------------------------------------------------------ TALLAHASSEE
    {
        "slug": "tallahassee-fl",
        "city": "Tallahassee",
        "county": "Leon County",
        "region": "Big Bend",
        "lat": "30.4383",
        "lng": "-84.2807",
        "title": "Tallahassee Insurance Appraiser | Claim Appraisal",
        "description": "Independent claim appraisal for Tallahassee, Leon County and the Big Bend: tree-fall, wind, roof and water damage disputes on homes and commercial property.",
        "h1": "Insurance Appraiser in Tallahassee, FL",
        "kicker": "Big Bend claim appraisal",
        "lead": "Tallahassee’s tree canopy is one of the city’s great assets and one of its biggest claim risks. When a storm brings oaks and pines down on homes across Leon County and the Big Bend, we help owners settle disputed repair costs through appraisal.",
        "neighborhoods": ["Midtown", "Betton Hills", "Killearn", "Southwood", "Indianhead Acres", "Frenchtown", "Crawfordville", "Quincy"],
        "storms": [
            (2016, "Hurricane Hermine", "Hermine made landfall near St. Marks and brought down thousands of trees in Tallahassee, leaving much of the city without power."),
            (2018, "Hurricane Michael", "Michael’s eastern side brought damaging winds, tree falls and outages to Leon and surrounding counties."),
            (2023, "Hurricane Idalia", "Idalia struck the Big Bend coast near Keaton Beach, damaging homes in Taylor County and bringing tree damage to eastern Leon County."),
            (2024, "Hurricane Helene", "Helene came ashore near Perry as a major hurricane, with destructive winds across the Big Bend and tree damage in Tallahassee."),
        ],
        "claim_issues": [
            "Tree-fall roof and structural damage",
            "Framing and truss repairs after impact",
            "Rural Big Bend homes and outbuildings",
            "Tornado and severe thunderstorm wind damage",
            "State and university-area rental property claims",
        ],
        "sections": [
            ("When the canopy comes down",
             '<p>Tallahassee’s live oaks, laurel oaks and tall pines shade nearly every neighborhood, from Betton Hills and Los Robles to Killearn and the newer streets of Southwood. In a hurricane, a tornado or even a strong summer thunderstorm, those trees can come down on roofs, porches, carports and vehicles. Tree-fall losses are deceptive: the visible damage is a crushed section of roof, but the impact can crack trusses and rafters, shift walls, break ceiling joists and open the house to rain for days.</p>'
             '<p>Initial estimates sometimes price a roof patch and a ceiling repair when the framing needs real structural work. Our <a href="/appraisal-services/roof-claim-appraisal/">roof claim appraisal</a> inspection looks beneath the surface at framing, sheathing and load paths.</p>'),
            ("The Big Bend storm track",
             '<p>The Big Bend coast, from Apalachee Bay to Cedar Key, has seen repeated landfalls in recent years. Hermine in 2016, Idalia in 2023 and Helene in 2024 all came ashore along that stretch, and Michael in 2018 brought damaging wind east from its Panhandle landfall, and in May 2024 a series of tornadoes tore through parts of the city. Coastal communities like St. Marks, Steinhatchee and Keaton Beach took surge, while Tallahassee itself dealt mostly with wind and falling trees.</p><p>Inland North Florida homes are also exposed to strong thunderstorms, straight-line winds and occasional hail outside of hurricane season. Those events are typically subject to your standard all-other-perils deductible rather than a hurricane deductible, which can make a meaningful difference in what you receive. Policies vary, so check the declarations page.</p>'
             '<p>Our <a href="/appraisal-services/hurricane-claim-appraisal/">hurricane claim appraisal</a> service covers coastal and inland properties across the Big Bend.</p>'),
            ("Homes, rentals and rural property",
             '<p>Leon County’s housing includes older brick ranch homes near the universities, larger homes on wooded lots in the northeast, student rentals and small apartment buildings, and farmhouses, barns and outbuildings in Gadsden, Jefferson and Wakulla counties. Rental and small commercial owners may also have loss-of-rents or business income questions, which depend on policy terms. Our <a href="/appraisal-services/commercial-claim-appraisal/">commercial claim appraisal</a> page explains how we approach income-producing property.</p>'),
            ("Florida Insurance Appraiser in North Florida",
             '<p>Florida Insurance Appraiser serves Tallahassee, Leon County and the surrounding Big Bend counties as part of our statewide practice. As your appraiser, we inspect the damage, prepare an itemized estimate and work with the insurer’s appraiser toward an agreed amount; if needed, an umpire decides what we cannot agree on. We are not public adjusters or attorneys, and appraisal sets the amount of loss rather than deciding coverage.</p>'
             '<p>Not sure you are ready? Try the <a href="/claim-tools/appraisal-readiness-quiz/">appraisal readiness quiz</a>.</p>'),
        ],
        "faqs": [
            ("Is tree removal included in my Tallahassee claim?",
             "Many policies provide some coverage for removing a tree that strikes a covered structure, often with a dollar limit. The policy controls; appraisal can address the cost if there is a dispute over the amount."),
            ("My insurer paid for a roof patch but I think the framing is damaged. Can appraisal help?",
             "Yes, if the claim is accepted and the dispute is about the scope and cost of repair. A thorough inspection of trusses, rafters and sheathing is the starting point."),
            ("Do you cover the coastal Big Bend counties?",
             "Yes. We serve Wakulla, Jefferson, Taylor, Dixie and nearby counties, including St. Marks, Steinhatchee and Perry."),
        ],
        "nearby": ["pensacola-fl", "jacksonville-fl", "orlando-fl"],
    },
    # -------------------------------------------------------------- PENSACOLA
    {
        "slug": "pensacola-fl",
        "city": "Pensacola",
        "county": "Escambia County",
        "region": "Panhandle",
        "lat": "30.4213",
        "lng": "-87.2169",
        "title": "Pensacola Insurance Appraiser | Claim Appraisal Help",
        "description": "Independent insurance appraisal for Pensacola, Escambia and Santa Rosa counties: hurricane wind, roof and water damage claims on homes and businesses.",
        "h1": "Insurance Appraiser in Pensacola, FL",
        "kicker": "Western Panhandle appraisal",
        "lead": "Pensacola and the western Panhandle have taken direct hits from several major hurricanes in the last two decades. If your Escambia or Santa Rosa County claim was underpaid, we can provide an independent valuation and represent your side in appraisal.",
        "neighborhoods": ["East Hill", "North Hill", "Downtown Pensacola", "Pensacola Beach", "Gulf Breeze", "Perdido Key", "Navarre", "Milton"],
        "storms": [
            (2004, "Hurricane Ivan", "Ivan made landfall just west of the Florida-Alabama line, devastating Pensacola Beach, Perdido Key and much of Escambia County and damaging the I-10 bridge over Escambia Bay."),
            (2005, "Hurricane Dennis", "Dennis came ashore on Santa Rosa Island less than a year later, adding new damage before many Ivan repairs were complete."),
            (2020, "Hurricane Sally", "Sally crawled ashore near Gulf Shores and dropped extreme rain on Pensacola, flooding downtown and damaging the Pensacola Bay Bridge."),
        ],
        "claim_issues": [
            "Slow-moving storm rainfall and water intrusion",
            "Historic homes in North Hill and East Hill",
            "Barrier-island condos on Pensacola Beach and Perdido Key",
            "Shingle and metal roof wind damage",
            "Wind vs. flood allocation on bayfront property",
        ],
        "sections": [
            ("A Panhandle storm history",
             '<p>Pensacola sits near where many Gulf hurricanes come ashore. Ivan in 2004 brought catastrophic surge and wind, Dennis followed in 2005, and Sally in 2020 showed how much damage a slow-moving storm can do through rainfall alone. Each storm left a different pattern: surge-driven destruction on the barrier islands, roof and wind damage across the city, and widespread interior water damage from torrential rain.</p>'
             '<p>Because a single property can show all three, documenting the damage carefully from the start makes a real difference in any later dispute.</p><p>Homes that survived Ivan and Dennis were often repaired quickly and sometimes imperfectly, during a period of material shortages and heavy contractor demand. When a newer storm damages those properties, insurers may point to prior damage or earlier repairs. Records of past work, permits and inspections can help separate old conditions from new damage, and we review whatever history is available.</p>'),
            ("Sally and the water that came through the roof",
             '<p>Sally stalled offshore and dropped extraordinary rainfall on Escambia and Santa Rosa counties. Many homes that lost only a few shingles still ended up with soaked ceilings, insulation, drywall and flooring as water poured through damaged roofs and openings. These claims often turn on scope: whether wet materials can be dried or must be replaced, and whether mold remediation is needed. Florida policies often cap mold coverage, so check your limits.</p>'
             '<p>Our <a href="/appraisal-services/water-damage-claim-appraisal/">water damage claim appraisal</a> service documents moisture readings and materials so drying-versus-replacement decisions are grounded in evidence.</p>'),
            ("Historic districts and coastal condos",
             '<p>Pensacola’s historic neighborhoods, including North Hill, East Hill and the Seville district, have Victorian and early twentieth-century homes with wood siding, heart-pine floors and detailed trim that standard pricing doesn’t capture. On Pensacola Beach and Perdido Key, condominiums and townhomes face salt exposure and wind-driven rain. Gulf Breeze, Navarre and Milton add newer subdivisions with shingle and metal roofs.</p>'
             '<p>Our <a href="/appraisal-services/condo-hoa-claim-appraisal/">condo and HOA claim appraisal</a> work serves coastal associations and unit owners alike.</p>'),
            ("Florida Insurance Appraiser in the Panhandle",
             '<p>Florida Insurance Appraiser serves Pensacola and the western Panhandle as part of our statewide practice, from Perdido Key east to Navarre and inland to Cantonment and Milton. We act as your appraiser when appraisal is invoked under your policy, not as a public adjuster or attorney. Our role is to inspect, estimate and work toward an agreed amount of loss with the insurer’s appraiser, with an umpire resolving anything we cannot agree on.</p>'
             '<p>Read the <a href="/appraisal-process/">appraisal process</a> page to see how a typical appraisal unfolds.</p>'),
        ],
        "faqs": [
            ("Was Sally rain damage covered under homeowners insurance?",
             "Rain that entered through storm-damaged roofs or openings is often treated differently from rising floodwater, which usually requires a flood policy. Your policy language controls how a specific loss is handled."),
            ("Do you work on Pensacola Beach and Perdido Key?",
             "Yes. We serve the barrier islands as well as Gulf Breeze, Navarre and the rest of Escambia and Santa Rosa counties."),
            ("Can appraisal help with an older home in North Hill?",
             "Yes, if your claim is accepted and the dispute is about cost. Appraisal is often useful when an estimate does not reflect the materials and labor a historic home requires."),
        ],
        "nearby": ["tallahassee-fl", "jacksonville-fl", "tampa-fl"],
    },
]

LOCATIONS = _PART_A + _PART_B
