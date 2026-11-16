"""Storm-history blog posts, one per city. Each `body` may use {city_url}
(the city service page), {hail}, {wind}, {water}, {fire}, {home} (service page
URLs) and {kw} ("<City> insurance appraiser")."""

PUBLISHED = "2026-11-16"

STORMS = {
"houston": {
    "title": "Houston Storm History: The Events Behind Houston Insurance Claims",
    "description": "From Alicia and Ike to Harvey, Uri, the 2024 derecho and Beryl: the storms that shaped Houston property claims and what each meant for policyholders.",
    "h1": "Houston Storm History: <span>The Events Behind Houston Claims</span>",
    "intro": "Houston's claim files are a storm diary. Every major event left a distinct pattern in how carriers adjusted, what they missed and which disputes ended up in appraisal. Here is the timeline, and what each entry means for a claim today.",
    "body": """
<h2>Hurricane Alicia, August 1983</h2>
<p>Alicia came ashore near Galveston as a Category 3 and sent tornadoes and glass through downtown Houston. It is the reference point for the modern Houston windstorm market and the reason many older policies carry separate wind deductibles that still surprise homeowners.</p>
<h2>Hurricane Ike, September 13, 2008</h2>
<p>Ike's surge devastated Galveston and the Bolivar Peninsula; its wind field covered the whole metro. Carriers adjusted hundreds of thousands of claims in weeks, and the pattern that would repeat for the next fifteen years was set: roof slopes partially approved, interior water intrusion under-scoped, fences and outbuildings omitted. Many Ike disputes were resolved through appraisal rather than litigation, which is where Houston's appraisal practice matured.</p>
<h2>The Memorial Day and Tax Day floods, 2015 and 2016</h2>
<p>Back-to-back flood events along Brays Bayou, Buffalo Bayou and the Cypress Creek watershed produced claims where the split between flood policies and homeowners policies dominated. Wind-driven rain and roof leaks during those storms were covered under homeowners policies and were frequently lumped in with excluded rising water.</p>
<h2>Hurricane Harvey, August 25 to 29, 2017</h2>
<p>Harvey dropped more than fifty inches of rain on parts of Harris County. Most of the damage was flood, but wind and wind-driven rain damaged roofs and interiors across the metro, and separating the two became the central dispute on thousands of homeowners claims. Documentation of entry paths, moisture mapping and photographs of roof damage decided those files.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Days of sub-freezing temperatures and grid failure burst supply lines in homes and apartments from Katy to Kingwood. Carriers scoped from phone photographs and paid for wet drywall; drying, flooring continuity, cabinets and plaster were disputed on a large share of files, many of which are still within the limitations period.</p>
<h2>The May 16, 2024 derecho</h2>
<p>Straight-line winds over 100 miles per hour blew out high-rise glass downtown and tore roofing, fences and trees across west and north Houston. The adjusting pattern was Ike's again: fast, partial, with collateral damage omitted.</p>
<h2>Hurricane Beryl, July 8, 2024</h2>
<p>Beryl's Category 1 landfall near Matagorda produced a wind and tornado event across Houston with a prolonged power outage. Roof, fence and interior claims from Beryl remain active and appraisable.</p>
<h2>What this history means for your claim</h2>
<p>Every one of these events produced accepted, underpaid claims, which is the dispute appraisal exists to resolve. If your Harvey, Uri, derecho or Beryl claim was accepted but short, a <a href="{city_url}">{kw}</a> can be appointed under your policy's appraisal clause to settle the amount of loss. Hurricane and wind losses are handled through our <a href="{wind}">hurricane and windstorm appraisal</a> service; freeze and plumbing losses through <a href="{water}">water damage appraisal</a>; roof claims through <a href="{hail}">hail and roof claim appraisal</a>.</p>
""",
},
"san-antonio": {
    "title": "San Antonio Storm History: Hail, Floods and the Freeze Behind SA Claims",
    "description": "The 1998 and 2013 floods, the April 2016 hailstorm, Winter Storm Uri and the hail seasons since: the events that drive San Antonio insurance claims and appraisals.",
    "h1": "San Antonio Storm History: <span>Hail, Floods and Freeze</span>",
    "intro": "San Antonio's claim history runs on hail from the northwest and water from the creeks, with one freeze that changed everything. Here is the timeline and what each event means for a claim today.",
    "body": """
<h2>The October 1998 floods</h2>
<p>A stalled tropical system dropped more than twenty inches of rain over the Hill Country and sent the San Antonio, Guadalupe and Medina rivers over their banks. The event defined flood-versus-homeowners coverage disputes in Bexar County for a generation and remains the benchmark for flash-flood claims.</p>
<h2>The Memorial Day flood, May 25, 2013</h2>
<p>Leon Creek and Olmos Creek flooded neighborhoods on the north and west sides. Interior water claims from that night were frequently denied as surface water when the entry path was actually a roof or window, and documentation decided them.</p>
<h2>The April 12, 2016 hailstorm</h2>
<p>Softball-sized hail fell across Stone Oak, Shavano Park, Helotes and the Medical Center, producing the costliest hail event in Texas history to that point. Carriers approved front and west slopes and denied the rest on tens of thousands of roofs; the 2016 storm is the reason repair-versus-replace appraisal became routine in San Antonio.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Pier-and-beam plumbing and attic PEX lines burst across the city during the grid failure. Carriers accepted the losses but disputed drying, flooring continuity and the cost of opening ceilings to replace lines.</p>
<h2>Spring hail seasons since 2016</h2>
<p>Bexar County has taken hail nearly every spring since, with the same north-side neighborhoods in the path and the same partial-scope estimates following. Tile and slate roofs in Alamo Heights and Monte Vista add matching disputes that production-shingle neighborhoods do not have.</p>
<h2>What this history means for your claim</h2>
<p>Hail, flood-adjacent water and freeze claims are accepted-but-underpaid claims more often than they are denials, and that is the appraisal clause's territory. A <a href="{city_url}">{kw}</a> can be appointed to settle the amount of loss on any of them. Roof disputes run through our <a href="{hail}">hail and roof claim appraisal</a> service, plumbing and freeze losses through <a href="{water}">water damage appraisal</a>, and homeowners claims generally through <a href="{home}">homeowners claim appraisal</a>.</p>
""",
},
"dallas": {
    "title": "Dallas Storm History: Hail, Tornadoes and Floods Behind Dallas Claims",
    "description": "The June 2012 hail, the October 2019 tornado, Winter Storm Uri, the August 2022 flood and the May 2024 wind event: the storms driving Dallas insurance claims.",
    "h1": "Dallas Storm History: <span>Hail, Tornadoes and Floods</span>",
    "intro": "Dallas County produces more hail claims than almost anywhere in the country, with a tornado and a flood thrown in each decade. Here is the record behind the claims, and what each event means for a dispute today.",
    "body": """
<h2>The June 13, 2012 hailstorm</h2>
<p>Baseball-sized hail fell across Lakewood, Lake Highlands, Preston Hollow and Irving in one evening, damaging more than a hundred thousand roofs. Carriers responded with volume adjusting, and the Dallas pattern of partial slope approvals and heavy depreciation was set.</p>
<h2>The October 20, 2019 tornado</h2>
<p>An EF-3 tornado tracked from near Love Field across Preston Hollow and North Dallas into Richardson, destroying schools, churches and hundreds of homes. Structural claims from that night raised the question that defines tornado appraisals: not whether the house was damaged, but how much of it had to come down.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Burst supply lines in two-story homes across the county produced claims carriers paid as single-room losses when water had run through every floor. Those files remain common appraisal subjects.</p>
<h2>The August 22, 2022 flash flood</h2>
<p>Up to fifteen inches of rain in twenty-four hours flooded East Dallas, Oak Cliff and the Trinity corridor. Interior water claims were disputed as surface water versus roof and window intrusion, and documentation of the entry path decided them.</p>
<h2>The May 28, 2024 wind event</h2>
<p>A line of storms with hurricane-force gusts knocked out power to a million customers and tore roofing, fences and trees across the Metroplex. Adjusting was fast and partial; collateral damage was widely omitted.</p>
<h2>Hail every spring</h2>
<p>Between the headline events, Dallas County takes damaging hail in most years, with the same neighborhoods in the path and the same carrier estimates following: no plank decking, no code items, repair allowances on roofs that cannot be repaired.</p>
<h2>What this history means for your claim</h2>
<p>If a Dallas hail, tornado, freeze or wind claim was accepted but underpaid, a <a href="{city_url}">{kw}</a> can be appointed under the appraisal clause to settle the amount of loss. Roof claims go through our <a href="{hail}">hail and roof claim appraisal</a> service, wind and tornado through <a href="{wind}">windstorm appraisal</a>, and freeze and flood-adjacent water through <a href="{water}">water damage appraisal</a>.</p>
""",
},
"fort-worth": {
    "title": "Fort Worth Storm History: Mayfest Hail, the 2000 Tornado and Since",
    "description": "The 1995 Mayfest hailstorm, the March 2000 downtown tornado, Winter Storm Uri and the hail seasons since: the storms behind Fort Worth insurance claims.",
    "h1": "Fort Worth Storm History: <span>Mayfest, the Downtown Tornado and Since</span>",
    "intro": "Fort Worth's storms arrive a half hour before Dallas's and hit a city with century-old neighborhoods and brand-new subdivisions in the same path. Here is the timeline behind Tarrant County claims.",
    "body": """
<h2>The Mayfest hailstorm, May 5, 1995</h2>
<p>Softball-sized hail fell on the Mayfest festival crowd in Trinity Park and across Fort Worth, injuring hundreds and producing what was then the costliest hailstorm in United States history. It remains the event every Tarrant County roofer and adjuster measures others against.</p>
<h2>The downtown tornado, March 28, 2000</h2>
<p>An F3 tornado struck downtown Fort Worth, blowing out windows in the Bank One Tower and damaging the Cultural District and Linwood. Commercial glass, roof and interior claims from that night defined large-loss appraisal practice in the county.</p>
<h2>Hail seasons through the 2000s and 2010s</h2>
<p>Storms building over Parker County reach Benbrook, Arlington Heights and the Cultural District first, then Haltom City and Keller. Carriers assign out-of-state catastrophe adjusters after large events, and partial scopes follow: a slope or two approved, no decking, no drip edge, gutters and screens omitted.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Fort Worth's pier-and-beam housing in Fairmount, Ryan Place and the Near Southside burst lines across the city. Claims were scoped from photographs and paid short on drying, flooring and plaster.</p>
<h2>The May 28, 2024 wind event</h2>
<p>The same derecho that hit Dallas crossed Tarrant County with gusts near hurricane strength, stripping roofing and fences across north Fort Worth's newer subdivisions.</p>
<h2>What this history means for your claim</h2>
<p>Accepted, underpaid hail, wind and freeze claims are what the appraisal clause resolves. A <a href="{city_url}">{kw}</a> can be appointed to settle the amount of loss on any of these events. Roof disputes run through <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and the Alliance-area warehouse roofs through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"austin": {
    "title": "Austin Storm History: Floods, Uri and the 2023 Ice Storm",
    "description": "The 2013 Halloween flood, the 2015 Memorial Day floods, Winter Storm Uri, the February 2023 ice storm and Austin's hail seasons: the events behind Austin claims.",
    "h1": "Austin Storm History: <span>Floods, Uri and the 2023 Ice Storm</span>",
    "intro": "Austin's claim history is written in water and ice more than hail, though the hail comes too. Here is the timeline behind Travis County claims and what each event means today.",
    "body": """
<h2>The Halloween flood, October 31, 2013</h2>
<p>Onion Creek rose more than forty feet in hours and swept through Southeast Austin neighborhoods. The event drove a city buyout program and set the pattern for flood-versus-homeowners disputes along Onion, Shoal and Walnut creeks.</p>
<h2>The Memorial Day floods, May 2015</h2>
<p>The Blanco River flood at Wimberley and flooding across Travis and Hays counties produced interior water claims where roof and window intrusion during the storm was lumped in with excluded rising water.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Austin lost power and water for days. Burst pipes in tens of thousands of homes and apartments, scoped from phone photographs because adjusters could not reach the city, produced the largest wave of underpaid water claims in Austin's history. Many remain within the limitations period.</p>
<h2>The February 2023 ice storm</h2>
<p>Freezing rain over three days brought down trees and limbs across Central Austin, damaging roofs, fences and vehicles and knocking out power for a week. Roof and tree-impact claims were adjusted quickly and often partially.</p>
<h2>Hail seasons</h2>
<p>Spring hail tracks from the northwest across Cedar Park, Northwest Hills and Pflugerville. Two-slope approvals and discontinued-shingle matching disputes follow the same pattern as the rest of Central Texas.</p>
<h2>What this history means for your claim</h2>
<p>If a Uri, ice-storm, hail or flood-adjacent claim was accepted but paid short, a <a href="{city_url}">{kw}</a> can be appointed to settle the amount of loss. Freeze and plumbing losses run through <a href="{water}">water damage appraisal</a>, roof and tree-impact claims through <a href="{hail}">hail and roof claim appraisal</a>, and homeowners claims generally through <a href="{home}">homeowners claim appraisal</a>.</p>
""",
},
"el-paso": {
    "title": "El Paso Storm History: Monsoon Floods, Freezes and Wind",
    "description": "The August 2006 floods, the February 2011 freeze, the 2021 freeze and El Paso's monsoon and wind seasons: the events behind El Paso insurance claims.",
    "h1": "El Paso Storm History: <span>Monsoon Floods, Freezes and Wind</span>",
    "intro": "El Paso's weather is nothing like the rest of Texas, and neither are its claims. Here is the record behind them and what each event means for a dispute today.",
    "body": """
<h2>The August 2006 floods</h2>
<p>A week of monsoon rain, more than the city normally sees in a year, sent water off the Franklin Mountains through the arroyos and into the Westside, Central and the Lower Valley. Flat roofs ponded and failed, and the flood-versus-roof-leak dispute that defines El Paso water claims was established.</p>
<h2>The February 2011 freeze</h2>
<p>Four days of single-digit temperatures with rolling blackouts and natural gas failures burst pipes across a city never built for sustained cold. Carriers adjusted thousands of plumbing claims against homes with crawl spaces and exposed supply lines.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Milder in El Paso than in the rest of Texas because the city sits on a different grid, Uri still froze lines in homes with exposed plumbing, and claims followed the 2011 pattern.</p>
<h2>Spring wind seasons</h2>
<p>Gusts well over sixty miles per hour off the mountains peel foam and modified-bitumen roofing, lift tile and ridge caps on the Eastside, and drive sand through every unsealed opening. Carriers often call that damage wear.</p>
<h2>Monsoon seasons every summer</h2>
<p>July through September, short violent storms overwhelm scuppers and parapets and flood streets. Every summer produces interior water claims where the entry path decides coverage and the scope decides the award.</p>
<h2>What this history means for your claim</h2>
<p>Accepted, underpaid flat-roof, freeze and wind claims are what the appraisal clause settles. An <a href="{city_url}">{kw}</a> who understands low-slope roofing can be appointed to determine the amount of loss. Roof-system disputes run through <a href="{hail}">roof claim appraisal</a>, freeze and monsoon water through <a href="{water}">water damage appraisal</a>, and the warehouse and medical roofs through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"arlington": {
    "title": "Arlington Storm History: The 2012 Tornadoes and the Hail Between",
    "description": "The April 3, 2012 tornado outbreak, the hail cycles before and since, Winter Storm Uri and the May 2024 wind event: the storms behind Arlington, TX insurance claims.",
    "h1": "Arlington Storm History: <span>The 2012 Tornadoes and the Hail Between</span>",
    "intro": "Arlington sits in the middle of the Metroplex storm track, and its 1960s and 1970s housing has been through every hail cycle since it was built. Here is the timeline behind Arlington claims.",
    "body": """
<h2>The Mayfest hailstorm, May 5, 1995</h2>
<p>The Fort Worth hailstorm's path continued east into Arlington, damaging roofs across the city and establishing the first of many hail cycles on Arlington's post-war neighborhoods.</p>
<h2>The April 3, 2012 tornado outbreak</h2>
<p>Multiple tornadoes crossed the southern Metroplex in one afternoon. One tracked through Kennedale and south Arlington, tossing tractor-trailers at a truck yard and destroying homes in the Forest Hill corridor. Structural scope disputes on homes paid as repairable followed, and many were resolved by appraisal.</p>
<h2>Hail seasons through the 2010s</h2>
<p>Storms maturing over western Tarrant County reach Arlington fully developed. Carriers repaired roofs in one year and called them worn the next, and the depreciation and repairability arguments that define Arlington appraisals grew out of that cycle.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Burst lines in Arlington's older housing and in its large apartment inventory produced claims paid as single-room losses when water had traveled across units and floors.</p>
<h2>The May 28, 2024 wind event</h2>
<p>Hurricane-force gusts crossed the Mid-Cities, stripping roofing and fences and bringing down trees across north and east Arlington.</p>
<h2>What this history means for your claim</h2>
<p>Accepted, underpaid tornado, hail, freeze and wind claims are the appraisal clause's territory. An <a href="{city_url}">{kw}</a> can be appointed to settle the amount of loss on any of them. Roof disputes run through <a href="{hail}">hail and roof claim appraisal</a>, wind and tornado through <a href="{wind}">windstorm appraisal</a>, and the apartment complexes along Cooper and Collins through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"corpus-christi": {
    "title": "Corpus Christi Storm History: Celia, Allen, Harvey and Hanna",
    "description": "Hurricanes Celia, Allen, Harvey and Hanna, plus the 2021 freeze: the storms behind Corpus Christi and Coastal Bend insurance claims, and what each meant for policyholders.",
    "h1": "Corpus Christi Storm History: <span>Celia, Allen, Harvey and Hanna</span>",
    "intro": "The Coastal Bend takes hurricanes head-on, and its claims history is a list of landfalls. Here is the record and what each storm means for a dispute today.",
    "body": """
<h2>Hurricane Celia, August 3, 1970</h2>
<p>Celia struck Corpus Christi directly with gusts estimated near 160 miles per hour, destroying or damaging most of the city's buildings. It is the storm that built the modern Texas windstorm insurance system, including the Texas Windstorm Insurance Association that writes much of the coast today.</p>
<h2>Hurricane Allen, August 1980</h2>
<p>Allen weakened before landfall north of Brownsville but drove surge and tornadoes across the Coastal Bend, reinforcing the TWIA market and the split between wind and non-wind coverage on coastal policies.</p>
<h2>Hurricane Harvey, August 25, 2017</h2>
<p>Harvey made landfall at Rockport as a Category 4 and devastated Rockport, Port Aransas and Aransas Pass. Many homes were paid as partial losses and later condemned, and the scope gaps on those files were enormous. Harvey claims in Aransas and San Patricio counties were a major appraisal docket for years.</p>
<h2>Hurricane Hanna, July 25, 2020</h2>
<p>Hanna crossed Padre Island as a Category 1 and pushed wind and water across Nueces and Kleberg counties. Windward slopes paid, leeward slopes denied, interior intrusion omitted: the coastal pattern again.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Even the coast froze. Slab-level supply lines and exposed plumbing in Corpus Christi's mid-century housing burst, and access-cost disputes followed.</p>
<h2>What this history means for your claim</h2>
<p>Coastal claims split between standard carriers and TWIA, and each has its own appraisal process. A <a href="{city_url}">{kw}</a> who works both can be appointed to settle the amount of loss on an accepted, underpaid Harvey, Hanna or freeze claim. Hurricane and wind losses run through <a href="{wind}">hurricane and windstorm appraisal</a>, and plumbing losses through <a href="{water}">water damage appraisal</a>.</p>
""",
},
"plano": {
    "title": "Plano Storm History: Collin County Hail and the 2021 Freeze",
    "description": "The March 2016 Collin County hailstorm, the spring seasons since, Winter Storm Uri and the May 2024 wind event: the storms behind Plano insurance claims.",
    "h1": "Plano Storm History: <span>Collin County Hail and the 2021 Freeze</span>",
    "intro": "Plano's roofs were built in two waves and Collin County hail finds both. Here is the timeline behind Plano claims and what each event means for a dispute today.",
    "body": """
<h2>The March 2016 hailstorms</h2>
<p>Late March 2016 brought baseball-sized hail across Wylie, east Plano and Murphy, and a second round in April across the county. Tens of thousands of roofs installed in the same few years with the same shingle lines were hit at once, and the matching disputes that define Plano appraisals were born.</p>
<h2>Hail seasons since</h2>
<p>Collin County has taken damaging hail in most springs since 2016. Carriers depreciate Plano roofs steeply because they know the frequency, and HOA uniformity rules turn every partial approval into a dispute.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Plano's two-story housing meant upstairs pipe failures damaged every floor below. Carriers paid single-room scopes on many of those claims.</p>
<h2>The May 28, 2024 wind event</h2>
<p>The Metroplex derecho crossed Plano with damaging gusts, stripping roofing and fences across the city's Legacy-area and east Plano neighborhoods.</p>
<h2>What this history means for your claim</h2>
<p>Matching, depreciation and multi-floor water scope are amount-of-loss disputes, which is what a <a href="{city_url}">{kw}</a> is appointed to settle under the appraisal clause. Roof claims run through <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and Legacy-area commercial roofs through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"lubbock": {
    "title": "Lubbock Storm History: Tornado, Blizzards, Hail and Dust",
    "description": "The 1970 Lubbock tornado, the South Plains blizzards and ice storms, the hail seasons and the haboobs: the weather events behind Lubbock insurance claims.",
    "h1": "Lubbock Storm History: <span>Tornado, Blizzards, Hail and Dust</span>",
    "intro": "Lubbock's weather is the most varied of any large Texas city: a historic tornado, large hail, blizzards, ice and blowing dust. Here is the record behind South Plains claims.",
    "body": """
<h2>The May 11, 1970 Lubbock tornado</h2>
<p>An F5 tornado struck downtown Lubbock and the north side, killing twenty-six people and damaging the Great Plains Life Building so badly it stood empty for years. The storm reshaped tornado engineering nationally and remains the benchmark for structural claims in the city.</p>
<h2>Blizzards and ice storms</h2>
<p>South Plains winters bring ice storms that snap limbs onto roofs and collapse carports, and blizzards that shut the roads so adjusters scope from photographs. The February 2021 freeze added burst lines in homes with crawl-space plumbing.</p>
<h2>Hail every spring</h2>
<p>Caprock hail is frequent and often large. Carrier estimates approve the roof and omit the evaporative coolers, screens, fences, painted metal and metal shops that the same storm destroyed.</p>
<h2>Haboobs and dust storms</h2>
<p>Walls of dust off the plains drive fine grit through attic vents, around windows and into ductwork. Carriers frequently decline the cleaning scope or deny dust intrusion entirely.</p>
<h2>What this history means for your claim</h2>
<p>Accepted hail, ice, freeze and dust claims paid short on scope are what a <a href="{city_url}">{kw}</a> is appointed to settle. Roof and collateral damage runs through <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and the cotton gins, barns and Loop 289 commercial roofs through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"irving": {
    "title": "Irving Storm History: The 2012 Hail, Uri and the 2024 Wind Event",
    "description": "The June 2012 hailstorm, the hail cycles since, Winter Storm Uri and the May 2024 derecho: the storms behind Irving and Las Colinas insurance claims.",
    "h1": "Irving Storm History: <span>The 2012 Hail, Uri and the 2024 Wind Event</span>",
    "intro": "Irving sits between Dallas and Fort Worth under the same supercells, with a dense inventory of hotels and office roofs near the airport. Here is the timeline behind Irving claims.",
    "body": """
<h2>The June 13, 2012 hailstorm</h2>
<p>The storm that hammered Dallas that evening continued across Irving, damaging roofs in south Irving's post-war neighborhoods and the hotels and office parks along State Highway 114. It remains the largest single hail event in the city's modern record.</p>
<h2>Hail cycles through the 2010s</h2>
<p>Irving's 1970s and 1980s roofs in north Irving reached end-of-life through repeated hail seasons, and the repair-versus-replace and brittleness disputes that define residential appraisal here followed.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Burst lines in Irving's older housing and in Las Colinas townhomes produced claims where association-versus-owner responsibility had to be sorted before the water scope could even be argued.</p>
<h2>The May 28, 2024 wind event</h2>
<p>The derecho crossed Irving with gusts near hurricane strength, damaging roofing, glass and rooftop equipment on the DFW Airport corridor's hotels and office buildings and fences across the city's neighborhoods.</p>
<h2>What this history means for your claim</h2>
<p>Hail, freeze and wind claims paid short on scope are what an <a href="{city_url}">{kw}</a> is appointed to settle under the appraisal clause. Residential roofs run through <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and the Las Colinas and airport-corridor commercial roofs through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"laredo": {
    "title": "Laredo Storm History: Flash Floods, Hail, Hanna and the Freeze",
    "description": "Flash flooding on Zacate and Chacon creeks, spring hail and wind, Hurricane Hanna's rains and Winter Storm Uri: the weather behind Laredo insurance claims.",
    "h1": "Laredo Storm History: <span>Flash Floods, Hail, Hanna and the Freeze</span>",
    "intro": "Laredo's claims are shaped by heat, sudden storms and the creeks that drain to the Rio Grande. Here is the record behind them and what each event means for a dispute today.",
    "body": """
<h2>Flash flooding on the creeks</h2>
<p>Zacate Creek, Chacon Creek and the arroyos that feed the river flood with little warning when summer storms stall over the city. Interior water claims from those events turn on the entry path: water through a roof or parapet is covered, water that rose from the street often is not.</p>
<h2>Spring hail and wind</h2>
<p>Thunderstorms rolling up from Mexico in spring and early summer bring hail and straight-line wind to roofs that have baked through a decade of summers above a hundred degrees. Carriers lean on that thermal aging to argue wear against storm damage.</p>
<h2>Hurricane Hanna's rains, July 2020</h2>
<p>Hanna's remnants brought heavy rain inland to Webb County, flooding low-lying neighborhoods and producing roof and interior water claims across the city.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Laredo's exposed plumbing froze during the grid failure, and burst-pipe claims followed in homes and in the duplexes and small multifamily buildings that make up much of the city's rental stock.</p>
<h2>What this history means for your claim</h2>
<p>Accepted claims paid short on scope are what a <a href="{city_url}">{kw}</a> is appointed to settle. Roof disputes run through <a href="{hail}">hail and roof claim appraisal</a>, freeze and flood-adjacent water through <a href="{water}">water damage appraisal</a>, and the I-35 warehouse and cold-storage losses through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"garland": {
    "title": "Garland Storm History: The 2015 Tornado and the Hail Corridor",
    "description": "The December 26, 2015 EF-4 tornado, the I-30 hail corridor, Winter Storm Uri and the May 2024 wind event: the storms behind Garland and Rowlett insurance claims.",
    "h1": "Garland Storm History: <span>The 2015 Tornado and the Hail Corridor</span>",
    "intro": "Garland's storm history has one headline event and a long tail of hail. Here is the timeline behind eastern Dallas County claims and what each means for a dispute today.",
    "body": """
<h2>The December 26, 2015 tornado</h2>
<p>An EF-4 tornado crossed Garland and Rowlett the day after Christmas, killing thirteen people, many at the Interstate 30 and President George Bush Turnpike interchange, and destroying hundreds of homes. Claims from that night taught Garland what a partial scope on a structurally damaged house looks like: racked framing, shifted foundations and compromised roof structures paid as repairable.</p>
<h2>The I-30 hail corridor</h2>
<p>Spring hail tracks the I-30 corridor through Garland, Rowlett and Rockwall in most years. Carriers approve partial slopes on Garland's 1960s and 1970s roofs, omit decking and code items and depreciate heavily.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Burst lines across central and south Garland's ranch homes and the apartment complexes along Garland Road produced claims paid short on drying and flooring.</p>
<h2>The May 28, 2024 wind event</h2>
<p>The Metroplex derecho crossed Garland with damaging gusts, stripping roofing and fences and bringing down trees across the city.</p>
<h2>What this history means for your claim</h2>
<p>Tornado, hail, freeze and wind claims that were accepted but underpaid are what a <a href="{city_url}">{kw}</a> is appointed to settle under the appraisal clause. Structural and roof disputes run through <a href="{wind}">windstorm appraisal</a> and <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>.</p>
""",
},
"frisco": {
    "title": "Frisco Storm History: Hail on a City Built in Waves",
    "description": "The 2016 and 2017 Collin County hail seasons, Winter Storm Uri, the May 2024 wind event and the spring hail since: the storms behind Frisco insurance claims.",
    "h1": "Frisco Storm History: <span>Hail on a City Built in Waves</span>",
    "intro": "Frisco's housing was built in a few short waves, which means each hailstorm hits thousands of nearly identical roofs at once. Here is the timeline behind Frisco claims.",
    "body": """
<h2>The 2016 Collin County hail season</h2>
<p>The late-March and April 2016 storms that hammered Wylie and Plano also crossed Frisco's production subdivisions, hitting roofs installed in the same two or three years with shingle lines that would soon be discontinued. The matching problem that defines Frisco appraisals began here.</p>
<h2>The 2017 hail season</h2>
<p>Spring 2017 brought further hail across Collin and Denton counties, including Frisco's estate communities west of the Tollway, where tile and high-end laminate roofs added repairability and matching disputes on larger, more complex roofs.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Frisco's newer two-story homes with PEX run through unconditioned attics failed during the grid outage, and water damage on every floor below the failure was paid as single-room losses on many claims.</p>
<h2>The May 28, 2024 wind event</h2>
<p>The derecho crossed Frisco with gusts near hurricane strength, stripping roofing and fences and damaging rooftop equipment at the Star district and Hall Park.</p>
<h2>Spring hail since</h2>
<p>Collin County hail returns most years, and each storm renews the matching argument on a city of roofs that are young but not identical to anything still manufactured.</p>
<h2>What this history means for your claim</h2>
<p>Matching, code correction and multi-floor water scope are amount-of-loss disputes, and a <a href="{city_url}">{kw}</a> is appointed to settle them under the appraisal clause. Roof claims run through <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and Frisco's commercial campuses through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"mckinney": {
    "title": "McKinney Storm History: Hail Up the US 75 Corridor",
    "description": "The Collin County hail seasons that track up US 75, Winter Storm Uri and the May 2024 wind event: the storms behind McKinney insurance claims on historic and new homes.",
    "h1": "McKinney Storm History: <span>Hail Up the US 75 Corridor</span>",
    "intro": "McKinney's storms intensify over the city as they track up US 75 from Allen, and they land on Victorian homes and brand-new subdivisions alike. Here is the timeline behind McKinney claims.",
    "body": """
<h2>Spring hail seasons, 2016 onward</h2>
<p>The 2016 Collin County hailstorms that hit Plano and Wylie continued north across McKinney, and most springs since have brought damaging hail to the city. In the historic district, carriers underscoped the cost of working on century-old roofs; in Stonebridge Ranch and Craig Ranch, they approved partial slopes on discontinued laminate lines.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>McKinney's two-story housing produced a wave of upstairs pipe failures that damaged every floor below, paid as single-room losses on many claims. The historic district's plaster and custom trim made those scopes larger than carriers allowed.</p>
<h2>The May 28, 2024 wind event</h2>
<p>The derecho crossed McKinney with damaging gusts, stripping roofing and fences across the US 380 corridor's newer subdivisions and bringing down trees in the historic district.</p>
<h2>Severe weather on the US 380 corridor</h2>
<p>The communities along US 380 toward Prosper and Princeton sit in the path of storms that cross northern Collin County, and their builder-grade roofs generate code-correction disputes on every replacement.</p>
<h2>What this history means for your claim</h2>
<p>Accepted hail, freeze and wind claims paid short on scope are what a <a href="{city_url}">{kw}</a> is appointed to settle under the appraisal clause. Roof claims run through <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and historic-district homes through <a href="{home}">homeowners claim appraisal</a> with preservation requirements priced in.</p>
""",
},
"amarillo": {
    "title": "Amarillo Storm History: Blizzards, Giant Hail and Panhandle Wind",
    "description": "The February 2013 and December 2015 blizzards, the Panhandle hail seasons, Winter Storm Uri and the constant wind: the weather events behind Amarillo insurance claims.",
    "h1": "Amarillo Storm History: <span>Blizzards, Giant Hail and Panhandle Wind</span>",
    "intro": "Amarillo's weather is the most severe of any large Texas city, and the carriers that write the Panhandle adjust accordingly. Here is the record behind Amarillo claims.",
    "body": """
<h2>The February 2013 blizzard</h2>
<p>Winter Storm Rocky dropped nineteen inches of snow on Amarillo in a day, the city's second-largest snowfall on record, collapsing carports and awnings and stranding adjusters for days. Claims were scoped from photographs after the roads reopened.</p>
<h2>The December 2015 Goliath blizzard</h2>
<p>A post-Christmas blizzard with hurricane-force gusts and drifts over the eaves closed Interstate 40 and produced roof, carport and livestock-structure claims across Potter and Randall counties.</p>
<h2>Giant hail in spring</h2>
<p>Panhandle supercells drop stones over two inches with regularity. Carrier estimates approve the roof and omit the siding, screens, gutters, fences, condensers and the detached shops and barns on nearly every Amarillo property.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Sustained sub-zero temperatures burst lines in homes with crawl spaces across Wolflin, Oliver-Eakle and the older neighborhoods near downtown, and the freeze claims that followed were adjusted remotely.</p>
<h2>Wind every month</h2>
<p>Sustained Panhandle wind drives rain and snow into attics and wall cavities and lifts shingles between storms. Carriers frequently call the resulting interior damage maintenance.</p>
<h2>What this history means for your claim</h2>
<p>Hail, blizzard, freeze and wind claims paid short on scope are what an <a href="{city_url}">{kw}</a> is appointed to settle under the appraisal clause. Roof and collateral damage runs through <a href="{hail}">hail and roof claim appraisal</a>, wind through <a href="{wind}">windstorm appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and the agricultural and I-40 commercial roofs through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"grand-prairie": {
    "title": "Grand Prairie Storm History: Hail, the 2012 Outbreak and the Freeze",
    "description": "The April 2012 tornado outbreak, the Metroplex hail seasons, Winter Storm Uri and the May 2024 wind event: the storms behind Grand Prairie insurance claims on homes and warehouses.",
    "h1": "Grand Prairie Storm History: <span>Hail, the 2012 Outbreak and the Freeze</span>",
    "intro": "Grand Prairie runs thirty miles north to south across two counties, so one storm can hit lakeside homes and I-30 warehouses the same afternoon. Here is the timeline behind Grand Prairie claims.",
    "body": """
<h2>The April 3, 2012 tornado outbreak</h2>
<p>The outbreak that struck Arlington, Kennedale, Lancaster and Forney crossed the southern Metroplex in one afternoon, and south Grand Prairie's neighborhoods toward Joe Pool Lake took wind and debris damage from the same supercells. Partial scopes on structurally damaged homes became disputes.</p>
<h2>Metroplex hail seasons</h2>
<p>Storms that hit Arlington and Irving hit Grand Prairie between them. North Grand Prairie's post-war ranch homes and the Dalworth rentals carry roofs through repeated cycles, and partial approvals with heavy depreciation follow each one.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Burst lines in older housing and in the lakeside subdivisions' two-story homes produced claims paid short on drying, flooring and the floors below the failure.</p>
<h2>The May 28, 2024 wind event</h2>
<p>The derecho crossed Grand Prairie with hurricane-force gusts, damaging the vast low-slope roofs and rooftop equipment of the city's warehouse and manufacturing inventory along I-30 and I-20, and stripping roofing and fences across neighborhoods.</p>
<h2>What this history means for your claim</h2>
<p>Hail, tornado, freeze and wind claims paid short on scope are what a <a href="{city_url}">{kw}</a> is appointed to settle under the appraisal clause. Residential roofs run through <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and the warehouse membranes through <a href="/services/commercial-property-appraisal/">commercial property appraisal</a>.</p>
""",
},
"brownsville": {
    "title": "Brownsville Storm History: Dolly, Alex, the 2018 Floods and Hanna",
    "description": "Hurricane Dolly, Hurricane Alex's rains, the June 2018 Rio Grande Valley floods, Hurricane Hanna and Winter Storm Uri: the storms behind Brownsville and Cameron County claims.",
    "h1": "Brownsville Storm History: <span>Dolly, Alex, the 2018 Floods and Hanna</span>",
    "intro": "Brownsville and Cameron County take hurricanes head-on and tropical rain that stalls for days. Here is the record behind Valley claims and what each storm means for a dispute today.",
    "body": """
<h2>Hurricane Dolly, July 23, 2008</h2>
<p>Dolly made landfall on South Padre Island as a Category 2 and crawled across Cameron County, dropping more than a foot of rain and damaging roofs from Port Isabel to Harlingen. Dolly claims established the Valley pattern: windward slopes paid, leeward slopes denied, interior intrusion attributed to flood.</p>
<h2>Hurricane Alex, June 30, 2010</h2>
<p>Alex made landfall in Mexico but its rain bands flooded the lower Valley for days, producing interior water claims where the entry path decided coverage.</p>
<h2>The June 2018 floods</h2>
<p>A stalled tropical disturbance dropped more than a foot of rain on Cameron and Hidalgo counties in two days, flooding neighborhoods and resacas across Brownsville, Harlingen and San Benito.</p>
<h2>Hurricane Hanna, July 25, 2020</h2>
<p>Hanna's Category 1 landfall on Padre Island pushed wind and water across the county. Carriers blamed salt-air corrosion for storm-torn flashing and HVAC coils, and the partial-scope pattern repeated on thousands of claims.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Even Brownsville froze. Exposed plumbing in homes never built for cold burst, and freeze claims followed across the county.</p>
<h2>What this history means for your claim</h2>
<p>Valley wind coverage is split between TWIA and standard carriers, each with its own appraisal process. A <a href="{city_url}">{kw}</a> who works both can be appointed to settle the amount of loss on an accepted, underpaid Dolly, Hanna, flood-adjacent or freeze claim. Hurricane losses run through <a href="{wind}">hurricane and windstorm appraisal</a>, water through <a href="{water}">water damage appraisal</a>.</p>
""",
},
"killeen": {
    "title": "Killeen Storm History: Hail, the Salado and Temple Tornadoes, Uri",
    "description": "Bell County hail seasons, the April 2022 Salado tornado, the May 2024 Temple tornado and Winter Storm Uri: the storms behind Killeen and Fort Cavazos insurance claims.",
    "h1": "Killeen Storm History: <span>Hail, the Salado and Temple Tornadoes, Uri</span>",
    "intro": "Bell County sits where the North Texas hail corridor meets Hill Country storm tracks, and Killeen's claims are filed by families who are often somewhere else. Here is the timeline behind them.",
    "body": """
<h2>Spring hail across Bell County</h2>
<p>Killeen takes hail most springs, with the older neighborhoods near downtown and along Rancier Avenue carrying roofs at end-of-life and the newer subdivisions in south Killeen and Harker Heights carrying discontinued laminate lines. Partial approvals, deferred-maintenance discounts and matching disputes follow.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Burst lines across Killeen's rental housing produced claims where absent landlords on orders accepted first estimates and discovered the shortfall when the property manager's contractor bid the job.</p>
<h2>The April 12, 2022 Salado tornado</h2>
<p>An EF-3 tornado struck Salado and the Bell County countryside south of Killeen, injuring more than twenty people and destroying homes along the Interstate 35 corridor. Structural scope disputes on homes paid as repairable followed.</p>
<h2>The May 22, 2024 Temple tornado</h2>
<p>An EF-2 tornado tracked across Temple, damaging hundreds of homes and businesses and reminding the whole county that a routine spring storm can become a catastrophe within minutes.</p>
<h2>What this history means for your claim</h2>
<p>Accepted hail, freeze and tornado claims paid short on scope are what a <a href="{city_url}">{kw}</a> is appointed to settle, and the process works whether you are in Harker Heights or deployed overseas. Roof claims run through <a href="{hail}">hail and roof claim appraisal</a>, tornado damage through <a href="{wind}">windstorm appraisal</a>, and freeze losses through <a href="{water}">water damage appraisal</a>.</p>
""",
},
"denton": {
    "title": "Denton Storm History: Hail at the Top of the Corridor",
    "description": "The Denton County hail seasons that build over Wise and Montague counties, Winter Storm Uri and the May 2024 wind event: the storms behind Denton insurance claims for homeowners and landlords.",
    "h1": "Denton Storm History: <span>Hail at the Top of the Corridor</span>",
    "intro": "Denton sits at the top of the Metroplex hail corridor, where storms mature before they reach the city, and a college town's rental stock takes the damage. Here is the timeline behind Denton claims.",
    "body": """
<h2>Hail from the northwest</h2>
<p>Supercells that build over Wise and Montague counties cross Krum, Sanger and the UNT campus before tracking into Corinth and Lewisville. Denton County's hail frequency rivals Collin County's, and the student-rental neighborhoods around the universities carry roofs through every cycle with deferred maintenance carriers use to discount the damage.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>Burst lines across Denton's older rental stock near UNT and TWU and in the historic homes around the square produced claims where landlord policies were settled at actual cash value and tenant interiors were left out of the scope.</p>
<h2>The May 28, 2024 wind event</h2>
<p>The derecho crossed Denton County with damaging gusts, stripping roofing and fences across the city and the rural edge's barns and outbuildings.</p>
<h2>Severe weather on the rural edge</h2>
<p>Denton County's farms and acreage properties toward Sanger, Aubrey and Krum take hail and wind on barns, shops and metal buildings that carrier estimates price as repairs or omit entirely.</p>
<h2>What this history means for your claim</h2>
<p>Accepted hail, freeze and wind claims paid short on scope, on a home or a rental, are what a <a href="{city_url}">{kw}</a> is appointed to settle under the appraisal clause. Roof claims run through <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and the historic homes around the square through <a href="{home}">homeowners claim appraisal</a>.</p>
""",
},
"mcallen": {
    "title": "McAllen Storm History: The 2012 Hail, the 2018 Floods and Hanna",
    "description": "The March 2012 McAllen hailstorm, Hurricane Dolly, the June 2018 Hidalgo County floods, Hurricane Hanna and Winter Storm Uri: the events behind McAllen and Rio Grande Valley claims.",
    "h1": "McAllen Storm History: <span>The 2012 Hail, the 2018 Floods and Hanna</span>",
    "intro": "The Rio Grande Valley's claim history is written in a few dates, and McAllen was in the path for all of them. Here is the record and what each event means for a dispute today.",
    "body": """
<h2>Hurricane Dolly, July 2008</h2>
<p>Dolly's slow crawl across the Valley brought a foot of rain and damaging wind inland to Hidalgo County, and the partial-scope pattern on tile and stucco homes was established.</p>
<h2>The March 29, 2012 hailstorm</h2>
<p>Baseball-sized hail fell across north McAllen, shredding roofs, windows and vehicles in the costliest hail event in Valley history. Tile roofs were repaired a tile at a time on carrier estimates, and tile-matching disputes defined the appraisals that followed.</p>
<h2>The June 20 and 21, 2018 floods</h2>
<p>A stalled disturbance dropped more than a foot of rain on Hidalgo County in two days, flooding Mission, Weslaco and parts of McAllen. Interior water claims turned on whether water came through the roof or rose from the street.</p>
<h2>Hurricane Hanna, July 25, 2020</h2>
<p>Hanna's wind and rain reached inland across Hidalgo County, damaging roofs and flooding neighborhoods. Windward slopes paid, leeward slopes denied, stucco patched in a different color.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>The Valley froze for the first time in a generation. Exposed plumbing and park-model homes burst lines across the county.</p>
<h2>What this history means for your claim</h2>
<p>Accepted hail, hurricane, flood-adjacent and freeze claims paid short on scope are what a <a href="{city_url}">{kw}</a> is appointed to settle under the appraisal clause. Tile and roof disputes run through <a href="{hail}">hail and roof claim appraisal</a>, hurricane losses through <a href="{wind}">hurricane and windstorm appraisal</a>, and water through <a href="{water}">water damage appraisal</a>.</p>
""",
},
"georgetown": {
    "title": "Georgetown Storm History: Jarrell, Uri and the 2022 Round Rock Tornado",
    "description": "The 1997 Jarrell tornado, Williamson County hail seasons, Winter Storm Uri and the March 2022 Round Rock tornado: the storms behind Georgetown and Sun City insurance claims.",
    "h1": "Georgetown Storm History: <span>Jarrell, Uri and the 2022 Round Rock Tornado</span>",
    "intro": "Williamson County's storms land on a city that has added tens of thousands of roofs in a decade, a large retirement community and a historic limestone square. Here is the timeline behind Georgetown claims.",
    "body": """
<h2>The Jarrell tornado, May 27, 1997</h2>
<p>An F5 tornado destroyed the Double Creek Estates subdivision in Jarrell, fifteen miles north of Georgetown, killing twenty-seven people and scouring homes from their slabs. It remains the benchmark for tornado risk in Williamson County and the reason local building practices changed.</p>
<h2>Hail from the west</h2>
<p>Storms that build over Burnet and Llano counties track east across Liberty Hill, Georgetown and Hutto. Because Georgetown's roofs were installed by the same builders in the same years, each storm hits thousands of identical, now-discontinued shingle lines, and matching becomes a community-scale dispute, especially in Sun City.</p>
<h2>Winter Storm Uri, February 2021</h2>
<p>PEX run through unconditioned attics in new construction and slab-level supply lines in Sun City's single-story homes burst during the grid failure. Carriers paid single-room losses on homes where water ran the length of the house.</p>
<h2>The March 21, 2022 Round Rock tornado</h2>
<p>An EF-2 tornado tracked through Round Rock and toward Granger on the same day a second tornado struck Elgin, damaging homes, businesses and a car dealership along Interstate 35 and reminding Georgetown how close the tornado risk sits.</p>
<h2>What this history means for your claim</h2>
<p>Matching, multi-floor water scope and tornado structural disputes are amount-of-loss questions, which is what a <a href="{city_url}">{kw}</a> is appointed to settle under the appraisal clause. Roof claims run through <a href="{hail}">hail and roof claim appraisal</a>, freeze losses through <a href="{water}">water damage appraisal</a>, and tornado damage through <a href="{wind}">windstorm appraisal</a>.</p>
""",
},
}
