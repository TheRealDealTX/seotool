"""Service-area pages for the towns around Hutto.

Each page is short, targets one "roofing <city> tx" keyword, carries genuinely
local detail (neighborhoods, drive time from Hutto, the weather pattern that
particular town sees) and links back to the Hutto homepage and services so the
area pages support the primary market rather than competing with it.
"""

from siteconfig import BIZ

PHONE = BIZ["phone_display"]

AREAS = [
    {
        "slug": "roofing-round-rock-tx",
        "city": "Round Rock",
        "keyword": "roofing round rock tx",
        "title": "Roofing Round Rock TX | Repair & Replacement | Hutto Roofers",
        "description": (
            "Roofing in Round Rock, TX from Hutto Roofers. Roof repair, replacement, hail and "
            "storm damage, inspections. Based 12 miles east in Hutto. Call (512) 297-7580."
        ),
        "h1": "Roofing in <span class=\"gold-text\">Round Rock, TX</span>",
        "h1_plain": "Roofing in Round Rock, TX",
        "eyebrow": "Round Rock Service Area",
        "drive": "about 15 minutes west of Hutto on US-79",
        "distance": "12 miles",
        "population": "~125,000",
        "county": "Williamson County",
        "hero_alt": "Residential roof in Round Rock, Texas",
        "body": """
<h2>Roofing in Round Rock, TX from a Hutto-based crew</h2>
<p><strong>Roofing</strong> work in <strong>Round Rock, TX</strong> is a straight run west for us &mdash;
US-79 connects Hutto to Round Rock directly, and we are on site in roughly fifteen minutes. That
proximity matters most on the calls where it matters most: an active leak, a storm-damaged roof
that needs covering, or a second opinion you would rather not wait three days for.</p>

<h2>What Round Rock roofs deal with</h2>
<p>Round Rock's housing stock spans a much wider range of build years than Hutto's does, and the
roofing picture changes noticeably across it. The established neighbourhoods around
<strong>Old Town Round Rock</strong> and off Chisholm Trail carry homes from the 1970s and 80s &mdash;
mature tree canopy, simpler roof geometry, and roofs that are frequently on their third covering.
Layered roofs and decades of accumulated repair work are common there, and a tear-off often
reveals more history than anyone expected.</p>
<p>The large planned communities &mdash; <strong>Teravista</strong>, <strong>Forest Creek</strong>,
<strong>Behrens Ranch</strong>, <strong>Paloma Lake</strong>, <strong>Stone Oak</strong> &mdash; are a different
proposition. Complex rooflines with multiple valleys, dormers and steep pitches, built in
concentrated waves, and now hitting the age where builder-grade shingle packages need replacing on
whole streets at once. Valleys are where those roofs concentrate their water and where the failures
start.</p>
<p>Round Rock also sits right on the I-35 corridor, which puts it in the path of essentially every
severe line that crosses Central Texas. The hail that reaches Hutto has usually passed over Round
Rock first &mdash; and because storms track from southwest to northeast, Round Rock frequently takes
the stronger part of a cell while Hutto gets the trailing edge. The
<a href="/services/hail-damage-roof-repair-hutto-tx/">hail assessment</a> we do in Hutto is the same
work, on roofs that see more of it.</p>
<p>One further wrinkle: Round Rock has more genuinely mature tree cover than Hutto, particularly
along Brushy Creek and in the older neighbourhoods. That means more shade &mdash; which helps shingles
last &mdash; but also more limb strikes, more leaf accumulation in valleys, and more moss and debris
holding moisture against the roof surface.</p>

<h2>Services available in Round Rock</h2>
<p>Everything we do in Hutto: <a href="/services/roof-repair-hutto-tx/">roof repair</a>,
<a href="/services/roof-replacement-hutto-tx/">roof replacement</a>,
<a href="/services/roof-installation-hutto-tx/">new roof installation</a>,
<a href="/services/hail-damage-roof-repair-hutto-tx/">hail damage repair</a>,
<a href="/services/storm-damage-roof-repair-hutto-tx/">storm damage repair</a>,
<a href="/services/shingle-roofing-hutto-tx/">shingle roofing</a>,
<a href="/services/metal-roofing-hutto-tx/">metal roofing</a>,
<a href="/services/roof-inspection-hutto-tx/">roof inspections</a>,
<a href="/services/commercial-roofing-hutto-tx/">commercial roofing</a> and
<a href="/services/emergency-roof-repair-hutto-tx/">emergency roof repair</a>.</p>
""",
    },
    {
        "slug": "roofing-pflugerville-tx",
        "city": "Pflugerville",
        "keyword": "roofing pflugerville tx",
        "title": "Roofing Pflugerville TX | Roof Repair | Hutto Roofers",
        "description": (
            "Roofing in Pflugerville, TX from Hutto Roofers. Roof repair, replacement, hail and "
            "storm damage, inspections. 14 miles from our Hutto base. Call (512) 297-7580."
        ),
        "h1": "Roofing in <span class=\"gold-text\">Pflugerville, TX</span>",
        "h1_plain": "Roofing in Pflugerville, TX",
        "eyebrow": "Pflugerville Service Area",
        "drive": "about 20 minutes southwest of Hutto via SH-130 or FM 685",
        "distance": "14 miles",
        "population": "~70,000",
        "county": "Travis County",
        "hero_alt": "Residential roof in Pflugerville, Texas",
        "body": """
<h2>Roofing in Pflugerville, TX</h2>
<p>Pflugerville is a twenty-minute run southwest from Hutto, either down SH-130 or across on FM 685.
It is the neighbour we are called to most often after a storm, largely because the same weather
system that crosses Hutto tends to catch Pflugerville within the same hour &mdash; and
<strong>roofing</strong> demand in <strong>Pflugerville, TX</strong> spikes on exactly the days ours does.</p>

<h2>What is different about Pflugerville roofs</h2>
<p>Pflugerville sits in <strong>Travis County</strong> rather than Williamson, which is a practical
distinction rather than a trivial one &mdash; permitting and inspection go through a different
jurisdiction, and the City of Pflugerville has its own requirements for re-roofing work. We handle
that as part of the job, but it is worth knowing why timelines can differ slightly from a Hutto
project.</p>
<p>The housing stock skews newer than Round Rock's and broadly comparable to Hutto's, with the bulk
of it built from the late 1990s onward. <strong>Falcon Pointe</strong>, <strong>Blackhawk</strong>,
<strong>Highland Park</strong>, <strong>Avalon</strong>, <strong>Springbrook</strong> and the
<strong>Sorento</strong> and <strong>Carmel</strong> developments make up most of what we see. Like Hutto's
subdivisions, these went up in tight construction windows with consistent builder shingle
specifications, so replacement demand arrives in clusters rather than spread evenly.</p>
<p>The local weather detail that matters here is <strong>Lake Pflugerville</strong> and the flat,
open terrain around it on the eastern side of town. Those subdivisions have very little wind break,
and storms crossing from the southwest hit them with the full force they carried across open
ground. The pattern is much like Hutto's northern edge: the first row of houses on the windward
side of a development takes a disproportionate share of the wind damage.</p>
<p>Pflugerville's newer neighbourhoods also share Hutto's shade problem. Limited mature canopy means
roofs take unbroken summer sun, which shortens asphalt shingle life relative to the older,
tree-covered parts of the metro. Attic ventilation is worth checking on any Pflugerville roof
approaching the fifteen-year mark.</p>

<h2>Services available in Pflugerville</h2>
<p>The full range: <a href="/services/roof-repair-hutto-tx/">roof repair</a>,
<a href="/services/roof-replacement-hutto-tx/">replacement</a>,
<a href="/services/hail-damage-roof-repair-hutto-tx/">hail damage repair</a>,
<a href="/services/storm-damage-roof-repair-hutto-tx/">storm damage repair</a>,
<a href="/services/roof-inspection-hutto-tx/">inspections</a>,
<a href="/services/metal-roofing-hutto-tx/">metal roofing</a>,
<a href="/services/commercial-roofing-hutto-tx/">commercial roofing</a> and
<a href="/services/emergency-roof-repair-hutto-tx/">emergency response</a>.</p>
""",
    },
    {
        "slug": "roofing-taylor-tx",
        "city": "Taylor",
        "keyword": "roofing taylor tx",
        "title": "Roofing Taylor TX | Repair & Replacement | Hutto Roofers",
        "description": (
            "Roofing in Taylor, TX from Hutto Roofers. Roof repair, replacement, metal roofing, "
            "hail damage and inspections. 10 miles from Hutto. Call (512) 297-7580."
        ),
        "h1": "Roofing in <span class=\"gold-text\">Taylor, TX</span>",
        "h1_plain": "Roofing in Taylor, TX",
        "eyebrow": "Taylor Service Area",
        "drive": "about 12 minutes east of Hutto on US-79",
        "distance": "10 miles",
        "population": "~17,000",
        "county": "Williamson County",
        "hero_alt": "Residential roof in Taylor, Texas",
        "body": """
<h2>Roofing in Taylor, TX</h2>
<p>Taylor is our closest neighbour &mdash; ten miles straight east on US-79, twelve minutes door to
door. <strong>Roofing</strong> in <strong>Taylor, TX</strong> is effectively an extension of our home
market, and we are there regularly enough that a same-week appointment is usually straightforward.</p>

<h2>Taylor's roofs are a genuinely different job</h2>
<p>Of all the towns around Hutto, Taylor has the most distinctive building stock, and it changes
what a roofing visit involves.</p>
<p><strong>Downtown Taylor</strong> is a historic district. The brick commercial buildings along Main
Street date to the late 1800s and early 1900s, and they carry low-slope roofs that have been
patched, coated and re-covered across more than a century. Working on those is as much archaeology
as roofing &mdash; you frequently do not know what is under the current surface until it comes off.
Several also fall under historic-district considerations that affect what can be done to a visible
roofline. Our <a href="/services/commercial-roofing-hutto-tx/">commercial roofing</a> approach
applies directly here.</p>
<p>The <strong>residential core</strong> around downtown is similarly old &mdash; craftsman and
early-twentieth-century homes with steep pitches, complex hip and gable arrangements, original
board decking rather than plywood sheathing, and tree canopy that has had a hundred years to grow
over them. Steep pitch plus plank decking plus mature limbs overhead is a combination you simply do
not encounter in Hutto's newer subdivisions.</p>
<p>Out past the town limits, Taylor is <strong>farm and ranch country</strong>, and that is where the
<a href="/services/metal-roofing-hutto-tx/">metal roofing</a> work is. Barns, equipment sheds,
workshops and outbuildings across the Blackland Prairie run on exposed-fastener panel roofs, where
the recurring job is fastener and washer service rather than replacement.</p>
<p>Taylor is also changing fast. The large semiconductor development on the northeast side has
brought new residential construction, and those new subdivisions have the same profile as Hutto's
&mdash; open exposure, no canopy, builder-grade shingles going on in concentrated waves. In ten years
Taylor will have both housing stocks at once.</p>
<p>Weather-wise, Taylor sits slightly east of Hutto on the same storm track. Cells moving northeast
across Williamson County generally reach Hutto first and Taylor a few minutes later, usually with
comparable hail and wind intensity.</p>

<h2>Services available in Taylor</h2>
<p><a href="/services/roof-repair-hutto-tx/">Roof repair</a>,
<a href="/services/roof-replacement-hutto-tx/">replacement</a>,
<a href="/services/roof-installation-hutto-tx/">installation</a>,
<a href="/services/metal-roofing-hutto-tx/">metal roofing</a>,
<a href="/services/shingle-roofing-hutto-tx/">shingle roofing</a>,
<a href="/services/hail-damage-roof-repair-hutto-tx/">hail damage repair</a>,
<a href="/services/roof-inspection-hutto-tx/">inspections</a>,
<a href="/services/commercial-roofing-hutto-tx/">commercial roofing</a> and
<a href="/services/emergency-roof-repair-hutto-tx/">emergency roof repair</a>.</p>
""",
    },
    {
        "slug": "roofing-georgetown-tx",
        "city": "Georgetown",
        "keyword": "roofing georgetown tx",
        "title": "Roofing Georgetown TX | Repair & Replacement | Hutto Roofers",
        "description": (
            "Roofing in Georgetown, TX from Hutto Roofers. Roof repair, replacement, hail damage "
            "and inspections across Williamson County. Call (512) 297-7580."
        ),
        "h1": "Roofing in <span class=\"gold-text\">Georgetown, TX</span>",
        "h1_plain": "Roofing in Georgetown, TX",
        "eyebrow": "Georgetown Service Area",
        "drive": "about 25 minutes northwest of Hutto via SH-130 or CR 110",
        "distance": "17 miles",
        "population": "~100,000",
        "county": "Williamson County",
        "hero_alt": "Residential roof in Georgetown, Texas",
        "body": """
<h2>Roofing in Georgetown, TX</h2>
<p>Georgetown is the {county} seat and about twenty-five minutes northwest of us. <strong>Roofing</strong>
in <strong>Georgetown, TX</strong> covers a wider spread of property types than anywhere else we work
&mdash; nineteenth-century limestone homes near the square, enormous active-adult developments on the
west side, and hill-country acreage out past Lake Georgetown.</p>

<h2>Three Georgetowns, three roofing problems</h2>
<p><strong>The historic core.</strong> The Victorian and limestone homes around the courthouse square
and in the Old Town district are the oldest residential roofs in Williamson County. Steep pitches,
elaborate rooflines, original plank decking, and in many cases historic-district review of anything
that changes the roof's appearance. Material choice is constrained, and the work is slower and more
careful than a standard re-roof.</p>
<p><strong>Sun City and the west-side developments.</strong> Sun City Texas alone accounts for
thousands of homes, built in phases from the mid-1990s through the 2010s. That phasing is the
roofing story: entire sections reach replacement age together, and the earliest phases are well
past twenty years on their original coverings. These are largely single-storey homes with
straightforward roof geometry, which makes them efficient to work on &mdash; but they sit high and
exposed on the west side with limited canopy.</p>
<p><strong>The hill country edge.</strong> West and north toward Lake Georgetown the terrain changes
from Blackland Prairie to rockier hill country, with larger lots, custom homes, heavier tree cover
and more <a href="/services/metal-roofing-hutto-tx/">metal roofing</a>. Fire resistance is a real
consideration on those properties during a dry summer, which is part of why metal is common.</p>

<h2>Georgetown's hail exposure</h2>
<p>Georgetown sits on the I-35 corridor at the northern end of the Austin metro, and it has a
well-earned reputation for catching hail. Storms firing along the dryline to the west frequently
mature right as they reach the Georgetown area, which means the city often takes a cell at its
strongest &mdash; before that same system tracks southeast and reaches Hutto somewhat weaker.</p>
<p>The practical consequence for Georgetown homeowners is that
<a href="/services/hail-damage-roof-repair-hutto-tx/">hail damage assessment</a> and
<a href="/services/roof-inspection-hutto-tx/">post-storm inspections</a> come up more often here than
almost anywhere else in the county, and impact-resistant shingles are worth pricing on any
Georgetown re-roof.</p>

<h2>Services available in Georgetown</h2>
<p><a href="/services/roof-repair-hutto-tx/">Roof repair</a>,
<a href="/services/roof-replacement-hutto-tx/">replacement</a>,
<a href="/services/hail-damage-roof-repair-hutto-tx/">hail damage repair</a>,
<a href="/services/storm-damage-roof-repair-hutto-tx/">storm damage repair</a>,
<a href="/services/shingle-roofing-hutto-tx/">shingle roofing</a>,
<a href="/services/metal-roofing-hutto-tx/">metal roofing</a>,
<a href="/services/roof-inspection-hutto-tx/">inspections</a>,
<a href="/services/commercial-roofing-hutto-tx/">commercial roofing</a> and
<a href="/services/emergency-roof-repair-hutto-tx/">emergency roof repair</a>.</p>
""",
    },
    {
        "slug": "roofing-manor-tx",
        "city": "Manor",
        "keyword": "roofing manor tx",
        "title": "Roofing Manor TX | Repair & Replacement | Hutto Roofers",
        "description": (
            "Roofing in Manor, TX from Hutto Roofers. Roof repair, replacement, hail and storm "
            "damage, inspections. 16 miles from our Hutto base. Call (512) 297-7580."
        ),
        "h1": "Roofing in <span class=\"gold-text\">Manor, TX</span>",
        "h1_plain": "Roofing in Manor, TX",
        "eyebrow": "Manor Service Area",
        "drive": "about 22 minutes south of Hutto via SH-130",
        "distance": "16 miles",
        "population": "~20,000",
        "county": "Travis County",
        "hero_alt": "Residential roof in Manor, Texas",
        "body": """
<h2>Roofing in Manor, TX</h2>
<p>Manor is a straight run south from Hutto on SH-130, roughly twenty-two minutes. Of everywhere we
work, Manor is the town that most resembles Hutto &mdash; a small agricultural community on the
Blackland Prairie that has grown very fast in a short time &mdash; and <strong>roofing</strong> in
<strong>Manor, TX</strong> presents almost exactly the same set of problems we see at home.</p>

<h2>Why Manor roofs behave like Hutto roofs</h2>
<p>The parallel is close enough to be useful. Manor's population has more than quadrupled since
2010, and that growth arrived as large planned subdivisions dropped onto former farmland:
<strong>ShadowGlen</strong>, <strong>Presidential Glen</strong>, <strong>Stonewater</strong>,
<strong>Bell Farms</strong>, <strong>Wildhorse</strong> and the developments filling in along US-290.
Concentrated build windows, uniform builder shingle packages, and now a synchronised march toward
replacement age &mdash; the same pattern driving Hutto's current replacement wave.</p>
<p>The terrain is the same too. Manor sits on flat, open Blackland Prairie with minimal elevation
change and very little mature tree canopy over the newer subdivisions. That produces the two
conditions that define roofing here: <strong>unbroken sun</strong> through the summer, which ages
asphalt shingles faster than in the shaded parts of the metro, and <strong>unobstructed wind</strong>,
which arrives at roof edges with nothing to slow it down. Attic ventilation and wind-rated nailing
patterns matter as much in Manor as they do in 78634.</p>
<p>Manor does have one thing Hutto does not, and it affects the weather picture. It sits further
south and east, closer to the Colorado River bottomlands, which puts it slightly off the main
Williamson County storm track. A cell that batters Hutto sometimes passes north of Manor entirely.
The reverse also happens. It is a good reminder that hail is a per-address question, not a
per-town one &mdash; which is why an <a href="/services/roof-inspection-hutto-tx/">inspection</a>
beats an assumption.</p>
<p>Manor is in <strong>Travis County</strong>, so permitting runs through a different jurisdiction from
our Williamson County work. We handle it, but it can shift the schedule slightly compared with a
Hutto job.</p>
<p>Outside the subdivisions, Manor remains farm country, with the barns, shops and equipment sheds
that go with it &mdash; and the <a href="/services/metal-roofing-hutto-tx/">metal panel roofing</a>
work that comes with those.</p>

<h2>Services available in Manor</h2>
<p><a href="/services/roof-repair-hutto-tx/">Roof repair</a>,
<a href="/services/roof-replacement-hutto-tx/">replacement</a>,
<a href="/services/roof-installation-hutto-tx/">installation</a>,
<a href="/services/hail-damage-roof-repair-hutto-tx/">hail damage repair</a>,
<a href="/services/storm-damage-roof-repair-hutto-tx/">storm damage repair</a>,
<a href="/services/shingle-roofing-hutto-tx/">shingle roofing</a>,
<a href="/services/metal-roofing-hutto-tx/">metal roofing</a>,
<a href="/services/roof-inspection-hutto-tx/">inspections</a>,
<a href="/services/commercial-roofing-hutto-tx/">commercial roofing</a> and
<a href="/services/emergency-roof-repair-hutto-tx/">emergency roof repair</a>.</p>
""",
    },
]

for _a in AREAS:
    _a["path"] = f"/service-areas/{_a['slug']}/"
    _a["nav_label"] = f"Roofing in {_a['city']}"
    _a["service_name"] = f"Roofing in {_a['city']}, TX"
    _a["service_type"] = "Roofing"
    _a["hero_image"] = "/assets/img/LOCAL-HUTTO-ROOFING.webp"
    _a["body"] = _a["body"].replace("{county}", _a["county"])
    _a["trail"] = [
        ("Home", "/"),
        ("Service Areas", "/service-areas/"),
        (_a["city"], None),
    ]
