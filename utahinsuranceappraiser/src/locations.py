"""Utah location pages. Local detail is general and drawn from public sources; no client results."""

LOCATIONS = [
    {
        "slug": "salt-lake-city", "city": "Salt Lake City", "county": "Salt Lake County", "region": "Wasatch Front",
        "near": ["west-valley-city", "sandy", "layton"],
        "perils": ["Canyon wind", "Hail", "Earthquake (endorsement)", "Ice dams", "Burst pipes"],
        "lede": "Utah’s capital mixes century-old brick bungalows, Victorian homes in the Avenues, mid-century ranches on the east bench and downtown high-rises. Each one fails differently in a storm, and each one prices differently in an estimate.",
        "body": """
<h2>Claims we see in Salt Lake City</h2>
<p>Salt Lake City sits at the heart of Salt Lake County, with neighborhoods that climb from the valley floor in Rose Park and Glendale to the foothills of Federal Heights and the East Bench. Summer thunderstorms bring hail and microbursts. Winter brings ice dams on older, poorly insulated roofs and frozen pipes during cold snaps. Canyon winds can hit the northern and eastern neighborhoods hard, as they did in September 2020.</p>
<h2>Storm and seismic history</h2>
<p>On August 11, 1999, a tornado moved through downtown Salt Lake City, the Avenues and Capitol Hill, damaging hundreds of buildings. On March 18, 2020, the magnitude 5.7 Magna earthquake rattled the valley; chimneys and brick parapets were damaged across the west side and in older neighborhoods. Owners who carry earthquake coverage should know their deductible before a claim.</p>
<h2>Housing that shapes the estimate</h2>
<ul>
<li><strong>Sugar House, Liberty Wells and the Avenues:</strong> early 1900s brick bungalows and Victorians with plaster walls, original trim and complex rooflines.</li>
<li><strong>Capitol Hill and Federal Heights:</strong> steep lots, older masonry and expensive access for roof and siding work.</li>
<li><strong>Rose Park and Glendale:</strong> mid-century homes, many with additions and older electrical and plumbing.</li>
<li><strong>Downtown and Central City:</strong> condominiums and mixed-use buildings where HOA master policies and unit-owner policies interact.</li>
</ul>
<h2>What to watch for</h2>
<p>Plaster and lath repairs, historic trim and masonry are routinely underpriced. For condos, check which policy covers interior finishes before assuming the association will handle it.</p>
""",
        "faqs": [
            ("Do you inspect homes in the Avenues and on the East Bench?", "Yes. We work throughout Salt Lake City, including hillside neighborhoods where access and steep roofs affect pricing."),
            ("My condo had a leak from the unit above. Who pays?", "It depends on the HOA’s master policy, the governing documents and your unit-owner policy. We can review the estimates once coverage is sorted out."),
        ],
    },
    {
        "slug": "west-valley-city", "city": "West Valley City", "county": "Salt Lake County", "region": "Wasatch Front",
        "near": ["salt-lake-city", "sandy", "lehi"],
        "perils": ["Hail", "Wind", "Earthquake (endorsement)", "Water losses", "Fire"],
        "lede": "Utah’s second-largest city spreads across the west side of the Salt Lake Valley, with 1960s–80s ranch and split-level homes, newer subdivisions toward the Oquirrhs and a large commercial and industrial base.",
        "body": """
<h2>A west-side mix of homes and industry</h2>
<p>West Valley City’s neighborhoods, from Granger and Hunter to Redwood and Chesterfield, are dominated by single-family homes built from the 1960s through the 1980s, plus townhome communities and newer construction on the west bench. Commercial and industrial properties line Redwood Road, 3500 South and the areas near the interstate.</p>
<h2>Weather and seismic exposure</h2>
<p>Hail and wind from summer storms are the most common property claims here. The March 2020 Magna earthquake was centered just west of the city, and homes in West Valley City, Magna and Kearns reported cracked masonry, chimneys and foundations. Many standard policies exclude earthquake damage, so the first question is always whether an endorsement applies.</p>
<h2>Housing notes</h2>
<ul>
<li><strong>Split-levels and ranches:</strong> often have aluminum or vinyl siding that is hard to match after a storm.</li>
<li><strong>Brick ranches:</strong> mortar and chimney damage after shaking or settlement need careful separation.</li>
<li><strong>Townhome communities:</strong> HOA master policies typically handle roofs and exteriors.</li>
<li><strong>Warehouses and flex space:</strong> large low-slope roofs where hail, wind and ponding issues overlap.</li>
</ul>
<h2>Common estimate gaps</h2>
<p>Siding matching, roof decking replacement and commercial roof tie-ins are frequent sources of disagreement in West Valley City claims.</p>
""",
        "faqs": [
            ("Was my house damaged in the 2020 earthquake covered?", "Only if you had earthquake coverage and your loss exceeded the earthquake deductible. Coverage questions are best answered by reviewing your policy."),
            ("Do you handle warehouse roof claims?", "Yes. We value low-slope commercial roofs, including membrane, metal and built-up systems."),
        ],
    },
    {
        "slug": "sandy", "city": "Sandy", "county": "Salt Lake County", "region": "Wasatch Front",
        "near": ["salt-lake-city", "lehi", "west-valley-city"],
        "perils": ["Hail", "Canyon wind", "Wildfire (foothills)", "Ice dams", "Frozen pipes"],
        "lede": "At the mouth of Little Cottonwood Canyon, Sandy pairs established 1970s–90s neighborhoods with large foothill homes that face snow, wind and wildfire risk from the Wasatch.",
        "body": """
<h2>Foothills and the valley floor</h2>
<p>Sandy runs from the valley floor near the Jordan River to the foothills of the Wasatch, with neighborhoods such as Alta Canyon, Granite, Dimple Dell and Willow Creek. Homes near the mountains see more snow, stronger winds and more exposure to brush fires than those closer to the valley center.</p>
<h2>Typical claims</h2>
<p>Summer hail is the most frequent roof claim. In winter, the higher neighborhoods deal with ice dams and heavy snow loads, especially on homes with complex rooflines and multiple valleys. Foothill homes near Dimple Dell and the canyon mouths also sit within wildland-urban interface areas where wildfire smoke and embers are a concern.</p>
<h2>Housing notes</h2>
<ul>
<li><strong>1970s–90s two-story homes:</strong> brick and stucco fronts with siding on other elevations, and often original or second-generation roofs.</li>
<li><strong>Large foothill homes:</strong> steep, cut-up roofs with high waste factors and steep-roof charges.</li>
<li><strong>Townhomes and condos:</strong> clustered near the TRAX line and major corridors.</li>
</ul>
<h2>What to check in your estimate</h2>
<p>Steep and high-roof charges, ice-and-water shield along eaves and valleys, and matching of stucco or stone veneer are frequent gaps on Sandy claims.</p>
""",
        "faqs": [
            ("My roof has several pitches. Does that matter?", "Yes. Pitch affects surface area, waste and labor charges. Our roof calculator shows how pitch changes the total."),
            ("Does my policy cover wildfire smoke damage?", "Many policies cover smoke damage from a nearby fire as physical damage. Document it promptly and keep any testing results."),
        ],
    },
    {
        "slug": "provo", "city": "Provo", "county": "Utah County", "region": "Utah Valley",
        "near": ["orem", "lehi", "salt-lake-city"],
        "perils": ["Hail", "Wildfire (foothills)", "Frozen pipes", "Water losses", "Fire"],
        "lede": "Home to BYU and a large rental market, Provo blends historic homes near downtown, student housing near campus and foothill neighborhoods below Y Mountain and Rock Canyon.",
        "body": """
<h2>A university city with diverse housing</h2>
<p>Provo is the county seat of Utah County. Neighborhoods such as Joaquin and Maeser near downtown hold older brick homes and converted rentals. Grandview, Edgemont and Rock Canyon climb toward the foothills, while the Riverbottoms and areas near Utah Lake have newer construction.</p>
<h2>Typical Provo claims</h2>
<ul>
<li><strong>Rental and multifamily water losses:</strong> burst pipes and appliance leaks in student housing and fourplexes, often discovered after breaks.</li>
<li><strong>Hail:</strong> summer storms moving down Utah Valley.</li>
<li><strong>Wildfire smoke:</strong> foothill neighborhoods face smoke and ember exposure during fire season. The 2018 Pole Creek and Bald Mountain fires to the south filled the valley with smoke.</li>
<li><strong>Kitchen fires:</strong> common in multi-tenant buildings.</li>
</ul>
<h2>Housing notes</h2>
<p>Older Provo homes often have basement apartments, mixed electrical and plumbing upgrades and multiple layers of roofing. Rental properties also raise loss-of-rents questions under landlord policies.</p>
<h2>What to watch for</h2>
<p>For landlords, check whether your policy covers fair rental value during repairs and what documentation it requires. For multifamily water losses, make sure every affected unit is scoped, not just the source unit.</p>
""",
        "faqs": [
            ("I own a rental near campus. Do you handle landlord claims?", "Yes. We value dwelling and multifamily rental losses and can help organize loss-of-rents documentation for the amount-of-loss question."),
            ("Do you work in Springville, Spanish Fork and Payson too?", "Yes. We serve all of Utah County and the rest of the state."),
        ],
    },
    {
        "slug": "orem", "city": "Orem", "county": "Utah County", "region": "Utah Valley",
        "near": ["provo", "lehi", "sandy"],
        "perils": ["Hail", "Wind", "Ice dams", "Water losses", "Fire"],
        "lede": "Once a city of orchards, Orem is now a dense suburban community of 1950s–80s homes, newer infill and busy commercial corridors along State Street and University Parkway.",
        "body": """
<h2>From orchards to neighborhoods</h2>
<p>Orem’s neighborhoods, including Cascade, Windsor, Sunset Heights and Orchard, grew quickly in the postwar decades. Many homes are brick or brick-and-siding ramblers and split-levels with finished basements, and a growing number have been expanded or rebuilt.</p>
<h2>Typical claims</h2>
<p>Hail and summer wind are the leading exterior claims in Orem. In winter, ice dams on low-slope additions and frozen pipes in exterior walls cause interior water damage. Commercial properties along State Street and near Utah Valley University see roof and water claims of their own.</p>
<h2>Housing notes</h2>
<ul>
<li><strong>Ramblers with finished basements:</strong> a single water loss can affect two full levels.</li>
<li><strong>Additions:</strong> mismatched rooflines where low-slope sections meet steep-slope roofs and leak under snow.</li>
<li><strong>Retail and office buildings:</strong> flat roofs and rooftop HVAC units exposed to hail.</li>
</ul>
<h2>What to check in your estimate</h2>
<p>Basement finishes, flooring continuity and the transition between old and new roof sections are common points of disagreement on Orem claims.</p>
""",
        "faqs": [
            ("How do I know if hail damaged my roof?", "Look for dents on vents, gutters and downspouts, damaged window screens and granule loss. A professional inspection can confirm functional damage."),
            ("Can you review the estimate before I agree to it?", "Yes. An estimate review is often the best first step."),
        ],
    },
    {
        "slug": "lehi", "city": "Lehi", "county": "Utah County", "region": "Utah Valley",
        "near": ["orem", "sandy", "provo"],
        "perils": ["Hail", "Wind", "Wildfire (foothills)", "Construction defects vs. damage", "Water losses"],
        "lede": "One of Utah’s fastest-growing cities, Lehi sits at the north end of Utah Valley with tech campuses, master-planned communities on Traverse Mountain and older homes near Main Street.",
        "body": """
<h2>Rapid growth, newer homes</h2>
<p>Lehi has grown from a farming town into a center of the Silicon Slopes tech corridor. Traverse Mountain, Holbrook Farms, Ivory Ridge and the neighborhoods near Thanksgiving Point are filled with homes built since the early 2000s, many with stucco, stone veneer and complex roofs.</p>
<h2>Typical claims</h2>
<ul>
<li><strong>Hail and wind:</strong> storms moving through the Point of the Mountain area, which is also known for strong winds.</li>
<li><strong>Wildfire smoke and brush fires:</strong> foothill neighborhoods border open hillsides.</li>
<li><strong>Water losses:</strong> supply line and appliance leaks in newer homes, frequently in second-floor laundry rooms.</li>
</ul>
<h2>New homes, new questions</h2>
<p>With newer construction, carriers sometimes argue that damage is really a construction defect or wear rather than storm damage. Careful documentation of the storm, the damage pattern and the date of loss helps separate the two.</p>
<h2>What to check in your estimate</h2>
<p>Stucco and stone veneer matching, multi-level roof access and HOA requirements for exterior materials are frequent gaps in Lehi claims.</p>
""",
        "faqs": [
            ("My HOA requires a specific shingle color. Does that affect my claim?", "It can affect matching and replacement scope. Share the HOA requirements with us when we review your estimate."),
            ("My builder warranty and insurance both might apply. What do I do?", "Builder warranties and insurance cover different things. Notify both if you’re unsure, and keep documentation."),
        ],
    },
    {
        "slug": "ogden", "city": "Ogden", "county": "Weber County", "region": "Northern Wasatch",
        "near": ["layton", "logan", "salt-lake-city"],
        "perils": ["Canyon wind", "Heavy snow", "Ice dams", "Hail", "Older-home water losses"],
        "lede": "Railroad history, historic 25th Street and a bench that faces the full force of Weber Canyon winds give Ogden claims a character of their own.",
        "body": """
<h2>Historic homes and a windy bench</h2>
<p>Ogden is the county seat of Weber County. The Jefferson Avenue and Eccles Avenue historic districts hold Victorian and early 1900s homes, while the East Bench and neighborhoods near Weber State University sit higher and closer to the mountains. Downslope winds funneling out of Weber Canyon can be intense, and the city sees significant snowfall.</p>
<h2>Typical claims</h2>
<ul>
<li><strong>Wind:</strong> shingles, siding, fences and trees damaged during canyon wind events.</li>
<li><strong>Snow and ice:</strong> ice dams on older homes and snow-load damage to porches, carports and outbuildings.</li>
<li><strong>Water:</strong> freeze-related pipe bursts in older homes with limited insulation.</li>
<li><strong>Hail:</strong> summer storms moving along the northern Wasatch Front.</li>
</ul>
<h2>Housing notes</h2>
<p>Historic homes in Ogden often have plaster walls, ornate trim, slate or older roofing and masonry that needs specialized repair. Estimates that use modern standard materials can fall short.</p>
<h2>Ogden Valley</h2>
<p>We also serve Huntsville, Eden and the Ogden Valley, where cabins and resort-area homes face mountain snow loads and freeze risk.</p>
""",
        "faqs": [
            ("Is my historic home’s plaster covered at replacement cost?", "Replacement cost generally means like kind and quality. Whether that means plaster or drywall depends on the policy and the facts. It’s a common appraisal issue."),
            ("Do you cover Ogden Valley cabins?", "Yes, including Huntsville, Eden and Liberty."),
        ],
    },
    {
        "slug": "layton", "city": "Layton", "county": "Davis County", "region": "Northern Wasatch",
        "near": ["ogden", "salt-lake-city", "logan"],
        "perils": ["Canyon wind", "Fallen trees", "Hail", "Ice dams", "Water losses"],
        "lede": "Davis County’s largest city sits in the path of the powerful east winds that have twice in recent memory torn through the county, damaging roofs, fences and thousands of trees.",
        "body": """
<h2>In the windstorm corridor</h2>
<p>Layton, along with Kaysville, Fruit Heights, Farmington and Centerville, lies beneath the steep western face of the Wasatch. On December 1, 2011, and again on September 8, 2020, downslope winds with hurricane-force gusts swept through Davis County, toppling trees, peeling roofs and damaging fences and outbuildings across thousands of properties.</p>
<h2>Typical claims</h2>
<ul>
<li><strong>Wind:</strong> roof, siding, gutter and fence damage, often across entire neighborhoods.</li>
<li><strong>Trees:</strong> mature trees falling onto homes, cars and outbuildings, with removal and debris costs.</li>
<li><strong>Hail and summer storms:</strong> roof and exterior damage.</li>
<li><strong>Winter:</strong> ice dams and frozen pipes, especially in East Layton homes nearer the mountains.</li>
</ul>
<h2>Housing notes</h2>
<p>Layton neighborhoods range from 1960s–70s homes near Hill Air Force Base and the original town center to newer subdivisions in East Layton. Many homes have vinyl or aluminum siding and wood fences that are hard to match after wind damage.</p>
<h2>What to check in your estimate</h2>
<p>Full-elevation siding replacement where pieces can’t be matched, complete fence runs and tree removal and debris costs are the most frequent gaps in Layton wind claims.</p>
""",
        "faqs": [
            ("My neighbor got a new roof after the windstorm but I didn’t. Why?", "Every claim is evaluated on its own damage and policy. Documentation matters. An estimate review can show whether your claim was scoped fully."),
            ("Are fences covered after a windstorm?", "Many policies cover fences as other structures, subject to limits and deductibles."),
        ],
    },
    {
        "slug": "st-george", "city": "St. George", "county": "Washington County", "region": "Southern Utah",
        "near": ["cedar-city", "provo", "salt-lake-city"],
        "perils": ["Flash flooding", "Monsoon wind", "Water losses", "Fire", "Wildfire (WUI)"],
        "lede": "Red rock, desert heat and booming growth define St. George. Its stucco-and-tile homes, monsoon storms and flash floods create claims unlike anywhere else in the state.",
        "body": """
<h2>Desert growth and its risks</h2>
<p>St. George is the county seat of Washington County and one of the fastest-growing areas in the country. Neighborhoods such as Bloomington, Little Valley, Green Valley, Sunbrook and Dixie Downs are dominated by stucco homes with concrete tile roofs, along with a large number of retirement and second-home communities.</p>
<h2>Typical claims</h2>
<ul>
<li><strong>Monsoon storms:</strong> late-summer thunderstorms bring intense wind, occasional hail and sudden downpours that can damage tile roofs and stucco.</li>
<li><strong>Flash flooding:</strong> in January 2005, the Santa Clara and Virgin rivers flooded and destroyed homes in the area. Flood damage is generally excluded from homeowners policies and requires separate flood insurance.</li>
<li><strong>Water losses:</strong> supply line and water heater failures, often in seasonal homes left empty for long periods.</li>
<li><strong>Brush fires:</strong> neighborhoods on the edge of open desert face wildfire exposure.</li>
</ul>
<h2>Housing notes</h2>
<p>Concrete tile roofs are durable but break when walked on and can be hard to match. Stucco repairs need careful blending of texture and color. Both are frequent appraisal issues.</p>
<h2>What to check in your estimate</h2>
<p>Tile breakage during repairs, underlayment replacement beneath tile, stucco matching and HOA architectural requirements are the most common gaps in St. George claims.</p>
""",
        "faqs": [
            ("Is flash flood damage covered by homeowners insurance?", "Generally not. Flood is usually excluded and requires a separate flood policy. Water from a burst pipe is a different matter and is often covered."),
            ("My tile roof was damaged during the adjuster’s inspection. What now?", "Document it right away and report it in writing. Damage caused during an inspection should be addressed separately from the storm claim."),
        ],
    },
    {
        "slug": "logan", "city": "Logan", "county": "Cache County", "region": "Northern Utah",
        "near": ["ogden", "layton", "park-city"],
        "perils": ["Extreme cold", "Frozen pipes", "Snow load", "Hail", "Ice dams"],
        "lede": "Cache Valley’s cold winters and university town housing make frozen pipes, snow load and ice dams the claims Logan property owners know best.",
        "body": """
<h2>A cold valley</h2>
<p>Logan is the county seat of Cache County and home to Utah State University. The valley is known for cold winter temperatures and inversions, and its neighborhoods, including the Island, Adams, Woodruff, Hillcrest and Bridger, hold a mix of historic homes, student rentals and newer subdivisions.</p>
<h2>Typical claims</h2>
<ul>
<li><strong>Frozen pipes:</strong> extended cold snaps burst pipes in exterior walls, crawlspaces and unheated areas.</li>
<li><strong>Snow load:</strong> during heavy winters, carports, porches, barns and older roofs can fail.</li>
<li><strong>Ice dams:</strong> on older homes with limited attic insulation and ventilation.</li>
<li><strong>Hail:</strong> summer storms moving through Cache Valley.</li>
</ul>
<h2>Housing notes</h2>
<p>Historic Logan homes often have plaster interiors, older masonry and complex additions. Agricultural properties in the surrounding valley add barns, shops and outbuildings with their own coverage questions.</p>
<h2>What to check in your estimate</h2>
<p>Hidden water damage inside walls and under floors, drying costs in cold weather and structural repairs after snow load are frequent gaps in Logan claims.</p>
""",
        "faqs": [
            ("My pipes froze while I was on vacation. Is that covered?", "Often, if you took reasonable steps to maintain heat. Policies may limit coverage for vacant or unheated homes. Review the conditions in your policy."),
            ("Do you handle barn and shop claims?", "Yes, when they’re insured under a farm or homeowners policy. We value outbuildings along with the main dwelling."),
        ],
    },
    {
        "slug": "park-city", "city": "Park City", "county": "Summit County", "region": "Mountain Resort Areas",
        "near": ["salt-lake-city", "sandy", "logan"],
        "perils": ["Snow load", "Ice dams", "Frozen pipes", "Wildfire", "High-value finishes"],
        "lede": "At roughly 7,000 feet, Park City homes and condos carry some of Utah’s heaviest snow loads, and their high-end finishes and short-term rental use make claims complex.",
        "body": """
<h2>Mountain town, mountain claims</h2>
<p>Park City, mostly in Summit County, includes historic Old Town miners’ homes, ski-in condos near the resorts, and larger homes in Park Meadows, Thaynes Canyon and Prospector. Elevation, deep snow and long winters shape nearly every claim.</p>
<h2>Typical claims</h2>
<ul>
<li><strong>Snow load and ice dams:</strong> heavy snow on roofs and decks, with ice dams forcing water into walls and ceilings.</li>
<li><strong>Frozen pipes:</strong> in second homes and rentals left vacant between stays.</li>
<li><strong>Wildfire:</strong> forested hillsides and canyons bring wildfire and smoke exposure in summer.</li>
<li><strong>Condo losses:</strong> water damage affecting several units, with HOA and unit-owner coverage overlapping.</li>
</ul>
<h2>Housing notes</h2>
<p>Many Park City homes feature custom timber framing, stone, metal roofing, radiant heating and luxury finishes. Labor and access costs are higher in mountain communities, and estimates that use valley pricing often fall short.</p>
<h2>What to check in your estimate</h2>
<p>Mountain labor and travel costs, custom materials, snow removal for access and short-term rental income questions are frequent gaps in Park City claims.</p>
""",
        "faqs": [
            ("Do you account for higher mountain construction costs?", "Yes. We price repairs with labor and material costs that reflect working in Summit and Wasatch counties."),
            ("My rental unit lost bookings during repairs. Can that be included?", "If your policy covers fair rental value or business income and the amount is disputed, it can be part of the appraisal."),
        ],
    },
    {
        "slug": "cedar-city", "city": "Cedar City", "county": "Iron County", "region": "Southern Utah",
        "near": ["st-george", "provo", "salt-lake-city"],
        "perils": ["Wildfire", "Flash flooding", "Wind", "Hail", "Frozen pipes"],
        "lede": "Cedar City sits between desert and mountains, with Southern Utah University, a growing industrial base and nearby cabin country that saw major wildfire losses in 2017.",
        "body": """
<h2>Between desert and mountain</h2>
<p>Cedar City is the largest city in Iron County. At about 5,800 feet, it gets more winter weather than St. George, and its location at the mouth of Cedar Canyon means flash floods and strong winds. Nearby Brian Head and Cedar Mountain hold cabins and resort homes.</p>
<h2>Typical claims</h2>
<ul>
<li><strong>Wildfire:</strong> the 2017 Brian Head Fire destroyed homes and cabins in the mountains east of town and burned for weeks.</li>
<li><strong>Flash flooding:</strong> summer monsoon storms can send water and debris out of Cedar Canyon and nearby washes. Flood is generally excluded under standard policies.</li>
<li><strong>Wind and hail:</strong> spring and summer storms.</li>
<li><strong>Freeze:</strong> burst pipes in cabins and homes during cold snaps.</li>
</ul>
<h2>Housing notes</h2>
<p>Cedar City has older homes near Main Street, newer subdivisions on the west side, student rentals near SUU and mountain cabins that may be accessible only part of the year. Cabin claims often involve delayed discovery of damage.</p>
<h2>What to check in your estimate</h2>
<p>Remote access costs for mountain cabins, smoke damage in homes near fire areas and outbuilding values are frequent gaps in Iron County claims.</p>
""",
        "faqs": [
            ("Do you serve Brian Head and Cedar Mountain cabins?", "Yes. We travel to mountain properties throughout southern Utah."),
            ("How do I prove when cabin damage happened?", "Weather records, utility usage, visitor logs and photos from your last visit can help establish the date of loss."),
        ],
    },
]
