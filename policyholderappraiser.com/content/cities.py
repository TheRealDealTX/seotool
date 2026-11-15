"""City pages: the twenty largest Texas cities plus McAllen and Georgetown.

Every page carries its own body copy. Nothing in `body` or `faq` is shared
between cities; validate.py enforces that no paragraph repeats across them.
"""

CITIES = [
    {
        "slug": "houston", "name": "Houston", "county": "Harris County",
        "region": "Greater Houston and the Upper Gulf Coast",
        "nearby": ["Katy", "Cypress", "Spring", "Pearland", "Sugar Land", "Pasadena", "Baytown", "The Woodlands"],
        "title": "Insurance Appraiser in Houston, TX | Policyholder Appraiser",
        "description": "Policyholder-appointed insurance appraiser in Houston, TX for hurricane, flood-adjacent wind, hail, water and fire claim disputes. Flat fee. (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>Houston, TX</span>",
        "intro": "Houston is where we live and where most of our appraisal work happens. Hurricanes, derechos, freeze events and ordinary plumbing failures keep Harris County claim volumes high, and carrier scopes written in a hurry after a storm are the main reason Houston homeowners end up demanding appraisal.",
        "body": """
<h2>Why Houston claims end up in appraisal</h2>
<p>Houston's claim calendar runs on named storms. Hurricane Harvey in 2017, the May 2024 derecho that tore roofing and glass across the west side and downtown, and Hurricane Beryl in July 2024 each produced tens of thousands of wind claims adjusted in a matter of weeks. When that many files move that fast, scopes are written from drone photos and a short walk-through, interior water intrusion is under-measured, and fences, screens and outbuildings fall off the estimate entirely. The carrier accepts the storm; it simply pays for less of it than the storm actually did. That is an amount-of-loss dispute, and appraisal is the tool built for it.</p>
<p>Between storms, Houston's expansive clay soils and slab foundations drive a steady volume of plumbing-leak claims: slab leaks, supply-line failures under kitchens and the tunneling or slab breakouts needed to reach them. Carriers routinely accept the leak and dispute the access cost, the flooring continuity and the cabinet replacement. Those are scope arguments an appraiser settles line by line.</p>

<h2>Houston housing stock and the scope fights it creates</h2>
<p>Inside the Loop and in the older close-in neighborhoods such as Meyerland, Oak Forest, Sharpstown and the East End, homes from the 1950s through the 1970s carry original hardwood floors, plaster or early drywall, and roofs that have been re-covered more than once. Layered roofs and brittle three-tab shingles make tab-level repairs impractical, which is the heart of most Houston repair-versus-replace disputes. In the master-planned suburbs of Katy, Cypress, Spring and Pearland, the argument is usually about matching: discontinued laminate shingles, large contiguous slopes and HOA appearance rules that make a partial replacement visibly obvious.</p>
<p>Commercially, Houston's strip retail, medical office and industrial flex buildings carry TPO and modified-bitumen roofs with rooftop HVAC that hail and wind-borne debris damage in ways a ground-level inspection never sees. We walk those roofs.</p>

<h2>Umpire appointment in Harris County</h2>
<p>If the two appraisers cannot agree on an umpire, either party may ask a Harris County civil court to appoint one. Harris County's district clerk publishes a standard umpire-appointment form, and the county's civil courts at law and district courts handle these requests regularly, so a Houston appraisal rarely stalls at the umpire stage. We also serve as a neutral umpire on Houston losses where neither party is connected to us.</p>

<h2>Where we go</h2>
<p>All of Harris County and the surrounding counties: Fort Bend, Montgomery, Brazoria, Galveston, Chambers and Liberty. Katy, Cypress, Spring, Pearland, Sugar Land, Pasadena, Baytown, The Woodlands, Humble, Kingwood, League City and Friendswood are regular stops, usually within a day or two of appointment.</p>
""",
        "faq": [
            ("My Houston claim is from Hurricane Beryl. Is it too late to demand appraisal?",
             "Usually not. Most Texas policies allow an appraisal demand until the limitations period for filing suit runs, often two years from the denial or underpayment. Check your policy's appraisal clause and suit-limitation clause, then call us; we will confirm the deadline for your specific policy."),
            ("Do you handle Houston claims that involve both wind and flood?",
             "Yes. When a storm produced both, the homeowners carrier pays for wind and wind-driven rain and the flood policy pays for rising water. Our appraisal estimate separates the two with moisture mapping and photo evidence so the wind portion is fully priced rather than written off as flood."),
        ],
    },
    {
        "slug": "san-antonio", "name": "San Antonio", "county": "Bexar County",
        "region": "San Antonio and the Hill Country",
        "nearby": ["New Braunfels", "Schertz", "Cibolo", "Boerne", "Helotes", "Converse", "Universal City", "Seguin"],
        "title": "Insurance Appraiser in San Antonio, TX | Policyholder Appraiser",
        "description": "Independent insurance appraiser for San Antonio, TX homeowners and businesses disputing hail, roof, water and fire claim amounts. Flat fee, binding award. (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>San Antonio, TX</span>",
        "intro": "San Antonio sits squarely in the Texas hail belt, and the April 2016 storm that dropped softball-sized hail across the north side remains one of the costliest hail events in state history. A decade later, Bexar County roofs are still the most common subject of the appraisals we handle here.",
        "body": """
<h2>Why San Antonio claims end up in appraisal</h2>
<p>San Antonio hail comes from the northwest, which means Stone Oak, Shavano Park, Helotes, Leon Valley and the Medical Center area take the first and hardest hits. The pattern on carrier estimates after a Bexar County hail event is consistent: front and west-facing slopes approved, rear slopes called "no damage" or "mechanical," and collateral items like window screens, gutters, HVAC fins and painted fascia left off entirely. The storm is accepted; the scope is not. Appraisal resolves that gap without a lawsuit.</p>
<p>The February 2021 freeze also hit San Antonio hard. Homes built on pier-and-beam with exposed supply lines, and newer homes with PEX run through unconditioned attics, both burst. Carriers accepted those losses but frequently disputed drying duration, flooring continuity and the cost of opening ceilings to replace lines.</p>

<h2>San Antonio housing stock and the scope fights it creates</h2>
<p>San Antonio's older neighborhoods, Alamo Heights, Monte Vista, Olmos Park, Monticello Park and the King William district, carry clay-tile, slate and standing-seam metal roofs, some original to the house. Hail damage on tile is a matching and repairability argument: individual tiles may be replaceable, but matching discontinued profiles and colors frequently is not. In the post-1980 subdivisions on the north and west sides, the argument is more often brittleness on aging three-tab shingles and whether code-required decking and underlayment upgrades are owed.</p>
<p>Commercial losses in San Antonio skew toward restaurants, car dealerships along Loop 410 and I-10, and church campuses with large low-slope roofs and rooftop units. Hail on condenser coils and TPO membranes is where carrier and policyholder estimates diverge most.</p>

<h2>Umpire appointment in Bexar County</h2>
<p>When appraisers cannot agree on an umpire, a Bexar County district court or county court at law can appoint one on a short motion. We have found Bexar County appointments to be routine and fast. We also accept umpire appointments on San Antonio losses where neither party nor either appraiser has any connection to us.</p>

<h2>Where we go</h2>
<p>All of Bexar County plus Comal, Guadalupe, Kendall, Medina and Wilson counties: New Braunfels, Schertz, Cibolo, Boerne, Helotes, Converse, Universal City, Seguin, Bulverde and Canyon Lake.</p>
""",
        "faq": [
            ("The carrier approved two slopes of my San Antonio roof. Can appraisal get the whole roof?",
             "Appraisal can award a full replacement if the evidence supports it: documented hail hits on every slope, brittleness that makes repairs impractical, or a matching problem the policy covers. We inspect every slope and test repairability before we tell you what to expect."),
            ("Does appraisal work for clay tile roofs in Alamo Heights?",
             "Yes, and tile is where an independent appraiser matters most. Tile claims turn on breakage counts, underlayment condition, and whether a matching tile is still manufactured. Those are factual questions an appraisal panel resolves far better than a desk adjuster working from photos."),
        ],
    },
    {
        "slug": "dallas", "name": "Dallas", "county": "Dallas County",
        "region": "Dallas-Fort Worth",
        "nearby": ["Richardson", "Garland", "Irving", "Mesquite", "Plano", "Carrollton", "Lancaster", "DeSoto"],
        "title": "Insurance Appraiser in Dallas, TX | Policyholder Appraiser",
        "description": "Policyholder-appointed insurance appraiser in Dallas, TX for hail, tornado, wind, water and fire claim disputes. Binding award, flat fee. Call (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>Dallas, TX</span>",
        "intro": "Dallas County produces more hail claims than almost any county in the country, and the October 2019 tornado that cut across North Dallas from Love Field to Richardson showed how quickly a routine claim season can turn into a catastrophe. Both leave Dallas homeowners with the same problem: an accepted claim and an estimate that does not rebuild the house.",
        "body": """
<h2>Why Dallas claims end up in appraisal</h2>
<p>Spring hail is the engine. March through June, supercells track northeast across Dallas County and drop hail on Oak Cliff, Lakewood, Lake Highlands, Preston Hollow and Far North Dallas in alternating years. Carriers respond with volume adjusting: test squares on two slopes, a repair allowance for "cosmetic" damage, and depreciation applied aggressively to roofs that are, in fact, at the end of their life. The February 2021 freeze layered burst-pipe claims on top of the same roofs. The October 20, 2019 EF-3 tornado added structural claims where the dispute was not whether the house was damaged but how much of it had to come down.</p>
<p>Dallas commercial claims are a category of their own: office buildings along the Tollway, apartment complexes in Vickery Meadow and along Northwest Highway, and retail along Preston Road and Greenville Avenue. Multi-building apartment claims after hail are the most frequently appraised commercial loss in Dallas County.</p>

<h2>Dallas housing stock and the scope fights it creates</h2>
<p>Dallas has three distinct roof populations. The Park Cities, Lakewood and Preston Hollow carry slate, clay tile and standing-seam metal on high-value homes where the dispute is almost always matching and repairability of specialty materials. The mid-century neighborhoods, Casa Linda, Lake Highlands, Northwest Dallas and Oak Cliff, carry composition shingles over original decking, often plank decking that modern code and manufacturer requirements say must be replaced or sheathed. The post-1990 subdivisions in Far North Dallas and the suburbs carry laminated shingles where discontinued colors create matching arguments on partial approvals.</p>
<p>Plank decking is the single biggest Dallas-specific scope item. If the roof must be replaced and the decking is 1x6 or 1x8 boards with gaps, the Dallas building code and shingle manufacturers require new sheathing. Carrier estimates frequently omit it.</p>

<h2>Umpire appointment in Dallas County</h2>
<p>Dallas County district courts and county courts at law appoint umpires on motion when the appraisers cannot agree. We give the required written notice, file the request with a copy to the carrier, and keep the process moving. We also serve as neutral umpire on Dallas losses where we have no connection to either side.</p>

<h2>Where we go</h2>
<p>All of Dallas County: Richardson, Garland, Irving, Mesquite, Carrollton, Farmers Branch, Lancaster, DeSoto, Duncanville, Cedar Hill, Grand Prairie, Rowlett, Sachse and Balch Springs, plus Plano and Collin County to the north.</p>
""",
        "faq": [
            ("The carrier says my Dallas roof damage is cosmetic. Is that a coverage denial or an amount dispute?",
             "It depends on the policy. If your policy has a cosmetic-damage exclusion for metal roofs, that is a coverage question. On a shingle roof, 'cosmetic' is usually the adjuster's judgment that the hail did not break the mat, which is a factual question about the amount of covered loss, and appraisal panels decide it with test squares and shingle samples."),
            ("My Dallas home has plank decking. Will appraisal pay to re-deck it?",
             "If replacement is awarded and the policy includes ordinance-or-law coverage, the decking required by the Dallas code and the shingle manufacturer's installation requirements belongs in the amount of loss. We document the decking type with attic photos and board-gap measurements so the umpire can see why it is owed."),
        ],
    },
    {
        "slug": "fort-worth", "name": "Fort Worth", "county": "Tarrant County",
        "region": "Dallas-Fort Worth",
        "nearby": ["Keller", "Southlake", "Mansfield", "Burleson", "Benbrook", "Haltom City", "North Richland Hills", "Weatherford"],
        "title": "Insurance Appraiser in Fort Worth, TX | Policyholder Appraiser",
        "description": "Independent insurance appraiser serving Fort Worth, TX policyholders on disputed hail, wind, water and fire claims. Flat fee quoted in writing. (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>Fort Worth, TX</span>",
        "intro": "Fort Worth gets the same supercells as Dallas a half hour earlier, and Tarrant County's mix of century-old neighborhoods and brand-new subdivisions on the far north side means carrier estimates miss in different ways on different streets. We serve as the policyholder's appraiser across Tarrant and Parker counties.",
        "body": """
<h2>Why Fort Worth claims end up in appraisal</h2>
<p>Hail and straight-line wind are the Fort Worth staples. Storms that build over Parker County reach Benbrook, Westover Hills, Arlington Heights and the Cultural District first, then track across downtown toward Haltom City and Keller. After a large event, carriers assign out-of-state catastrophe adjusters working a dozen roofs a day, and the result is a partial scope: a slope or two approved, no decking, no drip edge, no starter course, and gutters and screens left off. The February 2021 freeze brought burst supply lines across the city's older pier-and-beam housing. Both produce accepted claims that are underpaid on scope, which is exactly what appraisal fixes.</p>

<h2>Fort Worth housing stock and the scope fights it creates</h2>
<p>Fairmount, Ryan Place, Mistletoe Heights and the Near Southside carry early twentieth-century homes with plank decking, multiple roof layers and plaster interiors. Replacement scopes on these homes are large, and the arguments are about decking, layer tear-off and the cost of matching plaster and trim after water intrusion. Westover Hills, Rivercrest and Tanglewood carry slate, tile and standing-seam roofs where repairability and matching dominate. The post-2005 subdivisions in far north Fort Worth, Alliance, Heritage and Presidio, carry laminated shingles on complex roof geometries where the fight is matching on partial approvals and the price of steep-slope and high-roof labor.</p>
<p>Fort Worth's commercial base includes the Stockyards, Alliance-area distribution warehouses with vast low-slope roofs, and church campuses across the county. A hailed TPO roof on a 200,000-square-foot warehouse is a seven-figure scope question that belongs in front of qualified appraisers.</p>

<h2>Umpire appointment in Tarrant County</h2>
<p>Tarrant County district courts and county courts at law appoint umpires when the appraisers cannot agree. We provide the ten days' written notice the Texas rules require, file the request with a copy to the carrier, and propose qualified neutral candidates to keep the appointment quick. We also accept umpire appointments on Fort Worth losses where we have no connection to the parties or appraisers.</p>

<h2>Where we go</h2>
<p>All of Tarrant County and Parker County: Keller, Southlake, Mansfield, Burleson, Benbrook, Haltom City, North Richland Hills, Hurst, Euless, Bedford, Saginaw, Azle, Aledo and Weatherford.</p>
""",
        "faq": [
            ("Does appraisal cover the cost of steep-slope and two-story labor on my north Fort Worth roof?",
             "Yes. Industry-standard estimating software prices steep and high-roof charges as separate line items, and an appraisal award should include them where the roof geometry justifies it. Carrier estimates often omit them or apply them to only part of the roof."),
            ("My Fairmount house has two layers of shingles. Does the second layer tear-off belong in the award?",
             "If the roof is being replaced, every layer must come off and the tear-off and disposal of each layer is part of the amount of loss. We document layer count at the eave and in the attic so there is no argument about it at the umpire stage."),
        ],
    },
    {
        "slug": "austin", "name": "Austin", "county": "Travis County",
        "region": "Austin and Central Texas",
        "nearby": ["Round Rock", "Cedar Park", "Pflugerville", "Leander", "Kyle", "Buda", "Lakeway", "Bee Cave"],
        "title": "Insurance Appraiser in Austin, TX | Policyholder Appraiser",
        "description": "Policyholder-appointed insurance appraiser in Austin, TX for freeze, hail, wind, water and fire claim disputes. Binding award without a lawsuit. (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>Austin, TX</span>",
        "intro": "Austin's defining claim event is still the February 2021 freeze: days without power, burst pipes in tens of thousands of homes and apartments, and carrier scopes written from phone photos because adjusters could not get into the city. Hail seasons since have added roof claims on a housing stock that ranges from 1930s bungalows to homes finished last year.",
        "body": """
<h2>Why Austin claims end up in appraisal</h2>
<p>Winter Storm Uri produced the largest wave of accepted-but-underpaid water claims Austin has ever seen. Carriers paid for the obvious wet drywall and little else: no flooring continuity, minimal drying, no cabinet replacement, no plaster or custom trim. Many of those claims were never fully resolved and remain within the limitations period. Spring hail follows a northwest-to-southeast track across Travis and Williamson counties, so Cedar Park, Northwest Hills, Allandale and Pflugerville take frequent hits, and flash flooding along Onion Creek, Shoal Creek and Walnut Creek produces interior water claims where carriers argue over what was wind-driven rain and what was surface water.</p>

<h2>Austin housing stock and the scope fights it creates</h2>
<p>Central Austin, Hyde Park, Clarksville, Travis Heights, Bouldin Creek and Zilker, carries pre-war bungalows and mid-century ranches with plank decking, original hardwoods and plaster, and increasingly, high-end remodels with custom finishes that carrier pricing databases do not capture. Matching discontinued hardwood species and custom tile is the recurring dispute. West Austin and the lake communities, Westlake, Lakeway, Steiner Ranch and Bee Cave, carry tile, standing-seam metal and architectural shingles on large, complex roofs where steep-slope labor and matching drive the gap. The fast-built subdivisions of Pflugerville, Manor, Kyle and Buda carry laminated shingles where the fight is discontinued colors and code upgrades.</p>
<p>Austin's multifamily inventory, especially the garden apartments along Riverside Drive and in North Austin, generated enormous freeze claims with unit-by-unit scope disputes that are well suited to appraisal.</p>

<h2>Umpire appointment in Travis County</h2>
<p>If the appraisers cannot agree on an umpire, either party may apply to a Travis County district court or county court at law for appointment after the required ten days' written notice. We handle the notice and the filing. We also serve as neutral umpire on Austin losses where we have no relationship with either party or appraiser.</p>

<h2>Where we go</h2>
<p>All of Travis, Williamson and Hays counties: Round Rock, Cedar Park, Pflugerville, Leander, Georgetown, Hutto, Manor, Kyle, Buda, San Marcos, Dripping Springs, Lakeway and Bee Cave.</p>
""",
        "faq": [
            ("My Austin freeze claim from 2021 was underpaid. Is appraisal still available?",
             "Possibly. The deadline is set by your policy's suit-limitation clause and appraisal clause, and some carriers reopened or supplemented Uri claims, which can affect timing. Send us the policy and the last carrier letter and we will tell you whether a demand is still viable."),
            ("Can appraisal price custom finishes in a remodeled Hyde Park home?",
             "Yes. Appraisers are not limited to a carrier's pricing database. Where a finish is custom, we document it, obtain supplier or contractor pricing, and present it to the carrier's appraiser and the umpire as the actual cost to repair or replace with like kind and quality."),
        ],
    },
    {
        "slug": "el-paso", "name": "El Paso", "county": "El Paso County",
        "region": "El Paso and Far West Texas",
        "nearby": ["Socorro", "Horizon City", "Anthony", "Canutillo", "San Elizario", "Clint", "Fabens"],
        "title": "Insurance Appraiser in El Paso, TX | Policyholder Appraiser",
        "description": "Independent insurance appraiser for El Paso, TX homeowners and businesses disputing freeze, flood-season, wind and fire claim amounts. Flat fee. (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>El Paso, TX</span>",
        "intro": "El Paso's claims look nothing like the rest of Texas. Flat and low-slope roofs on stucco and adobe-style homes, a summer monsoon that floods arroyos and streets, and the February 2011 freeze that burst pipes across the city when gas and power failed together. Carrier adjusters trained on Houston and Dallas roofs routinely misjudge El Paso losses, and appraisal is where that gets corrected.",
        "body": """
<h2>Why El Paso claims end up in appraisal</h2>
<p>El Paso's monsoon season, July through September, delivers short, violent storms that overwhelm flat roofs with ponding water, push water under parapet caps and through scuppers, and flood ground floors from the arroyos that run off the Franklin Mountains. The August 2006 floods remain the benchmark, but every summer produces a wave of interior water claims where carriers dispute whether water came through the roof (covered) or rose from the ground (often excluded). Spring wind events, with gusts well over 60 miles per hour off the mountains, peel foam and modified-bitumen roofing and drive sand through every unsealed opening. The February 2011 freeze and the February 2021 freeze both burst lines in homes never built for sustained cold.</p>

<h2>El Paso housing stock and the scope fights it creates</h2>
<p>The Westside, Kern Place, Mission Hills and the older Central and Lower Valley neighborhoods carry flat and low-slope roofs with built-up, modified-bitumen or sprayed polyurethane foam systems, parapets, canales and scuppers. Carrier estimates written with pitched-roof assumptions miss the real repair: tapered insulation, parapet flashing, coating systems and the cost of a complete membrane rather than a patch. Stucco repair and color matching on large wall areas is another recurring dispute. The newer subdivisions on the far Eastside and in Horizon City carry tile and composition roofs on stucco homes where wind uplift of tile and ridge caps drives the argument.</p>
<p>El Paso's commercial base, warehousing and logistics near the ports of entry, medical campuses and the Fort Bliss support economy, carries large low-slope roofs and rooftop HVAC where monsoon and wind damage is frequently underscoped.</p>

<h2>Umpire appointment in El Paso County</h2>
<p>El Paso County's district courts and county courts at law can appoint an umpire when the appraisers cannot agree, after the ten days' written notice the Texas rules require. We prepare the notice and the request. We also accept neutral umpire appointments on El Paso losses where we have no connection to either party.</p>

<h2>Where we go</h2>
<p>All of El Paso County and Hudspeth County: Socorro, Horizon City, Anthony, Canutillo, San Elizario, Clint, Fabens and Fort Bliss housing areas, plus Las Cruces-area Texas properties.</p>
""",
        "faq": [
            ("My El Paso flat roof was patched by the carrier's estimate. Can appraisal award a full membrane?",
             "If the evidence shows the membrane has failed beyond repair, that saturated insulation must be removed, or that a patch cannot be made watertight on the existing system, an appraisal award can include the full roof system. We core-sample and moisture-scan low-slope roofs to prove it."),
            ("The carrier says my monsoon water damage is flood. Is that something appraisal can decide?",
             "Not by itself. Whether water came through the roof or rose from the ground is a coverage question. Appraisal determines the amount of the covered loss. We help by documenting the entry path with photos and moisture mapping; if the carrier then accepts a covered source and disputes the amount, appraisal resolves the rest."),
        ],
    },
    {
        "slug": "arlington", "name": "Arlington", "county": "Tarrant County",
        "region": "Dallas-Fort Worth",
        "nearby": ["Grand Prairie", "Mansfield", "Kennedale", "Pantego", "Dalworthington Gardens", "Hurst", "Euless"],
        "title": "Insurance Appraiser in Arlington, TX | Policyholder Appraiser",
        "description": "Policyholder-appointed insurance appraiser in Arlington, TX for hail, tornado, wind and water claim disputes. Binding award, flat fee. Call (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>Arlington, TX</span>",
        "intro": "Arlington sits in the middle of the Metroplex storm track, and the April 2012 tornado outbreak that crossed south Arlington and Kennedale is the reason many residents learned what an appraisal clause is. Hail does the rest of the work most years. We serve as the appraiser Arlington policyholders appoint.",
        "body": """
<h2>Why Arlington claims end up in appraisal</h2>
<p>Arlington's hail exposure is relentless because storms that form over Parker and western Tarrant counties mature right over the city. The 1960s and 1970s ranch homes south of I-30 and east of Cooper Street carry roofs that have been hit, repaired, hit again and depreciated to nearly nothing on carrier estimates. The dispute is rarely whether hail fell; it is whether the roof can be repaired, how much depreciation is fair on a roof the carrier itself approved repairs to three years earlier, and whether the decking and code items are owed. The April 3, 2012 tornadoes added structural scope disputes in the Forest Hill and Kennedale corridor that still inform how Arlington claims are handled.</p>

<h2>Arlington housing stock and the scope fights it creates</h2>
<p>North Arlington's post-war neighborhoods near UT Arlington and the entertainment district carry small, simple roofs where carriers push repair allowances; brittleness testing settles most of those. The large 1980s and 1990s subdivisions in southwest Arlington carry steeper, more complex roofs with discontinued shingle lines, so matching is the common argument. Arlington also has an unusually large stock of older apartment complexes and student housing where unit-by-unit interior scopes after hail-driven roof leaks are routinely under-measured.</p>
<p>Commercial claims in Arlington center on the entertainment district's hospitality properties, auto dealerships along I-20 and the retail corridors on Cooper and Collins, where hail on rooftop units and low-slope membranes is the usual dispute.</p>

<h2>Umpire appointment in Tarrant County</h2>
<p>Arlington losses fall under Tarrant County's district courts and county courts at law for umpire appointment when the appraisers cannot agree. We give the ten days' written notice, file the request and copy the carrier, and propose neutral candidates to shorten the process. We also serve as umpire on Arlington losses where we have no ties to either side.</p>

<h2>Where we go</h2>
<p>Arlington, Grand Prairie, Mansfield, Kennedale, Pantego, Dalworthington Gardens, Hurst, Euless, Bedford and the Mid-Cities, plus Fort Worth and the rest of Tarrant County.</p>
""",
        "faq": [
            ("The carrier approved a roof repair on my Arlington home three years ago and now says the roof is worn out. Can appraisal help?",
             "If the current hail event is accepted as covered, appraisal decides the amount of loss for that event, including whether a repair is feasible on a roof the carrier previously repaired. Prior repair approvals, brittleness testing and the roof's actual condition all go into the appraisers' analysis."),
            ("Can appraisal handle an Arlington apartment complex with twenty buildings?",
             "Yes. Large multifamily losses are among the most common commercial appraisals in Tarrant County. We scope each building and each affected unit, and the award is itemized so the carrier's payment can be reconciled building by building."),
        ],
    },
    {
        "slug": "corpus-christi", "name": "Corpus Christi", "county": "Nueces County",
        "region": "Coastal Bend",
        "nearby": ["Portland", "Rockport", "Port Aransas", "Aransas Pass", "Ingleside", "Kingsville", "Robstown", "Flour Bluff"],
        "title": "Insurance Appraiser in Corpus Christi, TX | Policyholder Appraiser",
        "description": "Independent insurance appraiser on the Texas coast: Corpus Christi hurricane, windstorm, TWIA and water claim disputes settled by binding award. (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>Corpus Christi, TX</span>",
        "intro": "Hurricane Harvey made landfall just up the coast at Rockport in August 2017, and the Coastal Bend has been adjusting its claims ever since. Corpus Christi policyholders also live with a split insurance market: a standard homeowners policy for most perils and a Texas Windstorm Insurance Association policy for wind and hail, each with its own appraisal process.",
        "body": """
<h2>Why Corpus Christi claims end up in appraisal</h2>
<p>Coastal wind claims are underpaid in predictable ways. Carriers approve the roof slopes that face the storm, call leeward damage "wear," and leave wind-driven rain intrusion through windows, doors and soffits out of the interior scope. Salt air shortens the life of every fastener, flashing and HVAC coil on the island and along Ocean Drive, and carriers use that corrosion to argue pre-existing damage on items a storm actually destroyed. After Harvey, many Rockport, Port Aransas and Aransas Pass claims were paid as partial losses on homes that were later condemned, and the scope gap on those files was enormous.</p>
<p>Corpus Christi also sees a steady flow of plumbing and cast-iron drain failures in the mid-century homes south of downtown, where slab-foundation access costs are disputed, and roof-leak claims on the flat and low-slope roofs common in Flour Bluff and the Southside.</p>

<h2>TWIA policies have their own appraisal process</h2>
<p>If your wind coverage is through TWIA, the appraisal process is governed by 28 TAC §5.4201 and following rather than by the general 2027 residential rules. TWIA appraisal has its own deadlines, its own appraiser and umpire qualification and conflict rules, and a TDI-maintained umpire roster that the Department selects from when the appraisers cannot agree. We handle TWIA appraisals under that process and can explain the differences on the first call. Standard homeowners policies for non-wind perils follow the policy's own appraisal clause.</p>

<h2>Corpus Christi housing stock and the scope fights it creates</h2>
<p>Ocean Drive, Del Mar and the older bayfront neighborhoods carry tile, slate and metal roofs on homes where matching and corrosion arguments dominate. Padre Island and Port Aransas carry elevated coastal construction with metal roofs, impact windows and exposed decks where carriers dispute whether damage to specialty components is storm-related. The Southside and Calallen subdivisions carry composition roofs where the dispute is slope-by-slope wind damage and the cost of code-required coastal fastening schedules on replacement.</p>

<h2>Umpire appointment in Nueces County</h2>
<p>For non-TWIA appraisals, a Nueces County district court or county court at law can appoint an umpire when the appraisers cannot agree, after ten days' written notice. For TWIA appraisals, umpire selection runs through the Department's roster process. We handle both. We also serve as a neutral umpire on Coastal Bend losses where we have no connection to either side.</p>

<h2>Where we go</h2>
<p>Nueces, San Patricio, Aransas, Kleberg and Refugio counties: Portland, Rockport, Port Aransas, Aransas Pass, Ingleside, Kingsville, Robstown, Flour Bluff and Padre Island.</p>
""",
        "faq": [
            ("My Corpus Christi wind claim is with TWIA. Do the 2027 Texas appraisal rules apply?",
             "No. TWIA policies are expressly excluded from the 2027 rules and follow TWIA's own appraisal process under 28 TAC §5.4201 and following, including TDI's umpire roster. We work within that process, and we will walk you through its deadlines before you demand appraisal."),
            ("The carrier blames salt-air corrosion for my damaged HVAC and flashing. Can appraisal address that?",
             "Appraisal resolves the amount of the covered loss. If the carrier has accepted the storm but attributes specific items to corrosion, that is a scope dispute an appraisal panel can decide on the evidence: impact patterns, bent fins, torn flashing and photo documentation of the condition before and after the storm."),
        ],
    },
    {
        "slug": "plano", "name": "Plano", "county": "Collin County",
        "region": "Dallas-Fort Worth",
        "nearby": ["Allen", "Murphy", "Richardson", "Wylie", "Frisco", "McKinney", "Parker", "Lucas"],
        "title": "Insurance Appraiser in Plano, TX | Policyholder Appraiser",
        "description": "Policyholder-appointed insurance appraiser in Plano, TX for disputed hail and roof claims, water losses and fire claims. Binding award, flat fee. (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>Plano, TX</span>",
        "intro": "Plano is a city of roofs built in two waves, the 1970s and 1980s subdivisions of west and central Plano and the 1990s and 2000s builds east of Central Expressway, and Collin County hail finds both. The disputes here are about matching, HOA standards and roofs that carriers insist can be repaired a shingle at a time.",
        "body": """
<h2>Why Plano claims end up in appraisal</h2>
<p>Collin County is a national hail hot spot, and Plano's storm history includes the March 2016 event that produced baseball-sized hail across Wylie and east Plano and repeated spring events since. Carriers know the frequency and respond by depreciating roofs steeply and approving partial scopes. Plano's homeowners associations complicate the partial-scope approach: many require uniform roofing appearance and specific shingle classes, which makes a two-slope replacement unacceptable and pushes the dispute to appraisal. The February 2021 freeze added burst-pipe claims across the city's two-story housing where upstairs failures damaged every floor below.</p>

<h2>Plano housing stock and the scope fights it creates</h2>
<p>West Plano's 1970s and 1980s homes near Willow Bend and Prestonwood carry roofs on their second or third covering, often with original decking and skylights, and brittleness on older three-tab and early laminate shingles makes repairs impractical. East Plano's 1990s subdivisions carry laminated shingles in colors long since discontinued; matching is the argument. Plano's newer Legacy-area townhomes and the condo communities along the Tollway raise unit-owner versus association responsibility questions that appraisal handles once the covered party is clear.</p>
<p>Plano's commercial inventory, the Legacy corporate campuses, retail along Preston and Park, and the large church properties, carries low-slope roofs and rooftop HVAC that hail damages in ways only a roof-level inspection reveals.</p>

<h2>Umpire appointment in Collin County</h2>
<p>If the appraisers cannot agree on an umpire, either party may apply to a Collin County district court or county court at law in McKinney after ten days' written notice. We handle the notice and the filing and propose neutral, qualified candidates. We also accept umpire appointments on Plano losses where we have no relationship with either side.</p>

<h2>Where we go</h2>
<p>Plano, Allen, Murphy, Wylie, Parker, Lucas, Richardson, Frisco and McKinney, and the rest of Collin County.</p>
""",
        "faq": [
            ("My Plano HOA requires a uniform roof. Does that help my appraisal?",
             "It can. Where the policy covers matching or the HOA's architectural rules make a partial replacement impractical, the appraisers consider that in determining the amount of loss. We obtain the HOA's written standards and include them in the appraisal submission."),
            ("Can appraisal recover the depreciation the carrier withheld on my Plano roof?",
             "The award states the amount of loss, usually at both replacement cost and actual cash value. Recoverable depreciation is then released under the policy's replacement-cost terms once repairs are complete. An appraisal award that corrects an unreasonably low replacement cost also corrects the depreciation calculated from it."),
        ],
    },
    {
        "slug": "lubbock", "name": "Lubbock", "county": "Lubbock County",
        "region": "South Plains",
        "nearby": ["Wolfforth", "Slaton", "Levelland", "Shallowater", "Idalou", "Ransom Canyon", "Abernathy"],
        "title": "Insurance Appraiser in Lubbock, TX | Policyholder Appraiser",
        "description": "Independent insurance appraiser serving Lubbock, TX and the South Plains on disputed hail, wind, dust-storm and water claims. Flat fee, binding award. (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>Lubbock, TX</span>",
        "intro": "Lubbock's weather is large hail, straight-line wind and blowing dust, in that order, and the carriers that write the South Plains price their adjusting accordingly. Lubbock homeowners get fast, formulaic estimates after every spring storm, and appraisal is how the ones that are wrong get corrected without a lawsuit.",
        "body": """
<h2>Why Lubbock claims end up in appraisal</h2>
<p>Hail on the Caprock is frequent and often large, and the flat terrain means wind arrives with nothing to slow it. Carrier estimates after a Lubbock hail event typically approve the roof and underpay everything around it: window screens, gutters, painted metal, fences, evaporative coolers and HVAC condensers. Dust storms, the haboobs that roll in off the plains, drive fine grit through attic vents and around windows and into ductwork, and carriers frequently decline the cleaning scope. Winter brings ice storms and the occasional freeze that bursts lines in homes with crawl-space plumbing.</p>

<h2>Lubbock housing stock and the scope fights it creates</h2>
<p>Lubbock's older neighborhoods, Tech Terrace, the Overton area and the homes south of 34th Street, carry 1940s through 1960s construction with plank decking, original wood windows and plaster, where replacement scopes grow once the attic is inspected. The post-1980 subdivisions in southwest Lubbock carry composition roofs with discontinued shingle lines, so matching and brittleness dominate. Lubbock has a notably large stock of homes with evaporative coolers and metal outbuildings, both of which hail destroys and carrier estimates tend to omit or price as repairs.</p>
<p>Commercial claims in Lubbock center on agricultural operations, cotton gins and equipment barns outside the city, and the retail and medical corridors along Loop 289, where low-slope roofs and rooftop units are the usual dispute.</p>

<h2>Umpire appointment in Lubbock County</h2>
<p>Lubbock County's district courts and county courts at law can appoint an umpire when the appraisers cannot agree, after the ten days' written notice the Texas rules require. We prepare and file the request. We also serve as umpire on South Plains losses where we have no connection to either party.</p>

<h2>Where we go</h2>
<p>Lubbock, Wolfforth, Slaton, Levelland, Shallowater, Idalou, Ransom Canyon, Abernathy and Plainview, plus Amarillo and the Panhandle by arrangement.</p>
""",
        "faq": [
            ("The carrier won't pay to clean my ductwork after a Lubbock dust storm. Is that an appraisal issue?",
             "If the carrier has accepted the storm as a covered loss and is disputing whether duct cleaning is a necessary part of the repair, that is a scope question appraisal can decide. If it has denied dust intrusion as a covered peril entirely, that is a coverage question; we will tell you which letter you have."),
            ("Do you travel to Lubbock for inspections?",
             "Yes. Travel is included in the quoted fee for Lubbock and the South Plains. We typically schedule West Texas inspections in clusters so the cost stays low, and early document review happens remotely before anyone drives."),
        ],
    },
    {
        "slug": "irving", "name": "Irving", "county": "Dallas County",
        "region": "Dallas-Fort Worth",
        "nearby": ["Las Colinas", "Coppell", "Grand Prairie", "Farmers Branch", "Euless", "Grapevine", "Valley Ranch"],
        "title": "Insurance Appraiser in Irving, TX | Policyholder Appraiser",
        "description": "Policyholder-appointed insurance appraiser in Irving and Las Colinas, TX for hail, wind, water and fire claim disputes on homes and commercial property. (832) 503-5866.",
        "h1": "Insurance Appraiser in <span>Irving, TX</span>",
        "intro": "Irving pairs some of the Metroplex's oldest post-war neighborhoods with the corporate towers and gated communities of Las Colinas, and hail treats them the same. The carrier estimates do not. We serve as the policyholder's appraiser on Irving residential and commercial claims.",
        "body": """
<h2>Why Irving claims end up in appraisal</h2>
<p>Irving's position between Dallas and Fort Worth puts it under the same spring supercells, and its proximity to DFW Airport means a dense population of hotels, office parks and light industrial roofs that hail hits every few years. Residential disputes follow the Dallas County pattern: partial slope approvals, no decking, heavy depreciation. Commercial disputes are larger and more technical: hail on TPO and EPDM membranes, on the fins of hundreds of rooftop condensers, and on the skylights and curtain walls of Las Colinas office buildings, where carriers argue that impact marks are cosmetic and policyholders argue the membrane is compromised.</p>

<h2>Irving housing stock and the scope fights it creates</h2>
<p>South Irving's 1950s and 1960s neighborhoods carry small, simple roofs over plank decking with original windows and plaster, and replacement scopes expand once decking and layers are documented. The 1970s and 1980s subdivisions of north Irving carry roofs at end-of-life where repair-versus-replace and brittleness dominate. Las Colinas and Valley Ranch carry tile, slate and high-end laminate on larger homes and townhome communities where matching discontinued materials is the fight, and where association-versus-owner responsibility must be sorted before appraisal begins.</p>

<h2>Umpire appointment in Dallas County</h2>
<p>Irving losses fall under Dallas County's district courts and county courts at law for umpire appointment when the appraisers cannot agree. We provide ten days' written notice, file the request with a copy to the carrier, and keep the appointment moving. We also accept umpire appointments on Irving losses where we have no ties to either party.</p>

<h2>Where we go</h2>
<p>Irving, Las Colinas, Valley Ranch, Coppell, Grand Prairie, Farmers Branch, Euless, Grapevine and the DFW Airport corridor.</p>
""",
        "faq": [
            ("The carrier says hail marks on my Las Colinas office roof are cosmetic. Can appraisal decide that?",
             "If the carrier has accepted the hail event and the dispute is whether the membrane damage requires replacement, that is an amount-of-loss question. We document fractures, punctures and seam damage with close-up photography and, where warranted, core samples so the panel can see whether the membrane is compromised."),
            ("My Irving townhome's roof is shared. Who demands appraisal?",
             "The party whose policy covers the damaged element. If the association's master policy covers the roof, the association demands appraisal; if your HO-6 covers interior finishes, you demand appraisal on those. We help sort the responsibility line before any demand goes out."),
        ],
    },
]

from content.cities2 import CITIES2  # noqa: E402
CITIES = CITIES + CITIES2
for c in CITIES:
    c['path'] = f"/service-areas/{c['slug']}-tx/"
BY_SLUG = {c['slug']: c for c in CITIES}
