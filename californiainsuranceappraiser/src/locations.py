"""Location pages. URL: /city-coverage/<slug>-insurance-appraiser/. Main keyword: 'insurance appraiser <City>'."""

LOCATIONS = [
    {
        "slug": "los-angeles", "city": "Los Angeles", "county": "Los Angeles County", "region": "Southern California",
        "perils": ["Wildfire & smoke", "Santa Ana winds", "Earthquake & fire following", "Storm leaks", "Water losses"],
        "hoods": "Pacific Palisades, Silver Lake, Highland Park, Encino, Westchester, Eagle Rock",
        "lede": "From Palisades hillside homes to Valley ranch houses and Westside condos, Los Angeles claims span every kind of loss California produces.",
        "body": """
<h2>Los Angeles claims after January 2025</h2>
<p>The Palisades and Eaton fires of January 2025 destroyed thousands of structures in Pacific Palisades, parts of Malibu and Altadena, pushed by an extreme Santa Ana wind event. Beyond the burn areas, homes across the basin dealt with smoke and ash infiltration and wind damage to roofs, fences and trees. Many of those claims are still being scoped, rebuilt or disputed, and an insurance appraiser in Los Angeles sees every stage of them.</p>
<h2>Neighborhoods and housing</h2>
<p>Los Angeles housing ranges from 1920s Spanish revival and Craftsman homes in Highland Park and Eagle Rock, to mid-century hillside homes in Silver Lake and the Hollywood Hills, to post-war ranch houses in Encino and Westchester. Apartment buildings, including the city’s many 1950s and 1960s “dingbat” buildings, make up a large share of the housing stock. Hillside lots raise rebuild costs through access limits, retaining walls and stepped foundations, and those costs are often under-estimated.</p>
<h2>Earthquakes and fire following</h2>
<p>The 1994 Northridge earthquake caused widespread damage across the San Fernando Valley. Earthquake damage is excluded from standard homeowner policies and covered only by separate earthquake insurance, such as a California Earthquake Authority policy. Fire following an earthquake, however, is generally covered under the standard fire policy, a distinction that matters in a city on several active faults.</p>
<h2>Water and storm losses</h2>
<p>February 2024’s record rainfall caused roof leaks and hillside mudslides across the city. Aging supply lines and slab leaks are a constant source of claims in older homes and apartment buildings, and leaks between units are among the most common condo disputes we see.</p>
""",
        "faqs": [
            ("Do you work on Palisades and Eaton fire claims?", "Yes. We value total-loss rebuilds, smoke and ash claims, and contents for homes affected by both fires, as appraiser or through estimate review."),
            ("Does my Los Angeles homeowner policy cover earthquake damage?", "Usually not. Earthquake damage requires separate coverage, such as a California Earthquake Authority policy. Fire following an earthquake is generally covered."),
            ("Are hillside rebuild costs included in standard estimates?", "Often not fully. Access, retaining walls and foundations can add substantially to costs, and we price them separately."),
        ],
        "near": ["irvine", "ventura", "riverside"],
    },
    {
        "slug": "san-diego", "city": "San Diego", "county": "San Diego County", "region": "Southern California",
        "perils": ["Wildfire", "Santa Ana winds", "Flash flooding", "Water leaks", "Tile roofs"],
        "hoods": "Scripps Ranch, Rancho Bernardo, Clairemont, North Park, La Jolla, Southcrest",
        "lede": "San Diego’s mild weather hides real risk: wind-driven wildfires in the canyons and sudden flooding in older neighborhoods.",
        "body": """
<h2>A history of canyon fires</h2>
<p>The 2003 Cedar Fire destroyed more than two thousand homes across San Diego County, including hundreds in Scripps Ranch. Four years later, the 2007 Witch Creek Fire burned into Rancho Bernardo and other communities during a Santa Ana wind event. Those fires shaped local building codes, defensible-space rules and the way insurers price canyon-rim homes. An insurance appraiser in San Diego needs to understand both the rebuild standards and the market for fire-resistant construction.</p>
<h2>January 2024 flooding</h2>
<p>In January 2024, an intense storm dropped record rain on San Diego and flooded homes in Southcrest, Shelltown, Encanto and other southeastern neighborhoods. Many homeowners learned that flood damage from rising water isn’t covered without separate flood insurance, while roof leaks and some other water damage may be. Separating those losses is often the heart of the dispute.</p>
<h2>Housing and roofs</h2>
<p>Stucco homes with concrete or clay tile roofs are typical of Clairemont, Mira Mesa and the northern suburbs, while North Park and University Heights have Craftsman bungalows and Spanish revival homes. La Jolla and the coastal neighborhoods add high-value custom homes and condos exposed to salt air. Tile roofs dominate, and broken tile, failed underlayment and discontinued profiles are frequent sources of disagreement.</p>
<h2>Condos and water</h2>
<p>San Diego has a large stock of condominiums and townhomes, where supply-line and water heater leaks often affect several units. We read the HOA’s CC&amp;Rs and master policy alongside the owner’s unit policy to identify who should pay for what.</p>
""",
        "faqs": [
            ("Was my January 2024 flood damage covered?", "Damage from rising surface water generally isn’t covered without flood insurance. Roof leaks and other non-flood water damage may be. We can help separate them."),
            ("Do you handle tile roof disputes in San Diego?", "Yes. Tile roof scope, underlayment and matching are among the most common issues we see in the county."),
            ("Can you inspect in North County?", "Yes. We inspect throughout San Diego County, from Oceanside and Escondido to Chula Vista and the backcountry."),
        ],
        "near": ["irvine", "riverside", "los-angeles"],
    },
    {
        "slug": "san-jose", "city": "San Jose", "county": "Santa Clara County", "region": "Bay Area",
        "perils": ["Creek flooding", "Earthquake & fire following", "Water leaks", "Low-slope roofs", "Wind"],
        "hoods": "Willow Glen, Rose Garden, Almaden Valley, Evergreen, Rock Springs, Cambrian",
        "lede": "San Jose’s Eichlers, ranch homes and high-rise condos come with their own claim patterns, from low-slope roof leaks to creek flooding.",
        "body": """
<h2>The 2017 Coyote Creek flood</h2>
<p>In February 2017, Coyote Creek overtopped its banks and flooded the Rock Springs neighborhood and surrounding areas, forcing thousands of evacuations. Flood damage from the creek generally required flood insurance, but many homes also had roof leaks and wind damage from the same storms. An insurance appraiser in San Jose needs to separate those losses carefully.</p>
<h2>Eichlers and low-slope roofs</h2>
<p>San Jose has thousands of mid-century Eichler homes, particularly in Willow Glen and Cambrian. Their low-slope roofs, radiant floor heating and post-and-beam construction make repairs specialized. A roof leak can damage tongue-and-groove ceilings that are hard to match, and radiant heat lines under slab floors complicate water claims. Estimates written for a typical tract home often miss these costs.</p>
<h2>Earthquakes</h2>
<p>The 1989 Loma Prieta earthquake caused significant damage across Santa Clara County. Earthquake damage requires separate coverage, but fire following an earthquake is generally covered under the standard fire policy. Owners of older homes should check whether foundation bolting or cripple wall retrofits have been completed, since those affect both risk and earthquake premiums.</p>
<h2>Housing and water losses</h2>
<p>Willow Glen and the Rose Garden have older homes from the 1920s through 1940s; Almaden Valley and Evergreen have larger homes from the 1970s through 1990s; and downtown has a growing number of high-rise condos. Water damage from failed supply lines and water heaters is the most common claim we see across all of them.</p>
""",
        "faqs": [
            ("Do you understand Eichler construction?", "Yes. We price low-slope roofing, tongue-and-groove ceilings and radiant floor systems specifically rather than using generic tract-home figures."),
            ("Is creek flooding covered?", "Generally only with flood insurance. Other storm damage, such as roof leaks, may be covered under a homeowner policy."),
            ("Do you serve the rest of Santa Clara County?", "Yes, including Sunnyvale, Santa Clara, Cupertino, Campbell, Los Gatos, Morgan Hill and Gilroy."),
        ],
        "near": ["san-francisco", "oakland", "santa-rosa"],
    },
    {
        "slug": "san-francisco", "city": "San Francisco", "county": "City and County of San Francisco", "region": "Bay Area",
        "perils": ["Water between units", "Earthquake & fire following", "Wind-driven rain", "Fire in older buildings", "Soft-story buildings"],
        "hoods": "Sunset, Richmond, Marina, Noe Valley, Bernal Heights, Mission",
        "lede": "Victorians, Edwardians, attached Sunset homes and condo towers: San Francisco claims are shaped by shared walls, steep lots and old buildings.",
        "body": """
<h2>Old buildings, shared walls</h2>
<p>Much of San Francisco was built in the decades after 1906, and many Victorian and Edwardian buildings remain. Row houses in the Sunset and Richmond share walls, and many buildings have been converted to condominiums or tenancies-in-common. A fire or water loss in one unit regularly affects neighbors, and determining which policy pays for which damage is half the work of an insurance appraiser in San Francisco.</p>
<h2>Earthquake history and retrofits</h2>
<p>The 1989 Loma Prieta earthquake caused severe damage in the Marina District, where buildings on fill suffered liquefaction and fires broke out. The city later adopted a mandatory soft-story retrofit program for many older wood-frame buildings with ground-floor garages. Earthquake damage requires separate coverage, but fire following an earthquake is generally covered under standard policies.</p>
<h2>Wind-driven rain and water losses</h2>
<p>Atmospheric rivers, like the series that hit in winter 2022–23, push rain into older buildings through windows, parapets and siding. Water damage between units, from bathrooms, kitchens and failed supply lines, is the most common claim type in the city’s multi-unit buildings.</p>
<h2>Repair costs</h2>
<p>San Francisco has some of the highest construction costs in the country. Parking restrictions, permit timelines, historic preservation requirements and the need to match ornate millwork and plaster all add to repair costs. Estimates priced for suburban work often miss these factors, which is one of the most common reasons we find a significant gap.</p>
<h3>Condos and TICs</h3>
<p>For condos, we review the HOA master policy and CC&amp;Rs alongside the owner’s unit policy. For tenancies-in-common, we look at the building policy and the TIC agreement to see who is responsible for what.</p>
""",
        "faqs": [
            ("Who pays when water from my upstairs neighbor damages my unit?", "Often the upstairs owner’s policy or the HOA master policy, depending on the source and the governing documents. Your own policy may also respond."),
            ("Are San Francisco repair costs reflected in standard estimates?", "Not always. Access, permits, historic finishes and local labor rates often need to be priced specifically."),
            ("Does my policy cover earthquake damage?", "Usually not without separate earthquake coverage. Fire following an earthquake is generally covered."),
        ],
        "near": ["oakland", "san-jose", "santa-rosa"],
    },
    {
        "slug": "sacramento", "city": "Sacramento", "county": "Sacramento County", "region": "Central Valley",
        "perils": ["Falling trees", "Atmospheric rivers", "Roof leaks", "Heat-aged roofs", "Water losses"],
        "hoods": "Land Park, East Sacramento, Midtown, Natomas, Arden-Arcade, Curtis Park",
        "lede": "The City of Trees has a lot of trees to lose. Winter storms in Sacramento bring falling oaks and elms along with rain that tests every roof.",
        "body": """
<h2>Trees and winter storms</h2>
<p>Sacramento’s urban forest is one of its signatures, and also one of its biggest sources of claims. When atmospheric rivers saturated soils in January 2023, wind toppled large trees across Land Park, East Sacramento and Arden-Arcade, crushing roofs, cars and fences, and leaving tens of thousands without power. An insurance appraiser in Sacramento spends much of the winter on tree-impact claims.</p>
<h2>What tree claims involve</h2>
<ul>
<li>Removing the tree from the structure, often with a crane.</li>
<li>Structural repair to framing, roof decking and ceilings.</li>
<li>Interior water damage from rain entering through the opening.</li>
<li>Fences, other structures and landscaping, usually under separate limits.</li>
</ul>
<p>Policies often limit coverage for removing a tree that fell without hitting anything, but when it strikes a covered structure, removal is typically part of the loss.</p>
<h2>Neighborhoods and housing</h2>
<p>Land Park, Curtis Park and East Sacramento have 1920s through 1940s homes with plaster walls, hardwood floors and detailed trim that are costly to match. Midtown has Victorians and converted apartments. Natomas and the northern suburbs have newer tract homes, many built behind levees. Matching original finishes in older homes is a frequent source of disagreement.</p>
<h2>Flooding</h2>
<p>Sacramento sits at the confluence of the Sacramento and American rivers and has a long history of flood risk, including major floods in 1986 and 1997. Flood damage requires separate flood insurance, but storm damage like roof leaks and fallen trees is generally covered.</p>
""",
        "faqs": [
            ("Is tree removal covered after a storm?", "Usually, when the tree hits a covered structure. Limits often apply, and removal of trees that didn’t hit anything may not be covered."),
            ("Can you match plaster and trim in older Sacramento homes?", "We price matching work specifically, including plaster repair and custom millwork, rather than substituting drywall and stock trim."),
            ("Do you serve the suburbs?", "Yes, including Elk Grove, Folsom, Roseville, Rancho Cordova, Citrus Heights and Davis."),
        ],
        "near": ["fresno", "chico", "oakland"],
    },
    {
        "slug": "fresno", "city": "Fresno", "county": "Fresno County", "region": "Central Valley",
        "perils": ["Extreme heat", "Wind", "Wildfire smoke", "Water leaks", "Agricultural buildings"],
        "hoods": "Tower District, Fig Garden, Woodward Park, Sunnyside, Old Fig, Bullard",
        "lede": "Fresno’s heat ages roofs and HVAC systems fast, and the foothills to the east bring wildfire and smoke to the edge of the valley.",
        "body": """
<h2>Heat, wind and roofs</h2>
<p>Summer temperatures in Fresno regularly exceed 100°F, which accelerates shingle aging, dries out seals and stresses HVAC equipment. When a storm or wind event damages a roof, carriers sometimes attribute the damage to age. An insurance appraiser in Fresno has to document storm damage carefully enough to separate it from wear.</p>
<h2>Wildfire and smoke from the Sierra</h2>
<p>The 2020 Creek Fire burned across the Sierra in Fresno and Madera counties, destroying hundreds of structures in mountain communities and blanketing the valley in smoke for weeks. Foothill and mountain homes face direct fire risk, while valley homes can have smoke infiltration claims during major fire seasons.</p>
<h2>Neighborhoods and housing</h2>
<p>The Tower District has 1920s and 1930s homes with stucco and Spanish details. Fig Garden and Old Fig have larger homes on big lots under mature trees. Woodward Park and the northeast have newer subdivisions with tile roofs. Clovis, next door, adds a large stock of newer homes. Many properties also include pools, outbuildings and solar systems that need separate attention in a claim.</p>
<h2>Agricultural and commercial property</h2>
<p>Fresno County is one of the most productive farming counties in the country. Packing sheds, barns, cold storage and equipment buildings are often insured on farm or commercial policies with different valuation terms. We value these structures with attention to their specialized systems.</p>
<h3>Water losses</h3>
<p>Slab leaks and failed supply lines are common across Fresno’s housing stock, and evaporative coolers and HVAC condensate lines add their own leak risks.</p>
""",
        "faqs": [
            ("The carrier says my roof damage is just age. What can I do?", "Document fresh damage with dated photos and a professional inspection. If coverage is accepted for part of the damage, appraisal can resolve the amount."),
            ("Do you handle farm buildings?", "Yes. We value barns, packing sheds and other agricultural structures, often insured under farm or commercial policies."),
            ("Do you serve Clovis and Madera?", "Yes, along with Visalia, Hanford, Madera and the foothill communities."),
        ],
        "near": ["sacramento", "riverside", "san-jose"],
    },
    {
        "slug": "santa-rosa", "city": "Santa Rosa", "county": "Sonoma County", "region": "North Bay",
        "perils": ["Wildfire", "Smoke & ash", "Russian River flooding", "Falling trees", "Earthquake"],
        "hoods": "Fountaingrove, Coffey Park, Rincon Valley, Bennett Valley, Montecito Heights, Skyhawk",
        "lede": "Santa Rosa has rebuilt after two major fires in four years. Its owners know more about wildfire claims than almost anyone.",
        "body": """
<h2>Tubbs and Glass</h2>
<p>In October 2017, the Tubbs Fire swept from Calistoga into Santa Rosa overnight, destroying more than five thousand structures, including much of Coffey Park and Fountaingrove. Three years later, the 2020 Glass Fire burned homes in Skyhawk, Rincon Valley and the hills to the east. Thousands of Sonoma County families have now worked through total-loss claims, underinsurance and long rebuilds, and an insurance appraiser in Santa Rosa has to be fluent in all of it.</p>
<h2>Lessons from the rebuild</h2>
<ul>
<li>Many owners discovered their dwelling limits were well below actual rebuild costs, even with extended replacement cost.</li>
<li>Post-fire demand pushed construction costs up sharply, so estimates priced before the surge were too low.</li>
<li>Code changes required fire-resistant construction and sometimes fire sprinklers, which building code upgrade coverage may or may not fully cover.</li>
</ul>
<h2>Neighborhoods and housing</h2>
<p>Fountaingrove has hillside homes with views and challenging foundations. Coffey Park, largely rebuilt, now has newer homes built to current codes. Rincon Valley and Bennett Valley have a mix of ranch homes and newer subdivisions. Montecito Heights has older homes on hillside lots. Each area has different access, foundation and cost considerations.</p>
<h2>Flooding and storms</h2>
<p>The Russian River flooded Guerneville and other west county communities in February 2019, and Santa Rosa Creek and Laguna de Santa Rosa can overflow in heavy storms. Flood damage requires flood insurance, while wind and tree damage are generally covered.</p>
""",
        "faqs": [
            ("Can you help with a claim from the 2017 or 2020 fires?", "It depends on where the claim stands and the policy’s deadlines. Contact us and we’ll review what’s still open."),
            ("Do you value rebuilds in Fountaingrove?", "Yes. We price hillside rebuilds, including foundations, access and current fire-safe construction standards."),
            ("Do you serve the rest of Sonoma County?", "Yes, including Petaluma, Rohnert Park, Windsor, Healdsburg, Sebastopol and Sonoma."),
        ],
        "near": ["oakland", "san-francisco", "chico"],
    },
    {
        "slug": "oakland", "city": "Oakland", "county": "Alameda County", "region": "Bay Area",
        "perils": ["Hillside wildfire", "Earthquake & fire following", "Storm leaks", "Falling trees", "Water losses"],
        "hoods": "Rockridge, Montclair, Temescal, Grand Lake, Oakland Hills, Fruitvale",
        "lede": "Oakland’s hills, Craftsman bungalows and older apartment buildings carry real fire, earthquake and storm risk.",
        "body": """
<h2>The 1991 Oakland Hills fire</h2>
<p>In October 1991, the Oakland Hills fire, also called the Tunnel Fire, destroyed thousands of homes in the hills above Rockridge and Montclair in a single day, driven by hot, dry Diablo winds. It remains one of the costliest urban wildfires in California history and still shapes building standards and insurance in the hills. An insurance appraiser in Oakland has to understand both hillside rebuild costs and how fire-resistant construction requirements affect them.</p>
<h2>Earthquakes</h2>
<p>The Hayward Fault runs through Oakland and is considered one of the most hazardous faults in the country. The 1989 Loma Prieta earthquake caused the collapse of the Cypress Street Viaduct in West Oakland. Earthquake damage requires separate coverage, but fire following an earthquake is generally covered under standard homeowner policies.</p>
<h2>Neighborhoods and housing</h2>
<p>Rockridge, Temescal and Grand Lake have Craftsman bungalows and brown-shingle homes from the early 1900s, with old-growth redwood trim and plaster walls. The hills have mid-century and newer custom homes on steep lots. Fruitvale and the flatlands have Victorians and older apartment buildings. Matching original materials and accounting for hillside access are common sources of disagreement.</p>
<h2>Storms and trees</h2>
<p>The winter of 2022–23 brought down large trees across the Oakland Hills, damaging homes and blocking roads. Tree impacts, roof leaks and wind-driven rain are among the most common storm claims in the city.</p>
""",
        "faqs": [
            ("Are hillside rebuild costs higher in Oakland?", "Usually. Steep lots, retaining walls and limited access add cost, and we price them specifically."),
            ("Do you serve Berkeley and the East Bay?", "Yes, including Berkeley, Alameda, San Leandro, Hayward, Piedmont and Walnut Creek."),
            ("Is earthquake damage covered?", "Only with separate earthquake coverage. Fire following an earthquake is generally covered under a standard policy."),
        ],
        "near": ["san-francisco", "san-jose", "santa-rosa"],
    },
    {
        "slug": "riverside", "city": "Riverside", "county": "Riverside County", "region": "Inland Empire",
        "perils": ["Santa Ana winds", "Wildfire", "Extreme heat", "Tile roofs", "Water leaks"],
        "hoods": "Wood Streets, Canyon Crest, La Sierra, Mission Grove, Orangecrest, Arlington",
        "lede": "Riverside sits in the path of the Santa Ana winds as they leave the passes, and the Inland Empire’s heat and fire seasons test every roof.",
        "body": """
<h2>Wind and fire in the Inland Empire</h2>
<p>Santa Ana winds accelerate through the Cajon Pass and San Gorgonio Pass into the Inland Empire, bringing gusts that break tile, topple palms and drive fires. The 2018 Holy Fire burned in the Santa Ana Mountains on the Riverside–Orange county line, and the 2022 Fairview Fire destroyed homes near Hemet. An insurance appraiser in Riverside regularly sees wind, fire and smoke damage from the same events.</p>
<h2>Neighborhoods and housing</h2>
<p>The Wood Streets have Craftsman and Spanish revival homes from the early 1900s. Canyon Crest and Mission Grove have homes from the 1970s through 1990s. Orangecrest has newer subdivisions with HOAs. La Sierra and Arlington mix older ranch homes with newer development. Concrete and clay tile roofs dominate, and many homes have pools, block walls and solar systems that all need attention in a claim.</p>
<h2>Heat and roofs</h2>
<p>Inland temperatures regularly exceed 100°F, which ages underlayment beneath tile roofs. When wind breaks tiles, the question becomes whether spot repairs will work with aged underlayment or whether a larger replacement is needed. We inspect and document both the tile and the underlayment so the panel has what it needs.</p>
<h2>Block walls and other structures</h2>
<p>Block walls and wrought-iron fences are common property boundaries in the Inland Empire. Wind and fallen trees damage them regularly, and they are typically covered under the other structures limit. Estimates for block walls often understate footings, rebar and matching cap blocks.</p>
""",
        "faqs": [
            ("Is wind damage to tile roofs common in Riverside?", "Yes. Santa Ana winds frequently break and lift tile, and underlayment condition determines whether spot repair is adequate."),
            ("Are block walls covered?", "Usually under the other structures coverage, which has its own limit. We price footings, reinforcement and matching materials."),
            ("Do you serve San Bernardino County?", "Yes, including San Bernardino, Ontario, Rancho Cucamonga, Fontana and Redlands, as well as all of Riverside County."),
        ],
        "near": ["irvine", "los-angeles", "san-diego"],
    },
    {
        "slug": "irvine", "city": "Irvine", "county": "Orange County", "region": "Southern California",
        "perils": ["Wildfire & smoke", "Santa Ana winds", "HOA master-policy gaps", "Water leaks", "Tile roofs"],
        "hoods": "Woodbridge, Northwood, Turtle Rock, Quail Hill, Portola Springs, University Park",
        "lede": "Irvine’s master-planned villages mean HOAs, shared walls and tile roofs, and its canyon edges bring wind-driven fire close.",
        "body": """
<h2>Fires on the canyon edges</h2>
<p>In October 2020, the Silverado Fire forced the evacuation of tens of thousands of Irvine residents as Santa Ana winds pushed flames toward Portola Springs and Orchard Hills. The Bond Fire followed weeks later in the nearby foothills, and the 2024 Airport Fire burned in the Santa Ana Mountains. Even without structure losses in the city, smoke and ash infiltration claims followed. An insurance appraiser in Irvine sees those claims alongside the water and roof losses typical of newer communities.</p>
<h2>Villages and HOAs</h2>
<p>Irvine is organized into villages, each with its own homeowner associations. Woodbridge and University Park date from the 1970s and 1980s, Northwood and Turtle Rock add homes from the 1980s and 1990s, and Quail Hill and Portola Springs are newer. Most homes are governed by an HOA with its own master policy, and condos and townhomes are common. Claims routinely involve the boundary between the association’s policy and the owner’s.</p>
<h3>How we approach HOA claims</h3>
<ul>
<li>Review the CC&amp;Rs to identify which components the association must insure.</li>
<li>Compare the master policy and the owner’s HO-6 or HO-3 policy.</li>
<li>Value each portion of the damage under the right policy.</li>
</ul>
<h2>Water and roofs</h2>
<p>Supply-line leaks, water heater failures and fire sprinkler discharges are the most common claims in Irvine’s condos and townhomes, often affecting several units. Concrete tile roofs dominate, and wind events regularly break and lift tile.</p>
""",
        "faqs": [
            ("My HOA says the damage is my responsibility. Is that right?", "It depends on the CC&Rs and the master policy. We review both to identify which policy should cover each component."),
            ("Do you serve the rest of Orange County?", "Yes, including Newport Beach, Costa Mesa, Lake Forest, Mission Viejo, Anaheim and Huntington Beach."),
            ("Did the Silverado Fire cause smoke claims in Irvine?", "Some homes near the canyon edges had smoke and ash damage. Coverage depends on the policy and documentation of physical damage."),
        ],
        "near": ["riverside", "los-angeles", "san-diego"],
    },
    {
        "slug": "ventura", "city": "Ventura", "county": "Ventura County", "region": "Central Coast",
        "perils": ["Wildfire", "Santa Ana winds", "Debris flows", "Storm leaks", "Coastal exposure"],
        "hoods": "Ventura Avenue, Midtown, Pierpont, Montalvo, Hillcrest, Downtown",
        "lede": "Ventura’s hills burned in the Thomas Fire, its coast takes winter storms head on, and its older neighborhoods need careful matching.",
        "body": """
<h2>The Thomas Fire</h2>
<p>In December 2017, the Thomas Fire started near Santa Paula and swept into the hillside neighborhoods of Ventura, destroying hundreds of homes before burning into Santa Barbara County. The following January, heavy rain on the burn scar triggered the deadly Montecito debris flows. The Woolsey Fire in November 2018 burned parts of eastern Ventura County as well. An insurance appraiser in Ventura has to understand total-loss rebuilds, smoke claims and the coverage questions that follow debris flows.</p>
<h2>Neighborhoods and housing</h2>
<p>Midtown and Downtown have older homes and bungalows from the early and mid-1900s. Hillcrest and the hillside areas above the city have homes with views and steep lots, many rebuilt after 2017. Pierpont, near the beach, has a mix of older cottages and newer homes exposed to salt air and wind. Ventura Avenue has older homes and small apartment buildings. Each area has different construction and access issues.</p>
<h2>Storms and coastal exposure</h2>
<p>The winter of 2022–23 brought flooding to parts of Ventura County, and January 2023 storms damaged homes and infrastructure along the coast. Beach-adjacent homes take wind-driven rain and salt corrosion that shorten the life of roofing, windows and fasteners, which carriers may cite as wear. Documenting fresh storm damage is essential.</p>
<h2>Debris flows and coverage</h2>
<p>Debris flows and mudslides after fires are typically excluded under flood or earth movement provisions in many homeowner policies, though related damage may be covered. These claims often need an attorney’s view on coverage before appraisal can address the amount.</p>
""",
        "faqs": [
            ("Do you handle Thomas or Woolsey fire claims?", "It depends on where the claim stands and the deadlines. We review open claims and supplemental disputes."),
            ("Is mudslide damage covered?", "Often not under standard homeowner policies, but some related damage may be. Coverage questions may require an attorney."),
            ("Do you serve Oxnard and Camarillo?", "Yes, along with Thousand Oaks, Simi Valley, Ojai, Santa Paula and the rest of Ventura County."),
        ],
        "near": ["los-angeles", "irvine", "san-diego"],
    },
    {
        "slug": "chico", "city": "Chico", "county": "Butte County", "region": "Northern California",
        "perils": ["Wildfire", "Smoke & ash", "Falling trees", "Storm leaks", "FAIR Plan policies"],
        "hoods": "Chapmantown, the Avenues, Barber, California Park, Canyon Oaks, Doe Mill",
        "lede": "Chico took in thousands of Camp Fire survivors from Paradise. It knows wildfire claims, underinsurance and FAIR Plan policies firsthand.",
        "body": """
<h2>The Camp Fire</h2>
<p>On November 8, 2018, the Camp Fire destroyed most of Paradise and much of Concow and Magalia, killing 85 people and destroying roughly 18,000 structures. It remains the deadliest and most destructive wildfire in California history. Chico, just down the hill, absorbed thousands of displaced residents. Many families spent years working through total-loss claims, contents inventories and rebuild decisions, and an insurance appraiser in Chico has to know that process in depth.</p>
<h2>FAIR Plan and underinsurance</h2>
<p>As private insurers have pulled back from fire-prone areas, many Butte County homes are now insured through the California FAIR Plan, often with a separate difference-in-conditions policy covering other perils. FAIR Plan dwelling policies are commonly written on an actual cash value basis unless replacement cost was purchased, and limits may be lower than rebuild costs. Understanding exactly what each policy covers is essential before any appraisal.</p>
<h2>Neighborhoods and housing</h2>
<p>The Avenues and Chapmantown have older homes from the early and mid-1900s near Bidwell Park and downtown. Barber and California Park include ranch homes and newer subdivisions. Canyon Oaks sits in the foothills with larger homes and greater fire exposure. Doe Mill and newer developments on the southeast side have recent construction. Mature trees across town mean tree impacts are common in winter storms.</p>
<h2>Oroville and storms</h2>
<p>In February 2017, damage to the Oroville Dam spillway forced the evacuation of nearly 190,000 people downstream. Winter storms regularly bring down trees and cause roof leaks across Butte County.</p>
""",
        "faqs": [
            ("Can appraisal be used with a FAIR Plan policy?", "FAIR Plan policies generally include an appraisal provision. Valuation terms such as actual cash value versus replacement cost matter a great deal."),
            ("Do you serve Paradise and Oroville?", "Yes, along with Magalia, Durham, Gridley and the rest of Butte County."),
            ("What if my dwelling limit won’t cover the rebuild?", "Appraisal can’t raise limits, but it can confirm the full cost so you can access extended replacement cost and code upgrade coverage where available."),
        ],
        "near": ["sacramento", "santa-rosa", "fresno"],
    },
]

# Hand-written meta descriptions (110-143 characters), one per location page.
LOC_DESC = {
    "los-angeles": "Insurance appraiser in Los Angeles for wildfire rebuilds, smoke and ash, Santa Ana wind and water claims the carrier valued too low.",
    "san-diego": "Insurance appraiser in San Diego for canyon wildfire, tile roof, storm and condo water claims across the city and San Diego County.",
    "san-jose": "Insurance appraiser in San Jose for Eichler roof leaks, water losses, storm damage and fire claims throughout Santa Clara County.",
    "san-francisco": "Insurance appraiser in San Francisco for water between units, fire, storm and condo claims where city repair costs run high.",
    "sacramento": "Insurance appraiser in Sacramento for fallen-tree, atmospheric river, roof leak and water claims in older and newer homes alike.",
    "fresno": "Insurance appraiser in Fresno for wind and roof claims, wildfire smoke, water losses and farm buildings across Fresno County.",
    "santa-rosa": "Insurance appraiser in Santa Rosa for wildfire total losses, smoke and ash, storm and flood-adjacent claims in Sonoma County.",
    "oakland": "Insurance appraiser in Oakland for hillside fire, storm, falling tree and water claims in Craftsman homes and apartment buildings.",
    "riverside": "Insurance appraiser in Riverside for Santa Ana wind, tile roof, wildfire smoke and block wall claims across the Inland Empire.",
    "irvine": "Insurance appraiser in Irvine for HOA master-policy gaps, condo water leaks, tile roofs and wildfire smoke in Orange County.",
    "ventura": "Insurance appraiser in Ventura for wildfire rebuilds, smoke, coastal storm and roof claims throughout Ventura County.",
    "chico": "Insurance appraiser in Chico for wildfire total losses, FAIR Plan claims, smoke and storm damage across Butte County.",
}
