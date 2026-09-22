"""Six Texas metros, written from what actually damages buildings in each.

Storm references are to real, documented events. The point of these pages is
that a hail file in Tarrant County and a surge file in Nueces County are
different arguments, not the same page with the city name swapped.
"""

from siteconfig import BIZ

P = BIZ["phone_display"]

AREAS = [

    {
        "slug": "austin",
        "city": "Austin",
        "nav_label": "Austin",
        "card_title": "Austin &amp; Central Texas",
        "card_blurb": ("Travis, Williamson and Hays counties &mdash; hail, freeze and a building "
                       "stock that doubled in fifteen years."),
        "title": "Austin Claims Consultants | Commercial Large Loss",
        "description": "Independent claims consultants for Austin commercial and institutional property claims. Churches, school districts, city facilities and portfolios across Central Texas.",
        "eyebrow": "Service area &middot; Central Texas",
        "h1": "Austin commercial<br>loss <em>consulting</em>",
        "h1_plain": "Claims consultants in Austin, Texas",
        "lede": ("Central Texas produces two kinds of institutional loss: hail on a very large "
                 "inventory of flat commercial roofing, and freeze damage to buildings that were "
                 "never designed for a week below freezing. We work both across the Austin metro."),
        "counties": "Travis, Williamson, Hays, Bastrop and Caldwell counties",
        "perils": [
            ("Hail", "Central Texas sits on the southern edge of the hail corridor. Spring "
                     "supercells regularly drop stones large enough to end the service life of a "
                     "modified bitumen or TPO roof without breaking a single window."),
            ("Winter freeze", "February 2021 exposed how much of the Austin building stock has "
                              "sprinkler and domestic water in unconditioned space. Freeze claims "
                              "here turn on heat-maintenance and winterisation records."),
            ("Wind and straight-line events", "Downbursts strip flashing, coping and rooftop "
                                              "equipment, and the resulting water intrusion is "
                                              "frequently reported as a roof leak months later."),
            ("Flash flooding", "Creek and low-water crossing flooding is a flood peril, not a "
                               "windstorm one. Whether your program responds at all is a "
                               "declarations-page question worth answering before May."),
        ],
        "local": [
            ("p", "The Austin metro added an extraordinary amount of institutional square footage "
                  "between 2010 and 2024 &mdash; school district bond programs across "
                  "Williamson and Hays counties, church campuses following the suburban growth "
                  "north and south, and municipal facilities in cities that were small towns "
                  "twenty years ago. A great deal of that construction is now old enough to have "
                  "taken several hail seasons and young enough that nobody has reviewed the "
                  "insured values since the certificate of occupancy."),
            ("p", "That combination produces a specific failure mode we see repeatedly: a campus "
                  "or a sanctuary insured at its 2013 construction cost, hit by hail in 2024, and "
                  "adjusted against a coinsurance clause nobody knew was there. The claim is "
                  "reduced by a ratio that has nothing to do with the damage."),
            ("p", "The other regional pattern is the freeze aftermath. A substantial number of "
                  "Central Texas institutions took freeze damage in 2021 that was repaired "
                  "cheaply, settled quickly and has been leaking quietly ever since. Where the "
                  "original repair was inadequate and the file was never closed with a release, "
                  "a supplemental claim is sometimes still available."),
        ],
        "faqs": [
            ("Do you work directly with Austin-area school districts and cities?",
             "<p>Yes, and the public-entity work has its own rhythm: board or council approval, "
             "a purchasing process, documentation written for a public packet, and a repair "
             "schedule built around the academic calendar or a council meeting cycle. We are used "
             "to all of it and produce the paperwork rather than asking the district to invent "
             "it.</p>"),
            ("How quickly can you get to a property in the Austin area?",
             "<p>Same day or next day for a significant loss under normal conditions. After a "
             "regional catastrophe, everybody in the industry is stretched &mdash; we will tell "
             "you honestly what we can commit to rather than booking an inspection we cannot "
             "staff.</p>"),
        ],
    },

    {
        "slug": "houston",
        "city": "Houston",
        "nav_label": "Houston",
        "card_title": "Houston &amp; the Gulf Coast",
        "card_blurb": ("Harris and the surrounding counties &mdash; wind, surge, derecho and the "
                       "flood-versus-wind argument that follows every named storm."),
        "title": "Houston Claims Consultants | Hurricane &amp; Large Loss",
        "description": "Independent claims consultants for Houston commercial and institutional property claims. Hurricane, windstorm, flood-versus-wind causation, fire and business interruption.",
        "eyebrow": "Service area &middot; Gulf Coast",
        "h1": "Houston commercial<br>and <em>catastrophe</em> claims",
        "h1_plain": "Claims consultants in Houston, Texas",
        "lede": ("No metro in Texas has been tested harder. Harvey in 2017, the May 2024 derecho, "
                 "Hurricane Beryl two months later &mdash; Houston institutions have learned more "
                 "about their policy wording in eight years than most learn in fifty."),
        "counties": "Harris, Fort Bend, Montgomery, Galveston, Brazoria and Liberty counties",
        "perils": [
            ("Named storms", "Percentage deductibles, anti-concurrent causation wording and the "
                             "wind-versus-surge line are the three things that decide a Houston "
                             "hurricane claim, and all three are settled with evidence gathered "
                             "in the first ten days."),
            ("Straight-line wind", "The May 2024 derecho demonstrated that a non-named event can "
                                   "produce hurricane-force damage across a metro &mdash; and, "
                                   "usefully for policyholders, without triggering a named-storm "
                                   "deductible. Which deductible applies is worth confirming."),
            ("Flooding", "Excluded on virtually every commercial property form. Where surge or "
                         "rainfall flooding contributed, expect the anti-concurrent causation "
                         "clause to be invoked broadly."),
            ("Fire and mechanical", "The industrial base means fire, equipment breakdown and "
                                    "contingent business interruption claims that are technically "
                                    "complex before any coverage question arises."),
        ],
        "local": [
            ("p", "Houston&rsquo;s recurring institutional problem is sequential loss. A church, "
                  "campus or civic building damaged by Harvey, repaired under a settlement that "
                  "was thin, then damaged again in 2024, arrives at the second claim with a "
                  "carrier arguing that the current condition is the unrepaired remnant of the "
                  "first event. Untangling that requires the prior claim file, the prior scope, "
                  "the invoices for what was actually done, and photographs from both periods."),
            ("p", "The second pattern is the flood-versus-wind split on the coastal side of the "
                  "metro. Where a property carries both a flood policy and a commercial property "
                  "policy, the two adjusters have opposite incentives about the same water line, "
                  "and a policyholder who lets them run independently frequently ends up "
                  "under-recovered by both. Those files need to be run together, with one "
                  "consistent damage description."),
            ("p", "Beryl in July 2024 added a third: extended power loss. Institutions with "
                  "spoiled stock, failed refrigeration, lost cold chain and days of closure "
                  "should check for service interruption cover, which frequently requires "
                  "physical damage to the utility&rsquo;s own property and frequently excludes "
                  "overhead transmission lines. It is a narrow extension, and it is worth "
                  "reading before you assume it responds."),
        ],
        "faqs": [
            ("Our Harvey claim was settled years ago. Is there anything left in it?",
             "<p>Occasionally, and it depends almost entirely on whether a full and final release "
             "was signed and whether the limitation period has run. Where repairs were never "
             "completed, where recoverable depreciation was never released, or where the damage "
             "proved materially worse than the settled scope, a supplement may still be live. "
             "It costs nothing to have the file looked at, and the answer usually comes within a "
             "week.</p>"),
            ("The carrier says our damage is flood. We do not carry flood.",
             "<p>That is the standard opening position on a coastal Texas claim and it is "
             "answerable with evidence. Roof and upper-floor damage above the water line is "
             "difficult to attribute to surge. Directional failure patterns, debris deposition, "
             "the timing of the wind field against the surge, and storm data for your specific "
             "coordinates all separate the perils. Where anti-concurrent causation wording is "
             "being applied aggressively, counsel should be looking at it alongside us.</p>"),
        ],
    },

    {
        "slug": "dallas-fort-worth",
        "city": "Dallas",
        "nav_label": "Dallas&ndash;Fort Worth",
        "card_title": "Dallas&ndash;Fort Worth",
        "card_blurb": ("The most hail-exposed metro in the United States, with an institutional "
                       "building stock to match."),
        "title": "Dallas&ndash;Fort Worth Claims Consultants | Hail Losses",
        "description": "Independent claims consultants for Dallas-Fort Worth commercial and institutional property claims. Hail, wind, tornado and fire losses across the Metroplex.",
        "eyebrow": "Service area &middot; North Texas",
        "h1": "Dallas&ndash;Fort Worth<br><em>hail</em> and large loss",
        "h1_plain": "Claims consultants in Dallas–Fort Worth",
        "lede": ("North Texas produces more insured hail damage than anywhere else in the country. "
                 "It has also produced a generation of carrier adjusters unusually practiced at "
                 "arguing that a twenty-year-old commercial roof was already finished."),
        "counties": "Dallas, Tarrant, Collin, Denton, Rockwall, Ellis and Johnson counties",
        "perils": [
            ("Hail", "Repeated severe hail across the Metroplex &mdash; the 2012 and 2016 events "
                     "among the costliest in US history &mdash; means most institutional roofs "
                     "here have a claim history, which carriers use to argue any new damage is "
                     "old."),
            ("Tornado and downburst", "The October 2019 Dallas tornado showed how a narrow track "
                                      "produces total losses on one street and argued-over claims "
                                      "two blocks away."),
            ("Freeze", "The 2021 event reached North Texas hard, and sprinkler failures in "
                       "unheated spaces produced some of the largest institutional water losses "
                       "in the state."),
            ("Wind-driven rain", "Coping and parapet failures on the region&rsquo;s vast stock of "
                                 "low-slope commercial roofing put water into buildings without "
                                 "any visible roof damage at all."),
        ],
        "local": [
            ("p", "The defining feature of a DFW commercial claim is the intervening-storm "
                  "argument. With multiple severe hail events across most of the Metroplex in the "
                  "last fifteen years, a carrier can almost always point to a prior date and "
                  "suggest the damage belongs to a policy period that has closed. Answering it "
                  "requires dated aerial imagery, the prior claim history, evidence of what was "
                  "repaired after each event, and a roof survey that distinguishes weathered "
                  "damage from fresh impact."),
            ("p", "The second feature is scale. School districts in Collin and Denton counties "
                  "run bond programs larger than some states&rsquo; entire school construction "
                  "budgets, and a single storm can touch twenty campuses. On files that size, the "
                  "occurrence definition and the deductible structure matter more than any "
                  "individual scope dispute."),
            ("p", "Cosmetic damage exclusions also appear more often on North Texas commercial "
                  "programs than elsewhere in the state, for obvious underwriting reasons. If "
                  "one is on your policy, the entire claim becomes an argument about function and "
                  "remaining service life &mdash; and that argument needs a qualified opinion, not "
                  "a contractor&rsquo;s letter."),
        ],
        "faqs": [
            ("How do we prove which storm caused the damage?",
             "<p>With dated evidence rather than assertion. Aerial and satellite imagery by date, "
             "the property&rsquo;s own inspection and maintenance records, the prior claim files "
             "and what was actually repaired, storm data for the specific coordinates, and a roof "
             "survey by someone competent to distinguish fresh impact from weathered damage. On "
             "DFW files this is usually the central factual question.</p>"),
            ("We have already had two hail claims. Will a third be taken seriously?",
             "<p>It will be scrutinised, which is not the same thing. The answer is documentation "
             "that the earlier damage was properly repaired: invoices, close-out photographs, "
             "warranty reinstatement. Where earlier claims were settled and the money spent on "
             "something else, that is a harder file &mdash; and still worth assessing honestly "
             "before you report.</p>"),
        ],
    },

    {
        "slug": "san-antonio",
        "city": "San Antonio",
        "nav_label": "San Antonio",
        "card_title": "San Antonio &amp; South Central Texas",
        "card_blurb": ("Bexar County and the Hill Country edge &mdash; hail, flash flood and a "
                       "deep stock of historic institutional buildings."),
        "title": "San Antonio Claims Consultants | Commercial Losses",
        "description": "Independent claims consultants for San Antonio commercial and institutional property claims. Hail, wind, flood and fire for churches, districts and municipalities.",
        "eyebrow": "Service area &middot; South Central Texas",
        "h1": "San Antonio<br><em>institutional</em> claims",
        "h1_plain": "Claims consultants in San Antonio, Texas",
        "lede": ("San Antonio has an unusually old institutional building stock for a Sun Belt "
                 "city &mdash; parish churches, mission-era structures, mid-century schools and "
                 "civic buildings. That makes ordinance and law coverage the decisive clause on a "
                 "large share of local claims."),
        "counties": "Bexar, Comal, Guadalupe, Kendall, Medina and Wilson counties",
        "perils": [
            ("Hail", "The April 2016 hailstorm remains one of the costliest in Texas history and "
                     "reset expectations about what Bexar County can produce. Stones over two "
                     "inches across a dense urban core."),
            ("Flash flooding", "The Hill Country edge produces some of the most severe flash "
                               "flooding in North America. It is a flood peril, and most "
                               "commercial property programs exclude it."),
            ("Wind and severe thunderstorm", "Straight-line damage to roofing, coping, signage "
                                             "and rooftop mechanical, usually followed by interior "
                                             "water claims months later."),
            ("Freeze", "Older masonry buildings with exposed or minimally insulated plumbing "
                       "runs are disproportionately represented in South Texas freeze losses."),
        ],
        "local": [
            ("p", "Age is the theme here. When a mid-century school building, a parish church or "
                  "a civic structure is substantially repaired, the local jurisdiction can require "
                  "the whole building to come up to current code &mdash; fire suppression, egress, "
                  "accessibility, energy, sometimes structural detailing that did not exist at "
                  "construction. That cost is frequently a large multiple of the storm damage "
                  "itself."),
            ("p", "Ordinance or law coverage is what answers it, and it normally comes in three "
                  "parts with three separate limits: the undamaged portion that must be "
                  "demolished, the demolition and debris cost, and the increased cost of "
                  "construction. Those limits were usually set as a small percentage of the "
                  "building limit by someone who was not imagining this repair. Establishing what "
                  "the building official will actually require, in writing, is the single highest "
                  "value early step on a San Antonio institutional file."),
            ("p", "Historic designation adds a further layer. Where a structure is designated, "
                  "replacement materials and methods may be constrained in ways that a standard "
                  "estimating platform prices at ordinary commercial rates. That gap is "
                  "documentable, and it should be documented before the carrier anchors a number."),
        ],
        "faqs": [
            ("Our building is historic. Does insurance pay for matching materials?",
             "<p>It depends on the valuation basis and on whether the requirement is legally "
             "imposed. A policy written on functional replacement cost permits modern equivalents. "
             "A replacement-cost policy contemplates like kind and quality. Where a historic "
             "designation or the building code legally requires specific materials or methods, "
             "ordinance and law coverage is the route &mdash; subject to its own limit, which is "
             "the number worth checking now rather than after a fire.</p>"),
            ("How much ordinance and law coverage should we carry?",
             "<p>More than the default, on almost any building older than about thirty years. The "
             "useful exercise is to ask your building official what a substantial repair would "
             "trigger, price that work, and compare it to the limit on your declarations page. "
             "That comparison takes an afternoon and is the most valuable thing most older "
             "institutions can do before renewal.</p>"),
        ],
    },

    {
        "slug": "corpus-christi-and-the-coastal-bend",
        "city": "Corpus Christi",
        "nav_label": "Corpus Christi &amp; Coastal Bend",
        "card_title": "Corpus Christi &amp; the Coastal Bend",
        "card_blurb": ("First-tier coastal counties, TWIA wind cover, and the surge line that "
                       "decides which policy responds."),
        "title": "Coastal Bend Claims Consultants | Corpus Christi",
        "description": "Independent claims consultants for Corpus Christi and the Coastal Bend commercial property claims. TWIA windstorm, hurricane, surge-versus-wind and business interruption.",
        "eyebrow": "Service area &middot; Coastal Bend",
        "h1": "Coastal Bend wind<br>and <em>surge</em> claims",
        "h1_plain": "Claims consultants in Corpus Christi and the Coastal Bend",
        "lede": ("On the coast the coverage architecture is different. Windstorm may sit with "
                 "TWIA, flood with a separate policy, and everything else with a commercial "
                 "carrier &mdash; three adjusters looking at one building and each hoping the "
                 "damage belongs to somebody else."),
        "counties": "Nueces, San Patricio, Aransas, Kleberg, Refugio, Bee and Jim Wells counties",
        "perils": [
            ("Hurricane and tropical storm", "Harvey made landfall near Rockport in 2017 as a "
                                             "Category 4 and rewrote what Coastal Bend "
                                             "institutions expect from a storm."),
            ("Storm surge", "Excluded from property policies and covered, if at all, by separate "
                            "flood insurance. The line between wind and water is the central "
                            "evidentiary question on every coastal file."),
            ("Windstorm under TWIA", "Property in the designated first-tier coastal counties may "
                                     "carry windstorm through the Texas Windstorm Insurance "
                                     "Association, which has its own procedures, deadlines and "
                                     "dispute process."),
            ("Corrosion and salt exposure", "Coastal mechanical equipment degrades faster, which "
                                            "gives carriers a ready-made wear argument on "
                                            "storm-damaged rooftop units."),
        ],
        "local": [
            ("p", "The multi-policy structure is what makes Coastal Bend claims difficult. A "
                  "school district or a city with TWIA windstorm cover, a separate flood policy "
                  "and an all-other-perils commercial program is dealing with three files, "
                  "three adjusters, three sets of deadlines and three different definitions of "
                  "what happened. Inconsistency between them is the single biggest self-inflicted "
                  "problem we see."),
            ("p", "TWIA in particular runs to its own timetable and its own appeal and dispute "
                  "resolution process, which is not the same as a standard carrier&rsquo;s and "
                  "which has deadlines that are genuinely unforgiving. Institutions used to "
                  "dealing with a commercial carrier regularly assume the ordinary process applies "
                  "and find out otherwise."),
            ("p", "The evidentiary priority after a landfalling storm is always the same: "
                  "establish the wind damage before the water damage is cleaned up. High-water "
                  "marks, roof condition, upper-floor damage, directional failure patterns and "
                  "debris deposition all disappear within days as the property is made safe. "
                  "Photograph first, mitigate second &mdash; and photograph again during "
                  "mitigation."),
        ],
        "faqs": [
            ("Our windstorm cover is with TWIA. Can a consultant help?",
             "<p>Yes, and the procedural differences are a large part of why it is worth having "
             "someone who knows them. TWIA has its own claim handling requirements, its own "
             "deadlines for disputing a decision and its own dispute resolution route. Those "
             "deadlines are strict, and an institution that treats a TWIA claim like an ordinary "
             "carrier claim can lose rights simply by waiting.</p>"),
            ("How do we handle having three separate policies on one loss?",
             "<p>With one damage description and one set of measurements, used across all three "
             "files. Each policy is presented with the portion of the loss that belongs to it, "
             "documented consistently, so that no adjuster can point at another policy and no "
             "inconsistency undermines any of the three. Coordinating that is most of the work "
             "on a coastal institutional claim.</p>"),
        ],
    },

    {
        "slug": "rio-grande-valley",
        "city": "McAllen",
        "nav_label": "Rio Grande Valley",
        "card_title": "Rio Grande Valley",
        "card_blurb": ("Hidalgo and Cameron counties &mdash; tropical systems, flooding, and some "
                       "of the fastest institutional growth in the state."),
        "title": "Rio Grande Valley Claims Consultants | Commercial",
        "description": "Independent claims consultants for Rio Grande Valley commercial and institutional property claims across Hidalgo, Cameron, Willacy and Starr counties.",
        "eyebrow": "Service area &middot; South Texas",
        "h1": "Rio Grande Valley<br>commercial <em>claims</em>",
        "h1_plain": "Claims consultants in the Rio Grande Valley",
        "lede": ("The Valley combines coastal windstorm exposure, inland flooding and the fastest "
                 "school and municipal construction growth in South Texas &mdash; against an "
                 "insurance market that has hardened sharply and a building stock that has "
                 "outgrown its statements of value."),
        "counties": "Hidalgo, Cameron, Willacy and Starr counties",
        "perils": [
            ("Tropical systems", "Hurricane Hanna in 2020 produced widespread wind and freshwater "
                                 "flood damage across the Valley and exposed how many "
                                 "institutions had neither flood cover nor accurate values."),
            ("Rainfall flooding", "Drainage capacity across much of the Valley is a known "
                                  "constraint, and heavy-rain flooding is a recurring "
                                  "institutional exposure that property policies exclude."),
            ("Hail and severe storm", "Less frequent than North Texas and entirely capable of "
                                      "ending a low-slope roof&rsquo;s service life when it "
                                      "happens."),
            ("Heat and thermal cycling", "Accelerated membrane aging gives carriers an easy wear "
                                         "argument; documented maintenance is the counter."),
        ],
        "local": [
            ("p", "Valley school districts and municipalities have built heavily over the last "
                  "fifteen years, frequently through bond programs, and the insured values on "
                  "that construction have not always kept pace with what it would now cost to "
                  "replace. Construction cost inflation since 2020 has been severe enough that a "
                  "schedule assembled in 2019 can fail a 90% coinsurance test today without "
                  "anybody having done anything wrong."),
            ("p", "The second local issue is the wind-versus-water split, which in the Valley is "
                  "usually rainfall flooding rather than surge. The distinction matters just as "
                  "much: property policies exclude flood, so establishing what the wind did "
                  "&mdash; roof, envelope, upper floors &mdash; before the ground-level water "
                  "damage is cleaned up is the difference between a covered claim and a denied "
                  "one."),
            ("p", "We work across Hidalgo, Cameron, Willacy and Starr counties and we can conduct "
                  "the engagement in English or Spanish, including the documentation a board or "
                  "council needs in order to approve it."),
        ],
        "faqs": [
            ("Do you work in Spanish?",
             "<p>Yes &mdash; inspections, meetings and correspondence. Where a board or council "
             "needs documentation in both languages for a public meeting, we produce it.</p>"),
            ("Our district built new campuses recently. Are the values likely to be wrong?",
             "<p>Frequently, and not through anyone&rsquo;s fault. Commercial construction costs "
             "in Texas rose sharply after 2020, and a statement of values built from 2018 or 2019 "
             "construction contracts can sit well below current replacement cost. If your "
             "program carries a coinsurance clause rather than agreed value, that gap becomes a "
             "penalty on every claim. It is worth testing before renewal rather than after a "
             "storm.</p>"),
        ],
    },
]

for _a in AREAS:
    _a["path"] = "/service-areas/%s/" % _a["slug"]
