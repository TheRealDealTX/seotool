"""Colorado service-area pages. Local detail is specific to each city."""

LOCATIONS = [
    {
        "slug": "denver", "city": "Denver", "county": "City & County of Denver", "region": "Front Range", "photo": "denver",
        "perils": ["Large hail", "Severe thunderstorms", "Spring snow", "Burst pipes", "Wind"],
        "near": ["aurora", "lakewood", "boulder"],
        "services": ["hail-roof-damage-appraisal", "homeowner-claim-appraiser", "commercial-hoa-appraisal", "water-pipe-burst-appraisal", "carrier-estimate-review"],
        "card": "Denver squares, bungalows and high-rise condos in the heart of Hail Alley.",
        "h1": "Insurance Appraiser in Denver",
        "title": "Insurance Appraiser in Denver, CO | Hail Claims",
        "desc": "Insurance appraiser for Denver homes, condos and businesses. Independent appraisal and estimate review for hail, wind, snow and water claims.",
        "lede": "Denver’s housing runs from 1890s Victorians to glass towers, and its hail season runs from April through September. We value disputed claims across the city’s neighborhoods.",
        "body": """
<h2>What shapes Denver claims</h2>
<p>Denver is a consolidated city and county, and its housing stock is unusually mixed. Capitol Hill and Baker hold brick Victorians and Denver squares; Wash Park, Platt Park and Berkeley are full of 1910s–1920s bungalows; Park Hill has Tudors and foursquares; and Central Park and the river corridor add newer townhomes and mid-rise condos. Each comes with its own roofing, siding and interior details — and its own ways for a generic estimate to miss.</p>
<p>The city sits squarely in Hail Alley. Summer storms that form over the foothills drift east over the metro, and many neighborhoods have filed hail claims more than once in the past decade. Repeat storms create arguments about prior damage, discontinued shingles and whether a roof can be patched.</p>
<h2>Disputes we see in Denver</h2>
<ul>
<li>Spot repairs on older laminated shingles that no longer match.</li>
<li>Historic-district requirements for windows, siding or roofing left out of the scope.</li>
<li>Brick and stucco repairs priced as simple patching.</li>
<li>Condo losses where the HOA master policy and the unit owner’s HO-6 policy overlap.</li>
<li>Basement water losses in older homes with original plumbing.</li>
</ul>
<h2>Working across the city</h2>
<p>We work in Highlands, Sloan’s Lake, Congress Park, Cherry Creek, Hilltop, Wash Park, University, Montbello, Green Valley Ranch, Stapleton/Central Park, Harvey Park and the rest of the city, scheduling inspections around your timeline and meeting contractors on site when that helps.</p>
""",
        "faqs": [
            ("Does a historic designation affect my Denver claim?", "It can. Landmark districts may require approved materials or methods for exterior repairs. When those requirements raise the cost, ordinance-or-law coverage may be relevant."),
            ("My condo HOA filed a claim too. Do I need my own?", "Often yes. The association’s master policy covers parts of the building it insures; your HO-6 policy covers your unit’s interior and contents. We help sort out which policy covers what."),
        ],
    },
    {
        "slug": "colorado-springs", "city": "Colorado Springs", "county": "El Paso County", "region": "Front Range", "photo": "cosprings",
        "perils": ["Large hail", "Wildfire", "Downslope wind", "Heavy snow", "Flash flooding"],
        "near": ["castle-rock", "pueblo", "denver"],
        "services": ["hail-roof-damage-appraisal", "wildfire-claim-appraisal", "wind-tornado-claim-appraisal", "homeowner-claim-appraiser", "fire-smoke-loss-appraisal"],
        "card": "Foothill neighborhoods shaped by Waldo Canyon, Black Forest and big hail.",
        "h1": "Insurance Appraiser in Colorado Springs",
        "title": "Colorado Springs Insurance Appraiser | El Paso Co.",
        "desc": "Colorado Springs insurance appraiser for El Paso County homes and businesses: hail, wildfire and wind claim appraisal and estimate reviews.",
        "lede": "Colorado Springs sits where the plains meet Pikes Peak. That means big hail on the east side, wildfire risk along the foothills and wind that can come from any direction.",
        "body": """
<h2>A city with a wildfire memory</h2>
<p>Colorado Springs residents remember the June 2012 Waldo Canyon Fire, which destroyed hundreds of homes in the Mountain Shadows neighborhood, and the June 2013 Black Forest Fire northeast of the city, which destroyed roughly 500 more. Both fires changed how local homeowners think about defensible space, roofing materials and the adequacy of their dwelling limits.</p>
<p>Hail is the more frequent claim. Storms rolling off the Rampart Range regularly hit Briargate, Northgate, Stetson Hills and the Powers corridor, and an August 2018 storm dropped baseball-sized hail across parts of the city.</p>
<h2>Housing and claim patterns</h2>
<ul>
<li><strong>Foothill neighborhoods</strong> — Broadmoor, Mountain Shadows, Rockrimmon and Cedar Heights: larger custom homes, steep roofs, wood and stucco, and wildland-urban interface exposure.</li>
<li><strong>Older core</strong> — Old North End and Old Colorado City: Victorian and early-1900s homes with details that standard line items price poorly.</li>
<li><strong>Northeast and east growth</strong> — Briargate, Banning Lewis Ranch and the Powers corridor: tract homes with laminated shingle roofs that take repeated hail.</li>
<li><strong>Military households</strong> near Fort Carson, Peterson and the Air Force Academy who may be reassigned mid-claim.</li>
</ul>
<h2>What we focus on here</h2>
<p>Steep-roof and high-roof charges on foothill homes, repairability of discontinued shingles, smoke and ash cleaning after nearby fires, and rebuild costs that reflect local labor and material availability.</p>
""",
        "faqs": [
            ("I’m being relocated by the military. Can appraisal continue?", "Yes. Appraisal can proceed while you’re away if the property is accessible for inspection. Plan for a local contact and keep your contact details current with the insurer."),
            ("Does living near open space affect my claim?", "It can affect coverage and premiums, but once a loss is accepted, appraisal focuses on the cost to repair or rebuild your property."),
        ],
    },
    {
        "slug": "aurora", "city": "Aurora", "county": "Arapahoe, Adams & Douglas Counties", "region": "Front Range", "photo": "aurora",
        "perils": ["Large hail", "Severe thunderstorms", "Wind", "Tornadoes", "Burst pipes"],
        "near": ["denver", "castle-rock", "greeley"],
        "services": ["hail-roof-damage-appraisal", "commercial-hoa-appraisal", "homeowner-claim-appraiser", "wind-tornado-claim-appraisal", "carrier-estimate-review"],
        "card": "Postwar ranches to new master-planned subdivisions on the eastern metro edge.",
        "h1": "Insurance Appraiser in Aurora",
        "title": "Insurance Appraiser Aurora, CO | Hail & Storm",
        "desc": "Insurance appraiser in Aurora, Colorado: independent appraisal for hail, wind and water claims on homes, townhomes and HOA communities.",
        "lede": "Aurora stretches across three counties and decades of construction. Storms crossing the eastern metro hit everything from 1950s ranch houses to brand-new townhome communities.",
        "body": """
<h2>A big city on the storm track</h2>
<p>Aurora is Colorado’s third-largest city, spread across Arapahoe, Adams and Douglas counties. Its eastern edge opens onto the plains, where summer thunderstorms often strengthen as they leave the foothills behind. Large hail and damaging straight-line winds are regular events, and the eastern plains occasionally produce tornado warnings close to town.</p>
<h2>Housing across the decades</h2>
<ul>
<li><strong>Original Aurora and Hoffman Heights</strong> — postwar brick and frame ranches, many with original or once-replaced roofs and older plumbing.</li>
<li><strong>1970s–1990s neighborhoods</strong> such as Mission Viejo and Heather Gardens, including a large share of attached and age-restricted housing.</li>
<li><strong>Master-planned communities</strong> — Southlands, Saddle Rock, Tallyn’s Reach and Murphy Creek, with HOA design rules that can affect how repairs must be done.</li>
<li><strong>Townhome and condo communities</strong> where the association’s master policy and owners’ HO-6 policies split responsibility.</li>
</ul>
<h2>Common Aurora disputes</h2>
<p>Partial roof or siding replacements that leave a home out of step with HOA appearance standards, gutters and fascia omitted from hail scopes, and community-wide hail claims where a carrier samples a few buildings and applies the findings to the rest.</p>
""",
        "faqs": [
            ("Do HOA rules affect how my roof must be repaired?", "They can. Covenants may require specific colors or materials. When those rules affect matching or cost, document them and share them with the adjuster."),
            ("Our townhome community was hit by hail. Who files?", "Usually the association files under its master policy for the parts it insures, and owners file under HO-6 policies for unit items. Governing documents decide the split."),
        ],
    },
    {
        "slug": "fort-collins", "city": "Fort Collins", "county": "Larimer County", "region": "Front Range", "photo": "fortcollins",
        "perils": ["Hail", "Wildfire smoke", "Flash flooding", "Wind", "Frozen pipes"],
        "near": ["greeley", "longmont", "boulder"],
        "services": ["hail-roof-damage-appraisal", "fire-smoke-loss-appraisal", "water-pipe-burst-appraisal", "homeowner-claim-appraiser", "carrier-estimate-review"],
        "card": "Old Town homes, CSU rentals and foothill exposure to fire and flood.",
        "h1": "Insurance Appraiser in Fort Collins",
        "title": "Fort Collins Insurance Appraiser | Larimer County",
        "desc": "Fort Collins insurance appraiser for Larimer County homes, rentals and businesses: appraisal for hail, smoke, water and wind claims.",
        "lede": "Fort Collins combines a historic downtown, a large university rental market and foothills to the west that bring wildfire smoke and flash-flood risk. We know how those claims differ.",
        "body": """
<h2>Fire, flood and hail in one city</h2>
<p>Fort Collins residents still talk about the July 1997 Spring Creek flood, when extreme rainfall sent water through neighborhoods and the Colorado State University campus. In 2020, the Cameron Peak Fire — the largest wildfire in state history — burned in the mountains to the west, filling the city with smoke and ash for weeks. And like the rest of the northern Front Range, the city sees regular summer hail.</p>
<h2>Local housing</h2>
<ul>
<li><strong>Old Town and Laurel School</strong> — historic homes with plaster, original trim and older roofs.</li>
<li><strong>Rental housing around CSU</strong> — landlord policies, tenant contents, and loss-of-rent questions.</li>
<li><strong>Midtown and south Fort Collins</strong> — 1970s–1990s homes and newer subdivisions along the Harmony corridor and in Rigden Farm.</li>
<li><strong>Foothills properties</strong> west of Overland Trail and up toward Horsetooth Reservoir, with wildfire exposure and steep sites.</li>
</ul>
<h2>Disputes we see</h2>
<p>Smoke and ash cleaning scopes that skip attics and HVAC systems, hail estimates on older roofs where the carrier argues prior damage, and water losses in finished basements where the drying and rebuild scope was cut back.</p>
""",
        "faqs": [
            ("Was smoke from a distant fire a covered loss?", "Smoke damage can be covered even when the fire wasn’t on your property. Policies and facts vary, so document odor, soot and cleaning costs and ask the insurer in writing."),
            ("I own a rental near campus. Can I recover lost rent?", "Many landlord policies include fair rental value or loss-of-rents coverage. That amount can be part of a disputed claim if the policy provides it."),
        ],
    },
    {
        "slug": "boulder", "city": "Boulder", "county": "Boulder County", "region": "Front Range", "photo": "boulder",
        "perils": ["Downslope windstorms", "Wildfire", "Flash flooding", "Hail", "Heavy snow"],
        "near": ["longmont", "lakewood", "denver"],
        "services": ["wildfire-claim-appraisal", "wind-tornado-claim-appraisal", "fire-smoke-loss-appraisal", "water-pipe-burst-appraisal", "homeowner-claim-appraiser"],
        "card": "Windstorms off the Flatirons, the 2013 floods and Marshall Fire lessons.",
        "h1": "Insurance Appraiser in Boulder",
        "title": "Boulder Insurance Appraiser | Wind & Wildfire",
        "desc": "Boulder insurance appraiser for Boulder County homes: wildfire, smoke and downslope windstorm claim appraisal, plus estimate reviews.",
        "lede": "Boulder sits right against the foothills, which brings some of the strongest downslope winds in the country, flash-flood canyons and wildfire risk. The Marshall Fire made those risks real for thousands of families nearby.",
        "body": """
<h2>Boulder’s distinct risks</h2>
<p>Downslope windstorms are a Boulder signature. Winter and early-spring winds off the Flatirons can gust well above hurricane force, tearing shingles, toppling trees and damaging fences. On December 30, 2021, those winds pushed the Marshall Fire through Louisville, Superior and unincorporated Boulder County, destroying more than a thousand homes in a matter of hours.</p>
<p>Water is the other big story. The September 2013 floods sent water out of Boulder Canyon, Fourmile Canyon and the creeks that cross the city, damaging homes from Table Mesa to North Boulder and devastating mountain towns like Jamestown and Lyons.</p>
<h2>Housing in Boulder</h2>
<ul>
<li><strong>Mapleton Hill, Whittier and Chautauqua</strong> — historic homes with high-end finishes and design-review requirements.</li>
<li><strong>Table Mesa, Martin Acres and Newlands</strong> — midcentury homes, many remodeled.</li>
<li><strong>Gunbarrel and North Boulder</strong> — townhomes and newer construction.</li>
<li><strong>Foothills and mountain properties</strong> west of town with steep access and wildfire exposure.</li>
</ul>
<h2>What we focus on</h2>
<p>High-end finish pricing that generic estimates undervalue, wind-creased shingles that look fine from the ground, smoke and ash in homes that survived nearby fires, and rebuild costs that reflect Boulder County’s labor market and building requirements.</p>
""",
        "faqs": [
            ("Is flood damage from a creek covered by my homeowners policy?", "Usually not. Surface flooding typically requires separate flood insurance. Damage from wind-driven rain through a damaged roof is a different matter."),
            ("Do Boulder building rules increase repair costs?", "They can. Energy-code and design-review requirements may add cost, and ordinance-or-law coverage may apply to code-driven upgrades."),
        ],
    },
    {
        "slug": "lakewood", "city": "Lakewood", "county": "Jefferson County", "region": "Front Range", "photo": "lakewood",
        "perils": ["Large hail", "Wind", "Heavy snow", "Wildfire near foothills", "Burst pipes"],
        "near": ["denver", "boulder", "castle-rock"],
        "services": ["hail-roof-damage-appraisal", "commercial-hoa-appraisal", "homeowner-claim-appraiser", "snow-load-ice-dam-appraisal", "carrier-estimate-review"],
        "card": "West-metro ranches and split-levels hit hard by the May 2017 hailstorm.",
        "h1": "Insurance Appraiser in Lakewood",
        "title": "Insurance Appraiser Lakewood, CO | Jefferson Co.",
        "desc": "Lakewood insurance appraiser for Jefferson County homes, condos and businesses: hail and wind claim appraisal, HOA claims and reviews.",
        "lede": "Lakewood took the brunt of one of the costliest hailstorms in Colorado history. Today its postwar neighborhoods, foothill homes and newer condos still see regular storm claims.",
        "body": """
<h2>The May 2017 hailstorm</h2>
<p>On May 8, 2017, a hailstorm crossed the west metro and hammered Lakewood, Wheat Ridge and nearby communities with stones up to several inches across. It damaged roofs, siding and cars by the tens of thousands and kept the Colorado Mills mall closed for months. The storm is widely cited as the most expensive insured event in state history.</p>
<p>Many homes here have had at least one roof replacement since, and some have been hit again. That history matters when a carrier argues that damage pre-dates the latest storm.</p>
<h2>Housing in Lakewood</h2>
<ul>
<li><strong>Postwar neighborhoods</strong> such as Eiber, Lakewood Park and Morse Park — brick ranches and split-levels.</li>
<li><strong>Green Mountain and Bear Creek</strong> — 1970s–1980s homes on the hillsides, often with steeper roofs and views that mean more exposure to wind.</li>
<li><strong>Belmar and the West Colfax corridor</strong> — newer condos, townhomes and mixed-use buildings with HOA master policies.</li>
<li><strong>Foothill edges</strong> near Red Rocks and Dinosaur Ridge, with wildfire and wind exposure.</li>
</ul>
<h2>What we focus on</h2>
<p>Separating new hail from prior damage, matching brick and siding on older homes, community-wide HOA claims, and snow-load or ice-dam losses on hillside homes after heavy spring storms.</p>
""",
        "faqs": [
            ("My roof was replaced after the 2017 storm and got hit again. Is that a problem?", "It shouldn’t be, but documentation matters. Keep records of the earlier replacement — invoices, permits and photos — so the new damage can be tied to the new storm."),
            ("Can commercial property owners in Lakewood use appraisal?", "Yes. Most commercial property policies have an appraisal clause similar to homeowners policies."),
        ],
    },
    {
        "slug": "pueblo", "city": "Pueblo", "county": "Pueblo County", "region": "Southern Colorado", "photo": "pueblo",
        "perils": ["Hail", "Wind", "Grass fires", "Flash flooding", "Freeze"],
        "near": ["colorado-springs", "castle-rock", "durango"],
        "services": ["hail-roof-damage-appraisal", "wind-tornado-claim-appraisal", "homeowner-claim-appraiser", "fire-smoke-loss-appraisal", "carrier-estimate-review"],
        "card": "Historic brick homes, steel-era neighborhoods and Pueblo West acreage.",
        "h1": "Insurance Appraiser in Pueblo",
        "title": "Pueblo Insurance Appraiser | Hail & Wind Claims",
        "desc": "Pueblo insurance appraiser for Pueblo County homes and businesses: hail and wind claim appraisal, historic-home repairs and reviews.",
        "lede": "Pueblo’s historic brick neighborhoods, steel-era homes and the acreage lots of Pueblo West face hail, strong wind and grass-fire risk. We value disputed claims across the county.",
        "body": """
<h2>Southern Colorado weather</h2>
<p>Pueblo sits in a broad river valley at a lower elevation than Denver, with a warmer, drier climate. Summer thunderstorms bring hail and strong outflow winds, spring winds can be relentless, and dry grassland around Pueblo West and the county’s rural areas carries grass-fire risk. Flash flooding along arroyos is another hazard during summer monsoon storms.</p>
<h2>Housing in Pueblo</h2>
<ul>
<li><strong>Historic districts</strong> — the Union Avenue district, Mesa Junction and the North Side hold Victorian and early-1900s brick homes with ornate details.</li>
<li><strong>Bessemer and the East Side</strong> — modest steel-era homes near the old mill, many with older roofing and plumbing.</li>
<li><strong>Belmont and Sunset Park</strong> — midcentury and later suburban homes.</li>
<li><strong>Pueblo West</strong> — ranch homes on large lots, often with outbuildings, fences and long driveways that broaden a claim.</li>
</ul>
<h2>Common disputes</h2>
<p>Repairs to historic brick, wood trim and slate or specialty roofing priced as modern materials; outbuildings and fencing left off wind claims; and hail claims where the carrier credits only the roof and skips siding, screens and soft metals.</p>
""",
        "faqs": [
            ("Are outbuildings covered under my homeowners policy?", "Detached structures are usually covered under “other structures,” often at a percentage of the dwelling limit. That limit can be part of a dispute if the damage is extensive."),
            ("Can older brick homes be repaired to match?", "Often, but matching brick and mortar takes care and cost. When matching isn’t possible, the scope may need to extend beyond the damaged area."),
        ],
    },
    {
        "slug": "greeley", "city": "Greeley", "county": "Weld County", "region": "Eastern Plains & Northern Front Range", "photo": "plains",
        "perils": ["Large hail", "Tornadoes", "Straight-line wind", "Ag building damage", "Blizzards"],
        "near": ["fort-collins", "longmont", "aurora"],
        "services": ["hail-roof-damage-appraisal", "wind-tornado-claim-appraisal", "commercial-hoa-appraisal", "homeowner-claim-appraiser", "carrier-estimate-review"],
        "card": "Plains storms, the Windsor tornado and farm properties under one policy.",
        "h1": "Insurance Appraiser in Greeley",
        "title": "Greeley Insurance Appraiser | Weld County Storms",
        "desc": "Greeley insurance appraiser for Weld County homes, farms and businesses: hail, tornado and wind claim appraisal plus carrier estimate reviews.",
        "lede": "Greeley sits where the Front Range meets the plains, and Weld County gets the storms that come with it — big hail, damaging wind and the occasional tornado.",
        "body": """
<h2>Plains storms</h2>
<p>Weld County is one of Colorado’s most storm-exposed areas. Summer supercells routinely produce large hail across the county, and tornadoes are more common here than almost anywhere else in the state. On May 22, 2008, an EF3 tornado tracked through Windsor, just west of Greeley, damaging hundreds of homes along its path. Winter brings ground blizzards that drift snow against buildings across open country.</p>
<h2>Housing and property types</h2>
<ul>
<li><strong>Central Greeley and the University District</strong> near UNC — early-1900s homes, bungalows and student rentals.</li>
<li><strong>West Greeley</strong> — newer subdivisions and HOA communities, many built in the last twenty years.</li>
<li><strong>Rural Weld County</strong> — farmhouses with barns, machine sheds, grain bins and fencing, sometimes under farm or ranch policies.</li>
<li><strong>Commercial and industrial</strong> — food processing, agriculture and energy-related buildings with large metal roofs.</li>
</ul>
<h2>Where claims go short</h2>
<p>Metal roofs and siding on outbuildings written off as cosmetic, tornado and wind claims that miss structural damage, and farm properties where coverage for each building sits in a different part of the policy.</p>
""",
        "faqs": [
            ("Is my barn covered under a homeowners policy?", "It depends. Barns and farm buildings may be covered as other structures, scheduled separately, or need a farm or ranch policy. Read the declarations to see what’s listed."),
            ("Does appraisal work for farm and ranch policies?", "Many farm and ranch policies include an appraisal clause. The process is similar, though values and coverage parts differ."),
        ],
    },
    {
        "slug": "longmont", "city": "Longmont", "county": "Boulder & Weld Counties", "region": "Front Range", "photo": "longmont",
        "perils": ["Hail", "Flooding along the St. Vrain", "Wind", "Wildfire smoke", "Frozen pipes"],
        "near": ["boulder", "fort-collins", "greeley"],
        "services": ["hail-roof-damage-appraisal", "water-pipe-burst-appraisal", "homeowner-claim-appraiser", "wind-tornado-claim-appraisal", "carrier-estimate-review"],
        "card": "A historic core, new-urbanist neighborhoods and 2013 flood lessons.",
        "h1": "Insurance Appraiser in Longmont",
        "title": "Longmont Insurance Appraiser | Hail & Water Claims",
        "desc": "Longmont insurance appraiser for homes and businesses in Boulder and Weld counties: hail, wind and water claim appraisal plus estimate reviews.",
        "lede": "Longmont mixes a historic downtown with fast-growing neighborhoods to the east and south. Hail, wind and memories of the 2013 St. Vrain flood shape local claims.",
        "body": """
<h2>Storms and the St. Vrain</h2>
<p>In September 2013, days of extreme rain sent the St. Vrain River out of its banks and through Longmont, cutting the city in half and damaging homes and infrastructure along the river corridor. The city has invested heavily in flood control since, but water remains part of the local claim picture, alongside regular summer hail and wind off the foothills.</p>
<h2>Housing in Longmont</h2>
<ul>
<li><strong>Historic Eastside and Old Town</strong> — 1880s–1930s homes with original features.</li>
<li><strong>Prospect New Town</strong> — a new-urbanist neighborhood with bold colors, varied rooflines and design standards that make matching important.</li>
<li><strong>Southmoor Park, Sunset and Clover Basin</strong> — midcentury to 2000s suburban homes.</li>
<li><strong>East and Weld County side</strong> — newer subdivisions and HOA communities.</li>
</ul>
<h2>What we focus on</h2>
<p>Matching unusual siding colors and roof profiles, hail scopes that skip soft metals and paint, basement water losses, and HOA claims across newer communities.</p>
""",
        "faqs": [
            ("Was the 2013 flood covered by homeowners insurance?", "River flooding is generally excluded from homeowners policies and covered by separate flood insurance. Policies and facts vary, so check your coverage."),
            ("Does Prospect’s design code affect repairs?", "Neighborhood design standards can limit material choices. Share those requirements with the adjuster when they affect matching or cost."),
        ],
    },
    {
        "slug": "castle-rock", "city": "Castle Rock", "county": "Douglas County", "region": "Front Range / Palmer Divide", "photo": "castlerock",
        "perils": ["Large hail", "Heavy snow", "Wind", "Wildfire", "Ice dams"],
        "near": ["colorado-springs", "aurora", "lakewood"],
        "services": ["hail-roof-damage-appraisal", "snow-load-ice-dam-appraisal", "homeowner-claim-appraiser", "commercial-hoa-appraisal", "wildfire-claim-appraisal"],
        "card": "Palmer Divide hail and snow on larger, newer Douglas County homes.",
        "h1": "Insurance Appraiser in Castle Rock",
        "title": "Castle Rock Insurance Appraiser | Douglas County",
        "desc": "Castle Rock insurance appraiser for Douglas County homes: hail, snow-load and wind claim appraisal for larger homes and HOA communities.",
        "lede": "Castle Rock sits high on the Palmer Divide between Denver and Colorado Springs. That elevation brings heavier snow and frequent hail to some of the state’s larger, newer homes.",
        "body": """
<h2>Weather on the Palmer Divide</h2>
<p>The Palmer Divide is a ridge of higher ground running east from the foothills between the Denver and Colorado Springs metros. At over 6,000 feet, Castle Rock often gets more snow than either city, and summer storms that form over the divide frequently drop hail on Douglas County neighborhoods. Wooded areas around town and toward Larkspur and Sedalia add wildfire exposure.</p>
<h2>Housing in Castle Rock</h2>
<ul>
<li><strong>Master-planned communities</strong> — The Meadows, Crystal Valley Ranch, Castlewood Ranch and Terrain, with HOA design standards and large homes.</li>
<li><strong>Complex rooflines</strong> — multiple hips, valleys and dormers that drive up waste factors and labor.</li>
<li><strong>Premium materials</strong> — concrete tile, designer laminated shingles, stone veneer and stucco.</li>
<li><strong>Older downtown homes</strong> near the historic town center.</li>
</ul>
<h2>Where estimates fall short</h2>
<p>Waste factors and steep charges underestimated on cut-up roofs, tile and designer shingles priced as standard materials, stucco and stone repairs that can’t be matched, and ice-dam and snow-load losses after heavy spring storms.</p>
""",
        "faqs": [
            ("My roof has many facets. Does that change the estimate?", "Yes. Complex roofs need higher waste factors and more labor for hips, valleys and flashing. Try our roof pitch and squares calculator to see the difference."),
            ("Can concrete tile be repaired after hail?", "Sometimes, if matching tiles are available and the underlayment is sound. Broken tiles often reveal underlayment damage that needs attention too."),
        ],
    },
    {
        "slug": "grand-junction", "city": "Grand Junction", "county": "Mesa County", "region": "Western Slope", "photo": "gj",
        "perils": ["Canyon wind", "Wildfire", "Hail", "Flash flooding", "Freeze"],
        "near": ["durango", "boulder", "pueblo"],
        "services": ["wind-tornado-claim-appraisal", "wildfire-claim-appraisal", "hail-roof-damage-appraisal", "homeowner-claim-appraiser", "carrier-estimate-review"],
        "card": "High-desert wind, mesa wildfires and orchard country on the Western Slope.",
        "h1": "Insurance Appraiser in Grand Junction",
        "title": "Grand Junction Insurance Appraiser | Mesa County",
        "desc": "Grand Junction insurance appraiser for Mesa County homes and businesses: wind, wildfire and hail claim appraisal on the Western Slope.",
        "lede": "Grand Junction is the hub of the Western Slope, where high-desert wind, mesa wildfires and summer storms meet. Repairs here often depend on contractors and materials traveling over the mountains.",
        "body": """
<h2>Western Slope risks</h2>
<p>Grand Junction’s weather is drier and more desert-like than the Front Range, but it has its own hazards. Strong winds funnel through the Grand Valley, wildfire threatens the surrounding mesas and canyons — the 2020 Pine Gulch Fire north of town burned more than 139,000 acres — and summer monsoon storms bring hail, lightning and flash floods to dry washes.</p>
<h2>Housing in the Grand Valley</h2>
<ul>
<li><strong>Downtown and the North Avenue corridor</strong> — early-1900s homes and midcentury ranches.</li>
<li><strong>The Redlands</strong> — larger homes near the Colorado National Monument, with wildfire and wind exposure.</li>
<li><strong>Orchard Mesa, Fruitvale and Clifton</strong> — mixed older and newer homes, manufactured housing and small acreages.</li>
<li><strong>Palisade and orchard country</strong> to the east, where farm buildings share policies with homes.</li>
</ul>
<h2>Why Western Slope estimates run short</h2>
<p>Fewer local contractors, material delivery from the Front Range and travel time for specialty trades all add cost. Estimates priced from metro data, or that don’t account for longer timelines, often fall short of real local bids.</p>
""",
        "faqs": [
            ("Do repair costs differ on the Western Slope?", "They can. Contractor availability, travel and material delivery affect pricing. A good estimate reflects actual Grand Valley costs."),
            ("Is manufactured housing eligible for appraisal?", "If the policy covering it has an appraisal clause, yes. Many manufactured-home policies do."),
        ],
    },
    {
        "slug": "durango", "city": "Durango", "county": "La Plata County", "region": "Southwest Colorado", "photo": "durango",
        "perils": ["Wildfire", "Heavy snow", "Frozen pipes", "Post-fire flooding", "Hail"],
        "near": ["grand-junction", "pueblo", "colorado-springs"],
        "services": ["wildfire-claim-appraisal", "snow-load-ice-dam-appraisal", "water-pipe-burst-appraisal", "fire-smoke-loss-appraisal", "homeowner-claim-appraiser"],
        "card": "Mountain-town wildfire, snow load and second homes in La Plata County.",
        "h1": "Insurance Appraiser in Durango",
        "title": "Durango Insurance Appraiser | La Plata County",
        "desc": "Durango insurance appraiser for La Plata County homes and cabins: wildfire, smoke, snow-load and frozen-pipe claim appraisal and reviews.",
        "lede": "Durango’s forested hillsides, historic downtown and mountain homes face wildfire, deep snow and freeze. Remote sites and a small contractor pool make accurate pricing essential.",
        "body": """
<h2>Mountain-town risks</h2>
<p>In June 2018, the 416 Fire burned more than 54,000 acres in the San Juan National Forest north of Durango, forcing evacuations along the Animas Valley and sending smoke through town. The burn scar then produced debris flows during summer rains. Winters bring heavy snow at higher elevations and cold snaps that freeze pipes in second homes and cabins.</p>
<h2>Housing in and around Durango</h2>
<ul>
<li><strong>Downtown historic district</strong> — Victorian-era homes and commercial buildings along Main Avenue and the East Third Avenue historic district.</li>
<li><strong>Crestview, Riverview and Three Springs</strong> — older and newer neighborhoods, with a mix of homes and townhomes.</li>
<li><strong>Animas Valley and Edgemont Highlands</strong> — larger homes on forested lots in the wildland-urban interface.</li>
<li><strong>Cabins and second homes</strong> in the surrounding mountains, often vacant for weeks at a time.</li>
</ul>
<h2>What we focus on</h2>
<p>Smoke and ash cleaning after nearby fires, rebuild costs that reflect remote access and short building seasons, snow-load and ice-dam damage, and frozen-pipe losses in seasonal homes.</p>
""",
        "faqs": [
            ("My cabin’s pipes froze while it was empty. Will that be covered?", "It depends on the policy’s freezing and vacancy terms, such as whether heat was maintained or water was shut off. If coverage is accepted, appraisal can resolve the repair cost."),
            ("Are debris flows after a wildfire covered?", "Mudflow and flooding are often excluded from homeowners policies, even after a fire. Flood insurance may respond. Policies vary, so read the exclusions carefully."),
        ],
    },
]
