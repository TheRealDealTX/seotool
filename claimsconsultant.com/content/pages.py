"""Standing pages: firm, method, fees, FAQ, glossary, contact, legal.

Also the shared FAQ list used on the homepage and the hub-page introductions,
which live here so the hubs are not thin.
"""

from siteconfig import BIZ, STANDARDS, FEES, FOOTER_SERVING

P = BIZ["phone_display"]
PH = BIZ["phone_href"]
E = BIZ["email"]

# ---------------------------------------------------------------------------
HOME_FAQS = [
    ("What is a claims consultant, and how is that different from an adjuster?",
     "<p>An adjuster works a claim on behalf of a party to it &mdash; a staff or independent "
     "adjuster for the insurer, a public adjuster for the policyholder. A claims consultant is "
     "retained to establish facts: what was damaged, what it costs to repair, how long the "
     "operation was interrupted and what that was worth. We produce the measurement and the "
     "analysis. What the parties then do with it is their business, and we are equally willing "
     "to hand the same work to either of them.</p>"),

    ("You work for policyholders and for insurers. Isn&rsquo;t that a conflict?",
     "<p>Not on a given matter, because we run a conflict check before taking one and we never "
     "act for both parties to the same loss. Across matters it is the point rather than the "
     "problem. A consultant who only ever produces numbers for one side learns to write numbers "
     "that side likes, and everyone in the industry knows it. Working both sides is what keeps "
     "the methodology honest &mdash; and it is why our analysis survives scrutiny in appraisal "
     "and in court.</p>"),

    ("How are you paid?",
     "<p>Consulting and expert engagements are billed hourly, or at a fixed fee where the "
     "deliverable is well defined. Public adjusting is on a contingent fee, capped by Texas "
     "statute at %s. Whichever applies is agreed in writing before work starts, against a "
     "written estimate of hours where the work is hourly.</p>" % FEES["pa_cap"]),

    ("We are a church / district / city. Do the usual insurance rules even apply to us?",
     "<p>Not always, and establishing which rules apply is the first thing we do. A great many "
     "Texas public entities and religious organizations cover property through an interlocal "
     "risk pool or a denominational program rather than a conventional insurance policy. Those "
     "are governed by their own coverage documents, with their own valuation provisions and "
     "their own appeal routes rather than the rules that apply to an insurance policy. The "
     "technical questions are identical; the procedure is not.</p>"),

    ("Can you serve as an appraiser or umpire?",
     "<p>Yes, in any of the three roles. As a party-appointed appraiser for either side, or as "
     "umpire where both appraisers will accept us. Umpire work in particular depends on being "
     "genuinely impartial and being seen to be, which is difficult for a firm that only ever "
     "works one side. We disclose prior engagements with either party before accepting any "
     "appraisal role.</p>"),

    ("How long will this take?",
     "<p>A scope and estimate on a single commercial building is typically two to four weeks "
     "from access. A large institutional loss with engineering, code analysis and a time-element "
     "component runs considerably longer, and the pace is usually set by access, records and "
     "third-party specialists rather than by us. We give a schedule with the engagement and tell "
     "you when it slips.</p>"),

    ("What size of matter do you take?",
     "<p>Large commercial and institutional property only. That is a deliberate focus rather "
     "than a boast: full-property surveys, specialist engagement and forensic accounting are "
     "proportionate on a large loss and wasteful on a small one. If a matter is modest, we will "
     "say so and point you somewhere more suitable rather than take it.</p>"),
]

# ---------------------------------------------------------------------------
# Hub page introductions
# ---------------------------------------------------------------------------

INDUSTRY_HUB_INTRO = [
    {
        "eyebrow": "Why it matters",
        "h2": "The property type changes the argument, not just the vocabulary.",
        "blocks": [
            ("p", "A hail loss on a warehouse and a hail loss on a school district are not the "
                  "same file with a different address. The district has a per-building deductible "
                  "applied across nineteen campuses, a coverage document that may be an "
                  "interlocal agreement rather than an insurance policy, a board that has to "
                  "approve the outcome in public, and a hard deadline in August. None of that "
                  "appears in the estimating software."),
            ("p", "We work a narrow set of property types on purpose. Each of the pages below "
                  "sets out the wording, the valuation problem and the political constraint "
                  "peculiar to that kind of owner &mdash; because knowing which question a file "
                  "actually turns on is most of the work, whichever party is asking."),
        ],
        "aside": [
            ("callout", "Large commercial only", [
                ("p", "We do not take residential matters, and we decline commercial losses too "
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
                "<strong>Nobody is running the time-element side.</strong> Interruption and extra expense are real on institutional losses and almost never documented while they are happening &mdash; which hurts whichever party later has to prove or test them.",
            ]),
        ],
    },
]

LOSS_HUB_INTRO = [
    {
        "eyebrow": "Why it is split this way",
        "h2": "The peril decides the evidence. The service decides the deliverable.",
        "blocks": [
            ("p", "A hail file and a freeze file need the same things from us &mdash; a scope, "
                  "a cost, a causation opinion, sometimes testimony. What differs completely is "
                  "the evidence that answers the question, and how fast it disappears. Test cuts "
                  "and soft-metal spatter settle a hail argument. Building management system "
                  "logs and a retained section of failed pipe settle a freeze argument. Neither "
                  "helps with the other."),
            ("p", "These six pages set out what each kind of loss turns on, what tends to get "
                  "under-scoped, and which specialist the question eventually needs."),
        ],
        "aside": [
            ("callout", "Evidence has a shelf life", [
                ("p", "On most of these, the material that would settle the dispute is gone "
                      "within weeks &mdash; cleaned, tarped, dried, demolished or repaired. It "
                      "is the single strongest argument for an early inspection, whichever side "
                      "is asking."),
            ]),
        ],
    },
]

SERVICE_HUB_INTRO = [
    {
        "eyebrow": "How to use this",
        "h2": "The first five are causes of loss. The last four are stages.",
        "blocks": [
            ("p", "The first four are the analytical core of the practice: testimony, "
                  "causation, cost estimating and appraisal. Most engagements are one of those, "
                  "and most of them start as a single narrow question rather than as a whole "
                  "claim."),
            ("p", "The next three are technical reports we are asked for by name &mdash; soot, "
                  "smoke and mold testing, cabinet repairability, contents itemizing and "
                  "pricing. They are narrow, they are frequently decisive, and they are cheap "
                  "relative to the argument they settle."),
            ("p", "The last two are different in kind. Public adjusting is the one capacity "
                  "where we act as a party&rsquo;s representative rather than establishing "
                  "facts. Policy review works best before there is a claim at all."),
        ],
        "aside": [
            ("ledger", "Engagement shapes", [
                ("Full scope &amp; estimate", "Most common"),
                ("Disputed portion only", "Frequent"),
                ("Appraiser or umpire", "Available"),
                ("Estimate critique", "Fixed fee"),
                ("Policy review", "Fixed fee"),
                ("Expert report &amp; testimony", "Available"),
            ], "Not every matter needs the whole service. The engagement letter defines the scope "
               "and the capacity we are acting in."),
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
                  "evidence that settles a particular question, the records to start keeping on "
                  "day one. If a draft reads like a brochure with subheadings, it does not go "
                  "up. Nothing here is written for one side of a file."),
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
    "title": "About the Firm | Texas Independent Claims Consultants",
    "description": ("%s is an independent claims consulting firm working large Texas commercial "
                    "and institutional property losses for policyholders, insurers, pools and "
                    "counsel." % BIZ["name"]),
    "eyebrow": "The firm",
    "h1": "We are not on<br>a <em>side</em>. We are on the facts.",
    "h1_plain": "About Claims Consultant",
    "lede": ("Independence is not a slogan here, it is the business model. We bill for the work "
             "rather than a share of the result, we take matters from either party, and the "
             "method does not change depending on who signed the engagement."),
    "trail": [("Home", "/"), ("The firm", None)],
    "head_aside": [
        ("ledger", "Practice profile", [
            ("Focus", "Large commercial"),
            ("Sectors", "Institutional"),
            ("Territory", "Texas"),
            ("Licensed", "Ch. 4101 &amp; 4102"),
            ("Retained by", "Either party"),
            ("Consulting fee", "Hourly"),
        ], "Texas adjuster and public insurance adjuster licences are both held, which is what "
           "allows either party to retain us. Not a law firm, not a contractor, not an agency."),
    ],
    "sections": [
        {
            "eyebrow": "Position",
            "h2": "A number is only worth what it survives.",
            "blocks": [
                ("p", "Every large property loss produces at least two estimates and a gap "
                      "between them. The gap is usually not fraud and usually not coverage. It is "
                      "dozens of judgment calls &mdash; effective age, repairability, matching, "
                      "code triggers, overhead and profit, the period of restoration &mdash; made "
                      "by people who each have a position, on measurements nobody took to an "
                      "evidentiary standard."),
                ("p", "We take those measurements. Then we state, in writing, what we concluded "
                      "and why, with the evidence attached. That document has to hold up in front "
                      "of a forensic accountant, an appraisal panel, a code official or a court, "
                      "and it has to hold up whichever party is reading it."),
                ("p", "Consulting and expert engagements are billed hourly, so the conclusion "
                      "costs the same whether it helps the client or not. Public adjusting, where "
                      "we act as the policyholder&rsquo;s representative, is on a contingent fee "
                      "capped by statute. Which capacity applies is settled in the engagement "
                      "letter before any work begins."),
            ],
            "aside": [
                ("callout", "One capacity per matter", [
                    ("p", "We hold both a Texas adjuster licence and a public insurance adjuster "
                          "licence. Holding both is what lets either party retain us; it is not "
                          "a licence to face both ways at once. On any individual matter we act "
                          "in one capacity, stated in the engagement letter, and we never act "
                          "for both parties to the same loss."),
                ]),
                ("callout", "What we are not", [
                    ("p", "Not a law firm &mdash; we do not give legal advice, and when a matter "
                          "needs counsel we say so. Not a contractor &mdash; we do not repair "
                          "what we assess, and we take no referral money from anyone who does. "
                          "Not an agency &mdash; we do not sell insurance."),
                ]),
            ],
        },
        {
            "band": "paper2",
            "eyebrow": "Focus",
            "h2": "Institutional and large commercial. Nothing else.",
            "blocks": [
                ("p", "Most consulting firms take whatever comes. We do not, for a practical "
                      "reason: the way we work a file &mdash; full-property survey rather than a "
                      "sample, specialist engagement where the loss warrants it, forensic "
                      "accounting on the time-element side &mdash; is proportionate on a large "
                      "institutional loss and absurd on a small one."),
                ("p", "So the practice is built around a narrow set of properties: churches and "
                      "faith organizations, school districts, cities and municipal entities, "
                      "colleges and universities, healthcare facilities, multifamily and "
                      "commercial portfolios. What those have in common is complex property, "
                      "complex coverage, and somebody who has to justify the outcome to a board, "
                      "a regulator, an auditor or a court."),
                ("html", '<a class="tlink" href="/who-we-serve/">Property types we work '
                         '<span class="arw">&rarr;</span></a>'),
            ],
        },
        {
            "band": "ink",
            "eyebrow": "Commitments",
            "h2": "Six things we do, and one we will not.",
            "blocks": [
                ("checks", [
                    "Run a conflict check before discussing any matter in detail, and decline where we are already engaged on the other side.",
                    "Put the scope of work, the rate and an estimate in writing before any work starts.",
                    "Read the policy or coverage document before walking the building, and explain what it says in plain language.",
                    "Document the whole property, not a representative sample of it.",
                    "Discuss every third-party cost before it is incurred.",
                    "Say early when a matter needs an attorney, a licensed adjuster or a specialist rather than more consulting.",
                ]),
                ("p", "The one we will not: shade a conclusion toward the party paying for it. "
                      "On matters this size the file is frequently examined by a forensic "
                      "accountant, an opposing expert, an appraisal panel or a court. A scope "
                      "padded or trimmed to suit a client destroys the credibility of the forty "
                      "findings around it that were right &mdash; and it ends the only thing this "
                      "firm actually sells."),
            ],
        },
        {
            "eyebrow": "Practicalities",
            "h2": "Working with us.",
            "blocks": [
                ("steps", [
                    ("The first call costs nothing",
                     "<p>Fifteen minutes, usually with the declarations page in front of you. We "
                     "run a conflict check, tell you what we think the matter needs, and whether "
                     "that is us. A meaningful share of these calls end with advice and no "
                     "engagement.</p>"),
                    ("A written engagement, or nothing",
                     "<p>Scope, rate, estimate, deliverables and the assumptions we are working "
                     "from, in writing, before work begins. Institutional clients need something "
                     "a board, a panel or a procurement officer can read; so do we.</p>"),
                    ("One point of contact, and a paper trail",
                     "<p>You get a named consultant who is actually on the file, not a "
                     "salesperson who hands you to a queue. Everything material goes in writing, "
                     "and at closeout you receive the complete record &mdash; photographs, "
                     "measurements, estimates, correspondence &mdash; whether or not you ever "
                     "need it again.</p>"),
                ]),
            ],
        },
    ],
    "faqs": [
        ("Are you licensed?",
         "<p>Yes &mdash; in Texas, both as an adjuster under chapter 4101 of the Insurance Code "
         "and as a public insurance adjuster under chapter 4102. Holding both is unusual and it "
         "is deliberate: it is what allows an insurer and a policyholder to retain the same "
         "firm, in different matters, without either one being served by somebody working "
         "outside their licence. Licence numbers are published in the footer and can be verified "
         "with the Texas Department of Insurance. Where a matter needs an attorney rather than a "
         "consultant, we say so.</p>"),
        ("Do you work outside Texas?",
         "<p>Our practice is Texas and the Gulf Coast. Consulting and expert work travels more "
         "easily than licensed activity does, so on a portfolio with property in several states "
         "we can usually help &mdash; and we will say plainly which parts we can handle ourselves "
         "and which need local counsel or a locally licensed professional.</p>"),
        ("Do you take residential matters?",
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
                ("html", '<div class="btn-row"><a class="btn btn--brass" href="/contact/">Discuss a matter '
                         '<span class="arw">&rarr;</span></a>'
                         '<a class="btn btn--ghost" href="/services/insurance-appraisal/">About appraisal</a></div>'),
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

FEES_PAGE = {
    "path": "/fees/",
    "title": "Fees &amp; Engagement Terms | Expert Witness &amp; Consulting",
    "description": ("How we bill: hourly on consulting and expert work, contingent on public "
                    "adjusting. Third-party costs, conflict checks and public-entity "
                    "procurement."),
    "eyebrow": "Commercial terms",
    "h1": "Paid for the work,<br>not the <em>outcome</em>",
    "h1_plain": "Fees and engagement terms",
    "lede": ("Boards and councils have to approve this in public and carriers have to reconcile "
             "it against a vendor schedule, so it needs to be simple enough to put in a packet "
             "and specific enough to survive an audit."),
    "trail": [("Home", "/"), ("Fees", None)],
    "head_aside": [
        ("ledger", "The commercial terms", [
            ("Consulting &amp; expert", "Hourly / fixed"),
            ("Public adjusting", "Contingent"),
            ("Statutory cap on PA fee", "10%"),
            ("Estimate", "In writing, up front"),
            ("Third-party costs", "Client, pre-authorized"),
            ("Conflict check", "Before any detail"),
        ], "Every one of these is written into the engagement letter before work starts."),
    ],
    "sections": [
        {
            "eyebrow": "The fee",
            "h2": "Hourly on consulting. Contingent on public adjusting.",
            "blocks": [
                ("p", "Consulting, expert, estimating and appraisal engagements are billed "
                      "hourly, agreed in writing before work begins and quoted against a written "
                      "estimate of the hours a matter should take. Where the deliverable is well "
                      "defined &mdash; a scope and estimate on a single building, a policy "
                      "review, an estimate critique &mdash; we quote a fixed fee instead."),
                ("p", "Public adjusting is different. There we act as the policyholder&rsquo;s "
                      "representative rather than establishing facts, and the engagement is on a "
                      "contingent fee, capped by Texas statute at %s of the claim settlement "
                      "(%s). Where an amount has already been offered we normally carve it out "
                      "of the fee base." % (FEES["pa_cap"], FEES["pa_cite"])),
                ("p", "Which capacity applies is settled in the engagement letter before "
                      "anything starts, because it changes the fee, the relationship and how the "
                      "work will be characterized by the other side."),
            ],
            "aside": [
                ("callout", "Estimates, and when they move", [
                    ("p", "Every engagement carries a written estimate of hours. If a matter "
                          "starts running toward it &mdash; access problems, a scope that turns "
                          "out to be three buildings, records that do not exist &mdash; you hear "
                          "about it before the number is passed, not on the invoice."),
                ]),
            ],
        },
        {
            "band": "paper2",
            "eyebrow": "Third-party costs",
            "h2": "Specialists are a separate, pre-authorized cost.",
            "blocks": [
                ("p", "Engineers, forensic accountants, industrial hygienists, roofing "
                      "consultants and laboratory testing are engaged where a loss warrants "
                      "them, and they are the client&rsquo;s direct cost rather than ours. On a "
                      "large institutional matter those costs can be substantial, which is "
                      "precisely why each one is discussed and authorized before it is incurred. "
                      "You will not receive a bill for something you did not agree to."),
                ("table", "Who pays for what", ["Item", "Paid by"], [
                    ["Our consulting time", "Client, at the agreed hourly or fixed rate"],
                    ["Engineers and technical consultants", "Client, authorized in advance"],
                    ["Forensic accounting", "Client, authorized in advance"],
                    ["Appraiser fee where we serve as a party appraiser", "The appointing party, per the policy&rsquo;s appraisal clause"],
                    ["Umpire fee where we serve as umpire", "Normally split between the parties"],
                    ["Expert testimony and deposition time", "Client, at the posted testimony rate"],
                    ["Legal representation", "Client, under separate engagement with counsel"],
                 ]),
            ],
        },
        {
            "eyebrow": "Conflicts",
            "h2": "We check before we listen.",
            "blocks": [
                ("p", "Because we act for both policyholders and insurers, a conflict check "
                      "comes before any detailed discussion of a matter &mdash; not after. Tell "
                      "us the property, the date of loss and the parties, and we will confirm "
                      "within a day whether we are clear. If we are already engaged on the other "
                      "side, we say so immediately and you tell us nothing further."),
                ("checks", [
                    "We never act for both parties to the same loss.",
                    "Prior engagements with either party are disclosed before we accept any appraisal or umpire role.",
                    "We take no referral fees, commissions or other compensation from contractors, restoration firms, engineers or vendors.",
                    "We do not repair, restore or rebuild property we have assessed.",
                    "Where we have served as a testifying expert against a party, we disclose it before accepting work for them.",
                ]),
            ],
        },
        {
            "band": "ink",
            "eyebrow": "For public entities",
            "h2": "Documentation your procurement process will want.",
            "blocks": [
                ("p", "School districts, cities and other public entities have their own "
                      "procurement rules for professional services, and your purchasing officer "
                      "and counsel &mdash; not us &mdash; determine how they apply. An hourly "
                      "professional-services engagement is a familiar shape to that process, "
                      "which is the usual shape of a consulting engagement."),
                ("checks", [
                    "A written scope of services suitable for an agenda item or board packet.",
                    "Hourly rates by role, a not-to-exceed figure, and a written estimate of hours.",
                    "Proof of professional liability insurance.",
                    "Written confirmation that we take no compensation from contractors or vendors on the matter.",
                    "A stated termination provision.",
                    "Status reporting at a cadence that matches your meeting cycle.",
                ]),
            ],
        },
    ],
    "faqs": [
        ("Which engagements are hourly and which are contingent?",
         "<p>Consulting, expert, estimating and appraisal work is hourly or fixed fee. Public "
         "adjusting is contingent, capped at %s by statute. The split follows the capacity: in "
         "the first group we are establishing facts for whoever asks, and an opinion that moves "
         "with the outcome is worth less to everyone, including the client. In the second we are "
         "the policyholder&rsquo;s representative, which is the role a contingent fee is built "
         "for.</p>" % FEES["pa_cap"]),
        ("Is the cost worth it on a smaller loss?",
         "<p>Often not, and we will say so. Below a certain size the cost of a full survey, a "
         "line-item scope and any specialist input is disproportionate to the amount in dispute. "
         "A single fixed-fee estimate review is sometimes the right answer instead &mdash; and "
         "sometimes the right answer is that you do not need us at all.</p>"),
        ("Can we cap the spend?",
         "<p>Yes. Most institutional engagements carry a not-to-exceed figure, and phased "
         "engagements are common: an initial assessment at a fixed fee, then a decision about "
         "whether the full scope is justified. We would rather structure it that way than "
         "present a surprise.</p>"),
    ],
}

FAQ_PAGE = {
    "path": "/faq/",
    "title": "Claims Consulting FAQ | Texas Commercial Property Questions",
    "description": ("Answers to what boards, councils, carriers and counsel ask about independent "
                    "claims consulting, Texas claim deadlines, fees, appraisal and risk pools."),
    "eyebrow": "Questions",
    "h1": "Questions we get<br>in the <em>first</em> call",
    "h1_plain": "Frequently asked questions",
    "lede": ("Grouped by the order people usually ask them. Where an answer is genuinely a legal "
             "question we say so rather than guessing at it."),
    "trail": [("Home", "/"), ("FAQ", None)],
    "sections": [
        {
            "eyebrow": "The basics",
            "h2": "What a claims consultant is",
            "blocks": [("faq", HOME_FAQS)],
        },
        {
            "band": "paper2",
            "eyebrow": "Independence",
            "h2": "Working both sides",
            "blocks": [("faq", [
                ("What licences do you hold?",
                 "<p>Texas adjuster (chapter 4101) and Texas public insurance adjuster (chapter "
                 "4102). Both, which is what makes it possible for an insurer to retain us on "
                 "one matter and a policyholder on another without anyone being served outside a "
                 "licence. On any single matter we act in one capacity only, named in the "
                 "engagement letter. Numbers are in the footer; verify them with TDI.</p>"),
                ("How do you handle conflicts?",
                 "<p>A conflict check runs before any detailed discussion of a matter. Give us "
                 "the property, the date of loss and the parties and we confirm within a day. We "
                 "never act for both parties to the same loss, and if we are already engaged on "
                 "the other side we say so immediately and you tell us nothing further.</p>"),
                ("Does your analysis change depending on who hired you?",
                 "<p>No, and that is testable. The same methodology, the same estimating "
                 "platform, the same evidentiary standard for every judgment call. What changes "
                 "with the client is which questions we are asked to answer, not what the "
                 "answers are. Anyone can check this the same way opposing counsel does &mdash; "
                 "by reading our work on matters where we were retained by the other side.</p>"),
                ("Can you serve as an appraiser or an umpire?",
                 "<p>Yes, in any of the three roles: party appraiser for either side, or umpire "
                 "where both appraisers accept us. Umpire work depends on being impartial and "
                 "being seen to be, so we disclose prior engagements with either party before "
                 "accepting any appraisal role.</p>"),
                ("Do you give expert testimony?",
                 "<p>Yes, for either party, subject to conflict check. Scope and cost opinions, "
                 "damage causation within our competence, time-element quantification and "
                 "critiques of an opposing estimate. Testimony time is billed hourly at a "
                 "posted rate, which is the first thing you will be asked about on "
                 "cross.</p>"),
            ])],
        },
        {
            "eyebrow": "Process",
            "h2": "How an engagement runs",
            "blocks": [("faq", [
                ("When is the best time to bring you in?",
                 "<p>Before the property changes. The scope documented in the first weeks is the "
                 "scope everyone argues from afterwards, and once tarps go up and crews clean, "
                 "evidence is gone for good. In practice most engagements start later &mdash; "
                 "when two estimates are far apart, when a file has stalled, or when appraisal "
                 "or litigation is in view. All of those are workable.</p>"),
                ("Can you take part of a matter only?",
                 "<p>Yes, and on institutional files that is common: the roofs only, the "
                 "time-element quantification only, a critique of an opposing estimate only, "
                 "appraisal only. The engagement letter defines the scope and the fee applies to "
                 "that scope.</p>"),
                ("What do you need from us to start?",
                 "<p>The declarations page and the full policy or coverage document, the claim "
                 "number, any estimates and reports already produced, and access to the "
                 "property. Everything else we can assemble. On a time-element matter we also "
                 "need somebody in finance who can pull records.</p>"),
                ("Do you handle repairs?",
                 "<p>No. We do not repair, restore or rebuild property we have assessed, and we "
                 "take no referral money from anyone who does. You select the contractor.</p>"),
            ])],
        },
        {
            "band": "paper2",
            "eyebrow": "Evidence and access",
            "h2": "Getting to the property, and what survives",
            "blocks": [("faq", [
                ("How quickly do you need to inspect?",
                 "<p>As soon as the property is safe and access can be arranged. High-water "
                 "marks survive days. A failed pipe survives until the plumber throws it out. "
                 "Building management logs frequently roll off in thirty to ninety days. Cabinet "
                 "substrate and roof assemblies survive until the repair. None of that is "
                 "recoverable later, and every item on the list settles an argument.</p>"),
                ("Can you work from photographs if the property is already repaired?",
                 "<p>Sometimes, and the resulting opinion is qualified accordingly. The usable "
                 "sources are contractor photographs and invoices, change orders, retained "
                 "materials, pre-loss survey or drone imagery, maintenance records and testing "
                 "done at the time. We will tell you plainly whether what survives supports a "
                 "conclusion rather than producing one that cannot be defended.</p>"),
                ("Do you need the other side present at the inspection?",
                 "<p>Not required, and frequently a good idea &mdash; particularly for "
                 "destructive testing. A joint inspection with both parties invited in writing "
                 "removes an entire category of later objection about what was done and what it "
                 "showed. Where an invitation is declined, the fact that it was made is itself "
                 "worth recording.</p>"),
                ("Our coverage is through a risk pool rather than an insurer. Does that change your work?",
                 "<p>Not the technical work, which is identical. What changes is the procedure: "
                 "an interlocal pool operates under a participation agreement rather than a "
                 "standard policy, with its own notice requirements, valuation provisions and "
                 "appeal route. It has to be read rather than assumed.</p>"),
            ])],
        },
        {
            "eyebrow": "Money",
            "h2": "Fees and costs",
            "blocks": [("faq", [
                ("How is the fee calculated?",
                 "<p>Hourly or fixed fee, agreed in writing before work starts, against a "
                 "written estimate of hours, on consulting and expert engagements. Public "
                 "adjusting is on a contingent fee capped by statute at 10%. See "
                 "<a href=\"/fees/\">fees and engagement terms</a>.</p>"),
                ("Who pays for engineers and accountants?",
                 "<p>The client, directly, and only where authorized in advance. Each specialist "
                 "is discussed before engagement rather than presented as a line on an invoice "
                 "afterwards.</p>"),
                ("Are consulting fees recoverable from the insurer?",
                 "<p>Generally no. Consulting costs are a cost of investigating or pursuing a "
                 "matter, not a covered cost of repair, though certain professional fees "
                 "genuinely required to execute the repair &mdash; design professionals, for "
                 "instance &mdash; are a different question. Where litigation is involved, "
                 "recoverability of fees and costs is a matter for counsel. Consulting fees are "
                 "also generally not an eligible cost under FEMA public assistance, which public "
                 "entities should factor in from the start.</p>"),
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
    ("Repairability",
     "Whether repair restores an item to its pre-loss condition and remaining service life. "
     "Not whether repair is physically possible, which it nearly always is."),
    ("Public adjuster",
     "A professional licensed to represent the policyholder in presenting and negotiating a "
     "claim, and paid by the policyholder. Distinct from a claims consultant, who is retained "
     "to establish facts rather than to act as a party&rsquo;s representative."),
    ("Claims consultant",
     "An independent professional retained to assess damage, produce scope and cost analysis, "
     "quantify time-element loss and give expert opinion. May be retained by either party, and "
     "is normally paid for the work rather than a share of the outcome."),
    ("Umpire",
     "The third member of an appraisal panel, selected by the two party-appointed appraisers or "
     "appointed by a court. Where the appraisers disagree, the umpire&rsquo;s agreement with "
     "either of them produces a binding award."),
    ("Independent adjuster (IA)",
     "An adjuster who works for insurers on a contract basis rather than as an employee. "
     "Independent of the insurer&rsquo;s payroll, not of its interest."),
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
                ("Repair or replace", "The test, and the evidence that settles it.",
                 "/blog/repair-or-replace-how-the-decision-gets-made/"),
            ])],
        },
    ],
}

CONTACT = {
    "path": "/contact/",
    "title": "Contact | Discuss a Matter | %s" % BIZ["name"],
    "description": ("Discuss a commercial or institutional property loss in Texas with an "
                    "independent claims consultant. Conflict check first. Call %s." % P),
    "eyebrow": "Contact",
    "h1": "Discuss a<br><em>matter</em>",
    "h1_plain": "Discuss a matter",
    "lede": ("The first conversation costs nothing and frequently ends with advice rather than "
             "an engagement. Tell us the property, the date of loss and the parties, and we will "
             "run a conflict check before anything else is discussed."),
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

CLIENTS = {
    "path": "/who-we-work-for/",
    "title": "Who We Work For | Policyholders, Insurers, Pools &amp; Counsel",
    "description": ("Independent claims consulting retained by policyholders, insurance "
                    "carriers, third-party administrators, risk pools, brokers and attorneys on "
                    "large Texas property losses."),
    "eyebrow": "Clients",
    "h1": "Six kinds of client,<br><em>one</em> methodology",
    "h1_plain": "Who we work for",
    "lede": ("Most consulting firms in this market pick a side and stay there. We did not, and "
             "the reason is practical rather than high-minded: work that is only ever produced "
             "for one party eventually reads that way, and everyone on the other side learns to "
             "discount it."),
    "trail": [("Home", "/"), ("Who we work for", None)],
    "head_aside": [
        ("ledger", "Engagement rules", [
            ("Conflict check", "Before any detail"),
            ("Both parties, same loss", "Never"),
            ("Capacity per matter", "One, stated"),
            ("Consulting fee", "Hourly / fixed"),
            ("PA fee", "Contingent"),
            ("Referral money", "None taken"),
        ], "The rules are the same whoever is paying, which is the only reason the analysis is "
           "worth anything to either of them."),
    ],
    "sections": [
        {
            "eyebrow": "The clients",
            "h2": "Who retains us, and what for.",
            "blocks": [
                ("cards", [
                    ("Policyholders &amp; owners",
                     "Churches, districts, cities, campuses, portfolios and large commercial "
                     "owners who need the loss measured properly before it is presented, or a "
                     "second opinion on an estimate that looks thin.",
                     "/who-we-serve/"),
                    ("Insurance carriers",
                     "Scope verification and cost review on large or unusual losses, specialist "
                     "assessment where the in-house estimate needs support, and independent "
                     "critique of a presented claim.",
                     "/loss-types/commercial-property-damage-claims/"),
                    ("TPAs &amp; independent adjusting firms",
                     "Surge capacity and technical depth on files past the point where a general "
                     "estimating platform helps &mdash; complex roofs, production equipment, "
                     "laboratory and healthcare environments.",
                     "/loss-types/hail-damage-claims/"),
                    ("Risk pools &amp; self-insureds",
                     "Interlocal pools and entities carrying large retentions, where the "
                     "coverage document is not a standard policy and the appeal route is its "
                     "own.",
                     "/who-we-serve/school-districts/"),
                    ("Brokers &amp; risk managers",
                     "Pre-loss program review, statement-of-value testing, and an independent "
                     "technical read when a client&rsquo;s claim is not moving.",
                     "/services/policy-review-and-pre-loss-consulting/"),
                    ("Attorneys, either side",
                     "Expert reports, estimate critiques, damage and cost opinions, deposition "
                     "and trial testimony &mdash; for policyholder counsel and for coverage and "
                     "defense counsel alike.",
                     "/services/insurance-appraisal/"),
                ]),
            ],
        },
        {
            "band": "paper2",
            "eyebrow": "How it holds together",
            "h2": "Three rules that make working both sides possible.",
            "blocks": [
                ("steps", [
                    ("Conflicts are checked before the conversation, not after",
                     "<p>Give us the property, the date of loss and the parties. We confirm "
                     "within a day whether we are clear. If we are already engaged on the other "
                     "side we say so immediately and you tell us nothing further. We never act "
                     "for both parties to the same loss, and we do not take a matter adverse to "
                     "a client we are currently engaged by.</p>"),
                    ("Consulting and expert work is billed hourly",
                     "<p>Hourly or fixed fee, agreed in writing, on every consulting, expert, "
                     "estimating and appraisal engagement. A consultant paid a share of the "
                     "recovery cannot credibly be retained by an insurer, and one paid a bonus "
                     "for a low number cannot credibly be retained by a policyholder. Public "
                     "adjusting is the exception and is contingent, because there we are a "
                     "party&rsquo;s representative rather than a neutral measurer.</p>"),
                    ("One capacity per matter, stated up front",
                     "<p>Consultant, party-appointed appraiser, umpire or adjuster &mdash; named "
                     "in the engagement letter before work starts. Where we are asked to serve "
                     "as umpire, prior engagements with either party are disclosed to both "
                     "appraisers first, and either can decline us.</p>"),
                ]),
            ],
        },
        {
            "band": "ink",
            "eyebrow": "The test",
            "h2": "You can check this yourself.",
            "dek": "The usual way to evaluate an expert is to ask who else they have worked for. "
                   "That question is the whole answer here.",
            "blocks": [
                ("p", "Ask for matters where we were retained by the party opposite to you and "
                      "read what we concluded. Ask whether our methodology, unit costs or "
                      "depreciation approach differ depending on who is paying. Ask what we have "
                      "written when the answer was unhelpful to the client &mdash; because on a "
                      "practice built this way, that happens regularly and it is the point."),
                ("p", "An expert whose opinions correlate perfectly with whoever retained them "
                      "is not an expert. They are a witness for hire with a technical vocabulary, "
                      "and a competent cross-examiner will establish that in about four "
                      "minutes."),
                ("html", '<div class="btn-row"><a class="btn btn--brass" href="/contact/">'
                         'Run a conflict check <span class="arw">&rarr;</span></a>'
                         '<a class="btn btn--ghost" href="/fees/">Fees &amp; engagement</a></div>'),
            ],
        },
    ],
    "faqs": [
        ("Doesn&rsquo;t working for insurers compromise you with policyholders?",
         "<p>It would if the analysis changed with the client. It does not, and that is "
         "verifiable rather than a promise &mdash; ask to see work produced for the other side. "
         "What working both sides actually buys a policyholder is a consultant who knows exactly "
         "how a carrier&rsquo;s file is built, which arguments its reviewers take seriously, and "
         "which ones get a claim quietly deprioritized.</p>"),
        ("And doesn&rsquo;t working for policyholders compromise you with carriers?",
         "<p>Same answer in reverse. A carrier retaining us is getting an assessment that will "
         "not fall apart when policyholder counsel reads it, precisely because it was written to "
         "the standard we would apply if we were on the other side. Work that only survives "
         "friendly scrutiny is a liability on a large file.</p>"),
        ("Will you take a matter against a party you have worked for before?",
         "<p>Potentially, once the earlier engagement is concluded and subject to confidentiality "
         "obligations, and we will disclose the prior relationship to both parties before "
         "accepting. We do not take a matter adverse to a client we are currently engaged by. If "
         "either party is uncomfortable, they should say so and we will decline &mdash; that is "
         "cheaper for everyone than an argument about it later.</p>"),
        ("Can counsel retain you rather than the party?",
         "<p>Yes, and on matters heading toward litigation that is frequently the sensible "
         "structure. Engagement through counsel is common for expert work; how it affects "
         "privilege and discoverability is a question for the attorney, not for us.</p>"),
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
        "description": ("Professional disclaimer: licensing, capacity, independence, and the "
                        "limits of the information published on this site."),
        "eyebrow": "Legal",
        "h1": "Disclaimer",
        "h1_plain": "Disclaimer",
        "lede": "What we are, what we are not, and what this site is for.",
        "trail": [("Home", "/"), ("Disclaimer", None)],
        "sections": [{"wrap": "narrow", "blocks": [
            ("h2", "What we do"),
            ("p", "%s is an independent claims consulting firm. Our work is damage assessment, "
                  "scope and construction cost analysis, time-element quantification, coverage-"
                  "adjacent technical analysis, appraisal and umpire service, and expert support "
                  "to counsel. We are retained by policyholders, insurers, third-party "
                  "administrators, risk pools, brokers and attorneys." % BIZ["name"]),
            ("h2", "Licensing and capacity"),
            ("p", "We hold Texas adjuster and public insurance adjuster licences, issued and "
                  "regulated by the Texas Department of Insurance. Licence numbers appear in the "
                  "footer of this site and can be verified directly with the department."),
            ("p", "Holding licences on both sides is what allows either party to retain this "
                  "firm. It does not mean we occupy both roles at once. On any individual matter "
                  "we act in a single, stated capacity &mdash; as consultant, as a "
                  "party-appointed appraiser, as umpire, or as an adjuster &mdash; identified in "
                  "the engagement letter before work begins. We do not act for both parties to "
                  "the same loss, and a conflict check is run before any matter is discussed in "
                  "detail."),
            ("h2", "Independence and compensation"),
            ("p", "We are paid for time and deliverables, on an hourly or fixed-fee basis. We do "
                  "not take a percentage of any settlement, award or recovery on those "
                  "engagements. Public adjusting, where we act as the policyholder&rsquo;s "
                  "representative, is on a contingent fee capped by statute. We accept no "
                  "referral fees, commissions or other consideration from contractors, "
                  "restoration companies, engineers, vendors or attorneys, in either direction."),
            ("h2", "We are not a law firm"),
            ("p", "Nothing on this site is legal advice, and we do not provide it. Several topics "
                  "discussed here &mdash; limitation periods, statutory remedies, pre-suit notice "
                  "the effect of releases, coverage interpretation and statutory remedies &mdash; "
                  "are legal questions on which you should consult a licensed Texas attorney. "
                  "Where we think a matter needs counsel, we say so."),
            ("h2", "We are not contractors"),
            ("p", "We do not repair, restore or reconstruct property, and we do not participate "
                  "directly or indirectly in the repair of property we have assessed. The "
                  "selection of contractors is the client&rsquo;s alone."),
            ("h2", "No guarantee of outcome"),
            ("p", "No firm can guarantee the result of a claim, an appraisal or a proceeding. "
                  "Every matter turns on its own policy wording, facts and evidence. Descriptions "
                  "of our approach on this site describe method, not promised outcomes, and "
                  "nothing here should be read as a prediction about any particular file."),
            ("h2", "Calculators and reference material"),
            ("p", "The calculators, timelines, unit costs and statutory summaries published here "
                  "are planning aids assembled from published sources and ordinary industry "
                  "convention. They are not appraisals, not coverage opinions, not expert "
                  "reports and not legal deadlines. Verify anything with a deadline attached "
                  "against the governing document and with counsel."),
            ("h2", "No relationship formed here"),
            ("p", "Using this site, running a calculator or sending an enquiry does not create a "
                  "professional relationship and does not put us under any duty to you. That "
                  "relationship begins only when a written engagement agreement is signed by "
                  "both parties. Do not send confidential or privileged material before then."),
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
