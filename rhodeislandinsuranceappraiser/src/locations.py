"""Location pages: twelve Rhode Island cities and towns. Rhode Island has five counties and no county government;
services are municipal, so pages name the county for orientation only."""

LOCATIONS = [
    {
        "slug": "providence", "city": "Providence", "county": "Providence County", "region": "Capital city",
        "photo": "providence-skyline",
        "lede": "From triple-deckers in Elmhurst to Victorian houses on College Hill and condos downtown, Providence claims cover the widest housing mix in the state.",
        "perils": ["Nor’easter wind", "Ice dams", "Burst pipes", "Hurricane surge history", "Fire in dense blocks"],
        "neighborhoods": ["College Hill", "Fox Point", "Federal Hill", "Elmhurst", "Mount Pleasant", "Wayland Square", "Olneyville", "Elmwood", "Washington Park"],
        "housing": "Providence has a large share of pre-1940 housing: wood-frame two- and three-family houses, brick rowhouses near downtown, large Victorian and Colonial Revival homes on the East Side, and mill buildings converted to lofts in Olneyville and along the Woonasquatucket. Downtown and the Jewelry District add mid- and high-rise condominiums.",
        "storms": [("1938", "The New England Hurricane pushed storm surge into downtown Providence."), ("1954", "Hurricane Carol flooded downtown again, leading to construction of the Fox Point Hurricane Barrier, completed in 1966."), ("2010", "Record March rains flooded rivers across the region."), ("2015 & 2022", "January blizzards brought heavy snow loads and ice dams to older roofs.")],
        "body": """
<p>Insurance appraisal in Providence usually involves older buildings. Plaster walls, slate and cedar roofs, original trim and multi-unit layouts all make repairs more involved than a standard estimate assumes. The city sits at the head of Narragansett Bay, so it has a long hurricane history, but day to day the claims we see most are winter water losses, wind damage from nor’easters and fires that spread between closely spaced houses.</p>
<h2>What makes Providence claims different</h2>
<p>Three-deckers bring shared roofs, porches and stairways that serve several units, and frequently tenants with their own contents claims. East Side homes in the College Hill Historic District may face review requirements for exterior changes, which can affect how repairs are done. Condo owners downtown deal with a master policy and their own unit policy at the same time.</p>
<h2>Hurricane barrier, but not hurricane-proof</h2>
<p>The Fox Point Hurricane Barrier protects downtown from storm surge, but it doesn’t stop wind. Roofs, windows and trees across the city are still exposed when a tropical system passes, and neighborhoods outside the barrier’s protection can see flooding.</p>""",
        "faqs": [("Do you inspect in all Providence neighborhoods?", "Yes. We inspect throughout the city, from Mount Pleasant and Elmhurst to Fox Point, Elmwood and Washington Park."), ("Does historic district review affect my claim?", "It can affect the materials and methods a repair needs. If a local commission requires a certain material, that belongs in the scope and the cost discussion."), ("My tenants were affected too. Can you help?", "We value the building loss under your policy and help you separate what belongs to tenants’ own renters policies.")],
        "near": ["pawtucket", "east-providence", "cranston"],
    },
    {
        "slug": "warwick", "city": "Warwick", "county": "Kent County", "region": "Kent County & West Bay",
        "photo": "warwick-shore",
        "lede": "Warwick has dozens of miles of bay shoreline and the Pawtuxet River running through it. Coastal wind and river flooding both shape claims here.",
        "perils": ["River flooding (flood policy)", "Coastal wind", "Tree fall", "Ice dams", "Water damage"],
        "neighborhoods": ["Pawtuxet Village", "Conimicut", "Oakland Beach", "Apponaug", "Warwick Neck", "Gaspee Plateau", "Buttonwoods", "Cowesett"],
        "housing": "Most of Warwick’s housing went up after World War II: capes, ranches and raised ranches on modest lots, with older cottages that became year-round homes near Oakland Beach, Conimicut and Buttonwoods, and larger waterfront houses on Warwick Neck.",
        "storms": [("1938 & 1954", "The 1938 hurricane and Hurricane Carol devastated the Oakland Beach shoreline."), ("2010", "The Pawtuxet River reached record levels in March, flooding homes and businesses in Warwick and Cranston."), ("2012", "Superstorm Sandy brought surge and wind damage to the Warwick shore."), ("2017", "An October nor’easter downed trees and power lines across Kent County.")],
        "body": """
<p>Insurance appraisal in Warwick often starts with a question about water. The March 2010 flood showed how far the Pawtuxet River can rise, and homes along the bay remember the surge from past hurricanes. Flood damage falls under a flood policy, not a homeowner policy, so we spend time separating wind and rain damage, which a homeowner policy may cover, from rising water, which it generally excludes.</p>
<h2>Typical Warwick claims</h2>
<ul>
<li>Roof and siding damage on exposed shoreline neighborhoods during nor’easters</li>
<li>Trees down on houses and garages in older, wooded neighborhoods</li>
<li>Ice dams on capes with finished upper floors and little attic space</li>
<li>Basement and interior water damage from burst pipes or appliance leaks</li>
</ul>
<h2>Capes and ranches</h2>
<p>Postwar construction is simpler to scope than a Victorian, but estimates still miss items: knee-wall insulation behind ice-dam leaks, the full run of matching siding or the second layer of roofing that has to come off.</p>""",
        "faqs": [("Can appraisal resolve a flood claim?", "Many flood policies, including those through the NFIP, have their own appraisal provisions with different rules. Your homeowner policy’s appraisal clause applies to covered homeowner losses, which generally exclude flood."), ("Do you work near the airport and Apponaug?", "Yes. We inspect throughout Warwick."), ("My cape had an ice-dam leak. What gets missed?", "Wet insulation behind knee walls, ceiling and wall finishes to a logical break, and damaged roofing at the eaves are the usual gaps.")],
        "near": ["cranston", "coventry", "north-kingstown"],
    },
    {
        "slug": "cranston", "city": "Cranston", "county": "Providence County", "region": "Providence metro",
        "photo": "triple-decker",
        "lede": "Cranston runs from dense neighborhoods near Providence to farms and woods in the west, so a claim can mean a triple-decker or a rural colonial with a well.",
        "perils": ["River flooding history", "Tree fall", "Nor’easter wind", "Ice dams", "Fire"],
        "neighborhoods": ["Edgewood", "Pawtuxet", "Garden City", "Knightsville", "Eden Park", "Auburn", "Western Cranston"],
        "housing": "Eastern Cranston has early twentieth-century homes and multi-family houses in Edgewood and near Pawtuxet Village. Garden City and Knightsville have postwar neighborhoods. Western Cranston is more rural, with larger lots, newer colonials and older farmhouses.",
        "storms": [("2010", "The Pawtuxet River crested at a record level at the Cranston gauge during the March floods."), ("2011", "Tropical Storm Irene brought down trees across the city."), ("2015", "The January blizzard dropped heavy snow on roofs."), ("2017", "An October nor’easter caused widespread tree and power-line damage.")],
        "body": """
<p>Insurance appraisal in Cranston reflects a city with two personalities. Near Providence, closely spaced houses mean wind, fire and water damage can affect more than one building. In western Cranston, mature trees and long driveways make storm cleanup and access part of the loss.</p>
<h2>Claims we see in Cranston</h2>
<ul>
<li>Tree impacts on roofs and porches after nor’easters and tropical storms</li>
<li>Wind damage to roofs and vinyl siding, with matching questions on the undamaged sides</li>
<li>Interior water losses from burst pipes and ice dams</li>
<li>Fire and smoke damage in multi-family homes</li>
</ul>
<h2>Edgewood and Pawtuxet homes</h2>
<p>Many Edgewood houses have original details, from leaded windows to hardwood floors laid in patterns. Replacing those properly costs more than a generic line item, and we price them accordingly.</p>""",
        "faqs": [("Do you inspect in western Cranston?", "Yes, including rural properties with outbuildings, which may fall under other structures coverage."), ("A neighbor’s tree hit my house. Whose policy pays?", "Usually your own policy covers damage to your house, whoever owned the tree. Your insurer may pursue the neighbor if negligence is involved."), ("Can you match old hardwood flooring?", "We price the work needed to achieve a reasonable match, which can include more area than the damaged boards alone.")],
        "near": ["providence", "warwick", "coventry"],
    },
    {
        "slug": "pawtucket", "city": "Pawtucket", "county": "Providence County", "region": "Blackstone Valley",
        "photo": "pawtucket-falls",
        "lede": "The birthplace of the American industrial revolution has mill buildings, triple-deckers and the Blackstone River, and claims shaped by all three.",
        "perils": ["Nor’easter wind", "Ice dams", "Burst pipes", "Fire", "Flat-roof leaks"],
        "neighborhoods": ["Darlington", "Oak Hill", "Fairlawn", "Woodlawn", "Quality Hill", "Pleasant View", "Downtown"],
        "housing": "Pawtucket is a city of two- and three-family houses, many over a century old, with nineteenth-century mill complexes along the Blackstone and Moshassuck rivers. Darlington and Oak Hill have larger single-family homes, and downtown has brick commercial blocks.",
        "storms": [("1955", "Floods from hurricanes Connie and Diane swelled the Blackstone River."), ("2010", "March flooding hit the Blackstone Valley."), ("2015", "Heavy January snow loaded flat roofs on triple-deckers."), ("2024", "Winter storms in December 2023 and January 2024 brought heavy rain, wind and river flooding to the region.")],
        "body": """
<p>Insurance appraisal in Pawtucket often involves flat or low-slope roofs on three-deckers, where a membrane failure or ice buildup lets water into the top-floor unit and down through the building. Shared stairways, back porches and party walls mean one loss can touch several households.</p>
<h2>Mill buildings and mixed-use blocks</h2>
<p>Converted mills now hold apartments, studios and businesses. Their brick walls, timber framing and large window systems call for specialist pricing, and the claims can involve both a building owner and several commercial tenants.</p>
<h2>What owners of multi-family homes should gather</h2>
<ul>
<li>Leases and rent records if units are uninhabitable (loss of rents)</li>
<li>Photos of each unit and common area</li>
<li>Invoices for emergency roof tarping, water extraction or board-up</li>
</ul>""",
        "faqs": [("Do you handle three-decker roof claims?", "Yes. Low-slope roofs on three-deckers are among the most common building claims in Pawtucket."), ("Can you value mill building damage?", "Yes. We scope masonry, timber and window systems, and bring in specialists when the loss requires it."), ("What if units are uninhabitable?", "Many landlord policies include loss of rents. We value the building damage, and you document the rent loss with leases and records.")],
        "near": ["providence", "east-providence", "woonsocket"],
    },
    {
        "slug": "east-providence", "city": "East Providence", "county": "Providence County", "region": "East Bay",
        "photo": "condo-building",
        "lede": "With the Seekonk and Providence rivers on one side and the bay to the south, East Providence claims mix shoreline exposure with older neighborhoods.",
        "perils": ["Coastal wind", "Storm surge (flood policy)", "Tree fall", "Ice dams", "Water damage"],
        "neighborhoods": ["Riverside", "Rumford", "Watchemoket", "Phillipsdale", "Kent Heights", "Bullocks Point"],
        "housing": "East Providence has early twentieth-century houses in Rumford and Watchemoket, cottage communities that grew into year-round neighborhoods in Riverside, postwar capes and ranches, and condominium developments along the waterfront.",
        "storms": [("1938", "The hurricane battered Riverside and the bay shore."), ("1954", "Hurricane Carol’s surge damaged waterfront property along the upper bay."), ("2012", "Superstorm Sandy brought wind and high water to the shoreline."), ("2017", "The October nor’easter caused widespread outages and tree damage.")],
        "body": """
<p>Insurance appraisal in East Providence covers everything from Riverside cottages a few feet above high tide to Rumford colonials on tree-lined streets. Shoreline homes see wind-driven rain and occasional surge; inland neighborhoods see more tree and ice-dam damage.</p>
<h2>Shoreline and condo claims</h2>
<p>Waterfront condominium associations deal with exposed roofs, decks and siding. When a storm damages common elements, the association’s master policy responds, and unit owners may have their own claims for interior finishes. We help boards value the common-element loss.</p>
<h2>Riverside cottages</h2>
<p>Many Riverside homes started as summer cottages and were expanded over the decades. Additions built at different times can have different framing and roofing, which matters when scoping a repair.</p>""",
        "faqs": [("Do you work with condo associations in East Providence?", "Yes. We value common-element damage under the master policy and coordinate with the board and manager."), ("My cottage has several additions. Does that complicate the claim?", "It can. Different construction eras mean different materials and methods, and a good scope accounts for each."), ("Is surge covered by my homeowner policy?", "Generally no. Storm surge is treated as flood and covered, if at all, under a separate flood policy.")],
        "near": ["providence", "pawtucket", "bristol"],
    },
    {
        "slug": "woonsocket", "city": "Woonsocket", "county": "Providence County", "region": "Blackstone Valley",
        "photo": "woonsocket-mill",
        "lede": "Woonsocket’s triple-deckers, mill buildings and hilly streets along the Blackstone River make for claims that are rarely simple.",
        "perils": ["Ice dams", "Snow load", "Burst pipes", "Fire", "Nor’easter wind"],
        "neighborhoods": ["Social", "Fairmount", "North End", "Constitution Hill", "East Woonsocket", "Globe", "Bernon"],
        "housing": "Woonsocket grew as a mill city, and its housing shows it: blocks of wood-frame three-deckers and two-family homes, large mill complexes along the Blackstone, and single-family neighborhoods in the North End and East Woonsocket.",
        "storms": [("1955", "The August flood from hurricanes Connie and Diane devastated parts of Woonsocket."), ("1978", "The Blizzard of 1978 buried northern Rhode Island."), ("2010", "Record March rains raised the Blackstone again."), ("2015 & 2022", "January blizzards loaded roofs across the city.")],
        "body": """
<p>Insurance appraisal in Woonsocket is shaped by winter. Northern Rhode Island tends to get more snow than the coast, and older multi-family homes with flat or shallow roofs collect it. Ice dams, snow-load damage and frozen pipes in unheated hallways and vacant units are common claims.</p>
<h2>Older multi-family homes</h2>
<p>Many three-deckers have balloon framing, plaster walls and original stairways. When water runs down through three floors, a complete scope includes every unit and the common areas, not just the top floor where the leak began.</p>
<h2>Fire losses</h2>
<p>Fires in closely spaced wood-frame buildings can damage neighboring houses with heat and smoke. If your building was damaged by a fire next door, your own policy usually responds first.</p>""",
        "faqs": [("Do you handle snow-load and ice-dam claims in Woonsocket?", "Yes. Winter losses are among the most common claims in northern Rhode Island."), ("Our building was damaged by a fire next door. What now?", "Report it to your own insurer. Smoke, heat and water damage to your building are typically handled under your policy."), ("Do you inspect mill buildings?", "Yes, for owners and associations, with specialists for masonry and structural work when needed.")],
        "near": ["pawtucket", "providence", "coventry"],
    },
    {
        "slug": "newport", "city": "Newport", "county": "Newport County", "region": "Aquidneck Island",
        "photo": "newport-harbor",
        "lede": "Colonial houses on the Point, Gilded Age mansions on Bellevue Avenue and a coastline open to the Atlantic make Newport claims highly specialized.",
        "perils": ["Hurricane wind", "Salt spray & wind-driven rain", "Storm surge (flood policy)", "Historic materials", "Ice dams"],
        "neighborhoods": ["The Point", "Historic Hill", "Fifth Ward", "Bellevue Avenue", "Ocean Drive", "Broadway", "Kay-Catherine", "Easton’s Point"],
        "housing": "Newport has one of the largest concentrations of colonial-era buildings in the country, much of it in the Point and Historic Hill. Bellevue Avenue and Ocean Drive have large estates and shingle-style houses, and neighborhoods like the Fifth Ward and Broadway have dense wood-frame homes.",
        "storms": [("1938", "The New England Hurricane caused major damage along the Newport shore."), ("1954", "Hurricane Carol flooded the waterfront."), ("1991", "Hurricane Bob damaged boats, docks and coastal property."), ("2012", "Superstorm Sandy damaged the Cliff Walk and shoreline areas.")],
        "body": """
<p>Insurance appraisal in Newport often hinges on materials and methods. Historic district rules can affect which windows, siding, roofing and trim a repair can use. Old-growth wood, hand-split shingles, slate, copper flashing and period millwork cost far more than modern stand-ins, and estimates that assume otherwise come up short.</p>
<h2>Exposure on Aquidneck Island</h2>
<p>Ocean Drive and the southern shore face the open Atlantic. Wind-driven rain and salt spray work into siding and windows during nor’easters and tropical storms, and surge affects low-lying waterfront areas. We separate wind and rain damage from flood damage so each policy is presented with the right scope.</p>
<h2>Large and high-value homes</h2>
<p>Estate homes may carry high-value policies with guaranteed or extended replacement cost. Valuing them takes detailed scopes, specialty trades and sometimes architects or conservators.</p>""",
        "faqs": [("Do historic district rules affect what my claim should pay?", "If the city requires specific materials or methods, the cost of meeting that requirement may be part of the repair. Ordinance-or-law coverage can also matter."), ("Do you work on high-value estate homes?", "Yes. These claims often need specialty trades and detailed documentation."), ("Do you cover Middletown, Portsmouth and Jamestown too?", "Yes. We work throughout Newport County.")],
        "near": ["bristol", "narragansett", "north-kingstown"],
    },
    {
        "slug": "westerly", "city": "Westerly", "county": "Washington County", "region": "South County shore",
        "photo": "westerly-beach",
        "lede": "Westerly’s Misquamicut, Watch Hill and Weekapaug face the open ocean. Hurricane history here runs from 1938 to Henri’s landfall in 2021.",
        "perils": ["Hurricane wind", "Storm surge (flood policy)", "Sand & wind-driven rain", "Hurricane deductibles", "Tree fall inland"],
        "neighborhoods": ["Misquamicut", "Watch Hill", "Weekapaug", "Dunn’s Corners", "Bradford", "Downtown Westerly", "Avondale"],
        "housing": "Westerly mixes year-round village neighborhoods with summer and seasonal homes near the beaches: shingle-style houses in Watch Hill, cottages and newer elevated homes in Misquamicut, and older houses near downtown and the Pawcatuck River.",
        "storms": [("1938", "The New England Hurricane destroyed hundreds of homes along Westerly’s barrier beaches."), ("1954", "Hurricane Carol struck the shore again."), ("2012", "Superstorm Sandy pushed sand and water through Misquamicut."), ("2021", "Hurricane Henri made landfall near Westerly as a tropical storm.")],
        "body": """
<p>Insurance appraisal in Westerly almost always starts with the hurricane deductible. When a named storm triggers it, the deductible can be thousands of dollars, so getting the total wind loss right matters even more. The second question is usually wind versus water: barrier-beach homes can have both in the same storm.</p>
<h2>Seasonal homes</h2>
<p>Many Westerly properties sit empty for part of the year. Storm damage can go unnoticed for days, and winter vacancy raises questions about heat and water shut-off. Documenting when the damage happened and when you found it helps.</p>
<h2>What we scope after a coastal storm</h2>
<ul>
<li>Roofing, siding, windows and doors damaged by wind</li>
<li>Interior damage from wind-driven rain, distinguished from flood water lines</li>
<li>Decks, railings and outdoor showers under the dwelling or other structures</li>
<li>Sand and debris cleanup tied to covered damage</li>
</ul>""",
        "faqs": [("Did Henri trigger hurricane deductibles?", "Whether a hurricane deductible applied to a particular storm depends on the trigger language in each policy. We review that wording as part of any coastal claim."), ("My summer house was damaged while I was away. Is that a problem?", "Not by itself. Report it promptly once you know, and document when you discovered the damage."), ("Can appraisal resolve wind damage when there’s also flood damage?", "Appraisal under the homeowner policy can value the wind damage. Flood damage is handled under a flood policy and its own process.")],
        "near": ["narragansett", "north-kingstown", "coventry"],
    },
    {
        "slug": "narragansett", "city": "Narragansett", "county": "Washington County", "region": "South County shore",
        "photo": "point-judith-light",
        "lede": "From the Pier to Point Judith and Bonnet Shores, Narragansett homes face the ocean and the bay. Coastal wind and water shape most claims.",
        "perils": ["Hurricane wind", "Nor’easter waves", "Storm surge (flood policy)", "Salt corrosion", "Ice dams"],
        "neighborhoods": ["Narragansett Pier", "Point Judith", "Galilee", "Bonnet Shores", "Scarborough", "Eastward Look", "Wakefield (nearby)"],
        "housing": "Narragansett has Victorian-era summer houses near the Pier, postwar cottages in Bonnet Shores and Eastward Look, year-round homes inland, and many rental properties near the University of Rhode Island.",
        "storms": [("1938", "The hurricane struck the Narragansett shoreline hard."), ("1954", "Hurricane Carol flooded Galilee and coastal neighborhoods."), ("2012", "Superstorm Sandy damaged the Ocean Road seawall and shoreline businesses."), ("2018", "March nor’easters brought wind and coastal flooding.")],
        "body": """
<p>Insurance appraisal in Narragansett covers a coastline where nor’easter waves and hurricane surge are facts of life. Homes near Ocean Road, Point Judith and Bonnet Shores see salt spray, wind-driven rain and, in strong storms, water. Inland homes see more ice-dam and tree damage.</p>
<h2>Rental properties</h2>
<p>Many Narragansett houses are rented seasonally or to students. Landlord policies (often written on dwelling forms) differ from owner-occupied homeowner policies, so we read the form closely before valuing the loss.</p>
<h2>Salt and wind</h2>
<p>Salt air shortens the life of fasteners, flashing and siding. When storm damage meets aged materials, the claim can turn into a debate about depreciation and wear. We document storm-created damage separately from pre-existing conditions.</p>""",
        "faqs": [("Do you inspect rental properties in Narragansett?", "Yes. We review the dwelling or landlord policy form and value the covered loss."), ("Is wear from salt air covered?", "Gradual wear generally isn’t. Storm damage is. We document the difference carefully."), ("Do you work in South Kingstown and Wakefield too?", "Yes. We work throughout Washington County.")],
        "near": ["westerly", "north-kingstown", "newport"],
    },
    {
        "slug": "bristol", "city": "Bristol", "county": "Bristol County", "region": "East Bay",
        "photo": "bristol-harbor",
        "lede": "Bristol’s Federal and colonial houses on Hope Street and its waterfront on three sides mean historic materials and bay exposure in the same claim.",
        "perils": ["Coastal wind", "Storm surge (flood policy)", "Historic materials", "Ice dams", "Tree fall"],
        "neighborhoods": ["Hope Street", "Downtown Waterfront", "Poppasquash Point", "Silver Creek", "Bristol Highlands", "Mount Hope"],
        "housing": "Bristol’s downtown has many eighteenth- and nineteenth-century homes, with larger estates on Poppasquash Point, postwar neighborhoods inland and newer homes near the town’s edges.",
        "storms": [("1938", "The New England Hurricane flooded Bristol’s waterfront."), ("1954", "Hurricane Carol drove surge into the harbor."), ("1991", "Hurricane Bob damaged trees and waterfront property."), ("2012", "Superstorm Sandy brought high water and wind to the East Bay.")],
        "body": """
<p>Insurance appraisal in Bristol often involves an old house near the water. Clapboard, wood shingles, plaster and period windows on downtown homes need careful matching, and waterfront streets see wind-driven rain and occasional flooding when a storm pushes up the bay.</p>
<h2>Historic homes</h2>
<p>Bristol has a local historic district, and exterior work may need review. When a repair must use particular materials or methods, the cost of doing so belongs in the valuation.</p>
<h2>Across the East Bay</h2>
<p>We also work in Warren and Barrington, where low-lying neighborhoods along the Warren and Palmer rivers and the bay share many of the same storm risks.</p>""",
        "faqs": [("Do you work in Warren and Barrington?", "Yes. We cover all of Bristol County."), ("My old windows were damaged. Will the claim pay for wood replacements?", "If matching the original windows is needed for a reasonable repair, or required by local rules, that can be part of the valuation. Policy wording matters."), ("What about my dock?", "Docks and piers are often limited or excluded. We check how your policy treats them.")],
        "near": ["east-providence", "newport", "providence"],
    },
    {
        "slug": "north-kingstown", "city": "North Kingstown", "county": "Washington County", "region": "West Bay",
        "photo": "wickford-village",
        "lede": "From colonial Wickford Village to Saunderstown and the Quonset business park, North Kingstown claims mix historic homes, shoreline and commercial property.",
        "perils": ["Coastal wind", "Storm surge (flood policy)", "Tree fall", "Ice dams", "Commercial roofs"],
        "neighborhoods": ["Wickford", "Saunderstown", "Quonset", "Davisville", "Hamilton", "Lafayette", "Poplar Point"],
        "housing": "Wickford has one of the state’s best-preserved collections of eighteenth- and nineteenth-century houses. Saunderstown and the shoreline have larger homes, inland neighborhoods are mostly postwar and newer, and Quonset Business Park holds industrial and commercial buildings.",
        "storms": [("1938", "The hurricane flooded Wickford harbor."), ("1954", "Hurricane Carol struck the West Bay shoreline."), ("2011", "Tropical Storm Irene downed trees across Washington County."), ("2012", "Superstorm Sandy brought surge to low-lying shoreline areas.")],
        "body": """
<p>Insurance appraisal in North Kingstown often means valuing an old house in a low-lying village. Wickford’s homes sit close to the harbor, so storms bring both wind and water. Inland, wooded neighborhoods see trees on houses after nor’easters and tropical storms.</p>
<h2>Commercial property at Quonset</h2>
<p>Quonset Business Park holds manufacturing, warehouse and office buildings with large low-slope roofs. Wind damage to membranes, metal panels and rooftop equipment calls for measured scopes and specialist pricing.</p>
<h2>Wickford homes</h2>
<p>Original clapboard, wood shingle and multi-pane windows are typical. We price repairs that respect what is there rather than substituting modern materials that won’t match.</p>""",
        "faqs": [("Do you value commercial roof damage at Quonset?", "Yes. We measure and scope large low-slope roofs and bring in specialists for rooftop equipment."), ("Are Wickford’s historic homes harder to value?", "They require more detail. Original materials and craft methods cost more, and the scope should reflect that."), ("Do you cover Exeter and East Greenwich?", "Yes. We work across Washington and Kent counties.")],
        "near": ["warwick", "narragansett", "westerly"],
    },
    {
        "slug": "coventry", "city": "Coventry", "county": "Kent County", "region": "Western Rhode Island",
        "photo": "ri-farm-field",
        "lede": "Coventry stretches from the mill villages along the Pawtuxet to the woods near the Connecticut line. Trees, snow and river flooding define claims here.",
        "perils": ["Tree fall", "Ice storms & snow", "River flooding history", "Frozen pipes", "Well & septic questions"],
        "neighborhoods": ["Anthony", "Washington", "Quidnick", "Harris", "Greene", "Johnson’s Pond area", "Coventry Center"],
        "housing": "Eastern Coventry has mill-village houses and postwar neighborhoods. Western Coventry is rural, with colonials and farmhouses on larger, wooded lots, many on private wells and septic systems. Homes ring Johnson’s Pond (the Flat River Reservoir).",
        "storms": [("2010", "March flooding along the South Branch of the Pawtuxet affected Coventry and West Warwick."), ("2011", "Tropical Storm Irene brought down trees and power lines."), ("2015", "The January blizzard dropped heavy snow on western Rhode Island."), ("2017", "The October nor’easter caused long outages in Kent County.")],
        "body": """
<p>Insurance appraisal in Coventry often begins with a tree. Western Rhode Island is heavily wooded, and nor’easters, ice storms and tropical systems bring down limbs and whole trees onto roofs, porches, garages and outbuildings. Snow and cold add ice dams and frozen pipes, and long power outages can lead to freeze damage.</p>
<h2>Rural property</h2>
<p>Barns, sheds, detached garages and fences fall under other structures coverage, usually with a separate limit. Wells, pumps and septic systems raise their own coverage questions. We value the building damage and flag those questions for you.</p>
<h2>Mill villages</h2>
<p>Anthony, Washington and Quidnick grew around mills on the Pawtuxet. Their older houses have the same plaster, trim and framing details we see in Pawtucket and Woonsocket.</p>""",
        "faqs": [("A tree damaged my barn. Is that covered?", "Barns and other detached buildings usually fall under other structures coverage, subject to its limit. Appraisal can resolve the cost if coverage is accepted."), ("My pipes froze during a power outage. What should I do?", "Shut off the water, document the damage and report the claim promptly. Freeze coverage often depends on the circumstances."), ("Do you cover Foster, Scituate and West Greenwich?", "Yes. We work throughout western Rhode Island.")],
        "near": ["warwick", "cranston", "westerly"],
    },
]

REGIONS = [
    ("metro", "Providence & Blackstone Valley", "Providence · Pawtucket · Woonsocket",
     ["Ice dams", "Burst pipes", "Flat-roof leaks", "Fire"],
     "The state’s densest housing: three-deckers, Victorian homes and converted mills. Winter water losses and fires that spread between buildings are common, and older materials push repair costs up.",
     "Providence, Pawtucket, Central Falls, Woonsocket, Cumberland, Lincoln, North Providence", "providence-college-hill"),
    ("kent", "Kent County & West Bay", "Warwick · Cranston · Coventry",
     ["River flooding history", "Tree fall", "Nor’easter wind", "Ice dams"],
     "Postwar neighborhoods, bay shoreline and the Pawtuxet River. The March 2010 floods still shape how owners here think about water, and wooded streets mean trees on houses after big storms.",
     "Warwick, Cranston, West Warwick, Coventry, East Greenwich, West Greenwich", "warwick-shore"),
    ("eastbay", "East Bay", "East Providence · Barrington · Bristol",
     ["Bay surge history", "Coastal wind", "Historic homes", "Tree fall"],
     "Low-lying peninsulas and long bay frontage. Hurricanes in 1938 and 1954 flooded these towns, and historic downtowns in Bristol and Warren add material-matching questions.",
     "East Providence, Barrington, Warren, Bristol", "bristol-harbor"),
    ("newport", "Newport County", "Newport · Middletown · Portsmouth",
     ["Hurricane wind", "Salt spray", "Historic materials", "High-value homes"],
     "Aquidneck Island and the eastern shore face the Atlantic. Colonial and Gilded Age buildings, estate homes and shoreline exposure make claims here detailed and expensive.",
     "Newport, Middletown, Portsmouth, Jamestown, Tiverton, Little Compton", "newport-harbor"),
    ("south", "South County & Block Island", "Westerly · Narragansett · North Kingstown",
     ["Hurricane deductibles", "Wind vs. flood", "Seasonal homes", "Dunes & sand"],
     "Barrier beaches, salt ponds and summer communities. The 1938 hurricane, Sandy in 2012 and Henri in 2021 all struck this coast. Hurricane deductibles and wind-versus-flood questions come up on almost every claim.",
     "Westerly, Charlestown, South Kingstown, Narragansett, North Kingstown, New Shoreham (Block Island)", "westerly-beach"),
    ("hills", "Northwest Hills", "Glocester · Scituate · Burrillville",
     ["Snow load", "Ice storms", "Trees on structures", "Frozen pipes"],
     "Higher ground, deep woods and the Scituate Reservoir. More snow than the coast, long outages after storms, and rural properties with barns, wells and long driveways.",
     "Burrillville, Glocester, Foster, Scituate, Smithfield, North Smithfield", "snow-roof"),
]
