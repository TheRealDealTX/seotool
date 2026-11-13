"""Wisconsin location pages. Local detail is written for each city."""

LOCATIONS = [
    # ------------------------------------------------------------------ Milwaukee
    {
        "slug": "milwaukee", "city": "Milwaukee", "county": "Milwaukee County", "region": "Southeast & Lakeshore",
        "perils": ["Sewer backup", "Flash flooding", "Lake-effect snow", "Frozen pipes", "Wind and hail"],
        "near": ["waukesha", "racine", "kenosha"],
        "housing": "Milwaukee mixes Cream City brick, early bungalows, Polish flats and side-by-side duplexes with postwar ranches and lakefront condominium buildings.",
        "storms": [
            ("July 22, 2010", "Flash flood that sent water and sewage into basements across the city and nearby suburbs"),
            ("February 1–2, 2011", "Groundhog Day blizzard that dropped roughly 20 inches of snow on Milwaukee"),
            ("Late January 2019", "Polar vortex cold that burst pipes and stressed heating systems across the region"),
        ],
        "neighborhoods": ["Bay View", "Washington Heights", "Riverwest", "Sherman Park", "Walker’s Point", "Historic Third Ward", "Lindsay Heights", "Layton Park", "Story Hill", "Wauwatosa"],
        "title": "Milwaukee Insurance Appraiser | Wisconsin Claim Appraisal",
        "desc": "Milwaukee insurance appraiser for Milwaukee County homes, duplexes and condos. Independent appraisal for sewer backup, snow and storm claims.",
        "lede": "Milwaukee claims often start in the basement and end in a disagreement over what an old house really costs to put back. We help owners across Milwaukee County settle those numbers through the appraisal clause.",
        "body": """
<h2>Old houses, big lake, hard winters</h2>
<p>Few cities pack as much building history into a short drive as Milwaukee. A single block in <strong>Washington Heights</strong> or <strong>Bay View</strong> can hold a 1920s bungalow, a Polish flat with a raised basement unit, and a Cream City brick cottage that predates the streetcar. Add the side-by-side duplexes of the north and south sides, the lofts of the Historic Third Ward and Walker’s Point, and the postwar ranches toward the county line, and you have a housing stock that rarely fits a carrier’s default line items.</p>
<p>That matters because pricing software is built around modern framing and drywall. Plaster on wood lath, old-growth trim, soft historic brick and two-unit layouts with shared systems all cost more to repair than a standard estimate assumes.</p>

<h2>Storms that shaped local claims</h2>
<p>Many longtime residents still talk about <em>July 22, 2010</em>, when a flash flood overwhelmed storm and sanitary sewers and pushed water into basements across Milwaukee and neighboring suburbs. The <em>Groundhog Day blizzard</em> of February 1–2, 2011 buried the city under roughly 20 inches of snow, and the polar vortex of late January 2019 brought the kind of cold that splits supply lines inside exterior walls. Lake-effect bands off Lake Michigan add snow load and ice damming to the list nearly every winter.</p>

<h2>Where Milwaukee claims tend to stall</h2>
<ul>
<li><strong>Sewer and water backup limits.</strong> Many policies cap backup coverage with an endorsement. Owners need to know what is subject to the sublimit and what may fall under other coverage. See our page on <a href="/appraisal-solutions/water-sewer-backup-appraisal/">water and sewer backup appraisal</a>.</li>
<li><strong>Finished basements in flats and duplexes.</strong> Lower units, laundry areas and shared mechanicals are often under-scoped.</li>
<li><strong>Plaster, masonry and trim.</strong> Matching Cream City brick or repairing lath and plaster is specialized work.</li>
<li><strong>Ice dams and frozen pipes.</strong> Disputes over whether damage was sudden or long-term are common after deep cold. Our <a href="/appraisal-solutions/ice-dam-frozen-pipe-appraisal/">ice dam and frozen pipe appraisal</a> page explains the issues.</li>
</ul>

<h2>How appraisal helps a Milwaukee owner</h2>
<p>Appraisal is a policy process for settling the <em>amount of loss</em> when you and your carrier agree there is coverage but disagree on the number. Each side names an independent appraiser, and an umpire resolves anything the two cannot agree on. We are not a law firm and not a public adjuster; our role is valuation. We inspect on site, build a line-by-line estimate, and compare it to the carrier’s figures.</p>
<p>As an illustrative example only: if a carrier prices a basement backup at $9,000 using drywall and carpet allowances, but the space has plaster walls, built-ins and a second unit’s furnace, a fully documented scope may come out very differently. Your actual numbers will depend on the property.</p>
<p>If your claim is already stuck, our <a href="/appraisal-solutions/carrier-estimate-review/">carrier estimate review</a> is a sensible first step, and the <a href="/appraisal-process-guide/">appraisal process guide</a> walks through each stage.</p>

<h2>Neighborhoods we serve</h2>
<p>We serve the whole city, including Riverwest, Sherman Park, Lindsay Heights, Layton Park, Story Hill and the East Side, plus nearby Wauwatosa and the rest of Milwaukee County. We also work in <a href="/local-appraisers/waukesha/">Waukesha</a> and <a href="/local-appraisers/racine/">Racine</a>. When you are ready, <a href="/contact-us/">contact us</a> to talk through your claim.</p>
""",
        "faqs": [
            ("My Milwaukee basement flooded from the sewer. Is that covered like other water damage?", "Not always. Many policies exclude sewer backup unless you bought an endorsement, and that endorsement often has its own limit. Appraisal can settle the dollar amount of the loss, but it does not decide coverage questions."),
            ("I own a duplex and live in one unit. Does that change the appraisal?", "It can affect which policy applies and how loss of rents is handled. For the appraisal itself, we scope both units and any shared systems so nothing falls between the cracks."),
            ("Can you match Cream City brick in an estimate?", "We price the repair using appropriate salvage or matching brick and the masonry methods soft historic brick requires, rather than a generic modern brick line item."),
        ],
    },
    # ------------------------------------------------------------------ Madison
    {
        "slug": "madison", "city": "Madison", "county": "Dane County", "region": "South Central",
        "perils": ["Flash flooding", "Tornadoes", "Hail", "Ice dams", "Basement water"],
        "near": ["janesville", "waukesha", "milwaukee"],
        "housing": "Madison pairs early 1900s homes on and near the isthmus with postwar ranches, newer suburban subdivisions and a large share of condominium associations.",
        "storms": [
            ("August 20, 2018", "Record rainfall west of Madison caused flash flooding in Middleton and across western Dane County"),
            ("August 18, 2005", "Tornado outbreak that struck Stoughton and other parts of Dane County"),
            ("June 1984", "F5 tornado that devastated Barneveld in Iowa County, west of Madison"),
        ],
        "neighborhoods": ["Marquette", "Tenney-Lapham", "Vilas", "Dudgeon-Monroe", "Westmorland", "Maple Bluff", "Monona", "Middleton", "Fitchburg", "Sun Prairie"],
        "title": "Madison Insurance Appraiser | Dane County Claim Disputes",
        "desc": "Madison insurance appraiser serving Dane County homes and condo associations. Independent appraisal for flood, hail, wind and water claims.",
        "lede": "Between the lakes, the isthmus and the fast-growing edge of Dane County, Madison sees a wide range of property claims. We help owners settle disputed amounts through the appraisal process.",
        "body": """
<h2>Two lakes and a lot of variety</h2>
<p>Madison’s housing tells the story of the city’s growth. On and near the isthmus, <strong>Marquette</strong>, <strong>Tenney-Lapham</strong> and <strong>Vilas</strong> are full of early 1900s homes with plaster walls, wood windows and steep roofs. Farther out, Westmorland and Dudgeon-Monroe add period revivals and postwar homes, while Fitchburg, Middleton and Sun Prairie have miles of newer subdivisions. Condominium associations are everywhere, from downtown towers to suburban townhome rows.</p>
<p>Each of those property types produces a different kind of claim, and each can expose gaps in a carrier’s estimate.</p>

<h2>What Dane County weather has done</h2>
<p>On <em>August 20, 2018</em>, record rainfall west of Madison turned roads into rivers and flooded basements in Middleton and other western Dane County communities. Thirteen years earlier, the <em>August 18, 2005</em> outbreak sent a tornado through Stoughton. And anyone who has lived here long remembers the June 1984 Barneveld tornado in neighboring Iowa County, a reminder of how violent summer storms can be in south central Wisconsin.</p>
<p>Hail, straight-line wind and winter ice dams round out the picture. Older isthmus homes with limited attic ventilation are especially prone to ice damming.</p>

<h2>Typical Madison claim disagreements</h2>
<h3>Water in finished lower levels</h3>
<p>Surface water, groundwater seepage and sewer backup are treated differently by most policies. Once coverage is sorted out, the fight is often about scope: how much drywall, flooring and cabinetry has to come out, and whether drying was done properly.</p>
<h3>Condo master policy versus unit owner coverage</h3>
<p>When a storm damages a building, the association and the unit owner may both have claims. Our <a href="/appraisal-solutions/commercial-hoa-appraisal/">commercial and HOA appraisal</a> work helps boards and owners value their portion.</p>
<h3>Hail and wind on mixed roofs</h3>
<p>Matching discontinued shingles or repairing older slate and cedar is a frequent point of contention. Read more on our <a href="/appraisal-solutions/hail-roof-damage-appraisal/">hail and roof damage appraisal</a> page.</p>

<h2>Our role in the process</h2>
<p>Appraisal settles the amount of loss when both sides accept that a claim is covered but cannot agree on the price. We serve as your independent appraiser or, when requested, as an umpire. We are not attorneys and we do not act as public adjusters. We inspect on site, measure and document, and prepare a detailed estimate.</p>
<p>As an illustrative example: a carrier might allow $14,000 for a flooded lower level, while a complete scope that includes built-in shelving, a second bathroom and code-required egress work could come out higher. Every property is different, so treat this only as an example of how scopes diverge.</p>
<p>Not sure if appraisal fits your situation? Start with the <a href="/appraisal-process-guide/">appraisal process guide</a> or try our <a href="/insurance-claim-calculators/">claim calculators</a>.</p>

<h2>Communities we cover around Madison</h2>
<p>We serve Madison and all of Dane County, including Maple Bluff, Monona, Middleton, Fitchburg, Verona and Sun Prairie. We also work south in <a href="/local-appraisers/janesville/">Janesville</a> and east toward <a href="/local-appraisers/waukesha/">Waukesha</a>. <a href="/contact-us/">Get in touch</a> to discuss your claim.</p>
""",
        "faqs": [
            ("My Middleton-area basement flooded in a big rainstorm. Can appraisal help?", "If your carrier agrees part of the loss is covered but disputes the amount, appraisal can settle that number. Whether surface water or seepage is covered at all is a coverage question that appraisal does not decide."),
            ("I live in a Madison condo. Who handles the roof claim?", "Usually the association’s master policy covers the roof and common elements, while your unit policy covers interior improvements and belongings. Your association documents control the details."),
        ],
    },
    # ------------------------------------------------------------------ Green Bay
    {
        "slug": "green-bay", "city": "Green Bay", "county": "Brown County", "region": "Fox Valley & Northeast",
        "perils": ["Snow load", "Ice dams", "Frozen pipes", "Wind damage", "Basement water"],
        "near": ["appleton", "oshkosh", "wausau"],
        "housing": "Green Bay has older frame homes near downtown, many postwar ranches and Cape Cods, and newer subdivisions and condos spreading into the surrounding villages.",
        "storms": [
            ("February 1–2, 2011", "Groundhog Day blizzard that brought heavy snow and drifting to much of eastern Wisconsin"),
            ("Late January 2019", "Polar vortex cold that led to frozen and burst pipes across the state"),
            ("Most springs", "Snowmelt and ice along the Fox and East rivers can push water toward low-lying properties"),
        ],
        "neighborhoods": ["Astor Park", "Fort Howard", "Navarino", "Preble", "Allouez", "De Pere", "Ashwaubenon", "Howard", "Bellevue", "Suamico"],
        "title": "Green Bay Insurance Appraiser | Brown County Appraisals",
        "desc": "Green Bay insurance appraiser for homes and businesses in Brown County. Appraisal help for snow load, ice dam, frozen pipe and storm claims.",
        "lede": "Long winters at the mouth of the Fox River put Green Bay roofs and plumbing to the test. When a claim payout looks short, we help Brown County owners use appraisal to settle the amount.",
        "body": """
<h2>A winter city at the mouth of the Fox</h2>
<p>Green Bay sits where the Fox River meets the bay, and its housing reflects more than a century of steady growth. Near downtown, <strong>Astor Park</strong>, <strong>Navarino</strong> and the old <strong>Fort Howard</strong> area on the west side have frame homes with additions stacked over the decades. Postwar ranches and Cape Cods fill much of Preble and the east side, while Ashwaubenon, Howard, Bellevue and Suamico have newer subdivisions and condo associations.</p>
<p>Older homes here often have shallow attics and modest insulation, which is a recipe for ice dams. Newer homes have their own issues, like complex roof lines and finished lower levels full of costly materials.</p>

<h2>Snow, cold and spring water</h2>
<p>Northeast Wisconsin winters are long. The <em>Groundhog Day blizzard</em> of February 1–2, 2011 brought heavy snow and drifting across much of eastern Wisconsin, and the <em>late January 2019</em> polar vortex left many homeowners dealing with burst pipes. Most springs, snowmelt and river ice along the Fox and East rivers raise concerns for low-lying properties. Summer thunderstorms add wind and hail damage to the mix.</p>

<h2>Common sticking points on Green Bay claims</h2>
<ul>
<li><strong>Ice dam water damage.</strong> Carriers may pay for interior stains but question the roof, insulation or sheathing behind them.</li>
<li><strong>Snow load stress.</strong> Sagging rafters, cracked trusses and damaged garages and pole buildings are sometimes written off as wear. Our <a href="/appraisal-solutions/snow-load-roof-collapse-appraisal/">snow load and roof collapse appraisal</a> page covers these losses.</li>
<li><strong>Burst pipes in exterior walls.</strong> Scope often stops at the visible damage rather than following the water through framing and insulation.</li>
<li><strong>Drying and mold remediation.</strong> Disputes about how long drying should take and how much material must be removed are common.</li>
</ul>

<h2>Settling the number through appraisal</h2>
<p>Most Wisconsin homeowners policies include an appraisal clause. When you and your carrier agree a loss is covered but cannot agree on its value, either side can usually demand appraisal. Each names an appraiser, the two try to agree, and an umpire decides any remaining differences. We act as your appraiser, and we can also serve as an umpire. We are not a law firm and not a public adjuster.</p>
<p>We inspect the property in person, document the damage room by room, and build an estimate that reflects local labor and material costs. As an illustrative example, a carrier might allow $6,500 to repair ice dam staining in two bedrooms, while a full scope that includes wet insulation, damaged sheathing and repainting of continuous walls may be considerably more. Your numbers will depend on your home.</p>
<p>Learn more about <a href="/appraisal-solutions/ice-dam-frozen-pipe-appraisal/">ice dam and frozen pipe appraisal</a>, or see how we can <a href="/appraisal-solutions/appraisal-demand-representation/">represent you after an appraisal demand</a>.</p>

<h2>Areas we serve around the bay</h2>
<p>We work throughout Green Bay and Brown County, including Allouez, De Pere, Ashwaubenon, Howard, Bellevue and Suamico. We also serve <a href="/local-appraisers/appleton/">Appleton</a> and <a href="/local-appraisers/oshkosh/">Oshkosh</a> to the south. <a href="/contact-us/">Reach out</a> to talk through your claim.</p>
""",
        "faqs": [
            ("My Green Bay garage roof sagged under heavy snow. Is that a covered loss?", "Many policies cover collapse caused by the weight of snow or ice, though wording varies. If coverage is accepted but the amount is in dispute, appraisal can settle the cost of repair."),
            ("How quickly should I act after an ice dam leak?", "Report the claim promptly, take photos, and dry the area to prevent further damage. Keep receipts for emergency work. Most policies require reasonable steps to protect the property."),
        ],
    },
    # ------------------------------------------------------------------ Kenosha
    {
        "slug": "kenosha", "city": "Kenosha", "county": "Kenosha County", "region": "Southeast & Lakeshore",
        "perils": ["Lake-effect snow", "Wind-driven rain", "Basement flooding", "Frozen pipes", "Hail"],
        "near": ["racine", "milwaukee", "waukesha"],
        "housing": "Kenosha combines older lakefront and uptown homes, many mid-century bungalows and ranches, and newer subdivisions and condos in Pleasant Prairie and Bristol.",
        "storms": [
            ("February 1–2, 2011", "Groundhog Day blizzard that hit southeast Wisconsin with heavy snow and high winds"),
            ("June 2008", "Heavy rains that caused widespread river and basement flooding across southern Wisconsin"),
            ("Late January 2019", "Polar vortex cold that caused frozen and burst pipes across the region"),
        ],
        "neighborhoods": ["Allendale", "Lincoln Park", "Uptown", "Columbus Park", "HarborPark", "Pleasant Prairie", "Somers", "Bristol", "Paddock Lake", "Salem Lakes"],
        "title": "Kenosha Insurance Appraiser | Lakeshore Property Claims",
        "desc": "Kenosha insurance appraiser for Kenosha County homes, condos and businesses. Appraisal for lakeshore wind, snow, water and hail claims.",
        "lede": "Kenosha’s homes face Lake Michigan wind and snow on one side and inland storms on the other. We help Kenosha County owners settle disputed claims through the appraisal clause.",
        "body": """
<h2>Lakefront exposure and a mix of homes</h2>
<p>Kenosha’s waterfront runs along Lake Michigan, where bluffs, harbor wind and lake-effect snow shape how homes weather. Older homes near <strong>Allendale</strong>, <strong>Lincoln Park</strong> and <strong>Uptown</strong> include early frame houses and brick homes, while mid-century bungalows and ranches fill much of the city. The HarborPark area has newer condominiums, and Pleasant Prairie and Bristol have grown with modern subdivisions.</p>
<p>West of I-94, the county turns more rural. Paddock Lake and Salem Lakes have lake homes and seasonal cottages that bring their own claim challenges.</p>

<h2>Notable weather in the area</h2>
<p>The <em>Groundhog Day blizzard</em> of February 1–2, 2011 hit southeast Wisconsin with heavy snow and strong winds. In <em>June 2008</em>, heavy rains caused widespread flooding across southern Wisconsin, including river flooding in several areas. And the polar vortex of <em>late January 2019</em> led to frozen pipes across the region. Lake-effect snow showers along the shoreline add to roof load and ice dam risk in a typical winter.</p>

<h2>What Kenosha claim disputes look like</h2>
<h3>Wind-driven rain and lakefront wear</h3>
<p>Carriers sometimes argue that lakefront siding, windows and roofing were already weathered. Separating storm damage from long-term exposure takes careful inspection and documentation.</p>
<h3>Basement water from heavy rain</h3>
<p>Backup, seepage and surface water each fall under different policy terms. Once coverage is clear, scope and pricing are often still in dispute. Our <a href="/appraisal-solutions/water-sewer-backup-appraisal/">water and sewer backup appraisal</a> page explains what we look for.</p>
<h3>Condo and townhome associations</h3>
<p>Newer associations near the harbor and in Pleasant Prairie often face questions about which policy pays for which component. See our <a href="/appraisal-solutions/commercial-hoa-appraisal/">commercial and HOA appraisal</a> services.</p>
<h3>Hail on roofs and siding</h3>
<p>Spring and summer storms bring hail that can damage shingles, gutters and vinyl siding. Matching materials across a whole elevation is a frequent issue.</p>

<h2>How we help</h2>
<p>We are independent property appraisers, not lawyers or public adjusters. When your carrier agrees there is coverage but disagrees on the amount, appraisal gives both sides a structured way to resolve it. Each party names an appraiser, and an umpire settles any differences the appraisers cannot resolve.</p>
<p>We inspect on site, measure and photograph everything, and prepare a detailed estimate. As an illustrative example, a carrier might offer $11,000 for wind damage to a lakefront home, while a complete scope including matching siding on every affected wall and window replacement could be higher. Actual results depend on the property and policy.</p>
<p>Already have an estimate from your carrier? Our <a href="/appraisal-solutions/carrier-estimate-review/">carrier estimate review</a> can show where the gaps are. The <a href="/appraisal-process-guide/">appraisal process guide</a> explains each step.</p>

<h2>Where we work in Kenosha County</h2>
<p>We serve Kenosha, Pleasant Prairie, Somers, Bristol, Paddock Lake, Salem Lakes and the rest of Kenosha County. We also work north in <a href="/local-appraisers/racine/">Racine</a> and <a href="/local-appraisers/milwaukee/">Milwaukee</a>. <a href="/contact-us/">Contact us</a> to discuss your claim.</p>
""",
        "faqs": [
            ("My Kenosha home is near the lake. Will the carrier blame the damage on weather exposure?", "That argument comes up often. An appraiser can document which damage is consistent with a specific storm and which reflects age, so the amount of loss is based on what the storm actually did."),
            ("Do you inspect lake cottages in western Kenosha County?", "Yes. We inspect on site throughout the county, including lake homes and seasonal properties around Paddock Lake and Salem Lakes."),
        ],
    },
    # ------------------------------------------------------------------ Racine
    {
        "slug": "racine", "city": "Racine", "county": "Racine County", "region": "Southeast & Lakeshore",
        "perils": ["Lake-effect snow", "Wind damage", "Basement water", "Ice dams", "Fire and smoke"],
        "near": ["kenosha", "milwaukee", "waukesha"],
        "housing": "Racine has historic lakefront homes, notable Prairie School architecture, older worker cottages and duplexes, and postwar ranches in Mount Pleasant and Caledonia.",
        "storms": [
            ("February 1–2, 2011", "Groundhog Day blizzard that brought heavy snow and wind to southeast Wisconsin"),
            ("June 2008", "Widespread heavy rain and flooding across southern Wisconsin"),
            ("Late January 2019", "Polar vortex cold that froze pipes in homes and businesses across the region"),
        ],
        "neighborhoods": ["Southside Historic District", "West Racine", "Westside", "Lakeshore", "Elmwood Park", "Mount Pleasant", "Caledonia", "Sturtevant", "Wind Point", "Union Grove"],
        "title": "Racine Insurance Appraiser | Independent Claim Appraisal",
        "desc": "Racine insurance appraiser serving historic and modern homes in Racine County. Appraisal for wind, snow, water, fire and smoke claims.",
        "lede": "Racine’s historic homes and lakefront setting make for claims that need careful, local valuation. We help Racine County owners resolve disputed amounts through appraisal.",
        "body": """
<h2>Architecture worth getting right</h2>
<p>Racine has an unusual architectural legacy for a city its size. It is known for Prairie School design, and the <strong>Southside Historic District</strong> along the lake holds Victorian, Italianate and early 1900s homes with craftsmanship that is hard to replicate. Elsewhere in the city, worker cottages and duplexes near the Root River sit alongside mid-century homes in West Racine, while Mount Pleasant, Caledonia and Sturtevant have postwar ranches and newer subdivisions.</p>
<p>When a home has custom millwork, art glass, plaster walls or original wood windows, a standard estimate built from modern line items can miss a lot.</p>

<h2>Lake Michigan weather</h2>
<p>Racine sits right on Lake Michigan, and that shapes its winters. The <em>Groundhog Day blizzard</em> of February 1–2, 2011 brought heavy snow and wind to southeast Wisconsin. In <em>June 2008</em>, heavy rain caused widespread flooding across southern Wisconsin. The <em>late January 2019</em> polar vortex led to frozen pipes across the area. Lake-effect snow, shoreline wind and ice dams are part of a normal winter here.</p>

<h2>Disputes we see on Racine properties</h2>
<ul>
<li><strong>Historic materials priced as modern.</strong> Plaster, old-growth trim and specialty windows are often replaced in estimates with cheaper substitutes.</li>
<li><strong>Fire and smoke damage.</strong> Older homes with balloon framing can let smoke travel through wall cavities, and scope disagreements are common. See our <a href="/appraisal-solutions/fire-smoke-damage-appraisal/">fire and smoke damage appraisal</a> page.</li>
<li><strong>Wind damage near the lake.</strong> Carriers may argue that shoreline wear, not a storm, caused the damage.</li>
<li><strong>Basement water.</strong> Root River area homes and older basements can see water from several sources, each with different coverage.</li>
<li><strong>Ice dams on complex roofs.</strong> Older homes with multiple dormers and valleys are prone to ice damming.</li>
</ul>

<h2>The appraisal process in brief</h2>
<p>Appraisal settles the amount of a covered loss when you and your carrier disagree. Each side selects an appraiser, the appraisers try to agree, and an umpire resolves any remaining items. We act as your appraiser or serve as an umpire. We are not a law firm or a public adjuster; we focus on what the damage costs to repair.</p>
<p>We inspect in person, research materials and methods, and prepare a detailed estimate. As an illustrative example, a carrier might allow $18,000 for smoke and water damage in a historic home, while a scope that accounts for plaster repair, trim matching and wall-cavity cleaning could be much higher. Every claim is different.</p>
<p>If you are unsure where to start, our <a href="/appraisal-process-guide/">appraisal process guide</a> explains each step. If the carrier has already demanded appraisal, learn about our <a href="/appraisal-solutions/appraisal-demand-representation/">appraisal demand representation</a>.</p>

<h2>Communities we serve</h2>
<p>We work throughout Racine and Racine County, including Mount Pleasant, Caledonia, Sturtevant, Wind Point and Union Grove. We also serve <a href="/local-appraisers/kenosha/">Kenosha</a> and <a href="/local-appraisers/milwaukee/">Milwaukee</a>. <a href="/contact-us/">Contact us</a> to talk about your claim.</p>
""",
        "faqs": [
            ("My Racine home is in a historic district. Does that affect the claim?", "It can. If local rules require specific materials or methods, the cost of repair may be higher, and ordinance or law coverage may come into play. An appraiser should price the repair the way it actually has to be done."),
            ("Can you help with smoke damage from a neighbor’s fire?", "Yes. Smoke from a nearby fire can damage your home, and we can document and price cleaning, deodorizing and repairs as part of an appraisal."),
        ],
    },
    # ------------------------------------------------------------------ Appleton
    {
        "slug": "appleton", "city": "Appleton", "county": "Outagamie County", "region": "Fox Valley & Northeast",
        "perils": ["Hail", "Wind damage", "Snow load", "Ice dams", "Frozen pipes"],
        "near": ["oshkosh", "green-bay", "wausau"],
        "housing": "Appleton’s housing runs from older homes near College Avenue and City Park to postwar ranches and large newer subdivisions in Grand Chute, Harrison and Fox Crossing.",
        "storms": [
            ("July 1996", "F5 tornado at Oakfield in Fond du Lac County, south of Lake Winnebago, one of the strongest in state history"),
            ("Late January 2019", "Polar vortex cold that caused frozen pipes throughout the Fox Valley"),
            ("February 1–2, 2011", "Groundhog Day blizzard that brought heavy snow to much of eastern Wisconsin"),
        ],
        "neighborhoods": ["City Park", "College Avenue", "Grand Chute", "Little Chute", "Kimberly", "Kaukauna", "Menasha", "Neenah", "Fox Crossing", "Harrison"],
        "title": "Appleton Insurance Appraiser | Fox Valley Claim Help",
        "desc": "Appleton insurance appraiser serving Outagamie County and parts of Calumet and Winnebago counties. Appraisal for storm, snow and water claims.",
        "lede": "Appleton straddles three counties and a lot of housing styles. We help Fox Valley owners settle disputed claim amounts through the appraisal clause.",
        "body": """
<h2>A city along the Fox River</h2>
<p>Appleton grew up along the Fox River, and its neighborhoods show it. Around <strong>City Park</strong> and the blocks near College Avenue, older homes have plaster walls, wood floors and detailed trim. Postwar ranches and split-levels fill much of the city, and Grand Chute, Harrison and Fox Crossing have grown with larger newer homes. Most of the city is in <strong>Outagamie County</strong>, with portions in Calumet and Winnebago counties.</p>
<p>Nearby Kimberly, Little Chute, Kaukauna, Menasha and Neenah share the same weather and many of the same claim issues. Lake Winnebago sits just south of the city, and storms that build over the open water can arrive with little warning. Because Appleton spans three counties, permit offices and local code requirements can differ from one side of a street to the other, which affects what a repair truly costs.</p>

<h2>Fox Valley storm history</h2>
<p>The Fox Valley sees severe summer thunderstorms with hail and straight-line wind. To the south, the <em>July 1996</em> Oakfield tornado in Fond du Lac County was rated F5 and remains one of the strongest in Wisconsin history. Winter brings its own risks: the <em>February 1–2, 2011</em> Groundhog Day blizzard dropped heavy snow across eastern Wisconsin, and the <em>late January 2019</em> polar vortex caused frozen pipes throughout the region.</p>

<h2>Where Appleton claims get stuck</h2>
<h3>Hail on newer, larger roofs</h3>
<p>Newer homes in Grand Chute and Harrison often have large, complex roofs. Carriers sometimes approve only partial repairs when matching shingles are unavailable. Our <a href="/appraisal-solutions/hail-roof-damage-appraisal/">hail and roof damage appraisal</a> page explains how we approach these claims.</p>
<h3>Wind damage after summer storms</h3>
<p>Straight-line wind can tear off shingles, siding and fencing and drop trees on homes. Learn more about <a href="/appraisal-solutions/tornado-straight-line-wind-appraisal/">tornado and straight-line wind appraisal</a>.</p>
<h3>Snow load and ice dams</h3>
<p>Heavy, wet snow can stress roofs and garages, and ice dams cause interior water damage that is often under-scoped.</p>
<h3>Frozen pipes</h3>
<p>Deep cold can burst pipes inside exterior walls, and the hidden damage behind finished surfaces is easy to miss.</p>

<h2>How appraisal works for you</h2>
<p>When your carrier agrees there is coverage but you cannot agree on the amount, the appraisal clause in most policies gives both sides a way forward. Each names an appraiser, and an umpire settles what the appraisers cannot. We are independent appraisers, not attorneys or public adjusters.</p>
<p>We inspect on site, document every area of damage, and prepare a detailed estimate. As an illustrative example, a carrier might approve $8,000 to repair one roof slope, while a full scope that reflects unavailable matching shingles across the whole roof could be higher. Your results will depend on your home and policy.</p>
<p>Use our <a href="/insurance-claim-calculators/">claim calculators</a> for a rough sense of your numbers, or read the <a href="/appraisal-process-guide/">appraisal process guide</a>.</p>

<h2>Where we serve in the Fox Valley</h2>
<p>We work throughout Appleton, Grand Chute, Little Chute, Kimberly, Kaukauna, Menasha, Neenah, Fox Crossing and Harrison. We also serve <a href="/local-appraisers/oshkosh/">Oshkosh</a> and <a href="/local-appraisers/green-bay/">Green Bay</a>. <a href="/contact-us/">Contact us</a> to talk about your claim.</p>
""",
        "faqs": [
            ("Part of Appleton is in Calumet County. Does that change anything?", "Not for the appraisal itself. Your policy terms and the damage are what matter. Local permit and code requirements can vary by municipality, and we account for those in the estimate."),
            ("My carrier will only replace one side of my hail-damaged roof. Can appraisal help?", "If the dispute is about the amount needed to repair the covered damage, including matching, appraisal can address it. Whether matching is required may depend on policy language and Wisconsin rules."),
        ],
    },
    # ------------------------------------------------------------------ Waukesha
    {
        "slug": "waukesha", "city": "Waukesha", "county": "Waukesha County", "region": "Southeast & Lakeshore",
        "perils": ["Hail", "Wind damage", "Basement water", "Ice dams", "Frozen pipes"],
        "near": ["milwaukee", "madison", "racine"],
        "housing": "Waukesha County includes historic downtown homes, many postwar ranches and split-levels, large newer subdivisions, condo associations and lake homes.",
        "storms": [
            ("July 22, 2010", "Heavy rain and flash flooding in the Milwaukee metro area that caused widespread basement and sewer backups"),
            ("February 1–2, 2011", "Groundhog Day blizzard that brought heavy snow to southeast Wisconsin"),
            ("Late January 2019", "Polar vortex cold that led to frozen and burst pipes across the region"),
        ],
        "neighborhoods": ["Downtown Waukesha", "Brookfield", "Pewaukee", "New Berlin", "Menomonee Falls", "Muskego", "Delafield", "Hartland", "Oconomowoc", "Sussex"],
        "title": "Waukesha Insurance Appraiser | Home & HOA Claim Appraisal",
        "desc": "Waukesha insurance appraiser for homes, condos and HOAs in Waukesha County. Appraisal for hail, wind, water backup and winter damage claims.",
        "lede": "Waukesha County’s suburbs, lake homes and condo communities each bring their own claim challenges. We help owners settle disputed amounts through appraisal.",
        "body": """
<h2>Suburbs, lakes and associations</h2>
<p>Waukesha County is one of the state’s fastest-growing areas, and its housing shows it. <strong>Downtown Waukesha</strong> has historic homes along the Fox River, while Brookfield, New Berlin and Menomonee Falls are full of postwar ranches and split-levels. Pewaukee, Hartland, Sussex and Oconomowoc have large newer subdivisions, and lake homes line Pewaukee Lake, Okauchee Lake and the lakes around Delafield and Oconomowoc. Condominium and homeowners associations are common across the county.</p>
<p>Each of these property types brings different claim issues, from old plaster to luxury finishes to shared roofs. A 1950s ranch in New Berlin and a five-year-old two-story in Sussex may sit under the same storm, but their repair costs, materials and code upgrades will look nothing alike. Higher-end finishes, such as stone veneer, engineered hardwood and custom cabinetry, are where we most often see estimates fall short, because generic line items rarely capture the real price of matching them.</p>

<h2>Weather history in the county</h2>
<p>The <em>July 22, 2010</em> storm brought heavy rain to the Milwaukee metro area, with widespread basement flooding and sewer backups. The <em>Groundhog Day blizzard</em> of February 1–2, 2011 buried southeast Wisconsin in heavy snow, and the <em>late January 2019</em> polar vortex caused frozen pipes across the region. Hail and straight-line wind are regular threats in summer.</p>

<h2>Common claim disputes in Waukesha County</h2>
<ul>
<li><strong>HOA and condo claims.</strong> Associations and unit owners often disagree with carriers on roof, siding and common area repairs. See our <a href="/appraisal-solutions/commercial-hoa-appraisal/">commercial and HOA appraisal</a> services.</li>
<li><strong>Hail on large roofs.</strong> Newer homes have big, complex roofs, and partial repair offers are a frequent point of contention.</li>
<li><strong>Finished basements.</strong> Basements with bars, theaters and bathrooms can be expensive to restore after water backup. Learn about <a href="/appraisal-solutions/water-sewer-backup-appraisal/">water and sewer backup appraisal</a>.</li>
<li><strong>Lake homes.</strong> Wind and ice can damage docks, boathouses and lakeside structures, and coverage for these varies.</li>
<li><strong>Frozen pipes.</strong> Burst pipes can cause hidden damage that is easy to under-scope.</li>
</ul>

<h2>What we do</h2>
<p>We are independent property appraisers. We are not a law firm and not a public adjuster. When your carrier accepts coverage but disputes the amount, appraisal is a way to resolve it. Each side names an appraiser, and an umpire settles any remaining differences.</p>
<p>We inspect on site, document the damage thoroughly, and prepare a detailed estimate. As an illustrative example, a carrier might offer $25,000 for a finished basement after a backup, while a full scope that includes custom cabinetry, a wet bar and a bathroom could come out higher. Your numbers will depend on the property and policy.</p>
<p>For associations choosing a neutral umpire, our <a href="/appraisal-solutions/umpire-selection-services/">umpire selection services</a> may help. You can also read the <a href="/appraisal-process-guide/">appraisal process guide</a>.</p>

<h2>Communities we cover</h2>
<p>We serve Waukesha, Brookfield, Pewaukee, New Berlin, Menomonee Falls, Muskego, Delafield, Hartland, Oconomowoc and Sussex. We also work in <a href="/local-appraisers/milwaukee/">Milwaukee</a> and <a href="/local-appraisers/madison/">Madison</a>. <a href="/contact-us/">Contact us</a> to discuss your claim.</p>
""",
        "faqs": [
            ("Our Waukesha County condo association disagrees with the carrier on a roof claim. Can you help?", "Yes. We work with associations on master policy claims, documenting damage across buildings and preparing estimates for the appraisal process."),
            ("Does my policy cover my dock or boathouse on the lake?", "Coverage for docks and boathouses varies widely. Some policies cover them as other structures; others limit or exclude them. Appraisal settles the amount of a covered loss, not whether coverage applies."),
        ],
    },
    # ------------------------------------------------------------------ Eau Claire
    {
        "slug": "eau-claire", "city": "Eau Claire", "county": "Eau Claire County", "region": "Western & Driftless",
        "perils": ["Snow load", "Wind damage", "Hail", "Frozen pipes", "Barn and outbuilding damage"],
        "near": ["la-crosse", "wausau", "madison"],
        "housing": "Eau Claire has older homes near the rivers and downtown, postwar ranches, student rentals near the university and farm properties in the surrounding countryside.",
        "storms": [
            ("February 2019", "Heavy snow after the polar vortex that led to numerous roof and barn collapses in western Wisconsin"),
            ("Late January 2019", "Polar vortex cold that caused frozen pipes across the state"),
            ("July 2019", "Severe storms and downbursts that damaged trees and buildings in parts of northern and western Wisconsin"),
        ],
        "neighborhoods": ["Third Ward", "Randall Park", "Eastside Hill", "Putnam Heights", "North Side", "Altoona", "Chippewa Falls", "Lake Hallie", "Fall Creek", "Lake Wissota"],
        "title": "Eau Claire Insurance Appraiser | Chippewa Valley Claims",
        "desc": "Eau Claire insurance appraiser serving Eau Claire County and Chippewa County homes and farms. Appraisal for snow, wind and hail claims.",
        "lede": "Eau Claire’s winters and summer storms can be hard on homes, farms and outbuildings. We help Chippewa Valley owners settle disputed claims through appraisal.",
        "body": """
<h2>Where two rivers meet</h2>
<p>Eau Claire grew up where the Chippewa and Eau Claire rivers come together, and the city still centers on the water. Older neighborhoods like the <strong>Third Ward</strong>, <strong>Randall Park</strong> and <strong>Eastside Hill</strong> have early 1900s homes with plaster walls and wood trim. Postwar ranches fill much of the north and west sides, student rentals cluster near the university, and Altoona and Lake Hallie have newer subdivisions. Most of the city is in Eau Claire County, with a portion in Chippewa County.</p>
<p>Outside the city, farms, barns and pole buildings are a big part of the landscape, along with lake homes around Lake Wissota. Many rural properties carry farm policies with separate schedules for each building, and older dairy barns with stone foundations and timber frames can be difficult to price with tools built for suburban homes. Getting the building description right at the start often decides how fair the final number will be.</p>

<h2>Weather in the Chippewa Valley</h2>
<p>Western Wisconsin winters can be severe. After the <em>late January 2019</em> polar vortex, <em>February 2019</em> brought heavy snow, and western Wisconsin saw numerous roof and barn collapses. In <em>July 2019</em>, severe storms and downbursts damaged trees and buildings in parts of northern and western Wisconsin. Hail and straight-line wind are regular summer threats.</p>

<h2>Common disputes on Eau Claire claims</h2>
<h3>Snow load and collapse</h3>
<p>Carriers sometimes argue that a collapse was caused by age or poor construction rather than snow weight. Our <a href="/appraisal-solutions/snow-load-roof-collapse-appraisal/">snow load and roof collapse appraisal</a> page explains how we document these losses.</p>
<h3>Barns and outbuildings</h3>
<p>Older barns and pole buildings are often hard to value, and replacement cost and actual cash value disputes are common. See our <a href="/appraisal-solutions/farm-barn-outbuilding-appraisal/">farm, barn and outbuilding appraisal</a> services.</p>
<h3>Wind and tree damage</h3>
<p>Summer storms can drop trees on homes and garages. Scope disagreements often involve tree removal, framing repair and interior damage.</p>
<h3>Rental properties</h3>
<p>Student rentals near campus may involve multiple units, loss of rent and tenant contents, which can complicate claims.</p>

<h2>How appraisal can help</h2>
<p>Appraisal settles the amount of a covered loss when you and your carrier disagree on the number. Each side names an appraiser, and an umpire resolves anything they cannot agree on. We are independent appraisers, not attorneys or public adjusters.</p>
<p>We inspect on site, including rural properties, and prepare detailed estimates. As an illustrative example, a carrier might offer $20,000 for a collapsed pole building based on depreciated value, while a scope reflecting current materials and labor could be higher. Results depend on your policy and property.</p>
<p>Read our <a href="/appraisal-process-guide/">appraisal process guide</a> to learn more, or have us do a <a href="/appraisal-solutions/carrier-estimate-review/">carrier estimate review</a>.</p>

<h2>Areas we serve</h2>
<p>We work in Eau Claire, Altoona, Chippewa Falls, Lake Hallie, Fall Creek and the surrounding countryside. We also serve <a href="/local-appraisers/la-crosse/">La Crosse</a> and <a href="/local-appraisers/wausau/">Wausau</a>. <a href="/contact-us/">Contact us</a> to talk through your claim.</p>
""",
        "faqs": [
            ("My barn near Eau Claire collapsed under snow. Is that covered?", "Many farm and homeowners policies cover collapse from the weight of snow or ice, but terms vary. If coverage is accepted and the amount is in dispute, appraisal can settle the value."),
            ("Do you inspect rural properties outside Eau Claire?", "Yes. We inspect on site throughout the Chippewa Valley, including farms, outbuildings and lake properties."),
        ],
    },
    # ------------------------------------------------------------------ Oshkosh
    {
        "slug": "oshkosh", "city": "Oshkosh", "county": "Winnebago County", "region": "Fox Valley & Northeast",
        "perils": ["Wind damage", "Hail", "Ice dams", "Basement water", "Frozen pipes"],
        "near": ["appleton", "green-bay", "madison"],
        "housing": "Oshkosh has older homes near downtown and the lake, many postwar ranches and Cape Cods, student rentals near campus and lake cottages along Lake Winnebago and Lake Butte des Morts.",
        "storms": [
            ("July 1996", "F5 tornado at Oakfield in Fond du Lac County, south of Lake Winnebago"),
            ("Late January 2019", "Polar vortex cold that caused frozen pipes throughout the region"),
            ("June 2008", "Heavy rains that caused widespread flooding in southern and central Wisconsin"),
        ],
        "neighborhoods": ["Millers Bay", "Menominee Park", "Westhaven", "Algoma", "Town of Oshkosh", "Omro", "Winneconne", "Neenah", "Fox Crossing", "Lake Butte des Morts"],
        "title": "Oshkosh Insurance Appraiser | Winnebago County Claims",
        "desc": "Oshkosh insurance appraiser for Winnebago County homes, rentals and lake properties. Appraisal for wind, hail, ice dam and water claims.",
        "lede": "Oshkosh sits on the shore of Lake Winnebago, where wind, ice and storms test homes every year. We help owners settle disputed claims through appraisal.",
        "body": """
<h2>Living on Lake Winnebago</h2>
<p>Oshkosh sits on the west shore of Lake Winnebago, where the Fox River enters the lake. Older homes near downtown, <strong>Millers Bay</strong> and <strong>Menominee Park</strong> have plaster walls, wood floors and detailed trim. Postwar ranches and Cape Cods fill much of the city, Westhaven has newer homes, and student rentals cluster near the university. Lake cottages and year-round homes line Lake Winnebago and Lake Butte des Morts.</p>
<p>All of these property types share the same lake-driven weather, but each brings its own claim issues. Wind comes across Lake Winnebago with nothing to slow it down, so east-facing walls and roofs along the shore take the brunt of summer squall lines. In winter, the lake freezes and shoreline ice can shove against docks, seawalls and boathouses. Inland, older frame homes near the Fox River often have basements that were never designed to stay dry, which complicates water claims when a sump fails or a drain backs up.</p>

<h2>What to have ready before an inspection</h2>
<p>A smooth appraisal starts with good records. Before we visit, it helps to gather:</p>
<ul>
<li>Your full policy, including declarations pages and any endorsements.</li>
<li>Every estimate and letter from your carrier.</li>
<li>Photos and video from the day of the loss, and older photos if you have them.</li>
<li>Receipts for emergency repairs, drying or tarping.</li>
</ul>

<h2>Storm history nearby</h2>
<p>South of Lake Winnebago, the <em>July 1996</em> Oakfield tornado in Fond du Lac County was rated F5. In <em>June 2008</em>, heavy rains caused widespread flooding in southern and central Wisconsin. The <em>late January 2019</em> polar vortex caused frozen pipes throughout the region. Summer storms with wind and hail are common, and winter brings ice dams and heavy snow.</p>

<h2>Typical Oshkosh claim disputes</h2>
<ul>
<li><strong>Wind damage to lakefront homes.</strong> Carriers sometimes attribute damage to wear rather than a specific storm. Learn about <a href="/appraisal-solutions/tornado-straight-line-wind-appraisal/">tornado and straight-line wind appraisal</a>.</li>
<li><strong>Hail on roofs and siding.</strong> Matching discontinued materials is a common issue.</li>
<li><strong>Ice dams.</strong> Older homes with limited insulation often see ice dam damage that is under-scoped. See <a href="/appraisal-solutions/ice-dam-frozen-pipe-appraisal/">ice dam and frozen pipe appraisal</a>.</li>
<li><strong>Basement water.</strong> Homes near the lake and river can see water from several sources.</li>
<li><strong>Rental properties.</strong> Multi-unit rentals can involve loss of rents and tenant issues.</li>
</ul>

<h2>Appraisal, explained simply</h2>
<p>If your carrier agrees a loss is covered but disagrees on the amount, the appraisal clause in most policies lets either side demand appraisal. Each side names an appraiser, and an umpire settles any differences. We are independent appraisers, not a law firm or public adjuster.</p>
<p>We inspect on site and prepare detailed estimates. As an illustrative example, a carrier might allow $7,500 for wind damage to a lake cottage, while a full scope including siding, windows and a damaged deck could come out higher. Results depend on the property and policy.</p>
<p>Want to know more first? Read the <a href="/appraisal-process-guide/">appraisal process guide</a> or try the <a href="/insurance-claim-calculators/">claim calculators</a>.</p>

<h2>Where we work</h2>
<p>We serve Oshkosh, the Town of Oshkosh, Omro, Winneconne, Neenah, Fox Crossing and the rest of Winnebago County. We also work in <a href="/local-appraisers/appleton/">Appleton</a> and <a href="/local-appraisers/green-bay/">Green Bay</a>. <a href="/contact-us/">Contact us</a> to talk through your claim.</p>
""",
        "faqs": [
            ("My cottage on Lake Winnebago was damaged by wind. Can appraisal help?", "If your carrier accepts coverage but disputes the amount, appraisal can settle the value of repairs. We inspect lake properties on site."),
            ("I own rental property near the Oshkosh campus. Can you appraise multi-unit losses?", "Yes. We document damage across all units and shared areas so the estimate reflects the full loss."),
        ],
    },
    # ------------------------------------------------------------------ Janesville
    {
        "slug": "janesville", "city": "Janesville", "county": "Rock County", "region": "South Central",
        "perils": ["River flooding", "Tornadoes", "Hail", "Basement water", "Frozen pipes"],
        "near": ["madison", "waukesha", "milwaukee"],
        "housing": "Janesville has historic homes on Courthouse Hill, many mid-century homes built during its manufacturing years and newer subdivisions on the east and north sides.",
        "storms": [
            ("June 2008", "Heavy rains that pushed the Rock River out of its banks and flooded parts of Janesville"),
            ("August 18, 2005", "Tornado outbreak that struck Stoughton in Dane County, just north of Rock County"),
            ("Late January 2019", "Polar vortex cold that caused frozen pipes across the region"),
        ],
        "neighborhoods": ["Courthouse Hill", "Look West", "Fourth Ward", "Downtown Janesville", "Milton", "Beloit", "Edgerton", "Evansville", "Footville", "Orfordville"],
        "title": "Janesville Insurance Appraiser | Rock County Appraisals",
        "desc": "Janesville insurance appraiser for Rock County homes and businesses. Appraisal for river flooding, tornado, hail and water damage claims.",
        "lede": "Janesville’s history along the Rock River includes floods and storms that test homes and businesses. We help Rock County owners settle disputed claims through appraisal.",
        "body": """
<h2>A river town with deep roots</h2>
<p>Janesville grew up along the Rock River and has a rich architectural history. <strong>Courthouse Hill</strong> and <strong>Look West</strong> have historic homes with Victorian and Italianate details, while the <strong>Fourth Ward</strong> has older worker homes. Mid-century homes built during the city’s manufacturing years fill many neighborhoods, and newer subdivisions have grown on the east and north sides.</p>
<p>Older homes bring plaster, old-growth trim and complex roofs, while newer homes bring finished basements and larger footprints. Many of the city’s mid-century houses have been remodeled more than once, so a single wall might hide several layers of paneling, drywall and plaster. That history matters when an adjuster prices a repair from a quick walk-through, because the real tear-out and rebuild often turn out larger than the first estimate allows.</p>
<p>Rural Rock County adds farmsteads, machine sheds and older barns around Footville and Orfordville, while Milton and Edgerton have small-town homes and lake properties nearby.</p>

<h2>Floods and storms</h2>
<p>In <em>June 2008</em>, heavy rains pushed the Rock River out of its banks and flooded parts of Janesville. Just north, the <em>August 18, 2005</em> tornado outbreak struck Stoughton in Dane County. The <em>late January 2019</em> polar vortex caused frozen pipes across the region. Summer storms with hail and wind are common.</p>

<h2>Where Janesville claims often stall</h2>
<h3>Flood versus other water</h3>
<p>Most homeowners policies exclude flood, but water damage from other sources may be covered. Separating the two is often the first battle. Once coverage is clear, scope and pricing disputes follow. See <a href="/appraisal-solutions/water-sewer-backup-appraisal/">water and sewer backup appraisal</a>.</p>
<h3>Historic homes</h3>
<p>Courthouse Hill homes often need specialized repair methods that standard estimates miss.</p>
<h3>Wind and hail</h3>
<p>Summer storms damage roofs and siding, and matching materials is a frequent dispute. Our <a href="/appraisal-solutions/hail-roof-damage-appraisal/">hail and roof damage appraisal</a> page has more.</p>
<h3>Commercial and rental properties</h3>
<p>Small businesses and rental owners face their own valuation questions. Learn about <a href="/appraisal-solutions/commercial-hoa-appraisal/">commercial and HOA appraisal</a>.</p>

<h2>How we help</h2>
<p>We are independent property appraisers, not lawyers or public adjusters. When your carrier accepts coverage but disputes the amount, appraisal provides a way to settle it. Each side names an appraiser, and an umpire resolves differences.</p>
<p>We inspect on site and prepare detailed estimates. As an illustrative example, a carrier might allow $12,000 for water damage to a historic home, while a full scope reflecting plaster repair and trim matching could be higher. Results depend on the property and policy.</p>
<p>Timing matters too. Most policies set deadlines for reporting a loss and for filing suit, and the appraisal clause usually spells out how quickly each side must name an appraiser. Read your policy carefully, and keep copies of every letter and estimate you receive.</p>
<p>Read the <a href="/appraisal-process-guide/">appraisal process guide</a> or ask us for a <a href="/appraisal-solutions/carrier-estimate-review/">carrier estimate review</a>.</p>

<h2>Communities we serve</h2>
<p>We work in Janesville, Milton, Beloit, Edgerton, Evansville, Footville, Orfordville and the rest of Rock County. We also serve <a href="/local-appraisers/madison/">Madison</a> and <a href="/local-appraisers/waukesha/">Waukesha</a>. <a href="/contact-us/">Contact us</a> to discuss your claim.</p>
""",
        "faqs": [
            ("My Janesville home took on water when the Rock River rose. Is that covered?", "River flooding is usually excluded from homeowners policies and covered only by separate flood insurance. Other water sources may be covered. Appraisal settles the amount of a covered loss, not coverage."),
            ("Do you work on historic homes on Courthouse Hill?", "Yes. We price repairs using appropriate materials and methods for older homes rather than generic modern line items."),
        ],
    },
    # ------------------------------------------------------------------ La Crosse
    {
        "slug": "la-crosse", "city": "La Crosse", "county": "La Crosse County", "region": "Western & Driftless",
        "perils": ["Tornadoes", "Wind damage", "Hail", "River flooding", "Frozen pipes"],
        "near": ["eau-claire", "madison", "wausau"],
        "housing": "La Crosse has Victorian homes downtown and on the south side, postwar homes on the north side, student rentals near campus and newer subdivisions in Onalaska and Holmen.",
        "storms": [
            ("May 22, 2011", "EF2 tornado that damaged homes and businesses on the north side of La Crosse"),
            ("Late January 2019", "Polar vortex cold that caused frozen pipes throughout the state"),
            ("Most springs", "Snowmelt and rain can raise the Mississippi, Black and La Crosse rivers toward low-lying properties"),
        ],
        "neighborhoods": ["North Side", "Goosetown", "Washburn", "Powell-Poage-Hamilton", "French Island", "Onalaska", "Holmen", "Campbell", "Shelby", "West Salem"],
        "title": "La Crosse Insurance Appraiser | Driftless Claim Appraisal",
        "desc": "La Crosse insurance appraiser serving La Crosse County homes and businesses. Appraisal for tornado, wind, hail and water damage claims.",
        "lede": "La Crosse sits between the Mississippi River and towering bluffs, a setting that brings both beauty and risk. We help owners settle disputed claims through appraisal.",
        "body": """
<h2>Bluffs, rivers and Victorian homes</h2>
<p>La Crosse sits on the Mississippi River below the bluffs of the Driftless Area. Downtown and the south side have Victorian homes with ornate trim, plaster walls and complex roofs, while <strong>Goosetown</strong>, <strong>Washburn</strong> and <strong>Powell-Poage-Hamilton</strong> have older homes of many styles. The <strong>North Side</strong> has postwar homes, student rentals cluster near campus, and Onalaska and Holmen have newer subdivisions.</p>
<p>The bluffs and rivers shape both the weather and the risks homes face here. Storms often roll in from the west across the Mississippi and the bluffs of the neighboring state, and the river valley can funnel wind through town. Many older homes sit on narrow lots with large old trees, so a single storm can mean roof, gutter, siding and fence damage all at once.</p>
<p>Victorian homes deserve special attention. Their wood shingles, slate or patterned roofs, carved brackets and wraparound porches take skilled trades to repair, and those trades are in demand after a big storm. An estimate that assumes standard asphalt shingles and stock trim can leave an owner well short of what the repair actually costs.</p>

<h2>Notable storms</h2>
<p>On <em>May 22, 2011</em>, an EF2 tornado struck the north side of La Crosse, damaging homes and businesses. The <em>late January 2019</em> polar vortex caused frozen pipes throughout the state. Most springs, snowmelt and rain raise the Mississippi, Black and La Crosse rivers, putting low-lying properties on French Island and elsewhere at risk.</p>

<h2>Common disputes on La Crosse claims</h2>
<ul>
<li><strong>Tornado and wind damage.</strong> Scope disputes over structural repairs, roofs and siding are common. See <a href="/appraisal-solutions/tornado-straight-line-wind-appraisal/">tornado and straight-line wind appraisal</a>.</li>
<li><strong>Victorian homes.</strong> Ornate trim, plaster and complex roofs are often under-priced in standard estimates.</li>
<li><strong>Hail on roofs.</strong> Matching discontinued materials is a frequent issue. Learn more about <a href="/appraisal-solutions/hail-roof-damage-appraisal/">hail and roof damage appraisal</a>.</li>
<li><strong>Water damage.</strong> River flooding is usually excluded, but other water damage may be covered.</li>
<li><strong>Rental properties.</strong> Student rentals can involve multiple units and loss of rents.</li>
</ul>

<h2>What appraisal can do</h2>
<p>Appraisal settles the amount of a covered loss when you and your carrier disagree. Each side names an appraiser, and an umpire resolves differences. We are independent appraisers, not attorneys or public adjusters.</p>
<p>We inspect on site and prepare detailed estimates. As an illustrative example, a carrier might allow $15,000 for wind damage to a Victorian home, while a full scope including ornate trim and slate repair could be higher. Results depend on the property and policy.</p>
<p>Learn more in the <a href="/appraisal-process-guide/">appraisal process guide</a>, or see our <a href="/appraisal-solutions/home-insurance-appraisal/">home insurance appraisal</a> services.</p>

<h2>Areas we serve</h2>
<p>We work in La Crosse, Onalaska, Holmen, Campbell, Shelby, West Salem and the rest of La Crosse County. We also serve <a href="/local-appraisers/eau-claire/">Eau Claire</a> and <a href="/local-appraisers/madison/">Madison</a>. <a href="/contact-us/">Contact us</a> to talk about your claim.</p>
""",
        "faqs": [
            ("My La Crosse home has ornate Victorian trim. Will the estimate account for that?", "It should. We price repairs using appropriate materials and craftsmanship rather than generic modern trim."),
            ("Does my policy cover Mississippi River flooding?", "Usually not. River flooding is typically covered only by separate flood insurance. Appraisal settles the amount of a covered loss, not coverage."),
        ],
    },
    # ------------------------------------------------------------------ Wausau
    {
        "slug": "wausau", "city": "Wausau", "county": "Marathon County", "region": "Central & North Woods",
        "perils": ["Snow load", "Wind damage", "Ice dams", "Frozen pipes", "Tree damage"],
        "near": ["eau-claire", "green-bay", "appleton"],
        "housing": "Wausau has historic homes in the Andrew Warren district and on the east side, postwar ranches, newer homes near Rib Mountain and Weston, and lake cottages farther north.",
        "storms": [
            ("July 2019", "Derecho and downburst winds that flattened timber and damaged buildings across parts of northern and central Wisconsin"),
            ("Late January 2019", "Polar vortex cold that caused frozen pipes across the state"),
            ("Most winters", "Heavy snow and long cold stretches that stress roofs and plumbing in central Wisconsin"),
        ],
        "neighborhoods": ["Andrew Warren Historic District", "East Hill", "Rib Mountain", "Weston", "Schofield", "Rothschild", "Kronenwetter", "Mosinee", "Marathon City", "Brokaw"],
        "title": "Wausau Insurance Appraiser | Marathon County Claims",
        "desc": "Wausau insurance appraiser serving Marathon County homes, cabins and businesses. Appraisal for snow load, wind, ice dam and tree damage claims.",
        "lede": "Wausau winters are long and summer storms can be fierce. We help Marathon County owners settle disputed claims through appraisal.",
        "body": """
<h2>Gateway to the North Woods</h2>
<p>Wausau sits along the Wisconsin River in the shadow of Rib Mountain. The <strong>Andrew Warren Historic District</strong> and <strong>East Hill</strong> have historic homes with ornate details, while postwar ranches fill much of the city. Weston, Schofield and Rothschild have newer subdivisions, and Rib Mountain has larger homes on wooded lots. Farther north, lake cottages and cabins dot the landscape.</p>
<p>Heavy tree cover and long winters shape the claims we see here. Tall pines and hardwoods grow close to many homes, and a single downburst can bring several down at once. Rib Mountain’s slopes add drainage challenges for homes below, while the Wisconsin River and its tributaries run through the heart of the metro.</p>
<p>The housing mix matters as well. Historic homes on East Hill have plaster walls and detailed millwork. Postwar ranches have shallow attics that invite ice dams. Newer homes in Weston and Kronenwetter often have vaulted ceilings, large windows and finished lower levels, all of which raise the cost of repair when water gets in.</p>

<h2>Weather in central Wisconsin</h2>
<p>In <em>July 2019</em>, derecho and downburst winds flattened timber and damaged buildings across parts of northern and central Wisconsin. The <em>late January 2019</em> polar vortex caused frozen pipes across the state. Most winters bring heavy snow and long cold stretches that stress roofs and plumbing.</p>

<h2>Common Wausau claim disputes</h2>
<h3>Tree damage</h3>
<p>Wooded lots mean trees often fall on homes, garages and cabins. Disputes over removal costs, structural repair and interior damage are common. See <a href="/appraisal-solutions/tornado-straight-line-wind-appraisal/">tornado and straight-line wind appraisal</a>.</p>
<h3>Snow load</h3>
<p>Heavy snow can damage roofs, garages and outbuildings. Learn about <a href="/appraisal-solutions/snow-load-roof-collapse-appraisal/">snow load and roof collapse appraisal</a>.</p>
<h3>Ice dams and frozen pipes</h3>
<p>Long cold stretches cause ice dams and burst pipes, and hidden damage is easy to miss. See <a href="/appraisal-solutions/ice-dam-frozen-pipe-appraisal/">ice dam and frozen pipe appraisal</a>.</p>
<h3>Cabins and seasonal homes</h3>
<p>Damage to cabins may go unnoticed for weeks, and carriers may question the timing. A frozen pipe that bursts in January might not be found until the spring opening, by which time water has soaked floors and walls. Clear records of visits, heating settings and caretaker checks can make a real difference in how the claim is handled.</p>

<h2>How we help</h2>
<p>We are independent property appraisers, not a law firm or public adjuster. When your carrier accepts coverage but disputes the amount, appraisal provides a way to settle it. Each side names an appraiser, and an umpire resolves differences.</p>
<p>We inspect on site and prepare detailed estimates. As an illustrative example, a carrier might allow $10,000 for tree damage to a home, while a full scope including roof framing and interior repairs could be higher. Results depend on the property and policy.</p>
<p>Read the <a href="/appraisal-process-guide/">appraisal process guide</a> or try our <a href="/insurance-claim-calculators/">claim calculators</a>.</p>

<h2>Areas we serve</h2>
<p>We work in Wausau, Rib Mountain, Weston, Schofield, Rothschild, Kronenwetter, Mosinee and the rest of Marathon County. We also serve <a href="/local-appraisers/eau-claire/">Eau Claire</a> and <a href="/local-appraisers/green-bay/">Green Bay</a>. <a href="/contact-us/">Contact us</a> to discuss your claim.</p>
""",
        "faqs": [
            ("A tree fell on my Wausau home in a storm. Can appraisal help?", "If your carrier accepts coverage but disputes the amount, appraisal can settle the cost of tree removal and repairs."),
            ("My cabin up north was damaged over the winter. Will the carrier question the timing?", "It may. Documenting when you last visited and when the damage was discovered can help. Appraisal settles the amount of a covered loss."),
        ],
    },
]
