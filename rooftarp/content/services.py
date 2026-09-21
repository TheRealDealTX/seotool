"""The eight Roof Tarp service pages.

The live WordPress site had no /services/ section at all, so the head terms
with the most Search Console impressions -- "emergency roof tarp" (9,654
impressions), "emergency roof tarping" (5,704), "emergency tarping" (3,079) --
had no dedicated page to rank. These pages exist to serve them.

One primary keyword per page. That keyword appears in the title tag, the H1,
the meta description and the opening body copy. Each page covers a genuinely
different subject -- emergency response, installation method, long-term
tarping, residential vs commercial, storm vs hail, round-the-clock dispatch --
so no two pages are paraphrases of one another. validate.py enforces that.
"""

from siteconfig import BIZ

PHONE = BIZ["phone_display"]
PHONE_SHORT = BIZ["phone_short"]
EMAIL = BIZ["email"]

SERVICES = [
    # ------------------------------------------------------------- emergency
    {
        "slug": "emergency-roof-tarping",
        "nav_label": "Emergency Roof Tarping",
        "keyword": "emergency roof tarp",
        "secondary": ["emergency roof tarping", "emergency tarping"],
        "title": "Emergency Roof Tarp | 24/7 Emergency Roof Tarping | Roof Tarp",
        "description": (
            "Emergency roof tarp service across Texas. Crews dispatched day or night to stop water "
            "entering after storm, hail or tree damage. Call (956) 465-6045."
        ),
        "h1": 'Emergency <span class="accent-text">Roof Tarp</span> Service',
        "h1_plain": "Emergency Roof Tarp Service",
        "eyebrow": "Emergency Response",
        "service_name": "Emergency Roof Tarp Installation",
        "service_type": "Emergency Roof Tarping",
        "card": (
            "Roof opened up by a storm, a fallen limb or hail? A crew is dispatched to get a "
            "secured tarp over the breach before the next band of rain arrives."
        ),
        "card_cta": "Emergency tarping",
        "hero_intro": (
            "An <strong>emergency roof tarp</strong> is a race against the next rainfall. Once the roof "
            "covering is breached, every hour of exposure pushes water deeper into decking, insulation "
            "and drywall &mdash; and the damage compounds faster than most homeowners expect. We dispatch "
            "day or night, seven days a week, to get a properly secured tarp over the opening and stop "
            "the loss where it is."
        ),
        "body": f"""
<h2>Why an emergency roof tarp is time-critical</h2>
<p>Water does not wait for business hours. Once wind lifts a section of shingles or a limb punches
through the decking, the roof has an open path to the structure below. A single overnight storm can
move water through the attic insulation, into the ceiling gypsum and down inside a wall cavity. By
morning the visible damage is a stained ceiling; the actual damage is wet cavity insulation that will
hold moisture for weeks.</p>
<p>That is the entire argument for an <strong>emergency roof tarp</strong>. It is not a repair and it does
not pretend to be one. It is a controlled, watertight cover that buys you the time to arrange a proper
repair, get an adjuster out and order materials, without the loss growing every night.</p>

<h3>When to call for emergency tarping immediately</h3>
<ul>
<li><strong>Visible sky or daylight</strong> from inside the attic</li>
<li><strong>A tree limb or debris resting on or through the roof</strong></li>
<li><strong>A large section of shingles stripped</strong> by straight-line wind</li>
<li><strong>Active dripping</strong> into living space during rain</li>
<li><strong>Decking exposed</strong> where the covering peeled back</li>
<li><strong>Storm forecast within 24&ndash;48 hours</strong> on a roof already compromised</li>
</ul>

<h2>What we do on an emergency call</h2>
<p>The first conversation happens on the phone, before anyone is dispatched. We ask what happened,
roughly how large the opening is, whether anything is still on the roof, and whether water is entering
living space right now. That tells us what to bring &mdash; the tarp size, whether a second crew member
is needed for a limb, and whether the roof is safe to walk at all.</p>
<ol>
<li><strong>Safety assessment first.</strong> A roof with compromised decking is not automatically
walkable. If the structure is unsound, the tarp is anchored from the perimeter and the ladder rather
than by crossing the damaged plane.</li>
<li><strong>Find the full extent of the breach.</strong> The visible hole is often smaller than the
compromised area. Lifted shingles either side of an opening will let water in just as readily.</li>
<li><strong>Size the tarp past the damage.</strong> A tarp that stops at the edge of the hole channels
water under its own edge. Coverage runs well past the breach in every direction, and over the ridge
where the damage is near the top of a slope.</li>
<li><strong>Anchor and seal.</strong> Anchoring method depends on the roof &mdash; see our
<a href="/services/roof-tarp-installation/">roof tarp installation</a> page for how that decision
gets made.</li>
<li><strong>Document everything.</strong> Photographs before, during and after. Insurance carriers
ask for evidence of the original damage and of the mitigation step, and a tarp installed without
documentation can complicate a claim.</li>
</ol>

<h2>Emergency tarping and your insurance claim</h2>
<p>Most homeowner policies include a duty to protect the property from further damage after a covered
loss. In practice that means a carrier can reduce or dispute the portion of a claim caused by water
that entered <em>after</em> the initial event, if nothing was done to stop it. Emergency tarping is the
step that satisfies that obligation.</p>
<p>Keep the documentation: the date and time of the call, photographs of the damage before the tarp
went on, and the invoice. We photograph the work as a matter of course and provide the images, because
they are frequently what an adjuster needs to see.</p>

<h2>How long an emergency tarp stays on</h2>
<p>An emergency tarp is sized for the gap between the damage and the repair. If that gap is a week,
a standard poly tarp properly anchored is the right answer. If permitting, materials or an insurance
process is going to push the repair out by months, the correct answer is different &mdash; see
<a href="/services/long-term-roof-tarping/">long-term roof tarping</a>, which uses heavier material
and a different anchoring approach built to survive UV exposure and repeated wind loading.</p>
<p>We will tell you honestly which situation you are in. Putting a lightweight emergency tarp on a
roof that will not be repaired for four months is setting up a second failure.</p>

<h2>Texas storm damage, and why the calls cluster</h2>
<p>Emergency tarping demand in Texas is not evenly spread through the year. Spring hail along the
I-35 and DFW corridors, summer and autumn tropical systems on the Gulf coast, and high-wind events
across the Panhandle and West Texas each produce their own concentrated wave of calls. After a
significant event, every roofer in the affected metro is booked out for weeks &mdash; which is exactly
when tarping matters most, because the repair genuinely cannot happen quickly.</p>
<p>We work across the state rather than in a single metro, which means crews can be moved toward wherever
the weather actually hit. Find your area on the <a href="/service-areas/">service areas</a> page.</p>
""",
        "faqs": [
            ("How quickly can you get an emergency roof tarp installed?",
             "We dispatch " + BIZ["origin"].split("//")[1] + " crews day or night and aim to be on site "
             "within hours of your call. Actual timing depends on distance, how many calls a storm has "
             "generated in that metro, and whether conditions are safe to work in &mdash; we will not put "
             "a crew on a roof during active lightning."),
            ("Can you tarp a roof in the rain?",
             "Usually yes, and that is often exactly when it is needed. Steady rain is workable. Active "
             "lightning, high wind or ice is not, and we will say so rather than risk a crew. In those "
             "cases we schedule for the first safe window and talk you through interior containment in "
             "the meantime."),
            ("Will an emergency tarp stop the leak completely?",
             "A correctly installed tarp stops water entering through the breach it covers. If there is "
             "a second failure point elsewhere on the roof, that one needs covering too &mdash; which is "
             "why we look at the whole roof rather than just the obvious hole."),
            ("Does homeowners insurance cover emergency roof tarping?",
             "Emergency mitigation is commonly covered, and most policies actually require you to take "
             "reasonable steps to prevent further damage. Coverage specifics vary by policy, so confirm "
             "with your carrier. Keep the invoice and the photographs either way."),
            ("What does an emergency roof tarp cost?",
             "It depends on the area to be covered, roof pitch and height, how the tarp has to be "
             "anchored, and whether debris has to be removed first. We give you a figure before work "
             "starts, not after."),
        ],
    },

    # ---------------------------------------------------------- installation
    {
        "slug": "roof-tarp-installation",
        "nav_label": "Roof Tarp Installation",
        "keyword": "roof tarp installation",
        "secondary": ["roof tarp installers", "tarp installation"],
        "title": "Roof Tarp Installation | Professional Tarp Installers | Roof Tarp",
        "description": (
            "Professional roof tarp installation across Texas. Correct anchoring for shingle, tile and "
            "metal roofs, with no-nail options. Call (956) 465-6045."
        ),
        "h1": '<span class="accent-text">Roof Tarp</span> Installation',
        "h1_plain": "Roof Tarp Installation",
        "eyebrow": "Installation Method",
        "service_name": "Roof Tarp Installation",
        "service_type": "Roof Tarp Installation",
        "card": (
            "How a tarp is anchored decides whether it survives the next storm. Board-wrapped, "
            "ballasted or mechanically fixed, chosen for your roof covering."
        ),
        "card_cta": "Installation detail",
        "hero_intro": (
            "Most failed tarps did not fail because the material tore. They failed at the anchor points, "
            "or because water was channelled under an unsealed edge. <strong>Roof tarp installation</strong> "
            "is the part that determines whether a cover holds through the next front or peels off at 2am "
            "and leaves you worse off than before."
        ),
        "body": """
<h2>Roof tarp installation is an anchoring problem</h2>
<p>A tarp is a sail. Wind moving over a roof plane generates lift, and an inadequately secured tarp
will catch that lift, balloon, work its fasteners loose and come off &mdash; often taking a course of
shingles with it. Getting the material over the hole is the easy part of <strong>roof tarp
installation</strong>. Keeping it there through 40mph gusts is the actual job.</p>
<p>Three variables decide the method: what the roof is covered with, how long the tarp needs to last,
and whether the decking underneath is sound enough to hold a fastener at all.</p>

<h3>The three anchoring methods we use</h3>
<ul>
<li><strong>Board-wrapped (furring strip) anchoring.</strong> The tarp edge is rolled around a
1x3 or 2x4 batten and the assembly is screwed down through the roof. Rolling the edge spreads load
across the whole batten instead of concentrating it at individual fastener holes, which is what stops
the tarp tearing free at its grommets. This is the standard for anything expected to last more than
a few days.</li>
<li><strong>Ballasted, no-penetration anchoring.</strong> Sandbags, water bladders or weighted battens
hold the tarp without any fastener entering the roof. Essential on tile, slate and standing-seam metal,
where a screw creates a new leak that outlives the tarp. Also the right call on low-slope commercial
decks. Covered in detail in our guide to
<a href="/blog/how-to-tarp-a-roof-without-nails/">tarping a roof without nails</a>.</li>
<li><strong>Mechanical fixing to sound structure.</strong> Where decking is compromised, fasteners are
driven into rafters or into undamaged decking outside the failure zone rather than into the weakened
area, which would simply pull through.</li>
</ul>

<h2>Running the tarp over the ridge</h2>
<p>When damage sits near the top of a slope, the tarp must continue over the ridge and down the
opposite side. A tarp that stops short at the ridge line gives wind a leading edge to get under, and
gives water running down the far slope a direct path beneath it. Carrying it over and anchoring on the
back side removes both problems at once.</p>

<h2>Why edges matter more than the middle</h2>
<p>Water finds edges. A tarp laid flat with loose edges will shed the rain that lands on it and then
let a meaningful share of that water run underneath at the perimeter. Every edge has to either be
sealed down or oriented so that water sheds away from it:</p>
<ol>
<li><strong>The upslope edge</strong> is the critical one. It must be secured tight and, where
possible, tucked under the course of shingles above so water runs over the tarp rather than behind it.</li>
<li><strong>Side edges</strong> are battened or weighted along their full length, not just at corners.</li>
<li><strong>The downslope edge</strong> runs past the eave so water discharges into the gutter or
clear of the fascia.</li>
<li><strong>Overlaps</strong>, where more than one tarp is needed, are shingled &mdash; upper over
lower &mdash; never butted.</li>
</ol>

<h2>Sizing: cover past the damage, not to it</h2>
<p>A tarp sized to the hole is a tarp that fails. Coverage extends well beyond the breach on all sides
so the anchor points sit on sound, intact roof covering rather than on the damaged margin. On a roof
where wind has lifted shingles across a wide area, the tarp covers the lifted zone too &mdash; those
shingles are no longer watertight even though they are technically still in place.</p>

<h2>Roof coverings and what changes</h2>
<ul>
<li><strong>Asphalt shingle.</strong> The most forgiving. Battens can be fastened through, and holes
are sealed at repair. Standard board-wrapped method applies.</li>
<li><strong>Clay and concrete tile.</strong> Brittle and walkable only along specific lines. Foot
traffic breaks more tile than the storm did. Ballasted anchoring, walking boards, minimal crossings.</li>
<li><strong>Standing-seam and corrugated metal.</strong> Never penetrated for a temporary cover. Seam
clamps and ballast do the work.</li>
<li><strong>Low-slope and flat commercial.</strong> Water does not shed by gravity alone, so the tarp
is laid and ballasted to avoid ponding, with attention to drains and scuppers. See
<a href="/services/commercial-roof-tarping/">commercial roof tarping</a>.</li>
</ul>

<h2>What a finished installation should look like</h2>
<p>Taut, not drum-tight &mdash; some give absorbs wind loading without stressing the anchors. No
flapping anywhere along the perimeter. No standing water pockets. Every edge either battened, weighted
or tucked. Anchors on sound material. And a set of photographs showing all of it, for your records and
your insurer's.</p>
""",
        "faqs": [
            ("Do you have to put holes in my roof to install a tarp?",
             "Not always. On tile, slate and metal we use ballasted, no-penetration methods as standard. "
             "On asphalt shingle, board-wrapped fastening is usually the most secure option and the "
             "screw holes are dealt with at repair &mdash; but if you would rather avoid penetration "
             "entirely, say so and we will weight it instead."),
            ("How long does roof tarp installation take?",
             "A straightforward single-slope tarp is typically an hour or two on site. Multiple damage "
             "zones, steep or high roofs, tile, or debris that has to be removed first all extend that."),
            ("Can I install a roof tarp myself?",
             "On a low single-storey roof in calm weather, some homeowners do. The risks are real "
             "though: falls, further damage to the covering, and an anchoring job that does not hold. "
             "If the roof is steep, tall, wet or structurally compromised, it is not a DIY job."),
            ("What size tarp will my roof need?",
             "Larger than the damage by a wide margin on every side, and over the ridge if the breach "
             "is high on the slope. We size it on site &mdash; a tarp cut close to the hole is the most "
             "common reason a cover leaks."),
            ("Will the tarp damage my shingles?",
             "A properly installed tarp protects the roof rather than harming it. Poor installation can "
             "cause damage &mdash; dragging material across granules, over-tightening, or letting an "
             "edge flap and abrade the surface. Method and care are what prevent that."),
        ],
    },

    # ------------------------------------------------------------- long-term
    {
        "slug": "long-term-roof-tarping",
        "nav_label": "Long-Term Roof Tarping",
        "keyword": "long-term roof tarp",
        "secondary": ["permanent tarp roof", "long term roof tarp"],
        "title": "Long-Term Roof Tarp | Extended Roof Protection | Roof Tarp",
        "description": (
            "Long-term roof tarp installation built to last months, not days. Heavy-duty material and "
            "UV-resistant anchoring for extended repair delays. Call (956) 465-6045."
        ),
        "h1": 'Long-Term <span class="accent-text">Roof Tarp</span> Protection',
        "h1_plain": "Long-Term Roof Tarp Protection",
        "eyebrow": "Extended Protection",
        "service_name": "Long-Term Roof Tarp Installation",
        "service_type": "Long-Term Roof Tarping",
        "card": (
            "When a repair is months away, a standard emergency tarp will not survive the wait. "
            "Heavier material, UV-stable, re-tensioned and inspected."
        ),
        "card_cta": "Long-term options",
        "hero_intro": (
            "A <strong>long-term roof tarp</strong> is a different product and a different installation "
            "from an overnight emergency cover. When insurance, permitting, materials or contractor "
            "backlog push a repair out by months, a lightweight poly tarp will degrade in UV, work its "
            "anchors loose and fail &mdash; usually during the storm you needed it for."
        ),
        "body": """
<h2>When you need a long-term roof tarp rather than an emergency one</h2>
<p>The distinction is simply the expected wait. Under two weeks, a well-anchored standard tarp is
appropriate and cost-effective. Beyond about a month, the material itself becomes the limiting factor
and a <strong>long-term roof tarp</strong> is the correct specification.</p>
<p>Extended waits are common and usually nobody's fault:</p>
<ul>
<li><strong>Insurance claims</strong> that involve adjuster scheduling, supplements or disputes</li>
<li><strong>Post-catastrophe contractor backlog</strong> &mdash; after a major hail or hurricane
event every roofer in the metro is booked for months</li>
<li><strong>Material lead times</strong> on tile, slate, standing-seam metal or discontinued profiles</li>
<li><strong>Permitting and HOA approval</strong>, particularly in historic districts</li>
<li><strong>Structural repairs</strong> that have to be completed and inspected before the covering
goes back on</li>
<li><strong>Funding gaps</strong> where the homeowner is assembling the money to proceed</li>
</ul>

<h2>What makes a tarp last months instead of weeks</h2>
<p>Three things, in order of importance:</p>
<ol>
<li><strong>UV-stabilised material.</strong> Ultraviolet exposure is what actually kills tarps in
Texas. A standard blue poly tarp becomes brittle and begins shedding fibres in a matter of weeks under
direct sun. Heavy-duty reinforced poly and vinyl carry UV inhibitors that extend usable life
substantially. Our comparison of
<a href="/blog/vinyl-roof-tarp-vs-polyethylene-tarp-durability/">vinyl versus polyethylene durability</a>
covers the trade-offs.</li>
<li><strong>Load-spreading anchors.</strong> Over months, a tarp is loaded and unloaded by wind
thousands of times. Anchors that concentrate that cycling at a grommet will eventually tear through.
Board-wrapped edges distribute it along a batten.</li>
<li><strong>Seam and edge detailing.</strong> Anywhere two pieces meet, or an edge terminates, is a
failure point given enough time. Long-term installations use fewer, larger pieces and properly shingled
overlaps.</li>
</ol>

<h2>Maintenance is part of the specification</h2>
<p>A long-term tarp is not fit-and-forget. Thermal cycling and wind loosen fastenings; debris collects;
water can pond in a slackening section and add weight that accelerates the sag. We recommend:</p>
<ul>
<li><strong>A check after every significant wind or hail event</strong>, even if nothing looks wrong
from the ground</li>
<li><strong>Re-tensioning</strong> as the material relaxes &mdash; usually needed within the first
month and periodically after</li>
<li><strong>Clearing debris</strong>, particularly leaf litter and branches that trap moisture against
the material</li>
<li><strong>Watching for ponding</strong>, which is the clearest early warning that a section has gone
slack</li>
</ul>
<p>Signs that a long-term tarp has reached the end of its service life are covered in
<a href="/blog/signs-a-roof-tarp-needs-replacement/">signs a roof tarp needs replacement</a>.</p>

<h2>"Permanent" tarps: an honest answer</h2>
<p>People search for permanent tarp roofing, and the honest answer is that no tarp is a roof. Even the
heaviest reinforced vinyl, perfectly installed, is a temporary covering with a service life measured in
months to a couple of years in Texas sun. It does not carry the fire rating, wind rating, insurance
standing or resale value of a roof covering.</p>
<p>What a long-term tarp does do is genuinely protect the structure for as long as the repair takes,
without you having to re-do it every few weeks. If someone offers you a tarp as a permanent solution,
they are selling you something that will fail.</p>

<h2>Texas UV is the hard constraint</h2>
<p>Roof surface temperatures in a Texas summer routinely exceed anything the material was tested at in
temperate conditions, and UV index runs high from March through October. A tarp rated for a season
elsewhere will not deliver that here. We specify accordingly, and we would rather tell you a heavier
material is needed than come back in eight weeks to redo a failed installation.</p>
""",
        "faqs": [
            ("How long can a long-term roof tarp actually last?",
             "With heavy-duty UV-stabilised material, correct anchoring and periodic re-tensioning, "
             "several months to around a year in Texas conditions. A standard hardware-store poly tarp "
             "in the same position may begin failing within weeks. Material and installation are what "
             "make the difference."),
            ("Is a long-term tarp more expensive than an emergency tarp?",
             "Yes, because the material is heavier and the installation more involved. It is "
             "substantially cheaper than replacing a failed cheap tarp repeatedly, and far cheaper than "
             "the water damage a failure causes."),
            ("Can a tarp be left on over winter?",
             "Yes, and in Texas that is usually less demanding than summer &mdash; UV does more damage "
             "than cold. Ice loading and winter wind events still warrant a check afterwards."),
            ("Will a long-term tarp affect my home insurance?",
             "Policies differ. Some carriers want notice that a temporary covering is in place, and a "
             "few limit coverage if a roof remains untarped or unrepaired beyond a period. Tell your "
             "carrier what has been done and keep the documentation."),
            ("Can you convert my existing emergency tarp to a long-term one?",
             "Usually. We assess the existing installation, and in most cases the right move is a fresh "
             "installation in heavier material rather than reinforcing a cover that is already partway "
             "through its life."),
        ],
    },

    # ----------------------------------------------------------- residential
    {
        "slug": "residential-roof-tarping",
        "nav_label": "Residential Roof Tarping",
        "keyword": "residential roof tarping",
        "secondary": ["home roof tarping", "tarp my roof"],
        "title": "Residential Roof Tarping | Home Roof Tarp Service | Roof Tarp",
        "description": (
            "Residential roof tarping for Texas homeowners. Shingle, tile and metal roofs covered "
            "without damaging what is still sound. Call (956) 465-6045."
        ),
        "h1": 'Residential <span class="accent-text">Roof Tarping</span>',
        "h1_plain": "Residential Roof Tarping",
        "eyebrow": "For Homeowners",
        "service_name": "Residential Roof Tarping",
        "service_type": "Residential Roof Tarping",
        "card": (
            "Pitched shingle, tile and metal roofs on occupied homes &mdash; covered without "
            "breaking tile, marking siding or damaging landscaping."
        ),
        "card_cta": "Residential service",
        "hero_intro": (
            "<strong>Residential roof tarping</strong> happens on an occupied home, usually with a family "
            "inside and belongings under the affected ceiling. That changes the job: the roof has to be "
            "covered, but the tile that is still intact, the siding, the landscaping and the interior all "
            "have to come through it unharmed too."
        ),
        "body": """
<h2>What residential roof tarping involves</h2>
<p>Homes have steeper roofs, more complex geometry and more fragile coverings than commercial
buildings. A typical Texas house roof brings valleys, hips, dormers, plumbing vents, chimneys and
skylights &mdash; each one a place where a tarp has to be worked around rather than simply laid across.
<strong>Residential roof tarping</strong> is largely about handling those transitions properly.</p>

<h3>Damage we are most often called to cover</h3>
<ul>
<li><strong>Wind-stripped shingle fields</strong> where a section has peeled back and exposed decking</li>
<li><strong>Tree and limb strikes</strong>, including penetrations through the decking</li>
<li><strong>Hail bruising</strong> severe enough to compromise the mat, particularly on older roofs</li>
<li><strong>Broken or slipped tile</strong> leaving underlayment exposed to direct sun and rain</li>
<li><strong>Failed valleys and flashing</strong> after a wind event has displaced them</li>
<li><strong>Fire or smoke damage</strong> where a section has been opened up by the fire service</li>
</ul>

<h2>Protecting what is not damaged</h2>
<p>This is the part that separates a careful residential job from a rushed one. On a tile roof, careless
foot traffic breaks more tile than the storm did &mdash; and replacement tile for an older profile can
be difficult to source, which turns a contained repair into a much larger one. We use walking boards,
plan a route across load-bearing points, and cross the field as few times as possible.</p>
<p>On the ground, ladders get standoffs so they bear on fascia rather than gutters, sandbags are placed
rather than dropped, and beds and shrubs get worked around. Debris from the damaged area gets collected
rather than swept off the roof into the garden.</p>

<h2>Working around an occupied house</h2>
<p>Someone is usually home, often distressed, sometimes with water still coming through a ceiling. A
few practical things we do as standard:</p>
<ol>
<li><strong>Tell you where we will be walking</strong> and for how long, so you can move anything
underneath the affected area.</li>
<li><strong>Advise on interior containment</strong> &mdash; where to place containers, when to pull
back insulation, and when to isolate a circuit if water is anywhere near a fixture or ceiling fan.</li>
<li><strong>Keep the driveway and access clear</strong> where possible, and tell you when it will not be.</li>
<li><strong>Warn about noise</strong>. Fastening battens on a roof directly above a bedroom is loud
inside, which matters at 3am.</li>
</ol>

<h2>Common residential roof coverings</h2>
<ul>
<li><strong>Asphalt shingle</strong> &mdash; the majority of Texas housing stock, and the most
straightforward to tarp securely.</li>
<li><strong>Clay and concrete tile</strong> &mdash; common in South and Central Texas. Ballasted
anchoring only; no fasteners through tile.</li>
<li><strong>Standing-seam metal</strong> &mdash; increasingly common on newer builds. Clamped and
weighted, never penetrated.</li>
<li><strong>Wood shake</strong> &mdash; rarer, brittle with age, needs careful weight distribution.</li>
</ul>

<h2>After the tarp is on</h2>
<p>We leave you with photographs of the damage and the completed cover, an invoice suitable for an
insurance claim, and a straight answer about how long the cover should hold. If the repair is going to
be a long wait, we will say so and explain what
<a href="/services/long-term-roof-tarping/">long-term tarping</a> would involve instead.</p>
<p>If water reached the ceiling or wall cavities, deal with that separately and promptly &mdash; our
guide to <a href="/blog/preventing-interior-water-damage-after-roof-failure/">preventing interior water
damage after roof failure</a> covers what matters in the first 48 hours.</p>
""",
        "faqs": [
            ("Will tarping break my roof tiles?",
             "It should not. Tile is walkable only along specific lines, so we use walking boards, plan "
             "the route and cross the field as little as possible. We also anchor by ballast rather than "
             "fastening through tile. Careless tarping on tile does cause breakage, which is exactly why "
             "method matters."),
            ("Do I need to be home for the tarping?",
             "It helps for the initial assessment so we can show you what we have found, but it is not "
             "essential provided we have safe access and your authorisation. We photograph everything "
             "either way."),
            ("Can you tarp a two-storey or steep roof?",
             "Yes. Height and pitch change the equipment and the time, not whether it can be done. Very "
             "steep or structurally compromised roofs may be anchored from the perimeter rather than by "
             "walking the damaged plane."),
            ("What if the damage is right at the ridge?",
             "The tarp carries over the ridge and anchors on the opposite slope. Stopping a tarp at the "
             "ridge line gives wind an edge to lift and water a path underneath."),
            ("Should I move things out of the room below?",
             "Yes, if water has come through or the ceiling is stained. Wet gypsum can fail without much "
             "warning. Move what you can, and we will tell you which areas to stay clear of while we work "
             "above."),
        ],
    },

    # ------------------------------------------------------------ commercial
    {
        "slug": "commercial-roof-tarping",
        "nav_label": "Commercial Roof Tarping",
        "keyword": "commercial roof tarping",
        "secondary": ["commercial roof tarp", "flat roof tarping"],
        "title": "Commercial Roof Tarping | Flat & Low-Slope Tarps | Roof Tarp",
        "description": (
            "Commercial roof tarping for flat and low-slope buildings across Texas. Ballasted covers, "
            "drain management, after-hours work. Call (956) 465-6045."
        ),
        "h1": 'Commercial <span class="accent-text">Roof Tarping</span>',
        "h1_plain": "Commercial Roof Tarping",
        "eyebrow": "For Businesses",
        "service_name": "Commercial Roof Tarping",
        "service_type": "Commercial Roof Tarping",
        "card": (
            "Flat and low-slope membrane roofs, ballasted rather than penetrated, with drains kept "
            "clear and work scheduled around your trading hours."
        ),
        "card_cta": "Commercial service",
        "hero_intro": (
            "<strong>Commercial roof tarping</strong> is a different discipline from residential work. "
            "Flat and low-slope roofs do not shed water by gravity, membranes cannot be penetrated without "
            "creating a new problem, and the cost of a leak is usually measured in lost trading and damaged "
            "stock rather than a stained ceiling."
        ),
        "body": """
<h2>Why flat roofs need a different approach</h2>
<p>On a pitched roof, gravity does most of the work &mdash; get a tarp over the hole and water runs off.
On a low-slope commercial deck, water sits. A tarp laid the way it would be on a house creates ponding,
and ponded water finds every seam and edge given time. <strong>Commercial roof tarping</strong> has to be
planned around where the water will actually go.</p>

<h3>What we account for on a commercial deck</h3>
<ul>
<li><strong>Drains and scuppers.</strong> A tarp that covers a drain converts a contained leak into a
flooded roof. Drainage paths stay open, and the cover is laid to direct water toward them.</li>
<li><strong>Existing membrane type.</strong> TPO, EPDM, modified bitumen and built-up roofs each behave
differently and have different repair implications. Penetrating any of them for a temporary cover is
almost always the wrong call.</li>
<li><strong>Rooftop plant.</strong> HVAC units, ducting, conduit, vents and walkway pads all have to be
worked around, and units generally need to stay serviceable.</li>
<li><strong>Parapets and edge detail.</strong> These are useful anchor points and also common leak
sources in their own right.</li>
<li><strong>Load limits.</strong> Ballast has to be adequate but distributed &mdash; concentrating
weight on a deck already compromised is not acceptable.</li>
</ul>

<h2>Ballast, not fasteners</h2>
<p>Commercial covers are held by weight in nearly every case: sandbags, weighted battens and water
bladders placed to spread load across the deck. This protects the membrane, avoids creating new
penetrations that a roofing contractor then has to chase, and keeps any eventual warranty conversation
simpler. Screwing battens through a TPO membrane to hold a temporary tarp is how a contained repair
turns into a membrane replacement argument.</p>

<h2>Business continuity comes first</h2>
<p>The point of a commercial tarp is usually to keep the business trading. That shapes the work:</p>
<ol>
<li><strong>Out-of-hours scheduling</strong> where daytime work would disrupt trading, and we will
work overnight when that is what keeps the doors open.</li>
<li><strong>Protecting what is underneath</strong> &mdash; server rooms, stock, kitchen equipment and
production lines get priority in the sequencing.</li>
<li><strong>Clear access and signage</strong> so customers and staff are not routed under the work.</li>
<li><strong>Documentation for the claim</strong>, which on a commercial policy frequently has to
satisfy a broker and a loss adjuster as well as the carrier.</li>
</ol>

<h2>Building types we cover</h2>
<ul>
<li><strong>Retail units and strip centres</strong> &mdash; often multi-tenant, where one breach
affects several businesses and the responsibility split matters</li>
<li><strong>Warehouses and distribution</strong> &mdash; large spans, high decks, significant stock
exposure</li>
<li><strong>Offices</strong> &mdash; IT and document exposure, and ceiling systems that show damage quickly</li>
<li><strong>Restaurants</strong> &mdash; health inspection implications if water reaches a prep area</li>
<li><strong>Schools, churches and civic buildings</strong> &mdash; usually needing work scheduled
around occupancy</li>
<li><strong>Light industrial</strong> &mdash; where production downtime dominates the cost of the loss</li>
</ul>

<h2>Property managers and multi-site operators</h2>
<p>If you run a portfolio across Texas metros, one point of contact for tarping across all of them is
usually simpler than a different local contractor per site. We work statewide &mdash; see
<a href="/service-areas/">service areas</a> &mdash; and can provide consistent documentation across
sites, which matters when a single carrier is handling several claims from one storm event.</p>
""",
        "faqs": [
            ("Can you tarp a flat commercial roof?",
             "Yes, and it is a large part of what we do. The method differs from a pitched roof: "
             "ballasted anchoring, careful attention to drains and scuppers, and layout planned so water "
             "does not pond on the cover."),
            ("Will tarping void my roof membrane warranty?",
             "Penetrating the membrane can. That is precisely why we ballast rather than fasten on "
             "commercial decks. If you have an active warranty, tell us who holds it and we will work "
             "to avoid compromising it."),
            ("Can you work outside business hours?",
             "Yes. Overnight and weekend work is routine for commercial jobs where daytime work would "
             "stop trading."),
            ("How do you handle multi-tenant buildings?",
             "We document the affected area precisely and photograph which units sit beneath it, "
             "because that is usually what determines how the claim and any cost split gets handled."),
            ("Do you provide documentation for commercial insurance claims?",
             "Yes &mdash; dated photographs before, during and after, a written description of the "
             "damage and the mitigation, and an itemised invoice. Commercial claims typically need more "
             "documentation than residential ones."),
        ],
    },

    # ----------------------------------------------------------------- storm
    {
        "slug": "storm-damage-roof-tarping",
        "nav_label": "Storm Damage Tarping",
        "keyword": "storm damage roof tarping",
        "secondary": ["emergency tarping services", "tarping services"],
        "title": "Storm Damage Roof Tarping | Texas Storm Response | Roof Tarp",
        "description": (
            "Storm damage roof tarping across Texas after wind, tornado and tropical systems. Crews "
            "moved toward the affected metro. Call (956) 465-6045."
        ),
        "h1": 'Storm Damage <span class="accent-text">Roof Tarping</span>',
        "h1_plain": "Storm Damage Roof Tarping",
        "eyebrow": "Storm Response",
        "service_name": "Storm Damage Roof Tarping",
        "service_type": "Storm Damage Roof Tarping",
        "card": (
            "After a named storm or a straight-line wind event, crews are moved toward the metro "
            "that actually got hit rather than waiting on a local backlog."
        ),
        "card_cta": "Storm response",
        "hero_intro": (
            "<strong>Storm damage roof tarping</strong> is a logistics problem as much as a roofing one. "
            "A severe event damages thousands of roofs in a metro within an hour, and every local roofer "
            "is immediately booked for weeks. The tarp is what carries you through that backlog without "
            "the loss growing every time it rains."
        ),
        "body": """
<h2>How Texas storms damage roofs</h2>
<p>Different systems do different damage, and the damage pattern changes what tarping is needed.</p>
<ul>
<li><strong>Straight-line winds.</strong> The most common cause of stripped shingle fields. Wind gets
under a leading edge &mdash; often at an eave or rake &mdash; and peels a section back. Damage is
usually concentrated on one slope, the one facing the wind.</li>
<li><strong>Tornadoes.</strong> Highly localised and often total. Debris impact alongside pure wind
loading. Structural assessment comes before any tarp.</li>
<li><strong>Tropical systems and hurricanes.</strong> Gulf coast metros. Prolonged wind loading over
many hours rather than a single gust, plus wind-driven rain that penetrates gaps a normal storm would
not reach. Coverage has to assume sustained loading.</li>
<li><strong>Hail.</strong> A distinct problem covered on our
<a href="/services/hail-damage-roof-tarping/">hail damage tarping</a> page &mdash; the damage is often
not visible from the ground.</li>
<li><strong>Falling trees and limbs.</strong> Point loading, frequently through the decking. The limb
usually has to come off before anything can be covered.</li>
</ul>

<h2>The post-storm backlog, and why tarping matters most then</h2>
<p>After a significant event the sequence is predictable. Day one, everyone calls a roofer. Week one,
every reputable local contractor is quoting weeks or months out. Week two, out-of-state storm chasers
arrive. Meanwhile the weather has not stopped, and every subsequent rainfall drives water through the
same opening into an increasingly saturated structure.</p>
<p>Tarping is what breaks that cycle. It is not competing with the repair &mdash; it is what makes it
acceptable for the repair to happen on a realistic timeline instead of an impossible one.</p>

<h2>Working a storm response</h2>
<p>Because we operate across Texas rather than from one metro, crews can be moved toward wherever the
system actually hit. In practice that means:</p>
<ol>
<li><strong>Triage by severity.</strong> Open decking and active interior water entry come before
cosmetic damage, regardless of call order.</li>
<li><strong>Safety assessment before access.</strong> After tornado or major wind damage, the roof may
not be structurally sound and downed power lines are a genuine hazard. We will not put a crew on an
unsafe structure, and we will tell you if that is the situation.</li>
<li><strong>Cover the whole compromised area.</strong> After wind, shingles well beyond the obviously
stripped section are often lifted and no longer watertight. Tarping only the bare patch leaves those
open.</li>
<li><strong>Documentation for what will be a busy claims season.</strong> Adjusters handling hundreds
of claims from one event move fastest on the files with clear dated evidence.</li>
</ol>

<h2>What to do before we arrive</h2>
<ul>
<li><strong>Stay off the roof.</strong> Wet, damaged roofing is the single most dangerous place on the
property right now.</li>
<li><strong>Photograph everything</strong> from the ground, including debris and any interior damage,
before anything is moved or cleaned up.</li>
<li><strong>Contain interior water</strong> &mdash; containers, moved furniture, and pulled-back
insulation where you can reach it safely.</li>
<li><strong>Kill power to affected circuits</strong> if water is near fixtures, ceiling fans or the
panel.</li>
<li><strong>Do not agree to anything at the door.</strong> Post-storm door-knocking is heavy in Texas
and not all of it is legitimate.</li>
</ul>

<h2>Seasonality across the state</h2>
<p>Spring is the severe convective season through Central and North Texas &mdash; wind and hail along
I-35 and across DFW. Summer and early autumn bring Gulf systems to Houston, Corpus Christi and
Beaumont. The Panhandle and West Texas see high-wind events and dust-driven storms with their own
timing. Because these peaks do not coincide, crews can be positioned toward whichever part of the state
is in season.</p>
""",
        "faqs": [
            ("How soon after a storm should I get a tarp on?",
             "As soon as it is safe. The damage from the storm itself is already done; what you are "
             "preventing is everything the next rainfall adds to it."),
            ("Do you work during a hurricane or active severe weather?",
             "No &mdash; not during the event itself. We stage and respond as soon as conditions allow. "
             "Sending a crew onto a roof in high wind or lightning is not something we will do."),
            ("What if a tree is still on my roof?",
             "Tell us when you call. The limb generally has to be removed before a tarp can go on, and "
             "how it is removed matters &mdash; dragging it off can widen the opening considerably."),
            ("My neighbours all have damage too. Can you do several houses?",
             "Yes, and it is usually more efficient for everyone. Tell us when you call and we will "
             "schedule the street together."),
            ("Should I wait for the insurance adjuster before tarping?",
             "No. Most policies require you to prevent further damage, and waiting typically makes the "
             "claim worse rather than better. Photograph the damage first, then tarp, and keep the "
             "invoice."),
        ],
    },

    # ------------------------------------------------------------------ hail
    {
        "slug": "hail-damage-roof-tarping",
        "nav_label": "Hail Damage Tarping",
        "keyword": "hail damage roof tarping",
        "secondary": ["hail damage roof tarp", "roof tarp after hail"],
        "title": "Hail Damage Roof Tarping | Texas Hail Alley | Roof Tarp",
        "description": (
            "Hail damage roof tarping across Texas hail alley. Covering bruised, fractured and "
            "punctured roofs before the next storm. Call (956) 465-6045."
        ),
        "h1": 'Hail Damage <span class="accent-text">Roof Tarping</span>',
        "h1_plain": "Hail Damage Roof Tarping",
        "eyebrow": "Hail Response",
        "service_name": "Hail Damage Roof Tarping",
        "service_type": "Hail Damage Roof Tarping",
        "card": (
            "Hail damage often is not visible from the ground. Where impact has fractured the mat or "
            "holed the decking, the roof needs covering before the next front."
        ),
        "card_cta": "Hail tarping",
        "hero_intro": (
            "<strong>Hail damage roof tarping</strong> is less obvious than wind tarping, because hail "
            "frequently does not leave a hole you can see from the driveway. It bruises the shingle mat, "
            "fractures the surface and knocks off the granule layer that protects the asphalt &mdash; and "
            "the roof then fails progressively over the following weeks."
        ),
        "body": """
<h2>What hail actually does to a roof</h2>
<p>A hailstone hitting an asphalt shingle does three things. It knocks granules off the surface,
exposing the asphalt beneath to UV. It bruises or fractures the fibreglass mat under the surface,
creating a soft spot that will not shed water reliably. And at larger stone sizes, it can punch
straight through the shingle and into the decking.</p>
<p>Only the third of those is visible from the ground. The first two are what make hail damage
insidious &mdash; the roof looks broadly intact, but its effective life has been cut dramatically and
it will begin leaking well before anyone expects it to.</p>

<h3>When hail damage warrants a tarp</h3>
<ul>
<li><strong>Visible punctures</strong> through shingle into decking</li>
<li><strong>Shattered or split tile</strong> leaving underlayment exposed</li>
<li><strong>Dented and split metal panels</strong> where the coating has been broken</li>
<li><strong>Widespread granule loss</strong> with exposed asphalt over a large area</li>
<li><strong>Skylights or vents broken</strong> by impact</li>
<li><strong>Any active leak</strong> following a hail event</li>
</ul>
<p>Widespread bruising without penetration usually does not need an immediate tarp &mdash; it needs an
inspection and a claim. If you are unsure which situation you are in, that is a reasonable thing to ask
us about on the phone.</p>

<h2>Checking for hail damage without climbing up</h2>
<p>Several ground-level indicators are reliable, and they are worth checking before deciding whether
you have a problem:</p>
<ol>
<li><strong>Gutters and downspouts.</strong> A heavy accumulation of granules where a downspout
discharges is one of the clearest signs the roof surface took a beating.</li>
<li><strong>The AC condenser.</strong> Its aluminium fins dent easily and at roughly the same
threshold as roofing damage. Dented fins means the stones were large enough to matter.</li>
<li><strong>Soft metals around the property</strong> &mdash; mailbox, gutter faces, vent caps, garage
door panels, window screens. Dents on these are a proxy for what hit the roof.</li>
<li><strong>Fence caps and deck boards</strong>, where fresh impact marks show clearly on wood.</li>
<li><strong>Cars left outside.</strong> If the vehicles were dented, the roof was hit at least as hard.</li>
</ol>

<h2>Texas hail alley</h2>
<p>North and Central Texas sit in one of the most hail-prone regions in the country. The DFW metro,
the I-35 corridor through Waco, Temple and Austin, and the Panhandle around Lubbock and Amarillo all
see multiple damaging hail events in a typical spring.</p>
<p>What makes hail difficult is how narrow the swaths are. A hail core can be a mile or two wide &mdash;
one subdivision is destroyed while the next street over is untouched. That is why "my neighbour's roof
is fine" is not evidence that yours is, and why a per-property check matters more with hail than with
wind.</p>

<h2>Hail, tarping and the claim</h2>
<p>Hail claims are among the most commonly disputed in Texas, largely because the damage is arguable in
a way that a tree through the roof is not. A few things help:</p>
<ul>
<li><strong>Date the event.</strong> Carriers work from specific storm dates, and knowing which one hit
you matters.</li>
<li><strong>Photograph before anything changes.</strong> Granule accumulation washes away; dents get
repaired.</li>
<li><strong>Do not let anyone "test" your roof by making marks on it.</strong> This happens, and it
compromises the claim.</li>
<li><strong>Keep the tarping invoice.</strong> It is evidence both of mitigation and of the damage
having been severe enough to require it.</li>
</ul>
<p>Once the roof is covered, the repair conversation can happen on a normal timescale. If that
conversation looks like it will run for months &mdash; common after a large hail event &mdash;
<a href="/services/long-term-roof-tarping/">long-term tarping</a> is the right specification rather
than leaving an emergency cover to degrade.</p>
""",
        "faqs": [
            ("Can hail damage a roof without breaking through it?",
             "Yes, and that is the usual case. Hail bruises the mat and strips the granule layer, which "
             "shortens the roof's life significantly and leads to leaks later. It is real damage even "
             "though nothing is visibly holed."),
            ("Do I need a tarp if there is no visible hole after hail?",
             "Often not immediately. If there is no penetration and no active leak, what you need is an "
             "inspection and a claim rather than a tarp. Call and describe what you are seeing and we "
             "will give you a straight answer."),
            ("How long do I have to file a hail claim in Texas?",
             "Policies set their own deadlines and Texas law has applicable time limits, but the "
             "practical answer is to file promptly. Delay makes it harder to attribute damage to a "
             "specific storm date, which is the most common reason hail claims get disputed."),
            ("Will hail damage show up on a metal roof?",
             "Yes, as dents and, where the coating has split, as corrosion starting later. Denting alone "
             "may be cosmetic on metal; broken coating is not."),
            ("Should I use the roofer who knocks on my door after a hailstorm?",
             "Be careful. Post-hail door-knocking in Texas draws a lot of out-of-state operators who "
             "leave after the season. Check licensing, insurance and a local track record before signing "
             "anything, and never sign a document that assigns your claim benefits away."),
        ],
    },

    # ------------------------------------------------------------------ 24/7
    {
        "slug": "24-7-roof-tarping",
        "nav_label": "24/7 Roof Tarping",
        "keyword": "24/7 roof tarping",
        "secondary": ["24 hour roof tarping", "overnight roof tarping"],
        "title": "24/7 Roof Tarping | Overnight & Weekend Tarp Crews | Roof Tarp",
        "description": (
            "24/7 roof tarping in Texas. Overnight, weekend and holiday dispatch for roofs that cannot "
            "wait until Monday. Call (956) 465-6045."
        ),
        "h1": '24/7 <span class="accent-text">Roof Tarping</span>',
        "h1_plain": "24/7 Roof Tarping",
        "eyebrow": "Round-the-Clock",
        "service_name": "24/7 Roof Tarping Dispatch",
        "service_type": "24/7 Roof Tarping",
        "card": (
            "Roofs fail at night and at weekends. Dispatch runs around the clock, including "
            "holidays, because waiting until Monday is how a contained loss spreads."
        ),
        "card_cta": "Round-the-clock",
        "hero_intro": (
            "<strong>24/7 roof tarping</strong> exists because roofs do not fail politely. The call that "
            "matters most usually comes at 11pm on a Saturday, with water coming through a ceiling and "
            "another band of rain an hour out. Waiting until Monday is what turns a contained loss into a "
            "structural one."
        ),
        "body": """
<h2>Why overnight response changes the outcome</h2>
<p>The cost of a roof breach is a function of how long it stays open and how much rain falls through it
in that time. A roof opened at 10pm and covered at midnight loses one room's ceiling. The same roof
covered on Monday morning has had two more nights of rain moving through wall cavities, insulation and
flooring &mdash; and at that point you are into drying equipment, mould remediation and replacement
rather than a patch and repaint.</p>
<p>That is the whole case for <strong>24/7 roof tarping</strong>. The tarp costs the same at 2am as it
does at 2pm. The damage it prevents does not.</p>

<h2>When people actually call</h2>
<ul>
<li><strong>Late evening storms</strong>, the most common by a wide margin &mdash; Texas convective
storms frequently fire in the late afternoon and run into the night</li>
<li><strong>Overnight wind events</strong> discovered when someone wakes to water</li>
<li><strong>Weekends</strong>, when the damage happened Friday and no local contractor is answering</li>
<li><strong>Holidays</strong> &mdash; Thanksgiving and Christmas storms are a recurring reality</li>
<li><strong>Pre-dawn discovery</strong>, where a slow leak finally comes through a ceiling</li>
<li><strong>Ahead of an incoming front</strong>, where a roof already damaged has hours before the
next system arrives</li>
</ul>

<h2>What working at night actually requires</h2>
<p>Night tarping is not daytime tarping with torches. It needs proper lighting so the crew can see the
roof plane and the edges they are anchoring to, and it needs a more conservative safety line, because
hazards that are obvious in daylight &mdash; a soft spot in decking, a displaced vent, a power drop
&mdash; are not at night.</p>
<ol>
<li><strong>Proper work lighting</strong>, set up before anyone goes up.</li>
<li><strong>A more cautious structural call.</strong> If we cannot satisfy ourselves the roof is safe
to walk in the dark, we anchor from the perimeter or we secure what we can and return at first light.
We will tell you which.</li>
<li><strong>Noise awareness.</strong> Fastening battens above a bedroom at 3am is loud, and we would
rather warn you than surprise you.</li>
<li><strong>Weather judgement.</strong> Lightning stops work, full stop. Rain alone generally does not.</li>
</ol>

<h2>What we can help with on the phone, immediately</h2>
<p>Even before a crew arrives, some of the most valuable things happen over the phone. When you call at
night we will talk you through:</p>
<ul>
<li>Where to place containers, and why a hole punched deliberately in a bulging ceiling is sometimes
the right move rather than letting it collapse</li>
<li>Which circuits to kill if water is near fixtures, fans or the panel</li>
<li>What to photograph before anything is moved</li>
<li>Whether what you are describing is safe to leave until morning &mdash; sometimes it genuinely is,
and we will say so rather than dispatch unnecessarily</li>
</ul>

<h2>Holidays and the quiet weeks</h2>
<p>Roofing companies thin out considerably over Christmas and New Year, and winter storms do not.
Dispatch runs through holidays. If you are getting voicemail everywhere else, that is precisely the
situation this service exists for.</p>
<p>For the detail of what happens once a crew is on site, see
<a href="/services/emergency-roof-tarping/">emergency roof tarping</a>.</p>
""",
        "faqs": [
            ("Do you really answer the phone at 3am?",
             "Yes. Dispatch runs around the clock, including weekends and holidays. If a storm has just "
             "moved through a metro there may be a queue, but the phone is answered."),
            ("Is overnight tarping more expensive?",
             "Out-of-hours work can carry a premium depending on the job and the metro. We tell you the "
             "figure before we dispatch, not afterwards."),
            ("Can you actually see well enough to work at night?",
             "With proper work lighting, yes. We take a more conservative view of what is safe to walk "
             "in the dark, and if a roof does not meet that bar we secure what we can and return at "
             "first light."),
            ("What if it is still storming when I call?",
             "We will not send a crew up during lightning or high wind. We will stage nearby, talk you "
             "through interior containment, and move the moment conditions allow."),
            ("Is it worth calling at night or should I wait until morning?",
             "Call. If it can safely wait we will tell you so honestly. If it cannot, the difference "
             "between covering it now and covering it in eight hours is often the difference between a "
             "repaint and a rebuild."),
        ],
    },
]

SERVICES_BY_SLUG = {s["slug"]: s for s in SERVICES}
