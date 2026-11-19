<?php defined('ERE') or exit;
return [
    'title'       => 'How to Analyze a Rental Property: NOI, Cap Rate and Cash Flow, With a Houston Example',
    'seo_title'   => 'How to Analyze a Rental Property (Houston Example)',
    'description' => 'How to analyze a rental property step by step: NOI, cap rate, cash-on-cash return and cash flow, with a worked Houston example using real Texas tax math.',
    'keyword'     => 'how to analyze a rental property',
    'category'    => 'investing',
    'date'        => '2026-10-14',
    'excerpt'     => 'A step-by-step method for running the numbers on a rental, from NOI and cap rate to cash-on-cash return, with a worked Houston example that models Texas taxes and insurance honestly.',
    'faq'         => [
        ['What is a good cap rate for a rental property in Houston?', 'There is no single good number. Cap rate depends on the neighborhood, the age of the house and how much risk you accept. Newer homes in strong suburbs usually trade at lower cap rates than older homes in tougher areas. What matters most is comparing the cap rate to your borrowing cost: if your cap rate is below your mortgage rate, leverage will reduce your return, not increase it.'],
        ['Does the 1% rule work in Texas?', 'The 1% rule is a quick screen, not an analysis. In Texas it is especially misleading because property taxes and insurance are high, so a house can pass the 1% rule and still produce thin or negative cash flow. Use it only to decide which listings deserve a full analysis, then model taxes, insurance, vacancy, repairs and management line by line.'],
        ['How do I estimate property taxes on a Texas rental?', 'Multiply the expected appraised value by the combined tax rate for that exact address. Rentals do not get a homestead exemption, so do not use the seller\'s current bill if the seller has one. Look up the rates for every taxing unit on the parcel through the appraisal district, and assume the appraisal will move toward your purchase price after you buy.'],
        ['What is the difference between cap rate and cash-on-cash return?', 'Cap rate measures the property\'s income relative to its price, ignoring financing. It lets you compare buildings to each other. Cash-on-cash return measures your annual pre-tax cash flow relative to the cash you actually invested, so it includes your loan payment. A property can have a decent cap rate and a poor cash-on-cash return if the loan is expensive.'],
        ['How much should I budget for repairs and capital expenses?', 'Many investors set aside 5% to 10% of gross rent for ordinary repairs and another 5% to 10% for big-ticket replacements such as roofs, HVAC systems and water heaters. Older Houston homes, homes with original plumbing and homes with aging HVAC systems in our heat deserve the higher end. Get an inspection and price the big systems before you choose a number.'],
    ],
    'products'    => ['book-rental-property', 'book-millionaire-investor', 'laser-measure'],
    'tools'       => ['rental-property-calculator', 'texas-property-tax-calculator'],
    'related'     => ['brrrr-method-explained', 'house-hacking-texas', 'protest-property-taxes-harris-county'],
    'body'        => <<<'HTML'
<p>To analyze a rental property, estimate the rent it will actually collect, subtract every operating expense to get net operating income (NOI), then compare that NOI to the price (cap rate) and, after your mortgage payment, to the cash you invest (cash-on-cash return). Knowing how to analyze a rental property this way keeps you from buying on gut feel or a seller's pro forma.</p>
<p>In Houston and the rest of Texas, the two expenses that sink most deals are property taxes and insurance. This guide walks through each metric, the quick rules of thumb and their limits, and a full worked example.</p>

<h2>Step 1: Estimate realistic income</h2>
<p>Start with market rent, not the rent the listing claims. Pull recent leases for similar homes within a mile: same bedroom and bathroom count, similar size, age and condition. A local agent can pull leased comps from the MLS, which is far more reliable than asking rents on listing sites.</p>
<p>Then reduce gross rent for vacancy and credit loss. Even good tenants move out, and turnover takes time for cleaning, repairs and showings. Many investors use 5% to 8% of gross rent. The result is your <strong>effective gross income</strong> (EGI), the money you can reasonably expect to collect.</p>
<ul>
<li><strong>Gross scheduled rent:</strong> monthly market rent times 12.</li>
<li><strong>Vacancy and credit loss:</strong> a percentage of gross rent, adjusted for the neighborhood and price point.</li>
<li><strong>Other income:</strong> pet fees or similar, only if they are common in that market. Leave them out if you are unsure.</li>
</ul>

<h2>Step 2: List every operating expense (Texas edition)</h2>
<p>Operating expenses are the costs of running the property, not the mortgage. Missing one here is the most common way new investors overpay.</p>
<h3>Property taxes</h3>
<p>Texas has no state income tax, and local governments lean heavily on property taxes. Combined rates in much of the Houston area land somewhere around 2% to 3% of appraised value, depending on the city, school district, MUD and other taxing units on the parcel. Look up the exact rates for the address through the <a href="https://hcad.org/">Harris County Appraisal District</a> or the relevant county appraisal district.</p>
<p>Two traps catch buyers. First, a rental gets no homestead exemption, so the seller's tax bill may be much lower than yours will be. Second, appraisal districts tend to move a recently sold property toward its sale price, so model taxes on your purchase price, not last year's appraised value. You can protest every year, and our guide on <a href="/blog/protest-property-taxes-harris-county/">protesting property taxes in Harris County</a> explains how.</p>
<h3>Insurance</h3>
<p>Landlord (dwelling) policies in the Houston area have become expensive, with wind, hail and hurricane exposure driving premiums and deductibles. Get an actual quote for the specific address before you make an offer. If the home sits in or near a flood zone, price flood insurance separately, because standard policies exclude flood.</p>
<h3>The rest of the list</h3>
<ul>
<li><strong>Property management:</strong> often 8% to 10% of collected rent, plus leasing fees. Include it even if you plan to self-manage, so the deal still works if you change your mind.</li>
<li><strong>Repairs and maintenance:</strong> commonly 5% to 10% of gross rent.</li>
<li><strong>Capital expenditures (CapEx):</strong> a reserve for roofs, HVAC, water heaters and flooring. Houston heat is hard on air conditioning systems.</li>
<li><strong>HOA dues, lawn care and any owner-paid utilities</strong> such as water and trash.</li>
</ul>

<h2>Step 3: Calculate NOI and cap rate</h2>
<p><strong>NOI = effective gross income minus operating expenses.</strong> NOI excludes your mortgage payment, depreciation and income taxes. It describes the property itself, regardless of who owns it or how it is financed.</p>
<p><strong>Cap rate = NOI divided by purchase price.</strong> A house that produces $10,000 of NOI and costs $200,000 has a 5% cap rate. Cap rate lets you compare properties on equal footing and quickly test whether a price makes sense.</p>
<p>A useful sanity check: if the cap rate is below your mortgage interest rate, borrowing money makes your return worse, not better. That situation is called negative leverage, and it is common when rates are high and prices have not adjusted.</p>

<h2>Step 4: Calculate cash flow and cash-on-cash return</h2>
<p><strong>Annual cash flow = NOI minus annual debt service</strong> (principal and interest on your loan). Lenders often express the same relationship as the debt service coverage ratio: NOI divided by debt service. A ratio below 1.0 means the property does not cover its loan.</p>
<p><strong>Cash-on-cash return = annual cash flow divided by total cash invested.</strong> Total cash includes your down payment, closing costs and any upfront repairs. This is the number that tells you what your money is earning compared with other options.</p>
<p>Cash-on-cash ignores principal paydown, appreciation and tax benefits, so it understates your total return. That is fine. Those other benefits are real but uncertain, and cash flow is what keeps you solvent when the AC dies in August.</p>
<h3>Look past year one</h3>
<p>A single-year snapshot can hide problems. Texas property taxes and insurance premiums can rise faster than rent, so a deal that barely breaks even today may lose money in three years. Run a simple projection: grow rent by a conservative rate, grow taxes and insurance faster, and see where cash flow lands. Also note when big items are due. A roof with three years of life left is a cost you will pay, even if it does not appear in your first-year numbers. If the deal only works under best-case assumptions, it does not work.</p>

<h2>The 1% rule, the 50% rule and their limits</h2>
<p>Rules of thumb help you screen dozens of listings quickly. They should never be the reason you buy.</p>
<table>
<thead><tr><th>Rule</th><th>What it says</th><th>Where it breaks down in Texas</th></tr></thead>
<tbody>
<tr><td>1% rule</td><td>Monthly rent should be at least 1% of the purchase price.</td><td>It ignores expenses entirely. With high taxes and insurance, a house can pass 1% and still barely cash flow.</td></tr>
<tr><td>50% rule</td><td>Operating expenses plus vacancy will eat about half of gross rent.</td><td>With Texas taxes and insurance, the true figure can run well above 50%, as the example below shows.</td></tr>
<tr><td>Cap rate vs. interest rate</td><td>Cap rate should beat your borrowing cost for leverage to help.</td><td>A good test, but it still depends on accurate expense inputs.</td></tr>
</tbody>
</table>
<p>Use the rules to decide which properties deserve a full analysis. Then run every line item, ideally in our <a href="/tools/rental-property-calculator/">rental property calculator</a>, so you can change one assumption at a time.</p>

<h2>Worked example: a Houston-area single-family rental</h2>
<p>Here is a hypothetical three-bedroom house in the Houston suburbs. The figures are illustrative assumptions, not quotes or market data, so replace them with real numbers for any property you are considering.</p>
<ul>
<li>Market rent: $2,000 per month; vacancy 6%</li>
<li>Property tax: 2.3% of purchase price (no homestead exemption)</li>
<li>Insurance: $2,800 per year; HOA: $500 per year</li>
<li>Management: 9% of collected rent; repairs 5% and CapEx 5% of gross rent</li>
<li>Financing: 25% down, 30-year loan at an assumed 7.0% rate, closing costs 3% of price</li>
</ul>
<p>The table compares the asking price with a lower offer.</p>
<table>
<thead><tr><th>Line item</th><th>At asking: $225,000</th><th>At offer: $170,000</th></tr></thead>
<tbody>
<tr><td>Gross scheduled rent</td><td>$24,000</td><td>$24,000</td></tr>
<tr><td>Vacancy (6%)</td><td>-$1,440</td><td>-$1,440</td></tr>
<tr><td>Effective gross income</td><td>$22,560</td><td>$22,560</td></tr>
<tr><td>Property taxes (2.3%)</td><td>-$5,175</td><td>-$3,910</td></tr>
<tr><td>Insurance</td><td>-$2,800</td><td>-$2,800</td></tr>
<tr><td>Management (9%)</td><td>-$2,030</td><td>-$2,030</td></tr>
<tr><td>Repairs (5%)</td><td>-$1,200</td><td>-$1,200</td></tr>
<tr><td>CapEx reserve (5%)</td><td>-$1,200</td><td>-$1,200</td></tr>
<tr><td>HOA</td><td>-$500</td><td>-$500</td></tr>
<tr><td><strong>NOI</strong></td><td><strong>$9,655</strong></td><td><strong>$10,920</strong></td></tr>
<tr><td>Cap rate</td><td>4.29%</td><td>6.42%</td></tr>
<tr><td>Loan amount (75%)</td><td>$168,750</td><td>$127,500</td></tr>
<tr><td>Annual debt service</td><td>-$13,476</td><td>-$10,176</td></tr>
<tr><td><strong>Annual cash flow</strong></td><td><strong>-$3,821</strong></td><td><strong>$744</strong></td></tr>
<tr><td>Cash invested (28%)</td><td>$63,000</td><td>$47,600</td></tr>
<tr><td>Cash-on-cash return</td><td>-6.07%</td><td>1.56%</td></tr>
<tr><td>Debt service coverage</td><td>0.72</td><td>1.07</td></tr>
</tbody>
</table>
<h3>What the numbers tell you</h3>
<p>At the asking price, the house loses about $318 a month before any surprise repair. The cap rate of 4.29% sits well below the 7% loan rate, which is negative leverage in action. A lender using a debt service coverage test would likely balk too.</p>
<p>At $170,000, the house passes the 1% rule ($2,000 is about 1.18% of the price), yet cash-on-cash return is only 1.56%. That is the limit of the 1% rule in plain view. Notice also that expenses plus vacancy consume about 55% to 60% of gross rent in both scenarios, more than the 50% rule predicts, mostly because of taxes and insurance.</p>
<p>The levers that would improve this deal are a lower price, a lower insurance quote, self-management, a larger down payment or a lower rate. If none are realistic, the right answer is to walk away and keep looking. Strategies like <a href="/blog/brrrr-method-explained/">the BRRRR method</a> try to create equity up front to solve exactly this problem.</p>

[[tool:rental-property-calculator]]

<h2>Due diligence before you trust your numbers</h2>
<ol>
<li><strong>Verify rent</strong> with leased comps, not asking rents.</li>
<li><strong>Get an insurance quote</strong> for the specific address, including wind and hail deductibles, and check the flood zone.</li>
<li><strong>Look up every taxing unit</strong> on the parcel, including MUDs and special districts, and model taxes on your price.</li>
<li><strong>Order an inspection</strong> and price the roof, HVAC, foundation, plumbing and water heater. Foundation movement is common on Houston clay soils.</li>
<li><strong>Read the deed restrictions and HOA rules</strong> for leasing limits or rental registration requirements.</li>
<li><strong>Stress test</strong> the deal with higher vacancy, a 10% to 15% jump in taxes and insurance, and one major repair in year one.</li>
</ol>
<p>Tax treatment of rental income, depreciation and deductions varies by situation, so confirm your plan with a CPA before you buy.</p>

<h2>Bottom line</h2>
<p>Analyzing a rental property comes down to honest inputs: market rent, real vacancy, and every expense, especially Texas property taxes and insurance. Calculate NOI, cap rate, cash flow and cash-on-cash return, use the 1% and 50% rules only as screens, and stress test before you offer. More strategies are in our <a href="/category/investing/">investing guides</a>.</p>
HTML,
];
