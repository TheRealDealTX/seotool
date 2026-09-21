"""About, FAQs and Contact.

These three existed on the WordPress site and are rebuilt here with their own
copy. The FAQ page answers the questions people actually search -- cost,
insurance, how long a tarp lasts, DIY -- rather than repeating the per-service
FAQ blocks, so it does not duplicate the service pages.
"""

from siteconfig import BIZ, RESPONSE_WINDOW

PHONE = BIZ["phone_display"]
EMAIL = BIZ["email"]

ABOUT = {
    "path": "/about/",
    "title": "About Roof Tarp | Texas Emergency Tarping Crews | Roof Tarp",
    "description": (
        "Roof Tarp provides 24/7 emergency roof tarping across Texas. What we do, how we work and "
        "why tarping is a discipline of its own. Call (956) 465-6045."
    ),
    "h1": 'About <span class="accent-text">Roof Tarp</span>',
    "h1_plain": "About Roof Tarp",
    "eyebrow": "Who We Are",
    "body": f"""
<h2>We do one thing</h2>
<p>Roof Tarp is an emergency tarping company. We are not a general roofing contractor who also tarps
when asked &mdash; tarping is the whole business, and that focus is deliberate.</p>
<p>The reason is simple. For a roofing company, a tarp is an unbilled inconvenience on the way to the
job they actually want. It gets done quickly, by whoever is free, with whatever is on the truck. For us
it is the job. We carry the right material in the right sizes, the crews have done it thousands of
times, and the anchoring method gets chosen for your roof rather than for speed.</p>

<h2>Why tarping is its own discipline</h2>
<p>Most failed tarps did not fail because the material tore. They failed at the anchor points, or
because an unsealed edge channelled water underneath, or because a cover sized to the hole left its
fixings on damaged roofing that could not hold them.</p>
<p>Getting a sheet over an opening is easy. Keeping it there through a 40mph front, without putting new
holes in a tile roof or voiding a membrane warranty, is a skill. It is worth having someone do it who
does nothing else.</p>

<h2>How we work</h2>
<ul>
<li><strong>We answer the phone.</strong> Dispatch runs 24 hours, including weekends and holidays.
Most roofs fail outside business hours, which is exactly when most companies are unreachable.</li>
<li><strong>We tell you the price first.</strong> You get a figure before work starts, not an invoice
afterwards.</li>
<li><strong>We photograph everything.</strong> Before, during and after. Insurers ask for evidence of
the original damage and of the mitigation step, and a tarp installed without documentation can
complicate a claim.</li>
<li><strong>We will talk you out of work you do not need.</strong> If what you are describing does not
need a tarp tonight, we will say so. Hail bruising with no penetration needs an inspection and a claim,
not an emergency call-out.</li>
<li><strong>We say when a roof is unsafe.</strong> If the structure will not carry a crew, we anchor
from the perimeter or we wait for daylight, and we tell you which.</li>
</ul>

<h2>Working across Texas</h2>
<p>We operate statewide rather than out of a single metro, which matters more than it sounds. Texas
storm seasons do not coincide: spring hail runs through DFW and the I-35 corridor, Gulf tropical
systems hit the coast in late summer and autumn, and the Panhandle and West Texas have their own
high-wind calendar. Because those peaks are staggered, crews can be moved toward whichever part of the
state is actually being hit.</p>
<p>That is the difference that matters after a major event. When every local roofer in a metro is booked
for two months, capacity has to come from somewhere else.</p>

<h2>What we are honest about</h2>
<p>A tarp is not a roof. Even the heaviest reinforced vinyl, perfectly installed, is a temporary
covering with a service life measured in months in Texas sun. It carries no fire rating, no wind rating
and no resale value. Anyone selling you a tarp as a permanent solution is selling you a second failure.</p>
<p>What a tarp does is stop the loss growing while you arrange the repair properly &mdash; through an
insurance process, a permit, a material lead time or a contractor backlog. That is genuinely valuable,
and it is all we claim.</p>

<h2>Get in touch</h2>
<p>Call <a href="tel:{BIZ['phone_href']}">{PHONE}</a> any time, or email
<a href="mailto:{EMAIL}">{EMAIL}</a>. We aim to be on site {RESPONSE_WINDOW}.</p>
""",
}

FAQS_PAGE = {
    "path": "/faqs/",
    "title": "Roof Tarping FAQs | Cost, Insurance & Tarp Life | Roof Tarp",
    "description": (
        "Common questions about roof tarping: what it costs, whether insurance covers it, how long a "
        "tarp lasts and when to DIY. Call (956) 465-6045."
    ),
    "h1": 'Roof Tarping <span class="accent-text">FAQs</span>',
    "h1_plain": "Roof Tarping FAQs",
    "eyebrow": "Common Questions",
    "intro": (
        "The questions we are asked most often, answered plainly. Service-specific questions are on "
        "the individual service pages; these are the general ones about cost, insurance, timing and "
        "whether you should be doing it yourself."
    ),
    "faqs": [
        ("What does roof tarping cost?",
         "It varies with the area to be covered, the roof pitch and height, the anchoring method the "
         "covering requires, and whether debris has to be removed first. A small single-slope cover on "
         "an accessible one-storey roof is at the low end; a large multi-plane cover on a steep "
         "two-storey tile roof with a limb to remove is considerably more. We give you a figure before "
         "work starts."),
        ("Does homeowners insurance cover emergency roof tarping?",
         "Usually, and most policies go further than that: they impose a duty on you to take reasonable "
         "steps to prevent further damage after a covered loss. Carriers can dispute the portion of a "
         "claim caused by water that entered after the event if nothing was done. Coverage specifics "
         "vary, so confirm with your carrier &mdash; and keep the invoice and photographs regardless."),
        ("How long does a roof tarp last?",
         "A standard poly tarp properly anchored is good for days to a few weeks, and UV is what kills "
         "it rather than wind. Heavy-duty UV-stabilised material installed with board-wrapped anchoring "
         "and re-tensioned periodically will run several months to around a year in Texas conditions. "
         "El Paso and West Texas are harder on material than the rest of the state."),
        ("Can I tarp my own roof?",
         "On a low, accessible single-storey roof in calm weather, some homeowners do it successfully. "
         "The risks are falls, further damage to the covering, and an anchoring job that does not hold "
         "&mdash; a tarp that comes off at 2am usually takes a course of shingles with it. If the roof "
         "is steep, tall, wet, tile, metal or structurally compromised, it is not a DIY job."),
        ("Do you have to put holes in my roof?",
         "Not always. On tile, slate and metal we use ballasted, no-penetration anchoring as standard, "
         "because a screw through those coverings creates a leak that outlives the tarp. On asphalt "
         "shingle, board-wrapped fastening is usually the most secure option and the holes are dealt "
         "with at repair &mdash; but if you would rather avoid penetration entirely, say so."),
        ("How quickly can you get here?",
         "We aim to be on site within hours of your call. Timing depends on distance, how many calls a "
         "storm has generated in that metro, and whether conditions are safe. We will not send a crew "
         "onto a roof during active lightning or high wind, and we will tell you if that is the "
         "situation rather than leave you waiting."),
        ("Can you tarp a roof while it is raining?",
         "Usually yes, and that is often exactly when it is needed. Steady rain is workable. Active "
         "lightning, high wind and ice are not. In those cases we schedule for the first safe window "
         "and talk you through interior containment in the meantime."),
        ("Should I wait for the insurance adjuster before tarping?",
         "No. Photograph the damage thoroughly first, then get it covered. Waiting typically makes the "
         "claim worse rather than better, because the additional water damage may not be covered."),
        ("Will a tarp stop the leak completely?",
         "A correctly installed cover stops water entering through the breach it covers. If there is a "
         "second failure point elsewhere on the roof, that needs covering too. It is also worth knowing "
         "that water already in the structure will continue to show up for a while after the roof is "
         "sealed &mdash; that is drying out, not a new leak."),
        ("What is the difference between an emergency tarp and a long-term one?",
         "Material and anchoring, driven by how long you need it. Under about two weeks, a standard "
         "tarp is appropriate and cost-effective. Beyond a month, UV degradation and repeated wind "
         "loading mean you need heavier UV-stabilised material and load-spreading anchors, or you will "
         "be paying for the job twice."),
        ("Do you work on commercial buildings?",
         "Yes. Flat and low-slope commercial roofs need a different method &mdash; ballasted anchoring "
         "rather than fasteners, and layout planned around drains and scuppers so the cover does not "
         "pond or block drainage. We schedule out of hours where daytime work would stop trading."),
        ("My roof was damaged months ago and is still not repaired. Is that a problem?",
         "It can be. Some carriers limit coverage if a damaged roof is left unprotected or unrepaired "
         "beyond a period, and the structure keeps degrading in the meantime. If the repair is genuinely "
         "months away, that is an argument for a properly specified long-term cover rather than leaving "
         "an emergency tarp to fail."),
    ],
}

CONTACT = {
    "path": "/contact/",
    "title": "Contact Roof Tarp | 24/7 Emergency Tarping | Roof Tarp",
    "description": (
        "Contact Roof Tarp for 24/7 emergency roof tarping across Texas. Call (956) 465-6045 or "
        "request a callback."
    ),
    "h1": 'Contact <span class="accent-text">Roof Tarp</span>',
    "h1_plain": "Contact Roof Tarp",
    "eyebrow": "Get In Touch",
    "body": f"""
<h2>If water is coming in right now, call</h2>
<p>Do not use the form. Call <a href="tel:{BIZ['phone_href']}">{PHONE}</a>. Dispatch is staffed 24
hours a day, seven days a week, including holidays, and a phone call gets a crew moving in a way a form
submission does not.</p>

<h2>What to have ready when you call</h2>
<p>None of this is essential, but it speeds things up considerably and helps us bring the right
equipment:</p>
<ul>
<li><strong>The property address</strong>, and anything unusual about access &mdash; a long private
drive, a gate code, a blocked road</li>
<li><strong>What happened</strong> &mdash; hail, wind, a fallen limb, or a leak with no obvious cause</li>
<li><strong>Roughly how big the damaged area is</strong>, even as a rough guess</li>
<li><strong>What the roof is covered with</strong> &mdash; asphalt shingle, tile, metal, or flat</li>
<li><strong>How many storeys</strong>, and how steep the roof is</li>
<li><strong>Whether anything is still on the roof</strong>, such as a tree or large debris</li>
<li><strong>Whether water is entering living space right now</strong></li>
</ul>

<h2>While you wait</h2>
<ol>
<li><strong>Stay off the roof.</strong> Wet, damaged roofing is the most dangerous place on the
property.</li>
<li><strong>Photograph everything</strong> from the ground, plus any interior damage, before moving or
cleaning anything up.</li>
<li><strong>Contain the water</strong> &mdash; containers under drips, furniture moved, belongings out
of the affected room.</li>
<li><strong>Cut power to affected circuits</strong> if water is near fixtures, ceiling fans or the
panel.</li>
<li><strong>If a ceiling is bulging</strong>, keep everyone out from under it. A trapped pocket of water
is heavy and ceilings fail without much warning.</li>
</ol>

<h2>Other ways to reach us</h2>
<p><strong>Phone:</strong> <a href="tel:{BIZ['phone_href']}">{PHONE}</a> &mdash; 24/7<br>
<strong>Dispatch:</strong> <a href="tel:{BIZ['dispatch_href']}">{BIZ['dispatch_display']}</a><br>
<strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a> &mdash; for non-urgent enquiries,
quotes and documentation requests</p>
<p>Email is fine for scheduling a non-urgent assessment, asking about long-term tarping, or requesting
copies of photographs and invoices for a claim. It is not the right channel for an active leak.</p>

<h2>Where we work</h2>
<p>Across Texas. See <a href="/service-areas/">service areas</a> for the metros we cover in detail. If
your town is not listed, call anyway &mdash; the list covers where we are asked most often, not the
limit of where we go.</p>
""",
}
