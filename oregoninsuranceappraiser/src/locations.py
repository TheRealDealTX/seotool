"""Location pages: 12 Oregon cities with local detail (county, neighborhoods, storm history, housing mix)."""

LOCATIONS = [
    {
        "slug": "portland",
        "city": "Portland",
        "county": "Multnomah County",
        "region": "Portland Metro",
        "perils": ["Ice storms", "Falling firs", "East-wind gusts", "Burst pipes", "Heat damage"],
        "hoods": "Laurelhurst, Irvington, Sellwood-Moreland, St. Johns, the Pearl District and the West Hills",
        "lede": "Portland’s tree canopy, century-old housing and Gorge winds create a distinct mix of claims. We value losses from Laurelhurst bungalows to Pearl District condos.",
        "body": """
<h2>What Portland claims look like</h2>
<p>Portland is Oregon’s largest city and the seat of Multnomah County, with small portions reaching into Washington County and Clackamas County. Much of the housing on the east side was built before 1940: Craftsman bungalows, Old Portland foursquares and English cottages in neighborhoods like Laurelhurst, Irvington, Eastmoreland and Sellwood-Moreland. Those homes have plaster walls, old-growth fir trim and original hardwood that cost far more to repair than the generic finishes in a carrier’s price list.</p>
<p>On the west side and in the Pearl District and South Waterfront, condo towers and mid-rise buildings bring association master policies and unit-owner policies into nearly every water loss.</p>
<h2>Storms that shaped Portland claims</h2>
<ul>
<li><strong>The February 2021 ice storm</strong> brought down limbs and whole trees across the city, with long power outages and burst pipes to follow.</li>
<li><strong>The January 2024 ice storm</strong> hit east Portland and the Gorge corridor especially hard, with freezing rain driven by strong east winds.</li>
<li><strong>The June 2021 heat dome</strong> set an all-time record high for the city and led to claims for heat-related failures and fires.</li>
<li><strong>East winds</strong> through the Columbia River Gorge regularly damage roofs and fences in Parkrose, Gateway and outer east Portland.</li>
</ul>
<h2>Common disputes we see here</h2>
<p>Partial approvals on older roofs where matching is impossible, plaster walls scoped as drywall, fallen-tree claims priced as simple patches, and condo water losses where the master policy and unit policy point at each other. Each one needs a scope built from what is actually in the house.</p>
""",
        "faqs": [
            ("Do you inspect in all Portland neighborhoods?", "Yes, across the city and the surrounding metro area, including east Multnomah County."),
            ("My house is over 100 years old. Does that affect the claim?", "It can affect pricing, matching and code requirements. Older finishes like plaster and old-growth trim usually cost more to repair, and the estimate should reflect that."),
            ("Who handles a leak in a Portland condo?", "It depends on the association’s bylaws and both policies. We review them before deciding which damage belongs to which policy."),
        ],
        "near": ["beaverton", "lake-oswego", "hillsboro"],
    },
    {
        "slug": "beaverton",
        "city": "Beaverton",
        "county": "Washington County",
        "region": "Portland Metro",
        "perils": ["Windstorms", "Ice-laden limbs", "Water leaks", "Roof wear disputes"],
        "hoods": "Murrayhill, Cedar Hills, Highland, Denney Whitford, Sexton Mountain and South Cooper Mountain",
        "lede": "Beaverton’s suburban neighborhoods mix 1960s ranch houses, 1990s subdivisions and new townhomes. We handle wind, ice and water claims across the city and Washington County.",
        "body": """
<h2>Beaverton’s housing mix</h2>
<p>Beaverton sits in Washington County just west of Portland. Older neighborhoods like Cedar Hills, Highland and Denney Whitford are full of 1950s through 1970s ranch homes and split-levels. Murrayhill and Sexton Mountain grew in the 1980s and 1990s with two-story homes on wooded lots, and South Cooper Mountain has added newer single-family homes and townhomes.</p>
<p>That range matters on a claim. A 1965 ranch house may have original wiring and plumbing that create code questions when walls are opened, while a newer townhome claim often involves a homeowners association and shared roof lines.</p>
<h2>What the weather brings</h2>
<ul>
<li><strong>Ice storms</strong> in 2021 and 2024 brought down limbs on roofs and cars across the west side.</li>
<li><strong>Winter windstorms</strong> damage composition roofs and fences, especially on exposed hillsides like Sexton Mountain and Cooper Mountain.</li>
<li><strong>Water losses</strong> from supply lines, water heaters and frozen pipes are the most common interior claims.</li>
</ul>
<h2>Where Beaverton claims go wrong</h2>
<p>Townhome roof claims scoped for one unit when the roof plane runs across several, partial-slope approvals on discontinued shingles, and water losses where drying stopped before materials were dry. We document each to an appraisal standard.</p>
""",
        "faqs": [
            ("Do you work with HOAs in Beaverton?", "Yes. Townhome and condo associations often need a consistent scope across many units, and we work with boards and managers on that."),
            ("Is my older ranch home harder to claim?", "Not harder, but older wiring, plumbing and materials can raise code and matching questions that the estimate should address."),
            ("Do you cover all of Washington County?", "Yes, including Hillsboro, Tigard, Tualatin, Forest Grove and unincorporated areas."),
        ],
        "near": ["hillsboro", "portland", "lake-oswego"],
    },
    {
        "slug": "hillsboro",
        "city": "Hillsboro",
        "county": "Washington County",
        "region": "Portland Metro",
        "perils": ["Windstorms", "Ice storms", "Commercial roofs", "Water leaks"],
        "hoods": "Orenco Station, AmberGlen, Witch Hazel, Jackson Bottom, Reedville and Reed’s Crossing",
        "lede": "Hillsboro has grown fast around its tech campuses, with master-planned neighborhoods and large commercial roofs. We handle residential and commercial claims across the city.",
        "body": """
<h2>A fast-growing county seat</h2>
<p>Hillsboro is the seat of Washington County and one of Oregon’s fastest-growing cities. Its economy centers on semiconductor and technology campuses, and its neighborhoods reflect that growth: Orenco Station’s townhomes and mixed-use buildings, newer subdivisions in South Hillsboro and Reed’s Crossing, and older homes near downtown and in Reedville.</p>
<p>The city also has a large inventory of industrial and commercial buildings with low-slope membrane roofs, which raise their own scope questions after wind and ice.</p>
<h2>Weather risks</h2>
<ul>
<li><strong>Ice storms</strong>, including February 2021, brought down limbs and caused outages across the Tualatin Valley.</li>
<li><strong>Winter windstorms</strong> sweep across the open farmland west of the city and hit exposed homes and commercial roofs.</li>
<li><strong>Water losses</strong> in newer homes from failed supply lines, fixtures and appliances.</li>
</ul>
<h2>Commercial and multifamily</h2>
<p>Apartment communities and commercial buildings in Hillsboro often involve large membrane roofs, rooftop equipment and tenant improvements. We price those losses with the access, phasing and code items commercial repairs need.</p>
""",
        "faqs": [
            ("Do you handle commercial claims in Hillsboro?", "Yes, including industrial buildings, retail centers and apartment communities."),
            ("My home is only a few years old. Can it still be underpaid?", "Yes. Newer homes still see scope and pricing disputes, especially on roofs and water losses."),
            ("Do you inspect on weekends?", "When needed for access, yes. Tell us what works when you call."),
        ],
        "near": ["beaverton", "portland", "corvallis"],
    },
    {
        "slug": "lake-oswego",
        "city": "Lake Oswego",
        "county": "Clackamas County",
        "region": "Portland Metro",
        "perils": ["Falling firs", "Ice storms", "High-value interiors", "Water leaks"],
        "hoods": "First Addition, Lake Grove, Westlake, Palisades, Forest Highlands and Mountain Park",
        "lede": "Lake Oswego’s heavy tree canopy and higher-value homes mean tree-impact and interior-finish claims are large and often underpaid. We value them in detail.",
        "body": """
<h2>Homes and trees in Lake Oswego</h2>
<p>Lake Oswego lies mostly in Clackamas County, with small parts in Multnomah County and Washington County. The city wraps around Oswego Lake, and neighborhoods like First Addition, Palisades, Forest Highlands and Mountain Park sit under a dense canopy of Douglas fir and other tall trees. Homes range from mid-century houses to large custom homes with high-end interiors.</p>
<p>Higher-value homes bring higher-value claims: custom millwork, stone, specialty flooring and complex roofs that a standard estimate doesn’t price well.</p>
<h2>Storm history</h2>
<ul>
<li><strong>The February 2021 ice storm</strong> was especially damaging in Clackamas County, with many large trees down and long power outages.</li>
<li><strong>Winter windstorms</strong> regularly bring down limbs and whole trees on saturated soil.</li>
<li><strong>Heat and drought</strong> in recent summers have stressed trees, which can make them more likely to fail in later storms.</li>
</ul>
<h2>What we focus on</h2>
<p>Structural damage from tree impacts, matching of high-end finishes, crane and removal costs, and interior water damage that spreads into custom cabinetry and flooring. We document these thoroughly so nothing is valued as standard grade when it isn’t.</p>
""",
        "faqs": [
            ("My home has custom finishes. Will the insurer price them correctly?", "Often not at first. Estimates tend to default to standard materials. We document and price the actual grade of finishes."),
            ("Who pays to remove a fir that fell on my house?", "Most policies pay to remove a tree that damaged a covered structure, up to a limit. Emergency removal to protect the home may be handled separately."),
            ("Do you cover the rest of Clackamas County?", "Yes, including West Linn, Oregon City, Happy Valley, Milwaukie and rural areas."),
        ],
        "near": ["portland", "beaverton", "salem"],
    },
    {
        "slug": "salem",
        "city": "Salem",
        "county": "Marion County",
        "region": "Mid-Willamette Valley",
        "perils": ["Ice storms", "Wildfire smoke", "Windstorms", "Tornado (rare)", "Frozen pipes"],
        "hoods": "West Salem, South Salem, Grant, Northeast Neighbors, Sunnyslope, Morningside and Highland",
        "lede": "Oregon’s capital took a direct hit in the February 2021 ice storm and sits next to the Santiam Canyon fire zone. We handle tree, ice, smoke and wind claims across Salem.",
        "body": """
<h2>Salem at a glance</h2>
<p>Salem is Oregon’s capital and the seat of Marion County; West Salem lies across the Willamette River in Polk County. Neighborhoods range from historic homes near the Capitol and in the Grant and Court-Chemeketa areas to mid-century ranch houses in South Salem and newer subdivisions on the edges of town. The state’s insurance regulator, the Division of Financial Regulation, is based here.</p>
<h2>Storms and fires that shaped Salem claims</h2>
<ul>
<li><strong>The February 2021 ice storm</strong> was one of the worst in the city’s memory, with trees down across neighborhoods and many homes without power for days.</li>
<li><strong>The 2020 Labor Day fires</strong>, especially Beachie Creek and Lionshead, burned through the Santiam Canyon east of Salem, destroying homes in Detroit, Gates and Mill City and blanketing the city in smoke.</li>
<li><strong>The December 2010 Aumsville tornado</strong>, an EF2, struck a small town just southeast of Salem.</li>
<li><strong>Winter windstorms</strong> bring down limbs and damage roofs every season.</li>
</ul>
<h2>Claims we see in Salem</h2>
<p>Tree impacts on older homes, ice-related pipe bursts, smoke infiltration in homes that survived nearby fires, and roof claims after windstorms. Older homes with plaster walls and original finishes need careful pricing.</p>
""",
        "faqs": [
            ("Do you handle Santiam Canyon wildfire claims?", "Yes. We work with property owners in the canyon and around Salem on rebuild, contents and smoke claims."),
            ("Can I file a complaint with the state about my claim?", "Yes. The Oregon Division of Financial Regulation accepts consumer complaints. That process is separate from appraisal, and you can use both."),
            ("Do you cover Polk County too?", "Yes, including West Salem, Dallas, Monmouth and Independence."),
        ],
        "near": ["corvallis", "lake-oswego", "eugene"],
    },
    {
        "slug": "eugene",
        "city": "Eugene",
        "county": "Lane County",
        "region": "Southern Willamette Valley",
        "perils": ["Snow & ice", "Fallen trees", "Wildfire smoke", "Windstorms", "Water leaks"],
        "hoods": "South Eugene, the Friendly Area, Whiteaker, Jefferson Westside, Santa Clara, River Road and College Hill",
        "lede": "Eugene’s 2019 snowstorm and the Holiday Farm Fire up the McKenzie River left lasting marks on local claims. We value tree, snow, fire and smoke losses across Lane County.",
        "body": """
<h2>Eugene’s neighborhoods and housing</h2>
<p>Eugene is the seat of Lane County and home to the University of Oregon. South Eugene and College Hill have older homes on wooded hillsides; the Friendly Area, Jefferson Westside and Whiteaker hold a mix of bungalows and mid-century houses; Santa Clara and River Road have larger lots and ranch homes. Student rentals near campus add landlord and multifamily claims to the mix.</p>
<h2>Events that shaped claims here</h2>
<ul>
<li><strong>The February 2019 snowstorm</strong> dropped heavy, wet snow on Eugene and Springfield, bringing down thousands of trees and limbs onto homes, cars and power lines.</li>
<li><strong>The 2020 Holiday Farm Fire</strong> burned along the McKenzie River east of Springfield, destroying hundreds of homes in communities like Blue River and Vida.</li>
<li><strong>Ice storms and windstorms</strong> continue to bring down limbs, especially in the hills of South Eugene.</li>
</ul>
<h2>Common disputes</h2>
<p>Snow and tree claims priced as roof patches when framing was damaged, smoke claims limited to light cleaning, and wildfire total losses where rebuild costs outran the estimate. We document these with measurements, photos and local pricing.</p>
""",
        "faqs": [
            ("Do you handle McKenzie River wildfire claims?", "Yes, including total losses, partial losses and smoke damage from the Holiday Farm Fire and later fires."),
            ("Do you work with landlords near the university?", "Yes. Rental property claims often involve loss of rents and multiple units, and we value those too."),
            ("Do you cover Springfield and the rest of Lane County?", "Yes, from Florence on the coast to Oakridge in the Cascades."),
        ],
        "near": ["corvallis", "salem", "bend"],
    },
    {
        "slug": "corvallis",
        "city": "Corvallis",
        "county": "Benton County",
        "region": "Mid-Willamette Valley",
        "perils": ["Windstorms", "Snow & ice", "Fallen trees", "Rental property losses"],
        "hoods": "College Hill, Job’s Addition, Witham Hill, Timberhill, Skyline West and North Corvallis",
        "lede": "Corvallis combines Oregon State University rentals with older homes and wooded hillsides. We handle wind, tree, ice and water claims for owners and landlords.",
        "body": """
<h2>A college town with old trees</h2>
<p>Corvallis is the seat of Benton County and home to Oregon State University. Neighborhoods near campus, like College Hill and Job’s Addition, have older homes, many of them rentals. Witham Hill, Timberhill and Skyline West sit on wooded slopes with newer homes, and North Corvallis has a mix of subdivisions and apartments.</p>
<h2>What the weather brings</h2>
<ul>
<li><strong>Winter windstorms</strong> sweep up the Willamette Valley and bring down limbs on hillside homes.</li>
<li><strong>The 2019 snowstorm and the 2021 ice storm</strong> both damaged trees and roofs across the mid-valley.</li>
<li><strong>Water losses</strong> in rentals and older homes from pipes, fixtures and roof leaks.</li>
</ul>
<h2>Landlord and multifamily claims</h2>
<p>Many Corvallis properties are rentals, so claims often involve loss of rental income, tenant contents questions and multiple units. We value the building damage and help landlords document lost rents where the policy covers them.</p>
""",
        "faqs": [
            ("Do you handle rental property claims?", "Yes, including single-family rentals, duplexes and apartment buildings."),
            ("My tenant’s belongings were damaged. Is that my claim?", "Usually not. Tenants’ belongings are generally covered by their own renters policy. Your landlord policy covers the building and your own property."),
            ("Do you cover Albany and Philomath?", "Yes, along with the rest of Benton and Linn counties."),
        ],
        "near": ["salem", "eugene", "newport"],
    },
    {
        "slug": "bend",
        "city": "Bend",
        "county": "Deschutes County",
        "region": "Central Oregon",
        "perils": ["Snow load", "Hail", "Frozen pipes", "Wildfire risk", "Wind"],
        "hoods": "Old Bend, Awbrey Butte, NorthWest Crossing, the Old Mill District, River West and Larkspur",
        "lede": "High-desert Bend sees snow load, frozen pipes, summer hail and wildfire risk, often in second homes that sit empty for weeks. We know how those claims play out.",
        "body": """
<h2>Central Oregon’s largest city</h2>
<p>Bend is the seat of Deschutes County and has grown quickly into a city of new construction, resort-style homes and older bungalows in Old Bend. NorthWest Crossing and Awbrey Butte have newer custom homes; the Old Mill District and River West mix condos and older houses; outlying areas include large lots in the wildland-urban interface. Nearby resort communities such as Sunriver add many second homes and short-term rentals.</p>
<h2>Weather and fire risks</h2>
<ul>
<li><strong>Snow load</strong> on roofs, decks and carports during heavy winters.</li>
<li><strong>Frozen pipes</strong> in cold snaps, especially in second homes that sit unoccupied.</li>
<li><strong>Summer hail</strong> from high-desert thunderstorms, which can damage roofs, siding and vehicles.</li>
<li><strong>Wildfire and smoke.</strong> Central Oregon’s forests and the wildland-urban interface around Bend carry real wildfire risk, and smoke infiltration claims follow fire seasons.</li>
</ul>
<h2>Second homes and vacancy</h2>
<p>Many policies have conditions about heat, water shutoff or vacancy for homes left empty. Those conditions can shape a frozen-pipe claim. We read the form before assuming a loss is fully covered, and we value the covered damage in full.</p>
""",
        "faqs": [
            ("Does hail damage happen in Bend?", "Yes. Summer thunderstorms in Central Oregon can produce hail that damages roofs and siding."),
            ("My vacation home pipes froze. Will the policy pay?", "It depends on your policy’s conditions for unoccupied homes, such as maintaining heat or shutting off water. Send us the form and the letter."),
            ("Do you cover Redmond, Sisters and Sunriver?", "Yes, across Deschutes, Crook and Jefferson counties."),
        ],
        "near": ["eugene", "pendleton", "medford"],
    },
    {
        "slug": "medford",
        "city": "Medford",
        "county": "Jackson County",
        "region": "Southern Oregon",
        "perils": ["Wildfire", "Smoke infiltration", "Extreme heat", "Wind", "Water leaks"],
        "hoods": "East Medford, West Medford, Southeast Medford and nearby Phoenix, Talent and Central Point",
        "lede": "The Almeda Fire swept from Ashland toward Medford in September 2020. Wildfire, smoke and heat now shape property claims across the Rogue Valley.",
        "body": """
<h2>The Rogue Valley’s hub</h2>
<p>Medford is the seat of Jackson County and the largest city in Southern Oregon. East Medford has newer homes on the hillsides, West Medford has older homes and neighborhoods, and the surrounding valley includes Central Point, Phoenix, Talent, Jacksonville and Ashland. Manufactured home parks are a significant part of the housing stock.</p>
<h2>The Almeda Fire</h2>
<p>On September 8, 2020, the Almeda Fire started near Ashland and burned north along the Bear Creek corridor through Talent and Phoenix toward Medford. It destroyed roughly 2,500 homes and businesses, many of them manufactured homes, in a single afternoon. The claims that followed raised every hard question in property insurance: rebuild costs, contents inventories, debris removal and underinsurance.</p>
<h2>Ongoing risks</h2>
<ul>
<li><strong>Wildfire and smoke</strong> from fires in the surrounding mountains most summers.</li>
<li><strong>Extreme heat</strong>, with summer temperatures often over 100°F.</li>
<li><strong>Wind and winter storms</strong> that damage roofs and trees.</li>
</ul>
<h2>Manufactured homes</h2>
<p>Manufactured home claims have their own pricing and replacement issues, including availability, transport and setup costs, and site work. We value them for what replacement really involves.</p>
""",
        "faqs": [
            ("Do you handle Almeda Fire claims?", "Yes, including rebuild, contents and smoke claims, and disputes about recoverable depreciation."),
            ("Can smoke from a nearby fire damage my home enough to claim?", "Yes. Smoke and ash infiltration can require cleaning or replacement of finishes, HVAC and contents."),
            ("Do you cover Ashland and Grants Pass?", "Yes, across Jackson and Josephine counties."),
        ],
        "near": ["grants-pass", "bend", "eugene"],
    },
    {
        "slug": "grants-pass",
        "city": "Grants Pass",
        "county": "Josephine County",
        "region": "Southern Oregon",
        "perils": ["Wildfire", "Smoke", "Heat", "Windstorms", "Rural outbuildings"],
        "hoods": "historic downtown, Redwood, Fruitdale, Harbeck and nearby Merlin and Murphy",
        "lede": "Grants Pass sits on the Rogue River surrounded by forested hills with a long wildfire history. We value fire, smoke and storm claims for homes, acreage and outbuildings.",
        "body": """
<h2>Living on the Rogue</h2>
<p>Grants Pass is the seat of Josephine County, set along the Rogue River in Southern Oregon. Housing includes older homes near the historic downtown, neighborhoods in Redwood and Fruitdale, and many rural properties on acreage with shops, barns and manufactured homes in the surrounding hills.</p>
<h2>Fire country</h2>
<p>Josephine County has a long wildfire history, from the massive 2002 Biscuit Fire in the Siskiyou Mountains to the 2018 Taylor Creek and Klondike fires west of Merlin. Smoke from regional fires settles in the Rogue Valley most summers. Rural homes in the wildland-urban interface face both direct fire risk and frequent smoke infiltration.</p>
<h2>Rural property claims</h2>
<ul>
<li><strong>Outbuildings</strong> such as barns, shops and pump houses under other-structures coverage</li>
<li><strong>Wells, septic and long driveways</strong> that affect access and rebuild costs</li>
<li><strong>Manufactured homes</strong> with their own replacement and setup costs</li>
<li><strong>Heat and wind damage</strong> to roofs and siding</li>
</ul>
<p>Rural claims often take longer to inspect and price. We make sure distance and access are reflected in the estimate.</p>
""",
        "faqs": [
            ("Do you travel to rural Josephine County?", "Yes. We inspect rural properties and outbuildings across the county."),
            ("Are barns and shops covered?", "Often under other-structures coverage, which may have a separate limit. Farm policies work differently. We review your form."),
            ("What if no insurer will write my rural home?", "If you can’t find coverage in the regular market, the Oregon FAIR Plan Association may offer basic property coverage. Its policies have their own terms."),
        ],
        "near": ["medford", "eugene", "newport"],
    },
    {
        "slug": "newport",
        "city": "Newport",
        "county": "Lincoln County",
        "region": "Central Oregon Coast",
        "perils": ["Coastal gales", "Wind-driven rain", "Salt-air corrosion", "Wildfire (Echo Mountain)"],
        "hoods": "Nye Beach, Agate Beach, the Bayfront, South Beach and Yaquina Heights",
        "lede": "Newport faces the Pacific head-on. Coastal gales, wind-driven rain and salt air shape every roof and siding claim. We value storm losses along the Lincoln County coast.",
        "body": """
<h2>A working harbor and beach town</h2>
<p>Newport is the seat of Lincoln County on the central Oregon coast. Nye Beach has older cottages and newer vacation homes; Agate Beach and Yaquina Heights sit on bluffs exposed to the ocean; the Bayfront mixes commercial fishing, seafood processing and tourism; South Beach lies across the Yaquina Bay Bridge. Vacation rentals and second homes are common.</p>
<h2>Storms on the coast</h2>
<ul>
<li><strong>The December 2007 Great Coastal Gale</strong> brought hurricane-force gusts to the Oregon coast and caused widespread damage and outages.</li>
<li><strong>Winter storms</strong> bring strong winds and heavy, wind-driven rain several times each season.</li>
<li><strong>The 2020 Echo Mountain Complex fire</strong> burned homes near Otis and Lincoln City, north of Newport.</li>
</ul>
<h2>Coastal claim issues</h2>
<p>Wind-driven rain gets behind siding and windows that look fine from outside. Salt air shortens the life of metal components, and insurers sometimes use that to argue damage is corrosion rather than storm. Vacation rentals add loss-of-rents questions. We document storm damage separately from long-term wear so the panel sees the difference.</p>
<div class="note"><b class="h">Flood and tsunami</b>Storm surge, tsunami and flood damage are generally excluded from homeowner policies and require separate coverage.</div>
""",
        "faqs": [
            ("Is wind-driven rain damage covered on the coast?", "Many policies cover interior rain damage only if wind first damaged the roof or walls. We review your form."),
            ("Do you handle vacation rental claims?", "Yes, including loss of rental income where the policy provides it."),
            ("Do you cover the rest of the coast?", "Yes, from Astoria to Brookings."),
        ],
        "near": ["corvallis", "salem", "portland"],
    },
    {
        "slug": "pendleton",
        "city": "Pendleton",
        "county": "Umatilla County",
        "region": "Eastern Oregon",
        "perils": ["Hail", "Thunderstorm wind", "Snow & cold", "Farm structures"],
        "hoods": "North Hill, South Hill, downtown and the surrounding wheat country",
        "lede": "Eastern Oregon’s hail, thunderstorm winds and hard winters damage roofs, siding and farm buildings. We value claims in Pendleton and across Umatilla County.",
        "body": """
<h2>Wheat country and a historic downtown</h2>
<p>Pendleton is the seat of Umatilla County in northeastern Oregon, known for the Pendleton Round-Up and its woolen mill. North Hill and South Hill have older homes overlooking downtown, and the surrounding area is wheat farms, ranches and small towns. Farm and ranch properties add barns, shops, grain storage and equipment buildings to many claims.</p>
<h2>Weather east of the mountains</h2>
<ul>
<li><strong>Hail</strong> from summer thunderstorms damages roofs, siding, windows and vehicles.</li>
<li><strong>Thunderstorm winds</strong> and downbursts damage roofs and outbuildings.</li>
<li><strong>Cold and snow</strong> bring frozen pipes and snow-load damage in hard winters.</li>
<li><strong>Flooding</strong>, such as the February 2020 Umatilla River flood, is generally excluded from property policies and requires separate flood coverage.</li>
</ul>
<h2>Hail claims in eastern Oregon</h2>
<p>Hail damage disputes often turn on whether impacts are “functional” or “cosmetic,” whether the roof can be repaired, and how metal roofs and siding are treated. Some policies limit cosmetic damage on metal. We read the form and document every impact.</p>
""",
        "faqs": [
            ("Do you handle farm and ranch claims?", "We handle the building portions of farm and ranch claims. Farm policies differ from homeowner policies, so we review the form first."),
            ("My metal roof has hail dents but no leaks. Is that covered?", "It depends on the policy. Some forms exclude cosmetic damage to metal roofs. We review the wording before valuing it."),
            ("Do you cover Hermiston and La Grande?", "Yes, across northeastern Oregon."),
        ],
        "near": ["bend", "portland", "salem"],
    },
]
