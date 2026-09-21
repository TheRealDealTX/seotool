"""The seventeen Roof Tarp metro pages.

These replace the 158 near-duplicate /service-areas/roof-tarp-<city>/ pages on
the WordPress site. Those pages were 98.17%-98.55% identical to one another --
the city name was the only thing that changed -- and Google's August 2026 spam
update demoted the whole domain for it on 21 August 2026.

Selection is evidence-based rather than exhaustive. Every metro kept here
earned clicks or meaningful impressions in the 16-month Search Console export;
the 131 city pages that earned zero clicks in 16 months are not rebuilt.

Each page carries its own county, geography, storm profile, roof-covering mix
and response detail. The storm profile is the real differentiator: Gulf
tropical systems on the coast, hail alley through DFW and I-35, High Plains
wind in Lubbock, desert monsoon in El Paso, pine fall in the Piney Woods.
validate.py fails the build if any two pages exceed the similarity threshold.
"""

from siteconfig import BIZ

PHONE = BIZ["phone_display"]

AREAS = [
    # --------------------------------------------------------------- Houston
    {
        "slug": "roof-tarp-houston",
        "city": "Houston",
        "county": "Harris County",
        "keyword": "roof tarp houston",
        "title": "Roof Tarp Houston TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Houston, TX. Hurricane and tropical storm response across "
            "Harris County, 24/7. Call (512) 297-7580."
        ),
        "blurb": "Gulf tropical systems, prolonged wind loading and wind-driven rain.",
        "hero_intro": (
            "Houston roofs fail differently from the rest of Texas. Tropical systems do not hit with a "
            "single gust and move on &mdash; they load a roof for hours, and wind-driven rain finds gaps "
            "that an ordinary thunderstorm never reaches. A <strong>roof tarp in Houston</strong> has to be "
            "anchored for sustained loading, not a brief squall."
        ),
        "storm_profile": """
<h2>What damages Houston roofs</h2>
<p>The defining hazard here is the tropical system. Hurricanes and tropical storms moving inland from
the Gulf subject a roof to many hours of continuous wind loading, often with the wind backing around
through 180 degrees as the centre passes. A roof that survives the first half of a storm can fail in
the second when the load arrives from the opposite direction and catches an edge that was previously
sheltered.</p>
<p>Wind-driven rain is the second Houston-specific problem. Rain moving horizontally penetrates ridge
vents, soffit vents, flashing laps and shingle courses that shed vertical rain perfectly well. Houston
homeowners regularly report interior water with no visible roof damage at all &mdash; the covering is
intact, but it was never designed to resist rain arriving sideways at 60mph.</p>
<p>Harris County's flat terrain and heavy clay soils compound it. There is nowhere for water to go
quickly, so a roof breach during a flooding event often means water rising from below at the same time
it is coming through above.</p>
""",
        "local_detail": """
<h3>Working across Harris County</h3>
<p>Houston is geographically enormous and the damage from a single system is rarely uniform across it.
A storm tracking up the Houston Ship Channel does different damage in Pasadena and Baytown than the
same system does out in Katy or Cypress. We cover the metro broadly &mdash; inside the Loop, the
Energy Corridor, Clear Lake, Spring, Humble, Kingwood, Sugar Land and the Woodlands corridor &mdash;
and prioritise by severity rather than by postcode.</p>
<p>Housing stock matters here too. Large parts of the metro are 1960s-1980s asphalt shingle on
relatively low-pitch roofs, which strip readily in sustained wind. Newer master-planned communities to
the north and west carry more architectural shingle and some standing-seam metal, which fails less
often but is harder to tarp without creating new penetrations.</p>
""",
        "faqs": [
            ("Can you tarp a roof in Houston before a hurricane makes landfall?",
             "Yes, and pre-storm covering of an already-damaged roof is worth doing if there is time. "
             "What we will not do is work once tropical-storm-force wind has arrived &mdash; at that "
             "point a tarp becomes a sail and the crew is at genuine risk."),
            ("Why is my Houston ceiling wet when the roof looks fine?",
             "Almost always wind-driven rain. Horizontal rain gets through ridge and soffit vents, "
             "flashing laps and shingle courses that handle vertical rain without any trouble. The "
             "covering is intact; it was simply never designed for rain arriving sideways."),
            ("How fast can you reach me in Harris County after a major storm?",
             "We aim to be on site within hours, but after a landfalling system the whole metro is "
             "calling at once and access is often the constraint &mdash; flooded roads and debris close "
             "routes. We triage by severity: open decking and active interior water first."),
        ],
    },

    # ---------------------------------------------------------------- Dallas
    {
        "slug": "roof-tarp-dallas",
        "city": "Dallas",
        "county": "Dallas County",
        "keyword": "roof tarp dallas",
        "title": "Roof Tarp Dallas TX | Emergency Hail Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Dallas, TX. Hail and spring supercell response across "
            "Dallas County, 24/7. Call (512) 297-7580."
        ),
        "blurb": "Hail alley &mdash; spring supercells and narrow, destructive hail swaths.",
        "hero_intro": (
            "Dallas sits in the most hail-prone metro in the United States. A <strong>roof tarp in "
            "Dallas</strong> is usually a hail job rather than a wind job, and hail damage has a "
            "characteristic that makes it awkward: it frequently is not visible from the ground, so "
            "people discover the problem weeks later when the roof starts leaking."
        ),
        "storm_profile": """
<h2>Why Dallas roofs take such a beating</h2>
<p>Dallas County sits where dryline convection fires in spring and matures into supercells as it moves
east. Those storms produce the large hail this metro is known for &mdash; and North Texas has produced
some of the costliest hailstorms on record.</p>
<p>The operationally important feature of hail is how narrow the damage swath is. A hail core is
commonly a mile or two wide. One subdivision gets destroyed while the neighbourhood across the highway
is completely untouched. This is why "everyone else's roof is fine" tells you nothing about your own,
and why a per-property inspection matters more with hail than with any other hazard.</p>
<p>Spring storms here also carry damaging straight-line wind and the occasional tornado, so a single
system often produces both stripped shingle fields and impact damage in the same neighbourhood.</p>
""",
        "local_detail": """
<h3>Working across Dallas County</h3>
<p>We cover the county broadly &mdash; East Dallas, Oak Cliff, Lake Highlands, Preston Hollow, Far
North Dallas, plus Garland, Mesquite, Irving, Richardson and Grand Prairie. After a hail event the
calls arrive in a tight geographic band, which actually makes scheduling easier: if your street was
hit, your neighbours almost certainly were too, and we will do several houses in one visit.</p>
<p>Older Dallas housing stock carries a lot of three-tab asphalt shingle, which is the most
hail-vulnerable common covering &mdash; the mat fractures readily and granule loss is immediate.
Newer construction across the northern suburbs uses impact-rated architectural shingle, which performs
considerably better but is not immune at larger stone sizes.</p>
""",
        "faqs": [
            ("My Dallas roof was hit by hail but I cannot see damage. Do I need a tarp?",
             "Probably not immediately. If nothing is penetrated and nothing is leaking, what you need "
             "is an inspection and a claim rather than a tarp. Check your gutters for granule "
             "accumulation and your AC condenser for dented fins &mdash; both are reliable proxies for "
             "what hit the roof."),
            ("How narrow are hail swaths in North Texas really?",
             "Often just one to two miles wide. It is completely normal for one side of a road to have "
             "destroyed roofs and the other side to be untouched. Judge your own roof, not the street."),
            ("Everyone in my neighbourhood needs tarping at once. Can you handle that?",
             "Yes, and it is the efficient way to do it. Hail damage is geographically concentrated by "
             "nature, so doing a whole street in one visit is normal for us after a Dallas hail event."),
        ],
    },

    # ------------------------------------------------------------ Fort Worth
    {
        "slug": "roof-tarp-fort-worth",
        "city": "Fort Worth",
        "county": "Tarrant County",
        "keyword": "roof tarp fort worth",
        "title": "Roof Tarp Fort Worth TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Fort Worth, TX. Hail and tornado response across Tarrant "
            "County, 24/7. Call (512) 297-7580."
        ),
        "blurb": "Western edge of the metroplex &mdash; storms arrive here first.",
        "hero_intro": (
            "Fort Worth takes the metroplex's weather before Dallas does. Storms moving in off the "
            "dryline reach Tarrant County first, often at their most intense, and frequently with a "
            "tornado risk that has already dropped off by the time the same system reaches eastern "
            "Dallas County. A <strong>roof tarp in Fort Worth</strong> is often a mixed-damage job."
        ),
        "storm_profile": """
<h2>First in line for the dryline</h2>
<p>Tarrant County's position on the western side of the metroplex puts it closest to where spring
convection initiates. Storms here are often still in their most violent phase &mdash; discrete
supercells rather than the merged line they become further east. That means Fort Worth sees a higher
proportion of tornado and very large hail events relative to its neighbours.</p>
<p>The practical consequence for tarping is that damage here is more often mixed. A single storm
produces impact damage from hail, stripped shingle fields from straight-line wind, and in the worst
cases structural damage from a tornado &mdash; sometimes on the same street. Each of those needs a
different approach, and the structural cases need assessing before anyone gets on the roof at all.</p>
<p>Tarrant County also sits over the Barnett Shale, and a good deal of the western county is
semi-rural, which means longer drives and more properties with outbuildings and metal roofing than
the eastern metroplex.</p>
""",
        "local_detail": """
<h3>Working across Tarrant County</h3>
<p>We cover Fort Worth proper &mdash; the near Southside, TCU area, Arlington Heights, Ridglea, Alliance
and the far north growth corridor &mdash; plus Keller, Southlake, Haltom City, North Richland Hills and
the western county out toward Weatherford.</p>
<p>Metal roofing is noticeably more common here than in Dallas, particularly on rural and semi-rural
properties and outbuildings. Metal changes the tarping method entirely: standing-seam and corrugated
panels are never penetrated for a temporary cover, so anchoring is by seam clamp and ballast. Hail
denting on metal may be cosmetic, but where the coating has split it will corrode, and that needs
covering.</p>
""",
        "faqs": [
            ("Does Fort Worth really get worse storms than Dallas?",
             "Often more intense ones, yes &mdash; Tarrant County is closer to where spring storms "
             "initiate, so they arrive here in a more violent, discrete phase. Dallas frequently gets "
             "the same system after it has merged into a line and weakened somewhat."),
            ("Can you tarp a metal roof without drilling it?",
             "Yes, and on metal we do that as standard. Seam clamps and ballast hold the cover without "
             "any fastener entering the panel &mdash; a screw through standing seam creates a leak that "
             "outlives the tarp."),
            ("Do you cover the rural parts of Tarrant County?",
             "Yes, out toward Weatherford and the western county. Drive times are longer, so tell us "
             "your location when you call and we will give you a realistic arrival window."),
        ],
    },

    # ---------------------------------------------------------------- Austin
    {
        "slug": "roof-tarp-austin",
        "city": "Austin",
        "county": "Travis County",
        "keyword": "roof tarping austin",
        "title": "Roof Tarp Austin TX | Emergency Roof Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Austin, TX. Hail and hill country storm response across "
            "Travis County, 24/7. Call (512) 297-7580."
        ),
        "blurb": "Hill country terrain, flash flood alley and spring hail off the I-35 corridor.",
        "hero_intro": (
            "Austin sits where the Balcones Escarpment meets the Blackland Prairie, and that terrain "
            "break drives the weather. Storms moving east off the hill country intensify as they hit the "
            "escarpment, which is why <strong>roof tarping in Austin</strong> clusters so heavily along "
            "the I-35 corridor in spring."
        ),
        "storm_profile": """
<h2>The escarpment effect</h2>
<p>Travis County straddles one of the sharpest terrain transitions in Texas. Moist Gulf air moving
inland is forced upward by the Balcones Escarpment, which enhances convection right where the hill
country meets the city. The result is that Austin sits in what is often called flash flood alley, and
that the storms producing hail here frequently intensify in the last few miles before they arrive.</p>
<p>For roofs, the practical outcome is spring hail plus intense short-duration rainfall. Austin storms
tend to dump a great deal of water very quickly, which matters enormously for a compromised roof: a
breach that would leak slowly in a steady rain takes on a very large volume in a hill country
downpour.</p>
<p>Tree fall is a secondary but real cause here, particularly in the older central neighbourhoods with
mature live oak and pecan canopy. Limb strikes during a wind event are a common call.</p>
""",
        "local_detail": """
<h3>Working across Travis County</h3>
<p>We cover central Austin &mdash; Hyde Park, Travis Heights, Tarrytown, Mueller, East Austin &mdash;
plus the western hill country suburbs around Westlake, Lakeway and Bee Cave, and the northern and
eastern growth corridors through Pflugerville, Round Rock, Manor and Del Valle.</p>
<p>The western hill country properties bring their own complication: steep sites, long driveways, heavy
tree cover and frequently metal or tile roofing. Access is genuinely harder there, and a crew that can
reach a Mueller bungalow in twenty minutes may need considerably longer to get to a Lakeway property
with a gated, sloped approach.</p>
<p>Central Austin's older housing stock includes a good deal of low-pitch roofing on mid-century
construction, where wind gets under a leading edge easily and water spreads laterally under the
covering rather than running off.</p>
""",
        "faqs": [
            ("Why do Austin storms cause so much water damage so fast?",
             "Rainfall intensity. Hill country storms dump a large volume in a short window &mdash; this "
             "is flash flood alley. A roof breach that would drip in a steady rain takes on serious "
             "water in an Austin downpour, so the window between damage and tarping matters more here."),
            ("Do you cover the hill country suburbs west of Austin?",
             "Yes &mdash; Westlake, Lakeway, Bee Cave and the surrounding area. Steep sites, gated "
             "approaches and heavy tree cover make access slower, so allow more time than for a central "
             "Austin address."),
            ("A tree limb came through my roof in central Austin. What now?",
             "Tell us when you call, because the limb usually has to come off before a tarp can go on "
             "and how it is removed matters &mdash; dragging it can widen the opening considerably. "
             "Stay out of the room below in the meantime."),
        ],
    },

    # ----------------------------------------------------------- San Antonio
    {
        "slug": "roof-tarp-san-antonio",
        "city": "San Antonio",
        "county": "Bexar County",
        "keyword": "roof tarp san antonio",
        "title": "Roof Tarp San Antonio TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in San Antonio, TX. Hail and tile roof tarping across Bexar "
            "County, 24/7. Call (512) 297-7580."
        ),
        "blurb": "Heavy clay and concrete tile &mdash; ballasted covers, no fasteners.",
        "hero_intro": (
            "San Antonio has a higher proportion of clay and concrete tile roofing than any other major "
            "Texas metro, and that single fact changes how <strong>roof tarping in San Antonio</strong> "
            "has to be done. Tile is brittle, walkable only along specific lines, and utterly unforgiving "
            "of a crew that treats it like asphalt shingle."
        ),
        "storm_profile": """
<h2>Tile roofs and hail: a difficult combination</h2>
<p>Bexar County sits at the southern end of the I-35 hail corridor and takes regular spring hail. Tile
responds to hail very differently from asphalt: rather than bruising, it cracks and shatters. A single
large stone can split a tile outright, and once a tile is broken the underlayment beneath is exposed to
direct sun and rain &mdash; which is what actually causes the leak, usually some weeks later.</p>
<p>The complication is sourcing. Tile profiles change over the decades and older ones are frequently
discontinued, so replacing twenty broken tiles on a 1980s roof can mean hunting for a match or
re-covering a whole plane. That makes the wait for a repair longer here than in a shingle metro, which
in turn makes the tarp specification more important.</p>
<p>Bexar County also catches the northern edge of Gulf moisture surges, so tropical remnants moving
inland bring heavy rain events well away from the coast.</p>
""",
        "local_detail": """
<h3>Working across Bexar County</h3>
<p>We cover the metro broadly &mdash; Alamo Heights, Stone Oak, the Medical Center, Southtown, the far
north along US-281 and 1604, plus Helotes, Converse and Schertz.</p>
<p>On tile, our method is non-negotiable: walking boards to spread load, a planned route across
load-bearing points, as few crossings of the field as possible, and ballasted anchoring with no
fastener entering a tile. Careless tarping breaks more tile than the storm did, and given the sourcing
problem above, that is an expensive mistake to make on someone else's roof.</p>
<p>The newer northern suburbs carry more architectural asphalt shingle, which is considerably more
straightforward &mdash; board-wrapped anchoring applies there as it would anywhere else.</p>
""",
        "faqs": [
            ("Will you break my tiles putting a tarp on?",
             "Not if it is done properly. We use walking boards, plan a route across load-bearing "
             "points, minimise crossings and anchor by ballast rather than fastening through tile. "
             "Breakage happens when a crew treats tile like shingle."),
            ("Some of my tiles are cracked but nothing is leaking yet. Is that urgent?",
             "More urgent than it looks. Once tile is broken the underlayment beneath is exposed to UV "
             "and rain, and that is what eventually leaks &mdash; often weeks later. Covering the area "
             "protects the underlayment while you source replacement tile."),
            ("Why does a tile roof repair take so long in San Antonio?",
             "Profile matching. Tile designs change over the decades and older ones are frequently "
             "discontinued, so finding twenty matching tiles for a 1980s roof can take a while. That "
             "long wait is exactly when long-term tarping specification matters."),
        ],
    },

    # --------------------------------------------------------------- El Paso
    {
        "slug": "roof-tarp-el-paso",
        "city": "El Paso",
        "county": "El Paso County",
        "keyword": "roof tarp el paso",
        "title": "Roof Tarp El Paso TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in El Paso, TX. Monsoon and high-wind response for flat and "
            "low-slope desert roofs. Call (512) 297-7580."
        ),
        "blurb": "Desert monsoon, flat roofs and intense UV &mdash; a different problem entirely.",
        "hero_intro": (
            "El Paso is a genuinely different roofing environment from the rest of Texas. Flat and "
            "low-slope roofs dominate, annual rainfall is low but arrives in violent monsoon bursts, and "
            "the UV load is the harshest in the state. <strong>Roof tarping in El Paso</strong> has to "
            "account for all three."
        ),
        "storm_profile": """
<h2>Monsoon bursts and desert wind</h2>
<p>El Paso gets very little rain by Texas standards, and that is precisely what makes its storms
dangerous for roofs. The bulk of annual precipitation arrives between July and September during the
North American monsoon, in short, extremely intense bursts. A roof that has baked dry for ten months
takes a year's worth of water in a handful of storms.</p>
<p>The second hazard is wind. Spring brings sustained high winds and dust storms through the Chihuahuan
Desert, and those wind events regularly lift roofing material from low-slope roofs &mdash; where a
lifted edge has no gravity assistance to reseat it.</p>
<p>Third, and specific to this corner of Texas: UV. El Paso's elevation and clear-sky fraction give it
the most punishing ultraviolet exposure in the state. This matters directly for tarping, because a
standard poly tarp degrades here faster than anywhere else in Texas. Anything expected to stay on for
more than a few weeks needs UV-stabilised material as a matter of course.</p>
""",
        "local_detail": """
<h3>Flat roofs change the method</h3>
<p>Much of El Paso's housing and nearly all of its commercial stock is flat or low-slope &mdash; built
up, modified bitumen, single-ply membrane, or the traditional adobe-influenced parapet roof. None of
these shed water by gravity the way a pitched roof does, which means a tarp cannot simply be laid over
a hole and left to drain.</p>
<p>Covers here are laid to direct water toward existing drains and scuppers, ballasted rather than
fastened, and checked for ponding. A tarp that blocks a scupper on a parapet roof turns a contained
leak into a flooded roof deck, which is a considerably worse problem.</p>
<p>We cover the city broadly &mdash; the Westside, Northeast, Lower Valley, Mission Valley and the
Far East side out toward the county line.</p>
""",
        "faqs": [
            ("Do flat roofs need a different kind of tarp?",
             "A different method, yes. Water does not run off a flat roof by gravity, so the cover is "
             "laid to direct water toward existing drains and scuppers, ballasted rather than fastened, "
             "and checked for ponding. Blocking a scupper makes things much worse."),
            ("How long will a tarp last in El Paso sun?",
             "Less time than anywhere else in Texas. The UV load here is the harshest in the state and "
             "standard poly tarps go brittle quickly. Anything staying on more than a few weeks should "
             "be UV-stabilised heavy-duty material from the outset."),
            ("We barely get rain here. Is tarping really necessary?",
             "The low annual total is misleading &mdash; most of it arrives in a few violent monsoon "
             "bursts between July and September. An open roof that has been fine for months can take a "
             "great deal of water in a single afternoon."),
        ],
    },

    # --------------------------------------------------------------- Lubbock
    {
        "slug": "roof-tarp-lubbock",
        "city": "Lubbock",
        "county": "Lubbock County",
        "keyword": "emergency roof tarp lubbock",
        "title": "Roof Tarp Lubbock TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Lubbock, TX. High Plains wind and hail response, 24/7. "
            "Call (512) 297-7580."
        ),
        "blurb": "High Plains wind &mdash; the hardest place in Texas to keep a tarp on.",
        "hero_intro": (
            "Lubbock is the most demanding tarping environment in Texas, and it is the wind that does it. "
            "The South Plains are flat, open and effectively unobstructed, so wind arrives at full speed "
            "with nothing to slow it. A <strong>roof tarp in Lubbock</strong> that would hold fine in "
            "Houston will be gone by morning."
        ),
        "storm_profile": """
<h2>Wind with nothing in its way</h2>
<p>The Llano Estacado is one of the flattest large landforms in North America. There is no terrain, and
very little tree cover, to disrupt airflow &mdash; so wind speeds at roof level here are substantially
higher for the same synoptic setup than they would be in a metro with hills or canopy.</p>
<p>Sustained spring winds of 30&ndash;40mph are routine rather than exceptional, and gusts well beyond
that are common. Add the dust that those winds carry, and you get an abrasive loading environment that
works fastenings loose over time and sandblasts tarp material at its stress points.</p>
<p>Lubbock also sits in a genuinely active hail region. Supercells crossing the South Plains produce
very large stones, and because the terrain offers no shelter, wind and hail usually arrive together
rather than sequentially.</p>
""",
        "local_detail": """
<h3>Anchoring for the South Plains</h3>
<p>Everything about our method here is tightened relative to the rest of the state. Board-wrapped
anchoring is standard rather than optional, batten spacing is closer, and edges are secured along their
full length rather than at intervals. A tarp that flaps at all in Lubbock will not last &mdash; the
oscillation works fastenings loose and abrades the material at every anchor point.</p>
<p>We also re-tension here sooner. Wind cycling relaxes a cover faster on the South Plains than
anywhere else, and a tarp that was drum-taut on installation can be noticeably slack within a fortnight.
If a cover is staying on for more than a few weeks, plan on a check.</p>
<p>We cover Lubbock proper and the surrounding communities &mdash; Wolfforth, Shallowater, Idalou and
Slaton.</p>
""",
        "faqs": [
            ("My last roof tarp blew off in Lubbock. Why?",
             "Almost certainly the anchoring, not the material. Standard spacing that works elsewhere in "
             "Texas is not adequate on the South Plains &mdash; wind arrives unobstructed here. Closer "
             "batten spacing, full-length edge securing and no flapping anywhere is what holds."),
            ("How often should a tarp be checked in Lubbock?",
             "More often than elsewhere. Wind cycling relaxes a cover quickly here, so plan on a "
             "re-tension check within the first couple of weeks and after any significant wind event."),
            ("Do you cover the smaller towns around Lubbock?",
             "Yes &mdash; Wolfforth, Shallowater, Idalou, Slaton and the surrounding area. Give us your "
             "location when you call and we will tell you a realistic arrival time."),
        ],
    },

    # -------------------------------------------------------- Corpus Christi
    {
        "slug": "roof-tarp-corpus-christi",
        "city": "Corpus Christi",
        "county": "Nueces County",
        "keyword": "roof tarp corpus christi",
        "title": "Roof Tarp Corpus Christi TX | Hurricane Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Corpus Christi, TX. Direct hurricane landfall response and "
            "coastal roof protection. Call (512) 297-7580."
        ),
        "blurb": "Direct landfall territory, plus salt air that corrodes fastenings.",
        "hero_intro": (
            "Corpus Christi is landfall territory. Unlike Houston, which usually takes tropical systems "
            "after they have crossed land and weakened, the Coastal Bend regularly sees hurricanes come "
            "ashore at full strength. A <strong>roof tarp in Corpus Christi</strong> has to be specified "
            "for that, and for the salt air that attacks everything holding it down."
        ),
        "storm_profile": """
<h2>Landfall, not remnants</h2>
<p>Nueces County's exposure is direct. Systems crossing the Gulf make landfall here with their full
wind field intact, and the Coastal Bend has taken several significant hurricanes in living memory. The
damage profile is correspondingly severe: not stripped shingle patches but whole roof planes removed,
and structural damage frequent enough that a safety assessment before any tarp work is standard rather
than precautionary.</p>
<p>Storm surge adds a dimension the inland metros do not have. Properties near the bay and on the
barrier islands can take water from below and above in the same event, and a roof tarp is only part of
the response in that situation.</p>
<p>Between named storms, the persistent hazard is salt. Marine air corrodes fastenings, and a tarp
anchored with ordinary fixings that would last a year inland can have its anchor points failing within
months here.</p>
""",
        "local_detail": """
<h3>Coastal specification</h3>
<p>Two things change for the Coastal Bend. Fastenings are corrosion-resistant as standard, because
ordinary ones will not survive marine exposure long enough to matter. And anchoring is specified for
sustained rather than gusting loads &mdash; a landfalling system loads a roof for many hours, often with
the wind direction reversing as the centre passes, and a cover anchored only against one direction will
fail when the wind backs.</p>
<p>We cover Corpus Christi and the surrounding Coastal Bend &mdash; Flour Bluff, Calallen, Portland,
Aransas Pass, Rockport and the Padre Island communities. Island and bayfront access can be restricted
after a landfalling storm, which affects timing more than anything else.</p>
""",
        "faqs": [
            ("Do coastal roofs need different tarp fastenings?",
             "Yes. Salt air corrodes ordinary fixings quickly, so we use corrosion-resistant fastenings "
             "as standard here. An anchor point that would last a year inland can start failing within "
             "months in marine air."),
            ("Will you tarp on Padre Island or in Rockport?",
             "Yes, across the Coastal Bend. After a landfalling storm, access to the islands and "
             "bayfront is often restricted for a period, which usually affects timing more than "
             "anything else."),
            ("How is a hurricane tarp different from a normal one?",
             "It is anchored for sustained multi-hour loading with the wind direction reversing as the "
             "centre passes, rather than for a single gust from one direction. A cover secured against "
             "one direction only will fail when the wind backs."),
        ],
    },

    # ------------------------------------------------------------- Arlington
    {
        "slug": "roof-tarp-arlington",
        "city": "Arlington",
        "county": "Tarrant County",
        "keyword": "emergency roof tarp arlington",
        "title": "Roof Tarp Arlington TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Arlington, TX. Mid-cities hail and wind response, 24/7. "
            "Call (512) 297-7580."
        ),
        "blurb": "Mid-cities density &mdash; dense housing, whole streets hit at once.",
        "hero_intro": (
            "Arlington sits in the middle of the metroplex, between Dallas and Fort Worth, and its "
            "defining characteristic for tarping is density. When a hail core crosses a mid-cities "
            "subdivision it hits hundreds of closely-spaced, similarly-built homes simultaneously &mdash; "
            "so <strong>roof tarping in Arlington</strong> tends to be street-scale rather than one-off."
        ),
        "storm_profile": """
<h2>Dense housing, concentrated damage</h2>
<p>The mid-cities were built out fast, largely in the 1970s through 1990s, in tightly-spaced
subdivisions where houses on a given street share construction era, roof pitch and covering type. That
uniformity means a hail core crossing the area does not damage a scattering of roofs &mdash; it damages
essentially all of them, in the same way, at the same moment.</p>
<p>For a homeowner this has one immediate consequence worth knowing: every roofing contractor within
thirty miles will be booked within about 48 hours, and the storm-chasing operations will arrive by the
end of the week. The gap between damage and repair here is routinely measured in months after a
significant event.</p>
<p>Tarrant County's position also means Arlington catches storms that are still strong, with hail and
straight-line wind arriving together rather than one or the other.</p>
""",
        "local_detail": """
<h3>Street-scale response</h3>
<p>Because damage clusters so tightly, we schedule Arlington work by street rather than by individual
call where we can. If your neighbours also need covering, telling us that when you ring means one visit
instead of several and a considerably faster response for everyone on the block.</p>
<p>The housing stock here is predominantly asphalt shingle on moderate-pitch roofs &mdash; the most
straightforward covering to tarp securely, using board-wrapped anchoring. Two-storey homes are common
in the newer sections, which affects equipment and time but not method.</p>
<p>We cover Arlington along with the surrounding mid-cities &mdash; Grand Prairie, Mansfield, Euless,
Bedford and Hurst.</p>
""",
        "faqs": [
            ("Can you do several houses on my street at once?",
             "Yes, and in Arlington that is usually how it works. Mid-cities damage is highly "
             "concentrated, so tell us when you call if neighbours need covering too &mdash; one visit "
             "is faster for everybody."),
            ("Why is it so hard to get a roofer in the mid-cities after hail?",
             "Density. A hail core crosses hundreds of similarly-built homes at once, so every "
             "contractor in the area is booked within about 48 hours. That gap is exactly what tarping "
             "is for."),
            ("Do you cover Grand Prairie and Mansfield too?",
             "Yes &mdash; Arlington plus the surrounding mid-cities including Grand Prairie, Mansfield, "
             "Euless, Bedford and Hurst."),
        ],
    },

    # ------------------------------------------------------------------ Waco
    {
        "slug": "roof-tarp-waco",
        "city": "Waco",
        "county": "McLennan County",
        "keyword": "waco roof tarping",
        "title": "Roof Tarp Waco TX | Emergency Roof Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Waco, TX. I-35 corridor hail and wind response across "
            "McLennan County. Call (512) 297-7580."
        ),
        "blurb": "Mid-corridor between DFW and Austin &mdash; hail from both directions.",
        "hero_intro": (
            "Waco sits halfway between the two biggest storm generators in the state, and takes weather "
            "from both. Systems tracking down from North Texas and systems firing off the Central Texas "
            "escarpment both reach McLennan County, which is why <strong>roof tarping in Waco</strong> "
            "has a longer season than either metro either side of it."
        ),
        "storm_profile": """
<h2>Caught between two storm regimes</h2>
<p>McLennan County's position on I-35 puts it at the overlap of two distinct severe weather patterns.
North Texas dryline supercells track southeast through the county, and Central Texas storms enhanced by
the Balcones Escarpment move up from the south. The result is a longer active season than either DFW or
Austin experiences alone, with damaging hail possible across a wider window.</p>
<p>Waco also has a notable tornado history, and the local awareness of that is high. In practical terms
it means residents here tend to take wind damage seriously and call quickly, which is genuinely
helpful &mdash; the sooner a compromised roof is covered, the less it costs.</p>
<p>The county mixes urban Waco with substantial rural acreage, so calls range from city bungalows to
farm properties with metal outbuildings.</p>
""",
        "local_detail": """
<h3>Working across McLennan County</h3>
<p>We cover Waco proper &mdash; including the Baylor area, Castle Heights, Mountainview and the older
central neighbourhoods &mdash; plus Hewitt, Woodway, Robinson, Bellmead and the surrounding rural
county.</p>
<p>Central Waco carries a lot of older housing with steeper pitches and, in the historic districts,
some genuinely old roof structures where decking condition cannot be assumed. On those we check what we
are anchoring into before committing a fastener &mdash; driving a batten screw into decking that will
not hold it achieves nothing and makes the eventual repair worse.</p>
<p>Rural properties in the county bring metal roofing and outbuildings, which get ballasted rather than
penetrated as standard.</p>
""",
        "faqs": [
            ("Does Waco really get more hail days than Dallas or Austin?",
             "A longer season, effectively. McLennan County sits where North Texas and Central Texas "
             "storm patterns overlap, so damaging hail is possible across a wider window than in either "
             "metro on its own."),
            ("My house is in a historic Waco district. Does that change anything?",
             "It can. Older roof structures mean decking condition cannot be assumed, so we check what "
             "we are anchoring into before committing a fastener. Ballasted anchoring is often the "
             "better call on those roofs."),
            ("Do you cover rural McLennan County and outbuildings?",
             "Yes. Farm outbuildings are usually metal, which we ballast and clamp rather than "
             "penetrate. Give us the location and we will confirm timing."),
        ],
    },

    # --------------------------------------------------------------- McKinney
    {
        "slug": "roof-tarp-mckinney",
        "city": "McKinney",
        "county": "Collin County",
        "keyword": "roof tarp mckinney",
        "title": "Roof Tarp McKinney TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in McKinney, TX. Collin County hail response for newer "
            "suburban roofs. Call (512) 297-7580."
        ),
        "blurb": "Fast-growing Collin County &mdash; newer, steeper, more complex roofs.",
        "hero_intro": (
            "McKinney's housing stock is newer and more architecturally complex than the older "
            "metroplex suburbs, and that changes the job. <strong>Roof tarping in McKinney</strong> "
            "usually means a steep-pitch roof with multiple gables, dormers and valleys &mdash; more "
            "transitions to work around, and more places for a poorly-fitted cover to let water past."
        ),
        "storm_profile": """
<h2>Collin County hail on complex roofs</h2>
<p>Collin County takes the same North Texas hail as Dallas does, but the roofs it lands on are
different. McKinney's rapid growth since the 1990s means a housing stock dominated by large
two-storey homes with steep pitches, multiple intersecting gables, dormers and long valleys.</p>
<p>Complex geometry cuts both ways for storm damage. Steep pitches shed hail at a more glancing angle,
which reduces impact severity somewhat. But the same geometry concentrates water volume in valleys, so
when something does fail near a valley, the volume of water reaching the breach is far higher than on a
simple gable roof.</p>
<p>Most of this stock carries architectural shingle, some of it impact-rated, which performs better
than the three-tab on older Dallas housing &mdash; but at larger stone sizes it still fails.</p>
""",
        "local_detail": """
<h3>Complex roofs take longer to cover properly</h3>
<p>A tarp on a simple gable is one plane and four edges. A tarp on a McKinney roof with a dormer and a
valley running through the damage zone is several planes, more edges and a set of transitions that each
need detailing. It takes longer, and a crew that rushes it leaves a cover that channels water into the
valley rather than out of it.</p>
<p>Where damage crosses a valley, we generally cover both planes and run the overlap so the upper sheds
onto the lower rather than butting them at the valley line. Steep pitch also means fall protection and
often roof jacks, which adds setup time before any tarp goes down.</p>
<p>We cover McKinney along with the surrounding Collin County communities &mdash; Allen, Frisco, Prosper,
Melissa and Princeton.</p>
""",
        "faqs": [
            ("Why does my McKinney roof take longer to tarp than my old house did?",
             "Geometry. Newer Collin County homes have steep pitches, multiple gables, dormers and "
             "valleys, so a cover has to be detailed across several planes and transitions rather than "
             "laid on one. Steep pitch also means fall protection setup before work starts."),
            ("The damage is right next to a valley. Is that worse?",
             "Yes, because valleys concentrate water from two planes. A breach near one takes far more "
             "volume than the same hole in the middle of a slope, so it wants covering promptly and "
             "detailed carefully."),
            ("Does impact-rated shingle mean I will not get hail damage?",
             "It performs considerably better, but it is not immune. At larger stone sizes impact-rated "
             "architectural shingle still fails &mdash; it just takes a bigger stone to do it."),
        ],
    },

    # ------------------------------------------------------------- Sugar Land
    {
        "slug": "roof-tarp-sugar-land",
        "city": "Sugar Land",
        "county": "Fort Bend County",
        "keyword": "roof tarp sugar land",
        "title": "Roof Tarp Sugar Land TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Sugar Land, TX. Fort Bend County storm response with "
            "HOA-aware work. Call (512) 297-7580."
        ),
        "blurb": "Master-planned Fort Bend County &mdash; HOA rules and expansive clay soils.",
        "hero_intro": (
            "Sugar Land is master-planned almost end to end, and that shapes a tarping job in ways the "
            "rest of the Houston metro does not. Deed restrictions and HOA rules govern what can be "
            "visible from the street and for how long, so <strong>roof tarping in Sugar Land</strong> "
            "usually involves a conversation about tidiness as well as watertightness."
        ),
        "storm_profile": """
<h2>Fort Bend County exposure</h2>
<p>Sugar Land takes the same tropical systems as the rest of the Houston metro, arriving slightly
weakened after crossing land but still carrying hours of sustained wind and wind-driven rain. The
county's flat terrain and Brazos River floodplain mean that water, once it is down, stays down.</p>
<p>The soils are the locally distinctive factor. Fort Bend County sits on highly expansive clay that
swells and shrinks dramatically with moisture. That movement works through the structure over time and
shows up at the roof as separated flashing, opened ridge lines and cracked mortar at chimneys &mdash;
all of which become water entry points during a storm, without any storm damage having occurred in the
conventional sense.</p>
<p>A roof here can leak badly in a system that did it no direct damage at all, simply because foundation
movement had already opened the paths.</p>
""",
        "local_detail": """
<h3>Working within HOA rules</h3>
<p>Most Sugar Land neighbourhoods carry deed restrictions that cover visible temporary structures, and
some set time limits on how long a tarp can remain. This is worth knowing early rather than discovering
by letter. Practically, we keep covers neat and trimmed rather than leaving loose material flapping,
choose the least conspicuous colour available where the specification allows a choice, and provide dated
documentation you can give the HOA to evidence that a repair is in progress.</p>
<p>If the repair is going to run long enough that the HOA will object, that is an argument for getting
the permanent repair scheduled rather than for a flimsier cover &mdash; and we will say so.</p>
<p>We cover Sugar Land, Missouri City, Richmond, Rosenberg and the surrounding Fort Bend communities.</p>
""",
        "faqs": [
            ("Will my HOA let me put a tarp on the roof?",
             "Almost always yes for emergency mitigation, but many Sugar Land deed restrictions set "
             "limits on how long it can stay visible. Tell your HOA what has happened and keep the dated "
             "documentation &mdash; it evidences that a repair is in progress."),
            ("My roof leaks but there was no storm damage. How?",
             "Very common in Fort Bend County. Expansive clay soils move the structure, which separates "
             "flashing and opens ridge lines and chimney mortar. The paths are already there; a heavy "
             "rain simply finds them."),
            ("Can you make the tarp less visible from the street?",
             "We keep covers trimmed and neat rather than leaving loose material, and where the "
             "specification allows a colour choice we will use the least conspicuous one. Watertightness "
             "comes first, but appearance is worth what it can be given."),
        ],
    },

    # ---------------------------------------------------------------- Midland
    {
        "slug": "roof-tarp-midland",
        "city": "Midland",
        "county": "Midland County",
        "keyword": "roof tarp midland",
        "title": "Roof Tarp Midland TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Midland, TX. Permian Basin wind, hail and dust storm "
            "response. Call (512) 297-7580."
        ),
        "blurb": "Permian Basin &mdash; wind, blowing dust and a long haul between towns.",
        "hero_intro": (
            "Midland sits in the middle of the Permian Basin, where the nearest comparable metro is a "
            "long drive in any direction. That isolation is the practical constraint on <strong>roof "
            "tarping in Midland</strong>: local roofing capacity is limited relative to demand, so after "
            "a significant storm the wait for a repair is longer here than in the big metros."
        ),
        "storm_profile": """
<h2>Wind, dust and distance</h2>
<p>West Texas wind is relentless. Like the South Plains, the Permian Basin is flat and open, so wind
arrives at roof level with little to slow it, and spring brings sustained high winds along with the
blowing dust those winds carry. Dust is genuinely abrasive: it works into fastenings, accumulates in
tarp folds and wears at material where it moves against a roof surface.</p>
<p>The region also takes severe hail. Supercells crossing the Basin produce large stones, and with no
terrain to break them up, hail and wind typically arrive together.</p>
<p>The structural issue here is distance. Midland and Odessa share a limited pool of roofing
contractors serving a wide area. After a damaging event, the backlog is proportionally worse than in
DFW or Houston simply because there are fewer crews and further to drive between jobs. That directly
raises the value of a cover specified to last rather than a short-term one.</p>
""",
        "local_detail": """
<h3>Specify for the wait</h3>
<p>Because repair timelines here run long, we lean toward heavier specification in the Permian Basin
than we would in a metro with dense contractor coverage. If the realistic repair date is two or three
months out, a standard emergency tarp will not survive that in West Texas wind and sun, and installing
one is setting up a second failure and a second call-out.</p>
<p>Dust makes re-tensioning checks more important too, because grit working into anchor points
accelerates loosening.</p>
<p>We cover Midland and Odessa along with the surrounding Basin communities &mdash; Greenwood, Gardendale
and Stanton.</p>
""",
        "faqs": [
            ("Why is the wait for a roof repair so long in Midland?",
             "Contractor density. The Permian Basin has a limited pool of roofing crews covering a wide "
             "area, so a damaging storm produces a proportionally worse backlog than in DFW or Houston. "
             "That is why we specify covers here to last."),
            ("Does blowing dust actually damage a tarp?",
             "Yes. Grit works into fastenings and accelerates loosening, collects in folds, and abrades "
             "material wherever it moves against the roof. It is a real factor in how long a West Texas "
             "cover lasts."),
            ("Do you cover Odessa as well as Midland?",
             "Yes, along with Greenwood, Gardendale, Stanton and the surrounding Basin communities."),
        ],
    },

    # --------------------------------------------------------------- Beaumont
    {
        "slug": "roof-tarp-beaumont",
        "city": "Beaumont",
        "county": "Jefferson County",
        "keyword": "roof tarp beaumont",
        "title": "Roof Tarp Beaumont TX | Hurricane Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Beaumont, TX. Extreme rainfall and hurricane response "
            "across Jefferson County. Call (512) 297-7580."
        ),
        "blurb": "The wettest corner of Texas &mdash; extreme rainfall totals.",
        "hero_intro": (
            "Southeast Texas takes more rain than anywhere else in the state, and Beaumont has recorded "
            "some of the highest storm rainfall totals in United States history. For <strong>roof "
            "tarping in Beaumont</strong>, the governing number is not wind speed &mdash; it is how many "
            "inches per hour a cover has to shed."
        ),
        "storm_profile": """
<h2>Rainfall is the dominant hazard</h2>
<p>Jefferson County sits in the wettest part of Texas, where Gulf moisture converges with stalling
tropical systems. The region has seen rainfall events that rank among the most extreme ever recorded in
the country, with totals measured in feet rather than inches over a few days.</p>
<p>That changes what a tarp has to do. In most of Texas, a cover's job is to stop the water from a
normal storm. Here it may need to shed several inches an hour for a sustained period, which puts real
hydraulic load on the material and, more importantly, on the edges. Any edge that would leak slightly
in an ordinary storm will leak badly in a Beaumont rainfall event.</p>
<p>Because tropical systems here often stall rather than passing through, the loading is prolonged.
A cover that would be perfectly adequate for a two-hour storm is being asked to perform for two days.</p>
""",
        "local_detail": """
<h3>Edges and volume</h3>
<p>Everything in a Beaumont installation comes back to edge detailing and water volume. Upslope edges
are tucked under the course above wherever that is achievable, so the water sheds over the cover rather
than finding a way behind it. Overlaps are shingled with generous laps rather than minimal ones. The
downslope edge is run well past the eave so discharge clears the fascia rather than running back along
it.</p>
<p>We also pay closer attention to where the shed water actually goes. A tarp that dumps several inches
an hour onto one section of gutter will overflow it, and that water then runs down the wall and into the
soffit &mdash; solving the roof leak while creating a different one.</p>
<p>We cover Beaumont, Port Arthur, Orange, Nederland and the surrounding Jefferson and Orange County
communities.</p>
""",
        "faqs": [
            ("Does heavy rain make a tarp leak even if it is installed correctly?",
             "Extreme rainfall tests edges far harder than normal rain does. Any edge that would seep "
             "slightly in an ordinary storm will leak properly in a Beaumont event, which is why edge "
             "detailing gets more attention here than anywhere else in Texas."),
            ("Where does all the water off the tarp go?",
             "That is a real design question here. A cover shedding several inches an hour will overflow "
             "a gutter, and that water then runs down the wall into the soffit. We plan discharge so it "
             "clears the fascia rather than creating a second problem."),
            ("Do you cover Port Arthur and Orange?",
             "Yes &mdash; Beaumont, Port Arthur, Orange, Nederland and the surrounding Jefferson and "
             "Orange County communities."),
        ],
    },

    # ---------------------------------------------------------- The Woodlands
    {
        "slug": "roof-tarp-the-woodlands",
        "city": "The Woodlands",
        "county": "Montgomery County",
        "keyword": "roof tarping the woodlands tx",
        "title": "Roof Tarp The Woodlands TX | Tree Damage Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in The Woodlands, TX. Falling pine and tree strike response "
            "across Montgomery County. Call (512) 297-7580."
        ),
        "blurb": "Dense pine canopy &mdash; tree strikes rather than wind stripping.",
        "hero_intro": (
            "The Woodlands was deliberately built into the forest, and its tree canopy is the reason "
            "people live there and the reason their roofs fail. <strong>Roof tarping in The "
            "Woodlands</strong> is overwhelmingly a tree damage business: loblolly pines coming down or "
            "dropping limbs through decking, rather than wind peeling shingles."
        ),
        "storm_profile": """
<h2>Pines are the hazard</h2>
<p>Montgomery County's loblolly pines grow tall, straight and shallow-rooted, in sandy soil that loses
its grip when saturated. The failure mode is specific and it is not gradual: heavy rain softens the
ground, wind pushes on a full canopy eighty feet up, and the tree either uproots entirely or snaps.
Either way, a substantial mass arrives on a roof at speed.</p>
<p>This produces a completely different damage pattern from the wind-stripping that dominates the open
metros. Instead of a peeled shingle field, you get concentrated point damage: a punched hole through
decking, often with structural members broken beneath, and frequently with the limb or trunk still in
place.</p>
<p>The canopy also means damage is often not visible from the ground at all &mdash; the tree is resting
on the roof under cover of branches, and the extent of the breach underneath is unknown until someone
gets up there.</p>
""",
        "local_detail": """
<h3>Debris removal comes first</h3>
<p>Nothing can be covered while a tree is sitting on it, and how that mass is removed matters enormously.
Dragging a trunk off a roof will widen the opening substantially and can pull broken decking with it.
The removal has to be planned so load comes off the structure in a controlled way, and on significant
strikes that means cutting the mass down in sections rather than moving it whole.</p>
<p>Structural assessment is also more relevant here than in most metros. A pine through the decking
frequently breaks rafters or trusses, and a roof with broken structural members is not safe to walk. In
those cases we anchor from the perimeter and, where the structure is genuinely unsound, say plainly that
the cover has to wait for the structure to be made safe.</p>
<p>We cover The Woodlands, Conroe, Spring, Magnolia and the surrounding Montgomery County communities.</p>
""",
        "faqs": [
            ("There is still a tree on my roof. Can you tarp it?",
             "Not until the tree is off. How it comes off matters a great deal &mdash; dragging a trunk "
             "will widen the opening and pull broken decking with it. Significant strikes get cut down "
             "in sections so load comes off the structure in a controlled way."),
            ("Why do pines fall when other trees do not?",
             "Loblolly pines are tall, shallow-rooted and carry a full canopy high up. Saturated sandy "
             "soil loses grip, wind loads the canopy, and the tree either uproots or snaps. It is a "
             "specific Montgomery County failure mode."),
            ("The branches are hiding the damage. How do you know how big it is?",
             "We do not, until someone gets up there safely and looks. That is normal here &mdash; "
             "canopy hides the breach. Assume the opening is larger than what is visible from the "
             "ground, because it usually is."),
        ],
    },

    # ------------------------------------------------------------- Huntsville
    {
        "slug": "roof-tarp-huntsville",
        "city": "Huntsville",
        "county": "Walker County",
        "keyword": "roof tarping huntsville tx",
        "title": "Roof Tarp Huntsville TX | Emergency Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Huntsville, TX. Piney Woods tree damage response across "
            "Walker County. Call (512) 297-7580."
        ),
        "blurb": "Piney Woods and rural acreage &mdash; long drives, big trees.",
        "hero_intro": (
            "Huntsville sits in the Piney Woods with a mix of town housing, university rental stock and "
            "substantial rural acreage. <strong>Roof tarping in Huntsville</strong> combines the tree "
            "damage profile of the East Texas forest with the access and distance challenges of a rural "
            "county."
        ),
        "storm_profile": """
<h2>Forest damage on rural properties</h2>
<p>Walker County is heavily wooded, and like the rest of the Piney Woods its dominant roof hazard is
falling timber rather than wind stripping. Pines and hardwoods both come down in saturated-soil wind
events, and on rural acreage a tree can be down across a roof for some time before anyone notices,
particularly on a property that is not permanently occupied.</p>
<p>The rural character adds a second factor: a meaningful share of the building stock is
manufactured housing, barns and outbuildings with metal roofing. Metal changes the anchoring method
entirely &mdash; no penetrations, clamps and ballast &mdash; and manufactured housing roofs have their
own structural limits on what can be walked or loaded.</p>
<p>Huntsville's student rental stock brings a different problem again: absentee landlords, tenants who
may not know who to call, and roofs where a small breach goes unreported until it has done real
damage.</p>
""",
        "local_detail": """
<h3>Distance and access</h3>
<p>Walker County properties can sit a long way down unpaved private drives, and after a storm those
drives are frequently blocked by the same trees that hit the roof. When you call, tell us about access
&mdash; whether the drive is clear, whether a full-size vehicle can reach the house, and whether there
is anything down across the route. It changes what we bring and when we can realistically arrive.</p>
<p>For metal-roofed outbuildings and manufactured homes, covers are ballasted and clamped rather than
fastened. On manufactured housing in particular we are careful about what load goes where, because the
roof structure is considerably lighter than conventional framing.</p>
<p>We cover Huntsville, New Waverly, Riverside and the surrounding Walker County area.</p>
""",
        "faqs": [
            ("My property is down a long private drive. Is that a problem?",
             "Only if we do not know in advance. Tell us when you call whether the drive is clear and "
             "whether a full-size vehicle can reach the house &mdash; after a storm those drives are "
             "often blocked by the same trees that hit the roof."),
            ("Can you tarp a mobile or manufactured home roof?",
             "Yes, with care about loading. Manufactured housing roof structure is considerably lighter "
             "than conventional framing, so ballast placement and where a crew walks both matter more "
             "than they would on a stick-built house."),
            ("I rent in Huntsville and the roof is leaking. Who calls you?",
             "Normally the owner or property manager authorises the work, since it is their structure. "
             "If you cannot reach them and water is actively coming in, call us anyway and we will talk "
             "you through containment in the meantime."),
        ],
    },

    # ------------------------------------------------------------------ Hutto
    {
        "slug": "roof-tarp-hutto",
        "city": "Hutto",
        "county": "Williamson County",
        "keyword": "roof tarp hutto",
        "title": "Roof Tarp Hutto TX | Emergency Roof Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service in Hutto, TX. Williamson County hail and wind response in "
            "78634. Call (512) 297-7580."
        ),
        "blurb": "Blackland Prairie, rapid growth and narrow Williamson County hail swaths.",
        "hero_intro": (
            "Hutto is our operating base, which in practice means the fastest response times we offer "
            "anywhere in Texas. <strong>Roof tarping in Hutto</strong> and across Williamson County is "
            "mostly spring hail and straight-line wind on a housing stock that has grown enormously in a "
            "short space of time."
        ),
        "storm_profile": """
<h2>Williamson County hail</h2>
<p>Hutto sits on the Blackland Prairie just east of the I-35 corridor, in the band where Central Texas
spring storms mature. The hail swaths here are characteristically narrow &mdash; one Hutto subdivision
can be hit hard while the next is missed entirely &mdash; which makes per-property assessment more
useful than neighbourhood-level assumptions.</p>
<p>Straight-line wind is the other regular cause. The prairie is open, and newer subdivisions with
young landscaping offer very little wind break, so the estates on the edge of town take wind loading
that older, more sheltered parts of the county do not.</p>
<p>The county's growth is itself a factor. Large volumes of housing built quickly in the same window
means whole subdivisions share a roof age and covering type, so when a hail core crosses one, the damage
is uniform across hundreds of homes at once.</p>
""",
        "local_detail": """
<h3>Local response</h3>
<p>Being based here means we can usually be on a Hutto roof faster than anywhere else we serve, and we
know the subdivisions &mdash; Star Ranch, Emory Farms, Creek Bend, Cottonwood Creek, Riverwalk and the
Legends of Hutto &mdash; well enough to find a property without directions at two in the morning.</p>
<p>We cover Hutto and 78634 along with the surrounding Williamson County communities: Round Rock,
Pflugerville, Taylor, Georgetown and Manor. The newer subdivisions are predominantly architectural
asphalt shingle on moderate to steep pitches, which is straightforward to anchor properly using
board-wrapped battens.</p>
""",
        "faqs": [
            ("How quickly can you get to a Hutto address?",
             "Faster than anywhere else we cover &mdash; Hutto is our base. Actual timing still depends "
             "on how many calls a storm has generated and whether conditions are safe to work in."),
            ("My neighbour's roof looks fine but mine is damaged. Is that normal?",
             "Completely normal in Williamson County. Hail swaths here are narrow enough that one "
             "subdivision gets hit while the next is missed. Judge your own roof rather than the street."),
            ("Do you cover Round Rock, Georgetown and Taylor?",
             "Yes &mdash; Hutto plus Round Rock, Pflugerville, Taylor, Georgetown and Manor across "
             "Williamson County."),
        ],
    },
]

AREAS_BY_SLUG = {a["slug"]: a for a in AREAS}
