<?php
// SEO copy for each /tools/{slug}/ page. The widget itself comes from inc/tools.php.

return [
    'side-hustle-quiz' => [
        'title' => 'Side Hustle Quiz: Find the Best Side Hustle for You (Free)',
        'description' => 'Take the free Better Side Hustles quiz. Answer 6 questions about your time, skills, budget and goals and get your 3 best-matched side hustles instantly.',
        'h1' => 'Side Hustle Quiz: Which Side Hustle Is Right for You?',
        'gear' => ['planner', 'book-side-hustle', 'book-100-startup'],
        'guides' => ['side-hustles-you-can-start-with-just-your-smartphone', 'digital-marketing-side-hustle', 'fiverr', 'lyft-uber', 'exploring-the-world-of-side-hustles-in-2023'],
        'body' => <<<'HTML'
<h2 id="how-the-quiz-works">How the side hustle quiz works</h2>
<p>Most "best side hustle" lists ignore the three things that decide whether you'll stick with one: how many hours you really have, how quickly you need the money, and whether you'd rather work at a laptop, on your phone or out in your city. This quiz scores 18 proven side hustles against your answers and ranks the top three.</p>
<p>A car-dependent gig never shows up if you don't have a car, and if your budget is zero we push you toward hustles you can start for free, like freelancing, tutoring or pet sitting.</p>
<h2 id="after-your-results">What to do with your results</h2>
<ol class="steps">
<li><strong>Read the guide for match #1.</strong> Each result links to a step-by-step guide with pay ranges and startup costs.</li>
<li><strong>Put a number on it.</strong> Plug your expected rate and hours into the <a href="/tools/income-calculator/">side hustle income calculator</a>.</li>
<li><strong>Commit to a two-week test.</strong> Work your first match for ten to fifteen hours before you judge it. The first week is always the slowest.</li>
</ol>
<div class="callout"><strong>Quick tip:</strong> If two of your matches are close, choose the one that pays out fastest. Seeing early income keeps you going.</div>
HTML,
        'faq' => [
            ['q' => 'How accurate is the side hustle quiz?', 'a' => 'It is a starting point, not a verdict. It weighs your schedule, goals, work style, skills, car and budget against typical requirements for each side hustle. Use the top three as a shortlist and read each guide before deciding.'],
            ['q' => 'Do I need to give my email to see results?', 'a' => 'No. Results appear instantly on the page and nothing you choose is stored or sent anywhere.'],
            ['q' => 'What is the easiest side hustle to start?', 'a' => 'Food delivery, selling things you already own and simple freelance services on Fiverr are the easiest to start because they need little setup and pay quickly.'],
        ],
    ],
    'income-calculator' => [
        'title' => 'Side Hustle Income Calculator: Monthly & Yearly Earnings',
        'description' => 'Free side hustle income calculator. Enter your hourly rate, hours and costs to see take-home pay per month and year, plus how fast you reach a savings goal.',
        'h1' => 'Side Hustle Income Calculator',
        'gear' => ['planner', 'book-psych-money', 'book-profit-first'],
        'guides' => ['side-hustles-you-can-start-with-just-your-smartphone', 'fiverr', 'lyft-uber', 'digital-marketing-side-hustle', 'best-side-hustles-in-indianapolis'],
        'body' => <<<'HTML'
<h2 id="how-it-works">How to use the side hustle income calculator</h2>
<p>Enter what you earn per hour (or your average hourly earnings for gig apps), how many hours you'll work each week and how many weeks a year. Subtract monthly costs such as app fees, supplies or gas. Then choose a tax set-aside: 25% is a safe default for most people with a full-time job.</p>
<p>The calculator shows your take-home pay per month and per year and how many months it will take to hit your savings goal. It also estimates what three years of that income could grow to if you invest it at a 7% average return.</p>
<h2 id="realistic-rates">Realistic hourly rates by side hustle</h2>
<table class="data"><thead><tr><th>Side hustle</th><th>Typical pay</th><th>Notes</th></tr></thead><tbody>
<tr><td>Food & grocery delivery</td><td>$15–$25/hr</td><td>Before gas; peak hours pay best</td></tr>
<tr><td>Rideshare driving</td><td>$18–$30/hr gross</td><td>Subtract 25–35% for car costs</td></tr>
<tr><td>Pet sitting / dog walking</td><td>$15–$30 per visit</td><td>Repeat clients make it steady</td></tr>
<tr><td>Cleaning & rental turnovers</td><td>$25–$45/hr</td><td>Supplies are a small cost</td></tr>
<tr><td>Freelance writing or design</td><td>$25–$75/hr</td><td>Grows with portfolio and niche</td></tr>
<tr><td>Digital marketing for small businesses</td><td>$300–$1,500 per client/mo</td><td>Retainers create predictable income</td></tr>
</tbody></table>
<div class="callout"><strong>Make the goal real:</strong> Set up a separate savings account just for side hustle money and move your take-home there every payday.</div>
HTML,
        'faq' => [
            ['q' => 'How much should I set aside for taxes on side hustle income?', 'a' => 'A common rule is 25–30% of profit. It covers the 15.3% self-employment tax plus federal and state income tax for most earners. Use our side hustle tax calculator for a closer estimate.'],
            ['q' => 'How many hours a week should a side hustle take?', 'a' => 'Most people sustain 5–15 hours a week alongside a full-time job. Start small and add hours once the hustle proves it pays.'],
            ['q' => 'Is $1,000 a month from a side hustle realistic?', 'a' => 'Yes. At $25 an hour, about 10 hours a week gets you close to $1,000 a month before taxes. Higher-skill work gets there in fewer hours.'],
        ],
    ],
    'gig-earnings-calculator' => [
        'title' => 'Uber, Lyft & DoorDash Earnings Calculator (True Hourly Pay)',
        'description' => 'Free gig driver earnings calculator for Uber, Lyft, DoorDash and Instacart. See your true hourly pay after gas and car wear, plus your IRS mileage deduction.',
        'h1' => 'Gig Driver Earnings Calculator: Your True Hourly Pay',
        'gear' => ['phone-mount', 'dash-cam', 'mileage-log', 'car-charger'],
        'guides' => ['lyft-uber', 'side-hustles-you-can-start-with-just-your-smartphone', 'best-side-hustles-in-indianapolis', 'best-side-hustles-in-sacramento', 'side-job-hustles-in-texas-emerging-trends-and-opportunities-for-all'],
        'body' => <<<'HTML'
<h2 id="why-true-hourly">Why your app's hourly number isn't your real pay</h2>
<p>Uber, Lyft, DoorDash and Instacart show what you earned while online. They don't subtract gas, oil changes, tires and the value your car loses with every mile. Those costs often take 25–40% of what the app shows. This calculator subtracts them so you can compare gig driving honestly with any other side hustle.</p>
<h2 id="inputs">What to enter</h2>
<ul>
<li><strong>Weekly app earnings:</strong> total payouts including tips, from your earnings tab.</li>
<li><strong>Hours online:</strong> count waiting time too, not just time on trips.</li>
<li><strong>Miles:</strong> every mile with the app on, including driving to pickups and back from drop-offs.</li>
<li><strong>Maintenance & depreciation:</strong> $0.10–$0.15 a mile is a reasonable estimate for most sedans.</li>
</ul>
<h2 id="mileage-deduction">The mileage deduction</h2>
<p>For taxes, most drivers deduct the IRS standard mileage rate instead of actual car costs. For 2026 the IRS set 72.5¢ a mile for January through June and raised it to 76¢ for miles driven from July 1. The deduction often wipes out most of the taxable profit from driving, but only if you keep a mileage log. An app or a simple [[amazon:mileage-log|mileage log book]] both work.</p>
<div class="callout"><strong>Raise your true hourly:</strong> Drive only the busiest windows (Friday and Saturday nights, airport rushes, big events). Decline long unpaid return trips and run two apps at once to cut idle time.</div>
HTML,
        'faq' => [
            ['q' => 'How much do Uber and Lyft drivers really make per hour?', 'a' => 'Gross pay commonly lands between $18 and $30 an hour depending on city and timing. After gas and car wear, many drivers net roughly $12–$22 an hour.'],
            ['q' => 'What is the IRS mileage rate for 2026?', 'a' => 'The IRS set 72.5 cents per mile for January–June 2026 and raised it to 76 cents per mile for business miles driven from July 1, 2026. Check IRS.gov for any later change.'],
            ['q' => 'Is DoorDash or Uber better for earnings?', 'a' => 'It depends on your market. Delivery suits shorter shifts and smaller cars, and rideshare pays more per trip around events and airports. Many drivers run both and keep the better offer.'],
        ],
    ],
    'self-employment-tax-calculator' => [
        'title' => 'Side Hustle Tax Calculator 2026: Self-Employment Tax',
        'description' => 'Free 2026 side hustle tax calculator. Estimate self-employment tax, extra federal income tax and state tax on side income, plus your quarterly payments.',
        'h1' => 'Side Hustle Tax Calculator (Self-Employment Tax, 2026)',
        'gear' => ['receipt-scanner', 'book-taxes', 'mileage-log'],
        'guides' => ['exploring-the-world-of-side-hustles-in-2023', 'fiverr', 'lyft-uber', 'shopify', 'udemy'],
        'body' => <<<'HTML'
<h2 id="how-side-hustle-income-is-taxed">How side hustle income is taxed</h2>
<p>Side hustle profit is hit by two federal taxes. <strong>Self-employment tax</strong> is 15.3% on 92.35% of your net earnings: 12.4% Social Security (up to the $184,500 wage base for 2026, shared with your W-2 wages) plus 2.9% Medicare. <strong>Income tax</strong> is charged at your top bracket, because side income stacks on top of your job. You can deduct half of your self-employment tax, and the calculator accounts for that.</p>
<h2 id="quarterly-payments">Do you need to pay quarterly?</h2>
<p>If you expect to owe $1,000 or more when you file, the IRS expects estimated payments each quarter. The usual due dates are April 15, June 15, September 15 and January 15. If you also have a W-2 job, you can raise your paycheck withholding instead and skip the quarterly vouchers.</p>
<h2 id="lower-your-bill">Ways to lower your side hustle taxes</h2>
<ol class="steps">
<li><strong>Track every expense.</strong> Supplies, software, phone and internet share, and platform fees are all deductible.</li>
<li><strong>Log your miles.</strong> Business driving is often the biggest single deduction for gig workers.</li>
<li><strong>Look into the QBI deduction.</strong> Many sole proprietors can deduct up to 20% of qualified business income from income tax.</li>
<li><strong>Open a solo 401(k) or SEP-IRA.</strong> Contributions cut your income tax and build retirement savings.</li>
</ol>
<div class="callout callout-warn"><strong>Note:</strong> This is an educational estimate, not tax advice. Your credits, deductions and local taxes affect what you owe, so talk to a tax professional for your own situation.</div>
HTML,
        'faq' => [
            ['q' => 'How much tax do I pay on a side hustle?', 'a' => 'Usually 25–35% of profit in total: 15.3% self-employment tax on 92.35% of net earnings, plus federal income tax at your marginal rate and any state income tax.'],
            ['q' => 'Do I pay taxes if my side hustle made less than $400?', 'a' => 'You owe no self-employment tax below $400 of net earnings, but the income is still reportable and may be subject to income tax.'],
            ['q' => 'Will I get a 1099 for my side hustle?', 'a' => 'Platforms issue 1099-NEC or 1099-K forms above reporting thresholds, but you must report all income whether or not you receive a form.'],
        ],
    ],
    'course-revenue-calculator' => [
        'title' => 'Online Course Revenue Calculator: Udemy vs Skillshare vs Thinkific',
        'description' => 'Compare what your online course could earn on Udemy, Skillshare and Thinkific. Free calculator with revenue share, royalties, fees and plan costs built in.',
        'h1' => 'Online Course Revenue Calculator',
        'gear' => ['usb-mic', 'ring-light', 'webcam', 'book-dotcom'],
        'guides' => ['udemy', 'skillshare', 'thinkific', 'coursera'],
        'body' => <<<'HTML'
<h2 id="how-each-platform-pays">How each platform pays course creators</h2>
<table class="data"><thead><tr><th>Platform</th><th>How you're paid</th><th>Who brings students</th></tr></thead><tbody>
<tr><td><a href="/udemy/">Udemy</a></td><td>37% of organic marketplace sales; 97% of sales from your own coupon links</td><td>Mostly Udemy</td></tr>
<tr><td><a href="/skillshare/">Skillshare</a></td><td>A share of a monthly royalty pool based on minutes watched</td><td>Skillshare</td></tr>
<tr><td><a href="/thinkific/">Thinkific</a></td><td>You keep 100% of sales minus payment processing and your plan fee</td><td>You</td></tr>
</tbody></table>
<p>The calculator shows the trade-off. Marketplaces take a big cut but supply the buyers. Your own Thinkific site keeps almost everything, but every sale depends on the audience you build. Many creators do both: a Udemy course for discovery and a premium version on Thinkific for students who want more.</p>
<div class="callout"><strong>Rates change.</strong> Udemy, Skillshare and Thinkific all adjust revenue shares and pricing over time, so check each platform's current terms before you plan around a number.</div>
HTML,
        'faq' => [
            ['q' => 'How much can you make selling an online course?', 'a' => 'Most first courses earn $50–$500 a month. Courses in strong niches with an audience behind them can earn thousands. Results depend on the topic, the quality and how much you promote it.'],
            ['q' => 'Is Udemy or Thinkific better for a first course?', 'a' => 'Udemy suits creators with no audience because it supplies buyers. Thinkific suits creators who already have an email list or social following and want to keep more of each sale.'],
            ['q' => 'How does Skillshare calculate teacher pay?', 'a' => 'Skillshare pools a share of subscription revenue each month and splits it among teachers by premium minutes watched, so longer watch time means more pay.'],
        ],
    ],
    'freelance-rate-calculator' => [
        'title' => 'Freelance Rate Calculator: What to Charge (Incl. Fiverr Fees)',
        'description' => 'Work out your freelance hourly rate and gig price. Free calculator includes Fiverr\'s 20% fee, taxes and costs so you know exactly what to charge clients.',
        'h1' => 'Freelance Rate Calculator: What Should You Charge?',
        'gear' => ['headset', 'laptop-stand', 'book-company-of-one'],
        'guides' => ['fiverr', 'digital-marketing-side-hustle', 'thinkific', 'semrush'],
        'body' => <<<'HTML'
<h2 id="work-backward">Price from your goal, not from guesses</h2>
<p>New freelancers tend to undercharge because they pick a number that "feels fair" and forget about fees, taxes and unpaid admin time. This calculator starts from the take-home you want each month and adds back taxes, costs and platform fees to get the rate you need.</p>
<h2 id="fiverr-fee">Accounting for Fiverr's fee</h2>
<p><a href="/fiverr/">Fiverr</a> keeps 20% of every order, tips included. A $100 gig pays you $80. To net $100, you need to charge $125. Direct clients usually cost less in fees (often just 3% payment processing), which is why most freelancers move repeat buyers to direct invoicing once the relationship allows it.</p>
<h2 id="raise-rates">When to raise your rates</h2>
<ul>
<li>You're booked more than two weeks out.</li>
<li>More than half of new leads say yes without negotiating.</li>
<li>You've added a skill, certification or strong portfolio piece.</li>
</ul>
<div class="callout"><strong>Package it:</strong> Clients compare packages, not hourly rates. Build three tiers so most buyers pick the middle one.</div>
HTML,
        'faq' => [
            ['q' => 'How much should a beginner freelancer charge?', 'a' => 'Many beginners start at $20–$35 an hour (or the gig equivalent) and raise prices after 5–10 good reviews. Use the calculator to make sure your starting rate still meets your income goal.'],
            ['q' => 'How much does Fiverr take from sellers?', 'a' => 'Fiverr keeps 20% of each order, including tips, so you receive 80% of the price.'],
            ['q' => 'Should I charge hourly or per project?', 'a' => 'Per project (or package) usually earns more, because you are paid for results and speed instead of time. Hourly suits ongoing work with an unclear scope.'],
        ],
    ],
    'product-profit-calculator' => [
        'title' => 'Product Profit Calculator: Shopify Margin & Break-Even',
        'description' => 'Free product profit calculator for Shopify, Etsy and Amazon sellers. Find profit per order, margin, monthly profit and break-even orders in seconds.',
        'h1' => 'Product Profit Calculator (Margin & Break-Even)',
        'gear' => ['label-printer', 'shipping-scale', 'light-box', 'poly-mailers'],
        'guides' => ['shopify', 'side-hustles-you-can-start-with-just-your-smartphone', 'digital-marketing-side-hustle'],
        'body' => <<<'HTML'
<h2 id="margin-basics">The numbers every store owner should know</h2>
<p>Revenue is vanity and profit is sanity. A $34 t-shirt can make you $10 or lose you $3 depending on print cost, shipping, payment fees and how much you spend on ads to sell it. This calculator breaks one order down into its parts so you can see where the money goes.</p>
<ul>
<li><strong>Profit per order:</strong> price minus product cost, shipping, payment processing (about 2.9% + 30¢ on <a href="/shopify/">Shopify</a>'s Basic plan) and ad spend.</li>
<li><strong>Margin:</strong> profit as a share of price. Aim for 30% or more.</li>
<li><strong>Break-even orders:</strong> how many sales cover your monthly plan and app fees.</li>
<li><strong>Max ad spend per order:</strong> the most you can pay to acquire a customer before you lose money.</li>
</ul>
<div class="callout"><strong>Easy wins:</strong> Bundles and "free shipping over $X" raise your average order value, which spreads ad and shipping costs across more revenue.</div>
HTML,
        'faq' => [
            ['q' => 'What is a good profit margin for a Shopify store?', 'a' => 'After product, shipping, fees and ads, 20–40% is healthy for most small stores. Print-on-demand often runs thinner, around 15–30%, and digital products can exceed 80%.'],
            ['q' => 'How do I calculate break-even for my store?', 'a' => 'Divide your monthly fixed costs (plan, apps, subscriptions) by your profit per order. The result is the number of orders you need each month to break even.'],
            ['q' => 'How much should I spend on ads per sale?', 'a' => 'Stay below your pre-ad profit per order. The calculator shows that ceiling as "max ad spend per order to break even".'],
        ],
    ],
    'affiliate-commission-calculator' => [
        'title' => 'Affiliate Commission Calculator: Project Affiliate Income',
        'description' => 'Project your affiliate marketing income from traffic, click-through rate, conversion rate and commission. Free calculator with 12-month growth projection.',
        'h1' => 'Affiliate Commission Calculator',
        'gear' => ['book-this-is-mkt', 'book-show-your-work', 'usb-mic'],
        'guides' => ['semrush', 'thinkific', 'shopify', 'digital-marketing-side-hustle'],
        'body' => <<<'HTML'
<h2 id="the-formula">The affiliate income formula</h2>
<p>Affiliate income = visitors × click-through rate × conversion rate × commission. Small changes in any one of these move the result a lot. Doubling click-through from 2% to 4%, for example, doubles your income without a single extra visitor.</p>
<h2 id="benchmarks">Typical benchmarks</h2>
<table class="data"><thead><tr><th>Metric</th><th>Typical range</th><th>How to improve it</th></tr></thead><tbody>
<tr><td>Click-through to offer</td><td>1–8%</td><td>Comparison tables, honest reviews, clear buttons</td></tr>
<tr><td>Conversion after click</td><td>0.5–5%</td><td>Send warm readers to free trials or deals</td></tr>
<tr><td>Commission per sale</td><td>$5–$450</td><td>Promote software and recurring programs</td></tr>
</tbody></table>
<p>High-ticket software programs pay the most per sale. <a href="/semrush/">Semrush</a> pays a flat commission per subscription and <a href="/thinkific/">Thinkific</a> pays recurring commissions, which is why they are popular with bloggers and YouTubers.</p>
<div class="callout"><strong>Disclose it:</strong> The FTC requires a clear affiliate disclosure near your links, and most programs make it a condition of joining.</div>
HTML,
        'faq' => [
            ['q' => 'How much traffic do I need to make money with affiliate marketing?', 'a' => 'With a $200 commission, 4% click-through and 2% conversion, about 1,250 visitors a month earns roughly one sale ($200). Lower-commission programs need far more traffic.'],
            ['q' => 'What is a good affiliate conversion rate?', 'a' => '1–3% of clicks converting is common. Free-trial offers and warm, review-style content convert higher.'],
            ['q' => 'Which affiliate programs pay the most?', 'a' => 'Software and SaaS programs usually pay the most per sale, often $50–$450 or recurring percentages, compared with 1–10% on most physical products.'],
        ],
    ],
];
