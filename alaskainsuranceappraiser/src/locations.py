"""Alaska community pages. Each entry carries local detail: borough, neighborhoods, housing and storm history."""

LOCATIONS = [
    {
        "slug": "anchorage", "city": "Anchorage", "county": "Municipality of Anchorage", "region": "Southcentral",
        "perils": ["Earthquake (with endorsement)", "Downslope windstorms", "Snow load & ice dams", "Frozen pipes", "Water losses"],
        "hoods": ["Downtown", "South Addition", "Midtown", "Spenard", "Turnagain", "Sand Lake", "Hillside", "Muldoon", "Mountain View", "Government Hill", "Huffman", "Rabbit Creek"],
        "housing": "1960s–80s ranch and split-level homes, condos and townhomes, fourplexes and larger Hillside homes on view lots",
        "events": ["1964 Great Alaska Earthquake", "November 30, 2018 magnitude 7.1 earthquake", "January 2025 windstorm"],
        "near": ["eagle-river", "wasilla", "palmer"],
        "lede": "Alaska's largest city sees almost every kind of property claim the state produces: earthquakes, Hillside windstorms, heavy-snow winters and the water losses that follow cold snaps.",
        "body": """
<h2>The Anchorage claim landscape</h2>
<p>About two of every five Alaskans live in the Municipality of Anchorage, a consolidated city and borough that stretches from Girdwood to Eklutna. That concentration means Anchorage produces more property claims than anywhere else in the state, and a wide range of them.</p>
<p>Earthquakes define Anchorage's history. The 1964 Great Alaska Earthquake, magnitude 9.2, triggered the Turnagain Heights landslide and destroyed blocks of downtown along Fourth Avenue. On November 30, 2018, a magnitude 7.1 quake centered just north of the city cracked foundations and drywall across the bowl, buckled roads and damaged thousands of homes. Owners who carried earthquake coverage then faced a new problem: high percentage deductibles and disagreements about which cracks the quake caused.</p>
<h2>Wind on the Hillside, snow everywhere</h2>
<p>Easterly downslope winds off the Chugach Mountains hit the Hillside, Huffman, Rabbit Creek and the east side hardest, lifting shingles, peeling metal roofing and dropping birch and spruce onto houses. The January 2025 windstorm brought gusts near 100 mph to parts of the area. Heavy-snow winters bring the other half of the Anchorage roof story: ice dams on older split-levels with poor attic ventilation, and collapsed carports, sheds and low-slope commercial roofs.</p>
<h2>Housing and common disputes</h2>
<p>Much of the city was built between the 1960s and 1980s. Split-levels and bi-levels in Sand Lake, Abbott Loop and Muldoon, condos and townhomes throughout Midtown, and fourplexes in Fairview and Mountain View all have their own claim patterns. We frequently see:</p>
<ul>
<li>Water losses where baseboard heat, insulation and subfloor were left out of the scope</li>
<li>Earthquake drywall claims paid room by room rather than for continuous wall and ceiling planes</li>
<li>Wind claims limited to individual shingles on roofs too brittle to spot-repair</li>
<li>Condo losses where the HOA master policy and HO-6 overlap</li>
</ul>
<h2>Where we work in Anchorage</h2>
<p>Downtown, South Addition, Government Hill, Midtown, Spenard, Turnagain, Sand Lake, Bayshore, the Hillside, Huffman, Rabbit Creek, Muldoon, Mountain View, Girdwood and everything between. Eagle River and Chugiak have their own page.</p>
""",
        "faqs": [
            ("Did my homeowner policy cover the 2018 earthquake?", "Only if you had earthquake coverage, which is usually added by endorsement or a separate policy. Without it, earthquake damage is typically excluded."),
            ("Is the Hillside windstorm risk reflected in my policy?", "Most Anchorage homeowner policies cover wind under the regular deductible, but some carry separate wind or percentage deductibles. Your declarations page will show it."),
        ],
    },
    {
        "slug": "eagle-river", "city": "Eagle River & Chugiak", "county": "Municipality of Anchorage", "region": "Southcentral",
        "perils": ["Earthquake (with endorsement)", "Downslope windstorms", "Snow load", "Frozen pipes & wells", "Wildfire risk"],
        "hoods": ["Downtown Eagle River", "Eagle River Valley", "South Fork", "Chugiak", "Peters Creek", "Birchwood", "Eklutna"],
        "housing": "1980s–2000s single-family homes, split-entries, homes on larger wooded lots with wells and septic in Chugiak and Peters Creek",
        "events": ["November 30, 2018 earthquake", "Chugach downslope wind events", "January 2025 windstorm"],
        "near": ["anchorage", "palmer", "wasilla"],
        "lede": "North of Anchorage along the Glenn Highway, Eagle River and Chugiak combine suburban subdivisions with wooded acreage, and both took some of the hardest shaking in the 2018 earthquake.",
        "body": """
<h2>Part of Anchorage, with its own character</h2>
<p>Eagle River, Chugiak, Peters Creek, Birchwood and Eklutna sit inside the Municipality of Anchorage but feel like a separate community. Homes climb the Eagle River Valley toward Chugach State Park, and many lots are wooded, sloped and on private wells and septic systems.</p>
<h2>Earthquake and wind history</h2>
<p>The November 2018 earthquake was felt strongly here, with widespread drywall, foundation and chimney damage and broken water lines. Owners with earthquake coverage often found the claims process slow and the estimates thin, especially for homes where the damage spread through multiple levels.</p>
<p>The same Chugach downslope winds that hit the Anchorage Hillside reach Eagle River and Chugiak, and the 2025 windstorm brought down trees and power lines across the area. Wooded lots mean tree-on-house claims are common, along with siding, roofing and fence damage.</p>
<h2>Housing and claim patterns</h2>
<ul>
<li>Split-entry and two-story homes from the 1980s through 2000s, many with finished lower levels</li>
<li>Larger custom homes in the Valley with complex rooflines and higher snow and wind exposure</li>
<li>Rural homes in Chugiak and Peters Creek with wells, pressure tanks and heat tape that can fail in cold snaps</li>
<li>Detached garages and shops with heavy snow-load exposure</li>
</ul>
<h2>What we see most</h2>
<p>Water losses from frozen supply lines and well systems, earthquake claims with incomplete drywall scopes, roof damage from wind and ice, and tree-strike claims with removal limits. We inspect throughout Eagle River, Chugiak, Peters Creek, Birchwood and Eklutna.</p>
""",
        "faqs": [
            ("Is a frozen well line covered?", "Damage from sudden freezing of plumbing is often covered, subject to conditions about maintaining heat. Repairs to the well itself may be treated differently. Read the policy."),
            ("Do trees that fall on my house count as wind damage?", "Usually the damage to the house is covered under the wind peril. Tree removal is often limited to a set amount."),
        ],
    },
    {
        "slug": "wasilla", "city": "Wasilla", "county": "Matanuska-Susitna Borough", "region": "Mat-Su Valley",
        "perils": ["Wildfire & smoke", "Windstorms", "Snow load", "Frozen pipes", "Earthquake (with endorsement)"],
        "hoods": ["Lake Lucille", "Knik-Fairview", "Meadow Lakes", "Cottonwood", "Settlers Bay", "Big Lake", "Houston"],
        "housing": "Newer stick-built homes, manufactured homes, large detached garages and shops on acreage",
        "events": ["1996 Miller's Reach Fire", "2018 earthquake (Vine Road collapse)", "January 2025 windstorm"],
        "near": ["palmer", "eagle-river", "anchorage"],
        "lede": "The Mat-Su is one of the fastest-growing parts of Alaska, and Wasilla is at its center. New subdivisions, manufactured homes and big shops all bring their own claim issues.",
        "body": """
<h2>Fast growth, newer homes</h2>
<p>Wasilla and the surrounding Matanuska-Susitna Borough have grown quickly for decades. Knik-Fairview, Meadow Lakes and the Parks Highway corridor are full of homes built since the 1990s, many by owners who have never filed a claim. Manufactured homes, modular homes and large detached garages and shops are common, often on acreage.</p>
<h2>Wildfire history</h2>
<p>The 1996 Miller's Reach Fire, which started near Big Lake and Houston, destroyed hundreds of structures and remains one of the most destructive fires in Alaska history. More recent fires near Willow, including the 2015 Sockeye Fire and the 2019 McKinley Fire, destroyed dozens of homes along the Parks Highway. Even when homes survive, smoke and ash claims can be significant.</p>
<h2>Earthquake and wind</h2>
<p>The November 2018 earthquake caused well-known damage in the Mat-Su, including the collapse of Vine Road near Wasilla, and many homes had foundation and drywall damage. The January 2025 windstorm brought down trees and damaged roofs across the borough, and the Mat-Su was among the areas covered by a state disaster declaration.</p>
<h2>Claim issues we see in Wasilla</h2>
<ul>
<li>Manufactured home claims where matching parts are no longer available</li>
<li>Shop and garage roof collapses under heavy snow</li>
<li>Smoke and ash cleaning versus replacement after nearby fires</li>
<li>Wind damage to metal roofs and siding on open lots</li>
<li>Frozen supply lines in crawlspaces and well houses</li>
</ul>
<p>We work throughout Wasilla, Knik-Fairview, Meadow Lakes, Big Lake, Houston, Willow and the Parks Highway corridor.</p>
""",
        "faqs": [
            ("Is smoke damage covered if the fire did not reach my home?", "Smoke damage is often covered under the fire peril, but the extent of the damage is frequently disputed. Document it early."),
            ("Is my shop covered under my homeowner policy?", "Detached structures are usually covered under Other Structures, often at a percentage of the dwelling limit. Large shops may need higher limits."),
        ],
    },
    {
        "slug": "palmer", "city": "Palmer", "county": "Matanuska-Susitna Borough", "region": "Mat-Su Valley",
        "perils": ["Matanuska & Knik winds", "Snow load", "Frozen pipes", "Wildfire", "Earthquake (with endorsement)"],
        "hoods": ["Downtown Palmer", "Butte", "Lazy Mountain", "Fishhook", "Gateway", "Sutton"],
        "housing": "Historic Colony-era farmhouses, rural acreage homes, barns, greenhouses and outbuildings",
        "events": ["Matanuska wind events", "2018 earthquake", "January 2025 windstorm"],
        "near": ["wasilla", "eagle-river", "anchorage"],
        "lede": "The Mat-Su borough seat sits where the Matanuska and Knik valleys open up, and the winds that pour out of them are some of the strongest in Southcentral Alaska.",
        "body": """
<h2>A farming town with a windy reputation</h2>
<p>Palmer began as the 1935 Matanuska Colony, a New Deal resettlement project that brought farm families north. Some of the original Colony farmhouses and barns still stand, alongside newer homes on acreage around the Butte, Lazy Mountain and Fishhook.</p>
<h2>Matanuska and Knik winds</h2>
<p>When cold air drains out of the interior through the Matanuska and Knik valleys, Palmer and the Butte take the brunt of it. These winds can blow for days in fall and winter, peeling roofing, flattening greenhouses and fences, and driving snow into attics. The January 2025 windstorm caused widespread damage across the area.</p>
<h2>Housing and claim patterns</h2>
<ul>
<li>Historic farmhouses and barns that are expensive to repair in kind</li>
<li>Rural homes with outbuildings, greenhouses and equipment sheds</li>
<li>Metal roofs and siding exposed to repeated wind events</li>
<li>Homes on wells and septic with freeze exposure</li>
</ul>
<h2>Common disputes</h2>
<p>Wind claims where only individual panels or shingles are paid on roofs that need broader repair, outbuildings valued below the cost to rebuild, and repeated-event claims where the carrier argues prior damage. Earthquake claims from 2018 also continue to come up for owners who carried that coverage.</p>
<p>We inspect in Palmer, Butte, Lazy Mountain, Fishhook, Sutton and throughout the Valley.</p>
""",
        "faqs": [
            ("My roof was damaged in two wind events. How is that handled?", "Each event may be a separate claim with its own deductible. Separating the damage can be difficult, and good photos after each event help."),
            ("Are greenhouses covered?", "Often as other structures, sometimes with limits for certain types of construction. Check your policy."),
        ],
    },
    {
        "slug": "fairbanks", "city": "Fairbanks", "county": "Fairbanks North Star Borough", "region": "Interior",
        "perils": ["Extreme cold & freeze-ups", "Snow & ice load", "Wildfire smoke", "Chimney fires", "Summer hail"],
        "hoods": ["Downtown", "Hamilton Acres", "Aurora", "Lemeta", "South Van Horn", "Chena Ridge", "Goldstream Valley", "Farmers Loop", "College", "Two Rivers", "Ester"],
        "housing": "Log homes, 1970s pipeline-era frame homes, dry cabins, newer homes on the hills, and multifamily near downtown",
        "events": ["1967 Chena River flood", "December 2021 freezing rain and heavy snow", "Summer wildfire smoke seasons"],
        "near": ["anchorage", "wasilla", "palmer"],
        "lede": "Interior Alaska's largest city sees temperature swings of more than 120 degrees a year. Forty-below cold, freezing rain, heavy snow and summer wildfire smoke all produce claims here.",
        "body": """
<h2>Claims shaped by extreme cold</h2>
<p>Fairbanks winters regularly bring stretches of minus 30 and colder. When a boiler fails, the power goes out or a heat tape stops working, water lines freeze quickly. Freeze-up claims are among the most common in the Fairbanks North Star Borough, and they are often larger than they first appear because damage spreads through walls, crawlspaces and heating systems.</p>
<h2>Rain on snow, and the weight it brings</h2>
<p>In December 2021, freezing rain followed by heavy snow loaded roofs across the Interior with ice and dense snow, and many structures were damaged. Events like that show why snow load and ice claims are not just a coastal problem.</p>
<h2>Fire and smoke</h2>
<p>Wood stoves and oil furnaces carry the city through winter, and chimney fires are a recurring cause of loss. In summer, wildfires across the Interior can fill the Tanana Valley with smoke for weeks, leading to smoke and odor claims even when the fire is far away. Summer thunderstorms also bring occasional hail, one of the few places in Alaska where it is a real roofing concern.</p>
<h2>Housing and common disputes</h2>
<ul>
<li>Log homes and cabins where specialized labor is scarce and costly</li>
<li>1970s homes from the pipeline construction era with older systems</li>
<li>Glycol heating systems and boilers that need repair after a freeze</li>
<li>Foundation movement claims, where frost heave and permafrost thaw are usually excluded but sudden water damage may be covered</li>
</ul>
<p>We work across Fairbanks, North Pole, College, Ester, Goldstream Valley, Chena Ridge, Farmers Loop, Two Rivers and the surrounding borough.</p>
""",
        "faqs": [
            ("Is foundation damage from permafrost covered?", "Settlement, frost heave and permafrost thaw are usually excluded as earth movement. Sudden water damage that results from a broken line may still be covered."),
            ("Are chimney fires covered?", "Fire damage is a core covered peril. Disputes often arise over smoke cleaning and whether the chimney itself needs replacement."),
        ],
    },
    {
        "slug": "juneau", "city": "Juneau", "county": "City and Borough of Juneau", "region": "Southeast",
        "perils": ["Heavy rain & water intrusion", "Taku winds", "Glacial outburst flooding", "Landslides", "Snow load"],
        "hoods": ["Downtown", "Starr Hill", "Casey-Shattuck", "Mendenhall Valley", "Lemon Creek", "Douglas", "West Juneau", "Auke Bay", "Thane"],
        "housing": "Older wood-frame homes on steep downtown lots, 1970s–80s split-levels in the Valley, condos and townhomes",
        "events": ["Suicide Basin glacial outburst floods (2023, 2024)", "Taku wind events", "Downtown landslides"],
        "near": ["sitka", "ketchikan", "anchorage"],
        "lede": "Alaska's capital is reachable only by air and water. Rain, Taku winds, landslides and the annual glacial outburst flood on the Mendenhall River all shape property claims here.",
        "body": """
<h2>A wet, steep, isolated city</h2>
<p>Juneau gets heavy rain most of the year, and much of the downtown area is built on steep slopes below Mount Juneau and Mount Roberts. Because there is no road connection to the rest of North America, materials arrive by barge or air, which affects repair costs and timelines.</p>
<h2>Mendenhall River flooding</h2>
<p>Since 2011, water has built up each summer in Suicide Basin beside the Mendenhall Glacier and then released suddenly down the Mendenhall River. In August 2023 the flood eroded riverbanks and destroyed homes, and in August 2024 record flooding inundated hundreds of homes in the Mendenhall Valley. Flood is generally excluded from homeowner policies, so these losses often raise questions about which damage is covered, such as sewer backup endorsements or separate flood policies.</p>
<h2>Wind, rain and slopes</h2>
<p>Taku winds, strong gusts that come down from the icefield, can hit downtown Juneau and Douglas with hurricane-force gusts. Rain-driven water intrusion through siding and windows is a constant concern. Landslides have damaged downtown homes, though earth movement is typically excluded.</p>
<h2>Housing and claim issues</h2>
<ul>
<li>Older wood-frame homes downtown with long stairs and difficult access</li>
<li>Split-levels in the Mendenhall Valley with finished lower levels</li>
<li>Condos and townhomes with shared roofs and exteriors</li>
<li>Higher material and labor costs due to barge freight</li>
</ul>
<p>We inspect throughout Juneau, Douglas, the Mendenhall Valley, Lemon Creek, Auke Bay and Thane.</p>
""",
        "faqs": [
            ("Was the Mendenhall flood covered by my homeowner policy?", "Surface flooding is usually excluded from homeowner policies. Separate flood policies and some endorsements may apply. Interior water from other causes may be treated differently."),
            ("Why are repairs in Juneau more expensive?", "Materials arrive by barge or air, and contractor availability is limited. A good estimate accounts for both."),
        ],
    },
    {
        "slug": "ketchikan", "city": "Ketchikan", "county": "Ketchikan Gateway Borough", "region": "Southeast",
        "perils": ["Extreme rainfall", "Windstorms", "Landslides", "Water intrusion", "Fire"],
        "hoods": ["Downtown", "Creek Street", "West End", "Bear Valley", "Shoreline Drive", "Carlanna", "Ward Cove", "North Point Higgins", "Saxman"],
        "housing": "Older homes on pilings and steep lots, homes reached by long stairways and boardwalks, waterfront and float-access properties",
        "events": ["August 2024 Third Avenue landslide", "Gulf of Alaska windstorms", "Atmospheric river rainfall"],
        "near": ["sitka", "juneau", "kodiak"],
        "lede": "One of the rainiest cities in the United States, Ketchikan sees roughly 150 inches of precipitation a year. Water intrusion, wind and steep-slope access dominate claims here.",
        "body": """
<h2>Rain is the main event</h2>
<p>Ketchikan averages around 150 inches of precipitation a year, and storms from the Gulf of Alaska can bring several inches in a day. Water finds its way through siding, windows, roofs and foundations, and the line between sudden damage and long-term seepage is often where claims get disputed.</p>
<h2>Steep lots and landslides</h2>
<p>Much of Ketchikan is built on steep hillsides between the mountains and Tongass Narrows. In August 2024, a landslide off the Third Avenue Bypass killed one person and damaged homes. Landslide damage is usually excluded as earth movement, but related losses, such as water damage or fire, may be treated differently.</p>
<h2>Housing and access</h2>
<ul>
<li>Older wood-frame homes on pilings and steep lots</li>
<li>Homes reached by long stairways and boardwalks, which increases labor and material handling costs</li>
<li>Waterfront homes exposed to wind and salt</li>
<li>Island and float-access properties that need boat transport for materials and crews</li>
</ul>
<h2>Common claim issues</h2>
<p>Wind-driven rain claims, roof leaks during storms, access and material handling costs left out of estimates, and disputes over whether water damage was sudden or gradual. We work throughout Ketchikan, Saxman, Ward Cove, North Point Higgins and on Revillagigedo and Gravina islands.</p>
""",
        "faqs": [
            ("Is wind-driven rain covered?", "Many policies cover rain entering through an opening created by wind. Water that seeps in over time is usually excluded."),
            ("Will the estimate include carrying materials up stairs?", "It should if access is difficult. Material handling and access charges are often missing from carrier estimates."),
        ],
    },
    {
        "slug": "sitka", "city": "Sitka", "county": "City and Borough of Sitka", "region": "Southeast",
        "perils": ["Heavy rain", "Gulf windstorms", "Landslides", "Water intrusion", "Snow load"],
        "hoods": ["Downtown", "Halibut Point Road", "Sawmill Creek Road", "Japonski Island", "Indian River", "Kramer Avenue area"],
        "housing": "Historic downtown buildings, mid-century frame homes, waterfront homes facing Sitka Sound",
        "events": ["August 2015 Kramer Avenue landslide", "Gulf of Alaska windstorms", "Heavy rain events"],
        "near": ["juneau", "ketchikan", "kodiak"],
        "lede": "On the outer coast of Baranof Island, Sitka faces the open Gulf of Alaska. Wind, rain and steep terrain shape claims in one of Alaska's most historic towns.",
        "body": """
<h2>Historic town on the outer coast</h2>
<p>Sitka was the capital of Russian America and has a historic downtown with buildings that are more complicated to repair than modern construction. The city faces Sitka Sound and the open Gulf of Alaska, so storms arrive with little to block them.</p>
<h2>Landslides and rain</h2>
<p>In August 2015, heavy rain triggered landslides in Sitka, including one on Kramer Avenue that killed three people. Since then, landslide risk has been a significant local concern. Earth movement is usually excluded from homeowner policies, but water damage and other covered perils may still apply.</p>
<h2>Wind and water intrusion</h2>
<p>Storms from the Gulf bring strong winds and driving rain, which find their way through siding and roofing. Water intrusion claims are common, as are disputes about whether damage is sudden or gradual.</p>
<h2>Housing and common issues</h2>
<ul>
<li>Historic buildings downtown that need specialized repair</li>
<li>Mid-century frame homes along Halibut Point and Sawmill Creek roads</li>
<li>Waterfront homes exposed to wind and salt spray</li>
<li>Barge-dependent material supply that raises costs and lengthens repairs</li>
</ul>
<p>We inspect throughout Sitka, including downtown, Japonski Island, Halibut Point Road and Sawmill Creek Road.</p>
""",
        "faqs": [
            ("Is landslide damage covered?", "Usually not under a standard homeowner policy, which excludes earth movement. Specialty coverage may be available."),
            ("Do historic buildings cost more to repair?", "Often yes. If your policy covers replacement with like kind and quality, historic materials and methods may be part of the scope."),
        ],
    },
    {
        "slug": "kenai-soldotna", "city": "Kenai & Soldotna", "county": "Kenai Peninsula Borough", "region": "Kenai Peninsula",
        "perils": ["Wildfire & smoke", "Windstorms", "Snow load", "Frozen pipes", "Earthquake (with endorsement)"],
        "hoods": ["Soldotna", "Kenai", "Sterling", "Kalifornsky", "Ridgeway", "Nikiski", "Funny River"],
        "housing": "1970s–80s oil-era homes, cabins and river lots, newer subdivisions off Kalifornsky Beach Road",
        "events": ["2019 Swan Lake Fire", "2014 Funny River Fire", "1964 Great Alaska Earthquake"],
        "near": ["homer", "anchorage", "kodiak"],
        "lede": "The central Kenai Peninsula combines oil-industry neighborhoods, river cabins and fast-growing subdivisions, with wildfire and wind as the main property risks.",
        "body": """
<h2>The central peninsula</h2>
<p>Kenai and Soldotna anchor the central Kenai Peninsula, with Sterling, Kalifornsky, Ridgeway, Nikiski and Funny River around them. Much of the housing dates from the oil boom of the 1970s and 1980s, and newer subdivisions have filled in along Kalifornsky Beach Road. Cabins and river lots along the Kenai River add a different set of properties.</p>
<h2>Wildfire</h2>
<p>The 2014 Funny River Fire burned nearly 200,000 acres south of Soldotna, and the 2019 Swan Lake Fire near Sterling burned for months, shutting the Sterling Highway at times and filling the area with smoke. Large stands of beetle-killed spruce have added to fire risk across the peninsula. Smoke and ash claims, as well as direct fire losses, are part of the local picture.</p>
<h2>Wind, snow and cold</h2>
<p>Winter storms bring wind and snow load issues, and cold snaps freeze supply lines in crawlspaces and outbuildings. Older oil-era homes with original windows, roofs and plumbing are particularly vulnerable.</p>
<h2>Common claim issues</h2>
<ul>
<li>Smoke cleaning versus replacement after nearby fires</li>
<li>Wind damage to roofs and siding</li>
<li>Frozen pipe claims in older homes and cabins</li>
<li>Seasonal cabins with vacancy and heat requirements</li>
</ul>
<p>We work in Kenai, Soldotna, Sterling, Nikiski, Kasilof and across the central peninsula.</p>
""",
        "faqs": [
            ("Is a seasonal cabin covered if it freezes while I'm away?", "Many policies require heat to be maintained or the water system drained. Vacancy clauses may also apply. Read the policy carefully."),
            ("Can smoke damage be appraised?", "Yes, when coverage is accepted and the disagreement is about the extent and cost of cleaning or replacement."),
        ],
    },
    {
        "slug": "homer", "city": "Homer", "county": "Kenai Peninsula Borough", "region": "Kenai Peninsula",
        "perils": ["Coastal windstorms", "Snow load", "Volcanic ash", "Frozen pipes", "Earthquake (with endorsement)"],
        "hoods": ["Homer Spit", "Old Town", "Baycrest", "East End Road", "Diamond Ridge", "Skyline Drive", "Kachemak City"],
        "housing": "Custom view homes on the bench and ridges, cabins, bed-and-breakfasts and commercial buildings on the Spit",
        "events": ["1964 earthquake subsidence of the Spit", "2006 Augustine Volcano eruption", "Kachemak Bay windstorms"],
        "near": ["kenai-soldotna", "kodiak", "anchorage"],
        "lede": "At the end of the Sterling Highway, Homer looks across Kachemak Bay to glaciers and volcanoes. Wind, snow and the occasional ashfall are part of owning property here.",
        "body": """
<h2>A town at the end of the road</h2>
<p>Homer sits at the southern end of the Sterling Highway, with homes climbing from Kachemak Bay up to Diamond Ridge and Skyline Drive. The Homer Spit extends into the bay with harbors, businesses and seasonal properties.</p>
<h2>Earthquakes and volcanoes</h2>
<p>The 1964 earthquake caused the Homer Spit to subside several feet. Across Cook Inlet, volcanoes such as Augustine, which erupted in 2006, and Redoubt can drop ash on the southern Kenai Peninsula. Volcanic eruption is listed as a covered peril in many homeowner policies, unlike earthquake, which is usually excluded.</p>
<h2>Wind and snow</h2>
<p>Storms off the bay can bring strong winds to exposed homes on the bench and the Spit. Higher elevations along Skyline Drive and Diamond Ridge get heavy snow. Wind damage, snow load and ice dam claims are common.</p>
<h2>Housing and common issues</h2>
<ul>
<li>Custom view homes with large windows and complex rooflines</li>
<li>Cabins and bed-and-breakfasts with mixed residential and business use</li>
<li>Commercial buildings on the Spit exposed to wind and salt</li>
<li>Higher costs and longer timelines for specialty trades</li>
</ul>
<p>We serve Homer, Kachemak City, Anchor Point, Fritz Creek and the southern peninsula.</p>
""",
        "faqs": [
            ("Is volcanic ash damage covered?", "Volcanic eruption is a named peril in many homeowner forms. Ash cleanup and damage to roofs, HVAC and vehicles may be covered depending on the policy."),
            ("My home is also a bed-and-breakfast. Does that matter?", "Yes. Business use may require a different policy or endorsement, and it can affect how a claim is handled."),
        ],
    },
    {
        "slug": "kodiak", "city": "Kodiak", "county": "Kodiak Island Borough", "region": "Kodiak & Gulf Coast",
        "perils": ["Coastal windstorms", "Heavy rain", "Earthquake (with endorsement)", "Snow load", "Water intrusion"],
        "hoods": ["Downtown Kodiak", "Aleutian Homes", "Mill Bay", "Monashka Bay", "Bells Flats", "Women's Bay", "Chiniak"],
        "housing": "Post-1964 rebuilt neighborhoods, older frame homes, rentals serving the fishing industry and Coast Guard families",
        "events": ["1964 earthquake and tsunami", "January 2018 offshore earthquake and tsunami warning", "Gulf of Alaska storms"],
        "near": ["homer", "kenai-soldotna", "sitka"],
        "lede": "Kodiak Island faces the Gulf of Alaska head-on. Storms, rain and seismic risk shape property claims in a community rebuilt after the 1964 tsunami.",
        "body": """
<h2>Rebuilt after the tsunami</h2>
<p>The 1964 Great Alaska Earthquake sent tsunami waves through Kodiak's downtown and harbor, destroying much of the waterfront. Neighborhoods such as Aleutian Homes were rebuilt in the years that followed. Today Kodiak is home to one of the largest fishing ports in the country and a major Coast Guard base.</p>
<h2>Weather and seismic risk</h2>
<p>Kodiak gets frequent storms from the Gulf of Alaska, bringing high winds and heavy rain. In January 2018, a magnitude 7.9 earthquake offshore triggered a tsunami warning and evacuations, a reminder that seismic risk is constant here.</p>
<h2>Housing and claim issues</h2>
<ul>
<li>Post-1964 homes in Aleutian Homes and around downtown</li>
<li>Rentals serving fishing crews and Coast Guard families</li>
<li>Homes in Bells Flats and Chiniak with longer travel and access costs</li>
<li>Barge-dependent supply that raises material costs</li>
</ul>
<h2>Common disputes</h2>
<p>Wind and rain damage to roofs and siding, water intrusion, and estimates that do not reflect the cost of shipping materials to the island. Earthquake claims depend on whether the owner carries that coverage.</p>
<p>We work throughout the Kodiak road system, including downtown, Mill Bay, Monashka Bay, Women's Bay and Chiniak.</p>
""",
        "faqs": [
            ("Is tsunami damage covered?", "Tsunami and flood damage are usually excluded from standard homeowner policies. Flood insurance or earthquake endorsements may apply depending on their terms."),
            ("Why do repairs on Kodiak cost more?", "Materials and specialty labor often come from off-island. A good estimate includes freight and travel."),
        ],
    },
    {
        "slug": "valdez", "city": "Valdez", "county": "Chugach Census Area", "region": "Prince William Sound",
        "perils": ["Extreme snowfall", "Snow load & sliding snow", "Gap winds", "Earthquake (with endorsement)", "Frozen pipes"],
        "hoods": ["Downtown Valdez", "Robe Lake area", "Richardson Highway corridor", "Small boat harbor area"],
        "housing": "Post-1964 frame homes with steep metal roofs, arctic entries and snow-shedding designs, plus commercial and industrial buildings",
        "events": ["1964 earthquake and relocation of the town", "Record snowfall winters", "Thompson Pass wind events"],
        "near": ["anchorage", "palmer", "kodiak"],
        "lede": "Valdez is one of the snowiest towns in North America. Snow load, sliding snow and wind through Thompson Pass make roof and structural claims a constant here.",
        "body": """
<h2>A town that moved</h2>
<p>The 1964 Great Alaska Earthquake triggered an underwater landslide and waves that destroyed the original Valdez waterfront. The town was rebuilt on more stable ground about four miles west, so most homes date from after 1964. Valdez is in the Chugach Census Area, part of Alaska's Unorganized Borough, and it is the southern end of the Trans-Alaska Pipeline.</p>
<h2>Snow, and lots of it</h2>
<p>Valdez averages several hundred inches of snow a year, and nearby Thompson Pass gets even more. Homes here are built with steep metal roofs, arctic entries and designs that shed snow, but heavy winters still overload roofs, crush decks and outbuildings, and send sliding snow into walls, vents and vehicles.</p>
<h2>Wind and cold</h2>
<p>Gap winds through Thompson Pass and down the valley can be strong, and cold snaps bring freeze risk. Snow-driven water intrusion and ice dams are also common.</p>
<h2>Common claim issues</h2>
<ul>
<li>Snow load damage to roofs, decks, carports and outbuildings</li>
<li>Sliding snow damage to siding, vents, meters and windows</li>
<li>Snow removal and shoring costs that are under-reimbursed</li>
<li>Higher material and labor costs due to location</li>
</ul>
<p>We serve Valdez and the surrounding Prince William Sound area.</p>
""",
        "faqs": [
            ("Is damage from sliding snow covered?", "Damage caused by the weight of snow or by snow sliding off a roof is often covered. Some structures, such as awnings and fences, may have limits."),
            ("Are snow removal costs covered?", "Reasonable costs to protect the property from further damage are often reimbursed. Keep receipts and photos."),
        ],
    },
]
