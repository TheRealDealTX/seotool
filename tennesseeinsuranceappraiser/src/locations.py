"""Tennessee location pages. Local detail is specific to each city.

Fields: slug, city, county, division (Grand Division), perils, near, lede, housing, body, faqs.
"""

LOCATIONS = [
    {
        "slug": "nashville", "city": "Nashville", "county": "Davidson County", "division": "Middle Tennessee",
        "perils": ["Tornadoes", "Hail", "Straight-line wind", "Burst pipes", "Tree strikes"],
        "near": ["franklin", "murfreesboro", "clarksville"],
        "housing": "Craftsman bungalows, tall-and-skinny infill, Gulch high-rises, 1960s ranches",
        "lede": "From East Nashville bungalows to Gulch condo towers, Metro Nashville’s housing changes block by block — and so do its claims. We value storm, water and fire losses across Davidson County.",
        "body": """
<h2>A city that keeps rebuilding</h2>
<p>Nashville has been hit hard more than once. The April 1998 tornado tore through downtown and East Nashville. The March 3, 2020 EF3 tornado crossed North Nashville, Germantown, East Nashville, Donelson and Hermitage in the middle of the night before continuing into Wilson County. In December 2023, another tornado struck Madison and continued toward Hendersonville. Each event left thousands of roof, siding, window and tree claims — and plenty of disputes about scope and price.</p>
<h2>Housing that complicates estimates</h2>
<p>Metro Nashville’s building boom created a patchwork. A street in Sylvan Park or Inglewood can hold a 1925 bungalow with plaster walls and original heart-pine floors next to a brand-new “tall and skinny” with fiber-cement siding and a low-slope roof. Downtown, The Gulch and SoBro add condo towers where the association’s master policy and each owner’s HO-6 split responsibility. Bellevue, Antioch and Donelson bring brick ranches and split-levels from the 1960s and 1970s.</p>
<h2>Disputes we see in Davidson County</h2>
<ul>
<li>Plaster-and-lath interiors priced as modern drywall.</li>
<li>Historic overlay requirements in neighborhoods such as Edgefield, Lockeland Springs and Belmont-Hillsboro left out of the scope.</li>
<li>Low-slope membrane roofs on infill homes estimated as if they were shingles.</li>
<li>Condo water losses where the source unit and the association disagree on responsibility.</li>
<li>Post-tornado pricing that doesn’t reflect the surge in contractor rates.</li>
</ul>
<h2>Where we work in Nashville</h2>
<p>East Nashville, Germantown, The Nations, Sylvan Park, 12 South, Green Hills, Belle Meade, Donelson, Hermitage, Madison, Inglewood, Bellevue, Antioch, Whites Creek and Bordeaux — plus Goodlettsville, Hendersonville and Mt. Juliet just outside the county line.</p>
""",
        "faqs": [
            ("My house is in a historic overlay. Will that affect the claim?", "It can. Historic and conservation overlays in Nashville may require approved materials or methods. When those requirements raise repair costs, ordinance-or-law coverage may be relevant."),
            ("Was the May 2010 flood something appraisal could help with?", "Rising floodwater is excluded under standard homeowner policies and is covered by flood insurance, which has its own claim and appeal process. Appraisal under a homeowner policy applies to covered perils such as wind, hail and sudden water damage."),
        ],
    },
    {
        "slug": "memphis", "city": "Memphis", "county": "Shelby County", "division": "West Tennessee",
        "perils": ["Derechos", "Ice storms", "Tornadoes", "Frozen pipes", "Tree strikes"],
        "near": ["jackson", "nashville", "franklin"],
        "housing": "Midtown four-squares, Tudor revivals, East Memphis ranches, suburban brick",
        "lede": "Memphis claims are shaped by big trees, older homes and wild weather off the river. We value derecho, ice storm, tornado and freeze losses across Shelby County and its suburbs.",
        "body": """
<h2>Storms Memphians remember</h2>
<p>On July 22, 2003, a derecho swept across the Mississippi River and into Memphis with hurricane-strength gusts. Locals nicknamed it “Hurricane Elvis.” Hundreds of thousands of customers lost power, and the tree and roof damage took weeks to clear. More recently, ice storms in February 2022 and February 2023 brought down heavy limbs across Midtown and East Memphis, and the January 2024 freeze split pipes in homes, apartments and businesses throughout the county.</p>
<h2>Old trees, older homes</h2>
<p>Memphis has one of the most impressive urban tree canopies in the South. Willow oaks and pin oaks line Central Gardens, Chickasaw Gardens and Cooper-Young, and they shed massive limbs in wind and ice. Many of the homes beneath them date to the 1910s–1940s: brick four-squares, Tudor revivals and bungalows with plaster walls, slate or clay-tile accents and wood windows that standard estimates rarely price correctly.</p>
<h2>Claims we see in Shelby County</h2>
<ul>
<li>Tree strikes priced without crane access on tight Midtown lots.</li>
<li>Ice-damaged gutters and fascia patched instead of replaced in matching runs.</li>
<li>Freeze-related water losses in apartment complexes affecting multiple units.</li>
<li>Commercial roof damage on warehouses and distribution buildings near the airport and Lamar Avenue.</li>
<li>Matching disputes on brick and masonry repairs.</li>
</ul>
<h2>Earthquake coverage note</h2>
<p>Shelby County sits near the New Madrid Seismic Zone. Standard homeowner policies exclude earth movement, and earthquake coverage is usually a separate endorsement with its own percentage deductible. If you carry it, our <a href="/tennessee-claim-tools/percentage-deductible-calculator/">percentage deductible calculator</a> shows what that deductible means in dollars.</p>
<h2>Where we work</h2>
<p>Midtown, Cooper-Young, Central Gardens, East Memphis, Harbor Town, Whitehaven, Frayser, Raleigh, Hickory Hill and Cordova, plus Germantown, Collierville, Bartlett, Arlington, Lakeland and Millington.</p>
""",
        "faqs": [
            ("Do I need to get my own estimate after an ice storm?", "It helps. After a citywide event, adjusters work fast and estimates often miss items. An independent estimate gives you something concrete to compare."),
            ("My apartment complex had dozens of burst pipes. Can one appraisal cover them all?", "Usually yes. A commercial or multifamily appraisal can cover all affected units under the same claim, with the award broken out by building or unit if needed."),
        ],
    },
    {
        "slug": "knoxville", "city": "Knoxville", "county": "Knox County", "division": "East Tennessee",
        "perils": ["Hail", "Severe thunderstorms", "Ice & snow", "Tree strikes", "Water losses"],
        "near": ["sevierville-gatlinburg", "chattanooga", "johnson-city"],
        "housing": "Victorian homes, mid-century ranches, hillside builds, student rentals",
        "lede": "Knoxville’s ridges and valleys funnel storms and complicate every roof job. We value hail, wind, ice and water losses across Knox County, from Fourth and Gill to Farragut.",
        "body": """
<h2>Ridge-and-valley weather</h2>
<p>Knoxville sits in the Tennessee Valley between the Cumberland Plateau and the Smokies. Strong spring thunderstorms bring hail and damaging wind, while winter can deliver snow and ice that settle on north-facing slopes for days. The terrain matters: a storm can damage roofs along one ridge and barely touch the next valley, which makes a precise date-of-loss and storm-location record especially important here.</p>
<h2>Housing across Knox County</h2>
<p>Fourth and Gill and Old North Knoxville hold some of the state’s best Victorian and Queen Anne homes, with complex rooflines, decorative trim and wood siding. Sequoyah Hills and Holston Hills have mid-century homes on wooded lots. West Knoxville, Bearden, Farragut and Hardin Valley add large suburban homes and HOA communities, while the Fort Sanders area near the University of Tennessee is full of student rentals and small apartment buildings.</p>
<h2>What we see in Knoxville claims</h2>
<ul>
<li>Steep, cut-up Victorian roofs priced without proper steep or high charges.</li>
<li>Decorative millwork and wood siding replaced with generic profiles.</li>
<li>Hillside access and staging costs left out of the scope.</li>
<li>Student-rental and landlord policies with different settlement terms.</li>
<li>Hail damage disputes when a neighborhood saw several storms in a short span.</li>
</ul>
<h2>Where we work</h2>
<p>Downtown and the Old City, Fourth and Gill, Old North, Fountain City, Halls, Powell, North Knoxville, South Knoxville, Island Home, Sequoyah Hills, Bearden, West Hills, Cedar Bluff, Hardin Valley, Farragut and Karns.</p>
""",
        "faqs": [
            ("My Victorian house has custom trim. Will the insurer pay to match it?", "Policies generally pay to repair with materials of like kind and quality. Custom millwork can be expensive to reproduce, and documenting the original profile helps establish the cost."),
            ("Can you handle claims on student rental properties near campus?", "Yes. Rental properties are often insured on dwelling-fire or commercial forms, and we review the policy before valuing the loss."),
        ],
    },
    {
        "slug": "chattanooga", "city": "Chattanooga", "county": "Hamilton County", "division": "East Tennessee",
        "perils": ["Tornadoes", "Hail", "Tree strikes", "Landslide-prone slopes", "Water losses"],
        "near": ["knoxville", "cookeville", "nashville"],
        "housing": "Mountain homes, St. Elmo bungalows, North Shore infill, lakeside builds",
        "lede": "Chattanooga’s mountains, river and history create claims you won’t see elsewhere. We value tornado, hail and tree losses across Hamilton County, from Signal Mountain to Ooltewah.",
        "body": """
<h2>Two outbreaks the city won’t forget</h2>
<p>On April 27, 2011, a historic tornado outbreak sent violent tornadoes across the Chattanooga area, including Apison and other communities in Hamilton County. On Easter Sunday night in April 2020, an EF3 tornado cut through East Brainerd and Ooltewah, damaging hundreds of homes and businesses. Both events showed how quickly a suburban neighborhood can be reduced to framing and debris.</p>
<h2>Building on slopes</h2>
<p>Lookout Mountain, Signal Mountain, Missionary Ridge and Raccoon Mountain give Chattanooga its views — and give contractors headaches. Steep driveways, retaining walls and limited staging areas raise the cost of nearly every repair. Roofs on hillside homes are often taller on the downhill side, triggering high-roof charges that are easy to miss. Wet seasons also bring slope movement, which is usually excluded as earth movement, so separating covered storm damage from excluded settlement matters.</p>
<h2>Neighborhood character</h2>
<p>St. Elmo and Highland Park hold early 20th-century bungalows and four-squares. North Shore and Riverview mix historic homes with modern infill and condos. Hixson, Red Bank, East Brainerd and Ooltewah are filled with suburban subdivisions, while lakeside homes along Chickamauga Lake bring docks and boathouses into the claim.</p>
<h2>Common Hamilton County disputes</h2>
<ul>
<li>High-roof, steep and access charges omitted on hillside homes.</li>
<li>Docks and boathouses excluded or underpriced.</li>
<li>Earth-movement exclusions raised against storm-related damage.</li>
<li>Tornado repairs scoped as patches when framing is compromised.</li>
</ul>
<h2>Where we work</h2>
<p>Downtown, North Shore, St. Elmo, Highland Park, Brainerd, East Brainerd, Ooltewah, Collegedale, Hixson, Red Bank, Signal Mountain, Lookout Mountain, East Ridge, Soddy-Daisy and Harrison.</p>
""",
        "faqs": [
            ("My retaining wall was damaged when a tree fell. Is that covered?", "Retaining walls are often covered under other structures, subject to the policy’s terms. If the damage resulted from a covered peril like a falling tree, it’s usually part of the claim."),
            ("The carrier says my cracks are from settling, not the storm. What now?", "Earth movement and settling are commonly excluded. If you believe the storm caused the damage, an engineer’s opinion is often the deciding evidence. That’s a coverage issue first, then an amount issue."),
        ],
    },
    {
        "slug": "clarksville", "city": "Clarksville", "county": "Montgomery County", "division": "Middle Tennessee",
        "perils": ["Tornadoes", "Hail", "Straight-line wind", "Frozen pipes", "Siding damage"],
        "near": ["nashville", "franklin", "murfreesboro"],
        "housing": "Newer subdivisions, military rentals, historic downtown homes",
        "lede": "One of Tennessee’s fastest-growing cities, Clarksville sees tornado and hail claims on thousands of newer homes. We value storm losses across Montgomery County.",
        "body": """
<h2>A city that knows tornadoes</h2>
<p>Downtown Clarksville was struck by a tornado in January 1999 that damaged the courthouse, Austin Peay State University and blocks of historic buildings. On December 9, 2023, a strong tornado tore through northern Clarksville neighborhoods, damaging or destroying hundreds of homes. The pattern is familiar: fast-moving storms hitting dense subdivisions where every home has similar construction and every claim tends to raise the same disputes.</p>
<h2>Newer homes, specific problems</h2>
<p>Much of Clarksville was built in the last twenty-five years. Sango, St. Bethlehem, Hilldale and the subdivisions along Highway 48 and Trenton Road are full of vinyl-sided, architectural-shingle homes. That sounds simple, but matching discontinued siding colors and shingle lines is one of the most common reasons claims come up short. Many homes are rentals owned by investors or leased to military families from nearby Fort Campbell, which brings landlord policies and absentee owners into the picture.</p>
<h2>What we see in Montgomery County claims</h2>
<ul>
<li>Vinyl siding replaced on one elevation even though the color is discontinued.</li>
<li>Roof repairs approved where the shingle line no longer exists.</li>
<li>Rental property claims delayed because the owner lives out of town.</li>
<li>Fence, shed and outbuilding damage left out of tornado estimates.</li>
</ul>
<h2>Where we work</h2>
<p>Downtown Clarksville, Sango, St. Bethlehem, New Providence, Hilldale, Woodlawn, Cunningham, Palmyra and the subdivisions off Exit 1, Exit 4 and Exit 11.</p>
""",
        "faqs": [
            ("I’m stationed away from Clarksville. Can you help with my rental property claim?", "Yes. We can inspect, document and coordinate with your property manager or tenant, and keep you updated remotely."),
            ("The insurer will only replace siding on one side of my house. Is that normal?", "It’s a common position, but matching is a frequent dispute. If the replacement siding can’t reasonably match, policy language and the facts may support more."),
        ],
    },
    {
        "slug": "murfreesboro", "city": "Murfreesboro", "county": "Rutherford County", "division": "Middle Tennessee",
        "perils": ["Tornadoes", "Hail", "Straight-line wind", "Water losses", "Roof damage"],
        "near": ["nashville", "franklin", "cookeville"],
        "housing": "Suburban subdivisions, HOA communities, student housing, historic homes",
        "lede": "Rutherford County’s rapid growth means thousands of newer homes and HOA communities. We value hail, wind and tornado losses across Murfreesboro, Smyrna and La Vergne.",
        "body": """
<h2>The 2009 tornado and what came after</h2>
<p>On April 10, 2009, an EF4 tornado tracked across southern Murfreesboro, destroying homes in the Sunnyside and Blackman areas. Since then, the county has added tens of thousands of residents, and with them come neighborhoods that spring storms continue to test. Hail is a frequent visitor, and broad straight-line wind events can damage entire subdivisions at once.</p>
<h2>Subdivision claims at scale</h2>
<p>When a hailstorm crosses Blackman, Siegel or the developments off Veterans Parkway, it can damage hundreds of similar homes in a single afternoon. Adjusters move quickly, and the same omissions repeat across claims: undercounted squares, missing ridge vent and starter, siding on only one elevation, and gutters left off entirely. HOA communities add design rules that can require specific colors and materials for repairs.</p>
<h2>Rutherford County properties we value</h2>
<ul>
<li>Single-family homes in Blackman, Siegel, Barfield and Rockvale.</li>
<li>HOA townhome and condo communities.</li>
<li>Student rentals near Middle Tennessee State University.</li>
<li>Historic homes near the downtown square.</li>
<li>Warehouses and distribution buildings in Smyrna and La Vergne.</li>
</ul>
<h2>Where we work</h2>
<p>Murfreesboro, Smyrna, La Vergne, Christiana, Rockvale, Eagleville, Lascassas and Walter Hill.</p>
""",
        "faqs": [
            ("Our HOA requires specific shingle colors. Does insurance pay for that?", "HOA rules aren’t policy terms, but they can affect what counts as a reasonable like-kind-and-quality repair. Documenting the requirement early helps."),
            ("My neighbors got full roofs and I got a repair. Why?", "Every claim is adjusted separately, and results vary by adjuster and by the evidence documented. An independent inspection can show whether your roof meets the same standard."),
        ],
    },
    {
        "slug": "franklin", "city": "Franklin", "county": "Williamson County", "division": "Middle Tennessee",
        "perils": ["Hail", "Straight-line wind", "Tornadoes", "Water losses", "High-value roofs"],
        "near": ["nashville", "murfreesboro", "clarksville"],
        "housing": "Custom homes, historic downtown houses, slate and cedar roofs, HOAs",
        "lede": "Williamson County’s high-value homes and specialty materials make accurate valuation essential. We appraise storm, water and fire losses in Franklin, Brentwood and surrounding communities.",
        "body": """
<h2>Where specialty materials meet storm season</h2>
<p>Franklin and Brentwood are home to some of the highest-value residential property in Tennessee. Custom homes in Westhaven, Fieldstone Farms, Governors Club and Brentwood’s estate neighborhoods often feature slate, cedar shake, copper flashing, standing-seam metal accents, stone veneer and custom windows. A standard estimate built for builder-grade materials simply doesn’t fit these homes.</p>
<h2>Historic downtown Franklin</h2>
<p>The historic district around Main Street and the neighborhoods nearby include homes from the 1800s with original brick, heart-pine floors and wood windows. Repairs may need historic commission approval, which can affect materials and cost. Those requirements are easy to miss in a fast storm estimate.</p>
<h2>Common Williamson County disputes</h2>
<ul>
<li>Slate and cedar roofs scoped as repairs when the material is no longer available.</li>
<li>Copper and specialty metals priced at standard steel rates.</li>
<li>Custom windows and doors replaced with off-the-shelf equivalents.</li>
<li>Large interior water losses involving premium finishes.</li>
<li>Matching problems across expansive, continuous flooring and stone.</li>
</ul>
<h2>Where we work</h2>
<p>Franklin, Brentwood, Nolensville, Spring Hill, Thompson’s Station, Arrington, Leiper’s Fork and Fairview, as well as Westhaven, Fieldstone Farms, McKay’s Mill and Cool Springs.</p>
""",
        "faqs": [
            ("My policy is a high-value homeowner form. Does that change appraisal?", "High-value forms often include broader settlement terms, such as extended replacement cost or cash-out options. The appraisal process is similar, but the policy terms can affect how the award is paid."),
            ("Can slate roofs be repaired after hail?", "Sometimes. It depends on the slate’s condition, availability and whether repairs would damage surrounding pieces. Specialist assessment is important."),
        ],
    },
    {
        "slug": "jackson", "city": "Jackson", "county": "Madison County", "division": "West Tennessee",
        "perils": ["Tornadoes", "Ice storms", "Straight-line wind", "Hail", "Commercial roofs"],
        "near": ["memphis", "nashville", "clarksville"],
        "housing": "Historic downtown, mid-century brick, newer north-side subdivisions",
        "lede": "Jackson has been struck by major tornadoes more than once in the last few decades. We value tornado, wind, ice and hail losses for homes and businesses across Madison County.",
        "body": """
<h2>A city shaped by tornadoes</h2>
<p>A powerful tornado struck downtown Jackson on May 4, 2003, damaging hundreds of buildings, including historic churches and businesses. On February 5, 2008, during the Super Tuesday outbreak, another tornado tore through Jackson and heavily damaged Union University’s campus. Downtown and neighboring areas have rebuilt, but the experience shaped how local property owners think about storms and coverage.</p>
<h2>West Tennessee weather</h2>
<p>Jackson sits between Memphis and Nashville on flat to rolling land where strong storm systems can maintain intensity. Ice storms are also a recurring risk, and their effect on trees and power lines can be significant. Hail and straight-line wind regularly affect roofs, siding and commercial buildings along the Highway 45 Bypass and Interstate 40.</p>
<h2>Properties we value in Madison County</h2>
<ul>
<li>Historic homes near downtown and the Lambuth area.</li>
<li>Mid-century brick ranches throughout central Jackson.</li>
<li>Newer subdivisions on the north side of the city.</li>
<li>Churches, schools and community buildings.</li>
<li>Retail and industrial buildings along major corridors.</li>
</ul>
<h2>Where we work</h2>
<p>Jackson, Medon, Pinson, Three Way, Humboldt, Milan, Bells, Henderson, Lexington and surrounding West Tennessee communities.</p>
""",
        "faqs": [
            ("Our church was damaged in a storm. Can you help?", "Yes. Churches often involve specialty finishes, large roofs and unique structures. We value these losses regularly."),
            ("Should I worry about earthquakes in Jackson?", "West Tennessee is near the New Madrid Seismic Zone. Standard policies exclude earthquake damage, so coverage requires a separate endorsement with its own deductible."),
        ],
    },
    {
        "slug": "johnson-city", "city": "Johnson City", "county": "Washington County", "division": "East Tennessee",
        "perils": ["Ice & snow", "Mountain wind", "Hail", "Tree strikes", "Frozen pipes"],
        "near": ["kingsport", "knoxville", "sevierville-gatlinburg"],
        "housing": "Tree Streets homes, mountain-view builds, student rentals, older brick",
        "lede": "Mountain weather, mature trees and a mix of old and new homes shape claims in Johnson City. We value wind, ice, hail and water losses across Washington County and the Tri-Cities.",
        "body": """
<h2>Northeast Tennessee weather</h2>
<p>Johnson City sits in the valley between the Appalachian ridges, where winter storms can bring heavy snow and ice and strong mountain winds funnel through gaps. Spring and summer thunderstorms bring hail and damaging winds. In late September 2024, the remnants of Hurricane Helene caused catastrophic flooding in Unicoi County, Carter County and Washington County. Floodwater is covered by flood insurance rather than homeowner policies, but wind and tree damage from the same storm fall under standard property coverage.</p>
<h2>The Tree Streets and beyond</h2>
<p>Johnson City’s Tree Streets neighborhood is full of early 20th-century homes with deep porches, wood siding and mature trees overhead. East Tennessee State University brings student rentals and small apartment buildings. Newer homes in North Johnson City and the hills toward Boones Creek and Gray offer mountain views but also more exposure to wind and steep-roof charges.</p>
<h2>Common claims we see</h2>
<ul>
<li>Ice-loaded limbs falling on roofs and porches.</li>
<li>Wind damage to shingles and siding on exposed hillside homes.</li>
<li>Frozen pipes in crawlspaces and older homes.</li>
<li>Questions about which Helene-related damage was wind and which was flood.</li>
</ul>
<h2>Where we work</h2>
<p>Johnson City, the Tree Streets, Boones Creek, Gray, Jonesborough, Elizabethton, Erwin, Unicoi, Piney Flats and Limestone.</p>
""",
        "faqs": [
            ("My house had both wind and flood damage from Helene. How does that work?", "Typically the flood policy handles damage from rising water, and the homeowner policy handles wind damage. Separating the two carefully is critical, and an independent valuation can help."),
            ("Do steep roofs cost more to replace?", "Yes. Steep pitches require additional labor and safety equipment, and estimates should include steep-roof charges where they apply."),
        ],
    },
    {
        "slug": "kingsport", "city": "Kingsport", "county": "Sullivan County", "division": "East Tennessee",
        "perils": ["Ice & snow", "Wind", "Hail", "Tree strikes", "Commercial roofs"],
        "near": ["johnson-city", "knoxville", "sevierville-gatlinburg"],
        "housing": "Planned-city neighborhoods, mid-century homes, hillside subdivisions",
        "lede": "Kingsport’s planned neighborhoods and hillside homes face winter ice and summer storms. We value storm, ice and water losses across Sullivan County and the Tri-Cities.",
        "body": """
<h2>A planned city in the mountains</h2>
<p>Kingsport was laid out in the early 20th century as one of the country’s early planned industrial cities, and many of its original neighborhoods still reflect that history. Homes in the Fort Henry, Ridgefields and Highland Park areas range from early 20th-century houses to mid-century ranches. Newer subdivisions climb the surrounding hills toward Colonial Heights and Rock Springs.</p>
<h2>Weather in Sullivan County</h2>
<p>Winter storms bring snow and ice, which weigh down trees and stress older roofs. Spring and summer thunderstorms bring hail and damaging winds. Hillside homes are more exposed to wind, while valley homes often deal with large, mature trees close to structures.</p>
<h2>Claims we value in Kingsport</h2>
<ul>
<li>Ice-damaged trees falling on homes and outbuildings.</li>
<li>Hail and wind damage to shingles, siding and gutters.</li>
<li>Frozen and burst pipes in older homes.</li>
<li>Commercial and industrial roof damage.</li>
</ul>
<h2>Where we work</h2>
<p>Kingsport, Colonial Heights, Rock Springs, Fall Branch, Blountville, Bristol, Bluff City, Church Hill and Mount Carmel.</p>
""",
        "faqs": [
            ("My house is on a steep lot. Will that increase my claim?", "It can affect costs. Difficult access, staging and steep roofs often require additional charges that should be included in the estimate."),
            ("Can you help with commercial claims in Kingsport?", "Yes. We value commercial, industrial and multifamily losses as well as homes."),
        ],
    },
    {
        "slug": "cookeville", "city": "Cookeville", "county": "Putnam County", "division": "Upper Cumberland",
        "perils": ["Tornadoes", "Hail", "Straight-line wind", "Ice", "Rural structures"],
        "near": ["murfreesboro", "nashville", "knoxville"],
        "housing": "Subdivisions, rural homes, student rentals, farm buildings",
        "lede": "The 2020 Cookeville tornado was one of the deadliest in Tennessee’s recent history. We value tornado, hail and wind losses across Putnam County and the Upper Cumberland.",
        "body": """
<h2>March 3, 2020</h2>
<p>Shortly before 2 a.m. on March 3, 2020, an EF4 tornado tore through western Putnam County near Baxter and the west side of Cookeville. It killed 19 people and destroyed or heavily damaged homes across several neighborhoods. Rebuilding took years, and many owners learned the hard way how much detail goes into valuing a total loss — and how easily items can be left out.</p>
<h2>The Upper Cumberland</h2>
<p>Cookeville sits on the Cumberland Plateau’s western edge, in a region of rolling hills, small towns and farmland. Properties range from new subdivisions and student rentals near Tennessee Tech to rural homes with barns, shops and outbuildings. Storms crossing the Plateau can produce hail and strong winds, and winter ice is a regular risk at these elevations.</p>
<h2>Claims we see in Putnam County</h2>
<ul>
<li>Total-loss valuations where the carrier’s replacement cost estimate falls short.</li>
<li>Barns, shops and outbuildings undervalued or omitted.</li>
<li>Hail and wind damage to rural homes and farm buildings.</li>
<li>Student rental and landlord claims near campus.</li>
</ul>
<h2>Where we work</h2>
<p>Cookeville, Baxter, Algood, Monterey, Livingston, Sparta, Gainesboro, Crossville and surrounding Upper Cumberland communities.</p>
""",
        "faqs": [
            ("My house was a total loss. Can appraisal help?", "Yes, if the dispute is about the cost to rebuild. Total-loss valuations involve many components, and an independent estimate often uncovers missing items."),
            ("Are barns and outbuildings covered under my homeowner policy?", "Many homeowner policies cover other structures, but farm buildings may need separate farm coverage. Review your policy to understand what applies."),
        ],
    },
    {
        "slug": "sevierville-gatlinburg", "city": "Sevierville & Gatlinburg", "county": "Sevier County", "division": "East Tennessee",
        "perils": ["Wildfire", "Mountain wind", "Ice & snow", "Tree strikes", "Rental cabin losses"],
        "near": ["knoxville", "johnson-city", "kingsport"],
        "housing": "Log and timber cabins, short-term rentals, resort properties, hillside homes",
        "lede": "Cabins, short-term rentals and mountain homes in Sevier County face wildfire, wind and winter weather. We value losses in Sevierville, Gatlinburg, Pigeon Forge and the Smokies foothills.",
        "body": """
<h2>The 2016 wildfires</h2>
<p>In late November 2016, the Chimney Tops 2 fire was driven by extreme winds out of the Great Smoky Mountains National Park and into Gatlinburg and the surrounding hills. The fires damaged or destroyed thousands of homes, cabins and businesses and took 14 lives. The recovery highlighted the challenges of valuing log and timber construction, resort properties and smoke-damaged buildings that didn’t burn.</p>
<h2>Cabins and short-term rentals</h2>
<p>Sevier County is filled with rental cabins and vacation homes. Many are insured on commercial or dwelling-fire policies rather than standard homeowner forms, with different settlement terms, vacancy provisions and business-income coverage. Log construction, hot tubs, decks, steep driveways and remote locations all affect repair costs.</p>
<h2>Claims we see in Sevier County</h2>
<ul>
<li>Log and timber repairs priced as conventional framing.</li>
<li>Smoke and ash damage to cabins near burned areas.</li>
<li>Wind damage on exposed ridgetop homes.</li>
<li>Frozen pipes in vacant or seasonal rentals.</li>
<li>Access and staging costs for remote properties.</li>
</ul>
<h2>Where we work</h2>
<p>Sevierville, Gatlinburg, Pigeon Forge, Pittman Center, Kodak, Seymour, Wears Valley, Cobbly Nob and the mountain communities around the national park.</p>
""",
        "faqs": [
            ("My rental cabin is insured under a commercial policy. Can you help?", "Yes. Commercial and dwelling-fire policies have different terms, and we review them before valuing the loss."),
            ("Are log homes more expensive to repair?", "Often yes. Log and timber construction requires specialized labor and materials, and estimates should reflect that."),
        ],
    },
]
