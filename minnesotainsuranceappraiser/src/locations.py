"""Minnesota location pages.

Each entry carries its own local detail (county, neighborhoods, housing stock,
storm history and typical perils) so that every city page reads on its own.
Copy is original to this site.
"""

LOCATIONS = [
    # ------------------------------------------------------------ Minneapolis
    {
        "slug": "minneapolis",
        "city": "Minneapolis",
        "county": "Hennepin County",
        "region": "Twin Cities Metro",
        "keyword": "insurance appraiser Minneapolis",
        "title": "Insurance Appraiser Minneapolis, MN | Claim Disputes",
        "desc": "Hail, tornado or water loss in Minneapolis and the insurer’s number is too low? Get an independent appraiser who knows the city’s older homes.",
        "perils": ["Hail", "Straight-line wind", "Tornadoes", "Ice dams", "Burst pipes"],
        "near": ["saint-paul", "bloomington", "plymouth"],
        "lede": "Minneapolis claims often involve century-old houses, mature boulevard trees and condo buildings with layered policies. When the carrier’s estimate misses that reality, the appraisal clause gives you a way to contest the amount.",
        "neighborhoods": ["Longfellow", "Nokomis", "Powderhorn", "Uptown", "Northeast", "Linden Hills", "Camden", "Jordan"],
        "housing": "1910s–1920s bungalows and four-squares to newer Uptown condos",
        "storm": "May 22, 2011 North Minneapolis tornado",
        "body": """
<h2>Why Minneapolis losses get underpaid</h2>
<p>Large parts of Minneapolis were built out before 1930. Walk through Longfellow, Nokomis or Powderhorn and you’ll see block after block of craftsman bungalows and American four-squares with plaster walls, old-growth trim, built-in buffets and multi-layer roofs. Those features cost more to repair than a desk-adjusted estimate assumes, and they are exactly where we see the gap between what was paid and what the work actually costs.</p>
<p>The city also has a long hail record. Spring and early-summer storms regularly drop hail across Hennepin County, and the result is a steady stream of roof, siding, gutter and window claims. In Uptown, Northeast and along the river, condominium and apartment buildings add another layer: an association master policy, individual HO-6 policies and arguments about who owns which repair.</p>

<h2>Lessons from the 2011 North Minneapolis tornado</h2>
<p>On May 22, 2011, a tornado cut across North Minneapolis, damaging homes in Jordan, Hawthorne and neighboring areas and toppling large numbers of trees. Many owners there dealt with roof and structural damage, tree strikes and long waits for contractors. The recovery made a few points that still apply to any wind claim in the city:</p>
<ul>
<li>Older framing and masonry often need more than a like-for-like patch once they are opened up.</li>
<li>Code upgrades required by the city can add real cost, and policies treat them differently.</li>
<li>Contractor pricing spikes after a big event; an estimate built on pre-storm rates falls short.</li>
<li>Tree removal from a roof is a separate cost question from the roof repair itself.</li>
</ul>

<h2>How appraisal works on a Minneapolis claim</h2>
<p>Most Minnesota homeowner and commercial property policies include an appraisal clause. If you and your insurer agree that a loss is covered but disagree on the amount, either side can demand appraisal. Each side names an appraiser, the two appraisers try to agree, and an umpire settles whatever they can’t. Our <a href="/appraisal-process-guide/">appraisal process guide</a> walks through each step.</p>
<p>Minnesota Insurance Appraiser inspects Minneapolis properties on site. We measure, photograph and price the damage line by line with current local costs, then argue the amount with the carrier’s appraiser. We don’t take sides on coverage questions; those belong to the policy, the insurer and, if needed, an attorney.</p>
<div class="note"><b class="h">Condo owners</b>If your building’s association is also filing, read both the master policy and your unit policy before you invoke appraisal. The two may define “unit” differently, and that changes whose claim a ceiling or window belongs to.</div>

<h2>Documenting a loss in an older Minneapolis house</h2>
<p>Good documentation is what turns a disagreement into a winnable appraisal. On a century-old home, that means recording more than the obvious damage. Before anything is torn out, photograph the original trim profiles, the plaster finish, the flooring species and the roof layers visible at the edges. Keep samples of damaged materials where you can. Note the age and condition of the roof before the storm, along with any recent repairs and the receipts for them.</p>
<p>If the insurer’s adjuster has already been out, ask for the full estimate, including the photo report and roof diagram. Compare the measurements to your own; we often find missing slopes, porch roofs, dormers or garages. Ask whether the estimate includes permit fees, debris removal, protection of finished floors and the general contractor’s overhead and profit. Each of those items can be legitimate and each is commonly left out.</p>
<p>Finally, get a contractor who works on older Minneapolis homes to look at the damage. Their scope won’t settle the claim on its own, but it gives the appraisers a real-world reference point for what the repair takes.</p>

<h2>Next steps</h2>
<p>Gather your policy, the insurer’s estimate and any photos, then <a href="/contact-us/">contact us</a> for a review. For roof losses, see our <a href="/appraisal-solutions/hail-roof-appraisal/">hail and roof appraisal</a> page; for storm structure claims, see <a href="/appraisal-solutions/tornado-derecho-wind-appraisal/">tornado and wind appraisal</a>.</p>
""",
        "faqs": [
            ("Can I use appraisal if my insurer says some of the damage is old?", "Appraisal decides the amount of loss. Whether specific damage was caused by the storm is sometimes argued in appraisal and sometimes treated as a coverage issue, depending on the policy and the facts. We can tell you how that usually plays out once we see the file."),
            ("Do you charge Minneapolis homeowners for an initial look?", "Contact us with your estimate and policy and we will explain our fee structure up front before any work begins."),
        ],
    },
    # ------------------------------------------------------------ St. Paul
    {
        "slug": "saint-paul",
        "city": "St. Paul",
        "county": "Ramsey County",
        "region": "Twin Cities Metro",
        "keyword": "insurance appraiser St. Paul",
        "title": "St. Paul, MN Insurance Appraiser for Disputed Claims",
        "desc": "Ice dams, slate roofs and Victorian detail make St. Paul claims costly. We review the insurer’s estimate and represent you in appraisal.",
        "perils": ["Ice dams", "Hail", "Heavy snow load", "Wind and falling trees", "Frozen pipes"],
        "near": ["minneapolis", "woodbury", "eagan"],
        "lede": "St. Paul has some of the oldest and most detailed housing in the state, from Summit Avenue mansions to Frogtown worker cottages. Repairing that stock correctly costs more than many insurer estimates allow.",
        "neighborhoods": ["Summit Hill", "Cathedral Hill", "Highland Park", "Macalester-Groveland", "Como", "Frogtown", "Payne-Phalen", "West Seventh"],
        "housing": "1880s Victorians to postwar Highland Park ramblers",
        "storm": "December 2010 blizzard and the ice-dam winter that followed",
        "body": """
<h2>Old houses, harsh winters</h2>
<p>Summit Avenue holds one of the longest stretches of Victorian residential architecture in the country, and the streets around it in Summit Hill and Cathedral Hill are full of late-1800s homes with slate, clay tile and cedar roofs, ornate cornices and deep box gutters. Farther out, Macalester-Groveland and Highland Park mix 1910s–1930s houses with postwar ramblers, and Como and Payne-Phalen add plenty of story-and-a-half homes with tight attic space.</p>
<p>That last detail matters in winter. Poorly ventilated attics and low-slope sections are where ice dams form, and ice dams send meltwater under shingles and into plaster walls. The winter of 2010–11, which opened with a December blizzard heavy enough to collapse the Metrodome roof across the river, produced waves of ice-dam claims across Ramsey County. Similar winters will keep coming.</p>

<h2>Where St. Paul estimates fall short</h2>
<ul>
<li><strong>Specialty roofing.</strong> Slate and clay tile need trades and materials that a standard asphalt line item doesn’t capture.</li>
<li><strong>Plaster interiors.</strong> Three-coat plaster priced as drywall leaves a visible, and costly, mismatch.</li>
<li><strong>Matching trim and millwork.</strong> Original woodwork often has to be milled to profile.</li>
<li><strong>Historic district review.</strong> Properties in a heritage preservation district may need approval for exterior changes, which can affect materials and timing.</li>
<li><strong>Hidden water damage.</strong> Ice-dam leaks run inside walls long before stains appear.</li>
</ul>

<h2>Our role in the appraisal clause</h2>
<p>When the insurer accepts the claim but you can’t agree on what it’s worth, the appraisal provision in your policy lets each side pick an appraiser. Minnesota Insurance Appraiser can serve as your appraiser: we inspect the house in person, build a detailed estimate with current Twin Cities pricing, and negotiate the amount. If the two appraisers can’t settle it, an umpire decides the disputed items.</p>
<p>We also review estimates before appraisal is ever demanded. Sometimes a well-documented supplement resolves the gap without the formal process.</p>

<h2>Reading the policy before winter hits</h2>
<p>St. Paul owners should look at three parts of their policy before the snow piles up. The first is the water damage section: most policies cover sudden and accidental discharge but exclude repeated seepage over time, and insurers sometimes argue an ice-dam leak falls into the second group. The second is the ordinance or law coverage, which can pay for code-required upgrades when an older house is repaired. On a home built before modern energy and electrical codes, those upgrades can be significant. The third is the appraisal clause itself, which spells out how to make a written demand, how long each side has to name an appraiser and how the umpire is chosen.</p>
<p>Insurers doing business here are regulated by the Minnesota Department of Commerce, which publishes consumer guidance and takes complaints about claim handling. Appraisal and a complaint are separate tools: one resolves the amount of the loss, the other addresses how the claim was handled.</p>

<h2>Winter claim tips for St. Paul owners</h2>
<p>Photograph ice buildup and interior stains as soon as you see them, keep receipts for roof raking or steaming, and don’t tear out wet plaster before it’s documented. Our <a href="/appraisal-solutions/ice-dam-winter-damage-appraisal/">ice dam and winter damage</a> page explains how those losses are valued, and the <a href="/free-tools/">free tools</a> can help you organize the file. When you’re ready, <a href="/contact-us/">reach out</a>.</p>
""",
        "faqs": [
            ("Is ice dam damage covered in Minnesota?", "Many policies cover sudden water damage from ice dams, while excluding long-term seepage or the ice itself. The wording varies, so read your policy carefully. Appraisal can resolve the amount once coverage is accepted."),
            ("My insurer priced my slate roof as asphalt. What can I do?", "Ask for the basis of the estimate in writing, document the existing material, and get a qualified slate contractor’s opinion. If the carrier still won’t move, appraisal is one way to contest the amount."),
            ("Do you work on Summit Avenue and other historic homes?", "Yes. We regularly price older homes and account for materials and methods that match the original construction."),
        ],
    },
    # ------------------------------------------------------------ Rochester
    {
        "slug": "rochester",
        "city": "Rochester",
        "county": "Olmsted County",
        "region": "Southern Minnesota",
        "keyword": "insurance appraiser Rochester MN",
        "title": "Rochester MN Property Claim Appraiser | Olmsted County",
        "desc": "Independent appraisal for Rochester homeowners, condo owners and businesses facing a low insurance estimate after hail, wind or water damage.",
        "perils": ["Hail", "Flash flooding", "Severe thunderstorms", "Sewer backup", "Ice dams"],
        "near": ["mankato", "eagan", "woodbury"],
        "lede": "Rochester sits in the Zumbro River valley, where summer thunderstorms bring hail and heavy rain. We help owners across Olmsted County contest underpaid property claims through the appraisal clause.",
        "neighborhoods": ["Pill Hill (Historic Southwest)", "Kutzky Park", "Slatterly Park", "Folwell", "Northwest Rochester", "Downtown"],
        "housing": "early-1900s Pill Hill homes to 2000s subdivisions and downtown condos",
        "storm": "July 1978 Zumbro River flash flood",
        "body": """
<h2>A river city with a flood history</h2>
<p>In July 1978, intense rain sent the Zumbro River and its tributaries over their banks and flooded large parts of Rochester, causing deaths and heavy property damage. The flood led to a major flood-control project along the Zumbro and its creeks, built over the following years, which has greatly reduced river flooding in the city. Heavy storms still cause trouble, though: overwhelmed storm sewers, basement seepage and sewer backup remain common claim types.</p>
<p>Keep in mind that standard homeowner policies exclude surface flooding. Water that backs up through a drain usually falls under a separate endorsement with its own limit, so check yours before a storm, not after.</p>

<h2>Housing across Olmsted County</h2>
<p>Rochester’s housing spans more than a century. Pill Hill, in the Historic Southwest, is known for large early-1900s homes built near the Mayo Clinic, many with tile or slate roofs and custom millwork. Kutzky Park and Slatterly Park hold modest older houses, while the northwest and southeast edges of the city filled in with split-levels, two-stories and townhomes from the 1970s onward. Downtown has added a large number of apartments and condominiums.</p>
<p>Each of these brings its own pricing issues, from specialty materials in older homes to shared-wall and association questions in townhomes and condos.</p>

<h2>Typical Rochester disputes</h2>
<ul>
<li>Hail damage to roofs and siding where the insurer approves repair but you believe replacement is needed.</li>
<li>Finished basements after a backup, with flooring, drywall and contents valued too low.</li>
<li>Condominium losses split between the association and unit owners.</li>
<li>Overhead and profit left out of a job that clearly needs a general contractor.</li>
</ul>

<h2>Hail and wind on the Rochester plateau</h2>
<p>Southeastern Minnesota sits in an active corridor for summer thunderstorms. Storms that build over the open farmland west of the city can arrive with large hail and strong outflow winds, damaging roofs, siding, skylights, vehicles and HVAC units in one pass. Because the same neighborhoods are hit repeatedly, adjusters may argue that some marks predate the current storm. Dated photos, roof inspection reports from a home purchase and earlier claim records all help answer that question.</p>
<p>Commercial buildings and medical-office properties near downtown add flat and low-slope roofs to the mix. Those systems are often priced on a square-foot basis that ignores tapered insulation, flashing details or the cost of working around rooftop equipment. An illustrative example: if an estimate allows membrane replacement but omits the insulation beneath a saturated area, the gap can be a large share of the total. We check each layer before forming an opinion on the amount.</p>

<h2>Working with Minnesota Insurance Appraiser</h2>
<p>We travel to Rochester and the surrounding Olmsted County communities to inspect losses in person. If your policy’s appraisal clause applies, we can serve as your appraiser, prepare a detailed estimate and negotiate the amount with the insurer’s appraiser, with an umpire available to resolve any remaining gap. You can read more in our <a href="/appraisal-process-guide/">guide to the process</a>.</p>
<p>If your dispute involves water, visit our <a href="/appraisal-solutions/water-damage-appraisal/">water damage appraisal</a> page. For associations and commercial buildings near downtown, see <a href="/appraisal-solutions/commercial-hoa-appraisal/">commercial and HOA appraisal</a>. Questions about your file? <a href="/contact-us/">Contact us</a>.</p>
""",
        "faqs": [
            ("Does appraisal help with a flood claim in Rochester?", "Appraisal only applies to covered losses. If your damage comes from surface flooding, it is generally covered by flood insurance rather than a homeowner policy, and that policy has its own dispute process. Sewer backup under an endorsement can often go to appraisal."),
            ("Do you inspect outside Rochester city limits?", "Yes. We serve owners across Olmsted County and the rest of southeastern Minnesota."),
        ],
    },
    # ------------------------------------------------------------ Duluth
    {
        "slug": "duluth",
        "city": "Duluth",
        "county": "St. Louis County",
        "region": "Northeast & Arrowhead",
        "keyword": "insurance appraiser Duluth",
        "title": "Duluth Insurance Appraiser – Lake Superior Claims, MN",
        "desc": "Duluth hillside homes, North Shore cabins and Lake Superior storms create hard claims. Get an appraiser on your side when the estimate falls short.",
        "perils": ["Flash flooding and erosion", "Heavy snow and ice dams", "Lake Superior wind", "Frozen pipes", "Falling trees"],
        "near": ["st-cloud", "blaine", "minneapolis"],
        "lede": "Duluth climbs steeply from Lake Superior, and its older homes take the brunt of lake wind, deep snow and fast-moving runoff. We help owners in the city and up the North Shore contest low claim estimates.",
        "neighborhoods": ["Lakeside", "Lester Park", "Congdon Park", "Chester Park", "Lincoln Park", "Park Point", "Woodland", "Duluth Heights"],
        "housing": "1890s–1920s hillside homes to North Shore cabins",
        "storm": "June 2012 flash flood",
        "body": """
<h2>Building on a hillside above the lake</h2>
<p>Much of Duluth was built in the late 1800s and early 1900s, when the port and the iron range drove fast growth. Congdon Park and Lakeside have large period homes with masonry, stucco and slate; Lincoln Park and the Central Hillside have tightly packed frame houses on steep lots. Park Point sits on a narrow sandbar exposed to the open lake. Outside the city, St. Louis County and the North Shore are dotted with cabins and seasonal homes that may sit empty for weeks at a time.</p>
<p>Steep grades, dozens of creeks running downhill to the lake and deep winter snow give Duluth a set of perils you don’t see as often in the southern part of the state.</p>

<h2>What the June 2012 flood showed</h2>
<p>In June 2012, record rainfall overwhelmed creeks and storm sewers across Duluth. Roads washed out, hillsides gave way and many basements flooded. The event also showed how insurance claims sort themselves after water: sewer backup endorsements paid some losses, flood policies paid others, and earth movement exclusions came up for damage tied to slides and washouts.</p>
<p>Those coverage questions have to be answered before appraisal can begin. Once a loss is accepted, though, the size of the payment is often the real fight.</p>

<h2>Arrowhead claims we see most</h2>
<ul>
<li>Ice dam leaks on older homes with complex rooflines and limited insulation.</li>
<li>Snow-load and wind damage to cabins, garages and outbuildings.</li>
<li>Frozen and burst pipes in seasonal properties.</li>
<li>Masonry and stucco repairs priced too low for the hillside access they require.</li>
<li>Higher labor and travel costs for remote North Shore sites that the estimate ignores.</li>
</ul>
<div class="note"><b class="h">Seasonal homes</b>Many policies limit coverage for freezing in a vacant or unheated building unless heat was maintained or water was shut off. Check that language before winter.</div>

<h2>Pricing repairs in the Northland</h2>
<p>Construction costs in Duluth and the Arrowhead don’t always track Twin Cities pricing. Specialty trades such as slate roofers, stone masons and plasterers may have to travel, and after a regional storm the local contractor pool fills up fast. The short building season also matters: exterior work that can’t be done before freeze-up may need temporary protection through winter, and that cost belongs in the estimate.</p>
<p>Hillside access adds its own expense. Scaffolding on a steep lot, material hoisting to a house with no driveway access to the rear and staging on narrow streets all take time and labor. A desk estimate that assumes flat-lot conditions will miss them. On the North Shore, travel time, lodging for crews and delivery charges can apply to remote cabins. We price these items specifically rather than relying on default percentages, and we explain the basis for each one so the insurer’s appraiser can follow the math.</p>

<h2>Our approach in Duluth</h2>
<p>Minnesota Insurance Appraiser comes to the property, whether that’s a house on the hillside or a cabin past Two Harbors. We document the damage, price it with current regional costs and present the amount in appraisal if your policy allows it. If a winter loss is the issue, see our <a href="/appraisal-solutions/ice-dam-winter-damage-appraisal/">ice dam and winter damage appraisal</a> page, or start with a <a href="/contact-us/">quick message</a>.</p>
""",
        "faqs": [
            ("Do you travel to North Shore cabins?", "Yes. We inspect properties in Duluth and along the North Shore and elsewhere in the Arrowhead. Remote sites may take a little more scheduling."),
            ("My Duluth basement flooded in a storm. Is that an appraisal issue?", "It depends on the source. Sewer backup under an endorsement can often go to appraisal once accepted. Surface water is usually a flood insurance matter with its own process."),
        ],
    },
    # ------------------------------------------------------------ Bloomington
    {
        "slug": "bloomington",
        "city": "Bloomington",
        "county": "Hennepin County",
        "region": "Twin Cities Metro",
        "keyword": "insurance appraiser Bloomington MN",
        "title": "Bloomington, MN Appraiser for Hail & Storm Claims",
        "desc": "Rambler roofs, lake-area homes and commercial property near the Mall of America. Independent appraisal for Bloomington insurance disputes.",
        "perils": ["Hail", "Wind", "Ice dams", "Water damage", "Sewer backup"],
        "near": ["minneapolis", "eagan", "plymouth"],
        "lede": "Bloomington grew fast in the 1950s and 1960s, and many of those ramblers are now on their second or third roof. When hail or wind brings a claim and the payment comes up short, we can help.",
        "neighborhoods": ["Normandale Lake", "Hyland Hills", "Oxboro", "Penn-American District", "South Loop", "West Bloomington", "Smith Park"],
        "housing": "1950s–1960s ramblers and split-levels to newer South Loop apartments",
        "storm": "June 14, 1981 tornado next door in Edina",
        "body": """
<h2>A postwar suburb with aging roofs</h2>
<p>Bloomington boomed after the Second World War, and most of the east side and much of the west side were built between the early 1950s and the 1970s. Single-story ramblers and split-levels with attached garages make up the bulk of the city’s housing. Many have finished lower levels, low-slope additions and roofs that have been replaced more than once. Around Normandale Lake and Hyland Hills, larger lots carry bigger two-stories built in later decades.</p>
<p>The east end of the city looks different. The South Loop district around the Mall of America, along with the Penn-American area near I-494, holds hotels, offices, retail and newer apartment buildings, all with their own commercial insurance programs.</p>

<h2>Storm exposure in the south metro</h2>
<p>Bloomington shares the metro’s hail exposure, and the city sits close to past tornado paths: on June 14, 1981, a tornado touched down in neighboring Edina and tracked northeast through south Minneapolis. Today the claims that come through most often are hail and wind damage to roofs, siding, gutters and garage doors, followed by ice dams in winter and water losses in finished basements.</p>

<h2>Common sticking points</h2>
<ul>
<li>Roof slopes, waste and ventilation measured incorrectly from aerial images.</li>
<li>Repair-only estimates on brittle older shingles that can’t be repaired without more damage.</li>
<li>Siding replacement limited to one elevation when the product no longer matches.</li>
<li>Commercial roof losses where depreciation and code costs are disputed.</li>
</ul>
<p>Disagreements like these are about the amount of the loss, which is what the appraisal clause is designed to settle.</p>

<h2>What to gather before calling an appraiser</h2>
<p>A little preparation makes the first review much faster. Pull together the complete policy, including the declarations page and every endorsement, since sewer backup, ordinance or law and roof payment schedules all live in endorsements. Add the insurer’s estimate and any letters explaining what was paid or denied. If you’ve had a contractor out, include their written scope and photos. Note the age of the roof and siding, and any prior claims on the property.</p>
<p>For a rambler, it also helps to know whether the roof has one layer or two, whether the attic has been reinsulated and whether gutters and downspouts were replaced with the last roof. Those details affect the price of a replacement and are often missing from a first estimate. On commercial property, gather the building’s roof warranty, maintenance records and any engineering reports. With that in hand, we can usually tell you quickly whether the difference between your number and the insurer’s is worth pursuing through appraisal.</p>

<h2>Residential and commercial help</h2>
<p>Minnesota Insurance Appraiser inspects Bloomington homes and businesses on site, writes a detailed estimate and represents you as your appraiser. For roof disputes, see our <a href="/appraisal-solutions/hail-roof-appraisal/">hail and roof appraisal</a> page. Property managers, associations and business owners near the South Loop can start with <a href="/appraisal-solutions/commercial-hoa-appraisal/">commercial and HOA appraisal</a>. Insurers in Minnesota are regulated by the Minnesota Department of Commerce, which is also where you can file a complaint if you believe a claim is being mishandled.</p>
<p>Ready for a second opinion? <a href="/contact-us/">Get in touch</a>.</p>
""",
        "faqs": [
            ("My Bloomington rambler’s roof was only approved for repair. Can that be appraised?", "Often yes. Whether hail damage requires a few shingles or a full roof is a question about the amount of loss, and it is one of the most common issues taken to appraisal."),
            ("Do you handle commercial property near the Mall of America?", "We work with commercial owners and managers throughout Bloomington, including offices, retail and multifamily buildings."),
        ],
    },
    # ------------------------------------------------------------ Plymouth
    {
        "slug": "plymouth",
        "city": "Plymouth",
        "county": "Hennepin County",
        "region": "Twin Cities Metro",
        "keyword": "insurance appraiser Plymouth MN",
        "title": "Plymouth MN Insurance Appraisal | Hail, Roof & HOA",
        "desc": "Plymouth homeowners and townhome associations: if your hail or wind settlement doesn’t cover the repair, an independent appraiser can help.",
        "perils": ["Hail", "Severe wind", "Ice dams", "Water damage", "Lightning"],
        "near": ["minneapolis", "bloomington", "blaine"],
        "lede": "Plymouth’s 1980s and 1990s two-stories and its many townhome associations see their share of west-metro hail. We help owners and boards contest roof, siding and water claims that come in low.",
        "neighborhoods": ["Medicine Lake", "Parkers Lake", "Bass Lake", "Schmidt Lake", "Plymouth Creek", "Elm Creek area"],
        "housing": "1970s split-levels to 1990s–2000s two-stories and townhomes",
        "storm": "May 15, 1998 Twin Cities hailstorm",
        "body": """
<h2>The hail problem in the west metro</h2>
<p>Hail is the claim that defines Plymouth. Spring and summer storms move across western Hennepin County regularly, and the Twin Cities hailstorm of May 15, 1998, remains one of the costliest in state history. Since then, waves of smaller events have kept roofers busy, and many neighborhoods have had more than one hail claim in the past two decades. That history leads to familiar arguments about prior damage and whether a roof can still be repaired.</p>

<h2>Plymouth homes and associations</h2>
<p>Most of Plymouth was developed from the 1970s through the early 2000s. Around Parkers Lake and Medicine Lake you’ll find older split-levels and lakeside homes; around Bass Lake, Schmidt Lake and the Plymouth Creek area, larger two-stories with steep, cut-up rooflines, architectural shingles and fiber cement or vinyl siding. The city also has a large number of townhome communities, where the association often insures roofs and exteriors under one master policy.</p>
<h3>What makes HOA claims different</h3>
<p>An association claim may cover dozens of buildings at once. Small per-building errors in measurement or pricing add up quickly, and boards have to balance owner expectations with what the carrier will pay. The governing documents also matter, since they spell out what the association insures and what falls to each owner.</p>

<h2>Disputes we review in Plymouth</h2>
<ul>
<li>Steep and complex roofs priced without steep-slope or high-roof labor.</li>
<li>Discontinued shingle or siding colors with no matching option.</li>
<li>Gutters, downspouts, window wraps and screens left out of the scope.</li>
<li>Association claims where some buildings were approved and others denied for the same storm.</li>
</ul>

<h2>Timing matters after a hail storm</h2>
<p>Hail damage isn’t always obvious from the ground. Bruised shingles, cracked seals and dented metal can take a trained eye to spot, and some damage only shows up as granule loss weeks later. Plymouth owners sometimes wait until a leak appears, by which point the insurer may question when the damage happened. Most policies require prompt notice of a loss and may limit how long you have to file suit, so report storm damage soon after you notice it.</p>
<p>Once a claim is open, keep a simple log: dates of inspections, who attended, what was said and what documents you received. If the insurer issues a partial payment, cash it if you need to start repairs, but keep track of what it covers. A first payment doesn’t end the claim, and appraisal can still be demanded if the amount remains in dispute. For an association, the board should appoint one contact person so that communications with the carrier, the contractor and the appraiser stay consistent.</p>

<h2>Bringing in an appraiser</h2>
<p>If the insurer has accepted coverage and the dispute is over dollars, the appraisal clause lets you name your own appraiser. Minnesota Insurance Appraiser inspects every roof and elevation in person, prices the work with current local costs and negotiates directly with the carrier’s appraiser. See <a href="/appraisal-solutions/hail-roof-appraisal/">hail and roof appraisal</a> or, for boards, <a href="/appraisal-solutions/commercial-hoa-appraisal/">commercial and HOA appraisal</a>.</p>
<p>Illustrative example: an insurer approves repairs to two slopes on a ten-slope roof. If the remaining slopes show the same hail pattern, the appraisers would measure and price the full roof and argue the difference. Every claim is different, so we look at the facts before giving an opinion. <a href="/contact-us/">Send us your estimate</a>.</p>
""",
        "faqs": [
            ("Can a townhome association invoke appraisal for all its buildings at once?", "Usually the association’s master policy covers the buildings under one claim, and appraisal can address the full loss. The policy wording controls, so we review it first."),
            ("My insurer says the hail hit my roof in an earlier storm. What now?", "Gather records of prior claims, roof age and any inspection reports. Whether damage is new is sometimes decided in appraisal and sometimes treated as coverage, depending on the policy."),
        ],
    },
    # ------------------------------------------------------------ Woodbury
    {
        "slug": "woodbury",
        "city": "Woodbury",
        "county": "Washington County",
        "region": "Twin Cities Metro",
        "keyword": "insurance appraiser Woodbury MN",
        "title": "Woodbury, MN Claim Appraiser – Washington County",
        "desc": "Newer Woodbury homes and HOA communities still get underpaid after hail and wind. See how the appraisal clause can settle a claim dispute.",
        "perils": ["Hail", "Wind", "Tornadoes", "Ice dams", "Water damage"],
        "near": ["saint-paul", "eagan", "blaine"],
        "lede": "Woodbury is one of the fastest-growing cities in the east metro, with newer subdivisions and many association-managed neighborhoods. New construction doesn’t mean simple claims, and we help owners push back on low estimates.",
        "neighborhoods": ["Colby Lake", "Eagle Valley", "Prestwick", "Stonemill Farms", "City Place", "Dancing Waters", "Wedgewood"],
        "housing": "1980s split-entries to 2010s two-stories and townhomes",
        "storm": "May 25, 2008 Hugo tornado in northern Washington County",
        "body": """
<h2>Growth and storm exposure in Washington County</h2>
<p>Woodbury went from farm fields to one of Minnesota’s larger suburbs in a few decades. Early neighborhoods near Colby Lake and the city’s north end date to the late 1970s and 1980s; Eagle Valley, Prestwick and Stonemill Farms came later, and new homes continue to rise in the south. Much of the city is governed by homeowner or townhome associations that set exterior standards.</p>
<p>The east metro gets the same spring and summer thunderstorms as the rest of the Twin Cities, and Washington County has seen serious tornado damage. On May 25, 2008, a tornado struck Hugo in the northern part of the county, destroying and damaging dozens of homes. Hail and straight-line wind are far more frequent and account for most local claims.</p>

<h2>Newer homes, different disputes</h2>
<p>A newer house can mean a simpler repair, but it can also mean pricier materials and stricter matching rules. Here’s what tends to come up:</p>
<ul>
<li><strong>Architectural and designer shingles</strong> that cost more than the base product in the estimate.</li>
<li><strong>Fiber cement and engineered siding</strong> with specific installation and trim requirements.</li>
<li><strong>Association standards</strong> that require a uniform look across a street or building.</li>
<li><strong>Large window packages</strong> where a single damaged unit can’t be matched.</li>
<li><strong>Finished lower levels</strong> damaged by water, with costly flooring and built-ins.</li>
</ul>

<h2>Is appraisal the right tool?</h2>
<p>Appraisal works best when the insurer has accepted the claim and the disagreement is about scope or price. It doesn’t resolve whether a loss is covered in the first place. If you’re unsure which you’re facing, our <a href="/appraisal-process-guide/">appraisal process guide</a> lays out the difference, and our <a href="/free-tools/">free claim tools</a> can help you compare estimates.</p>

<h2>The matching question</h2>
<p>Few issues come up more in Woodbury than matching. A hailstorm damages one or two elevations of siding, the insurer approves those walls, and the replacement product doesn’t match the rest of the house because the color has faded or the line has been discontinued. Whether the insurer must pay to replace undamaged walls for a uniform look depends on the policy wording and Minnesota law, and how that applies to a given house is very much a question of fact.</p>
<p>In practice, the appraisers look at whether a match is available, how visible the transition would be and whether the elevations are separated by corners or other natural breaks. Association rules may also come into play if they require a uniform look. Photos of every elevation, the product name and color if you have them, and a supplier’s statement that the product is discontinued are all useful evidence. We handle these questions regularly and price the full scope that a uniform result requires.</p>

<h2>Serving Woodbury and the east metro</h2>
<p>Minnesota Insurance Appraiser serves Woodbury, Cottage Grove, Lake Elmo, Stillwater and the rest of Washington County. We inspect in person, write our own estimate and represent you in the appraisal process. For roof and siding losses, see <a href="/appraisal-solutions/hail-roof-appraisal/">hail and roof appraisal</a>; for wind events, <a href="/appraisal-solutions/tornado-derecho-wind-appraisal/">tornado and derecho appraisal</a>. When you’re ready, <a href="/contact-us/">contact us</a>.</p>
""",
        "faqs": [
            ("Does my HOA’s architectural rule affect what my insurer has to pay?", "Association rules alone don’t change your policy, but they can affect what a reasonable repair looks like and whether matching is required. The policy language and the facts both matter."),
            ("Do you serve other Washington County cities?", "Yes. We work throughout Washington County, including Cottage Grove, Lake Elmo, Stillwater, Forest Lake and Hugo."),
        ],
    },
    # ------------------------------------------------------------ Eagan
    {
        "slug": "eagan",
        "city": "Eagan",
        "county": "Dakota County",
        "region": "Twin Cities Metro",
        "keyword": "insurance appraiser Eagan MN",
        "title": "Eagan MN Insurance Appraiser for Underpaid Claims",
        "desc": "Split-levels, ramblers and townhomes in Eagan face hail, snow load and ice dams. An appraiser can dispute your insurer’s low estimate.",
        "perils": ["Hail", "Heavy snow and ice dams", "Wind", "Water damage", "Sewer backup"],
        "near": ["bloomington", "saint-paul", "woodbury"],
        "lede": "Eagan’s split-levels, ramblers and townhomes are now old enough that roofs, siding and plumbing all start to show their age. When a storm adds damage and the claim comes up short, we can step in.",
        "neighborhoods": ["Cedar Grove", "Thomas Lake", "Blackhawk Lake", "Lexington-Diffley", "Cliff Lake", "Lebanon Hills area"],
        "housing": "1970s–1980s split-levels to 1990s townhomes",
        "storm": "Halloween 1991 blizzard",
        "body": """
<h2>Eagan’s housing at a glance</h2>
<p>Eagan grew quickly in the 1970s and 1980s as I-35E and I-494 opened up northern Dakota County. Split-level and split-entry houses dominate many neighborhoods around Cedar Grove and Thomas Lake, with ramblers and larger two-stories near Blackhawk Lake and the parkland around Lebanon Hills. The city also has a large share of townhomes and condominiums, many governed by associations that insure the exteriors.</p>
<p>Split-levels have their own repair quirks: multiple roof planes at different heights, partially below-grade lower levels prone to water intrusion, and siding that wraps several elevations.</p>

<h2>Snow, ice and hail in Dakota County</h2>
<p>The Halloween blizzard of 1991 buried the Twin Cities under more than two feet of snow in a matter of days, still a benchmark for heavy early-season storms. Big snow years bring roof-load damage, collapsed gutters and ice dams. In the warm season, hail and wind take over. Many Eagan roofs have been replaced after hail at least once, and adjusters sometimes argue that new damage is old.</p>

<h2>Ways an Eagan claim goes sideways</h2>
<ul>
<li>Each split-level roof plane measured separately and some slopes skipped.</li>
<li>Lower-level water damage limited to drywall when flooring and cabinetry are also affected.</li>
<li>Sewer backup paid up to a low endorsement limit without a full accounting of the loss.</li>
<li>Association buildings approved one at a time instead of as a single storm event.</li>
<li>Depreciation taken at rates that don’t match the actual age of the roof.</li>
</ul>

<h2>Depreciation and replacement cost</h2>
<p>Many Eagan homeowners are surprised by the first check after a claim. Most policies pay replacement cost, but they often pay actual cash value first, holding back depreciation until the repairs are done. If the insurer has applied too much depreciation, or has used the wrong age for the roof or siding, that first check will be too low, and the work itself may be harder to start.</p>
<p>Depreciation is part of the amount of loss, which makes it a proper subject for appraisal. The appraisers can consider the actual age and condition of the materials, what the remaining useful life was before the storm and whether certain items, such as labor, should be depreciated under the policy wording. An illustrative example: a fifteen-year-old roof depreciated as if it were twenty-five years old would leave a meaningful gap between the first payment and a fair actual cash value. Records showing the roof installation date, such as a permit or invoice, help settle that argument.</p>

<h2>How we help</h2>
<p>Minnesota Insurance Appraiser reviews your policy and the insurer’s estimate, then inspects the property in person. If the appraisal clause applies and you choose to use it, we act as your appraiser: we prepare a detailed estimate, meet with the insurer’s appraiser and work toward an agreed award, with an umpire if needed.</p>
<p>Learn more about <a href="/appraisal-solutions/ice-dam-winter-damage-appraisal/">winter damage appraisal</a>, <a href="/appraisal-solutions/water-damage-appraisal/">water damage appraisal</a> and <a href="/appraisal-solutions/hail-roof-appraisal/">hail claims</a>, or <a href="/contact-us/">ask us to review your file</a>.</p>
""",
        "faqs": [
            ("Can appraisal fix a sewer backup claim that hit my endorsement limit?", "Appraisal can determine the full amount of the loss, but payment is still capped by your endorsement limit. If the loss exceeds the limit, appraisal won’t raise it."),
            ("Do you work in Apple Valley, Burnsville and Inver Grove Heights too?", "Yes. We serve Eagan and the rest of Dakota County."),
        ],
    },
    # ------------------------------------------------------------ Blaine
    {
        "slug": "blaine",
        "city": "Blaine",
        "county": "Anoka County",
        "region": "Twin Cities Metro",
        "keyword": "insurance appraiser Blaine MN",
        "title": "Blaine, MN Storm Claim Appraiser | Anoka County",
        "desc": "Blaine homeowners with tornado, hail or wind claims: an independent appraiser can review the insurer’s estimate and represent you in appraisal.",
        "perils": ["Hail", "Tornadoes", "Straight-line wind", "Ice dams", "Frozen pipes"],
        "near": ["plymouth", "woodbury", "st-cloud"],
        "lede": "Anoka County has a long tornado and hail history, and Blaine’s mix of 1970s homes and newer developments sees plenty of storm claims. We help owners contest settlements that don’t cover the work.",
        "neighborhoods": ["The Lakes", "Club West", "Laddie Lake", "Lexington Avenue corridor", "Paul Parkway area", "Northtown area"],
        "housing": "1960s–1970s ramblers to 2000s two-stories",
        "storm": "May 6, 1965 Fridley tornadoes",
        "body": """
<h2>Tornado country in the north metro</h2>
<p>On May 6, 1965, a series of tornadoes struck the northern Twin Cities, with Fridley and neighboring Anoka County communities among the hardest hit. Hundreds of homes were damaged or destroyed. More than half a century later, Anoka County still sees regular severe weather: hail, straight-line winds and the occasional tornado. In May 2008, a tornado tore through Hugo, just east of the county line, a reminder that the risk hasn’t gone away.</p>

<h2>Blaine’s housing mix</h2>
<p>Blaine’s older neighborhoods in the south part of the city, near Northtown and along University and Central Avenues, were built mainly in the 1960s and 1970s and consist largely of ramblers, split-entries and small two-stories. North of 109th Avenue, developments such as The Lakes and Club West added larger homes from the 1990s through the 2010s, often with association covenants. Townhome communities are spread throughout.</p>
<h3>Older homes</h3>
<p>Older Blaine houses often have multiple roof layers, aluminum or steel siding no longer made, and original windows. Matching is often the main dispute.</p>
<h3>Newer homes</h3>
<p>Newer homes bring steep, complex roofs and premium siding and stone accents, all of which push repair costs above a basic estimate.</p>

<h2>Where we focus on Blaine claims</h2>
<ul>
<li>Wind claims where uplift and creasing are dismissed as wear.</li>
<li>Hail claims limited to soft metals without a full roof inspection.</li>
<li>Siding that can’t be matched, leaving mismatched elevations.</li>
<li>Tree-strike claims where removal and structural repairs are lumped together.</li>
</ul>
<div class="note"><b class="h">After a tornado or derecho</b>Protect the property from further damage, document everything before cleanup and keep receipts for emergency work. Those costs are often part of the claim.</div>

<h2>What appraisal can and can’t do</h2>
<p>Appraisal is a focused tool. It decides the amount of loss: the scope of covered damage and what it costs to repair. It doesn’t decide whether your policy covers a peril, whether an exclusion applies or whether the insurer acted in bad faith. Those questions go to the insurer, the Minnesota Department of Commerce or the courts.</p>
<p>Within its lane, appraisal can be faster and less expensive than litigation. Each side pays its own appraiser, and the umpire’s fee is usually split. An agreement signed by any two of the three, either both appraisers or one appraiser and the umpire, typically sets the amount. For Blaine homeowners with a wind or hail claim where the insurer agrees there’s damage but offers too little, that structure often works well. For claims where coverage itself is denied, talk to an attorney first. We’re glad to tell you which category your claim seems to fall into after reviewing the file.</p>

<h2>Help for Anoka County owners</h2>
<p>Minnesota Insurance Appraiser comes to the property, builds an independent estimate and represents you if you invoke appraisal. We serve Blaine, Coon Rapids, Ham Lake, Lino Lakes, Andover and the rest of Anoka County. See <a href="/appraisal-solutions/tornado-derecho-wind-appraisal/">tornado and wind appraisal</a> or <a href="/appraisal-solutions/hail-roof-appraisal/">hail and roof appraisal</a>, or <a href="/contact-us/">reach out</a> with your estimate.</p>
""",
        "faqs": [
            ("What’s the difference between tornado and straight-line wind for insurance purposes?", "For most homeowner policies, both fall under windstorm coverage. The difference matters more for how damage is documented than whether it is covered."),
            ("Can I invoke appraisal if my insurer hasn’t finished the claim yet?", "Appraisal is usually available once there is a disagreement over the amount. Many policies also set deadlines for lawsuits, so don’t wait too long. Read your policy or ask a lawyer about timing."),
        ],
    },
    # ------------------------------------------------------------ St. Cloud
    {
        "slug": "st-cloud",
        "city": "St. Cloud",
        "county": "Stearns County",
        "region": "Central Minnesota",
        "keyword": "insurance appraiser St. Cloud",
        "title": "St. Cloud MN Insurance Appraiser | Central Minnesota",
        "desc": "From Southside rentals to Lake George homes, we help St. Cloud owners contest underpaid hail, wind and winter claims through appraisal.",
        "perils": ["Hail", "Heavy snow and ice dams", "Wind", "River flooding", "Frozen pipes"],
        "near": ["blaine", "plymouth", "duluth"],
        "lede": "St. Cloud spans Stearns, Benton and Sherburne counties along the Mississippi. Its older granite-era neighborhoods, student rentals and newer suburbs each bring different claim issues.",
        "neighborhoods": ["Lake George", "Southside", "Northside", "Talahi Woods", "Wilson Park", "East Side", "West St. Cloud"],
        "housing": "early-1900s frame houses to 1990s–2000s ramblers",
        "storm": "spring 1965 Mississippi River flood",
        "body": """
<h2>St. Cloud and the upper Mississippi</h2>
<p>St. Cloud grew up around granite quarries and the Mississippi River, and you can still see both in the city’s older buildings and neighborhoods. Lake George and the Southside near St. Cloud State University hold many early-1900s homes, a lot of them now rentals. The Northside and East Side mix older frame houses with postwar ramblers, and the edges of the city, along with Sartell, Sauk Rapids and Waite Park, filled in with newer subdivisions.</p>
<p>The city covers parts of three counties: Stearns, Benton and Sherburne. That rarely changes how a claim is valued, but it can matter for local permits and code requirements.</p>

<h2>River, snow and storms</h2>
<p>The spring flood of 1965 pushed the Mississippi to historic levels through central Minnesota, and flooding along the river and its tributaries remains a risk in high-snow years. More often, St. Cloud claims come from:</p>
<ul>
<li>Deep snow that loads roofs and causes ice dams on older, poorly insulated houses.</li>
<li>Summer thunderstorms with hail and damaging wind.</li>
<li>Frozen pipes in rentals and seasonal properties during cold snaps.</li>
</ul>

<h2>Rental property claims</h2>
<p>Landlords near campus face added complications: tenant-damaged areas mixed with storm damage, lost rent or fair rental value coverage, and disputes about what was already worn. Separating those categories clearly is a big part of a successful claim. Larger multifamily or commercial buildings may fall under <a href="/appraisal-solutions/commercial-hoa-appraisal/">commercial and HOA appraisal</a>.</p>

<h2>Winter readiness for central Minnesota properties</h2>
<p>Many of the St. Cloud claims we see could be smaller with a few precautions. Keep attics well ventilated and insulated to reduce ice dams, and clear snow from the lower few feet of the roof after big storms. In rentals, make sure tenants know where the main water shutoff is and how to keep the heat on during breaks. For seasonal or vacant properties, read the policy carefully; many limit coverage for freezing or water damage unless heat was maintained or the water was drained.</p>
<p>When damage does happen, act quickly to stop it from getting worse. Mitigation costs such as water extraction, drying equipment and temporary tarps are usually part of the claim, and policies generally require reasonable steps to protect the property. Keep every receipt and photograph the conditions before and after mitigation. That record becomes important if the amount of the loss is later disputed, because appraisers need to see what the damage looked like at its worst.</p>

<h2>Central Minnesota appraisal help</h2>
<p>Minnesota Insurance Appraiser inspects properties in St. Cloud and throughout central Minnesota. We write a line-by-line estimate and, if you invoke the appraisal clause, serve as your appraiser in negotiations with the insurer’s appraiser. If the two can’t agree, an umpire decides.</p>
<p>Not sure where to start? Use our <a href="/free-tools/">free tools</a> to organize your paperwork, read the <a href="/appraisal-process-guide/">appraisal process guide</a>, or <a href="/contact-us/">contact us</a> directly.</p>
""",
        "faqs": [
            ("Do you work with landlords near St. Cloud State?", "Yes. We review storm and water claims on rental properties and help separate covered damage from wear and tenant issues."),
            ("Do you serve Sartell, Sauk Rapids and Waite Park?", "Yes, along with the rest of Stearns, Benton and Sherburne counties."),
        ],
    },
    # ------------------------------------------------------------ Mankato
    {
        "slug": "mankato",
        "city": "Mankato",
        "county": "Blue Earth County",
        "region": "Southern Minnesota",
        "keyword": "insurance appraiser Mankato",
        "title": "Mankato Insurance Claim Appraiser | Blue Earth Co., MN",
        "desc": "Tornado, derecho and hail claims in Mankato and North Mankato. Independent appraisal when your insurer’s estimate won’t cover the repair.",
        "perils": ["Tornadoes", "Derecho wind", "Hail", "River flooding", "Ice dams"],
        "near": ["rochester", "eagan", "bloomington"],
        "lede": "Mankato sits where the Minnesota River bends north, in a part of the state with serious tornado and derecho history. We help homeowners, landlords and businesses in Blue Earth and Nicollet counties contest low settlements.",
        "neighborhoods": ["Old Town", "Lincoln Park", "Hilltop", "North Mankato", "Upper North Mankato", "Minnesota State University area"],
        "housing": "late-1800s river-valley homes to 1990s–2000s hilltop subdivisions",
        "storm": "March 29, 1998 St. Peter and Comfrey tornadoes",
        "body": """
<h2>Severe weather in the Minnesota River valley</h2>
<p>On March 29, 1998, an unusually early tornado outbreak struck south-central Minnesota. A long-track tornado hit Comfrey, southwest of Mankato, and another tore through St. Peter, about a dozen miles north, damaging hundreds of homes and historic buildings. More recently, the derecho of May 12, 2022, sent destructive straight-line winds across southern and western Minnesota. Hail and thunderstorms are routine here every summer.</p>
<p>The Minnesota River also floods in wet springs, though the levee system protects much of Mankato and North Mankato. Flooding is excluded from standard homeowner policies, so wind, hail and water from other sources make up most appraisal disputes in the area.</p>

<h2>Homes and rentals in Mankato</h2>
<p>Old Town and Lincoln Park, in the river valley, hold some of the city’s oldest homes, many with brick, limestone and decorative trim. Up the bluffs, the Hilltop area and Upper North Mankato have newer houses built from the 1960s onward. Around Minnesota State University, Mankato, a large share of houses and small apartment buildings are rentals.</p>
<p>Across the river, North Mankato sits in Nicollet County. Both counties are part of our service area.</p>

<h2>Claim issues worth watching</h2>
<ul>
<li>Wind claims after a derecho where the insurer treats a full roof replacement as a repair.</li>
<li>Historic brick and stone needing specialized masons.</li>
<li>Rental losses with lost-rent coverage left unaddressed.</li>
<li>Outbuildings, fences and trees on larger lots left off the scope.</li>
<li>Contractor shortages after big storms that push up real costs.</li>
</ul>

<h2>After a big regional storm</h2>
<p>When a tornado or derecho hits southern Minnesota, it rarely hits just one town. Insurers bring in adjusters from out of state, contractors arrive from everywhere, and local building suppliers run short. Estimates written in the first weeks may rely on pricing that doesn’t reflect what local crews actually charge once demand surges. Supplement requests pile up, and owners can wait a long time for answers.</p>
<p>A few steps help in that environment. Get written estimates from established local contractors, check that out-of-area contractors are licensed in Minnesota, and don’t sign an assignment of benefits or a contract you don’t fully understand. Keep a list of everything damaged, including trees, fences, sheds and items in outbuildings, which are easy to overlook in a farmhouse or a property on a larger lot. If the insurer’s final figure still doesn’t match the repair cost, appraisal gives you a structured way to resolve the difference.</p>

<h2>Representation for southern Minnesota</h2>
<p>Minnesota Insurance Appraiser travels to Mankato and surrounding communities to inspect losses in person. If your policy allows appraisal and you elect it, we serve as your appraiser and negotiate the amount of the loss with the insurer’s appraiser, with an umpire to settle any unresolved items.</p>
<p>Explore <a href="/appraisal-solutions/tornado-derecho-wind-appraisal/">tornado and derecho appraisal</a>, <a href="/appraisal-solutions/hail-roof-appraisal/">hail and roof appraisal</a>, or <a href="/contact-us/">talk with us</a> about your claim.</p>
""",
        "faqs": [
            ("Do you serve North Mankato and St. Peter?", "Yes. We work throughout Blue Earth and Nicollet counties and the rest of south-central Minnesota."),
            ("My insurer paid actual cash value after a derecho. Can I get more?", "Many policies pay actual cash value first and the rest of replacement cost after repairs are completed. If you disagree with the amount either way, appraisal may help."),
        ],
    },
    # ------------------------------------------------------------ Moorhead
    {
        "slug": "moorhead",
        "city": "Moorhead",
        "county": "Clay County",
        "region": "Red River Valley",
        "keyword": "insurance appraiser Moorhead MN",
        "title": "Moorhead, MN Insurance Appraiser | Red River Valley",
        "desc": "Prairie wind, hail, blizzards and frozen pipes. We help Moorhead and Clay County owners dispute insurance estimates that fall short.",
        "perils": ["Blizzards and snow load", "Hail", "High wind", "Frozen pipes", "Spring flooding"],
        "near": ["st-cloud", "duluth", "blaine"],
        "lede": "Across the Red River from Fargo, Moorhead faces open-prairie wind, long winters and a well-known flood history. We help Clay County owners contest property claims when the insurer’s estimate falls short.",
        "neighborhoods": ["Village Green", "South Moorhead", "North Moorhead", "Downtown Moorhead", "Concordia College area", "Minnesota State University Moorhead area"],
        "housing": "early-1900s homes near the colleges to 2000s south-side subdivisions",
        "storm": "1997 Red River flood",
        "body": """
<h2>Living with the Red River</h2>
<p>The Red River flood of 1997 swamped Grand Forks and threatened communities all along the valley, including Moorhead. In 2009, the river crested at record levels at Fargo–Moorhead, and residents spent weeks building sandbag dikes. Since then, Moorhead has bought out many riverfront properties and built levees and floodwalls, and the larger Fargo–Moorhead diversion project is reshaping flood risk for the metro.</p>
<p>From an insurance standpoint, river flooding is covered by flood policies, not homeowner policies. But spring thaw also brings sewer backup and seepage claims, and those can fall under endorsements that do go to appraisal.</p>

<h2>Prairie weather the rest of the year</h2>
<p>With few trees or hills to break it, wind across the Red River Valley is relentless. Blizzards bring heavy drifting and roof loads, deep cold freezes pipes and summer storms bring hail and straight-line wind. Moorhead homes range from early-1900s houses near Concordia College and Minnesota State University Moorhead to newer subdivisions on the south side such as Village Green.</p>

<h2>Common Clay County claim disputes</h2>
<ul>
<li>Wind-damaged shingles and siding written off as normal wear.</li>
<li>Frozen pipe losses where the insurer questions whether heat was maintained.</li>
<li>Hail damage on newer roofs approved only in part.</li>
<li>Basement backups capped well below the actual cost of repair.</li>
</ul>
<p>Minnesota has 87 counties and no state wind pool; if a standard carrier won’t write your property, the Minnesota FAIR Plan is the market of last resort. Whatever company insures you, the appraisal clause in your policy works the same way.</p>

<h2>Wind claims on the open prairie</h2>
<p>Wind damage is one of the most argued claim types in the valley. Shingles that have been lifted and creased by wind may lie flat again after the storm, so the damage is easy to miss from the ground and easy to call wear. A hand inspection of the roof, looking for broken seal strips and creases, gives a much better picture. Siding blown off one wall or cracked by debris raises the same matching questions as hail.</p>
<p>Because storms in the valley can arrive with little terrain to slow them, it also helps to know the date and time of the event. Local weather service reports and storm data can confirm high winds on a specific day. Pair that with dated photos of the property, and you have a much stronger record when the insurer questions whether damage is storm-related. Once coverage is accepted, the remaining dispute is usually about scope and price, which is where appraisal fits.</p>

<h2>Appraisal help in the Red River Valley</h2>
<p>Minnesota Insurance Appraiser serves Moorhead, Dilworth, Barnesville and the rest of Clay County, and we inspect on site. We build an independent estimate and represent you in appraisal when the dispute is over the amount of the loss. See our <a href="/appraisal-solutions/water-damage-appraisal/">water damage appraisal</a> and <a href="/appraisal-solutions/ice-dam-winter-damage-appraisal/">winter damage appraisal</a> pages, or <a href="/contact-us/">contact us</a> to talk through your claim.</p>
""",
        "faqs": [
            ("Do you handle property on the North Dakota side in Fargo?", "Our focus is Minnesota property. If you own property in both states, contact us and we can discuss what makes sense for your Minnesota claim."),
            ("Can a frozen pipe claim go to appraisal?", "Yes, once the insurer accepts coverage and the dispute is about the cost of repairs. Whether freezing is covered depends on your policy and whether heat was maintained."),
        ],
    },
]
