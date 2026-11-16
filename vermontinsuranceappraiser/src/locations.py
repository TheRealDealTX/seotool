"""Town pages. Each has county, neighborhoods/villages, storm history and housing mix."""

LOCATIONS = [
    {
        "slug": "burlington", "desc": "Insurance appraiser in Burlington, VT for Old North End rentals, Hill Section homes and lakeside condos with short ice dam or wind claims.", "city": "Burlington", "county": "Chittenden County", "region": "Champlain Valley",
        "kw": "insurance appraiser in Burlington, VT",
        "perils": ["Ice dams", "Lake-effect wind", "Frozen pipes", "Older multifamily"],
        "near": ["south-burlington", "st-albans", "middlebury"],
        "lede": "Vermont’s largest city sits on the eastern shore of Lake Champlain, with a housing mix that runs from Victorian mansions on the Hill Section to student rentals and duplexes in the Old North End.",
        "body": """
<h2>Burlington’s housing and what it means for claims</h2>
<p>Burlington’s neighborhoods are old and dense. The Old North End is full of late-1800s worker housing, many of them now two- and three-unit buildings. The Hill Section near the University of Vermont has large Victorian and Colonial Revival homes. The South End mixes bungalows with converted industrial space along Pine Street, and the New North End is mostly postwar ranches, capes and split-levels. Downtown, around Church Street, there are condos above storefronts and newer mid-rise buildings.</p>
<p>That variety means an insurance appraiser in Burlington, VT has to price plaster, slate, balloon framing and old wiring as readily as vinyl and drywall. A carrier’s estimate that defaults to modern materials can fall well short in this city.</p>
<h2>Weather on the lake</h2>
<p>Burlington is one of the milder places in Vermont, but winds off Lake Champlain can be strong, and winter brings repeated freeze-thaw cycles that build ice dams on older, under-insulated roofs. The Halloween storm of 2019 brought damaging winds to the area. In spring 2011, Lake Champlain rose to a record level, flooding low-lying shoreline property, including parts of Burlington’s waterfront.</p>
<h2>Rental and multifamily claims</h2>
<p>Many Burlington owners hold small rental buildings. A single water loss can affect several units and tenants at once, adding loss-of-rents questions and tenant coordination to the building claim. We value the building loss and help landlords keep the dwelling estimate separate from contents and income questions.</p>
<h2>Local permitting</h2>
<p>Repairs in Burlington’s historic districts may need design review. That can change materials and timelines, which in turn affects cost. We note those constraints in the estimate.</p>
""",
        "faqs": [
            ("Do you inspect in Burlington?", "Yes. Chittenden County is one of the areas where we work most often."),
            ("My triplex had a water loss affecting all three units. Is that one claim?", "Usually it is one claim on the building policy, with contents claims by any tenants under their own renters policies."),
        ],
    },
    {
        "slug": "south-burlington", "desc": "Insurance appraiser in South Burlington, VT for condo, townhouse and suburban home claims where the carrier’s estimate came up short.", "city": "South Burlington", "county": "Chittenden County", "region": "Champlain Valley",
        "kw": "insurance appraiser in South Burlington, VT",
        "perils": ["Wind", "Hail", "Condo water losses", "Ice dams"],
        "near": ["burlington", "middlebury", "stowe"],
        "lede": "South Burlington’s condos, townhouses and suburban homes surround Burlington International Airport and the new City Center along Market Street.",
        "body": """
<h2>A city of condos and subdivisions</h2>
<p>South Burlington grew mostly after the 1960s. Neighborhoods off Dorset Street, Hinesburg Road and Spear Street are filled with ranches, colonials and split-levels, while the Southeast Quadrant and the City Center area have added townhouses and mid-rise condos. Many residents own under an HO-6 policy with an association master policy above it.</p>
<p>An insurance appraiser in South Burlington, VT spends a lot of time sorting out which policy pays for what. A burst pipe in a third-floor unit may damage four units below and the common walls between them.</p>
<h2>Weather patterns</h2>
<p>Summer thunderstorms move east across the lake and can bring hail and gusty winds to South Burlington. Winter brings the usual Champlain Valley mix of snow, freezing rain and thaw. Flat and low-slope roofs on commercial buildings along Williston Road and Shelburne Road can pond water and collect drifted snow.</p>
<h2>Commercial and retail</h2>
<p>The city’s retail corridors and office parks carry larger commercial policies. Membrane roofs, rooftop units and storefront glass are common claim items.</p>
<h2>Working with associations</h2>
<p>When an association files on its master policy, unit owners often wonder how the deductible will be assessed. We help boards and owners understand the estimate, so the assessment conversation starts from accurate numbers.</p>
""",
        "faqs": [
            ("My condo association’s adjuster wrote the estimate. Can I challenge it?", "If the association is the insured, the board usually controls the master claim. You can raise concerns with the board, and your HO-6 policy may cover parts the master policy does not."),
            ("Do you cover Williston and Shelburne too?", "Yes. We work throughout Chittenden County."),
        ],
    },
    {
        "slug": "rutland", "desc": "Insurance appraiser in Rutland, VT for Victorian homes, Killington condos and Irene-country properties with disputed claim estimates.", "city": "Rutland", "county": "Rutland County", "region": "Southern Green Mountains",
        "kw": "insurance appraiser in Rutland, VT",
        "perils": ["Tropical storm flooding", "Snow load", "Ice dams", "Fire"],
        "near": ["middlebury", "bennington", "hartford"],
        "lede": "The Marble City sits in the Otter Creek valley between the Taconic and Green Mountains, with Victorian homes, older multifamily buildings and the routes to Killington and Okemo.",
        "body": """
<h2>Rutland’s homes</h2>
<p>Rutland’s marble and railroad history left behind large Victorian homes in the Northwest neighborhood and along Main Street, worker housing near the rail yard, and a historic downtown of brick commercial blocks. Rutland Town and the surrounding towns add newer subdivisions and rural properties. Many homes are well over a century old.</p>
<h2>Irene and the Route 4 corridor</h2>
<p>Tropical Storm Irene in 2011 hit the Rutland area hard. Floodwaters damaged Route 4 east toward Mendon and Killington, cutting off communities for days, and rivers rose across the county. Many properties had both a covered wind or tree claim and a separate flood question. An insurance appraiser in Rutland, VT has to keep those categories distinct while valuing the covered part fully.</p>
<h2>Snow and mountain weather</h2>
<p>East of the city, elevation brings heavier snow. Ski-area condos and lodges near Killington carry large roof loads every winter, and freeze-ups in unoccupied units are a recurring claim. Ice dams are common on older homes in the city itself.</p>
<h2>Fire</h2>
<p>Heating with wood and oil, and older wiring in many buildings, make fire and smoke claims a regular part of the work in this county.</p>
""",
        "faqs": [
            ("Do you handle ski condo claims near Killington?", "Yes, both for individual unit owners and for associations."),
            ("I had a flood and a tree on my house in the same storm. What do I do?", "Report both. The tree damage is typically a homeowners claim, while rising water is usually a flood policy issue."),
        ],
    },
    {
        "slug": "montpelier", "desc": "Insurance appraiser in Montpelier, VT for historic downtown blocks and hillside homes after floods, ice jams and winter water losses.", "city": "Montpelier", "county": "Washington County", "region": "Central Vermont",
        "kw": "insurance appraiser in Montpelier, VT",
        "perils": ["River flooding", "Ice jams", "Ice dams", "Historic buildings"],
        "near": ["barre", "stowe", "hartford"],
        "lede": "The smallest state capital in the country sits where the North Branch meets the Winooski River, and in July 2023 floodwater filled its downtown.",
        "body": """
<h2>July 2023</h2>
<p>On July 10 and 11, 2023, days of heavy rain sent the Winooski River and the North Branch over their banks. Downtown Montpelier flooded, with water filling basements and ground-floor businesses along State and Main Streets. It was one of the worst floods in the city since 1927. Many buildings had both covered damage, such as sewer backup under an endorsement or wind-related damage, and excluded flood damage, and owners had to work through more than one policy.</p>
<h2>Ice jams</h2>
<p>Montpelier also has a history of ice-jam floods, including a severe one in March 1992 when ice blocked the Winooski and water rose quickly into downtown. Late-winter thaws remain a concern.</p>
<h2>Historic downtown, hillside homes</h2>
<p>The downtown is a historic district of brick and granite commercial blocks with apartments above. The residential neighborhoods climb the hills on either side of the river, with Victorian and early twentieth-century homes on narrow lots and steep driveways. An insurance appraiser in Montpelier, VT has to price restoration work on buildings where matching materials and historic review both matter.</p>
<h2>Winter claims</h2>
<p>Steep roofs and older homes make ice dams common. Narrow streets and hills complicate access for roofing crews and dumpsters, adding cost that estimates often omit.</p>
""",
        "faqs": [
            ("My building flooded in 2023. Is it too late to dispute the claim?", "It depends on your policy’s deadlines and whether the claim is still open. Flood policies have strict proof-of-loss rules. Talk to a professional promptly."),
            ("Can appraisal help with a flood claim?", "The standard NFIP flood policy has its own appraisal provision for disputes over the value of covered damage, with its own procedures."),
        ],
    },
    {
        "slug": "barre", "desc": "Insurance appraiser in Barre, VT for granite-era multifamily homes hit by the 2023 and 2024 floods, frozen pipes and ice dams.", "city": "Barre", "county": "Washington County", "region": "Central Vermont",
        "kw": "insurance appraiser in Barre, VT",
        "perils": ["Flash flooding", "Ice dams", "Frozen pipes", "Older multifamily"],
        "near": ["montpelier", "stowe", "hartford"],
        "lede": "The Granite City flooded in July 2023 and again in July 2024, when the remnants of Hurricane Beryl sent the Stevens Branch and Jail Branch through town.",
        "body": """
<h2>Two floods in two summers</h2>
<p>Barre sits in a narrow valley where the Stevens Branch and the Jail Branch meet. In July 2023, heavy rain flooded parts of the city. Almost exactly a year later, in July 2024, the remnants of Hurricane Beryl brought another round of flash flooding that damaged homes, roads and businesses. For some owners, the second flood arrived before repairs from the first were finished.</p>
<p>An insurance appraiser in Barre, VT has to carefully separate damage by date and cause when two losses overlap, and confirm which policy and which deductible applies to each.</p>
<h2>Granite-era housing</h2>
<p>Barre’s granite industry drew immigrant stonecutters in the late 1800s and early 1900s, and the housing reflects it: two- and three-family homes, tenement-style buildings, and modest single-family houses on small lots. Many have been rental properties for decades. Granite foundations and older plumbing are common.</p>
<h2>Winter losses</h2>
<p>Barre’s valley location brings cold air pooling and hard freezes. Frozen pipes in older multi-unit buildings, especially in unheated common areas, are a frequent claim. Ice dams on steep, older roofs follow every snowy winter.</p>
<h2>Barre Town and surrounding communities</h2>
<p>Outside the city, Barre Town and Williamstown have more rural properties, outbuildings and newer homes.</p>
""",
        "faqs": [
            ("My house flooded in 2023 and again in 2024. Are these separate claims?", "Usually yes. Each event is a separate loss with its own deductible and its own documentation."),
            ("Do you work on rental properties?", "Yes. Many Barre clients are landlords with two- to six-unit buildings."),
        ],
    },
    {
        "slug": "st-albans", "desc": "Insurance appraiser in St. Albans, VT for Victorian homes, bay camps and Franklin County dairy barns with disputed property claims.", "city": "St. Albans", "county": "Franklin County", "region": "Northwest Vermont",
        "kw": "insurance appraiser in St. Albans, VT",
        "perils": ["Wind off the lake", "Ice storms", "Farm buildings", "Ice dams"],
        "near": ["burlington", "south-burlington", "stowe"],
        "lede": "Franklin County’s seat sits above St. Albans Bay near the Canadian border, with a Victorian downtown around Taylor Park and dairy farms in every direction.",
        "body": """
<h2>City, town and countryside</h2>
<p>St. Albans City has a compact historic downtown around Taylor Park, Victorian homes on the surrounding streets and older multifamily buildings near the rail yards. St. Albans Town wraps around it with newer subdivisions and lakefront camps on St. Albans Bay. Beyond that is some of Vermont’s most productive dairy country.</p>
<p>An insurance appraiser in St. Albans, VT works on all three: in-town homes, lake camps and farm buildings.</p>
<h2>Weather near the border</h2>
<p>The northwest corner of Vermont gets strong winds off Lake Champlain and some of the state’s worst ice storms. The January 1998 ice storm coated northwestern Vermont and neighboring Quebec in heavy ice, bringing down trees and power lines. Ice storms, heavy snow and spring thaws remain the main winter risks.</p>
<h2>Farm claims</h2>
<p>Barns, free-stall housing, silos, manure systems and equipment sheds fall under farm policies with their own forms and valuation rules. Snow-load collapse on older barns and wind damage to large roofs are the most common farm claims we see in Franklin County.</p>
<h2>Lake camps</h2>
<p>Seasonal camps on the bay face freeze-ups when unheated, wind and ice damage to docks and shoreline structures, and spring high water. Policies often limit coverage for docks and require heat or draining for freeze coverage.</p>
""",
        "faqs": [
            ("Do you handle farm policies?", "Yes. Farm forms differ from homeowners policies, and we read them carefully before valuing a barn or equipment loss."),
            ("Is ice damage to my dock covered?", "Many policies exclude or limit damage to docks and piers from ice. Check the property not covered and other structures sections."),
        ],
    },
    {
        "slug": "brattleboro", "desc": "Insurance appraiser in Brattleboro, VT for hillside homes and downtown blocks with tree, wind, ice dam and Irene-style storm claims.", "city": "Brattleboro", "county": "Windham County", "region": "Southeast Vermont",
        "kw": "insurance appraiser in Brattleboro, VT",
        "perils": ["Tropical storm flooding", "Fallen trees", "Ice dams", "Hillside drainage"],
        "near": ["bennington", "hartford", "rutland"],
        "lede": "Brattleboro climbs the hills above the big river on Vermont’s eastern border, where Whetstone Brook runs through the middle of town and flooded badly during Irene.",
        "body": """
<h2>Irene and Whetstone Brook</h2>
<p>When Tropical Storm Irene arrived in August 2011, Whetstone Brook rose rapidly and flooded the Flat Street area and the neighborhoods along its banks. Nearby towns in the Deerfield Valley, including Wilmington, saw even worse damage. Brattleboro owners dealt with a mix of flood, tree and wind losses, often on the same property.</p>
<h2>Housing on hillsides</h2>
<p>Brattleboro’s homes sit on steep streets above the river: Victorian and early twentieth-century houses, many divided into apartments, alongside newer homes on the edges of town. Downtown has historic brick blocks with residential units above shops on Main Street. Steep lots make drainage, retaining walls and access part of many claims.</p>
<p>An insurance appraiser in Brattleboro, VT often prices work that requires extra labor for access: materials carried up stairs, scaffolding on sloped lots and limited parking downtown.</p>
<h2>Trees and storms</h2>
<p>Mature hardwoods surround most of the town. Summer thunderstorms and autumn gales bring trees down onto roofs and porches, and heavy wet snow breaks limbs in late winter.</p>
<h2>Southern Vermont winters</h2>
<p>Winters are a little milder here than in the north, which means more freeze-thaw cycles. That pattern builds ice dams and drives water into older roofs.</p>
""",
        "faqs": [
            ("Is a tree falling on my house covered?", "Generally yes, if it damages a covered structure. Removal of the tree itself may be limited by a sub-limit."),
            ("Do you cover the Deerfield Valley?", "Yes, including Wilmington, Dover and the surrounding towns."),
        ],
    },
    {
        "slug": "bennington", "desc": "Insurance appraiser in Bennington, VT for Old Bennington homes, mill-era buildings and valley properties with underpaid claims.", "city": "Bennington", "county": "Bennington County", "region": "Southwest Vermont",
        "kw": "insurance appraiser in Bennington, VT",
        "perils": ["River flooding", "Wind", "Ice dams", "Historic homes"],
        "near": ["brattleboro", "rutland", "middlebury"],
        "lede": "Bennington spreads along the Walloomsac River below Mount Anthony, with Old Bennington’s historic homes on the hill and mill-era neighborhoods in the valley.",
        "body": """
<h2>Old Bennington to the valley</h2>
<p>Old Bennington, on the hill west of downtown, is a historic district of eighteenth- and nineteenth-century homes near the Bennington Battle Monument. Downtown Bennington and the surrounding neighborhoods grew around mills on the Walloomsac River and Roaring Branch, with worker housing, multifamily homes and commercial blocks. North Bennington adds another historic village and the Bennington College campus.</p>
<p>An insurance appraiser in Bennington, VT regularly works on homes where clapboard, plaster, slate and original millwork drive the cost of a proper repair.</p>
<h2>Flooding</h2>
<p>Tropical Storm Irene in 2011 flooded parts of Bennington along the Roaring Branch and the Walloomsac. The town’s rivers respond quickly to heavy rain in the surrounding hills.</p>
<h2>Wind and winter</h2>
<p>Southwestern Vermont sits in the path of storms moving in from the west across the Taconic Mountains. Strong winds, ice and snow all reach the area, and summer thunderstorms bring occasional hail.</p>
<h2>Commercial buildings</h2>
<p>Bennington’s former mills and downtown blocks have been converted into offices, apartments and shops. Large old roofs, masonry and mixed-use occupancy make these commercial claims complex.</p>
""",
        "faqs": [
            ("My house is in a historic district. Does that change the claim?", "It can affect required materials and permits, which affects cost. Whether the policy pays for those extra costs depends on its wording."),
            ("Do you work in Manchester and Arlington?", "Yes, throughout Bennington County."),
        ],
    },
    {
        "slug": "middlebury", "desc": "Insurance appraiser in Middlebury, VT for village homes, college rentals and Addison County barns hit by wind, hail or heavy snow.", "city": "Middlebury", "county": "Addison County", "region": "Champlain Valley",
        "kw": "insurance appraiser in Middlebury, VT",
        "perils": ["Wind", "Hail", "Farm buildings", "Ice dams"],
        "near": ["burlington", "rutland", "south-burlington"],
        "lede": "Addison County’s shire town straddles Otter Creek Falls, with a college, a historic village center and open farmland reaching to Lake Champlain.",
        "body": """
<h2>Village and farmland</h2>
<p>Middlebury’s village center has nineteenth-century homes and commercial buildings clustered around the falls of Otter Creek and the town green. Middlebury College adds large institutional buildings and student rentals. Outside the village, Addison County is some of Vermont’s flattest, most open farmland, with dairy farms, orchards and long views to the Adirondacks.</p>
<p>An insurance appraiser in Middlebury, VT sees in-town homes, rental properties and agricultural buildings, often in the same week.</p>
<h2>Open country weather</h2>
<p>The open Champlain Valley lets wind build. Summer thunderstorms crossing the lake from the Adirondacks can bring hail and damaging gusts, and microbursts have flattened barns and orchards in Addison County. In winter, wind drifts snow onto barn roofs and against buildings.</p>
<h2>Agricultural claims</h2>
<p>Barns, silos, greenhouses and equipment storage carry high replacement values and specialized construction. Farm policies may value them differently from a dwelling, and snow or wind damage to a large roof can be expensive.</p>
<h2>Historic homes</h2>
<p>Many village homes date to the early 1800s. Restoration with matching materials costs more than generic replacement, and estimates need to reflect that.</p>
""",
        "faqs": [
            ("Do you appraise barn and orchard losses?", "We value building and structure losses under farm policies. Crop losses fall under separate crop insurance programs."),
            ("Do you cover Vergennes and Bristol?", "Yes, all of Addison County."),
        ],
    },
    {
        "slug": "st-johnsbury", "desc": "Insurance appraiser in St. Johnsbury, VT for Northeast Kingdom homes and camps after flash floods, freeze-ups, snow load and fire.", "city": "St. Johnsbury", "county": "Caledonia County", "region": "Northeast Kingdom",
        "kw": "insurance appraiser in St. Johnsbury, VT",
        "perils": ["Flash flooding", "Snow load", "Frozen pipes", "Fire"],
        "near": ["barre", "stowe", "montpelier"],
        "lede": "The hub of the Northeast Kingdom sits where the Passumpsic, Moose and Sleepers rivers meet, with a Victorian Main Street on the hill and mill buildings below.",
        "body": """
<h2>Summer 2024</h2>
<p>In July 2024 the Northeast Kingdom was hit twice. The remnants of Hurricane Beryl flooded parts of the region around July 11, and at the end of the month a second round of intense thunderstorms caused flash flooding in Caledonia County, including St. Johnsbury and nearby Lyndon. Roads washed out and homes along small streams were damaged.</p>
<p>An insurance appraiser in St. Johnsbury, VT has to sort out which of those events caused which damage, and which policy applies.</p>
<h2>The town</h2>
<p>St. Johnsbury’s Main Street, on the hill above the rivers, has Victorian mansions and civic buildings left by the Fairbanks scale fortune. Railroad Street, below, has commercial blocks and apartments. Outlying neighborhoods and the surrounding towns are rural, with farmhouses, camps and manufactured homes.</p>
<h2>A colder corner of the state</h2>
<p>The Northeast Kingdom has some of Vermont’s coldest winters. Long cold snaps freeze pipes in older homes, camps and vacant buildings, and deep snowpacks load barn and garage roofs. Wood heat is common, so chimney fires are part of the claim mix.</p>
<h2>Distance and cost</h2>
<p>Remote properties cost more to repair: contractors travel farther, materials are delivered from a distance and the building season is short. Estimates should reflect those local conditions.</p>
""",
        "faqs": [
            ("Do you travel to the Northeast Kingdom?", "Yes. We work in Caledonia, Orleans and Essex counties."),
            ("My camp froze while I was away. Am I covered?", "That depends on your policy’s vacancy and heat conditions, and what you did to maintain heat or drain the plumbing."),
        ],
    },
    {
        "slug": "stowe", "desc": "Insurance appraiser in Stowe, VT for ski condos, lodges and second homes with snow load, ice dam and frozen pipe claim disputes.", "city": "Stowe", "county": "Lamoille County", "region": "Northern Green Mountains",
        "kw": "insurance appraiser in Stowe, VT",
        "perils": ["Snow load", "Ice dams", "Frozen pipes", "Second-home claims"],
        "near": ["montpelier", "burlington", "barre"],
        "lede": "Stowe sits below Mount Mansfield, Vermont’s highest peak, where lodges, condos and high-end second homes carry some of the heaviest snow loads in the state.",
        "body": """
<h2>Resort and village</h2>
<p>Stowe village has a classic white-steepled center with older homes and inns. Up the Mountain Road toward the ski resort are lodges, condominium complexes and large custom homes, many owned as second homes or short-term rentals. Elsewhere in Lamoille County, Morrisville, Johnson and Hyde Park have more typical year-round housing.</p>
<p>An insurance appraiser in Stowe, VT often works on higher-value homes with custom finishes, timber framing and complex roof lines, where both the price per square foot and the stakes are high.</p>
<h2>Snow and ice</h2>
<p>Elevation and the mountain’s location bring heavy, frequent snow. Roof snow loads, ice dams on complicated roofs and snow sliding off metal roofs onto decks and lower roofs are all common claims. Heated driveways, radiant floors and complex mechanical systems add freeze risk when power fails.</p>
<h2>Second homes</h2>
<p>Many Stowe properties sit empty for weeks at a time. Policies often have vacancy, unoccupancy and heat-maintenance conditions that affect freeze and water claims. Short-term rental use can also affect coverage, depending on the policy.</p>
<h2>2023 flooding in Lamoille County</h2>
<p>The July 2023 floods hit Lamoille County hard, especially Johnson and Cambridge along the Lamoille River, and damaged roads and properties around Stowe as well.</p>
""",
        "faqs": [
            ("Does renting my home short-term affect my claim?", "It can. Some homeowners policies limit or exclude coverage for business use. Check your policy and any home-sharing endorsement."),
            ("Do you appraise high-value custom homes?", "Yes. Custom finishes and timber framing need careful pricing, and we build estimates accordingly."),
        ],
    },
    {
        "slug": "hartford", "desc": "Insurance appraiser in Hartford, VT covering White River Junction, Quechee and Wilder homes, condos and commercial roof claims.", "city": "Hartford", "county": "Windsor County", "region": "Upper Valley",
        "kw": "insurance appraiser in Hartford, VT",
        "perils": ["River flooding", "Tropical storm damage", "Ice dams", "Commercial roofs"],
        "near": ["montpelier", "rutland", "brattleboro"],
        "lede": "Hartford’s villages, including White River Junction, Quechee and Wilder, sit where the White River meets the big river on the state line, the center of the Upper Valley.",
        "body": """
<h2>Five villages, one town</h2>
<p>The town of Hartford includes White River Junction, a railroad hub with a brick downtown now full of galleries and apartments, along with Quechee, Wilder, West Hartford and Hartford Village. Quechee adds a resort community of condos and second homes around its golf courses and lakes. Housing ranges from nineteenth-century village homes to 1980s condos to new construction.</p>
<p>An insurance appraiser in Hartford, VT covers the whole Upper Valley side of Windsor County, from Norwich to Woodstock.</p>
<h2>Irene in the White River valley</h2>
<p>Tropical Storm Irene in 2011 devastated the White River valley upstream in towns like Rochester, Bethel and Royalton. In Quechee, the Ottauquechee River severely damaged the village’s historic covered bridge, and West Hartford saw serious flooding along the White River.</p>
<h2>Commercial and institutional buildings</h2>
<p>The Upper Valley is a regional employment center. Hartford has offices, medical facilities, warehouses and retail with large low-slope roofs, where snow drifting, ponding and membrane failure are common claims.</p>
<h2>Winter in the valley</h2>
<p>Cold air settles into the river valleys, and freeze-thaw cycles on older village homes build ice dams. Frozen pipes in condos used part-time are another recurring loss.</p>
""",
        "faqs": [
            ("Do you cover Woodstock and Norwich?", "Yes, throughout Windsor County."),
            ("I own a Quechee condo I visit on weekends. What should I know about freeze claims?", "Read your HO-6 policy’s heat and unoccupancy conditions, and keep records of thermostat settings and any monitoring alerts."),
        ],
    },
]
