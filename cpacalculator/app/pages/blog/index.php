<?php defined('CPA') or exit;
$isTopic = $P['path'] === '/topic/guides/';
if ($isTopic) {
  $P['title'] = 'Tax Guides: ' . TAX_YEAR . ' Tax Help for Freelancers & Employees | CPA Calculator';
  $P['description'] = 'Tax guides in plain English: what to do with a 1099, quarterly estimated taxes, your W-2 box by box, and federal tax by salary, updated for ' . TAX_YEAR . ' rules.';
  $h1 = 'Tax Guides';
  $crumb = [['Tax Guides', '/topic/guides/']];
} else {
  $P['title'] = 'Tax Blog: ' . TAX_YEAR . ' Guides to 1099s, W-2s & Quarterly Taxes | CPA Calculator';
  $P['description'] = 'Plain-English tax guides from the CPA Calculator team: 1099 income, quarterly estimated taxes, W-2 boxes, physician taxes and federal tax by salary for ' . TAX_YEAR . '.';
  $h1 = 'Tax guides &amp; articles';
  $crumb = [['Guides', '/blog/']];
}
$P['pageType'] = 'CollectionPage';
$slugs = live_posts();
$P['modified'] = max(array_map(fn($s) => POSTS[$s][2], $slugs));
$P['schema'][] = [
  '@type' => 'ItemList',
  'name' => strip_tags(html_entity_decode($h1)),
  'numberOfItems' => count($slugs),
  'itemListElement' => array_map(fn($s, $i) => [
    '@type' => 'ListItem', 'position' => $i + 1, 'url' => SITE_ORIGIN . post_url($s), 'name' => POSTS[$s][0]], $slugs, array_keys($slugs)),
];
?>
<section class="page-hero"><div class="wrap">
  <?= breadcrumbs($crumb) ?>
  <h1><?= $h1 ?></h1>
  <p class="lede">Clear, step-by-step explanations of the tax questions people actually search for, written for <?= TAX_YEAR ?> rules and paired with free calculators so you can run your own numbers.</p>
</div></section>

<section class="section-tight"><div class="wrap">
  <div class="sec-head">
    <span class="kicker">Latest guides</span>
    <h2>Understand your taxes, then estimate them</h2>
    <p>Each guide covers one topic in depth: freelance and 1099 income, quarterly estimated payments, reading your W-2, taxes for 1099 physicians, and how much federal income tax you will pay at different salaries. Examples use the same <?= TAX_YEAR ?> IRS figures as our calculators, so the numbers always match.</p>
  </div>
  <?= post_cards($slugs) ?>
</div></section>

<section class="section-tight section-alt"><div class="wrap">
  <div class="sec-head">
    <span class="kicker">Popular calculators</span>
    <h2>Put the guides into numbers</h2>
    <p>Free, no sign-up, updated for <?= TAX_YEAR ?>.</p>
  </div>
  <?= tool_cards(['federal-income-tax', '1099-tax-calculator', 'quarterly-estimated-tax', 'tax-refund-calculator', 'self-employment-tax', 'paycheck-calculator']) ?>
</div></section>
