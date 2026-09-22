"""What we are retained to do.

Ordered the way engagements actually arrive: testimony and causation first,
then the estimating and appraisal work, then the three technical report types
we are asked for by name, then representation and pre-loss work.

Loss types &mdash; hail, fire, water, wind &mdash; live in content/losstypes.py.
"""

from siteconfig import BIZ, STANDARDS, FEES

P = BIZ["phone_display"]

SERVICES = [

    # ========================================================= expert witness
    {
        "slug": "expert-witness-and-litigation-support",
        "nav_label": "Expert Witness",
        "card_title": "Expert witness &amp; litigation support",
        "card_blurb": ("Reports, rebuttals, deposition and trial testimony on damage, scope, "
                       "causation and cost &mdash; for either side."),
        "title": "Property Damage Expert Witness | Texas Litigation Support",
        "description": ("Expert witness and litigation support on Texas property damage: scope, "
                        "cost, causation and estimate critique. Reports, depositions and trial "
                        "testimony for either party."),
        "eyebrow": "Service &middot; Testimony",
        "h1": "An opinion that<br>survives <em>cross</em>",
        "h1_plain": "Expert witness and litigation support",
        "lede": ("The question that decides an expert&rsquo;s value is not what they concluded. "
                 "It is what happens when a competent attorney spends two hours trying to take "
                 "the conclusion apart. Everything about how we work is built backwards from "
                 "that afternoon."),
        "head_aside": [
            ("ledger", "Engagement facts", [
                ("Retained by", "Either party"),
                ("Fee basis", "Hourly"),
                ("Prior testimony", "Disclosed"),
                ("Conflict check", "Before intake"),
                ("Report standard", "TRE 702"),
            ], "Expert work is billed hourly. It is the first question on cross and it should "
               "have a boring answer."),
        ],
        "sections": [
            {
                "eyebrow": "The standard",
                "h2": "Reliability is a method question, not a credentials question.",
                "blocks": [
                    ("p", "Texas Rule of Evidence 702 lets a qualified expert give opinion "
                          "testimony where it will help the trier of fact, and Texas courts test "
                          "that opinion for reliability and relevance. In practice the challenge "
                          "is rarely aimed at whether the witness is qualified. It is aimed at "
                          "the gap between the data and the conclusion &mdash; whether the method "
                          "can be described, whether it was actually followed, and whether "
                          "someone else applying it would reach the same place."),
                    ("p", "That has consequences for how a file is built long before anyone files "
                          "anything. Measurements have to be recorded, not remembered. "
                          "Assumptions have to be stated as assumptions. Photographs have to be "
                          "indexed to locations. Where a conclusion rests on something we did not "
                          "personally observe, the report has to say so."),
                    ("p", "The corollary is that we will not write an opinion we cannot defend. "
                          "If the evidence does not support the position the retaining party "
                          "wants, we say so in the first conversation, in writing if it helps, "
                          "and the engagement ends there. That is a cheaper outcome than a "
                          "withdrawn expert in month nine."),
                ],
                "aside": [
                    ("callout", "The credibility ledger", [
                        ("p", "Every expert accumulates a record: who retained them, what they "
                              "concluded, how often those two correlate. Ours is deliberately "
                              "mixed, because a witness whose opinions always favor the paying "
                              "side is an advocate with a CV. Prior engagements and testimony are "
                              "disclosed on request &mdash; and to opposing counsel as a matter "
                              "of course."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Deliverables",
                "h2": "What an engagement actually produces.",
                "blocks": [
                    ("table", "Work product", ["Deliverable", "What it contains", "Typical stage"], [
                        ["Preliminary assessment",
                         "A short written view on whether the position is supportable, before anyone commits to a report.",
                         "Pre-suit, or on first review of the file"],
                        ["Expert report",
                         "Qualifications, materials reviewed, methodology, observations, opinions and the basis for each, with photographic and measurement appendices.",
                         "Per the scheduling order"],
                        ["Rebuttal report",
                         "A methodology-level critique of the opposing expert: scope of inspection, data sources, assumptions, internal consistency, and what the report does not say.",
                         "After opposing disclosure"],
                        ["Estimate variance analysis",
                         "Line-by-line reconciliation of two competing estimates, showing where the difference actually sits and how much each disputed item is worth.",
                         "Mediation and appraisal prep"],
                        ["Deposition",
                         "Preparation, testimony, and a written note of anything the deposition changed in our view.",
                         "Discovery"],
                        ["Trial testimony &amp; demonstratives",
                         "Direct and cross testimony, with exhibits built to be understood by people who have never walked the building.",
                         "Trial"],
                    ]),
                    ("callout", "Working through counsel", [
                        ("p", "On matters heading to litigation, engagement through counsel "
                              "rather than directly through the party is common. How that affects "
                              "privilege, work product and discoverability is a question for the "
                              "attorney; we simply follow whatever structure they set and keep "
                              "our file accordingly."),
                    ]),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "Scope of opinion",
                "h2": "What we will and will not opine on.",
                "blocks": [
                    ("checks", [
                        "<strong>Will:</strong> the extent of physical damage, the scope of work required to repair it, the reasonable cost of that work, and whether an opposing estimate is complete.",
                        "<strong>Will:</strong> causation within our competence &mdash; hail versus wear, wind versus water, freeze versus long-term seepage, impact versus settlement.",
                        "<strong>Will:</strong> the period reasonably required to repair, and the documentary basis of a time-element calculation.",
                        "<strong>Will not:</strong> interpret the policy or opine on coverage. That is counsel&rsquo;s work and a court&rsquo;s.",
                        "<strong>Will not:</strong> opine on structural engineering, industrial hygiene or accounting where those require a separate licensed discipline. We identify what is needed and work alongside it.",
                        "<strong>Will not:</strong> accept an engagement where the conclusion is specified in advance.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Do you testify for policyholders or for insurers?",
             "<p>Both, and not in fixed proportion. It is the single most useful thing about the "
             "practice and the single most awkward thing to establish if you have never done it "
             "&mdash; which is why firms that start on one side tend to stay there. Prior "
             "engagements are disclosed, and if either party is uncomfortable with our history "
             "they should say so early.</p>"),
            ("How is expert work billed?",
             "<p>Hourly, at a posted rate, with testimony time billed at the same rate whether "
             "the testimony helps or not. Public adjusting engagements are contingent, but that "
             "is a different capacity and a different kind of work &mdash; expert and consulting "
             "engagements are not.</p>"),
            ("Can you review another expert&rsquo;s report without producing one of your own?",
             "<p>Yes, and it is a common and inexpensive first engagement. A methodology review "
             "of an opposing report frequently tells counsel what they need to know &mdash; "
             "whether the opinion is vulnerable, and on what ground &mdash; without the cost of a "
             "full competing analysis.</p>"),
            ("How late can we bring you in?",
             "<p>Later than is ideal, usually. The binding constraints are the scheduling order "
             "and the condition of the property. If the building has been repaired we work from "
             "the documentary record, which is harder and frequently still viable. If the "
             "disclosure deadline has passed, that is a question for counsel before it is a "
             "question for us.</p>"),
        ],
    },

    # ================================================== causation determination
    {
        "slug": "causation-determinations",
        "nav_label": "Causation Determinations",
        "card_title": "Causation determinations",
        "card_blurb": ("What actually caused the damage, and when &mdash; hail or wear, wind or "
                       "water, freeze or long-term seepage."),
        "title": "Property Damage Causation Determination | Texas Consultants",
        "description": ("Independent causation analysis on Texas commercial property damage: "
                        "hail versus wear, wind versus water, freeze versus seepage, and the "
                        "date-of-loss question."),
        "eyebrow": "Service &middot; Causation",
        "h1": "What caused it,<br>and <em>when</em>",
        "h1_plain": "Causation determinations",
        "lede": ("Almost every contested property claim turns into a causation argument "
                 "eventually. Not whether the building is damaged &mdash; that is usually agreed "
                 "&mdash; but whether the thing that damaged it is the thing the policy responds "
                 "to, and whether it happened inside the policy period."),
        "head_aside": [
            ("ledger", "The four recurring questions", [
                ("Hail or wear?", "Test cuts"),
                ("Wind or water?", "Water line"),
                ("Freeze or seepage?", "Records"),
                ("Impact or settlement?", "Pattern"),
                ("Which storm?", "Dated imagery"),
                ("Inside the period?", "All of the above"),
            ], "Each has a physical answer. The difficulty is that the evidence for it decays "
               "within weeks."),
        ],
        "sections": [
            {
                "eyebrow": "Method",
                "h2": "Differential analysis, not assertion.",
                "blocks": [
                    ("p", "A causation opinion is only worth what its method is worth. Ours is "
                          "conventional and deliberately unexciting: identify every mechanism "
                          "capable of producing the observed condition, gather the physical "
                          "evidence that distinguishes them, and eliminate the ones the evidence "
                          "does not support. Where the evidence does not eliminate a competing "
                          "cause, the report says the question is open rather than picking the "
                          "convenient answer."),
                    ("p", "That last habit is what makes the rest of a report credible. An expert "
                          "who resolves every ambiguity in favor of the party paying them has "
                          "told you nothing about the ambiguities."),
                    ("checks", [
                        "Site inspection with measured documentation and location-indexed photography, before anything is cleaned or repaired.",
                        "Destructive testing where the question lives below the surface &mdash; roof test cuts, cavity openings, cabinet and substrate sampling.",
                        "Address-specific weather data for the claimed date of loss, rather than the nearest reporting station or a regional summary.",
                        "Dated aerial and satellite imagery to bracket when a condition first appeared, which is what answers the intervening-storm argument.",
                        "The building&rsquo;s own records: maintenance logs, prior inspection and survey reports, warranty status, earlier claims and what was repaired.",
                        "Laboratory analysis where the material itself carries the answer &mdash; soot and char characterization, corrosion products, microbial speciation.",
                    ]),
                ],
                "aside": [
                    ("callout", "The date-of-loss problem", [
                        ("p", "On commercial roofs in particular, the hardest question is not "
                              "whether hail caused the damage but which hail. Multiple severe "
                              "events across a metro over fifteen years give either party a date "
                              "to point at. Answering it needs dated imagery, prior claim "
                              "history, and evidence of what was actually repaired after each "
                              "event &mdash; not an opinion about probability."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "The four arguments",
                "h2": "What separates each pair, physically.",
                "blocks": [
                    ("table", "Distinguishing evidence",
                     ["The question", "Evidence that separates them"], [
                        ["Hail impact or normal weathering",
                         "Fractured insulation beneath an intact membrane, seen in test cuts; directional consistency across elevations; spatter and denting on soft metals and rooftop equipment; granule displacement patterns; the roof&rsquo;s documented condition and maintenance before the event."],
                        ["Wind-driven rain or surge and flood",
                         "High-water marks and debris deposition lines; the condition of the roof and upper floors relative to the water line; direction of structural failure; the timing of the wind field against the surge, from data specific to the coordinates."],
                        ["Freeze rupture or long-term seepage",
                         "The failed component itself, retained and examined; building management system and thermostat logs; utility outage records for the address and period; material condition analysis distinguishing recent saturation from long-term staining and microbial growth."],
                        ["Impact damage or foundation movement",
                         "Crack morphology, width and propagation direction; whether displacement is consistent across elements; elevation survey; whether the pattern radiates from a point of impact or follows a settlement plane."],
                     ]),
                    ("callout", "Where we hand off", [
                        ("p", "Causation frequently reaches a point where a licensed professional "
                              "engineer, an origin-and-cause investigator or an industrial "
                              "hygienist is required rather than optional. We say so and work "
                              "alongside them. An opinion offered outside the witness&rsquo;s "
                              "competence is the easiest thing in the world to strike."),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("The other side already has an engineering report. Is it too late?",
             "<p>No, and reading theirs carefully is the first thing to do. Engineering reports "
             "are frequently narrower than their conclusions suggest: a visual-only inspection, "
             "two roof sections out of nine, weather data from a station fifteen miles away, "
             "assumptions about prior condition stated without support. The methodology section "
             "is where a rebuttal is usually found.</p>"),
            ("Can you determine causation if the property has already been repaired?",
             "<p>Sometimes, from the documentary record &mdash; contractor photographs, invoices, "
             "change orders, retained materials, pre-loss survey imagery and maintenance files. "
             "It is materially harder and the resulting opinion is correspondingly more "
             "qualified. We will tell you honestly whether what survives can support a "
             "conclusion.</p>"),
            ("Do you do origin and cause investigation on fires?",
             "<p>Fire origin and cause is its own discipline with its own investigator "
             "qualifications, and we do not hold ourselves out in it. What we do is everything "
             "downstream: the extent of fire, smoke and suppression-water damage, whether "
             "materials are restorable, and the cost of the repair.</p>"),
        ],
    },

    # ========================================================= cost estimating
    {
        "slug": "cost-estimating",
        "nav_label": "Cost Estimating",
        "card_title": "Construction cost estimating",
        "card_blurb": ("Line-item scopes in the industry-standard platforms, and forensic "
                       "critique of somebody else&rsquo;s."),
        "title": "Commercial Construction Cost Estimating | Insurance Claims",
        "description": ("Independent line-item construction cost estimating for Texas commercial "
                        "property claims, plus forensic critique and variance analysis of "
                        "opposing estimates."),
        "eyebrow": "Service &middot; Estimating",
        "h1": "The estimate, and<br>the estimate of the <em>estimate</em>",
        "h1_plain": "Construction cost estimating",
        "lede": ("Two thirds of the disputed value on a large property claim is decided in a "
                 "spreadsheet nobody reads line by line. We write those, and we take other "
                 "people&rsquo;s apart."),
        "head_aside": [
            ("ledger", "Estimating practice", [
                ("Platform", "Industry standard"),
                ("Detail", "Line item"),
                ("Pricing", "Local, dated"),
                ("Code work", "Scheduled separately"),
                ("O&amp;P", "Stated, not buried"),
                ("Output", "Exportable"),
            ], "Anything summarized is anything that can be deleted without argument."),
        ],
        "sections": [
            {
                "eyebrow": "Building one",
                "h2": "Scope first, price second, and never in the same step.",
                "blocks": [
                    ("p", "The most common defect in a claim estimate is not the unit price. It "
                          "is that the scope was inferred from a walkthrough rather than measured, "
                          "so the quantities are approximately right and nothing can be checked. "
                          "An estimate built that way cannot be defended line by line, which "
                          "means the whole document gets negotiated as a lump sum."),
                    ("p", "We measure the property, write the scope of work from the measurements, "
                          "and price it afterwards. Code-driven work, soft costs, contents and "
                          "time-element losses are carried on separate schedules so that none of "
                          "them disappears into a general allowance. Every unit price is sourced "
                          "and dated, and where a line is a judgment call rather than a "
                          "measurement, it says so."),
                    ("checks", [
                        "Measured survey of the whole affected area, not a representative sample.",
                        "Line-item scope in the platform the other party is using, so the two documents can be compared directly.",
                        "Local, current pricing with the source and date recorded for anything unusual.",
                        "Access, protection, containment and phasing priced explicitly rather than absorbed into unit costs.",
                        "Overhead, profit and general conditions shown on their own lines with the basis stated.",
                        "Code and ordinance work on a separate schedule, cross-referenced to the requirement that triggers it.",
                    ]),
                    ("html", '<a class="tlink" href="/tools/overhead-profit-general-conditions-calculator/">'
                             'Model O&amp;P and general conditions <span class="arw">&rarr;</span></a>'),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Taking one apart",
                "h2": "Variance analysis: where the difference actually is.",
                "blocks": [
                    ("p", "When two estimates are $1.4 million apart, the instinct is to argue "
                          "about $1.4 million. That is almost never where the dispute lives. Run "
                          "the two documents against each other line by line and the gap usually "
                          "resolves into a handful of decisions: a quantity difference on one "
                          "assembly, a missing trade, a repair-versus-replace call, O&amp;P, and "
                          "code work that one side scheduled and the other did not."),
                    ("p", "A variance analysis puts a number on each of those and reduces the "
                          "negotiation to six arguments instead of one. It is also, on most "
                          "files, the single most cost-effective thing we produce: it is quick, "
                          "it is checkable, and it frequently shows both parties that they are "
                          "closer than the totals suggest."),
                    ("table", "What a variance analysis separates",
                     ["Category", "Typical share of the gap"], [
                        ["Quantity and measurement differences", "Often the largest single component, and the easiest to resolve"],
                        ["Scope omissions &mdash; trades or areas absent from one estimate", "Frequently substantial and usually unintentional"],
                        ["Repair versus replace decisions", "Technical; resolved by manufacturer or specialist input"],
                        ["Unit pricing", "Usually the smallest component, despite getting the most attention"],
                        ["Overhead, profit and general conditions", "A percentage of everything above, so it moves last"],
                        ["Code and ordinance work", "Binary &mdash; either scheduled or not"],
                     ]),
                ],
            },
        ],
        "faqs": [
            ("Which estimating platform do you use?",
             "<p>The industry-standard platforms used by carriers and contractors, chosen to "
             "match whatever the other party is working in so the documents can be reconciled "
             "directly. An estimate that cannot be compared line by line with the one it "
             "disagrees with is much less useful than it looks.</p>"),
            ("Can you produce an estimate without inspecting the property?",
             "<p>We can produce an analysis of somebody else&rsquo;s estimate from documents, and "
             "frequently do. We will not produce an original scope from photographs and call it "
             "an estimate &mdash; the quantities would be invented, and that is exactly the "
             "defect we are usually retained to expose in other people&rsquo;s work.</p>"),
            ("How long does an estimate take?",
             "<p>On a single commercial building, typically two to four weeks from access: a day "
             "or two on site, then the scope and pricing. Multi-building schedules and anything "
             "requiring specialist input run longer. A variance analysis of an existing estimate "
             "is usually a matter of days.</p>"),
        ],
    },

    # ============================================================== appraisal
    {
        "slug": "insurance-appraisal",
        "nav_label": "Appraisal &amp; Umpire",
        "card_title": "Appraisal &amp; umpire service",
        "card_blurb": ("Party appraiser for either side, or umpire &mdash; the policy&rsquo;s own "
                       "mechanism for settling the amount of loss."),
        "title": "Insurance Appraisal &amp; Umpire Services | Texas",
        "description": ("Appraisal and umpire services on Texas commercial property claims. "
                        "Party-appointed appraiser for either side, or umpire where both "
                        "appraisers agree."),
        "eyebrow": "Service &middot; Appraisal",
        "h1": "Two appraisers,<br>one <em>umpire</em>",
        "h1_plain": "Insurance appraisal and umpire service",
        "lede": ("Nearly every commercial property policy contains an appraisal clause, and most "
                 "policyholders have never read it. It settles the amount of loss without "
                 "litigation, in weeks rather than years, and the award binds both parties."),
        "head_aside": [
            ("ledger", "How appraisal works", [
                ("Who invokes", "Either party"),
                ("Appraisers", "One each"),
                ("Umpire", "Agreed or court"),
                ("Binding on", "Amount of loss"),
                ("Not binding on", "Coverage"),
                ("Signatures needed", "Two of three"),
            ], "Two of three signatures set the number. Which is why umpire selection matters "
               "more than anything else in the process."),
        ],
        "sections": [
            {
                "eyebrow": "The distinction",
                "h2": "Amount of loss, not liability.",
                "blocks": [
                    ("p", "Appraisal decides how much the damage costs to put right. It does not "
                          "decide whether the policy covers it. A panel can return an award of "
                          "$2.4 million and the insurer can still decline on the basis that the "
                          "cause of loss was excluded &mdash; although in practice, paying an "
                          "award and then denying coverage is an awkward position to hold."),
                    ("p", "Causation sits uncomfortably across that line. Where the dispute is "
                          "whether hail or age ended a roof&rsquo;s service life, Texas panels "
                          "frequently allocate between covered and non-covered causes as part of "
                          "determining the amount. How that will be handled is worth agreeing at "
                          "the start rather than discovering in the award."),
                    ("callout", "When appraisal fits", [
                        ("p", "Use it when both parties accept the loss is covered and disagree "
                              "about what it costs. Do not use it when the real dispute is a "
                              "denial, an exclusion, a late-notice defense or a misrepresentation "
                              "allegation. Appraisal cannot resolve those, and invoking it can "
                              "complicate a claim heading for litigation. That is a decision to "
                              "take with counsel."),
                    ]),
                ],
                "aside": [
                    ("callout", "Which role we take", [
                        ("p", "Party-appointed appraiser for a policyholder or an insurer, or "
                              "umpire where both appraisers will accept us. We disclose prior "
                              "engagements with either party before accepting any appraisal "
                              "role, and either appraiser can decline us on that basis without "
                              "explanation."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "The process",
                "h2": "Five stages, and one of them decides the outcome.",
                "blocks": [
                    ("steps", [
                        ("Demand",
                         "<p>Written demand under the policy&rsquo;s own clause, naming an "
                         "appraiser. Wording and timing matter; a defective demand gives the "
                         "other party grounds to resist the process entirely.</p>"),
                        ("Appraiser appointment",
                         "<p>Each party names a competent and impartial appraiser within the "
                         "period the policy states. Impartial does not mean neutral about the "
                         "evidence &mdash; an appraiser should know the building and the scope "
                         "thoroughly.</p>"),
                        ("Umpire selection",
                         "<p>The two appraisers agree an umpire, or a court appoints one. This is "
                         "the most consequential step in the process, because in a split panel "
                         "the umpire decides the number. Who is proposed, who is resisted and "
                         "what their background is deserves real attention.</p>"),
                        ("Inspection and exchange",
                         "<p>The panel inspects. Appraisers exchange scopes and estimates and "
                         "attempt to reconcile. A large share of appraisals settle here, between "
                         "the two appraisers, without the umpire ruling at all.</p>"),
                        ("Award",
                         "<p>Any two of the three sign. The award typically itemizes actual cash "
                         "value and replacement cost, and binds both parties on the amount of "
                         "loss, subject to the policy&rsquo;s terms and any reserved coverage "
                         "position.</p>"),
                    ]),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "Preparation",
                "h2": "The panel is looking at the building, not listening to the speech.",
                "blocks": [
                    ("checks", [
                        "A complete line-item estimate in the standard format, priced to the local market and defensible line by line.",
                        "Measured and photographic documentation supporting every disputed item.",
                        "Specialist reports where causation or repairability is in issue.",
                        "A written statement of exactly which items are disputed and why, so the panel can work efficiently.",
                        "Agreement, ideally in writing, on how causation allocation will be treated if it arises.",
                    ]),
                    ("p", "Awards are difficult to unwind. Texas courts generally uphold them "
                          "absent fraud, accident, or a panel acting outside its authority "
                          "&mdash; for instance by deciding coverage rather than amount. That "
                          "finality is the point of the mechanism, and it is why preparation "
                          "before the panel matters far more than argument afterwards."),
                ],
            },
        ],
        "faqs": [
            ("Can you serve as umpire?",
             "<p>Yes, where both appraisers accept us. Umpire work depends on being impartial and "
             "being seen to be, so prior engagements with either party are disclosed to both "
             "appraisers before we accept. A firm that only ever works one side has a structural "
             "problem being accepted as umpire, which is one practical argument for the way this "
             "practice is built.</p>"),
            ("How much does appraisal cost compared with litigation?",
             "<p>Each side pays its own appraiser and the parties normally split the umpire. "
             "Against years of discovery, depositions, expert reports and motion practice, "
             "appraisal is typically far cheaper and far faster &mdash; weeks to a few months on "
             "a well-run panel.</p>"),
            ("Is appraisal a good idea for a public entity?",
             "<p>Frequently, and for a reason beyond cost: it is a contractual process rather "
             "than public litigation against an insurer. For a school board, a city council or a "
             "church membership, that is often a materially easier thing to approve and to "
             "explain.</p>"),
        ],
    },

    # ============================================= soot, smoke and mold testing
    {
        "slug": "soot-smoke-and-mold-testing",
        "nav_label": "Soot, Smoke &amp; Mold Testing",
        "card_title": "Soot, smoke &amp; mold testing and reporting",
        "card_blurb": ("Sampling, laboratory analysis and written findings on combustion residue "
                       "and microbial contamination &mdash; and on what remediation is actually "
                       "required."),
        "title": "Soot, Smoke &amp; Mold Testing and Reporting | Texas",
        "description": ("Independent soot, smoke and mold testing and reporting for Texas "
                        "commercial property. Sampling, laboratory analysis, remediation scope "
                        "and post-remediation verification."),
        "eyebrow": "Service &middot; Testing",
        "h1": "Contamination is a<br><em>laboratory</em> question",
        "h1_plain": "Soot, smoke and mold testing and reporting",
        "lede": ("&ldquo;It smells smoky&rdquo; and &ldquo;there is no visible mold&rdquo; are "
                 "both opinions, and both get asserted with total confidence by people on either "
                 "side of a claim. Sampling and analysis replace the argument with a number."),
        "head_aside": [
            ("ledger", "What testing settles", [
                ("Residue present?", "Yes / no"),
                ("Residue type", "Characterized"),
                ("Distribution", "Mapped"),
                ("Background", "Compared"),
                ("Remediation scope", "Defined"),
                ("Clearance", "Verified"),
            ], "The same sampling answers whether the work is needed and whether it worked."),
        ],
        "sections": [
            {
                "eyebrow": "Soot and smoke",
                "h2": "What burned decides what the residue is.",
                "blocks": [
                    ("p", "Combustion residue is not one substance. A protein fire from a kitchen "
                          "leaves a thin, pervasive, almost invisible film that defeats ordinary "
                          "cleaning and carries an odor out of all proportion to what can be seen. "
                          "Plastics and electronics produce acidic residues that keep corroding "
                          "metal, circuit boards and wiring for months after the fire is out. "
                          "Natural cellulose produces something different again."),
                    ("p", "That distinction decides whether an item is cleaned, restored or "
                          "replaced &mdash; and multiplied across a contents inventory or a "
                          "building&rsquo;s electrical and mechanical systems, it is usually the "
                          "largest disputed number in a fire claim. It is also entirely testable, "
                          "relatively cheaply, which is why the argument is so unnecessary."),
                    ("checks", [
                        "Surface sampling by tape lift and wipe, at locations chosen to map distribution rather than to prove a point.",
                        "Characterization of the particulate &mdash; combustion byproduct versus ordinary settled dust, char versus ash versus soot.",
                        "Background and control samples from unaffected areas of the same building, which is what makes a positive result mean anything.",
                        "Sampling inside air-handling systems and above ceilings, the most common route for building-wide contamination and the most common omission.",
                        "Corrosion assessment on electrical distribution, controls, servers and exposed metal where acidic residues are indicated.",
                        "A written scope of remediation that follows from the findings, rather than a scope written first and justified afterwards.",
                    ]),
                ],
                "aside": [
                    ("callout", "Odor is not a standard", [
                        ("p", "Odor is real, and it is also the least defensible basis for a "
                              "remediation scope, because it varies by person and by day. Where "
                              "odor is the presenting complaint, the useful deliverable is a "
                              "sampling result and an objective completion criterion &mdash; "
                              "something both parties can test against at the end."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Mold and microbial",
                "h2": "Condition, not just presence.",
                "blocks": [
                    ("p", "Mold is present in every building, which is why a bare positive result "
                          "proves very little. What matters is whether indoor conditions differ "
                          "materially from outdoor and unaffected-area baselines, whether the "
                          "species present indicate sustained water activity, and whether there "
                          "is an identified moisture source that would let it continue."),
                    ("p", "The industry standards that govern remediation set out water damage "
                          "categories and condition classifications, and those classifications "
                          "drive the scope: what is cleaned, what is removed, what containment is "
                          "required, and what has to be demonstrated before the space goes back "
                          "into use. A report that gives a result without placing it against "
                          "those criteria has not finished the job."),
                    ("table", "Typical sampling program",
                     ["Method", "What it establishes"], [
                        ["Air sampling, spore trap", "Airborne concentration and genera, indoors against outdoor and unaffected-area controls"],
                        ["Surface sampling, tape lift and swab", "Whether visible growth is fungal, and what it is"],
                        ["Bulk sampling", "Whether growth extends into the material rather than sitting on it"],
                        ["Moisture mapping and meter readings", "The water source and the extent of affected material, which is what actually sizes the scope"],
                        ["Post-remediation verification", "Whether the completed work meets the clearance criteria set at the start"],
                     ]),
                    ("callout", "Set clearance criteria before the work, not after", [
                        ("p", "The most expensive disputes in remediation come from nobody having "
                              "written down in advance what &ldquo;finished&rdquo; means. Agreed "
                              "clearance criteria at the start convert a subjective argument at "
                              "the end into a pass or a fail."),
                    ]),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "The coverage angle",
                "h2": "Remediation sub-limits make timing expensive.",
                "blocks": [
                    ("p", "Texas commercial forms frequently sub-limit fungus and mold "
                          "remediation, sometimes to a figure that is trivial against the "
                          "building limit above it. Where microbial growth results from a covered "
                          "water event and is addressed as part of drying and repair within a "
                          "reasonable time, the work is typically part of the repair. Where it is "
                          "left to develop, the cost gets reclassified against the sub-limit and "
                          "the exposure lands on the owner."),
                    ("p", "Which means early, documented drying with logged readings is not "
                          "administrative box-ticking. It is the difference between a repair cost "
                          "and a capped one, and it matters to whichever party ends up "
                          "carrying it."),
                ],
            },
        ],
        "faqs": [
            ("Do you perform the remediation as well?",
             "<p>No, and that separation is the point. A firm that tests, writes the scope and "
             "then performs the work has an interest in the scope it wrote. We test, we report, "
             "and somebody else does the work &mdash; chosen by the client, with no referral "
             "relationship in either direction.</p>"),
            ("Can you do post-remediation verification on work scoped by someone else?",
             "<p>Yes, and it is a common engagement from both sides. What matters is that the "
             "clearance criteria were defined before the work started. Where they were not, we "
             "will say what the result shows against ordinary standards and note the absence of "
             "an agreed criterion rather than inventing one retrospectively.</p>"),
            ("Is testing worth it on a smaller loss?",
             "<p>Often yes, because it is cheap relative to what it settles. A few hundred "
             "dollars of sampling routinely resolves a five-figure argument about whether "
             "contents are restorable or a building-wide cleaning scope is justified. It is one "
             "of the few places in this business where the analysis costs much less than the "
             "disagreement.</p>"),
        ],
    },

    # ================================================= cabinet repairability
    {
        "slug": "cabinet-repairability-reports",
        "nav_label": "Cabinet Repairability",
        "card_title": "Cabinet repairability reports",
        "card_blurb": ("Whether damaged casework can actually be restored &mdash; substrate, "
                       "finish, hardware and whether the profile can still be matched."),
        "title": "Cabinet Repairability Reports | Casework Damage Assessment",
        "description": ("Independent cabinet and casework repairability assessment after water, "
                        "smoke or impact damage. Substrate condition, refinishing feasibility, "
                        "matching and replacement scope."),
        "eyebrow": "Service &middot; Casework",
        "h1": "Can the cabinets<br>actually be <em>saved</em>?",
        "h1_plain": "Cabinet repairability reports",
        "lede": ("It is a small question that carries a large number. Refinishing a kitchen and "
                 "replacing it differ by an order of magnitude, the decision is made early, and "
                 "on multifamily and institutional property it is made across hundreds of "
                 "units at once."),
        "head_aside": [
            ("ledger", "What the report answers", [
                ("Substrate", "Sound or failed"),
                ("Moisture", "Measured"),
                ("Finish", "Restorable?"),
                ("Hardware", "Serviceable?"),
                ("Profile", "Still available?"),
                ("Scope", "Repair or replace"),
            ], "Five physical findings and one conclusion, each with the evidence attached."),
        ],
        "sections": [
            {
                "eyebrow": "The substrate question",
                "h2": "What the boxes are made of decides almost everything.",
                "blocks": [
                    ("p", "Most commercial and multifamily casework is built from "
                          "particleboard or MDF with a thermofoil, melamine or veneer face. Those "
                          "substrates do not recover from sustained moisture. They swell "
                          "irreversibly, lose fastener holding at the joints, and delaminate at "
                          "the face &mdash; and the swelling frequently appears at the toe kick "
                          "and the bottom of the end panels first, where water wicked upward, "
                          "rather than where the leak was."),
                    ("p", "Plywood-box casework with solid-wood face frames behaves quite "
                          "differently, and is often genuinely restorable after the same event. "
                          "So the first question on any cabinet claim is not how wet it got. It "
                          "is what it is made of, which requires looking at a cut edge rather "
                          "than at the finished face."),
                    ("checks", [
                        "Substrate identified from an exposed or cut edge, not assumed from the door style.",
                        "Moisture readings taken at the toe kick, base, end panels and back, recorded by location with the meter and scale noted.",
                        "Swelling measured rather than described &mdash; thickness at affected and unaffected points on the same component.",
                        "Joint integrity and fastener holding tested, since a box that has lost its corners is not repairable whatever the faces look like.",
                        "Face condition assessed separately: thermofoil delamination and veneer lifting are different failures from a damaged topcoat.",
                        "Hinges, slides and hardware checked for corrosion, which frequently outlives a successful box repair.",
                    ]),
                ],
                "aside": [
                    ("callout", "Why this gets disputed", [
                        ("p", "The standard position on the other side of a cabinet claim is "
                              "&ldquo;clean, dry and refinish.&rdquo; It is a reasonable opening "
                              "on solid-wood casework and close to meaningless on swollen "
                              "particleboard. The disagreement is almost always resolvable with "
                              "a substrate identification and four moisture readings, which is "
                              "why it is such a wasteful thing to argue about for six months."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Matching",
                "h2": "Even repairable casework has an availability problem.",
                "blocks": [
                    ("p", "Suppose half the run is genuinely restorable and half is not. The next "
                          "question is whether the replacement half can be made to match the "
                          "half that stays &mdash; same door profile, same species or laminate "
                          "pattern, same finish, in a kitchen that has aged five years under UV."),
                    ("p", "Cabinet lines are discontinued constantly. Door profiles change, "
                          "laminate patterns are dropped, stain formulations are reformulated. "
                          "Establishing that a profile is no longer available is a documentary "
                          "exercise &mdash; manufacturer correspondence, discontinued-product "
                          "notices, supplier quotes &mdash; and it is what converts a partial "
                          "replacement into a continuous-run replacement under a matching "
                          "argument."),
                    ("table", "What the report records",
                     ["Finding", "Why it matters"], [
                        ["Manufacturer, line and door profile", "Determines whether matching components can be sourced at all"],
                        ["Substrate and construction type", "Determines whether repair is physically possible"],
                        ["Moisture and dimensional data by location", "The evidence base for the repairability conclusion"],
                        ["Finish system and current condition", "Whether refinishing produces a uniform result across old and new"],
                        ["Availability correspondence", "Documented discontinuation is the foundation of a matching claim"],
                        ["Run and elevation photography", "Establishes what a &ldquo;continuous run&rdquo; means in this space"],
                     ]),
                ],
            },
        ],
        "faqs": [
            ("Why commission a separate report for cabinets?",
             "<p>Because the decision is worth a great deal and is usually made by someone "
             "eyeballing a finished face. On a single kitchen the difference between refinishing "
             "and replacing is perhaps tens of thousands. On a 200-unit multifamily property or a "
             "school district with casework in forty classrooms, the same judgment applied "
             "wrongly moves seven figures.</p>"),
            ("Do you assess bathroom vanities, built-ins and commercial millwork too?",
             "<p>Yes. The same analysis applies to vanities, reception and nurse-station "
             "millwork, laboratory casework, library shelving and church built-ins &mdash; and on "
             "laboratory and healthcare casework there is usually a chemical-resistance or "
             "cleanability specification that constrains what a repair is allowed to be.</p>"),
            ("Can you report on units that have already been gutted?",
             "<p>Partially. Where photographs, retained components and the contractor&rsquo;s "
             "documentation survive, an opinion is possible and will be qualified accordingly. "
             "This is a strong argument for getting the assessment done before demolition &mdash; "
             "it is a one-day exercise that becomes impossible a week later.</p>"),
        ],
    },

    # ============================================ contents itemizing & pricing
    {
        "slug": "contents-itemizing-and-pricing-disputes",
        "nav_label": "Contents &amp; Pricing Disputes",
        "card_title": "Contents itemizing &amp; pricing disputes",
        "card_blurb": ("Room-by-room inventory, like-kind-and-quality research and the "
                       "depreciation arguments that decide a contents claim."),
        "title": "Contents Inventory &amp; Pricing Disputes | Personal Property Claims",
        "description": ("Independent contents itemizing, like-kind-and-quality pricing research "
                        "and depreciation analysis on Texas commercial and institutional "
                        "contents claims."),
        "eyebrow": "Service &middot; Contents",
        "h1": "Line by line,<br>and <em>priced</em>",
        "h1_plain": "Contents itemizing and pricing disputes",
        "lede": ("Contents claims are lost in the detail rather than in the principle. Nobody "
                 "disputes that the inventory was destroyed. What gets disputed is 4,000 "
                 "individual descriptions, comparables and depreciation entries, one at a time."),
        "head_aside": [
            ("ledger", "Where contents claims break", [
                ("Description", "Too vague"),
                ("Comparable", "Not like kind"),
                ("Age", "Unsupported"),
                ("Condition", "Asserted"),
                ("Depreciation", "Table-driven"),
                ("Non-restorable", "Undocumented"),
            ], "Each line is small. Multiplied by four thousand, they are the claim."),
        ],
        "sections": [
            {
                "eyebrow": "Itemizing",
                "h2": "A description that cannot be priced is not a description.",
                "blocks": [
                    ("p", "The single biggest cause of contents disputes is an inventory written "
                          "in a hurry. &ldquo;Office chair &mdash; $250&rdquo; invites a $90 "
                          "comparable and there is no basis to argue. &ldquo;Task chair, mesh "
                          "back, synchro-tilt, adjustable arms and lumbar, commercial-grade, "
                          "purchased 2019&rdquo; produces a comparable in the right category, "
                          "because it describes what actually has to be replaced."),
                    ("p", "We inventory room by room, from photographs and physical inspection "
                          "where the items still exist, and from records, invoices, asset "
                          "registers and owner interview where they do not. Each line carries "
                          "the detail that determines price: make and model where known, "
                          "material, size, grade, age and condition, with the source of each "
                          "noted."),
                    ("checks", [
                        "Room-by-room capture with photographs indexed to the inventory line.",
                        "Specification-level descriptions, so a comparable can be sourced rather than guessed.",
                        "Age and purchase evidence where it exists &mdash; asset registers, invoices, capital schedules, grant records.",
                        "Condition recorded at the item level rather than applied as a blanket assumption.",
                        "Restorable, non-restorable and questionable segregated, with the basis stated for each.",
                        "Anything disposed of photographed and sampled before it goes, because it will be asked about.",
                    ]),
                ],
                "aside": [
                    ("callout", "Institutional contents are not household contents", [
                        ("p", "Classroom furniture, laboratory instruments, library collections, "
                              "sanctuary seating, commercial kitchen equipment, hotel FF&amp;E "
                              "and warehouse stock all price from trade channels rather than "
                              "retail. A comparable pulled from a consumer website is the wrong "
                              "market, and saying so is frequently worth more than arguing about "
                              "the number."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Pricing",
                "h2": "Like kind and quality, in the right market.",
                "blocks": [
                    ("p", "Replacement cost for contents means the cost to replace with property "
                          "of like kind and quality &mdash; not the cheapest item that performs "
                          "the same function. Most pricing disputes are really disputes about "
                          "whether a proposed comparable is genuinely equivalent in grade, "
                          "durability, specification and channel."),
                    ("p", "The way through is documentation rather than assertion: a sourced, "
                          "dated comparable from the market the item would actually be bought in, "
                          "with the specification set out so the equivalence can be checked. "
                          "Where an exact match is discontinued, the report says so and prices "
                          "the nearest current equivalent, showing the difference."),
                    ("table", "Common pricing arguments",
                     ["The position", "What resolves it"], [
                        ["The comparable is not like kind and quality", "Side-by-side specification comparison, in the correct trade channel, dated and sourced"],
                        ["The item was older than claimed", "Purchase records, asset register, serial or model dating, warranty documentation"],
                        ["Condition was poor before the loss", "Pre-loss photographs, maintenance and service records, replacement cycle policy"],
                        ["Depreciation applied from a generic table", "Actual useful life for that item in that use, with manufacturer or industry support"],
                        ["The item was restorable", "Cleaning trial results, testing where contamination is in issue, manufacturer position on restored equipment"],
                        ["Quantity is overstated", "Photographic count, floor plan, purchase and delivery records"],
                     ]),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "Depreciation",
                "h2": "A table is a starting point, not a finding.",
                "blocks": [
                    ("p", "Contents depreciation is normally applied from standard tables of "
                          "useful life, which is efficient and frequently wrong at the item level. "
                          "A commercial-grade item in light institutional use outlives its table "
                          "entry comfortably; a consumer-grade item in heavy use does not reach "
                          "it. Condition, maintenance and actual use are the variables, and all "
                          "three are evidenced rather than assumed."),
                    ("p", "On a replacement cost policy this is money that is recoverable once "
                          "the items are actually replaced and documented &mdash; within whatever "
                          "period the policy allows. On institutional claims that deadline is "
                          "missed routinely, because replacing four thousand items takes longer "
                          "than anyone plans for."),
                    ("html", '<a class="tlink" href="/tools/rcv-acv-depreciation-calculator/">'
                             'Model the depreciation holdback <span class="arw">&rarr;</span></a>'),
                ],
            },
        ],
        "faqs": [
            ("Can you build an inventory when everything is already gone?",
             "<p>Frequently, and it is much of what this work is. The sources are asset "
             "registers, purchase and capital records, insurance schedules, photographs taken for "
             "other reasons, video walkthroughs, supplier histories and structured interviews "
             "with the people who used the space. It is slower than inventorying what survives, "
             "and it produces a defensible document.</p>"),
            ("Who should do the itemizing &mdash; us or you?",
             "<p>On a small inventory, the owner, with a template and half an hour of guidance. "
             "Beyond a few hundred items, the quality of the descriptions starts to determine the "
             "outcome and it is worth having done properly. The failure mode is a large inventory "
             "written quickly by someone with other priorities.</p>"),
            ("Do you handle commercial stock and inventory as well as FF&amp;E?",
             "<p>Yes, and stock carries its own valuation question: whether finished goods are "
             "valued at the cost to reproduce or at selling price depends on the policy and on "
             "whether a selling-price endorsement exists. That is a wording check worth making "
             "before the inventory is even built.</p>"),
        ],
    },

    # ======================================================= public adjusting
    {
        "slug": "public-adjusting",
        "nav_label": "Public Adjusting",
        "card_title": "Public adjusting",
        "card_blurb": ("Where the engagement is to present and negotiate the claim as the "
                       "policyholder&rsquo;s representative, under chapter 4102."),
        "title": "Public Adjusting | Texas Commercial Claim Representation",
        "description": ("Licensed public adjusting for Texas commercial and institutional "
                        "policyholders: presenting, documenting and negotiating the claim as your "
                        "representative under chapter 4102."),
        "eyebrow": "Service &middot; Representation",
        "h1": "When the engagement<br>is to <em>represent</em> you",
        "h1_plain": "Public adjusting",
        "lede": ("Most of our work is consulting and testimony, where we are retained to "
                 "establish facts for whoever asks. Public adjusting is the exception: here we "
                 "act as the policyholder&rsquo;s representative, and the engagement is "
                 "different in kind."),
        "head_aside": [
            ("ledger", "This capacity only", [
                ("Acting for", "Policyholder"),
                ("Licence", "Tex. ch. 4102"),
                ("Statutory fee cap", "10%"),
                ("Authority", "&sect;4102.104"),
                ("Repair work", "Prohibited"),
                ("Stated in", "Engagement letter"),
            ], "A single matter is worked in one capacity. Where this is the capacity, it is "
               "named in the engagement letter before anything begins."),
        ],
        "sections": [
            {
                "eyebrow": "The distinction",
                "h2": "Consulting establishes facts. Public adjusting takes a side.",
                "blocks": [
                    ("p", "The two capacities are genuinely different and it matters that nobody "
                          "confuses them. As a consultant or expert, we are retained to measure, "
                          "analyze and report, and the conclusions do not change with the client. "
                          "As a public adjuster, we are the policyholder&rsquo;s representative "
                          "in presenting and negotiating their claim &mdash; an advocacy role, "
                          "licensed separately under chapter 4102 of the Texas Insurance Code."),
                    ("p", "We hold both licences, and we act in one capacity per matter, named in "
                          "the engagement letter. We never act for both parties to the same loss, "
                          "and a conflict check runs before any matter is discussed in detail."),
                    ("callout", "Fees are different in this capacity", [
                        ("p", "Consulting, estimating, appraisal and expert engagements are "
                              "hourly or fixed fee. Public adjusting engagements are on a "
                              "contingent fee, which Texas caps at 10% of the claim settlement "
                              "under &sect;4102.104. Whichever applies is stated in writing "
                              "before work starts, and where an amount has already been offered "
                              "we normally carve it out of the fee base."),
                    ]),
                ],
                "aside": [
                    ("callout", "When to choose which", [
                        ("p", "If you need somebody to run the claim, deal with the carrier and "
                              "negotiate, that is public adjusting. If you need a defensible "
                              "measurement, a report your own broker or counsel can rely on, or "
                              "testimony, that is consulting &mdash; and it is usually the "
                              "cheaper of the two on a well-handled file."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "What it covers",
                "h2": "First notice to final release.",
                "blocks": [
                    ("steps", [
                        ("Coverage analysis",
                         "<p>Declarations, forms, endorsements, schedule of values and prior loss "
                         "history, read before the site visit, with a written summary of limits, "
                         "deductible mechanics, valuation basis and every condition that carries "
                         "a deadline.</p>"),
                        ("Documentation and estimate",
                         "<p>Measured survey of the whole property, indexed photography, "
                         "specialists where the loss warrants them, and a line-item estimate "
                         "with code work, soft costs, contents and time-element carried "
                         "separately.</p>"),
                        ("Presentation",
                         "<p>A sworn proof of loss where appropriate, which states a number and "
                         "starts the insurer&rsquo;s clock rather than leaving the file "
                         "open-ended.</p>"),
                        ("Negotiation to conclusion",
                         "<p>Positions stated in writing and dated, differences itemized, "
                         "supplements filed as actual costs come in, and an early view on whether "
                         "the gap needs appraisal or counsel rather than more letters.</p>"),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Why would we use you as a consultant rather than as a public adjuster?",
             "<p>Because on many files it is cheaper and gets the same result. If the insurer is "
             "engaging properly and your team can run the correspondence, what you actually need "
             "is a defensible scope and estimate &mdash; a fixed-fee consulting deliverable, not "
             "a percentage of the whole settlement. Where the file needs somebody to carry it, "
             "public adjusting earns its fee. We will tell you which we think you are looking "
             "at.</p>"),
            ("Can you switch capacity mid-matter?",
             "<p>Rarely, and never quietly. Moving from consultant to representative changes the "
             "relationship, the fee basis and how the earlier work will be characterized by the "
             "other side. If it is genuinely the right move it is done by a new written "
             "engagement, and if we have served as a neutral or an umpire on the matter, it is "
             "not available at all.</p>"),
            ("Do you take referral fees from contractors?",
             "<p>No, in any capacity. Chapter 4102 prohibits a public adjuster from participating "
             "in the repair of property they adjusted, and we go further: no referral fees, "
             "commissions or other consideration from contractors, restoration firms, engineers "
             "or vendors, in either direction, on any engagement.</p>"),
        ],
    },

    {
        "slug": "policy-review-and-pre-loss-consulting",
        "nav_label": "Policy Review &amp; Pre-Loss",
        "card_title": "Policy review &amp; pre-loss consulting",
        "card_blurb": ("The cheapest hour in insurance: reading the wording before there is a "
                       "claim, while it can still be changed."),
        "title": "Commercial Policy Review &amp; Pre-Loss Consulting | TX",
        "description": "Independent commercial property policy review for Texas institutions. Find the gaps before the loss, while renewal can still fix them.",
        "eyebrow": "Service &middot; Before the loss",
        "h1": "Read the policy while<br>it can still be <em>changed</em>",
        "h1_plain": "Commercial policy review and pre-loss consulting",
        "lede": ("Every argument on this website is an argument about wording that was agreed years "
                 "before the storm. A coinsurance clause, a margin clause, a per-building "
                 "deductible, an ordinance and law limit set at 10% &mdash; all fixable at "
                 "renewal, none fixable afterwards."),
        "head_aside": [
            ("ledger", "What a review covers", [
                ("Valuation basis", "RCV / ACV / FRC"),
                ("Coinsurance", "Or agreed value"),
                ("Deductible mechanics", "Per what?"),
                ("Ordinance &amp; law", "A, B and C"),
                ("Time element", "Structure &amp; period"),
                ("Schedule accuracy", "Values tested"),
            ], "Delivered as a written report your board or council can act on at renewal, with "
               "the questions to put to your broker."),
        ],
        "sections": [
            {
                "eyebrow": "Why bother",
                "h2": "We are not selling you insurance, which is the point.",
                "blocks": [
                    ("p", "Your broker is usually competent and is always paid by placement. That "
                          "does not make their advice wrong, but it does mean nobody in the chain "
                          "is paid to tell you the policy will underperform in a loss. We read "
                          "wording from the other end &mdash; from years of watching which clauses "
                          "cost institutions money when a claim is actually made."),
                    ("p", "A review is a fixed-fee engagement, independent of any claim, and it "
                          "produces a written report: where the program is sound, where it is "
                          "exposed, what the exposure is worth in a realistic loss scenario, and "
                          "the specific questions to raise with your broker before renewal. We do "
                          "not sell insurance and we take no commission from anyone who does."),
                    ("checks", [
                        "Valuation basis on every scheduled location, and whether the reported values would actually rebuild the building today.",
                        "Coinsurance exposure modelled against a realistic partial loss, not just a total one.",
                        "Deductible mechanics for wind, hail and named storm, applied to a multi-building event to show the true retention.",
                        "Ordinance and law coverage tested against what your jurisdiction would actually require on a substantial repair.",
                        "Time-element structure: period of indemnity, extensions, waiting periods, dependent property, and whether the income streams you actually have are covered.",
                        "Documentation readiness &mdash; whether the records that prove a claim exist and are retrievable before you need them.",
                    ]),
                ],
                "aside": [
                    ("callout", "Best timed 90 days out", [
                        ("p", "Ninety days before renewal is the window where findings can still "
                              "be marketed, endorsed or negotiated. A review delivered two weeks "
                              "before expiry is a report about next year."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Also useful",
                "h2": "Loss-readiness, not just wording.",
                "blocks": [
                    ("p", "Half of what determines a claim outcome has nothing to do with the "
                          "policy. It is whether anyone knows where the declarations page is at 2am, "
                          "whether the roof was surveyed before the storm, whether the BMS logs are "
                          "retained for longer than thirty days, and whether the person who will "
                          "take the first phone call knows not to sign anything."),
                    ("steps", [
                        ("Pre-loss condition record",
                         "<p>A dated photographic and drone survey of roofs and elevations, held "
                         "on file. It is the single most effective rebuttal to a wear-and-tear "
                         "denial, and it costs a fraction of the argument it prevents.</p>"),
                        ("Document retention",
                         "<p>Confirming that building management logs, maintenance records, "
                         "utility data and financial reporting are retained long enough and "
                         "exportable quickly. Several systems overwrite in thirty days.</p>"),
                        ("First-72-hours protocol",
                         "<p>A one-page instruction for whoever is on site: what to photograph, "
                         "what not to throw away, who to call, what not to sign, and how to record "
                         "emergency spend so it is recoverable.</p>"),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("How much does a policy review cost?",
             "<p>It is a flat fee, quoted against the size and complexity of the schedule, and paid "
             "whether or not there is ever a claim &mdash; which is the opposite of how we are paid "
             "on claim work and is deliberate. You are buying independent analysis, not a "
             "interest in the conclusion.</p>"),
            ("Will this annoy our broker?",
             "<p>Good brokers welcome it, and several of the reviews we do arrive by broker "
             "referral. A written, independent assessment gives them something concrete to take to "
             "the market on your behalf. If a broker objects to their client having the policy "
             "read, that is itself information.</p>"),
            ("We are in a risk pool. Is a review still worth doing?",
             "<p>Arguably more so. Pool coverage documents are non-standard, they change from year "
             "to year, and the differences from a commercial form &mdash; in valuation, in "
             "exclusions, in the appeal process, in how the retention works &mdash; are exactly the "
             "things nobody reads until there is a loss.</p>"),
        ],
    },
]

for _s in SERVICES:
    _s["path"] = "/services/%s/" % _s["slug"]
