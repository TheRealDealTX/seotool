"""Arizona city pages. Local detail is specific to each community.

Fields: slug, city, county, region, housing, perils, near, lede, body (HTML), faqs.
"""

LOCATIONS = [
    {
        "slug": "phoenix", "city": "Phoenix", "county": "Maricopa County", "region": "Valley of the Sun",
        "housing": "Ranch block homes, flat-roof historic districts, tile-roof subdivisions, high-rise condos",
        "perils": ["Monsoon microbursts", "Hail", "Haboobs", "Extreme heat", "Slab leaks"],
        "near": ["glendale", "scottsdale", "mesa"],
        "lede": "From flat-roofed 1930s bungalows in Willo to tile-roofed subdivisions in Laveen and Desert Ridge, Phoenix claims span almost every kind of construction in the state.",
        "body": """
<h2>What shapes Phoenix property claims</h2>
<p>Phoenix is the anchor of Maricopa County, one of the most populous counties in the country, and its housing stock spans nearly a century. Historic districts such as Willo, Encanto-Palmcroft and Coronado mix period revival homes and bungalows with low-slope roofs that rely on foam, rolled or built-up systems. Post-war ranch homes in Maryvale and around North Mountain are often block construction with later tile or shingle roofs. Newer communities in Laveen, Desert Ridge and Ahwatukee Foothills were built almost entirely with stucco and concrete tile.</p>
<h2>Storms that define the Phoenix claim calendar</h2>
<p>Monsoon outflow is the city’s signature peril. The July 5, 2011 haboob buried the metro in dust, and microbursts every summer lift tile, flatten shade structures and drop trees across arterial streets. On October 5, 2010, an unusual autumn storm pelted the Phoenix area with hail and is widely described as the costliest hailstorm in Arizona history. On September 8, 2014, remnants of Hurricane Norbert set a single-day rainfall record at Sky Harbor and flooded freeways.</p>
<p>Heat is a slower peril. In July 2023 Phoenix recorded 31 consecutive days at or above 110°F. Heat does not usually create a claim by itself, but it ages underlayment, foam coatings and plumbing, and that aging becomes the carrier’s argument when a storm finally causes damage.</p>
<h2>Common Phoenix disputes</h2>
<ul>
<li>Foam roof recoat offered when the foam itself is fractured.</li>
<li>Tile roof “spot repair” on underlayment that cannot survive being disturbed.</li>
<li>Slab leaks with access, re-pipe and resulting-damage costs split unclearly.</li>
<li>Condo water losses in Midtown and Downtown towers involving HOA master policies.</li>
<li>Block walls and shade structures omitted from monsoon claims.</li>
</ul>
<h2>Neighborhoods we cover</h2>
<p>Arcadia, Biltmore, North Central, Moon Valley, Paradise Valley Village, Desert Ridge, Ahwatukee Foothills, South Mountain, Laveen, Maryvale, Deer Valley, Willo, Encanto-Palmcroft, Coronado and Downtown, plus neighboring towns across the Valley.</p>
""",
        "faqs": [
            ("Does a flat roof in a Phoenix historic district change my claim?", "It can. Foam and built-up roofs are valued differently from tile, and historic-district rules may affect materials. We scope the actual system on your home."),
            ("Can heat damage be part of a storm claim?", "Wear from heat and age is generally not covered, but storm damage to an aging roof usually is. The fight is often over what the storm did versus what time did."),
            ("Do you inspect in summer?", "Yes. We schedule roof inspections early in the morning during the hottest months for safety and accuracy."),
        ],
    },
    {
        "slug": "tucson", "city": "Tucson", "county": "Pima County", "region": "Southern Arizona",
        "housing": "Adobe and territorial homes, slump-block mid-century, foothills custom homes, master-planned suburbs",
        "perils": ["Monsoon flash flooding", "Microbursts", "Hail", "Hard freezes", "Wildfire near the mountains"],
        "near": ["sierra-vista", "phoenix", "chandler"],
        "lede": "Tucson’s adobe and territorial homes, mid-century slump-block ranches and Catalina Foothills estates each fail differently when a monsoon storm drops off the Santa Catalinas.",
        "body": """
<h2>A city ringed by mountains</h2>
<p>Tucson sits in a basin surrounded by the Santa Catalina, Rincon, Santa Rita and Tucson mountains. Monsoon storms build over those ranges and collapse into the city, sending water racing down washes such as the Rillito, Pantano and Tanque Verde. In July 2006 a severe storm triggered debris flows in Sabino Canyon, and in October 1983 the remnants of Tropical Storm Octave caused some of the worst flooding in the region’s history.</p>
<h2>Housing you only find here</h2>
<p>Central neighborhoods such as Barrio Viejo, Armory Park and El Presidio hold adobe and Sonoran row houses with flat roofs and parapets. Sam Hughes and the Grant–Swan corridor are full of 1930s to 1950s brick and slump-block homes. The Catalina Foothills, Oro Valley and Marana add large custom homes on hillside lots, and the southeast side, including Rita Ranch and Civano, is mostly newer stucco and tile.</p>
<p>Those flat roofs with parapets are a classic source of disputes. Scuppers, canales and parapet caps fail in wind-driven rain, and water entry through a parapet can look like long-term neglect unless the storm damage is carefully documented.</p>
<h2>Freeze and fire</h2>
<p>Tucson rarely freezes hard, which is exactly why the February 2011 freeze caused so many burst pipes in homes with exposed lines. On Mount Lemmon above the city, the 2003 Aspen Fire destroyed much of Summerhaven, a reminder that wildfire risk sits on the city’s northern horizon.</p>
<h2>Areas we cover</h2>
<p>Central Tucson, Sam Hughes, Armory Park, Barrio Viejo, Catalina Foothills, Tanque Verde, Oro Valley, Marana, Dove Mountain, Rita Ranch, Civano, Vail, Sahuarita, Green Valley and the rest of Pima County.</p>
""",
        "faqs": [
            ("My adobe home has a flat roof that leaked in a monsoon. Is it covered?", "If storm wind or debris created the opening that let the rain in, the resulting damage is often covered. Ordinary wear on parapets and roof coatings usually is not. Documentation is everything."),
            ("Is wash flooding covered by homeowners insurance?", "Rising surface water is usually excluded and needs flood insurance. Rain entering through storm-damaged roofs or windows is a different matter."),
            ("Do you cover Green Valley and Sahuarita?", "Yes, along with Vail, Marana, Oro Valley and the rest of Pima County."),
        ],
    },
    {
        "slug": "mesa", "city": "Mesa", "county": "Maricopa County", "region": "East Valley",
        "housing": "1970s–80s tract homes, 55+ communities, manufactured-home parks, foothills custom homes",
        "perils": ["Microbursts", "Hail", "Dust storms", "Water heater & slab leaks", "Brush fire near the foothills"],
        "near": ["gilbert", "chandler", "phoenix"],
        "lede": "Mesa is Arizona’s third-largest city, with a housing mix that runs from 1970s ranch homes and 55+ communities to custom homes against the Usery and Superstition foothills.",
        "body": """
<h2>Mesa’s housing mix</h2>
<p>Mesa grew in waves. Dobson Ranch and much of west Mesa filled in during the 1970s and 1980s with stucco and block homes, many of which are now on their second or third roof. East Mesa added large active-adult communities and manufactured-home and RV resorts that fill with winter visitors. Red Mountain Ranch, Las Sendas and the Usery Pass area added custom homes on desert lots, and Eastmark brought a new master-planned community on the former General Motors proving grounds.</p>
<h2>Storms and losses we see</h2>
<p>East Valley monsoon storms often build over the Superstition Mountains and race west. Microbursts topple palms and eucalyptus, peel tile and rip manufactured-home roofing and skirting. Dust storms follow the same path. Hail is less frequent than wind but heavy when it comes, and it can crack tile and dent cooler housings across whole subdivisions.</p>
<p>Inside the home, water heaters, supply lines and slab leaks are frequent, especially in houses with original plumbing. Seasonal residents may not discover a leak for weeks, which brings the question of long-term seepage into play.</p>
<h2>Manufactured homes and 55+ communities</h2>
<p>Manufactured homes are repaired with different materials and methods than site-built homes, and pricing must reflect that. In age-restricted communities, the HOA may insure some components while the owner insures others. We read both documents before valuing the loss.</p>
<h2>Areas we cover</h2>
<p>Dobson Ranch, downtown Mesa, Lehi, Alta Mesa, Red Mountain Ranch, Las Sendas, Eastmark, Superstition Springs, Leisure World and the communities along the US-60 corridor.</p>
""",
        "faqs": [
            ("Do you handle manufactured-home claims in Mesa?", "Yes. We price manufactured-home repairs with the methods and materials those homes actually use."),
            ("I was away for the summer and found water damage. Can I still claim?", "Report it promptly. Expect questions about when the leak began and about vacancy terms. Evidence such as utility usage can help establish timing."),
            ("Does Mesa require permits for roof replacement?", "Many roofing projects require permits in Mesa. Permit fees and code items are legitimate parts of the repair cost when required."),
        ],
    },
    {
        "slug": "chandler", "city": "Chandler", "county": "Maricopa County", "region": "East Valley",
        "housing": "1990s–2000s master-planned subdivisions, lakeside communities, tech and industrial campuses",
        "perils": ["Microbursts", "Hail", "Dust-driven rain", "Plumbing failures", "Commercial roof damage"],
        "near": ["gilbert", "mesa", "tucson"],
        "lede": "Chandler’s master-planned neighborhoods and its Price Road tech corridor mean residential tile-roof claims and large commercial losses often come from the same storm.",
        "body": """
<h2>Homes built in the boom years</h2>
<p>Much of Chandler was built in the 1990s and 2000s: Ocotillo with its lakes, Fulton Ranch, Cooper Commons, and neighborhoods around downtown Chandler. Stucco walls, concrete tile roofs and HOA architectural guidelines are the norm. Two decades in, many of those roofs are reaching the age when underlayment becomes the central question in any storm claim.</p>
<h2>Matching under HOA rules</h2>
<p>Homeowners associations often require approved tile colors and profiles. If the original tile has been discontinued, replacing part of a roof with a different tile may violate the HOA’s rules and leave a visible patch. That is a matching question the valuation has to address, and it is one of the most common reasons Chandler roof claims end up in appraisal.</p>
<h2>Commercial and industrial property</h2>
<p>The Price Road corridor and the areas around Chandler Airpark hold large office, manufacturing and flex buildings. Low-slope roof systems, rooftop mechanical units and tenant improvements can make a single storm loss substantial. Business income and coinsurance issues often travel with those claims.</p>
<h2>Areas we cover</h2>
<p>Ocotillo, Fulton Ranch, downtown Chandler, Andersen Springs, Cooper Commons, Sun Groves, Sun Lakes and the Price Road and Chandler Airpark business areas.</p>
""",
        "faqs": [
            ("My HOA won’t approve a patch with different tile. What can I do?", "Document the HOA’s written requirements and the availability of matching tile. Those facts support a valuation that reflects what it actually costs to restore a uniform roof."),
            ("Can you handle a claim for a business in Chandler?", "Yes. We value commercial building losses, including roofs, mechanical equipment and tenant improvements."),
            ("Are rooftop solar panels part of a roof claim?", "If they are damaged or must be removed and reinstalled to repair the roof, those costs belong in the estimate."),
        ],
    },
    {
        "slug": "gilbert", "city": "Gilbert", "county": "Maricopa County", "region": "East Valley",
        "housing": "HOA-governed tile-roof subdivisions, agrihood and lake communities, newer infill",
        "perils": ["Microbursts", "Hail", "Fallen trees", "Pool & shade structures", "Water losses"],
        "near": ["chandler", "mesa", "scottsdale"],
        "lede": "Gilbert grew from farm town to one of the largest towns in the country in a few decades, and nearly every neighborhood is HOA-governed tile roofs and stucco.",
        "body": """
<h2>A town of HOAs</h2>
<p>Gilbert’s neighborhoods, including Val Vista Lakes, Power Ranch, Morrison Ranch, Seville and Agritopia, were built under detailed HOA guidelines. That uniformity is attractive until a storm damages part of a block. Matching tile colors, wall finishes and fence styles across a community can drive the cost of repair well beyond the carrier’s first estimate.</p>
<h2>Backyard losses</h2>
<p>Gilbert claims often include the backyard: pools, ramadas, pergolas, shade sails, outdoor kitchens and block walls. These items may fall under other structures coverage with its own limit, and they are frequently left off estimates entirely. We scope them separately and price them at what Gilbert contractors actually charge.</p>
<h2>Storm patterns</h2>
<p>Monsoon cells drifting off the San Tan and Superstition mountains bring microbursts and, in some years, hail. Mature shade trees planted when subdivisions were new are now large enough to cause real damage when they fall.</p>
<h2>Areas we cover</h2>
<p>Val Vista Lakes, Power Ranch, Morrison Ranch, Seville, Agritopia, Lyons Gate, Heritage District, Cooley Station and the surrounding communities, plus Queen Creek and San Tan Valley in neighboring Pinal County.</p>
""",
        "faqs": [
            ("Is my pool equipment covered after a storm?", "Many policies cover pool equipment and structures under other structures or dwelling coverage. We include it in the valuation when it is damaged."),
            ("Do you work in Queen Creek and San Tan Valley?", "Yes. We serve the southeast Valley, including communities across the line in Pinal County."),
            ("Should my HOA and I file separate claims?", "It depends on who owns and insures each component. Read your CC&Rs and both policies; we can help sort out which items belong to which claim."),
        ],
    },
    {
        "slug": "scottsdale", "city": "Scottsdale", "county": "Maricopa County", "region": "Valley of the Sun",
        "housing": "Luxury custom homes, clay-tile and flat-roof contemporaries, resort and commercial properties",
        "perils": ["Microbursts", "Hail", "Desert brush fire", "High-value water losses", "Solar & roof equipment damage"],
        "near": ["phoenix", "gilbert", "mesa"],
        "lede": "Scottsdale’s custom homes in DC Ranch, Troon and Silverleaf carry high-end materials, and high-end materials make the gap between a quick estimate and the real cost much larger.",
        "body": """
<h2>High-value homes, high-value disputes</h2>
<p>North Scottsdale is known for custom homes with clay tile, flat-roof contemporary designs, stone veneers, large glass walls and specialty finishes. Communities such as DC Ranch, Silverleaf, Troon, Desert Mountain, Pinnacle Peak and Gainey Ranch include homes where a single room’s finishes can cost more than a typical house. Estimates that rely on standard-grade line items undervalue these losses badly.</p>
<h2>Water losses in luxury homes</h2>
<p>A failed supply line in a home with natural stone flooring, custom millwork and integrated systems can produce a six-figure loss. Matching continuous stone floors or discontinued finishes is often the core dispute. We document materials carefully, including sources, grades and availability.</p>
<h2>Desert edge exposure</h2>
<p>The north end of the city borders the McDowell Sonoran Preserve and the Tonto National Forest. Brush fires in the Sonoran Desert are less common than forest fires up north but can move quickly in wet years with heavy grass. Microbursts and hail also cross the city, damaging tile, solar arrays and rooftop equipment.</p>
<h2>Commercial and resort properties</h2>
<p>Old Town and the Scottsdale Airpark hold restaurants, galleries, offices and resorts. Commercial claims there often involve business income alongside the building loss.</p>
<h2>Areas we cover</h2>
<p>Old Town, McCormick Ranch, Gainey Ranch, Scottsdale Ranch, DC Ranch, Silverleaf, Grayhawk, Troon, Pinnacle Peak, Desert Mountain and nearby Paradise Valley, Fountain Hills and Cave Creek.</p>
""",
        "faqs": [
            ("Do high-value homeowners policies handle appraisal differently?", "The appraisal clause usually works the same way, but high-value policies may include guaranteed replacement cost or cash-out options that affect the final payment."),
            ("Can appraisal address matching of natural stone?", "Yes. The cost to achieve a reasonable match is a valuation question, and documentation of the stone’s source and availability is key."),
            ("Do you work in Paradise Valley and Fountain Hills?", "Yes, along with Cave Creek, Carefree and the rest of the northeast Valley."),
        ],
    },
    {
        "slug": "glendale", "city": "Glendale", "county": "Maricopa County", "region": "West Valley",
        "housing": "Historic bungalows, 1970s–90s subdivisions, Arrowhead-area homes, entertainment and retail districts",
        "perils": ["Microbursts", "Hail", "Dust storms", "Slab leaks", "Commercial roof damage"],
        "near": ["phoenix", "scottsdale", "yuma"],
        "lede": "Glendale covers the historic homes of Catlin Court, the subdivisions of Arrowhead Ranch and the Westgate entertainment district, with claims to match each one.",
        "body": """
<h2>From historic downtown to the Loop 101</h2>
<p>Glendale’s Catlin Court historic district holds early twentieth-century bungalows converted to shops and homes. Central Glendale neighborhoods filled in with block and stucco ranch homes in the 1960s and 1970s. Arrowhead Ranch, built around lakes and golf courses, added larger tile-roof homes in the 1980s and 1990s. West Glendale near Westgate and State Farm Stadium adds hotels, retail and entertainment venues.</p>
<h2>West Valley storm exposure</h2>
<p>Monsoon storms that build to the north and east often push outflow and dust across the West Valley. Microbursts here regularly topple trees and block walls, peel tile and damage evaporative coolers and HVAC equipment. Hail is less frequent but can be widespread when it arrives.</p>
<h2>Older plumbing, newer problems</h2>
<p>Many central Glendale homes still have original copper or galvanized lines. Slab leaks and supply-line failures are frequent, and estimates often undervalue the cost to access, repair and restore floors in homes with continuous tile.</p>
<h2>Areas we cover</h2>
<p>Catlin Court, downtown Glendale, Arrowhead Ranch, Sahuaro Ranch, Westgate, Bellair and the surrounding West Valley, including Peoria, Sun City and Surprise.</p>
""",
        "faqs": [
            ("Do you cover Peoria, Sun City and Surprise?", "Yes. We handle claims throughout the West Valley."),
            ("My evaporative cooler was damaged in a storm. Is it worth claiming?", "On its own it may fall under your deductible, but coolers and HVAC units are often part of a larger roof claim and should be included."),
            ("Does a historic home cost more to repair?", "Often yes. Original materials and methods can raise costs, and that difference belongs in the valuation."),
        ],
    },
    {
        "slug": "flagstaff", "city": "Flagstaff", "county": "Coconino County", "region": "Northern Arizona",
        "housing": "Pitched shingle and metal roofs, forest cabins, student rentals, historic downtown buildings",
        "perils": ["Wildfire", "Post-fire flooding", "Snow load", "Frozen pipes", "Hail"],
        "near": ["prescott", "phoenix", "lake-havasu-city"],
        "lede": "At about 7,000 feet in the ponderosa pines, Flagstaff deals with wildfire, post-fire floods, heavy snow and frozen pipes, often in the same year.",
        "body": """
<h2>A mountain town with mountain claims</h2>
<p>Flagstaff sits beneath the San Francisco Peaks in Coconino County, surrounded by one of the largest ponderosa pine forests in the world. It is one of the snowiest cities in the country, and its housing reflects that: steep shingle and metal roofs, wood-frame cabins and older homes in Southside and around Northern Arizona University.</p>
<h2>Fire, then flood</h2>
<p>Recent years have made Flagstaff a case study in back-to-back perils. The 2019 Museum Fire burned in the Dry Lake Hills above town, and in the years afterward neighborhoods below the burn scar flooded repeatedly as monsoon rain ran off the burned slopes. In 2022 the Tunnel Fire destroyed homes north of the city and the Pipeline Fire forced evacuations soon after. Wildfire claims here range from total losses to homes filled with smoke and ash.</p>
<p>Flood damage from surface water is usually excluded from homeowners policies. Where the line falls between excluded flood and covered water entry is a coverage question; our job is to value the physical damage accurately and identify its cause.</p>
<h2>Winter losses</h2>
<p>Heavy, wet storms load roofs and carports. Ice dams push water under shingles. Cabins and rentals left unheated can freeze. In October 2010, tornadoes even struck near Bellemont west of town.</p>
<h2>Areas we cover</h2>
<p>Downtown, Southside, Cheshire, Coconino Estates, Continental, University Heights, Ponderosa Trails, Kachina Village, Mountainaire, Doney Park, Timberline and the surrounding parts of Coconino County, including Williams and Sedona.</p>
""",
        "faqs": [
            ("Is post-fire flooding covered by my homeowners policy?", "Surface flooding is commonly excluded and needs separate flood insurance. Mudflow and debris situations can be more complicated. Talk to an attorney if the carrier denies a significant claim on that basis."),
            ("Do you handle vacation rental claims in Flagstaff?", "Yes. Short-term rentals often have landlord or commercial policies with different terms, and we value the loss accordingly."),
            ("Can snow load damage be appraised?", "Yes, once the carrier accepts coverage. Structural repairs often need an engineer’s input, which we coordinate."),
        ],
    },
    {
        "slug": "prescott", "city": "Prescott", "county": "Yavapai County", "region": "Central Highlands",
        "housing": "Victorian homes, granite-dell custom builds, retirement communities, manufactured homes",
        "perils": ["Wildfire", "Hail", "Monsoon wind", "Snow & ice", "Frozen pipes"],
        "near": ["flagstaff", "glendale", "phoenix"],
        "lede": "Prescott’s Victorian homes around Courthouse Plaza, hillside custom homes and retirement communities face wildfire, monsoon hail and real winter weather.",
        "body": """
<h2>Mile-high, four seasons</h2>
<p>Prescott, the Yavapai County seat, sits at roughly 5,400 feet among granite dells and pine-covered hills. Downtown around Courthouse Plaza and Whiskey Row holds some of the oldest commercial buildings in the state, and nearby streets are lined with Victorian and early twentieth-century homes. Newer neighborhoods such as Prescott Lakes, Hassayampa and the Williamson Valley corridor added custom homes, and Prescott Valley and Chino Valley grew quickly with tract and manufactured homes.</p>
<h2>Wildfire in the wildland-urban interface</h2>
<p>Prescott is home to the Granite Mountain Hotshots, and the 2013 Yarnell Hill Fire, which took the lives of 19 of the crew and destroyed homes in Yarnell, is a defining event for the region. Other fires, including the 2017 Goodwin Fire near Mayer, have forced evacuations across Yavapai County. Many Prescott homes sit among pines and chaparral where smoke, ash and ember damage are real risks.</p>
<h2>Storms and winter</h2>
<p>Monsoon storms bring hail more often here than in the low desert, and hail-damaged shingle and metal roofs are a common claim. Winter storms add snow, ice dams and frozen pipes, especially in homes owned by part-time residents.</p>
<h2>Historic homes</h2>
<p>Victorian homes have wood siding, trim profiles and original windows that standard estimates rarely price correctly. Matching historic materials is often the heart of the dispute.</p>
<h2>Areas we cover</h2>
<p>Downtown and Courthouse Plaza, Prescott Lakes, Hassayampa, Forest Highlands, Williamson Valley, Prescott Valley, Chino Valley, Dewey-Humboldt and the wider quad-city area.</p>
""",
        "faqs": [
            ("Do you cover Prescott Valley and Chino Valley?", "Yes, along with Dewey-Humboldt and the rest of the quad-city area."),
            ("Hail damaged my metal roof but it doesn’t leak. Is that a claim?", "Cosmetic dents may be excluded by endorsement on some policies; functional damage is usually covered. Check your policy for a cosmetic damage exclusion."),
            ("What if my historic siding can’t be matched?", "The cost to achieve a reasonable match, including replacing more siding than was damaged if necessary, is a valuation question we document."),
        ],
    },
    {
        "slug": "yuma", "city": "Yuma", "county": "Yuma County", "region": "Western Desert",
        "housing": "Stucco and block homes, Foothills retirement areas, RV and manufactured-home parks, agricultural buildings",
        "perils": ["Monsoon wind", "Dust storms", "Extreme heat", "Plumbing failures", "Agricultural building damage"],
        "near": ["lake-havasu-city", "glendale", "tucson"],
        "lede": "Yuma is one of the sunniest and hottest places in the country. Its claims come from monsoon wind, dust and the steady toll heat takes on roofs, coolers and plumbing.",
        "body": """
<h2>Heat, sun and wind</h2>
<p>Yuma sits along the Colorado River near the California and Mexico borders and is often called the sunniest city in the world. Summer highs routinely pass 110°F. That heat ages roof coatings, underlayment and plumbing, and when a monsoon storm or dust storm finally hits, carriers often argue that age, not the storm, caused the damage.</p>
<h2>Housing and property types</h2>
<p>Central Yuma has older block and stucco homes. The Foothills east of town filled with homes and manufactured-home communities popular with retirees and winter visitors. RV resorts, agricultural packing sheds and equipment buildings serve the region’s farming economy. Metal buildings and carports are vulnerable to monsoon gusts.</p>
<h2>Seasonal residents</h2>
<p>Many Foothills and RV-park homes sit empty from spring to fall. A failed water heater or supply line can run for weeks before anyone notices. Expect questions about vacancy conditions and the timing of the leak, and keep records of any property checks.</p>
<h2>Areas we cover</h2>
<p>Central Yuma, the Foothills, Fortuna Foothills, Somerton, San Luis, Wellton and the agricultural areas of Yuma County.</p>
""",
        "faqs": [
            ("Can heat alone cause a covered claim?", "Usually not. Gradual heat deterioration is typically treated as wear. A storm or sudden event acting on that aged material is what usually triggers coverage."),
            ("Do you appraise agricultural buildings?", "Yes. Farm and ranch structures are valued like other commercial buildings, though policies for them can have their own terms."),
            ("I spend summers out of state. How do I protect my claim?", "Arrange regular property checks and keep a log. Shut off water when you leave if your home allows it."),
        ],
    },
    {
        "slug": "lake-havasu-city", "city": "Lake Havasu City", "county": "Mohave County", "region": "Western River Country",
        "housing": "Stucco and tile homes, vacation and second homes, boat and RV garages, waterfront commercial",
        "perils": ["Monsoon microbursts", "Flash floods in washes", "Extreme heat", "Leaks in vacant homes", "Hail"],
        "near": ["yuma", "flagstaff", "prescott"],
        "lede": "London Bridge, the lake and a large share of second homes make Lake Havasu City unique. Storm, wash-flood and vacant-home water losses top the list here.",
        "body": """
<h2>A resort city on the Colorado River</h2>
<p>Lake Havasu City was founded in the 1960s and became famous when London Bridge was rebuilt here in 1971. Most homes are stucco with tile roofs, and many include oversized garages for boats and RVs. A large share are second homes and vacation rentals, which means long stretches with no one inside.</p>
<h2>Storms and washes</h2>
<p>Monsoon storms over the Mohave Mountains can produce violent microbursts and intense rain. Water runs through the city’s many washes and can surge across streets with little warning. Surface flood damage is usually excluded from homeowners policies, but wind damage and rain entering through storm-created openings often are not. Careful cause documentation matters.</p>
<h2>Vacant-home water losses</h2>
<p>Summer heat over 115°F stresses plumbing, water heaters and appliance lines. In an empty home, a small leak can soak floors and walls for weeks. Carriers may raise vacancy or long-term seepage issues. Smart water shutoffs, monitoring systems and property-check logs help both prevention and proof.</p>
<h2>Boat garages and outbuildings</h2>
<p>Large detached garages, shade structures and docks often fall under other structures coverage with its own limit. They belong in the valuation when they are damaged.</p>
<h2>Areas we cover</h2>
<p>The Island, Havasu Foothills, Desert Hills, North and South Havasu, and the surrounding communities of Mohave County, including Kingman and Bullhead City.</p>
""",
        "faqs": [
            ("Is my boat garage covered under my homeowners policy?", "Detached garages are often covered under other structures, usually with a separate limit. The boat itself typically needs its own policy."),
            ("How do vacancy clauses affect my claim?", "Some policies limit coverage for certain losses after a home has been vacant for a set period. Read the clause and keep records of occupancy and property checks."),
            ("Do you cover Kingman and Bullhead City?", "Yes. We handle claims throughout Mohave County."),
        ],
    },
    {
        "slug": "sierra-vista", "city": "Sierra Vista", "county": "Cochise County", "region": "Southeast Arizona",
        "housing": "Military-family subdivisions, canyon-edge homes, manufactured homes, ranch properties",
        "perils": ["Monsoon hail", "Microbursts", "Wildfire", "Post-fire flooding", "Freeze"],
        "near": ["tucson", "chandler", "yuma"],
        "lede": "Below the Huachuca Mountains and next to Fort Huachuca, Sierra Vista gets some of Arizona’s most intense monsoon storms, and in 2011 it watched the Monument Fire burn homes at the edge of town.",
        "body": """
<h2>High desert at the foot of the Huachucas</h2>
<p>Sierra Vista sits at about 4,600 feet in Cochise County, beside Fort Huachuca and beneath the Huachuca Mountains. The elevation brings milder summers than Tucson, cool winters and very active monsoon storms that build over the mountains nearly every afternoon in July and August.</p>
<h2>The Monument Fire</h2>
<p>In June 2011 the Monument Fire burned through canyons on the east side of the Huachucas and destroyed dozens of homes in the Hereford and Miller Canyon areas south of town. As in Flagstaff, the burned slopes then sent flooding and debris into neighborhoods during the following monsoon seasons. Homes along the mountain front remain exposed to both fire and post-fire runoff.</p>
<h2>Housing and claims</h2>
<p>Many neighborhoods were built for military families and retirees, with stucco, block and tile or shingle roofs. Rural properties include manufactured homes, barns, wells and long fences. Hail and microbursts are common sources of roof claims, and occasional hard freezes break pipes.</p>
<h2>Military families</h2>
<p>Service members can receive orders in the middle of a claim. We work with remote communication, a designated representative or a property manager so the claim keeps moving after a move.</p>
<h2>Areas we cover</h2>
<p>Sierra Vista, Fort Huachuca-area neighborhoods, Hereford, Huachuca City, Whetstone, Benson, Bisbee, Douglas and the rest of Cochise County.</p>
""",
        "faqs": [
            ("Can you handle my claim if I receive PCS orders?", "Yes. We can work through a designated representative and handle communication remotely so the claim continues after you relocate."),
            ("Are wells and pumps covered after a storm?", "Many policies cover them under dwelling or other structures, sometimes with limits. Lightning and power-surge damage to pumps is a common claim."),
            ("Do you cover Bisbee and Douglas?", "Yes, along with Benson, Huachuca City and the rest of Cochise County."),
        ],
    },
]
