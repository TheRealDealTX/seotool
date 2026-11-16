"""Connecticut town and city pages. Each carries its own local detail."""

LOCATIONS = [
    {
        "slug": "hartford", "city": "Hartford", "county": "Hartford County", "region": "Capitol Region",
        "title": "Insurance Appraiser in Hartford, CT | Claim Appraisal",
        "desc": "Insurance appraiser in Hartford, CT for underpaid storm, tree, ice dam and fire claims on three-families, Victorians and downtown buildings.",
        "lede": "The state capital and long-time insurance hub has some of Connecticut’s oldest and most varied housing, from Asylum Hill Victorians to rows of three-family houses in Frog Hollow and the South End.",
        "neighborhoods": "West End, Asylum Hill, Frog Hollow, South End, Blue Hills, Parkville, Sheldon-Charter Oak",
        "housing": "Two- and three-family houses, Victorian and Queen Anne homes, brick apartment blocks and downtown office towers",
        "perils": ["Tree falls", "Ice dams", "Frozen pipes", "Thunderstorm wind", "Fire"],
        "body": """
<h2>Claims we see in Hartford</h2>
<p>Hartford’s housing is dense and old. Many homes in the West End and Asylum Hill have slate roofs, plaster walls and ornate millwork that standard estimates don’t price correctly. In Frog Hollow, Parkville and the South End, the classic three-family house means a single roof leak can damage three apartments and a shared stairwell, each with its own finishes and tenants.</p>
<h2>Storm history</h2>
<p>The October 2011 nor’easter dropped heavy wet snow on fully leafed trees, bringing down limbs across Hartford’s tree-lined streets. The October 1979 tornado passed just north of the city through Windsor and Windsor Locks. Winters regularly bring ice dams and frozen pipes, especially in older buildings with limited attic insulation.</p>
<h2>Commercial property</h2>
<p>Downtown and the Asylum Avenue corridor include office towers, churches and mixed-use buildings with large low-slope roofs. Commercial claims here often hinge on membrane repairability and code-driven insulation upgrades.</p>
""",
        "faqs": [
            ("Do you handle three-family houses in Hartford?", "Yes. We scope each unit and the common areas separately, and we can coordinate access with tenants."),
            ("Can you price a slate roof in the West End?", "Yes. Slate repair and replacement require specialized labor and materials, and we price them accordingly rather than as asphalt."),
        ],
        "near": ["west-hartford", "torrington", "new-haven"],
    },
    {
        "slug": "new-haven", "city": "New Haven", "county": "New Haven County", "region": "South Central Shoreline",
        "title": "Insurance Appraiser in New Haven, CT | Claim Appraisal",
        "desc": "Insurance appraiser in New Haven, CT for disputed wind, tree, water and fire claims, from East Rock and Westville to Morris Cove and the Annex.",
        "lede": "New Haven combines a working harbor, a university city and historic neighborhoods, and its claims range from shoreline wind in Morris Cove to century-old plaster in East Rock.",
        "neighborhoods": "East Rock, Westville, Wooster Square, Fair Haven, Morris Cove, the Annex, Prospect Hill",
        "housing": "Historic single-family homes, two- and three-family houses, brick rowhouses, condos and institutional buildings",
        "perils": ["Tornado & microburst", "Coastal wind", "Tree falls", "Water damage", "Fire"],
        "body": """
<h2>Claims we see in New Haven</h2>
<p>East Rock and Prospect Hill have large late-Victorian and Colonial Revival houses with slate roofs and detailed interiors. Fair Haven and the Hill have many multifamily homes. Along the East Shore, Morris Cove and the Annex are exposed to wind off Long Island Sound.</p>
<h2>Storm history</h2>
<p>On July 10, 1989, a powerful tornado tracked through Hamden and into parts of New Haven, damaging homes and uprooting trees. Another round of tornadoes and a macroburst on May 15, 2018 struck Hamden and surrounding towns. Tropical Storm Irene and Superstorm Sandy brought wind and shoreline flooding to the East Shore in 2011 and 2012.</p>
<h2>Wind versus water on the East Shore</h2>
<p>For homes near the water, the line between wind damage under a homeowners policy and flood damage under a flood policy matters. We document each separately.</p>
""",
        "faqs": [
            ("Do you work in Hamden and East Haven too?", "Yes. We cover the entire New Haven area and every Connecticut town."),
            ("Can appraisal help with a condo in downtown New Haven?", "Yes, once responsibility between your unit policy and the association’s master policy is sorted out."),
        ],
        "near": ["milford", "waterbury", "hartford"],
    },
    {
        "slug": "stamford", "city": "Stamford", "county": "Fairfield County", "region": "Gold Coast",
        "title": "Insurance Appraiser in Stamford, CT | Claim Appraisal",
        "desc": "Insurance appraiser in Stamford, CT for high-value homes, Shippan waterfront houses, downtown condos and office buildings with disputed claims.",
        "lede": "Stamford mixes downtown high-rises, waterfront homes on Shippan Point and wooded estates in North Stamford, so one storm can produce very different claims across the city.",
        "neighborhoods": "Shippan, the Cove, Downtown, Harbor Point, Glenbrook, Springdale, North Stamford",
        "housing": "High-value single-family homes, waterfront houses, high-rise condos and apartments, and Class A office space",
        "perils": ["Hurricane & surge", "Tree falls", "Wind-driven rain", "Water damage", "Commercial roofs"],
        "body": """
<h2>Claims we see in Stamford</h2>
<p>Shippan Point and the Cove sit right on Long Island Sound, where tropical storms bring wind-driven rain and surge. North Stamford is heavily wooded, and tree impacts are common after nor’easters and tropical storms. Downtown and Harbor Point have many newer high-rise condos and offices, where water damage between units and large commercial roofs drive claims.</p>
<h2>Storm history</h2>
<p>The Stamford Hurricane Barrier, completed in the late 1960s, protects much of the downtown harbor area, but neighborhoods outside it took heavy damage during Sandy in 2012. Tropical Storm Isaias in 2020 brought down trees and power lines throughout the city.</p>
<h2>High-value homes</h2>
<p>Custom finishes, imported materials and specialty systems are easy to underprice with standard line items. We document and price the quality of what was actually installed.</p>
""",
        "faqs": [
            ("Do you handle high-value homes?", "Yes. High-value homes need detailed documentation of materials and craftsmanship, and that’s how we approach them."),
            ("Can you help with a condo water leak between units?", "Yes, after we sort out which policy covers which items under your association’s documents."),
        ],
        "near": ["greenwich", "norwalk", "danbury"],
    },
    {
        "slug": "bridgeport", "city": "Bridgeport", "county": "Fairfield County", "region": "Greater Bridgeport",
        "title": "Insurance Appraiser in Bridgeport, CT | Claim Appraisal",
        "desc": "Insurance appraiser in Bridgeport, CT for multifamily, shoreline and commercial claims in Black Rock, the North End, the East Side and beyond.",
        "lede": "Connecticut’s largest city has a long industrial waterfront, dense multifamily neighborhoods and shoreline homes in Black Rock, which gives it a wide mix of property claims.",
        "neighborhoods": "Black Rock, North End, East Side, East End, West End, Brooklawn, Downtown",
        "housing": "Two- and three-family houses, shoreline single-family homes, brick industrial and commercial buildings",
        "perils": ["Coastal wind", "Storm surge", "Frozen pipes", "Fire", "Commercial roofs"],
        "body": """
<h2>Claims we see in Bridgeport</h2>
<p>Bridgeport has one of the largest concentrations of multifamily housing in the state. Water damage that starts in one unit often affects the units below, and fires in multifamily buildings involve several households and policies. Black Rock and the South End sit on the water and take the brunt of coastal storms.</p>
<h2>Storm history</h2>
<p>Superstorm Sandy in 2012 flooded parts of Black Rock, the South End and the East End. Tropical Storm Irene the year before brought damaging winds. Older brick commercial buildings near the harbor are also exposed to wind and water from strong nor’easters.</p>
<h2>Landlords and investors</h2>
<p>Many Bridgeport owners hold rental property under dwelling-fire or commercial policies, which differ from standard homeowners forms in how they value losses and cover lost rent. We read the form before we value the loss.</p>
""",
        "faqs": [
            ("Do you work with landlords?", "Yes. We value rental property claims, including lost rent where the policy provides it and it is part of the dispute."),
            ("Can appraisal address flood damage?", "Appraisal under a homeowners policy values covered damage, usually wind. Flood damage is handled under a separate flood policy."),
        ],
        "near": ["milford", "norwalk", "stamford"],
    },
    {
        "slug": "waterbury", "city": "Waterbury", "county": "New Haven County", "region": "Naugatuck Valley",
        "title": "Insurance Appraiser in Waterbury, CT | Claim Appraisal",
        "desc": "Insurance appraiser in Waterbury, CT for disputed claims on three-deckers, hillside homes and brick mill buildings across the Naugatuck Valley.",
        "lede": "The Brass City sits in the Naugatuck River Valley among steep hills, with three-decker neighborhoods, older single-family homes and brick mill and factory buildings.",
        "neighborhoods": "Bunker Hill, Town Plot, Overlook, East End, Brooklyn, Hillside, Downtown",
        "housing": "Three-family homes, older single-family houses, brick mills, churches and small commercial buildings",
        "perils": ["Ice dams", "Frozen pipes", "Tree falls", "Wind", "Fire"],
        "body": """
<h2>Claims we see in Waterbury</h2>
<p>Waterbury’s hills make its winters harsher than the shoreline’s, and ice dams and frozen pipes drive many claims. Three-deckers in Brooklyn, the North End and the East End have flat or low-slope roofs where snow and ice linger. Older mill buildings carry large, aging roofs and complex construction.</p>
<h2>Storm history</h2>
<p>The August 1955 floods, caused by the remnants of Hurricanes Connie and Diane, devastated the Naugatuck Valley and remain the region’s defining disaster. More recently, nor’easters and summer thunderstorms have downed trees across hillside neighborhoods.</p>
<h2>Old mills and commercial buildings</h2>
<p>Converted factories have layered construction, heavy timber framing and older roofs. Valuing a loss in these buildings requires understanding how they were built and what code requires when they are repaired.</p>
""",
        "faqs": [
            ("Do you cover the rest of the Naugatuck Valley?", "Yes, including Naugatuck, Seymour, Ansonia, Derby and the surrounding towns."),
            ("Are flat-roof three-deckers harder to appraise?", "Not harder, but different. Low-slope roof systems are priced differently from shingles, and we scope them that way."),
        ],
        "near": ["torrington", "new-haven", "danbury"],
    },
    {
        "slug": "norwalk", "city": "Norwalk", "county": "Fairfield County", "region": "Gold Coast",
        "title": "Insurance Appraiser in Norwalk, CT | Claim Appraisal",
        "desc": "Insurance appraiser in Norwalk, CT for coastal wind, tree and water claims in Rowayton, East Norwalk, SoNo, Silvermine and Cranbury homes.",
        "lede": "Norwalk runs from the Norwalk Islands and Rowayton’s waterfront up to wooded Silvermine and Cranbury, with SoNo’s converted industrial buildings in between.",
        "neighborhoods": "Rowayton, East Norwalk, SoNo, Silvermine, Cranbury, West Norwalk, Spring Hill",
        "housing": "Waterfront homes, colonials and capes, condos, and converted mill and industrial buildings",
        "perils": ["Hurricane & surge", "Tree falls", "Wind", "Water damage", "Ice dams"],
        "body": """
<h2>Claims we see in Norwalk</h2>
<p>Rowayton and East Norwalk face Long Island Sound and the Norwalk River, where tropical storms bring wind and flooding. Silvermine and Cranbury are heavily wooded, so tree damage is common. SoNo’s older brick buildings, many converted to condos and offices, have their own roofing and water damage challenges.</p>
<h2>Storm history</h2>
<p>Superstorm Sandy flooded parts of East Norwalk and Rowayton in 2012, and Tropical Storm Isaias in 2020 downed trees across the city. Heavy rain from the remnants of Ida in 2021 caused flooding along the Norwalk River.</p>
<h2>Condos and converted buildings</h2>
<p>Condo owners in SoNo and along Route 1 face questions about who covers what between the unit and the association. We start there before valuing anything.</p>
""",
        "faqs": [
            ("Do you cover Rowayton?", "Yes. Rowayton is part of Norwalk, and we work throughout the city."),
            ("Can you help after a tree falls on my house?", "Yes. Tree claims are among the most common we value in Fairfield County."),
        ],
        "near": ["stamford", "bridgeport", "danbury"],
    },
    {
        "slug": "danbury", "city": "Danbury", "county": "Fairfield County", "region": "Housatonic Valley",
        "title": "Insurance Appraiser in Danbury, CT | Claim Appraisal",
        "desc": "Insurance appraiser in Danbury, CT for hail, wind, tree and winter claims on lake homes, Victorians and subdivisions near Candlewood Lake.",
        "lede": "Danbury sits inland near Candlewood Lake, where hail and thunderstorms are more frequent than on the coast, and its housing ranges from Victorian city homes to newer subdivisions.",
        "neighborhoods": "Great Plain, Mill Plain, Pembroke, King Street, Downtown, Candlewood Lake shore, Germantown",
        "housing": "Victorian and foursquare homes, lake houses, newer subdivisions, condos and retail centers",
        "perils": ["Hail", "Thunderstorm wind", "Tree falls", "Ice dams", "Frozen pipes"],
        "body": """
<h2>Claims we see in Danbury</h2>
<p>Inland western Connecticut gets more hail than the shoreline, and Danbury’s roofs show it after strong summer storms. Downtown and Osborne Street have Victorian and foursquare homes with older roofs, while Great Plain, King Street and the lake shore have a mix of older homes and newer construction.</p>
<h2>Storm history</h2>
<p>Summer thunderstorms with hail and damaging winds affect the Danbury area regularly. Winter storms bring heavy snow and ice, and the October 2011 nor’easter brought down trees throughout the region.</p>
<h2>Lake homes</h2>
<p>Houses around Candlewood Lake can include docks, boathouses and seasonal use. Vacancy, heat and other-structures provisions in the policy can affect a claim.</p>
""",
        "faqs": [
            ("Is hail common in Danbury?", "More common than on the coast. Hail swaths are narrow, so documentation from your own property is important."),
            ("Do you cover Bethel, Brookfield and New Fairfield?", "Yes, along with every other Connecticut town."),
        ],
        "near": ["norwalk", "waterbury", "torrington"],
    },
    {
        "slug": "new-london", "city": "New London", "county": "New London County", "region": "Southeastern Connecticut",
        "title": "Insurance Appraiser in New London, CT | Claim Appraisal",
        "desc": "Insurance appraiser in New London, CT for hurricane, wind and water claims near Ocean Beach, Pequot Avenue and the Thames, plus Groton homes.",
        "lede": "At the mouth of the Thames River, New London has felt every major hurricane to strike the state, from 1938 to Sandy. Its housing ranges from whaling-era homes to shoreline cottages.",
        "neighborhoods": "Ocean Beach, Pequot Avenue, Downtown, Whale Oil Row, Hodges Square, Montauk Avenue",
        "housing": "Historic downtown buildings, shoreline cottages, colonials, multifamily homes and waterfront commercial property",
        "perils": ["Hurricane & surge", "Coastal wind", "Tree falls", "Water damage", "Fire"],
        "body": """
<h2>Claims we see in New London</h2>
<p>Pequot Avenue and Ocean Beach sit directly on the water, where hurricanes and nor’easters bring wind and surge. Downtown has historic commercial buildings and older homes with complex roofs. Across the river, Groton has a mix of shoreline homes and neighborhoods near the submarine base.</p>
<h2>Storm history</h2>
<p>The 1938 hurricane brought fire and flooding to downtown New London. Hurricane Carol in 1954 and Gloria in 1985 also hit hard. Irene, Sandy and Isaias each caused shoreline wind damage and power outages in the region.</p>
<h2>Historic buildings</h2>
<p>Many downtown buildings date to the 1800s. Repairs may involve historic materials, and some properties are in historic districts with their own review requirements.</p>
""",
        "faqs": [
            ("Do you cover Groton, Waterford and Stonington?", "Yes. We cover all of southeastern Connecticut and every other town in the state."),
            ("Does my policy have a hurricane deductible?", "Many shoreline policies do. Check your declarations page, and use our hurricane deductible calculator to see it in dollars."),
        ],
        "near": ["milford", "new-haven", "hartford"],
    },
    {
        "slug": "greenwich", "city": "Greenwich", "county": "Fairfield County", "region": "Gold Coast",
        "title": "Insurance Appraiser in Greenwich, CT | Claim Appraisal",
        "desc": "Insurance appraiser in Greenwich, CT for high-value homes, estates and waterfront property in Old Greenwich, Riverside, Cos Cob and Byram.",
        "lede": "Greenwich has some of the highest-value homes in the country, from waterfront properties in Old Greenwich and Riverside to backcountry estates on large wooded lots.",
        "neighborhoods": "Old Greenwich, Riverside, Cos Cob, Byram, Glenville, Central Greenwich, Backcountry",
        "housing": "Estates, waterfront homes, historic houses, custom new construction and Greenwich Avenue commercial buildings",
        "perils": ["Tree falls", "Hurricane & surge", "Water damage", "Ice dams", "Fire"],
        "body": """
<h2>Claims we see in Greenwich</h2>
<p>Large homes with custom finishes, slate and cedar roofs, specialty windows and complex mechanical systems are expensive to repair and easy to underprice. The backcountry is heavily wooded, and tree falls are common. Old Greenwich, Riverside and Byram are exposed to coastal storms.</p>
<h2>Storm history</h2>
<p>Superstorm Sandy flooded parts of Old Greenwich, Byram and the waterfront in 2012. Tropical Storm Isaias in 2020 caused widespread tree damage and long power outages across the town.</p>
<h2>High-value policies</h2>
<p>High-value homeowners policies often include broader coverage, guaranteed replacement cost or cash settlement options. Those features change how a loss is valued, so we read the policy before we start.</p>
""",
        "faqs": [
            ("Do you work with high-value insurers?", "Yes. We work on claims with every type of carrier, including high-value specialty insurers."),
            ("Can you value custom finishes and imported materials?", "Yes. We document what was installed and price it with specialist quotes where needed."),
        ],
        "near": ["stamford", "norwalk", "danbury"],
    },
    {
        "slug": "west-hartford", "city": "West Hartford", "county": "Hartford County", "region": "Capitol Region",
        "title": "Insurance Appraiser in West Hartford, CT | Claims",
        "desc": "Insurance appraiser in West Hartford, CT for tree, ice dam, wind and water claims on colonials and Tudors in Elmwood, Westmoor and Blue Back.",
        "lede": "West Hartford’s tree-lined streets of colonials, Tudors and capes are beautiful until a storm brings the canopy down. Its housing stock is older, detailed and costly to match.",
        "neighborhoods": "West Hartford Center, Blue Back Square, Elmwood, Bishop’s Corner, Westmoor, Sunset Farm, Buena Vista",
        "housing": "Colonials, Tudors, capes, two-family “perfect sixes,” condos and Center retail buildings",
        "perils": ["Tree falls", "Ice dams", "Frozen pipes", "Wind", "Water damage"],
        "body": """
<h2>Claims we see in West Hartford</h2>
<p>Many West Hartford homes date from the 1920s through the 1950s, with plaster walls, hardwood floors that run through several rooms, slate or older asphalt roofs and detailed trim. Matching those materials is often the core of the dispute. Two-family houses near the Hartford line add multi-unit complexity.</p>
<h2>Storm history</h2>
<p>The October 2011 nor’easter brought down huge numbers of trees in West Hartford, and Tropical Storm Isaias did the same in 2020. Winter ice dams are common on older homes with limited attic insulation.</p>
<h2>Matching and continuity</h2>
<p>When a tree damages one part of a roof or a leak ruins one room of hardwood, the question is how far repairs must extend to look uniform. We document products, profiles and availability so the panel can decide on facts.</p>
""",
        "faqs": [
            ("Do you handle hardwood floor matching disputes?", "Yes. We document species, width, finish and continuity to support the scope needed for a uniform result."),
            ("Do you cover Farmington, Avon and Simsbury?", "Yes, along with every other town in the state."),
        ],
        "near": ["hartford", "torrington", "waterbury"],
    },
    {
        "slug": "milford", "city": "Milford", "county": "New Haven County", "region": "South Central Shoreline",
        "title": "Insurance Appraiser in Milford, CT | Claim Appraisal",
        "desc": "Insurance appraiser in Milford, CT for shoreline wind, surge-area and tree claims in Woodmont, Walnut Beach, Devon, Laurel Beach and Bayview.",
        "lede": "Milford has about seventeen miles of shoreline, more than most Connecticut towns, and its beach neighborhoods took some of the state’s heaviest damage from Irene and Sandy.",
        "neighborhoods": "Woodmont, Walnut Beach, Devon, Laurel Beach, Bayview, Fort Trumbull, Milford Center",
        "housing": "Beach cottages, elevated and rebuilt shoreline homes, capes and colonials, condos and Route 1 retail",
        "perils": ["Hurricane & surge", "Coastal wind", "Tree falls", "Water damage", "Ice dams"],
        "body": """
<h2>Claims we see in Milford</h2>
<p>Many beach houses in Woodmont, Walnut Beach, Laurel Beach and Bayview began as summer cottages and have been expanded, winterized or elevated over time. That history matters when valuing a loss. Inland neighborhoods such as Devon and the area around Milford Center see more tree and winter claims.</p>
<h2>Storm history</h2>
<p>Tropical Storm Irene in 2011 and Superstorm Sandy in 2012 caused severe damage along Milford’s shoreline, destroying and damaging many homes. Strong nor’easters continue to bring wind and coastal flooding.</p>
<h2>Elevated and rebuilt homes</h2>
<p>Homes rebuilt or elevated after Sandy were constructed to newer codes. Valuing damage to them requires pricing current materials and methods, not the original cottage.</p>
""",
        "faqs": [
            ("Do you help with shoreline wind claims?", "Yes. We document wind damage separately from flood damage so each policy is asked to pay the right part."),
            ("Do you cover Stratford, West Haven and Orange?", "Yes, along with every Connecticut town."),
        ],
        "near": ["new-haven", "bridgeport", "new-london"],
    },
    {
        "slug": "torrington", "city": "Torrington", "county": "Litchfield County", "region": "Litchfield Hills",
        "title": "Insurance Appraiser in Torrington, CT | Claim Appraisal",
        "desc": "Insurance appraiser in Torrington, CT and the Litchfield Hills for snow-load, ice dam, tree, frozen pipe and fire claims on homes and barns.",
        "lede": "Torrington is the largest city in Litchfield County, where higher elevation means colder winters, heavier snow and more ice than the rest of the state.",
        "neighborhoods": "Downtown, Torringford, Drakeville, Newfield, Burrville, and nearby Litchfield, Goshen and Harwinton",
        "housing": "Older city homes and multifamily houses, farmhouses, barns, seasonal and second homes",
        "perils": ["Snow load", "Ice dams", "Frozen pipes", "Tree falls", "Fire"],
        "body": """
<h2>Claims we see in Torrington and the Litchfield Hills</h2>
<p>The Litchfield Hills get more snow and colder temperatures than shoreline Connecticut. Ice dams, frozen pipes and snow-load damage are common, especially on older homes and barns. Second homes and seasonal properties raise questions about heat, vacancy and maintenance under the policy.</p>
<h2>Storm history</h2>
<p>The August 1955 flood devastated downtown Torrington along the Naugatuck River. The October 2011 nor’easter dropped heavy snow on the region while trees still had leaves, and winters such as 2011 brought widespread roof collapses on barns and outbuildings.</p>
<h2>Farm buildings and outbuildings</h2>
<p>Barns, garages and sheds are often covered under other-structures coverage or a farm policy, each with its own limits. We make sure they are not lost in a larger claim.</p>
""",
        "faqs": [
            ("Do you cover the rest of Litchfield County?", "Yes, including Litchfield, New Milford, Winsted, Canaan and every other town."),
            ("Is a barn collapse from snow covered?", "It depends on the policy that covers the barn and its collapse provisions. We read the form before valuing the loss."),
        ],
        "near": ["waterbury", "danbury", "west-hartford"],
    },
]
