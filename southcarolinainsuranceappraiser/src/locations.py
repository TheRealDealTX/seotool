"""South Carolina location pages.

Twelve city pages, ordered for navigation. Each entry carries its own
metadata (title, desc, h1, kw), short local facts used in the page hero and
sidebar, an HTML body written for that city, and three local FAQs. Storm
references are limited to well-documented events. Nothing here is legal
advice; pages point readers to a South Carolina attorney for legal questions.
"""

LOCATIONS = [
    # ------------------------------------------------------------ Charleston
    {
        "slug": "charleston",
        "city": "Charleston",
        "county": "Charleston & Berkeley Counties",
        "region": "Lowcountry",
        "kw": "insurance appraiser Charleston SC",
        "title": "Charleston SC Insurance Appraiser for Disputed Claims",
        "desc": "Independent insurance appraiser in Charleston SC for Charleston & Berkeley Counties: hurricane, roof, water and historic-home claim disputes.",
        "h1": "Insurance Appraiser for Charleston, SC Property Claims",
        "lede": "An independent insurance appraiser for Charleston, SC homeowners and owners of historic, coastal and commercial property. We price disputed claims line by line, from piazza ceilings on the peninsula to roofs on Daniel Island.",
        "perils": ["Hurricane wind", "Storm surge & tidal flooding", "Wind-driven rain", "Live-oak limb fall", "Earthquake (if endorsed)"],
        "neighborhoods": ["South of Broad", "Ansonborough", "Harleston Village", "Wagener Terrace", "West Ashley", "James Island", "Daniel Island", "Elliotborough"],
        "housing": "Charleston single houses with side piazzas, stuccoed masonry and wood-frame homes downtown give way to mid-century ranches in West Ashley and newer elevated and slab-built homes on the islands.",
        "storms": [
            "1989 · Hurricane Hugo — Category 4 landfall near Sullivan’s Island; widespread roof and surge damage",
            "2016 · Hurricane Matthew — downed trees, power loss and flooding across the peninsula",
            "2017 · Hurricane Irma — storm surge pushed water into downtown streets",
            "2023 · Hurricane Idalia — tidal flooding on the peninsula and low-lying islands",
        ],
        "near": ["mount-pleasant", "summerville", "beaufort"],
        "body": """
<h2>Why Charleston claims rarely fit a standard estimate</h2>
<p>A carrier’s estimating software is built around typical construction. Much of downtown Charleston is anything but typical. A single house south of Broad may have a standing-seam or slate roof, two tiers of piazzas with beadboard ceilings, heart-pine floors, lime-based stucco over brick and hand-run plaster cornices. When a storm damages that kind of building, a line item for “drywall, ½ inch” or “paint exterior siding” does not describe the repair.</p>
<p>The <strong>Board of Architectural Review</strong> adds another layer. In the districts it oversees, exterior changes visible from the street generally need approval, and the board can expect in-kind materials rather than the cheapest substitute. If your policy includes ordinance or law coverage, some of that added cost may be payable up to the limit you bought. If it does not, the gap becomes a negotiation. Either way, the repair scope has to reflect what the city will actually let you build.</p>
<p>Elevation matters just as much. Large parts of the peninsula, James Island and West Ashley sit low, and tidal flooding now arrives on sunny days as well as in storms. That puts a lot of Charleston property in a special flood hazard area, which means two or three policies may be in play on one loss: a homeowners policy, a flood policy and, in some coastal areas, a separate wind policy from the South Carolina Wind and Hail Underwriting Association.</p>

<h2>How the storm record shows up in today’s claims</h2>
<p>Hurricane Hugo made landfall near Sullivan’s Island in September 1989 as a Category 4 storm, and its effects are still visible in Charleston’s building stock. Many homes were reroofed or rebuilt in the early 1990s, so carriers sometimes argue that damaged roofs or framing from that era were already near the end of their lives. Irma in 2017 and Idalia in 2023 were very different events: modest wind, but water in the streets. Those storms produce the classic Charleston argument over whether damage came from wind-driven rain, which a homeowners or wind policy may cover, or from rising water, which only a flood policy covers.</p>
<p>Our <a href="/appraisal-guides/wind-pool-claims-and-appraisal/">guide to wind pool claims and appraisal</a> explains how split policies interact when both carriers point at each other.</p>

<h2>Estimate disputes we see most often here</h2>
<ul>
<li><strong>Matching and continuity.</strong> Replacing one slope of a slate or metal roof, or one section of stucco, rarely produces a uniform result on a historic façade.</li>
<li><strong>Specialty trades.</strong> Plasterers, copper and slate roofers and millwork shops cost more than generic labor rates, and their availability after a storm affects price.</li>
<li><strong>Access charges.</strong> Narrow lots, tall two- and three-story elevations and steep roofs often need lifts or extra safety setup that first estimates leave out.</li>
<li><strong>Hurricane deductible triggers.</strong> Whether the percentage deductible applies depends on the policy definition and the storm’s status at the time of loss.</li>
<li><strong>Live-oak removal.</strong> Debris and tree removal sub-limits can be small next to the real cost of moving a large limb off a roof.</li>
</ul>

<h2>Documenting a Charleston loss and how we work</h2>
<p>Photograph the outside of the building from every side before any temporary repair, including the piazzas, the roof from the street, and water lines on walls or fences. Keep any correspondence with the Board of Architectural Review or city staff, because it supports material and method choices. If you have old photos or a preservation easement file showing original details, set them aside.</p>
<p>When we take an assignment, we inspect in person, measure the building ourselves and build an independent estimate rather than marking up the carrier’s. If the dispute is about scope and price, appraisal may resolve it. If it is really about coverage or a denial, we will say so, and suggest talking to a South Carolina attorney. You can read more about our <a href="/claim-dispute-services/hurricane-claim-appraisal/">hurricane claim appraisal</a> work.</p>
""",
        "faqs": [
            ("Will my insurer pay for the materials the Board of Architectural Review requires?", "It depends on your policy. Ordinance or law coverage, if you have it, may pay some of the added cost of meeting local requirements up to its limit. We separate those costs in the estimate so they can be reviewed on their own."),
            ("I have a wind policy and a homeowners policy. Who handles what?", "In parts of coastal Charleston County, wind and hail may be insured by the South Carolina Wind and Hail Underwriting Association while a homeowners policy covers other perils and flood is separate. We help sort damage by cause so each carrier sees its portion."),
            ("Can appraisal settle a flood-versus-wind argument?", "Sometimes it can value each part of the damage, but whether a peril is covered is a coverage question. If a carrier has denied part of the claim on coverage grounds, ask a South Carolina attorney before relying on appraisal alone."),
        ],
    },
    # ------------------------------------------------------------ Columbia
    {
        "slug": "columbia",
        "city": "Columbia",
        "county": "Richland & Lexington Counties",
        "region": "Midlands",
        "kw": "insurance appraiser Columbia SC",
        "title": "Columbia SC Insurance Appraisal & Claim Dispute Help",
        "desc": "Insurance appraiser in Columbia SC serving Richland & Lexington Counties. Estimate review and appraisal for flood-adjacent, hail and tree claims.",
        "h1": "Columbia, SC Insurance Appraiser for Underpaid Home Claims",
        "lede": "If you need an insurance appraiser in Columbia, SC, we review and rebuild disputed estimates for homes and businesses across Richland and Lexington Counties, from Shandon bungalows to newer houses around Lake Murray.",
        "perils": ["Hail", "Tree fall", "Water damage", "Ice storms", "Flash flooding (flood policy)"],
        "neighborhoods": ["Shandon", "Rosewood", "Melrose Heights", "Earlewood", "Elmwood Park", "Five Points", "Forest Acres", "Irmo"],
        "housing": "Older neighborhoods near downtown are full of 1920s–40s bungalows and brick cottages under mature oaks, while Lexington County and the northeast suburbs are dominated by newer vinyl and brick subdivision homes.",
        "storms": [
            "1989 · Hurricane Hugo — damaging winds reached inland across the Midlands",
            "2014 · February ice storm — fallen limbs and power lines across the region",
            "2015 · October “thousand-year” flood — dam failures and flooding along Gills Creek",
            "2021–22 · Elgin/Lugoff earthquake swarm — small quakes felt across the Columbia area",
        ],
        "near": ["aiken", "rock-hill", "florence"],
        "body": """
<h2>What sets Columbia claims apart</h2>
<p>Columbia sits well inland, but it is not short on property claims. The older neighborhoods closest to downtown, such as Shandon, Melrose Heights, Earlewood and Elmwood Park, were built mostly between the 1920s and 1940s. Many of those houses have plaster walls, original wood windows, crawlspaces and roof framing that does not line up with modern sheet sizes. The street trees that make those neighborhoods attractive are also the main cause of roof and structural damage when wind or ice comes through.</p>
<p>Farther out, in northeast Richland County and across Lexington County, the housing is newer and more uniform. Claims there tend to be about hail and wind on asphalt shingle roofs, siding and gutters, and the disputes are about how many slopes or elevations need replacing. Some of Columbia’s older districts also have design guidelines, so ask the city before changing exterior materials on a home in one of them.</p>

<h2>Storm history and what it means for a claim now</h2>
<p>Hugo is remembered as a Charleston storm, but in 1989 it kept hurricane-force gusts well inland and toppled trees across the Midlands. The February 2014 ice storm did similar damage in a quieter way: limbs coated in ice broke over roofs, decks and fences, and outages lasted for days. Those two events are why tree-fall and ice claims are familiar to Columbia adjusters.</p>
<p>The October 2015 flood is a different story. Days of record rain led to a series of dam failures, and neighborhoods along Gills Creek and other streams took serious water damage. The lasting lesson for owners is that flooding from surface water is usually excluded by homeowners policies and covered only under a separate flood policy. That makes the cause of water damage the first thing to pin down, before anyone argues over price. The 2021–22 earthquake swarm near Elgin and Lugoff was a reminder that earthquake is also typically excluded unless you bought an endorsement.</p>

<h2>Common estimate disputes in the Midlands</h2>
<ul>
<li><strong>Plaster versus drywall.</strong> Carriers often price drywall for rooms that actually have plaster on lath. The repair method and cost are different.</li>
<li><strong>Partial roof replacement.</strong> After hail, the question is whether a few repaired slopes can match the rest, or whether the whole roof needs replacing for a uniform result.</li>
<li><strong>Tree removal limits.</strong> Many policies cap debris and tree removal. Getting a large oak off a house can cost more than the cap, and the line between removal and structural repair matters.</li>
<li><strong>Code items.</strong> Older homes may need upgraded electrical, decking or ventilation once walls or roofs are opened. Whether those costs are covered depends on ordinance or law coverage.</li>
<li><strong>Water damage scope.</strong> Hidden moisture in subfloors and wall cavities is often underestimated in the first visit.</li>
</ul>
<p>Our <a href="/claim-dispute-services/claim-estimate-review/">claim estimate review</a> is a good starting point when you are not yet sure whether the gap is large enough to justify appraisal.</p>

<h2>Practical documentation and how we work locally</h2>
<p>Take photos before cleanup, including wide shots that show where a tree landed and close-ups of broken framing. After hail, photograph soft metals such as gutters, vents and window wraps, and note the date of the storm. For any water loss, record moisture readings if a mitigation company provides them and keep every invoice.</p>
<p>We inspect the property ourselves, measure it and write an independent estimate. If the disagreement is about the amount of loss, the appraisal clause in your policy may be the right path. If it is about coverage, a denial or claims handling, appraisal does not decide those questions and you should speak with a South Carolina attorney.</p>
""",
        "faqs": [
            ("My basement flooded during heavy rain. Is that a homeowners claim?", "Often not. Surface water and rising water are typically covered only by a flood policy, while water from a burst pipe or roof leak may fall under homeowners coverage. Read your declarations and exclusions, and ask your agent or a South Carolina attorney if the cause is disputed."),
            ("The adjuster priced drywall but my house has plaster walls. Can appraisal fix that?", "That is the kind of scope and pricing issue appraisal is meant to handle. We document the actual wall construction and price the proper repair method so the panel can compare like with like."),
            ("Do Lexington County and Richland County claims work differently?", "The policy and process are the same. What changes is the local housing mix, contractor pricing and, for some properties, flood-zone status, so we look at each property on its own facts."),
        ],
    },
    # ------------------------------------------------------------ Greenville
    {
        "slug": "greenville",
        "city": "Greenville",
        "county": "Greenville County",
        "region": "Upstate",
        "kw": "insurance appraiser Greenville SC",
        "title": "Greenville SC Insurance Appraiser | Hail, Wind & Trees",
        "desc": "Need an insurance appraiser in Greenville SC? Appraisal and estimate review for hail, wind and tree-fall claims across Greenville County homes.",
        "h1": "Greenville, SC Insurance Appraiser for Storm and Tree Claims",
        "lede": "We are an independent insurance appraiser for Greenville, SC property owners, focused on the hail, wind and falling-tree claims that follow Upstate storms, from mill-village cottages to new subdivisions.",
        "perils": ["Hail", "Tree fall", "Tornadoes", "Ice storms", "Freeze & burst pipes"],
        "neighborhoods": ["North Main", "Augusta Road", "Alta Vista", "Overbrook", "Hampton-Pinckney", "Monaghan Mill", "Simpsonville", "Travelers Rest"],
        "housing": "Greenville mixes early 1900s homes and mill-village cottages close to downtown with brick ranches from the 1950s–70s and large newer subdivisions toward Simpsonville, Greer and Travelers Rest.",
        "storms": [
            "2020 · April 13 tornado outbreak — an EF3 struck nearby Seneca and Oconee County",
            "2022 · January winter storm — ice and snow brought down limbs and power lines",
            "2024 · Hurricane Helene — severe wind, widespread tree fall and very long outages",
        ],
        "near": ["spartanburg", "rock-hill", "columbia"],
        "body": """
<h2>What makes Greenville property claims different</h2>
<p>Greenville County has some of the most varied housing in the state. Around North Main, Augusta Road and Alta Vista there are early twentieth-century homes with hardwood floors, plaster and detailed trim. West of downtown, former mill villages such as Monaghan and Poe Mill have small frame cottages on piers, many of them renovated in stages over decades. Toward Simpsonville, Greer and Travelers Rest, the picture changes to newer subdivision homes with complex roof lines and engineered siding.</p>
<p>All of that sits under a heavy hardwood canopy. Oaks, poplars and pines over older neighborhoods are beautiful until a storm saturates the ground and pushes them over. Historic districts such as Hampton-Pinckney also come with design review, which can affect the materials allowed on a visible repair.</p>

<h2>How recent storms show up in Upstate claims</h2>
<p>Hurricane Helene in September 2024 was the defining event for the Upstate. By the time it reached the region it was no longer a coastal storm, but it brought severe wind and an enormous amount of tree fall across Greenville County, with outages that lasted well over a week for many households. Claims from Helene often include roof and framing damage from trees, damaged fences and outbuildings, food spoilage and, where power stayed off, frozen or failed equipment. Many also involve the hurricane deductible question, because whether a percentage deductible applies depends on how the policy defines the triggering event.</p>
<p>Spring storms are the other constant. The April 2020 tornado outbreak produced an EF3 in nearby Seneca, and hail is a recurring spring hazard across the Upstate. Winter storms, including the January 2022 ice and snow, add limb damage and burst pipes.</p>

<h2>Estimate disputes we see in Greenville County</h2>
<ul>
<li><strong>Hail on shingles and soft metals.</strong> Carriers sometimes accept dents to gutters and vents but deny functional damage to the roof covering. Test squares, photos and storm dates all matter.</li>
<li><strong>Roof matching.</strong> Discontinued shingles and weathered colors make a uniform repair hard, especially on newer subdivision homes with many facets.</li>
<li><strong>Tree removal and structural repair.</strong> A sub-limit may cap tree removal, but framing, decking and interior damage caused by the tree are usually separate repair items.</li>
<li><strong>Steep and high charges.</strong> Upstate homes often have steep pitches and two-story walls that call for additional labor and safety equipment.</li>
<li><strong>Older-home code items.</strong> Opening walls in a mill cottage or 1920s home can expose wiring and framing that need updating under current code.</li>
</ul>
<p>For tree-heavy losses, our <a href="/claim-dispute-services/tree-fall-ice-storm-appraisal/">tree fall and ice storm appraisal</a> page explains how we separate removal costs from repair costs.</p>

<h2>Documentation tips and how we work locally</h2>
<p>Before a tree service cuts anything, photograph the tree on the house from several angles and capture where it struck the roof and walls. Keep the tree service invoice and any notes about crane use. After hail, photograph the roof, gutters, downspouts, window screens and HVAC fins, and record the date and time of the storm. If the power was off for days, keep receipts for food, generator fuel and temporary lodging, since some policies respond to those costs.</p>
<p>We inspect in person, measure and photograph the property, and write an independent estimate built on local labor and material pricing. If the disagreement is about the amount of loss, appraisal may be the right path. If the insurer has denied coverage, appraisal is not the tool to decide that, and a South Carolina attorney is the right person to ask.</p>
""",
        "faqs": [
            ("Does my hurricane deductible apply to Helene damage in Greenville?", "It depends on the policy wording, not on how far you live from the coast. Many policies tie the deductible to a named storm or a hurricane watch or warning. Read the definition in your declarations, and ask a South Carolina attorney if the application is disputed."),
            ("The insurer paid for gutters but not the roof after hail. Is that common?", "It happens. Dented soft metals do not always mean the shingles were functionally damaged, and the reverse is also true. A careful inspection and photos tied to the storm date help an appraisal panel decide the scope."),
            ("Who pays to remove a tree that fell on my house?", "Most homeowners policies cover removal of a tree that damaged a covered structure, often subject to a sub-limit. The repairs to the house itself are usually handled separately under dwelling coverage."),
        ],
    },
    # ------------------------------------------------------------ Myrtle Beach
    {
        "slug": "myrtle-beach",
        "city": "Myrtle Beach",
        "county": "Horry County",
        "region": "Grand Strand",
        "kw": "insurance appraiser Myrtle Beach SC",
        "title": "Myrtle Beach SC Insurance Appraisal | Condo & Hurricane",
        "desc": "Insurance appraiser for Myrtle Beach SC and Horry County: appraisal for hurricane, condo, wind pool and water damage claims on the Grand Strand.",
        "h1": "Myrtle Beach, SC Insurance Appraiser for Coastal and Condo Claims",
        "lede": "An independent insurance appraiser for Myrtle Beach, SC owners of oceanfront condos, rental properties and inland homes. We value disputed hurricane, wind and water losses across Horry County and the Grand Strand.",
        "perils": ["Hurricane wind", "Storm surge (flood policy)", "River flooding", "Wind-driven rain", "Mold after water losses"],
        "neighborhoods": ["Market Common", "Carolina Forest", "Pine Lakes", "Socastee", "Surfside Beach", "North Myrtle Beach", "Murrells Inlet"],
        "housing": "Oceanfront high-rise and mid-rise condominiums line the beach, backed by older cottages and motels, golf-course communities and large newer subdivisions in Carolina Forest and along the Waccamaw.",
        "storms": [
            "1954 · Hurricane Hazel — devastated the Grand Strand, destroying many oceanfront buildings",
            "2016 · Hurricane Matthew — wind damage and inland river flooding in Horry County",
            "2018 · Hurricane Florence — record Waccamaw River flooding around Conway and Socastee",
            "2022 · Hurricane Ian — landfall near Georgetown; surge and wind damage along the Strand",
        ],
        "near": ["florence", "mount-pleasant", "charleston"],
        "body": """
<h2>Why Grand Strand claims have more moving parts</h2>
<p>A single hurricane claim in Myrtle Beach can involve four policies. An oceanfront condo owner might have an HO-6 unit policy, rely on the association’s master policy for the building, carry a wind and hail policy through the South Carolina Wind and Hail Underwriting Association, and hold flood insurance through the NFIP or a private carrier. Each policy has its own deductible, its own definitions and its own adjuster. Before anyone argues about price, someone has to work out which policy pays for which piece.</p>
<p>The housing itself adds complexity. High-rise towers along Ocean Boulevard have commercial roofing, balcony assemblies, storefront glazing and shared mechanical systems. Inland, Carolina Forest and Socastee are mostly newer wood-frame homes with vinyl siding and asphalt roofs. Golf communities around Pine Lakes and Market Common sit somewhere in between. Rental and second-home properties also raise questions about vacancy, loss of rents and who discovered the damage and when.</p>

<h2>How the storm record shapes claims today</h2>
<p>Hurricane Hazel in October 1954 remains the benchmark for the Grand Strand; it wiped out much of the oceanfront that existed at the time. More recent storms have been less dramatic on the beach but costly inland. Matthew in 2016 and especially Florence in 2018 sent rivers out of their banks for days after the rain stopped, and the Waccamaw flooding around Conway and Socastee damaged homes that had never flooded before. Many of those owners had no flood policy.</p>
<p>Hurricane Ian came ashore near Georgetown in September 2022, bringing surge and wind damage to piers and oceanfront property along the Strand. Ian claims are a good example of the wind-versus-water split: surge damage on lower floors belongs to the flood carrier, while roof, window and balcony damage from wind belongs to the wind or homeowners carrier. Our <a href="/free-claim-tools/wind-flood-damage-splitter/">wind and flood damage splitter</a> can help you think through that division before a claim is negotiated.</p>

<h2>Estimate disputes common on the Grand Strand</h2>
<ul>
<li><strong>Master policy versus unit policy.</strong> Association bylaws and the master policy decide whether cabinets, flooring and fixtures in a unit belong to the building or the owner.</li>
<li><strong>Hurricane deductibles.</strong> Percentage deductibles on high coverage limits can absorb a large share of a loss, and the trigger language varies.</li>
<li><strong>Wind-driven rain versus surge.</strong> Water inside a unit may have come through a failed slider or roof, or from rising water, and each answer points to a different policy.</li>
<li><strong>Commercial roofing and balconies.</strong> Pricing for towers depends on access, staging and specialty contractors, all of which first estimates often understate.</li>
<li><strong>Mold after delayed discovery.</strong> Second homes may sit for days before anyone sees the damage, which invites arguments about mold and mitigation limits.</li>
</ul>

<h2>Documentation advice and how we work locally</h2>
<p>If you own a rental or second home, arrange for someone to check it promptly after a storm and photograph every room, the balcony, sliders and any water lines. Request a copy of the association’s master policy and the bylaws section on insurance responsibilities. Keep a list of contacts for every policy and note claim numbers for each one.</p>
<p>We inspect in person, review the policies that apply and write an independent estimate. For associations, our <a href="/claim-dispute-services/commercial-hoa-appraisal/">commercial and HOA appraisal</a> work covers building-wide losses. Appraisal settles the amount of loss; it does not decide coverage, so if a carrier has denied part of the claim outright, talk with a South Carolina attorney.</p>
""",
        "faqs": [
            ("My condo association and I both have insurance. Who covers my unit’s floors and cabinets?", "That depends on the master policy and the association’s governing documents. Some cover original finishes; others leave everything inside the unit walls to the owner’s HO-6. We review both before valuing your portion."),
            ("My Carolina Forest home flooded from the river. Will my homeowners policy pay?", "Generally, river and surface flooding are covered only by a flood policy. Your homeowners policy may still cover other damage, such as wind damage to the roof. A South Carolina attorney can advise if coverage is disputed."),
            ("Can appraisal be used on a South Carolina wind pool claim?", "Wind and hail policies often have their own appraisal provisions. We read the policy language first, then advise whether appraisal fits the disagreement you have."),
        ],
    },
    # ------------------------------------------------------------ Spartanburg
    {
        "slug": "spartanburg",
        "city": "Spartanburg",
        "county": "Spartanburg County",
        "region": "Upstate",
        "kw": "insurance appraiser Spartanburg SC",
        "title": "Spartanburg SC Insurance Appraiser for Storm Claims",
        "desc": "Spartanburg SC insurance appraiser for Spartanburg County: appraisal and estimate review on tree-fall, hail, wind and burst-pipe home claims.",
        "h1": "Insurance Appraisal in Spartanburg, SC for Disputed Storm Damage",
        "lede": "When you need an insurance appraiser in Spartanburg, SC, we provide independent estimates and appraisal for homes and businesses across Spartanburg County, from mill villages to new homes near Boiling Springs.",
        "perils": ["Tree fall", "Hail", "Wind & tornadoes", "Ice storms", "Freeze & burst pipes"],
        "neighborhoods": ["Converse Heights", "Hampton Heights", "Duncan Park", "Drayton", "Boiling Springs", "Inman", "Duncan"],
        "housing": "Historic homes near downtown and Converse Heights sit alongside former textile mill villages such as Drayton and Beaumont, with fast-growing subdivisions in Boiling Springs, Duncan and along the I-85 corridor.",
        "storms": [
            "2020 · April 13 tornado outbreak — strong storms and tornadoes across the Upstate",
            "2022 · January winter storm — ice and snow downed limbs and power lines",
            "2024 · Hurricane Helene — severe wind and extensive tree fall; long outages",
        ],
        "near": ["greenville", "rock-hill", "columbia"],
        "body": """
<h2>What shapes Spartanburg claims</h2>
<p>Spartanburg grew on textiles, and the mill villages left behind are still a big part of the housing stock. Drayton, Beaumont and other former villages are made up of small frame houses, many on brick piers, with additions and updates layered on over the decades. Repairing one of those homes after a storm is rarely as simple as swapping a few line items, because framing sizes, siding profiles and window openings often do not match current stock.</p>
<p>Closer to downtown, Converse Heights and Hampton Heights have larger historic homes with detailed trim and plaster interiors. Out in Boiling Springs, Duncan and the I-85 corridor, the housing is newer and more uniform, and claims tend to center on roofs, siding and gutters. Across all of it, a mature hardwood and pine canopy turns any strong wind into a tree-fall event.</p>

<h2>Storm history and how it appears in claims</h2>
<p>Hurricane Helene in September 2024 changed the picture for Spartanburg County. Its winds brought down large numbers of trees, many of them onto homes, cars and outbuildings, and power was out for days or longer across much of the county. Many owners found out for the first time what their policy says about tree removal limits, other structures, spoilage and the hurricane deductible.</p>
<p>Spring and winter storms fill in the rest. The April 2020 tornado outbreak was a reminder that the Upstate sees tornadoes, and hail is a regular spring hazard. The January 2022 winter storm brought ice and snow, with limb damage and burst pipes in homes that lost heat.</p>

<h2>Estimate disputes we see in Spartanburg County</h2>
<ul>
<li><strong>Partial versus full roof replacement.</strong> After a tree strike or hail, carriers often price a repair to one area. If the shingles cannot be matched, the result may not be a uniform roof.</li>
<li><strong>Mill-house framing.</strong> Rough-sawn or full-dimension lumber and older siding profiles cost more to match than modern materials.</li>
<li><strong>Tree removal sub-limits.</strong> The cost of getting a large tree off a house, sometimes with a crane, can exceed the removal limit even when structural repairs are covered.</li>
<li><strong>Other structures.</strong> Detached garages, sheds and fences are covered under a separate limit that is often overlooked in the first estimate.</li>
<li><strong>Burst pipe water damage.</strong> Hidden water in crawlspaces and wall cavities can be underestimated, and mitigation invoices are sometimes cut without explanation.</li>
</ul>
<p>Our <a href="/appraisal-guides/when-a-tree-falls-on-your-house/">guide on what to do when a tree falls on your house</a> walks through the first days of a tree claim.</p>

<h2>Practical documentation and how we work</h2>
<p>Photograph damage before any tree is cut and before any tarp goes on, including wide shots that show where the tree came from. Keep invoices from tree services, tarping companies and mitigation crews. After hail, photograph gutters, vents, siding and window screens, and note the storm date. If the house went without power, save receipts for spoiled food and any lodging.</p>
<p>We inspect the property ourselves, measure every elevation and write an independent estimate using current local pricing. If the dispute is about scope or price, appraisal under your policy may resolve it. If it is about coverage or a denial, appraisal does not decide that question, and you should speak with a South Carolina attorney.</p>
""",
        "faqs": [
            ("A tree from my neighbor’s yard fell on my house. Whose insurance pays?", "In most cases your own homeowners policy responds to damage to your house, regardless of where the tree stood. Questions about the neighbor’s responsibility are legal ones for a South Carolina attorney."),
            ("My detached garage was crushed. Is that part of the dwelling claim?", "Usually it falls under other structures coverage, which has its own limit. We itemize it separately so it is not lost inside the main dwelling estimate."),
            ("Can you match materials on an old mill house?", "We price the materials and methods needed to restore the home to its pre-loss condition, including older lumber sizes and siding profiles, and explain the cost basis to the other side."),
        ],
    },
    # ------------------------------------------------------------ Mount Pleasant
    {
        "slug": "mount-pleasant",
        "city": "Mount Pleasant",
        "county": "Charleston County",
        "region": "Lowcountry",
        "kw": "insurance appraiser Mount Pleasant SC",
        "title": "Mount Pleasant SC Insurance Appraisal | Coastal Claims",
        "desc": "Insurance appraiser in Mount Pleasant SC, Charleston County. Appraisal for wind pool, hurricane, roof and water claims on marsh-front and newer homes.",
        "h1": "Mount Pleasant, SC Insurance Appraiser for Wind and Water Losses",
        "lede": "An independent insurance appraiser for Mount Pleasant, SC homeowners, from the Old Village to Carolina Park. We value disputed hurricane, roof and water claims on coastal and marsh-front property in Charleston County.",
        "perils": ["Hurricane wind", "Storm surge (flood policy)", "Wind-driven rain", "Roof damage", "Mold after water losses"],
        "neighborhoods": ["Old Village", "I’On", "Park West", "Carolina Park", "Snee Farm", "Belle Hall", "Hamlin Plantation"],
        "housing": "Older cottages and raised homes in the Old Village give way to traditional neighborhood designs like I’On and large planned communities such as Park West and Carolina Park, many with marsh or creek frontage.",
        "storms": [
            "1989 · Hurricane Hugo — Category 4 landfall on neighboring Sullivan’s Island",
            "2016 · Hurricane Matthew — wind, tree damage and flooding across East Cooper",
            "2017 · Hurricane Irma — storm surge and tidal flooding in low-lying areas",
            "2023 · Hurricane Idalia — tidal flooding along the harbor and creeks",
        ],
        "near": ["charleston", "summerville", "beaufort"],
        "body": """
<h2>What makes Mount Pleasant claims distinctive</h2>
<p>Mount Pleasant has grown quickly, and most of its housing was built in the past few decades. Planned communities such as Park West, Carolina Park, Belle Hall and Snee Farm are full of two-story wood-frame homes with complex roofs, fiber-cement siding and large window packages. Those details look good and cost real money to repair; a few damaged siding courses or a single window can mean disturbing a whole elevation to get a uniform result.</p>
<p>The Old Village is older and smaller in scale, with cottages and raised homes near Charleston Harbor, and the town applies extra review to visible changes in its historic district. If you own there, check with the town before replacing exterior materials. Across town, homes along Shem Creek, the marsh and the Wando River often sit in special flood hazard areas, so the line between wind and flood damage comes up in nearly every storm claim.</p>

<h2>Storm history and its effect on today’s claims</h2>
<p>Hurricane Hugo made landfall on neighboring Sullivan’s Island in 1989, and much of Mount Pleasant was rebuilt or newly built after that storm under updated codes. Since then, storms have mostly brought water rather than catastrophic wind. Matthew in 2016 brought down trees and power, Irma in 2017 pushed surge into low-lying neighborhoods, and Idalia in 2023 produced tidal flooding along the harbor and creeks.</p>
<p>Those events produce a familiar pattern: an owner finds water inside after a storm, the homeowners carrier says it was flood, and the flood carrier says it was wind-driven rain through the windows or roof. Sorting that out depends on physical evidence like water lines, damage patterns and the condition of the building envelope. Our <a href="/claim-dispute-services/wind-tornado-claim-appraisal/">wind claim appraisal</a> page describes how we document the wind portion of a loss.</p>

<h2>Common estimate disputes in Mount Pleasant</h2>
<ul>
<li><strong>Siding and window continuity.</strong> Fiber-cement siding and window packages may be discontinued or impossible to match closely, which raises the question of replacing a full elevation.</li>
<li><strong>Two-story access.</strong> Many homes need lifts or additional scaffolding to reach upper walls and steep roof sections.</li>
<li><strong>Hurricane deductibles.</strong> On higher-value homes, a percentage deductible can be large, and its trigger depends on policy wording.</li>
<li><strong>Wind pool versus homeowners coverage.</strong> Some properties carry wind and hail through the South Carolina Wind and Hail Underwriting Association with a homeowners policy that excludes wind, and the two carriers may value the same damage differently.</li>
<li><strong>Mitigation and mold.</strong> Humid conditions after a storm mean drying and mold remediation costs can grow quickly and are often capped.</li>
</ul>

<h2>How to document and how we work locally</h2>
<p>Before any cleanup, photograph water lines inside and outside the house, wet drywall, flooring and baseboards, plus the condition of windows, doors and roof. Note when you first saw water and what the weather was doing. Keep receipts for drying equipment and temporary repairs. If your home is in a homeowners association, ask whether the association has rules about exterior materials, because those can affect what the repair has to include.</p>
<p>We inspect in person, measure, and write an independent estimate. If the dispute is about the amount of loss, appraisal may resolve it efficiently. If a carrier has denied coverage, appraisal is not designed to decide that, and a South Carolina attorney can advise on your options.</p>
""",
        "faqs": [
            ("Water came in during a storm. How do I know if it is a flood claim or a wind claim?", "It depends on how the water entered. Rising water from outside is generally flood; rain blown through a damaged roof, window or wall is generally a wind or homeowners claim. Physical evidence and timing help show which happened."),
            ("Does the Old Village historic district affect my repair costs?", "It can, if visible repairs require specific materials or approval. Ordinance or law coverage, where you have it, may pay some added cost up to its limit. We itemize those costs separately."),
            ("My HOA requires a particular siding. Will my insurer pay for it?", "Policies generally pay to restore like kind and quality. HOA rules are not the same as building codes, so the answer depends on your policy. We document the existing materials carefully to support a proper match."),
        ],
    },
    # ------------------------------------------------------------ Summerville
    {
        "slug": "summerville",
        "city": "Summerville",
        "county": "Dorchester, Berkeley & Charleston Counties",
        "region": "Lowcountry",
        "kw": "insurance appraiser Summerville SC",
        "title": "Summerville SC Insurance Appraiser for Home Claims",
        "desc": "Insurance appraiser for Summerville SC homes in Dorchester, Berkeley & Charleston Counties: tree, roof, water and new-build claim disputes.",
        "h1": "Summerville, SC Insurance Appraiser for Tree, Roof and Water Claims",
        "lede": "We are an independent insurance appraiser for Summerville, SC homeowners, valuing disputed tree, roof and water claims from the historic district to new neighborhoods like Nexton and Cane Bay.",
        "perils": ["Pine tree fall", "Hurricane wind", "Heavy rain & flash flooding", "Roof damage", "Earthquake (if endorsed)"],
        "neighborhoods": ["Historic District", "Knightsville", "Legend Oaks", "Pine Forest", "Nexton", "Cane Bay", "Summers Corner"],
        "housing": "Summerville pairs a historic core of older cottages and Victorian homes under tall pines with some of the fastest-growing new subdivisions in the state, built mostly with wood framing, vinyl or fiber-cement siding and asphalt roofs.",
        "storms": [
            "1886 · Charleston earthquake — epicenter near Summerville and Middleton Place",
            "1989 · Hurricane Hugo — widespread tree fall and roof damage inland",
            "2016 · Hurricane Matthew — downed pines and power outages",
            "2024 · Tropical Storm Debby — heavy Lowcountry rain and localized flooding",
        ],
        "near": ["charleston", "mount-pleasant", "beaufort"],
        "body": """
<h2>What makes Summerville claims different</h2>
<p>Summerville calls itself the Flower Town in the Pines, and the pines are the first thing to think about with any storm claim here. Tall loblolly and longleaf pines are shallow-rooted in wet ground, and they snap or uproot in strong wind. A single tree can puncture a roof, damage framing, crush a fence and take out a screened porch in one fall.</p>
<p>The town also spans three counties and two very different kinds of housing. The historic district around Hutchinson Square has older homes, many with wood siding and original details, and the town’s Board of Architectural Review oversees visible exterior changes there. Out in Nexton, Cane Bay, Summers Corner and the other large new communities, homes are recent builds with a lot of identical components. That sounds simpler, but newer homes come with their own disputes over matching, discontinued materials and builder-grade versus actual specification.</p>

<h2>Storm history and what it means for claims</h2>
<p>Summerville has a distinctive piece of history: the 1886 earthquake that badly damaged Charleston had its epicenter near Summerville and Middleton Place. It is the reason earthquake comes up in conversations here, but most homeowners policies exclude earth movement unless you bought an earthquake endorsement or separate policy. Check your declarations rather than assuming.</p>
<p>Hurricane Hugo in 1989 caused heavy tree fall and roof damage well inland, and Matthew in 2016 repeated that pattern on a smaller scale. More recently, Tropical Storm Debby in August 2024 brought heavy rain to the Lowcountry and flooding in low spots. Those rain events raise the question every Summerville owner should know the answer to: water that enters from above because of storm damage is treated very differently from surface water that rises from the ground, which typically needs a flood policy.</p>

<h2>Common estimate disputes in Summerville</h2>
<ul>
<li><strong>Tree removal and structural repair.</strong> Removal sub-limits may be low compared with crane work, while framing and roof repairs are usually separate items under dwelling coverage.</li>
<li><strong>Matching on newer homes.</strong> Builder siding colors and shingle lines change quickly, and a patch may not blend with the rest of the house.</li>
<li><strong>Screened porches and fences.</strong> These are often underpriced or placed under the wrong coverage part.</li>
<li><strong>Historic-district materials.</strong> Where review applies, in-kind materials can cost more than standard replacements. Ordinance or law coverage may help, depending on your policy.</li>
<li><strong>Water damage scope.</strong> Slab-on-grade homes can hide moisture under flooring and behind cabinets, which drives disputes over how much to remove.</li>
</ul>
<p>To estimate how a hurricane deductible could affect your claim, try our <a href="/free-claim-tools/hurricane-deductible-calculator/">hurricane deductible calculator</a>.</p>

<h2>Documenting your loss and how we work locally</h2>
<p>Photograph the tree, the point of impact and the attic or interior before any removal begins. Keep the tree service’s invoice and note whether a crane was needed. For newer homes, find your builder’s selection sheet or closing documents listing siding, shingle and window brands, since those help prove what a proper match looks like. For water losses, keep moisture readings and photos of every room before demolition.</p>
<p>We inspect in person, measure each elevation, and write an independent estimate with current local pricing. If the disagreement is about the amount of loss, appraisal may be the efficient path. If the carrier has denied coverage, appraisal does not decide that, and you should consult a South Carolina attorney.</p>
""",
        "faqs": [
            ("Is earthquake damage covered under my Summerville homeowners policy?", "Usually not, unless you added an earthquake endorsement or bought a separate policy. Check your declarations page, and talk with your agent if you are unsure what you have."),
            ("My builder’s siding color is discontinued. Will the insurer replace the whole wall?", "It depends on the policy language and how visible the mismatch is. We document the original product and the closest available match so the question can be decided on evidence."),
            ("Does it matter which county my Summerville home is in?", "The policy terms are the same, but permitting, code requirements and flood mapping can differ between Dorchester, Berkeley and Charleston Counties, and those can affect the repair scope."),
        ],
    },
    # ------------------------------------------------------------ Rock Hill
    {
        "slug": "rock-hill",
        "city": "Rock Hill",
        "county": "York County",
        "region": "Upstate",
        "kw": "insurance appraiser Rock Hill SC",
        "title": "Rock Hill SC Insurance Appraisal for Underpaid Claims",
        "desc": "Rock Hill SC insurance appraiser for York County, including Fort Mill and Tega Cay: appraisal and estimate review for hail, wind and water claims.",
        "h1": "Insurance Appraiser in Rock Hill, SC for Hail, Wind and Water Claims",
        "lede": "An independent insurance appraiser for Rock Hill, SC and the rest of York County. We review and rebuild disputed estimates for hail, wind, tree and water losses on older homes and fast-growing new neighborhoods alike.",
        "perils": ["Hail", "Wind & tornadoes", "Tree fall", "Freeze & burst pipes", "Water damage"],
        "neighborhoods": ["Old Town", "India Hook", "Riverwalk", "Newport", "Fort Mill", "Tega Cay", "Lake Wylie"],
        "housing": "Rock Hill’s older core includes early twentieth-century homes and former mill housing, surrounded by large newer subdivisions in Fort Mill, Tega Cay, Lake Wylie and along the Catawba River.",
        "storms": [
            "1989 · Hurricane Hugo — tracked inland near Rock Hill with damaging winds",
            "2022 · January winter storm — ice and snow, downed limbs and outages",
            "2024 · Hurricane Helene — strong winds, tree fall and outages in the region",
        ],
        "near": ["columbia", "spartanburg", "greenville"],
        "body": """
<h2>What makes York County claims distinctive</h2>
<p>Rock Hill and the communities around it have grown fast. Fort Mill, Tega Cay and the Lake Wylie area have filled with new subdivisions, and Rock Hill itself keeps adding neighborhoods such as Riverwalk along the Catawba. Most of those homes are recent wood-frame builds with asphalt roofs, vinyl or fiber-cement siding and open floor plans. Closer to downtown and Winthrop University, the older parts of the city have early twentieth-century houses and former mill housing with plaster, hardwood and roof framing that predates modern standards.</p>
<p>That mix means two different kinds of disputes. On new homes the fight is usually about matching and how much of a roof or elevation to replace. On older homes it is about method: plaster versus drywall, original trim, and code upgrades once walls are opened.</p>

<h2>Storm history and how it shows up in claims</h2>
<p>Hurricane Hugo is the storm older Rock Hill residents remember. In 1989 it kept moving north after landfall and passed near Rock Hill on its way inland, bringing down trees and damaging roofs across York County. More recently, the January 2022 winter storm brought ice and snow, and Hurricane Helene in September 2024 produced strong winds, tree fall and outages across the region.</p>
<p>Spring is hail and severe-thunderstorm season across the Piedmont. Hail claims here are usually about shingles and soft metals, and the questions are whether the shingles suffered functional damage and whether repaired areas will match. When power goes out in winter, frozen and burst pipes become the main source of interior water damage.</p>

<h2>Estimate disputes we see in Rock Hill</h2>
<ul>
<li><strong>Roof replacement scope.</strong> Carriers may approve a few slopes after hail; owners often need a full roof for a uniform result. Test squares and storm data both matter.</li>
<li><strong>Siding matching.</strong> Builder siding colors fade and get discontinued, which raises the question of replacing an entire elevation.</li>
<li><strong>Overhead and profit.</strong> When a repair needs several trades to coordinate, general contractor overhead and profit may be appropriate even if the first estimate left it out.</li>
<li><strong>Burst pipe losses.</strong> Water travels through wall cavities and under flooring, and drying or tear-out is often underestimated.</li>
<li><strong>Older-home code upgrades.</strong> Electrical, framing and ventilation updates can be required once damage is opened up.</li>
</ul>
<p>Our <a href="/claim-dispute-services/roof-hail-damage-appraisal/">roof and hail damage appraisal</a> page explains how we build a roof estimate that holds up in front of an appraisal panel.</p>

<h2>Documentation tips and how we work locally</h2>
<p>After hail, photograph the roof, gutters, downspouts, vents, window screens and air-conditioning units, and write down the date and approximate time of the storm. After a pipe failure, photograph the break, standing water and every affected room before cleanup, and keep the plumber’s invoice describing the cause. If you live in a newer community, locate your builder’s list of materials, since it helps prove what the original siding and shingles were.</p>
<p>We inspect in person, measure the property and write an independent estimate using current local pricing. If the disagreement is about the amount of loss, appraisal under your policy may resolve it. If the insurer has denied coverage or there are questions about claim handling, a South Carolina attorney is the right person to ask.</p>
""",
        "faqs": [
            ("The insurer approved part of my roof after hail. Can appraisal decide the rest?", "If coverage for hail damage is accepted and the disagreement is about how much of the roof needs replacing, that is a scope question appraisal can address. We document the condition of every slope to support the estimate."),
            ("My Fort Mill home is only a few years old. Why can’t the siding be matched?", "Manufacturers update colors and profiles often, and installed siding weathers. We identify the original product and the closest available replacement so the matching question is decided on evidence."),
            ("Is a burst pipe covered?", "Sudden and accidental water from a burst pipe is often covered, but policies may exclude damage from long-term leaks or freezing in an unheated home if reasonable care was not taken. Read your policy, and ask a South Carolina attorney if coverage is disputed."),
        ],
    },
    # ------------------------------------------------------------ Hilton Head Island
    {
        "slug": "hilton-head-island",
        "city": "Hilton Head Island",
        "county": "Beaufort County",
        "region": "Lowcountry",
        "kw": "insurance appraiser Hilton Head Island SC",
        "title": "Hilton Head Island SC Insurance Appraiser for Villas",
        "desc": "Insurance appraiser for Hilton Head Island SC in Beaufort County: hurricane, tree-fall, villa and wind pool claim appraisal and estimate review.",
        "h1": "Hilton Head Island, SC Insurance Appraiser for Hurricane and Villa Claims",
        "lede": "We are an independent insurance appraiser for Hilton Head Island, SC owners of homes, villas and rental property. We value disputed hurricane, tree-fall and water claims across the island’s plantations and Beaufort County.",
        "perils": ["Hurricane wind", "Tree fall", "Storm surge (flood policy)", "Wind-driven rain", "Mold after water losses"],
        "neighborhoods": ["Sea Pines", "Palmetto Dunes", "Shipyard", "Port Royal Plantation", "Hilton Head Plantation", "Wexford", "Long Cove", "Indigo Run"],
        "housing": "Most of the island is organized into gated plantations of single-family homes, villas and condominiums, many built from the 1970s onward, with a large share used as second homes or vacation rentals.",
        "storms": [
            "1959 · Hurricane Gracie — struck the Beaufort area, with damage across the region",
            "2016 · Hurricane Matthew — massive tree loss and roof damage across the island",
            "2017 · Hurricane Irma — storm surge and tidal flooding in low-lying areas",
            "2024 · Tropical Storm Debby — heavy rain and localized flooding",
        ],
        "near": ["beaufort", "charleston", "summerville"],
        "body": """
<h2>What makes Hilton Head claims different</h2>
<p>Hilton Head Island is not one neighborhood but a set of planned communities, most of them gated plantations with their own architectural review boards. Sea Pines, Palmetto Dunes, Shipyard, Long Cove and the others set rules on exterior colors, materials and roof types. Those rules are not building codes, but they shape what a repair has to look like, and they can stretch out timelines when approvals are needed.</p>
<p>The housing is mostly single-family homes, villas and condominiums built from the 1970s onward, many of them used as second homes or vacation rentals. Villa and condo owners deal with the same split as on the Grand Strand: an association master policy for the building, an HO-6 for the unit, a wind policy that may come from the South Carolina Wind and Hail Underwriting Association, and separate flood coverage. Single-family homes under a heavy canopy of live oaks, pines and palmettos face a different risk: tree fall.</p>

<h2>How the storm record shows up in claims</h2>
<p>Hurricane Matthew in October 2016 is the storm that shaped modern claims on the island. It made landfall farther up the coast but brought strong winds to Hilton Head, and the tree loss was enormous. Roofs were punctured, pool enclosures and screened porches crushed, and debris removal went on for months. Many of the disputes from Matthew were about tree removal limits, the hurricane deductible and whether roofs could be repaired or needed replacing.</p>
<p>Older residents also remember Hurricane Gracie in 1959, which struck the Beaufort area. Irma in 2017 brought surge and tidal flooding to low-lying parts of the island, and Debby in 2024 brought heavy rain. Each of those raised the question of whether water damage was caused by wind or by flooding, which decides which policy responds. Our <a href="/appraisal-guides/hurricane-deductibles-explained/">guide to hurricane deductibles</a> explains how percentage deductibles are triggered and applied.</p>

<h2>Common estimate disputes on the island</h2>
<ul>
<li><strong>Tree removal versus repair.</strong> Removal sub-limits may be small, while roof, framing and interior repairs from a tree strike are separate dwelling items.</li>
<li><strong>Review board requirements.</strong> Plantation rules can require specific roofing or siding. Whether a policy pays for those choices depends on its wording and on matching existing materials.</li>
<li><strong>Master versus unit coverage.</strong> For villas and condos, governing documents decide who covers interior finishes, cabinets and flooring.</li>
<li><strong>Rental income.</strong> Owners of rental properties may have loss-of-rents coverage, but documenting lost bookings takes care.</li>
<li><strong>Delayed discovery.</strong> Second homes may sit for days after a storm, which leads to arguments about mold and mitigation.</li>
</ul>

<h2>Documentation advice and how we work locally</h2>
<p>If you are off-island when a storm hits, arrange for a property manager or neighbor to photograph every room, the roof, the lanai and any trees down as soon as access is allowed. Keep your plantation’s architectural guidelines and any approval letters for past work. For rentals, save booking records and cancellations. Collect every policy that might apply, including the association’s master policy if you own a villa.</p>
<p>We inspect in person, review the applicable policies and write an independent estimate. If the dispute is about the amount of loss, appraisal may be the right path. If a carrier has denied coverage, appraisal is not designed to settle that, and you should speak with a South Carolina attorney.</p>
""",
        "faqs": [
            ("Do my plantation’s architectural rules change what insurance pays?", "Not directly. Policies typically pay to restore like kind and quality, and community rules are not building codes. We document existing materials closely so that a proper match, which often satisfies the review board, is reflected in the estimate."),
            ("I own a villa. Is the roof my claim or the association’s?", "Usually the association’s master policy covers the building structure, including the roof, but governing documents vary. We review them before valuing your portion of the loss."),
            ("Can I claim lost rental income after a hurricane?", "If your policy includes fair rental value or loss-of-rents coverage, it may respond while the property cannot be rented. Booking records and cancellations are the key documents."),
        ],
    },
    # ------------------------------------------------------------ Florence
    {
        "slug": "florence",
        "city": "Florence",
        "county": "Florence County",
        "region": "Pee Dee",
        "kw": "insurance appraiser Florence SC",
        "title": "Florence SC Insurance Appraiser | Wind & Water Disputes",
        "desc": "Insurance appraiser in Florence SC for Florence County and the Pee Dee: appraisal and estimate review for wind, ice storm, tree and water claims.",
        "h1": "Florence, SC Insurance Appraiser for Pee Dee Storm Claims",
        "lede": "An independent insurance appraiser for Florence, SC and the surrounding Pee Dee. We review and rebuild disputed estimates for wind, tree, ice storm and water claims on homes, farms and businesses in Florence County.",
        "perils": ["Hurricane wind", "River flooding (flood policy)", "Ice storms", "Tree fall", "Tornadoes"],
        "neighborhoods": ["Timrod Park", "Downtown Florence", "West Florence", "Mars Bluff", "Quinby", "Timmonsville", "Darlington"],
        "housing": "Older brick and frame homes near Timrod Park and downtown sit beside mid-century ranches, newer subdivisions in West Florence, and manufactured homes and farm buildings across the rural county.",
        "storms": [
            "2014 · February ice storm — heavy ice, broken trees and long outages across the Pee Dee",
            "2016 · Hurricane Matthew — wind damage and severe inland flooding in the region",
            "2018 · Hurricane Florence — record river flooding across the Pee Dee",
        ],
        "near": ["myrtle-beach", "columbia", "summerville"],
        "body": """
<h2>What makes Pee Dee claims different</h2>
<p>Florence is the hub of the Pee Dee, and claims here reflect a mix of city and country. Near Timrod Park and downtown, older brick and frame homes have hardwood floors, plaster and large porches. West Florence has newer subdivisions with typical asphalt roofs and vinyl siding. Out in the county, around Mars Bluff, Quinby, Timmonsville and Pamplico, there are farms, outbuildings, manufactured homes and older houses on large lots, often surrounded by pines.</p>
<p>Rural properties bring their own questions. Barns, sheds and equipment buildings may fall under other structures coverage, a farm policy or not be covered at all, depending on how the property was insured. Manufactured homes often carry specialty policies with different settlement terms. Knowing which policy and which coverage part applies is the first step before arguing over price.</p>

<h2>How storm history shows up in claims</h2>
<p>The February 2014 ice storm hit the Pee Dee hard. Ice loaded pines and hardwoods until they broke, damaging roofs, porches and vehicles, and many households were without power for days. Two years later, Hurricane Matthew brought wind damage and severe inland flooding to the region in October 2016.</p>
<p>Then came Hurricane Florence in September 2018, which stalled over the Carolinas and dropped enormous amounts of rain. The rivers of the Pee Dee rose for days after the storm passed, and record flooding reached properties well away from the coast. Many affected owners had no flood policy, because they had never been in a mapped flood zone. That experience is why the first question in a Pee Dee water claim is always where the water came from: through a damaged roof, which a homeowners policy may cover, or from rising water, which generally needs a flood policy.</p>

<h2>Estimate disputes we see in Florence County</h2>
<ul>
<li><strong>Wind versus flood.</strong> After a hurricane, both wind and water can damage the same home. Careful documentation is needed to separate the two.</li>
<li><strong>Tree and debris removal.</strong> Ice storms and hurricanes leave a lot of debris, and removal limits can be small compared with the actual cleanup.</li>
<li><strong>Outbuildings and fences.</strong> Detached structures are often missed or underpriced in the first estimate.</li>
<li><strong>Manufactured home pricing.</strong> Parts and labor for manufactured homes are specialized, and generic pricing may not reflect the real cost.</li>
<li><strong>Contractor availability.</strong> After a regional event, labor and material costs rise, and estimates written using pre-storm pricing can fall short.</li>
</ul>
<p>Not sure whether your claim gap is worth pursuing? Our <a href="/free-claim-tools/claim-gap-fee-estimator/">claim gap and fee estimator</a> gives you a rough sense before you commit.</p>

<h2>Practical documentation and how we work locally</h2>
<p>Photograph every building on the property, not just the house, and include wide shots that show trees, fences and outbuildings. For water damage, photograph water lines inside and out and note the date and time water appeared. Keep receipts for tarps, generators, chainsaw work and temporary lodging. If you have a farm policy or a separate policy on a manufactured home, gather those documents too.</p>
<p>We inspect in person, measure, and write an independent estimate using current local pricing. If the dispute is about the amount of loss, appraisal may resolve it. If a carrier has denied coverage, appraisal is not the right tool to decide that, and a South Carolina attorney can advise you.</p>
""",
        "faqs": [
            ("My barn was damaged in a storm. Is it covered by my homeowners policy?", "It depends. Some barns fall under other structures coverage, but buildings used for farming or business may be excluded and need a farm or commercial policy. Check your declarations and ask your agent if you are unsure."),
            ("My home flooded during Hurricane Florence but I was not in a flood zone. Is there any coverage?", "Homeowners policies generally exclude flood regardless of flood-zone status. Wind or rain damage that entered through a damaged roof may still be covered. A South Carolina attorney can advise on any dispute."),
            ("Can you appraise a manufactured home claim?", "Yes. We price manufactured home repairs using specialized parts and labor rather than generic site-built pricing, and we read the specific policy terms that apply."),
        ],
    },
    # ------------------------------------------------------------ Beaufort
    {
        "slug": "beaufort",
        "city": "Beaufort",
        "county": "Beaufort County",
        "region": "Lowcountry",
        "kw": "insurance appraiser Beaufort SC",
        "title": "Beaufort SC Insurance Appraisal for Historic Homes",
        "desc": "Insurance appraiser for Beaufort SC and Beaufort County: appraisal for historic homes, marsh-front property, hurricane, tree and wind pool claims.",
        "h1": "Beaufort, SC Insurance Appraiser for Historic and Waterfront Property",
        "lede": "An independent insurance appraiser for Beaufort, SC owners of historic homes, waterfront property and newer houses on the Sea Islands. We value disputed hurricane, tree and water claims across Beaufort County.",
        "perils": ["Hurricane wind", "Live-oak limb fall", "Storm surge (flood policy)", "Wind-driven rain", "Mold after water losses"],
        "neighborhoods": ["The Point", "Old Commons", "Northwest Quadrant", "Mossy Oaks", "Lady’s Island", "Port Royal", "Dataw Island", "Habersham"],
        "housing": "Beaufort’s historic district holds antebellum and Victorian homes, many raised on masonry foundations with wide porches, while Lady’s Island, Port Royal and the Sea Islands have a mix of older cottages and newer homes along the marsh.",
        "storms": [
            "1959 · Hurricane Gracie — struck the Beaufort area with damaging wind",
            "2016 · Hurricane Matthew — heavy tree loss and roof damage",
            "2017 · Hurricane Irma — storm surge and tidal flooding",
            "2024 · Tropical Storm Debby — heavy Lowcountry rain",
        ],
        "near": ["hilton-head-island", "charleston", "summerville"],
        "body": """
<h2>What makes Beaufort claims different</h2>
<p>Beaufort’s historic district is one of the best preserved in the South, and owners who live in it face a specific challenge after a storm. Antebellum and Victorian homes on The Point and in the Old Commons and Northwest Quadrant are typically raised on masonry foundations, with wide porches, wood siding, tall windows and interiors finished with plaster and heart pine. Some older buildings in the area include tabby, the local mix of lime, sand and oyster shell. The city’s Historic Review Board reviews visible exterior changes, which means repairs may need approved materials and methods rather than the cheapest substitute.</p>
<p>Across the bridges, Lady’s Island, Port Royal, Dataw and the Sea Islands have a broader mix: older cottages, mid-century homes, and newer houses along the marsh and rivers. Much of that property sits low, so flood coverage, and in some areas a South Carolina Wind and Hail Underwriting Association wind policy, may be part of the picture alongside a homeowners policy.</p>

<h2>Storm history and how it shapes claims</h2>
<p>Hurricane Gracie struck the Beaufort area in September 1959, and it remains part of local memory. In more recent years, Matthew in 2016 caused the most damage, with large numbers of live oaks and pines down on homes, porches and outbuildings. Irma in 2017 brought surge and tidal flooding to low-lying areas, and Debby in 2024 dropped heavy rain.</p>
<p>Those storms produce two main kinds of disputes. Tree claims raise questions about removal limits, structural repairs and roof replacement. Water claims raise the question of cause: water driven in through a damaged roof or wall may fall under a homeowners or wind policy, while rising water typically needs a flood policy. Our <a href="/appraisal-guides/storm-damage-photo-checklist/">storm damage photo checklist</a> can help you capture the evidence that separates the two.</p>

<h2>Estimate disputes we see in Beaufort</h2>
<ul>
<li><strong>Historic materials and methods.</strong> Plaster, wood windows, heart-pine flooring and hand-milled trim cost more than modern substitutes. Ordinance or law coverage may help with review board requirements, depending on your policy.</li>
<li><strong>Porch and piazza repairs.</strong> Columns, railings, beadboard ceilings and decking are often underpriced or treated as simple carpentry.</li>
<li><strong>Raised foundations.</strong> Masonry piers and foundations may need specialty masons, and access under raised homes adds labor.</li>
<li><strong>Tree removal limits.</strong> Removing large live oaks can exceed policy sub-limits, while the repairs to the house are separate.</li>
<li><strong>Wind versus surge.</strong> Waterfront homes may show both kinds of damage, and each belongs to a different policy.</li>
</ul>

<h2>Documentation advice and how we work locally</h2>
<p>Photograph the exterior from every side, including porches, roofs, foundations and any trees down, before temporary repairs. Inside, photograph plaster cracks, water stains and wet flooring. Keep any correspondence with the Historic Review Board, along with old photos or survey records that show original details. For waterfront homes, note water lines and the time water arrived.</p>
<p>We inspect in person, measure the building ourselves and write an independent estimate that reflects the actual construction. If the dispute is about the amount of loss, appraisal may resolve it. If a carrier has denied coverage, appraisal is not the right tool to decide that, and a South Carolina attorney can advise you. Learn more about our <a href="/claim-dispute-services/home-insurance-appraisal/">home insurance appraisal</a> service.</p>
""",
        "faqs": [
            ("Does the Historic Review Board affect what my insurer pays?", "It can affect the repair scope. Ordinance or law coverage, if your policy has it, may pay some added cost of meeting local requirements up to its limit. We separate those costs so they can be reviewed on their own."),
            ("My porch was damaged by a falling oak. Is it part of the house claim?", "An attached porch is usually part of the dwelling. We price the columns, railings, ceiling and decking as the original construction requires, rather than as generic carpentry."),
            ("Can appraisal handle a claim where both wind and flood damaged my home?", "Appraisal can value the amount of damage under the policy that invokes it, but whether a peril is covered is a coverage question. If a carrier has denied part of the claim, consult a South Carolina attorney."),
        ],
    },
    # ------------------------------------------------------------ Aiken
    {
        "slug": "aiken",
        "city": "Aiken",
        "county": "Aiken County",
        "region": "Midlands",
        "kw": "insurance appraiser Aiken SC",
        "title": "Aiken SC Insurance Appraiser | Tree & Ice Storm Claims",
        "desc": "Insurance appraiser in Aiken SC for Aiken County: appraisal and estimate review on tree-fall, Helene wind, ice storm, barn and roof claims.",
        "h1": "Aiken, SC Insurance Appraiser for Tree-Fall and Storm Damage",
        "lede": "We are an independent insurance appraiser for Aiken, SC homeowners, horse-property owners and businesses. We value disputed tree-fall, wind and ice storm claims across Aiken County, from the Horse District to North Augusta.",
        "perils": ["Tree fall", "Hurricane-force wind", "Ice storms", "Hail", "Barn & outbuilding damage"],
        "neighborhoods": ["Horse District", "Downtown Aiken", "Woodside", "Houndslake", "Gem Lakes", "North Augusta", "Graniteville"],
        "housing": "Aiken combines Winter Colony estates and historic cottages near downtown, horse properties with barns and stables, golf communities like Woodside and Houndslake, and suburban subdivisions toward North Augusta.",
        "storms": [
            "2014 · February ice storm — heavy ice, massive tree damage and long outages in Aiken County",
            "2015 · October flood — record rain across the Midlands",
            "2024 · Hurricane Helene — severe wind and widespread tree fall; very long outages",
        ],
        "near": ["columbia", "summerville", "beaufort"],
        "body": """
<h2>What makes Aiken claims distinctive</h2>
<p>Aiken looks unlike any other city in South Carolina. Near downtown, the Winter Colony left behind large estates and historic cottages, and the Horse District still has unpaved streets, stables and riding trails beside Hitchcock Woods. Across the county there are horse farms with barns, fencing and arenas, golf communities such as Woodside and Houndslake, and suburban subdivisions toward North Augusta.</p>
<p>Two features dominate Aiken claims. First, the canopy: tall pines and old hardwoods cover much of the city, and they fail in ice and wind. Second, the number of outbuildings. Barns, stables, guest houses and run-in sheds are often insured under other structures coverage with a limit set as a percentage of the dwelling, and that limit may not match the real value of a large barn. Aiken’s historic districts also have design guidelines, so check with the city before changing visible materials.</p>

<h2>Storm history and how it shows up in claims</h2>
<p>The February 2014 ice storm was a turning point for Aiken County. Heavy ice brought down trees and limbs across the area, damaging roofs, barns and fences and leaving many households without power for an extended time. Ten years later, Hurricane Helene in September 2024 brought severe wind and widespread tree fall to Aiken County, with outages that lasted well over a week for many. Helene claims often combine tree damage to roofs and framing with destroyed fencing, damaged barns and spoiled food or feed.</p>
<p>The October 2015 rains that flooded much of the Midlands were another reminder that surface flooding is generally excluded by homeowners policies and needs a separate flood policy. Our <a href="/claim-dispute-services/tree-fall-ice-storm-appraisal/">tree fall and ice storm appraisal</a> page explains how we handle losses where trees did most of the damage.</p>

<h2>Estimate disputes we see in Aiken County</h2>
<ul>
<li><strong>Other structures limits.</strong> Barns and stables may be valued well below their replacement cost when the limit is tied to a percentage of the house.</li>
<li><strong>Fencing.</strong> Horse fencing such as board, wire mesh and electric runs is costly per linear foot and often underestimated.</li>
<li><strong>Tree removal and debris.</strong> Sub-limits for tree removal rarely cover the full cost after a major event, and debris often has to be cleared before repairs can start.</li>
<li><strong>Hurricane deductibles inland.</strong> Whether a hurricane deductible applies to Helene damage depends on the policy definition, not on distance from the coast.</li>
<li><strong>Historic homes.</strong> Winter Colony homes may need specialty materials and craftsmen for proper repair.</li>
</ul>

<h2>Practical documentation and how we work locally</h2>
<p>Photograph every structure on the property, not just the house, including barns, fences, arenas and run-in sheds, before any cleanup. Wide shots showing the trees that fell help establish cause. Keep invoices for tree services, generator fuel, temporary fencing and any boarding costs for horses. If you have a separate farm or equine policy, gather it with your homeowners policy.</p>
<p>We inspect in person, measure each building and write an independent estimate using current local pricing. If the dispute is about the amount of loss, appraisal may resolve it. If coverage is denied, appraisal is not designed to decide that question, and you should speak with a South Carolina attorney.</p>
""",
        "faqs": [
            ("My barn was destroyed by a falling tree. Is it covered at full value?", "It depends on the coverage part and limit. Many homeowners policies insure barns under other structures coverage with a set limit, while farm or equine operations may need separate coverage. We value the barn at actual repair or replacement cost so any shortfall is clear."),
            ("Does my hurricane deductible apply to Helene damage in Aiken?", "Possibly. The deductible usually depends on how your policy defines a hurricane or named storm event, not on how far you live from the coast. A South Carolina attorney can advise if the application is disputed."),
            ("Can you price horse fencing?", "Yes. We measure fence runs and price the actual fence type, posts and gates, rather than using generic residential fencing rates."),
        ],
    },
]
