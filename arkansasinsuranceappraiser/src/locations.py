"""Arkansas location pages. Facts are general and cautious; storm references are to widely reported events."""

LOCATIONS = [
    {
        "slug": "little-rock", "city": "Little Rock", "county": "Pulaski County", "region": "Central Arkansas",
        "perils": ["Tornadoes", "Hail", "Severe thunderstorms", "Ice storms", "Burst pipes"],
        "lede": "The capital city’s housing runs from Victorian homes in the Quapaw Quarter to brick ranches in Midtown and newer houses in Chenal Valley. Storm claims touch every part of it.",
        "body": """
<h2>Storm history in Little Rock</h2>
<p>On March 31, 2023, a powerful tornado tracked across west Little Rock, through neighborhoods near Walnut Valley and the Kanis and Shackleford corridors, and on across the river into North Little Rock and Jacksonville. Thousands of homes and businesses were damaged. Many owners just outside the main path found their claims grew as roofers and drywall crews opened walls and attics weeks later. Little Rock also sees regular spring hail and occasional winter ice that brings down the city’s mature oaks.</p>
<h2>Neighborhoods and housing</h2>
<ul>
<li><strong>Quapaw Quarter and downtown:</strong> 19th- and early-20th-century homes with plaster walls, original millwork and slate or wood details that estimating software often prices as generic materials.</li>
<li><strong>Hillcrest and the Heights:</strong> Craftsman bungalows and Tudor-style homes under large trees, where limb damage and matching are recurring issues.</li>
<li><strong>Midtown and southwest Little Rock:</strong> mid-century brick ranches with low-slope additions and older electrical systems.</li>
<li><strong>West Little Rock and Chenal Valley:</strong> larger homes with steep, cut-up roofs and higher-end interiors that raise the stakes on a short estimate.</li>
</ul>
<h2>Commercial property</h2>
<p>Office towers downtown, medical buildings along the I-630 corridor and retail centers in west Little Rock carry commercial policies with their own deductibles and coinsurance terms. We value commercial losses building by building.</p>""",
        "faqs": [
            ("Do you inspect in person in Little Rock?", "Yes. Central Arkansas inspections are scheduled directly, usually within a few business days."),
            ("My home was near the 2023 tornado path but the damage looked minor. Is it too late?", "That depends on your policy’s deadlines and whether the claim is still open. Call promptly and have your claim letters ready."),
            ("Can you help with historic home pricing?", "Yes. We document original materials so the estimate reflects like kind and quality rather than a generic substitute."),
        ],
        "near": ["north-little-rock", "conway", "hot-springs", "pine-bluff"],
    },
    {
        "slug": "north-little-rock", "city": "North Little Rock", "county": "Pulaski County", "region": "Central Arkansas",
        "perils": ["Tornadoes", "Straight-line winds", "Hail", "Fallen trees", "Water losses"],
        "lede": "Across the Arkansas River from the capital, North Little Rock mixes historic Argenta, hillside Park Hill, Lakewood’s lakeside homes and fast-growing suburbs to the north.",
        "body": """
<h2>Recent storms</h2>
<p>The March 31, 2023 tornado crossed the Arkansas River and continued through parts of North Little Rock toward Sherwood and Jacksonville, damaging homes, apartment complexes and businesses. Severe thunderstorms and hail are common every spring, and straight-line winds have toppled large trees in older neighborhoods more than once.</p>
<h2>Neighborhoods and housing mix</h2>
<ul>
<li><strong>Argenta:</strong> a historic district of restored Victorian and early-20th-century homes alongside new infill townhomes and lofts.</li>
<li><strong>Park Hill:</strong> 1920s through 1950s homes on wooded hills, many with original hardwood and plaster.</li>
<li><strong>Lakewood:</strong> mid-century brick homes around a chain of small lakes, with mature trees close to rooflines.</li>
<li><strong>Indian Hills and the north side:</strong> 1970s through 2000s subdivisions with composition roofs and vinyl or brick exteriors.</li>
</ul>
<h2>Apartments and commercial</h2>
<p>North Little Rock has many multifamily communities and light-industrial buildings near the interstate corridors. Multi-building claims need separate scopes for each structure so nothing is averaged out of the estimate.</p>""",
        "faqs": [
            ("Do you work with apartment owners in North Little Rock?", "Yes. We scope each building and summarize differences in a format owners and lenders can follow."),
            ("Our tree fell on the house during a storm. What can be claimed?", "Structural repairs to the house, interior water damage and some tree removal costs, subject to your policy’s limits."),
            ("Is an Argenta historic home harder to appraise?", "It takes more documentation. Original materials and craftsmanship need to be shown clearly so they’re priced correctly."),
        ],
        "near": ["little-rock", "conway", "pine-bluff", "hot-springs"],
    },
    {
        "slug": "fort-smith", "city": "Fort Smith", "county": "Sebastian County", "region": "Arkansas River Valley",
        "perils": ["Tornadoes", "Hail", "Straight-line winds", "River flooding", "Ice storms"],
        "lede": "Arkansas’s border city on the Arkansas River blends historic Belle Grove homes, mid-century neighborhoods and new growth at Chaffee Crossing.",
        "body": """
<h2>Storm and flood history</h2>
<p>On April 21, 1996, a tornado struck downtown Fort Smith and Van Buren across the river, damaging historic buildings and hundreds of homes. In late May and early June 2019, the Arkansas River rose to record levels at Fort Smith and Van Buren, flooding low-lying neighborhoods. River flooding is generally excluded from homeowner policies and handled through flood insurance, so separating flood damage from wind or rain damage is a frequent issue here.</p>
<h2>Housing across Fort Smith</h2>
<ul>
<li><strong>Belle Grove Historic District:</strong> Victorian and Queen Anne homes with complex roof forms, decorative trim and plaster interiors.</li>
<li><strong>Central and east Fort Smith:</strong> early-to-mid 20th-century bungalows and brick cottages.</li>
<li><strong>South side and Chaffee Crossing:</strong> newer subdivisions with architectural shingles and open floor plans where flooring and paint continuity matter.</li>
</ul>
<h2>Commercial and industrial</h2>
<p>Fort Smith has a large manufacturing and distribution base. Metal buildings, low-slope roofs and large warehouse footprints make commercial hail and wind claims a significant part of the work in Sebastian and Crawford counties.</p>""",
        "faqs": [
            ("My house was flooded and also lost shingles. How does that work?", "The homeowner policy may cover the wind damage while flood insurance covers rising water. Each loss needs separate documentation."),
            ("Do you cover Van Buren and Crawford County?", "Yes, along with the rest of the River Valley."),
            ("Can you help with metal warehouse roofs?", "Yes. We review cosmetic-damage language first, then document seams, fasteners and panels."),
        ],
        "near": ["fayetteville", "springdale", "conway", "hot-springs"],
    },
    {
        "slug": "fayetteville", "city": "Fayetteville", "county": "Washington County", "region": "Northwest Arkansas",
        "perils": ["Large hail", "Ice storms", "Tornadoes", "Fallen hardwoods", "Flash flooding"],
        "lede": "Home of the University of Arkansas, Fayetteville spreads across Ozark hills, with older homes near Dickson Street and Wilson Park and newer neighborhoods to the west.",
        "body": """
<h2>Hail and ice in the Ozarks</h2>
<p>Northwest Arkansas sits in one of the state’s most active hail zones. Spring supercells regularly drop golf-ball-size hail or larger across Washington and Benton counties, producing waves of roof claims. In January 2009, a severe ice storm snapped hardwoods across the region and left parts of Fayetteville without power for days. Hilly terrain also brings flash flooding along creeks during heavy rain.</p>
<h2>Neighborhoods and homes</h2>
<ul>
<li><strong>Wilson Park and Washington-Willow:</strong> historic homes from the late 1800s through the 1930s under mature oak canopy.</li>
<li><strong>Mount Sequoyah and east Fayetteville:</strong> hillside homes with steep driveways and steep roofs that add access and safety costs.</li>
<li><strong>Campus area:</strong> rental houses, duplexes and student apartment complexes with commercial policies.</li>
<li><strong>West Fayetteville:</strong> newer subdivisions with complex architectural shingle roofs.</li>
</ul>
<h2>Rental owners</h2>
<p>Many Fayetteville property owners hold a few rental houses or a small apartment building near campus. Dwelling-fire and landlord policies use different terms than a standard homeowner form. We read your specific policy before advising on appraisal.</p>""",
        "faqs": [
            ("How common are hail claims in Fayetteville?", "Very common. Northwest Arkansas sees significant hail most springs, and many roofs have been replaced more than once."),
            ("Do steep hillside roofs cost more to replace?", "Usually. Steep pitch, height and difficult access add labor and safety equipment that should appear in the estimate."),
            ("Do you work with student-rental landlords?", "Yes. We handle single rentals and small multifamily buildings."),
        ],
        "near": ["springdale", "rogers", "bentonville", "fort-smith"],
    },
    {
        "slug": "springdale", "city": "Springdale", "county": "Washington & Benton Counties", "region": "Northwest Arkansas",
        "perils": ["Hail", "Tornadoes", "Straight-line winds", "Ice storms", "Commercial roof damage"],
        "lede": "Straddling Washington and Benton counties, Springdale combines a revitalized downtown, established neighborhoods and a large poultry and food-processing industrial base.",
        "body": """
<h2>Storm exposure</h2>
<p>Springdale shares Northwest Arkansas’s heavy hail exposure. Spring storms frequently produce large hail, and tornado warnings are a regular part of the season. The January 2009 ice storm brought down trees and power lines across the city. Commercial and industrial buildings along the US-412 and I-49 corridors carry large roofs that make hail claims especially expensive.</p>
<h2>Housing mix</h2>
<ul>
<li><strong>Downtown and Emma Avenue area:</strong> older homes and commercial buildings near the Razorback Greenway, many recently renovated.</li>
<li><strong>Established neighborhoods:</strong> 1960s through 1990s brick and siding homes, often with original or second-generation roofs.</li>
<li><strong>Newer subdivisions:</strong> fast-growing areas toward the west and north with larger homes and complex roof lines.</li>
</ul>
<h2>Industrial and agricultural property</h2>
<p>Processing plants, warehouses and poultry houses involve specialized construction and commercial policies with business-income exposure. These claims often benefit from an independent scope and, where needed, specialty consultants for refrigeration or roofing systems.</p>""",
        "faqs": [
            ("Do you handle poultry house or agricultural building claims?", "Yes, when they are covered under a property policy. Farm policies have unique terms, so we start with a policy review."),
            ("Which county are you assigning my Springdale claim to?", "It doesn’t matter for our work. We cover both Washington and Benton counties the same way."),
            ("Can a warehouse hail claim go to appraisal?", "Yes, if coverage is accepted and the dispute is about scope or cost."),
        ],
        "near": ["fayetteville", "rogers", "bentonville", "fort-smith"],
    },
    {
        "slug": "rogers", "city": "Rogers", "county": "Benton County", "region": "Northwest Arkansas",
        "perils": ["Large hail", "Tornadoes", "Ice storms", "Lake-area wind", "Commercial losses"],
        "lede": "Rogers runs from a historic downtown to the Pinnacle Hills retail and office district and out to homes along Beaver Lake.",
        "body": """
<h2>Storms in Benton County</h2>
<p>Benton County is one of Arkansas’s most frequent hail targets, and spring tornado outbreaks have struck the area repeatedly, including the late-May 2024 storms that caused serious damage in parts of the county. Ice storms such as January 2009’s also brought down large trees across the city. Homes near Beaver Lake face more open wind exposure and steep, wooded lots.</p>
<h2>Neighborhoods and property types</h2>
<ul>
<li><strong>Downtown Rogers:</strong> early-20th-century homes and brick commercial buildings.</li>
<li><strong>Pinnacle Hills:</strong> high-value homes, offices, hotels and retail with commercial roofs and glass curtain walls.</li>
<li><strong>Suburban Rogers:</strong> rapidly built subdivisions from the 2000s onward, where roof age and matching drive many disputes.</li>
<li><strong>Beaver Lake area:</strong> lake homes, boathouses and docks that may fall under other-structures coverage or separate policies.</li>
</ul>
<h2>High-value homes</h2>
<p>Larger homes with custom finishes are where a short estimate costs the most. We document upgraded materials, cabinetry, stone and specialty roofing so the estimate reflects like kind and quality.</p>""",
        "faqs": [
            ("Are boat docks covered by my homeowner policy?", "Sometimes, under other structures or a separate watercraft or dock policy. We review your policy before including them."),
            ("My subdivision had hail last year and again this year. Does that matter?", "It can. Each storm must be documented separately, and prior repairs affect what the new claim covers."),
            ("Do you appraise office and retail buildings in Pinnacle Hills?", "Yes, including low-slope roofs and storefront systems."),
        ],
        "near": ["bentonville", "springdale", "fayetteville", "fort-smith"],
    },
    {
        "slug": "bentonville", "city": "Bentonville", "county": "Benton County", "region": "Northwest Arkansas",
        "perils": ["Large hail", "Tornadoes", "Ice storms", "Wind", "New-construction issues"],
        "lede": "One of the fastest-growing cities in the region, Bentonville pairs a historic square and the Crystal Bridges grounds with block after block of new construction.",
        "body": """
<h2>Hail, wind and ice</h2>
<p>Bentonville shares Benton County’s heavy hail exposure, and spring tornado warnings are routine. Ice storms, especially the January 2009 event, damaged trees and power infrastructure across the area. Because so much of the city is new, many claims involve roofs and finishes only a few years old, where depreciation and matching disputes look different than on older homes.</p>
<h2>Neighborhoods and construction</h2>
<ul>
<li><strong>Downtown and the square:</strong> restored historic homes and new modern infill with flat or low-slope roofs.</li>
<li><strong>Bella Vista edge and north Bentonville:</strong> wooded lots where tree damage is common in wind and ice events.</li>
<li><strong>New subdivisions:</strong> large tracts with architectural shingles, open floor plans and builder finishes that may already be discontinued.</li>
<li><strong>Corporate and commercial growth:</strong> offices, hotels and retail with commercial policies and large roofs.</li>
</ul>
<h2>Discontinued products</h2>
<p>Fast building cycles mean shingle colors, siding profiles and flooring lines change quickly. When a damaged product can’t be matched, the repair scope often expands. We document availability so the panel can price the real repair.</p>""",
        "faqs": [
            ("My roof is only three years old. Will depreciation be minimal?", "Depreciation should reflect age and condition. On a newer roof it should be modest, and we check how the carrier applied it."),
            ("Can modern flat-roof homes be appraised?", "Yes. Low-slope residential roofs are scoped like commercial membranes, with attention to insulation and drainage."),
            ("Do you cover Bella Vista?", "Yes, along with all of Benton County."),
        ],
        "near": ["rogers", "springdale", "fayetteville", "fort-smith"],
    },
    {
        "slug": "jonesboro", "city": "Jonesboro", "county": "Craighead County", "region": "Northeast Arkansas & Crowley’s Ridge",
        "perils": ["Tornadoes", "Straight-line winds", "Hail", "Ice storms", "Earthquake questions"],
        "lede": "Northeast Arkansas’s largest city sits on Crowley’s Ridge above the Delta, home to Arkansas State University and a growing regional medical and retail center.",
        "body": """
<h2>Tornado history</h2>
<p>On March 28, 2020, a tornado struck Jonesboro, heavily damaging the Mall at Turtle Creek area, nearby businesses and homes. The city was also struck by a deadly tornado in May 1968. Spring and late-fall storms crossing the Delta regularly bring damaging straight-line winds and hail, and ice storms affect the region in some winters.</p>
<h2>Housing and neighborhoods</h2>
<ul>
<li><strong>Older central Jonesboro:</strong> early and mid-20th-century homes, many with pier-and-beam foundations and crawl spaces.</li>
<li><strong>University area:</strong> rental houses and apartment complexes near Arkansas State.</li>
<li><strong>South and west Jonesboro:</strong> newer subdivisions and larger homes, often brick with complex hip roofs.</li>
<li><strong>Rural Craighead County:</strong> farmhouses, shops and grain or equipment buildings.</li>
</ul>
<h2>Earthquake coverage</h2>
<p>Northeast Arkansas lies near the New Madrid Seismic Zone. Standard homeowner policies generally exclude earth movement, and earthquake coverage is usually a separate endorsement. If you carry that endorsement and have a dispute over the amount of an earthquake loss, appraisal may apply like any other covered peril.</p>""",
        "faqs": [
            ("Is earthquake damage covered in Jonesboro?", "Usually only if you bought an earthquake endorsement or policy. Check your declarations page."),
            ("Do you serve Paragould and the rest of northeast Arkansas?", "Yes. We cover Craighead, Greene, Mississippi, Poinsett and the surrounding counties."),
            ("Can you help with a farm shop damaged by wind?", "Yes, if it’s insured under a property policy. Farm policies vary, so we start with a review."),
        ],
        "near": ["conway", "north-little-rock", "little-rock", "pine-bluff"],
    },
    {
        "slug": "conway", "city": "Conway", "county": "Faulkner County", "region": "Central Arkansas",
        "perils": ["Tornadoes", "Hail", "Severe storms", "Ice storms", "Water losses"],
        "lede": "“The City of Colleges” is home to the University of Central Arkansas, Hendrix College and Central Baptist College, and to fast-growing neighborhoods north of Little Rock.",
        "body": """
<h2>Tornadoes in Faulkner County</h2>
<p>Faulkner County has been struck by some of Arkansas’s most destructive tornadoes. On April 27, 2014, a violent EF4 tornado tracked through Mayflower and Vilonia, just outside Conway, destroying hundreds of homes. Vilonia had also been hit hard in April 2011. Conway itself sees regular hail and severe thunderstorms each spring.</p>
<h2>Housing in and around Conway</h2>
<ul>
<li><strong>Old Conway:</strong> historic homes near downtown and Hendrix, many with original hardwood, plaster and detailed trim.</li>
<li><strong>College-area rentals:</strong> houses and apartments near UCA and Hendrix with landlord policies.</li>
<li><strong>Newer subdivisions:</strong> rapid growth to the west and north, with architectural shingles and open plans.</li>
<li><strong>Greenbrier, Vilonia and Mayflower:</strong> suburban and rural homes, many rebuilt after past tornadoes.</li>
</ul>
<h2>Rebuilds and total losses</h2>
<p>When a home is destroyed, the dispute often centers on replacement cost: what it truly costs to rebuild the same home in Faulkner County today, plus debris removal, code upgrades, other structures and contents. We build that valuation from the ground up.</p>""",
        "faqs": [
            ("Do you cover Vilonia, Mayflower and Greenbrier?", "Yes, all of Faulkner County and the surrounding area."),
            ("My home was rebuilt after a tornado and damaged again. Does the new construction matter?", "Yes. Newer materials mean lower depreciation, and the rebuild documents help prove what was there."),
            ("Can appraisal help on a total loss?", "Yes, if the dispute is about the amount, such as replacement cost, debris removal or contents."),
        ],
        "near": ["little-rock", "north-little-rock", "hot-springs", "jonesboro"],
    },
    {
        "slug": "pine-bluff", "city": "Pine Bluff", "county": "Jefferson County", "region": "Arkansas Delta",
        "perils": ["Tornadoes", "Straight-line winds", "Fallen trees", "Water losses", "River flooding"],
        "lede": "On the Arkansas River at the edge of the Delta, Pine Bluff has a deep stock of historic and mid-century homes alongside farms, churches and industrial property.",
        "body": """
<h2>Storm exposure</h2>
<p>Pine Bluff sits where Delta storm systems often intensify. Tornadoes and straight-line winds have damaged the city and surrounding Jefferson County many times, and large pines and oaks near homes make tree impacts common. The 2019 Arkansas River flood raised water levels along the river through Jefferson County. Flood damage is typically excluded from homeowner policies, so separating it from wind and rain damage matters.</p>
<h2>Housing and buildings</h2>
<ul>
<li><strong>Historic downtown and nearby districts:</strong> late-1800s and early-1900s homes and commercial blocks with plaster, tall ceilings and older roof systems.</li>
<li><strong>Mid-century neighborhoods:</strong> brick ranch homes with original features and aging plumbing.</li>
<li><strong>Churches and community buildings:</strong> large roofs, steeples and specialty windows.</li>
<li><strong>Rural Jefferson County:</strong> farmhouses, shops and agricultural buildings.</li>
</ul>
<h2>Older homes and code items</h2>
<p>Repairing an older home can trigger code requirements for electrical, plumbing or roofing. Whether ordinance-or-law coverage pays for those upgrades depends on your policy, but the cost should be identified in the estimate so it can be evaluated.</p>""",
        "faqs": [
            ("Do you appraise church property?", "Yes. Churches often have large roofs, steeples and specialty glass that need careful pricing."),
            ("Will my policy pay to bring old wiring up to code?", "Only if you have ordinance-or-law coverage. We identify the costs so you can see what applies."),
            ("Do you cover the rest of southeast Arkansas?", "Yes, including the Delta counties along the Arkansas and Mississippi rivers."),
        ],
        "near": ["little-rock", "north-little-rock", "hot-springs", "texarkana"],
    },
    {
        "slug": "hot-springs", "city": "Hot Springs", "county": "Garland County", "region": "Ouachita Mountains",
        "perils": ["Fallen trees", "Ice storms", "Flash flooding", "Hail", "Wildfire smoke"],
        "lede": "Set in the Ouachita Mountains around Bathhouse Row, Lake Hamilton and Lake Ouachita, Hot Springs mixes historic homes, lake houses and retirement communities.",
        "body": """
<h2>Mountain and lake hazards</h2>
<p>Hot Springs’ wooded hills mean trees stand close to many homes, and ice storms and high winds bring them down. Steep terrain funnels heavy rain into creeks that can flash flood, including through the downtown area. Spring hail and severe storms occur throughout Garland County, and dry seasons can bring woodland fires in the surrounding national forest.</p>
<h2>Housing mix</h2>
<ul>
<li><strong>Historic Hot Springs:</strong> early-1900s homes and buildings near Central Avenue with plaster, stone and ornate details.</li>
<li><strong>Lake Hamilton and Lake Ouachita:</strong> lake homes with decks, docks and boathouses on steep lots.</li>
<li><strong>Hot Springs Village:</strong> a large gated community extending into Saline County, with many homes on wooded golf-course lots.</li>
<li><strong>Vacation rentals:</strong> properties that may need a landlord or short-term-rental policy rather than a standard homeowner form.</li>
</ul>
<h2>Access and steep lots</h2>
<p>Steep driveways, hillside foundations and lakefront access add real costs for equipment and labor. Those costs belong in the estimate.</p>""",
        "faqs": [
            ("Do you cover Hot Springs Village?", "Yes, both the Garland and Saline county portions."),
            ("Is my vacation rental covered like my home?", "Not always. Short-term rentals may need a separate policy. We review the policy before advising."),
            ("Is flash flood damage covered?", "Rising surface water is generally excluded from homeowner policies and covered by flood insurance."),
        ],
        "near": ["little-rock", "conway", "pine-bluff", "texarkana"],
    },
    {
        "slug": "texarkana", "city": "Texarkana", "county": "Miller County", "region": "Southwest Arkansas",
        "perils": ["Ice storms", "Tornadoes", "Tropical remnants", "Fallen pines", "Hail"],
        "lede": "Texarkana, Arkansas sits on the state line in Miller County, where the Gulf Coastal Plain’s pine forests meet older neighborhoods and growing commercial corridors.",
        "body": """
<h2>Ice, wind and tropical remnants</h2>
<p>The December 2000 ice storms hit southwest Arkansas especially hard, coating Texarkana and surrounding counties in heavy ice and causing long power outages and widespread tree damage. Tornadoes and severe thunderstorms are a spring and fall risk, and remnants of Gulf hurricanes, such as Laura in August 2020, have brought strong gusts and fallen pines to the region.</p>
<h2>Housing and buildings</h2>
<ul>
<li><strong>Older central neighborhoods:</strong> early and mid-20th-century homes, many on pier-and-beam foundations.</li>
<li><strong>Suburban Miller County:</strong> newer brick and siding homes with composition roofs.</li>
<li><strong>Rural property:</strong> homes surrounded by tall pines, where a single wind event can bring several trees down at once.</li>
<li><strong>Commercial corridors:</strong> retail, restaurants and warehouses along the interstate.</li>
</ul>
<h2>Tree damage claims</h2>
<p>Many policies limit tree removal to a set amount per tree and per event, and only when a tree damages a covered structure. We document every impact, the structural repairs and the removal costs separately so the limits are applied correctly.</p>""",
        "faqs": [
            ("Does it matter which side of the state line my property is on?", "Yes. Insurance rules follow the state where the property sits. We handle property on the Arkansas side."),
            ("Are tree removal costs covered after an ice storm?", "Often only when the tree damages a covered structure, and subject to limits. We help document them."),
            ("Do you cover Hope, Magnolia and El Dorado?", "Yes, all of southwest and south Arkansas."),
        ],
        "near": ["hot-springs", "pine-bluff", "little-rock", "fort-smith"],
    },
]
