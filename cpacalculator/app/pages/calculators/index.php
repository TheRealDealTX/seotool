<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$P['title'] = "All Tax & Accounting Calculators ($Y) | CPA Calculator";
$P['description'] = "Browse every free CPA Calculator tool: federal income tax, 1099 and self-employment tax, quarterly estimates, paycheck, capital gains, S corp and more.";
$P['pageType'] = 'CollectionPage';
$P['schema'][] = ['@type' => 'ItemList', 'itemListElement' => array_map(fn($s, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'name' => TOOLS[$s][0], 'url' => SITE_ORIGIN . tool_url($s)], array_keys(TOOLS), array_keys(array_keys(TOOLS)))];
$cats = [];
foreach (TOOLS as $s => $t) $cats[$t[4]][] = $s;
$intro = [
  'Income tax' => 'For employees and anyone who wants to know their federal tax, paycheck and refund.',
  'Self-employed' => 'For freelancers, contractors, gig workers and side hustlers paid on a 1099.',
  'Investing' => 'For selling stocks, crypto, funds or property.',
  'Deductions' => 'Write-offs that lower taxable income for self-employed people and business owners.',
  'Business' => 'Entity choice, pricing, profitability and asset math for small businesses and marketers.',
];
?>
<section class="page-hero"><div class="wrap">
  <?= breadcrumbs([['Calculators', '/calculators/']]) ?>
  <h1>Free tax &amp; accounting calculators</h1>
  <p class="lede">Every CPA Calculator tool in one place — updated for the <?= $Y ?> tax year, free to use with no signup. Pick a category or jump straight to the most popular: the <a href="/calculators/federal-income-tax/" style="color:#6ee7b7">federal income tax calculator</a> and the <a href="/calculators/1099-tax-calculator/" style="color:#6ee7b7">1099 tax calculator</a>.</p>
  <ul class="pill-links" style="margin-top:22px"><?php foreach (array_keys($cats) as $c): ?><li><a href="#<?= strtolower(str_replace(' ', '-', $c)) ?>"><?= e($c) ?></a></li><?php endforeach; ?></ul>
</div></section>
<?php foreach ($cats as $c => $slugs): ?>
<section class="section-tight" id="<?= strtolower(str_replace(' ', '-', $c)) ?>"><div class="wrap">
  <div class="sec-head reveal" style="margin-bottom:24px"><span class="kicker"><?= count($slugs) ?> calculator<?= count($slugs) > 1 ? 's' : '' ?></span><h2><?= e($c) ?> calculators</h2><p><?= e($intro[$c] ?? '') ?></p></div>
  <?= tool_cards($slugs) ?>
</div></section>
<?php endforeach; ?>
<section class="section-tight"><div class="wrap" style="max-width:900px">
<?= faq_block([
  ['Are these calculators really free?', '<p>Yes. Every CPA Calculator tool is free, with no account or email required, and your inputs never leave your browser.</p>'],
  ['Is this advice from a real CPA?', '<p>No — the calculators follow the same rules and order of operations a CPA uses, but they produce educational estimates, not personalized tax advice. For a business with employees, foreign income, a home sale, an inheritance or an IRS notice, work with a licensed CPA or enrolled agent.</p>'],
  ['Are the calculators updated for ' . $Y . '?', "<p>Yes. They use the $Y inflation-adjusted brackets, standard deductions, Social Security wage base, mileage rate and contribution limits, plus the rules from the One Big Beautiful Bill Act. Most tax tools also let you switch to " . ($Y - 1) . ".</p>"],
  ['What if I made a mistake on a past return?', '<p>You can generally file an amended return (Form 1040-X) within three years of the original due date. If you owe, paying late is better than not paying — the failure-to-pay penalty is far smaller than the failure-to-file penalty.</p>'],
]) ?>
</div></section>
