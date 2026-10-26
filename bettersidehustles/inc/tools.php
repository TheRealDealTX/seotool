<?php
// Markup for the interactive tools. The maths lives in assets/js/tools.js,
// keyed by data-tool. Every field has a sensible default so results show
// immediately, and the form still reads clearly with JavaScript off.

const TOOL_FIELDS = [
    'income-calculator' => [
        'title' => 'Side Hustle Income Calculator',
        'intro' => 'Plug in your rate and hours to see monthly and yearly take-home — and how long until you hit a goal.',
        'fields' => [
            ['rate', 'Hourly rate or average earnings per hour', 25, 1, '$', '/hr'],
            ['hours', 'Hours per week', 8, 0.5, '', 'hrs'],
            ['weeks', 'Weeks worked per year', 48, 1, '', 'wks'],
            ['costs', 'Monthly costs (apps, gas, supplies)', 40, 5, '$', '/mo'],
            ['tax', 'Tax set-aside', 25, 1, '', '%'],
            ['goal', 'Savings goal', 5000, 100, '$', ''],
        ],
    ],
    'gig-calculator' => [
        'title' => 'Gig Driver Earnings Calculator',
        'intro' => 'Uber, Lyft, DoorDash or Instacart — see what you really earn per hour after gas and wear on your car.',
        'fields' => [
            ['gross', 'Weekly app earnings incl. tips', 450, 10, '$', '/wk'],
            ['hours', 'Hours online per week', 20, 1, '', 'hrs'],
            ['miles', 'Miles driven per week', 300, 10, '', 'mi'],
            ['mpg', 'Your car\'s fuel economy', 28, 1, '', 'mpg'],
            ['gas', 'Gas price per gallon', 3.25, 0.05, '$', ''],
            ['wear', 'Maintenance & depreciation per mile', 0.12, 0.01, '$', '/mi'],
            ['irs', 'IRS mileage rate (76¢ from July 2026)', 0.76, 0.005, '$', '/mi'],
        ],
    ],
    'tax-estimator' => [
        'title' => 'Side Hustle Tax Calculator',
        'intro' => 'Estimate the federal self-employment tax and income tax on your side income, plus what to set aside each quarter.',
        'fields' => [
            ['profit', 'Side hustle profit for the year (after expenses)', 12000, 100, '$', ''],
            ['wages', 'Other income (W-2 job) for the year', 55000, 1000, '$', ''],
            ['state', 'State income tax rate (0 for TX, FL, NV…)', 4, 0.1, '', '%'],
        ],
        'select' => ['status', 'Filing status', ['single' => 'Single', 'married' => 'Married filing jointly', 'hoh' => 'Head of household']],
    ],
    'course-calculator' => [
        'title' => 'Online Course Revenue Calculator',
        'intro' => 'See what one course could earn per month on Udemy, Skillshare and your own Thinkific site.',
        'fields' => [
            ['price', 'Average sale price', 19.99, 1, '$', ''],
            ['sales', 'Sales per month', 60, 1, '', 'sales'],
            ['own', 'Share of sales you bring in yourself (coupons, email)', 20, 5, '', '%'],
            ['minutes', 'Skillshare minutes watched per month', 6000, 100, '', 'min'],
            ['perMin', 'Skillshare payout per minute (est.)', 0.05, 0.005, '$', ''],
            ['plan', 'Thinkific plan cost', 54, 1, '$', '/mo'],
        ],
    ],
    'freelance-rate' => [
        'title' => 'Freelance Rate Calculator',
        'intro' => 'Work backward from the money you want to the rate you need to charge — after platform fees and taxes.',
        'fields' => [
            ['target', 'Take-home goal per month', 1500, 50, '$', '/mo'],
            ['hours', 'Billable hours per week', 10, 1, '', 'hrs'],
            ['fee', 'Platform fee (Fiverr = 20%, direct = 0%)', 20, 1, '', '%'],
            ['tax', 'Tax set-aside', 25, 1, '', '%'],
            ['costs', 'Monthly software & costs', 30, 5, '$', '/mo'],
            ['gigHours', 'Hours a typical gig takes', 3, 0.5, '', 'hrs'],
        ],
    ],
    'shopify-profit' => [
        'title' => 'Product Profit Calculator',
        'intro' => 'Find your margin, profit per order and break-even point for a Shopify, Etsy or Amazon product.',
        'fields' => [
            ['price', 'Selling price', 34, 1, '$', ''],
            ['cost', 'Product / print cost', 12.5, 0.5, '$', ''],
            ['ship', 'Shipping & packaging per order', 5, 0.5, '$', ''],
            ['feePct', 'Payment processing', 2.9, 0.1, '', '%'],
            ['ads', 'Ad spend per order', 6, 0.5, '$', ''],
            ['fixed', 'Monthly fixed costs (plan, apps)', 49, 1, '$', '/mo'],
            ['orders', 'Orders per month', 40, 1, '', 'orders'],
        ],
    ],
    'affiliate-calculator' => [
        'title' => 'Affiliate Commission Calculator',
        'intro' => 'Project affiliate income from your traffic. Defaults reflect a $200-per-sale software program like Semrush.',
        'fields' => [
            ['visitors', 'Monthly visitors to the page', 3000, 100, '', ''],
            ['ctr', 'Click-through to the offer', 4, 0.5, '', '%'],
            ['conv', 'Conversion rate after the click', 2, 0.1, '', '%'],
            ['commission', 'Commission per sale', 200, 5, '$', ''],
            ['growth', 'Monthly traffic growth', 5, 1, '', '%'],
        ],
    ],
];

function tool_html(string $key, string $mode = 'inline'): string
{
    $GLOBALS['uses_tools'] = true;
    if ($key === 'quiz') {
        return quiz_html($mode);
    }
    $t = TOOL_FIELDS[$key] ?? null;
    if (!$t) {
        return '';
    }
    $slug = null;
    foreach (TOOLS as $s => $def) {
        if ($def[0] === $key) {
            $slug = $s;
        }
    }
    $uid = $key . '-' . substr(md5($mode . mt_rand()), 0, 5);
    $h = '<div class="tool tool-' . e($mode) . ' reveal" data-tool="' . e($key) . '">';
    $h .= '<div class="tool-head"><span class="tool-ic">' . icon(TOOLS[$slug][3] ?? 'chart') . '</span><div><h3 class="tool-title">' . e($t['title']) . '</h3>';
    if ($mode !== 'sidebar') {
        $h .= '<p>' . e($t['intro']) . '</p>';
    }
    $h .= '</div></div><form class="tool-form" onsubmit="return false">';
    foreach ($t['fields'] as [$name, $label, $def, $step, $pre, $suf]) {
        $id = "$uid-$name";
        $h .= '<label class="field" for="' . $id . '"><span>' . e($label) . '</span><span class="input">'
            . ($pre ? '<i>' . e($pre) . '</i>' : '')
            . '<input id="' . $id . '" name="' . e($name) . '" type="number" inputmode="decimal" min="0" step="' . e((string) $step) . '" value="' . e((string) $def) . '">'
            . ($suf ? '<i>' . e($suf) . '</i>' : '') . '</span></label>';
    }
    if (!empty($t['select'])) {
        [$name, $label, $opts] = $t['select'];
        $h .= '<label class="field" for="' . "$uid-$name" . '"><span>' . e($label) . '</span><span class="input"><select id="' . "$uid-$name" . '" name="' . e($name) . '">';
        foreach ($opts as $v => $l) {
            $h .= '<option value="' . e($v) . '">' . e($l) . '</option>';
        }
        $h .= '</select></span></label>';
    }
    $h .= '</form><div class="tool-out" aria-live="polite"></div>';
    if ($mode !== 'full' && $slug) {
        $h .= '<a class="tool-more" href="/tools/' . e($slug) . '/">Open full calculator ' . icon('arrow') . '</a>';
    }
    return $h . '</div>';
}

function quiz_html(string $mode): string
{
    $qs = [
        ['time', 'How much time can you give it each week?', ['lt5' => 'Under 5 hours', '5to10' => '5–10 hours', '10to20' => '10–20 hours', 'gt20' => '20+ hours']],
        ['goal', 'What matters most right now?', ['fast' => 'Cash this week', 'steady' => 'Steady monthly income', 'scale' => 'Something that can grow', 'passive' => 'Mostly passive income']],
        ['where', 'Where do you want to work?', ['home' => 'From home / my laptop', 'phone' => 'Just my phone', 'out' => 'Out and about in my city', 'any' => 'Either works']],
        ['skill', 'Which sounds most like you?', ['people' => 'Good with people', 'creative' => 'Creative — writing, design, video', 'tech' => 'Techy or analytical', 'hands' => 'Handy and practical']],
        ['car', 'Do you have a reliable car?', ['yes' => 'Yes', 'no' => 'No']],
        ['budget', 'How much can you spend to start?', ['0' => 'Nothing', '100' => 'Up to $100', '500' => 'Up to $500', 'more' => '$500+']],
    ];
    $h = '<div class="tool quiz tool-' . e($mode) . ' reveal" data-tool="quiz">';
    $h .= '<div class="tool-head"><span class="tool-ic">' . icon('target') . '</span><div><h3 class="tool-title">Side Hustle Matcher</h3>';
    if ($mode !== 'sidebar') {
        $h .= '<p>Six quick questions. We\'ll match you with the three side hustles that fit you best.</p>';
    }
    $h .= '</div></div><div class="quiz-progress"><span></span></div><div class="quiz-steps">';
    foreach ($qs as $i => [$name, $q, $opts]) {
        $h .= '<fieldset class="quiz-step' . ($i === 0 ? ' is-active' : '') . '" data-q="' . e($name) . '"><legend><small>Question ' . ($i + 1) . ' of ' . count($qs) . '</small>' . e($q) . '</legend><div class="quiz-opts">';
        foreach ($opts as $v => $l) {
            $h .= '<button type="button" class="quiz-opt" data-v="' . e($v) . '">' . e($l) . '</button>';
        }
        $h .= '</div></fieldset>';
    }
    $h .= '</div><div class="quiz-result" aria-live="polite" hidden></div></div>';
    return $h;
}
