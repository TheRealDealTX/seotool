"""Service page copy for floridainsuranceappraiser.com.

HTML bodies use single-quoted Python strings so href attributes can use
double quotes; apostrophes in copy are typographic (’).
"""

SERVICES = [
    # ------------------------------------------------------------------
    {
        "slug": "homeowners-claim-appraisal",
        "name": "Homeowners Claim Appraisal",
        "icon": "home",
        "short": "Independent appraisal for Florida homeowners whose insurer agrees the loss is covered but disagrees on what it will cost to repair.",
        "title": "Homeowners Claim Appraisal in Florida",
        "description": "Insurer accepted the claim but paid too little? Florida Insurance Appraiser handles homeowners claim appraisal statewide to settle the amount of loss.",
        "h1": "Homeowners Claim Appraisal for Florida Property Owners",
        "kicker": "Residential amount-of-loss disputes",
        "lead": "When your carrier agrees the damage is covered but its estimate will not put your home back together, the appraisal clause in most Florida homeowners policies gives you a structured way to resolve the dollar figure. We act as your independent appraiser and build the case around measurements, pricing and documentation.",
        "sections": [
            (
                "What homeowners appraisal actually resolves",
                '<p>Appraisal is a contractual process written into most Florida HO-3 and HO-5 policies. It exists for one narrow purpose: deciding the <strong>amount of loss</strong> when you and the insurer cannot agree on it. It does not decide whether a peril is covered, whether an exclusion applies or whether the carrier acted in bad faith. Those are coverage and legal questions, and they belong with an attorney or the courts.</p>'
                '<p>That narrow focus is also its strength. If the dispute really is about square footage, scope, unit pricing, depreciation or whether a matching repair is reasonable, appraisal can move faster and cost less than litigation. Florida Insurance Appraiser works only in that amount-of-loss lane.</p>',
            ),
            (
                "How the two-appraiser and umpire structure works",
                '<p>Once appraisal is properly invoked, each side names its own competent, independent appraiser. The two appraisers inspect the property, exchange estimates and try to reach agreement. If they cannot, they select a neutral umpire, and a written award signed by any two of the three generally sets the amount of loss.</p>'
                '<ol><li>Written demand for appraisal under your policy’s provision</li><li>Each party names an appraiser within the time the policy allows</li><li>Joint inspection and estimate exchange</li><li>Negotiation item by item</li><li>Umpire involvement only on items still in dispute</li><li>Signed award</li></ol>'
                '<p>We walk through each stage in more detail on our <a href="/appraisal-process/">appraisal process</a> page.</p>',
            ),
            (
                "Where homeowner estimates usually fall short",
                '<p>Carrier estimates on Florida homes tend to come up short in predictable places. We see the same patterns across ranch homes in Ocala and two-story block houses in Broward:</p>'
                '<ul><li><strong>Partial-room scope</strong> that paints one wall instead of the full room, leaving visible mismatches</li><li><strong>Flooring</strong> priced as a patch when the product line has been discontinued and continuous flooring runs through several rooms</li><li><strong>Depreciation</strong> applied too aggressively to labor or to items with long service lives</li><li><strong>Overhead and profit</strong> omitted even though the job plainly needs a general contractor to coordinate multiple trades</li><li><strong>Ordinance or law</strong> items, such as code-required upgrades, left out entirely</li></ul>',
            ),
            (
                "Additional living expense and contents",
                '<p>The dwelling estimate is rarely the whole loss. If your home was unlivable during repairs, Coverage D (additional living expense or loss of use) may reimburse the extra costs of staying elsewhere. Contents claims need an itemized inventory with ages and replacement prices, which many families never finish because the task feels overwhelming. Our free <a href="/claim-tools/contents-inventory-builder/">contents inventory builder</a> helps break that list into manageable rooms before we ever get to the appraisal table.</p>',
            ),
            (
                "Appraisal versus other Florida options",
                '<p>Appraisal is not your only route. The Florida Department of Financial Services runs a mediation program for many residential property disputes, which can be a lower-cost first step. Some homeowners hire a public adjuster to present the claim; others need an attorney because the insurer has denied coverage outright. We are neither public adjusters nor lawyers. If your problem is a denial rather than a low number, we will tell you that appraisal is probably the wrong tool.</p>',
            ),
            (
                "Is your claim a good candidate?",
                '<p>Appraisal tends to make sense when the gap between your contractor’s estimate and the carrier’s payment is large enough to justify the appraisal and umpire fees your policy assigns to each side. Our <a href="/claim-tools/appraisal-worth-it-calculator/">appraisal worth-it calculator</a> gives a rough read in a couple of minutes. Florida Insurance Appraiser is also glad to review your paperwork and give an honest opinion before you commit. This page is general information, not legal advice; your policy language controls.</p>',
            ),
        ],
        "checklist": [
            "Full policy with declarations page and all endorsements",
            "Carrier’s estimate and every payment letter",
            "Your contractor’s estimate or bids",
            "Dated photos and video of the damage",
            "Receipts for emergency repairs and mitigation",
            "Hotel, rental or meal receipts if you were displaced",
            "Claim correspondence and adjuster notes you received",
        ],
        "faqs": [
            ("Can appraisal force my insurer to cover something it denied?", "No. Appraisal sets the dollar amount of a covered loss. If the carrier has denied coverage for a peril or an item, that is a coverage question for an attorney or the courts, not for appraisers."),
            ("Who pays for the appraisal?", "Most Florida policies say each side pays its own appraiser and the umpire’s fee is split. Check the appraisal provision in your policy, since wording varies by carrier."),
            ("Do I have to accept the appraisal award?", "Policies typically make an award signed by two of the three panel members binding on the amount of loss. Coverage defenses and policy conditions can still affect what is ultimately paid, so read your policy and get legal advice if you have concerns."),
            ("How long does homeowners appraisal take?", "It depends on scheduling, the size of the loss and whether an umpire is needed. Many residential appraisals resolve in weeks to a few months, but no timeline can be guaranteed."),
        ],
        "related_tools": ["appraisal-worth-it-calculator", "contents-inventory-builder", "appraisal-readiness-quiz"],
        "related_services": ["roof-claim-appraisal", "water-damage-claim-appraisal", "xactimate-estimate-review"],
    },
    # ------------------------------------------------------------------
    {
        "slug": "hurricane-claim-appraisal",
        "name": "Hurricane Claim Appraisal",
        "icon": "hurricane",
        "short": "Appraisal for windstorm and hurricane losses across Florida, from roof and soffit damage to wind-driven rain and interior repairs.",
        "title": "Hurricane Claim Appraisal in Florida",
        "description": "Florida hurricane claim appraisal for underpaid windstorm losses. We document wind damage, test the hurricane deductible math and build a defensible estimate.",
        "h1": "Hurricane Claim Appraisal Across Florida",
        "kicker": "Windstorm loss valuation",
        "lead": "After a named storm, carriers are processing thousands of claims at once, and estimates written under that pressure often miss scope. We help Florida policyholders use the appraisal clause to settle what a covered hurricane loss is actually worth.",
        "sections": [
            (
                "The hurricane deductible changes the math",
                '<p>Most Florida homeowners policies carry a separate hurricane deductible expressed as a percentage of Coverage A, the dwelling limit, rather than a flat dollar amount. On a home insured for $400,000, a 2% deductible is $8,000 and a 5% deductible is $20,000. That means a carrier estimate that looks only modestly low can leave you with little or nothing above the deductible.</p>'
                '<p>Florida law generally applies the hurricane deductible once per hurricane season for residential policies rather than once per storm, though the details depend on your policy and whether you have had earlier hurricane claims that year. Run your own numbers with our <a href="/claim-tools/hurricane-deductible-calculator/">hurricane deductible calculator</a> before deciding whether appraisal is worth pursuing.</p>',
            ),
            (
                "Wind versus water: know which policy pays",
                '<p>Standard homeowners policies cover wind and wind-driven rain that enters through a storm-created opening. They generally exclude flood, meaning rising surface water and storm surge. Flood coverage comes from a separate policy, typically through the National Flood Insurance Program or a private flood carrier, with its own claim process and its own dispute rules.</p>'
                '<p>Appraisal under a homeowners policy can value the wind portion of a mixed loss, but it cannot decide whether a given water line on your drywall came from wind-driven rain or surge. That causation question is a coverage issue. What appraisers can do is carefully separate the line items so the wind scope is fully priced. At Florida Insurance Appraiser, that separation is one of the first things we review.</p>',
            ),
            (
                "Hurricane damage that adjusters often under-scope",
                '<ul><li>Lifted or creased shingles and broken seal strips that are not obvious from the ground</li><li>Tile roofs with cracked or displaced tiles, where matching tile may no longer be available</li><li>Soffit, fascia and gutter damage that lets rain into the attic</li><li>Screen enclosures and pool cages, which often carry their own sublimits</li><li>Wet attic insulation and ceiling drywall from water intrusion through damaged roof decking</li><li>Fences, sheds and other structures, typically under Coverage B</li></ul>'
                '<p>We document each of these with measurements and photos tied to specific estimate lines, so the appraisal discussion stays about facts.</p>',
            ),
            (
                "Timing after a Florida storm",
                '<p>Florida has tightened claim reporting deadlines in recent years, and your policy may also set its own timeframes for supplemental claims and for invoking appraisal. Do not assume you have unlimited time. Our <a href="/claim-tools/claim-deadline-calculator/">claim deadline calculator</a> gives a general sense of the windows involved, but your policy and current Florida statutes control, and an attorney can confirm deadlines for your specific situation.</p>',
            ),
            (
                "How we approach a hurricane appraisal",
                '<p>Our team starts with the carrier’s estimate and photos, then reinspects the property ourselves. We compare scope, measurements and pricing against current market conditions for your area, which matters after a major storm when labor and material costs can spike. From there we prepare an independent estimate and negotiate with the carrier’s appraiser line by line. If an umpire is needed, we present the disputed items with supporting documentation.</p>'
                '<p>We serve coastal and inland communities alike, including <a href="/florida-locations/fort-myers-fl/">Fort Myers</a>, Tampa Bay, the Panhandle and South Florida.</p>',
            ),
            (
                "Citizens and private carriers",
                '<p>Many Florida homeowners are insured by Citizens Property Insurance Corporation, the state-created insurer of last resort, while others are with private carriers or surplus lines insurers. Appraisal provisions differ between these policies, and some carriers have changed their provisions over time. Florida Insurance Appraiser reads your specific form before recommending anything, and we will tell you if a flood claim or a coverage denial needs a different professional. This is general information, not legal advice.</p>',
            ),
        ],
        "checklist": [
            "Declarations page showing Coverage A and your hurricane deductible percentage",
            "Any flood policy and its claim number, if you have one",
            "Pre-storm photos of the home, if available",
            "Post-storm photos and video, including the roof and attic",
            "Carrier estimate, payment letters and denial letters",
            "Invoices for tarping, dry-out or tree removal",
        ],
        "faqs": [
            ("Can appraisal decide whether damage was caused by wind or flood?", "No. Causation and coverage questions are outside appraisal. Appraisers value the covered loss, so the wind-related scope needs to be clearly separated from flood or surge damage."),
            ("Does the hurricane deductible apply to every storm?", "Florida law generally applies it once per hurricane season for residential policies, but the specifics depend on your policy and prior claims that season. Review your declarations page and policy wording."),
            ("Is it worth appraising a claim that is close to my deductible?", "Sometimes. If the true repair cost is well above the deductible but the carrier’s estimate is not, appraisal can make a real difference. If the gap is small, fees may outweigh the benefit."),
            ("Do you work with Citizens policies?", "Yes. We review the appraisal provision in your Citizens or private carrier policy before recommending a course of action, since the wording varies."),
        ],
        "related_tools": ["hurricane-deductible-calculator", "claim-deadline-calculator", "appraisal-worth-it-calculator"],
        "related_services": ["roof-claim-appraisal", "condo-hoa-claim-appraisal", "umpire-services"],
    },
    # ------------------------------------------------------------------
    {
        "slug": "roof-claim-appraisal",
        "name": "Roof Claim Appraisal",
        "icon": "roof",
        "short": "Roof-focused appraisal for shingle, tile, metal and flat roofs, covering measurements, matching, code items and roof payment schedules.",
        "title": "Roof Claim Appraisal in Florida",
        "description": "Disputing a Florida roof claim estimate? We measure, document and price shingle, tile, metal and flat roofs, then negotiate the amount of loss in appraisal.",
        "h1": "Florida Roof Claim Appraisal",
        "kicker": "Shingle, tile, metal and flat roofs",
        "lead": "Roofs are where Florida property claims are most often fought, and the rules around them shifted after the 2022 insurance reforms. We focus on what appraisal can resolve: how much roof is damaged, what a proper repair or replacement costs and how your policy’s roof terms affect the number.",
        "sections": [
            (
                "Repair or replace: the core roof dispute",
                '<p>The most common roof disagreement is not whether a storm hit the house. It is whether the damage calls for a few squares of repair or a full slope or full roof replacement. Carriers often price spot repairs; contractors often say the roof cannot be repaired without creating a patchwork or violating code. Appraisal is well suited to this kind of scope argument because it turns on measurements, material availability and repairability.</p>',
            ),
            (
                "The 2022 reforms and roof terms in your policy",
                '<p>Florida’s 2022 property insurance legislation changed how roof claims are handled in several ways. Insurers gained more room to offer policies with roof payment schedules or actual cash value terms for older roofs, which can mean depreciation is deducted from roof payments even when the rest of the dwelling is on a replacement cost basis. Rules around when a partially damaged roof must be fully replaced to meet code were also revised, including treatment of roofs already built to newer code standards.</p>'
                '<p>We will not guess at your policy’s roof terms. We read the actual endorsements, identify any roof schedule or ACV language and price the claim accordingly. Our article on <a href="/blog/florida-roof-claims-after-the-2022-reforms/">Florida roof claims after the 2022 reforms</a> covers the background, and it is general information rather than legal advice.</p>',
            ),
            (
                "Measurement is where money hides",
                '<p>A roof estimate lives or dies by its quantities. Small errors in pitch, waste factor, ridge length or starter course add up quickly. We verify:</p>'
                '<ul><li>Total squares by slope, with pitch confirmed</li><li>Waste factor appropriate to the roof geometry, hips and valleys</li><li>Linear feet of ridge, hip, valley, drip edge and eave</li><li>Underlayment type required by current code</li><li>Steep and high-roof charges where the pitch or height warrants them</li></ul>'
                '<p>Try our <a href="/claim-tools/roof-measurement-calculator/">roof measurement calculator</a> to get a rough sense of squares before we inspect.</p>',
            ),
            (
                "Matching tile and discontinued shingles",
                '<p>Concrete and clay tile roofs are common across Florida, and replacement tile that matches in profile and color is frequently unavailable. The same is true of shingle lines that have been discontinued. Florida law generally addresses matching for residential claims, requiring reasonable uniformity in appearance, though how that applies to your roof depends on the facts and your policy. We document availability with supplier information so the matching argument rests on evidence.</p>',
            ),
            (
                "Depreciation and roof age",
                '<p>Roof age is now a central factor in Florida claims. Depreciation should reflect the roof’s actual condition and expected life, not just a calendar calculation. A well-maintained tile roof and a neglected shingle roof of the same age are not equivalent. If your policy pays roofs at actual cash value, check the carrier’s depreciation figure with our <a href="/claim-tools/acv-depreciation-calculator/">ACV depreciation calculator</a>.</p>',
            ),
            (
                "Working with Florida Insurance Appraiser on a roof claim",
                '<p>Florida Insurance Appraiser inspects the roof directly when it is safe to do so, photographs each slope, records test squares where appropriate and prepares an itemized estimate. We then negotiate with the carrier’s appraiser and, if needed, present the remaining items to an umpire. We do not decide coverage, and we cannot promise any result, but we make sure the roof is measured and priced correctly.</p>',
            ),
        ],
        "checklist": [
            "Policy endorsements, especially any roof payment schedule or ACV roof language",
            "Roof permit or installation date, if you know it",
            "Roofer’s estimate and any repairability opinion",
            "Photos of each slope and interior leaks",
            "Carrier’s roof report, diagram or aerial measurements",
            "Prior roof repair invoices or inspection reports",
        ],
        "faqs": [
            ("Can appraisal decide whether my roof gets fully replaced?", "Appraisal can decide the scope and cost of repairing covered damage, which often includes whether repair is feasible or replacement is required to restore the roof. It cannot override a coverage denial."),
            ("My policy pays my roof at actual cash value. Is appraisal still useful?", "It can be. Depreciation is part of the amount of loss, and appraisers can dispute both the replacement cost and how much depreciation was applied."),
            ("What changed with Florida roof claims in 2022?", "The reforms changed several roof-related rules, including allowing roof payment schedules on some policies and revising when partial damage triggers full replacement under code. Check your policy and consult an attorney for specifics."),
            ("Do you need to get on the roof?", "When it is safe, yes. Hands-on inspection gives better measurements and evidence than photos alone. We use other documentation where access is unsafe."),
        ],
        "related_tools": ["roof-measurement-calculator", "acv-depreciation-calculator"],
        "related_services": ["hurricane-claim-appraisal", "homeowners-claim-appraisal", "xactimate-estimate-review"],
    },
    # ------------------------------------------------------------------
    {
        "slug": "water-damage-claim-appraisal",
        "name": "Water Damage Claim Appraisal",
        "icon": "water",
        "short": "Appraisal for sudden plumbing, appliance and roof-leak water losses, covering mitigation, tear-out, drying and rebuild costs in Florida homes.",
        "title": "Water Damage Claim Appraisal in Florida",
        "description": "Florida water damage claim appraisal for burst pipes, appliance leaks and AC line failures. We value mitigation, tear-out and rebuild when estimates run low.",
        "h1": "Water Damage Claim Appraisal in Florida",
        "kicker": "Plumbing, appliance and leak losses",
        "lead": "A failed supply line or air handler pan can soak several rooms of a Florida home in hours. When the carrier accepts the claim but trims the drying invoice, cabinets or flooring, we use appraisal to settle the full cost of the covered loss.",
        "sections": [
            (
                "Sudden versus long-term leaks",
                '<p>Most homeowners policies cover sudden and accidental discharge of water and exclude damage from continuous or repeated seepage over an extended period. Many policy forms in Florida use a specific number of days in that exclusion. Whether a leak qualifies is a coverage question, not an appraisal question. Once the carrier has accepted the loss, though, the remaining argument is usually about scope and price, and that is where we come in.</p>',
            ),
            (
                "Mitigation invoices under scrutiny",
                '<p>Carriers frequently challenge water mitigation bills: the number of air movers and dehumidifiers, the number of drying days and the amount of material removed. Florida’s humidity makes drying slower than in many other states, and a slab-on-grade home with tile over concrete behaves differently from a raised wood floor. We review moisture logs and photo documentation to support reasonable equipment counts and durations.</p>'
                '<p>Some Florida policies also include a sublimit for emergency water mitigation unless the carrier approves more, so check your endorsements before assuming the full invoice is recoverable.</p>',
            ),
            (
                "Tear-out and the matching problem",
                '<p>Water losses almost always touch materials that run continuously through a home:</p>'
                '<ul><li>Tile or luxury vinyl plank that flows from the kitchen into living areas</li><li>Base cabinets where replacement doors and finishes no longer match the uppers</li><li>Countertops that crack when cabinets are removed</li><li>Baseboard, trim and paint across connected rooms</li></ul>'
                '<p>Florida law generally addresses matching for residential claims, so that repaired areas are reasonably uniform in appearance with adjacent areas. We document where a line stops naturally, such as a doorway or a change in material, and where it does not.</p>',
            ),
            (
                "Mold sublimits and hidden moisture",
                '<p>If water sat for even a few days in a closed wall cavity, mold may follow. Many Florida policies cap mold remediation at a modest sublimit, and some exclude it except where it results from a covered water loss. Appraisal can value remediation within the available limit, but it cannot expand the limit. We separate mold-related line items so they are evaluated against the right coverage.</p>',
            ),
            (
                "Living elsewhere during repairs",
                '<p>Kitchens and bathrooms are the rooms most often affected by water, and they are the rooms you cannot live without. If repairs displace your household, additional living expense coverage may reimburse reasonable extra costs. Keep every receipt. Florida Insurance Appraiser can help you organize ALE documentation as part of the overall loss presentation.</p>',
            ),
            (
                "Next steps",
                '<p>Before invoking appraisal, confirm the carrier has accepted coverage and compare its estimate with your contractor’s. Take our <a href="/claim-tools/appraisal-readiness-quiz/">appraisal readiness quiz</a> to see if your file is complete, and see the <a href="/claim-glossary/">claim glossary</a> for terms like “tear-out” and “sudden and accidental.” Florida Insurance Appraiser offers a free initial review. This page is general information, not legal advice.</p>',
            ),
            (
                "Contents and personal property in a water loss",
                '<p>Water rarely stops at the walls. Rugs, upholstered furniture, mattresses, electronics on the floor and items stored in lower cabinets are often ruined, and they are easy to forget once the drying crew has moved them into the garage. Photograph items before they are discarded, note brand and approximate age and keep a sample of anything a carrier may want to inspect. Contents values are part of the amount of loss and can be included in appraisal alongside the dwelling estimate, provided they fall within your personal property coverage.</p>',
            ),
        ],
        "checklist": [
            "Plumber’s or leak-detection report identifying the source",
            "Mitigation company invoice, moisture logs and drying photos",
            "Carrier estimate and any mitigation reduction letter",
            "Photos of flooring, cabinets and wall damage before tear-out",
            "Product details for flooring and cabinets, if known",
            "ALE receipts if you had to move out",
        ],
        "faqs": [
            ("Can appraisal help if my water claim was denied as long-term seepage?", "No. That is a coverage denial. Appraisal only applies once the carrier accepts that the loss is covered and the dispute is about the amount."),
            ("Will appraisal cover my whole mitigation bill?", "Appraisers determine the reasonable cost of mitigation, which may be more or less than the invoice. Policy sublimits on mitigation still apply."),
            ("What if only part of my flooring was wet?", "If the flooring is continuous and cannot be reasonably matched, the scope may extend beyond the wet area. That is a common appraisal issue we document carefully."),
            ("Is mold included in the appraisal?", "Mold remediation can be valued in appraisal, but only within whatever mold coverage and sublimit your policy provides."),
        ],
        "related_tools": ["appraisal-readiness-quiz", "contents-inventory-builder"],
        "related_services": ["homeowners-claim-appraisal", "condo-hoa-claim-appraisal", "xactimate-estimate-review"],
    },
    # ------------------------------------------------------------------
    {
        "slug": "sinkhole-claim-appraisal",
        "name": "Sinkhole Claim Appraisal",
        "icon": "sinkhole",
        "short": "Appraisal for accepted Florida sinkhole and ground-collapse claims, focused on repair scope, stabilization costs and above-ground damage.",
        "title": "Sinkhole Claim Appraisal in Florida",
        "description": "Florida sinkhole claim appraisal for accepted sinkhole and catastrophic ground cover collapse losses. We value stabilization and above-ground repair scope.",
        "h1": "Sinkhole Claim Appraisal in Florida",
        "kicker": "Subsurface and structural losses",
        "lead": "Sinkhole claims are concentrated in west-central Florida but can arise anywhere the limestone beneath us shifts. They involve engineering reports, specialized stabilization work and cosmetic repairs that carriers often value very differently from homeowners. We help with the amount-of-loss side of accepted claims.",
        "sections": [
            (
                "Sinkhole coverage versus catastrophic ground cover collapse",
                '<p>Florida treats these as two different things. Standard homeowners policies are generally required to include coverage for <strong>catastrophic ground cover collapse</strong>, which is a narrow definition: roughly, an abrupt collapse of the ground cover, a visible depression, structural damage to the building and condemnation of the structure. Broader <strong>sinkhole loss</strong> coverage, which can reach gradual settlement and cracking caused by sinkhole activity, is usually optional and purchased separately, often with its own deductible.</p>'
                '<p>Which coverage you have, and whether it applies, is a coverage question. Read your declarations page and endorsements carefully, and talk to an attorney if the carrier has denied the claim.</p>',
            ),
            (
                "Florida’s sinkhole-specific procedures",
                '<p>Florida has statutes specific to sinkhole claims that address testing, engineering reports and how repair payments are made. Policies commonly require that stabilization and foundation repairs follow the recommendations of a professional engineer, and payments may be tied to entering into a repair contract. Florida’s Department of Financial Services also offers a neutral evaluation program for certain sinkhole disputes, which can be an alternative or a complement to appraisal. We work within whatever framework your policy and current law set out.</p>',
            ),
            (
                "What appraisal can value in a sinkhole claim",
                '<p>Once a sinkhole loss is accepted, disagreements tend to cluster around:</p>'
                '<ul><li>The cost of the engineer-recommended subsurface work, such as grouting or underpinning</li><li>Above-ground repairs: wall cracks, slab cracking, doors and windows out of square, tile and drywall</li><li>How much interior finish work is needed after stabilization causes further movement</li><li>Pool deck, driveway and other structures</li><li>Temporary relocation costs during foundation work</li></ul>'
                '<p>We do not perform engineering or select stabilization methods. We price the scope that the engineering supports and challenge estimates that leave pieces out.</p>',
            ),
            (
                "Why above-ground damage gets underestimated",
                '<p>Carriers sometimes approach cosmetic repairs as simple patch-and-paint work. In practice, stabilization can move a structure again, re-opening cracks and stressing finishes. A credible estimate sequences cosmetic repairs after subsurface work and accounts for the realistic extent of drywall, tile and trim replacement. We also document cracks with measurements and dated photos so changes over time are visible.</p>',
            ),
            (
                "Where we see sinkhole claims",
                '<p>Hernando, Pasco and Hillsborough counties have historically seen many sinkhole claims, along with Marion, Citrus and Polk. Florida Insurance Appraiser assists homeowners throughout the region, including <a href="/florida-locations/tampa-fl/">Tampa</a> and <a href="/florida-locations/orlando-fl/">Orlando</a> area communities, as well as other parts of the state.</p>',
            ),
            (
                "Getting started",
                '<p>Send us the engineering report, the carrier’s estimate and your contractor’s numbers. We will tell you plainly whether the dispute looks like an amount-of-loss issue that appraisal can address, or a coverage issue that needs a lawyer. Florida Insurance Appraiser does not provide legal advice, and nothing on this page should be read as such. For an overview of the full sequence, see the <a href="/appraisal-process/">appraisal process</a>.</p>',
            ),
            (
                "Documenting movement over time",
                '<p>Sinkhole claims can stretch over long periods while testing, engineering and repair contracting play out. During that time, cracks may widen and new ones may appear. We recommend keeping a simple log: date, location, crack width measured with a crack gauge or ruler, and a photo with a reference object in frame. That record helps separate pre-existing settlement from sinkhole-related movement and gives both appraisers a shared factual baseline when they sit down to compare estimates.</p>',
            ),
        ],
        "checklist": [
            "Declarations page showing sinkhole or catastrophic ground cover collapse coverage",
            "Engineering and geological testing reports",
            "Carrier’s estimate and any repair contract requirements",
            "Dated crack photos and measurements over time",
            "Foundation repair contractor proposals",
            "Prior inspection or repair records for the home",
        ],
        "faqs": [
            ("Is sinkhole damage covered by a standard Florida homeowners policy?", "Standard policies generally must cover catastrophic ground cover collapse, which is narrowly defined. Broader sinkhole loss coverage is typically optional. Check your declarations page."),
            ("Can appraisal decide whether a sinkhole caused my cracks?", "No. Causation and coverage are not decided in appraisal. Appraisal values an accepted loss."),
            ("Do you recommend grouting or underpinning?", "No. Stabilization methods are an engineering decision. We value the scope that the engineering report supports."),
            ("Is there a state program for sinkhole disputes?", "Florida’s Department of Financial Services has offered a neutral evaluation program for certain sinkhole claims. Check with DFS for current eligibility and procedures."),
        ],
        "related_tools": ["appraisal-worth-it-calculator", "claim-deadline-calculator"],
        "related_services": ["homeowners-claim-appraisal", "umpire-services"],
    },
    # ------------------------------------------------------------------
    {
        "slug": "fire-smoke-claim-appraisal",
        "name": "Fire & Smoke Claim Appraisal",
        "icon": "fire",
        "short": "Appraisal for fire, smoke and soot losses, covering structural rebuild, cleaning versus replacement, contents and additional living expenses.",
        "title": "Fire and Smoke Damage Claim Appraisal in Florida",
        "description": "Fire and smoke claim appraisal for Florida homes and businesses. We value rebuild scope, soot cleaning versus replacement, contents and living expenses.",
        "h1": "Fire and Smoke Damage Claim Appraisal",
        "kicker": "Rebuild, cleaning and contents",
        "lead": "Fire claims are rarely just about the room that burned. Smoke and soot travel through HVAC systems, attics and wall cavities, and the argument with the carrier is often about how far the damage really extends. We help Florida policyholders settle that through appraisal.",
        "sections": [
            (
                "Clean, seal or replace?",
                '<p>The biggest dollar swing in many fire claims is the decision between cleaning and replacing. Carriers lean toward cleaning and sealing drywall, framing and contents; homeowners often find that odor persists after cleaning. Appraisal is a reasonable forum for this argument when the evidence supports it: soot testing results, photos of residue in unaffected-looking rooms and documentation of odor that survived an initial cleaning attempt.</p>',
            ),
            (
                "Structural rebuild scope",
                '<p>After a significant fire, the structure may need partial or full reconstruction. That brings in items carrier estimates sometimes leave thin:</p>'
                '<ul><li>Demolition and debris removal, including disposal fees</li><li>Engineering for fire-weakened framing or trusses</li><li>Electrical rewiring, which often must meet current code</li><li>Full HVAC cleaning or replacement of ductwork</li><li>Permits and inspections</li><li>General contractor overhead and profit for multi-trade work</li></ul>',
            ),
            (
                "Ordinance or law and code upgrades",
                '<p>When a substantially damaged Florida home is rebuilt, local building departments generally require the new work to meet current code. That can mean upgraded windows and doors in wind-borne debris regions, roof-to-wall connections, electrical panels and more. Many policies include ordinance or law coverage, often as a percentage of Coverage A, to pay for these upgrades. We identify code-driven line items separately so they are valued against the right coverage.</p>',
            ),
            (
                "Contents after a fire",
                '<p>Contents claims after a fire can include hundreds or thousands of items, many of them smoke-damaged rather than burned. A complete, room-by-room inventory with replacement costs and approximate ages is the foundation of any contents appraisal. Start with our <a href="/claim-tools/contents-inventory-builder/">contents inventory builder</a>, and check the carrier’s depreciation with the <a href="/claim-tools/acv-depreciation-calculator/">ACV depreciation calculator</a>.</p>',
            ),
            (
                "Additional living expense for a long rebuild",
                '<p>Fire rebuilds in Florida can take many months, especially when permits and contractor availability are tight. Additional living expense coverage may pay for reasonable rent, mileage and other increased costs while you are out of the home, subject to policy limits and time limits. Florida Insurance Appraiser can help document ALE as part of the overall amount of loss.</p>',
            ),
            (
                "Commercial fire losses",
                '<p>For businesses, a fire claim also raises business income and extra expense questions, plus tenant improvements and equipment. See our <a href="/appraisal-services/commercial-claim-appraisal/">commercial claim appraisal</a> page for how we approach those. As always, appraisal decides the amount of loss and does not resolve coverage disputes such as cause-of-fire or vacancy issues. Florida Insurance Appraiser provides general information here, not legal advice.</p>',
            ),
            (
                "Protecting the property after a fire",
                '<p>Most policies require you to take reasonable steps to prevent further damage after a loss. In Florida, an open roof or broken windows invite rain within days, which can turn a fire claim into a fire and water claim. Board-up, tarping and temporary fencing costs are usually part of the claim, so keep the invoices. Avoid discarding damaged materials before they are documented, because the carrier’s adjuster and the appraisers may need to see them to agree on scope.</p>',
            ),
        ],
        "checklist": [
            "Fire department incident report number",
            "Carrier estimate, contents valuation and payment letters",
            "Photos of every room, including those with only smoke damage",
            "Soot or air quality testing results, if any",
            "Room-by-room contents inventory",
            "Rental, hotel and mileage receipts while displaced",
        ],
        "faqs": [
            ("Can appraisal resolve a dispute about whether smoke-damaged items should be replaced?", "Yes, if the carrier has accepted the loss. Whether an item can be restored by cleaning or must be replaced is a valuation question appraisers commonly address."),
            ("Does appraisal cover code upgrades after a fire?", "Appraisers can value code-required work, but whether and how much is paid depends on your ordinance or law coverage and its limit."),
            ("What if the carrier is investigating the cause of the fire?", "Cause and coverage investigations are outside appraisal. Appraisal applies to the amount of a covered loss."),
            ("Can contents be included in the appraisal?", "Yes. Contents can be part of the amount of loss, and a detailed inventory makes that portion much stronger."),
        ],
        "related_tools": ["contents-inventory-builder", "acv-depreciation-calculator"],
        "related_services": ["homeowners-claim-appraisal", "commercial-claim-appraisal", "xactimate-estimate-review"],
    },
    # ------------------------------------------------------------------
    {
        "slug": "condo-hoa-claim-appraisal",
        "name": "Condo & HOA Claim Appraisal",
        "icon": "building",
        "short": "Appraisal for Florida condominium associations, HOAs and unit owners, covering master policies, common elements and unit interiors.",
        "title": "Condo and HOA Claim Appraisal in Florida",
        "description": "Condo and HOA claim appraisal in Florida for associations and unit owners. We value master policy losses, common elements and unit interior damage.",
        "h1": "Condo and HOA Claim Appraisal in Florida",
        "kicker": "Associations and unit owners",
        "lead": "Florida condominium claims involve at least two policies, a board, a management company and often dozens of unit owners. We help associations and individual owners resolve amount-of-loss disputes on master policies and HO-6 unit policies.",
        "sections": [
            (
                "Who insures what in a Florida condo",
                '<p>Florida’s condominium statute and your association’s declaration together divide responsibility. Broadly, the association’s master policy covers the building structure and common elements, while the unit owner’s HO-6 policy covers personal property and certain interior items. Florida law generally excludes items like floor, wall and ceiling coverings, cabinets, countertops and fixtures inside a unit from the association’s insurance obligation, but declarations and older condo documents can vary. Getting this split right is the first step in any condo claim.</p>',
            ),
            (
                "Master policy losses for associations",
                '<p>Association claims after a hurricane or major water event can reach across multiple buildings and dozens of roofs, balconies and stairwells. The disputes tend to involve:</p>'
                '<ul><li>Roof systems across multiple buildings, often with different ages and materials</li><li>Exterior walls, stucco, balconies and railings</li><li>Windows and sliding doors where they are association responsibility</li><li>Elevators, mechanical rooms and common-area finishes</li><li>Code upgrades triggered by the extent of repairs</li><li>Building-wide hurricane deductibles, which for large associations can be substantial</li></ul>'
                '<p>Florida Insurance Appraiser organizes these claims building by building so each component is priced and tracked.</p>',
            ),
            (
                "The 2022 condo safety law context",
                '<p>After the Surfside collapse, Florida enacted condo safety legislation in 2022 that introduced milestone structural inspections for certain buildings and structural integrity reserve study requirements. These rules are not insurance coverage provisions, and they do not make an insurer pay for deferred maintenance. They do mean associations are producing more engineering documentation, which can be useful in separating pre-existing conditions from new storm damage during an appraisal.</p>',
            ),
            (
                "Unit owner claims under HO-6 policies",
                '<p>Individual owners often find themselves caught between their own carrier and the association’s. A leak from the unit above, for example, may involve the upstairs owner’s policy, your HO-6 and the master policy depending on the source and the materials damaged. We help unit owners value their portion, including interior finishes, contents and loss assessment exposure if the association passes along part of its deductible or a shortfall.</p>',
            ),
            (
                "Board approval and authority",
                '<p>For association claims, invoking appraisal is a board decision that should follow the association’s governing documents and Florida’s condominium or HOA statutes. Boards typically want a clear explanation of the dispute, the fee structure and how appraisal interacts with any other professionals on the claim. We are happy to present to a board, and we coordinate with association counsel when one is involved. We are not attorneys and do not give legal advice.</p>',
            ),
            (
                "Phasing repairs across a community",
                '<p>Large associations rarely repair every building at once. Contractors may phase work over months, and pricing can shift between phases. An appraisal estimate should reflect a realistic construction schedule, including mobilization for each phase, protection of occupied units and access constraints such as elevator use and parking. We also track which units have interior damage tied to common-element failures, so the association and unit owners each know which portion of the loss falls on which policy.</p>',
            ),
            (
                "Coastal and high-rise experience",
                '<p>Much of Florida’s condo inventory sits along the coast, from <a href="/florida-locations/miami-fl/">Miami</a> and <a href="/florida-locations/naples-fl/">Naples</a> to Clearwater and Destin. See our <a href="/claim-tools/hurricane-deductible-calculator/">hurricane deductible calculator</a> for a sense of how percentage deductibles scale on large insured values. Florida Insurance Appraiser can assist associations of many sizes, from small villa HOAs to large condominium communities.</p>',
            ),
        ],
        "checklist": [
            "Association declaration and insurance responsibility provisions",
            "Master policy declarations, including hurricane deductible",
            "HO-6 unit policy, if you are a unit owner",
            "Milestone inspection or reserve study reports, if available",
            "Board minutes authorizing the claim or appraisal",
            "Carrier estimates for each building or unit",
        ],
        "faqs": [
            ("Can a unit owner invoke appraisal on the master policy?", "Generally the association, as the named insured, controls the master policy claim. Unit owners can typically invoke appraisal on their own HO-6 policies."),
            ("Does the 2022 condo safety law change what insurance pays?", "Not directly. It added inspection and reserve requirements. Coverage is still governed by the policy, though engineering reports can help document the condition of the building."),
            ("Who pays the master policy hurricane deductible?", "The association typically bears it, and it may be funded by reserves or assessments. Unit owners may have loss assessment coverage under their HO-6 policies."),
            ("Do you work with association attorneys?", "Yes. We focus on valuation and coordinate with counsel, who handles legal and coverage questions."),
        ],
        "related_tools": ["hurricane-deductible-calculator", "appraisal-readiness-quiz"],
        "related_services": ["hurricane-claim-appraisal", "commercial-claim-appraisal", "water-damage-claim-appraisal"],
    },
    # ------------------------------------------------------------------
    {
        "slug": "commercial-claim-appraisal",
        "name": "Commercial Claim Appraisal",
        "icon": "briefcase",
        "short": "Appraisal for Florida commercial property claims, including retail, office, warehouse, hospitality and multifamily buildings and their contents.",
        "title": "Commercial Property Claim Appraisal in Florida",
        "description": "Commercial property claim appraisal in Florida for offices, retail, warehouses, hotels and multifamily. We value building, equipment and business income loss.",
        "h1": "Commercial Property Claim Appraisal in Florida",
        "kicker": "Business and investment property",
        "lead": "Commercial losses bring larger numbers, more complex policies and the pressure of a business that needs to reopen. We act as the insured’s appraiser on amount-of-loss disputes for Florida commercial properties.",
        "sections": [
            (
                "Commercial policies are not homeowners policies",
                '<p>Commercial property forms are written differently. Many include coinsurance clauses, blanket or scheduled limits, agreed value endorsements, separate wind deductibles and specific valuation provisions. Appraisal clauses appear in most of them, but the wording, deadlines and fee terms vary widely. We start every commercial engagement by reading the policy form and endorsements in full.</p>',
            ),
            (
                "Property types we work on",
                '<ul><li>Strip centers and freestanding retail</li><li>Office buildings and medical office space</li><li>Warehouses, flex space and light industrial</li><li>Hotels and short-term rental properties</li><li>Apartment complexes and other multifamily buildings</li><li>Churches, schools and nonprofit facilities</li></ul>'
                '<p>Each property type has its own common damage patterns. Large-format warehouse roofs fail differently from a hotel’s mechanical systems, and a strip center’s tenant improvements raise questions about who insured what.</p>',
            ),
            (
                "Building, equipment and tenant improvements",
                '<p>The building estimate on a commercial loss often involves roofing systems like modified bitumen, TPO or standing seam metal, along with storefront glazing, rooftop HVAC units and fire suppression. Tenant improvements and betterments may be covered under the tenant’s policy, the landlord’s policy or both, depending on the lease. We separate these components clearly so each is valued against the right coverage.</p>',
            ),
            (
                "Business income and extra expense",
                '<p>Lost income during the period of restoration is often a major part of a commercial claim. Whether business income loss can be decided in appraisal depends on the policy language and, in some cases, on how courts interpret it. Where it is within the scope of appraisal, the analysis typically relies on financial records, a realistic restoration timeline and documentation of extra expenses incurred to keep operating. We work alongside forensic accountants when the claim calls for one.</p>',
            ),
            (
                "Coinsurance and valuation traps",
                '<p>A coinsurance penalty can reduce a payment if the property was underinsured relative to its value at the time of loss. Valuation disputes can also arise over replacement cost versus actual cash value and how depreciation is calculated on commercial components. Because these issues interact with the amount of loss, they deserve attention early. Florida Insurance Appraiser will flag them, but coverage interpretation itself is a matter for your broker or attorney.</p>',
            ),
            (
                "Keeping the business running during the claim",
                '<p>Commercial owners cannot wait for an appraisal award to start mitigation or temporary repairs. Policies generally expect you to protect the property and reduce the loss, and reasonable extra expenses to keep operating may themselves be covered. Track every temporary measure with invoices and photos: generators, temporary roofing, security, relocated inventory, rented equipment. That documentation supports both the building estimate and any extra expense portion of the claim, and it keeps the appraisal focused on verifiable costs.</p>',
            ),
            (
                "How we run a commercial appraisal",
                '<p>Commercial appraisals usually require multiple site visits, coordination with property managers and contractors and a detailed, organized estimate. We frequently use <a href="/appraisal-services/xactimate-estimate-review/">Xactimate estimate review</a> to break down a carrier’s numbers before negotiating. If the appraisers cannot agree, the umpire decides remaining items, and our <a href="/appraisal-services/umpire-services/">umpire services</a> page explains that role. We serve commercial owners statewide, including <a href="/florida-locations/jacksonville-fl/">Jacksonville</a> and South Florida. Florida Insurance Appraiser provides general information here, not legal advice.</p>',
            ),
        ],
        "checklist": [
            "Complete commercial policy with all forms and endorsements",
            "Statement of values or schedule of locations",
            "Leases showing tenant improvement and insurance responsibilities",
            "Carrier estimates, reports and payment history",
            "Contractor bids and equipment replacement quotes",
            "Financial statements for any business income claim",
        ],
        "faqs": [
            ("Can business income losses be appraised?", "It depends on the policy language. Some forms clearly allow it, others are ambiguous. We review your policy and coordinate with your attorney or broker on that question."),
            ("Do you handle multifamily properties?", "Yes. Apartment complexes and other multifamily buildings are part of our commercial work, and condo associations are covered on our condo and HOA page."),
            ("What is a coinsurance penalty?", "A reduction in payment that can apply if the property was insured for less than the required percentage of its value. It is a policy condition, so review it with your broker or attorney."),
            ("How long do commercial appraisals take?", "Larger and more complex losses generally take longer, especially if an umpire is needed. We cannot promise a specific timeline."),
        ],
        "related_tools": ["appraisal-worth-it-calculator", "claim-deadline-calculator", "acv-depreciation-calculator"],
        "related_services": ["condo-hoa-claim-appraisal", "xactimate-estimate-review", "umpire-services"],
    },
    # ------------------------------------------------------------------
    {
        "slug": "umpire-services",
        "name": "Umpire Services",
        "icon": "scale",
        "short": "Neutral umpire services for Florida property insurance appraisals when two appraisers cannot agree on the amount of loss.",
        "title": "Insurance Appraisal Umpire Services in Florida",
        "description": "Neutral umpire services for Florida property insurance appraisals. When two appraisers cannot agree, the umpire reviews the disputed items and joins an award.",
        "h1": "Appraisal Umpire Services in Florida",
        "kicker": "Neutral resolution of disputed items",
        "lead": "When two appraisers cannot agree on every item, the appraisal clause calls for an umpire. We can serve as a neutral umpire on Florida residential and commercial appraisals when selected by both appraisers or appointed by a court.",
        "sections": [
            (
                "What the umpire does",
                '<p>The umpire’s job is limited and specific: review the items on which the two appraisers disagree and join with one of them in a written award. The umpire does not represent either side, does not advocate and does not decide coverage. In most appraisals, the appraisers resolve many items themselves and bring only a short list of disputed line items to the umpire.</p>'
                '<p>The umpire is a separate role from the party appraisers. When Florida Insurance Appraiser serves as umpire on a claim, we do not also act as appraiser for either side on that claim.</p>',
            ),
            (
                "How an umpire is selected",
                '<p>Most Florida policies direct the two appraisers to agree on an umpire. If they cannot agree within the time the policy provides, either party can generally ask a court of competent jurisdiction to appoint one. Appraisers often exchange a few candidate names and settle on someone both consider qualified and impartial. Your policy’s appraisal provision controls the specifics.</p>',
            ),
            (
                "Our umpire process",
                '<ol><li><strong>Engagement and disclosures.</strong> We confirm we have no conflicts and disclose any prior relationships with either appraiser or party.</li><li><strong>Submissions.</strong> Each appraiser provides an estimate and a list of disputed items with supporting documentation.</li><li><strong>Inspection.</strong> We inspect the property, usually with both appraisers present, focused on the disputed items.</li><li><strong>Review.</strong> We evaluate the evidence for each disputed line: measurements, pricing, scope and depreciation.</li><li><strong>Award.</strong> We prepare an award for signature, typically itemized so both sides can see how each issue was resolved.</li></ol>',
            ),
            (
                "Neutrality in practice",
                '<p>An umpire’s value depends on being genuinely independent. That means equal communication with both appraisers, no private conversations about disputed issues with one side and no stake in the outcome. We document the umpire process so the parties can see how decisions were reached. Fees are typically shared between the parties under the policy’s terms, not paid by one side alone.</p>',
            ),
            (
                "Items umpires commonly decide",
                '<ul><li>Repair versus replacement on roofs and flooring</li><li>Matching where materials are discontinued</li><li>Unit pricing for labor and materials in the local market</li><li>Whether overhead and profit is warranted</li><li>Depreciation rates and actual cash value</li><li>Code-required upgrades under ordinance or law coverage</li></ul>'
                '<p>Definitions for many of these terms are in our <a href="/claim-glossary/">claim glossary</a>.</p>',
            ),
            (
                "Requesting an umpire",
                '<p>Appraisers or attorneys who would like to propose Florida Insurance Appraiser as umpire can contact us with the claim details for a conflict check. Policyholders who are earlier in the process may want to start with the <a href="/appraisal-process/">appraisal process</a> overview. This page is general information, not legal advice.</p>',
            ),
            (
                "What makes umpire submissions effective",
                '<p>From the umpire’s chair, the most useful submissions are short and specific. A disputed item list that names the line, both appraisers’ figures and the reason for the difference lets the umpire focus on the real question. Supporting evidence such as supplier quotes, manufacturer discontinuation notices, measurement photos and local labor rates carries more weight than general argument. We encourage both appraisers to narrow the list as far as possible before umpire review, since agreed items do not need a decision.</p>',
            ),
        ],
        "checklist": [
            "Names of both appraisers and their contact information",
            "Copy of the policy’s appraisal provision",
            "Both appraisers’ estimates",
            "A list of agreed items and disputed items",
            "Supporting photos, reports and pricing documentation",
        ],
        "faqs": [
            ("Can the same firm be my appraiser and the umpire?", "No. The umpire must be neutral. If we serve as umpire on a claim, we do not act as appraiser for either party on that claim."),
            ("What happens if the appraisers cannot agree on an umpire?", "Most policies allow either party to ask a court to appoint one. Check your policy’s appraisal provision for the exact procedure."),
            ("Does the umpire decide coverage?", "No. The umpire, like the appraisers, decides the amount of loss on disputed items. Coverage questions remain with the parties and the courts."),
            ("Who pays the umpire?", "Policies commonly split the umpire’s fee equally between the insured and the insurer. Your policy language controls."),
        ],
        "related_tools": ["appraisal-readiness-quiz", "appraisal-worth-it-calculator"],
        "related_services": ["homeowners-claim-appraisal", "commercial-claim-appraisal", "xactimate-estimate-review"],
    },
    # ------------------------------------------------------------------
    {
        "slug": "xactimate-estimate-review",
        "name": "Xactimate Estimate Review",
        "icon": "file",
        "short": "Line-by-line review of your insurer’s Xactimate estimate to find missing scope, pricing gaps, depreciation errors and omitted O&P.",
        "title": "Xactimate Estimate Review for Florida Claims",
        "description": "Line-by-line Xactimate estimate review for Florida property claims. We flag missing scope, pricing gaps, depreciation errors and omitted overhead and profit.",
        "h1": "Xactimate Estimate Review for Florida Property Claims",
        "kicker": "Line-by-line estimate analysis",
        "lead": "Most Florida carriers write their estimates in Xactimate, and the numbers can look final and authoritative. They are not. We review the estimate line by line to show you exactly where it may fall short before you decide whether appraisal makes sense.",
        "sections": [
            (
                "Why the estimate deserves a second look",
                '<p>An Xactimate estimate is only as good as the scope, measurements and selections the adjuster entered. The software applies regional price lists, but it does not know that your kitchen tile runs into the hallway, that your roof has three layers of shingles or that a contractor in your area cannot do the job for the listed price. A careful review often shows the real dispute is not about the software at all, but about what was left out.</p>',
            ),
            (
                "What we look for",
                '<ul><li><strong>Missing line items</strong> such as detach-and-reset, content manipulation, protection and cleanup</li><li><strong>Quantities</strong> that do not match field measurements</li><li><strong>Wrong line codes</strong> that price a lower grade of material than what was installed</li><li><strong>Price list and date</strong> that may not reflect current local conditions, especially after a major storm</li><li><strong>Depreciation</strong> applied to labor or at rates inconsistent with condition</li><li><strong>Overhead and profit</strong> omitted where a general contractor is reasonably needed</li><li><strong>Code items</strong> that belong under ordinance or law coverage</li></ul>',
            ),
            (
                "Overhead and profit on Florida claims",
                '<p>General contractors charge overhead and profit to coordinate trades, carry insurance and stand behind the work. Carriers sometimes leave it off, particularly on claims that involve only a few trades. Whether O&amp;P is warranted depends on the complexity of the job, not a fixed number of trades. We look at the actual scope and explain whether a general contractor would reasonably be needed.</p>',
            ),
            (
                "Reading depreciation correctly",
                '<p>Replacement cost policies typically pay actual cash value first and release recoverable depreciation after repairs are completed, subject to policy conditions. Roof payment schedules and ACV endorsements, which became more common after Florida’s 2022 reforms, can make some depreciation non-recoverable. We check whether the depreciation in the estimate is reasonable and whether it is labeled correctly. Use our <a href="/claim-tools/acv-depreciation-calculator/">ACV depreciation calculator</a> to test a few line items yourself.</p>',
            ),
            (
                "What you receive",
                '<p>Florida Insurance Appraiser provides a written summary that groups findings by category, flags the items with the most dollar impact and notes where more documentation would help. Where appropriate, we prepare a competing estimate in the same format so the comparison is apples to apples. The review stands on its own: you can use it to request a supplement from your carrier, take it to DFS mediation or use it as the starting point for appraisal.</p>',
            ),
            (
                "When a review is the right first step",
                '<p>If you are unsure whether your claim is truly underpaid, an estimate review costs less than a full appraisal and gives you facts to work with. Our guide on <a href="/blog/what-to-do-when-a-florida-claim-is-underpaid/">what to do when a Florida claim is underpaid</a> lays out the options. Florida Insurance Appraiser does not negotiate claims as a public adjuster and does not give legal advice; the review is an independent valuation opinion.</p>',
            ),
            (
                "Common Xactimate line items worth checking",
                '<table><thead><tr><th>Item</th><th>What to check</th></tr></thead><tbody><tr><td>Content manipulation</td><td>Moving furniture out of rooms before flooring or paint work</td></tr><tr><td>Detach and reset</td><td>Appliances, toilets, vanities, gutters and solar panels that must come off for repairs</td></tr><tr><td>Floor protection and masking</td><td>Protecting finished surfaces in occupied homes</td></tr><tr><td>Paint scope</td><td>Full walls or full rooms rather than isolated patches</td></tr><tr><td>Permits and fees</td><td>Required by most Florida building departments for roof and structural work</td></tr><tr><td>Dumpster and haul-off</td><td>Debris volume consistent with the tear-out scope</td></tr></tbody></table>',
            ),
        ],
        "checklist": [
            "The carrier’s full estimate, ideally the PDF with all pages",
            "Any roof diagram or sketch attached to the estimate",
            "Payment letters showing ACV paid and depreciation held back",
            "Your contractor’s estimate, if you have one",
            "Photos of the damaged areas",
            "Your policy’s declarations page and endorsements",
        ],
        "faqs": [
            ("Do I need to be in appraisal to get an estimate review?", "No. Many clients use a review to decide whether appraisal is worthwhile, to request a supplement or to prepare for mediation."),
            ("Is Xactimate pricing always accurate for my area?", "Xactimate uses regional price lists, but conditions change, particularly after storms. Pricing should be checked against current local costs."),
            ("Can you review a commercial estimate?", "Yes. We review residential and commercial estimates, including large-loss estimates with multiple buildings."),
            ("Will the review guarantee a higher payment?", "No. A review identifies potential gaps and supports your position with documentation, but no outcome can be guaranteed."),
        ],
        "related_tools": ["acv-depreciation-calculator", "appraisal-worth-it-calculator", "roof-measurement-calculator"],
        "related_services": ["homeowners-claim-appraisal", "roof-claim-appraisal", "commercial-claim-appraisal"],
    },
]
