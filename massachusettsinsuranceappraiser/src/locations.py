"""City and town pages for Massachusetts Insurance Appraiser.

Each entry describes one community: its county and region, the perils that
drive local property claims, the housing stock, a notable storm, and an HTML
body written for that place. Bodies use only h2/h3 headings and link only to
pages that exist on the site.
"""

LOCATIONS = [
    {
        "slug": "boston", "city": "Boston", "county": "Suffolk County", "region": "Greater Boston",
        "perils": ["Nor’easters", "Coastal flooding", "Ice dams", "Burst pipes", "Fire in attached housing"],
        "near": ["cambridge", "quincy", "salem"],
        "housing": "Triple-deckers, brownstones, row houses and condo buildings",
        "storm": "January 2018 nor’easter harbor flooding",
        "lede": "Boston claims often involve shared walls, condo master policies and buildings older than the policy forms that cover them. We help owners in every neighborhood get an independent number when the carrier’s estimate falls short.",
        "title": "Insurance Appraiser in Boston, MA | Claim Disputes",
        "desc": "Disputed property claim in Boston? Independent appraisal for triple-deckers, brownstones and condos, from Dorchester to Charlestown.",
        "body": """
<h2>Old buildings, tight lots and shared walls</h2>
<p>Much of Boston’s housing was built before modern codes, and that shapes almost every claim in Suffolk County. In Dorchester and parts of Jamaica Plain, wood-frame triple-deckers stack three households under one roof, so a single burst pipe or kitchen fire can touch three units, two policies and a condo association at once. Back Bay and the South End add brick and brownstone row houses with slate or copper details, ornate plaster and narrow access that drives up labor and staging costs. Charlestown and South Boston have dense blocks of attached row houses where a fire or water loss next door becomes your loss too.</p>
<p>When an estimate prices plaster as drywall, ignores the cost of working on a one-way street with no driveway, or leaves out code upgrades the city requires once walls are opened, the gap between the carrier’s figure and a real contractor bid can be wide. Our <a href="/what-we-appraise/claim-estimate-review/">claim estimate review</a> compares the two line by line before anyone invokes appraisal.</p>

<h2>The harbor, the snow and the wind</h2>
<p>East Boston, the Seaport, the waterfront near Long Wharf and low-lying parts of Dorchester sit close to sea level. The January 2018 nor’easter pushed harbor water into streets around the waterfront, and the March 2018 storms that followed added more coastal flooding around the region. Those events are a reminder that flood and wind are covered differently: standard homeowner policies exclude flood, so many disputes turn on what the wind did versus what the water did.</p>
<p>Winter brings its own pattern. Boston received roughly 110 inches of snow in the winter of 2015, and ice dams and roof leaks followed across West Roxbury, Roslindale and Hyde Park. Interior damage from an ice dam is often covered while the dam itself is treated as maintenance, which is why our <a href="/what-we-appraise/ice-dam-snow-load-appraisal/">ice dam and snow load appraisal</a> work focuses on documenting the full interior scope.</p>
<div class="note"><b class="h">Condo owners: two policies, one loss</b>Many Boston units sit in buildings with an association master policy. Your HO-6 may only respond to what the master policy does not. Our guide to <a href="/claim-library/condo-master-policy-vs-ho6-claims/">condo master policy vs. HO-6 claims</a> explains how the pieces usually fit.</div>

<h2>Common Boston claim disagreements</h2>
<ul>
<li>Triple-decker losses where the scope stops at one unit even though damage runs through shared framing.</li>
<li>Historic or architectural trim priced as stock material.</li>
<li>Wind-versus-flood arguments after coastal storms in East Boston or the Seaport.</li>
<li>Ice dam claims that cover the ceiling stain but not insulation, framing or electrical repairs.</li>
<li>Smoke damage in attached homes that the estimate limits to the unit where the fire started.</li>
</ul>
<p>If your carrier’s number does not match the repair, appraisal under your policy may let a neutral process set the amount of loss. Start with our <a href="/appraisal-roadmap/">appraisal roadmap</a> to see how the steps usually unfold.</p>
""",
        "faqs": [
            ("Does appraisal work for a Boston triple-decker owned as three condos?", "It can. Each unit owner and the association may each have a policy, and appraisal generally sets the amount of loss under the policy that invokes it. Sorting out which policy covers which part of the building usually comes first."),
            ("My basement in East Boston flooded during a nor’easter. Will my homeowners policy pay?", "Standard homeowner policies exclude flood from surface water and storm surge, so that part typically falls to an NFIP or private flood policy. Wind or roof damage from the same storm may still be covered under your homeowners policy. Check your policy wording."),
            ("Can appraisal decide whether my Boston claim was handled unfairly?", "No. Appraisal is about the dollar amount of loss. Questions about claim handling or consumer-protection laws are legal matters; consult a Massachusetts attorney."),
        ],
    },
    {
        "slug": "worcester", "city": "Worcester", "county": "Worcester County", "region": "Central Massachusetts",
        "perils": ["Ice storms", "Heavy snow load", "Tree fall", "Summer hail", "Tornadoes"],
        "near": ["lowell", "boston", "springfield"],
        "housing": "Triple-deckers, hillside Colonials and post-war Capes",
        "storm": "June 9, 1953 F4 tornado",
        "lede": "Worcester’s hills, mature trees and deep stock of triple-deckers give claims here a character of their own. We provide independent appraisal and estimate review across the city and Worcester County.",
        "title": "Worcester, MA Insurance Appraiser | Storm & Roof Claims",
        "desc": "Independent insurance appraisal in Worcester, MA for ice storm, tree, snow load and roof claims on triple-deckers and hillside homes.",
        "body": """
<h2>A city of hills and triple-deckers</h2>
<p>Worcester is known as a city built on seven hills, and its housing follows the terrain. Main South, Vernon Hill and Grafton Hill hold some of the largest concentrations of triple-deckers in New England, many with original porches stacked three high, clapboard or asbestos siding layered under vinyl, and flat or low-slope roofs. Farther west, Tatnuck and the West Side have larger Colonials and Tudors on wooded lots, while Greendale and Burncoat lean toward Capes and ranches built after the war.</p>
<p>That variety matters when an estimate is written from a template. Stacked porches need staging and structural work, not just new decking. Low-slope triple-decker roofs are built differently from a pitched Cape roof. A carrier’s scope that treats every Worcester house the same is a common source of disagreement.</p>

<h2>Storm history in Worcester County</h2>
<p>The June 9, 1953 tornado is part of the city’s memory. Rated F4, it is counted among the deadliest tornadoes in U.S. history and tore through neighborhoods in the northern part of the city, including the Great Brook Valley area. Tornadoes remain uncommon here, but summer thunderstorms with hail and straight-line wind do reach Central Massachusetts more often than the coast.</p>
<p>The December 2008 ice storm is the more recent benchmark. Ice brought down limbs and whole trees across Worcester County and left many households without power for days. Old maples and oaks over narrow lots still create the same risk every winter, and tree claims often come with fence, gutter, siding and roof damage bundled together. Heavy snow on low-slope roofs adds snow load and ice dam claims in hard winters.</p>
<div class="note"><b class="h">Hail on a Worcester roof</b>Hail claims frequently turn on whether bruised shingles are “functional” damage. A roof measurement and pitch check helps keep the quantity honest; try our <a href="/estimators/roof-area-pitch-converter/">roof area and pitch converter</a> before you compare estimates.</div>

<h2>Disputes that come up often</h2>
<ul>
<li>Tree-fall claims where removal, debris and roof repair are capped or split oddly.</li>
<li>Frozen pipe losses in vacant or partly occupied triple-decker units.</li>
<li>Hail damage written as cosmetic on older asphalt or slate roofs.</li>
<li>Siding repairs that ignore matching problems on multi-layer walls.</li>
<li>Porch and stair repairs priced without staging or code work.</li>
</ul>

<h2>How we help</h2>
<p>We start with the policy and the carrier’s estimate, then price the job the way a Worcester contractor would actually build it. If appraisal makes sense, we can act as your appraiser through our <a href="/what-we-appraise/roof-hail-damage-appraisal/">roof and hail damage appraisal</a> service or broader <a href="/what-we-appraise/insurance-appraisal-representation/">appraisal representation</a>. We never promise a result; we work to document the full scope so the number reflects the real repair.</p>
""",
        "faqs": [
            ("Is a triple-decker in Worcester rated as a home or a commercial building?", "It depends on the policy and how the building is occupied. Owner-occupied triple-deckers are often written on homeowner forms, while fully rented buildings may be on a dwelling or commercial policy. The form affects how appraisal and coverage work."),
            ("A neighbor’s tree fell on my house during an ice storm. Whose policy pays?", "In many cases your own homeowners policy responds to damage to your house, regardless of whose tree it was. Tree removal coverage often has its own limits. Check your policy and talk to your agent."),
            ("Does hail really hit Worcester?", "Yes. Central Massachusetts gets summer thunderstorms with hail more often than the coast. Damage can be subtle on older roofs, so a careful inspection matters."),
        ],
    },
    {
        "slug": "springfield", "city": "Springfield", "county": "Hampden County", "region": "Pioneer Valley & the Berkshires",
        "perils": ["Tornadoes", "Wind and tree fall", "Early snowstorms", "Summer hail", "River flooding"],
        "near": ["pittsfield", "worcester", "boston"],
        "housing": "Victorians, brick multi-families and mid-century ranches",
        "storm": "June 1, 2011 EF3 tornado",
        "lede": "Springfield knows what a tornado can do to a city block. We give owners in Hampden County an independent view of their loss when wind, tree and storm claims stall.",
        "title": "Insurance Appraiser in Springfield, MA | Wind & Hail",
        "desc": "Wind, tornado, tree or hail claim in Springfield, MA? Independent appraisal and estimate review for owners from Forest Park to Sixteen Acres.",
        "body": """
<h2>The 2011 tornado and its lessons</h2>
<p>On June 1, 2011, an EF3 tornado tracked from Westfield across the Connecticut River and into Springfield, then continued east through Wilbraham, Monson and Brimfield. In the city it damaged downtown, the South End, Forest Park, East Forest Park and Sixteen Acres, tearing roofs off brick apartment blocks, toppling old trees and leaving many homes partly standing but badly racked.</p>
<p>Claims after events like that show how hard it is to value partial damage. A house that looks repairable from the street can have shifted framing, broken rafters or a foundation crack that only shows up once work starts. Estimates written quickly after a disaster often miss that hidden damage, and supplements become a long negotiation. Our <a href="/what-we-appraise/wind-tornado-claim-appraisal/">wind and tornado claim appraisal</a> service is built around that kind of loss.</p>

<h2>Housing across Springfield</h2>
<p>Springfield’s housing stock is old and varied. Forest Park and the McKnight district have large Victorians and Queen Annes with slate roofs, wraparound porches and detailed trim. The South End and neighborhoods near downtown include brick multi-family buildings and row houses. Sixteen Acres and East Forest Park lean toward Capes, splits and ranches on bigger lots with mature trees. Each of those requires a different approach to pricing, and template estimates often miss slate, copper flashing, or the labor of matching period details.</p>
<div class="note"><b class="h">Slate and older roofs</b>Slate is often repairable, but only by trades who know it. When an estimate swaps slate for asphalt or limits repairs to a few tiles on a brittle roof, the scope deserves a closer look.</div>

<h2>Other Pioneer Valley storms</h2>
<p>The same year as the tornado, an unusual late-October 2011 snowstorm fell on trees still in leaf, bringing down limbs across the region and causing long outages. The valley also gets summer thunderstorms with hail and damaging wind, and the Connecticut and Mill rivers can flood low areas in heavy rain. Flood from rising water is excluded under standard homeowner policies, but wind, hail and tree damage from the same storm may still be covered.</p>

<h2>Common Springfield claim issues</h2>
<ul>
<li>Racked framing and hidden structural damage left out of the first estimate.</li>
<li>Tree removal limits applied to large trees that came down on the house.</li>
<li>Slate and historic trim priced as modern materials.</li>
<li>Code upgrades required by the city but excluded from the scope.</li>
<li>Hail claims denied as old or cosmetic.</li>
</ul>
<p>If the numbers are far apart, the <a href="/estimators/appraisal-award-gap-estimator/">appraisal award gap estimator</a> can help you see whether the difference is worth pursuing through appraisal.</p>
""",
        "faqs": [
            ("My Springfield house was damaged by the 2011 tornado and I found more damage later. Can I still reopen it?", "Time limits in your policy and in Massachusetts law may apply, and many policies limit suits to about two years. Check your policy and talk to a Massachusetts attorney about your situation."),
            ("Does my homeowners policy cover flooding from the Connecticut River?", "Generally no. Flood from rising water is excluded and usually requires an NFIP or private flood policy. Wind and rain entering through a damaged roof are handled differently."),
            ("Can you help with a brick multi-family in the South End?", "Yes. We review residential and smaller commercial or multi-family claims, including masonry repairs and shared roofs."),
        ],
    },
    {
        "slug": "cambridge", "city": "Cambridge", "county": "Middlesex County", "region": "Greater Boston",
        "perils": ["Ice dams", "Heavy snow", "Burst pipes", "Tree fall", "Fire in wood-frame housing"],
        "near": ["boston", "quincy", "salem"],
        "housing": "Victorians, two-families, triple-deckers and condo conversions",
        "storm": "Winter 2015 record snowfall",
        "lede": "Cambridge has some of the densest wood-frame housing in the state, and much of it has been split into condos. We help owners and associations sort out disputed losses from Porter to Cambridgeport.",
        "title": "Cambridge, MA Insurance Appraiser | Condo & Home Claims",
        "desc": "Insurance appraisal in Cambridge, MA for ice dam, pipe burst and fire claims in Victorians, two-families and condo conversions near Harvard.",
        "body": """
<h2>Dense, old and mostly wood</h2>
<p>Cambridge packs a lot of housing into a small area. Around Harvard Square and Mid-Cambridge, large Victorians and mansard-roof homes sit on small lots. Cambridgeport and the area near Central Square have rows of two-families and triple-deckers. East Cambridge mixes older worker housing with newer condo buildings near Kendall. Porter Square and North Cambridge have more two-families, many of them converted into condominiums.</p>
<p>Wood-frame buildings this close together carry real fire exposure, and a fire or smoke loss next door can damage your home too. Many of these houses also have plaster walls, original trim and balloon framing, which change how a repair is priced. Our <a href="/what-we-appraise/fire-smoke-damage-appraisal/">fire and smoke damage appraisal</a> work focuses on getting those details into the scope.</p>

<h2>Winter is the big season</h2>
<p>In the winter of 2015, repeated storms buried Greater Boston, and Cambridge saw ice dams, roof leaks and interior water damage across older homes with little attic insulation. Ice dam claims are a familiar pattern: the policy may treat the dam as maintenance but cover the resulting interior damage, and the dispute is over how much of the ceiling, insulation, framing and paint actually has to be replaced.</p>
<p>Frozen and burst pipes are the other common winter loss, especially in older buildings where pipes run through exterior walls or unheated porches. Large old trees along Cambridge streets also bring limbs down during wind storms and heavy wet snow.</p>
<div class="note"><b class="h">Snow load on flat and low-slope roofs</b>Many Cambridge two-families and triple-deckers have low-slope roofs where snow and ice can build up. Our <a href="/estimators/roof-snow-load-estimator/">roof snow load estimator</a> gives a rough sense of the weight involved.</div>

<h2>Condo conversions and shared policies</h2>
<p>A Cambridge two-family split into two condos often has a small association with its own master policy, plus an HO-6 policy for each owner. Water from an upstairs unit, a roof leak, or a fire can involve all three. Who repairs what depends on the master deed and the policies. We help owners understand where the lines fall before valuing the loss; see our <a href="/what-we-appraise/condo-hoa-commercial-appraisal/">condo and HOA appraisal</a> page for more.</p>

<h2>Common Cambridge disputes</h2>
<ul>
<li>Ice dam interiors scoped as a patch-and-paint job.</li>
<li>Plaster and period trim priced as drywall and stock molding.</li>
<li>Unit-to-unit water losses with unclear master-policy and HO-6 responsibility.</li>
<li>Smoke damage in a neighboring unit downplayed or left out.</li>
<li>Small association policies with high deductibles and confusion over who pays.</li>
</ul>
""",
        "faqs": [
            ("Our two-unit condo in Cambridge has a small association. Does it need its own policy?", "Most associations carry a master policy for the building, and each owner carries an HO-6. The master deed and bylaws usually explain who insures what. Check your documents and ask your agent."),
            ("Is ice dam damage covered in Massachusetts?", "Policies often cover resulting interior water damage from an ice dam but not the ice dam removal or maintenance itself. Wording varies, so check your policy."),
            ("Can appraisal help if my insurer and the association’s insurer disagree?", "Appraisal sets the amount of loss under the policy that invokes it. It does not decide which policy is responsible. Coverage disputes may need advice from a Massachusetts attorney."),
        ],
    },
    {
        "slug": "lowell", "city": "Lowell", "county": "Middlesex County", "region": "North Shore & Merrimack Valley",
        "perils": ["River flooding", "Ice dams", "Burst pipes", "Fire", "Wind and tree fall"],
        "near": ["cambridge", "boston", "salem"],
        "housing": "Mill-loft condos, triple-deckers and Victorian two-families",
        "storm": "Mother’s Day flood of May 2006",
        "lede": "Lowell’s converted mills, river setting and older neighborhoods create claims that need careful work. We provide independent appraisal for owners and associations across the city.",
        "title": "Insurance Appraiser in Lowell, MA | Mill Lofts & Homes",
        "desc": "Insurance appraisal in Lowell, MA for mill-loft condos, triple-deckers and older homes, with help on water, fire and storm claim disputes.",
        "body": """
<h2>From mills to lofts</h2>
<p>Lowell grew around textile mills powered by the Merrimack River and its canals, and many of those brick mill buildings downtown are now loft condos and apartments. These buildings bring their own claim issues: heavy timber framing, large windows, shared roofs and mechanical systems, and a condo association master policy that sits on top of each owner’s HO-6. A water loss on an upper floor of a mill building can run through several units and common areas before anyone finds the source.</p>
<p>Outside downtown, the Acre, Centralville, Pawtucketville, Belvidere and the Highlands are full of triple-deckers, two-families and Victorian homes. Belvidere has some of the city’s larger older homes, while the Acre and Centralville have dense multi-family blocks close together.</p>
<div class="note"><b class="h">Mill-loft condos</b>In a converted mill, the master deed often defines what the association insures and what belongs to each unit owner. Read it alongside our guide on <a href="/claim-library/condo-master-policy-vs-ho6-claims/">condo master policy vs. HO-6 claims</a> before you assume a loss is all yours or all theirs.</div>

<h2>The river and the weather</h2>
<p>The Merrimack and Concord rivers have flooded Lowell more than once. In May 2006, heavy rain brought serious flooding to the Merrimack Valley, and low-lying parts of the region took water. Flood from rising water is excluded under standard homeowner policies, so flood losses usually go through an NFIP or private flood policy, while wind and rain damage through a roof or window may be covered by the homeowners policy. When both happen in one storm, the split can be contested.</p>
<p>Winter brings ice dams, frozen pipes and snow load on older roofs. Many Lowell triple-deckers have low-slope roofs and stacked porches, both of which collect snow and ice. Our <a href="/what-we-appraise/water-damage-claim-appraisal/">water damage claim appraisal</a> service covers burst pipes, ice dam leaks and sudden plumbing failures.</p>

<h2>Common Lowell claim disputes</h2>
<ul>
<li>Loft water losses with unclear responsibility between the association and unit owners.</li>
<li>Fire and smoke losses in dense triple-decker blocks.</li>
<li>Flood versus wind or sewer backup in the same event.</li>
<li>Frozen pipes in vacant or partially rented units.</li>
<li>Older plaster, trim and windows priced as modern materials.</li>
</ul>

<h2>Getting started</h2>
<p>We start by reviewing the policy, the claim file and the carrier’s estimate. If there is a real gap and your policy has an appraisal or reference provision, we can serve as your appraiser. Our <a href="/estimators/appraisal-file-checkup/">appraisal file checkup</a> is a quick way to see whether you have the documents you need.</p>
""",
        "faqs": [
            ("My loft in a Lowell mill building had water damage from a unit above. Who pays?", "It depends on the master deed, the association’s master policy and your HO-6. Often the association covers common elements and original structure, while your HO-6 covers your improvements and belongings."),
            ("Does my homeowners insurance cover Merrimack River flooding?", "Usually not. Flood from rising water is excluded from standard homeowner policies and typically needs separate flood insurance."),
            ("Can appraisal be used for a triple-decker I rent out?", "Often yes, if the policy includes an appraisal or reference provision. Rental properties may be on a dwelling or commercial form, so the wording matters."),
        ],
    },
    {
        "slug": "quincy", "city": "Quincy", "county": "Norfolk County", "region": "South Shore & South Coast",
        "perils": ["Coastal flooding", "Nor’easters", "Wind damage", "Ice dams", "Burst pipes"],
        "near": ["boston", "brockton", "cambridge"],
        "housing": "Capes, Colonials, two-families and waterfront condos",
        "storm": "March 2018 back-to-back nor’easters",
        "lede": "Quincy has miles of shoreline, and its coastal neighborhoods take the brunt of nor’easters. We help owners sort out wind, water and winter claims across the city.",
        "title": "Quincy, MA Insurance Appraiser | Nor’easter Claims",
        "desc": "Quincy, MA insurance appraisal for nor’easter, coastal flood, wind and ice dam claims in Houghs Neck, Squantum, Wollaston and Merrymount.",
        "body": """
<h2>A city on the water</h2>
<p>Quincy, in Norfolk County, wraps around Quincy Bay with neighborhoods that sit right on the shore. Houghs Neck reaches out into the bay with homes close to the water on several sides. Squantum sits on a peninsula near Boston. Wollaston Beach runs along Quincy Shore Drive, and Merrymount and Adams Shore are low-lying neighborhoods near the water. Inland, Quincy Center, West Quincy and South Quincy have older two-families, Capes and Colonials, plus condo buildings near the Red Line.</p>

<h2>The March 2018 nor’easters</h2>
<p>In March 2018, back-to-back nor’easters brought high winds and coastal flooding to the South Shore. Houghs Neck and other shoreline areas of Quincy saw streets flood and water reach homes. Storms like these are exactly where coverage disputes come from: water from storm surge is flood, which a standard homeowners policy excludes, while wind damage to roofs, siding and windows is usually covered.</p>
<p>When a nor’easter does both, the carrier and the owner may disagree about which damage came from which cause. Our guide to <a href="/claim-library/noreaster-wind-vs-flood-claims/">nor’easter wind vs. flood claims</a> walks through how that split is often argued. For the wind side of the claim, see our <a href="/what-we-appraise/hurricane-noreaster-appraisal/">hurricane and nor’easter appraisal</a> service.</p>
<div class="note"><b class="h">Coastal deductibles</b>Some coastal policies carry a separate wind or named-storm deductible, often a percentage of the dwelling limit. Check your declarations page, and try our <a href="/estimators/hurricane-deductible-calculator/">hurricane deductible calculator</a> to see what that means in dollars.</div>

<h2>Winter and inland claims</h2>
<p>Away from the water, Quincy claims look like most of Greater Boston: ice dams on older Capes, burst pipes in cold snaps, tree limbs on roofs and fire in closely spaced wood-frame homes. The city’s granite quarry history also means some homes sit on ledge and slopes, which can complicate drainage and foundation repairs.</p>

<h2>Common Quincy disputes</h2>
<ul>
<li>Wind versus surge arguments after coastal storms.</li>
<li>Siding and shingle repairs that ignore salt exposure or matching.</li>
<li>Percentage wind deductibles applied without clear explanation.</li>
<li>Condo water losses involving both the master policy and an HO-6.</li>
<li>Ice dam interior damage scoped too narrowly.</li>
</ul>
<p>If the carrier’s estimate is far below a contractor’s bid, appraisal may be a path to an independent amount of loss. Each side names an appraiser, the two appraisers try to agree, and an umpire settles what they cannot. Before you start, gather photos taken soon after the storm, tide and wind information if you have it, contractor bids and the full claim file. Shoreline homes in Squantum and Houghs Neck often have exterior damage on the side facing the bay and interior damage that shows up weeks later, so a complete record makes a real difference when the scope is argued.</p>
""",
        "faqs": [
            ("My Houghs Neck home took water in a nor’easter. Is that covered?", "Storm surge and rising water are generally excluded from homeowner policies and covered under flood insurance, if you have it. Wind damage from the same storm may still be covered under your homeowners policy."),
            ("Do Quincy homes have hurricane deductibles?", "Some coastal policies in Quincy include a wind or named-storm deductible, often set as a percentage. Your declarations page should show it."),
            ("Can appraisal resolve a wind versus flood dispute?", "Appraisal sets the amount of loss. Whether flood or wind caused a given item can overlap with coverage questions that appraisal may not decide. Consult a Massachusetts attorney if coverage is disputed."),
        ],
    },
    {
        "slug": "new-bedford", "city": "New Bedford", "county": "Bristol County", "region": "South Shore & South Coast",
        "perils": ["Hurricanes", "Nor’easters", "Wind-driven rain", "Fire", "Burst pipes"],
        "near": ["plymouth", "brockton", "barnstable"],
        "housing": "Triple-deckers, whaling-era homes and mill buildings",
        "storm": "1938 hurricane and Hurricane Carol (1954)",
        "lede": "New Bedford has lived with hurricanes for generations, and the harbor barrier is proof. We help owners on the South Coast get an independent look at disputed storm, fire and water claims.",
        "title": "Insurance Appraiser in New Bedford, MA | Storm Claims",
        "desc": "Storm, wind or fire claim in New Bedford, MA? Independent appraisal for triple-deckers and historic homes in the North End, South End and beyond.",
        "body": """
<h2>A harbor city shaped by storms</h2>
<p>New Bedford sits on Buzzards Bay in Bristol County, and its harbor has taken some of the worst storms in New England history. The Great New England Hurricane of 1938 and Hurricane Carol in 1954 both brought severe flooding to the waterfront. After those storms, the federal government built the New Bedford hurricane barrier, a large stone and earth dike with gates across the harbor entrance, finished in the 1960s.</p>
<p>The barrier protects much of the inner harbor from storm surge, but it does not stop wind. Hurricanes and nor’easters still bring damaging wind and driving rain to the city, and areas outside the barrier, including parts of Clarks Point and the South End shoreline, are more exposed.</p>

<h2>Neighborhoods and housing</h2>
<p>The North End and South End are dense with triple-deckers and multi-family homes, many built for mill and fishing workers. The historic downtown has whaling-era homes and brick commercial buildings. County Street has large older homes, and the West End mixes two-families and single homes. Former mill buildings around the city have been converted to housing and business space.</p>
<p>Older triple-deckers bring porches, low-slope roofs and layered siding. Whaling-era homes may have plaster, original windows and trim that cost more to repair than estimates often allow.</p>
<div class="note"><b class="h">Fire in dense neighborhoods</b>In closely spaced triple-decker blocks, a fire next door can bring heat, smoke and water damage to your home. Our <a href="/what-we-appraise/fire-smoke-damage-appraisal/">fire and smoke damage appraisal</a> service looks at the full scope, including odor and soot cleaning.</div>

<h2>Common New Bedford claim issues</h2>
<ul>
<li>Wind-driven rain damage treated as wear or maintenance.</li>
<li>Triple-decker losses that touch several units and policies.</li>
<li>Siding and roof repairs on older homes priced without matching.</li>
<li>Percentage wind or hurricane deductibles applied to coastal homes.</li>
<li>Fire and smoke damage in neighboring buildings.</li>
</ul>

<h2>Triple-decker claims</h2>
<p>New Bedford has a large stock of triple-deckers, and they bring special claim questions about stacked porches, shared roofs and multiple owners or tenants. Our guide on <a href="/claim-library/triple-decker-insurance-claims/">triple-decker insurance claims</a> covers the most common sticking points. If the carrier’s estimate falls short, appraisal under the policy may provide an independent amount of loss.</p>
<p>Massachusetts property policies are built around the state’s standard fire policy, which includes a process often called reference, where disinterested referees set the amount of loss. Many homeowner forms call it appraisal. It does not decide coverage or claim-handling questions; for those, consult a Massachusetts attorney. Our role is narrower: pricing the repair accurately and presenting it clearly.</p>
""",
        "faqs": [
            ("Does the hurricane barrier lower my insurance risk?", "The barrier reduces storm-surge flooding for much of the inner harbor. It does not prevent wind damage, and homes outside the barrier can still face surge. Your insurer sets rates and deductibles by its own rules."),
            ("Is a New Bedford triple-decker covered differently from a single-family home?", "It can be. Owner-occupied buildings are often on homeowner forms; fully rented buildings may be on dwelling or commercial policies. The wording affects coverage and appraisal."),
            ("Can you help with an older whaling-era home?", "Yes. We review claims on older homes where plaster, trim and windows need careful pricing."),
        ],
    },
    {
        "slug": "brockton", "city": "Brockton", "county": "Plymouth County", "region": "South Shore & South Coast",
        "perils": ["Wind and tree fall", "Ice dams", "Burst pipes", "Fire", "Heavy snow"],
        "near": ["quincy", "plymouth", "new-bedford"],
        "housing": "Triple-deckers, Capes, ranches and older two-families",
        "storm": "October 2017 wind storm",
        "lede": "Brockton’s older homes and mature trees make wind and winter claims common. We offer independent appraisal and estimate review across the city.",
        "title": "Brockton, MA Insurance Appraiser | Wind & Winter Claims",
        "desc": "Insurance appraisal in Brockton, MA for tree, wind, ice dam and fire claims on triple-deckers, Capes and two-families in Campello and Montello.",
        "body": """
<h2>A former shoe city with older housing</h2>
<p>Brockton, in Plymouth County, grew as a major shoe-manufacturing center, and its housing reflects that history. Campello in the south and Montello in the north have dense blocks of triple-deckers and two-families built for factory workers. Other parts of the city, including the west side near D.W. Field Park, have Capes, ranches and Colonials on larger lots with mature trees.</p>
<p>Older multi-family homes bring stacked porches, low-slope roofs and layered siding that are easy to underestimate. Capes and ranches bring ice dams and attic leaks in hard winters. Our <a href="/what-we-appraise/home-insurance-claim-appraisal/">home insurance claim appraisal</a> service covers both.</p>

<h2>Wind and trees</h2>
<p>In late October 2017, a powerful wind storm swept across southeastern Massachusetts, bringing down trees and knocking out power for many households. Another strong storm in October 2019 did similar damage. In Brockton, where large oaks and maples shade many streets, these storms often mean tree-fall claims with damage to roofs, gutters, siding, fences and cars.</p>
<p>Tree claims can get complicated. Tree removal coverage often has its own limits, and damage to the house may be split from removal costs. A careful scope covers framing, roofing, interior water damage and debris removal together.</p>
<div class="note"><b class="h">Roof measurements matter</b>Many tree and wind disputes come down to how much roof needs replacing. Our <a href="/estimators/roof-area-pitch-converter/">roof area and pitch converter</a> helps check the measurements in an estimate.</div>

<h2>Winter claims</h2>
<p>Brockton gets the same heavy snow and cold snaps as the rest of the South Shore. Ice dams on Capes, frozen pipes in older multi-families and snow load on low-slope roofs are all familiar. In multi-family buildings, a frozen pipe in one unit can damage others, which raises questions about which policy responds.</p>

<h2>Common Brockton disputes</h2>
<ul>
<li>Tree-fall claims with low removal limits or incomplete roof repairs.</li>
<li>Triple-decker water losses that cross units.</li>
<li>Ice dam interior damage scoped too narrowly.</li>
<li>Fire and smoke damage in closely spaced homes.</li>
<li>Siding repairs without matching on older homes.</li>
</ul>
<p>If the carrier’s number does not cover the repair, our <a href="/what-we-appraise/claim-estimate-review/">claim estimate review</a> is a good first step before deciding on appraisal.</p>
<h3>What to gather</h3>
<p>Photos of the damage before cleanup, the carrier’s estimate and any supplements, contractor bids, receipts for emergency work such as tree removal or tarping, and every letter from the insurer. Many Massachusetts policies limit lawsuits to about two years after a loss, so check your policy and talk to an attorney if timing is a concern. Our <a href="/estimators/claim-calendar-builder/">claim calendar builder</a> can help you keep track of dates.</p>
""",
        "faqs": [
            ("A tree fell on my Brockton home in a wind storm. What does my policy cover?", "Most homeowner policies cover damage to the house from a falling tree. Tree removal often has its own sublimit. Check your policy for details."),
            ("My Campello triple-decker had a frozen pipe that damaged two units. Is that one claim or two?", "If you own the building, it may be one claim under your policy. Tenants’ belongings are usually covered by their own renters policies. The wording of your policy matters."),
            ("Do you work with Brockton condo associations?", "Yes. We review condo and association claims, including disputes involving master policies."),
        ],
    },
    {
        "slug": "plymouth", "city": "Plymouth", "county": "Plymouth County", "region": "South Shore & South Coast",
        "perils": ["Hurricanes", "Nor’easters", "Coastal erosion", "Wind and tree fall", "Ice dams"],
        "near": ["brockton", "barnstable", "quincy"],
        "housing": "Capes, Colonials, beach cottages and newer subdivisions",
        "storm": "Hurricane Bob, August 1991",
        "lede": "Plymouth is the largest town by area in Massachusetts, with miles of coast, ponds and pine woods. We help owners with storm, wind and winter claims from Manomet to North Plymouth.",
        "title": "Insurance Appraiser in Plymouth, MA | Coastal Claims",
        "desc": "Plymouth, MA insurance appraisal for hurricane, nor’easter, wind and tree claims on homes in Manomet, White Horse Beach and Cedarville.",
        "body": """
<h2>A large town with a long coast</h2>
<p>Plymouth covers more land than any other municipality in Massachusetts, stretching along Cape Cod Bay from North Plymouth to the Cape Cod Canal area. Its coastal neighborhoods include Manomet, White Horse Beach, Priscilla Beach and Ellisville, many of them with older beach cottages and homes on bluffs or close to the water. Inland, Cedarville, South Pond and the pine woods have newer subdivisions, ranches and Colonials. Downtown Plymouth has older homes near the waterfront.</p>
<p>That mix means claims range from wind-driven damage on exposed oceanfront homes to tree-fall losses in wooded neighborhoods.</p>

<h2>Hurricanes and nor’easters</h2>
<p>Hurricane Bob in August 1991 brought strong winds to southeastern Massachusetts, including Plymouth, with widespread tree damage and power outages. Nor’easters are more frequent and can bring high winds, coastal flooding and erosion to bluffs and beaches, especially in places like Manomet and White Horse Beach.</p>
<p>Coastal homes may have separate wind or named-storm deductibles, often a percentage of the dwelling limit. Flood from storm surge is excluded from standard homeowner policies. Our <a href="/what-we-appraise/hurricane-noreaster-appraisal/">hurricane and nor’easter appraisal</a> service focuses on documenting the wind side of these losses.</p>
<div class="note"><b class="h">Know your deductible</b>A percentage deductible can be much larger than the flat deductible you expect. Use our <a href="/estimators/hurricane-deductible-calculator/">hurricane deductible calculator</a> to understand what applies before a storm.</div>

<h2>Wooded neighborhoods and winter</h2>
<p>Much of inland Plymouth is wooded with pitch pine and oak. Wind storms and heavy wet snow bring trees down on roofs, decks and fences. In winter, ice dams on Capes and frozen pipes in seasonal or lightly used homes are common claims. Seasonal homes left unheated can have pipes freeze and burst, and some policies have conditions about maintaining heat or draining systems.</p>

<h2>Common Plymouth claim disputes</h2>
<ul>
<li>Wind versus surge arguments on coastal homes.</li>
<li>Percentage hurricane deductibles applied after named storms.</li>
<li>Tree-fall claims with removal limits.</li>
<li>Frozen pipe claims on seasonal homes.</li>
<li>Cedar shingle siding repairs without matching.</li>
</ul>
<p>Appraisal may help when the carrier’s estimate is far below the real repair cost. It is not the right tool for every problem, though. If the insurer denies coverage outright, for example by calling the whole loss flood, appraisal may not resolve that question, and a Massachusetts attorney can explain your options.</p>
<h3>Seasonal and second homes</h3>
<p>Plymouth has many homes that sit empty for part of the year. Damage there can go unnoticed for weeks, and insurers sometimes argue that a slow leak or long-standing moisture is not a sudden loss. Regular checks, a working low-temperature alarm, and dated photos of the home’s condition can help if a dispute arises later.</p>
""",
        "faqs": [
            ("My Manomet home has a hurricane deductible. How does that work?", "Many coastal policies use a percentage deductible for named storms or wind, based on your dwelling limit. Check your declarations page for the exact terms."),
            ("I have a seasonal cottage in Plymouth and the pipes froze. Is that covered?", "It can be, but many policies require you to maintain heat or drain the plumbing in unoccupied homes. Check your policy conditions."),
            ("Does Plymouth have flood zones?", "Yes, many coastal areas are in FEMA flood zones. Flood is excluded from homeowner policies and needs separate flood insurance."),
        ],
    },
    {
        "slug": "barnstable", "city": "Barnstable", "county": "Barnstable County", "region": "Cape Cod & the Islands",
        "perils": ["Hurricanes", "Nor’easters", "Coastal flooding", "Wind-driven rain", "Frozen pipes"],
        "near": ["plymouth", "new-bedford", "brockton"],
        "housing": "Cape Cod cottages, shingle-style homes and seasonal houses",
        "storm": "Hurricane Carol (1954) and Bob (1991)",
        "lede": "Barnstable takes in Hyannis and six other villages along Nantucket Sound and Cape Cod Bay. We help Cape owners with hurricane, nor’easter and winter claims when the numbers do not add up.",
        "title": "Barnstable & Hyannis, MA Insurance Appraiser",
        "desc": "Insurance appraisal in Barnstable, MA covering Hyannis, Osterville, Centerville and Cotuit, with help on hurricane and nor’easter claims.",
        "body": """
<h2>Seven villages, one town</h2>
<p>Barnstable is the largest town on Cape Cod and the county seat of Barnstable County. It is made up of seven villages: Hyannis, Centerville, Osterville, Cotuit, Marstons Mills, West Barnstable and Barnstable Village. Hyannis has the harbor, ferries to Nantucket and Martha’s Vineyard, and a mix of year-round homes, condos and commercial buildings. Osterville, Centerville and Cotuit have large shingle-style homes and smaller Capes along Nantucket Sound. West Barnstable and Barnstable Village face Cape Cod Bay and the Great Marsh.</p>

<h2>Hurricane history</h2>
<p>The Cape has a long hurricane history. Hurricane Carol in 1954 and Hurricane Bob in 1991 both brought strong winds and storm surge to Barnstable and the rest of the Cape. Nor’easters come more often, with high winds, coastal flooding and erosion. Homes along the south shore of the Cape facing Nantucket Sound can be exposed to surge in a major storm.</p>
<p>Many Cape homes are insured through the Massachusetts Property Insurance Underwriting Association, the state’s FAIR Plan, which writes a large share of coastal policies. FAIR Plan and private policies here commonly carry percentage wind or hurricane deductibles, often between 1% and 5% of the dwelling limit.</p>
<div class="note"><b class="h">Percentage deductibles</b>A 2% deductible on a home insured for $800,000 is $16,000, for example. Our <a href="/estimators/hurricane-deductible-calculator/">hurricane deductible calculator</a> helps you see the real number before you need it.</div>

<h2>Cape housing and claim patterns</h2>
<p>Cedar shingle siding, wood windows and older roofs are common on the Cape. Salt air wears materials faster, and matching shingles or trim after a storm can be difficult. Seasonal homes left empty in winter face frozen pipes and undiscovered leaks. Wind-driven rain can enter through siding and windows and cause hidden damage. Our <a href="/what-we-appraise/hurricane-noreaster-appraisal/">hurricane and nor’easter appraisal</a> service is built for these kinds of claims.</p>

<h2>Common Barnstable disputes</h2>
<ul>
<li>Wind versus storm surge on waterfront homes.</li>
<li>Percentage deductibles applied without clear explanation.</li>
<li>Cedar shingle and trim repairs without matching.</li>
<li>Frozen pipe claims on seasonal homes.</li>
<li>Hidden wind-driven rain damage behind siding.</li>
</ul>
<p>If your claim is stuck, our <a href="/appraisal-roadmap/">appraisal roadmap</a> explains how the process usually works.</p>
<h3>Picking an umpire on the Cape</h3>
<p>When the two appraisers cannot agree, an umpire decides the items in dispute. On the Cape, it helps if that person understands coastal construction, cedar shingle work and the cost of getting trades to a village like Cotuit or Osterville in peak season. Our guide to <a href="/claim-library/choosing-an-umpire-in-massachusetts/">choosing an umpire in Massachusetts</a> covers what to look for and what to avoid.</p>
""",
        "faqs": [
            ("Is my Hyannis home insured through the FAIR Plan?", "Many Cape homes are insured through the Massachusetts Property Insurance Underwriting Association. Your declarations page shows your insurer."),
            ("Does the FAIR Plan allow appraisal?", "Massachusetts property policies generally include an appraisal or reference process. Check your policy wording for the exact terms."),
            ("My Osterville summer home had a frozen pipe. Is that covered?", "It may be, but many policies have conditions for unoccupied homes, such as maintaining heat or draining pipes. Check your policy."),
        ],
    },
    {
        "slug": "pittsfield", "city": "Pittsfield", "county": "Berkshire County", "region": "Pioneer Valley & the Berkshires",
        "perils": ["Heavy snow load", "Ice dams", "Frozen pipes", "Summer hail", "River and stream flooding"],
        "near": ["springfield", "worcester", "lowell"],
        "housing": "Victorians, older two-families, Capes and lake cottages",
        "storm": "Tropical Storm Irene, August 2011",
        "lede": "Pittsfield winters are long and snowy, and the city’s older homes feel it. We provide independent appraisal for owners across the Berkshires.",
        "title": "Pittsfield, MA Insurance Appraiser | Snow & Ice Claims",
        "desc": "Pittsfield, MA insurance appraisal for snow load, ice dam, frozen pipe and hail claims on older homes, two-families and lake cottages.",
        "body": """
<h2>The Berkshires’ largest city</h2>
<p>Pittsfield is the county seat and largest city of Berkshire County, set in a valley between the Taconic Range and the hills to the east. Its neighborhoods include Morningside and the Westside, both with older two-families and worker housing, plus Victorians near downtown and Capes and ranches on the edges of the city. Homes near Pontoosuc Lake and Onota Lake range from cottages to larger year-round houses.</p>
<p>Many of these homes are older, with plaster, slate or older asphalt roofs, and limited attic insulation, which affects how winter damage happens and how it is repaired.</p>

<h2>Snow, ice and cold</h2>
<p>Pittsfield gets more snow than Boston and colder temperatures, especially at higher elevations nearby. Heavy snow and ice on roofs can cause ice dams, leaks and, in extreme cases, structural damage. Frozen pipes are common in older homes and seasonal lake properties.</p>
<p>Ice dam claims often turn on what is covered: interior water damage from a dam is often covered, while the dam itself is treated as maintenance. Our <a href="/what-we-appraise/ice-dam-snow-load-appraisal/">ice dam and snow load appraisal</a> service focuses on getting the full interior damage into the estimate. Our guide on <a href="/claim-library/ice-dam-claims-what-gets-missed/">ice dam claims</a> explains what often gets left out.</p>
<div class="note"><b class="h">Snow load</b>Our <a href="/estimators/roof-snow-load-estimator/">roof snow load estimator</a> gives a rough sense of how much weight snow and ice put on a roof.</div>

<h2>Storms and flooding</h2>
<p>Tropical Storm Irene in August 2011 brought heavy rain and flooding to western Massachusetts, with the worst damage in hill towns and river valleys. Summer thunderstorms in the Berkshires can bring hail and damaging winds. Flood from rising water is excluded under standard homeowner policies.</p>

<h2>Common Pittsfield disputes</h2>
<ul>
<li>Ice dam interior damage scoped too narrowly.</li>
<li>Frozen pipe claims on seasonal lake homes.</li>
<li>Hail damage written as cosmetic.</li>
<li>Slate roof repairs priced as asphalt.</li>
<li>Flood versus surface water or sewer backup.</li>
</ul>
<p>When the carrier’s estimate does not cover the repair, appraisal may provide an independent amount of loss.</p>
<h3>Distance and contractor pricing</h3>
<p>Estimating software sometimes uses regional prices that do not match what Berkshire contractors actually charge, especially after a storm when local trades are booked for weeks. Specialty work like slate roofing may require bringing in crews from farther away. We compare the carrier’s pricing with local bids and note where travel, availability or specialty labor change the real cost. If you want an outside check first, our <a href="/what-we-appraise/claim-estimate-review/">claim estimate review</a> is a lower-commitment place to start.</p>
""",
        "faqs": [
            ("Is snow load damage covered in Massachusetts?", "Many policies cover collapse or damage from the weight of snow or ice, but wording varies. Check your policy."),
            ("My lake cottage near Onota Lake had frozen pipes. Is that covered?", "It may be, but many policies have conditions for unoccupied homes. Check your policy."),
            ("Does hail hit Pittsfield?", "Yes. Summer thunderstorms in the Berkshires can bring hail."),
        ],
    },
    {
        "slug": "salem", "city": "Salem", "county": "Essex County", "region": "North Shore & Merrimack Valley",
        "perils": ["Nor’easters", "Coastal flooding", "Ice dams", "Fire in historic homes", "Wind and tree fall"],
        "near": ["lowell", "cambridge", "boston"],
        "housing": "Federal-era homes, Victorians, two-families and condos",
        "storm": "Blizzard of February 1978",
        "lede": "Salem’s historic homes and harbor neighborhoods bring claims that need careful pricing. We help owners on the North Shore get an independent number.",
        "title": "Salem, MA Insurance Appraiser | Historic Home Claims",
        "desc": "Insurance appraisal in Salem, MA for historic homes, coastal storm and ice dam claims in the McIntire district, Derby Street and Salem Willows.",
        "body": """
<h2>Historic homes on the harbor</h2>
<p>Salem, in Essex County, has one of the most concentrated collections of historic homes in the country. The McIntire Historic District along Chestnut Street and Federal Street has Federal-era mansions, many with original woodwork, plaster and windows. Derby Street runs along the harbor near the waterfront, with older homes and businesses. Salem Willows sits on a point at the edge of the harbor, with cottages and homes exposed to wind and water.</p>
<p>Other neighborhoods, including the Point, South Salem and the area near Gallows Hill, have two-families, triple-deckers and Victorians. Condo conversions are common in older buildings across the city.</p>

<h2>Storms on the North Shore</h2>
<p>The Blizzard of February 1978 brought heavy snow, high winds and coastal flooding to the North Shore, and it remains a benchmark for coastal storms here. Nor’easters still bring wind, rain and flooding to Salem’s waterfront neighborhoods. Flood from storm surge is excluded under standard homeowner policies, while wind damage is usually covered.</p>
<p>Our <a href="/what-we-appraise/hurricane-noreaster-appraisal/">hurricane and nor’easter appraisal</a> service focuses on the wind side of these claims. For water damage from burst pipes or ice dams, see <a href="/what-we-appraise/water-damage-claim-appraisal/">water damage claim appraisal</a>.</p>
<div class="note"><b class="h">Historic repairs cost more</b>Original woodwork, plaster and windows in Salem’s historic homes often cost more to repair than estimates allow. Historic district rules may also require specific materials.</div>

<h2>Common Salem claim disputes</h2>
<ul>
<li>Historic woodwork and plaster priced as modern materials.</li>
<li>Wind versus surge on waterfront homes.</li>
<li>Ice dam interior damage scoped too narrowly.</li>
<li>Fire and smoke damage in closely spaced older homes.</li>
<li>Condo water losses involving both the master policy and an HO-6.</li>
</ul>

<h2>Getting started</h2>
<p>If your claim is stuck, our <a href="/claim-library/massachusetts-reference-and-appraisal-clause/">guide to the Massachusetts reference and appraisal clause</a> explains how the process usually works. In short, each side picks a disinterested appraiser, the appraisers try to agree on the amount of loss, and an umpire or referee resolves what they cannot. The process sets a number; it does not decide coverage, and it is not a lawsuit.</p>
<h3>Documenting an older Salem home</h3>
<p>For a historic house, the best evidence is often what the home looked like before the loss: photos of moldings, doors, mantels and windows, notes on original materials, and any past restoration invoices. That record helps show why a like-kind repair costs more than a modern replacement. If a historic commission review is required for exterior work, keep copies of those requirements too, since they can affect both cost and schedule.</p>
<p>Salem’s waterfront neighborhoods also face salt exposure year-round, which can shorten the life of roofing, flashing and paint. Insurers sometimes point to that wear when they limit a claim, so separating storm damage from age-related wear is an important part of any estimate review.</p>
""",
        "faqs": [
            ("Do historic district rules affect my Salem claim?", "They can. Historic district rules may require specific materials or methods, which can raise repair costs. Ordinance-or-law coverage in your policy may apply."),
            ("My Salem Willows home flooded in a nor’easter. Is that covered?", "Storm surge flooding is generally excluded from homeowner policies and covered under flood insurance, if you have it."),
            ("Can you help with a condo in a converted Salem building?", "Yes. We review condo claims, including disputes involving master policies and HO-6 coverage."),
        ],
    },
]
