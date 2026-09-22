"""Standing pages: firm, method, fees, FAQ, glossary, contact, legal.

Also the shared FAQ list used on the homepage and the hub-page introductions,
which live here so the hubs are not thin.
"""

from siteconfig import BIZ, STATUTE, FOOTER_SERVING

P = BIZ["phone_display"]
PH = BIZ["phone_href"]
E = BIZ["email"]

# ---------------------------------------------------------------------------
HOME_FAQS = [
    ("What is a public adjuster, and how is that different from the adjuster the insurer sent?",
     "<p>A public insurance adjuster is licensed to represent the policyholder &mdash; and only "
     "the policyholder &mdash; in presenting and negotiating a claim. The adjuster the carrier "
     "sends, whether a staff employee or an independent contractor, is retained and paid by the "
     "insurer. Both may be entirely competent; only one of them is working from your side of the "
     "table. In Texas we are licensed under %s and regulated by the Texas Department of "
     "Insurance.</p>" % STATUTE["chapter"]),

    ("How much does it cost, and when do we pay?",
     "<p>Our fee is a percentage of what is recovered, agreed in writing before any work starts, "
     "and capped by statute at %s of the claim settlement (%s). If nothing is recovered there is "
     "no fee. Where the carrier has already made an offer before we are engaged, we normally "
     "carve that amount out of the fee base so the percentage applies to the improvement rather "
     "than to money already on the table &mdash; ask for that in writing, from us or from anyone "
     "else you are considering.</p>" % (STATUTE["fee_cap"], STATUTE["fee_cite"])),

    ("We are a church / district / city. Do the usual insurance rules even apply to us?",
     "<p>Not always, and establishing which rules apply is the first thing we do. A great many "
     "Texas public entities and religious organizations cover property through an interlocal risk "
     "pool or a denominational program rather than a conventional insurance policy. Those are "
     "governed by their own coverage documents, with their own appeal routes, and the statutory "
     "prompt-payment machinery in the Insurance Code may not apply in the same way. The scope "
     "disputes are identical; the leverage is different.</p>"),

    ("Will hiring a public adjuster make the claim adversarial?",
     "<p>Less often than people fear. Most carrier adjusters deal with represented policyholders "
     "constantly and several prefer it &mdash; a well-documented, line-item claim from someone "
     "who understands the policy is easier to process than a folder of contractor proposals. What "
     "changes is that the scope stops being decided unilaterally.</p>"),

    ("How long will the claim take?",
     "<p>A straightforward commercial roof claim can settle in two to four months. A large "
     "institutional loss involving engineering, code analysis and a time-element component "
     "typically runs nine to eighteen. The strongest predictor is how completely the loss was "
     "documented in the first thirty days &mdash; which is the single best argument for calling "
     "early, even if you decide not to engage anyone.</p>"),

    ("What size of claim do you take?",
     "<p>We work large commercial and institutional property losses. That is a deliberate focus "
     "rather than a boast: the methods on this site &mdash; full-property surveys, specialist "
     "engagement, forensic accounting, appraisal &mdash; are proportionate on a large loss and "
     "wasteful on a small one. If your loss is modest, we will say so and point you somewhere "
     "more suitable rather than take the file.</p>"),
]

# ---------------------------------------------------------------------------
# Hub page introductions
# ---------------------------------------------------------------------------

INDUSTRY_HUB_INTRO = [
    {
        "eyebrow": "Why it matters",
        "h2": "The property type changes the argument, not just the vocabulary.",
        "blocks": [
            ("p", "A hail claim on a warehouse and a hail claim on a school district are not the "
                  "same file with a different address. The district has a per-building deductible "
                  "applied across nineteen campuses, a coverage document that may be an "
                  "interlocal agreement rather than an insurance policy, a board that has to "
                  "approve the settlement in public, and a hard deadline in August. None of that "
                  "appears in the estimating software."),
            ("p", "We work a narrow set of property types on purpose. Each of the pages below "
                  "sets out the wording, the valuation problem and the political constraint "
                  "peculiar to that kind of owner &mdash; because knowing which argument to make "
                  "is most of the work."),
        ],
        "aside": [
            ("callout", "Large commercial only", [
                ("p", "We do not take residential claims, and we decline commercial losses too "
                      "small to justify the method. That is not exclusivity; it is a question of "
                      "what a full-property survey and specialist engagement are proportionate "
                      "to."),
            ]),
        ],
    },
    {
        "band": "paper2",
        "eyebrow": "Common ground",
        "h2": "What every institutional claim has in common.",
        "blocks": [
            ("checks", [
                "<strong>Somebody has to approve it in public.</strong> Boards, councils, trustees and vestries all need documentation they can put in a packet without rewriting it.",
                "<strong>The values are stale.</strong> Statements of value assembled years ago, against construction costs that moved sharply after 2020.",
                "<strong>The building is old enough to trigger code.</strong> Which makes ordinance and law coverage the decisive clause more often than anyone expects.",
                "<strong>The deductible structure is unexamined.</strong> Per occurrence or per building, flat or percentage &mdash; on a multi-structure schedule that single clause can decide the claim.",
                "<strong>Nobody is running the time-element side.</strong> Interruption and extra expense are real on institutional losses and almost never documented while they are happening.",
            ]),
        ],
    },
]

SERVICE_HUB_INTRO = [
    {
        "eyebrow": "How to use this",
        "h2": "The first five are causes of loss. The last four are stages.",
        "blocks": [
            ("p", "Most people arrive knowing what happened to their building, so the first five "
                  "pages are organised by peril: wind, hail, fire, water and the general case. "
                  "Each sets out the coverage question that peril raises and the evidence that "
                  "answers it."),
            ("p", "The last four are for claims that are already in trouble &mdash; deadlocked on "
                  "amount, denied outright, or short-paid and closed &mdash; plus the one service "
                  "that works best before there is a claim at all."),
        ],
        "aside": [
            ("ledger", "Engagement shapes", [
                ("Full representation", "Most common"),
                ("Disputed portion only", "Frequent"),
                ("Appraisal only", "Available"),
                ("Estimate review", "Fixed fee"),
                ("Policy review", "Fixed fee"),
                ("Expert support to counsel", "Available"),
            ], "Not every file needs the whole service. The engagement letter defines the scope, "
               "and the fee applies to that scope."),
        ],
    },
]

TOOL_HUB_INTRO = [
    {
        "eyebrow": "How these work",
        "h2": "Everything runs in your browser. Nothing is stored or sent.",
        "blocks": [
            ("p", "There is no form to fill in before you see an answer, no email capture, and no "
                  "server involved. The arithmetic runs locally, the figures never leave your "
                  "machine, and closing the tab discards everything. Each tool has a copy and a "
                  "print button if you want a record for a file or a board packet."),
            ("p", "What they are not is an estimate. Every one of them applies published "
                  "conventions to assumptions you supply. A real claim figure comes from a "
                  "measured survey, a line-item scope and the specific wording of your policy. "
                  "Use these to find out whether the number on your desk is in the right "
                  "ballpark &mdash; that is genuinely useful, and it is all they do."),
        ],
        "aside": [
            ("callout", "Built from live files", [
                ("p", "These are simplified versions of the models we run on real claims. The "
                      "defaults in each field are realistic starting points for a mid-sized "
                      "institutional loss, which makes them a reasonable sanity check even "
                      "before you enter your own figures."),
            ]),
        ],
    },
]

AREA_HUB_INTRO = [
    {
        "eyebrow": "Coverage",
        "h2": "Statewide, with six metros where we work constantly.",
        "blocks": [
            ("p", "We take institutional and large commercial files anywhere in Texas. The pages "
                  "below cover the metros where the volume is, and each one is written from what "
                  "actually damages buildings there &mdash; the hail corridor through "
                  "Dallas&ndash;Fort Worth, surge and the wind-water line on the Coastal Bend, "
                  "the ordinance and law exposure in San Antonio&rsquo;s older institutional "
                  "stock."),
            ("p", "If your property is outside these areas, call anyway. Statewide response on a "
                  "large loss is a scheduling question, not a coverage one, and we will tell you "
                  "honestly whether we can staff it."),
        ],
        "aside": [
            ("callout", "After a catastrophe", [
                ("p", "Following a major regional event every firm in the industry is "
                      "oversubscribed, including this one. We would rather decline an engagement "
                      "than take a file we cannot work properly &mdash; and we will still spend "
                      "ten minutes on the phone telling you what to photograph before the crews "
                      "arrive."),
            ]),
        ],
    },
]

BLOG_INTRO = [
    {
        "eyebrow": "Editorial policy",
        "h2": "Written for the person who has to explain the claim to a board.",
        "blocks": [
            ("p", "One rule governs this section: every piece has to teach something a reader "
                  "could act on without hiring anybody. Policy wording, Texas statute, the "
                  "evidence that wins a particular argument, the records to start keeping on day "
                  "one. If a draft reads like a brochure with subheadings, it does not go up."),
            ("p", "Nothing here is legal advice, and where a question is genuinely legal we say "
                  "so and recommend counsel."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Standing pages
# ---------------------------------------------------------------------------

ABOUT = {
    "path": "/about/",
    "title": "About the Firm | Texas Commercial Public Adjusters",
    "description": ("%s represents Texas churches, school districts, municipalities and large "
                    "commercial owners in property insurance claims. No recovery, no fee."
                    % BIZ["name"]),
    "eyebrow": "The firm",
    "h1": "We represent the<br>policyholder. <em>Only</em> the policyholder.",
    "h1_plain": "About Claims Consultant",
    "lede": ("There is no version of this business where we also work for insurers, take "
             "referral money from contractors, or repair the buildings we adjust. That is partly "
             "statute and mostly the point."),
    "trail": [("Home", "/"), ("The firm", None)],
    "head_aside": [
        ("ledger", "Practice profile", [
            ("Focus", "Large commercial"),
            ("Sectors", "Institutional"),
            ("Territory", "Texas"),
            ("Licensing", "Tex. Ins. Code ch. 4102"),
            ("Fee", "Contingent, capped"),
            ("Repair work", "None, ever"),
        ], "We are licensed public insurance adjusters. We are not a law firm, not a contractor "
           "and not an insurance agency."),
    ],
    "sections": [
        {
            "eyebrow": "Position",
            "h2": "One side of the table, by construction.",
            "blocks": [
                ("p", "Property insurance is an industry with a structural imbalance in it. The "
                      "insurer has a claims department, an estimating platform, a panel of "
                      "engineers and decades of institutional memory about which arguments work. "
                      "The policyholder has a facilities director who has handled two claims in "
                      "their career and a contractor with an interest in the scope."),
                ("p", "A public adjuster is the correction to that. We bring the same estimating "
                      "software, the same expert disciplines and the same familiarity with the "
                      "arguments &mdash; with an incentive pointing the other way. Chapter 4102 "
                      "of the Texas Insurance Code makes the position exclusive: a licensed "
                      "public adjuster may not act for insurers on the same loss, and may not "
                      "participate in repairing the property they adjusted."),
                ("p", "We think that rule is a feature rather than a constraint, and we go "
                      "further than it requires. We take no compensation of any kind from "
                      "contractors, restoration firms, engineers or anyone else in the supply "
                      "chain. You choose who does the work; we have no view worth buying."),
            ],
            "aside": [
                ("callout", "What we are not", [
                    ("p", "Not a law firm &mdash; we do not give legal advice, and when a file "
                          "needs counsel we say so. Not a contractor &mdash; we do not repair "
                          "what we adjust. Not an agency &mdash; we do not sell insurance or "
                          "receive commission from anyone who does."),
                ]),
            ],
        },
        {
            "band": "paper2",
            "eyebrow": "Focus",
            "h2": "Institutional and large commercial. Nothing else.",
            "blocks": [
                ("p", "Most public adjusting firms take whatever comes. We do not, for a "
                      "practical reason: the way we work a claim &mdash; full-property survey "
                      "rather than a sample, specialist engagement where the loss warrants it, "
                      "forensic accounting on the time-element side, appraisal where the gap will "
                      "not close &mdash; is proportionate on a large institutional loss and "
                      "absurd on a small one."),
                ("p", "So the practice is built around a narrow set of owners: churches and faith "
                      "organizations, school districts, cities and municipal entities, colleges "
                      "and universities, healthcare facilities, multifamily and commercial "
                      "portfolios. What those have in common is complex property, complex "
                      "coverage, and somebody who has to justify the outcome in public."),
                ("html", '<a class="tlink" href="/who-we-serve/">Who we serve <span class="arw">&rarr;</span></a>'),
            ],
        },
        {
            "band": "ink",
            "eyebrow": "Commitments",
            "h2": "Six things we will do, and one we will not.",
            "blocks": [
                ("checks", [
                    "Tell you in the first conversation whether we think representation is worth it &mdash; including when the answer is no.",
                    "Put the fee, the scope of the engagement and any carve-out in writing before any work starts.",
                    "Read the policy before we walk the building, and explain what it says in plain language.",
                    "Document the whole property, not a representative sample of it.",
                    "Discuss every third-party cost with you before it is incurred.",
                    "Say early when a file needs a lawyer instead of, or alongside, an adjuster.",
                ]),
                ("p", "The one we will not: inflate a scope. On claims this size the file is "
                      "frequently examined by a forensic accountant, an engineer, an appraisal "
                      "panel or a court. Every line has to survive that, and a scope padded to "
                      "create negotiating room destroys the credibility of the forty lines around "
                      "it that were right."),
            ],
        },
        {
            "eyebrow": "Practicalities",
            "h2": "Working with us.",
            "blocks": [
                ("steps", [
                    ("The first call costs nothing",
                     "<p>Fifteen minutes on the phone, usually with the policy declarations page "
                     "in front of you. We will tell you what we think the file needs and whether "
                     "that is us. A meaningful share of these calls end with advice and no "
                     "engagement.</p>"),
                    ("A written engagement, or nothing",
                     "<p>Scope, fee, carve-outs and the cancellation provision, in writing, "
                     "before work begins. Chapter 4102 requires a written contract; we would "
                     "insist on one regardless, because institutional clients need something "
                     "their board can read.</p>"),
                    ("One point of contact, and a paper trail",
                     "<p>You get a named adjuster who is actually on the file, not a salesperson "
                     "who hands you to a queue. Everything material goes in writing, and at "
                     "closeout you receive the complete record &mdash; photographs, estimates, "
                     "correspondence &mdash; whether or not you ever need it again.</p>"),
                ]),
            ],
        },
    ],
    "faqs": [
        ("Are you licensed?",
         "<p>Yes &mdash; as licensed public insurance adjusters under chapter 4102 of the Texas "
         "Insurance Code. License status can be verified directly with the Texas Department of "
         "Insurance, and you should verify it for any firm you are considering, including this "
         "one. Ask for the license number and check it yourself; it takes two minutes.</p>"),
        ("Do you work outside Texas?",
         "<p>Public adjusting is licensed state by state and we do not practice where we are not "
         "licensed. Where an institution has property in several states we can usually help "
         "coordinate, and we will say plainly which parts of that we can and cannot handle "
         "ourselves.</p>"),
        ("Do you take residential claims?",
         "<p>No. It is not what the practice is built for, and a firm that works institutional "
         "property all week is not the right choice for a house. We will point you toward "
         "somebody appropriate.</p>"),
    ],
}

HOW_WE_WORK = {
    "path": "/how-we-work/",
    "title": "How We Work a Commercial Claim | Method &amp; Process",
    "description": ("The method: coverage analysis before the site visit, full-property "
                    "documentation, a line-item estimate, sworn proof of loss, and negotiation to "
                    "settlement or appraisal."),
    "eyebrow": "Method",
    "h1": "How a claim file<br>gets <em>built</em>",
    "h1_plain": "How we work a commercial claim",
    "lede": ("There is no clever trick in any of this. It is the ordinary discipline of reading "
             "the policy first, documenting everything while it is still true, pricing the work "
             "properly, and putting every position in writing."),
    "trail": [("Home", "/"), ("How we work", None)],
    "head_aside": [
        ("ledger", "Typical timeline", [
            ("Coverage analysis", "Days 1&ndash;3"),
            ("Site documentation", "Days 1&ndash;10"),
            ("Specialists engaged", "Weeks 1&ndash;4"),
            ("Line-item estimate", "Weeks 2&ndash;5"),
            ("Proof of loss", "Weeks 4&ndash;8"),
            ("Negotiation", "Months 2&ndash;9"),
        ], "Large institutional files run longer. The variable that moves the timeline most is "
           "how complete the documentation was in month one."),
    ],
    "sections": [
        {
            "eyebrow": "Stage one",
            "h2": "Policy before property.",
            "blocks": [
                ("p", "We do not walk the building first. We read the declarations, the forms, "
                      "the endorsements, the schedule of values and any prior loss history, and "
                      "we produce a written coverage summary before anyone gets on a roof."),
                ("p", "The reason is practical. Half of what will be argued about in month six is "
                      "already settled by wording you own today: whether the valuation basis is "
                      "replacement cost, actual cash value or functional replacement cost; "
                      "whether there is a coinsurance clause or an agreed value endorsement; what "
                      "the ordinance and law limits are; how the deductible applies across "
                      "multiple buildings; what the time-element structure covers and for how "
                      "long. Knowing all of that shapes what we go and document."),
                ("checks", [
                    "Limits, sub-limits and how the schedule is structured &mdash; blanket, per location, with or without a margin clause.",
                    "Deductible mechanics, including named-storm and percentage wording and how occurrence is defined.",
                    "Valuation basis by category, including any roof surfacing or cosmetic damage endorsement.",
                    "Ordinance or law coverages A, B and C, with their separate limits.",
                    "Time-element structure: period of indemnity, extensions, waiting periods, dependent property.",
                    "Every condition carrying a deadline &mdash; notice, proof of loss, suit limitation, recoverable depreciation.",
                ]),
            ],
        },
        {
            "band": "paper2",
            "eyebrow": "Stage two",
            "h2": "Document the whole property, not a sample of it.",
            "blocks": [
                ("p", "Sampling is an estimating convenience. On a 288-unit community, a campus "
                      "with forty roof sections or a center with fourteen tenants, extrapolating "
                      "from four inspections carries whatever error was in those four, multiplied "
                      "by a few hundred."),
                ("p", "So we survey everything, measure everything and photograph everything, "
                      "indexed by location so any line on the estimate can be traced to the "
                      "evidence for it. Where the dispute will be technical &mdash; roof "
                      "membrane, cause of failure, contamination class, equipment condition "
                      "&mdash; we engage the relevant specialist rather than offering an opinion "
                      "we are not qualified to give."),
                ("table", "Specialists we engage, and when",
                 ["Discipline", "Engaged when"], [
                    ["Roofing consultant", "Any commercial roof claim where repairability or cause is contested"],
                    ["Structural or forensic engineer", "Structural damage, collapse, or where the carrier has retained an engineer"],
                    ["Industrial hygienist", "Mould, contamination, or any healthcare or laboratory environment"],
                    ["Forensic accountant", "Time-element losses of any real size"],
                    ["Equipment specialist / OEM", "Production equipment, medical imaging, laboratory instruments"],
                    ["Code consultant", "Older buildings where ordinance and law exposure is material"],
                 ]),
            ],
        },
        {
            "eyebrow": "Stage three",
            "h2": "Build the estimate, then the argument.",
            "blocks": [
                ("p", "The estimate is produced in the same industry-standard platform the "
                      "carrier uses, priced to your market and your occupancy, at line-item "
                      "detail. Code upgrade work, soft costs, contents and time-element losses "
                      "are carried as separate schedules so that nothing can be quietly folded "
                      "into a lump-sum allowance and disappear."),
                ("p", "Then a sworn proof of loss, where it is appropriate, which states a number "
                      "and puts the carrier on the clock rather than leaving the file open-ended. "
                      "A great many commercial claims drift for a year because nobody ever "
                      "required a decision."),
            ],
            "aside": [
                ("callout", "Why line-item detail matters", [
                    ("p", "A lump sum invites a lump-sum counter. A 400-line estimate forces the "
                          "conversation onto specific items, each of which has an evidentiary "
                          "answer. Detail is not bureaucracy; it is how the negotiation gets "
                          "moved from opinion to fact."),
                ]),
            ],
        },
        {
            "band": "ink",
            "eyebrow": "Stage four",
            "h2": "Negotiate in writing, and know when to stop.",
            "blocks": [
                ("p", "Every position we take is stated in writing and dated. Every position the "
                      "carrier takes is recorded the same way. Differences are itemised rather "
                      "than described. Supplements are filed as actual costs come in. Where "
                      "statutory deadlines apply, they are cited by date rather than referred to "
                      "in general terms."),
                ("p", "And when the gap will not close, we tell you which route we think fits. If "
                      "the dispute is about the amount of loss, that is usually appraisal. If it "
                      "is about coverage, a denial, late notice or the carrier&rsquo;s conduct, "
                      "that is a lawyer &mdash; and saying so in month four is worth considerably "
                      "more to you than saying it in month fourteen."),
                ("html", '<div class="btn-row"><a class="btn btn--brass" href="/contact/">Start a claim review '
                         '<span class="arw">&rarr;</span></a>'
                         '<a class="btn btn--ghost" href="/services/appraisal-and-claim-disputes/">About appraisal</a></div>'),
            ],
        },
    ],
    "faqs": [
        ("What do you need from us to start?",
         "<p>The declarations page and the full policy if you have it, any correspondence with "
         "the carrier, the claim number, and access to the property. Everything else we can "
         "assemble. If you cannot find the policy, your broker can produce it within a day and "
         "we can ask on your behalf.</p>"),
        ("How much of our time will this take?",
         "<p>Meaningfully less than handling it yourselves. Expect an initial half-day for the "
         "policy review and walkthrough, access for the survey, and periodic decisions from "
         "whoever has authority. On the time-element side we need someone in finance who can pull "
         "records; that is usually the largest demand we make.</p>"),
        ("Can you work alongside our broker and our attorney?",
         "<p>Routinely, and it is often the right structure. Brokers hold institutional knowledge "
         "about the placement that is genuinely useful. Counsel handles coverage and statutory "
         "remedies. We handle scope, valuation and the evidentiary record. Clear lanes make all "
         "three more effective.</p>"),
    ],
}

FEES = {
    "path": "/fees/",
    "title": "Fees &amp; Engagement Terms | Texas Public Adjuster Fee Cap",
    "description": ("How our fee works: a percentage of recovery, capped at 10% by Texas statute, "
                    "with the prior offer normally carved out. Third-party costs explained."),
    "eyebrow": "Commercial terms",
    "h1": "What it costs,<br>stated <em>plainly</em>",
    "h1_plain": "Fees and engagement terms",
    "lede": ("Boards and councils have to approve this in public, so it needs to be simple enough "
             "to put in a packet and specific enough to survive an audit."),
    "trail": [("Home", "/"), ("Fees", None)],
    "head_aside": [
        ("ledger", "The commercial terms", [
            ("Basis", "Contingent"),
            ("Statutory cap", STATUTE["fee_cap"]),
            ("Authority", "&sect;4102.104"),
            ("Prior offer", "Normally carved out"),
            ("If no recovery", "No fee"),
            ("Third-party costs", "Client, pre-authorised"),
        ], "Every one of these is written into the engagement letter before work starts."),
    ],
    "sections": [
        {
            "eyebrow": "The fee",
            "h2": "A percentage of what is recovered, and nothing if nothing is.",
            "blocks": [
                ("p", "Texas caps a public insurance adjuster&rsquo;s compensation at 10%% of the "
                      "amount of the claim settlement (%s). Within that cap, the rate is agreed "
                      "before work begins and reflects the size and complexity of the file. On "
                      "very large losses it is normally lower than the cap, for the obvious "
                      "reason that ten percent of an eight-figure recovery is not proportionate "
                      "to the work." % STATUTE["fee_cite"]),
                ("p", "If the claim recovers nothing, there is no fee. That is not a marketing "
                      "line; it is the structure, and it is why we decline files we do not think "
                      "we can move."),
            ],
            "aside": [
                ("callout", "The carve-out", [
                    ("p", "Where the carrier has already offered an amount before we are engaged, "
                          "we normally exclude that sum from the fee base so the percentage "
                          "applies only to the improvement. Not every firm does this. Ask any "
                          "firm you are considering to put their answer in writing."),
                ]),
                ("html", '<a class="tlink" href="/tools/public-adjuster-fee-calculator/">'
                         'Model the net <span class="arw">&rarr;</span></a>'),
            ],
        },
        {
            "band": "paper2",
            "eyebrow": "Third-party costs",
            "h2": "Experts are a separate, pre-authorised cost.",
            "blocks": [
                ("p", "Engineers, forensic accountants, industrial hygienists, roofing "
                      "consultants and specialist surveys are engaged where the loss warrants "
                      "them, and they are normally the client&rsquo;s direct cost rather than "
                      "ours. On a large institutional file those costs can be substantial, which "
                      "is precisely why every one of them is discussed and authorised before it "
                      "is incurred. You will not receive a bill for something you did not agree "
                      "to."),
                ("p", "Where a cost is genuinely part of the cost of repair &mdash; design "
                      "professionals required to permit and execute the work, for instance "
                      "&mdash; we claim it from the carrier as such."),
                ("table", "Who pays for what", ["Item", "Paid by"], [
                    ["Our adjusting services", "Contingent fee, out of the recovery"],
                    ["Engineers and technical consultants", "Client, authorised in advance"],
                    ["Forensic accounting", "Client, authorised in advance"],
                    ["Appraiser fee, if appraisal is invoked", "Client, per the policy&rsquo;s appraisal clause"],
                    ["Umpire fee", "Normally split between the parties"],
                    ["Legal representation", "Client, under separate engagement with counsel"],
                 ]),
            ],
        },
        {
            "eyebrow": "For public entities",
            "h2": "Documentation your procurement process will want.",
            "blocks": [
                ("p", "School districts, cities and other public entities have their own "
                      "procurement rules for professional services, and your purchasing officer "
                      "and counsel &mdash; not us &mdash; determine how they apply. What we can "
                      "do is produce the documentation the process needs without you having to "
                      "invent it."),
                ("checks", [
                    "A written scope of services suitable for an agenda item or board packet.",
                    "Fee terms expressed as a percentage of recovery, with the statutory cap and authority cited.",
                    "Proof of licensure and insurance.",
                    "Confirmation in writing that we take no compensation from contractors or vendors on the loss.",
                    "A stated cancellation provision.",
                    "Status reporting at a cadence that matches your meeting cycle.",
                ]),
            ],
        },
    ],
    "faqs": [
        ("Is the 10% cap per claim or per payment?",
         "<p>The statutory limit is expressed against the amount of the claim settlement. How "
         "supplements, advance payments and any amount already offered are treated within that is "
         "a matter for the engagement letter, which is why those points should be written down "
         "before work starts rather than discussed at settlement.</p>"),
        ("Can we cancel?",
         "<p>Yes. Statute and the engagement letter provide a cancellation right, and the terms "
         "are stated in the contract you sign. Read that clause before signing &mdash; with us or "
         "with anyone else.</p>"),
        ("Do you ever work on a flat fee?",
         "<p>For policy reviews and pre-loss consulting, always &mdash; those are fixed-fee "
         "engagements precisely so there is no contingent interest in the advice. For estimate "
         "reviews and expert support to counsel, frequently. For full claim representation, "
         "almost never: the contingent structure is what aligns our interest with yours.</p>"),
    ],
}

FAQ_PAGE = {
    "path": "/faq/",
    "title": "Public Adjuster FAQ | Texas Commercial Claims Questions",
    "description": ("Answers to the questions boards, councils and facilities directors ask about "
                    "public adjusters, Texas claim deadlines, fees, appraisal and risk pools."),
    "eyebrow": "Questions",
    "h1": "Questions we get<br>in the <em>first</em> call",
    "h1_plain": "Frequently asked questions",
    "lede": ("Grouped by the order people usually ask them. Where an answer is genuinely a legal "
             "question we say so rather than guessing at it."),
    "trail": [("Home", "/"), ("FAQ", None)],
    "sections": [
        {
            "eyebrow": "The basics",
            "h2": "What a public adjuster is",
            "blocks": [("faq", HOME_FAQS)],
        },
        {
            "band": "paper2",
            "eyebrow": "Process",
            "h2": "How a claim actually runs",
            "blocks": [("faq", [
                ("When is the best time to engage someone?",
                 "<p>Before the first carrier inspection, because the scope documented in week one "
                 "is the scope everyone argues from afterwards. In practice most engagements start "
                 "later &mdash; when a short estimate lands, when a file has gone quiet, or after "
                 "a denial. All of those are workable. The genuinely hard case is a claim where "
                 "repairs are finished, records are thin and the limitation period is close.</p>"),
                ("Can we engage you for part of a claim only?",
                 "<p>Yes, and on institutional files that is common: the roofs only, the "
                 "time-element loss only, the disputed supplement only, or appraisal only. The "
                 "engagement letter defines the scope and the fee applies to that scope.</p>"),
                ("What happens if we have already accepted a payment?",
                 "<p>Accepting a payment is not the same as signing a full and final release, and "
                 "most property policies contemplate supplemental claims where the actual cost of "
                 "repair exceeds the estimate. What matters is the policy&rsquo;s own time limits "
                 "and the suit limitation period, which is why a file in that position should be "
                 "looked at quickly.</p>"),
                ("Will you tell us if we do not need you?",
                 "<p>Regularly, and we would rather do it on the first call than after you sign. "
                 "If the loss will not clear the deductible, if the carrier&rsquo;s estimate is "
                 "genuinely thorough, or if the real problem is a coverage denial that needs a "
                 "lawyer rather than an adjuster, that is what we will say.</p>"),
                ("Do you handle the repairs?",
                 "<p>No, and we are prohibited from doing so. Chapter 4102 bars a public adjuster "
                 "from participating directly or indirectly in the repair of property they "
                 "adjusted. You select the contractor; we have no financial relationship with "
                 "anyone in that supply chain.</p>"),
            ])],
        },
        {
            "eyebrow": "Texas specifics",
            "h2": "Statute, deadlines and risk pools",
            "blocks": [("faq", [
                ("What deadlines does Texas law impose on our insurer?",
                 "<p>Under subchapter B of chapter 542, an insurer receiving written notice of a "
                 "claim must generally acknowledge it, begin investigating and request what it "
                 "reasonably needs within 15 days; notify you in writing whether the claim is "
                 "accepted or rejected within 15 business days of receiving the items it "
                 "requested; and pay within 5 business days of an acceptance. Missing those can "
                 "expose the insurer to statutory interest and attorney&rsquo;s fees. The detail "
                 "matters and it is a legal question &mdash; the "
                 "<a href=\"/tools/texas-claim-deadline-calculator/\">deadline calculator</a> is a "
                 "starting point, not advice.</p>"),
                ("What is chapter 542A and does it apply to us?",
                 "<p>Chapter 542A governs claims arising from forces of nature &mdash; wind, hail, "
                 "rain and similar perils. Its most practically important feature is a pre-suit "
                 "notice requirement: written notice to the insurer at least 61 days before "
                 "filing, stating the acts complained of, the amount claimed and the "
                 "attorney&rsquo;s fees incurred. It also affects how interest is calculated. If "
                 "your loss is weather-related, assume it applies and plan the timeline "
                 "accordingly.</p>"),
                ("Our coverage is through a risk pool. Do these rules apply?",
                 "<p>Possibly not in the same way. An interlocal risk pool operates under a "
                 "participation agreement rather than an insurance policy, and the statutory "
                 "machinery aimed at insurers may not reach it. The coverage document governs: "
                 "its notice requirements, its valuation provisions, its appeal process. The "
                 "scope disputes are identical; the leverage differs, and using the wrong "
                 "playbook wastes months.</p>"),
                ("How long do we have to sue?",
                 "<p>Texas commercial policies commonly carry a two-year suit limitation, and "
                 "some wording is shorter. Layer the 61-day pre-suit notice requirement on top "
                 "and the practical deadline to have counsel engaged is materially earlier than "
                 "the limitation date. This is a legal question &mdash; get it confirmed by a "
                 "lawyer rather than relying on any calculator, including ours.</p>"),
            ])],
        },
        {
            "band": "paper2",
            "eyebrow": "Money",
            "h2": "Fees, costs and net recovery",
            "blocks": [("faq", [
                ("How is the fee calculated?",
                 "<p>A percentage of what is recovered, agreed in writing before work starts, "
                 "capped by statute at 10% of the claim settlement. Larger losses normally carry a "
                 "lower rate. Where the carrier has already offered an amount, we normally carve "
                 "it out of the fee base. See <a href=\"/fees/\">fees and engagement terms</a>.</p>"),
                ("What if the claim is denied entirely?",
                 "<p>Then there is no recovery and no fee. Third-party costs you authorised "
                 "directly &mdash; an engineer, an accountant &mdash; remain your cost, which is "
                 "why each one is discussed before it is incurred rather than presented as a bill "
                 "afterwards.</p>"),
                ("Are your fees recoverable from the insurer?",
                 "<p>Generally no. A public adjuster&rsquo;s fee is a cost of pursuing the claim, "
                 "not a covered cost of repair. On a file that later involves litigation, "
                 "attorney&rsquo;s fees may be recoverable under the Insurance Code &mdash; that "
                 "is a question for counsel. Public adjuster fees are also generally not an "
                 "eligible cost under FEMA public assistance, which public entities should factor "
                 "in from the start.</p>"),
            ])],
        },
    ],
}

GLOSSARY_TERMS = [
    ("Actual cash value (ACV)",
     "Replacement cost less depreciation. Commonly the basis for the first payment on a "
     "replacement cost policy, with the balance held back as recoverable depreciation."),
    ("Agreed value",
     "An endorsement suspending the coinsurance clause for the policy term, in exchange for a "
     "signed statement of values the insurer accepts. The cleanest answer to a coinsurance "
     "exposure."),
    ("Anti-concurrent causation",
     "Wording excluding loss caused directly or indirectly by an excluded peril regardless of any "
     "other cause contributing concurrently or in any sequence. The clause at the center of most "
     "coastal wind-versus-water disputes."),
    ("Appraisal",
     "A contractual mechanism for determining the amount of loss when the parties disagree. Each "
     "side appoints an appraiser; the two select an umpire; any two of the three set the amount. "
     "It does not decide coverage."),
    ("Blanket limit",
     "A single limit applying across multiple buildings or locations rather than a separate limit "
     "for each. Usually conditioned on the accuracy of reported values, and frequently subject to "
     "a margin clause."),
    ("Business income",
     "The net profit the operation would have earned plus continuing normal operating expenses, "
     "for the period of restoration. Not lost revenue."),
    ("Civil authority",
     "A time-element extension responding when an order of civil authority prohibits access to "
     "your premises. Usually requires covered physical damage nearby and is short in duration."),
    ("Coinsurance",
     "A clause requiring you to carry insurance of at least a stated percentage of the "
     "property&rsquo;s value. Fall short and every covered loss is reduced by the ratio of what "
     "was carried to what was required."),
    ("Contingent business interruption",
     "Cover for income lost because a supplier, customer or other dependent property sustained "
     "physical damage. Frequently requires the dependent property to be named and is usually "
     "sub-limited."),
    ("Cosmetic damage exclusion",
     "An endorsement removing coverage for damage to roof surfacing that does not affect "
     "function. Increasingly common on Texas commercial property, and decisive on a hail claim "
     "where it appears."),
    ("Deductible, percentage",
     "A retention calculated as a percentage of insured values rather than a flat dollar amount. "
     "Does not scale down with a small loss, and may apply per building or per occurrence."),
    ("Extended period of indemnity",
     "An endorsement covering the ramp-back in income after operations resume, for a stated "
     "number of days. Frequently the last third of a time-element claim."),
    ("Extra expense",
     "Costs incurred to continue operating or to speed the repair, generally recoverable to the "
     "extent they reduce the overall loss."),
    ("Functional replacement cost",
     "A valuation basis permitting repair with modern equivalent materials rather than matching "
     "what was there. Common on older churches and civic buildings."),
    ("Margin clause",
     "An endorsement capping recovery at a stated percentage of the value reported for the "
     "affected location, notwithstanding a larger blanket limit above it."),
    ("Matching",
     "The question of how far replacement must extend into undamaged areas to achieve reasonably "
     "uniform appearance when a product is discontinued or cannot be matched."),
    ("Occurrence",
     "The unit the deductible applies to. Frequently defined for wind and hail as damage within a "
     "continuous period of hours &mdash; 72 is common &mdash; which determines whether a "
     "multi-campus storm is one retention or many."),
    ("Ordinance or law coverage",
     "Cover for the cost of complying with building codes on repair, in three parts: the "
     "undamaged portion required to be demolished (A), demolition cost (B), and increased cost of "
     "construction (C). Each has its own limit."),
    ("Period of restoration",
     "The period that should reasonably be required to repair or replace the damaged property, "
     "exercising due diligence and dispatch. Not the period you were actually closed &mdash; which "
     "is the argument."),
    ("Proof of loss",
     "A sworn statement of the amount claimed. Where required, it starts the carrier&rsquo;s "
     "decision clock rather than leaving the file open-ended."),
    ("Prompt Payment of Claims Act",
     "Subchapter B of chapter 542 of the Texas Insurance Code, setting deadlines for insurers to "
     "acknowledge, decide and pay claims, with statutory interest and attorney&rsquo;s fees "
     "exposure for non-compliance."),
    ("Public adjuster",
     "A professional licensed to represent the policyholder in presenting and negotiating a "
     "claim. In Texas, licensed under chapter 4102, fee capped at 10% of the settlement, and "
     "prohibited from repairing the property adjusted."),
    ("Recoverable depreciation",
     "The amount withheld from a replacement cost claim until the work is completed and "
     "documented. Time-limited under most policies."),
    ("Replacement cost value (RCV)",
     "The cost to repair or replace with materials of like kind and quality, without deduction "
     "for depreciation."),
    ("Risk pool (interlocal)",
     "A coverage arrangement among public entities operating under an interlocal participation "
     "agreement rather than an insurance policy. Its own document governs, and the Insurance "
     "Code&rsquo;s insurer provisions may not apply."),
    ("Service interruption",
     "A time-element extension responding to off-premises failure of power, water, gas or "
     "communications. Frequently requires physical damage to the utility&rsquo;s property and may "
     "exclude overhead transmission lines."),
    ("Statement of values",
     "The schedule of insured values by location reported to the insurer. The document behind "
     "most coinsurance and margin clause problems."),
    ("Subrogation",
     "The insurer&rsquo;s right, after paying, to pursue a third party responsible for the loss. "
     "A reason to preserve failed components."),
    ("Suit limitation",
     "The contractual deadline within which the insured must bring suit. Commonly two years in "
     "Texas commercial policies, sometimes shorter."),
    ("TWIA",
     "The Texas Windstorm Insurance Association, which writes windstorm and hail cover for "
     "property in designated coastal counties and operates its own claim procedures, deadlines "
     "and dispute process."),
]

GLOSSARY = {
    "path": "/glossary/",
    "title": "Commercial Property Insurance Claims Glossary | Texas Terms",
    "description": ("A plain-English glossary of the commercial property insurance terms that "
                    "decide Texas claims: coinsurance, ordinance and law, appraisal and more."),
    "eyebrow": "Reference",
    "h1": "The vocabulary<br>that decides <em>claims</em>",
    "h1_plain": "Commercial property insurance claims glossary",
    "lede": ("Thirty terms, defined the way they actually operate in a Texas commercial claim "
             "rather than the way a textbook would put it."),
    "trail": [("Home", "/"), ("Glossary", None)],
    "sections": [
        {
            "blocks": [("table", "A&ndash;Z", ["Term", "What it means in practice"],
                        [[t, d] for t, d in GLOSSARY_TERMS])],
        },
        {
            "band": "paper2",
            "eyebrow": "Go deeper",
            "h2": "Where these terms are argued.",
            "blocks": [("links", [
                ("Coinsurance explained", "The formula, why institutions fail it, and the three ways out.",
                 "/blog/commercial-property-coinsurance-explained/"),
                ("Ordinance and law coverage", "Three coverages, three limits, and why 10% is rarely enough.",
                 "/blog/ordinance-and-law-coverage-explained/"),
                ("Appraisal or litigation", "Which mechanism fits which dispute.",
                 "/blog/insurance-appraisal-vs-litigation-in-texas/"),
                ("The Texas prompt payment deadlines", "What chapter 542 requires and how to use it.",
                 "/blog/texas-prompt-payment-of-claims-act-deadlines/"),
            ])],
        },
    ],
}

CONTACT = {
    "path": "/contact/",
    "title": "Request a Claim Review | %s" % BIZ["name"],
    "description": ("Request a no-obligation review of a commercial or institutional property "
                    "insurance claim in Texas. Call %s or send the details of your loss." % P),
    "eyebrow": "Contact",
    "h1": "Request a<br>claim <em>review</em>",
    "h1_plain": "Request a claim review",
    "lede": ("The first conversation costs nothing and frequently ends with advice rather than an "
             "engagement. If we do not think representation is worth it on your file, we will say "
             "so."),
    "trail": [("Home", "/"), ("Contact", None)],
    "head_aside": [
        ("ledger", "What to have to hand", [
            ("Declarations page", "Most useful"),
            ("Claim number", "If reported"),
            ("Date of loss", "Exact"),
            ("Carrier or pool", "Name"),
            ("Carrier&rsquo;s estimate", "If received"),
            ("Photographs", "Any at all"),
        ], "None of it is mandatory for a first call. The declarations page alone answers most of "
           "what we would ask."),
    ],
    "sections": [
        {
            "eyebrow": "Send the details",
            "h2": "Tell us about the loss.",
            "dek": "Nothing on this form is stored on this website. Submitting it opens your own "
                   "email client with the details filled in, so you keep a copy and we receive it "
                   "directly.",
            "blocks": [("html", """<form class="formcard" data-contact="%s">
  <div class="field-row field-row--2">
    <div class="field"><label for="c-org">Organization</label>
      <input type="text" name="org" id="c-org" autocomplete="organization"></div>
    <div class="field"><label for="c-name">Your name</label>
      <input type="text" name="name" id="c-name" autocomplete="name"></div>
  </div>
  <div class="field-row field-row--2">
    <div class="field"><label for="c-role">Your role</label>
      <input type="text" name="role" id="c-role" placeholder="Facilities director, business manager, trustee"></div>
    <div class="field"><label for="c-location">Property location</label>
      <input type="text" name="location" id="c-location" placeholder="City and county"></div>
  </div>
  <div class="field-row field-row--2">
    <div class="field"><label for="c-phone">Phone</label>
      <input type="text" name="phone" id="c-phone" autocomplete="tel"></div>
    <div class="field"><label for="c-email">Email</label>
      <input type="email" name="email" id="c-email" autocomplete="email"></div>
  </div>
  <div class="field-row field-row--2">
    <div class="field"><label for="c-dol">Date of loss</label>
      <input type="date" name="dol" id="c-dol"></div>
    <div class="field"><label for="c-cause">Cause of loss</label>
      <select name="cause" id="c-cause">
        <option>Hail</option><option>Wind or named storm</option><option>Fire or smoke</option>
        <option>Water or freeze</option><option>Other or not yet determined</option>
      </select></div>
  </div>
  <div class="field-row field-row--2">
    <div class="field"><label for="c-carrier">Carrier or risk pool</label>
      <input type="text" name="carrier" id="c-carrier"></div>
    <div class="field"><label for="c-status">Claim status</label>
      <select name="status" id="c-status">
        <option>Not yet reported</option><option>Reported, awaiting inspection</option>
        <option>Estimate received, appears short</option><option>Underpaid or partially paid</option>
        <option>Denied</option><option>Closed &mdash; considering a supplement</option>
      </select></div>
  </div>
  <div class="field"><label for="c-message">What happened<span class="hint">A few sentences is plenty. What was damaged, what the carrier has said, and what you need.</span></label>
    <textarea name="message" id="c-message"></textarea></div>
  <div class="btn-row" style="margin-top:8px;">
    <button class="btn" type="submit">Send the details <span class="arw">&rarr;</span></button>
    <a class="btn btn--ghost" href="tel:%s">Call %s instead</a>
  </div>
  <p class="consent" style="margin-top:22px;"><span aria-hidden="true">&mdash;</span>
    <span>Sending this does not create a professional relationship and is not a substitute for
    legal advice. Do not send confidential information you would not want read by anyone other
    than the intended recipient.</span></p>
</form>""" % (E, PH, P))],
        },
        {
            "band": "paper2",
            "eyebrow": "Other ways",
            "h2": "Or just pick up the phone.",
            "blocks": [
                ("p", "For a loss that happened in the last few days, calling is better than "
                      "writing. Most of what matters in the first week is about what to "
                      "photograph and what not to throw away, and that is a ten-minute "
                      "conversation rather than a form."),
                ("ledger", "Direct", [
                    ("Telephone", '<a href="tel:%s">%s</a>' % (PH, P)),
                    ("Email", '<a href="mailto:%s">%s</a>' % (E, E)),
                    ("Based in", "%s, %s" % (BIZ["city"], BIZ["state"])),
                    ("Serving", "Statewide Texas"),
                    ("Hours", "Mon&ndash;Fri, 8am&ndash;6pm CT"),
                    ("After a catastrophe", "Extended"),
                ], "Serving %s." % FOOTER_SERVING),
            ],
        },
    ],
    "faqs": [
        ("Does calling commit us to anything?",
         "<p>No. There is no engagement until a written contract is signed, and a meaningful share "
         "of first calls end with advice and no engagement at all.</p>"),
        ("We are still deciding whether to report the claim. Can you advise before we do?",
         "<p>Yes, and on commercial roofs that is often the right sequence. A pre-notice "
         "assessment tells you whether the damage clears your deductible and whether it will "
         "survive a wear-and-tear challenge. A reported claim you then abandon still appears in "
         "your loss history.</p>"),
        ("How quickly do you respond?",
         "<p>Same business day for anything urgent. After a major regional catastrophe everyone in "
         "the industry is stretched, and we will tell you honestly what we can commit to rather "
         "than booking an inspection we cannot staff.</p>"),
    ],
}

# ---------------------------------------------------------------------------
# Legal
# ---------------------------------------------------------------------------

LEGAL = [
    {
        "path": "/privacy-policy/",
        "title": "Privacy Policy | %s" % BIZ["name"],
        "description": ("How claimsconsultant.com handles information, cookies and inquiries. "
                        "The site has no database and the calculators run in your browser."),
        "eyebrow": "Legal",
        "h1": "Privacy policy",
        "h1_plain": "Privacy policy",
        "lede": "Short, because the site collects very little.",
        "trail": [("Home", "/"), ("Privacy", None)],
        "sections": [{"wrap": "narrow", "blocks": [
            ("h2", "What this site collects"),
            ("p", "This is a static website. It has no database, no user accounts and no server-side "
                  "form processing. The calculators run entirely in your browser: the figures you "
                  "enter are never transmitted, logged or stored anywhere, and they are discarded "
                  "when you close the tab."),
            ("p", "The contact form does not submit to a server. Pressing send opens your own email "
                  "client with the details you entered, so you keep a copy and the message travels "
                  "by ordinary email."),
            ("h2", "Third parties"),
            ("p", "Typefaces are loaded from Google Fonts, which means your browser makes a request "
                  "to Google&rsquo;s servers and Google may log your IP address in the ordinary "
                  "course of serving that request. Your web host keeps standard server access logs. "
                  "If analytics or advertising tags are added to this site in future, this page "
                  "will be updated before they are."),
            ("h2", "Information you send us"),
            ("p", "If you contact us by email or telephone, we keep what you send in order to "
                  "respond to you and, if you engage us, to work your claim. We do not sell it, "
                  "rent it or share it with anyone other than the professionals working on your "
                  "matter with your knowledge, or where we are required to by law."),
            ("h2", "Confidentiality"),
            ("p", "Please do not send confidential or privileged material through an unencrypted "
                  "contact form or by ordinary email. Sending it does not create a professional "
                  "relationship, and email is not a secure channel."),
            ("h2", "Contact"),
            ("p", 'Questions about this policy: <a href="mailto:%s">%s</a>.' % (E, E)),
        ]}],
    },
    {
        "path": "/terms/",
        "title": "Terms of Use | %s" % BIZ["name"],
        "description": ("Terms governing use of claimsconsultant.com, including the calculators, "
                        "the limits of the information published here and governing law."),
        "eyebrow": "Legal",
        "h1": "Terms of use",
        "h1_plain": "Terms of use",
        "lede": "The terms on which this website is made available.",
        "trail": [("Home", "/"), ("Terms", None)],
        "sections": [{"wrap": "narrow", "blocks": [
            ("h2", "Information only"),
            ("p", "This website is published for general information. It does not constitute legal "
                  "advice, an insurance coverage opinion, an appraisal, or a recommendation about "
                  "any particular claim. Coverage is determined by the policy or coverage document "
                  "in force at the date of loss, not by anything written here."),
            ("h2", "No professional relationship"),
            ("p", "Using this site, running a calculator or sending an inquiry does not create an "
                  "adjuster-client relationship. That relationship begins only when a written "
                  "engagement agreement is signed by both parties."),
            ("h2", "Calculators"),
            ("p", "The calculators apply published statutory deadlines and ordinary industry "
                  "conventions to figures you supply. They are planning aids. Outputs are estimates "
                  "only and will not match a properly prepared claim estimate, an appraisal award "
                  "or a legal deadline computed by counsel. Do not rely on them for any decision "
                  "with a deadline attached."),
            ("h2", "Accuracy"),
            ("p", "We take care with what is published here, and statutes, policy forms and market "
                  "costs change. Nothing on this site is warranted to be current, complete or "
                  "applicable to your circumstances."),
            ("h2", "Limitation"),
            ("p", "To the fullest extent permitted by law, we accept no liability for loss arising "
                  "from reliance on this website. Links to third-party sites are provided for "
                  "convenience and imply no endorsement."),
            ("h2", "Governing law"),
            ("p", "These terms are governed by the laws of the State of Texas."),
        ]}],
    },
    {
        "path": "/disclaimer/",
        "title": "Disclaimer | %s" % BIZ["name"],
        "description": ("Professional disclaimer: licensing, scope of services, and the limits of "
                        "the information published on this site."),
        "eyebrow": "Legal",
        "h1": "Disclaimer",
        "h1_plain": "Disclaimer",
        "lede": "What we are, what we are not, and what this site is for.",
        "trail": [("Home", "/"), ("Disclaimer", None)],
        "sections": [{"wrap": "narrow", "blocks": [
            ("h2", "We are public insurance adjusters"),
            ("p", "%s is a public insurance adjusting firm. Public insurance adjusters in Texas are "
                  "licensed and regulated under chapter 4102 of the Texas Insurance Code by the "
                  "Texas Department of Insurance. We represent policyholders in the presentation "
                  "and negotiation of property insurance claims. We do not practice public "
                  "adjusting in states where we are not licensed." % BIZ["name"]),
            ("h2", "We are not a law firm"),
            ("p", "Nothing on this site is legal advice, and we do not provide it. Several topics "
                  "discussed here &mdash; limitation periods, statutory remedies, pre-suit notice "
                  "under chapter 542A, the effect of releases &mdash; are legal questions on which "
                  "you should consult a licensed Texas attorney. Where we think a file needs "
                  "counsel, we say so."),
            ("h2", "We are not contractors"),
            ("p", "We do not repair, restore or reconstruct property, and chapter 4102 prohibits a "
                  "public adjuster from participating directly or indirectly in the repair of "
                  "property they adjusted. We accept no referral fees, commissions or other "
                  "compensation from contractors, restoration companies, engineers or vendors."),
            ("h2", "No guarantee of outcome"),
            ("p", "No firm can guarantee the result of an insurance claim. Every claim turns on its "
                  "own policy wording, facts and evidence. Descriptions of our approach on this "
                  "site describe method, not promised outcomes."),
            ("h2", "Calculators and reference material"),
            ("p", "The calculators, timelines, unit costs and statutory summaries published here "
                  "are planning aids assembled from published sources and ordinary industry "
                  "convention. They are not appraisals, not coverage opinions and not legal "
                  "deadlines. Verify anything with a deadline attached against your policy and "
                  "with counsel."),
        ]}],
    },
    {
        "path": "/accessibility/",
        "title": "Accessibility | %s" % BIZ["name"],
        "description": ("Our approach to accessibility on claimsconsultant.com, the WCAG 2.1 AA "
                        "standard we work to, known limitations and how to report a problem."),
        "eyebrow": "Legal",
        "h1": "Accessibility",
        "h1_plain": "Accessibility statement",
        "lede": "What we have done, and how to tell us when it is not enough.",
        "trail": [("Home", "/"), ("Accessibility", None)],
        "sections": [{"wrap": "narrow", "blocks": [
            ("h2", "Our approach"),
            ("p", "This site is built to be usable with a keyboard, with a screen reader, at high "
                  "zoom levels and with reduced motion enabled. We aim at the WCAG 2.1 AA success "
                  "criteria as a working standard."),
            ("h2", "What that means in practice"),
            ("checks", [
                "Semantic HTML with a single main landmark, one h1 per page and a logical heading order.",
                "A visible skip link, visible focus indicators throughout, and no keyboard traps.",
                "Text contrast tested against AA thresholds in both the light and dark sections of the design.",
                "Every form control has a persistent visible label rather than a placeholder standing in for one.",
                "Animation is limited and respects the prefers-reduced-motion setting.",
                "Text reflows without horizontal scrolling down to a 320px viewport, and the layout holds at 200% zoom.",
                "Tables carry captions and header cells with scope, so they are navigable by screen reader.",
            ]),
            ("h2", "Known limitations"),
            ("p", "Some data tables are wide and scroll horizontally on small screens. Typefaces are "
                  "loaded from a third-party service; if that service is unavailable, the site "
                  "falls back to system fonts and remains fully usable."),
            ("h2", "Tell us"),
            ("p", 'If anything on this site is difficult or impossible for you to use, please email '
                  '<a href="mailto:%s">%s</a> or call <a href="tel:%s">%s</a>. Tell us the page and '
                  'what happened, and we will fix it. If you need any information on this site in '
                  'another format, ask and we will provide it.' % (E, E, PH, P)),
        ]}],
    },
]
