"""Copy for the free claim tools. Widget markup lives in tools.py, logic in static/assets/js/app.js."""

TOOL_COPY = {
    "appraisal-payoff-estimator": {
        "name": "Appraisal Payoff Estimator",
        "kind": "Estimator",
        "keyword": "appraisal payoff estimator",
        "short": "Compare the carrier’s estimate to yours, weigh appraisal costs and see the net increase you might keep.",
        "title": "Appraisal Payoff Estimator | Is Appraisal Worth It?",
        "desc": "Free appraisal payoff estimator: compare two estimates, test where an award may land, subtract fees and find your break-even point before you demand.",
        "h1": "Kentucky Appraisal Payoff Estimator for Disputed Claims",
        "lede": "Before you invoke the appraisal clause, test whether the gap between the two estimates is big enough to cover what appraisal costs. Everything runs in your browser and nothing is stored.",
        "explain": """<h2>How to use the estimator</h2>
<p>Enter the insurer’s replacement cost value (RCV) estimate and your own estimate, whether that is a contractor bid or an independent line-item estimate. The difference between them is the <strong>disputed amount</strong>. Then move the slider to guess where an award might land inside that gap: 0% means the award matches the carrier’s number, 100% means it matches yours. Finally, enter your appraiser’s fee as a flat dollar figure or as a percentage of the increase, and tick the umpire box if you want to include your half of an umpire’s fee.</p>
<h2>The math in plain words</h2>
<p>The projected award is the carrier’s estimate plus your chosen share of the gap. The gross increase is the projected award minus the carrier’s estimate. Costs are your appraiser’s fee plus, if selected, half the umpire’s fee, since most policies have each side pay its own appraiser and split the umpire. The net increase is the gross increase minus those costs.</p>
<p>The <strong>break-even landing %</strong> is the most useful number on the page. It is the smallest share of the gap the award must reach before your costs are covered. If break-even is 15%, the award only has to move a little toward your number for appraisal to pay for itself. If it is 70%, you need a strong, well-documented estimate to come out ahead.</p>
<h3>An illustrative example</h3>
<p>Illustrative figures only: the carrier estimates $18,000 and your contractor estimates $30,000, a $12,000 gap. With a $2,500 flat appraiser fee and a $1,000 share of the umpire, costs are $3,500, so break-even is about 29% of the gap. An award landing halfway would produce a $6,000 gross increase and a $2,500 net increase.</p>
<h2>What the result does and doesn’t mean</h2>
<p>The slider is your assumption, not a prediction. No calculator can tell you how a panel will weigh the evidence, and the result is not a promise of any outcome. It also ignores deductibles, depreciation holdback and prior payments, which change what actually reaches you. Use the <a href="/appraisal-calculators/rcv-acv-holdback-calculator/">RCV &amp; ACV holdback calculator</a> for that side of the picture.</p>
<h2>Kentucky context</h2>
<p>Appraisal under a Kentucky property policy settles the amount of loss, not coverage. If the insurer has denied the claim or says an exclusion applies, the payoff math here may not matter, and a Kentucky attorney is the right first call. If the dispute really is about price, a second set of eyes on the carrier’s estimate often tightens your number before you commit. Our <a href="/insurance-appraisal/second-look-estimate-review/">second-look estimate review</a> is built for exactly that step.</p>""",
        "faqs": [
            ("What does the break-even landing percentage tell me?", "It is the minimum share of the gap between the two estimates that the award has to reach before your appraisal costs are paid back. Below that point, appraisal would cost more than it adds."),
            ("Does the estimator know how appraisal panels usually rule?", "No. The landing slider is your own assumption. The tool does arithmetic on the figures you enter and does not predict any outcome."),
            ("Is my claim information saved anywhere?", "No. The calculation runs entirely in your browser, and nothing you type is sent to us or stored."),
        ],
    },
    "rcv-acv-holdback-calculator": {
        "name": "RCV & ACV Holdback Calculator",
        "kind": "Calculator",
        "keyword": "RCV and ACV holdback calculator",
        "short": "Estimate your first ACV check, the depreciation held back and what you can recover after repairs.",
        "title": "RCV and ACV Holdback Calculator for Claims",
        "desc": "RCV and ACV holdback calculator: estimate depreciation by item age and life, your first actual cash value check and what is released after repairs.",
        "h1": "Use an RCV and ACV Holdback Calculator on Your Claim",
        "lede": "See how depreciation splits a replacement cost claim into a first actual cash value check and a holdback you may recover later. Everything runs in your browser and nothing is stored.",
        "explain": """<h2>How to use the calculator</h2>
<p>Add one row for each damaged item or building component: a roof, siding, flooring, a water heater. For each row enter the replacement cost, its age in years and its expected useful life. Set a depreciation cap if you want to limit how far any single item can be depreciated, enter your deductible, and choose whether your policy pays replacement cost or <strong>ACV only</strong>. The “repairs completed” toggle shows what changes once the work is done and documented.</p>
<h2>The math in plain words</h2>
<p>The tool uses straight-line depreciation: age divided by expected life, multiplied by the replacement cost, and capped at the limit you set. A 10-year-old roof with a 25-year life is depreciated 40%. Actual cash value (ACV) is replacement cost minus depreciation.</p>
<ul>
<li><strong>First ACV check:</strong> total ACV minus the deductible.</li>
<li><strong>Depreciation held back:</strong> total depreciation the insurer withholds until repairs are done.</li>
<li><strong>Released after repairs:</strong> the holdback paid once you show the work is complete, if your policy pays replacement cost.</li>
<li><strong>Total if fully recovered:</strong> replacement cost minus the deductible.</li>
</ul>
<p>On an ACV-only policy the holdback is never released, so the first check is the whole payment.</p>
<h3>An illustrative example</h3>
<p>Illustrative figures only: a $20,000 roof that is 10 years into a 25-year life carries $8,000 of depreciation. With a $1,000 deductible, the first check is $11,000, $8,000 is held back, and the total after repairs is $19,000.</p>
<h2>What the result does and doesn’t mean</h2>
<p>Insurers don’t all depreciate the same way. Some depreciate labor, some only materials; some use condition rather than age; some items are not depreciated at all. Your estimate may also include overhead and profit or code upgrades that this simple model leaves out. Treat the output as a way to understand the structure of your payments, not as the number your carrier must pay.</p>
<h2>Kentucky context</h2>
<p>Most replacement cost policies set a window to complete repairs or notify the insurer that you intend to claim the holdback, and that window varies by form. After a big Kentucky hail or wind event, contractor backlogs can push repairs past it, so read your policy and put the date on your calendar with the <a href="/appraisal-calculators/claim-timeline-builder/">claim timeline builder</a>. When depreciation itself is the disagreement, for example an unreasonable age or condition on a roof, that pricing question can be part of a <a href="/insurance-appraisal/home-insurance-appraisal/">homeowners insurance appraisal</a>.</p>""",
        "faqs": [
            ("What is recoverable depreciation?", "It is the part of a replacement cost claim the insurer holds back until repairs or replacement are completed. Once you document the work within the policy’s window, the holdback is typically released."),
            ("Why does my insurer depreciate differently than this calculator?", "Carriers use different methods, such as condition-based depreciation or depreciating materials but not labor. This tool uses simple straight-line depreciation with a cap so you can see the structure."),
            ("Does the calculator store my figures?", "No. All math runs in your browser and nothing is saved or sent anywhere."),
        ],
    },
    "roof-measurement-calculator": {
        "name": "Roof Measurement Calculator",
        "kind": "Calculator",
        "keyword": "roof measurement calculator",
        "short": "Turn a footprint and pitch into roofing squares, add waste and compare against the carrier’s count.",
        "title": "Roof Measurement Calculator | Squares, Pitch, Waste",
        "desc": "Roof measurement calculator: convert footprint and pitch to squares with waste and bundles, then compare your count to the carrier’s estimate.",
        "h1": "Check the Carrier’s Squares With a Roof Measurement Calculator",
        "lede": "Estimate roof surface area, squares and bundles from a simple footprint, then see how your count compares with the insurer’s. Everything runs in your browser and nothing is stored.",
        "explain": """<h2>How to use the calculator</h2>
<p>Enter the building footprint length and width plus the overhang at the eaves and rakes, or type in a known flat area if you already have one. Pick the roof pitch, such as 6/12, and a waste factor. Add a price per square if you want a rough cost. Then enter the number of squares shown on the carrier’s estimate to see the difference in squares and as a percentage.</p>
<h2>The math in plain words</h2>
<p>The flat area is (length plus two overhangs) times (width plus two overhangs). A sloped roof has more surface than its footprint, so the flat area is multiplied by a <strong>pitch multiplier</strong>. A 6/12 roof uses about 1.118; a 12/12 roof uses about 1.414. That gives the surface area. One roofing square is 100 square feet, so squares are surface area divided by 100. Waste for cuts at hips, valleys and starter courses is added as a percentage, and most architectural shingles come three bundles to a square.</p>
<h3>An illustrative example</h3>
<p>Illustrative figures only: a 50 by 30 foot footprint with 1-foot overhangs is 52 by 32, or 1,664 square feet flat. At 6/12 that becomes about 1,860 square feet, or 18.6 squares. With 10% waste you would order about 20.5 squares, or 62 bundles. If the carrier lists 17 squares, the gap is roughly 3.5 squares, about 20%.</p>
<h2>What the result does and doesn’t mean</h2>
<p>A footprint calculation is a reasonableness check, not a measurement report. Dormers, multiple pitches, porches and complex hip roofs all change the real number, and waste on a cut-up roof can run well above a simple gable. If your count and the carrier’s are close, the dispute is probably about something else. If they are far apart, it is worth getting a proper measurement before arguing the point.</p>
<h2>Steep slopes and Kentucky roofs</h2>
<p>Estimating software commonly adds steep-slope labor charges once a roof reaches about 7/12, with higher tiers around 8/12 and above, and may add charges for two-story heights. Those line items are easy to miss on older Kentucky farmhouses and Victorian homes in places like Covington and Paducah, where steep pitches are common. If the carrier priced a steep roof as walkable, or left out waste and steep charges, that is a pricing difference appraisal can address. See our <a href="/insurance-appraisal/roof-hail-appraisal/">roof and hail appraisal</a> page for how we document those disputes.</p>""",
        "faqs": [
            ("What is a roofing square?", "A square is 100 square feet of roof surface. Estimates and material orders are usually written in squares rather than square feet."),
            ("Why is my count different from the insurer’s?", "Common reasons include a different pitch, missing overhangs, a lower waste factor or sections of the roof left off. The calculator gives a reasonableness check; a field or aerial measurement settles it."),
            ("Does the tool save my measurements?", "No. It runs entirely in your browser and nothing you enter is stored or sent."),
        ],
    },
    "percentage-deductible-calculator": {
        "name": "Percentage Deductible Calculator",
        "kind": "Calculator",
        "keyword": "percentage deductible calculator",
        "short": "See what a 1%, 2% or 5% wind and hail deductible really costs next to a flat deductible.",
        "title": "Percentage Deductible Calculator | Wind & Hail",
        "desc": "Percentage deductible calculator: turn a wind and hail percent into dollars, compare it to a flat deductible and find the loss size that pays nothing.",
        "h1": "Wind and Hail Percentage Deductible Calculator for Kentucky Homes",
        "lede": "A 2% deductible sounds small until you multiply it by your dwelling limit. Compare a percentage deductible with a flat one for the same loss. Everything runs in your browser and nothing is stored.",
        "explain": """<h2>How to use the calculator</h2>
<p>Find your Coverage A (dwelling) limit and your wind/hail deductible percentage on the declarations page. Enter both, plus your flat all-other-perils deductible and the estimated size of the loss. The tool shows the percentage deductible in dollars, what the insurer would pay under each deductible, the extra you pay out of pocket because of the percentage, the deductible as a share of the loss, and the break-even loss size.</p>
<h2>The math in plain words</h2>
<p>A percentage deductible is calculated on the dwelling limit, not on the size of the loss. So the dollar deductible is Coverage A times the percentage. Payment under each option is the loss minus that deductible, never less than zero. The extra out-of-pocket is the difference between the two deductibles, up to the size of the loss. The <strong>break-even loss size</strong> is simply the dollar deductible: any covered loss below it pays nothing.</p>
<h3>An illustrative example</h3>
<p>Illustrative figures only: a home with $300,000 of Coverage A and a 2% wind/hail deductible has a $6,000 deductible. On a $14,000 hail claim, the insurer pays $8,000. With a flat $1,000 deductible it would pay $13,000, so the percentage costs $5,000 more. A $5,500 claim would pay nothing.</p>
<h2>What the result does and doesn’t mean</h2>
<p>The calculator assumes the deductible applies to the whole loss. Real policies differ: some apply the percentage only to named storm, hail or windstorm losses, some set a minimum dollar amount, and some apply it per occurrence across several buildings. The deductible is also subtracted from what the loss is actually worth, so if the estimate is short, the deductible eats a larger share of a smaller number. Check the exact endorsement wording before relying on the result.</p>
<h2>Kentucky context</h2>
<p>Percentage wind and hail deductibles show up on many Kentucky policies, especially after rounds of spring hail across the Bluegrass and western Kentucky. Because the deductible is fixed, every dollar the estimate is low comes straight out of your recovery. If the carrier’s number barely clears the deductible, it is worth checking the scope before accepting it; our <a href="/insurance-appraisal/tornado-wind-appraisal/">tornado and wind appraisal</a> page explains how pricing disputes on storm claims are handled, and the <a href="/appraisal-calculators/appraisal-payoff-estimator/">appraisal payoff estimator</a> helps you weigh whether appraisal is worth it.</p>""",
        "faqs": [
            ("Is a percentage deductible based on the loss or the dwelling limit?", "On most policies it is based on the Coverage A dwelling limit shown on the declarations page, not on the size of the loss. Check your endorsement for the exact wording."),
            ("Can appraisal change my deductible?", "No. Appraisal sets the amount of loss. It can change the number the deductible is subtracted from, but not the deductible itself."),
            ("Is my policy information stored?", "No. The calculation runs in your browser and nothing is saved or sent to us."),
        ],
    },
    "claim-timeline-builder": {
        "name": "Claim Timeline Builder",
        "kind": "Planner",
        "keyword": "claim timeline builder",
        "short": "Build a dated list of claim milestones from your date of loss and export it to your calendar.",
        "title": "Claim Timeline Builder | Insurance Claim Dates",
        "desc": "Claim timeline builder: enter a date of loss or appraisal demand to map proof of loss, holdback and appraisal dates, then export a calendar file.",
        "h1": "Insurance Claim Timeline Builder With Calendar Export",
        "lede": "Turn your date of loss into a dated checklist of claim milestones and save it to your calendar. The windows are editable defaults, not legal advice. Everything runs in your browser and nothing is stored.",
        "explain": """<h2>How to use the timeline builder</h2>
<p>Enter the date of loss. If appraisal has already been demanded, enter that date too. The tool builds a list of milestones, each with a default window you can change to match your policy. When it looks right, export it as a .ics file and open it in Google Calendar, Outlook or Apple Calendar so the reminders come to you.</p>
<h2>What the milestones are</h2>
<ul>
<li><strong>Report the claim:</strong> a target date for notifying the insurer. Most policies require prompt notice, so sooner is better.</li>
<li><strong>Temporary repairs:</strong> tarping, board-up and water extraction to prevent further damage, with receipts kept.</li>
<li><strong>Proof of loss:</strong> many policies require a sworn proof of loss within a set number of days after the insurer asks for it.</li>
<li><strong>Replacement cost or holdback notice:</strong> the window to complete repairs or tell the insurer you intend to claim the depreciation holdback.</li>
<li><strong>Suit limitation date:</strong> a placeholder you fill in from your policy.</li>
</ul>
<p>If you enter a demand date, two more items appear: <strong>name your appraiser</strong> (many policies allow 20 days after the demand) and <strong>umpire selection</strong> (commonly 15 days after the appraisers are named).</p>
<h2>The math in plain words</h2>
<p>Each milestone is the start date plus the number of days in its window. Change a window and every date tied to it moves. Nothing else is calculated, and the tool cannot read your policy for you.</p>
<h2>What the result does and doesn’t mean</h2>
<p>These are planning defaults, not deadlines that bind you or your insurer. Policies differ, carriers send letters that start their own clocks, and some deadlines run from the insurer’s request rather than the date of loss. The timeline is not legal advice.</p>
<div class="note"><b class="h">Suit limitation</b>Your policy’s legal action clause sets how long you have to file suit, and Kentucky law affects how that clause applies. Read the clause and speak with a Kentucky attorney well before the date approaches. Appraisal may not pause it.</div>
<h2>Kentucky context</h2>
<p>After widespread events such as ice storms or tornado outbreaks, adjusters and contractors fall behind and claims stretch for months. That is exactly when a window quietly closes. Our <a href="/kentucky-appraisal-process/">Kentucky appraisal process</a> guide explains each appraisal step in order, and the <a href="/appraisal-calculators/appraisal-readiness-checkup/">appraisal readiness checkup</a> helps you confirm your file is in shape before you demand.</p>""",
        "faqs": [
            ("Are these dates my actual legal deadlines?", "No. They are editable planning defaults. Your policy, letters from your insurer and Kentucky law control the real deadlines, so check them and speak with a Kentucky attorney about suit limitation."),
            ("How long do I have to name an appraiser?", "Many policies allow about 20 days after the written demand, but the wording varies. Read your appraisal clause and adjust the window in the tool to match it."),
            ("Does the calendar export upload my dates anywhere?", "No. The .ics file is created in your browser and saved straight to your device. Nothing is stored or sent to us."),
        ],
    },
    "appraisal-readiness-checkup": {
        "name": "Appraisal Readiness Checkup",
        "kind": "Checkup",
        "keyword": "appraisal readiness checkup",
        "short": "Answer 10 yes-or-no questions to see if your claim file is ready for appraisal and what to fix first.",
        "title": "Appraisal Readiness Checkup | 10-Question Self-Test",
        "desc": "Appraisal readiness checkup: ten yes-or-no questions score your claim file, flag missing documents and build a to-do list before you invoke appraisal.",
        "h1": "Is Your Claim Ready? Take the Appraisal Readiness Checkup",
        "lede": "Ten quick questions show how prepared your claim file is for appraisal and what to work on next. Everything runs in your browser and nothing is stored.",
        "explain": """<h2>How to use the checkup</h2>
<p>Answer each of the ten questions yes or no. The meter fills as you go, and every “no” adds a specific item to your to-do list. You can change answers at any time and the score updates instantly. When you are done, work through the list from the top, since it is ordered by how much each item matters.</p>
<h2>What the questions cover</h2>
<p>The questions follow the things appraisers, umpires and insurers look for first:</p>
<ul>
<li>Whether the insurer has accepted that a covered loss happened, so the dispute is about price rather than coverage.</li>
<li>Whether you have the full policy, including declarations and endorsements, and have read the appraisal clause.</li>
<li>Whether you have the carrier’s estimate and a competing line-item estimate.</li>
<li>Whether the damage is documented with dated photos and video.</li>
<li>Whether mitigation and temporary repair receipts are organized.</li>
<li>Whether you know your key policy windows, such as proof of loss and the replacement cost deadline.</li>
<li>Whether the gap between the estimates is large enough to justify appraisal costs.</li>
</ul>
<h2>The math in plain words</h2>
<p>Each question carries a weight. Questions that can stop appraisal from working at all, such as an open coverage denial or the lack of any competing estimate, weigh more than housekeeping items. Your score is the sum of the weights for your “yes” answers, shown as a percentage of the total possible.</p>
<h2>What the result does and doesn’t mean</h2>
<p>A high score means your file has the basic pieces in place. It does not mean appraisal will produce a particular award, and a low score does not mean your claim is weak. It usually just means documents are missing or a question needs answering first. If the checkup flags a coverage question, appraisal may be the wrong tool and a Kentucky attorney is the better first step.</p>
<h2>Kentucky context</h2>
<p>Many Kentucky claims stall not because the damage is unclear but because the file is scattered: an estimate here, photos on three phones, the policy still in the agent’s office. Getting organized before you demand appraisal saves time once the 20-day window to name an appraiser starts running on many policies. Our <a href="/kentucky-appraisal-process/">guide to the Kentucky appraisal process</a> walks through what happens after the demand, and you can <a href="/contact-us/">contact us</a> if you want a second opinion on your file.</p>""",
        "faqs": [
            ("What score means I am ready for appraisal?", "There is no magic number. A high score means the core pieces are in place; any heavily weighted “no,” such as an unresolved coverage denial, is worth fixing or getting advice on before you demand."),
            ("Why does a coverage question lower my score so much?", "Appraisal sets the amount of a covered loss. If coverage itself is disputed, appraisal may not resolve the real problem, so that question carries extra weight."),
            ("Are my answers saved?", "No. The checkup runs entirely in your browser and your answers are not stored or sent anywhere."),
        ],
    },
    "tree-removal-coverage-calculator": {
        "name": "Storm Tree Removal Coverage Calculator",
        "kind": "Calculator",
        "keyword": "tree removal coverage calculator",
        "short": "Estimate how much of a storm tree removal bill your homeowners policy may cover and what you might pay.",
        "title": "Tree Removal Coverage Calculator | Storm Debris",
        "desc": "Tree removal coverage calculator for Kentucky storms: apply per-tree and per-occurrence limits and estimate covered and out-of-pocket costs.",
        "h1": "Storm Tree Removal Coverage Calculator for Kentucky Homes",
        "lede": "Ice and wind bring down trees across Kentucky every year. Estimate how much removal your policy may pay under common debris limits. Everything runs in your browser and nothing is stored.",
        "explain": """<h2>How to use the calculator</h2>
<p>Enter the number of fallen trees, the removal cost per tree from your tree service quote, and whether each tree hit a covered structure or is blocking a driveway or a ramp built for a person with a disability. Then set the per-tree limit and per-occurrence limit from your policy. The defaults, $500 per tree and $1,000 per occurrence, reflect a common pattern, but you should edit them to match your form.</p>
<h2>The math in plain words</h2>
<p>Only trees that meet a qualifying condition are counted. For each, the covered amount is the lower of the removal cost and the per-tree limit. Those amounts are added up and then capped at the per-occurrence limit. The out-of-pocket figure is the total removal bill minus the estimated covered amount.</p>
<h3>An illustrative example</h3>
<p>Illustrative figures only: three qualifying trees at $1,200 each cost $3,600 to remove. Each is capped at $500, which would be $1,500, but the $1,000 occurrence limit applies, so the estimated covered removal is $1,000 and the out-of-pocket is $2,600.</p>
<h2>What the result does and doesn’t mean</h2>
<p>Many homeowners forms cap tree debris removal with a per-tree and per-occurrence limit like this, and often pay only when the tree damaged a covered structure or blocks access. Limits, conditions and covered causes vary by form and carrier, and some policies pay nothing for a tree that fell in the yard without hitting anything. Your deductible may also apply. The tool does not know your policy, so read the debris removal and trees, shrubs and plants sections before relying on the number.</p>
<p>One important distinction: removing the part of a tree that is resting on a damaged house is often handled as part of the dwelling repair, not under the tree debris limit. If an estimate pushes that work into the capped tree line, it is worth questioning.</p>
<h2>Kentucky context</h2>
<p>Kentucky knows this problem well. The January 2009 ice storm snapped and uprooted trees across western and central Kentucky, and the March 2023 windstorm brought down trees statewide. After events like these, removal crews are scarce, prices rise, and the gap between the bill and the debris limit grows. If the dispute is about how dwelling damage and tree work were priced, see our <a href="/insurance-appraisal/ice-storm-freeze-appraisal/">ice storm and freeze appraisal</a> page.</p>""",
        "faqs": [
            ("Why does my policy only pay a small amount for tree removal?", "Many homeowners forms cap tree debris removal with a per-tree limit and a per-occurrence limit, and pay only if the tree hit a covered structure or blocks access. Check your form for the exact limits and conditions."),
            ("Is removing a tree from my roof part of the tree limit?", "Often not. Getting the tree off a damaged house is frequently treated as part of the dwelling repair. How your carrier handles it depends on the policy wording and the estimate."),
            ("Does the calculator save my numbers?", "No. Everything runs in your browser and nothing you enter is stored or sent."),
        ],
    },
}
