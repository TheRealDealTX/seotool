<?php
// Renter tools: registry used by the hub, each tool page, the nav and the sitemap.
// Markup for each tool lives in views/tools/{slug}.php; behavior in assets/js/tools.js.
defined('HA_ROOT') || exit;

const TOOLS_BASE = '/houston-apartment-tools/';

const TOOLS = [
    'rent-affordability-calculator' => [
        'icon'  => '💵',
        'name'  => 'Rent Affordability Calculator',
        'h1'    => 'How Much Rent Can I Afford in Houston?',
        'short' => 'Turn your income into a realistic rent budget using the rules Houston leasing offices actually apply.',
        'meta'  => 'Free Houston rent affordability calculator: enter your income and debts to see the rent you qualify for under the 3x-income rule and a comfortable monthly budget.',
        'body'  => '<h2>How Houston apartments decide what you can afford</h2>
<p>Most Houston apartment communities ask that your gross monthly income is about <strong>three times the rent</strong>. Some write it as an annual rule – income of 40 times the monthly rent – which works out to almost the same number. Leasing offices usually count income from every adult on the lease, so roommates and couples can combine pay.</p>
<p>Qualifying and being comfortable are different things. Budget experts often suggest keeping rent near <strong>30% of gross income</strong>, and lower if you carry car payments, student loans or credit card balances. The calculator shows both the maximum you’re likely to be approved for and a range that leaves room for utilities, parking and savings.</p>
<h2>Tips if your budget is tight</h2>
<ul><li>Look at the suburbs – Katy, Cypress, Humble and Baytown often offer more space for the same rent.</li>
<li>Ask about move-in specials. A few free weeks lowers your real monthly cost over the lease.</li>
<li>Add a co-signer or guarantor if your income is just under the requirement.</li>
<li>Let a locator check which communities are flexible on income or credit.</li></ul>',
        'faqs'  => [
            ['How much do I need to make to rent an apartment in Houston?', 'Most communities want gross monthly income of about three times the rent. For a $1,300 apartment that is roughly $3,900 a month, or about $46,800 a year before taxes.'],
            ['Do apartments count my roommate’s income?', 'Usually yes. When everyone signs the lease, most Houston properties combine the applicants’ incomes to meet the requirement, though each person still goes through screening.'],
            ['What if I don’t meet the income requirement?', 'Options include adding a guarantor, paying an extra deposit, showing savings, or choosing a property with lower requirements. A locator can tell you which communities accept these.'],
        ],
    ],
    'move-in-cost-calculator' => [
        'icon'  => '📦',
        'name'  => 'Move-In Cost Calculator',
        'h1'    => 'Apartment Move-In Cost Calculator',
        'short' => 'Add up deposits, fees, prorated rent, pet costs and movers so nothing surprises you at signing.',
        'meta'  => 'Estimate what you’ll pay to move into a Houston apartment: deposit, application and admin fees, prorated rent, pet fees, utilities and movers – all in one free calculator.',
        'body'  => '<h2>What you’ll pay before you get the keys</h2>
<p>Rent is only part of moving in. Houston apartments typically charge an <strong>application fee</strong> for each adult, a one-time <strong>administration fee</strong>, and a <strong>security deposit</strong> that can be a flat amount or up to a month’s rent depending on your screening. Pets usually add a deposit or one-time fee plus monthly pet rent.</p>
<p>Many communities also collect <strong>prorated rent</strong> for the days left in your move-in month. If you move in on the 20th of a 30-day month, you pay for 11 days now and a full month on the 1st. Set your move-in date in the calculator to see the exact amount.</p>
<h2>Ways to lower move-in costs</h2>
<ul><li>Ask whether the property offers a reduced deposit or a deposit alternative.</li>
<li>Time your move for the end of the month to keep prorated rent small, or ask to start the lease on the 1st.</li>
<li>Look for look-and-lease specials that waive the admin or application fee.</li>
<li>Get two or three moving quotes – prices vary a lot in Houston.</li></ul>',
        'faqs'  => [
            ['How much is a typical apartment deposit in Houston?', 'Deposits range widely. Applicants with strong credit often pay a flat deposit of a few hundred dollars, while others may be asked for up to one month’s rent. The leasing office confirms the amount after screening.'],
            ['What is prorated rent?', 'Prorated rent is the partial rent for the days you live in the apartment during your first month. It is calculated from the daily rate (monthly rent divided by the days in that month).'],
            ['Are application fees refundable?', 'Generally no. Application fees cover screening costs and are usually non-refundable even if you are not approved, so it pays to apply only where you qualify.'],
        ],
    ],
    'rent-split-calculator' => [
        'icon'  => '🤝',
        'name'  => 'Roommate Rent Split Calculator',
        'h1'    => 'Roommate Rent Split Calculator',
        'short' => 'Split rent and utilities fairly – evenly, by bedroom size, or by income.',
        'meta'  => 'Split rent fairly with roommates: divide rent and utilities evenly, by bedroom size and private bathroom, or by income with this free rent split calculator.',
        'body'  => '<h2>Three fair ways to split the rent</h2>
<p><strong>Even split</strong> is simplest when the bedrooms are similar. When one room is bigger or has its own bathroom, a <strong>size-based split</strong> feels fairer: the calculator weighs each room’s square footage and adds a premium for a private bath. Couples and friends with very different pay sometimes prefer an <strong>income-based split</strong>, where each person pays the same share of what they earn.</p>
<p>Utilities and internet are usually split evenly because everyone uses the shared space. Agree on the method before you sign – and put it in writing so there are no surprises later.</p>
<h2>Before you sign with roommates</h2>
<ul><li>Most Houston leases make every roommate responsible for the full rent, not just their share.</li>
<li>Decide who pays the landlord and how others reimburse them.</li>
<li>Look for floor plans with “roommate style” layouts – bedrooms on opposite sides with their own baths.</li></ul>',
        'faqs'  => [
            ['How do you split rent when rooms are different sizes?', 'Weigh each bedroom by its square footage, give extra weight to private bathrooms, then divide the rent in proportion. Shared spaces are treated as equal for everyone.'],
            ['Is everyone on the lease responsible for the whole rent?', 'Usually yes. Most leases are “joint and several,” meaning the property can collect the full rent from any roommate if someone doesn’t pay.'],
        ],
    ],
    'apartment-cost-comparison' => [
        'icon'  => '⚖️',
        'name'  => 'Apartment True-Cost Comparison',
        'h1'    => 'Compare the True Monthly Cost of Apartments',
        'short' => 'Rent isn’t the whole story. Compare utilities, parking, pet rent, specials and commute costs side by side.',
        'meta'  => 'Compare Houston apartments by true monthly cost: rent, utilities, parking, pet rent, move-in specials and commute driving costs side by side.',
        'body'  => '<h2>Why the cheapest rent isn’t always the cheapest apartment</h2>
<p>A lower rent in the suburbs can cost more once you add a longer drive on I-10 or US-59, and a downtown high-rise with garage parking and valet trash fees can creep well past its advertised price. This tool adds every recurring cost and spreads move-in specials across the lease so you compare apartments on what you’ll actually pay each month.</p>
<p>Driving cost uses a per-mile rate (default 70¢, close to the IRS standard rate that covers gas, maintenance and depreciation). Change it to match your car.</p>',
        'faqs'  => [
            ['How do move-in specials affect monthly cost?', 'A special such as six weeks free on a 12-month lease is worth 1.5 months of rent. Spread over the lease, it lowers your effective monthly rent by about 12.5%.'],
            ['What does it cost to commute by car in Houston?', 'A common estimate is about 70 cents per mile including gas, maintenance and wear. A 15-mile one-way commute, five days a week, adds roughly $450 a month.'],
        ],
    ],
    'commute-apartment-finder' => [
        'icon'  => '🚗',
        'name'  => 'Commute Apartment Finder',
        'h1'    => 'Find Houston Apartments Near Your Work',
        'short' => 'Enter your office or school and how far you’ll travel – we’ll map the area and show apartments inside it.',
        'meta'  => 'Find apartments near your job in Houston: enter your work address and commute distance to map the area and see matching apartments.',
        'body'  => '<h2>Pick your commute first, then your apartment</h2>
<p>Houston is huge, so commute time matters more than ZIP code. Enter your workplace, school or the Texas Medical Center, choose how far you’re willing to go, and the finder draws that area on the map. One click opens our map search limited to apartments inside the circle, where you can keep filtering by beds, pets and amenities.</p>
<p>Distances are straight-line estimates. Freeway access matters – an apartment 10 miles out along the Katy Freeway can be quicker than one 6 miles away across town – so treat the circle as a starting point, then use the draw tool to fine-tune.</p>',
        'faqs'  => [
            ['How far is a 20-minute commute in Houston?', 'Outside rush hour it can be 10–15 miles on the freeways; in peak traffic it may be only 5–8 miles. Use a smaller radius if you’ll drive at rush hour.'],
            ['Can I draw my own shape instead of a circle?', 'Yes. Open the map search and use “Draw area” to trace any shape – for example along a rail line or freeway.'],
        ],
    ],
    'apartment-tour-checklist' => [
        'icon'  => '✅',
        'name'  => 'Apartment Tour Checklist',
        'h1'    => 'Apartment Tour Checklist',
        'short' => 'A tap-to-check list of what to inspect and ask on every tour. Saves on your phone and prints cleanly.',
        'meta'  => 'Free interactive apartment tour checklist: what to inspect in the unit and building, questions to ask the leasing office, and notes – saved on your phone.',
        'body'  => '<h2>Get more out of every tour</h2>
<p>Tours move fast, and after the third property they start to blur together. Use this checklist on your phone while you walk through each apartment – your checks and notes are saved in this browser, so you can compare later. Add the property name at the top, then start a fresh list for the next one.</p>
<p>In Houston, pay extra attention to <strong>water pressure, A/C performance and signs of past leaks or flooding</strong>, and ask how the building handled the last big storm.</p>',
        'faqs'  => [
            ['What should I look for when touring an apartment?', 'Check water pressure and hot water, the A/C, windows and locks, signs of pests or leaks, cell signal, noise, parking and trash areas, and how well the common areas are kept.'],
            ['What questions should I ask the leasing office?', 'Ask about total monthly fees beyond rent, utility averages, parking costs, pet policies, lease-break terms, current specials and how maintenance requests are handled.'],
        ],
    ],
    'moving-checklist' => [
        'icon'  => '🗓️',
        'name'  => 'Houston Moving Checklist',
        'h1'    => 'Moving to a Houston Apartment: Checklist',
        'short' => 'A week-by-week plan from eight weeks out to move-in day, with Houston-specific steps like choosing an electricity plan.',
        'meta'  => 'A week-by-week checklist for moving into a Houston apartment: notice to your landlord, choosing an electricity provider, movers, address changes and move-in inspection.',
        'body'  => '<h2>A calmer move, one week at a time</h2>
<p>Work through the list from the top. Your progress is saved in this browser, so you can come back any time. Houston has a few local twists: most of the area has a deregulated electricity market, so you’ll pick a retail electric provider yourself (compare plans on the state’s Power to Choose site), and Texas asks new residents to update their driver license and vehicle registration soon after moving.</p>',
        'faqs'  => [
            ['How do I set up electricity in a Houston apartment?', 'In most of Houston you choose a retail electricity provider. Compare plans, sign up with your new address and move-in date, and the provider coordinates with the local utility to start service.'],
            ['How soon should I start apartment hunting before moving?', 'Start searching four to six weeks before your move date. Many Houston communities only hold apartments for a few weeks, so applying too early can be hard.'],
        ],
    ],
];
