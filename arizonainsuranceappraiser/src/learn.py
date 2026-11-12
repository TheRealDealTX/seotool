"""Resources: appraisal roadmap (process guide), grouped FAQ, glossary and articles."""

STEPS = [
    ("Pin down the disagreement", "Before anything formal happens, write down exactly where you and the carrier differ: which rooms, which roof slopes, which line items and what your number is. Send that to the adjuster with your contractor’s estimate and photos. A specific, documented supplement request settles more Arizona claims than any other single step, and it creates a record if you go further."),
    ("Read the Appraisal condition and the deadlines around it", "Find the Appraisal paragraph in your policy’s conditions. Note whether it sets a deadline to name an appraiser, whether it requires a sworn proof of loss first, and how it describes the appraisers (competent, independent, disinterested or impartial). Then find the suit-limitation condition and put that date on your calendar. Appraisal may not stop it."),
    ("Send a written demand", "Either side can demand appraisal in writing. The demand should identify the claim, say that you disagree on the amount of loss, invoke the appraisal provision and name your appraiser or commit to naming one within the policy’s time frame. Send it in a way you can prove, such as certified mail plus email."),
    ("Both sides name appraisers", "Each party chooses its own appraiser. Yours reviews the file, inspects the property independently and builds a line-item estimate. The carrier’s appraiser does the same. A good appraiser can explain every line of their number to the other side and to an umpire."),
    ("The appraisers choose an umpire", "The two appraisers select a neutral umpire, ideally early, before positions harden. Look for relevant experience, such as tile and foam roofs, large commercial losses or wildfire rebuilds, and full disclosure of past relationships. If the appraisers deadlock, many policies allow a court in the county where the property sits to appoint one."),
    ("The appraisers work through the differences", "Most of the dispute is resolved here. The two appraisers compare scopes item by item, agree where they can, and narrow the rest to a short list. If they agree on everything, they sign an award and the umpire never has to act."),
    ("The umpire decides what is left", "For items still in dispute, each appraiser submits a position with support: photos, measurements, pricing, manufacturer data. The umpire may inspect the property. The umpire then decides each disputed item."),
    ("The award is signed and paid", "When the umpire and one appraiser, or both appraisers, sign the award, the amount of loss is set. The carrier then applies the deductible, depreciation, limits and prior payments under the policy. Payment timing depends on the policy and Arizona’s claim-handling rules; ask the carrier for its timeline in writing."),
]

PROCESS_BODY = '<ol class="toc-steps">' + "".join(f'<li><a href="#step-{i + 1}">{t}</a></li>' for i, (t, _) in enumerate(STEPS)) + "</ol>" + "".join(f'<h2 class="step-h" id="step-{i + 1}"><span>Step {i + 1}</span> {t}</h2><p>{p}</p>' for i, (t, p) in enumerate(STEPS)) + """
<div class="note"><b class="h">Where Arizona’s rules come in</b>Arizona’s Department of Insurance and Financial Institutions (DIFI) regulates insurers and handles consumer complaints. Arizona statutes describe unfair claim settlement practices that the department can act on, and Arizona courts have long recognized a separate legal claim for insurer bad faith. Those are legal matters for an attorney. Appraisal deals only with the amount of loss.</div>
<h2>How long it takes</h2>
<p>Straightforward residential appraisals often finish in two to four months. Commercial claims, disputes involving engineers and umpire schedules during a busy monsoon season can take longer.</p>
<h2>What it costs</h2>
<p>Each side pays its own appraiser. The umpire’s fee is usually split evenly. The <a href="/claim-calculators/appraisal-payoff-estimator/">appraisal payoff estimator</a> shows how those costs affect what you net.</p>
"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "A process written into most property policies for settling disagreements over the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and an award signed by two of the three sets the amount."),
        ("What does an Arizona Insurance Appraiser do?", "We serve as the appraiser you name, review estimates before a dispute escalates, and act as a neutral umpire on other panels. Our work is valuing property damage, not deciding coverage or giving legal advice."),
        ("Is appraisal the same as arbitration?", "No. Appraisal is limited to the amount of loss. It does not decide coverage, liability or bad-faith questions, and it is usually faster and less formal than arbitration."),
        ("Who can start appraisal?", "Either you or the insurer, usually by written demand, as long as the disagreement is about the amount of loss."),
        ("Is the award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. Courts can set aside awards in limited circumstances such as fraud or a panel exceeding its authority."),
    ]),
    ("Costs and timing", [
        ("How much does an appraiser cost?", "Fees are either flat or a percentage of the increase over the carrier’s figure, depending on the claim. We put ours in writing before any work begins."),
        ("Who pays the umpire?", "Most policies split the umpire’s fee equally between you and the insurer."),
        ("How long does appraisal take?", "Commonly two to four months for a home, longer for complex or commercial losses."),
        ("Is there a minimum claim size?", "No formal minimum, but if the gap is only a few thousand dollars, fees may consume most of the gain. Run the payoff estimator first."),
        ("When is the best time to invoke appraisal?", "After coverage is accepted, the carrier’s estimate is final, you have your own itemized estimate and supplement requests have stalled."),
    ]),
    ("Arizona specifics", [
        ("Who regulates insurers in Arizona?", "The Arizona Department of Insurance and Financial Institutions (DIFI). You can file a consumer complaint with DIFI if you believe your claim was mishandled."),
        ("Does Arizona have a FAIR plan or state wind pool?", "Arizona does not operate a FAIR plan or a state wind pool like coastal states do. Homes that are hard to insure in the standard market are usually placed with surplus lines carriers, whose policies can differ in important ways."),
        ("What happens if my insurer becomes insolvent?", "Arizona has a property and casualty insurance guaranty fund that pays certain covered claims of insolvent licensed insurers, subject to limits. Surplus lines policies are generally not covered by it."),
        ("Does Arizona have a bad-faith law?", "Arizona statutes list unfair claim settlement practices the department can act on, and Arizona courts recognize a separate legal claim against insurers for bad faith. Whether either applies to you is a question for an Arizona attorney."),
        ("How many counties do you cover?", "All 15 Arizona counties, from Apache to Yuma."),
    ]),
    ("Roofs and storms", [
        ("Can appraisal decide whether my tile roof should be replaced?", "Appraisal can decide the cost to repair the covered damage, which often turns on whether a repair is feasible given the underlayment and tile availability. Matching questions can involve coverage too."),
        ("What if the carrier says the damage is wear and tear?", "That is partly a causation and coverage question. Many policies and courts treat some causation questions as part of the amount of loss and others as coverage. Document the storm date and damage carefully."),
        ("Are monsoon losses handled differently from hail?", "The appraisal process is the same. The difference is in what gets damaged and how a deductible applies. Some Arizona policies have a separate wind/hail deductible."),
        ("Is flood covered under my homeowners policy?", "Surface flooding is usually excluded and needs separate flood insurance. Rain entering through storm-created openings is often covered."),
    ]),
    ("Working with us", [
        ("Do you replace my public adjuster or attorney?", "No. We work alongside them. Public adjusters manage claims; attorneys handle legal issues; we value the loss inside appraisal."),
        ("Can I hire you just for an estimate review?", "Yes. Many clients start with a review and decide later whether to invoke appraisal."),
        ("Do you guarantee results?", "No honest appraiser can. We promise a careful, defensible valuation and straight talk about your options."),
    ]),
]

GLOSSARY = sorted([
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Often the first payment on a replacement cost claim."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while your home is being repaired after a covered loss."),
    ("Amount of loss", "The dollar value of covered damage. The only thing an appraisal panel decides."),
    ("Appraisal clause", "The policy condition that lets either party demand appraisal when they disagree on the amount of loss."),
    ("Appraisal award", "The written decision on the amount of loss, binding once signed by two of the three panel members."),
    ("Battens", "Wood or plastic strips fastened to the roof deck that hold tile in place on some roof systems."),
    ("Business income", "Commercial coverage for lost income while a business is closed or limited because of covered property damage."),
    ("Coinsurance", "A commercial policy condition that can reduce payment if the building is insured for less than a required percentage of its value."),
    ("Coverage A", "Dwelling coverage on a homeowners policy, the limit for the house itself."),
    ("Coverage B", "Other structures coverage for detached garages, walls, fences, ramadas and similar items."),
    ("Declarations page", "The summary page of your policy listing limits, deductibles, endorsements and the policy period."),
    ("Depreciation", "The reduction in value from age, wear and condition, deducted from replacement cost to reach ACV."),
    ("DIFI", "The Arizona Department of Insurance and Financial Institutions, which regulates insurers and handles consumer complaints."),
    ("Elastomeric coating", "A flexible reflective coating applied over spray foam roofs to protect the foam from sun and weather."),
    ("Endorsement", "A written change to a policy that adds, removes or modifies coverage."),
    ("Haboob", "A wall of dust pushed ahead of a collapsing thunderstorm, common during the Arizona monsoon."),
    ("Holdback", "Recoverable depreciation the insurer withholds until repairs are completed."),
    ("Ice dam", "A ridge of ice at the eave that traps meltwater, which can back up under roofing."),
    ("Line item", "A single priced entry in an estimate, such as a quantity of drywall or a roof component."),
    ("Matching", "Whether repairs must reasonably match undamaged areas in color, texture and profile."),
    ("Microburst", "A sudden, concentrated downdraft from a thunderstorm that spreads damaging straight-line wind."),
    ("Mitigation", "Reasonable steps to prevent further damage after a loss, such as tarping or drying."),
    ("Monsoon", "Arizona’s summer storm season, officially June 15 to September 30."),
    ("Ordinance or law coverage", "Coverage for added costs of meeting current building codes during repair."),
    ("Overhead and profit (O&P)", "A general contractor’s charge for coordinating trades and running the job, often 10% plus 10%."),
    ("Price list", "The regional cost database an estimating program uses to price line items."),
    ("Proof of loss", "A sworn statement of the amount claimed, which some policies require within a set time after the insurer asks."),
    ("Public adjuster", "A licensed professional who represents policyholders in preparing and negotiating claims for a fee."),
    ("Recoverable depreciation", "Depreciation you can collect after repairs under a replacement cost policy."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with like kind and quality, without deducting depreciation."),
    ("Scope of loss", "The list of everything that must be repaired or replaced, before pricing."),
    ("Slab leak", "A leak in a water line running beneath a concrete slab foundation."),
    ("Spray polyurethane foam (SPF)", "A sprayed roofing material common on Arizona flat roofs, protected by an elastomeric coating."),
    ("Square", "100 square feet of roof surface, the standard unit for roofing."),
    ("Steep charge", "An added labor charge for roofs too steep to walk safely, often starting at 7/12 or 8/12."),
    ("Suit limitation", "The policy time limit for filing a lawsuit over the claim."),
    ("Supplement", "A request to add missing items or costs to the insurer’s estimate."),
    ("Surplus lines insurer", "A non-admitted insurer that covers risks the standard market will not. Policies can differ from standard forms."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the two appraisers cannot agree on."),
    ("Underlayment", "The waterproof layer beneath roof tile or shingles; on tile roofs it does most of the waterproofing."),
    ("Wildland-urban interface (WUI)", "Areas where homes meet forest, brush or grassland, with higher wildfire exposure."),
    ("Xactimate", "Widely used estimating software for property insurance claims."),
], key=lambda t: t[0].lower())

POSTS = [
    {
        "slug": "documenting-monsoon-storm-damage",
        "title": "Documenting Monsoon Storm Damage: A Checklist for Arizona Owners",
        "seo": "Documenting Monsoon Storm Damage in Arizona | Checklist",
        "desc": "What to photograph, save and write down after an Arizona monsoon storm so your roof, wall and water damage claim holds up later in appraisal.",
        "summary": "The first 72 hours after a microburst decide how strong your claim will be. Here is what to capture before cleanup erases the evidence.",
        "date": "2026-07-14", "read": "7 min",
        "body": """
<p>Monsoon storms move fast. A microburst can last only minutes, and by the next morning neighbors are hauling branches to the curb and roofers are knocking on doors. The evidence that will matter in an appraisal disappears just as quickly. Here is how to preserve it.</p>
<h2>Before anything is moved</h2>
<ul><li>Take wide photos of each side of the house, then close-ups of every damaged area.</li>
<li>Photograph fallen trees and limbs where they landed, including the root ball or break point.</li>
<li>Photograph block walls, ramadas, shade sails, pool equipment, solar panels and coolers.</li>
<li>Take a short video walking the property. Narrate what you see and the date.</li></ul>
<h2>Pin down the date and the storm</h2>
<p>Write down when the storm hit and what you saw and heard. Save weather alerts from your phone. Neighbors’ photos and local news coverage can help confirm the event. If the carrier later questions whether damage came from this storm or an earlier one, those records matter.</p>
<h2>Roofs: what to look for safely</h2>
<p>Do not climb a tile roof. Tiles break underfoot and you can be badly hurt. From the ground, photograph displaced tiles, debris in gutters and pieces of tile on the ground. Inside, check ceilings for stains and the attic for daylight or wet insulation. Let a roofer document the roof itself, and ask for photos of the underlayment.</p>
<h2>Mitigate and keep every receipt</h2>
<p>Tarp openings, dry wet areas and remove spoiled items, but photograph first. Keep receipts for tarps, fans, dumpster rental and emergency services. Reasonable mitigation is usually reimbursable and protects you from arguments that you allowed damage to grow.</p>
<h2>Then build your estimate</h2>
<p>Get an itemized estimate, not a one-line bid. Compare it with the carrier’s, line by line. If the gap is meaningful, run the numbers in our <a href="/claim-calculators/appraisal-payoff-estimator/">appraisal payoff estimator</a> and check your file with the <a href="/claim-calculators/claim-file-readiness-check/">claim file readiness check</a>.</p>
""",
    },
    {
        "slug": "tile-roof-claims-underlayment-matching",
        "title": "Tile Roof Claims in Arizona: Breakage, Underlayment and Matching",
        "seo": "Arizona Tile Roof Claims: Underlayment & Matching",
        "desc": "Why Arizona tile roof claims stall over broken-tile counts, brittle underlayment and discontinued profiles, and how to document each issue well.",
        "summary": "Concrete tile can outlast the felt beneath it by decades. That mismatch is behind most tile roof disputes in the Valley and Tucson.",
        "date": "2026-08-25", "read": "8 min",
        "body": """
<p>Drive through almost any Phoenix or Tucson subdivision built in the last forty years and you will see concrete tile. Tile is durable and fire-resistant, and it handles heat well. It also produces some of the most stubborn insurance disputes in the state.</p>
<h2>Fight one: the breakage count</h2>
<p>Hail cracks in tile can be hairline, and some tiles crack on the underside without visible damage on top. A quick inspection from one corner of the roof often undercounts. A slope-by-slope survey with marked photos, done by someone who knows how to walk tile without breaking it, produces a far more defensible number.</p>
<h2>Fight two: the underlayment</h2>
<p>On most tile roofs, the underlayment beneath the tile is what actually keeps water out. Older felt underlayment can turn brittle after two decades of desert heat. To replace a broken tile, a roofer has to lift and slide neighboring tiles. If the underlayment cracks or crumbles when that happens, the “repair” creates new leaks.</p>
<p>That makes repairability a genuine valuation question. Photographs of the underlayment in several areas, notes on its age, and a roofer’s written opinion on whether it can be disturbed are key evidence. Our <a href="/claim-calculators/tile-roof-repair-or-replace-checker/">tile roof repair-or-replace checker</a> walks through these factors.</p>
<h2>Fight three: matching</h2>
<p>Manufacturers discontinue tile profiles and colors regularly. Salvaged tile may be available, or it may not. A patch of new tile in a different color on a street-facing slope is more than cosmetic, especially when an HOA requires uniform roofs.</p>
<p>How much matching a policy requires depends on its wording and on Arizona law, which can change. The valuation side is documenting what is available, from whom, and what a reasonable match would cost.</p>
<h2>Foot traffic damage</h2>
<p>Inspections themselves can break tile. Photograph your roof before inspections when you can, and note any new breakage afterward. Inspection damage is not storm damage, but it still needs to be fixed by someone.</p>
""",
    },
    {
        "slug": "wildfire-smoke-and-ash-cleanup-claims",
        "title": "Smoke and Ash After an Arizona Wildfire: Valuing the Cleanup",
        "seo": "Wildfire Smoke & Ash Claims in Arizona | Cleanup Value",
        "desc": "Your home survived the wildfire but filled with smoke and ash. How Arizona owners can document HVAC, insulation, contents and cleaning claims.",
        "summary": "Homes that never burned can still need far more than a wipe-down. Here is how to document smoke and ash damage after a wildfire.",
        "date": "2026-06-10", "read": "7 min",
        "body": """
<p>When the Tunnel Fire, the Museum Fire or the Rodeo-Chediski Fire burned toward neighborhoods, many homes survived the flames but not the smoke. Fine ash drifted through vents, attic openings and gaps around doors and windows. Months later, owners were still smelling it on hot afternoons.</p>
<h2>Why smoke claims are undervalued</h2>
<p>Carriers often start with a standard cleaning scope: wipe surfaces, clean carpets, change the furnace filter. That can be enough for light exposure. It often is not enough when ash has entered the HVAC system and attic, or when porous materials keep releasing odor.</p>
<h2>What to document</h2>
<ul><li>Ash on window sills, inside cabinets, on attic insulation and inside supply registers.</li>
<li>Odor in specific rooms, closets and fabrics, noted by date and temperature.</li>
<li>HVAC filters, returns and duct interiors, photographed by a technician.</li>
<li>Electronics, appliances and anything with fans that drew in smoky air.</li>
<li>Exterior surfaces: stucco, paint, decks and solar panels coated with ash.</li></ul>
<h2>Testing can help</h2>
<p>When the scope is disputed, testing by an industrial hygienist or a qualified restoration professional can show how far particulates traveled. Test results turn “it still smells” into evidence.</p>
<h2>Contents</h2>
<p>Soft goods such as clothing, bedding and upholstered furniture may clean successfully or may not. Keep a list of what was cleaned, what still smells afterward and what had to be discarded. Photos before disposal are essential.</p>
<h2>Living expenses</h2>
<p>If smoke made the home unlivable, additional living expense coverage may apply. Keep hotel, meal and mileage receipts.</p>
<p>For the full range of wildfire claims, see <a href="/appraisal/wildfire-and-ash-claims/">wildfire, smoke and ash appraisal</a>.</p>
""",
    },
    {
        "slug": "water-leaks-in-seasonal-homes",
        "title": "Water Leaks in Seasonal Homes: What Arizona Snowbirds Should Know",
        "seo": "Water Leaks in Arizona Seasonal Homes | Snowbird Claims",
        "desc": "Winter visitors and second-home owners face vacancy clauses and long-term seepage disputes on Arizona water claims. How to prevent and prove them.",
        "summary": "A slow leak in an empty house can run for weeks. Vacancy clauses and seepage exclusions then turn a water claim into a timing argument.",
        "date": "2026-10-06", "read": "6 min",
        "body": """
<p>Arizona is full of homes that sit empty for part of the year: winter homes in Mesa, Yuma and Lake Havasu City, cabins in Pinetop and Payson, vacation rentals in Sedona and Flagstaff. Water losses in those homes raise two questions full-time residents rarely face.</p>
<h2>Question one: vacancy and unoccupancy</h2>
<p>Many policies restrict coverage for certain losses if the home has been vacant or unoccupied beyond a set period, and some require you to keep heat on or drain the plumbing. The exact wording matters: vacant (empty of furnishings) and unoccupied (furnished but no one living there) can mean different things in a policy.</p>
<h2>Question two: sudden or long-term?</h2>
<p>Policies typically cover sudden and accidental discharges and exclude repeated seepage or leakage over weeks or longer. When no one is home, a carrier may argue that damage built up slowly. Evidence of when the leak started becomes central.</p>
<h2>Prevention that also helps proof</h2>
<ul><li><strong>Shut off the main</strong> when you leave, if your irrigation and other systems allow it.</li>
<li><strong>Install a smart water shutoff or leak sensors.</strong> Their logs can show exactly when a leak began.</li>
<li><strong>Arrange regular property checks</strong> and keep a dated log or photos from each visit.</li>
<li><strong>Keep utility bills.</strong> Water usage spikes can help date a leak.</li></ul>
<h2>If a loss happens</h2>
<p>Stop the water, start drying, document everything and report promptly. Gather the check logs, sensor data and utility records before the carrier asks. If coverage is denied over vacancy or seepage, that is a legal question for an attorney. If coverage is accepted and the dispute is about cost, appraisal can help.</p>
""",
    },
    {
        "slug": "appraisal-difi-complaint-or-attorney",
        "title": "Appraisal, a DIFI Complaint or an Attorney? Choosing Your Path",
        "seo": "Appraisal, DIFI Complaint or Attorney? Arizona Options",
        "desc": "Arizona policyholders have several ways to push back on a claim. When appraisal fits, when a DIFI complaint helps and when to call an attorney.",
        "summary": "Each option solves a different problem. Picking the right one first saves time, money and sometimes the claim itself.",
        "date": "2026-09-15", "read": "6 min",
        "body": """
<p>When an Arizona property claim goes sideways, owners usually hear about three options: invoke appraisal, complain to the state, or hire a lawyer. They are not interchangeable, and they can be used together.</p>
<h2>Appraisal: when the fight is about the number</h2>
<p>Appraisal fits when the carrier accepts that the loss is covered but you disagree on what it costs to fix. It is defined by your policy, relatively fast, and ends with a binding amount of loss. It does not decide coverage or whether the carrier acted fairly.</p>
<h2>A DIFI complaint: when the process is the problem</h2>
<p>The Arizona Department of Insurance and Financial Institutions takes consumer complaints about insurers. A complaint can help when the carrier is not responding, has not explained a decision, or seems to be ignoring its own procedures. The department can ask the insurer to respond. It does not act as your lawyer or decide the value of your claim.</p>
<h2>An attorney: when coverage, conduct or deadlines are at stake</h2>
<p>Call an Arizona attorney when the claim has been denied in whole or large part, when the carrier invokes an exclusion you dispute, when you believe the claim was handled in bad faith, or when a suit-limitation deadline is approaching. Arizona courts recognize claims against insurers for bad faith, and those cases depend heavily on facts and timing.</p>
<h2>Using them together</h2>
<p>It is common to have an attorney advise on coverage while an appraisal panel values the loss, or to file a DIFI complaint about unanswered letters while preparing for appraisal. What matters is matching each tool to the problem it solves.</p>
<table><thead><tr><th scope="col">Problem</th><th scope="col">Best first step</th></tr></thead><tbody>
<tr><th scope="row">Covered, but the estimate is short</th><td>Estimate review, supplement, then appraisal</td></tr>
<tr><th scope="row">No response or explanation from the carrier</th><td>Written follow-up, then a DIFI complaint</td></tr>
<tr><th scope="row">Denied, or a disputed exclusion</th><td>Arizona attorney</td></tr>
<tr><th scope="row">Suit deadline approaching</th><td>Arizona attorney, immediately</td></tr>
</tbody></table>
""",
    },
    {
        "slug": "overhead-profit-and-price-lists",
        "title": "Overhead, Profit and Price Lists: Where Arizona Estimates Come Up Short",
        "seo": "Overhead & Profit and Price Lists in Arizona Estimates",
        "desc": "Two quiet ways property estimates come up short: missing overhead and profit and outdated regional price lists. How to spot both in an Arizona claim.",
        "summary": "Missing O&P and stale pricing rarely jump off the page, but on a multi-trade claim they can be worth thousands.",
        "date": "2026-05-12", "read": "6 min",
        "body": """
<p>When owners compare their contractor’s bid with the carrier’s estimate, they usually look at quantities: how many squares, how much drywall. Two other items can matter as much and are easy to miss.</p>
<h2>Overhead and profit</h2>
<p>General contractors charge for coordinating trades, supervising the job, insurance, permits and running a business. In estimating software this is often shown as overhead and profit, commonly 10% and 10%. Carriers sometimes leave it out, arguing a general contractor is not needed.</p>
<p>On a job that involves roofing, drywall, painting, flooring and electrical work, it is hard to argue no one needs to coordinate the trades. Whether O&amp;P is owed depends on the policy and the complexity of the job, but its absence on a multi-trade claim deserves a question.</p>
<h2>Price lists</h2>
<p>Estimating programs price line items using regional price lists that are updated over time. An estimate written months ago, or with the wrong region selected, may use outdated or mismatched costs. After a large storm, demand for roofers and materials can push real prices up faster than the lists change.</p>
<p>Check the price list code and date printed on the estimate. Compare a few major line items, such as tile per square or drywall per square foot, against current local bids.</p>
<h2>Sales tax and permits</h2>
<p>Arizona’s transaction privilege tax and local rates apply to materials and, depending on how a contract is structured, to contracting. Permits are required for many roof and structural repairs. Both are easy to omit and legitimate to include.</p>
<p>A line-by-line <a href="/appraisal/claim-estimate-second-opinion/">estimate review</a> catches these issues before you decide whether appraisal is worth it.</p>
""",
    },
]
