<?php
// Interactive career tools. Markup lives here; the maths runs in assets/js/tools.js.

function tool_slug_for(string $key): ?string
{
    foreach (TOOLS as $slug => $t) {
        if ($t[3] === $key) {
            return $slug;
        }
    }
    return null;
}

function num_field(string $name, string $label, $value, string $prefix = '', string $suffix = '', string $step = 'any', string $min = '0'): string
{
    $id = 't-' . $name . '-' . substr(md5(uniqid('', true)), 0, 5);
    return '<label class="tfield" for="' . $id . '"><span class="tfield__label">' . e($label) . '</span><span class="tfield__box">'
        . ($prefix ? '<span class="tfield__fix">' . e($prefix) . '</span>' : '')
        . '<input id="' . $id . '" type="number" inputmode="decimal" name="' . e($name) . '" value="' . e($value) . '" step="' . e($step) . '" min="' . e($min) . '">'
        . ($suffix ? '<span class="tfield__fix">' . e($suffix) . '</span>' : '')
        . '</span></label>';
}

function select_field(string $name, string $label, array $options, string $selected = ''): string
{
    $id = 't-' . $name . '-' . substr(md5(uniqid('', true)), 0, 5);
    $out = '<label class="tfield" for="' . $id . '"><span class="tfield__label">' . e($label) . '</span><span class="tfield__box"><select id="' . $id . '" name="' . e($name) . '">';
    foreach ($options as $val => $text) {
        $out .= '<option value="' . e($val) . '"' . ((string)$val === $selected ? ' selected' : '') . '>' . e($text) . '</option>';
    }
    return $out . '</select></span></label>';
}

/** $embedded = true when the tool sits inside a blog post or another page. */
function tool_widget(string $key, bool $embedded = false): string
{
    $slug = tool_slug_for($key);
    if (!$slug) {
        return '';
    }
    [$title, $desc, $ico] = TOOLS[$slug];
    $head = '<div class="tool__head"><span class="tool__ico">' . icon($ico) . '</span><div><p class="tool__kicker">Free Best Jobs Pro tool</p>'
        . '<p class="tool__title">' . e($title) . '</p></div></div>';
    $foot = $embedded
        ? '<p class="tool__more"><a href="/career-tools/' . $slug . '/">Open the full ' . e($title) . ' ' . icon('arrow') . '</a></p>'
        : '';

    $body = match ($key) {
        'paycheck' => tool_paycheck(),
        'contractor-tax' => tool_contractor_tax(),
        'freelance-rate' => tool_freelance_rate(),
        'resume-keywords' => tool_resume_keywords(),
        'job-quiz' => tool_job_quiz(),
        'vacancy-cost' => tool_vacancy_cost(),
    };
    return '<div class="tool' . ($embedded ? ' tool--embedded' : '') . '" data-tool="' . e($key) . '">' . $head . $body . $foot . '</div>';
}

function tool_paycheck(): string
{
    return '<form class="tool__form" onsubmit="return false">'
        . '<div class="seg" role="radiogroup" aria-label="Pay type"><label><input type="radio" name="mode" value="hourly" checked><span>Hourly</span></label><label><input type="radio" name="mode" value="salary"><span>Salary</span></label></div>'
        . '<div class="tool__grid">'
        . num_field('rate', 'Hourly wage', '18', '$', '/hr', '0.25')
        . num_field('hours', 'Hours per week', '40', '', 'hrs', '1')
        . num_field('salary', 'Annual salary', '45000', '$', '/yr', '500')
        . num_field('ot', 'Overtime hours per week', '0', '', 'hrs', '1')
        . select_field('filing', 'Filing status', ['single' => 'Single', 'married' => 'Married filing jointly', 'head' => 'Head of household'])
        . num_field('weeks', 'Weeks worked per year', '52', '', 'wks', '1')
        . '</div></form>'
        . '<div class="tool__out" aria-live="polite">'
        . '<div class="kpis"><div class="kpi kpi--hl"><span>Estimated take-home / year</span><strong data-out="net">-</strong></div><div class="kpi"><span>Gross / year</span><strong data-out="gross">-</strong></div></div>'
        . '<div class="kpis kpis--4"><div class="kpi"><span>Per month (net)</span><strong data-out="month">-</strong></div><div class="kpi"><span>Per 2 weeks (net)</span><strong data-out="biweek">-</strong></div><div class="kpi"><span>Per week (net)</span><strong data-out="week">-</strong></div><div class="kpi"><span>Effective hourly (net)</span><strong data-out="hourly">-</strong></div></div>'
        . '<div class="bar" data-out="bar" aria-hidden="true"><span class="bar__net"></span><span class="bar__fed"></span><span class="bar__fica"></span></div>'
        . '<ul class="legend"><li><i class="l-net"></i>Take-home <b data-out="netpct"></b></li><li><i class="l-fed"></i>Federal income tax <b data-out="fed"></b></li><li><i class="l-fica"></i>Social Security + Medicare <b data-out="fica"></b></li><li><i class="l-tx"></i>Texas state income tax <b>$0</b></li></ul>'
        . '<p class="tool__note">Estimate for the 2026 tax year using the standard deduction and 2026 federal brackets. Texas has no state income tax. Overtime is paid at 1.5×. Actual withholding depends on your W-4, benefits and pre-tax deductions.</p>'
        . '</div>';
}

function tool_contractor_tax(): string
{
    return '<form class="tool__form" onsubmit="return false"><div class="tool__grid">'
        . num_field('income', '1099 / self-employed income (year)', '60000', '$', '', '500')
        . num_field('expenses', 'Business expenses (year)', '8000', '$', '', '100')
        . select_field('filing', 'Filing status', ['single' => 'Single', 'married' => 'Married filing jointly', 'head' => 'Head of household'])
        . num_field('w2', 'Other W-2 wages (year)', '0', '$', '', '500')
        . '</div></form>'
        . '<div class="tool__out" aria-live="polite">'
        . '<div class="kpis"><div class="kpi kpi--hl"><span>Quarterly estimated payment</span><strong data-out="quarter">-</strong></div><div class="kpi"><span>Total estimated federal tax</span><strong data-out="total">-</strong></div></div>'
        . '<div class="kpis kpis--4"><div class="kpi"><span>Net profit</span><strong data-out="profit">-</strong></div><div class="kpi"><span>Self-employment tax</span><strong data-out="se">-</strong></div><div class="kpi"><span>Income tax (est.)</span><strong data-out="inc">-</strong></div><div class="kpi"><span>Set aside per $100 earned</span><strong data-out="per100">-</strong></div></div>'
        . '<div class="deadlines"><p class="deadlines__t">' . icon('calendar') . ' 2026 tax-year payment deadlines</p><ol data-out="deadlines"><li><b>Apr 15, 2026</b><span>Q1</span></li><li><b>Jun 15, 2026</b><span>Q2</span></li><li><b>Sep 15, 2026</b><span>Q3</span></li><li><b>Jan 15, 2027</b><span>Q4</span></li></ol></div>'
        . '<p class="tool__note">General estimate, not tax advice. Uses 2026 figures: 15.3% self-employment tax on 92.35% of net profit (Social Security portion capped at the $184,500 wage base), half of SE tax deducted, the 20% QBI deduction, the standard deduction and 2026 federal brackets. Texas has no state income tax. If you have W-2 withholding, it already covers part of the income tax shown.</p>'
        . '</div>';
}

function tool_freelance_rate(): string
{
    return '<form class="tool__form" onsubmit="return false"><div class="tool__grid">'
        . num_field('target', 'Take-home income goal (year)', '60000', '$', '', '1000')
        . num_field('expenses', 'Business costs (software, gear, insurance)', '6000', '$', '/yr', '100')
        . num_field('hours', 'Billable hours per week', '25', '', 'hrs', '1')
        . num_field('weeks', 'Weeks off per year', '6', '', 'wks', '1')
        . num_field('fee', 'Platform / marketplace fee', '10', '', '%', '0.5')
        . num_field('tax', 'Tax set-aside', '25', '', '%', '1')
        . '</div></form>'
        . '<div class="tool__out" aria-live="polite">'
        . '<div class="kpis"><div class="kpi kpi--hl"><span>Minimum hourly rate</span><strong data-out="rate">-</strong></div><div class="kpi"><span>Day rate (8 hrs)</span><strong data-out="day">-</strong></div></div>'
        . '<div class="kpis kpis--4"><div class="kpi"><span>Billable hours / year</span><strong data-out="hrs">-</strong></div><div class="kpi"><span>Revenue needed</span><strong data-out="rev">-</strong></div><div class="kpi"><span>Paid in fees</span><strong data-out="fees">-</strong></div><div class="kpi"><span>Equivalent W-2 salary</span><strong data-out="w2">-</strong></div></div>'
        . '<p class="tool__note">Rate = (income goal + costs) ÷ (1 − tax set-aside) ÷ (1 − platform fee) ÷ billable hours. "Equivalent W-2 salary" is a rough comparison that backs out the employer share of payroll tax and typical benefits (about 25%).</p>'
        . '</div>';
}

function tool_resume_keywords(): string
{
    return '<form class="tool__form" onsubmit="return false"><div class="tool__grid tool__grid--2">'
        . '<label class="tfield"><span class="tfield__label">Job description</span><textarea name="jd" rows="9" placeholder="Paste the full job posting here…"></textarea></label>'
        . '<label class="tfield"><span class="tfield__label">Your résumé</span><textarea name="cv" rows="9" placeholder="Paste your résumé text here…"></textarea></label>'
        . '</div><p class="tool__actions"><button class="btn btn--sm" type="button" data-action="scan">' . icon('scan') . ' Scan my résumé</button> <button class="btn btn--sm btn--outline" type="button" data-action="sample">Try an example</button></p></form>'
        . '<div class="tool__out" aria-live="polite" hidden>'
        . '<div class="score"><div class="ring" data-out="ring"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52"/><circle class="ring__val" cx="60" cy="60" r="52"/></svg><strong data-out="score">0%</strong></div>'
        . '<div><p class="score__t" data-out="verdict">-</p><p class="score__s" data-out="summary"></p></div></div>'
        . '<div class="kw"><div><p class="kw__t">' . icon('check') . ' Keywords you match</p><div class="chips chips--ok" data-out="have"></div></div>'
        . '<div><p class="kw__t">' . icon('x') . ' Missing from your résumé</p><div class="chips chips--miss" data-out="miss"></div></div></div>'
        . '<p class="tool__note">Everything runs in your browser; nothing you paste is uploaded. Add missing keywords only where they are true for you, ideally inside a bullet that shows a result.</p>'
        . '</div>';
}

function tool_job_quiz(): string
{
    $qs = [
        ['Where would you rather spend your workday?', [['office', 'At a desk, indoors'], ['labor', 'On my feet in a warehouse or plant'], ['trades', 'On a job site, building or fixing things'], ['driving', 'On the road']]],
        ['What do people say you are best at?', [['office', 'Staying organized'], ['customer', 'Talking with people'], ['trades', 'Working with my hands'], ['labor', 'Keeping a fast pace']]],
        ['Which schedule suits you?', [['office', 'Monday to Friday, daytime'], ['labor', 'Shifts, including nights'], ['customer', 'Flexible or part-time'], ['driving', 'Long days, then time off']]],
        ['What do you bring today?', [['office', 'Computer and phone skills'], ['trades', 'A trade skill or certification'], ['driving', 'A CDL or clean driving record'], ['labor', 'A strong work ethic and willingness to learn']]],
        ['What matters most in your next job?', [['labor', 'Starting work quickly'], ['trades', 'Learning a skill that pays more over time'], ['customer', 'Helping people'], ['office', 'A steady, predictable routine']]],
        ['Pick the task that sounds most satisfying:', [['customer', 'Turning an unhappy customer into a happy one'], ['office', 'Clearing an inbox and a stack of invoices'], ['trades', 'Welding a clean seam or framing a wall'], ['driving', 'Delivering every stop on time']]],
    ];
    $out = '<form class="quiz" onsubmit="return false"><div class="quiz__progress" aria-hidden="true"><span></span></div>';
    foreach ($qs as $i => [$q, $opts]) {
        $out .= '<fieldset class="quiz__q"' . ($i ? ' hidden' : '') . ' data-step="' . $i . '"><legend><span class="quiz__n">Question ' . ($i + 1) . ' of ' . count($qs) . '</span>' . e($q) . '</legend><div class="quiz__opts">';
        foreach ($opts as [$val, $label]) {
            $out .= '<label class="quiz__opt"><input type="radio" name="q' . $i . '" value="' . e($val) . '"><span>' . e($label) . '</span></label>';
        }
        $out .= '</div></fieldset>';
    }
    $out .= '</form><div class="quiz__result" aria-live="polite" hidden><p class="quiz__kicker">Your best match</p><p class="quiz__match" data-out="cat"></p><p data-out="blurb"></p>'
        . '<div class="quiz__bars" data-out="bars"></div><p class="quiz__jobs-t">Openings that fit:</p><ul class="quiz__jobs" data-out="jobs"></ul>'
        . '<p class="tool__actions"><a class="btn btn--sm" href="/applications/">Apply in 5 minutes</a> <button class="btn btn--sm btn--outline" type="button" data-action="restart">Retake quiz</button></p></div>';
    $jobs = [];
    foreach (JOBS as [$name, $cat]) {
        $jobs[$cat][] = $name;
    }
    $out .= '<script type="application/json" class="quiz-data">' . json_encode(['jobs' => $jobs, 'cats' => JOB_CATEGORIES], JSON_HEX_TAG) . '</script>';
    return $out;
}

function tool_vacancy_cost(): string
{
    return '<form class="tool__form" onsubmit="return false"><div class="tool__grid">'
        . num_field('salary', 'Annual pay for the role', '45000', '$', '', '1000')
        . num_field('multiplier', 'Revenue or output per employee vs. pay', '2', '', '×', '0.25', '1')
        . num_field('days', 'Days the role stays open (in-house)', '42', '', 'days', '1')
        . num_field('agencyDays', 'Days to fill with an agency', '10', '', 'days', '1')
        . num_field('hrHours', 'Hours your team spends hiring', '40', '', 'hrs', '1')
        . num_field('hrRate', 'Cost of that team time', '35', '$', '/hr', '1')
        . '</div></form>'
        . '<div class="tool__out" aria-live="polite">'
        . '<div class="kpis"><div class="kpi kpi--hl"><span>Lost output while the seat is empty</span><strong data-out="vacancy">-</strong></div><div class="kpi"><span>Potential savings filling it faster</span><strong data-out="saved">-</strong></div></div>'
        . '<div class="kpis kpis--4"><div class="kpi"><span>Cost per open day</span><strong data-out="perday">-</strong></div><div class="kpi"><span>Internal hiring time</span><strong data-out="hr">-</strong></div><div class="kpi"><span>Cost of a bad hire (est.)</span><strong data-out="bad">-</strong></div><div class="kpi"><span>Total in-house cost</span><strong data-out="total">-</strong></div></div>'
        . '<div class="compare" data-out="compare" aria-hidden="true"><div><span>In-house</span><i class="compare__a"></i></div><div><span>With Best Jobs Pro</span><i class="compare__b"></i></div></div>'
        . '<p class="tool__note">Cost per open day = pay × output multiplier ÷ 260 working days. Bad-hire estimate uses 30% of first-year pay, the figure the U.S. Department of Labor has cited. Savings exclude agency fees, which depend on the role and arrangement. <a href="/contact-us/">Ask us for a quote</a>.</p>'
        . '</div>';
}
