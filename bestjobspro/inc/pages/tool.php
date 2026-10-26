<?php
/** @var string $toolSlug */
[$title, $desc, $ic, $key] = TOOLS[$toolSlug];

// Per-tool SEO copy: meta, intro, how-it-works paragraphs, tips, FAQs and related reading.
$copy = [
    'paycheck-calculator' => [
        'seo' => 'Texas Paycheck Calculator 2026 (Hourly & Salary)',
        'meta' => 'Free Texas paycheck calculator for 2026. Convert hourly pay or salary to weekly, biweekly, monthly and yearly take-home after federal tax and FICA.',
        'intro' => 'See what an hourly wage or salary is really worth in Texas. Enter your pay and hours to get gross and estimated take-home pay per week, paycheck, month and year, including overtime.',
        'how' => ['Your gross pay is your hourly rate times regular hours, plus overtime at 1.5 times your rate, times the weeks you work. For salaried roles we start from the annual figure.', 'From that we subtract an estimate of federal income tax (using the 2026 standard deduction and brackets for your filing status) plus Social Security (6.2%) and Medicare (1.45%). Texas has no state income tax, so there is nothing else to take out at the state level.', 'Your real paycheck can differ because of your W-4 choices, health insurance, retirement contributions and other pre-tax deductions.'],
        'tips' => ['Compare offers by take-home, not just hourly rate: a $1/hr raise at 40 hours is about $2,080 a year before tax.', 'Overtime adds up fast: five extra hours a week at $20/hr is roughly $7,800 a year in gross pay.', 'Ask whether a temp role converts to permanent and when benefits start; that changes the real value of an offer.'],
        'faqs' => [
            ['q' => 'Does Texas have a state income tax?', 'a' => 'No. Texas does not tax personal income, so your paycheck only has federal income tax, Social Security and Medicare withheld, plus any benefits or deductions you choose.'],
            ['q' => 'How much is $20 an hour per year in Texas?', 'a' => 'At 40 hours a week for 52 weeks, $20 an hour is $41,600 a year before taxes. Use the calculator to see your estimated take-home based on your filing status.'],
            ['q' => 'How is overtime calculated in Texas?', 'a' => 'Texas follows the federal Fair Labor Standards Act: non-exempt employees earn at least 1.5 times their regular rate for hours over 40 in a workweek.'],
            ['q' => 'Why is my actual paycheck different from the estimate?', 'a' => 'Withholding depends on your W-4, and many paychecks also include health insurance premiums, retirement contributions and other deductions. The calculator gives a planning estimate, not a pay stub.'],
        ],
        'related' => ['flexible-scheduling-for-parents-in-todays-workforce', 'on-demand-jobs-how-flexible-work-is-changing-careers', 'ways-to-diversify-income-streams'],
    ],
    'job-match-quiz' => [
        'seo' => 'Job Match Quiz: What Job Is Right for Me?',
        'meta' => 'Take the free Best Jobs Pro job match quiz. Six questions reveal which jobs fit you: office, warehouse, skilled trades, customer service or driving.',
        'intro' => 'Not sure which job to go after next? Answer six quick questions about how you like to work and get matched with the job types, and the open positions, that fit you best.',
        'how' => ['Each answer leans toward one of five job families that Best Jobs Pro recruits for: office and admin, warehouse and labor, skilled trades, customer service, and driving.', 'At the end we total your answers, show how strongly you match each family, and list current openings that fit your top results.', 'It is a starting point, not a test. Plenty of people do well in more than one family, and our recruiters can talk you through the options.'],
        'tips' => ['Answer for how you want to work, not just what you have done before.', 'If two families score closely, apply for roles in both; it widens your options.', 'Mention your quiz result when a recruiter calls; it helps us understand you faster.'],
        'faqs' => [
            ['q' => 'How do I know what job is right for me?', 'a' => 'Think about where you like to work, what people say you are good at, the schedule you want and what matters most in a job. The quiz turns those answers into job families that fit.'],
            ['q' => 'What jobs can I get with no experience?', 'a' => 'Warehouse packing and stocking, general labor, housekeeping, food service and many customer service roles often hire people without experience and train on the job.'],
            ['q' => 'Is the quiz free?', 'a' => 'Yes. It is free, takes about a minute and does not ask for your email or any personal details.'],
        ],
        'related' => ['easy-jobs-you-can-do-and-apply-for-in-syracuse-ny', 'skills-needed-for-remote-digital-work', 'on-demand-jobs-how-flexible-work-is-changing-careers'],
    ],
    'resume-keyword-checker' => [
        'seo' => 'Free Résumé Keyword Checker (ATS Match Score)',
        'meta' => 'Paste a job description and your résumé to get a free keyword match score. See which ATS keywords you have and which are missing. Private, no sign-up.',
        'intro' => 'Most employers use applicant tracking systems (ATS) and quick human scans to shortlist résumés. This free checker compares your résumé with a job posting and shows the important keywords you match and the ones you are missing.',
        'how' => ['We pull the most important words and two-word phrases from the job description, skipping filler like "the," "team" and "responsibilities."', 'Then we check which of those terms appear in your résumé and calculate a match score.', 'Everything happens in your browser. Nothing you paste is uploaded or saved.'],
        'tips' => ['Aim for a score of 60–80% for a role you are qualified for. 100% usually means keyword stuffing.', 'Use the exact phrasing from the posting where it is true: "data entry," not just "typing."', 'Put key skills in a short summary at the top and prove them in bullet points with numbers.'],
        'faqs' => [
            ['q' => 'What is an ATS keyword?', 'a' => 'It is a skill, tool, certification or job title from the job description that an applicant tracking system or recruiter looks for when screening résumés, such as "forklift certified," "QuickBooks" or "customer service."'],
            ['q' => 'What is a good résumé match score?', 'a' => 'For a job you are genuinely qualified for, 60 to 80 percent is strong. Lower scores usually mean your résumé describes the same skills in different words.'],
            ['q' => 'Should I add every missing keyword?', 'a' => 'Only the ones that are true for you. Add them naturally, ideally in a bullet that shows a result. Listing skills you do not have will come out in the interview.'],
        ],
        'related' => ['skills-needed-for-remote-digital-work', 'building-a-professional-freelancer-profile', 'easy-jobs-you-can-do-and-apply-for-in-syracuse-ny'],
    ],
    'self-employment-tax-calculator' => [
        'seo' => '1099 Self-Employment Tax Calculator (2026)',
        'meta' => 'Estimate 2026 self-employment tax, federal income tax and quarterly estimated payments for 1099 independent contractors. Free calculator, Texas-friendly.',
        'intro' => 'Working as an independent contractor, freelancer or gig worker? No one withholds taxes for you. Estimate your self-employment tax, federal income tax and quarterly payments so April does not bring a surprise.',
        'how' => ['Net profit is your 1099 income minus business expenses. Self-employment tax is 15.3% of 92.35% of that profit: 12.4% for Social Security (up to the 2026 wage base of $184,500, shared with any W-2 wages) and 2.9% for Medicare.', 'For income tax, half of your self-employment tax is deducted, then the standard deduction and the 20% qualified business income (QBI) deduction are applied before using 2026 federal brackets. Texas has no state income tax.', 'Divide the total by four for an even quarterly estimated payment. This is general information, not tax advice. Talk to a tax professional about your situation.'],
        'tips' => ['Set aside 25–30% of every payment in a separate savings account the day it arrives.', 'Track mileage and expenses all year; every deductible dollar lowers both income tax and self-employment tax.', 'If you also have a W-2 job, raising your withholding there can cover tax on your side income.'],
        'faqs' => [
            ['q' => 'How much should I set aside for taxes as a 1099 contractor?', 'a' => 'Many contractors set aside 25 to 30 percent of net income to cover self-employment tax and federal income tax. Use the calculator to get a figure for your income and filing status.'],
            ['q' => 'When are quarterly estimated taxes due for 2026?', 'a' => 'For 2026 income, estimated payments are due April 15, 2026, June 15, 2026, September 15, 2026 and January 15, 2027.'],
            ['q' => 'What is the self-employment tax rate?', 'a' => 'It is 15.3 percent: 12.4 percent for Social Security up to the annual wage base and 2.9 percent for Medicare, applied to 92.35 percent of net self-employment earnings.'],
            ['q' => 'Do independent contractors in Texas pay state income tax?', 'a' => 'No. Texas has no personal income tax, so contractors there pay federal income tax and self-employment tax only.'],
        ],
        'related' => ['independent-contractor-tax-responsibilities', 'on-demand-jobs-how-flexible-work-is-changing-careers', 'how-freelance-marketplaces-work'],
    ],
    'freelance-rate-calculator' => [
        'seo' => 'Freelance Rate Calculator: What Should I Charge?',
        'meta' => 'Work out your freelance hourly rate from your income goal, costs, time off, taxes and platform fees. Free calculator for freelancers and contractors.',
        'intro' => 'Charging too little is the most common freelancing mistake. Start from the income you want, add your costs, taxes, time off and marketplace fees, and see the minimum hourly and day rate that gets you there.',
        'how' => ['We add your take-home goal and business costs, gross that up for your tax set-aside, then gross it up again for the platform fee, because fees come off the top of what clients pay.', 'Billable hours are your weekly billable hours times the weeks you actually work. Most freelancers bill 20–30 hours a week; the rest goes to admin, sales and learning.', 'The result is your floor. Price above it when you can show results.'],
        'tips' => ['Do not count every working hour as billable; plan for 60–75% at best.', 'Marketplace fees vary widely, so compare platforms and factor the fee into your rate.', 'Raise rates for new clients first, then for existing ones with notice.'],
        'faqs' => [
            ['q' => 'How do I calculate my freelance hourly rate?', 'a' => 'Add your desired take-home pay and business costs, adjust for taxes and platform fees, and divide by the hours you can realistically bill in a year. The calculator does this for you.'],
            ['q' => 'Why should freelancers charge more than employees earn per hour?', 'a' => 'Freelancers pay both halves of payroll tax, fund their own benefits and time off, cover equipment and software, and spend unbilled time finding work.'],
            ['q' => 'How many billable hours should a freelancer plan for?', 'a' => 'Most freelancers bill 20 to 30 hours in a 40-hour week. The rest goes to marketing, proposals, invoicing and skill-building.'],
        ],
        'related' => ['building-a-professional-freelancer-profile', 'how-freelance-marketplaces-work', 'ways-to-diversify-income-streams'],
    ],
    'cost-of-vacancy-calculator' => [
        'seo' => 'Cost of Vacancy & Bad Hire Calculator',
        'meta' => 'Calculate what an unfilled position and a bad hire cost your business, and how much faster staffing saves. Free cost of vacancy calculator from Best Jobs Pro.',
        'intro' => 'An open seat is not free. Work slows, overtime climbs and good people burn out covering for it. Estimate the daily cost of a vacancy, the hidden cost of a bad hire, and what filling the role faster could save.',
        'how' => ['Cost per open day is the role\'s annual pay times its output multiplier (what that person produces relative to their pay), spread over 260 working days.', 'Vacancy cost multiplies that by the working days the seat stays empty. We add the cost of your team\'s time spent hiring.', 'The bad-hire figure uses 30% of first-year pay, the estimate the U.S. Department of Labor has cited. Agency fees vary, so they are not included; ask us for a quote.'],
        'tips' => ['Start recruiting before someone leaves when you can; notice periods are short.', 'A clear job posting with pay listed attracts better-fit applicants faster.', 'Temp-to-hire lets you test fit on the job and lowers the risk of a bad hire.'],
        'faqs' => [
            ['q' => 'What is the cost of vacancy?', 'a' => 'It is the value of the work that does not get done while a position is unfilled, plus related costs like overtime for coworkers and the time spent recruiting.'],
            ['q' => 'How much does a bad hire cost?', 'a' => 'The U.S. Department of Labor has estimated a bad hire can cost at least 30 percent of the employee\'s first-year earnings, before counting lost productivity and morale.'],
            ['q' => 'How can a staffing agency reduce hiring costs?', 'a' => 'An agency like Best Jobs Pro keeps a pool of screened candidates, handles sourcing, interviews, background checks and drug screening, and can often fill roles faster, which shortens the vacancy and reduces the risk of a bad hire.'],
        ],
        'related' => ['top-5-advantages-of-hiring-an-agency-to-find-the-best-applicants-in-texas', 'flexible-scheduling-for-parents-in-todays-workforce', 'skills-needed-for-remote-digital-work'],
    ],
][$toolSlug];

$path = '/career-tools/' . $toolSlug . '/';
$crumbs = [['Career Tools', '/career-tools/'], [$title, $path]];
page_start([
    'title'       => $copy['seo'] . ' | Best Jobs Pro',
    'description' => $copy['meta'],
    'path'        => $path,
    'crumbs'      => $crumbs,
    'schema'      => [
        ['@type' => 'WebApplication', 'name' => $title, 'url' => url($path), 'applicationCategory' => 'BusinessApplication', 'operatingSystem' => 'Any', 'browserRequirements' => 'Requires JavaScript', 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'provider' => ['@id' => SITE_URL . '/#organization']],
        faq_schema($copy['faqs']),
    ],
]);
page_hero(e($title), e($copy['intro']), $crumbs, '', 'Free career tool');
?>
<section class="section">
  <div class="wrap" style="max-width:1040px">
    <div class="reveal in"><?= tool_widget($key) ?></div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap split" style="align-items:start">
    <div class="reveal">
      <h2>How the <?= e($title) ?> works</h2>
<?php foreach ($copy['how'] as $p): ?>
      <p><?= e($p) ?></p>
<?php endforeach; ?>
    </div>
    <div class="reveal">
      <div class="card" style="padding:30px">
        <div class="card__ico"><?= icon('star') ?></div>
        <h3>Tips from our recruiters</h3>
        <ul class="checks" style="margin:0">
<?php foreach ($copy['tips'] as $t): ?>
          <li><?= e($t) ?></li>
<?php endforeach; ?>
        </ul>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap"><?= faq_block($copy['faqs']) ?></div>
</section>
<section class="related">
  <div class="wrap">
    <div class="section__head"><h2>Related reading</h2></div>
    <div class="posts">
<?php foreach (array_filter(array_map('get_post', $copy['related'])) as $p) echo post_card($p); ?>
    </div>
    <p style="text-align:center;margin-top:30px"><a class="btn btn--outline" href="/career-tools/">See all career tools <?= icon('arrow') ?></a></p>
  </div>
</section>
<?= cta_band() ?>
<?php page_end(['/assets/js/tools.js']);
