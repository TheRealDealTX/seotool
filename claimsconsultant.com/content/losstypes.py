"""The six kinds of loss we are brought in on.

These are causes of loss rather than services: what happened to the building.
What we are retained to do about it lives in content/services.py.
"""

from siteconfig import BIZ, STANDARDS, FEES

P = BIZ["phone_display"]

LOSS_TYPES = [

    {
        "slug": "commercial-property-damage-claims",
        "nav_label": "Commercial Property Damage",
        "card_title": "Commercial property damage claims",
        "card_blurb": ("The whole file, first notice to final release, scope, valuation, "
                       "documentation and negotiation."),
        "title": "Commercial Property Damage | Texas Claims Consultants",
        "description": "Expert witness and damage consulting for large commercial property damage in Texas. We scope, document and value the loss to an evidentiary standard.",
        "eyebrow": "Service &middot; Full claim representation",
        "h1": "Commercial losses,<br>established as <em>fact</em>",
        "h1_plain": "Commercial property damage claims",
        "lede": ("Insurers do not underpay large claims with a single dramatic decision. They do it "
                 "with forty small ones, each defensible on its own. The counter is not outrage. "
                 "It is a file built to the same standard, item by item, with an opposite "
                 "incentive behind it."),
        "head_aside": [
            ("ledger", "What full representation covers", [
                ("Policy analysis", "Day 1"),
                ("Site documentation", "Days 1&ndash;10"),
                ("Line-item estimate", "Weeks 2&ndash;5"),
                ("Experts engaged", "As warranted"),
                ("Proof of loss", "Prepared"),
                ("Negotiation", "To settlement"),
            ], "We do not hand you a report and leave. The engagement runs until the claim closes "
               "or you end it."),
        ],
        "sections": [
            {
                "eyebrow": "The gap",
                "h2": "Where the money goes missing.",
                "blocks": [
                    ("p", "Ask ten commercial policyholders why their settlement was short and most "
                          "will say the adjuster lowballed them. In our experience that is rarely "
                          "what happened. The estimate was produced competently, from a template, "
                          "by someone under production pressure who had ninety minutes on site and "
                          "no instruction to look for anything not immediately visible."),
                    ("p", "The result is a document that is accurate about what it contains and "
                          "silent about everything else. Silence is what costs money."),
                    ("table", "The eight recurring omissions", ["Item", "The carrier&rsquo;s position", "The counter-argument"], [
                        ["Overhead and profit",
                         "Not owed unless a general contractor is used.",
                         "Reasonably likely to be needed is the usual test, and three or more trades is the usual threshold. On commercial work it is nearly always met."],
                        ["Code and ordinance upgrades",
                         "Betterment. The policy pays to restore, not improve.",
                         "That is what Coverage B and C exist for. The question is the limit, not the entitlement."],
                        ["Matching of undamaged areas",
                         "Only the damaged slope, elevation or room is owed.",
                         "Turns on the policy wording and on proof the product is discontinued or cannot be reasonably matched."],
                        ["Depreciation on labor",
                         "Applied as a matter of course by the estimating software.",
                         "Labor does not wear out. Whether it may be depreciated turns on the valuation wording."],
                        ["Access, protection and containment",
                         "Overheads absorbed in unit cost.",
                         "Scaffolding, lifts, floor protection, dust control and after-hours working are real line items on occupied commercial property."],
                        ["Consultant and engineering fees",
                         "Not a covered cost of repair.",
                         "Where design professionals are required to permit and execute the repair, they are part of the cost of repair."],
                        ["Soft costs and general conditions",
                         "Folded into a percentage allowance.",
                         "On a job of any size, supervision, temporary utilities, permits and logistics are quantifiable and separately owed."],
                        ["Time-element loss",
                         "Left for later, then time-barred or forgotten.",
                         "Business income and extra expense must be documented from day one or they cannot be proved at all."],
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Method",
                "h2": "One survey, three documents, no improvisation.",
                "blocks": [
                    ("steps", [
                        ("Coverage analysis",
                         "<p>Declarations, forms, endorsements, schedule of values and any prior "
                         "loss history. We produce a written coverage summary before the site "
                         "visit: limits, sub-limits, deductible mechanics, valuation basis, "
                         "coinsurance or agreed value, ordinance and law, time-element structure, "
                         "and every condition that carries a deadline.</p>"),
                        ("Forensic documentation",
                         "<p>Measured survey of the whole property, not a sample. Photography "
                         "indexed by location. Drone and thermal where it earns its place. "
                         "Moisture mapping. Test cuts on roofing where the dispute will be about "
                         "membrane and insulation. Engineers, industrial hygienists, forensic "
                         "accountants and specialist trades engaged where the loss warrants them"
                         ", and not where it does not.</p>"),
                        ("Estimate and proof of loss",
                         "<p>A line-item estimate in the industry-standard platform, priced to "
                         "your market and your occupancy, with code work, soft costs, contents and "
                         "time-element carried separately. Then a sworn proof of loss that states "
                         "a number and starts the carrier&rsquo;s clock instead of waiting on "
                         "theirs.</p>"),
                        ("Negotiation, appraisal or referral",
                         "<p>Differences itemised in writing, positions dated, supplements filed "
                         "as actual costs come in. Where the gap is about the amount of loss and "
                         "will not close, appraisal. Where it is about coverage, we tell you it is "
                         "time for a lawyer, and we say so early.</p>"),
                    ]),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "Boundaries",
                "h2": "What we will not do.",
                "blocks": [
                    ("checks", [
                        "We do not give legal advice or hold ourselves out as attorneys. When a file needs counsel, we say so and step into a support role.",
                        "We do not take referral fees from contractors, and we do not direct repairs to a preferred vendor. You choose who does the work.",
                        "We do not inflate a scope. Every line has to survive an examination under oath and a forensic review, because on files this size it commonly gets one.",
                        "We do not take claims we cannot move. If the policy does not respond, we will tell you that in the first conversation instead of after you have signed.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("At what point in a claim should we bring you in?",
             "<p>Before the first inspection if you can, because the scope documented in week one "
             "is the scope everybody argues from afterwards. That said, the majority of our "
             "engagements start later &mdash; when an estimate arrives that is obviously short, "
             "when a file has gone quiet for months, or when a denial letter lands. All of those "
             "are workable. What is hard is a claim where repairs are complete, records "
             "are thin and the limitation period is close.</p>"),
            ("How much does it cost?",
             "<p>Hourly, or a fixed fee where the deliverable is well defined, agreed in writing "
         "before we start and quoted against a written estimate of hours. Public adjusting "
         "engagements, where we act as the policyholder&rsquo;s representative, are on a "
         "contingent fee capped by statute at 10%. See <a href=\"/fees/\">fees and engagement terms</a>.</p>"),
            ("Do we have to engage you for the whole matter?",
             "<p>No. Limited engagements are common on institutional files: the roofs only, the "
             "time-element loss only, the disputed supplement only. The engagement letter defines "
             "the scope and the fee applies to that scope.</p>"),
            ("Can you work with our attorney?",
             "<p>Routinely, and it is often the right structure. Counsel handles coverage, statutory "
             "remedies and litigation; we handle scope, valuation and the evidentiary record. On "
             "weather claims the pre-suit notice and inspection mechanics make that division of "
             "labor particularly useful.</p>"),
        ],
    },

    # ============================================================= wind ====,

    {
        "slug": "hurricane-and-windstorm-claims",
        "nav_label": "Hurricane &amp; Windstorm",
        "card_title": "Hurricane &amp; windstorm claims",
        "card_blurb": ("Named-storm deductibles, wind-versus-water causation, and coastal wording "
                       "that behaves differently from the rest of the state."),
        "title": "Hurricane &amp; Windstorm Losses | Texas Claims Consultants",
        "description": "Expert witness and damage consulting for Texas hurricane and windstorm losses on commercial property. Named storm deductibles, wind-versus-flood causation and TWIA.",
        "eyebrow": "Service &middot; Named storm",
        "h1": "Wind, water, and the<br>line <em>between</em> them",
        "h1_plain": "Hurricane and windstorm damage claims",
        "lede": ("After a named storm the coverage question is almost never whether you were "
                 "damaged. It is what damaged you. Wind is covered by the property policy; storm "
                 "surge generally is not. Carriers know exactly where that line sits, and so "
                 "should you."),
        "head_aside": [
            ("ledger", "Named storm mechanics", [
                ("Deductible", "% of values"),
                ("Trigger", "Named &amp; dated"),
                ("Wind-driven rain", "Conditioned"),
                ("Surge / flood", "Separate policy"),
                ("Anti-concurrent cause", "Usually present"),
                ("TWIA", "Coastal counties"),
            ], "A 5% named-storm deductible on a $30m schedule is $1.5m of retention. It changes "
               "the whole strategy."),
        ],
        "sections": [
            {
                "eyebrow": "Causation",
                "h2": "Anti-concurrent causation is the clause that decides coastal claims.",
                "blocks": [
                    ("p", "Most commercial property forms contain wording that excludes loss caused "
                          "directly or indirectly by an excluded peril, flood, for example"
                          ", regardless of any other cause contributing concurrently or in "
                          "any sequence. Read at its widest, an insurer will argue that clause "
                          "excludes damage where surge played any part at all, even to property "
                          "the wind had already opened up."),
                    ("p", "The practical answer is evidence, and it is time-sensitive. Water lines "
                          "on walls, debris deposition, the direction of structural failure, the "
                          "condition of the roof above the water line, and the timing of the wind "
                          "field relative to the surge all separate the two perils. Within ten "
                          "days, cleanup has destroyed most of it."),
                    ("checks", [
                        "Photograph high-water marks before anything is cleaned, with a scale and a location reference in the frame.",
                        "Document roof and upper-floor damage separately from ground-floor damage, wind losses above the water line are hard to attribute to surge.",
                        "Preserve a sample of affected materials where contamination class is likely to be disputed.",
                        "Obtain the storm data for your specific coordinates, not the regional summary: wind field, gust history, rainfall and surge timing.",
                        "Where flood and wind policies both respond, run them in parallel and keep the damage descriptions consistent.",
                    ]),
                ],
                "aside": [
                    ("callout", "Wind-driven rain", [
                        ("p", "Many commercial forms cover rain entering the building only if wind "
                              "first made an opening in the roof or walls. Proving that opening "
                              "existed, and that it was storm-created rather than a "
                              "pre-existing maintenance defect &mdash; is often the whole "
                              "interior claim."),
                    ]),
                    ("callout", "TWIA", [
                        ("p", "Property in the designated coastal counties may be written through "
                              "the Texas Windstorm Insurance Association, which has its own claim "
                              "handling procedure, its own deadlines and its own appeal and "
                              "dispute resolution path. Those procedures are not the same as a "
                              "standard carrier&rsquo;s, and missing one of their deadlines is "
                              "expensive."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Deductibles",
                "h2": "Work out your retention before you decide anything else.",
                "blocks": [
                    ("p", "Percentage deductibles are calculated on insured values rather than on "
                          "the size of the loss, so they do not scale down with a small claim. On "
                          "a multi-building institutional schedule the application matters as much "
                          "as the percentage: per occurrence, per building, or per occurrence with "
                          "a per-building minimum are three very different numbers for the same "
                          "storm."),
                    ("html", '<a class="tlink" href="/tools/commercial-claim-value-estimator/">'
                             'Model the retention against the loss <span class="arw">&rarr;</span></a>'),
                ],
            },
        ],
        "faqs": [
            ("The carrier says our damage is flood, which we do not have. Is that the end of it?",
             "<p>No, it is the beginning of an evidentiary argument. Very few coastal losses are "
             "purely one peril. The task is to separate what the wind did from what the water did "
             "and to establish the wind portion with evidence the carrier&rsquo;s engineer cannot "
             "dismiss, roof condition, interior damage above the water line, directional "
             "failure patterns, and the storm data for your location. Where anti-concurrent "
             "causation wording is being applied aggressively, that is a point at which counsel "
             "should be looking at the file alongside us.</p>"),
            ("How long after a hurricane can we still file?",
             "<p>Policies contain their own notice requirements, usually prompt notice, "
             "sometimes a specific number of days, and Texas weather claims are separately "
             "affected by the suit limitation in the policy. Late notice is a defense insurers "
             "raise often and win with sometimes, generally where they can show prejudice, and "
             "it is a question for counsel. What is certain is that evidence does not improve "
             "with age.</p>"),
            ("We already got a payment right after the storm. Can the claim be reopened?",
             "<p>Usually yes, as a supplemental claim, provided you have not signed a full and "
             "final release and the policy&rsquo;s time limits have not run. Early post-storm "
             "payments are typically issued on a rapid drive-by scope, and the real cost of repair "
             "emerges months later when contractors open the building up. That difference is what "
             "a supplement is for.</p>"),
        ],
    },

    # ============================================================= hail ====,

    {
        "slug": "hail-damage-claims",
        "nav_label": "Hail Damage",
        "card_title": "Hail damage claims",
        "card_blurb": ("Commercial roof systems, test cuts, and the wear-and-tear denial that "
                       "answers most Texas hail claims."),
        "title": "Commercial Hail Damage Claims | Texas Roof Consultants",
        "description": "Expert witness and damage consulting for commercial hail losses in Texas. Test cuts, membrane and insulation damage, HVAC coils, and the wear-and-tear denial.",
        "eyebrow": "Service &middot; Hail",
        "h1": "Hail damage you<br>cannot see from <em>the ground</em>",
        "h1_plain": "Commercial hail damage claims",
        "lede": ("Texas leads the country in hail losses, and the commercial version of the claim "
                 "is almost nothing like the residential one. The damage is to membrane, "
                 "insulation, coping and equipment, it is often invisible at grade, and the "
                 "standard denial is that your roof was simply old."),
        "head_aside": [
            ("ledger", "Proving a commercial hail loss", [
                ("Test cuts", "2&ndash;4 per section"),
                ("Soft metal spatter", "Corroborating"),
                ("HVAC coil damage", "Separate item"),
                ("Storm data", "By coordinate"),
                ("Maintenance history", "Rebuts wear"),
                ("Engineer", "Often needed"),
            ], "Test cuts are destructive, so they get resisted. They are also the only direct "
               "evidence of what happened beneath the membrane."),
        ],
        "sections": [
            {
                "eyebrow": "The evidence",
                "h2": "The membrane is intact. The insulation underneath is not.",
                "blocks": [
                    ("p", "On a modified bitumen or single-ply roof, a hailstone large enough to "
                          "matter does its damage by fracturing the insulation board and bruising "
                          "the membrane from beneath. The surface can look almost undisturbed. Two "
                          "years later the bruise weathers open and the building starts leaking, "
                          "by which point the carrier has an easy argument that this is age, not a "
                          "storm."),
                    ("p", "A test cut settles it. Four-inch squares taken through the assembly in "
                          "each roof section, photographed in place and then patched, show "
                          "fractured insulation, displaced granules and membrane damage directly. "
                          "Carriers rarely propose them and usually resist them, which tells "
                          "you how effective they are."),
                    ("p", "Around the roof, corroboration matters as much as the roof itself. "
                          "Spatter marks on oxidised metal, dented gutters and downspouts, damaged "
                          "coping and cap flashing, dinged vents and curbs, split gravel stops, "
                          "and hail impact on rooftop mechanical equipment all establish that "
                          "stones of a given size actually landed here, on this date, from this "
                          "direction."),
                ],
                "aside": [
                    ("callout", "HVAC coils", [
                        ("p", "Hail flattens condenser fins, which reduces airflow and efficiency "
                          "long before the unit fails outright. Carriers will offer comb-out. "
                          "Whether that restores the unit to pre-loss condition is a technical "
                          "question with a manufacturer&rsquo;s answer, and on a campus with "
                          "eighty rooftop units the difference between comb-out and replacement is "
                          "the largest single line on the estimate."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "The denial",
                "h2": "Answering &ldquo;wear and tear, not hail&rdquo;.",
                "blocks": [
                    ("table", "The four standard positions and how they break", ["Carrier position", "Evidence that answers it"], [
                        ["The roof was at the end of its service life anyway.",
                         "Maintenance records, prior roof survey reports, warranty status and photographs predating the storm. A serviceable 18-year-old roof that would have run another 7 years is a loss, not a write-off."],
                        ["The damage is cosmetic only.",
                         "Test cuts showing insulation fracture and membrane damage; manufacturer statements on how impact affects the remaining service life of that specific system."],
                        ["Hail of that size did not fall here.",
                         "Storm data for the property coordinates instead of the nearest reporting station, plus physical corroboration on soft metals and equipment at the site."],
                        ["The damage predates the policy period.",
                         "Sequential storm history, prior inspection reports, satellite and aerial imagery by date, and the condition of repairs made between events."],
                    ]),
                    ("callout", "Cosmetic damage exclusions", [
                        ("p", "Some Texas commercial policies carry a cosmetic damage exclusion "
                              "for roof surfacing, which removes coverage for dents that do not "
                              "affect function. Whether it applies is a factual question about "
                              "function and remaining service life, but you need to know "
                              "the endorsement is there before you build the claim, not after."),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("How long do we have to file a hail claim in Texas?",
             "<p>Two separate clocks run. The policy requires prompt notice, and some forms now "
             "state a specific reporting window for weather losses. Separately, the policy&rsquo;s "
             "suit limitation, commonly two years in Texas, and governed for many weather "
             "caps how long there is to sue, and that is a question for counsel. Delay is also an "
             "evidentiary problem: the longer the wait, the easier the intervening-storm "
             "argument becomes.</p>"),
            ("Can you tell whether we have a claim before we report it?",
             "<p>That is usually the right sequence on a commercial roof. A pre-notice inspection "
             " (roof survey, test cuts where appropriate, storm data for the address) "
             "tells you whether the damage clears your deductible and whether it will survive a "
             "wear-and-tear challenge. Reporting a claim you then abandon still shows up in your "
             "loss history.</p>"),
            ("Our roof is 20 years old. Is it worth pursuing?",
             "<p>Sometimes very much so, and sometimes not. Age affects depreciation and it affects "
             "the wear argument, but a roof at 20 years on a 30-year system that was maintained "
             "and functioning is still a covered loss when hail ends its service life early. What "
             "usually decides it is the valuation basis: replacement cost with recoverable "
             "depreciation is a fundamentally different claim from actual cash value on a roof "
             "that age.</p>"),
        ],
    },

    # ============================================================= fire ====,

    {
        "slug": "commercial-fire-claims",
        "nav_label": "Fire &amp; Smoke",
        "card_title": "Commercial fire &amp; smoke claims",
        "card_blurb": ("Where the smoke, water and code exposure reach far beyond anything that "
                       "burned."),
        "title": "Commercial Fire Damage Claims | Texas Consultants",
        "description": "Expert witness and damage consulting for commercial fire and smoke losses in Texas. Smoke residue, code upgrades, contents and business interruption.",
        "eyebrow": "Service &middot; Fire &amp; smoke",
        "h1": "Most fire damage<br>is not <em>burned</em>",
        "h1_plain": "Commercial fire and smoke damage claims",
        "lede": ("A contained fire in a mechanical room can produce a seven-figure claim without "
                 "spreading past the door. Smoke migrates through every return air path in the "
                 "building, suppression water finds three floors below, and the rebuild triggers "
                 "codes that did not exist when the building went up."),
        "head_aside": [
            ("ledger", "Fire loss components", [
                ("Burn area", "Smallest"),
                ("Smoke &amp; odour", "Building-wide"),
                ("Suppression water", "Downward"),
                ("Code upgrade", "Ord. &amp; law"),
                ("Contents", "Item by item"),
                ("Downtime", "Months"),
            ], "The estimate that only scopes the room that burned is the one to be suspicious of."),
        ],
        "sections": [
            {
                "eyebrow": "Smoke",
                "h2": "Smoke is a chemistry problem, not a cleaning problem.",
                "blocks": [
                    ("p", "What burned determines what the residue is and how it must be treated. "
                          "Protein fires from a kitchen leave a thin, foul, almost invisible film "
                          "that defeats ordinary cleaning. Plastics and electronics produce acidic "
                          "residues that continue to corrode metal, circuit boards and wiring for "
                          "months after the fire is out. Neither is remedied by wiping surfaces "
                          "and running a hydroxyl machine for a week."),
                    ("p", "The distinction matters because it decides whether an item is cleaned, "
                          "restored or replaced, and that decision, multiplied across a "
                          "contents inventory or a building&rsquo;s electrical and mechanical "
                          "systems, is usually the largest disputed number in the claim. "
                          "Independent testing for residue type and distribution costs relatively "
                          "little and settles arguments that otherwise run for months."),
                    ("checks", [
                        "Residue sampling and analysis before cleaning begins, at multiple locations including inside HVAC and above ceilings.",
                        "Corrosion assessment on electrical distribution, controls, servers and any exposed metal.",
                        "Air-handling systems inspected internally &mdash; ductwork is the most common route for building-wide contamination and the most common omission.",
                        "Odour treated as a completion standard with an objective test, not as a matter of opinion at walkthrough.",
                        "Contents inventoried item by item before anything is discarded, with photographs and a documented restore-or-replace decision on each.",
                    ]),
                ],
                "aside": [
                    ("callout", "Suppression water travels", [
                        ("p", "Sprinkler and hose water goes down, and it goes into wall cavities "
                              "and floor assemblies where it will sit. Moisture mapping of the "
                              "floors below the fire is not optional on a commercial building, and "
                              "a fire claim that contains no water damage scope in the levels "
                              "beneath the burn is an incomplete claim."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Code",
                "h2": "Rebuilding an older building means building it to today&rsquo;s code.",
                "blocks": [
                    ("p", "Once repair work passes the threshold the local jurisdiction treats as "
                          "substantial, the whole structure can be pulled up to current "
                          "requirements, sprinklers, fire alarm, egress, accessibility, "
                          "energy code, structural provisions, sometimes wind and seismic detailing "
                          "that did not exist at construction. On a mid-century civic building, "
                          "church or campus structure, that cost can rival the fire damage itself."),
                    ("p", "Ordinance or law coverage exists precisely for this, and it usually "
                          "comes in three parts: the value of the undamaged portion that must be "
                          "demolished, the cost of demolition and debris removal, and the "
                          "increased cost of construction. Each has its own limit. Those limits "
                          "are commonly set as a small percentage of the building limit, chosen "
                          "years ago by someone who was not imagining this fire."),
                    ("callout", "Get the code official&rsquo;s position in writing", [
                        ("p", "A letter from the building official stating what the jurisdiction "
                              "will require is worth more in a negotiation than any amount of "
                              "argument about what the code says. Ask for it early; it takes weeks."),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("The fire was small. Why is the claim taking so long?",
             "<p>Because the burn area is usually the simplest part. Establishing the extent of "
             "smoke migration, deciding restore-versus-replace across a contents inventory, "
             "identifying what code will require on rebuild, and quantifying the interruption loss "
             "all take time, and the carrier will investigate origin and cause before it commits "
             "to anything. A commercial fire claim of any size running six to twelve months is "
             "normal; running two years usually means something is stuck.</p>"),
            ("Should we start cleaning before the adjuster comes?",
             "<p>Do what is needed to make the property safe and to prevent further damage, "
             "that is your duty under the policy and it is not optional. Beyond that, document "
             "before you disturb. Photograph everything, keep damaged items until they have been "
             "inventoried, and retain a sample of anything you must dispose of. The most damaging "
             "thing an owner can do after a fire is tidy up efficiently.</p>"),
            ("Can we use our own restoration contractor?",
             "<p>Yes. You choose who performs the work; the carrier chooses what it is prepared to "
             "pay. Be careful with direction-to-pay agreements and assignments of benefit signed "
             "in the first forty-eight hours, when the restoration company is on site and you are "
             "not thinking clearly. Read what you sign, or let us read it.</p>"),
        ],
    },

    # ============================================================ water ====,

    {
        "slug": "water-damage-and-freeze-claims",
        "nav_label": "Water &amp; Freeze",
        "card_title": "Water damage &amp; freeze claims",
        "card_blurb": ("Pipe bursts, roof leaks and freeze events, where the exclusion "
                       "wording does most of the work."),
        "title": "Commercial Water &amp; Freeze Losses | Texas Consultants",
        "description": "Expert witness and damage consulting for commercial water and freeze losses in Texas. Burst pipes, sprinkler leaks, roof leaks and the exclusions carriers use.",
        "eyebrow": "Service &middot; Water &amp; freeze",
        "h1": "Water claims are<br>won in the <em>exclusions</em>",
        "h1_plain": "Commercial water damage and freeze claims",
        "lede": ("Almost every commercial policy covers sudden and accidental water discharge and "
                 "almost every one excludes repeated seepage, wear, faulty maintenance and, in "
                 "many cases, freeze damage where the building was left unheated. Which side of "
                 "that line your loss falls on is decided by the facts you can prove."),
        "head_aside": [
            ("ledger", "What the carrier will ask", [
                ("Date of discharge", "Exact"),
                ("Duration", "Hours or weeks?"),
                ("Heat maintained", "Records"),
                ("System drained", "If vacant"),
                ("Maintenance history", "Documented"),
                ("Cause of failure", "Engineer"),
            ], "Every one of these is answerable with records you already have &mdash; if somebody "
               "collects them in the first week."),
        ],
        "sections": [
            {
                "eyebrow": "Freeze",
                "h2": "After a Texas freeze, the fight is about what you did, not what happened.",
                "blocks": [
                    ("p", "The February 2021 freeze taught Texas commercial policyholders something "
                          "they had not needed to know: many property forms exclude loss from water "
                          "that freezes in a plumbing or sprinkler system unless the insured "
                          "maintained heat in the building, or drained the system and shut off the "
                          "supply. Buildings that lost power for four days lost heat for reasons "
                          "outside their control, and carriers have litigated that distinction "
                          "hard ever since."),
                    ("p", "What wins these claims is contemporaneous evidence of reasonable care: "
                          "building management system logs showing setpoints and interior "
                          "temperatures, utility outage records for the specific address, work "
                          "orders and staffing records for the freeze period, and any written "
                          "winterisation procedure that was followed. Most institutions "
                          "have all of this and have never thought to assemble it."),
                    ("checks", [
                        "BMS and thermostat logs exported before they roll off, many systems retain only 30 to 90 days.",
                        "Utility outage confirmation for the property address and the exact period.",
                        "Staffing, security and work-order records showing the building was attended and monitored.",
                        "Photographs of the failure point before the plumber cuts it out, and retention of the failed component itself.",
                        "Any winterisation checklist, vendor contract or standard operating procedure in force at the time.",
                    ]),
                ],
                "aside": [
                    ("callout", "Keep the pipe", [
                        ("p", "The single most valuable physical object in a water claim is the "
                              "failed component. Once the plumber removes it, ask for it, label "
                              "it, photograph it and put it in a box. Where the cause of failure "
                              "is disputed, and where product liability or subrogation may "
                              "be in play. That piece of pipe is the evidence."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Long-term seepage",
                "h2": "&ldquo;It has been leaking for years&rdquo; is a coverage defense, not an observation.",
                "blocks": [
                    ("p", "When a carrier says the damage resulted from repeated seepage or "
                          "leakage over a period of weeks or more, it is invoking a specific "
                          "exclusion, and the burden of proving the exclusion applies generally "
                          "sits with the insurer. That is worth remembering, because the argument "
                          "is usually made as though it were self-evident."),
                    ("p", "Rebutting it is a matter of records: maintenance logs showing the area "
                          "was inspected and dry, water bills without an unexplained rise, tenant "
                          "or staff complaint history showing when the problem first appeared, and "
                          "material condition analysis distinguishing a recent saturation event "
                          "from long-term staining and microbial growth."),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "Mould",
                "h2": "Remediation limits are usually far smaller than people assume.",
                "dek": "Texas commercial forms often sub-limit fungus and mould remediation "
                       " (sometimes to $15,000 or $25,000) regardless of the building "
                       "limit above it.",
                "blocks": [
                    ("p", "That sub-limit is one reason speed matters on a water loss. Where mould "
                          "results from a covered water event and is addressed as part of drying "
                          "and repair within a reasonable time, the work is typically part of the "
                          "repair. Where it is left to develop, the carrier will reclassify the "
                          "cost against the remediation sub-limit and the exposure lands on you. "
                          "Document the drying, log the readings, and get to dry standard on the "
                          "record."),
                ],
            },
        ],
        "faqs": [
            ("Our building lost heat because the power failed. Is the freeze damage excluded?",
             "<p>It depends on the exact wording and on what you can show. Many forms condition "
             "coverage on the insured using reasonable care to maintain heat, which is not the "
             "same as guaranteeing heat. Where the outage was utility-wide, outside your control, "
             "and you can demonstrate the building was heated and monitored up to the failure, "
             "that is a strong position. Where a building was vacant, unmonitored and never "
             "winterised, it is a much harder one. The records decide it.</p>"),
            ("How fast does a water claim need to be reported?",
             "<p>Immediately, and mitigation should begin at once regardless of whether an adjuster "
             "has been out. Every property policy imposes a duty to protect the property from "
             "further damage, and failing it gives the carrier a defense on the additional damage "
             "that followed. Photograph first, then dry.</p>"),
            ("The carrier is only paying to dry the building, not to repair the finishes.",
             "<p>A common midpoint, and usually incomplete. Drying is mitigation; it is not repair. "
             "Once the structure is dry, the claim still owes removal and replacement of materials "
             "that cannot be restored, reinstatement of finishes, and any code-driven work the "
             "repair triggers. Where flooring, cabinetry or wall systems have been partially "
             "removed, matching becomes the argument.</p>"),
        ],
    },

    # ================================================ business interruption =,

    {
        "slug": "business-interruption-claims",
        "nav_label": "Business Interruption",
        "card_title": "Business interruption &amp; extra expense",
        "card_blurb": ("The half of the claim that is documented worst and disputed hardest, "
                       "because nobody was recording it while it happened."),
        "title": "Business Interruption Claims | Texas Consultants",
        "description": "Expert witness and damage consulting for Texas business interruption and extra expense. Period of restoration, continuing expenses, civil authority and contingent BI.",
        "eyebrow": "Service &middot; Time element",
        "h1": "The loss that keeps<br>running after the <em>water stops</em>",
        "h1_plain": "Business interruption and extra expense claims",
        "lede": ("Property damage is visible and finite. The income loss behind it is neither, "
                 "which is why it is the part of a commercial claim most often left unquantified"
                 ", and, when it finally is quantified, most often disputed line by line by "
                 "a forensic accountant the carrier retained months earlier."),
        "head_aside": [
            ("ledger", "The four variables", [
                ("Period of restoration", "Disputed"),
                ("Revenue projection", "Trend-adjusted"),
                ("Continuing expenses", "Proven"),
                ("Saved expenses", "Deducted"),
                ("Extra expense", "Documented"),
                ("Waiting period", "Check form"),
            ], "Change the period of restoration by two months and the whole number changes. That "
               "is where the argument goes."),
        ],
        "sections": [
            {
                "eyebrow": "Period of restoration",
                "h2": "How long should it have taken to rebuild?",
                "blocks": [
                    ("p", "Business income coverage does not pay for as long as you were "
                          "closed. It pays for the period it should reasonably have taken to "
                          "repair or replace the damaged property, exercising due diligence and "
                          "dispatch. Those are the words that carry the argument. If the carrier "
                          "says the rebuild should have taken five months and it took nine, the "
                          "last four months are yours unless you can explain them."),
                    ("p", "Which means the reasons for every delay have to be on the record as they "
                          "happen: permitting timelines, long-lead equipment, the carrier&rsquo;s "
                          "own delay in authorising scope, supply constraints, code review, "
                          "specialist trade availability. A construction schedule maintained from "
                          "week one, with the causes of variance noted, is the single most useful "
                          "document in a time-element negotiation."),
                    ("callout", "Extended period of indemnity", [
                        ("p", "Reopening is not recovery. Customers, students, congregations and "
                              "guests come back gradually. Many policies offer an extended period "
                              "of indemnity endorsement covering that ramp-back for a stated "
                              "number of days after operations resume. Whether you have one, and "
                              "how long it runs, is worth checking on day one. It is "
                              "commonly the last third of the claim."),
                    ]),
                ],
                "aside": [
                    ("callout", "Set up the capture immediately", [
                        ("p", "A separate general ledger account for loss-related costs, opened in "
                              "the first week, will save more argument than any amount of "
                              "reconstruction later. Every invoice, every overtime hour, every "
                              "rented piece of equipment coded to that account is a line the "
                              "accountant cannot question the provenance of."),
                    ]),
                    ("html", '<a class="tlink" href="/tools/business-interruption-calculator/">'
                             'Model your interruption loss <span class="arw">&rarr;</span></a>'),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Coverage parts",
                "h2": "Six extensions that pay when the main grant does not.",
                "blocks": [
                    ("table", "Time-element extensions worth checking", ["Extension", "What triggers it", "Typical constraint"], [
                        ["Extra expense", "Costs incurred to continue operating or to speed the repair.", "Must reduce the overall loss; reasonableness is tested"],
                        ["Civil authority", "An order of civil authority prohibiting access to your premises.", "Usually requires covered physical damage nearby; short duration; waiting period"],
                        ["Ingress / egress", "Physical obstruction of access, without an official order.", "Not on every form; radius and duration limits"],
                        ["Dependent property (contingent BI)", "Damage at a named supplier, customer or attraction property.", "Property often must be scheduled by name; sub-limited"],
                        ["Service interruption", "Off-premises failure of power, water, gas or communications.", "Often requires physical damage to the utility&rsquo;s property; may exclude overhead transmission lines"],
                        ["Extended period of indemnity", "The ramp-back after operations resume.", "Fixed number of days; must be endorsed"],
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Our organization is a nonprofit. Is there anything to claim?",
             "<p>Usually yes, and it is often missed because the revenue is not called "
             "revenue. Tithes and offerings, tuition and program fees, facility rentals, event "
             "income, dining and bookstore receipts, camp and conference bookings, these are "
             "income streams that interrupt. Whether they are covered depends on the form, and "
             "nonprofit-specific programs often address them explicitly. Read the endorsements.</p>"),
            ("The carrier retained a forensic accountant. Should we be worried?",
             "<p>Not worried, but you should stop treating the process as informal. That accountant "
             "works for the insurer and will request years of financial records, test every "
             "assumption in your projection and propose their own. The correct response is a "
             "similarly qualified professional on your side, engaged early, with the production of "
             "records managed rather than open-ended. On a claim of any size the cost of that is "
             "small relative to the swing.</p>"),
            ("How is the loss actually calculated?",
             "<p>In outline: project the revenue the operation would have earned during the period "
             "of restoration, using its own trend and any relevant market benchmark; subtract "
             "revenue earned; apply the appropriate margin so you are claiming lost "
             "earnings instead of lost turnover; add expenses that continued but produced nothing; "
             "subtract expenses saved; add extra expense reasonably incurred. Every one "
             "of those six steps is a place where reasonable professionals disagree, which is why "
             "the claim is worth building properly.</p>"),
        ],
    },

    # ======================================================== appraisal ====,
]

for _l in LOSS_TYPES:
    _l["path"] = "/loss-types/%s/" % _l["slug"]
