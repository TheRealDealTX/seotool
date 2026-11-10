"""Wyoming location pages. Local detail is specific to each town."""

LOCATIONS = [
    {
        "slug": "cheyenne", "city": "Cheyenne", "county": "Laramie County", "region": "Southeast Wyoming",
        "perils": ["Large hail", "Downslope wind", "Tornadoes", "Flash flooding", "Frozen pipes"],
        "near": ["laramie", "casper", "rawlins"],
        "housing": "1900s brick homes in the Avenues, post-war ranches, newer east-side subdivisions",
        "lede": "Wyoming’s capital sits on the open high plains where Front Range storms come out of the mountains with hail and wind. More of our roof and siding work happens here than anywhere else in the state.",
        "body": """
<h2>A hail city by geography</h2>
<p>Cheyenne sits at about 6,000 feet on the plains east of the Laramie Range, at the northern end of the hail corridor that runs along the Front Range. Afternoon storms build over the mountains and cross Laramie County quickly, often with hail driven on a strong west wind. Many Cheyenne homeowners can name more than one roof they’ve replaced.</p>
<p>The city has history with severe weather. On July 16, 1979, a tornado tore through north Cheyenne and the area around the airport, damaging hundreds of homes and businesses — still counted among the most destructive tornadoes in Wyoming. On August 1, 1985, a stalled thunderstorm dropped heavy rain and hail on the city in a few hours; the flash flood that followed killed twelve people and left hail piled in drifts.</p>
<h2>Housing and claim patterns</h2>
<p>Cheyenne’s housing mix runs from early-1900s brick homes around the Avenues and the Rainsford Historic District, to post-war and 1970s ranches in neighborhoods like Sun Valley and Western Hills, to newer subdivisions on the east and north sides and acreage homes in the ranchettes. Each brings its own disputes: older homes with discontinued siding and plaster interiors; mid-century ranches with layered roofs; newer homes with matching problems on stucco, stone veneer or composite siding.</p>
<h2>What we see most in Laramie County</h2>
<ul>
<li>Hail claims approved on west and north slopes only, with the siding and windows on the same elevations missed.</li>
<li>Repeated hail claims where the carrier attributes damage to an earlier storm.</li>
<li>Wind-creased shingles written off as age.</li>
<li>Winter pipe bursts in older homes with exterior-wall plumbing.</li>
<li>Commercial and multifamily roofs along the Dell Range and I-80 corridors.</li>
</ul>
""",
        "faqs": [
            ("How often does Cheyenne get damaging hail?", "Laramie County has one of the highest hail frequencies in the United States, and damaging storms affect parts of the Cheyenne area most summers. Any single property may go several years between losses, or see two in a row."),
            ("Does a prior hail claim on my house hurt a new one?", "It can complicate it. Carriers sometimes argue damage is from an earlier storm. Photos after each repair and dated weather records help separate events."),
        ],
    },
    {
        "slug": "casper", "city": "Casper", "county": "Natrona County", "region": "Central Wyoming",
        "perils": ["Winter windstorms", "Hail", "Heavy snow", "Frozen pipes", "Grass fire"],
        "near": ["riverton", "gillette", "cheyenne"],
        "housing": "oil-boom ranches and split-levels, historic downtown buildings, Casper Mountain cabins",
        "lede": "Casper sits on the North Platte under Casper Mountain, in a wind corridor that rarely rests. Its claims run from mountain cabins to oil-boom subdivisions and a historic downtown.",
        "body": """
<h2>Wind, snow and the North Platte</h2>
<p>Casper is Wyoming’s second-largest city and the hub of Natrona County. Westerly winds funnel through the area for much of the year, and winter windstorms are as likely to damage a roof as a summer thunderstorm. Casper Mountain, just south of town, collects heavy snow, and the cabins and homes up there deal with snow load and frozen-pipe losses that town homes don’t.</p>
<h2>Housing built in waves</h2>
<p>Much of Casper was built during oil and gas booms: 1950s–1980s ranches, split-levels and bi-levels across the east and west sides, newer homes in subdivisions toward Paradise Valley and the edges of town, and neighboring communities like Mills, Evansville and Bar Nunn. Downtown’s Old Yellowstone District has brick commercial buildings with their own matching and code issues. Boom-era homes often have siding, windows and shingles that are long discontinued, which drives matching disputes.</p>
<h2>Claims we see around Casper</h2>
<ul>
<li>Wind losses where siding and shingles blew off on the west elevation and a partial repair can’t match.</li>
<li>Hail claims on homes and on metal shops and outbuildings around town.</li>
<li>Frozen pipes in older homes and in vacant rentals during cold snaps.</li>
<li>Commercial buildings and warehouses serving the energy industry along the highway corridors.</li>
<li>Snow and freeze damage to Casper Mountain cabins.</li>
</ul>
""",
        "faqs": [
            ("Does the wind/hail deductible apply to a winter windstorm in Casper?", "Often yes. Many policies apply the wind/hail deductible to any windstorm. Check your declarations page for the deductible amount and how it is triggered."),
            ("My Casper Mountain cabin had a freeze loss. Is that covered?", "It depends on whether heat was maintained or the water was shut off and drained, as many policies require for unoccupied buildings. That coverage question needs to be answered before appraisal."),
        ],
    },
    {
        "slug": "laramie", "city": "Laramie", "county": "Albany County", "region": "Southeast Wyoming",
        "perils": ["High wind", "Hail", "Extreme cold", "Frozen pipes", "Wildfire smoke"],
        "near": ["cheyenne", "rawlins", "casper"],
        "housing": "historic downtown homes, university-area rentals, West Laramie and rural acreage",
        "lede": "At 7,200 feet in a wide mountain basin, Laramie gets cold, wind and summer hail — plus a large stock of older homes and student rentals that complicate claims.",
        "body": """
<h2>High, cold and windy</h2>
<p>Laramie sits in the Laramie Basin between the Laramie Range and the Snowy Range, home to the University of Wyoming. Winters are long and very cold, which makes frozen pipes a regular claim, and the wind along the I-80 corridor west of town is notorious. Summer storms bring hail off the mountains, and smoke from fires in the Medicine Bow and northern Colorado can settle in the basin for days.</p>
<h2>Older homes and rentals</h2>
<p>Laramie’s historic downtown and the neighborhoods around the university include late-1800s and early-1900s homes with brick, stone and wood details, many converted to rentals. West Laramie, the subdivisions toward the edges of town and rural acreage on the basin add newer ranches and manufactured homes. Landlords and property managers here face recurring water and hail claims, and they need estimates that account for older construction.</p>
<h2>Claims we see in Albany County</h2>
<ul>
<li>Frozen and burst pipes in older homes and vacant rentals between semesters.</li>
<li>Hail damage to roofs, siding and windows on houses and apartment buildings.</li>
<li>Wind damage to roofs and fences in exposed areas around the basin.</li>
<li>Smoke and ash cleaning claims after nearby wildfires.</li>
<li>Snow and freeze damage to cabins in the Snowy Range and around Centennial.</li>
</ul>
""",
        "faqs": [
            ("I own rentals near the university. Do you work with landlords?", "Yes. We work with individual landlords and property managers, and we coordinate access around tenants."),
            ("What about my cabin in the Snowy Range?", "We inspect mountain properties when access allows. Winter losses are documented as soon as roads open, with photos you take in the meantime."),
        ],
    },
    {
        "slug": "gillette", "city": "Gillette", "county": "Campbell County", "region": "Northeast Wyoming",
        "perils": ["Hail", "Severe thunderstorms", "Tornadoes", "Wind", "Grass fire"],
        "near": ["sheridan", "casper", "cody"],
        "housing": "energy-boom subdivisions, manufactured homes, metal shops on acreage",
        "lede": "The energy capital of the Powder River Basin sees some of Wyoming’s strongest summer thunderstorms, and its boom-era housing makes hail and wind claims especially tricky.",
        "body": """
<h2>Thunderstorm country</h2>
<p>Gillette sits on the rolling plains of the Powder River Basin, closer in weather to the Dakotas than to the mountain west. Summer brings severe thunderstorms with large hail, damaging winds and the occasional tornado. In August 2005, a tornado struck the small town of Wright in southern Campbell County, killing two people and destroying homes — a reminder that the plains here can produce violent storms.</p>
<h2>Built fast during the booms</h2>
<p>Gillette grew in surges tied to coal, oil and gas. Large parts of town were built quickly: subdivisions of ranches and bi-levels, many manufactured and modular homes, and metal shops and outbuildings on acreage around Antelope Valley and other areas outside the city limits. Boom-era materials are often discontinued, and manufactured homes and metal buildings need specialized pricing.</p>
<h2>Claims we see in Campbell County</h2>
<ul>
<li>Hail claims on manufactured homes, where roof and siding materials are hard to match.</li>
<li>Metal shops and pole barns with dented panels, damaged doors and torn trim.</li>
<li>Commercial and industrial buildings serving the energy sector.</li>
<li>Wind damage to roofs, skirting, fences and outbuildings.</li>
<li>Grass fire losses to outbuildings and fencing on acreage.</li>
</ul>
""",
        "faqs": [
            ("Can you appraise a manufactured home hail claim?", "Yes. We price manufactured home materials from manufacturer and supplier sources rather than site-built substitutes."),
            ("My metal shop has hail dents but the carrier says they’re cosmetic.", "Whether cosmetic damage to metal is covered depends on your policy. If it isn’t excluded, the cost to repair or replace dented panels is a valuation question a panel can decide."),
        ],
    },
    {
        "slug": "rock-springs", "city": "Rock Springs", "county": "Sweetwater County", "region": "Southwest Wyoming",
        "perils": ["Extreme wind", "Hail", "Winter storms", "Frozen pipes", "Flash floods"],
        "near": ["green-river", "evanston", "rawlins"],
        "housing": "historic miners’ homes, boom-era subdivisions, manufactured housing",
        "lede": "Rock Springs is a high-desert railroad and mining town on I-80 where wind is constant and winter storms close the interstate. Its housing reflects more than a century of boom and bust.",
        "body": """
<h2>Wind on the high desert</h2>
<p>Rock Springs sits at about 6,300 feet in the Green River Basin. The I-80 corridor across Sweetwater County is one of the windiest stretches of highway in the country, and winter storms bring ground blizzards that close the road for hours or days. Summer thunderstorms are fewer than on the eastern plains but can bring hail and sudden flash flooding in the draws through town.</p>
<h2>A mix of old and new</h2>
<p>Rock Springs began as a coal town on the Union Pacific line, and its older neighborhoods still include small miners’ homes and historic brick commercial buildings downtown. Trona mining, oil and gas brought later booms and the subdivisions, apartment complexes and manufactured home communities that came with them. Claims here often mix century-old construction with 1970s and 2000s materials that are no longer available.</p>
<h2>Claims we see in Sweetwater County</h2>
<ul>
<li>Wind damage to roofs and siding, especially on exposed lots on the edges of town.</li>
<li>Frozen pipes during cold snaps, including in rental and manufactured homes.</li>
<li>Hail claims on homes and commercial buildings.</li>
<li>Water losses from flash flooding and drainage — where coverage depends heavily on the source of the water.</li>
<li>Industrial and commercial building claims tied to the mining and energy economy.</li>
</ul>
""",
        "faqs": [
            ("Is flash flood damage covered by homeowners insurance?", "Surface water and flooding are usually excluded from standard homeowners policies and covered only by separate flood insurance. Water from a burst pipe or roof leak is treated differently."),
            ("Do you come to Rock Springs for inspections?", "Yes. We cover all of Sweetwater County and schedule inspections around weather and road conditions."),
        ],
    },
    {
        "slug": "sheridan", "city": "Sheridan", "county": "Sheridan County", "region": "North-Central Wyoming",
        "perils": ["Hail", "Wind", "Heavy snow", "Wildfire", "Frozen pipes"],
        "near": ["gillette", "cody", "casper"],
        "housing": "historic Main Street buildings, Victorian homes, ranches and foothill properties",
        "lede": "Sheridan lies at the foot of the Bighorn Mountains, with a historic downtown, ranching country all around and summer storms that roll off the mountains.",
        "body": """
<h2>Bighorn weather</h2>
<p>Sheridan sits along Goose Creek at the eastern base of the Bighorn Mountains. Summer thunderstorms form over the range and drift east with hail and gusty winds; winters bring snow and cold, and the foothill communities of Big Horn, Story and Dayton get more snow than town. Wildfires in the Bighorns can send smoke through the valley.</p>
<h2>Historic downtown, ranch country</h2>
<p>Sheridan’s Main Street is one of the best-preserved historic downtowns in the state, with brick buildings, decorative cornices and storefronts that require careful matching and specialized trades. Residential neighborhoods include Victorian and early-1900s homes, mid-century ranches and newer subdivisions, while the surrounding county is ranch country with homes, barns and outbuildings spread across large properties.</p>
<h2>Claims we see in Sheridan County</h2>
<ul>
<li>Hail damage to roofs, siding and windows, including on older homes with discontinued materials.</li>
<li>Commercial claims on historic downtown buildings, where matching and code upgrades drive cost.</li>
<li>Ranch claims involving barns, shops, fencing and outbuildings.</li>
<li>Snow and freeze damage in foothill homes and cabins.</li>
<li>Smoke and ash cleaning after Bighorn wildfires.</li>
</ul>
""",
        "faqs": [
            ("My building is on Sheridan’s historic Main Street. Does that change the claim?", "It can. Matching historic materials and meeting current code during repairs can raise costs. Whether ordinance-or-law coverage applies depends on your policy."),
            ("Do you handle ranch outbuildings?", "Yes. Barns, shops, sheds and fencing are documented and valued separately under the coverage that applies."),
        ],
    },
    {
        "slug": "green-river", "city": "Green River", "county": "Sweetwater County", "region": "Southwest Wyoming",
        "perils": ["Extreme wind", "Winter storms", "Hail", "Frozen pipes", "River flooding"],
        "near": ["rock-springs", "evanston", "rawlins"],
        "housing": "trona-boom subdivisions, older homes near the river, manufactured housing",
        "lede": "Green River sits under its sandstone bluffs on the river of the same name, the county seat of Sweetwater County and the heart of Wyoming’s trona country.",
        "body": """
<h2>River town, wind country</h2>
<p>Green River lies along the Green River where Interstate 80 and the Union Pacific line cross it, beneath distinctive sandstone formations like Castle Rock. Like Rock Springs fifteen miles east, it lives with constant wind and winter storms that can close I-80. The river corridor and Expedition Island park are lovely in summer; spring runoff and ice jams can raise flood questions for nearby properties.</p>
<h2>Built around trona</h2>
<p>The trona mines west and north of town are among the largest in the world, and much of Green River’s housing was built to house mine workers during growth periods from the 1960s onward: ranches, split-levels and bi-levels, apartment complexes and manufactured home communities, alongside older homes near downtown and the river.</p>
<h2>Claims we see in Green River</h2>
<ul>
<li>Wind damage to roofs, siding, fences and garage doors.</li>
<li>Frozen pipes in winter, especially in homes with plumbing in exterior walls.</li>
<li>Hail claims on roofs and siding.</li>
<li>Water losses near the river, where the source of water determines coverage.</li>
<li>Commercial and industrial claims connected to the mining economy.</li>
</ul>
""",
        "faqs": [
            ("Is river flooding covered by my homeowners policy?", "Usually not. Flooding from rising water is typically excluded from standard homeowners policies and covered by separate flood insurance."),
            ("What makes wind claims in Green River hard?", "Carriers often see wind damage as long-term wear. Documenting the date, gust speeds and fresh damage helps show a specific storm event."),
        ],
    },
    {
        "slug": "evanston", "city": "Evanston", "county": "Uinta County", "region": "Southwest Wyoming",
        "perils": ["Heavy snow", "Wind", "Frozen pipes", "Ice dams", "Hail"],
        "near": ["green-river", "rock-springs", "jackson"],
        "housing": "historic railroad-era homes, 1980s boom subdivisions, rural acreage",
        "lede": "Evanston sits on the Bear River at Wyoming’s southwest corner, where higher snowfall and long winters make snow load, ice dams and frozen pipes the claims to watch.",
        "body": """
<h2>Snow and cold at the Utah line</h2>
<p>Evanston lies near the Utah border at roughly 6,700 feet, in the Bear River valley north of the Uinta Mountains. It gets more snow than much of southern Wyoming, and long cold stretches make frozen pipes and ice dams common. Wind along I-80 and summer thunderstorms with hail round out the risks. Wind farms on the ridges of Uinta County are a reminder of how steady the wind is.</p>
<h2>Railroad heritage and a 1980s boom</h2>
<p>Evanston grew as a Union Pacific railroad town, and its historic downtown and older neighborhoods include homes and buildings from that era. The Overthrust Belt oil and gas boom of the late 1970s and 1980s brought rapid growth and many subdivisions, apartments and manufactured homes built in a short time. Rural properties along the Bear River and toward Almy add ranch homes and outbuildings.</p>
<h2>Claims we see in Uinta County</h2>
<ul>
<li>Ice dam leaks into ceilings and walls during long cold spells.</li>
<li>Snow load damage to porches, carports and outbuildings.</li>
<li>Frozen and burst pipes in homes and rentals.</li>
<li>Wind and hail damage to roofs and siding.</li>
<li>Older homes with discontinued materials that complicate matching.</li>
</ul>
""",
        "faqs": [
            ("Are ice dam leaks covered?", "Many policies cover sudden water damage from ice dams, though wording varies. The extent of interior and roof repair is a valuation question once coverage is accepted."),
            ("My carport collapsed under snow. Is it covered?", "It depends on your policy’s collapse provisions, which sometimes treat structures like carports differently. That coverage question comes first."),
        ],
    },
    {
        "slug": "riverton", "city": "Riverton", "county": "Fremont County", "region": "Central Wyoming",
        "perils": ["Hail", "Wind", "Extreme cold", "Frozen pipes", "Flooding"],
        "near": ["casper", "cody", "jackson"],
        "housing": "farm and ranch homes, mid-century ranches, manufactured homes",
        "lede": "Riverton is the largest town in Fremont County, set in the Wind River Basin among irrigated farmland, with cold winters and summer storms off the Wind River Range.",
        "body": """
<h2>The Wind River Basin</h2>
<p>Riverton lies at the confluence of the Wind River and Little Wind River, surrounded by irrigated farms and ranches. The Wind River Range to the west and the basin’s low elevation shape its weather: hot summers with thunderstorms and hail, and cold winters where temperature inversions trap frigid air for days. The Wind River Indian Reservation borders the town, and communities like Hudson, Pavillion and Shoshoni are nearby.</p>
<h2>Farm country housing</h2>
<p>Riverton’s housing includes mid-century ranches, newer subdivisions, manufactured homes and farm and ranch properties with barns, shops and grain storage. Rural properties often have multiple outbuildings, and farm structures need their own valuation.</p>
<h2>Claims we see around Riverton</h2>
<ul>
<li>Hail damage to homes, outbuildings and metal farm buildings.</li>
<li>Wind damage to roofs, siding and fences.</li>
<li>Frozen pipes during long cold inversions.</li>
<li>Water losses where coverage depends on the water source.</li>
<li>Farm and ranch structures with mixed residential and agricultural coverage.</li>
</ul>
""",
        "faqs": [
            ("Do you handle farm buildings?", "Yes. We appraise barns, shops and other farm structures under the coverage that applies, whether a homeowners, farm or commercial policy."),
            ("Do you work in Lander and Dubois too?", "Yes. We cover all of Fremont County, including Lander, Dubois, Shoshoni and the surrounding communities."),
        ],
    },
    {
        "slug": "jackson", "city": "Jackson", "county": "Teton County", "region": "Northwest Wyoming",
        "perils": ["Heavy snow load", "Ice dams", "Wildfire", "Frozen pipes", "Avalanche & slide"],
        "near": ["evanston", "cody", "riverton"],
        "housing": "custom log and timber-frame homes, condos and townhomes, historic cabins",
        "lede": "Jackson Hole has some of the highest-value homes in the country and some of the heaviest snow loads in the lower 48. Claims here are large, technical and expensive to rebuild.",
        "body": """
<h2>Snow, cold and high stakes</h2>
<p>Jackson sits at the south end of Jackson Hole, beneath the Teton Range and near Grand Teton and Yellowstone national parks. Deep winter snow is a defining feature: design snow loads in Teton County are among the highest in the lower 48, and roofs, decks and porches carry enormous weight in a big year. Ice dams, frozen pipes in second homes, and wildfire risk in the surrounding forest add to the picture. In March 2017 a porch roof at a Grand Teton National Park visitor center gave way under snow.</p>
<h2>Expensive, custom construction</h2>
<p>Teton County has the highest home values in Wyoming. Many homes in Jackson, Wilson, Teton Village and the surrounding valley are custom log or timber-frame houses with complex roofs, stone, specialty windows and high-end finishes. Condominiums and townhomes in town and at the resort add association master policies to the mix. Construction costs are far higher than elsewhere in the state, and labor availability is limited.</p>
<h2>Claims we see in Teton County</h2>
<ul>
<li>Snow load damage to roofs, decks and structural framing.</li>
<li>Ice dam leaks into high-end interiors.</li>
<li>Frozen pipe losses in second homes left unattended.</li>
<li>Condo and HOA claims split between master and unit-owner policies.</li>
<li>Estimates that use statewide pricing instead of Teton County labor and material costs.</li>
</ul>
""",
        "faqs": [
            ("Why do Jackson claims need local pricing?", "Labor, lodging and material costs in Teton County are much higher than the rest of Wyoming. Estimates built on statewide averages can fall well short."),
            ("My second home had a frozen pipe while I was away. Is it covered?", "It may be, depending on whether heat was maintained or the water was shut off and drained as many policies require. That question should be settled before appraisal."),
        ],
    },
    {
        "slug": "cody", "city": "Cody", "county": "Park County", "region": "Northwest Wyoming",
        "perils": ["Downslope wind", "Hail", "Wildfire", "Heavy snow", "Frozen pipes"],
        "near": ["sheridan", "jackson", "riverton"],
        "housing": "historic downtown, ranches and acreage homes, cabins toward Yellowstone",
        "lede": "Cody sits in the Bighorn Basin at the gateway to Yellowstone’s east entrance, with powerful winds off the Absarokas, summer hail and cabins in fire country.",
        "body": """
<h2>Gateway weather</h2>
<p>Cody lies along the Shoshone River at the western edge of the Bighorn Basin, about fifty miles from Yellowstone’s east entrance. Strong downslope winds off the Absaroka Range can gust to damaging speeds, particularly in winter, and summer storms bring hail across the basin. Up the North Fork and South Fork valleys toward Yellowstone, cabins and lodges face heavy snow and wildfire risk.</p>
<h2>Western town, rural properties</h2>
<p>Cody’s historic downtown and older neighborhoods include early-1900s buildings and homes, while newer subdivisions, ranches and acreage homes spread across the surrounding benches. Nearby Powell adds farm country housing. Many properties include shops, barns and guest cabins.</p>
<h2>Claims we see in Park County</h2>
<ul>
<li>Wind damage to roofs, siding and outbuildings during downslope wind events.</li>
<li>Hail claims on homes and farm buildings in the Bighorn Basin.</li>
<li>Wildfire and smoke damage to cabins and lodges in the forest valleys.</li>
<li>Snow load and frozen pipe damage to seasonal properties.</li>
<li>Commercial claims on tourism businesses where timing matters.</li>
</ul>
""",
        "faqs": [
            ("My guest cabin and lodge depend on summer business. Can appraisal move quickly?", "Panels can move fast when both sides cooperate and the documentation is ready. We prioritize getting your file complete early."),
            ("Do you cover Powell and Meeteetse?", "Yes. We work throughout Park County and the Bighorn Basin."),
        ],
    },
    {
        "slug": "rawlins", "city": "Rawlins", "county": "Carbon County", "region": "South-Central Wyoming",
        "perils": ["Extreme wind", "Ground blizzards", "Hail", "Frozen pipes", "Wildfire"],
        "near": ["laramie", "rock-springs", "casper"],
        "housing": "historic downtown buildings, railroad-era homes, manufactured housing",
        "lede": "Rawlins sits on the Continental Divide basin along I-80, in one of the windiest regions of the country, with historic buildings and ranch country all around.",
        "body": """
<h2>The windiest stretch of I-80</h2>
<p>Rawlins is the county seat of Carbon County, on Interstate 80 between Laramie and Rock Springs. The stretch of highway around Rawlins, Elk Mountain and Arlington is famous for high winds and ground blizzards that close the road. Wind is the dominant peril here, but summer thunderstorms bring hail, and fires in the Sierra Madre and Medicine Bow ranges to the south can affect the area.</p>
<h2>Railroad history</h2>
<p>Rawlins grew as a Union Pacific town, and its downtown, the historic Ferris Mansion and the old Wyoming Frontier Prison reflect that era. Residential areas include older railroad-era homes, mid-century ranches and manufactured homes. Nearby Sinclair, Saratoga and Encampment add refinery, resort and ranch properties.</p>
<h2>Claims we see in Carbon County</h2>
<ul>
<li>Wind damage to roofs, siding, fencing and outbuildings.</li>
<li>Frozen pipes in older homes and vacant properties.</li>
<li>Hail damage to roofs and siding.</li>
<li>Wildfire and smoke claims for cabins in the southern mountains.</li>
<li>Historic building claims with matching challenges.</li>
</ul>
""",
        "faqs": [
            ("How do you prove a specific windstorm caused my damage?", "We combine fresh damage evidence with weather station data from Rawlins and nearby stations to tie damage to the date of loss."),
            ("Do you work in Saratoga and Encampment?", "Yes. We cover all of Carbon County."),
        ],
    },
]
