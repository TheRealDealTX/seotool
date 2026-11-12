# -*- coding: utf-8 -*-
"""Learning content for Maine Insurance Appraiser: process guide, FAQ,
glossary and owner guides (blog posts)."""

# ---------------------------------------------------------------------------
# Process guide (/the-appraisal-path/)
# ---------------------------------------------------------------------------

PROCESS_INTRO = """<h2>How a Maine appraisal actually moves</h2>
<p>Insurance appraisal is a dispute process written into most Maine homeowners, condo and commercial property policies. It exists for one narrow situation: the carrier has accepted the claim, but you and the carrier cannot agree on what the damage costs to repair or replace. Instead of arguing indefinitely, each side names its own appraiser, the two appraisers pick a neutral umpire, and the panel sets the amount of loss.</p>
<p>The seven steps below follow the order most appraisal clauses use. Policy wording varies from carrier to carrier, and a surplus lines policy on an oceanfront cottage may read differently than a standard homeowners form on a cape in Waterville, so treat this as a map rather than a rulebook. Keep your own policy open beside it, and talk to a Maine attorney about any legal question or deadline that comes up along the way.</p>
"""

PROCESS_STEPS = [
    (
        "Pin down the disagreement and read the clause",
        """<p>Appraisal only works when the fight is about money, not about whether the loss is covered. Confirm that the carrier has accepted the claim in writing and paid, or offered to pay, something. A denial, a reservation of rights or a dispute over what caused the damage is a different problem that a panel generally cannot resolve.</p>
<p>Then put the gap on paper and open your policy to the condition titled “Appraisal.” Check these points:</p>
<ul>
<li>Exactly which items, quantities and unit prices separate the two estimates</li>
<li>Who may demand appraisal and whether the demand must be in writing</li>
<li>How many days each side has to name an appraiser and choose an umpire</li>
<li>Who pays the appraisers and the umpire</li>
<li>Whether an endorsement changes the base wording or limits what the panel decides</li>
</ul>
<p>Surplus lines and commercial forms sometimes add extra steps. If anything is unclear, or a policy deadline is close, ask a Maine attorney before you send a demand.</p>""",
    ),
    (
        "Send a written demand",
        """<p>Once you understand the clause, put the demand in writing. A short letter or email to the adjuster is usually enough, and it should say plainly that you are invoking the appraisal provision of the policy because the parties disagree on the amount of loss.</p>
<p>A solid demand typically includes:</p>
<ul>
<li>Your name, the property address and the claim number</li>
<li>The date of loss and the type of damage</li>
<li>A sentence identifying the disagreement as one over amount, not coverage</li>
<li>The name and contact information of your appraiser, if you have chosen one</li>
</ul>
<p>Send it in a way you can prove, such as certified mail or email with a read receipt, and keep a copy. The date the carrier receives your demand often starts the clock for naming appraisers, so note it in a deadline tracker the same day.</p>""",
    ),
    (
        "Each side names its appraiser",
        """<p>Many policies give each party 20 days after the demand to select a competent and disinterested appraiser and tell the other side who it is. Your appraiser advocates for an accurate number on your behalf but should have no financial stake in the outcome beyond a fee agreed in advance.</p>
<p>When choosing an appraiser, look for:</p>
<ul>
<li>Hands-on knowledge of Maine construction, from cedar shingle capes to standing-seam roofs</li>
<li>Comfort reading and writing line-item estimates in the software carriers use</li>
<li>No prior relationship that could make them look interested, such as being your contractor</li>
<li>A written fee arrangement you understand before work begins</li>
</ul>
<p>The carrier will name its own appraiser, often someone who works on carrier-side files. That is normal. The two appraisers are expected to work toward a fair figure, and the umpire stands behind them if they cannot get there.</p>""",
    ),
    (
        "The appraisers agree on an umpire",
        """<p>After both appraisers are named, they choose a neutral umpire together. The umpire only becomes involved on items the two appraisers cannot settle, but having one in place early keeps the process moving and discourages stalling.</p>
<p>Umpires are often experienced estimators, contractors, engineers or retired adjusters. A good candidate is:</p>
<ul>
<li>Independent of both appraisers and both parties</li>
<li>Familiar with the type of loss, whether that is ice dam damage, a puffback or a commercial roof</li>
<li>Available within a reasonable time, which matters after a big storm</li>
</ul>
<p>If the appraisers cannot agree on an umpire within the time the policy sets, often 15 days, many policies allow either party to ask a court of record in the state where the property sits to appoint one. In Maine that typically means a Superior Court petition, which is a step to take with an attorney’s guidance.</p>""",
    ),
    (
        "Inspect, exchange estimates and reconcile",
        """<p>This is where most of the work happens. The two appraisers inspect the property, ideally together, and measure what needs measuring: roof squares, wall areas, flooring, trim and contents if they are part of the dispute. Each appraiser then prepares or refines an estimate and shares it with the other.</p>
<p>Reconciliation goes line by line. For each item, the appraisers ask:</p>
<ul>
<li>Is this repair actually needed because of the covered loss?</li>
<li>Is the quantity right?</li>
<li>Is the unit price realistic for this town and this season?</li>
<li>Does matching, code work or access cost belong here?</li>
</ul>
<p>Items they agree on are locked in. Many files settle at this stage without the umpire, because two knowledgeable people working from the same measurements usually close most of the gap. Disputed items go on a short list for the umpire, with each side’s figure and reasoning attached.</p>""",
    ),
    (
        "The umpire resolves what remains",
        """<p>The umpire reviews only the items the appraisers could not agree on. That may involve reading both estimates, looking at photos and reports, and sometimes visiting the property. The umpire then picks a figure for each disputed item, which may land on either side’s number or somewhere between.</p>
<p>The result is written into an appraisal award, usually a form listing the amount of loss and, where the policy calls for it, replacement cost and actual cash value figures. Under typical wording, an award signed by any two of the three panel members is binding on the amount of loss.</p>
<ul>
<li>The appraisers sign if they agree on every item</li>
<li>One appraiser and the umpire sign if the umpire breaks a deadlock</li>
<li>Each line on the award should be clear enough for the carrier to process payment</li>
</ul>""",
    ),
    (
        "Payment and the limits of an award",
        """<p>After the award is signed, the carrier calculates payment by applying the deductible, any prior payments and, if the policy pays actual cash value first, the depreciation holdback that you recover once repairs are done. Most policies require payment within a set number of days after the award, and Maine law separately addresses timely claim payment.</p>
<p>It helps to know what appraisal does not decide:</p>
<ul>
<li>Whether the loss is covered at all</li>
<li>Whether the carrier acted in bad faith, which is a legal claim</li>
<li>Policy interpretation questions, such as whether an exclusion applies</li>
</ul>
<p>Causation is a gray area. Some courts and policies let the panel decide how much damage a covered event caused, while others treat that as a coverage question. If the carrier pushes back on an award or raises coverage after it, talk to a Maine attorney about your options.</p>""",
    ),
]

PROCESS_OUTRO = """<h2>Mistakes that slow Maine appraisals down</h2>
<p>Most appraisal problems are avoidable. The ones we see most often have nothing to do with estimating skill and everything to do with timing and paperwork:</p>
<ul>
<li><strong>Demanding appraisal on a coverage fight.</strong> If the carrier says the loss is not covered, a panel will not fix that. Sort out coverage first, with an attorney if needed.</li>
<li><strong>Missing a policy deadline.</strong> Proof of loss dates, appraiser selection windows and the suit limitation period in your policy all keep running while you negotiate. Many policies set a suit limitation of one to two years, but read yours.</li>
<li><strong>Choosing an appraiser with a stake in the job.</strong> Your roofer may know the house best, but a contractor who expects to do the work is rarely disinterested.</li>
<li><strong>Arriving without photos and measurements.</strong> The panel works from evidence, and a file without dated photos or a measured scope is harder to win.</li>
</ul>
<h3>Maine timing realities</h3>
<p>Weather shapes every step here. A roof inspection in January may mean waiting for a thaw or working around two feet of snow, and damage that looks minor under snow can grow once the roof is bare in April. The construction season is short, and after a major nor’easter or windstorm, roofers and restoration crews can be booked for months, which pushes up prices and stretches repair timelines. Island and remote properties add ferry schedules and travel time to all of it.</p>
<p>Plan around those realities instead of fighting them. Track every policy date in the <a href="/claim-math/claim-date-tracker/">claim date tracker</a>, and before you send a demand, run your file through the <a href="/claim-math/appraisal-file-strength-test/">appraisal file strength test</a> to see where the gaps are.</p>
"""

# ---------------------------------------------------------------------------
# FAQ (/answers/)
# ---------------------------------------------------------------------------

FAQ = [
    (
        "Appraisal basics",
        [
            (
                "What is insurance appraisal in plain terms?",
                "It is a process in most property policies for settling a disagreement over how much a covered loss costs. Each side names an appraiser, the appraisers choose an umpire, and an award signed by two of the three sets the amount of loss.",
            ),
            (
                "When does appraisal make sense for a homeowner?",
                "It makes sense when the carrier has accepted the claim but its estimate is well below what repairs will really cost, and talking with the adjuster has stalled. It is not designed for denied claims or arguments over whether something is covered.",
            ),
            (
                "Can my insurance company demand appraisal too?",
                "Yes, many policies let either party invoke appraisal. If the carrier demands it, you will still name your own appraiser and the process runs the same way.",
            ),
            (
                "Is an appraisal award final?",
                "Under most policy wording, an award signed by any two panel members is binding on the amount of loss. It can sometimes be challenged in court for reasons like fraud or a panel member who was not disinterested, which is a question for an attorney.",
            ),
            (
                "How is appraisal different from a lawsuit?",
                "Appraisal decides only the dollar value of a covered loss and is usually faster and less formal than litigation. A lawsuit can address coverage, contract breaches and claim-handling conduct, which appraisal does not.",
            ),
        ],
    ),
    (
        "Cost, timing and paperwork",
        [
            (
                "Who pays for the appraisers and the umpire?",
                "Most policies say each side pays its own appraiser and the two sides split the umpire’s fee equally. Check the appraisal condition in your policy, since some forms differ.",
            ),
            (
                "How long does a typical appraisal take?",
                "Many residential appraisals wrap up within a few weeks to a few months after both appraisers are named. Winter access, umpire availability and the number of disputed items all affect the timeline.",
            ),
            (
                "What documents should I gather before demanding appraisal?",
                "Collect the full policy with declarations and endorsements, every carrier estimate and payment letter, your contractor estimates, dated photos and any reports from mitigation companies or engineers. A simple timeline of calls and emails with the adjuster also helps.",
            ),
            (
                "Do I still have to file a proof of loss?",
                "If your policy requires a sworn proof of loss, the requirement usually stays in place during appraisal. Read the deadline in your policy and meet it, and ask a Maine attorney if you are unsure how to complete it.",
            ),
            (
                "Can I keep negotiating with the adjuster during appraisal?",
                "Yes, nothing usually stops the parties from settling on their own at any point. Many files close during the appraisers’ reconciliation without the umpire ever ruling.",
            ),
        ],
    ),
    (
        "Maine rules and resources",
        [
            (
                "Who regulates insurance companies in Maine?",
                "The Maine Bureau of Insurance, part of the Department of Professional and Financial Regulation, oversees insurers and is headed by the Superintendent of Insurance. The Bureau accepts consumer complaints about claim handling.",
            ),
            (
                "Does Maine have a FAIR plan for hard-to-insure homes?",
                "No. Maine chose a market-assistance approach instead of a FAIR plan or state wind pool, so many older, vacant or oceanfront homes are insured through surplus lines carriers whose policy wording can differ from standard forms.",
            ),
            (
                "What Maine law covers unfair claim handling?",
                "Maine’s Unfair Claims Settlement Practices statute, 24-A M.R.S. section 2436-A, allows an insured to bring a civil action over certain claim-handling conduct by their own insurer. Courts apply it narrowly, and whether it fits your situation is a question for a Maine attorney, not an appraisal panel.",
            ),
            (
                "Does my homeowners policy cover flood damage?",
                "Standard homeowners policies exclude flood and storm surge. Flood coverage comes from a separate National Flood Insurance Program or private flood policy, and appraisal under a homeowners policy will not change that exclusion.",
            ),
            (
                "Is there a deadline to sue my insurance company in Maine?",
                "Most policies include a suit limitation clause, and many set a period of one to two years from the date of loss. Read your own policy and talk with a Maine attorney about how that clause and Maine law apply to your claim.",
            ),
        ],
    ),
    (
        "Winter and storm claims",
        [
            (
                "Are ice dam leaks covered by homeowners insurance?",
                "Interior water damage from an ice dam is commonly covered, though policies often exclude the cost of the ice dam itself or repairs tied to wear and maintenance. The scope of the interior damage is where many ice dam disputes land.",
            ),
            (
                "What if pipes froze at my seasonal camp while nobody was there?",
                "Many policies require you to keep heat on or drain the plumbing in an unoccupied building, and some limit coverage after a set number of days of vacancy. Review those conditions closely, since they may decide coverage before appraisal is even an option.",
            ),
            (
                "How do adjusters split wind and water after a nor’easter?",
                "Wind and wind-driven rain entering through storm-created openings are usually covered, while rising water and storm surge fall under the flood exclusion. When both happen at once, the dispute often turns on which damage came from which source.",
            ),
            (
                "Will my policy pay to remove a fallen tree?",
                "Policies typically pay to remove a tree that damaged a covered structure, often with a dollar cap per tree and per loss. A tree that fell without hitting anything covered may not qualify for removal coverage.",
            ),
            (
                "Can a winter roof inspection be accurate?",
                "An inspection under snow can miss lifted shingles, cracked flashing and soft decking. If the roof is buried, it is reasonable to ask for a follow-up inspection after the thaw before the scope is finalized.",
            ),
        ],
    ),
    (
        "Working with our practice",
        [
            (
                "How are your fees set?",
                "We put every fee arrangement in writing before work starts, so you know the cost and how it is calculated. We will talk through the options on a first call.",
            ),
            (
                "What do you need from me to review a claim?",
                "Send the policy declarations and appraisal condition, the carrier’s estimate and payment letters, any contractor estimates and your photos. That is usually enough for an initial read on whether appraisal fits.",
            ),
            (
                "Can you serve as an umpire instead of a party appraiser?",
                "Yes, we can be considered for umpire roles when we have no connection to either party or appraiser. We do not act as both appraiser and umpire on the same claim.",
            ),
            (
                "Do you give legal advice?",
                "No. We are an appraisal practice, not a law firm or a public adjuster, so questions about coverage, bad faith or legal deadlines should go to a Maine attorney.",
            ),
            (
                "Do you work on island and rural properties?",
                "Yes, we work statewide across all 16 counties, including ferry-served islands and remote camps. Access logistics are planned into the inspection schedule.",
            ),
        ],
    ),
]

# ---------------------------------------------------------------------------
# Glossary (/plain-english-glossary/)
# ---------------------------------------------------------------------------

_GLOSSARY = [
    ("Actual cash value", "The value of damaged property after depreciation is subtracted from its replacement cost. Many policies pay this amount first and the rest once repairs are complete."),
    ("Additional living expense", "Coverage for the extra costs of living elsewhere while your home is unlivable after a covered loss, such as rent, meals and mileage above your normal spending."),
    ("Appraisal award", "The written decision of an appraisal panel stating the amount of loss. Under typical wording it is binding on amount once signed by any two of the three panel members."),
    ("Appraisal clause", "The policy condition that lets either party ask for a panel to settle a disagreement over the amount of a covered loss."),
    ("Bureau of Insurance", "The Maine state agency, within the Department of Professional and Financial Regulation, that regulates insurers and takes consumer complaints about claim handling."),
    ("Cedar shingle", "A wood roofing or siding material common on older Maine capes and coastal cottages. Repair estimates often turn on matching weathered shingles and the higher labor involved."),
    ("Coverage A", "The part of a homeowners policy that covers the dwelling itself, including attached structures like a connected garage or ell."),
    ("Coverage B", "The part of a homeowners policy that covers other structures on the property not attached to the house, such as a detached barn, shed or fence."),
    ("Coverage C", "The part of a homeowners policy that covers personal property, meaning the contents you own such as furniture, clothing and tools."),
    ("Coverage D", "The part of a homeowners policy that covers loss of use, usually additional living expense or lost rental income while the home cannot be lived in."),
    ("Declarations page", "The summary page of a policy listing the insured, the property, coverage limits, deductibles and the policy period."),
    ("Deductible", "The portion of a covered loss you pay before the policy pays. It is usually a flat dollar amount but can be a percentage for some perils."),
    ("Depreciation", "A reduction in value for age, wear and condition, subtracted from replacement cost to arrive at actual cash value."),
    ("Disinterested appraiser", "An appraiser with no financial stake in the outcome of the claim beyond an agreed fee and no relationship that would bias the result. Most appraisal clauses require it."),
    ("Ell", "A wing attached to a Maine farmhouse, often part of the connected big house, little house, back house and barn layout. Damage to an ell is usually covered as part of the dwelling."),
    ("Freeze exclusion", "A policy provision denying coverage for frozen pipe damage unless the owner kept heat on or drained the plumbing and shut off the water. Also called a heat-maintenance condition."),
    ("Holdback", "The depreciation a carrier withholds from an initial payment until repairs or replacement are completed, under a replacement cost policy."),
    ("Ice and water shield", "A self-sealing waterproof membrane installed under roofing along eaves and valleys to stop water backed up by ice dams. Building codes in cold climates often require it at the eaves."),
    ("Ice dam", "A ridge of ice that forms at the roof edge when melting snow refreezes, causing water to back up under shingles and into ceilings and walls."),
    ("Line item", "A single entry in a repair estimate that describes one task or material, with a quantity, unit and price."),
    ("Matching", "The question of whether undamaged materials must be replaced so repairs look uniform, for example when a discontinued siding color cannot be matched."),
    ("Mitigation", "The steps taken right after a loss to prevent further damage, such as tarping a roof, extracting water or running dehumidifiers. Most policies require reasonable mitigation."),
    ("Named storm deductible", "A separate deductible that applies when damage comes from a named storm or hurricane, often set as a percentage of the dwelling limit. Also called a percentage deductible."),
    ("Ordinance or law coverage", "Coverage for the added cost of bringing repaired parts of a building up to current building codes, usually limited to a percentage of the dwelling limit."),
    ("Overhead and profit", "The general contractor’s charge for coordinating trades and running the job, commonly figured as a percentage added to an estimate when several trades are needed."),
    ("Proof of loss", "A sworn statement of the amount claimed that many policies require within a set time after the carrier asks for it."),
    ("Puffback", "A misfire in an oil burner that blows soot and smoke through the furnace, ductwork and living space. Cleanup can reach every surface in the house."),
    ("Recoverable depreciation", "Depreciation that a replacement cost policy pays back once repairs or replacement are completed and documented."),
    ("Replacement cost value", "The cost to repair or replace damaged property with materials of like kind and quality, without subtracting depreciation."),
    ("Scope of loss", "The list of damaged items and the repairs needed for each, which forms the basis of an estimate."),
    ("Square", "A roofing unit equal to 100 square feet of roof surface. Estimates count roofing in squares, plus a waste allowance."),
    ("Standing-seam metal roof", "A metal roof with raised interlocking seams, common in Maine snow country because it sheds snow well. Repairs often involve whole panels rather than small patches."),
    ("Steep charge", "An added labor charge for working on roofs above a certain pitch, reflecting the extra safety gear and time steep slopes demand."),
    ("Storm surge", "Coastal flooding pushed ashore by a storm’s winds. It is treated as flood and excluded under standard homeowners policies."),
    ("Supplement", "A request for additional payment after the first estimate, usually because hidden damage was found or items were missed."),
    ("Surplus lines carrier", "An insurer not licensed as a standard admitted carrier in the state but allowed to write coverage that the standard market will not. Many hard-to-place Maine homes are insured this way."),
    ("Umpire", "The neutral third member of an appraisal panel, chosen by the two appraisers, who decides items they cannot agree on."),
    ("Unoccupancy", "A condition where a building is furnished but nobody is living in it, such as a seasonal camp in winter. Some policies limit certain coverages after a set period of unoccupancy."),
    ("Vacancy clause", "A policy provision that limits or removes coverage for some perils when a building has been empty of people and most belongings for a stated period, often 30 or 60 days."),
    ("Wind-driven rain", "Rain forced into a building by high winds. Policies often cover it only when wind first creates an opening in the roof or walls."),
    ("Xactimate", "Estimating software widely used by insurance carriers and adjusters to price repairs line by line using regional price lists."),
]

GLOSSARY = sorted(_GLOSSARY, key=lambda t: t[0].lower())

# ---------------------------------------------------------------------------
# Owner guides (/owner-guides/<slug>/)
# ---------------------------------------------------------------------------

POSTS = [
    {
        "slug": "ice-dam-claims-maine-estimates",
        "title": "Ice Dam Claims in Maine: Why the First Estimate Runs Short",
        "seo": "Ice Dam Claims in Maine: Estimate Gaps",
        "desc": "Why ice dam claims in Maine often come back underpaid, which line items carriers miss, and how to document hidden water damage after the thaw.",
        "keyword": "ice dam claims Maine",
        "date": "2026-09-16",
        "read": "8 min",
        "summary": "Ice dam claims in Maine tend to grow after the first inspection. Here is where estimates fall short and how to build a file that shows the full damage.",
        "body": """<h2>Why ice dam claims in Maine get underestimated</h2>
<p>Ice dam claims in Maine have a timing problem built into them. Ice dams don’t announce themselves. The water shows up in a closet ceiling in February, weeks after the dam formed, and by the time an adjuster visits, the roof is under snow and the wet insulation is hidden behind drywall. The first estimate is written from what can be seen that day, which is rarely everything.</p>
<p>That gap between visible and actual damage is the single biggest reason ice dam claims come back short. A stained ceiling patch and a few feet of repainting may be all that makes it into the first estimate, while soaked cellulose, swollen subfloor and mold-prone framing stay out of view.</p>
<h2>Where the water actually goes</h2>
<p>Meltwater backed up behind an ice dam travels under shingles and follows gravity and framing. In a typical Maine cape, that often means it runs into the knee walls and down into the first-floor exterior walls. In connected farmhouses, it can travel along the joint between the main house and the ell.</p>
<h3>Commonly missed areas</h3>
<ul>
<li>Insulation in the attic eaves and knee-wall spaces, which loses value once wet</li>
<li>Exterior wall cavities below the eave, where water sits behind plaster or drywall</li>
<li>Window and door trim that swells or stains weeks later</li>
<li>Hardwood flooring that cups slowly after water seeps from the walls</li>
<li>Electrical boxes and fixtures in wet ceilings that need inspection</li>
</ul>
<h3>Roof items carriers dispute</h3>
<p>Many policies exclude the ice dam itself and wear or maintenance issues, but a roof section torn open to reach interior damage, or shingles damaged by the dam, may still belong in the scope. Ice and water shield is a frequent sticking point. Where code requires it at the eaves on any reroofing, leaving it out of the estimate understates the true repair.</p>
<h2>Building a file that shows the full loss</h2>
<p>The strongest ice dam claims are documented in layers, starting the day the leak appears and continuing through the thaw. Here is what helps most:</p>
<ol>
<li>Photograph the ceiling stains, the ice along the eaves and any icicles inside soffits, with dates.</li>
<li>Record moisture readings from a mitigation company, not just a visual inspection.</li>
<li>Keep invoices for roof raking, steaming and emergency tarping, since mitigation is usually part of the claim.</li>
<li>Ask for a follow-up inspection once the roof is clear of snow.</li>
<li>Get a contractor estimate that lists each room and surface, not a single lump sum.</li>
</ol>
<div class="note"><b class="h">Snow hides roof damage</b><p>A Maine claim that looks small in March can look very different once the snow is off the roof. If the carrier inspected in midwinter, put a written request for a spring reinspection in the file before you accept any final figure.</p></div>
<h2>Reading the carrier’s estimate line by line</h2>
<p>When the estimate arrives, compare it room by room against what you know is wet. Look at each line item’s quantity and unit. Drywall should be measured by square foot for the full affected area, not just the stained patch. Painting usually needs to cover the whole wall or ceiling plane to look right.</p>
<p>Check whether the estimate includes overhead and profit when several trades are involved, such as drywall, insulation, painting and flooring together. Check whether depreciation on paint and drywall seems reasonable for the age of the surfaces. Our <a href="/appraisal-work/carrier-estimate-line-review/">carrier estimate line review</a> covers this in detail.</p>
<p><strong>Illustrative example:</strong> suppose a carrier estimate for a two-story colonial in Bangor covers one bedroom ceiling at $1,900. After the thaw, moisture readings show the wall below and the closet are also wet, and a contractor scope including insulation, drywall, trim, paint and a section of hardwood comes to $9,400. The numbers are hypothetical, but the pattern of a modest first estimate growing several times over is common with ice dam losses.</p>
<h2>When ice dam claims in Maine go to appraisal</h2>
<p>If the carrier has accepted the loss but will not move on the scope or pricing, appraisal is often the right next step. The panel can look at the moisture data, the photos and both estimates and decide what the repair really costs. It cannot decide whether the policy covers the ice dam itself, which remains a coverage question for the carrier and, if needed, a Maine attorney.</p>
<p>Before you demand appraisal, read our guide to <a href="/appraisal-work/ice-dam-snow-load-appraisal/">ice dam and snow load appraisal</a>, and track every policy date in the <a href="/claim-math/claim-date-tracker/">claim date tracker</a>. Ice dam claims in Maine reward patience and good records more than almost any other winter loss.</p>
""",
    },
    {
        "slug": "maine-appraisal-clause-plain-reading",
        "title": "The Maine Appraisal Clause: A Plain Reading, Sentence by Sentence",
        "seo": "Maine Appraisal Clause: A Plain Reading",
        "desc": "A sentence-by-sentence plain reading of the appraisal clause in Maine property policies: who can demand it, the 20-day window, umpires and awards.",
        "keyword": "Maine appraisal clause",
        "date": "2026-09-29",
        "read": "8 min",
        "summary": "A plain-language walk through the appraisal clause found in most Maine property policies, with the questions to ask at each sentence.",
        "body": """<h2>What the Maine appraisal clause is for</h2>
<p>The Maine appraisal clause is the short paragraph in your property policy that gives you and the carrier a way out of a stalemate over money. It is not a Maine statute. It is contract language, and most carriers writing in Maine use some version of the standard homeowners form wording. Surplus lines carriers, which insure many older, vacant and oceanfront homes here, may use their own versions.</p>
<p>Because it is contract language, the exact words in your policy control. What follows is a plain reading of the typical clause, sentence by sentence, with the questions worth asking at each step. Keep your own policy open while you read, and ask a Maine attorney about anything that affects a deadline or your legal rights.</p>
<h2>Sentence one: the trigger</h2>
<p>Most clauses open with something like: if you and we fail to agree on the amount of loss, either may demand an appraisal of the loss. Three ideas sit in that sentence.</p>
<ul>
<li><strong>Fail to agree</strong> means there must be a real disagreement, usually shown by competing estimates and some back and forth.</li>
<li><strong>Amount of loss</strong> limits appraisal to value, not coverage.</li>
<li><strong>Either may demand</strong> means the carrier can invoke it too, not just you.</li>
</ul>
<p>Some versions add that the demand must be in writing. Even when it is not required, a written demand is the safer choice.</p>
<h2>Sentence two: choosing appraisers</h2>
<p>The next sentence usually says each party will choose a competent and disinterested appraiser within 20 days after receiving a written request from the other. That is the wording in many policies, but some use different windows.</p>
<h3>What competent and disinterested mean</h3>
<p>Competent means the appraiser understands construction, estimating and the kind of damage involved. Disinterested means no financial stake in the result beyond an agreed fee and no relationship that would bias them. Courts in various states have looked at contingency fees and prior relationships when deciding whether an appraiser was truly disinterested, so ask any appraiser you consider how they charge and whether they have worked on your property before.</p>
<h2>Sentence three: the umpire</h2>
<p>Next, the two appraisers choose an umpire. If they cannot agree within a set time, often 15 days, many policies allow either party to request that a judge of a court of record in the state where the property is located select one. In Maine, that request would generally go to the Superior Court, and an attorney should handle it.</p>
<div class="note"><b class="h">Watch the clock</b><p>The 20-day and 15-day windows in many policies run from specific events, such as receipt of the written demand. Write down the date each step happens. Our <a href="/claim-math/claim-date-tracker/">claim date tracker</a> can export those dates to your calendar.</p></div>
<h2>Sentence four: the award</h2>
<p>The clause then explains that the appraisers will separately set the amount of loss. If they submit a written report of an agreement, that amount becomes the amount of loss. If they fail to agree, they submit their differences to the umpire, and a decision agreed to by any two will set the amount of loss.</p>
<h3>Why the award format matters</h3>
<p>Many policies ask the panel to state both replacement cost and actual cash value. If your policy pays actual cash value first, the difference is the depreciation holdback you can recover after repairs. A clear award that breaks out these figures by line or category makes payment easier and leaves less room for later disputes. Use our <a href="/claim-math/rcv-acv-holdback-calculator/">RCV, ACV and holdback calculator</a> to see how the pieces fit.</p>
<h2>Sentence five: fees and the fine print</h2>
<p>Most clauses close by saying each party pays its own appraiser and the parties share the umpire’s fee and other appraisal expenses equally. Some policies add one more sentence that matters a great deal: that the carrier keeps its right to deny the claim even after an appraisal.</p>
<p>That line reflects a basic rule of appraisal. The panel decides how much, not whether. If coverage is still in question, the award does not settle it. Bad faith claims under Maine’s Unfair Claims Settlement Practices statute, 24-A M.R.S. § 2436-A, also sit outside the panel’s job and belong with an attorney.</p>
<h3>Putting the Maine appraisal clause to work</h3>
<p>Reading the Maine appraisal clause carefully before you act saves time later. Confirm the claim is accepted, list the disputed items, note every deadline and choose an appraiser who is both competent and disinterested. If you want help deciding whether your file is ready, our <a href="/appraisal-work/party-appraiser-representation/">party appraiser representation</a> page explains how we work on the insured’s side of the panel.</p>
<p><strong>Illustrative example:</strong> a condo association in Scarborough receives a carrier estimate of $48,000 for wind damage to a building’s siding and trim, against a contractor figure of $86,000. The board sends a written demand, names its appraiser within the policy window, and the two appraisers agree on most items. The umpire decides four remaining line items. These figures are illustrative only, but they show how the clause channels a large gap into a short list of disputed items.</p>
""",
    },
    {
        "slug": "seasonal-camp-vacancy-freeze-claims",
        "title": "Seasonal Camp Freeze Claims: Vacancy, Heat and What Gets Paid",
        "seo": "Seasonal Camp Freeze Claims in Maine",
        "desc": "How vacancy, unoccupancy and heat-maintenance conditions shape seasonal camp freeze claims in Maine, and how to document a burst pipe loss well.",
        "keyword": "seasonal camp freeze claims",
        "date": "2026-10-08",
        "read": "8 min",
        "summary": "Seasonal camp freeze claims often turn on vacancy and heat conditions before the amount of loss is ever discussed. Here is how to read those terms and document the loss.",
        "body": """<h2>Why seasonal camp freeze claims are different</h2>
<p>Seasonal camp freeze claims are among the most common winter losses in Maine and among the most argued. A camp on a lake in Oxford or Piscataquis County sits empty from Columbus Day to Memorial Day. A power outage or a failed furnace in January goes unnoticed for weeks, a pipe splits, and water runs until a neighbor or a plow driver sees ice on the windows.</p>
<p>Unlike most losses, the first fight in these claims is often about coverage rather than dollars. Vacancy clauses, unoccupancy limits and heat-maintenance conditions can decide whether the policy pays at all. Only once that is settled does the size of the check become the question.</p>
<h2>The policy conditions that matter</h2>
<p>Three kinds of policy language come up again and again in seasonal camp freeze claims.</p>
<h3>Heat-maintenance or freeze conditions</h3>
<p>Many homeowners and seasonal dwelling policies exclude freezing damage to plumbing unless you either maintained heat in the building or shut off the water supply and drained the system and appliances. Some policies require both a working heat source and monitoring, such as a low-temperature alarm.</p>
<h3>Vacancy and unoccupancy</h3>
<p>Vacancy usually means the building is empty of people and most belongings. Unoccupancy means furnished but nobody living there, which describes most camps in winter. Some policies limit coverage for certain perils, including freezing, after a set number of days in either state. Seasonal dwelling forms are often written with this use in mind, which is one reason it matters what form you actually have.</p>
<h3>Surplus lines wording</h3>
<p>Because Maine has no FAIR plan, many remote or older camps are insured through surplus lines carriers. Their forms can add unique conditions, such as requiring a caretaker visit every set number of days. Read every endorsement.</p>
<div class="note"><b class="h">Check before winter, not after</b><p>Our <a href="/claim-math/seasonal-camp-vacancy-check/">seasonal camp vacancy check</a> walks through the vacancy, unoccupancy and freeze-protection questions so you can see where your camp stands before the first hard freeze.</p></div>
<h2>Documenting a burst pipe loss</h2>
<p>If the carrier accepts coverage, the amount of loss is the next battle, and the evidence you gather early does most of the work.</p>
<ul>
<li>Photograph the burst fitting, the frozen lines and any ice inside before anything is removed.</li>
<li>Keep fuel delivery receipts, propane tank readings or electric bills that show heat was on.</li>
<li>Save caretaker logs, alarm system records and smart thermostat history.</li>
<li>Get moisture mapping from a mitigation company, including subfloor and crawlspace readings.</li>
<li>Save the failed pipe section or fitting, since a plumber or engineer may want to examine it.</li>
</ul>
<h2>Where camp estimates run short</h2>
<p>Carrier estimates for seasonal camps often miss costs tied to location and season.</p>
<ul>
<li><strong>Access.</strong> Camps on unplowed roads or reachable only by boat or snowmobile in winter carry real access costs.</li>
<li><strong>Drying time.</strong> Unheated buildings dry slowly, and temporary heat may be needed to dry them at all.</li>
<li><strong>Older materials.</strong> Knotty pine paneling, wide pine floors and beadboard ceilings are hard to match.</li>
<li><strong>Contractor travel.</strong> Crews may need to travel an hour or more each way to reach a remote lake.</li>
<li><strong>Plumbing and systems.</strong> Water heaters, pumps and pressure tanks that froze are often part of the loss.</li>
</ul>
<p><strong>Illustrative example:</strong> a carrier estimate for a burst pipe at a Rangeley-area camp covers kitchen drywall and a section of vinyl floor at $7,200. The owner’s contractor adds wet knotty pine paneling, a replaced pressure tank, temporary heat for drying and winter access by plowing, for a total of $18,600. The figures are made up for illustration, but camp losses often widen this way once location costs are counted.</p>
<h2>When appraisal fits a seasonal camp freeze claim</h2>
<p>Appraisal fits seasonal camp freeze claims once the carrier has accepted coverage and the disagreement is over scope or price. It will not resolve a denial based on a heat or vacancy condition. That is a coverage dispute, and a Maine attorney is the right person to review it.</p>
<p>If coverage is accepted and you think the numbers are short, our <a href="/appraisal-work/water-damage-loss-appraisal/">water damage loss appraisal</a> page explains how we approach freeze losses. Keep the dates of the loss, the discovery and every payment in one place, and read your policy’s suit limitation clause, which in many policies runs one to two years. Seasonal camp freeze claims reward early, careful records.</p>
""",
    },
    {
        "slug": "noreaster-wind-versus-flood-maine",
        "title": "Nor’easter Damage in Maine: Sorting Wind From Flood on a Claim",
        "seo": "Nor’easter Wind vs Flood Damage in Maine",
        "desc": "How carriers split nor’easter wind and flood damage in Maine, what the flood exclusion means, and how to document wind damage when water also rose.",
        "keyword": "nor’easter wind versus flood",
        "date": "2026-10-20",
        "read": "8 min",
        "summary": "When a nor’easter brings wind, rain and surge at once, the claim turns on sorting wind from flood. Here is how that split works and how to document it.",
        "body": """<h2>The nor’easter wind versus flood problem</h2>
<p>The nor’easter wind versus flood question is the heart of most coastal storm claims in Maine. A big nor’easter brings three forces at once: sustained wind, wind-driven rain and coastal surge. The January 10 and 13, 2024 storms showed this clearly, with a record tide at the Portland gauge, flooded waterfronts from Camp Ellis to Rockland and wind damage well inland.</p>
<p>Homeowners policies generally cover wind and exclude flood. When both hit the same building, the carrier has to decide which damage came from which source, and that decision drives the check.</p>
<h2>What the flood exclusion usually says</h2>
<p>Standard homeowners policies exclude flood, surface water, waves, tidal water and storm surge, whether or not driven by wind. Many include anti-concurrent causation language that tries to exclude damage when an excluded cause like flood combines with a covered cause like wind. How courts read that language varies, and it is a legal question for a Maine attorney.</p>
<p>Flood coverage comes from a separate National Flood Insurance Program policy or a private flood policy. If you have one, you may have two claims, two adjusters and two sets of rules for the same storm.</p>
<h2>What wind damage typically looks like</h2>
<p>Wind damage tends to show up high on the building and in patterns tied to wind direction.</p>
<ul>
<li>Missing or creased shingles, lifted ridge caps and torn underlayment</li>
<li>Siding and trim pulled off on the windward side</li>
<li>Broken windows and doors from debris</li>
<li>Fallen trees and limbs on roofs, decks and outbuildings</li>
<li>Interior water stains from rain entering through wind-created openings</li>
</ul>
<h3>Wind-driven rain</h3>
<p>Many policies only cover rain damage inside the house if wind or hail first created an opening in the roof or walls. Rain pushed through an intact window frame may be treated differently. That distinction matters a lot after a long nor’easter with hours of sideways rain.</p>
<h2>Separating wind from flood on paper</h2>
<p>Clear evidence is the best tool for keeping wind damage from being folded into an excluded flood loss.</p>
<ol>
<li>Photograph the high-water line inside and outside, with a tape measure for scale.</li>
<li>Photograph roof, siding and window damage above that line separately.</li>
<li>Note the time water rose and the time wind damage happened, if you saw either.</li>
<li>Keep weather reports, tide gauge data and local news coverage of the storm.</li>
<li>Ask contractors to separate wind items from flood items in their estimates.</li>
</ol>
<div class="note"><b class="h">Two policies, two files</b><p>If you carry flood coverage, keep separate folders, photos and estimates for each policy. Overlap is where payments get delayed, and a clean split helps both adjusters do their jobs.</p></div>
<h2>Where wind estimates fall short after a nor’easter</h2>
<p>Even when the carrier accepts wind damage, the estimate often understates it. Common gaps include roof sections priced as patches when the shingles cannot be matched, siding on one elevation priced without matching the rest, and interior water damage assigned to flood when it came through the roof.</p>
<p>After a big storm, Maine contractor availability also matters. Roofers along the coast can be booked for months, and prices climb with demand. An estimate written with pre-storm pricing may not reflect what it costs to get the work done that season.</p>
<p><strong>Illustrative example:</strong> an oceanfront cottage in York takes on two feet of surge in the basement and loses a large section of roof shingles and a band of cedar siding. The homeowners carrier estimates the wind damage at $11,000, attributing interior ceiling stains to flood. The owner’s contractor estimates $27,500, separating the roof leak damage from the basement flooding and adding matching for the siding. The numbers are invented for illustration only.</p>
<h2>When the dispute is over amount, appraisal can help</h2>
<p>Appraisal works when the carrier accepts that wind caused some damage and the disagreement is over how much. The panel can sort line items and decide what the wind repairs cost. Whether the flood exclusion or anti-concurrent causation language bars part of the loss is a coverage question, and some panels and courts treat causation disputes differently, so get a Maine attorney’s view on that piece.</p>
<p>Our <a href="/appraisal-work/noreaster-hurricane-appraisal/">nor’easter and hurricane appraisal</a> page covers how we approach these files. If trees came down too, see <a href="/appraisal-work/fallen-tree-limb-appraisal/">fallen tree and limb appraisal</a>. Getting the nor’easter wind versus flood split right on paper is often worth more than any argument made later.</p>
""",
    },
    {
        "slug": "appraiser-adjuster-or-lawyer-maine",
        "title": "Appraiser, Adjuster or Lawyer in Maine: Matching Help to the Problem",
        "seo": "Appraiser, Adjuster or Lawyer in Maine?",
        "desc": "When a Maine property claim needs an appraiser, a public adjuster or a lawyer, what each one does, how they are paid and where their roles overlap.",
        "keyword": "appraiser adjuster or lawyer Maine",
        "date": "2026-10-29",
        "read": "8 min",
        "summary": "An appraiser, a public adjuster and a lawyer each solve a different claim problem. This guide helps Maine owners match the help to the dispute.",
        "body": """<h2>Three kinds of help for three kinds of problems</h2>
<p>Choosing between an appraiser, adjuster or lawyer in Maine starts with naming the problem. Is the carrier refusing to pay at all, or paying too little? Do you need someone to manage the whole claim, or just to fight about the number? Each professional fits a different answer.</p>
<p>This guide explains what each one does, how each is typically paid and where their work overlaps. It is general information, and the right choice depends on your policy and your claim. For any legal question or deadline, talk to a Maine attorney.</p>
<h2>The party appraiser</h2>
<p>A party appraiser works within the appraisal clause of your policy. Once appraisal is invoked, your appraiser inspects the loss, builds or reviews the estimate, negotiates line items with the carrier’s appraiser and, if needed, presents disputed items to the umpire.</p>
<h3>When an appraiser fits</h3>
<ul>
<li>The carrier has accepted the claim in writing</li>
<li>The dispute is over scope, quantities or pricing</li>
<li>Negotiation with the adjuster has stalled</li>
</ul>
<p>An appraiser does not decide coverage, give legal advice or manage the claim from start to finish. The role is narrow by design, which is part of why appraisal can move faster than a lawsuit.</p>
<h2>The public adjuster</h2>
<p>A public adjuster is hired by the policyholder to prepare, present and negotiate the whole claim with the carrier. In Maine, public adjusters are regulated by the Bureau of Insurance. They often step in early, sometimes right after the loss, and handle documentation, estimates and communication.</p>
<h3>When a public adjuster fits</h3>
<ul>
<li>You want someone to manage the claim from day one</li>
<li>The loss is large or complex, such as a fire or a commercial building</li>
<li>You do not have time to gather documents and deal with the carrier yourself</li>
</ul>
<p>Public adjusters are commonly paid a percentage of the claim payment, and the terms should be in a written contract.</p>
<h2>The attorney</h2>
<p>A Maine attorney handles the legal side: coverage disputes, denials, policy interpretation, bad faith claims and lawsuits. If the carrier has denied the claim, invoked an exclusion or is relying on a vacancy or heat condition, an attorney is usually the right first call.</p>
<h3>When an attorney fits</h3>
<ul>
<li>The claim was denied, or coverage is disputed</li>
<li>A suit limitation deadline is approaching</li>
<li>You believe the carrier handled the claim unfairly, which may raise questions under 24-A M.R.S. § 2436-A</li>
<li>The carrier is challenging an appraisal award</li>
</ul>
<h2>Side by side</h2>
<div class="table-wrap"><table>
<thead><tr><th>Question</th><th>Party appraiser</th><th>Public adjuster</th><th>Attorney</th></tr></thead>
<tbody>
<tr><td>Main job</td><td>Set the amount of loss through the appraisal clause</td><td>Prepare and negotiate the full claim</td><td>Handle coverage, legal rights and litigation</td></tr>
<tr><td>Best timing</td><td>After the claim is accepted and the amount is disputed</td><td>Early, often soon after the loss</td><td>At a denial, coverage dispute or approaching deadline</td></tr>
<tr><td>Decides coverage?</td><td>No</td><td>No, but argues the claim</td><td>Advises on it and can litigate it</td></tr>
<tr><td>Legal advice?</td><td>No</td><td>No</td><td>Yes</td></tr>
<tr><td>Typical pay</td><td>Agreed in writing, varies by practice</td><td>Often a percentage of payments</td><td>Hourly or contingency, agreed in writing</td></tr>
</tbody>
</table></div>
<div class="note"><b class="h">Roles can overlap</b><p>A public adjuster may recommend appraisal and help choose an appraiser. An attorney may advise on a demand letter while the appraiser handles the estimate. Just make sure everyone knows who is doing what, and that your appraiser stays disinterested.</p></div>
<h2>Matching help to your claim</h2>
<p>Start by reading the carrier’s latest letter. If it says the loss is covered and offers a payment, the problem is probably the amount, and an appraiser may be enough. If it denies the claim or reserves rights, start with an attorney. If you are early in a large loss and overwhelmed, a public adjuster may help organize the file.</p>
<p><strong>Illustrative example:</strong> a Lewiston triple-decker owner receives $22,000 for fire and smoke damage after the carrier accepts coverage, while contractor estimates total $61,000. There is no coverage dispute, so the owner considers appraisal. Had the carrier instead denied the smoke portion as pre-existing, the first call would go to an attorney. These figures are illustrative only.</p>
<p>To test whether your file is ready for appraisal, try the <a href="/claim-math/appraisal-file-strength-test/">appraisal file strength test</a>. To estimate the size of the gap and the likely fees, use the <a href="/claim-math/settlement-gap-projector/">settlement gap projector</a>. And for how we work as a party appraiser, see <a href="/our-approach/">our approach</a>. Picking the right appraiser, adjuster or lawyer in Maine early saves time and money on the back end.</p>
""",
    },
    {
        "slug": "oil-burner-puffback-documentation",
        "title": "Oil Burner Puffback Claims: How to Document Soot Damage Well",
        "seo": "Oil Burner Puffback: Documenting Soot Loss",
        "desc": "How to document an oil burner puffback in Maine: soot testing, contents, HVAC cleaning and the estimate items carriers most often leave out.",
        "keyword": "oil burner puffback",
        "date": "2026-11-09",
        "read": "8 min",
        "summary": "An oil burner puffback can coat a whole house in soot within seconds. This guide covers documentation, cleaning scope and where carrier estimates run short.",
        "body": """<h2>What an oil burner puffback does to a house</h2>
<p>An oil burner puffback is a misfire inside the furnace or boiler that pushes soot and oily smoke out through the burner, the flue and often the ductwork. Maine relies heavily on heating oil, with roughly six in ten homes using it, so puffbacks are a familiar winter loss here. They tend to happen on the first cold mornings of the season or after a service visit.</p>
<p>Puffback soot is fine, greasy and travels far. It can coat walls, ceilings, carpets, clothing in closed closets and the inside of ducts on every floor. Because a light film is hard to see, the full extent of the damage often goes undocumented.</p>
<h2>First steps after a puffback</h2>
<p>Safety comes first. Shut the burner down and have a licensed oil technician inspect it before it runs again. Then start documenting before anything is cleaned.</p>
<ol>
<li>Photograph the boiler room, the flue pipe and soot around registers in each room.</li>
<li>Wipe a white cloth on walls, ceilings and furniture in every room and photograph the result.</li>
<li>Note any odor, even in rooms without visible soot.</li>
<li>Keep the technician’s service report and any invoice for the repair.</li>
<li>Call the carrier promptly and ask about emergency cleaning approval.</li>
</ol>
<h3>Testing and the cleaning protocol</h3>
<p>Some puffbacks call for a written cleaning protocol or surface testing, particularly in larger homes or where occupants have health concerns. A restoration company or industrial hygienist can document how far the soot traveled. That report often becomes the backbone of the scope.</p>
<h2>What a full puffback scope includes</h2>
<p>A thorough oil burner puffback scope usually covers more than walls and ceilings.</p>
<ul>
<li><strong>Structure cleaning</strong> of walls, ceilings, trim, windows and fixtures in every affected room</li>
<li><strong>Sealing and painting</strong> where cleaning cannot remove staining or odor</li>
<li><strong>HVAC cleaning</strong> of ductwork, registers, the air handler and filters</li>
<li><strong>Contents cleaning</strong> of clothing, bedding, upholstery, electronics and kitchen items</li>
<li><strong>Carpet and soft surface cleaning</strong> or replacement where soot cannot be removed</li>
<li><strong>Odor control</strong> such as thermal fogging or hydroxyl treatment</li>
<li><strong>Contents pack-out</strong> and storage while the house is cleaned</li>
</ul>
<div class="note"><b class="h">Contents add up fast</b><p>In a puffback, contents cleaning can rival the structure cleaning in cost. Keep a room-by-room inventory with photos, and do not throw anything away until the adjuster or your appraiser has documented it.</p></div>
<h2>Where carrier estimates leave gaps</h2>
<p>Carrier estimates for puffbacks often treat the loss as a basement event, limiting cleaning to the boiler room and a few nearby rooms. Common gaps include:</p>
<ul>
<li>Upper floors and closed rooms where soot traveled through ducts</li>
<li>Duct cleaning priced for part of the system instead of all of it</li>
<li>Painting omitted on the assumption that cleaning alone will work</li>
<li>Contents cleaning missing or priced as a lump sum</li>
<li>Additional living expense for families who cannot stay during cleaning</li>
</ul>
<p>In older Maine homes with plaster walls, hot-air systems and tight closets, soot can be stubborn, and a cleaning-only scope may not hold up after the first heating season. Our <a href="/appraisal-work/fire-smoke-puffback-appraisal/">fire, smoke and puffback appraisal</a> page explains what we look for.</p>
<p><strong>Illustrative example:</strong> a carrier estimate for a puffback in a Brunswick colonial covers the basement and first-floor kitchen cleaning at $6,800. A restoration company’s wipe tests show soot on all three floors, and the full scope with duct cleaning, contents cleaning, sealing and painting comes to $24,000. These numbers are illustrative, not drawn from a real claim.</p>
<h2>When appraisal helps with an oil burner puffback</h2>
<p>When the carrier has accepted the puffback claim and the dispute is over how many rooms, how much cleaning and what it costs, appraisal is a natural fit. The panel can review wipe test photos, the restoration report and both estimates. It can also weigh whether sealing and painting are needed or whether cleaning alone will restore the surfaces, which is one of the most common sticking points in puffback files. Pricing for contents cleaning, pack-out and storage is another area where the appraisers often need to work through each line carefully.</p>
<p>Before you take that step, gather your documentation and check the file with the <a href="/claim-math/appraisal-file-strength-test/">appraisal file strength test</a>. If you have questions about your claim, you can <a href="/reach-us/">reach us</a> for an initial read. If the carrier denies the oil burner puffback claim or raises a coverage issue, a Maine attorney should review it first.</p>
""",
    },
]
