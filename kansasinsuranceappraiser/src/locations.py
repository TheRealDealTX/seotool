"""Kansas location pages. Local detail is specific to each city."""

LOCATIONS = [
    {
        "slug": "wichita", "city": "Wichita", "county": "Sedgwick County", "region": "South Central Kansas",
        "perils": ["Large hail", "Tornadoes", "Straight-line wind", "Ice storms", "Water losses"],
        "near": ["hutchinson", "salina", "dodge-city"],
        "housing": "Post-war ranches, 1920s bungalows, newer east-side subdivisions",
        "lede": "Kansas’s largest city sits in one of the most active hail corridors in the country. We value losses from College Hill bungalows to new construction in Bel Aire, Maize and Goddard.",
        "body": """
<h2>Hail, wind and a very large roof count</h2>
<p>Wichita and the rest of Sedgwick County see damaging hail most years, and a single storm can produce thousands of roof claims across the metro. When that happens, adjusters are stretched, estimates are rushed and roofing crews are booked for months. That combination is where many underpaid claims begin.</p>
<p>The city also carries tornado history. The April 1991 outbreak that devastated Andover also struck near McConnell Air Force Base, and the May 3, 1999 tornado tore through Haysville and south Wichita. Storms like these shape how residents think about wind and how carriers handle structural claims.</p>
<h2>Housing across the metro</h2>
<ul>
<li><strong>College Hill, Riverside and Delano:</strong> 1910s–1930s homes with plaster walls, wood windows and detailed trim that generic estimates under-price.</li>
<li><strong>Mid-century neighborhoods</strong> in south and west Wichita: brick and frame ranches, many with older roofs that raise depreciation and repairability questions.</li>
<li><strong>East and northeast growth areas</strong> near Andover, Bel Aire and Rose Hill: newer homes, HOAs and architectural shingles.</li>
<li><strong>Commercial and industrial:</strong> aviation suppliers, warehouses and retail centers with large low-slope roofs.</li>
</ul>
<h2>Common Wichita disputes</h2>
<p>Partial roof approvals after hail, siding that can’t be matched, older roofs placed on payment schedules, and commercial membrane roofs where the carrier and owner disagree on how much area is damaged. We document every slope and elevation so the panel sees the whole picture.</p>
""",
        "faqs": [
            ("Do you inspect in Haysville, Derby and Andover?", "Yes. We work throughout Sedgwick County and the surrounding communities, including Derby, Haysville, Andover, Maize, Goddard and Park City."),
            ("Why does my Wichita roof estimate differ so much from my roofer’s?", "Often because of scope, such as how many slopes are replaced, plus missing items like drip edge, steep charges or gutters. An estimate review pinpoints the differences."),
        ],
    },
    {
        "slug": "overland-park", "city": "Overland Park", "county": "Johnson County", "region": "Kansas City Metro",
        "perils": ["Hail", "Severe thunderstorms", "Water in basements", "Ice dams", "Wind"],
        "near": ["olathe", "kansas-city", "lawrence"],
        "housing": "1950s–60s ranches and split-levels north of I-435, large newer homes to the south",
        "lede": "Overland Park’s mix of mid-century neighborhoods and newer Blue Valley subdivisions means claims range from simple roof repairs to large HOA and finished-basement losses.",
        "body": """
<h2>A city of finished basements and HOAs</h2>
<p>Overland Park is Kansas’s second-largest city and the heart of Johnson County. Many homes north of 95th Street were built in the 1950s and 1960s as ranches and split-levels. South of I-435, larger homes from the 1990s onward sit in HOA communities with architectural standards for roofs and exteriors.</p>
<p>Spring storms bring hail to the metro regularly, and heavy rain finds its way into finished basements. Water losses here are often bigger than they first appear because so much living space sits below grade.</p>
<h2>What we see in Overland Park claims</h2>
<ul>
<li>HOA roof and exterior standards that require specific shingle colors or materials.</li>
<li>Finished-basement water losses with carpet, drywall, built-ins and bathrooms affected.</li>
<li>Hail damage to vinyl and fiber-cement siding, gutters, screens and fences.</li>
<li>Townhome communities where the association and owners each carry part of the coverage.</li>
<li>Higher local labor costs that statewide price lists don’t capture.</li>
</ul>
<h2>Neighborhoods we serve</h2>
<p>Downtown Overland Park, Nall Hills, Indian Creek, Corporate Woods and the Blue Valley area, plus nearby Leawood, Prairie Village and Lenexa. We schedule inspections around work hours and can meet your contractor on site.</p>
""",
        "faqs": [
            ("Does my HOA’s shingle requirement affect the claim?", "It can. If HOA rules require a specific product and that affects repair cost or matching, it should be documented. Whether the policy pays the extra cost depends on its terms."),
            ("Is a basement flood from heavy rain covered?", "Usually not under a standard policy unless you have flood coverage. Water from a sump pump failure or backup typically requires an endorsement."),
        ],
    },
    {
        "slug": "kansas-city", "city": "Kansas City", "county": "Wyandotte County", "region": "Kansas City Metro",
        "perils": ["Hail", "Wind", "Aging roofs", "Water intrusion", "Ice storms"],
        "near": ["overland-park", "olathe", "lawrence"],
        "housing": "Early 1900s brick and frame homes, mid-century ranches, new builds near Village West",
        "lede": "Kansas City, Kansas has some of the oldest housing in the state, from Strawberry Hill to Rosedale and Argentine. Older homes bring unique materials and frequent disputes over repairability.",
        "body": """
<h2>Older homes, real repair costs</h2>
<p>Wyandotte County’s neighborhoods grew around rail yards, meatpacking and river industry in the late 1800s and early 1900s. Strawberry Hill, Rosedale, Argentine and Armourdale still have many brick and frame homes from that era: multiple roof layers, plaster walls, wood siding and historic details that don’t price like modern construction.</p>
<p>In the west, Piper and the area around Village West and the Legends have seen newer subdivisions and commercial development. The May 2019 tornado that touched down near Linwood and Bonner Springs showed how quickly storms can reach the western county.</p>
<h2>Common disputes in KCK</h2>
<ul>
<li>Roofs with multiple shingle layers, where tear-off and decking costs are underestimated.</li>
<li>Older roofs pushed onto payment schedules or denied as “wear and tear.”</li>
<li>Plaster interiors priced as drywall after water losses.</li>
<li>Brick masonry and chimney repairs after wind or tree damage.</li>
<li>Commercial and industrial buildings with large, aging low-slope roofs.</li>
</ul>
<h2>Serving Wyandotte County</h2>
<p>We work across Kansas City, Kansas, Bonner Springs, Edwardsville and nearby Johnson County communities. Our estimates use pricing that reflects older-home repair methods and current metro labor rates.</p>
""",
        "faqs": [
            ("My house has two layers of shingles. Does that matter?", "Yes. Multiple layers increase tear-off, disposal and often decking costs. Current code may require removal of all layers before re-roofing."),
            ("Can appraisal help if the carrier blames wear and tear?", "If the insurer denies the damage was caused by a covered peril, that is a coverage dispute. If it accepts some damage but disputes the amount, appraisal can help."),
        ],
    },
    {
        "slug": "olathe", "city": "Olathe", "county": "Johnson County", "region": "Kansas City Metro",
        "perils": ["Hail", "Wind", "Basement water", "Ice dams", "Tornado risk"],
        "near": ["overland-park", "lawrence", "kansas-city"],
        "housing": "1990s–2020s subdivisions with HOAs, older homes near downtown",
        "lede": "Olathe has grown fast, and its subdivisions share similar roofs, siding and HOA standards. When hail crosses town, whole neighborhoods file at once and estimates follow a template.",
        "body": """
<h2>Fast growth, similar roofs</h2>
<p>As the Johnson County seat, Olathe has a historic downtown surrounded by decades of rapid suburban growth. Many neighborhoods were built by the same builders in the same years, with similar architectural shingles, vinyl or fiber-cement siding and HOA rules about color and material.</p>
<p>That uniformity cuts both ways after a hailstorm. It makes damage patterns easy to see across a street, but it also encourages template estimates that miss what is specific to your house: a different pitch, an extra gable, a deck or a fence.</p>
<h2>What we see in Olathe claims</h2>
<ul>
<li>Partial roof approvals in neighborhoods where neighbors received full replacements.</li>
<li>Discontinued shingle colors that conflict with HOA requirements.</li>
<li>Fiber-cement siding repairs that require painting full elevations.</li>
<li>Finished-basement water losses from failed sump pumps or supply lines.</li>
<li>Commercial buildings along I-35 with large flat roofs.</li>
</ul>
<h2>Neighborhoods we serve</h2>
<p>Downtown Olathe, Cedar Creek, the Black Bob area, and subdivisions along K-7 and 119th Street, plus nearby Gardner, Spring Hill and De Soto.</p>
""",
        "faqs": [
            ("My neighbor got a new roof and I didn’t. Why?", "Every claim is adjusted separately. Differences in damage, roof age and documentation can lead to different results. A review can show whether your roof was evaluated fully."),
            ("Do you work with HOA boards in Olathe?", "Yes. We help associations document community-wide damage building by building."),
        ],
    },
    {
        "slug": "topeka", "city": "Topeka", "county": "Shawnee County", "region": "Northeast Kansas",
        "perils": ["Tornadoes", "Hail", "Ice storms", "Wind", "Tree damage"],
        "near": ["lawrence", "manhattan", "kansas-city"],
        "housing": "Victorian homes in Potwin, mid-century ranches, newer west-side homes",
        "lede": "Topeka remembers the 1966 tornado that crossed Burnett’s Mound and cut through the city. Today’s claims range from Potwin Victorians to west-side ranches and state government buildings.",
        "body": """
<h2>A capital city with tornado history</h2>
<p>On June 8, 1966, a violent tornado crossed Burnett’s Mound on Topeka’s southwest side and carved a path through the city, including Washburn University and downtown. It remains one of the most damaging tornadoes in Kansas history and a reason Topeka residents take severe weather seriously.</p>
<p>Today, hail and wind cause most claims, with ice storms bringing down limbs from the mature trees that shade older neighborhoods.</p>
<h2>Topeka housing</h2>
<ul>
<li><strong>Potwin:</strong> late-1800s Victorian homes with complex roofs, wood siding and ornate trim.</li>
<li><strong>College Hill and Westboro:</strong> early 20th-century homes near Washburn with plaster interiors and mature trees.</li>
<li><strong>Central and North Topeka:</strong> modest frame and brick homes, some with older roofs.</li>
<li><strong>West Topeka and Sherwood:</strong> newer subdivisions with architectural shingles and HOAs.</li>
</ul>
<h2>Common disputes</h2>
<p>Steep, complex Victorian roofs measured incorrectly, wood siding and trim priced as vinyl, tree removal limits after ice storms and older roofs placed on payment schedules. We document and price older homes with the methods they actually require.</p>
""",
        "faqs": [
            ("Is the Kansas Insurance Department in Topeka?", "Yes. The Kansas Insurance Department is based in Topeka and offers consumer assistance for policyholders with questions or complaints about insurers."),
            ("Can appraisal handle a complex Victorian roof?", "Yes. Accurate measurement and pitch-by-pitch pricing are especially important on complex roofs."),
        ],
    },
    {
        "slug": "lawrence", "city": "Lawrence", "county": "Douglas County", "region": "Northeast Kansas",
        "perils": ["Hail", "Tornadoes", "Wind", "Water losses", "Tree damage"],
        "near": ["topeka", "olathe", "overland-park"],
        "housing": "Historic homes in Old West Lawrence, student rentals, newer west-side homes",
        "lede": "Lawrence blends historic neighborhoods, student rentals near KU and newer subdivisions to the west. The May 2019 EF4 tornado reminded the county how fast storms can arrive.",
        "body": """
<h2>Historic homes and rental properties</h2>
<p>Lawrence is home to the University of Kansas and some of the most historic neighborhoods in the state. Old West Lawrence and East Lawrence have homes from the late 1800s and early 1900s. Around the Oread neighborhood, many older houses have been converted to student rentals, which brings landlord policies and loss-of-rent questions into claims.</p>
<p>On May 28, 2019, an EF4 tornado crossed southern Douglas County near Linwood, damaging homes and farms. Hail and wind remain the most common claims in town.</p>
<h2>What we see in Lawrence claims</h2>
<ul>
<li>Historic homes with wood siding, slate or older roofs, and detailed trim.</li>
<li>Rental properties where landlord and tenant coverages overlap.</li>
<li>Apartment complexes and multifamily buildings with multiple roofs.</li>
<li>Mature trees falling on homes during storms.</li>
<li>Newer homes in west Lawrence with HOA standards.</li>
</ul>
<h2>Neighborhoods we serve</h2>
<p>Old West Lawrence, East Lawrence, Oread, Hillcrest, Prairie Park and west Lawrence, plus Eudora, Baldwin City and rural Douglas County.</p>
""",
        "faqs": [
            ("Do you handle rental property claims?", "Yes. Landlord policies often include loss of rent coverage, and we value both the building damage and help document the rental period."),
            ("Is a historic district a factor?", "It can be. If local rules require specific materials, that should be documented. Whether the extra cost is covered depends on ordinance-or-law terms."),
        ],
    },
    {
        "slug": "manhattan", "city": "Manhattan", "county": "Riley County", "region": "Flint Hills",
        "perils": ["Tornadoes", "Hail", "Wind", "Flooding", "Ice storms"],
        "near": ["topeka", "salina", "lawrence"],
        "housing": "Older homes near campus, rentals, newer west-side neighborhoods",
        "lede": "Manhattan sits at the edge of the Flint Hills and is home to Kansas State University. The June 2008 EF4 tornado struck the campus and nearby neighborhoods.",
        "body": """
<h2>The Little Apple and the Flint Hills</h2>
<p>Manhattan is a university town that spills into Pottawatomie County to the east, with Fort Riley just to the west. On June 11, 2008, an EF4 tornado struck the city and the K-State campus, damaging dozens of homes and university buildings. Flooding is a separate concern near Wildcat Creek and the rivers that meet near town, and flood losses usually require separate flood coverage.</p>
<h2>Housing in Manhattan</h2>
<ul>
<li>Older homes near campus and Aggieville, many converted to rentals.</li>
<li>Limestone buildings and homes that reflect the area’s native stone.</li>
<li>Newer subdivisions on the west side and toward Wamego.</li>
<li>Apartment complexes serving students and military families.</li>
</ul>
<h2>Common disputes</h2>
<p>Rental property claims with loss-of-rent issues, limestone masonry repairs, hail damage to apartment complexes and newer homes, and wind claims where structural damage is easy to miss. We document each property fully and value repairs with local pricing.</p>
""",
        "faqs": [
            ("Is flooding from Wildcat Creek covered?", "Surface water and rising water are usually excluded from homeowner policies. You would typically need flood insurance."),
            ("Do you serve Wamego and Junction City?", "Yes. We cover Riley, Pottawatomie, Geary and nearby counties."),
        ],
    },
    {
        "slug": "salina", "city": "Salina", "county": "Saline County", "region": "North Central Kansas",
        "perils": ["Hail", "Wind", "Tornadoes", "Ice storms", "Grass fire"],
        "near": ["manhattan", "hays", "hutchinson"],
        "housing": "Mid-century ranches, older brick homes, commercial along I-70 and I-135",
        "lede": "Salina sits at the crossroads of I-70 and I-135 in the Smoky Hills. Hail and wind are frequent, and the city’s commercial strip adds large roof claims to the mix.",
        "body": """
<h2>Crossroads of central Kansas</h2>
<p>Salina is the hub of north-central Kansas, with Kansas Wesleyan University, a large regional medical center and a busy commercial corridor along I-70 and I-135. The Smoky Hill River winds through town. Severe storms move through regularly in spring and summer, bringing hail and damaging wind.</p>
<h2>Housing and buildings</h2>
<ul>
<li>Mid-century ranches and split-levels across much of the city.</li>
<li>Older brick and frame homes near downtown.</li>
<li>Newer homes on the south and east sides.</li>
<li>Commercial buildings, warehouses and truck stops near the interstates.</li>
<li>Farmsteads and acreages in surrounding Saline County.</li>
</ul>
<h2>Common disputes</h2>
<p>Partial hail approvals, older roofs on payment schedules, commercial membrane and metal roofs, and rural outbuildings under farm policies. We price repairs with central Kansas labor and material costs.</p>
""",
        "faqs": [
            ("Do you handle commercial claims in Salina?", "Yes. We value retail, warehouse, office and agricultural commercial buildings."),
            ("Do you serve rural Saline County?", "Yes, including farmsteads and acreages throughout the county and surrounding area."),
        ],
    },
    {
        "slug": "hutchinson", "city": "Hutchinson", "county": "Reno County", "region": "South Central Kansas",
        "perils": ["Hail", "Wind", "Grass fire", "Tornadoes", "Ice storms"],
        "near": ["wichita", "salina", "dodge-city"],
        "housing": "Older frame homes, mid-century ranches, rural acreages",
        "lede": "Home of the Kansas State Fair, Hutchinson faces hail, wind and wind-driven grass fires. In March 2017, fires burned homes on the city’s northern edge.",
        "body": """
<h2>Salt City storms and fires</h2>
<p>Hutchinson is known for the Kansas State Fair, the Cosmosphere and the salt deposits beneath the city. It also sits in an area where hail and wind are common, and where dry grass and strong winds can turn a spark into a fast-moving fire. In March 2017, wind-driven fires burned homes and outbuildings near Hutchinson and across Reno County.</p>
<h2>Housing in Hutchinson</h2>
<ul>
<li>Older frame homes near downtown and the fairgrounds.</li>
<li>Mid-century ranches across much of the city.</li>
<li>Rural acreages and farmsteads around Reno County.</li>
<li>Commercial and industrial buildings.</li>
</ul>
<h2>Common disputes</h2>
<p>Hail and wind claims on older homes, grass fire losses involving homes, outbuildings and fence, and smoke damage to homes that didn’t burn. We value each part of the loss line by line.</p>
""",
        "faqs": [
            ("Is a grass fire claim different from a house fire?", "Grass fire claims often involve fences, outbuildings and smoke damage across a property, which may fall under different coverages."),
            ("Do you serve South Hutchinson and Nickerson?", "Yes, along with the rest of Reno County."),
        ],
    },
    {
        "slug": "dodge-city", "city": "Dodge City", "county": "Ford County", "region": "Southwest Kansas",
        "perils": ["Hail", "Tornadoes", "Wind", "Grass fire", "Blowing dust"],
        "near": ["garden-city", "hutchinson", "hays"],
        "housing": "Older frame homes, ranches, commercial and agricultural buildings",
        "lede": "Dodge City’s storms are legendary. On May 24, 2016, several tornadoes circled the city at once, and hail is a near-annual event across Ford County.",
        "body": """
<h2>Wild West, wild weather</h2>
<p>Dodge City is famous for its frontier history, but locals know it for weather too. On May 24, 2016, multiple tornadoes touched down around the city in a single afternoon, widely photographed from town. Hail, high wind and wildfire risk are part of life in southwest Kansas.</p>
<h2>Housing and buildings</h2>
<ul>
<li>Older frame homes near downtown.</li>
<li>Ranches and newer homes on the north and west sides.</li>
<li>Large agricultural and meatpacking facilities.</li>
<li>Farmsteads, barns and outbuildings across Ford County.</li>
</ul>
<h2>Common disputes</h2>
<p>Hail damage to homes and metal buildings, wind damage to roofs and siding, cosmetic exclusions on metal roofs, and rural losses where contractor travel adds cost. We value repairs with pricing that reflects southwest Kansas realities.</p>
""",
        "faqs": [
            ("Do contractors charge more in southwest Kansas?", "Travel time, equipment delivery and limited crews after a storm can raise costs. Those factors should be reflected in an accurate estimate."),
            ("Do you handle metal building claims?", "Yes, including shops, barns and commercial metal buildings."),
        ],
    },
    {
        "slug": "garden-city", "city": "Garden City", "county": "Finney County", "region": "Southwest Kansas",
        "perils": ["Hail", "Wind", "Tornadoes", "Grass fire", "Blowing dust"],
        "near": ["dodge-city", "hays", "hutchinson"],
        "housing": "Ranches and newer homes, agricultural and commercial buildings",
        "lede": "Garden City is the hub of southwest Kansas agriculture. Hail, wind and dust storms hit homes, metal buildings and feed operations across Finney County.",
        "body": """
<h2>High Plains hub</h2>
<p>Garden City serves a wide region of farms, feedlots and agricultural businesses on the High Plains. The weather can be extreme: large hail, strong winds, blowing dust and grass fires are all part of the risk picture.</p>
<h2>Housing and buildings</h2>
<ul>
<li>Ranches and split-levels across established neighborhoods.</li>
<li>Newer subdivisions on the edges of town.</li>
<li>Agricultural, processing and commercial facilities.</li>
<li>Farmsteads and outbuildings across Finney County.</li>
</ul>
<h2>Common disputes</h2>
<p>Hail damage to roofs, siding and metal buildings, wind damage, and rural losses with contractor access issues. We value homes and farm buildings with pricing that reflects the realities of the High Plains.</p>
""",
        "faqs": [
            ("Do you travel to Garden City?", "Yes. We work statewide, including Finney, Kearny, Haskell and surrounding counties."),
            ("Are dust storms covered?", "Wind-driven damage is often covered as windstorm. Dust infiltration depends on the policy and how damage occurred."),
        ],
    },
    {
        "slug": "hays", "city": "Hays", "county": "Ellis County", "region": "Northwest Kansas",
        "perils": ["Hail", "Wind", "Grass fire", "Tornadoes", "Ice storms"],
        "near": ["salina", "garden-city", "dodge-city"],
        "housing": "Limestone and frame homes, ranches, rural farmsteads",
        "lede": "Hays and Ellis County know wind and fire. The December 15, 2021 windstorm drove the Four County Fire across the region, and hail is common every spring.",
        "body": """
<h2>Post rock country</h2>
<p>Hays is the largest city in northwest Kansas and home to Fort Hays State University. The area is known for limestone “post rock” fence posts and buildings, Volga German heritage and wide-open country. On December 15, 2021, an extreme windstorm swept across the state and fueled the Four County Fire in Ellis, Russell, Osborne and Rooks counties, burning homes, outbuildings and pasture.</p>
<h2>Housing and buildings</h2>
<ul>
<li>Limestone homes and buildings with unique masonry repair needs.</li>
<li>Older frame homes near downtown.</li>
<li>Ranches and newer homes across town.</li>
<li>Farmsteads, barns and outbuildings in rural Ellis County.</li>
</ul>
<h2>Common disputes</h2>
<p>Limestone masonry repairs priced too low, hail damage to roofs and metal buildings, grass fire losses involving fence and outbuildings, and wind damage across the region. We value each claim with local knowledge.</p>
""",
        "faqs": [
            ("Do you value limestone repairs?", "Yes. Limestone masonry requires skilled trades and matching stone, which should be reflected in the estimate."),
            ("Do you serve Russell and Victoria?", "Yes, along with the rest of northwest Kansas."),
        ],
    },
]
