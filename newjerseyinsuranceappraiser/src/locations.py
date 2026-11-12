"""New Jersey location pages. Local detail is specific to each community."""

LOCATIONS = [
    {
        "slug": "newark", "city": "Newark", "county": "Essex County", "region": "Gateway North Jersey",
        "perils": ["Flash flooding", "Burst pipes", "Multi-family fires", "Flat-roof leaks", "Wind"],
        "near": ["jersey-city", "paterson", "hackensack"],
        "housing": "Two- and three-family frame homes, brick rowhouses, mid-rise apartments",
        "lede": "New Jersey’s largest city packs a century of housing into 24 square miles: Ironbound row houses, North Ward two-families, Forest Hill mansions and downtown high-rises. Each one fails differently in a storm.",
        "body": """
<h2>Newark’s housing and the claims it produces</h2>
<p>Much of Newark was built between the 1890s and the 1950s. In the Ironbound, narrow frame and brick homes stand shoulder to shoulder, so a fire or roof leak in one often reaches the next. The North Ward and Vailsburg are full of two- and three-family houses with flat or low-slope roofs that pond water after heavy rain. Forest Hill has large early-1900s homes with slate roofs, plaster walls and detailed millwork. Downtown and University Heights add apartment towers and converted commercial buildings.</p>
<h2>Storms that hit Newark</h2>
<p>Sandy’s surge pushed up the Passaic River and Newark Bay in 2012, flooding parts of the waterfront and Port Newark. In September 2021, Ida’s remnants dropped intense rain on Essex County, flooding basements and streets across the city. Winter brings frozen pipes in older buildings with exterior plumbing runs and boiler systems that strain in cold snaps.</p>
<h2>Disputes we see most in Newark</h2>
<ul>
<li>Low-slope roofs patched on paper when the membrane and insulation need replacement.</li>
<li>Multi-unit water losses valued as a single unit.</li>
<li>Plaster interiors priced as drywall.</li>
<li>Smoke damage in attached homes dismissed as “no direct fire damage.”</li>
<li>Basement water claims denied as flood or groundwater without checking the source.</li>
</ul>
<p>We inspect throughout the Ironbound, North Ward, Central Ward, South Ward, Vailsburg, Weequahic, Forest Hill, Roseville and Clinton Hill, and in nearby Essex County towns.</p>
""",
        "faqs": [
            ("My two-family home in Newark has damage in both units. Is that one claim?", "Usually one claim under the owner’s policy, with a separate scope for each unit and the shared areas. Tenants’ belongings fall under their own renters policies."),
            ("Water came through the basement walls during Ida. Is that covered?", "Groundwater and surface water are usually excluded under homeowners policies and fall under flood coverage. Sewer backup may be covered by an endorsement. The source of the water matters, so document it."),
        ],
    },
    {
        "slug": "jersey-city", "city": "Jersey City", "county": "Hudson County", "region": "Gateway North Jersey",
        "perils": ["Coastal surge", "Condo water losses", "Wind-driven rain", "Brownstone roof leaks", "Fire"],
        "near": ["newark", "hackensack", "paterson"],
        "housing": "Brownstones, row houses, waterfront condo towers",
        "lede": "From Paulus Hook brownstones to Journal Square two-families and the condo towers along the Hudson, Jersey City claims mix century-old construction with some of the newest buildings in the state.",
        "body": """
<h2>Old row houses, new towers</h2>
<p>Downtown neighborhoods such as Paulus Hook, Van Vorst Park and Hamilton Park are lined with 19th-century brownstones and brick row houses with shared walls, flat roofs and ornate cornices. The Heights and Journal Square have frame two- and three-family homes. Along the waterfront, Newport, Exchange Place and Liberty Harbor hold dozens of high-rise condominiums insured under association master policies. Greenville and Bergen-Lafayette add a mix of older homes and new construction.</p>
<h2>Sandy and after</h2>
<p>In 2012 Sandy’s surge flooded much of downtown Jersey City, filling basements, garages and PATH stations. Since then, the city has raised building standards in flood zones, but wind-driven rain, roof failures and plumbing leaks in tall buildings remain the most common claims we see here.</p>
<h2>Jersey City disputes we handle</h2>
<ul>
<li>Condo water losses that move down several floors and touch master and unit-owner policies.</li>
<li>Brownstone roof and cornice repairs priced without specialty masonry or historic details.</li>
<li>Party-wall fire and smoke damage between attached homes.</li>
<li>Curtain-wall and window leaks in towers during wind-driven rain.</li>
</ul>
<p>We work in Downtown, Paulus Hook, Hamilton Park, The Heights, Journal Square, McGinley Square, West Side, Bergen-Lafayette, Greenville and the waterfront, and in neighboring Hoboken, Bayonne and Union City.</p>
""",
        "faqs": [
            ("My condo was damaged by a leak from the unit above. Whose policy pays?", "It depends on the association’s bylaws, the master policy and both owners’ HO-6 policies. We value the damage so each policy’s share can be applied."),
            ("Do historic district rules affect repairs in Jersey City?", "They can. Properties in designated historic districts may need approval for exterior work and specific materials. Ordinance-or-law coverage may help pay for the added cost."),
        ],
    },
    {
        "slug": "paterson", "city": "Paterson", "county": "Passaic County", "region": "Gateway North Jersey",
        "perils": ["River flooding", "Basement water", "Multi-family fires", "Ice dams", "Wind"],
        "near": ["hackensack", "newark", "morristown"],
        "housing": "Frame multi-family homes, brick mill buildings, hillside single-families",
        "lede": "Built around the Great Falls of the Passaic, Paterson has old mill buildings, dense multi-family blocks and neighborhoods that know exactly how high the river can rise.",
        "body": """
<h2>A river city</h2>
<p>The Passaic River wraps around Paterson on three sides. Hurricane Irene in 2011 brought some of the worst flooding in the city’s modern history, and the remnants of Ida flooded neighborhoods again in 2021. Most of that flood water is a matter for flood insurance, not homeowners coverage, which makes separating flood damage from wind, rain and plumbing damage especially important here.</p>
<h2>Paterson’s housing</h2>
<p>The Eastside has large early-1900s homes on wide streets. Riverside, People’s Park and the Northside are dense with frame two- and three-family houses. The historic district around the Great Falls holds 19th-century brick mill buildings, many converted to apartments and businesses. Hillcrest and the Totowa section have single-family homes on hillside lots.</p>
<h2>Claims we see in Paterson</h2>
<ul>
<li>Roof and interior damage from wind-driven rain during storms that also flooded the street.</li>
<li>Multi-family fires that spread through balloon framing.</li>
<li>Masonry and roof repairs on converted mill buildings.</li>
<li>Winter water losses from frozen pipes in older multi-family homes.</li>
</ul>
<p>We serve Paterson and surrounding Passaic County communities, including Clifton, Passaic, Totowa, Haledon, Wayne and Little Falls.</p>
""",
        "faqs": [
            ("My basement flooded and my roof leaked in the same storm. How is that handled?", "Usually as two claims: flood damage under a flood policy and roof or rain damage under the homeowners policy. Clear photos and notes about where water entered help each policy pay its share."),
            ("Do you work with owners of converted mill buildings?", "Yes. Older masonry buildings need specialty repairs that general estimates often miss."),
        ],
    },
    {
        "slug": "hackensack", "city": "Hackensack", "county": "Bergen County", "region": "Gateway North Jersey",
        "perils": ["Tidal & river flooding", "Tree fall", "Hail", "Wind", "High-rise water losses"],
        "near": ["paterson", "jersey-city", "newark"],
        "housing": "Colonials, garden apartments, Prospect Avenue high-rises",
        "lede": "Bergen County’s seat sits on the Hackensack River, with older colonials on tree-lined streets, garden apartment complexes and a row of high-rises along Prospect Avenue.",
        "body": """
<h2>Bergen County claims start here</h2>
<p>Bergen is New Jersey’s most populous county, and Hackensack is its legal and medical hub. Neighborhoods like Fairmount and the streets west of Prospect Avenue have 1920s and 1930s colonials and Tudors under mature oaks. Garden apartment complexes and co-ops date from the postwar decades, and Prospect Avenue is lined with high-rise condos and co-ops.</p>
<h2>Weather in the Hackensack area</h2>
<p>The Hackensack River and its tributaries flood in heavy rain, and the lower Meadowlands are affected by tides. Ida’s remnants flooded streets and basements across Bergen County in 2021. The Halloween nor’easter of 2011 brought down thousands of trees in the county, and summer thunderstorms bring hail and wind several times a decade.</p>
<h2>Common disputes in Hackensack and Bergen County</h2>
<ul>
<li>Tree damage to roofs and framing priced as simple repairs.</li>
<li>Slate and tile roofs on older homes priced as asphalt shingle.</li>
<li>Co-op and condo water losses split between master and unit policies.</li>
<li>Hail damage to siding and gutters left out of roof-only estimates.</li>
</ul>
<p>We serve Hackensack and neighboring Bergen County towns, including Teaneck, River Edge, Maywood, Paramus, Englewood, Fort Lee and Lodi.</p>
""",
        "faqs": [
            ("Do co-op buildings use the appraisal clause?", "Yes. The co-op corporation’s building policy usually contains appraisal language. Individual shareholders’ HO-6 policies have their own."),
            ("A tree from the town right-of-way fell on my house. Who pays?", "Your homeowners policy usually responds first. Whether the town is liable depends on notice and other facts, which is a question for an attorney."),
        ],
    },
    {
        "slug": "edison", "city": "Edison", "county": "Middlesex County", "region": "Central Jersey",
        "perils": ["Flash flooding", "Wind", "Hail", "Tree fall", "Burst pipes"],
        "near": ["trenton", "long-branch", "morristown"],
        "housing": "Split-levels, ranches, colonials, townhome communities",
        "lede": "One of New Jersey’s largest townships, Edison is a patchwork of 1950s split-levels, newer colonials and townhome communities, with Route 1 commerce running through the middle.",
        "body": """
<h2>Central Jersey suburbs</h2>
<p>Edison grew fast after World War II. Neighborhoods such as Clara Barton, Menlo Park, Oak Tree and North Edison are filled with ranches, split-levels and bi-levels from the 1950s and 1960s, now often expanded with additions and finished basements. Newer colonials and townhome associations fill the rest. Route 1 and Route 27 carry retail centers, offices and Raritan Center’s warehouses.</p>
<h2>Storm history around Edison</h2>
<p>Tropical Storm Floyd in 1999 brought record flooding along the Raritan River and its tributaries in Middlesex and Somerset counties. The remnants of Ida flooded roads and homes across the area in 2021. Wind and hail from summer storms, plus ice and tree damage in winter, make up most homeowner claims here.</p>
<h2>Disputes we see in Edison</h2>
<ul>
<li>Additions and finished basements left out of a water loss scope.</li>
<li>Roof replacements priced without the second layer that older split-levels often carry.</li>
<li>Townhome association roof claims split by building without a consistent scope.</li>
<li>Warehouse and retail roof losses in Raritan Center and along Route 1.</li>
</ul>
<p>We serve all of Edison and nearby Middlesex County communities, including Metuchen, Highland Park, New Brunswick, Piscataway, South Plainfield and Woodbridge.</p>
""",
        "faqs": [
            ("My finished basement was damaged by a sump pump failure. Is that covered?", "Not under the base homeowners policy in many cases. Water backup coverage is usually an endorsement with its own limit. Check your declarations page."),
            ("Can townhome associations use appraisal for a single building?", "Yes. The association can dispute the amount of loss on any building covered by its policy."),
        ],
    },
    {
        "slug": "morristown", "city": "Morristown", "county": "Morris County", "region": "Skylands & Highlands",
        "perils": ["Tree fall", "Ice dams", "Heavy snow", "Wind", "Frozen pipes"],
        "near": ["paterson", "edison", "hackensack"],
        "housing": "Victorians, colonials, historic downtown buildings",
        "lede": "Morristown’s historic Green, Victorian homes and wooded hills give it plenty of character. They also make it one of the busiest areas in New Jersey for tree, snow and ice claims.",
        "body": """
<h2>Historic homes under old trees</h2>
<p>Morris County’s seat is known for its Revolutionary War history and its Victorian and colonial homes. Neighborhoods near the Green, along Franklin Street and in the surrounding Morris Township have large homes under mature oaks and maples, many with slate roofs, wood siding and plaster interiors. Downtown holds older commercial and mixed-use buildings.</p>
<h2>Winter weather and trees</h2>
<p>Morristown sits higher and colder than the coastal plain, so winter claims dominate. The Halloween nor’easter of 2011 dropped heavy snow on trees in full leaf, leaving Morris County with some of the worst tree damage and longest power outages in the state. Ice dams form on older homes with little attic insulation, and frozen pipes follow every hard cold snap.</p>
<h2>Disputes we handle in Morristown</h2>
<ul>
<li>Tree removal with cranes priced as basic ground work.</li>
<li>Slate roof repairs priced as asphalt shingle.</li>
<li>Ice-dam water damage cut to a single room when it ran through walls.</li>
<li>Historic exterior details and materials left out of the scope.</li>
</ul>
<p>We serve Morristown, Morris Township, Morris Plains, Madison, Mendham, Parsippany, Randolph and the rest of Morris County.</p>
""",
        "faqs": [
            ("Does my policy cover removing a tree that fell on my house?", "Removing the tree from the house is usually part of the structure claim. Hauling it away from the yard is debris removal, which often has a per-tree limit. Our fallen tree calculator walks through the math."),
            ("Are ice dams a covered claim?", "Interior damage from ice dams is commonly covered. Removing the ice and improving insulation usually is not. Document the damage before repairs."),
        ],
    },
    {
        "slug": "trenton", "city": "Trenton", "county": "Mercer County", "region": "Central Jersey",
        "perils": ["River & creek flooding", "Rowhouse fires", "Roof leaks", "Wind", "Burst pipes"],
        "near": ["edison", "cherry-hill", "toms-river"],
        "housing": "Brick rowhouses, Victorians, state office buildings",
        "lede": "The state capital has some of New Jersey’s oldest neighborhoods. Brick rowhouses in Chambersburg, Victorians in Mill Hill and stately homes in Hiltonia all bring their own claim problems.",
        "body": """
<h2>A city of rowhouses and history</h2>
<p>Trenton’s housing is old and dense. Chambersburg, Wilbur and North Trenton are lined with brick rowhouses with flat roofs and shared walls. Mill Hill is a historic district of restored 19th-century homes. Hiltonia, Glen Afton and Cadwalader Heights have larger early-1900s homes on tree-lined streets. Downtown holds state office buildings and older commercial blocks.</p>
<h2>Flooding and storms</h2>
<p>Trenton sits on a major river at the fall line, and the river flooded the city’s low-lying areas in 2004, 2005 and 2006. Assunpink Creek, which runs through downtown, floods in heavy rain. Wind-driven rain and roof leaks in flat-roofed rowhouses are the most common homeowner claims we see in the city.</p>
<h2>Trenton disputes we handle</h2>
<ul>
<li>Flat-roof membrane and parapet repairs on rowhouses.</li>
<li>Fire and smoke damage between attached homes.</li>
<li>Historic district repairs that need specific materials.</li>
<li>Water losses in older buildings with outdated plumbing.</li>
</ul>
<p>We serve Trenton and nearby Mercer County communities, including Hamilton, Ewing, Lawrence, Princeton, Hopewell and Robbinsville.</p>
""",
        "faqs": [
            ("The fire next door damaged my rowhouse. Who do I claim against?", "Usually your own policy first. Your insurer may then seek recovery from the neighbor’s insurer if the neighbor was at fault."),
            ("Does Mill Hill’s historic designation affect repairs?", "Exterior work in designated historic districts may need review and specific materials. Ordinance-or-law coverage can help with the added cost."),
        ],
    },
    {
        "slug": "toms-river", "city": "Toms River", "county": "Ocean County", "region": "Jersey Shore",
        "perils": ["Coastal storms", "Wildfire smoke", "Wind", "Tree fall", "Frozen pipes"],
        "near": ["long-branch", "atlantic-city", "ocean-city"],
        "housing": "Capes, ranches, bayfront bungalows, elevated rebuilds",
        "lede": "Ocean County’s seat runs from the barrier island at Ortley Beach to neighborhoods along the edge of the Pine Barrens. Few towns in New Jersey see both coastal storms and wildfire risk so close together.",
        "body": """
<h2>From the barrier island to the pines</h2>
<p>Toms River covers about 50 square miles. Ortley Beach, on the barrier island, was one of the hardest-hit communities in the state when Sandy came ashore in 2012; many homes there have since been rebuilt or raised. On the mainland, neighborhoods like Silverton, Gilford Park and the areas along Barnegat Bay have capes, ranches and bayfront bungalows. North Dover and the western sections back up to pine forest.</p>
<h2>Two very different risks</h2>
<p>Coastal storms bring wind, wind-driven rain and surge, which means homeowners and flood claims often overlap. Inland, the Pinelands bring wildfire risk. The 2007 Warren Grove fire and the 2025 Jones Road Wildfire both burned large areas of Ocean County and sent smoke into nearby neighborhoods.</p>
<h2>Disputes we see in Toms River</h2>
<ul>
<li>Wind and flood damage on the same home, split unevenly between policies.</li>
<li>Elevated homes with stairs, decks and utilities left out of the scope.</li>
<li>Smoke damage from wildfire dismissed because the house didn’t burn.</li>
<li>Roof and siding damage from nor’easters.</li>
</ul>
<p>We serve Toms River and nearby Ocean County communities, including Brick, Lakewood, Berkeley, Lacey, Manchester, Seaside Heights and Island Heights.</p>
""",
        "faqs": [
            ("My shore home was damaged by wind and storm surge. How do the claims work?", "Usually as two claims: flood damage under a flood policy and wind damage under the homeowners policy. Documenting what was damaged by each cause is the key."),
            ("Wildfire smoke got into my home during an evacuation. Is that covered?", "Smoke damage is commonly covered under homeowners policies. The question is usually how much cleaning or replacement is needed."),
        ],
    },
    {
        "slug": "long-branch", "city": "Long Branch", "county": "Monmouth County", "region": "Jersey Shore",
        "perils": ["Nor’easters", "Coastal surge", "Wind-driven rain", "Salt corrosion", "Condo losses"],
        "near": ["toms-river", "edison", "atlantic-city"],
        "housing": "Victorians, oceanfront condos, bungalows",
        "lede": "Long Branch has been a shore resort since the 1800s. Victorian homes in Elberon, oceanfront condos at Pier Village and bungalows in the West End all face the Atlantic head-on.",
        "body": """
<h2>A historic shore city</h2>
<p>Long Branch was a summer resort for presidents in the 19th century, and some of that history remains in Elberon’s large Victorian and Colonial Revival homes. The West End and North Long Branch have smaller homes and bungalows. Pier Village and the oceanfront hold newer condo buildings, many insured under association master policies.</p>
<h2>Storms on the Monmouth County coast</h2>
<p>Sandy’s surge damaged much of the Monmouth County coast in 2012, including nearby Sea Bright and Monmouth Beach. Nor’easters bring days of onshore wind, surf and rain, and salt air shortens the life of roofing, siding and HVAC equipment.</p>
<h2>Disputes we see in Long Branch</h2>
<ul>
<li>Condo master policy claims for roofs, windows and balconies.</li>
<li>Wind-driven rain through older windows and doors.</li>
<li>Historic home repairs needing specialty materials.</li>
<li>Wind and flood damage split between policies.</li>
</ul>
<p>We serve Long Branch and nearby Monmouth County communities, including Asbury Park, Red Bank, Sea Bright, Monmouth Beach, Ocean Township and Eatontown.</p>
""",
        "faqs": [
            ("Does a nor’easter trigger my hurricane deductible?", "Usually not. Hurricane deductibles typically apply only when specific hurricane trigger language is met. Check your policy’s endorsement."),
            ("Our condo association disagrees with the carrier on a roof claim. Can we use appraisal?", "Yes, if the dispute is about the amount of loss and the master policy has an appraisal clause."),
        ],
    },
    {
        "slug": "cherry-hill", "city": "Cherry Hill", "county": "Camden County", "region": "South Jersey",
        "perils": ["Derecho winds", "Hail", "Tree fall", "Burst pipes", "Tornadoes"],
        "near": ["trenton", "atlantic-city", "ocean-city"],
        "housing": "1950s–70s ranches, bi-levels, colonials",
        "lede": "Cherry Hill grew up in the postwar suburban boom, and its neighborhoods of ranches, bi-levels and colonials now face aging roofs, mature trees and South Jersey’s strong summer storms.",
        "body": """
<h2>A postwar suburb, growing older</h2>
<p>Most of Cherry Hill was built between the 1950s and the 1970s. Neighborhoods such as Erlton, Kingston Estates, Barclay Farm, Woodcrest and Old Orchard have ranches, bi-levels, split-levels and colonials, many now on their second or third roof. Route 70 and Route 38 carry retail and office buildings.</p>
<h2>South Jersey weather</h2>
<p>The June 2012 derecho brought down trees and power lines across Camden County. In 2021, the remnants of Ida produced a strong tornado in nearby Mullica Hill in Gloucester County. Summer thunderstorms bring wind and hail, and winter cold snaps cause frozen pipes in older homes.</p>
<h2>Disputes we see in Cherry Hill</h2>
<ul>
<li>Roof replacements denied as wear and tear on older roofs.</li>
<li>Tree damage priced as simple repairs.</li>
<li>Siding that can’t be matched, forcing replacement decisions.</li>
<li>Commercial roof losses along Route 70 and Route 38.</li>
</ul>
<p>We serve Cherry Hill and nearby Camden and Burlington county communities, including Haddonfield, Voorhees, Marlton, Moorestown, Collingswood and Mount Laurel.</p>
""",
        "faqs": [
            ("My roof is 18 years old and the carrier calls the damage wear and tear. Can appraisal help?", "It depends. If the dispute is about the amount of storm damage, appraisal may help. If the carrier denies that a storm caused the damage at all, that may be a coverage question."),
            ("Can you help with commercial property in Cherry Hill?", "Yes. We value retail, office and mixed-use losses throughout Camden County."),
        ],
    },
    {
        "slug": "atlantic-city", "city": "Atlantic City", "county": "Atlantic County", "region": "Jersey Shore",
        "perils": ["Coastal storms", "Wind", "Salt corrosion", "High-rise water losses", "Commercial roofs"],
        "near": ["ocean-city", "toms-river", "cherry-hill"],
        "housing": "Condo towers, elevated homes, commercial and hospitality buildings",
        "lede": "Atlantic City’s Boardwalk, casino towers and neighborhoods like Chelsea and Venice Park sit on a barrier island fully exposed to the Atlantic. Wind and water test every building here.",
        "body": """
<h2>A barrier island city</h2>
<p>Atlantic City sits on Absecon Island, with the Atlantic Ocean on one side and back bays on the other. Chelsea and Ducktown have older homes and apartment buildings. Venice Park and Bungalow Park have smaller homes on lagoons. The Marina District and the Boardwalk hold casino hotels and high-rise condos.</p>
<h2>Storms on Absecon Island</h2>
<p>Sandy came ashore just north of Atlantic City, near Brigantine, in 2012. The Ash Wednesday Storm of 1962 and many nor’easters since have flooded the island and damaged the Boardwalk. Salt air and constant wind wear down roofs, windows and mechanical equipment faster than inland.</p>
<h2>Disputes we see in Atlantic City</h2>
<ul>
<li>Condo tower water losses through windows and balconies.</li>
<li>Commercial roof and HVAC damage.</li>
<li>Wind and flood damage split between policies.</li>
<li>Elevated home repairs on lagoon lots.</li>
</ul>
<p>We serve Atlantic City and nearby Atlantic County communities, including Ventnor, Margate, Brigantine, Egg Harbor Township, Absecon and Galloway.</p>
""",
        "faqs": [
            ("Do you handle commercial and hospitality claims?", "Yes. We value large commercial losses, including roofs, mechanical equipment and interiors."),
            ("Who covers homes the regular market won’t insure?", "The New Jersey Insurance Underwriting Association, the state’s FAIR Plan, offers basic property coverage. Its policies include appraisal language."),
        ],
    },
    {
        "slug": "ocean-city", "city": "Ocean City", "county": "Cape May County", "region": "Jersey Shore",
        "perils": ["Coastal flooding", "Nor’easters", "Wind", "Frozen pipes in seasonal homes", "Salt corrosion"],
        "near": ["atlantic-city", "toms-river", "cherry-hill"],
        "housing": "Up-down duplex condos, elevated single-family homes, beach blocks",
        "lede": "Ocean City’s duplex condos, raised beach houses and bayside lagoon homes face the Atlantic year-round, and many sit empty all winter. That combination shapes almost every claim here.",
        "body": """
<h2>Seasonal homes on a barrier island</h2>
<p>Ocean City is an eight-mile barrier island in Cape May County. Many properties are up-down duplexes split into two condominium units, each with its own owner and policy. The North End and South End have elevated single-family homes, and the bay side has homes on lagoons. Many owners use them only in summer.</p>
<h2>Storms that shaped the island</h2>
<p>The Ash Wednesday Storm of 1962 flooded nearly the whole island. Sandy damaged homes and the boardwalk in 2012. Winter Storm Jonas in January 2016 brought record coastal flooding to parts of Cape May County. Frozen pipes in empty winter homes are among the most common claims we see.</p>
<h2>Disputes we see in Ocean City</h2>
<ul>
<li>Duplex claims where two owners and two policies share a roof.</li>
<li>Frozen pipe losses in vacant homes, where heat and water shutoff matter.</li>
<li>Wind and flood damage on the same home.</li>
<li>Elevated home stairs, decks and utilities left out of the scope.</li>
</ul>
<p>We serve Ocean City and nearby Cape May County communities, including Sea Isle City, Somers Point, Marmora, Strathmere, Avalon and Cape May.</p>
""",
        "faqs": [
            ("My duplex neighbor and I share a roof. How do we handle a claim?", "Each owner claims under their own policy, and any association governing the duplex may also have coverage. We value the shared roof so each policy pays its share."),
            ("My pipes froze while my shore house was empty. Am I covered?", "It depends on the freezing exclusion. Many policies cover freezing only if heat was maintained or the water was shut off and drained."),
        ],
    },
]
