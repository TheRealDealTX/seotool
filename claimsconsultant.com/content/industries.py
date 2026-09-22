"""The nine property types we take claims for.

Each page argues from the wording and the politics peculiar to that kind of
owner: a school district answers to a board and a bond schedule, a city has a
FEMA obligation running alongside its insurance, a church usually finds out too
late that its steeple was scheduled at a number set in 2011.
"""

from siteconfig import BIZ, STANDARDS, FEES

P = BIZ["phone_display"]


def _path(slug):
    return "/who-we-serve/%s/" % slug


INDUSTRIES = [

    # ==================================================== churches ==========
    {
        "slug": "churches-and-religious-organizations",
        "nav_label": "Churches &amp; Faith Organizations",
        "card_title": "Churches &amp; faith organizations",
        "card_blurb": ("Sanctuaries, family life centers, schools and parsonages, usually "
                       "insured on values nobody has revisited in a decade."),
        "title": "Church Property Loss Consultants | Texas",
        "description": "Expert witness and damage consulting for Texas churches. Storm, hail, fire and water loss assessment on sanctuaries, family life centers and church schools.",
        "eyebrow": "Who we serve &middot; Faith organizations",
        "h1": "Church property losses,<br>measured <em>properly</em>",
        "h1_plain": "Church insurance claims in Texas",
        "lede": ("A church is the hardest building in town to value and the easiest one to "
                 "underpay. The sanctuary is irregular, the finishes are not in any estimating "
                 "database, the organ is a scheduled item nobody has looked at since 2011, and the "
                 "congregation needs the room back by Sunday. We handle the claim so the staff can "
                 "handle the church."),
        "head_aside": [
            ("ledger", "Where church claims go wrong", [
                ("Values last reviewed", "8&ndash;15 yrs"),
                ("Coinsurance clause present", "Usually"),
                ("Ordinance &amp; law limit", "Often 10%"),
                ("Stained glass scheduled", "Rarely"),
                ("Loss of tithes covered", "Depends"),
                ("Who reads the policy first", "Nobody"),
            ], "Six lines that decide most sanctuary claims, and the six that nobody checks "
               "until the roof is already open."),
        ],
        "sections": [
            {
                "eyebrow": "The valuation problem",
                "h2": "The building was never worth what the schedule says.",
                "blocks": [
                    ("p", "Most Texas churches are insured on a statement of values that was "
                          "assembled once, at the time of a refinance or a building campaign, and "
                          "then rolled forward with a small annual inflation factor. Meanwhile the "
                          "congregation added a family life center, enclosed a breezeway, bought "
                          "the building next door for the pre-school, and replaced the sound and "
                          "lighting package twice."),
                    ("p", "That gap does not matter at all until there is a loss. Then it matters "
                          "in two ways at once. It caps what the policy can pay, and &mdash; if the "
                          "form carries a coinsurance clause, which most church forms do. It "
                          "reduces the payment on every loss by the ratio of the limit carried to "
                          "the limit required. A partial roof claim on a badly scheduled sanctuary "
                          "gets cut by the same percentage as a total loss would."),
                    ("p", "The first thing we do on a church file is establish what the replacement "
                          "value actually is, on today's costs, for a building of that "
                          "construction. Sometimes that strengthens the claim. Sometimes it tells "
                          "the board something uncomfortable they needed to know two years ago. "
                          "Either way it is better established by us in week one than by the "
                          "carrier's consultant in month seven."),
                    ("html", '<a class="tlink" href="/tools/coinsurance-penalty-calculator/">'
                             'Test your own coinsurance exposure <span class="arw">&rarr;</span></a>'),
                ],
                "aside": [
                    ("callout", "Functional replacement cost", [
                        ("p", "Older sanctuaries are often written on a <strong>functional "
                              "replacement cost</strong> basis instead of true RCV. That wording "
                              "lets the carrier rebuild with modern equivalent materials instead of "
                              "matching plaster, millwork or leaded glass. It is not automatically "
                              "wrong, but it is a completely different number, and it should "
                              "be a decision the church made, not one it discovered."),
                    ]),
                    ("callout", "Denominational programs", [
                        ("p", "Churches insured through a denominational or church-specialty "
                              "program often have better wording than the open market, "
                              "agreed value, replacement cost on contents, generous debris removal"
                              ", and no one at the church has ever read it. The endorsement "
                              "list is where the money is."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Scope",
                "h2": "The line items carriers regularly leave off a sanctuary estimate.",
                "dek": "None of these are exotic. They are simply not in the standard template, so "
                       "they do not appear unless somebody puts them there.",
                "blocks": [
                    ("table", "Commonly omitted church scope", ["Item", "Why it gets missed", "What it is worth"], [
                        ["Steeple, spire and cupola access",
                         "Priced as roof work rather than as a separate structure needing rigging, a crane or a lift.",
                         "~Often five figures"],
                        ["Stained and leaded glass",
                         "Treated as window glass. Re-leading, protective glazing and artisan labor are different trades entirely.",
                         "~Per opening"],
                        ["Pipe organ and console",
                         "Water and dust intrusion damages an organ invisibly. Assessment requires a builder, not an adjuster.",
                         "~Specialist report"],
                        ["Acoustic and AVL systems",
                         "Sanctuary acoustics are engineered. Like-kind replacement of ceiling treatment is not optional trim.",
                         "~Design + install"],
                        ["Code upgrades on assembly occupancy",
                         "Sprinklers, egress and ADA trigger on substantial repair. Written off as betterment.",
                         "~Ord. &amp; law limit"],
                        ["Loss of tithes and offerings",
                         "Business income for a nonprofit. Recorded as giving, not revenue, so nobody claims it.",
                         "~Time element"],
                        ["Temporary worship space",
                         "Extra expense (tent, school gym, rented hall, sound hire) if the form allows it.",
                         "~Extra expense"],
                        ["Pre-school and day-care interruption",
                         "A separate revenue stream with its own licensing and staffing costs.",
                         "~Time element"],
                    ]),
                ],
            },
            {
                "eyebrow": "What we do",
                "h2": "From the first tarp to the last release.",
                "blocks": [
                    ("steps", [
                        ("Read the policy with the trustees",
                         "<p>Declarations, forms, endorsements and the statement of values, in one "
                         "sitting, with whoever on the board will have to answer for the decision. "
                         "Most churches have never had the policy explained to them by someone "
                         "without a commission on the renewal.</p>"),
                        ("Document before the volunteers clean",
                         "<p>Congregations are helpful, and that is the problem. Within seventy-two "
                         "hours of a loss the wet carpet is in a dumpster and the ceiling tiles are "
                         "gone. We photograph, measure and moisture-map first, then tell you what is "
                         "safe to move.</p>"),
                        ("Build a sanctuary-specific estimate",
                         "<p>Line-item, in the same platform the carrier uses, with specialist "
                         "trades quoted rather than guessed and code work carried as its own "
                         "schedule so it cannot be folded into the general allowance.</p>"),
                        ("Negotiate, and report to the board",
                         "<p>Every position in writing, every deadline cited, and a plain-English "
                         "summary the church can put in front of a business meeting without a "
                         "translator.</p>"),
                    ]),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "Also relevant",
                "h2": "Church schools, camps and parsonages sit on the same policy, and get forgotten.",
                "dek": "If the organization owns it, the claim should scope it. We regularly find "
                       "outbuildings, portable classrooms, playground structures, fellowship halls "
                       "and church-owned housing on the schedule that nobody inspected after the storm.",
                "blocks": [
                    ("checks", [
                        "Church-operated schools, pre-schools and mother&rsquo;s-day-out programs, including their revenue interruption.",
                        "Gymnasiums and family life centers, floors, backstops, HVAC and roof systems.",
                        "Parsonages and church-owned residential property, which may be scheduled under a different valuation basis.",
                        "Camps, retreat centers and cemetery structures, often in a different county from the main campus.",
                        "Detached storage, bus barns and maintenance buildings where hail damage shows earliest.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Can a church engage a claims consultant, and who has to approve it?",
             "<p>A church engages a consultant the same way it engages an architect or an attorney: "
             "through whatever its bylaws require for a contract of that size, usually trustee or "
             "board approval. Denominational insurance programs do not prohibit it. What they often "
             "do is offer their own claims assistance, which is useful and still paid for "
             "by the same organization that will pay the claim. Those two things can coexist. An "
             "independent measurement of the loss is useful to the church and, frankly, useful "
             "to a well-run program too &mdash; it is easier to pay a documented number than an "
             "asserted one.</p>"),
            ("Our insurance is through a church-specific carrier. Are those claims different?",
             "<p>In the wording, yes, usually for the better. Church programs commonly carry agreed "
             "value in place of coinsurance, replacement cost on contents, broader debris removal, "
             "and extensions for things the standard commercial form ignores, counselling "
             "expense, loss of tithes, temporary worship facilities. The difficulty is that almost "
             "nobody at the church knows those extensions exist, so they are never claimed. Reading "
             "the endorsement schedule is often the single highest-value hour of a church file.</p>"),
            ("The roof looks fine from the ground. Should we still have it looked at after a hail storm?",
             "<p>Yes, and preferably before the policy&rsquo;s claim-reporting window and the "
             "two-year suit limitation start to bite. Hail bruising on a modified bitumen or "
             "single-ply commercial roof is usually invisible from grade and sometimes invisible "
             "from the roof surface without a test cut. The damage that matters is to the membrane "
             "and the insulation beneath it, and it expresses itself as leaks eighteen months later"
             ", by which point the carrier will argue the cause was wear, not the storm.</p>"),
            ("Will filing a claim raise our premium or get us non-renewed?",
             "<p>It is a fair worry and we will not pretend otherwise: in a hard property market, "
             "loss history affects both. What we would say is that the calculation should be made "
             "with a real number in hand instead of a guess. A church that quietly absorbs a "
             "$400,000 roof loss to protect a $9,000 premium has made a bad trade. One that files a "
             "marginal $22,000 claim in a year when it is already on notice may have made a worse "
             "one. We will tell you which situation you are in before you give notice.</p>"),
        ],
    },

    # ============================================== school districts ========
    {
        "slug": "school-districts",
        "nav_label": "School Districts &amp; ISDs",
        "card_title": "School districts &amp; ISDs",
        "card_blurb": ("Multi-campus property programs, risk-pool coverage, bond-funded buildings "
                       "and a repair window that closes in August."),
        "title": "School District Property Losses | Texas Consultants",
        "description": "Expert witness and damage consulting for Texas school districts. Hail, wind, fire and water losses across multi-campus programs and risk pools.",
        "eyebrow": "Who we serve &middot; Public education",
        "h1": "School district claims,<br>settled before <em>August</em>",
        "h1_plain": "School district property insurance claims",
        "lede": ("A district property loss is really three problems stacked on each other: the "
                 "damage, the calendar, and the board meeting. Campuses have to be occupiable when "
                 "the buses run, the money has to reconcile against a bond schedule, and every "
                 "decision is made in public. We work district files with all three in view."),
        "head_aside": [
            ("ledger", "District file, typical shape", [
                ("Campuses on one schedule", "4&ndash;40+"),
                ("Deductible basis", "Per occurrence"),
                ("Coverage vehicle", "Pool or carrier"),
                ("Repair window", "Jun&ndash;Aug"),
                ("Board approval needed", "Yes"),
                ("FEMA in play", "If declared"),
            ], "The scheduling constraint is the leverage. A carrier that knows you must be open in "
               "August negotiates differently than one that does not."),
        ],
        "sections": [
            {
                "eyebrow": "The pool question",
                "h2": "First establish whether you are insured.",
                "blocks": [
                    ("p", "A large share of Texas districts cover property through an interlocal "
                          "risk pool rather than a traditional insurance policy. That distinction "
                          "is not academic. A pool operates under an interlocal participation "
                          "agreement, and the statutory machinery that governs insurers, the "
                          "statutory machinery aimed at insurers may not apply to it in the same way."),
                    ("p", "What that changes is procedure, not the technical work. A pool coverage "
                          "document has its own appeal process, its own valuation provisions and "
                          "its own definitions, and it is answerable to a board of trustees whose "
                          "members are also the pool&rsquo;s owners. An insurance policy answers "
                          "to a different set of rules. Which one applies is worth establishing "
                          "in week one, because the documentation that persuades each is "
                          "assembled differently."),
                    ("p", "We work out which one you have on day one, from the coverage document "
                          "itself rather than from what the broker calls it."),
                    ("html", '<a class="tlink" href="/services/causation-determinations/">'
                             'How causation gets established <span class="arw">&rarr;</span></a>'),
                ],
                "aside": [
                    ("callout", "Ask your broker for three things", [
                        ("p", "The full coverage document including all endorsements or "
                              "amendments; the current statement of values by campus; and the "
                              "deductible provision in full, including any per-building, "
                              "named-storm or percentage wording. Those three documents answer most "
                              "of what a board will ask in the first meeting after a loss."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Deductibles",
                "h2": "How the deductible is written decides how much of a district-wide hail event you recover.",
                "dek": "One storm crossing nineteen campuses can be one occurrence or nineteen. "
                       "Both readings appear in Texas school property programs, and the difference "
                       "on a mid-sized district runs into seven figures.",
                "blocks": [
                    ("table", "Deductible structures seen on Texas district programs",
                     ["Structure", "How it applies", "Effect on a multi-campus hail event"], [
                        ["Flat per occurrence",
                         "One retention for the whole event, regardless of how many buildings are damaged.",
                         "Best case. One deductible against the entire loss."],
                        ["Per building, per occurrence",
                         "The retention applies separately at each damaged structure.",
                         "Nineteen campuses can mean nineteen retentions. Often fatal to small-per-campus losses."],
                        ["Percentage of values, per building",
                         "A percentage, commonly 1% to 5%, of the insured value of each affected building.",
                         "Scales with the schedule. A high-value high school can absorb its own claim entirely."],
                        ["Named storm / wind-hail separate",
                         "A different, usually larger, retention for named storms or for all wind and hail.",
                         "Determines whether a hail claim is worth filing at all. Check the trigger wording."],
                        ["Annual aggregate",
                         "Retentions accumulate toward a stop; losses after that point are covered in full.",
                         "The reason to file small campus losses properly. They erode the aggregate."],
                     ]),
                    ("callout", "The occurrence definition is where this is decided", [
                        ("p", "Look for the phrase defining occurrence in terms of a continuous "
                              "period of hours &mdash; 72 hours is common for wind and hail. "
                              "Damage at every campus within that window is usually one occurrence. "
                              "That single sentence is worth reading before you agree to how the "
                              "carrier has structured the claim file."),
                    ]),
                ],
            },
            {
                "eyebrow": "Scope",
                "h2": "What gets under-scoped on a school campus.",
                "blocks": [
                    ("checks", [
                        "<strong>Roof systems by section.</strong> Campuses are rarely one roof. A 1978 built-up section, a 2004 modified bitumen addition and a 2019 TPO wing have three different ages, three different repairability arguments and three different unit costs.",
                        "<strong>Gym floors.</strong> Maple sports floors cup and crown from humidity alone. Sanding is not always the remedy and moisture testing under the vapor barrier is not optional.",
                        "<strong>Portable and modular classrooms.</strong> Usually missing from the statement of values altogether, and the first structures to sustain wind damage.",
                        "<strong>Athletic facilities.</strong> Press boxes, field houses, bleachers, netting, scoreboards, track surfaces and turf infill &mdash; all separately damageable, all rarely inspected by the carrier&rsquo;s adjuster.",
                        "<strong>Kitchen equipment and food stock.</strong> A refrigeration outage during a wind event is a spoilage claim and a health-department event at the same time.",
                        "<strong>Technology and instructional equipment.</strong> Interactive panels, lab equipment, one-to-one device inventories and network hardware in ceiling spaces that took water.",
                        "<strong>Code upgrades on renovation.</strong> Substantial repair to an older campus triggers current accessibility, egress and fire-suppression requirements. That is ordinance and law coverage, not betterment.",
                        "<strong>Extra expense to open on time.</strong> Portable leasing, bussing to an alternate campus, overtime and accelerated construction premiums, where the coverage document allows them.",
                    ]),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "After a declared disaster",
                "h2": "Insurance and FEMA have to be sequenced, not run in parallel.",
                "dek": "Public assistance is a payer of last resort. Federal law prohibits "
                       "duplication of benefits, so what your insurance ought to have paid is "
                       "deducted from federal assistance whether or not you pursued it.",
                "blocks": [
                    ("p", "The practical consequence for a district is uncomfortable: under-settling "
                          "the insurance claim does not shift the shortfall onto FEMA. The federal "
                          "share is generally reduced by the insurance proceeds that were available, "
                          "actual or anticipated, and applicants are separately required to obtain "
                          "and maintain insurance as a condition of assistance on the same facility "
                          "in future. Districts that take the carrier&rsquo;s first number to get "
                          "the campus open often discover the cost of that decision in the "
                          "obligation phase, months later."),
                    ("p", "We document the insurance claim to a standard the public assistance file "
                          "can be built on: same measurements, same scope, same photographs, same "
                          "dates. It is more work at the start and materially less argument at the "
                          "end."),
                ],
            },
        ],
        "faqs": [
            ("Does a school district need to competitively bid a claims consultant?",
             "<p>Professional services procurement varies by district policy and by the value of the "
             "engagement, and your purchasing officer and counsel are the right people to answer it "
             "for your board, not us. What we can tell you is that ours is an ordinary "
             "hourly professional-services engagement with a written estimate and a "
             "not-to-exceed figure, which is a familiar shape to a purchasing process. We are "
             "used to producing the documentation a board packet requires.</p>"),
            ("Our district is in a risk pool. Is there anything for a consultant to do?",
             "<p>Often more, not less. Pool coverage documents are not standard-form insurance "
             "policies, so the exclusions, the valuation basis and the appeal process all have to "
             "be read rather than assumed. The adjusting is commonly done by the same third-party "
             "administrators the insurance industry uses, and the scope disputes are identical: "
             "roof age, repairability, matching, code upgrade, overhead and profit. What changes is "
             "that there is no statutory pressure to fall back on, so everything rests on "
             "documentation and on the pool&rsquo;s own process.</p>"),
            ("Can you work around the school calendar?",
             "<p>It is the central planning constraint on every district file we take. Inspections "
             "get scheduled around instruction, invasive testing goes in breaks, and the negotiation "
             "sequence is built backwards from the date the campus must be occupiable. Where the "
             "deadline is genuinely immovable, we would rather document heavily, get an advance "
             "payment released to start work, and keep the scope disputes live, than let the "
             "calendar force the district into accepting a number as final.</p>"),
            ("What if repairs have already been done?",
             "<p>Then the claim gets built from what survives: invoices, contractor photographs, "
             "change orders, board minutes, maintenance work orders, pre-loss drone or roof-survey "
             "imagery, and the district&rsquo;s own facilities records. It is harder and it is "
             "regularly still worth doing, particularly on supplemental claims where costs came in "
             "above the carrier&rsquo;s estimate. What we cannot do is recreate evidence, which is "
             "why the call is better made early.</p>"),
        ],
    },

    # =========================================== cities / municipalities ====
    {
        "slug": "cities-and-municipalities",
        "nav_label": "Cities &amp; Municipalities",
        "card_title": "Cities &amp; municipalities",
        "card_blurb": ("City halls, public safety, utilities and public works, with FEMA, a "
                       "council and the open-records file all watching."),
        "title": "Municipal Property Losses | Texas Claims Consultants",
        "description": "Expert witness and damage consulting for Texas cities and municipal entities. City hall, public safety, utilities and public works claims, including FEMA coordination.",
        "eyebrow": "Who we serve &middot; Local government",
        "h1": "Municipal claims, built<br>for the <em>public record</em>",
        "h1_plain": "Municipal and city property insurance claims",
        "lede": ("A city cannot settle a property claim quietly. The number ends up in a council "
                 "packet, in the audit, sometimes in the newspaper, and often in a federal "
                 "obligation file three years later. That is a good reason to get it right the "
                 "first time and to be able to show your working."),
        "head_aside": [
            ("ledger", "What a municipal file has to satisfy", [
                ("Council / commission", "Public vote"),
                ("Annual audit", "Documented"),
                ("Open records", "Disclosable"),
                ("FEMA PA", "If declared"),
                ("Insurance obtain &amp; maintain", "Required"),
                ("Continuity of services", "Non-negotiable"),
            ], "Six audiences for one number. We build the file so it holds up in front of all of "
               "them, not just the carrier."),
        ],
        "sections": [
            {
                "eyebrow": "Continuity first",
                "h2": "Public safety does not get to wait for the adjuster.",
                "blocks": [
                    ("p", "When a fire station takes a roof off, the trucks still roll. When a "
                          "water treatment facility floods, the city still has to produce water. "
                          "Municipal property losses are almost always emergencies of operation "
                          "before they are questions of coverage, and the decisions made in those "
                          "first days, where to relocate, what to demolish, which contractor "
                          "to bring in under an emergency purchase &mdash; are the decisions the "
                          "carrier will scrutinize hardest afterwards."),
                    ("p", "The way through is not to slow the city down. It is to document at the "
                          "speed the city is moving. We put a scope and a photographic record "
                          "around emergency work while it happens, capture the pre-mitigation "
                          "condition, and keep the emergency spend in a separate, defensible "
                          "ledger so it can be presented as reasonable mitigation expense rather "
                          "than argued about as uncontrolled cost."),
                    ("html", '<a class="tlink" href="/loss-types/business-interruption-claims/">'
                             'Extra expense and continuity losses <span class="arw">&rarr;</span></a>'),
                ],
                "aside": [
                    ("callout", "Emergency spend, defensibly", [
                        ("p", "Timestamped photographs before work starts. A written scope, even a "
                              "rough one, before the crew arrives. Daily logs. Invoices separated "
                              "by facility and by task rather than lumped. Those four habits turn "
                              "an argument into a schedule."),
                    ]),
                    ("callout", "Risk pools and self-insurance", [
                        ("p", "Many Texas cities cover property through an intergovernmental risk "
                              "pool operating under an interlocal agreement, sometimes with a "
                              "substantial self-insured retention beneath it. The coverage document"
                              ", not the insurance code, is the primary rulebook, and "
                              "it needs to be read before positions are taken."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "FEMA",
                "h2": "The duplication-of-benefits rule shapes the whole insurance strategy.",
                "dek": "Federal disaster assistance is a payer of last resort. Under the Stafford "
                       "Act, assistance is reduced by insurance proceeds that are actually or "
                       "reasonably anticipated to be available for the same work.",
                "blocks": [
                    ("p", "Read plainly, that means a city cannot improve its position by settling "
                          "the insurance claim cheaply and asking the federal government to cover "
                          "the difference. The anticipated insurance recovery is deducted whether "
                          "or not it was pursued with any vigor. A weak insurance "
                          "settlement therefore lands on the city&rsquo;s own general "
                          "fund, twice over."),
                    ("p", "There is a second obligation that outlives the disaster. Applicants "
                          "receiving public assistance for an insurable facility are generally "
                          "required to obtain and maintain insurance on that facility going "
                          "forward, in an amount at least equal to the eligible damage, and "
                          "failing to do so can jeopardise assistance after the next event. The "
                          "insurance decision made this year constrains the next declaration."),
                    ("table", "Sequencing the two files", ["Stage", "Insurance", "Public assistance"], [
                        ["Days 0&ndash;7", "Notice given, emergency mitigation documented, scope photographed.",
                         "Damage inventory started, categories identified, emergency work logged."],
                        ["Weeks 2&ndash;8", "Line-item estimate built, specialists engaged, proof of loss prepared.",
                         "Project worksheets developed from the same measurements and photographs."],
                        ["Months 2&ndash;9", "Negotiation, supplements, appraisal if the gap will not close.",
                         "Obligation, with insurance proceeds and anticipated recovery disclosed."],
                        ["Closeout", "Recoverable depreciation released on completed work.",
                         "Final reconciliation; under-recovery here is not backfilled."],
                    ]),
                    ("callout", "One set of measurements", [
                        ("p", "The most common self-inflicted wound in municipal recovery is two "
                              "inconsistent damage descriptions, one written for the carrier "
                              "and one written for the federal file. They will eventually be read "
                              "side by side. Build them from the same survey."),
                    ]),
                ],
            },
            {
                "eyebrow": "Facilities",
                "h2": "What a city owns, and how each part fails.",
                "blocks": [
                    ("cards", [
                        ("City hall &amp; civic buildings",
                         "Often the oldest structure on the schedule, often historic, almost "
                         "always the one where ordinance and law coverage decides the outcome. "
                         "Records rooms and server rooms are the hidden exposure.",
                         "/loss-types/commercial-property-damage-claims/"),
                        ("Police, fire &amp; EMS",
                         "Apparatus bays, dispatch and communications, backup power, and a "
                         "continuity requirement that forbids waiting. Extra expense is usually the "
                         "larger half of the claim.",
                         "/loss-types/business-interruption-claims/"),
                        ("Water, wastewater &amp; utilities",
                         "Control buildings, SCADA, pump and lift stations, chemical storage. "
                         "Equipment breakdown and property coverage overlap here and carriers "
                         "exploit the seam.",
                         "/loss-types/water-damage-and-freeze-claims/"),
                        ("Public works &amp; fleet",
                         "Barns, shops, salt and material storage, fuel islands and vehicle "
                         "inventory. The buildings are cheap and the contents are not.",
                         "/loss-types/hail-damage-claims/"),
                        ("Libraries, museums &amp; community centers",
                         "Collections, archives and special contents with valuation problems of "
                         "their own, plus smoke and water exposure far beyond the burn area.",
                         "/loss-types/commercial-fire-claims/"),
                        ("Parks, pools &amp; athletic facilities",
                         "Pavilions, press boxes, lighting, netting, shade structures and pool "
                         "mechanical, often omitted from the carrier&rsquo;s inspection "
                         "list entirely.",
                         "/loss-types/hurricane-and-windstorm-claims/"),
                    ]),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "Reporting",
                "h2": "Everything we produce is written to be read in public.",
                "dek": "Council packets, audit files and open-records requests are not an "
                       "afterthought on a municipal claim. They are the format.",
                "blocks": [
                    ("checks", [
                        "A plain-English status memo at every stage, suitable for a council packet without rewriting.",
                        "Scope and estimate delivered in a standard estimating format your finance department and any state or federal reviewer can follow.",
                        "Photographic record indexed by facility, date and location, with the raw files handed over at closeout.",
                        "A written record of every carrier position and every response, with dates, which is also the record that makes a statutory argument possible later.",
                        "Fee and engagement terms stated as a percentage of recovery, in writing, before any work begins.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Can a Texas city engage a claims consultant?",
             "<p>Cities engage professional services of this kind regularly, subject to their own "
             "charter, purchasing policy and council approval thresholds, which your city "
             "attorney and purchasing officer will apply, not us. Ours is an hourly "
             "professional-services engagement with a written estimate and a not-to-exceed "
             "figure, which most purchasing policies already have a route for. We will supply "
             "whatever documentation the agenda item requires.</p>"),
            ("Will using a consultant interfere with our FEMA public assistance?",
             "<p>It should strengthen it. The federal file needs a defensible damage description, "
             "consistent measurements and a documented insurance recovery. Those are the same "
             "deliverables as the insurance claim. The risk to avoid is the opposite one: a thin "
             "insurance settlement does not increase federal assistance, because anticipated "
             "insurance proceeds are deducted regardless. Note that claims consulting fees are "
             "generally not an eligible public assistance cost, so the engagement should be "
             "structured with that in mind from the start.</p>"),
            ("Our coverage is through a risk pool, not an insurance company. Does that change things?",
             "<p>It changes the rulebook. A pool operates under an interlocal participation "
             "agreement instead of an insurance policy, so the remedies that apply to an "
             "insurer may not reach it. The technical questions, though, are identical, roof age, "
             "repairability, matching, code upgrade, depreciation, overhead and profit &mdash; and "
             "those are won with documentation and with the pool&rsquo;s own appeal mechanism.</p>"),
            ("How quickly can you mobilise after a declared event?",
             "<p>Fast, and that matters more for a city than for almost any other client, because "
             "emergency work begins immediately and the pre-mitigation condition disappears with "
             "it. Call the moment the situation is stable enough to have the conversation. If we "
             "cannot get a person on site within the window that matters, we will say so rather "
             "than hold the engagement.</p>"),
        ],
    },

    # ================================================= higher education =====
    {
        "slug": "universities-and-colleges",
        "nav_label": "Universities &amp; Colleges",
        "card_title": "Universities &amp; colleges",
        "card_blurb": ("Campus-wide schedules, research exposure, auxiliary revenue and blanket "
                       "limits nobody has stress-tested."),
        "title": "University &amp; College Property | Texas Consultants",
        "description": "Expert witness and damage consulting for Texas universities and colleges. Residence halls, research facilities, athletics and auxiliary revenue interruption claims.",
        "eyebrow": "Who we serve &middot; Higher education",
        "h1": "Campus losses are<br><em>portfolio</em> losses",
        "h1_plain": "University and college property insurance claims",
        "lede": ("A campus is a city that happens to share one insurance schedule. A single "
                 "hailstorm can touch forty roofs, three research buildings, a residence hall "
                 "system with contractual obligations to students, and an athletics program with "
                 "a broadcast contract. The claim has to be run like the portfolio it is."),
        "head_aside": [
            ("ledger", "Campus claim anatomy", [
                ("Structures affected", "10&ndash;60+"),
                ("Limit basis", "Usually blanket"),
                ("Auxiliary revenue", "Time element"),
                ("Research exposure", "Specialist"),
                ("Occupancy deadline", "Semester"),
                ("Deductible test", "Occurrence wording"),
            ], "Blanket limits feel like safety until a single event tests them across the whole "
               "campus at once."),
        ],
        "sections": [
            {
                "eyebrow": "Blanket limits",
                "h2": "A blanket limit is only as good as the values behind it.",
                "blocks": [
                    ("p", "Campus programs are normally written blanket, which lets the full "
                          "limit respond anywhere on the schedule instead of trapping recovery at "
                          "a single building value. It is the right structure. It also creates a "
                          "quiet dependency: blanket coverage is usually conditioned on the "
                          "accuracy of the reported statement of values, and the margin clause or "
                          "occurrence limit of liability endorsement can cap recovery at a fixed "
                          "percentage of the value reported for the affected location."),
                    ("p", "So a building reported at $14 million in a schedule assembled four years "
                          "ago, with a 110% margin clause, is functionally insured for $15.4 "
                          "million today no matter how large the blanket limit above it is. On a "
                          "science building with modern mechanical systems, that gap is real money."),
                    ("p", "Establishing current replacement cost for the affected structures is "
                          "therefore not a formality on a campus file. It is the first substantive "
                          "argument, and it is much easier to make before the carrier&rsquo;s "
                          "consultant has anchored a number."),
                ],
                "aside": [
                    ("callout", "Three endorsements to find", [
                        ("p", "<strong>Margin clause</strong> or occurrence limit of liability"
                              ", caps recovery to a percentage of reported values. "
                              "<strong>Errors and omissions</strong>, protects unreported "
                              "or misreported locations, within limits. <strong>Newly acquired "
                              "property</strong>, and how many days you had to report it. "
                              "Together they decide whether a blanket limit behaves the way "
                              "everyone assumes."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Time element",
                "h2": "Auxiliary revenue is where the second half of a campus claim lives.",
                "dek": "Tuition may be insulated. Housing, dining, parking, athletics, conferences "
                       "and the bookstore are not.",
                "blocks": [
                    ("table", "Campus revenue streams that interrupt", ["Stream", "How the loss shows up", "Documentation needed"], [
                        ["Residence halls", "Displaced students rehoused off campus, refunds or credits issued, beds out of inventory for a term.", "Occupancy contracts, refund ledger, historical fill rates"],
                        ["Dining &amp; retail", "Closed venues, contract caterer minimums, spoiled stock, relocated service at higher cost.", "POS history, contract terms, spoilage inventory"],
                        ["Athletics", "Relocated or canceled events, lost gate and concessions, broadcast and guarantee obligations.", "Event schedule, prior-year gate, contracts"],
                        ["Conferences &amp; summer camps", "Canceled bookings in the months the calendar depends on.", "Booking pipeline, deposits, cancellation correspondence"],
                        ["Parking &amp; facilities rental", "Garages and lots out of service, external rentals suspended.", "Permit and rental revenue history"],
                        ["Research", "Interrupted studies, lost specimens, equipment recalibration, grant timeline exposure.", "Protocol records, equipment logs, grant terms"],
                    ]),
                    ("callout", "Extra expense usually outruns business income", [
                        ("p", "On a campus, the instinct is to keep operating at any cost, "
                              "hotels for students, chartered buses, rented modular labs, "
                              "accelerated construction. That spend is usually recoverable as "
                              "extra expense, and it is often unrecorded because it is "
                              "scattered across twelve departmental budgets. Centralise the capture "
                              "on day one."),
                    ]),
                ],
            },
            {
                "eyebrow": "Research",
                "h2": "Laboratory losses are not repaired, they are re-validated.",
                "blocks": [
                    ("p", "A water event in a research building produces two claims. The first is "
                          "the building: drywall, ceilings, flooring, mechanical. The second is "
                          "everything the building was holding &mdash; instruments that need "
                          "recalibration and requalification, controlled environments that must be "
                          "recertified, cold storage whose contents may be irreplaceable, and "
                          "protocols that cannot resume."),
                    ("p", "Carriers scope the first competently and the second almost never, "
                          "because it requires manufacturer engagement and documentation from "
                          "principal investigators who are, understandably, thinking about their "
                          "work rather than an insurance file. We put that capture process in "
                          "place early, in a format the carrier&rsquo;s consultant cannot wave "
                          "away."),
                    ("checks", [
                        "Instrument-by-instrument condition assessment with manufacturer service reports instead of adjuster opinion.",
                        "Cleanroom, vivarium and controlled-environment recertification treated as part of repair, not as an upgrade.",
                        "Cold-storage contents inventoried and valued before anything is discarded, with chain-of-custody documentation.",
                        "Code and safety upgrades triggered by laboratory renovation carried under ordinance and law, separately scheduled.",
                        "Grant and sponsored-program consequences documented contemporaneously, whether or not they are ultimately covered.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("We have a risk management office and a broker. What does a consultant add?",
             "<p>Capacity and independence, mostly. A campus risk office is typically two to five "
             "people who also run the whole insurance program, and a large loss is a full-time "
             "job for months. Your broker is useful and is also structurally conflicted: "
             "their relationship with the market is a long one and yours with this claim is short. "
             "We add estimating capability, specialist engagement and the capacity to work a file "
             "full-time for months, at an hourly rate against a written estimate.</p>"),
            ("Can you work on part of a claim instead of the whole thing?",
             "<p>Yes, and on campus files that is often the sensible structure. A common engagement "
             "is on the disputed portion only: the roofs the carrier says are repairable, "
             "the time-element loss nobody has quantified, the research contents, while the "
             "risk office keeps the undisputed portion moving. The engagement letter defines the "
             "scope and the fee applies to that scope.</p>"),
            ("How is the fee handled on an institutional engagement?",
             "<p>Hourly, or fixed fee where the deliverable is well defined, with a written estimate "
             "of hours and a not-to-exceed figure. "
             "Institutions almost always want that structure documented before procurement "
             "review, and we would rather produce it at the start than negotiate it later.</p>"),
        ],
    },

    # ======================================================= healthcare =====
    {
        "slug": "hospitals-and-healthcare",
        "nav_label": "Hospitals &amp; Healthcare",
        "card_title": "Hospitals &amp; healthcare",
        "card_blurb": ("Where remediation standards, licensure and patient volume all constrain "
                       "what a repair is allowed to be."),
        "title": "Hospital &amp; Healthcare Property | Texas Consultants",
        "description": "Expert witness and damage consulting for Texas hospitals and surgery centers. Water, fire and storm losses with infection control, licensure and patient-volume exposure.",
        "eyebrow": "Who we serve &middot; Healthcare",
        "h1": "In healthcare, the<br>repair standard <em>is</em> the claim",
        "h1_plain": "Hospital and healthcare property insurance claims",
        "lede": ("A ceiling leak in an office building is a ceiling leak. The same leak over a "
                 "sterile corridor is an infection-control event, a licensure question, a "
                 "canceled surgical schedule and a remediation project governed by standards that "
                 "have nothing to do with the estimating software."),
        "head_aside": [
            ("ledger", "What raises a healthcare scope", [
                ("Infection control", "ICRA required"),
                ("Containment", "Negative pressure"),
                ("Clearance", "Third-party"),
                ("Equipment", "Recalibration"),
                ("Licensure", "State survey"),
                ("Revenue", "Per-case"),
            ], "Every line here is cost the carrier&rsquo;s standard template does not contain."),
        ],
        "sections": [
            {
                "eyebrow": "Remediation",
                "h2": "You cannot dry a hospital the way you dry a warehouse.",
                "blocks": [
                    ("p", "Water intrusion in a clinical environment triggers an infection control "
                          "risk assessment, containment and negative-pressure isolation of the work "
                          "area, HEPA filtration, controlled access, and independent post-"
                          "remediation verification before the space can be returned to patient "
                          "use. Work is commonly restricted to hours when adjacent departments "
                          "are not operating, which doubles labor cost by itself."),
                    ("p", "All of that is ordinary practice in healthcare construction and "
                          "absent from a standard water-mitigation estimate. The gap between the "
                          "two is not an upgrade the facility is choosing. It is the only lawful "
                          "way to do the repair, and it belongs in the claim as such, with "
                          "the protocol, the contractor&rsquo;s ICRA documentation and the "
                          "clearance testing attached as proof."),
                    ("html", '<a class="tlink" href="/loss-types/water-damage-and-freeze-claims/">'
                             'Water and freeze claims <span class="arw">&rarr;</span></a>'),
                ],
                "aside": [
                    ("callout", "Get clearance in writing", [
                        ("p", "Third-party post-remediation verification is both a patient-safety "
                              "requirement and the single most useful document in the eventual "
                              "negotiation. It converts a dispute about whether the scope was "
                              "excessive into a record of what was required before the space could "
                              "reopen."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Time element",
                "h2": "Lost patient volume is measurable. Prove it that way.",
                "blocks": [
                    ("p", "Healthcare business interruption is unusually provable, which is an "
                          "advantage worth using. Case volumes, payer mix, average reimbursement "
                          "per case and departmental contribution margin all exist in systems "
                          "already. A closed operating room has a defensible daily value. Diverted "
                          "emergency volume, canceled elective schedules, imaging downtime and "
                          "displaced clinic sessions each translate into a number that survives "
                          "scrutiny from a forensic accountant."),
                    ("p", "What defeats these claims is not weak data. It is data assembled nine "
                          "months later by a finance team reconstructing from memory. We engage a "
                          "forensic accountant early on losses of this size and set up the capture "
                          "while the disruption is still happening."),
                    ("table", "Building a healthcare time-element claim", ["Component", "Source", "Common carrier objection"], [
                        ["Lost case volume", "Scheduling and EHR records against prior-period baseline", "Volume would have been lost anyway"],
                        ["Contribution margin", "Departmental cost accounting, payer mix", "Gross revenue used instead of margin"],
                        ["Continuing expenses", "Payroll, leases, service contracts held during closure", "Should have been mitigated"],
                        ["Extra expense", "Temporary space, mobile units, transfer and diversion cost, overtime", "Not reasonable or necessary"],
                        ["Recovery period", "Ramp-back curve after reopening", "Period of restoration ended at reopening"],
                    ]),
                ],
            },
            {
                "eyebrow": "Equipment",
                "h2": "Medical equipment fails quietly and expensively.",
                "blocks": [
                    ("checks", [
                        "Imaging equipment exposed to water, dust or power events requires manufacturer inspection and recalibration, and sometimes will not be recertified at all, which converts a repair into a replacement.",
                        "Sterile processing equipment, autoclaves and scope reprocessors have validation requirements that survive any cosmetic repair.",
                        "Laboratory analyzers need requalification before results can be reported clinically.",
                        "Refrigerated pharmaceuticals, vaccines and specimens have temperature excursion rules that render stock unusable regardless of appearance.",
                        "Equipment breakdown coverage and property coverage overlap here; carriers periodically use the seam between two policies to delay both.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Is a consultant appropriate for a hospital with in-house risk management?",
             "<p>Often yes, for the same reason hospitals use outside counsel with a general "
             "counsel in place. The in-house team runs the program; a large loss needs dedicated "
             "estimating, specialist engagement and sustained negotiation for six to eighteen "
             "months. We work alongside risk management rather than replacing it, and the "
             "engagement can be limited to the disputed components.</p>"),
            ("Will the claim cover the cost of infection control requirements?",
             "<p>Where those requirements are what the work reasonably and necessarily involved, "
             "they belong in the repair cost, and they are supportable with the ICRA documentation, "
             "the contractor&rsquo;s containment plan and the clearance results. The objection you "
             "should expect is that the containment was excessive. The answer is documentation "
             "created at the time, which is why this needs to be set up at the start of the "
             "remediation rather than argued afterwards.</p>"),
            ("Our facility is part of a larger health system with a single property program. Can you still help?",
             "<p>Yes, and system programs have their own particular issues: per-occurrence "
             "deductibles applied across multiple affected facilities, blanket limits with margin "
             "clauses, and locations whose reported values have drifted. The engagement is usually "
             "scoped at system level with the affected facilities identified in the engagement "
             "letter.</p>"),
        ],
    },

    # ====================================================== multifamily =====
    {
        "slug": "multifamily-and-apartment-portfolios",
        "nav_label": "Multifamily &amp; Apartments",
        "card_title": "Multifamily &amp; apartment portfolios",
        "card_blurb": ("Per-building deductibles, loss of rents, and a unit-by-unit scope nobody "
                       "on the carrier&rsquo;s side wants to walk."),
        "title": "Apartment &amp; Multifamily Insurance Claims | Texas",
        "description": "Expert witness and damage consulting for Texas apartment communities, multifamily portfolios and condominium associations. Hail, wind, fire, freeze and loss-of-rents claims.",
        "eyebrow": "Who we serve &middot; Multifamily",
        "h1": "Two hundred units,<br>one <em>walked</em> building",
        "h1_plain": "Apartment and multifamily property claims",
        "lede": ("The carrier&rsquo;s adjuster inspects four units, extrapolates, and writes the "
                 "estimate. On a 288-unit community that method is not a shortcut, it is the "
                 "difference between a repair budget and a rebuild budget. Multifamily claims are "
                 "won by walking the whole thing."),
        "head_aside": [
            ("ledger", "Multifamily pressure points", [
                ("Deductible basis", "Often per building"),
                ("Loss of rents", "Actual loss sustained"),
                ("Unit interiors", "Inspected sample"),
                ("Matching", "Siding, roofing, brick"),
                ("Tenant displacement", "Extra expense"),
                ("Lender", "Loss payee consent"),
            ], "Per-building deductibles on a garden-style community can consume an entire hail "
               "claim. Read that clause before the storm, not after."),
        ],
        "sections": [
            {
                "eyebrow": "Scope method",
                "h2": "Sampling is an estimating convenience, not a finding of fact.",
                "blocks": [
                    ("p", "There is nothing improper about inspecting a representative sample of "
                          "units. The problem is what happens next. A sample taken from the four "
                          "units whose residents happened to be home on a Tuesday is not "
                          "representative of the top-floor units under the damaged roof section, "
                          "and the extrapolation carries that error across the whole community, "
                          "multiplied by a few hundred."),
                    ("p", "On a live claim we scope every affected building and, where interior "
                          "damage is in question, every unit in the affected stacks. It is slow. It "
                          "is also the only way to answer the question the carrier will eventually "
                          "ask, which is: prove it, unit by unit."),
                    ("p", "The same principle governs the exterior. Roof sections, elevations, "
                          "soft-metal test surfaces, windows, screens, siding, gutters, fencing, "
                          "carports, mailrooms, pool structures and amenity buildings each need to "
                          "appear on the estimate on their own line. Anything summarized is "
                          "anything that can be deleted."),
                ],
                "aside": [
                    ("callout", "Matching", [
                        ("p", "When a discontinued siding profile or a roof color can no longer be "
                              "sourced, the question of how far replacement must extend to achieve "
                              "reasonably uniform appearance is one of the most valuable arguments "
                              "on a multifamily file. It turns on the policy wording and on the "
                              "evidence you assemble about availability. Photograph elevations "
                              "whole, and keep the discontinued-product correspondence."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Loss of rents",
                "h2": "The rent roll is the claim document.",
                "blocks": [
                    ("p", "Loss of rental income is usually written on an actual-loss-sustained "
                          "basis, which means it must be proven rather than estimated. The proof is "
                          "the rent roll, the pre-loss occupancy trend, the concession history, the "
                          "down-unit log, and the record of what each displaced resident was "
                          "paying. A community running at 94% before a freeze event and "
                          "76% for five months afterwards has a quantifiable loss, but only if "
                          "somebody kept the records in a form an accountant can follow."),
                    ("checks", [
                        "Down-unit log maintained daily from the date of loss, by unit number, with the reason each unit is offline.",
                        "Pre-loss occupancy and effective rent trend for at least twelve months, so seasonality can be shown rather than argued.",
                        "Concessions, relocation costs and hotel expense captured as they are incurred, not reconstructed later.",
                        "Lease terminations and non-renewals attributable to the loss, with resident correspondence.",
                        "The ramp-back period after units return to service, occupancy does not recover the day the work finishes.",
                    ]),
                ],
            },
            {
                "eyebrow": "Condominiums",
                "h2": "Associations have a boundary problem before they have a claim.",
                "blocks": [
                    ("p", "On a condominium loss, the first fight is rarely with the carrier. It is "
                          "with the declaration. Where the association&rsquo;s responsibility ends "
                          "and the unit owner&rsquo;s begins &mdash; studs-out, bare walls, "
                          "original-specification finishes, betterments and improvements, is "
                          "set by the declaration and the governing statute, and it determines "
                          "which policy pays for what."),
                    ("p", "Get that boundary defined in writing early and the rest of the claim is "
                          "an ordinary property claim. Leave it ambiguous and the association "
                          "spends a year mediating between its own members while the master policy "
                          "carrier waits."),
                    ("callout", "Board duty", [
                        ("p", "Boards are often unpaid volunteers making a decision that "
                              "commits every owner in the community. Documentation is not "
                              "bureaucracy here; it is how a board demonstrates it acted "
                              "reasonably. We write to that standard."),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Our deductible is 2% per building. Is the claim even worth filing?",
             "<p>Sometimes not, and we will tell you that for free. Run the arithmetic before you "
             "give notice: 2% of each affected building&rsquo;s insured value, applied separately, "
             "against the per-building damage. On garden-style communities with many small "
             "structures the retention regularly exceeds the loss on most buildings while a handful "
             "of larger ones clear it comfortably. The answer is usually that part of the claim is "
             "worth pursuing properly and part is not worth reporting at all.</p>"),
            ("Can you handle a portfolio instead of a single property?",
             "<p>Yes. Portfolio events are actually where the method pays best, because the same "
             "storm produces a dozen files with the same carrier, the same deductible wording and "
             "the same arguments. Consistency across the files is leverage.</p>"),
            ("Will our lender need to be involved?",
             "<p>Almost certainly. Most multifamily mortgages name the lender as loss payee or "
             "mortgagee, and claim proceeds above a threshold are routed through the lender and "
             "disbursed against construction draws. Build that requirement into the repair schedule "
             "from the start, the disbursement process, not the settlement, is what delays "
             "most multifamily repairs.</p>"),
        ],
    },

    # ====================================================== hospitality =====
    {
        "slug": "hotels-and-hospitality",
        "nav_label": "Hotels &amp; Hospitality",
        "card_title": "Hotels &amp; hospitality",
        "card_blurb": ("Where the room-nights lost are worth more than the drywall, and the brand "
                       "standard dictates the scope."),
        "title": "Hotel Insurance Claims | Texas Hospitality Adjusters",
        "description": "Expert witness and damage consulting for Texas hotels and resorts. Storm, fire, water and business interruption claims measured in room nights, ADR and RevPAR.",
        "eyebrow": "Who we serve &middot; Hospitality",
        "h1": "Rooms out of<br>inventory are the <em>loss</em>",
        "h1_plain": "Hotel and hospitality insurance claims",
        "lede": ("A hotel measures damage in room nights. Fifty rooms down for ninety days at a "
                 "$182 average daily rate is a larger number than the repair that caused it, and "
                 "it is the number carriers scrutinize hardest and policyholders document worst."),
        "head_aside": [
            ("ledger", "Hospitality claim drivers", [
                ("Unit of loss", "Room night"),
                ("Rate basis", "ADR / RevPAR"),
                ("Seasonality", "Material"),
                ("Brand standard", "Scope driver"),
                ("PIP obligations", "Timing risk"),
                ("F&amp;B and events", "Separate stream"),
            ], "A time-element claim built from last year&rsquo;s STR data holds up. One built from "
               "an annual average does not."),
        ],
        "sections": [
            {
                "eyebrow": "Time element",
                "h2": "Build the revenue loss from the data the industry already produces.",
                "blocks": [
                    ("p", "Hospitality is one of the best-instrumented industries there is. "
                          "Occupancy, average daily rate and revenue per available room exist "
                          "nightly, by segment, with competitive-set benchmarking available from "
                          "third parties. That makes a hotel business-interruption claim unusually "
                          "provable, and it makes a badly built one unusually easy to attack."),
                    ("p", "The right construction projects what the property would have earned"
                          ", using its own historical performance adjusted by what the "
                          "competitive set did during the loss period, and "
                          "subtracts what it did earn. That method survives a forensic accountant. "
                          "An annual-average calculation applied to a property with a Formula 1 "
                          "weekend, a rodeo season or a spring-break peak does not."),
                    ("checks", [
                        "Nightly occupancy, ADR and RevPAR for at least twenty-four months before the loss, by segment.",
                        "Competitive-set performance during the loss period, to show the market instead of the property explains any shortfall.",
                        "Group and event bookings canceled, with contract value and attrition terms.",
                        "Food and beverage, banquet, spa, parking and resort-fee revenue as separate streams.",
                        "The ramp-back period &mdash; online reputation and channel ranking recover more slowly than the building does.",
                    ]),
                ],
                "aside": [
                    ("callout", "Saved expenses are real", [
                        ("p", "Expect the carrier to deduct expenses that did not continue during "
                              "the closure: housekeeping labor, laundry, commissions, some "
                              "utilities. Some of that is legitimate. Much of it is overstated, "
                              "particularly where staff were retained to protect the operation. "
                              "Track it rather than conceding it."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Brand standards",
                "h2": "Franchise requirements can make like-kind repair impossible.",
                "blocks": [
                    ("p", "A flagged hotel does not get to repair to the specification that was "
                          "there before. The franchise agreement sets current brand standards, and "
                          "a substantial renovation often triggers a property improvement plan"
                          ", a mandated upgrade program covering guest rooms, corridors, "
                          "lobby, fitness and technology, at the brand&rsquo;s current "
                          "specification instead of the property&rsquo;s previous one."),
                    ("p", "Carriers treat that delta as betterment, and the argument is not "
                          "frivolous: a standard property form pays to repair with like kind and "
                          "quality. Whether the PIP cost is recoverable depends on the wording, on "
                          "ordinance and law coverage where a code is involved, and on "
                          "any brand-standards or franchise endorsement the property carries. It "
                          "is a wording question with a large number attached, and it should be "
                          "identified in week one rather than discovered at closeout."),
                    ("callout", "Loss of franchise is its own exposure", [
                        ("p", "Where a property is out of service long enough, or fails to complete "
                          "a mandated improvement plan on schedule, the flag itself can be at "
                          "risk. The consequences of that go well beyond the repair cost, and they "
                          "are worth raising with the carrier early, as a reason for "
                          "urgency and for extra-expense spend, not as an afterthought."),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("How is business interruption calculated for a hotel?",
             "<p>Properly done, it projects what the property would have earned during the period "
             "of restoration from its own historical performance, adjusted for what the competitive "
             "set did in that period, then deducts actual earnings and saved "
             "expenses, and adds extra expense reasonably incurred to reduce the loss. The two "
             "arguments that decide the number are the length of the period of restoration and "
             "whether the ramp-back after reopening is included.</p>"),
            ("Can we claim for rooms that were not damaged but could not be sold?",
             "<p>Often yes. If corridors are under containment, lifts are out, or an entire floor "
             "is inaccessible because of work on the floor above, those rooms are out of inventory "
             "as a direct result of the physical damage. That has to be documented as it happens"
             ", a daily out-of-order log by room number is the single most useful record you "
             "can keep during a hotel loss.</p>"),
            ("The storm closed the roads, not the hotel. Is there any coverage?",
             "<p>Possibly, under civil authority or ingress/egress extensions, which respond when "
             "access to the property is prevented by an order of civil authority or by physical "
             "damage nearby. These extensions are narrow, time-limited and heavily conditioned, and "
             "they usually require physical damage of a type covered by the policy within a stated "
             "radius. Worth checking; not worth assuming.</p>"),
        ],
    },

    # ============================================ industrial / warehouse ====
    {
        "slug": "industrial-and-manufacturing",
        "nav_label": "Industrial &amp; Manufacturing",
        "card_title": "Industrial &amp; manufacturing",
        "card_blurb": ("Plants, warehouses and distribution centers, where the equipment and the "
                       "downtime dwarf the building."),
        "title": "Manufacturing &amp; Warehouse Losses | Texas Consultants",
        "description": "Expert witness and damage consulting for Texas manufacturers and warehouses. Equipment, stock, contingent business interruption and extra expense claims.",
        "eyebrow": "Who we serve &middot; Industrial",
        "h1": "The building is the<br><em>cheapest</em> thing in it",
        "h1_plain": "Manufacturing, warehouse and distribution claims",
        "lede": ("On an industrial loss the structure is often a fraction of the exposure. The "
                 "production line, the stock, the racking, the cold chain and the contract you "
                 "cannot fulfill are the claim. They are also the parts a general property adjuster "
                 "is least equipped to scope."),
        "head_aside": [
            ("ledger", "Where industrial value sits", [
                ("Building", "Smallest share"),
                ("Equipment", "Specialist valuation"),
                ("Stock", "Selling price?"),
                ("Racking &amp; MHE", "Often omitted"),
                ("Downtime", "Largest exposure"),
                ("Dependent property", "Check wording"),
            ], "The valuation clause on finished stock &mdash; cost versus selling price, "
               "can change a stock claim by a third."),
        ],
        "sections": [
            {
                "eyebrow": "Equipment",
                "h2": "Repairable, replaceable, or obsolete: three answers, three numbers.",
                "blocks": [
                    ("p", "The central dispute on most plant losses is whether a damaged machine "
                          "can be restored. Carriers prefer repair, and for good reason. It "
                          "is usually cheaper. Manufacturers prefer replacement, also for good "
                          "reason: a repaired machine that comes back out of tolerance costs more "
                          "in scrap and downtime than it saved."),
                    ("p", "That argument is not won with opinion. It is won with the "
                          "manufacturer&rsquo;s own assessment, with tolerance and calibration "
                          "data, with parts availability for equipment whose controls are twenty "
                          "years old, and with the practical question of what the installation "
                          "requires, rigging, foundations, power, controls "
                          "integration and requalification. Those installation costs regularly "
                          "exceed the price of the machine and are regularly left off the "
                          "carrier&rsquo;s estimate."),
                    ("checks", [
                        "OEM inspection reports rather than adjuster assessment on any production-critical asset.",
                        "Obsolescence and parts availability documented where the equipment predates current control systems.",
                        "Rigging, foundation work, utility connections, controls integration and commissioning carried as separate line items.",
                        "Requalification and validation where the process requires it, food, pharma, aerospace, automotive.",
                        "Equipment breakdown and property coverage reviewed together, so neither carrier can point at the other.",
                    ]),
                ],
                "aside": [
                    ("callout", "Racking and material handling", [
                        ("p", "Pallet racking, mezzanines, conveyors, ASRS and dock equipment are "
                              "usually classed as contents, often omitted from the "
                              "statement of values, and almost always under-scoped after a fire or "
                              "a roof collapse. Damaged racking must be engineer-assessed, not "
                              "eyeballed. It is a life-safety component."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Stock",
                "h2": "What is finished goods actually worth?",
                "blocks": [
                    ("p", "Standard property forms value stock at replacement cost, which for "
                          "finished goods means the cost to manufacture it again, not what "
                          "you would have sold it for. A selling-price endorsement changes that for "
                          "finished stock, and on a distribution operation with thin manufacturing "
                          "content it is worth a great deal. Whether you have one is a "
                          "thirty-second check that most people never make until there is a fire."),
                    ("table", "Stock valuation in practice", ["Category", "Default treatment", "What to check"], [
                        ["Raw materials", "Replacement cost at time of loss", "Market moves since purchase; commodity spikes"],
                        ["Work in progress", "Cost of materials plus labor and overhead expended", "Costing records good enough to prove stage of completion"],
                        ["Finished goods", "Cost to reproduce", "Selling-price endorsement; firm orders in hand"],
                        ["Goods of others", "Bailee coverage, if any", "Customers&rsquo; property on site and the contract terms"],
                        ["Temperature-sensitive", "Spoilage / refrigerated stock endorsement", "Breakdown trigger, deductible, and whether power failure off-premises is covered"],
                    ]),
                ],
            },
            {
                "eyebrow": "Downtime",
                "h2": "Contingent exposure runs in both directions.",
                "blocks": [
                    ("p", "A plant can be shut down by damage it did not suffer. Contingent business "
                          "interruption responds when a supplier or a customer sustains physical "
                          "damage that interrupts your operation: a sole-source component "
                          "supplier burns down, a port closes, the customer who takes 60% of your "
                          "output stops taking it. Coverage is usually sub-limited, commonly "
                          "requires the dependent property to be named, and is regularly the piece "
                          "nobody thought about until it happened."),
                    ("p", "Extra expense is the other half of the calculation, and on an industrial "
                          "file it is where recovery is genuinely earned: outsourced production, "
                          "expedited freight, rented equipment, temporary warehousing, overtime, "
                          "and the premium paid to accelerate the rebuild. Every dollar of that "
                          "spent sensibly reduces the business-income loss, and every dollar needs "
                          "a paper trail from the day it is incurred."),
                    ("html", '<a class="tlink" href="/tools/business-interruption-calculator/">'
                             'Model the downtime loss <span class="arw">&rarr;</span></a>'),
                ],
            },
        ],
        "faqs": [
            ("Our loss is mostly equipment, not building. Is that still a property claim?",
             "<p>Yes, and it is the part most likely to be under-adjusted, because scoping a "
             "production line requires manufacturer engagement instead of an estimating template. "
             "It may also sit across two coverages, property and equipment breakdown, "
             "with different deductibles and different adjusters. Getting those coordinated early "
             "prevents each side waiting on the other for four months.</p>"),
            ("How long does an industrial claim take?",
             "<p>Longer than anyone wants. A straightforward warehouse roof claim can settle in two "
             "to four months. A plant loss involving equipment assessment, forensic accounting and "
             "a contested period of restoration is typically nine to eighteen. The variable that "
             "moves that timeline most is how complete the documentation was in the first thirty "
             "days.</p>"),
            ("Can you get an advance payment while the claim is being worked?",
             "<p>Usually, and we push for it as a matter of routine. Where part of the loss is "
             "undisputed, there is rarely a good reason for the carrier to withhold it while the "
             "contested portion is argued. Advances keep the rebuild moving and reduce the "
             "business-income loss, which is in everybody&rsquo;s interest including the "
             "carrier&rsquo;s.</p>"),
        ],
    },

    # ================================================ retail / commercial ===
    {
        "slug": "retail-and-shopping-centers",
        "nav_label": "Retail &amp; Shopping Centers",
        "card_title": "Retail &amp; shopping centers",
        "card_blurb": ("Landlord and tenant obligations, loss of rents, co-tenancy exposure and a "
                       "roof nobody has walked in four years."),
        "title": "Shopping Center &amp; Retail Losses | Consultants",
        "description": "Expert witness and damage consulting for Texas shopping centers and retail owners. Hail and wind damage, loss of rents, tenant disruption and co-tenancy exposure.",
        "eyebrow": "Who we serve &middot; Retail",
        "h1": "One roof, fourteen<br>tenants, <em>one</em> claim",
        "h1_plain": "Shopping center and retail property claims",
        "lede": ("A retail center loss is a landlord claim, a set of tenant claims and a lease "
                 "dispute waiting to happen. Who repairs what, who is owed rent abatement and "
                 "whose insurance responds are all answered by documents written years before the "
                 "storm."),
        "head_aside": [
            ("ledger", "Retail center checklist", [
                ("Lease type", "NNN / gross"),
                ("Repair obligation", "Per lease"),
                ("Rent abatement", "Per lease"),
                ("Co-tenancy clause", "Check anchors"),
                ("Tenant improvements", "Whose policy?"),
                ("Signage &amp; pylon", "Separate item"),
            ], "The lease decides more of a retail claim than the policy does. Read both together."),
        ],
        "sections": [
            {
                "eyebrow": "Lease first",
                "h2": "The lease allocates the damage before the policy pays for it.",
                "blocks": [
                    ("p", "Before anyone argues about scope, establish who is obliged to repair "
                          "what. Most retail leases put the roof, structure and common areas on the "
                          "landlord and the interior, fixtures and tenant improvements on the "
                          "tenant, but the line is drawn differently in every lease, and "
                          "tenant improvements installed by the landlord and amortised through rent "
                          "can sit on either side of it."),
                    ("p", "Getting this wrong produces the worst outcome available: the "
                          "landlord&rsquo;s carrier declines an item as the tenant&rsquo;s "
                          "responsibility, the tenant&rsquo;s carrier declines it as the "
                          "landlord&rsquo;s, and nobody pays for eight months while both are right "
                          "about the other. We map the allocation against the leases at the start "
                          "and present the claim consistently with it."),
                ],
                "aside": [
                    ("callout", "Rent abatement is the hidden clock", [
                        ("p", "Where a lease abates rent while premises are untenantable, every "
                              "week of delay is a direct cost to the landlord that the loss-of-"
                              "rents coverage may or may not fully replace. That asymmetry is "
                              "usually the strongest argument for pushing the carrier on pace."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Scope",
                "h2": "What gets missed on a strip center.",
                "blocks": [
                    ("checks", [
                        "<strong>Roof by section and by age.</strong> Centers are extended over decades. Different membranes, different ages, different arguments about wear versus storm.",
                        "<strong>HVAC units.</strong> Rooftop package units take hail on coils and cabinets. Coil damage reduces efficiency long before it stops the unit, and comb-out is not always a repair.",
                        "<strong>Pylon and monument signage.</strong> Separately damageable, separately valued, and often subject to current sign-code restrictions on replacement.",
                        "<strong>Parapets, coping and flashing.</strong> Where wind damage begins, and where water gets in for the next two years.",
                        "<strong>Storefront glazing and awnings.</strong> Including the frames, which are rarely inspected.",
                        "<strong>Parking, lighting and site work.</strong> Pole lights, canopies, cart corrals, landscaping and drainage.",
                        "<strong>Tenant improvements and betterments.</strong> Identify whose policy covers them before either carrier is asked to pay.",
                    ]),
                    ("callout", "Co-tenancy", [
                        ("p", "If an anchor goes dark long enough after a loss, co-tenancy clauses "
                              "in the inline leases can trigger rent reductions or termination "
                              "rights across the center. That consequence is rarely covered "
                              "directly, and it is a powerful reason to treat the anchor&rsquo;s "
                              "restoration as the critical path."),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Should the landlord and the tenants file one claim or separate claims?",
             "<p>Separate policies mean separate claims, but they should be coordinated. The "
             "landlord&rsquo;s claim covers the building, common areas and loss of rents; each "
             "tenant&rsquo;s covers their improvements, contents and business income. Where they "
             "are presented inconsistently &mdash; different dates, different damage descriptions, "
             "overlapping scope, both carriers slow down. A single documented survey of the "
             "center that everyone works from prevents most of that.</p>"),
            ("The carrier says our roof damage is wear and tear, not hail. What now?",
             "<p>That is the single most common denial on Texas commercial roofs and it is "
             "answerable. The evidence is test cuts, spatter patterns on soft metals and "
             "mechanical equipment, directional consistency, the storm data for the date of loss, "
             "and the roof&rsquo;s documented maintenance history. Where the carrier has retained "
             "an engineer, you generally need your own. This is a frequent route into appraisal.</p>"),
            ("Can you help after we have already accepted a payment?",
             "<p>Often, through a supplemental claim. Accepting a payment is not the same as "
             "signing a full and final release, and most property policies contemplate supplements "
             "when the actual cost of repair exceeds the estimate. What matters is the policy&rsquo;s "
             "own time limits and the suit limitation period, which is why this is worth looking at "
             "now instead of next year.</p>"),
        ],
    },
]

for _i in INDUSTRIES:
    _i["path"] = _path(_i["slug"])
