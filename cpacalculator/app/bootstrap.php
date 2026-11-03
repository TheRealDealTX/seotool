<?php
/* CPA Calculator — shared bootstrap: site constants, registries, layout and helpers. */
defined('CPA') or exit;

const SITE_NAME   = 'CPA Calculator';
const SITE_ORIGIN = 'https://cpacalculator.com';
const SITE_EMAIL  = 'info@cpacalculator.com';
const SITE_ROOT   = __DIR__ . '/..';

$TAX = json_decode(file_get_contents(__DIR__ . '/data/tax.json'), true);
define('TAX_YEAR', (int) $TAX['default']);

/* ------------------------------------------------------------------ registries */

/* Every calculator: slug => [name, short label, one-line pitch, icon key, category]. Order = display order. */
const TOOLS = [
  'federal-income-tax'      => ['Federal Income Tax Calculator', 'Federal Income Tax', 'Your 2026 federal tax, effective rate, marginal bracket and take-home pay.', 'flag', 'Income tax'],
  '1099-tax-calculator'     => ['1099 Tax Calculator', '1099 Tax', 'Self-employment tax, income tax, write-offs and quarterly payments for 1099 income.', 'receipt', 'Self-employed'],
  'self-employment-tax'     => ['Self-Employment Tax Calculator', 'Self-Employment Tax', 'Social Security and Medicare on your net self-employment earnings (Schedule SE).', 'briefcase', 'Self-employed'],
  'quarterly-estimated-tax' => ['Quarterly Estimated Tax Calculator', 'Quarterly Estimated Tax', 'How much to pay each quarter, safe-harbor amounts and the 2026 due dates.', 'calendar', 'Self-employed'],
  'paycheck-calculator'     => ['Paycheck Calculator', 'Paycheck / Take-Home', 'Net pay per paycheck after federal tax, FICA, 401(k) and other deductions.', 'wallet', 'Income tax'],
  'tax-refund-calculator'   => ['Tax Refund Calculator', 'Tax Refund Estimator', 'Will you get a refund or owe? Compare your withholding with your actual tax.', 'refund', 'Income tax'],
  'capital-gains-tax'       => ['Capital Gains Tax Calculator', 'Capital Gains Tax', 'Short- and long-term capital gains tax, the 0/15/20% brackets and NIIT.', 'chart', 'Investing'],
  's-corp-tax-savings'      => ['S Corp Tax Savings Calculator', 'S Corp vs LLC Savings', 'Compare sole-prop/LLC tax with an S corporation paying a reasonable salary.', 'building', 'Business'],
  'mileage-deduction'       => ['Mileage Deduction Calculator', 'Mileage Deduction', 'Business mileage deduction at the 2026 IRS rate of 72.5¢ per mile vs actual costs.', 'car', 'Deductions'],
  'home-office-deduction'   => ['Home Office Deduction Calculator', 'Home Office Deduction', 'Simplified vs regular method — see which home office deduction is bigger.', 'home', 'Deductions'],
  'depreciation-calculator' => ['Depreciation Calculator', 'Depreciation', 'Straight-line, declining balance and MACRS schedules, year by year.', 'layers', 'Business'],
  'profit-margin'           => ['Profit Margin Calculator', 'Profit Margin & Markup', 'Gross margin, markup, and the price you need to hit a target margin.', 'percent', 'Business'],
  'break-even'              => ['Break-Even Calculator', 'Break-Even Point', 'Units and revenue needed to cover fixed costs, with a contribution-margin chart.', 'scale', 'Business'],
  'cost-per-acquisition'    => ['Cost Per Acquisition (CPA) Calculator', 'CPA Formula (Marketing)', 'The CPA formula for marketing: cost per acquisition, target CPA and ROAS.', 'target', 'Business'],
  'salary-to-hourly'        => ['Salary to Hourly Calculator', 'Salary ↔ Hourly', 'Convert annual salary to hourly, weekly and monthly pay — before and after tax.', 'clock', 'Income tax'],
];

/* Blog posts: slug => [title, description, ISO date, image (relative to site root), primary keyword, read minutes]. Newest first. */
const POSTS = [
  'do-i-have-to-pay-quarterly-taxes-my-first-year' => ['Do I Have to Pay Quarterly Taxes My First Year Self-Employed?', 'First year freelancing? Here is exactly when the IRS expects quarterly estimated payments, how the safe harbor works with no prior-year tax, and what to pay.', '2026-11-02', '/assets/img/blog-first-year.png', 'do i have to pay quarterly taxes my first year', 8],
  '1099-taxes-for-physicians' => ['1099 Physician Tax Guide: Locums, Moonlighting and Contract Doctors', 'How 1099 physicians are taxed: self-employment tax above the wage base, QBI limits for medical practices, retirement plans and quarterly payments.', '2026-10-30', '/assets/img/blog-physician.png', '1099 physician tax calculator', 9],
  'how-much-federal-tax-will-i-pay' => ['How Much Federal Income Tax Will I Pay? 2026 Examples by Salary', 'Worked 2026 examples of federal income tax at $30k, $50k, $75k, $100k and $150k, with the brackets, standard deduction and effective rates explained.', '2026-10-28', '/assets/img/blog-federal.png', 'how much federal income tax will i pay', 8],
  'quarterly-taxes-101-guide' => ['Quarterly Taxes 101: Who Pays, How Much, and When (2026)', 'Quarterly estimated taxes explained: who must pay, the 2026 due dates, safe-harbor rules, how to calculate each payment and how to avoid IRS penalties.', '2026-04-28', '/wp-content/uploads/2026/04/Quarterly-Taxes-101-Guide.webp', 'quarterly taxes', 10],
  'understanding-your-w-2' => ['Understanding Your W-2: Every Box Explained (2026)', 'A box-by-box guide to Form W-2: wages, withholding, Social Security and Medicare, Box 12 codes, state boxes, and what to do if your W-2 is wrong.', '2026-04-27', '/wp-content/uploads/2026/04/Understanding-Your-W-2.webp', 'understanding your w-2', 9],
  'got-a-1099-exactly-what-to-do-next' => ['Got a 1099? Here’s Exactly What to Do Next (Step by Step)', 'Received a 1099-NEC, 1099-K or 1099-MISC? Check it, estimate the tax, track write-offs, pay quarterly and file Schedule C — a step-by-step 1099 guide.', '2026-04-26', '/wp-content/uploads/2026/04/Got-a-1099_-Heres-Exactly-What-to-Do-Next-Step-by-Step.webp', 'got a 1099 what to do', 10],
];

/* Salary pages under /calculators/federal-income-tax/{amount}/ (GSC "federal tax on $X" queries). */
const SALARY_PAGES = [15000, 20000, 25000, 30000, 35000, 38000, 40000, 45000, 50000, 56000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 100000, 110000, 120000, 125000, 150000, 175000, 200000, 250000, 300000];

const NAV = [
  ['Calculators', '/calculators/'],
  ['Federal Tax', '/calculators/federal-income-tax/'],
  ['1099 Tax', '/calculators/1099-tax-calculator/'],
  ['Guides', '/blog/'],
  ['Methodology', '/our-methodology/'],
];

/* ------------------------------------------------------------------ helpers */

function e($s): string { return htmlspecialchars((string) $s, ENT_QUOTES | ENT_HTML5, 'UTF-8'); }
function money($n, int $dp = 0): string { return ($n < 0 ? '−$' : '$') . number_format(abs($n), $dp); }
function asset(string $p): string { $f = SITE_ROOT . $p; return $p . (is_file($f) ? '?v=' . substr(md5_file($f), 0, 8) : ''); }
function tool_url(string $slug): string { return '/calculators/' . $slug . '/'; }
function post_url(string $slug): string { return '/blog/' . $slug . '/'; }
function fmt_date(string $iso): string { return date('F j, Y', strtotime($iso)); }

/* Federal tax (PHP mirror of calc-core.js estimate() for W-2 wages, standard deduction). */
function fed_tax(float $taxable, string $status, int $year = TAX_YEAR): array {
  global $TAX;
  $br = $TAX['years'][(string) $year]['brackets'][$status];
  $prev = 0; $tax = 0; $marg = 0.10; $layers = [];
  foreach ($br as [$top, $rate]) {
    $top = $top ?? INF;
    $amt = max(0, min($taxable, $top) - $prev);
    $layers[] = ['from' => $prev, 'to' => $top, 'rate' => $rate, 'amount' => $amt, 'tax' => $amt * $rate];
    $tax += $amt * $rate;
    if ($taxable > $prev) $marg = $rate;
    $prev = $top;
  }
  return ['tax' => $tax, 'marginal' => $marg, 'layers' => $layers];
}
function salary_breakdown(float $gross, string $status, int $year = TAX_YEAR): array {
  global $TAX;
  $y = $TAX['years'][(string) $year];
  $std = $y['std'][$status];
  $taxable = max(0, $gross - $std);
  $f = fed_tax($taxable, $status, $year);
  $ss = min($gross, $y['ssWageBase']) * 0.062;
  $med = $gross * 0.0145 + max(0, $gross - $y['addlMedicare'][$status]) * 0.009;
  return [
    'gross' => $gross, 'std' => $std, 'taxable' => $taxable, 'tax' => $f['tax'], 'marginal' => $f['marginal'], 'layers' => $f['layers'],
    'ss' => $ss, 'medicare' => $med, 'fica' => $ss + $med, 'net' => $gross - $f['tax'] - $ss - $med,
    'effective' => $gross > 0 ? $f['tax'] / $gross : 0,
  ];
}
function status_label(string $s): string {
  return ['single' => 'Single', 'mfj' => 'Married filing jointly', 'mfs' => 'Married filing separately', 'hoh' => 'Head of household'][$s] ?? $s;
}

/* ------------------------------------------------------------------ icons (inline SVG, stroke-based) */
function icon(string $k, string $cls = 'ic'): string {
  $p = [
    'flag' => '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    'receipt' => '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    'briefcase' => '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
    'calendar' => '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18M8 14h2M14 14h2M8 17h2"/>',
    'wallet' => '<path d="M3 7a2 2 0 0 1 2-2h13v4"/><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M16 13.5h2"/>',
    'refund' => '<path d="M4 12a8 8 0 1 0 2.3-5.6L4 8.7"/><path d="M4 4v4.7h4.7"/><path d="M12 8v8M9.5 10.5c0-1 1.1-1.5 2.5-1.5s2.5.6 2.5 1.6c0 2.4-5 1.4-5 3.8 0 1 1.1 1.6 2.5 1.6s2.5-.5 2.5-1.5"/>',
    'chart' => '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 6-7"/>',
    'building' => '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/>',
    'car' => '<path d="M5 17h14M5 17a2 2 0 1 0 4 0M15 17a2 2 0 1 0 4 0M3 17v-4l2-5h14l2 5v4"/><path d="M5 12h14"/>',
    'home' => '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><rect x="9" y="13" width="6" height="7"/>',
    'layers' => '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    'percent' => '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
    'scale' => '<path d="M12 3v18M5 21h14M5 7h14"/><path d="M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
    'target' => '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    'clock' => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'check' => '<path d="M5 12l5 5L20 7"/>',
    'arrow' => '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'book' => '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/>',
    'shield' => '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    'mail' => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    'calc' => '<rect x="5" y="2" width="14" height="20" rx="2"/><rect x="8" y="5" width="8" height="4" rx="1"/><path d="M8 13h.01M12 13h.01M16 13h.01M8 17h.01M12 17h.01M16 17h.01"/>',
    'menu' => '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'spark' => '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
  ];
  return '<svg class="' . e($cls) . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . ($p[$k] ?? $p['calc']) . '</svg>';
}

function logo_svg(): string {
  return '<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="url(#lg)"/><defs><linearGradient id="lg" x1="0" y1="0" x2="40" y2="40"><stop offset="0" stop-color="#10b981"/><stop offset="1" stop-color="#0e7490"/></linearGradient></defs><rect x="11" y="8" width="18" height="24" rx="3.5" fill="none" stroke="#fff" stroke-width="2.2"/><rect x="14.5" y="11.5" width="11" height="5" rx="1.2" fill="#fff"/><path d="M15 22.5l3 3 6-6.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
}

/* ------------------------------------------------------------------ page components */

function breadcrumbs(array $items): string {
  global $P;
  $all = array_merge([['Home', '/']], $items);
  $P['schema'][] = ['@type' => 'BreadcrumbList', 'itemListElement' => array_map(fn($it, $i) => [
    '@type' => 'ListItem', 'position' => $i + 1, 'name' => $it[0], 'item' => SITE_ORIGIN . $it[1]], $all, array_keys($all))];
  $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
  foreach ($all as $i => [$n, $u]) {
    $h .= $i === count($all) - 1 ? '<li aria-current="page">' . e($n) . '</li>' : '<li><a href="' . e($u) . '">' . e($n) . '</a></li>';
  }
  return $h . '</ol></nav>';
}

/* FAQ block + FAQPage schema. $faqs = [[q, a_html], ...] */
function faq_block(array $faqs, string $heading = 'Frequently asked questions', string $id = 'faq'): string {
  global $P;
  $P['schema'][] = ['@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => [
    '@type' => 'Question', 'name' => $f[0], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => trim(strip_tags($f[1]))]], $faqs)];
  $h = '<section class="faq reveal" id="' . e($id) . '"><h2>' . e($heading) . '</h2><div class="faq-list">';
  foreach ($faqs as $i => [$q, $a]) {
    $h .= '<details' . ($i === 0 ? ' open' : '') . '><summary>' . e($q) . '<span class="faq-x" aria-hidden="true"></span></summary><div class="faq-a">' . $a . '</div></details>';
  }
  return $h . '</div></section>';
}

/* Schema for a calculator page (WebApplication). */
function tool_schema(string $slug): void {
  global $P;
  [$name, , $pitch] = TOOLS[$slug];
  $P['schema'][] = [
    '@type' => 'WebApplication', 'name' => $name, 'url' => SITE_ORIGIN . tool_url($slug), 'description' => $pitch,
    'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any', 'browserRequirements' => 'Requires JavaScript',
    'isAccessibleForFree' => true, 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
    'publisher' => ['@id' => SITE_ORIGIN . '/#org'], 'dateModified' => date('Y-m-d', filemtime(SITE_ROOT . '/app/pages/calculators/' . $slug . '.php')),
  ];
}

/* Grid of tool cards. */
function tool_cards(array $slugs, string $cls = ''): string {
  $h = '<div class="tool-grid ' . e($cls) . '">';
  foreach ($slugs as $i => $s) {
    if (!isset(TOOLS[$s])) continue;
    [$name, $short, $pitch, $ic, $cat] = TOOLS[$s];
    $h .= '<a class="tool-card reveal" style="--d:' . ($i % 6) * 60 . 'ms" href="' . tool_url($s) . '"><span class="tc-ic">' . icon($ic) . '</span><span class="tc-cat">' . e($cat) . '</span><strong>' . e($short) . '</strong><span class="tc-p">' . e($pitch) . '</span><span class="tc-go">Open calculator ' . icon('arrow') . '</span></a>';
  }
  return $h . '</div>';
}

function related_tools(string $current, array $slugs): string {
  return '<section class="related reveal"><h2>Related calculators</h2>' . tool_cards(array_values(array_diff($slugs, [$current]))) . '</section>';
}

function post_cards(array $slugs): string {
  $h = '<div class="post-grid">';
  foreach ($slugs as $i => $s) {
    if (!isset(POSTS[$s])) continue;
    [$t, $d, $date, $img, , $min] = POSTS[$s];
    $h .= '<a class="post-card reveal" style="--d:' . ($i % 3) * 80 . 'ms" href="' . post_url($s) . '"><span class="pc-img"><img src="' . e($img) . '" alt="" loading="lazy" width="640" height="360"></span><span class="pc-body"><span class="pc-meta">' . fmt_date($date) . ' · ' . $min . ' min read</span><strong>' . e($t) . '</strong><span class="pc-d">' . e($d) . '</span></span></a>';
  }
  return $h . '</div>';
}

/* Standard calculator action bar. */
function tool_actions(): string {
  return '<div class="tool-actions"><button type="button" class="btn-ghost" data-share>Copy share link</button><button type="button" class="btn-ghost" data-print>Print / save PDF</button><button type="button" class="btn-ghost" data-reset>Reset</button></div>';
}

/* Inline tax data so calc-core.js shares app/data/tax.json. */
function tax_data_script(): string {
  global $TAX;
  return '<script>window.TAX=' . json_encode($TAX, JSON_UNESCAPED_SLASHES) . ';</script>';
}

/* ------------------------------------------------------------------ layout */

function render_page(array $P, string $body): void {
  $title = $P['title'];
  if (mb_strlen($title) > 66 && str_ends_with($title, ' | CPA Calculator')) $title = substr($title, 0, -17);
  $desc = $P['description'];
  $canon = SITE_ORIGIN . ($P['canonical'] ?? $P['path']);
  $img = SITE_ORIGIN . ($P['image'] ?? '/assets/img/og-cpa-calculator.png');
  $graph = array_merge([
    ['@type' => 'Organization', '@id' => SITE_ORIGIN . '/#org', 'name' => SITE_NAME, 'url' => SITE_ORIGIN . '/', 'email' => SITE_EMAIL,
     'logo' => ['@type' => 'ImageObject', 'url' => SITE_ORIGIN . '/assets/img/logo-512.png', 'width' => 512, 'height' => 512]],
    ['@type' => 'WebSite', '@id' => SITE_ORIGIN . '/#website', 'name' => SITE_NAME, 'url' => SITE_ORIGIN . '/', 'publisher' => ['@id' => SITE_ORIGIN . '/#org'], 'inLanguage' => 'en-US'],
    ['@type' => $P['pageType'] ?? 'WebPage', '@id' => $canon . '#webpage', 'url' => $canon, 'name' => $title, 'description' => $desc,
     'isPartOf' => ['@id' => SITE_ORIGIN . '/#website'], 'inLanguage' => 'en-US', 'dateModified' => $P['modified'] ?? date('Y-m-d')],
  ], $P['schema'] ?? []);
  $cur = $P['path'];
  header('Content-Type: text/html; charset=utf-8');
  ?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<?php if (!empty($P['noindex'])): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<?php endif; ?>
<meta property="og:site_name" content="<?= SITE_NAME ?>">
<meta property="og:type" content="<?= e($P['ogType'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($P['ogTitle'] ?? $title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:image" content="<?= e($img) ?>">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($P['ogTitle'] ?? $title) ?>">
<meta name="twitter:description" content="<?= e($desc) ?>">
<meta name="twitter:image" content="<?= e($img) ?>">
<?php if (!empty($P['published'])): ?><meta property="article:published_time" content="<?= e($P['published']) ?>">
<meta property="article:modified_time" content="<?= e($P['modified'] ?? $P['published']) ?>">
<?php endif; ?>
<meta name="theme-color" content="#0b1220">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap">
<link rel="stylesheet" href="<?= asset('/assets/css/site.css') ?>">
<script type="application/ld+json"><?= json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?></script>
</head>
<body class="<?= e($P['bodyClass'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span></span></div>
<header class="site-header">
  <div class="wrap hdr">
    <a class="brand" href="/" aria-label="CPA Calculator home"><?= logo_svg() ?><span>CPA<b>Calculator</b></span></a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>
<?php foreach (NAV as [$n, $u]): ?>
        <li><a href="<?= $u ?>"<?= $cur === $u ? ' aria-current="page"' : '' ?>><?= e($n) ?></a></li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn-sm nav-cta" href="/calculators/federal-income-tax/">Estimate my taxes</a>
    </nav>
    <button class="nav-toggle" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><?= icon('menu') ?></button>
  </div>
</header>
<main id="main">
<?= $body ?>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="ft-top">
      <div class="ft-brand">
        <a class="brand" href="/"><?= logo_svg() ?><span>CPA<b>Calculator</b></span></a>
        <p>Free, CPA-grade tax and accounting calculators built on current IRS tables. Updated for the <?= TAX_YEAR ?> tax year.</p>
        <a class="ft-mail" href="mailto:<?= SITE_EMAIL ?>"><?= icon('mail') ?><?= SITE_EMAIL ?></a>
      </div>
      <div class="ft-col"><h3>Tax calculators</h3><ul>
<?php foreach (['federal-income-tax', '1099-tax-calculator', 'self-employment-tax', 'quarterly-estimated-tax', 'paycheck-calculator', 'tax-refund-calculator', 'capital-gains-tax', 'salary-to-hourly'] as $s): ?>
        <li><a href="<?= tool_url($s) ?>"><?= e(TOOLS[$s][1]) ?></a></li>
<?php endforeach; ?>
      </ul></div>
      <div class="ft-col"><h3>Business tools</h3><ul>
<?php foreach (['s-corp-tax-savings', 'mileage-deduction', 'home-office-deduction', 'depreciation-calculator', 'profit-margin', 'break-even', 'cost-per-acquisition'] as $s): ?>
        <li><a href="<?= tool_url($s) ?>"><?= e(TOOLS[$s][1]) ?></a></li>
<?php endforeach; ?>
      </ul></div>
      <div class="ft-col"><h3>Company</h3><ul>
        <li><a href="/about-us/">About us</a></li>
        <li><a href="/our-methodology/">Our methodology</a></li>
        <li><a href="/blog/">Tax guides</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/disclaimer/">Disclaimer</a></li>
        <li><a href="/privacy-policy/">Privacy policy</a></li>
        <li><a href="/terms-of-use/">Terms of use</a></li>
      </ul></div>
    </div>
    <div class="ft-bottom">
      <p>© <?= date('Y') ?> CPA Calculator · cpacalculator.com. Estimates are for education and planning, not tax, legal or accounting advice. Always confirm with a licensed CPA before filing.</p>
    </div>
  </div>
</footer>
<script src="<?= asset('/assets/js/site.js') ?>" defer></script>
<?php if (!empty($P['scripts'])): ?>
<?= tax_data_script() ?>
<script src="<?= asset('/assets/js/calc-core.js') ?>" defer></script>
<?php foreach ($P['scripts'] as $s): ?>
<script src="<?= asset($s) ?>" defer></script>
<?php endforeach; endif; ?>
</body>
</html>
<?php
}

/* ------------------------------------------------------------------ shared content blocks */

function bracket_table(string $status, int $year = TAX_YEAR): string {
  global $TAX;
  $br = $TAX['years'][(string) $year]['brackets'][$status];
  $h = '<div class="table-wrap"><table><caption class="sr-only">' . $year . ' federal tax brackets — ' . e(status_label($status)) . '</caption><thead><tr><th>Rate</th><th>Taxable income</th><th class="n">Tax owed in this bracket</th></tr></thead><tbody>';
  $prev = 0; $cum = 0;
  foreach ($br as [$top, $rate]) {
    $range = $top === null ? 'Over ' . money($prev) : money($prev === 0 ? 0 : $prev + 1) . ' – ' . money($top);
    $owed = $prev === 0 ? round($rate * 100) . '% of taxable income' : money($cum) . ' + ' . round($rate * 100) . '% over ' . money($prev);
    $h .= '<tr><td><b>' . round($rate * 100) . '%</b></td><td>' . $range . '</td><td class="n">' . $owed . '</td></tr>';
    if ($top !== null) { $cum += ($top - $prev) * $rate; $prev = $top; }
  }
  return $h . '</tbody></table></div>';
}

function std_deduction_table(): string {
  global $TAX;
  $h = '<div class="table-wrap"><table><thead><tr><th>Filing status</th>';
  $years = array_keys($TAX['years']); sort($years);
  foreach ($years as $y) $h .= '<th class="n">' . $y . '</th>';
  $h .= '<th class="n">Extra if 65+ / blind (' . TAX_YEAR . ')</th></tr></thead><tbody>';
  foreach (['single', 'mfj', 'mfs', 'hoh'] as $s) {
    $h .= '<tr><td>' . status_label($s) . '</td>';
    foreach ($years as $y) $h .= '<td class="n">' . money($TAX['years'][$y]['std'][$s]) . '</td>';
    $h .= '<td class="n">' . money($TAX['years'][(string) TAX_YEAR]['addl65'][$s]) . '</td></tr>';
  }
  return $h . '</tbody></table></div>';
}

/* Standard calculator page hero. */
function tool_hero(string $slug, string $h1, string $lede, array $badges): string {
  global $P;
  tool_schema($slug);
  $b = '';
  foreach ($badges as $x) $b .= '<span class="badge">' . icon('check') . e($x) . '</span>';
  return '<section class="page-hero"><div class="wrap">' . breadcrumbs([['Calculators', '/calculators/'], [TOOLS[$slug][0], tool_url($slug)]]) .
    '<h1>' . $h1 . '</h1><p class="lede">' . $lede . '</p><div class="badges">' . $b . '</div></div></section>';
}

/* Reusable money input. */
function money_field(string $name, string $label, $value = '', string $tip = '', string $hint = '', string $pre = '$'): string {
  $id = 'f-' . $name;
  return '<div class="field"><label for="' . $id . '">' . e($label) . ($tip ? ' <span class="tip" tabindex="0" data-tip="' . e($tip) . '">?</span>' : '') . '</label>' .
    '<div class="inp ' . ($pre === '%' ? 'suf" data-suf="%' : ($pre === '' ? '' : 'pre" data-pre="' . e($pre))) . '"><input id="' . $id . '" name="' . e($name) . '" inputmode="decimal" autocomplete="off" data-money value="' . e($value === '' ? '' : (is_numeric($value) && $pre !== '%' ? number_format((float) $value, floor((float) $value) == (float) $value ? 0 : 2) : $value)) . '" placeholder="0"></div>' .
    ($hint ? '<span class="hint">' . $hint . '</span>' : '') . '</div>';
}

function status_field(string $name = 'status', string $sel = 'single', bool $mfs = true): string {
  $h = '<div class="field"><span class="lbl">Filing status</span><div class="seg" role="radiogroup" aria-label="Filing status">';
  foreach (['single' => 'Single', 'mfj' => 'Married jointly', 'mfs' => 'Married separately', 'hoh' => 'Head of household'] as $k => $v) {
    if (!$mfs && $k === 'mfs') continue;
    $h .= '<label><input type="radio" name="' . $name . '" value="' . $k . '"' . ($k === $sel ? ' checked' : '') . '><span>' . $v . '</span></label>';
  }
  return $h . '</div></div>';
}

function year_field(string $name = 'year'): string {
  global $TAX;
  $years = array_keys($TAX['years']); rsort($years);
  $h = '<div class="field"><label for="f-' . $name . '">Tax year</label><select id="f-' . $name . '" name="' . $name . '">';
  foreach ($years as $y) $h .= '<option value="' . $y . '"' . ((int) $y === TAX_YEAR ? ' selected' : '') . '>' . $y . ($y == TAX_YEAR ? ' (current)' : ' (filing now / amended)') . '</option>';
  return $h . '</select></div>';
}

/* ------------------------------------------------------------------ blog post layout */

function post_open(string $slug, string $updated = ''): string {
  global $P;
  [$t, $d, $date, $img, , $min] = POSTS[$slug];
  $mod = $updated ?: $date;
  $P['title'] = mb_strlen($t) > 58 ? $t : $t . ' | CPA Calculator';
  $P['ogTitle'] = $t;
  $P['description'] = $d;
  $P['ogType'] = 'article';
  $P['published'] = $date;
  $P['modified'] = $mod;
  $P['image'] = $img;
  $P['pageType'] = 'WebPage';
  $P['schema'][] = ['@type' => 'BlogPosting', 'headline' => $t, 'description' => $d, 'image' => SITE_ORIGIN . $img,
    'datePublished' => $date, 'dateModified' => $mod, 'mainEntityOfPage' => SITE_ORIGIN . post_url($slug),
    'author' => ['@type' => 'Organization', 'name' => 'CPA Calculator Editorial Team', 'url' => SITE_ORIGIN . '/about-us/'],
    'publisher' => ['@id' => SITE_ORIGIN . '/#org']];
  return '<section class="page-hero"><div class="wrap">' . breadcrumbs([['Guides', '/blog/'], [$t, post_url($slug)]]) .
    '<h1>' . e($t) . '</h1><p class="lede">' . e($d) . '</p><div class="byline"><span>By the CPA Calculator Editorial Team</span><span>Updated ' . fmt_date($mod) . '</span><span>' . $min . ' min read</span></div></div></section>' .
    '<div class="wrap content-grid"><article class="prose"><figure class="post-hero-img"><img src="' . e($img) . '" alt="' . e($t) . '" width="1200" height="675"></figure>';
}

/* $tool = slug of the calculator promoted in the sidebar CTA. */
function post_close(string $slug, string $tool, array $related = []): string {
  [$name, , $pitch] = TOOLS[$tool];
  $h = '</article><aside class="aside"><div class="card"><div class="res-label" style="margin-bottom:10px">On this page</div><ul class="toc" data-toc></ul>' .
    '<div class="aside-cta"><strong>' . e($name) . '</strong>' . e($pitch) . '<a class="btn btn-sm" href="' . tool_url($tool) . '">Open calculator</a></div></div></aside></div>';
  $related = $related ?: array_slice(array_values(array_diff(array_keys(POSTS), [$slug])), 0, 3);
  return $h . '<section class="section-tight section-alt"><div class="wrap"><h2>Keep reading</h2>' . post_cards($related) . '</div></section>';
}

/* Simple content page shell (about, methodology, legal). */
function simple_hero(string $h1, string $lede, string $crumb, string $updated = ''): string {
  global $P;
  return '<section class="page-hero"><div class="wrap">' . breadcrumbs([[$crumb, $P['path']]]) . '<h1>' . $h1 . '</h1><p class="lede">' . $lede . '</p>' .
    ($updated ? '<div class="byline"><span>Last updated ' . fmt_date($updated) . '</span></div>' : '') . '</div></section>';
}
