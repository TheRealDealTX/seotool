"""North Carolina location pages. Each entry is written for its own market."""

LOCATIONS = [
    # ------------------------------------------------------------------ RALEIGH
    {
        "slug": "raleigh",
        "city": "Raleigh",
        "county": "Wake County",
        "region": "Triangle / Piedmont",
        "geo": "Raleigh",
        "title": "Raleigh Insurance Appraiser | Wake County Claims",
        "desc": "Independent insurance appraisal in Raleigh and Wake County: appraisal-clause appraiser, estimate review and umpire work for disputed claims.",
        "lede": "Raleigh’s oak canopy, plaster-walled older homes and fast-growing suburbs produce claims where the real fight is over price and scope. We value disputed property losses across Wake County.",
        "perils": ["Falling oaks", "Ice storms", "Spring tornadoes", "Hail bursts", "Winter pipe bursts"],
        "hoods": ["Oakwood", "Five Points", "Hayes Barton", "Boylan Heights", "Mordecai", "North Hills", "Glenwood-Brooklyn", "Brier Creek", "Wakefield"],
        "housing": "Raleigh mixes Victorian and craftsman homes in the historic core, mid-century ranches inside the Beltline and large HOA subdivisions and townhome communities toward Brier Creek, Wakefield and the county line.",
        "storms": [
            ("1996", "Hurricane Fran", "Fran’s winds brought down thousands of mature trees across Raleigh, crushing roofs and cutting power for days."),
            ("2000", "January snowstorm", "A surprise storm buried Raleigh under roughly 20 inches of snow, a local record that collapsed carports and porch roofs."),
            ("2002", "December ice storm", "Ice accumulation snapped limbs and power lines throughout Wake County, leaving much of the city without power."),
            ("2011", "April 16 tornado outbreak", "Tornadoes tracked across the Triangle that afternoon, with heavy damage in parts of Raleigh."),
        ],
        "near": ["cary", "durham", "fayetteville"],
        "body": """<h2>Why Raleigh losses rarely come down to one line item</h2>
<p>Raleigh calls itself the City of Oaks, and the name is earned. Willow oaks and red oaks planted along streets in Five Points, Hayes Barton and Oakwood have grown well above the rooflines they shade. When a summer squall line or an ice event comes through, a single limb can open a roof, break rafters, crush a porch and take out a fence on the same lot. Those claims are seldom denied outright. The disagreement is almost always about how much of the house was actually affected and what it costs to put it back.</p>
<p>The city’s growth adds a second layer. Contractors in Wake County have stayed busy for years, and after a regional event their schedules fill quickly. An estimate built on generic unit pricing can look reasonable on paper and still fall short of what local trades will actually charge to do the work.</p>
<h2>Housing stock that shapes the estimate</h2>
<p>Inside the Beltline, many homes date from the 1910s through the 1950s. Plaster over lath, original heart-pine floors, wood windows with true divided lites and slate or standing-seam roofs all show up regularly. Oakwood, Boylan Heights and other locally designated historic districts can require review before exterior materials are changed, which affects both scope and timeline.</p>
<p>Farther out, the issues change. In newer subdivisions near Brier Creek and Wakefield, the questions are usually about matching: whether a discontinued shingle color or a faded vinyl siding profile can be patched without an obvious mismatch, and whether a partial replacement leaves the home in a reasonably uniform condition. Townhome communities add the HOA master policy, which may cover the structure while the owner’s policy covers interiors and improvements.</p>
<h3>What we look at first</h3>
<ul>
<li>Whether plaster walls and ceilings were priced as drywall.</li>
<li>Roof decking, rafter repairs and framing hidden behind a tree strike.</li>
<li>Tree removal and crane costs on tight in-town lots.</li>
<li>Matching for siding, shingles and continuous flooring.</li>
<li>Code-related items and historic-district requirements left out of the scope.</li>
</ul>
<h2>Disputes we see most often in Wake County</h2>
<p>Many Raleigh appraisals start with a roof. One estimate calls for spot repairs; the other calls for replacement because brittle shingles cannot be lifted without breaking. Interior water losses are another frequent source of disagreement, especially in older homes where drying a plaster wall is a different job than cutting out and replacing gypsum board. Hail tends to come in narrow swaths here, so neighbors on the same street can end up with very different outcomes and very different estimates.</p>
<p>Appraisal is designed for exactly these amount-of-loss disagreements. When a policy contains an appraisal clause and either side invokes it, each party typically names its own appraiser, the two appraisers select an umpire, and a written award resolves the value of the loss. It does not decide whether a loss is covered; that remains between you and your insurer. We work as your appointed appraiser, as an umpire, or as an estimate reviewer before you decide whether appraisal makes sense at all.</p>
<h2>Where we work around the capital</h2>
<p>We handle Raleigh claims from Mordecai and Glenwood-Brooklyn to North Hills, Brier Creek and Wakefield, as well as surrounding Wake County towns such as Garner, Knightdale, Wake Forest and Holly Springs. If you are unsure whether your disagreement is a pricing question or a coverage question, a short call can usually sort that out.</p>""",
        "faqs": [
            ("Our Five Points home has plaster walls. Why does that matter in an appraisal?",
             "Plaster over lath is slower and more expensive to repair than drywall, and blending a patch into an old wall takes skilled labor. When an estimate prices plaster rooms as standard gypsum board, the gap can be significant. An appraiser documents the existing materials and prices the repair that the home actually requires."),
            ("A tree from my neighbor’s yard fell on my Raleigh house. Can appraisal still help?",
             "Often, yes. Your own homeowners policy usually responds to damage to your home regardless of whose tree it was. If your insurer accepts the claim but you disagree on the repair cost, including framing, roofing, interior damage and tree removal, appraisal may be available under your policy to settle the amount of the loss."),
            ("Does the HOA policy or my policy pay for storm damage to my Wake County townhome?",
             "It depends on the governing documents and both policies. Many townhome associations insure exterior elements such as roofs and siding, while owners insure interiors and upgrades, but arrangements vary. We review both estimates against what each policy is actually responding to before valuing the loss, so nothing is double counted or left out."),
        ],
    },
    # ------------------------------------------------------------------ CHARLOTTE
    {
        "slug": "charlotte",
        "city": "Charlotte",
        "county": "Mecklenburg County",
        "region": "Charlotte metro",
        "geo": "Charlotte",
        "title": "Charlotte Claim Appraisal | Mecklenburg County",
        "desc": "Disputed home or business claim in Charlotte? Independent appraisal-clause appraisers, estimate review and umpire services in Mecklenburg County.",
        "lede": "From Myers Park’s willow oaks to South End’s condo towers, Charlotte claims run the full range of property types. We help owners settle disputes over what a loss is actually worth.",
        "perils": ["Hailstorms", "Tree strikes", "Ice accumulation", "Straight-line winds", "Condo water leaks"],
        "hoods": ["Myers Park", "Dilworth", "Plaza Midwood", "NoDa", "Elizabeth", "South End", "Eastover", "Ballantyne", "University City"],
        "housing": "Charlotte pairs 1910s–1930s bungalows and colonial-revival homes in Dilworth, Myers Park and Elizabeth with mill houses in NoDa, mid-rise condos in Uptown and South End, and large suburban subdivisions toward Ballantyne and the county edges.",
        "storms": [
            ("1989", "Hurricane Hugo", "Hugo was still a strong storm when it reached Charlotte, toppling huge numbers of trees onto homes and leaving most of the city without power."),
            ("2002", "December ice storm", "Heavy ice brought down limbs and lines across Mecklenburg County and caused one of the largest power outages in the region’s history."),
        ],
        "near": ["greensboro", "winston-salem", "asheville"],
        "body": """<h2>A city built under a tree canopy</h2>
<p>Charlotte’s older neighborhoods were planted with willow oaks a century ago, and those trees now tower over Myers Park, Dilworth and Eastover. Residents who remember Hurricane Hugo in 1989 know what happens when an inland storm meets that canopy. The 2002 ice storm repeated the lesson in a different form. Today, a thunderstorm with strong straight-line winds can still drop a trunk across a roof, and those claims involve structure, interiors, landscaping and often a crane.</p>
<p>The metro also sees hail. Storms that build over the Piedmont in spring can lay down a swath of damage across one part of the county and miss another entirely. That creates a familiar argument: whether marks on a roof are new hail damage, older wear or something an adjuster considers cosmetic.</p>
<h2>From bungalows to towers: the property types we value</h2>
<p>Charlotte claims rarely fit a single pattern because the housing stock does not. In Dilworth and Elizabeth, craftsman bungalows and colonial-revival homes come with plaster, original millwork and older roofs that may not survive a partial repair. In NoDa and Plaza Midwood, former mill houses have been renovated many times, so the materials behind one wall can differ from the next.</p>
<p>Uptown and South End have added thousands of condominium units. In those buildings, a water loss that starts in one unit can travel through several floors. Sorting out what the association’s master policy covers and what falls to the unit owner’s HO-6 policy has to happen before the amount of loss can be settled. In the newer subdivisions toward Ballantyne, Steele Creek and University City, the questions are more likely to involve matching siding, roofing and flooring across large, uniform surfaces.</p>
<h2>Where Charlotte estimates tend to diverge</h2>
<ul>
<li>Hail damage to shingles, gutters and metal trim characterized as wear or cosmetic.</li>
<li>Partial roof or siding repairs that leave a visible mismatch.</li>
<li>Condo water losses split between master and unit-owner policies.</li>
<li>Plaster and custom trim in older homes priced as standard materials.</li>
<li>Tree removal, debris haul-off and crane costs on mature lots.</li>
<li>Business interruption or contents values on commercial claims.</li>
</ul>
<h3>How appraisal fits</h3>
<p>Appraisal addresses the amount of a loss, not whether it is covered. When a policy includes an appraisal provision and it is invoked, each side typically names an appraiser, the two choose an umpire, and an award signed by any two of the three sets the value. For a homeowner who has an accepted claim but an estimate that does not reflect the actual repair, it can be a faster and more focused path than a long back-and-forth. We serve as a party appraiser, as an umpire, or as an independent reviewer who tells you plainly whether the gap is worth pursuing.</p>
<h2>Mecklenburg County and nearby</h2>
<p>We work throughout Charlotte, from Myers Park and Eastover to NoDa, South End, Ballantyne and University City, and in surrounding communities including Matthews, Mint Hill, Huntersville, Cornelius and Pineville. Commercial owners with retail, office or multifamily properties can also use appraisal when a policy provides for it.</p>""",
        "faqs": [
            ("My South End condo was damaged by a leak from the unit above. Who handles the claim?",
             "Usually two policies are involved: the association’s master policy and your HO-6 unit-owner policy. Which one pays for drywall, cabinets, flooring and upgrades depends on the declarations and bylaws. Once responsibility is sorted out, appraisal may be available under the policy that covers your portion if you disagree on the amount."),
            ("My Charlotte roof had hail damage but the insurer said it is only cosmetic. Is that an appraisal issue?",
             "It can be part of one. Whether a cosmetic-damage exclusion applies is a coverage question, which appraisal does not decide. But when an insurer acknowledges some hail damage and the dispute is over how much of the roof needs repair or replacement, appraisal may be the right tool for valuing the loss."),
            ("Do you handle appraisals for commercial properties in Mecklenburg County?",
             "Yes. Many commercial property policies contain an appraisal clause similar to homeowners policies. We review building estimates for retail, office and multifamily properties and can serve as a party appraiser or umpire. Business income disputes are more complex and depend heavily on the policy wording and the records available."),
        ],
    },
    # ------------------------------------------------------------------ GREENSBORO
    {
        "slug": "greensboro",
        "city": "Greensboro",
        "county": "Guilford County",
        "region": "Triad",
        "geo": "Greensboro",
        "title": "Greensboro Insurance Appraiser for Disputed Claims",
        "desc": "Greensboro and Guilford County insurance appraisal: independent review of tornado, hail and water damage estimates, plus appraiser and umpire work.",
        "lede": "Greensboro sits squarely in the Triad’s path for spring tornadoes and summer hail, with housing that ranges from Fisher Park Victorians to east Greensboro brick ranches. We help settle what those losses are worth.",
        "perils": ["Spring tornadoes", "Hail swaths", "Downburst winds", "Ice storms", "Interior water"],
        "hoods": ["Fisher Park", "Irving Park", "Sunset Hills", "Westerwood", "Lindley Park", "Starmount", "College Hill", "Lake Jeanette", "Summerfield"],
        "housing": "Greensboro’s housing runs from Victorian and colonial-revival homes in Fisher Park and Irving Park to 1940s–1960s brick ranches in east and south Greensboro, student rentals near UNCG and North Carolina A&T, and newer subdivisions toward Summerfield.",
        "storms": [
            ("2018", "April 15 tornado", "An EF2 tornado cut across east Greensboro, damaging hundreds of homes and several schools along its path."),
            ("2002", "December ice storm", "The Piedmont-wide ice storm brought down limbs and power lines across the Triad and caused widespread outages."),
        ],
        "near": ["winston-salem", "durham", "charlotte"],
        "body": """<h2>Storm patterns in the Triad</h2>
<p>Greensboro sits in the middle of the Piedmont, where spring storm systems often organize into lines of severe thunderstorms. The April 2018 tornado that crossed east Greensboro is the event most residents remember, but straight-line winds and hail produce far more claims year to year. A downburst can flatten a row of fences and peel back shingles across a neighborhood without a tornado ever touching down.</p>
<p>The aftermath of a broad event matters as much as the storm. When many homes are damaged at once, roofers and framers book up, and an estimate written in the first week may not reflect what it actually costs to get the work done months later.</p>
<h2>How Greensboro’s housing shows up in estimates</h2>
<p>In Fisher Park, Irving Park and Westerwood, older homes have plaster walls, tall ceilings, original trim and wood windows. Fisher Park is a locally designated historic district, so exterior changes may require review, which affects scope and timing. Pricing those homes from a standard database often misses the labor involved in matching profiles and finishes.</p>
<p>East and south Greensboro have many mid-century brick ranches. Brick veneer cracked by a falling tree or wind-driven debris, older electrical and plumbing that must be brought up to current requirements during repairs, and original hardwood floors under carpet all show up in those claims. Near UNCG and North Carolina A&T, rental properties raise their own issues, including tenant-damaged contents and loss of rental income under landlord policies.</p>
<h3>Common sources of disagreement</h3>
<ul>
<li>Brick veneer repairs that ignore matching mortar and brick.</li>
<li>Roof repairs versus full replacement on older, brittle shingles.</li>
<li>Hardwood flooring replaced in one room when it runs continuously through several.</li>
<li>Code upgrade items triggered during repair.</li>
<li>Loss-of-rent and fair rental value calculations on investment properties.</li>
<li>Overhead and profit when several trades are needed.</li>
</ul>
<h2>Using appraisal after a Triad storm</h2>
<p>When an insurer has accepted a claim and the remaining dispute is about money, appraisal can narrow the issue to the numbers. Under a typical appraisal clause, each party selects an appraiser, those two agree on an umpire, and the agreement of any two sets the amount of loss. It is not a lawsuit, and it does not resolve coverage questions such as whether a particular exclusion applies.</p>
<p>We start by reviewing the carrier’s estimate and any contractor estimates line by line, inspecting the property and identifying where the real gaps are. Sometimes the right recommendation is to submit a supplement rather than invoke appraisal. When appraisal is the right move, we act as your appraiser and document the loss in a way an umpire can follow.</p>
<h2>Where we work in Guilford County</h2>
<p>We cover Greensboro from Fisher Park, Sunset Hills and Lindley Park to Starmount, College Hill and the Lake Jeanette area, and surrounding communities including Summerfield, Oak Ridge, Jamestown, Pleasant Garden and Gibsonville. High Point property owners in Guilford County are served as part of the same area.</p>""",
        "faqs": [
            ("Our east Greensboro brick home was damaged in a storm. Why is the brick estimate so low?",
             "Brick repairs are often underestimated because matching older brick and mortar color is difficult and labor intensive. Some estimates price a small patch that will never blend in. An appraiser looks at what a reasonable repair requires, including sourcing compatible brick and the masonry labor involved, and documents it."),
            ("I own a rental near UNCG. Can appraisal cover lost rent after storm damage?",
             "If your landlord or dwelling policy includes fair rental value or loss-of-rents coverage and the insurer accepts that part of the claim, disagreements over the amount can sometimes be handled in appraisal along with the building damage. The answer depends on the specific policy language, so we review it before advising."),
            ("Is Fisher Park’s historic district status relevant to my insurance claim?",
             "It can be. Exterior changes in a locally designated historic district may require review, and replacement materials may need to match the original character. Whether and how a policy pays for those requirements depends on its terms, including any ordinance or law coverage. We make sure the scope reflects what the repair actually involves."),
        ],
    },
    # ------------------------------------------------------------------ DURHAM
    {
        "slug": "durham",
        "city": "Durham",
        "county": "Durham County",
        "region": "Triangle / Piedmont",
        "geo": "Durham",
        "title": "Durham Property Claim Appraisal & Estimate Review",
        "desc": "Insurance claim appraisal for Durham and Durham County homes, rentals and mill lofts. Estimate review, appraisal-clause appraiser and umpire work.",
        "lede": "Durham’s tobacco-era lofts, mill houses and tree-lined streets near Duke make for claims where materials and history drive the cost. We help owners resolve disputes over the amount of a loss.",
        "perils": ["Tree strikes", "Ice storms", "Flash flooding", "Thunderstorm winds", "Plumbing leaks"],
        "hoods": ["Trinity Park", "Watts-Hillandale", "Old West Durham", "Forest Hills", "Duke Park", "Walltown", "Hope Valley", "Brightleaf", "Southpoint"],
        "housing": "Durham’s housing combines early-1900s homes and mill houses in Trinity Park, Old West Durham and Walltown, condos carved from former tobacco warehouses downtown, student rentals near Duke and North Carolina Central University, and newer subdivisions in south Durham.",
        "storms": [
            ("1996", "Hurricane Fran", "Fran’s winds felled large numbers of trees across Durham, damaging homes in older wooded neighborhoods."),
            ("2002", "December ice storm", "Ice-laden limbs and power lines fell across Durham County, leaving many residents without power for days."),
        ],
        "near": ["raleigh", "cary", "greensboro"],
        "body": """<h2>The Bull City’s mix of old and new</h2>
<p>Durham grew up around tobacco and textiles, and those industries left behind a distinctive building stock. Brick warehouses in Brightleaf and around the American Tobacco campus are now offices, restaurants and condominiums. Mill houses in Old West Durham, Walltown and East Durham have been renovated, expanded and in many cases rebuilt from the studs. Around Duke’s East Campus, Trinity Park and Watts-Hillandale hold large early-twentieth-century homes under a heavy tree canopy.</p>
<p>That variety means two claims from the same storm can look nothing alike. A limb through a Trinity Park roof involves plaster, old-growth framing and custom millwork. A water leak in a converted warehouse condo involves exposed brick, heavy timber, large industrial windows and an association master policy.</p>
<h2>Weather that drives Durham claims</h2>
<p>Most Durham losses come from wind, trees and water. Summer thunderstorms bring down limbs throughout the year, and ice events like the December 2002 storm can do the same across the whole county at once. Heavy rain can also overwhelm smaller creeks and storm drains, and that raises a question we see often: whether water entered from above, from a plumbing failure or as surface flooding. Standard homeowners policies generally exclude flood, which is usually insured separately through the NFIP or a private flood policy, so identifying the cause and the responding policy comes before any discussion of amount.</p>
<h2>Material and pricing issues we look for</h2>
<p>Older Durham homes often have plaster and lath, heart-pine floors and wood windows that do not appear in standard estimating categories. Converted lofts can have specialty finishes and building-wide elements that require coordination with the association. Student rentals near Duke and North Carolina Central raise questions about the condition of the property before the loss and about loss-of-rent coverage for landlords.</p>
<ul>
<li>Plaster walls and ceilings priced as standard drywall.</li>
<li>Heart-pine or old-growth flooring replaced with lower-grade material in the estimate.</li>
<li>Specialty windows and masonry in loft conversions.</li>
<li>Pre-existing condition arguments on frequently turned-over rentals.</li>
<li>Drying and mold remediation scope after water losses.</li>
<li>Permit and code items required by the City of Durham during repair.</li>
</ul>
<h3>Where appraisal helps and where it does not</h3>
<p>Appraisal is designed for disagreements about the value of a covered loss. If your policy contains an appraisal clause and it is invoked, each side typically chooses an appraiser, the two choose an umpire, and an agreed award resolves the amount. Appraisal does not decide whether a loss is covered, and it is not legal representation. When a disagreement is really about coverage, we will say so.</p>
<h2>Our Durham service area</h2>
<p>We work throughout Durham County, including Trinity Park, Duke Park, Forest Hills, Hope Valley, Walltown, Old West Durham and the downtown loft districts, as well as south Durham near Southpoint and the Research Triangle Park area. Nearby Chapel Hill, Hillsborough and Orange County properties are within reach as well.</p>""",
        "faqs": [
            ("Our condo is in a converted tobacco warehouse. How does that affect a water damage claim?",
             "Converted warehouses often have exposed brick, heavy timber and large industrial windows that cost more to repair than typical finishes. The association’s master policy may cover some of these elements while your HO-6 policy covers others. We review the governing documents and both estimates to price the repair accurately for the portion your policy covers."),
            ("My Durham basement took on water after heavy rain. Will appraisal help?",
             "It depends on the cause. If the water was surface flooding, a standard homeowners policy generally excludes it and a separate flood policy would apply. If it came from a failed sump pump, a plumbing leak or a roof opening, other coverages may respond. Appraisal only addresses the amount of loss under a policy that covers the damage."),
            ("I rent out a house near Duke. The insurer says the floor damage was pre-existing. Can appraisal resolve that?",
             "Appraisers routinely distinguish storm or water damage from wear and tear when measuring the amount of loss, and photos and records from before the loss help. A broader dispute about whether a loss is covered at all, however, is outside appraisal. We explain where your disagreement falls before you decide on next steps."),
        ],
    },
    # ------------------------------------------------------------------ WINSTON-SALEM
    {
        "slug": "winston-salem",
        "city": "Winston-Salem",
        "county": "Forsyth County",
        "region": "Triad",
        "geo": "Winston-Salem",
        "title": "Winston-Salem Insurance Appraiser | Forsyth Co.",
        "desc": "Winston-Salem insurance appraiser for Forsyth County homeowners and businesses: estimate review, appraisal-clause appraiser and umpire services.",
        "lede": "Winston-Salem’s hilly, wooded neighborhoods and early-twentieth-century homes make storm and water claims more involved than they first appear. We help resolve disputes over the cost to repair.",
        "perils": ["Hillside tree falls", "Hail storms", "Wind-driven rain", "Ice events", "Frozen pipes"],
        "hoods": ["Buena Vista", "West End", "Ardmore", "Old Salem", "Reynolda Park", "Washington Park", "Sherwood Forest", "Clemmons", "Lewisville"],
        "housing": "Winston-Salem includes Tudor-revival and craftsman homes in Buena Vista, Ardmore and the West End, restored Moravian-era buildings in Old Salem, 1950s–1970s ranches and split-levels across the suburbs, and newer subdivisions in Clemmons and Lewisville.",
        "storms": [
            ("1989", "Hurricane Hugo", "Hugo’s winds were still strong enough to topple trees and down power lines across the western Piedmont as the storm moved inland."),
            ("2002", "December ice storm", "Freezing rain coated trees and lines across much of the Piedmont, bringing down limbs and causing widespread outages."),
        ],
        "near": ["greensboro", "charlotte", "asheville"],
        "body": """<h2>Rolling terrain, big trees and older homes</h2>
<p>Winston-Salem sits on rolling ground at the western edge of the Triad, and many of its best-known neighborhoods were built on wooded hillsides in the early twentieth century. Buena Vista, Ardmore and the West End have mature oaks and poplars growing on slopes above and beside the homes. When a thunderstorm or an ice event brings a tree down on a hillside lot, removal can require cranes, rigging and careful access, all of which affect cost.</p>
<p>Sloped lots also influence water claims. Wind-driven rain enters through failed flashing and older windows, and water that collects on the uphill side of a home can find its way into basements and crawlspaces. Identifying whether water came in from a storm opening, a plumbing failure or surface flow matters, because standard homeowners policies treat those causes differently and generally exclude flood.</p>
<h2>Building types that complicate estimates</h2>
<p>Many homes in the West End and Buena Vista are Tudor-revival, craftsman or colonial-revival designs with plaster walls, slate or tile roofs, stucco, leaded or divided-lite windows and detailed millwork. Repairing those materials properly takes specialized trades, and the costs rarely match a standard estimating line. Old Salem, a historic district with restored eighteenth- and nineteenth-century buildings, carries its own review requirements for exterior work.</p>
<p>The suburbs bring different questions. In mid-century ranches and split-levels, a partial roof or siding repair may leave an obvious mismatch. In newer subdivisions in Clemmons and Lewisville, discontinued shingle lines and vinyl profiles create matching disputes. Small commercial buildings and older industrial structures downtown add questions about specialty roofing systems.</p>
<h3>Typical gaps between estimates</h3>
<ul>
<li>Slate, tile or clay roofs priced with asphalt-shingle assumptions.</li>
<li>Stucco and plaster repairs that ignore blending with existing surfaces.</li>
<li>Hillside tree removal and crane access left out or underpriced.</li>
<li>Basement and crawlspace water losses where cause is disputed.</li>
<li>Discontinued roofing and siding that cannot be reasonably matched.</li>
<li>Code upgrades required when older electrical or plumbing is opened up.</li>
</ul>
<h2>Our role in a Forsyth County dispute</h2>
<p>We are an independent appraisal firm, not a law firm and not a public adjuster. Our job is to determine and document the amount of a loss. When a policy includes an appraisal clause and appraisal is invoked, we can serve as your appointed appraiser, working with the insurer’s appraiser and, if needed, an umpire to reach an award. We also act as umpires and provide estimate reviews for owners who want an independent view before choosing a path.</p>
<p>Appraisal works best when the insurer has accepted that a loss occurred and the remaining disagreement is about scope and price. It is not designed to resolve coverage disputes, and we will tell you if that is what you are facing.</p>
<h2>Communities we serve</h2>
<p>We work across Winston-Salem, including Buena Vista, Ardmore, the West End, Washington Park, Reynolda Park and Sherwood Forest, and throughout Forsyth County in Clemmons, Lewisville, Kernersville, Rural Hall and Walkertown.</p>""",
        "faqs": [
            ("Our Buena Vista home has a slate roof. Why does the insurer’s estimate seem so low?",
             "Slate roofs require specialized installers, salvaged or matching slate and careful repair techniques. Estimates that apply asphalt-shingle pricing or assume a simple patch often fall well short. An appraiser documents the existing roof system and prices the repair or replacement a slate roofer would actually perform."),
            ("A tree fell on our hillside lot in Ardmore. Is removal cost part of the appraisal?",
             "Tree removal is typically covered within specific limits stated in the policy, often tied to whether the tree damaged a covered structure. When removal is covered and the dispute is over the amount, including crane and rigging costs on a steep lot, that can be part of the appraisal. Check your policy’s debris removal terms."),
            ("Can appraisal be used for a small business building in downtown Winston-Salem?",
             "Many commercial property policies include an appraisal clause. If your insurer has accepted the claim and you disagree about the cost to repair the building, roofing system or equipment, appraisal may be available. We review the policy language and the estimates first to confirm the dispute is about amount rather than coverage."),
        ],
    },
    # ------------------------------------------------------------------ FAYETTEVILLE
    {
        "slug": "fayetteville",
        "city": "Fayetteville",
        "county": "Cumberland County",
        "region": "Sandhills",
        "geo": "Fayetteville",
        "title": "Fayetteville NC Claim Appraisal for Homeowners",
        "desc": "Insurance appraisal in Fayetteville and Cumberland County: estimate reviews, appraisal-clause appraisers and umpires for hurricane and wind claims.",
        "lede": "Fayetteville sits where hurricanes weaken but still dump enormous rain, and its housing ranges from Haymount homes to rentals serving Fort Bragg families. We help settle disputes over the amount of a loss.",
        "perils": ["Hurricane winds", "River flooding", "Falling pines", "Tornado spin-ups", "Rental property damage"],
        "hoods": ["Haymount", "Westover", "Gillis Hill", "Hope Mills", "Spring Lake", "Stoney Point", "Vander", "Eastover"],
        "housing": "Fayetteville combines older homes in Haymount, large numbers of 1960s–1990s ranches and rental properties serving military families near Fort Bragg, manufactured homes in outlying areas, and newer subdivisions toward Hope Mills and the western part of the county.",
        "storms": [
            ("2016", "Hurricane Matthew", "Matthew’s rainfall pushed the Cape Fear River and local creeks into neighborhoods across Cumberland County, causing major flood damage."),
            ("2018", "Hurricane Florence", "Florence stalled over the Carolinas and its rain flooded areas along the Cape Fear River and Little River, while winds downed trees across the county."),
        ],
        "near": ["raleigh", "wilmington", "cary"],
        "body": """<h2>Hurricanes that arrive inland</h2>
<p>Fayetteville is roughly a two-hour drive from the coast, far enough that hurricanes usually lose some of their wind before they arrive but close enough that their rain does not. Matthew in 2016 and Florence in 2018 both brought extraordinary rainfall to the Sandhills. Water rose along the Cape Fear River, Cross Creek, Little River and smaller tributaries, and wind brought down tall pines onto roofs and vehicles throughout Cumberland County.</p>
<p>That combination makes cause the first question in many Fayetteville claims. Wind damage and wind-driven rain entering through a storm-created opening are typically handled under a homeowners policy. Rising surface water is generally excluded from standard homeowners coverage and handled by a separate flood policy, usually through the NFIP or a private insurer. When both happen to the same home, separating the damage is essential before anyone can agree on a number.</p>
<h2>Housing patterns in Cumberland County</h2>
<p>Haymount, one of the city’s oldest neighborhoods, has older homes with plaster, hardwood floors and established trees. Much of the rest of Fayetteville was built in the second half of the twentieth century, with brick and vinyl ranches and split-levels, many of them rental properties. Because of Fort Bragg, Fayetteville has a large share of homes owned by military families who rent them out after a reassignment, and owners are often managing a claim from another state or overseas.</p>
<p>Manufactured homes are common in outlying parts of the county and in nearby towns, and they have their own construction and pricing issues. Newer subdivisions toward Hope Mills and Gillis Hill raise familiar questions about matching roofing and siding.</p>
<h3>Disputes we see after Sandhills storms</h3>
<ul>
<li>Wind versus flood allocation on homes with both types of damage.</li>
<li>Roof replacement versus repair after tall pines fall across a ridge.</li>
<li>Loss-of-rent calculations for landlord policies.</li>
<li>Manufactured home components priced like site-built construction.</li>
<li>Mold and drying scope after prolonged water exposure.</li>
<li>Contractor pricing after a regional storm compared with pre-storm estimates.</li>
</ul>
<h2>When owners are far away</h2>
<p>A service member who has been reassigned, or a landlord who lives elsewhere, may not be able to walk the property with an adjuster. Appraisal can be useful in those situations because it puts the valuation in the hands of appraisers who inspect and document the loss. When a policy includes an appraisal clause and it is invoked, each side typically selects an appraiser, the two appraisers choose an umpire, and an agreement of two sets the amount. It is limited to the value of the loss and does not resolve coverage issues.</p>
<p>We act as party appraisers, as umpires and as estimate reviewers. An honest review sometimes shows the insurer’s estimate is close, and we will say so.</p>
<h2>Where we work around Fayetteville</h2>
<p>We serve Fayetteville from Haymount and Westover to Gillis Hill, as well as Hope Mills, Spring Lake, Stoney Point, Vander and Eastover, and nearby communities in Hoke and Harnett counties.</p>""",
        "faqs": [
            ("I’m stationed away from Fayetteville and my rental was damaged. Can appraisal still work?",
             "Yes. Appraisal does not require you to be at the property. Appraisers inspect the home, review estimates and document the loss, and you can authorize access through a property manager or tenant. If your landlord policy includes an appraisal clause and the claim is accepted, the amount can be resolved without you traveling back."),
            ("My Hope Mills home had wind and flood damage from the same storm. How is that handled?",
             "Wind damage typically falls under your homeowners policy, while rising water is generally excluded and handled by a separate flood policy if you have one. The two claims are evaluated separately. Appraisal applies to amount-of-loss disputes under the policy covering the damage, so separating wind and water damage carefully is the first step."),
            ("Does appraisal work for a manufactured home in Cumberland County?",
             "It can. Many manufactured home policies include an appraisal provision. These homes have specific components, such as roofing systems, wall panels and underbelly materials, that are priced differently from site-built homes. We review the policy and estimate to see whether those components were priced correctly before advising on appraisal."),
        ],
    },
    # ------------------------------------------------------------------ CARY
    {
        "slug": "cary",
        "city": "Cary",
        "county": "Wake County",
        "region": "Triangle / Piedmont",
        "geo": "Cary",
        "title": "Cary NC Insurance Appraiser | HOA & Hail Claims",
        "desc": "Cary insurance appraisal for Wake County homes: matching disputes, hail and tree claims, estimate review, appraiser and umpire work.",
        "lede": "Cary’s planned neighborhoods look uniform, and that uniformity is exactly what makes partial repairs contentious. We help homeowners settle disputes over matching, scope and price.",
        "perils": ["Hail damage", "Tree limb strikes", "Siding mismatch", "Ice storms", "Water heater leaks"],
        "hoods": ["Preston", "MacGregor Downs", "Lochmere", "Amberly", "Carpenter Village", "Downtown Cary", "Kildaire Farms", "Morrisville", "Apex"],
        "housing": "Cary is dominated by HOA-governed subdivisions built from the 1970s onward, from early golf-course communities like MacGregor Downs and Lochmere to newer areas such as Amberly, with townhomes and a small historic core downtown.",
        "storms": [
            ("1996", "Hurricane Fran", "Fran’s winds downed trees throughout western Wake County, damaging homes in Cary’s wooded neighborhoods."),
            ("2000", "January snowstorm", "Record snowfall across the Triangle brought heavy loads on roofs, carports and trees."),
            ("2002", "December ice storm", "Ice brought down limbs and lines across Wake County and left many Cary residents without power for days."),
        ],
        "near": ["raleigh", "durham", "fayetteville"],
        "body": """<h2>The matching problem in planned communities</h2>
<p>Much of Cary was built as planned residential development, with homeowners associations that set exterior standards for roofing color, siding, trim and fencing. Homes on a street often share builders, materials and paint palettes. That consistency is attractive until a storm damages one or two elevations of a single house. If replacement shingles or siding in the original color and profile are no longer available, a partial repair can leave a home visibly mismatched, and possibly out of step with the association’s standards.</p>
<p>How a policy treats mismatch depends on its wording, and North Carolina owners should read their own policies carefully. But in an appraisal focused on the amount of loss, the practical question is what it costs to restore the home to a reasonably uniform appearance, and estimates often disagree sharply on that point.</p>
<h2>Weather and tree exposure in western Wake County</h2>
<p>Cary’s neighborhoods were carved out of pine and hardwood forest, and many developments preserved large stands of trees between homes and along greenways. That canopy means limbs on roofs after summer thunderstorms and ice events. Hail also reaches the area, sometimes in narrow bands that damage one subdivision and spare the next. Inside the home, water heaters, supply lines and dishwashers in houses built in the 1980s and 1990s are a steady source of water claims.</p>
<h2>Housing in Cary and how estimates handle it</h2>
<p>Early communities such as MacGregor Downs, Lochmere and Kildaire Farms date from the 1970s and 1980s, with cedar and hardboard siding, older roofs and original hardwood or parquet floors. Preston and later developments added larger homes with complex rooflines, multiple gables and stone or brick accents. Newer communities like Amberly include townhomes where the association master policy may cover exteriors.</p>
<ul>
<li>Discontinued shingle colors and siding profiles that cannot be reasonably matched.</li>
<li>Complex roof geometry with steep pitches, valleys and multiple stories priced as simple roofs.</li>
<li>Continuous hardwood flooring replaced in only one room.</li>
<li>Cabinet runs where a damaged section cannot be matched.</li>
<li>Townhome claims split between the HOA policy and the owner’s policy.</li>
<li>Hardboard siding with limited repair options.</li>
</ul>
<h3>How we approach Cary claims</h3>
<p>We start by reviewing your insurer’s estimate, your contractor’s estimate and the policy, then inspect the property. Steep, cut-up roofs need accurate measurement and pitch-appropriate labor. Matching questions need product research. Interior water losses need a realistic drying and repair scope.</p>
<p>If a policy includes an appraisal clause and the dispute is about the amount of loss, appraisal can resolve it through a structured process: each side selects an appraiser, the appraisers choose an umpire if needed, and an award signed by two of the three sets the value. Appraisal does not address coverage questions. We are an appraisal firm, not lawyers or public adjusters.</p>
<h2>Our coverage in and around Cary</h2>
<p>We work throughout Cary, including Preston, MacGregor Downs, Lochmere, Kildaire Farms, Carpenter Village, Amberly and downtown, and in neighboring Morrisville, Apex, Holly Springs and western Raleigh.</p>""",
        "faqs": [
            ("Hail damaged the front of my Cary home, but the siding color is discontinued. What happens?",
             "Whether a policy pays to replace undamaged siding for a uniform appearance depends on its specific wording. When the insurer agrees some siding must be replaced but the parties disagree on how much is needed to achieve a reasonable match, that amount question can often be handled through appraisal. Product research on availability is key."),
            ("My HOA requires a specific roof color. Does that affect the insurance appraisal?",
             "HOA standards do not override your policy, but they are part of the practical context. If an exact match to the original shingle is unavailable and a partial replacement would clearly not match, that affects the scope of a reasonable repair. We document availability and the visual result so the appraisal reflects reality."),
            ("We have a townhome in Cary. Does our policy or the association’s cover the roof?",
             "It depends on your association’s declarations and its master policy. Many townhome communities insure roofs and exteriors through the association, while owners insure interiors. Some do the opposite. We review both policies and the governing documents first, because appraisal must be pursued under the policy that actually covers the damage."),
        ],
    },
    # ------------------------------------------------------------------ WILMINGTON
    {
        "slug": "wilmington",
        "city": "Wilmington",
        "county": "New Hanover County",
        "region": "Southeastern coast",
        "geo": "Wilmington",
        "title": "Wilmington Hurricane Claim Appraisal Services",
        "desc": "Hurricane and wind claim appraisal in Wilmington and New Hanover County: estimate review, appraisal-clause appraisers and umpires for coastal homes.",
        "lede": "Wilmington lives with hurricanes, from the historic district’s nineteenth-century homes to beach houses on pilings. We help owners resolve wind-claim disputes over what repairs actually cost.",
        "perils": ["Hurricane winds", "Wind-driven rain", "Storm surge", "Falling live oaks", "Roof uplift"],
        "hoods": ["Historic Downtown", "Carolina Heights", "Forest Hills", "Sunset Park", "Wrightsville Beach", "Carolina Beach", "Kure Beach", "Ogden", "Monkey Junction"],
        "housing": "Wilmington ranges from antebellum and Victorian homes in one of the state’s largest historic districts to mid-century homes in Forest Hills and Sunset Park, condos and raised beach houses at Wrightsville, Carolina and Kure beaches, and large suburban subdivisions in Ogden and Monkey Junction.",
        "storms": [
            ("1996", "Hurricane Fran", "Fran made landfall near Cape Fear, bringing damaging winds and surge to New Hanover County beaches weeks after Bertha."),
            ("1996", "Hurricane Bertha", "Bertha struck the southeastern coast in July, damaging beach properties and setting up a difficult season for the area."),
            ("2018", "Hurricane Florence", "Florence made landfall near Wrightsville Beach, and record rainfall flooded roads until Wilmington was effectively cut off for days."),
        ],
        "near": ["new-bern", "fayetteville", "outer-banks"],
        "body": """<h2>Coastal claims start with wind</h2>
<p>Wilmington and the New Hanover County beaches sit directly in the path of Atlantic hurricanes. Hazel in 1954, Bertha and Fran in 1996 and Florence in 2018 are part of local memory. Florence made landfall near Wrightsville Beach and lingered, and its slow movement turned what began as a wind event into a prolonged rain and flooding disaster that cut the city off from the rest of the state for days.</p>
<p>Most homeowners claims here involve wind and wind-driven rain: roofs lifted at the edges, shingles and metal panels torn away, soffits and siding blown off and water forced into walls and ceilings. Storm surge and rising water are a different matter. Standard homeowners policies generally exclude flood, which is usually insured through the NFIP or private flood policies, so separating wind damage from water damage is often the central question on coastal properties.</p>
<h2>Coastal insurance in North Carolina</h2>
<p>Many property owners on the beaches and in coastal parts of New Hanover County buy wind and hail coverage through the North Carolina Insurance Underwriting Association, known as the Coastal Property Insurance Pool, which serves beach and coastal areas of 18 counties. Others have wind included in a standard homeowners policy, or pair a homeowners policy that excludes wind with a separate wind policy. Knowing which policy covers which peril is the first step, because appraisal applies under the policy that covers the damage.</p>
<h2>A housing stock shaped by the coast</h2>
<p>Downtown Wilmington and Carolina Heights contain antebellum, Italianate and Victorian homes with plaster, heart-pine floors, tall windows and porches. Historic preservation review applies to exterior changes in designated districts. Forest Hills and Sunset Park have older homes under large live oaks. At Wrightsville, Carolina and Kure beaches, homes on pilings and oceanfront condominiums face salt exposure, wind-rated construction requirements and association master policies.</p>
<h3>Where coastal estimates fall short</h3>
<ul>
<li>Wind versus surge allocation on beach and soundside homes.</li>
<li>Roof repairs that ignore current wind-resistance installation requirements.</li>
<li>Wind-driven rain damage to insulation and interior walls underestimated.</li>
<li>Historic-district materials priced with modern equivalents.</li>
<li>Condo claims divided between master and unit-owner policies.</li>
<li>Labor and material costs in the months after a major storm.</li>
</ul>
<h2>How appraisal fits after a hurricane</h2>
<p>After a large storm, insurers handle thousands of claims, and the initial estimate may be written quickly. If a claim has been accepted and you disagree with the amount, an appraisal clause may allow either side to request appraisal. Typically, each party selects an appraiser, those two choose an umpire, and an award agreed by two of the three resolves the amount of loss. Appraisal is not a lawsuit and does not settle coverage disputes.</p>
<p>We work as party appraisers, umpires and estimate reviewers. We are not a law firm or public adjuster.</p>
<h2>Where we work on the southeastern coast</h2>
<p>We serve Wilmington from the historic district and Carolina Heights to Forest Hills, Sunset Park, Ogden and Monkey Junction, along with Wrightsville Beach, Carolina Beach, Kure Beach and nearby communities in Brunswick and Pender counties.</p>""",
        "faqs": [
            ("My Wrightsville Beach home has a Coastal Property Insurance Pool wind policy. Does appraisal apply?",
             "Policies issued through the North Carolina Insurance Underwriting Association generally contain an appraisal provision similar to other property policies. If your wind claim is accepted and you disagree on the amount, appraisal may be available. We review your specific policy form first, because the wording controls the process and timelines."),
            ("Florence damaged my Wilmington home with both wind and flood water. How do we separate them?",
             "Separating wind and flood damage requires a careful inspection of the home, water lines, roof and wall openings and storm data. Wind-related damage generally falls under the homeowners or wind policy, while rising water falls under a flood policy. Appraisal addresses the amount of loss under the policy covering the damage, so accurate allocation matters."),
            ("Can appraisal help with a historic home in downtown Wilmington?",
             "Yes, when the dispute is about the cost to repair. Historic homes often have plaster, heart-pine floors, custom millwork and wood windows that are costly to repair properly, and preservation review may affect materials. We document existing materials and price a realistic repair so the appraisal reflects what the home actually requires."),
        ],
    },
    # ------------------------------------------------------------------ ASHEVILLE
    {
        "slug": "asheville",
        "city": "Asheville",
        "county": "Buncombe County",
        "region": "Mountains",
        "geo": "Asheville",
        "title": "Asheville Insurance Appraiser After Helene",
        "desc": "Asheville and Buncombe County insurance appraiser for Helene, wind, tree and water claims: estimate review, appraisal-clause appraiser and umpire.",
        "lede": "Helene showed how quickly mountain storms turn into wind, tree and water losses at once. We help Asheville and Buncombe County owners resolve disagreements over what those repairs truly cost.",
        "perils": ["River flooding", "Landslides", "Hillside tree falls", "Wind damage", "Ice and snow"],
        "hoods": ["Montford", "Grove Park", "Kenilworth", "West Asheville", "Biltmore Village", "River Arts District", "Haw Creek", "Swannanoa", "Black Mountain"],
        "housing": "Asheville blends 1900s–1930s arts-and-crafts and Queen Anne homes in Montford and Grove Park, bungalows in West Asheville and Kenilworth, steep-lot mountain homes and cabins across the county, and condos and short-term rentals throughout.",
        "storms": [
            ("1916", "French Broad flood", "Back-to-back tropical systems sent the French Broad River to historic levels, devastating riverside areas of Asheville."),
            ("2004", "Hurricanes Frances and Ivan", "Two tropical storms in September flooded parts of Asheville, including Biltmore Village along the Swannanoa River."),
            ("2024", "Hurricane Helene", "Helene caused catastrophic flooding and widespread wind and tree damage across Buncombe County, devastating Biltmore Village, the River Arts District and Swannanoa."),
        ],
        "near": ["charlotte", "winston-salem", "greensboro"],
        "body": """<h2>After Helene: mountain losses are layered</h2>
<p>Hurricane Helene in September 2024 brought rainfall that overwhelmed the French Broad and Swannanoa rivers and countless smaller creeks. Biltmore Village, the River Arts District and Swannanoa saw catastrophic flooding, while high winds and saturated soil brought down trees across the entire county. Landslides damaged homes and roads on steep slopes. Many properties experienced more than one type of damage in the same storm.</p>
<p>For insurance purposes, those types of damage are often treated very differently. Wind and falling trees are typically covered under homeowners policies. Rising water is generally excluded and handled through flood policies, usually NFIP or private flood coverage. Earth movement, including landslides and mudflow, is commonly excluded from standard homeowners policies, though wording varies. Sorting out which damage falls under which coverage is the foundation for any discussion of amount.</p>
<h2>Terrain and access shape the cost of repair</h2>
<p>Asheville’s steep, winding roads and hillside lots make even ordinary repairs more expensive. Getting a crane to a tree on a slope, staging roofing materials on a narrow drive or hauling debris down a mountain road all add labor and equipment costs that standard estimating databases may not capture. After Helene, demand for contractors across western North Carolina exceeded supply, and pricing has reflected that.</p>
<h2>Housing stock across Buncombe County</h2>
<p>Montford and Grove Park contain Queen Anne, arts-and-crafts and shingle-style homes with plaster, chestnut and oak trim, stone foundations and complex rooflines. West Asheville and Kenilworth have bungalows from the 1920s and later. Outside the city, homes are often built into slopes with walk-out basements, decks on tall posts and log or timber framing. Condos, accessory units and short-term rentals add questions about loss of rental income and contents.</p>
<h3>Disputes that come up in mountain claims</h3>
<ul>
<li>Allocation of damage between wind, flood and earth movement.</li>
<li>Tree removal and crane access on steep lots.</li>
<li>Specialty materials such as stone, log and timber framing.</li>
<li>Decks and retaining structures on hillside homes.</li>
<li>Loss of rental income for long-term and short-term rentals.</li>
<li>Labor and material pricing in a stretched local market.</li>
</ul>
<h2>How appraisal can help</h2>
<p>Many claims in western North Carolina remain unresolved long after a storm. Appraisal will not answer coverage questions, but if your insurer has accepted a claim and you disagree on the amount, an appraisal clause may provide a structured way forward. Each side typically selects an appraiser, the two select an umpire, and an award agreed by two of the three determines the amount of loss.</p>
<p>We serve as party appraisers, umpires and estimate reviewers. We are not attorneys or public adjusters, and if a disagreement is really about coverage, we will tell you so you can seek the right help.</p>
<h2>Where we work in the mountains</h2>
<p>We serve Asheville, including Montford, Grove Park, Kenilworth, West Asheville, Haw Creek, Biltmore Village and the River Arts District, and communities across Buncombe County such as Swannanoa, Black Mountain, Weaverville, Woodfin and Fairview.</p>""",
        "faqs": [
            ("My Asheville home had tree damage and flood damage from Helene. Can appraisal handle both?",
             "Appraisal works within a single policy’s amount-of-loss dispute. Tree and wind damage is usually under your homeowners policy, while flood damage is under a separate flood policy if you have one. Each claim is evaluated on its own terms. Careful documentation separating the damage is the first step before considering appraisal."),
            ("A landslide damaged my home near Black Mountain. Will appraisal help?",
             "Earth movement, including landslides, is commonly excluded from standard homeowners policies, although wording varies and some endorsements add coverage. Whether the loss is covered is a coverage question outside appraisal. If part of the damage is covered, such as a tree strike, appraisal may apply to the amount of that portion."),
            ("Repairs in Buncombe County cost more since Helene. Does appraisal account for that?",
             "Appraisal aims to determine the reasonable cost to repair the damage in the local market. After a major regional disaster, labor and material costs often rise, and access on steep lots adds expense. We document current local pricing and site conditions so the award reflects what the repair actually costs in western North Carolina."),
        ],
    },
    # ------------------------------------------------------------------ GREENVILLE
    {
        "slug": "greenville",
        "city": "Greenville",
        "county": "Pitt County",
        "region": "Coastal Plain",
        "geo": "Greenville",
        "title": "Greenville NC Insurance Appraiser | Pitt County",
        "desc": "Greenville and Pitt County insurance appraisal for homes and student rentals: estimate review, appraisal-clause appraiser and umpire services.",
        "lede": "Greenville’s place on the Tar River and its large student rental market shape almost every property claim in town. We help owners and landlords resolve disputes over what a loss is worth.",
        "perils": ["Tar River flooding", "Hurricane winds", "Tornado warnings", "Rental property damage", "Fallen pines"],
        "hoods": ["Uptown Greenville", "College View", "Tar River area", "Brook Valley", "Winterville", "Ayden", "Simpson", "Grimesland", "Farmville"],
        "housing": "Greenville includes early-twentieth-century homes near East Carolina University, a large concentration of student rental houses and apartment complexes, mid-century brick ranches, newer subdivisions toward Winterville and rural farmhouses across Pitt County.",
        "storms": [
            ("1999", "Hurricane Floyd", "Floyd’s rainfall drove the Tar River to record levels, flooding large parts of Greenville and Pitt County and devastating nearby Princeville."),
            ("2016", "Hurricane Matthew", "Matthew’s rainfall again pushed the Tar River above flood stage, threatening low-lying neighborhoods in Greenville."),
        ],
        "near": ["new-bern", "raleigh", "outer-banks"],
        "body": """<h2>Life along the Tar River</h2>
<p>For Greenville, Hurricane Floyd in 1999 remains the defining storm. Floyd’s rain fell on ground already saturated by Hurricane Dennis, and the Tar River rose to record levels, flooding neighborhoods, farmland and businesses across Pitt County. Matthew in 2016 brought the river up again. Both events taught the same lesson: in eastern North Carolina, river flooding can follow a storm by days, long after the wind has passed.</p>
<p>That timing matters for claims. Wind damage to roofs and siding from a hurricane or severe thunderstorm is usually handled under a homeowners or dwelling policy. Rising floodwater is generally excluded from those policies and covered, if at all, by a separate flood policy through the NFIP or a private carrier. Owners with both types of damage need careful documentation that distinguishes wind from water.</p>
<h2>A city shaped by East Carolina University</h2>
<p>ECU’s presence gives Greenville one of the largest concentrations of student rental housing in the state. Older homes near campus and in College View have been converted into rentals, and apartment and townhome complexes spread out along major roads. Many landlords own multiple properties and carry dwelling or landlord policies rather than standard homeowners policies.</p>
<p>Those properties create distinct claim questions. Was damage caused by the storm or by tenants? What was the condition of the property before the loss? Is loss of rent covered, and for how long? Turnover between leases can complicate documentation, so photographs and inspection records become important.</p>
<h2>Building types we see in Pitt County</h2>
<p>Older homes near Uptown and campus have plaster, hardwood floors and wood windows. Mid-century brick ranches are common across the city. Newer subdivisions in Winterville and Brook Valley have vinyl siding and architectural shingles where matching becomes the main issue. In rural parts of the county, farmhouses and outbuildings such as barns and equipment sheds add specialty items.</p>
<h3>Typical sources of disagreement</h3>
<ul>
<li>Wind versus flood allocation after hurricanes.</li>
<li>Tenant wear and tear versus storm or water damage.</li>
<li>Loss-of-rent duration and amount on landlord policies.</li>
<li>Roof repair versus replacement after tall pines fall.</li>
<li>Outbuildings and farm structures priced too low.</li>
<li>Drying and mold remediation after prolonged moisture.</li>
</ul>
<h2>Appraisal for Greenville owners and landlords</h2>
<p>If your insurer has accepted a claim and you disagree only about the amount, appraisal may be available under your policy. Typically each side selects an appraiser, the appraisers choose an umpire and an agreement between two of the three determines the amount of loss. Appraisal does not decide coverage issues, and it is not legal representation.</p>
<p>We act as party appraisers, umpires and estimate reviewers. For landlords with several damaged properties, we can review each estimate and identify which claims have a meaningful gap worth pursuing.</p>
<h2>Our Pitt County service area</h2>
<p>We serve Greenville, including Uptown, College View, the areas along the Tar River and Brook Valley, along with Winterville, Ayden, Simpson, Grimesland, Farmville and surrounding parts of Pitt County.</p>""",
        "faqs": [
            ("I own several student rentals near ECU. Can appraisal help with more than one property?",
             "Each property and claim is typically handled separately under its policy, but we can review all of the estimates together and identify where the gaps are meaningful. If appraisal is invoked on more than one claim, the process runs for each, though coordinating inspections and documentation can make it more efficient."),
            ("The insurer says damage at my Greenville rental was tenant wear, not storm damage. What can I do?",
             "Appraisers routinely distinguish storm or water damage from wear and tear when determining the amount of loss. Photos from move-in inspections and maintenance records help. If the dispute is whether any damage is covered at all, however, that is a coverage question outside appraisal, and we will tell you if that applies."),
            ("Does a Pitt County homeowners policy cover Tar River flooding?",
             "Standard homeowners policies generally exclude flood damage from rising water. Flood coverage is usually purchased separately through the NFIP or a private flood insurer. If you have flood coverage, disputes over the amount of a flood claim are handled under that policy’s own terms, which may differ from homeowners appraisal provisions."),
        ],
    },
    # ------------------------------------------------------------------ NEW BERN
    {
        "slug": "new-bern",
        "city": "New Bern",
        "county": "Craven County",
        "region": "Inner Banks",
        "geo": "New Bern",
        "title": "New Bern Claim Appraisal | Craven County Homes",
        "desc": "Insurance appraisal in New Bern and Craven County for hurricane, wind and water damage: estimate review, appraiser and umpire services for owners.",
        "lede": "New Bern sits where the Neuse and Trent rivers meet, which means hurricanes bring wind, rain and wind-driven water. We help owners in Craven County resolve disputes over the cost of repairs.",
        "perils": ["Wind-driven surge", "Hurricane winds", "Riverfront flooding", "Falling oaks", "Roof leaks"],
        "hoods": ["Historic Downtown", "Ghent", "DeGraffenried Park", "Trent Woods", "River Bend", "James City", "Fairfield Harbour", "Taberna", "Bridgeton"],
        "housing": "New Bern combines eighteenth- and nineteenth-century homes in its historic downtown, early-twentieth-century homes in Ghent, mid-century neighborhoods like DeGraffenried Park, waterfront and canal homes in River Bend and Fairfield Harbour, and newer subdivisions such as Taberna.",
        "storms": [
            ("2011", "Hurricane Irene", "Irene’s winds pushed water up the Neuse and Trent rivers, flooding low-lying areas around New Bern."),
            ("2018", "Hurricane Florence", "Florence drove a destructive surge up the Neuse River into New Bern, flooding downtown and riverfront neighborhoods and damaging thousands of homes."),
        ],
        "near": ["greenville", "wilmington", "outer-banks"],
        "body": """<h2>Where two rivers meet the storm</h2>
<p>New Bern lies at the confluence of the Neuse and Trent rivers, where the Neuse widens into a broad estuary leading to Pamlico Sound. When a hurricane approaches from the right angle, its winds push water up that estuary and into the city. Florence in 2018 did exactly that, driving a surge into downtown, along East Front Street and into riverfront neighborhoods and communities like Fairfield Harbour and River Bend. Irene in 2011 had pushed water into low-lying areas years earlier.</p>
<p>That history makes the distinction between wind and water central to New Bern claims. Damage from wind and wind-driven rain entering through a storm opening is typically covered under homeowners or wind policies. Surge and rising water are generally excluded from standard homeowners policies and handled through flood policies, usually NFIP or private flood coverage. Homes with both types of damage need clear documentation.</p>
<h2>North Carolina’s second-oldest town</h2>
<p>New Bern’s historic downtown includes homes and buildings from the colonial and early federal periods, along with many from the nineteenth century. Plaster walls, heart-pine floors, wood windows, original millwork and brick foundations are common, and exterior changes in historic districts can require review. Ghent and DeGraffenried Park have early and mid-twentieth-century homes, many shaded by large live oaks and water oaks.</p>
<p>Along the water, River Bend and Fairfield Harbour include canal-front homes, docks, bulkheads and boathouses. Newer subdivisions in Taberna and around Trent Woods add vinyl siding and architectural shingles, where matching is often the main issue.</p>
<h3>Disputes we see after eastern North Carolina storms</h3>
<ul>
<li>Allocation between wind damage and surge or flood damage.</li>
<li>Historic materials priced as modern equivalents.</li>
<li>Docks, piers and boathouses and how policies treat them.</li>
<li>Wind-driven rain damage to wall cavities and insulation.</li>
<li>Tree removal and roof repairs after large oaks fall.</li>
<li>Contractor pricing and availability after a regional storm.</li>
</ul>
<h2>Military and retiree households</h2>
<p>New Bern is near Marine Corps Air Station Cherry Point in Havelock, and many households are military families or retirees who may be away from the property for extended periods. A rental owner or a homeowner who is not on site can still pursue appraisal, because appraisers inspect and document the loss directly.</p>
<h2>How appraisal fits</h2>
<p>If your insurer has accepted a claim and you disagree on the amount, an appraisal clause may allow either side to invoke appraisal. Typically each side selects an appraiser, the two appraisers choose an umpire and an award agreed by two of the three sets the amount of loss. Appraisal does not resolve coverage disputes and is not a lawsuit.</p>
<p>We act as party appraisers, umpires and estimate reviewers. We are an appraisal firm, not a law firm or public adjuster.</p>
<h2>Where we work in Craven County</h2>
<p>We serve New Bern, including the historic downtown, Ghent, DeGraffenried Park and Trent Woods, and nearby River Bend, Fairfield Harbour, James City, Taberna, Bridgeton and Havelock.</p>""",
        "faqs": [
            ("Florence flooded my New Bern home, and wind damaged the roof. How is that handled?",
             "Roof and wind damage is typically handled under your homeowners or wind policy, while surge and rising water are generally excluded and fall under a separate flood policy if you have one. The claims are evaluated separately. Appraisal applies to the amount of loss under the policy covering that damage."),
            ("Our downtown New Bern home is historic. Does that affect the appraisal?",
             "It often does. Older homes may have plaster, heart-pine floors, original millwork and wood windows, and historic district review may affect materials. Whether ordinance or law coverage applies depends on your policy. In appraisal, we document existing materials and price a realistic repair."),
            ("Can appraisal include my dock in Fairfield Harbour?",
             "Coverage for docks, piers and boathouses varies widely between policies, and some exclude or limit them. If your policy covers the dock and the insurer accepts the claim, disagreements over the repair cost can be part of an appraisal. We review the policy language first."),
        ],
    },
    # ------------------------------------------------------------------ OUTER BANKS
    {
        "slug": "outer-banks",
        "city": "Outer Banks",
        "county": "Dare County",
        "region": "Outer Banks",
        "geo": "Nags Head",
        "title": "Outer Banks Insurance Appraiser | Dare County",
        "desc": "Outer Banks insurance appraisal for Dare County beach homes and rentals: wind claim estimate review, appraisal-clause appraiser and umpire work.",
        "lede": "On the Outer Banks, beach homes on pilings face hurricanes, nor’easters and salt air year after year. We help Dare County owners settle disputes over what wind damage actually costs to repair.",
        "perils": ["Hurricane winds", "Nor’easters", "Overwash and surge", "Salt corrosion", "Roof and siding loss"],
        "hoods": ["Duck", "Southern Shores", "Kitty Hawk", "Kill Devil Hills", "Nags Head", "Manteo", "Rodanthe", "Avon", "Hatteras"],
        "housing": "The Outer Banks are dominated by raised beach homes on pilings, many of them large vacation rentals, along with older flat-top and cottage-style homes in Nags Head and Kill Devil Hills, soundside homes, and historic buildings in Manteo.",
        "storms": [
            ("1962", "Ash Wednesday Storm", "A powerful nor’easter battered the Outer Banks over several tide cycles, destroying homes and reshaping the beaches."),
            ("2003", "Hurricane Isabel", "Isabel cut a new inlet through Hatteras Island, isolating the village of Hatteras until the gap was filled."),
            ("2011", "Hurricane Irene", "Irene breached NC 12 on Hatteras Island in several places, cutting off villages on the island."),
            ("2019", "Hurricane Dorian", "Dorian’s soundside surge flooded much of Ocracoke Island, damaging homes and businesses."),
        ],
        "near": ["wilmington", "new-bern", "greenville"],
        "body": """<h2>Barrier islands, constant weather</h2>
<p>The Outer Banks stretch along a narrow chain of barrier islands, exposed to the Atlantic on one side and the sounds on the other. Hurricanes get most of the attention, but nor’easters also cause serious damage, sometimes lingering through several tide cycles. The Ash Wednesday Storm of 1962 remains a reference point, and Isabel in 2003, Irene in 2011 and Dorian in 2019 each showed how quickly the islands can be cut off.</p>
<p>Wind is the main source of homeowners claims: shingles, siding and trim torn away, decks and stairs damaged, windows and doors broken and wind-driven rain forced into walls. Overwash, surge and rising sound water are a different category. Standard homeowners and wind policies generally exclude flood, which is usually insured through the NFIP or private flood policies. Separating wind from water damage is often the first and most important task.</p>
<h2>How beach properties are insured</h2>
<p>Many Dare County owners buy wind and hail coverage through the North Carolina Insurance Underwriting Association, the Coastal Property Insurance Pool that serves beach and coastal areas of 18 counties. Some pair a homeowners or dwelling policy that excludes wind with a separate pool wind policy and a flood policy. Knowing which policy responds to which damage matters, because appraisal applies to amount-of-loss disputes under the policy that covers the damage.</p>
<h2>Raised homes and rental properties</h2>
<p>Most newer beach homes are built on pilings, with large decks, multiple stories, cedar shakes or fiber-cement siding and metal or architectural shingle roofs. Many are vacation rentals, and some have pools, elevators and hot tubs. Older flat-top and cottage-style homes in Nags Head and Kill Devil Hills carry different construction details. Salt air speeds corrosion of fasteners, flashing and metal components, which can lead to arguments over what is storm damage and what is long-term deterioration.</p>
<h3>Where beach-house estimates diverge</h3>
<ul>
<li>Wind versus overwash or flood allocation.</li>
<li>Corrosion and wear claims used to reduce wind damage.</li>
<li>Decks, stairs and walkways on raised homes priced too low.</li>
<li>Material and labor costs on remote islands, including transport.</li>
<li>Loss of rental income for vacation rental owners.</li>
<li>Cedar shake and specialty siding priced as standard materials.</li>
</ul>
<h2>Appraisal on the Outer Banks</h2>
<p>Repair costs on the islands often run higher than inland because materials and crews have to come over the bridges or by ferry, and demand spikes after a storm. If your insurer has accepted a claim and you disagree on the amount, an appraisal clause may allow either side to invoke appraisal. Typically each side selects an appraiser, the two appraisers choose an umpire and an award agreed by two of the three determines the amount of loss. Appraisal does not decide coverage.</p>
<p>We act as party appraisers, umpires and estimate reviewers. We are not attorneys or public adjusters.</p>
<h2>Where we work</h2>
<p>We serve the Outer Banks from Duck and Southern Shores through Kitty Hawk, Kill Devil Hills, Nags Head and Manteo, and down Hatteras Island to Rodanthe, Avon, Buxton and Hatteras, as well as Corolla and Ocracoke.</p>""",
        "faqs": [
            ("My Nags Head rental home has a pool wind policy. Can I use appraisal for a wind claim?",
             "Policies issued through the North Carolina Insurance Underwriting Association generally contain an appraisal provision. If the insurer accepts your wind claim and you disagree on the amount, appraisal may be available. We review your specific policy form first, because its wording controls the process and timelines."),
            ("The adjuster says the damage to my Kill Devil Hills home is corrosion, not wind. What now?",
             "Salt air causes corrosion over time, and insurers often argue that metal components failed from deterioration rather than wind. An appraiser examines the damage pattern, fasteners and storm data to distinguish wind damage from long-term wear when measuring the amount of loss. A broader coverage dispute is outside appraisal."),
            ("Repairs on Hatteras Island cost more than on the mainland. Is that considered?",
             "Appraisal aims to determine the reasonable cost to repair the damage where the property is located. On Hatteras Island, transporting materials and crews, limited contractor availability and post-storm demand can increase costs. We document those local factors so the appraisal reflects realistic island pricing."),
        ],
    },
]
