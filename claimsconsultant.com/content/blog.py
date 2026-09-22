"""Eight long-form articles.

House rule for this section: every piece has to teach a reader something they
could act on without hiring us. If it reads like a brochure with subheadings,
it does not go up.
"""

from siteconfig import BIZ

P = BIZ["phone_display"]

POSTS = [

    # =====================================================================
    {
        "slug": "first-72-hours-after-a-commercial-property-loss",
        "category": "Field guide",
        "published": "2026-08-18",
        "modified": "2026-09-02",
        "read": "11",
        "words": 1750,
        "title": "The First 72 Hours After a Commercial Property Loss | Field Guide",
        "description": ("What to photograph, what to keep, what to sign and what not to sign in "
                        "the first three days after a major commercial or institutional property "
                        "loss in Texas."),
        "h1": "The first 72 hours<br>after a <em>major loss</em>",
        "h1_plain": "The first 72 hours after a commercial property loss",
        "blurb": ("Evidence has a shelf life. Almost everything that decides a large claim is "
                  "either captured or destroyed in the first three days."),
        "lede": ("Nobody is thinking clearly on the morning after a fire or a storm, which is "
                 "exactly why the decisions made then carry so much weight later. This is the "
                 "list we would want a facilities director to have taped inside a cupboard door."),
        "body": [
            ("p", "There is a particular kind of loss that ends badly for reasons that have "
                  "nothing to do with the damage. The building is repaired, the settlement is "
                  "reasonable on its face, and eighteen months later the organization discovers "
                  "it absorbed several hundred thousand dollars it did not have to. Trace it "
                  "back and the cause is almost never a dramatic error. It is that nobody "
                  "photographed the ceiling before the volunteers pulled it down, or that the "
                  "emergency restoration contract signed at eleven at night contained an "
                  "assignment of benefits."),
            ("p", "What follows is not legal advice and it is not a substitute for reading your "
                  "policy. It is what we wish every institutional client had done before we "
                  "arrived."),

            ("h2", "Hour zero to six: safety, then evidence"),
            ("p", "Life safety comes first and nothing here changes that. Once the building is "
                  "secure and people are accounted for, the priority shifts immediately to "
                  "capture, because the property is about to start changing."),
            ("p", "Photograph everything before anything moves. Wide shots that establish the "
                  "space, then medium shots that show the relationship between the damage and "
                  "the building, then close-ups. Include a reference for scale. Photograph the "
                  "undamaged areas too &mdash; six months from now, proving what a room looked "
                  "like before demolition will matter more than you expect. Video walkthroughs "
                  "with narration are unglamorous and extraordinarily useful."),
            ("callout", "The single most valuable photograph", [
                ("p", "On a water loss, it is the failed component before the plumber cuts it "
                      "out. On a fire, it is the contents inventory before anything is cleared. "
                      "On a storm, it is the high-water mark before the walls are washed. Each "
                      "takes thirty seconds and each has settled arguments worth six figures."),
            ]),
            ("p", "Then start a log. A notebook, a shared document, anything with dates. Who "
                  "attended, what was decided, which vendor arrived and when, what the carrier "
                  "said on the phone. A contemporaneous log is worth more in a dispute than any "
                  "reconstruction made later, and no one ever regrets having kept one."),

            ("h2", "Hour six to twenty-four: mitigate, but do not destroy"),
            ("p", "Every commercial property policy imposes a duty to protect the property from "
                  "further damage. That duty is real and failing it gives the carrier a defense "
                  "on everything that happened afterwards. Board up, tarp, extract water, get "
                  "power to the building, start drying. Do not wait for an adjuster to authorise "
                  "emergency mitigation; that is not how the obligation works."),
            ("p", "What you should avoid is destroying evidence while discharging that duty. "
                  "There is a difference between drying a building and gutting it. Before "
                  "materials are removed, photograph them in place. Where anything must be "
                  "disposed of, keep a representative sample and photograph the rest in the "
                  "dumpster. Retain failed components &mdash; pipes, fittings, valves, electrical "
                  "equipment &mdash; labelled and boxed. If subrogation or a product defect ever "
                  "becomes relevant, that box is the case."),
            ("checks", [
                "Photograph before, during and after every mitigation activity.",
                "Keep failed components; label them with location and date.",
                "Retain a sample of any material you must dispose of.",
                "Log moisture readings daily, by location, with the equipment used.",
                "Keep every emergency invoice separate from the eventual repair contract.",
            ]),

            ("h2", "Read before you sign: three documents that arrive early"),
            ("p", "Restoration companies monitor scanner traffic and arrive fast, which is "
                  "genuinely useful. What they bring with them deserves a careful reading even "
                  "at two in the morning."),
            ("table", "What gets put in front of you in the first day",
             ["Document", "What it does", "What to watch"], [
                ["Work authorisation", "Permits emergency mitigation to begin.",
                 "Scope and rate schedule; open-ended time and materials with no cap."],
                ["Assignment of benefits", "Transfers your rights under the policy to the contractor.",
                 "You lose control of that portion of the claim. Rarely necessary. Think hard."],
                ["Direction to pay", "Instructs the insurer to pay the contractor directly.",
                 "Less severe than an AOB, still a commitment. Confirm it applies to their invoice only."],
             ]),
            ("p", "None of these are inherently improper and all of them are easier to sign than "
                  "to undo. If a vendor will not let you take an hour to read a contract during "
                  "an emergency, that is information about the vendor."),

            ("h2", "Day two: give notice, properly"),
            ("p", "The date of notice anchors every other date in the file, including how "
                  "long the property sat before anyone competent looked at it. That interval is "
                  "the first thing an opposing expert calculates, so it is worth keeping short "
                  "and worth being able to prove."),
            ("p", "So give notice in writing, keep proof of when you sent it, and describe the "
                  "loss accurately but without speculating about cause. &ldquo;Water damage "
                  "throughout the north wing following the storm of 14 March&rdquo; is a "
                  "description. &ldquo;The roof failed because it was old&rdquo; is a gift."),
            ("callout", "If you are covered by a risk pool", [
                ("p", "Many Texas districts, cities and other public entities cover property "
                      "through an interlocal risk pool rather than an insurer. The coverage "
                      "document governs the notice requirements and the appeal route, and it "
                      "is not a standard policy. Read it rather than assuming."),
            ]),

            ("h2", "Day two to three: set the file up so it can be proved"),
            ("p", "This is the part organizations skip, and it is the part that determines "
                  "whether the time-element claim is provable nine months from now. Open a "
                  "separate general ledger account for loss-related costs on day two. Every "
                  "invoice, every overtime hour, every rented piece of equipment, every hotel "
                  "night for displaced staff or residents gets coded there. It takes your "
                  "finance team twenty minutes to set up and saves an argument that would "
                  "otherwise run for months."),
            ("p", "At the same time, export anything that expires. Building management system "
                  "logs frequently retain only thirty to ninety days of data. Access control "
                  "and CCTV overwrite. Utility outage records are easiest to obtain close to the "
                  "event. If any of those matter to your claim &mdash; and on a freeze claim the "
                  "BMS logs are frequently the whole case &mdash; pull them this week."),
            ("checks", [
                "Separate GL account or cost code opened for loss-related spend.",
                "BMS, thermostat, access control and CCTV data exported and stored off-system.",
                "Utility outage confirmation requested for the property address and period.",
                "Declarations page, full policy and schedule of values located and circulated internally.",
                "One person designated as the single point of contact for the carrier.",
            ]),

            ("h2", "What not to do"),
            ("p", "Do not give a recorded statement without preparing for it. You are entitled "
                  "to understand what will be asked, to have someone present, and to correct "
                  "yourself. Do not speculate about cause, age or prior condition &mdash; "
                  "&ldquo;I think that roof was about twenty-five years old&rdquo; said casually "
                  "on a recording will be quoted back to you for the next two years."),
            ("p", "Do not accept a scope you have not read because the check attached to it "
                  "would be useful this month. And do not sign a release. A payment is not a "
                  "release, and most policies contemplate supplemental claims when the actual "
                  "cost of repair exceeds the estimate. Signing a full and final release closes "
                  "that door permanently."),
            ("quote", "Nearly every claim we are asked to rescue was survivable in week one and "
                      "difficult by month six. The damage did not change. The evidence did.",
             "From the claims desk"),

            ("h2", "When to call someone"),
            ("p", "You do not need a consultant on every loss, and any firm that tells you "
                  "otherwise is selling. Below the deductible, or where the estimate on the table "
                  "is clearly thorough and the number is right, an independent review costs money "
                  "for nothing."),
            ("p", "Where it earns its keep is on losses large enough that a scope dispute is "
                  "worth six figures, on buildings complex enough that a template estimate will "
                  "miss things, on any claim with a meaningful time-element component, and on "
                  "any file where an engineer has already been retained. On institutional "
                  "property, that is most significant losses."),
            ("p", "If you are inside the first 72 hours right now, the useful call is not about "
                  "engagement. It is about what to photograph before the crews arrive. That "
                  "conversation is free and it takes ten minutes."),
        ],
    },

    # =====================================================================
    {
        "slug": "repair-or-replace-how-the-decision-gets-made",
        "category": "Field guide",
        "published": "2026-07-09",
        "modified": "2026-08-30",
        "read": "10",
        "words": 1600,
        "title": "Repair or Replace: How the Decision Actually Gets Made",
        "description": ("The repair-versus-replace test, and the evidence that settles it on "
                        "roofs, casework, contents and equipment."),
        "h1": "Repair or replace:<br>how it <em>gets decided</em>",
        "h1_plain": "Repair or replace: how the decision gets made",
        "blurb": ("More disputed dollars turn on this one question than on coverage. It has an "
                  "answerable test, and almost nobody applies it."),
        "lede": ("Strip the argument out of most contested property claims and what is left is a "
                 "single question asked forty times: can this be fixed, or does it have to be "
                 "replaced. It is a technical question with a technical answer, and it is "
                 "routinely settled by whoever asserts hardest."),
        "body": [
            ("p", "The pattern is the same whatever the component. One side says the item can be "
                  "cleaned, dried, refinished, coated, patched or recalibrated. The other says it "
                  "is finished. Both positions are stated with total confidence, neither is "
                  "supported by a measurement, and the file sits for four months while two "
                  "people who have never opened the assembly disagree about what is inside it."),

            ("h2", "The test"),
            ("p", "The question is not whether a repair is physically possible. Almost anything "
                  "is physically possible. The question is whether repair restores the item to "
                  "its pre-loss condition and remaining service life."),
            ("p", "Those last four words carry most of the weight. A roof membrane with bruised "
                  "insulation beneath it can be patched. It will not perform for the fifteen "
                  "years it had left, and the manufacturer will frequently decline to warrant "
                  "it. A swollen particleboard cabinet box can be refinished. It will not hold a "
                  "hinge screw. Repair that leaves the owner with a shorter-lived asset than "
                  "they had before the loss has not restored anything; it has deferred the cost "
                  "and moved it onto them."),
            ("callout", "The corollary cuts the other way too", [
                ("p", "A well-maintained plywood cabinet run that got wet at the toe kick and "
                      "dried within forty-eight hours is repairable, and claiming otherwise "
                      "because replacement is cleaner is exactly the same error in the opposite "
                      "direction. The test does not have a preferred answer."),
            ]),

            ("h2", "Four components, four kinds of evidence"),
            ("table", "What actually settles it",
             ["Component", "The real question", "Evidence that answers it"], [
                ["Low-slope roofing",
                 "Is the insulation beneath an intact membrane fractured?",
                 "Test cuts through the assembly, photographed in place; manufacturer position on warranting a patched system; soft-metal corroboration around the property"],
                ["Casework and millwork",
                 "What is the substrate, and has it lost dimensional stability?",
                 "Substrate identified at a cut edge; moisture readings by location; swelling measured at affected and unaffected points; joint and fastener testing"],
                ["Contents and equipment",
                 "Can it be restored to reliable service, and can that be certified?",
                 "Manufacturer or OEM inspection; cleaning trial on a representative sample; contamination testing where residue is in issue; recalibration and requalification results"],
                ["Finishes and substrates after smoke",
                 "What is the residue, and has it penetrated?",
                 "Residue characterization by sampling, not by smell; background comparison from unaffected areas; test cleaning with a documented result"],
             ]),
            ("p", "Every row in that table describes something that can be done in a day or two "
                  "for a few hundred to a few thousand dollars. Every one of them routinely goes "
                  "undone on claims where the disputed amount is six or seven figures, which is "
                  "the least rational feature of this industry."),

            ("h2", "The threshold nobody writes down"),
            ("p", "There is a second question that arrives once repairability is established: "
                  "whether a partial repair is the sensible outcome even when it is possible. "
                  "Replace eleven of thirty-four cabinet boxes and you have two mobilizations, a "
                  "visible line between old and new finish, and a warranty on a third of the "
                  "run. At some cost ratio that stops being a saving."),
            ("p", "Around 70% of the replacement cost is a reasonable place to have the "
                  "conversation, though it is a rule of thumb rather than a standard and it "
                  "varies by component. The useful move is to price both paths explicitly and "
                  "put the comparison in front of both parties, rather than defending a marginal "
                  "saving line by line."),
            ("html", '<a class="tlink" href="/tools/cabinet-repair-vs-replace-calculator/">'
                     'Compare the two paths <span class="arw">&rarr;</span></a>'),

            ("h2", "Matching, which is a different question again"),
            ("p", "Suppose half a run is genuinely repairable and half is not. Whether the "
                  "replacement half can be blended into the half that stays is not a "
                  "repairability question at all &mdash; it is an availability question, and it "
                  "is answered with documents rather than with judgment."),
            ("p", "Cabinet lines are discontinued constantly. Roof membranes change "
                  "formulation. Tile runs are dropped. Establishing that a product can no longer "
                  "be sourced takes manufacturer correspondence, a discontinued-product notice "
                  "or a supplier quote, and that paperwork is what converts a partial "
                  "replacement into a continuous-run replacement. Asserted without it, the "
                  "matching argument fails, and it deserves to."),
            ("quote", "Repairability is a finding. Matching is a document. Neither is an "
                      "opinion, and both get argued as though they were.",
             "From the claims desk"),

            ("h2", "What to do about it"),
            ("checks", [
                "Identify the disputed repair-or-replace decisions explicitly and list them. On a large file there are usually between five and fifteen, not forty.",
                "Price both paths for each one, so the comparison exists rather than being asserted.",
                "Get the physical evidence for the ones worth more than the cost of getting it &mdash; which is nearly all of them.",
                "Put manufacturer positions in writing. A letter declining to warrant a repaired system frequently ends the argument in a paragraph.",
                "Treat matching as a separate question with a documentary answer, and gather the correspondence before claiming it.",
                "Where a decision genuinely turns on judgment rather than measurement, say so, and record the basis on both sides.",
            ]),
            ("p", "None of this requires anyone to concede anything. It requires the question to "
                  "be asked in a form that has an answer, which is most of what an expert is "
                  "actually for."),
        ],
    },
    {
        "slug": "commercial-property-coinsurance-explained",
        "category": "Policy wording",
        "published": "2026-06-11",
        "modified": "2026-08-14",
        "read": "9",
        "words": 1450,
        "title": "Coinsurance on Commercial Property: The Clause That Cuts Claims",
        "description": ("How the coinsurance clause works on a commercial property policy, why "
                        "Texas institutions keep failing it, and the three ways to fix the "
                        "exposure before a loss."),
        "h1": "Coinsurance: the<br>clause nobody <em>reads</em>",
        "h1_plain": "Commercial property coinsurance explained",
        "blurb": ("It reduces every covered loss by the ratio of what you bought to what you "
                  "should have bought &mdash; and it hurts most on partial claims."),
        "lede": ("A church discovers it after a hailstorm. A district discovers it after a fire. "
                 "The damage is covered, the limit is nowhere near exhausted, and the payment is "
                 "still cut by a third. This is how that happens."),
        "body": [
            ("p", "Coinsurance is the most consequential clause in commercial property insurance "
                  "that almost no policyholder can describe. It sits on the declarations page as "
                  "a percentage next to each building&rsquo;s limit &mdash; 80%, 90%, sometimes "
                  "100% &mdash; and it does nothing at all until there is a claim."),

            ("h2", "What it actually does"),
            ("p", "The clause requires you to carry insurance of at least the stated percentage "
                  "of the property&rsquo;s value. If you do, losses are paid normally. If you do "
                  "not, every covered loss is reduced by the ratio of what you carried to what "
                  "you should have carried."),
            ("p", "The arithmetic is unforgiving and simple:"),
            ("table", "The coinsurance formula", ["Step", "Calculation"], [
                ["Required insurance", "Property value at the date of loss &times; coinsurance percentage"],
                ["Recovery ratio", "Limit carried &divide; required insurance"],
                ["Loss payable", "Amount of loss &times; recovery ratio, less the deductible"],
             ]),
            ("p", "Work an example. A sanctuary would cost $24 million to rebuild today. The "
                  "policy carries a $16 million limit with a 90% coinsurance clause. Required "
                  "insurance is $21.6 million; the ratio is 74%. A $3.2 million hail and water "
                  "loss &mdash; well within the limit, entirely covered &mdash; pays $2.37 "
                  "million before the deductible. The other $830,000 is uninsured, not because "
                  "of anything to do with the damage, but because of a number on a schedule."),
            ("html", '<a class="tlink" href="/tools/coinsurance-penalty-calculator/">'
                     'Run your own figures <span class="arw">&rarr;</span></a>'),
            ("callout", "The critical detail", [
                ("p", "The test is applied at the date of loss, using the property&rsquo;s value "
                      "then. Not the value when the policy was bound, not the value in the "
                      "appraisal from the last refinance. Construction costs move; the required "
                      "amount moves with them, and the limit does not."),
            ]),

            ("h2", "Why Texas institutions fail it so consistently"),
            ("p", "Three reasons, and none of them involve negligence."),
            ("h3", "Statements of value go stale"),
            ("p", "Most institutional schedules were assembled once, for a specific reason "
                  "&mdash; a bond issue, a refinance, a merger &mdash; and have been rolled "
                  "forward with a small annual inflation factor ever since. That factor has not "
                  "matched what actually happened to commercial construction costs in Texas "
                  "since 2020."),
            ("h3", "Buildings change and schedules do not"),
            ("p", "A congregation adds a family life center. A district encloses a breezeway and "
                  "buys the adjacent property. A city converts a warehouse into a maintenance "
                  "facility. Each of those changes the replacement value; none of them "
                  "automatically reaches the statement of values."),
            ("h3", "Nobody owns the number"),
            ("p", "The broker reports what the client supplies. The client assumes the broker "
                  "checks. The board approves a renewal summary that shows premium, not "
                  "adequacy. The value sits unexamined until a claim tests it, at which point "
                  "the carrier examines it very carefully indeed."),

            ("h2", "Three ways out, in order"),
            ("steps", [
                ("Agreed value",
                 "<p>An agreed value endorsement suspends the coinsurance clause for the policy "
                 "term in exchange for a signed statement of values the insurer accepts. It is "
                 "the cleanest solution available, it is frequently less expensive than people "
                 "expect, and a surprising number of institutions already have it and do not "
                 "know. Look at your declarations page before you do anything else.</p>"),
                ("Revalue and raise the limits",
                 "<p>A professional valuation, or at minimum a current cost-per-square-foot "
                 "review by construction class and occupancy. Then adjust the limits at renewal. "
                 "It costs premium, and it costs far less than a penalty applied to every claim "
                 "for the next five years.</p>"),
                ("Contest the value at claim time",
                 "<p>The fallback, and a legitimate one. The required amount depends on the "
                 "property&rsquo;s actual value at the date of loss, which is a question of "
                 "evidence rather than the carrier&rsquo;s assertion. Where a penalty is being "
                 "applied on a valuation that overstates what the building would really cost to "
                 "reproduce, that valuation is contestable &mdash; and on older or unusual "
                 "buildings it is frequently wrong.</p>"),
            ]),

            ("h2", "Two adjacent traps"),
            ("p", "Blanket coverage feels like the answer, and mostly it is: a blanket limit "
                  "responds anywhere on the schedule rather than trapping recovery at one "
                  "building&rsquo;s value. But blanket cover is usually conditioned on the "
                  "accuracy of the reported values, and a <strong>margin clause</strong> or "
                  "occurrence limit of liability endorsement can cap recovery at a fixed "
                  "percentage &mdash; commonly 110% or 115% &mdash; of the value reported for "
                  "the affected location. Understate the value and the blanket limit above it "
                  "becomes decorative."),
            ("p", "The second trap is <strong>functional replacement cost</strong>, which "
                  "appears frequently on older churches and civic buildings. It permits the "
                  "carrier to rebuild with modern equivalent materials rather than matching what "
                  "was there. It is not automatically wrong &mdash; for some buildings it is "
                  "sensible and cheaper &mdash; but it should be a decision the organization "
                  "made knowingly."),
            ("quote", "The cheapest hour in commercial insurance is the one spent reading the "
                      "declarations page while it can still be changed.",
             "From the claims desk"),

            ("h2", "What to do this week"),
            ("checks", [
                "Find the declarations page. Look at the figure next to each building&rsquo;s limit. If it says 80, 90 or 100, the clause is live.",
                "If it says agreed value, confirm the signed statement of values is current &mdash; that is the condition of the suspension.",
                "Get a current replacement cost per square foot for your construction class and occupancy, and multiply it out.",
                "Compare that figure against the limit, and apply the percentage. Now you know your ratio.",
                "If there is a shortfall, raise it with your broker at least 90 days before renewal, when something can still be done about it.",
            ]),
            ("p", "This is the rare insurance problem with a genuinely simple fix, available only "
                  "in advance. After a loss, all that remains is the argument."),
        ],
    },

    # =====================================================================
    {
        "slug": "documenting-a-commercial-hail-roof-claim",
        "category": "Field guide",
        "published": "2026-05-20",
        "modified": "2026-07-28",
        "read": "10",
        "words": 1550,
        "title": "Documenting a Commercial Hail Roof Claim in Texas",
        "description": ("Test cuts, soft-metal corroboration, storm data and maintenance records "
                        "&mdash; how to build a commercial hail roof claim that withstands a "
                        "carrier&rsquo;s engineering report."),
        "h1": "Hail damage the<br>engineer <em>cannot</em> dismiss",
        "h1_plain": "Documenting a commercial hail roof claim",
        "blurb": ("The carrier's engineer will write that the damage is wear. Here is the "
                  "evidence that makes that report untenable."),
        "lede": ("On a commercial roof, the difference between a paid claim and a denied one is "
                 "rarely the damage. It is whether anybody produced evidence in the first month "
                 "that a consulting engineer, retained in month four, cannot simply write around."),
        "body": [
            ("p", "Here is the sequence, and it is remarkably consistent. Storm in April. Claim "
                  "reported in May. Carrier&rsquo;s adjuster inspects in June, notes some "
                  "damage, and refers the matter to an engineering consultant. Report lands in "
                  "August concluding that the observed condition is consistent with normal "
                  "weathering and long-term deterioration rather than a discrete hail event. "
                  "Denial follows in September."),
            ("p", "That report is not fraudulent. It is a professional opinion assembled largely "
                  "from a visual inspection, four months after the event, on a roof that has "
                  "since had a Texas summer. Beating it requires evidence collected before it "
                  "was written."),

            ("h2", "What hail actually does to a commercial roof"),
            ("p", "Residential hail claims are argued over shingles, where impact is visible as "
                  "a bruise or a fracture on the surface. Commercial low-slope roofing fails "
                  "differently, and the difference is the whole argument."),
            ("p", "On a modified bitumen or single-ply membrane over rigid insulation, a "
                  "significant hailstone transmits energy through the membrane into the "
                  "insulation board beneath it. The board fractures. The membrane, being "
                  "flexible, may show only a faint bruise, displaced granules, or nothing "
                  "discernible from above. The roof does not leak. It has, however, lost a "
                  "material part of its remaining service life, and it will begin leaking in "
                  "eighteen months to three years as the bruised membrane weathers through."),
            ("p", "By which time the carrier has an easy and superficially reasonable position: "
                  "this roof is old, it is leaking, that is what old roofs do."),
            ("callout", "Which is why test cuts matter", [
                ("p", "A test cut is a small square removed through the full assembly, "
                      "photographed in place, then patched. It shows fractured insulation, "
                      "displaced granules and membrane damage directly, on the date it is taken. "
                      "It is the only direct evidence of what happened under the membrane, and "
                      "it is the piece of evidence carriers most often decline to propose."),
            ]),

            ("h2", "The five-part evidence package"),
            ("h3", "1. Test cuts, properly executed"),
            ("p", "Two to four per roof section, located to represent the full range of "
                  "condition rather than only the worst spots &mdash; a package that only "
                  "samples the damage invites the argument that the sample was selective. "
                  "Photograph the location on the roof plan, the cut in place, the removed "
                  "sample with a scale, and the patch. Have them taken by a qualified roofing "
                  "consultant, ideally with the carrier&rsquo;s representative present and "
                  "invited in writing."),
            ("h3", "2. Soft-metal corroboration"),
            ("p", "Hail large enough to damage a membrane leaves marks on softer surfaces all "
                  "over the property. Spatter on oxidised metal flashing, dents in gutters, "
                  "downspouts, gravel stops and coping, damage to vents, curbs and rooftop "
                  "mechanical cabinets, and impact on air-conditioning condenser fins. These "
                  "establish that stones of a given size landed here, on this date, from this "
                  "direction. They are also frequently a separate claim item in their own right."),
            ("h3", "3. Storm data for your coordinates"),
            ("p", "Not the regional summary and not the nearest official reporting station, "
                  "which may be fifteen miles away. Address-specific hail and wind data is "
                  "commercially available and inexpensive, and it either supports the reported "
                  "date of loss or tells you early that it does not &mdash; which is itself "
                  "worth knowing before you build a file."),
            ("h3", "4. Maintenance and condition history"),
            ("p", "The wear-and-tear defense depends on the roof having been in poor condition "
                  "already. Service records, prior inspection and infrared survey reports, "
                  "warranty documentation and repair invoices all rebut it. A roof under an "
                  "active manufacturer&rsquo;s warranty, inspected annually, is a very different "
                  "proposition from one nobody has walked in six years."),
            ("h3", "5. Dated imagery"),
            ("p", "Aerial and satellite imagery is available by date for most of urban Texas. "
                  "Before-and-after comparison around the date of loss is powerful, and it also "
                  "answers the intervening-storm argument in metros like Dallas&ndash;Fort Worth "
                  "where multiple hail events complicate attribution."),

            ("h2", "Reading their engineer&rsquo;s report"),
            ("p", "When the report arrives, read it for what it does not say. These documents "
                  "are usually more limited than their conclusions suggest, and the limitations "
                  "are stated in the methodology section that nobody reads."),
            ("table", "What to look for in a carrier&rsquo;s engineering report",
             ["Look for", "Why it matters"], [
                ["Scope of inspection", "Visual only? How many roof sections? Were test cuts taken, and if not, why not?"],
                ["Date of inspection", "How long after the loss? What weather intervened?"],
                ["Data sources", "Which weather station, and how far away? Was address-specific data used?"],
                ["Concessions", "Reports frequently acknowledge some storm-related damage while concluding it is not the primary cause. That concession is a starting point."],
                ["Assumptions about age and condition", "Often stated without documentary support. Your maintenance records are the answer."],
             ]),
            ("p", "Then get your own. Disagreement without a comparable expert report is just "
                  "disagreement, and a panel or a court will treat it that way."),

            ("h2", "Two arguments worth preparing for"),
            ("p", "<strong>Cosmetic damage exclusions.</strong> Some Texas commercial policies "
                  "exclude damage to roof surfacing that is merely cosmetic and does not affect "
                  "function. Where one applies, the entire claim becomes an argument about "
                  "function and remaining service life &mdash; which requires a manufacturer or "
                  "engineering opinion, not a contractor&rsquo;s letter."),
            ("p", "<strong>Repair versus replacement.</strong> The carrier will price patching. "
                  "The test is whether repair genuinely restores the roof to its pre-loss "
                  "condition and service life. Widespread insulation fracture beneath an intact "
                  "membrane usually cannot be patched back to a warrantable system, and the "
                  "manufacturer will often say so in writing. That letter frequently ends the "
                  "argument."),
            ("quote", "A test cut costs a few hundred dollars and patches in ten minutes. We have "
                      "watched that decision swing seven-figure claims.",
             "From the claims desk"),

            ("h2", "The short version"),
            ("checks", [
                "Get on the roof early, with a qualified consultant, and take test cuts.",
                "Photograph soft-metal corroboration everywhere on the property, not just the roof.",
                "Buy address-specific storm data for the date of loss before you build the claim.",
                "Assemble maintenance, inspection and warranty records &mdash; they are the answer to wear and tear.",
                "Invite the carrier&rsquo;s representative to the inspection in writing, and record that you did.",
                "Read their engineering report for its limitations before you respond to its conclusions.",
            ]),
        ],
    },

    # =====================================================================
    {
        "slug": "ordinance-and-law-coverage-explained",
        "category": "Policy wording",
        "published": "2026-04-14",
        "modified": "2026-07-02",
        "read": "9",
        "words": 1400,
        "title": "Ordinance and Law Coverage: Rebuilding to Code",
        "description": ("How ordinance or law coverage works in three parts, why the limits are "
                        "usually far too small on older Texas churches, schools and civic "
                        "buildings, and what to do about it."),
        "h1": "Rebuilding to<br><em>today&rsquo;s</em> code",
        "h1_plain": "Ordinance and law coverage explained",
        "blurb": ("A fire in a 1962 building triggers 2026 code. The gap between the two is "
                  "covered only to the extent somebody bought a limit for it."),
        "lede": ("This is the clause that decides large losses on older institutional buildings, "
                 "and the one where the default limit is most often set by nobody in particular, "
                 "years ago, without reference to what the building would actually require."),
        "body": [
            ("p", "A standard property policy pays to repair or replace what was damaged, with "
                  "materials of like kind and quality. It is a restoration promise: put the "
                  "building back the way it was."),
            ("p", "Building codes do not permit that. Once a repair exceeds whatever threshold "
                  "the local jurisdiction treats as substantial, the work &mdash; and sometimes "
                  "the entire structure &mdash; must be brought up to current requirements. "
                  "Sprinklers where there were none. Current egress widths and travel distances. "
                  "Accessibility. Energy code. Structural and wind provisions written decades "
                  "after the building went up."),
            ("p", "None of that is restoring the building to its prior condition, so none of it "
                  "is covered by the basic insuring agreement. Which is what ordinance or law "
                  "coverage exists to address."),

            ("h2", "The three parts"),
            ("p", "Ordinance or law coverage is conventionally written in three coverages, each "
                  "with its own limit. Understanding which is which is the difference between "
                  "thinking you are covered and being covered."),
            ("table", "The three coverages", ["Coverage", "What it pays for", "Common failure"], [
                ["A &mdash; Undamaged portion",
                 "The value of the undamaged part of the building that a law or ordinance requires you to demolish.",
                 "Frequently included within the building limit rather than in addition to it"],
                ["B &mdash; Demolition cost",
                 "The cost of demolishing that undamaged portion and removing the debris.",
                 "Limit set as a small percentage; badly undersized on large or contaminated structures"],
                ["C &mdash; Increased cost of construction",
                 "The additional cost of rebuilding to current code rather than to the prior specification.",
                 "The big one, and usually the most inadequate. Often 10% of the building limit"],
             ]),
            ("p", "On a $12 million school building, a 10% Coverage C limit is $1.2 million. Ask "
                  "your building official what a substantial renovation of a 1968 campus would "
                  "trigger &mdash; full fire suppression, current egress, accessibility "
                  "throughout, energy code envelope and mechanical upgrades &mdash; and you will "
                  "quickly establish whether $1.2 million is a serious number."),

            ("h2", "The enforcement question"),
            ("p", "Coverage generally responds to what the law actually requires and the "
                  "jurisdiction actually enforces, not to what would be nice to do while the "
                  "building is open. That distinction produces most of the disputes."),
            ("p", "Which makes one document unusually valuable: a written statement from the "
                  "building official setting out what the jurisdiction will require for this "
                  "repair, at this scale, on this building. It converts an argument about code "
                  "interpretation into a documented requirement. Ask for it early &mdash; it "
                  "routinely takes several weeks &mdash; and put the request in writing so the "
                  "timeline is on the record."),
            ("callout", "Watch the trigger threshold", [
                ("p", "Many jurisdictions set substantial improvement or substantial damage at a "
                      "percentage of the building&rsquo;s value &mdash; 50% is a common figure, "
                      "particularly in floodplain administration. Whether a repair crosses that "
                      "line can therefore depend on the valuation used, which means the scope "
                      "dispute and the code dispute are connected."),
            ]),

            ("h2", "Where it bites hardest in Texas"),
            ("p", "Three categories of institutional building are disproportionately exposed."),
            ("h3", "Mid-century churches and civic buildings"),
            ("p", "Assembly occupancies built before modern fire and life-safety codes. "
                  "Sprinklering an unsprinklered sanctuary, bringing egress up to current "
                  "standards and adding accessible routes can cost more than the fire that "
                  "triggered it. Historic designation narrows the options further."),
            ("h3", "Older school campuses"),
            ("p", "A 1970s campus undergoing substantial repair can face accessibility, egress, "
                  "fire alarm and suppression, and energy code work across the whole building. "
                  "On a multi-campus district hit by one storm, that exposure is repeated."),
            ("h3", "Any building with a low-slope roof"),
            ("p", "This one surprises people. A full roof tear-off frequently triggers current "
                  "energy code insulation requirements, which means thicker insulation than what "
                  "was there, which means extending mechanical curbs and raising rooftop units, "
                  "modifying drainage and possibly adding tapered insulation. That is ordinance "
                  "and law exposure on an ordinary hail claim, and it is regularly left off the "
                  "carrier&rsquo;s estimate entirely."),
            ("html", '<a class="tlink" href="/tools/commercial-roof-replacement-cost-estimator/">'
                     'Price a code-compliant re-roof <span class="arw">&rarr;</span></a>'),

            ("h2", "What to do about it"),
            ("steps", [
                ("Find out what you have",
                 "<p>Look for the ordinance or law endorsement on your policy and read the three "
                 "limits. If Coverage C is expressed as a percentage of the building limit, "
                 "multiply it out for your largest structures. Many institutions discover the "
                 "coverage is either absent or nominal.</p>"),
                ("Find out what you would need",
                 "<p>Ask your building official, in writing, what a substantial repair to your "
                 "principal buildings would trigger today. Then have a contractor or consultant "
                 "price that work. The comparison usually takes an afternoon and it is the most "
                 "useful pre-loss exercise an older institution can do.</p>"),
                ("Fix it at renewal",
                 "<p>Increasing ordinance and law limits is normally among the cheaper "
                 "adjustments available on a commercial property program, particularly relative "
                 "to the exposure it closes. Raise it 90 days out, with the numbers in hand.</p>"),
            ]),
            ("quote", "We have never seen an institution regret buying more ordinance and law "
                      "coverage. We have watched several discover, in the worst week of their "
                      "year, exactly how little 10% buys.",
             "From the claims desk"),
        ],
    },

    # =====================================================================
    {
        "slug": "building-a-business-interruption-claim",
        "category": "Time element",
        "published": "2026-03-10",
        "modified": "2026-06-19",
        "read": "10",
        "words": 1550,
        "title": "Building a Business Interruption Claim That Holds Up",
        "description": ("How commercial business interruption claims are actually calculated, "
                        "where carriers attack the assumptions, and the records to start keeping "
                        "on day one."),
        "h1": "The interruption claim,<br>built to <em>survive</em>",
        "h1_plain": "Building a business interruption claim",
        "blurb": ("Six variables, each contestable. The one that decides the number is the "
                  "period of restoration, and it is decided by your construction schedule."),
        "lede": ("Time-element losses are the largest under-recovered component of commercial "
                 "property claims, not because coverage is narrow, but because the proof is "
                 "assembled nine months late by people reconstructing events from memory."),
        "body": [
            ("p", "Property damage has a satisfying quality: you can photograph it, measure it "
                  "and price it. The income loss behind it has none of those properties. It is a "
                  "counterfactual &mdash; what the organization would have earned had the loss "
                  "not occurred &mdash; and counterfactuals are argued, not observed."),
            ("p", "Which is why the carrier retains a forensic accountant early, and why you "
                  "should too."),

            ("h2", "What the coverage actually pays"),
            ("p", "Business income coverage pays the net profit the operation would have earned "
                  "plus the continuing normal operating expenses it had to keep paying during "
                  "the period of restoration. It does not pay lost revenue &mdash; the most "
                  "common error in a first-draft claim &mdash; and it does not pay expenses that "
                  "stopped."),
            ("p", "Extra expense coverage pays costs incurred to continue operating or to speed "
                  "the repair, generally to the extent they reduce the overall loss. On many "
                  "institutional claims it is the larger half, because the instinct is always to "
                  "keep going at any cost."),
            ("table", "The six variables", ["Variable", "What it is", "How the carrier attacks it"], [
                ["Projected revenue", "What the operation would have earned.", "Your growth assumption was optimistic"],
                ["Margin", "The profit rate applied to lost revenue.", "Wrong definition used; policy defines it differently"],
                ["Continuing expenses", "Costs that ran while producing nothing.", "You should have cut them"],
                ["Saved expenses", "Costs that stopped.", "More was saved than you credited"],
                ["Period of restoration", "How long repair should reasonably have taken.", "It should have taken less time"],
                ["Extra expense", "Spend to keep going or speed repair.", "Not reasonable, not necessary, did not reduce the loss"],
             ]),

            ("h2", "The period of restoration is the whole argument"),
            ("p", "Read the definition in your policy. It does not say the period you were "
                  "actually closed. It says, in substance, the period that should reasonably be "
                  "required to repair or replace the damaged property, exercising due diligence "
                  "and dispatch. Those last four words carry the entire dispute."),
            ("p", "If the rebuild took nine months and the carrier&rsquo;s consultant opines it "
                  "should have taken five, the last four months are yours unless you can explain "
                  "them. And the explanations are almost always good ones: permitting, long-lead "
                  "equipment, the carrier&rsquo;s own delay in authorising a scope, specialist "
                  "trade availability after a regional catastrophe, code review, supply "
                  "constraints."),
            ("p", "But they have to be recorded as they happen. A construction schedule "
                  "maintained from week one, with the cause of every variance noted and dated, "
                  "is the single most valuable document in a time-element negotiation. "
                  "Reconstructing it afterwards from emails is possible and never as "
                  "persuasive."),
            ("callout", "Extended period of indemnity", [
                ("p", "Reopening is not recovery. Congregations, students, guests and customers "
                      "return gradually, and a policy without an extended period of indemnity "
                      "endorsement stops paying the day operations resume. Where the endorsement "
                      "exists, it typically covers a stated number of days of ramp-back. Check "
                      "for it on day one &mdash; it is frequently the last third of the claim."),
            ]),
            ("html", '<a class="tlink" href="/tools/business-interruption-calculator/">'
                     'Model the six variables <span class="arw">&rarr;</span></a>'),

            ("h2", "Setting up the capture"),
            ("p", "This takes your finance team about twenty minutes in week one and saves "
                  "months of argument."),
            ("checks", [
                "Open a separate general ledger account or cost code for all loss-related expenditure, and use it without exception.",
                "Log every incremental cost as it is incurred: overtime, temporary premises, rented equipment, expedited freight, additional staffing.",
                "Track what actually stopped &mdash; the saved-expenses credit will be proposed by the carrier, so propose it yourself first and correctly.",
                "Maintain a dated construction schedule with the cause of every delay noted.",
                "Preserve the operating data that establishes the baseline: two years of monthly performance, by department or revenue stream.",
                "Record the ramp-back after reopening, so the extended period can be quantified if the endorsement exists.",
            ]),

            ("h2", "Translating it for institutions"),
            ("p", "The vocabulary in the policy is commercial, and it maps onto institutional "
                  "operations with a little work."),
            ("table", "Institutional income streams that interrupt",
             ["Organization", "Interrupted streams"], [
                ["Church", "Tithes and offerings, facility rentals, pre-school and day-care fees, events, bookstore and cafe"],
                ["School district", "Cafeteria and athletics revenue, facility rentals, community education, extra expense for portables and bussing"],
                ["City", "Facility rentals, utility revenue, permit and program fees &mdash; but extra expense is usually the dominant component"],
                ["University", "Housing, dining, parking, athletics, conferences and summer camps, research continuity"],
                ["Hospital", "Case volume by department, measured at contribution margin rather than gross charges"],
             ]),
            ("p", "Public entities frequently assume there is nothing to claim because they do "
                  "not have revenue in the commercial sense. That is usually wrong on two "
                  "counts: auxiliary income streams do interrupt, and extra expense &mdash; the "
                  "cost of continuing to deliver the service &mdash; is often substantial and "
                  "recoverable."),

            ("h2", "When the carrier&rsquo;s accountant arrives"),
            ("p", "Treat it as a formal process from the first request. That accountant works "
                  "for the insurer, will ask for several years of financial records, and will "
                  "test every assumption you have made. That is their job and there is nothing "
                  "improper about it."),
            ("p", "What is unwise is responding informally: sending unreconciled spreadsheets, "
                  "answering questions verbally, or allowing document production to become "
                  "open-ended. Engage a qualified professional on your side, route the "
                  "production through one person, and put the methodology in writing before the "
                  "numbers are exchanged. On a claim of any size the cost of that is small "
                  "against the swing in the answer."),
            ("quote", "We have never seen a carrier dispute a time-element claim that was "
                      "documented weekly from day one. We have seen dozens dismantled that were "
                      "assembled in month nine.",
             "From the claims desk"),
        ],
    },

    # =====================================================================
    {
        "slug": "insurance-appraisal-vs-litigation-in-texas",
        "category": "Dispute resolution",
        "published": "2026-02-05",
        "modified": "2026-05-16",
        "read": "9",
        "words": 1400,
        "title": "Appraisal or Litigation on a Deadlocked Texas Claim",
        "description": ("When the appraisal clause is the right tool on a commercial property "
                        "claim, when it is the wrong one, and what the process actually involves "
                        "in Texas."),
        "h1": "Appraisal, or a<br><em>lawsuit</em>?",
        "h1_plain": "Appraisal vs litigation on a Texas insurance claim",
        "blurb": ("Appraisal resolves the amount of loss, fast and bindingly. It cannot resolve "
                  "coverage. Choosing wrong costs months."),
        "lede": ("Almost every commercial property policy contains an appraisal clause, and "
                 "almost no policyholder has read it. It is a contractual mechanism for breaking "
                 "a deadlock over how much the damage costs &mdash; and it is either exactly the "
                 "right tool or exactly the wrong one."),
        "body": [
            ("p", "The clause is usually a single paragraph. If the parties fail to agree on the "
                  "amount of loss, either may demand appraisal. Each selects a competent and "
                  "impartial appraiser. The two appraisers select an umpire, or a court appoints "
                  "one. Any two of the three who agree set the amount of loss, and that "
                  "determination binds both parties."),
            ("p", "That is the whole machine. Its simplicity is the point, and also the source "
                  "of every mistake made with it."),

            ("h2", "The distinction that governs everything"),
            ("p", "Appraisal decides <strong>how much</strong>. It does not decide "
                  "<strong>whether</strong>."),
            ("p", "A panel can determine that the loss amounts to $2.4 million and the carrier "
                  "can still decline to pay it on the basis that the cause of loss was excluded, "
                  "that notice was late, or that a condition was breached. In practice, paying "
                  "an appraisal award and then denying coverage is an awkward position for an "
                  "insurer to occupy &mdash; but it remains available, and a policyholder who "
                  "invokes appraisal expecting it to resolve a coverage dispute has bought "
                  "nothing."),
            ("table", "Which tool fits", ["The real dispute is...", "The route"], [
                ["We agree it is covered; we disagree about the cost.", "Appraisal. This is exactly what it is for."],
                ["They say the cause of loss is excluded.", "Coverage dispute. Counsel first."],
                ["They say notice was late or a condition was breached.", "Coverage dispute. Counsel first."],
                ["They have denied outright without meaningful investigation.", "Counsel. There may be extra-contractual exposure."],
                ["Partly a scope dispute, partly causation.", "Take advice. Texas panels often allocate between covered and non-covered causes, but how that is handled should be agreed up front."],
             ]),

            ("h2", "Why appraisal is often the better route"),
            ("p", "On a straightforward amount-of-loss dispute, appraisal is faster, cheaper and "
                  "more predictable than litigation by a wide margin. A well-run panel resolves "
                  "in weeks to a few months. The cost is your appraiser&rsquo;s fee and half the "
                  "umpire&rsquo;s &mdash; against years of discovery, depositions, expert "
                  "reports and motion practice."),
            ("p", "It also removes the dispute from a forum where the policyholder&rsquo;s "
                  "practical problem &mdash; the building is not repaired and the money is not "
                  "there &mdash; counts for nothing, and puts it in front of construction people "
                  "who look at the building."),
            ("p", "And for institutions, there is a governance advantage worth naming: appraisal "
                  "is a contractual process rather than public litigation against an insurer. "
                  "For a school board, a city council or a church membership, that is "
                  "frequently a materially easier thing to approve."),

            ("h2", "Why it sometimes is not"),
            ("p", "Finality cuts both ways. Texas courts generally uphold appraisal awards absent "
                  "fraud, accident, or the panel exceeding its authority &mdash; for instance by "
                  "deciding coverage rather than amount. If you go into an appraisal "
                  "under-prepared and the award comes back low, there is very little to be done "
                  "about it."),
            ("p", "There is also a strategic dimension. On a claim where the carrier&rsquo;s "
                  "handling has been poor enough to raise extra-contractual exposure, invoking "
                  "appraisal and accepting an award can affect the posture of that claim. This "
                  "is squarely a question for counsel, and it should be answered before the "
                  "demand is sent rather than afterwards."),
            ("callout", "The umpire decides the number", [
                ("p", "In a split panel, the umpire is the decision. Who is proposed, who is "
                      "resisted and what their background is &mdash; roofing, general "
                      "construction, engineering, forensic accounting &mdash; deserves as much "
                      "attention as everything else in the process combined. A great deal of "
                      "appraisal strategy is umpire selection."),
            ]),

            ("h2", "Preparing properly"),
            ("p", "The single biggest predictor of the outcome is the quality of the scope you "
                  "bring. A panel reconciles two positions; if yours is a contractor&rsquo;s "
                  "one-page proposal and theirs is a 60-page line-item estimate, the umpire has "
                  "very little to work with on your side."),
            ("checks", [
                "A complete, defensible line-item estimate in the industry-standard format, priced to your market.",
                "Photographic and measured documentation supporting every disputed line.",
                "Expert reports where causation or repairability is in issue &mdash; engineering, manufacturer, roofing consultant.",
                "A written summary of exactly which items are disputed and why, so the panel can work efficiently.",
                "An appraiser who knows your property type and can defend the estimate under challenge.",
                "Agreement, ideally in writing, on how the panel will treat causation allocation if it arises.",
            ]),
            ("p", "A large share of appraisals settle between the two appraisers before the "
                  "umpire ever rules. That outcome is usually a function of one side arriving "
                  "with a package the other cannot argue with."),
            ("quote", "Appraisal rewards preparation more than advocacy. The panel is looking at "
                      "the building, not listening to the speech.",
             "From the claims desk"),

            ("h2", "One practical note"),
            ("p", "Either party can invoke appraisal, and policyholders do so far less often than "
                  "insurers. That asymmetry is worth noticing. A well-documented policyholder "
                  "with a thorough scope and a competent appraiser is frequently in a strong "
                  "position in that forum &mdash; considerably stronger than in a correspondence "
                  "war with a claims department that has no deadline to meet."),
        ],
    },

    # =====================================================================
    {
        "slug": "who-is-who-on-a-commercial-property-claim",
        "category": "The basics",
        "published": "2026-01-15",
        "modified": "2026-06-04",
        "read": "9",
        "words": 1400,
        "title": "Who&rsquo;s Who on a Large Commercial Property Claim",
        "description": ("Staff adjuster, independent adjuster, public adjuster, consultant, "
                        "appraiser, umpire and forensic accountant &mdash; who each works for, "
                        "and what they actually decide."),
        "h1": "Who&rsquo;s who on a<br>large <em>property</em> claim",
        "h1_plain": "Who's who on a commercial property claim",
        "blurb": ("Eight roles, four paymasters and a great deal of confusion about which is "
                  "which. A map of who decides what."),
        "lede": ("By month three a large commercial loss can have a dozen professionals on it, "
                 "and most people on the file could not say with confidence who any of them "
                 "works for. It is worth knowing, because it tells you exactly how to read what "
                 "each one produces."),
        "body": [
            ("p", "The single most useful question to ask about anyone working a claim is not "
                  "how qualified they are. It is who pays them, and whether that payment moves "
                  "with the outcome. Everything else &mdash; how to weigh their report, what "
                  "they can and cannot decide, what they are likely to be challenged on "
                  "&mdash; follows from the answer."),

            ("h2", "The adjusters"),
            ("table", "Three kinds of adjuster",
             ["Role", "Paid by", "What they do"], [
                ["Staff adjuster",
                 "The insurer, as an employee.",
                 "Investigates, scopes and evaluates the claim for the insurer. Usually holds the settlement authority, or reports to whoever does."],
                ["Independent adjuster (IA)",
                 "The insurer, on contract.",
                 "The same work, outsourced &mdash; common after catastrophes and on specialist risks. &ldquo;Independent&rdquo; means independent of the payroll, not of the interest."],
                ["Public adjuster",
                 "The policyholder, usually a percentage of the recovery.",
                 "Prepares, presents and negotiates the claim as the policyholder&rsquo;s representative. Licensed separately; in Texas, under chapter 4102."],
             ]),
            ("p", "None of this is a criticism of anyone. A staff adjuster on a large loss is "
                  "frequently the most experienced person on the file. The point is structural: "
                  "each of these three is a party&rsquo;s representative, and their work should "
                  "be read as a position rather than as a finding."),

            ("h2", "The consultant"),
            ("p", "A claims consultant is retained to establish facts rather than to represent a "
                  "party. Damage assessment, scope, construction cost analysis, time-element "
                  "quantification, technical critique of somebody else&rsquo;s estimate. Either "
                  "side can retain one, and the useful ones are paid for the work rather than a "
                  "share of the result &mdash; because the moment the fee moves with the number, "
                  "the analysis becomes an argument and gets treated as one."),
            ("callout", "The question to ask a consultant", [
                ("p", "&ldquo;Who else have you worked for?&rdquo; If the answer is only ever "
                      "policyholders, or only ever carriers, their conclusions correlate with "
                      "their client list and any competent cross-examiner will establish that "
                      "quickly. It is the first question in a deposition for a reason."),
            ]),

            ("h2", "The appraisal panel"),
            ("p", "Most commercial property policies contain an appraisal clause: a contractual "
                  "mechanism for settling the amount of loss when the parties cannot agree. It "
                  "produces three roles and they are routinely confused with each other."),
            ("table", "The three appraisal roles",
             ["Role", "Appointed by", "What they decide"], [
                ["Party appraiser", "One party each. Must be competent and impartial, which is not the same as neutral about the evidence.", "Their own determination of the amount of loss, then negotiates with the other appraiser."],
                ["Umpire", "The two appraisers jointly, or a court if they cannot agree.", "Breaks the deadlock. Agreement between the umpire and either appraiser produces a binding award."],
                ["The panel as a whole", "&mdash;", "The amount of loss. Not coverage, not liability, not whether the policy responds at all."],
             ]),
            ("p", "That last row is the one people get wrong. An award of $2.4 million does not "
                  "decide that the insurer owes $2.4 million; it decides what the damage costs. "
                  "Coverage defences survive the award, at least in principle."),
            ("html", '<a class="tlink" href="/blog/insurance-appraisal-vs-litigation-in-texas/">'
                     'When appraisal is the right tool <span class="arw">&rarr;</span></a>'),

            ("h2", "The specialists"),
            ("checks", [
                "<strong>Forensic engineer.</strong> Retained by either side on causation and repairability. Read the methodology section before the conclusion &mdash; how many roof sections were examined, were test cuts taken, how far away was the weather station.",
                "<strong>Forensic accountant.</strong> Almost always appears on a time-element claim of any size, usually for the insurer first. Tests the revenue projection, the margin, the continuing and saved expenses and the period of restoration.",
                "<strong>Industrial hygienist.</strong> Contamination class, remediation protocol and post-remediation clearance. On healthcare and laboratory property their clearance letter, not an adjuster&rsquo;s opinion, is what returns the space to use.",
                "<strong>Cost estimator or roofing consultant.</strong> Produces or critiques the line-item scope. Where the dispute is about square footage and unit cost rather than causation, this is the person who resolves it.",
                "<strong>Coverage counsel.</strong> Interprets the policy. Nobody else on this list can, whatever they may say over the phone.",
            ]),

            ("h2", "Reading a report you did not commission"),
            ("p", "When an engineering or accounting report arrives from the other side, the "
                  "instinct is to argue with its conclusion. Read the rest of it first. These "
                  "documents are frequently more limited than their summaries suggest, and the "
                  "limits are stated plainly in the parts nobody reads."),
            ("checks", [
                "Scope of inspection &mdash; how much of the property, and by what method.",
                "Date, and what happened to the property between the loss and the visit.",
                "Data sources, and how specific to the property they are.",
                "Concessions &mdash; most reports acknowledge something, and that acknowledgement is a starting point.",
                "Assumptions stated without support, especially about age, prior condition and maintenance.",
                "What the author was actually asked to opine on, which is often narrower than the conclusion implies.",
            ]),
            ("quote", "The useful question about any report on a claim file is not whether it is "
                      "right. It is what it was asked, what it looked at, and who pays the "
                      "author.",
             "From the claims desk"),

            ("h2", "A short map"),
            ("table", "Who decides what", ["Question", "Who actually settles it"], [
                ["Is it covered?", "The policy &mdash; interpreted, if contested, by counsel and ultimately a court."],
                ["What was damaged?", "The scope document, built from a survey. Contested by competing experts."],
                ["What does it cost?", "The estimate, and failing agreement, an appraisal panel."],
                ["What caused it?", "Engineering evidence, and failing agreement, a court."],
                ["How long should it take?", "The construction schedule, tested by the other side&rsquo;s consultant."],
                ["What was the income loss?", "Forensic accounting, from the claimant&rsquo;s own records."],
            ]),
            ("p", "Most large files get stuck because one of those six questions is being argued "
                  "by people equipped to answer a different one. Working out which question is "
                  "actually in dispute, and who is qualified to close it, resolves more claims "
                  "than any amount of correspondence."),
        ],
    },
]

for _p in POSTS:
    _p["path"] = "/blog/%s/" % _p["slug"]
    _p["og_type"] = "article"
    _p["page_type"] = "Article"
