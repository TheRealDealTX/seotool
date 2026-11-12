"""Maine location pages for Maine Insurance Appraiser.

Each entry holds town-specific copy: neighborhoods, housing mix, real storm
history and FAQs. Storm details are limited to well-documented events.
"""

LOCATIONS = [
    # ------------------------------------------------------------------ Portland
    {
        "slug": "portland-maine",
        "city": "Portland",
        "county": "Cumberland County",
        "region": "Greater Portland & Casco Bay",
        "perils": ["Coastal storm surge", "Ice dams", "Nor’easter wind", "Burst pipes"],
        "near": ["scarborough-maine", "biddeford-maine", "brunswick-maine"],
        "neighborhoods": ["Munjoy Hill", "West End", "Deering", "Back Cove", "Old Port", "Stroudwater", "Peaks Island"],
        "housing": "Victorian brick and Italianate homes in the West End, triple-deckers and multi-units on Munjoy Hill and East Bayside, capes and bungalows in Deering, and a growing stock of condos on the peninsula and ferry-served island homes.",
        "storms": [
            ("Jan 2024", "Back-to-back coastal storms", "Record 14.57 ft tide on Jan 13 flooded Commercial Street and damaged Old Port wharves."),
            ("Feb 1978", "Blizzard of 1978", "Set a 14.17 ft Portland tide record that stood for 46 years; heavy snow and surge along the waterfront."),
            ("Oct 2017", "October windstorm", "Record statewide power outages; fallen trees on roofs and cars across Portland neighborhoods."),
        ],
        "title": "Insurance Appraiser Portland, Maine | Claim Disputes",
        "desc": "Portland, Cumberland County property claim underpaid? An independent appraiser for storm surge, ice dam, water and fire loss disputes.",
        "lede": "From West End brick to Munjoy Hill triple-deckers and Peaks Island cottages, Portland claims rarely fit a stock estimate. We review and appraise underpaid property claims across the city and Casco Bay islands.",
        "body": """<h2>Where Portland claims go sideways</h2>
<p>Most Portland disputes we hear about are not denials. The carrier accepted the loss, sent an estimate and paid something. The problem is the gap between that number and what a Portland contractor will actually charge to put a peninsula house back together. An independent insurance appraiser in Portland looks at that gap line by line, using the appraisal clause in your policy when the disagreement is about amount rather than coverage.</p>
<p>Cumberland County’s largest city packs a lot of building types into a small footprint. A single block on Munjoy Hill can hold a 1880s triple-decker, a gut-renovated condo and a new infill building, each with a different repair path after the same storm.</p>
<h2>Brick, clapboard and three-decker math</h2>
<p>The West End’s Victorian and Italianate homes carry plaster walls, tall windows, slate or copper details and ornate trim that rarely show up correctly in a carrier’s software. Triple-deckers in Munjoy Hill and East Bayside raise a different issue: a roof leak or burst pipe on the third floor often runs through two units below, and the estimate has to follow the water all the way down. In Deering, Back Cove and Stroudwater, capes and bungalows tend to be simpler, but siding and shingle matching still drive many disagreements when a discontinued clapboard color or profile can’t be found.</p>
<ul>
<li>Plaster and lath priced as half-inch drywall.</li>
<li>Condo losses split between the association master policy and a unit owner’s policy.</li>
<li>Historic-district window and trim work left out of scope.</li>
<li>Peninsula access, parking and staging costs ignored.</li>
</ul>
<h2>Tides that rewrote the record book</h2>
<p>On January 13, 2024, the Portland tide gauge hit 14.57 feet, beating the 14.17-foot mark set in the Blizzard of 1978. Seawater ran up Commercial Street and into buildings along the Old Port wharves, days after a January 10 storm had already done damage. Coastal flood damage is excluded under most homeowners policies and belongs to flood coverage, but the wind, wind-driven rain and roof damage from the same storms often belong to the property claim. Separating the two is where many Portland disagreements start; our guide to <a href="/owner-guides/noreaster-wind-versus-flood-maine/">nor’easter wind versus flood</a> walks through it.</p>
<p>The October 2017 windstorm is the other modern benchmark: record outages statewide, and big hardwoods down on houses and cars across the city’s older neighborhoods.</p>
<h2>Island work and inspection notes</h2>
<p>Peaks Island and the other Casco Bay islands add ferry fares, barge costs for materials and dumpsters, and crew travel time that a mainland estimate leaves out. A Portland insurance appraiser should price those access costs as part of the repair, not as an afterthought. Winter work on any peninsula roof also means snow removal, staging on steep pitches and shorter days.</p>
<p>If the dispute centers on water, see our <a href="/appraisal-work/water-damage-loss-appraisal/">water damage loss appraisal</a> page; for association buildings, our <a href="/appraisal-work/commercial-condo-association-appraisal/">condo and commercial appraisal</a> work covers master-policy losses. Coverage questions and deadlines belong with a Maine attorney.</p>
""",
        "faqs": [
            ("Does my Portland homeowners policy cover flooding from a record tide?", "Usually not. Most homeowners policies exclude flood, including storm surge, and that damage belongs to an NFIP or private flood policy. Wind, wind-driven rain and roof damage from the same storm are often covered, so read your policy and separate the two carefully."),
            ("Can appraisal account for the extra cost of working on Peaks Island?", "Yes, when the disagreement is about the amount of loss. Ferry fares, barging materials and crew travel are real repair costs, and an appraiser can document and price them as part of the estimate."),
            ("My Munjoy Hill triple-decker leak damaged three units. Who handles that?", "It depends on whether the building is one owner’s policy or a condo with a master policy plus unit-owner policies. The policies decide who pays which part, and appraisal can then set the amount once responsibility is clear."),
        ],
    },
    # ------------------------------------------------------------------ Lewiston
    {
        "slug": "lewiston-maine",
        "city": "Lewiston",
        "county": "Androscoggin County",
        "region": "Western Mountains & Lakes",
        "perils": ["Burst pipes", "Ice dams", "Oil-burner puffback", "Fallen trees"],
        "near": ["brunswick-maine", "augusta-maine", "portland-maine"],
        "neighborhoods": ["Tree Streets", "Little Canada", "Bates Mill District", "Lisbon Street downtown", "South Lewiston", "Auburn"],
        "housing": "Wood-frame triple-deckers and multi-family tenements in the Tree Streets and downtown, brick mill buildings converted to offices and apartments, and capes, ranches and split-levels toward the city’s edges.",
        "storms": [
            ("Dec 2023", "December 18 storm", "Wind and heavy rain sent the Androscoggin to major flood levels; trees and lines down across the city."),
            ("Jan 1998", "Ice Storm of 1998", "Heavy glaze toppled trees and lines across central and southern Maine; long outages in Androscoggin County."),
            ("Apr 1987", "April 1987 floods", "Snowmelt and rain pushed the Androscoggin to one of its highest crests at Lewiston and Auburn."),
        ],
        "title": "Insurance Appraiser Lewiston, Maine | Underpaid Claims",
        "desc": "Underpaid claim in Lewiston or elsewhere in Androscoggin County? Independent appraisal for multi-family, mill building and winter losses.",
        "lede": "Lewiston’s multi-family tenements and mill buildings turn a single burst pipe or puffback into a multi-unit claim. We review carrier estimates and serve as appraiser when the amount of loss is in dispute.",
        "body": """<h2>A city of shared walls</h2>
<p>Lewiston grew around the Great Falls of the Androscoggin, and its housing still shows it. The Tree Streets and the old Little Canada area are dense with wood-frame triple-deckers and tenement blocks built for mill workers. When a pipe freezes on the third floor of one of those buildings in January, the water does not stop at one unit. Ceilings, wiring, flooring and tenant contents below all become part of the same claim, and that is where carrier estimates tend to come up short.</p>
<p>An insurance appraiser in Lewiston spends a lot of time on these multi-unit losses: following the water path, counting every affected room, and making sure loss-of-rents and code items that apply to rental buildings are not left out when the policy covers them.</p>
<h2>Mills, brick and the cost of old buildings</h2>
<p>The Bates Mill complex and other brick mills along the canals have been converted to offices, restaurants and apartments. Those buildings have heavy timber framing, tall masonry walls and large roof areas, and their repair costs do not resemble a standard Androscoggin County house. Commercial owners and associations in these buildings should expect the estimate fight to center on scope and access, not unit prices alone. Our <a href="/appraisal-work/commercial-condo-association-appraisal/">commercial and condo appraisal</a> page explains how appraisal works for larger buildings.</p>
<h3>Heating oil and puffback</h3>
<p>Like much of Maine, a large share of Lewiston’s older housing heats with oil. A burner misfire can blow soot through every room and every unit served by the system. Puffback claims are often underpaid because the soot is fine and spread wide, so cleaning scopes miss closets, ductwork and contents. See our <a href="/owner-guides/oil-burner-puffback-documentation/">puffback documentation guide</a> before cleanup starts.</p>
<h2>Storms that shaped local claims</h2>
<p>The December 18, 2023 storm combined damaging wind with heavy rain on snowpack, and the Androscoggin rose to major flood levels through Lewiston and Auburn. River flooding is excluded under homeowners policies, but the fallen trees and roof damage from the same storm were property claims. The April 1987 floods are still the reference point for older residents along the river, and the Ice Storm of January 1998 left much of the region without power for days, with frozen pipes following in homes that lost heat.</p>
<h2>What we check on a Lewiston inspection</h2>
<ul>
<li>Every unit and common area touched by water, not just the source unit.</li>
<li>Plaster, wood lath and old wiring that has to be opened up and brought to code.</li>
<li>Soot migration through shared heating systems and stairwells.</li>
<li>Tree removal and crane access on tight lots in South Lewiston and downtown.</li>
</ul>
<p>A Lewiston insurance appraiser can only resolve the amount of loss. If the carrier is disputing coverage or you are close to a policy deadline, talk to a Maine attorney.</p>
""",
        "faqs": [
            ("Does appraisal work for a Lewiston rental building with several units?", "Yes. Appraisal decides the amount of loss for the whole covered claim, which can include damage across several units, common areas and loss of rents if your policy covers it."),
            ("The carrier’s puffback estimate only covers the basement. Is that normal?", "It is a common shortfall. Soot from an oil burner misfire often travels through ducts and stairwells, so the cleaning scope should be based on where soot is actually found throughout the building."),
            ("Was the December 2023 Androscoggin flooding covered by homeowners policies?", "River flooding is generally excluded and falls under flood insurance. Wind damage and fallen trees from the same storm are typically handled under the property policy, so check your policy language."),
        ],
    },
    # ------------------------------------------------------------------ Bangor
    {
        "slug": "bangor-maine",
        "city": "Bangor",
        "county": "Penobscot County",
        "region": "Penobscot Valley & Highlands",
        "perils": ["Ice dams", "Snow load", "River ice and surge", "Chimney fires"],
        "near": ["bar-harbor-maine", "waterville-maine", "rockland-maine"],
        "neighborhoods": ["Downtown Bangor", "Broadway Historic District", "Fairmount", "Little City", "East Side", "Brewer", "Hampden"],
        "housing": "Lumber-era Victorian and Greek Revival homes along Broadway and West Broadway, brick downtown blocks rebuilt after the 1911 fire, and capes, ranches and newer subdivisions toward Hampden and Brewer.",
        "storms": [
            ("Feb 1976", "Groundhog Day Gale", "Storm surge ran up the Penobscot and flooded downtown Bangor, submerging cars on the streets."),
            ("Jan 1998", "Ice Storm of 1998", "Ice-laden trees and lines came down across the Bangor region; many homes lost heat for days."),
            ("Oct 2017", "October windstorm", "Record statewide outages; downed trees and lines across Greater Bangor."),
        ],
        "title": "Bangor, Maine Insurance Appraiser | Estimate Review",
        "desc": "Insurance appraisal for Bangor and Penobscot County homes and businesses: ice dams, snow load, fire and wind claims the carrier underpaid.",
        "lede": "Bangor’s lumber-baron Victorians, post-1911 brick blocks and long, snowy winters create claims that standard estimates often miss. We help owners across Penobscot County challenge underpaid property claims.",
        "body": """<h2>Winter is the main event</h2>
<p>Bangor sits far enough inland that its winters are colder and longer than the coast, and that shows up in the claims. Ice dams on Fairmount and Little City capes, snow load on flat and low-slope commercial roofs downtown, and pipes that freeze when a furnace quits overnight are the bread and butter of property disputes here. Ice dam water often appears weeks after the dam formed, which leads carriers to question timing and prior damage. A Bangor insurance appraiser documents the dam, the water path and the interior damage together so the estimate reflects the whole loss. Our <a href="/owner-guides/ice-dam-claims-maine-estimates/">ice dam estimates guide</a> covers what to photograph.</p>
<h2>Lumber money and old houses</h2>
<p>Bangor was once a leading lumber port, and the mansions along Broadway and West Broadway show it: Victorian and Greek Revival houses with slate roofs, deep cornices, plaster ceilings and hardwood details. Repairing those homes takes specialized trades, and in Penobscot County there are not many of them. After a regional storm, that scarcity pushes prices and timelines up.</p>
<p>Downtown is different again. The Great Fire of April 1911 destroyed much of the business district, and the brick blocks that replaced it are now over a century old. Masonry repointing, parapet repairs and old timber framing complicate both fire and water claims there.</p>
<h2>The river remembers</h2>
<p>On February 2, 1976, the Groundhog Day Gale pushed a surge up the Penobscot that flooded downtown Bangor and submerged cars along the Kenduskeag Stream. The Ice Storm of January 1998 brought down trees and lines across the region, and the October 2017 windstorm caused record outages statewide. Flood is excluded under homeowners policies, but wind, fallen trees and freeze damage that follows a long outage generally fall under the property claim.</p>
<h2>What an insurance appraiser in Bangor watches for</h2>
<ul>
<li>Slate and cedar roofs priced as asphalt replacements.</li>
<li>Snow and ice removal needed before roofers can work.</li>
<li>Chimney and wood-stove fire claims where smoke spread is under-scoped.</li>
<li>Brewer and Hampden properties where tree removal near lines needs specialized crews.</li>
</ul>
<p>Many Bangor homes rely on oil heat. A burner puffback in a big Victorian can coat three floors of plaster and woodwork in soot, and cleaning those surfaces costs more than wiping drywall. Wood stoves and chimneys in Hampden and Brewer add fire and smoke claims each heating season. Whether the problem is soot, smoke or water, the estimate should reflect the age and finishes of the house, not a generic room.</p>
<p>When the disagreement is purely about price, appraisal under the policy can settle it. See our <a href="/appraisal-work/ice-dam-snow-load-appraisal/">ice dam and snow load appraisal</a> page for how we approach winter roof losses. For coverage disputes or deadline questions, consult a Maine attorney.</p>
""",
        "faqs": [
            ("My Bangor ice dam leak showed up in March. Will the carrier say it is old damage?", "They may raise it. Ice dam water often appears weeks after the dam forms, so photos of the roof edge, ice buildup and interior staining help tie the damage to the winter event."),
            ("Does appraisal help with a slate roof on a Broadway Victorian?", "It can. If the carrier priced a slate roof as asphalt or ignored matching, the appraisal panel can set the amount based on proper materials and labor, as long as coverage itself is not disputed."),
            ("Who decides whether downtown Bangor flood damage is covered?", "Your policy language decides, and flood is usually excluded from property policies. Appraisal does not decide coverage, so a Maine attorney is the right resource for coverage questions."),
        ],
    },
    # ------------------------------------------------------------------ Augusta
    {
        "slug": "augusta-maine",
        "city": "Augusta",
        "county": "Kennebec County",
        "region": "Central Maine & the Kennebec Valley",
        "perils": ["River-adjacent water", "Ice dams", "Windstorm trees", "Frozen pipes"],
        "near": ["waterville-maine", "lewiston-maine", "brunswick-maine"],
        "neighborhoods": ["Water Street downtown", "Sand Hill", "the East Side", "Capitol area", "North Augusta", "Hallowell", "Manchester"],
        "housing": "Nineteenth-century brick commercial blocks on Water Street, Victorian and Colonial Revival homes near the State House, mill-era duplexes on the East Side, and capes and ranches toward North Augusta and Manchester.",
        "storms": [
            ("Dec 2023", "December 18 storm", "Kennebec reached major flood stage, swamping Water Street lots in Augusta and downtown Hallowell."),
            ("Apr 1987", "April 1987 floods", "Kennebec flood inundated low-lying downtown Augusta and Hallowell along the river."),
            ("Jan 1998", "Ice Storm of 1998", "Ice brought down trees and lines across the Kennebec Valley; outages lasted days to weeks."),
        ],
        "title": "Augusta, Maine Insurance Appraiser | Claim Appraisal",
        "desc": "Augusta and Kennebec County property claims reviewed by an independent appraiser. Wind, ice dam, water and fire losses the carrier underpaid.",
        "lede": "In Augusta, the Kennebec, hillside neighborhoods and old brick downtown each shape how a claim plays out. We review carrier estimates for homes and businesses and act as appraiser when the amount of loss is disputed.",
        "body": """<h2>Augusta claims in context</h2>
<p>Augusta is the capital and the county seat of Kennebec County, and it is a river city first. Water Street’s brick blocks sit right on the Kennebec, the East Side climbs from the river with mill-era duplexes and older single-family homes, and the Capitol area holds Victorian and Colonial Revival houses on tree-lined streets. An insurance appraiser in Augusta has to account for all of these: masonry downtown, plaster and old framing up the hill, and newer construction in North Augusta.</p>
<h2>The Kennebec and the flood line</h2>
<p>Twice in living memory the river has taken over downtown. The April 1987 floods put the Kennebec into low-lying parts of Augusta and Hallowell, and on December 18, 2023, the river reached major flood stage again, filling the Water Street parking lots and flooding businesses in neighboring Hallowell. That storm also brought strong winds that toppled trees across the Kennebec Valley.</p>
<p>River flooding is excluded under homeowners and most commercial property policies, and it belongs to flood insurance. But a storm like December 2023 almost always produces both kinds of damage. A tree through the roof, wind-driven rain through a damaged wall, or a sump failure with its own endorsement may fall under the property policy. Keeping those losses separate and well documented matters before any appraisal begins.</p>
<h2>Ice, outages and frozen pipes</h2>
<p>The Ice Storm of January 1998 is still the benchmark for central Maine outages. When heat is out for days in January, pipes freeze and split, and the water damage that follows can dwarf the tree damage that started it. The same pattern repeats on a smaller scale nearly every winter. If you own a camp or second home on one of the area’s lakes, our <a href="/claim-math/seasonal-camp-vacancy-check/">seasonal camp vacancy check</a> helps you see how vacancy and freeze-protection terms in your policy may apply.</p>
<h2>Where an Augusta insurance appraiser looks closer</h2>
<ul>
<li>Brick and masonry work on Water Street buildings, including scaffolding and street access.</li>
<li>Hidden water in plaster walls and ceilings after a freeze.</li>
<li>Tree removal costs on steep East Side lots where cranes are needed.</li>
<li>Contents and inventory for downtown businesses.</li>
</ul>
<p>Commercial owners on Water Street face an extra layer: many buildings share party walls, so a fire or roof leak in one block can damage its neighbors. Business income, inventory and tenant improvements all come into play. Homeowners in Sand Hill and on the East Side often have older plumbing and wiring that repairs expose, and code upgrades may be covered if the policy includes ordinance or law coverage.</p>
<p>Appraisal is designed for disputes over the amount of loss. Our <a href="/the-appraisal-path/">appraisal process guide</a> explains each step, and the <a href="/claim-math/claim-date-tracker/">claim date tracker</a> helps you keep proof-of-loss and policy dates in view. For coverage disputes or questions about legal deadlines, consult a Maine attorney.</p>
""",
        "faqs": [
            ("My Augusta business had river water and roof damage in December 2023. Can appraisal handle both?", "Appraisal sets the amount of a covered loss. River flood damage is usually excluded and handled by flood insurance, while wind and roof damage may be covered by the property policy, so the losses should be documented separately."),
            ("Do frozen pipes after a power outage count as a covered loss?", "Often yes, but policies can limit coverage if heat was not maintained or the home was vacant. Read the freeze and vacancy language in your policy, and keep records of the outage."),
            ("Can I invoke appraisal if the carrier has not finished its estimate?", "Generally appraisal is used once there is a disagreement over the amount of loss. Check your policy’s appraisal clause for its exact conditions and timing, and ask a Maine attorney about deadlines."),
        ],
    },
    # ------------------------------------------------------------------ Biddeford
    {
        "slug": "biddeford-maine",
        "city": "Biddeford",
        "county": "York County",
        "region": "Southern Coast",
        "perils": ["Seawall and surf", "Nor’easter wind", "Mill building water", "Ice dams"],
        "near": ["scarborough-maine", "portland-maine", "sanford-maine"],
        "neighborhoods": ["Downtown Main Street", "Mill District", "Biddeford Pool", "Hills Beach", "Fortunes Rocks", "Granite Point", "Saco"],
        "housing": "Massive brick textile mills along the Saco River now converted to apartments, studios and offices, wood-frame tenements and duplexes downtown, and oceanfront cottages and year-round homes at Biddeford Pool, Hills Beach and Fortunes Rocks.",
        "storms": [
            ("Jan 2024", "Back-to-back coastal storms", "Surf undermined the Fortunes Rocks seawall; several shorefront homes were declared unsafe."),
            ("Mar 2024", "March 10 coastal storm", "High tide and wind hit the same Biddeford Pool and Fortunes Rocks shoreline still under repair."),
            ("May 2006", "Mother’s Day flood", "More than a foot of rain in places caused widespread flooding and damage across York County."),
        ],
        "title": "Insurance Appraiser Biddeford, Maine | Coast and Mill",
        "desc": "Biddeford and York County claim appraisal for shorefront homes and mill conversions. Get a second look at an underpaid storm or water claim.",
        "lede": "Biddeford pairs huge brick mill conversions along the Saco River with exposed shorefront at the Pool, Hills Beach and Fortunes Rocks. We help owners and associations challenge underpaid claims on both kinds of property.",
        "body": """<h2>Two very different Biddefords</h2>
<p>Downtown Biddeford is defined by its mills. The Pepperell Mill campus and its neighbors along the Saco River are massive brick buildings, many now converted to apartments, condos, studios and restaurants. A few miles east, the city turns into shoreline: Biddeford Pool, Hills Beach, Fortunes Rocks and Granite Point, where cottages and year-round homes sit close to the surf. An insurance appraiser in Biddeford has to price both a fourth-floor water loss in a mill condo and wave damage to a shingle-style cottage.</p>
<h2>Shorefront losses after 2024</h2>
<p>The January 10 and 13, 2024 storms hit the Biddeford shoreline hard. Surf undermined the seawall along Fortunes Rocks, roads washed out, and several shorefront homes were declared unsafe. The March 10, 2024 storm then struck the same stretch while repairs were still under way. Three storms in three months create a real challenge: carriers may argue that damage from one event was really from another, or that it pre-dated the policy period.</p>
<p>Wave wash and storm surge are flood, and homeowners policies typically exclude them. Wind damage to roofs, siding and windows from the same storms is usually a property claim. Good dated photos after each storm make the difference when separating the two. Our <a href="/appraisal-work/noreaster-hurricane-appraisal/">nor’easter and hurricane appraisal</a> page explains how we handle mixed-cause coastal losses.</p>
<h2>Inside the mills</h2>
<p>Mill conversions bring association master policies, unit-owner policies and commercial tenants under one roof. A sprinkler or pipe failure on an upper floor can run through heavy timber floors into several units and a business below. Questions about who owns which piece of the building come first and are decided by the policies and association documents; appraisal then sets the amount. Biddeford associations can read about our <a href="/appraisal-work/commercial-condo-association-appraisal/">commercial and condo association appraisal</a> work.</p>
<h2>Pricing realities in York County</h2>
<ul>
<li>Shorefront jobs often need engineering, permitting and seasonal timing that estimates leave out.</li>
<li>Cedar shingle siding and trim on older cottages are hard to match after partial damage.</li>
<li>Mill repairs involve masonry, tall ceilings, large windows and lift access.</li>
<li>After a regional storm, York County contractors book out for months, which raises prices.</li>
</ul>
<p>Mill-era duplexes and tenements downtown add another layer. Many still heat with oil, share plumbing between units, and have plaster walls under later paneling. A frozen pipe or puffback in one of these buildings spreads into several apartments, and the estimate has to follow it. Owners at Biddeford Pool and Hills Beach often have seasonal homes that sit empty in winter, where freeze-ups raise vacancy questions under the policy.</p>
<p>The May 2006 Mother’s Day flood is another reminder that inland water can be as costly as the surf. Whatever the cause, a Biddeford insurance appraiser can only resolve the amount of loss. Coverage questions and policy deadlines belong with a Maine attorney.</p>
""",
        "faqs": [
            ("My Fortunes Rocks home was hit by storms in January and March 2024. How do I keep the claims straight?", "Use dated photos, contractor notes and any carrier inspection reports for each storm. Clear records make it easier to show which damage came from which event and under which claim."),
            ("Does appraisal apply to a mill condo water loss in Biddeford?", "Yes, once the policies establish who covers which part of the building. The association’s master policy and the unit owner’s policy each have their own appraisal clauses."),
            ("Is wave damage to my Biddeford Pool cottage covered under homeowners insurance?", "Wave wash and surge are usually treated as flood and excluded. Wind damage to the roof and siding is often covered, so review both your homeowners and flood policies."),
        ],
    },
    # ------------------------------------------------------------------ Brunswick
    {
        "slug": "brunswick-maine",
        "city": "Brunswick",
        "county": "Cumberland County",
        "region": "Midcoast",
        "perils": ["Fallen pines", "Ice dams", "Coastal wind", "Puffback soot"],
        "near": ["lewiston-maine", "portland-maine", "scarborough-maine"],
        "neighborhoods": ["Downtown Maine Street", "Bowdoin College area", "Mere Point", "Pennellville", "Cook’s Corner", "Brunswick Landing", "Topsham"],
        "housing": "Federal and Greek Revival homes near Maine Street and the college, connected farmhouses and capes on the rural roads, shorefront homes on Mere Point and Maquoit Bay, and newer housing on the former naval air station at Brunswick Landing.",
        "storms": [
            ("Oct 2017", "October windstorm", "Record statewide outages; tall pines snapped onto roofs and lines across the Midcoast."),
            ("Jan 2024", "Back-to-back coastal storms", "Record tides damaged wharves and shore roads in neighboring Harpswell and around Casco Bay."),
            ("Jan 1998", "Ice Storm of 1998", "Heavy ice brought down trees and power lines across southern and central Maine for days."),
        ],
        "title": "Brunswick, Maine Insurance Appraiser | Claim Help",
        "desc": "Independent appraisal for Brunswick and Cumberland County homeowners whose tree, wind, ice dam or puffback claim came in too low.",
        "lede": "Brunswick’s historic Maine Street homes, wooded rural roads and Casco Bay shorefront each bring their own claim problems. We review carrier estimates for homes and businesses and serve as appraiser when the amount is disputed.",
        "body": """<h2>Old houses, tall trees</h2>
<p>Brunswick, at the northern edge of Cumberland County, is where many people say the Midcoast begins. Around the Bowdoin College campus and along Maine Street, the housing is old: Federal and Greek Revival homes with plaster walls, original trim and multi-pane windows. Out on the rural roads, connected farmhouses sit under tall white pines. Many of the Brunswick claims we hear about start with one of those trees.</p>
<p>When the October 2017 windstorm swept through, it caused record power outages statewide, and Midcoast towns were left with snapped pines across roofs, porches and ells. Tree claims look simple until you add crane time, removal limits, and the hidden framing damage that only shows once the trunk is gone. An insurance appraiser in Brunswick looks at all of it. Our <a href="/appraisal-work/fallen-tree-limb-appraisal/">fallen tree and limb appraisal</a> page explains how those claims break down.</p>
<h2>The connected farmhouse problem</h2>
<p>“Big house, little house, back house, barn.” Brunswick has plenty of these connected buildings, and they complicate claims. A roof collapse in the ell can damage the main house; snow sliding off one roof can tear gutters and trim off another. Carriers sometimes treat outbuildings and attached structures under different coverage parts, which affects limits. The policy decides that question. The estimate still needs to capture each building correctly.</p>
<h2>Shorefront and the bay</h2>
<p>Mere Point, Maquoit Bay and the shore roads toward Harpswell face Casco Bay. The January 2024 storms brought record tides, damaging wharves and shore roads in neighboring Harpswell. Surge and wave damage are flood and typically excluded under homeowners policies, but wind damage to roofs and siding is usually part of the property claim.</p>
<h2>Heat, oil and winter</h2>
<p>Many older Brunswick homes still heat with oil, and a burner puffback can coat every room in fine soot. The Ice Storm of January 1998 showed what long outages do: frozen pipes and water damage followed in homes that lost heat. Before cleanup, read our <a href="/owner-guides/oil-burner-puffback-documentation/">puffback documentation guide</a>.</p>
<h3>What we look for</h3>
<ul>
<li>Plaster, original trim and old windows on Maine Street homes priced as modern materials.</li>
<li>Framing and ell damage hidden under a fallen tree.</li>
<li>Cleaning scopes that skip closets, ducts and contents after puffback.</li>
<li>Newer Brunswick Landing homes where matching siding and roofing still matter.</li>
</ul>
<p>Brunswick Landing adds a newer layer to the town’s housing. Homes and commercial buildings on the former naval air station are recent construction, but newer does not mean simple: siding, roofing and window lines can be discontinued within a few years, and partial repairs raise the same matching questions as an old cape. Topsham, across the Androscoggin, shares much of the same mix of older village homes and newer subdivisions.</p>
<p>A Brunswick insurance appraiser resolves the amount of loss, not coverage. For coverage disputes or deadline questions, consult a Maine attorney.</p>
""",
        "faqs": [
            ("A pine fell on my Brunswick farmhouse ell. Is the whole connected building one claim?", "It often is, but policies can treat attached and detached structures differently. Your policy language decides coverage, and the estimate should capture damage to each part of the building."),
            ("Does the carrier have to pay for crane time to remove a tree from my roof?", "Many policies cover reasonable debris and tree removal tied to covered damage, sometimes with limits. Read your policy, and make sure the estimate reflects the equipment actually needed."),
            ("Can appraisal help with a puffback claim in an older Brunswick home?", "Yes, if the dispute is about the amount. Appraisers can look at whether cleaning, repainting and contents work were scoped for the whole home."),
        ],
    },
    # ------------------------------------------------------------------ Scarborough
    {
        "slug": "scarborough-maine",
        "city": "Scarborough",
        "county": "Cumberland County",
        "region": "Greater Portland & Casco Bay",
        "perils": ["Marsh and surge water", "Shorefront wind", "Ice dams", "Condo water losses"],
        "near": ["portland-maine", "biddeford-maine", "sanford-maine"],
        "neighborhoods": ["Pine Point", "Higgins Beach", "Prouts Neck", "Blue Point", "Oak Hill", "Dunstan", "Scarborough Marsh"],
        "housing": "Shingle-style summer homes on Prouts Neck, cottages and year-round homes at Pine Point and Higgins Beach, colonials and capes in newer subdivisions, and a large stock of condos and townhouse associations near Oak Hill and Route 1.",
        "storms": [
            ("Jan 2024", "Back-to-back coastal storms", "Surge closed every road to Pine Point; crews pumped over a million gallons of sea and marsh water."),
            ("Feb 1978", "Blizzard of 1978", "Portland-gauge record tide of 14.17 ft drove surge into low-lying Casco Bay shorefronts."),
            ("Oct 2017", "October windstorm", "Record statewide outages; trees and limbs down across Scarborough’s wooded subdivisions."),
        ],
        "title": "Scarborough, Maine Insurance Appraiser | Claims",
        "desc": "Scarborough, Cumberland County claim appraisal for shorefront homes, condos and subdivisions. Independent review of underpaid property claims.",
        "lede": "Scarborough’s claims range from Pine Point surge and Higgins Beach wind to condo water losses near Oak Hill. We review carrier estimates for owners and associations and serve as appraiser when the amount is in dispute.",
        "body": """<h2>The marsh, the beaches and everything between</h2>
<p>Scarborough wraps around the largest salt marsh in the state, and its housing follows the water. Pine Point, Blue Point and Higgins Beach are dense with cottages and year-round homes close to the dunes. Prouts Neck holds large shingle-style summer houses. Inland, Oak Hill and Dunstan have colonials, capes and a growing number of condo and townhouse associations along the Route 1 corridor. A Scarborough insurance appraiser sees every type of Cumberland County claim inside a single town.</p>
<h2>January 2024 on Pine Point and Higgins Beach</h2>
<p>When the January 13, 2024 storm drove the Portland gauge to a new record, Scarborough’s coastal neighborhoods took moderate to significant damage. Every road to Pine Point closed, and town crews pumped more than a million gallons of sea and marsh water. Higgins Beach homes were battered by surf. The Blizzard of 1978, which set the previous tide record, is the only storm many residents compare it to.</p>
<div class="note"><b class="h">Flood versus wind</b><p>Surge and marsh flooding are excluded under homeowners policies and belong to flood coverage. Wind-torn roofing, broken windows and wind-driven rain are usually property claims. Document each separately, with dated photos, before repairs begin.</p></div>
<p>Our guide to <a href="/owner-guides/noreaster-wind-versus-flood-maine/">nor’easter wind versus flood in Maine</a> covers how to sort a mixed loss.</p>
<h2>Condo and association claims</h2>
<p>Many Scarborough residents live in associations, where a roof leak or burst pipe triggers both the master policy and individual unit-owner policies. The association documents and policies decide who pays which part; disputes over the amount can then go to appraisal under each policy. Ice dams on long townhouse rooflines are a regular winter source of these claims. See our <a href="/appraisal-work/commercial-condo-association-appraisal/">condo association appraisal</a> page.</p>
<h2>Pricing what Scarborough repairs really cost</h2>
<ul>
<li>Shorefront work that needs permits and seasonal timing near dunes and marsh.</li>
<li>Cedar shingle siding and trim on Prouts Neck and beach cottages.</li>
<li>Matching siding and roofing across attached townhouse units.</li>
<li>Contractor scarcity after a regional storm, when every Casco Bay town needs the same trades.</li>
</ul>
<p>Prouts Neck and the larger shorefront homes bring their own issues: custom millwork, cedar shingle exteriors, high-end finishes and long lead times for materials. Carrier estimates built on standard grades often miss the quality of what was there. On the other end, Oak Hill and Dunstan subdivisions face ice dams, wind-damaged siding and fallen trees, and the questions there usually turn on matching and the full scope of interior damage.</p>
<p>The October 2017 windstorm, with record outages statewide, also brought trees and limbs down across Scarborough’s wooded subdivisions. Whether the loss is wind, water or ice, an insurance appraiser in Scarborough can help only on the amount of loss. For coverage disputes and policy deadlines, consult a Maine attorney.</p>
""",
        "faqs": [
            ("Is Pine Point surge damage from January 2024 covered by my homeowners policy?", "Surge and marsh flooding are generally excluded and fall under flood insurance. Wind damage to the roof, siding or windows from the same storm is usually handled under the homeowners policy."),
            ("My Scarborough condo leak involves the association and my own policy. Where do I start?", "Start with the association’s documents and both policies to see who covers which part. Once that is clear, disputes over the amount can go to appraisal under the relevant policy."),
            ("Can appraisal address matching siding on attached townhouse units?", "It can address the amount needed to make a reasonable repair, including matching where your policy and Maine practice support it. Coverage questions about matching are for the policy and a Maine attorney."),
        ],
    },
    # ------------------------------------------------------------------ Waterville
    {
        "slug": "waterville-maine",
        "city": "Waterville",
        "county": "Kennebec County",
        "region": "Central Maine & the Kennebec Valley",
        "perils": ["Frozen pipes", "Ice dams", "Windstorm trees", "Puffback soot"],
        "near": ["augusta-maine", "rockland-maine", "lewiston-maine"],
        "neighborhoods": ["Downtown Main Street", "South End", "North End", "Mayflower Hill", "Hathaway Creative Center area", "Winslow", "Oakland"],
        "housing": "Franco-American tenements and duplexes in the South End, Victorian homes in the North End and near downtown, brick mill buildings like the Hathaway shirt factory reused for apartments and offices, and capes and ranches toward Oakland.",
        "storms": [
            ("Dec 2023", "December 18 storm", "Kennebec breached its banks; the Hathaway Creative Center lot flooded and residents were evacuated."),
            ("Apr 1987", "April 1987 floods", "Major Kennebec flood swamped riverfront land from Waterville and Winslow downstream."),
            ("Jan 1998", "Ice Storm of 1998", "Ice-laden trees and lines fell across the Kennebec Valley; many homes lost heat for days."),
        ],
        "title": "Insurance Appraiser Waterville, Maine | Estimates",
        "desc": "Waterville and Kennebec County homeowners: an independent appraiser for underpaid frozen pipe, ice dam, puffback and windstorm claims.",
        "lede": "Waterville’s South End tenements, North End Victorians and converted mills make for claims that standard estimates rarely capture. We review the numbers and act as appraiser when the amount is disputed.",
        "body": """<h2>What claims look like in Waterville</h2>
<p>Waterville sits on the Kennebec in northern Kennebec County, across the river from Winslow. Its housing reflects its mill-town past. The South End, long the heart of the city’s Franco-American community, is full of wood-frame tenements and duplexes. The North End and the streets near downtown hold larger Victorian homes. The Hathaway shirt factory, a brick mill on the river, now houses apartments and offices. Each of those building types turns a winter loss into a different kind of claim.</p>
<p>Most of what a Waterville insurance appraiser sees is winter: frozen pipes, ice dams on older capes, and puffbacks from oil burners. Wind and fallen trees round out the list.</p>
<h2>River years</h2>
<p>On December 18, 2023, the Kennebec breached its banks from Waterville downstream. The parking lot at the Hathaway Creative Center went under, cars were lost, and residents were evacuated. The April 1987 floods did similar damage along the river. River flooding is excluded under homeowners and most property policies, but that December storm also produced wind damage, fallen trees and outages across the area that were property claims.</p>
<p>The Ice Storm of January 1998 is the outage everyone still measures against. Days without heat in January meant split pipes and flooded basements, and those water losses often cost more than the tree damage that started them.</p>
<h2>Tenements, mills and the estimate gap</h2>
<p>Multi-unit buildings in the South End share plumbing, heating and roofs. A frozen pipe on the top floor travels down through every unit; a puffback spreads soot through every apartment on the same system. Carrier estimates often scope only the obvious rooms. We follow the damage through the building and price plaster, old trim and code upgrades where the policy covers them. For winter roof losses, see our <a href="/appraisal-work/ice-dam-snow-load-appraisal/">ice dam and snow load appraisal</a> page.</p>
<h3>Camps and second homes</h3>
<p>Many Waterville-area owners also have camps on nearby lakes. Freeze losses in a vacant camp raise policy questions about vacancy and heat. Our <a href="/owner-guides/seasonal-camp-vacancy-freeze-claims/">seasonal camp freeze claims guide</a> walks through the usual policy terms.</p>
<h2>Our Waterville inspection checklist</h2>
<ul>
<li>Every unit and stairwell touched by water or soot.</li>
<li>Plaster ceilings, wood lath and old wiring exposed during repairs.</li>
<li>Oil tank, burner and chimney condition documented for puffback claims.</li>
<li>Tree removal and roof framing damage after windstorms.</li>
</ul>
<p>Mayflower Hill and the newer neighborhoods toward Oakland have more modern construction, but the same winter perils apply. Ice dams form on low-slope roofs and over poorly ventilated attics, and the water often shows up in a closet ceiling weeks after the dam formed. Carriers may question timing, so good photos of the roof edge and ice buildup help tie the damage to a single winter event.</p>
<p>An insurance appraiser in Waterville can resolve disagreements over the amount of loss. Coverage questions and policy deadlines belong with a Maine attorney.</p>
""",
        "faqs": [
            ("My South End rental had a frozen pipe that damaged three apartments. Is that one claim?", "Usually it is one loss under the building owner’s policy, covering all units affected by the same pipe break. Tenant belongings are generally covered by each tenant’s own renters policy."),
            ("Was flooding at the Hathaway lot in December 2023 a homeowners claim?", "River flooding is generally excluded under homeowners policies, and flood damage to buildings typically requires a separate flood policy. Flooded cars are a separate question under each owner’s auto policy."),
            ("Does a camp freeze-up qualify for appraisal?", "If the carrier accepts the claim but you disagree on the amount, appraisal may apply. If it denies coverage for vacancy or lack of heat, that is a coverage question for your policy and a Maine attorney."),
        ],
    },
    # ------------------------------------------------------------------ Rockland
    {
        "slug": "rockland-maine",
        "city": "Rockland",
        "county": "Knox County",
        "region": "Midcoast",
        "perils": ["Harbor storm surge", "Nor’easter wind", "Ice dams", "Fallen trees"],
        "near": ["augusta-maine", "waterville-maine", "brunswick-maine"],
        "neighborhoods": ["Downtown Main Street", "South End", "North End", "Jameson Point", "Owls Head", "Thomaston"],
        "housing": "Nineteenth-century brick commercial blocks on Main Street, wood-frame Greek Revival and Victorian homes in the South End and North End, waterfront condos near Jameson Point, and capes and farmhouses toward Owls Head and Thomaston.",
        "storms": [
            ("Jan 2024", "Back-to-back coastal storms", "Flooded the Public Landing to levels few had seen and wrecked a pier at a Rockland marina."),
            ("Oct 2017", "October windstorm", "Record statewide outages; trees down on homes and lines across Knox County."),
            ("Feb 1976", "Groundhog Day Gale", "Hurricane-force gusts and surge struck Penobscot Bay; worst flooding came upriver in Bangor."),
        ],
        "title": "Rockland, Maine Insurance Appraiser | Midcoast Claims",
        "desc": "Rockland and Knox County claim appraisal for harborfront, downtown and island property. Independent review when the carrier pays too little.",
        "lede": "Rockland’s working harbor, brick Main Street and ferry links to the islands make for claims with real access and timing costs. We review carrier estimates for Knox County owners and serve as appraiser when the amount is disputed.",
        "body": """<h2>A harbor city’s claims</h2>
<p>Rockland is the Knox County seat and one of the Midcoast’s busiest working harbors. Main Street’s brick blocks face the water, the South End and North End hold wood-frame Greek Revival and Victorian homes, and condos near Jameson Point look out over the breakwater. A Rockland insurance appraiser deals with harborfront exposure, old downtown buildings and the logistics of the islands, often in the same week.</p>
<h2>January 2024 at the waterfront</h2>
<p>The January 10, 2024 storm flooded Rockland’s Public Landing to a level many residents had never seen, and storm surge wrecked a pier at a local marina. The January 13 storm followed with another record tide along the coast, and the keeper’s house on the Rockland Breakwater was damaged. For harborfront owners, these storms produced both flood damage, which homeowners and most commercial property policies exclude, and wind damage to roofs, siding and windows, which property policies usually cover.</p>
<p>Docks, piers and floats are a separate question. Many policies limit or exclude them, and the policy language controls. Where they are covered, pricing marine work in winter is its own specialty.</p>
<h2>Island and access pricing</h2>
<p>Rockland is the ferry terminal for Vinalhaven, North Haven and Matinicus, and many Knox County homeowners have island property. Repairs out there mean ferry reservations, barged materials, crews who stay overnight and short working windows. Carrier estimates built on mainland unit prices leave those costs out. An insurance appraiser in Rockland should include them in the amount of loss, because they are part of what it takes to make the repair. Our <a href="/appraisal-work/carrier-estimate-line-review/">carrier estimate line review</a> is a good first step when you suspect access costs are missing.</p>
<h2>Downtown buildings and old homes</h2>
<ul>
<li>Brick parapets, cornices and flat roofs on Main Street blocks after wind and snow.</li>
<li>Plaster, old trim and original windows in South End and North End homes.</li>
<li>Ice dams on low-slope additions and connected barns.</li>
<li>Tree damage on wooded lots toward Owls Head and Thomaston, where the October 2017 windstorm left many without power.</li>
</ul>
<h3>Older storms still shape expectations</h3>
<p>The Groundhog Day Gale of February 2, 1976, struck Penobscot Bay with hurricane-force gusts and surge, though its worst flooding came upriver at Bangor. Long-time owners remember it alongside 2024.</p>
<p>Rockland’s brick downtown also brings fire exposure. Many Main Street buildings share party walls, so smoke and water from a fire in one block can reach its neighbors. Restaurants, galleries and shops stacked beside and above each other mean business income, inventory and tenant improvements all come into the claim. Estimates need to account for masonry, old timber framing and the cost of working on a busy street.</p>
<p>For coastal storm claims, see our <a href="/appraisal-work/noreaster-hurricane-appraisal/">nor’easter and hurricane appraisal</a> page. Appraisal resolves only the amount of loss. For coverage questions or deadlines, consult a Maine attorney.</p>
""",
        "faqs": [
            ("Are docks and floats covered after a storm like January 2024?", "It depends on your policy. Many homeowners and commercial policies limit or exclude docks, piers and floats, so read the property definitions and exclusions carefully."),
            ("Can appraisal include ferry and barge costs for a Vinalhaven repair?", "Yes, if the dispute is over the amount of a covered loss. Ferry fares, barging materials and crew lodging are real repair costs that belong in the estimate."),
            ("My Main Street building had wind and water damage. Is that one claim or two?", "Wind and rain damage are usually property claims, while surge or flood water is typically excluded and handled by flood coverage. Document each type separately with dated photos."),
        ],
    },
    # ------------------------------------------------------------------ Bar Harbor
    {
        "slug": "bar-harbor-maine",
        "city": "Bar Harbor",
        "county": "Hancock County",
        "region": "Down East & Acadia",
        "perils": ["Shorefront surge", "Post-tropical wind", "Seasonal freeze-ups", "Fallen spruce"],
        "near": ["bangor-maine", "rockland-maine", "waterville-maine"],
        "neighborhoods": ["Downtown", "West Street", "Hulls Cove", "Town Hill", "Salisbury Cove", "Otter Creek", "Hadley Point"],
        "housing": "Shingle-style cottages and inns from the summer-colony era, wood-frame homes and small hotels downtown, year-round houses in Town Hill and Hulls Cove, and many seasonal homes and rentals left vacant through the winter.",
        "storms": [
            ("Jan 2024", "Back-to-back coastal storms", "Water topped the town pier, tore a hole in the Bar Harbor Inn pier and damaged the Shore Path."),
            ("Sep 2023", "Post-tropical Storm Lee", "Strong winds downed trees and lines Down East, leaving much of Mount Desert Island without power."),
            ("Oct 1947", "Great Fire of 1947", "Wildfire burned much of eastern Mount Desert Island, destroying many of Bar Harbor’s grand cottages."),
        ],
        "title": "Bar Harbor, Maine Insurance Appraiser | Acadia Claims",
        "desc": "Bar Harbor and Hancock County claim appraisal for cottages, inns and seasonal homes. Independent review of underpaid storm and freeze claims.",
        "lede": "Bar Harbor’s summer cottages, inns and seasonal homes face surge, Down East wind and winter freeze-ups while owners are away. We review carrier estimates and act as appraiser when the amount is in dispute.",
        "body": """<h2>Seasonal property, year-round risk</h2>
<p>A large share of Bar Harbor’s buildings sit empty from late fall to spring. Shingle-style cottages, inns, small hotels and vacation rentals close up when the cruise ships and park visitors leave, and that is when Hancock County’s weather does its work. Pipes freeze, roofs leak under snow and ice, and nobody sees the damage until weeks later. An insurance appraiser in Bar Harbor deals with timing questions as often as pricing ones.</p>
<p>Vacancy and unoccupancy terms in your policy can limit or exclude some of these losses, particularly freezing if heat was not maintained. Our <a href="/claim-math/seasonal-camp-vacancy-check/">seasonal camp and second-home vacancy check</a> helps you see how your policy terms may apply before you file.</p>
<h2>Storms Down East</h2>
<p>The January 10 and 13, 2024 storms put a foot or two of water over the town pier, tore a hole in the Bar Harbor Inn pier, and damaged the Shore Path that runs along the water. In September 2023, post-tropical storm Lee brought strong winds Down East, bringing down spruce and fir across Mount Desert Island and knocking out power to much of the island.</p>
<p>Surge and wave damage are flood, generally excluded under homeowners and commercial property policies. Wind damage to roofs, siding and windows from those same storms is usually a property claim. The distinction matters most for waterfront owners along the Shore Path, Hulls Cove and Hadley Point.</p>
<h2>Building after 1947</h2>
<p>The Great Fire of October 1947 burned much of eastern Mount Desert Island, including many of the grand summer cottages along Bar Harbor’s shore. What survived, and what was rebuilt, gives the town an unusual mix of old shingle-style buildings and mid-century construction. For fire, smoke and puffback losses, see our <a href="/appraisal-work/fire-smoke-puffback-appraisal/">fire, smoke and puffback appraisal</a> page.</p>
<h2>Pricing realities on the island</h2>
<ul>
<li>Short construction season, with contractors booked solid before and during tourist months.</li>
<li>Travel time and lodging for off-island trades.</li>
<li>Cedar shingle roofs and siding on older cottages that are hard to match.</li>
<li>Lost business income for inns and rentals, where the policy covers it.</li>
<li>Winter work on exposed sites in Salisbury Cove, Town Hill and Otter Creek.</li>
</ul>
<p>Downtown and West Street hold many older wood-frame inns and homes with tight lot lines, where a fire or a fallen tree can affect neighbors. Repairs on narrow streets during tourist season can mean limited hours, parking and staging problems, and permit timing. Year-round homes in Town Hill and Hulls Cove face more familiar Maine losses: ice dams, frozen pipes and wind damage to roofs and siding.</p>
<p>A Bar Harbor insurance appraiser should account for all of these when setting the amount of loss. Appraisal does not decide coverage questions like vacancy or flood exclusions; for those, and for policy deadlines, consult a Maine attorney.</p>
""",
        "faqs": [
            ("My Bar Harbor rental froze while closed for winter. Is that covered?", "It depends on your policy’s vacancy, unoccupancy and heat maintenance terms. Some policies limit freezing losses if heat was not kept on or water was not shut off, so read those sections first."),
            ("Can appraisal include lost income for an inn damaged in a storm?", "If your policy includes business income coverage and the carrier accepts the claim, disputes over the amount of lost income can often go to appraisal. Check your policy’s appraisal clause."),
            ("Does Down East repair pricing really differ from southern Maine?", "Often yes. Fewer contractors, off-island travel and a short building season can raise costs, and a fair estimate should reflect local conditions."),
        ],
    },
    # ------------------------------------------------------------------ Presque Isle
    {
        "slug": "presque-isle-maine",
        "city": "Presque Isle",
        "county": "Aroostook County",
        "region": "The County (Aroostook)",
        "perils": ["Snow load collapse", "Ice dams", "Frozen pipes", "Farm building wind"],
        "near": ["bangor-maine", "bar-harbor-maine", "waterville-maine"],
        "neighborhoods": ["Downtown Main Street", "UMPI campus area", "Chapman", "Mapleton", "Easton", "Westfield"],
        "housing": "Capes, ranches and two-story farmhouses in town, older wood-frame homes near downtown, and potato storage houses, pole barns and metal farm buildings across the surrounding farmland.",
        "storms": [
            ("Mar 2008", "Record snow winter", "Heavy snow and rain loaded roofs; buildings collapsed in Presque Isle and nearby County towns."),
            ("Apr 2008", "Spring flood", "Snowmelt and rain flooded northern Maine rivers; the worst damage came at Fort Kent."),
            ("Dec 1973", "Aroostook River flood", "Rare winter flood on the Aroostook damaged homes and camps along the river near Presque Isle."),
        ],
        "title": "Presque Isle, Maine Insurance Appraiser | The County",
        "desc": "Presque Isle and Aroostook County appraisal for snow load, ice dam and farm building claims. Independent review when the carrier pays too little.",
        "lede": "In Presque Isle, snow load, deep cold and farm buildings drive most claims. We review carrier estimates for homes, potato storage houses and businesses across Aroostook County, and serve as appraiser when needed.",
        "body": """<h2>Snow load is the headline</h2>
<p>Presque Isle gets some of the heaviest snow in New England, and the winter of 2007 to 2008 showed what that means for buildings. Nearby Caribou set a seasonal snowfall record, and in March 2008 heavy snow followed by rain loaded roofs across Aroostook County. Buildings collapsed in Presque Isle and other County towns, and city crews shoveled public roofs to head off more damage. An insurance appraiser in Presque Isle sees snow load claims nearly every winter, and the big years produce disputes over whether the damage was collapse, wear or poor maintenance.</p>
<p>Policies treat collapse in specific ways, and the definitions matter. The policy decides coverage; the estimate still has to capture shoring, framing and the cost of working in deep snow. Our <a href="/appraisal-work/ice-dam-snow-load-appraisal/">ice dam and snow load appraisal</a> page explains our approach.</p>
<h2>Farm buildings and The County economy</h2>
<p>Potato storage houses, pole barns and metal machine sheds dot the land around Presque Isle, Mapleton, Easton and Westfield. Their repair costs bear little resemblance to a house. Storage buildings may carry specialized insulation, ventilation and climate control, and a roof or wall failure can also put stored crops at risk if the policy covers them. Carrier software often prices these structures as generic outbuildings.</p>
<ul>
<li>Metal roofing and wall panels that must match existing profiles.</li>
<li>Insulation and ventilation systems in storage houses.</li>
<li>Engineering and permitting for structural repairs.</li>
<li>Equipment rental and access across snowbound farm lanes.</li>
</ul>
<h2>Homes in deep cold</h2>
<p>Presque Isle homes are mostly capes, ranches and farmhouses, many heated with oil or wood. Frozen pipes, ice dams and chimney fires are the common losses. A furnace failure at minus 20 can freeze a house in hours. Wood stove and chimney fires bring smoke damage that spreads further than it first appears.</p>
<h2>Rivers and spring melt</h2>
<p>Spring melt is its own season in The County. The April and May 2008 flood swamped northern Maine rivers, with the worst damage at Fort Kent, and the Aroostook River has flooded homes and camps near Presque Isle before, including in December 1973. River flooding is excluded under homeowners policies and requires separate flood coverage.</p>
<h2>Distance and timing</h2>
<p>Commercial buildings along Main Street and the businesses that serve the farm economy face the same snow and cold. Flat and low-slope roofs collect drifts, and rooftop equipment adds weight. When a roof sags or leaks, the estimate needs to account for snow removal, interior damage, inventory and the cost of working in winter.</p>
<p>Contractors are scarce and the building season is short this far north. Estimates that ignore travel, winter conditions and the wait for trades often come up short. A Presque Isle insurance appraiser should account for those realities. Start with our <a href="/claim-math/appraisal-file-strength-test/">appraisal file strength test</a> to see how ready your claim is. For coverage questions or deadlines, consult a Maine attorney.</p>
""",
        "faqs": [
            ("My potato storage roof collapsed under snow. Will appraisal cover the building and the crop?", "Appraisal sets the amount of covered loss only. Whether the building and stored crops are covered depends on your farm or commercial policy, so read the collapse and property sections first."),
            ("Why would a carrier say snow load damage is wear and tear?", "Carriers sometimes argue a roof failed from age or poor maintenance rather than the weight of snow. Photos, snow depth records and contractor findings help show what actually happened."),
            ("Can appraisal include travel costs for contractors coming to Presque Isle?", "Yes, when those costs are a real part of the repair. Travel and lodging for trades are common in The County and belong in a fair estimate."),
        ],
    },
    # ------------------------------------------------------------------ Sanford
    {
        "slug": "sanford-maine",
        "city": "Sanford",
        "county": "York County",
        "region": "Southern Coast",
        "perils": ["Summer hail", "Ice storm trees", "Mill building water", "Frozen pipes"],
        "near": ["biddeford-maine", "scarborough-maine", "portland-maine"],
        "neighborhoods": ["Downtown Sanford", "Springvale", "South Sanford", "Number One Pond", "Bauneg Beg Lake area", "Alfred"],
        "housing": "Brick textile mills along the Mousam River in Sanford and Springvale, many converted to apartments, older wood-frame duplexes and tenements near downtown, capes and ranches in South Sanford, and seasonal camps on nearby lakes.",
        "storms": [
            ("Jul 2020", "York County hailstorm", "Thunderstorms dropped hail and downed trees; hail damaged vehicles at a Sanford dealership."),
            ("Mar 2024", "Late-March ice storm", "Ice brought down trees and wires across York County, including along Route 4 in Sanford."),
            ("May 2006", "Mother’s Day flood", "Heavy rain sent the Mousam River and other York County streams into widespread flooding."),
        ],
        "title": "Insurance Appraiser Sanford, Maine | Claim Review",
        "desc": "Sanford and Springvale property claims reviewed by an independent appraiser. Hail, ice storm and water losses across York County, explained.",
        "lede": "Sanford’s mills, Springvale tenements and lakeside camps face hail, ice storms and winter water losses. We review carrier estimates across the Sanford area and serve as appraiser when the amount of loss is in dispute.",
        "body": """<h2>Inland York County is not the coast</h2>
<p>Sanford sits inland in western York County, and its weather and claims differ from the beach towns. Summer thunderstorms here can bring hail, which is uncommon on the coast. Ice storms hit harder when cold air settles in the valley. The housing is different too: brick mills on the Mousam River in Sanford and Springvale, wood-frame duplexes near downtown, capes and ranches in South Sanford, and camps on lakes like Number One Pond and Bauneg Beg. An insurance appraiser in Sanford needs to understand all of it.</p>
<h2>Hail, ice and water</h2>
<h3>July 2020 hail</h3>
<p>On July 14, 2020, powerful thunderstorms crossed York County, dropping hail and knocking down trees. Vehicles at a Sanford dealership were damaged by hail. Roofs, siding and gutters in the storm’s path took hits too. Hail claims in Maine are less common, so carriers sometimes question whether marks on shingles are hail or wear. Our <a href="/appraisal-work/roof-hail-loss-appraisal/">roof and hail loss appraisal</a> page explains what we document.</p>
<h3>March 2024 ice storm</h3>
<p>In late March 2024, freezing rain coated York County, bringing down trees and wires across the region, including along Route 4 in Sanford. Tree claims that follow ice storms often involve removal limits, framing damage and roofing that cannot be matched.</p>
<h3>Rivers and the 2006 flood</h3>
<p>The May 2006 Mother’s Day flood sent the Mousam River and other York County streams into widespread flooding. River flooding is excluded under homeowners policies; separate flood coverage applies.</p>
<h2>The mills and the multi-family stock</h2>
<p>Sanford’s and Springvale’s mill buildings are large brick structures with heavy timber floors, now home to apartments and businesses. A sprinkler or pipe failure on an upper floor can affect several units. Near downtown, duplexes and tenements share plumbing and heat, so a frozen pipe or puffback spreads. Estimates need to follow the damage through the whole building.</p>
<h2>What a Sanford insurance appraiser checks</h2>
<ul>
<li>Hail marks on roofing, siding, gutters and window wraps, documented promptly.</li>
<li>Tree removal and hidden framing damage after ice storms.</li>
<li>Water spread through multi-unit buildings.</li>
<li>Camp freeze-ups, where vacancy and heat terms in the policy matter.</li>
</ul>
<p>Camps around Number One Pond, Bauneg Beg and the lakes beyond often sit empty in winter. Freeze-ups there can go unnoticed for weeks, and policies may limit coverage if heat was not maintained or water was not shut off. When coverage is accepted, the dispute usually turns on how far the water spread and what it costs to repair camp construction properly.</p>
<p>Use our <a href="/claim-math/settlement-gap-projector/">settlement gap projector</a> to estimate whether the difference between your number and the carrier’s is worth pursuing. Appraisal resolves only the amount of loss. Coverage questions and policy deadlines belong with a Maine attorney.</p>
""",
        "faqs": [
            ("Does Sanford really get hail damage?", "It happens more often inland than on the coast. The July 2020 storm dropped hail in Sanford, damaging vehicles and property in its path."),
            ("My Springvale duplex had a frozen pipe that damaged both units. Is that one claim?", "Usually yes, under the building owner’s policy, since the same pipe break caused the damage. Tenants’ belongings are generally covered by their own renters policies."),
            ("Was Mousam River flooding covered by homeowners insurance?", "River flooding is generally excluded under homeowners policies. Flood damage to buildings typically requires a separate NFIP or private flood policy."),
        ],
    },
]
