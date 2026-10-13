<?php
// Shared layout for the /tools/ calculator pages.
require_once __DIR__ . '/layout.php';

const TOOLS = [
    'claim-settlement-calculator'   => ['Claim Settlement Calculator', '&#129518;', 'Estimate your first check and your total payout from replacement cost, depreciation and deductible.'],
    'public-adjuster-fee-calculator' => ['Public Adjuster Fee Calculator', '&#128181;', 'Compare what you keep with and without a public adjuster, and find your break-even point.'],
    'hurricane-deductible-calculator' => ['Hurricane Deductible Calculator', '&#127744;', 'Convert a 1%–5% named-storm deductible into dollars and compare it with your standard deductible.'],
    'depreciation-calculator'       => ['Depreciation Calculator', '&#128201;', 'Check the carrier’s depreciation on a roof, flooring, HVAC or contents using age and useful life.'],
    'claim-deadline-calculator'     => ['Texas Claim Deadline Calculator', '&#128197;', 'Map Texas Prompt Payment Act deadlines and key policy dates for your claim.'],
    'additional-living-expense-calculator' => ['Additional Living Expense Calculator', '&#127976;', 'Estimate your Loss of Use (Coverage D) claim when you can’t live at home.'],
    'contents-inventory'            => ['Contents Inventory Builder', '&#128203;', 'List damaged belongings room by room, total them, then print or export to CSV.'],
];

/**
 * $t keys: slug, title, desc, h1, lede, form (html), prose (html), faqs ([[q,a]...])
 */
function tool_page(array $t): void {
    $path = '/tools/' . $t['slug'] . '/';
    $crumbs = [['Home', '/'], ['Claim Tools', '/tools/'], [TOOLS[$t['slug']][0], $path]];
    $schema = [[
        '@type' => 'WebApplication',
        'name' => TOOLS[$t['slug']][0],
        'url' => SITE_URL . $path,
        'applicationCategory' => 'FinanceApplication',
        'operatingSystem' => 'Any (runs in the browser)',
        'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
        'provider' => ['@id' => SITE_URL . '/#business'],
        'description' => $t['desc'],
    ]];
    if (!empty($t['faqs'])) $schema[] = faq_schema($t['faqs']);
    page_start([
        'title' => $t['title'],
        'desc' => $t['desc'],
        'path' => $path,
        'crumbs' => $crumbs,
        'schema' => $schema,
        'scripts' => ['/assets/js/tools.js'],
    ]);
    echo page_hero($t['h1'], $t['lede'], $crumbs, 'Free tool from Houston Public Adjusters');
    ?>
<div class="wrap layout-sidebar">
  <div>
    <div class="tool"><?= $t['form'] ?></div>
    <p class="tool-note">Estimates only, for planning. Your policy language, the carrier&rsquo;s estimate and Texas law control your actual claim. Nothing you enter leaves your browser.</p>
    <div class="prose"><?= $t['prose'] ?>
<?php if (!empty($t['faqs'])): ?>
      <h2>Frequently asked questions</h2>
      <?= faq_html($t['faqs']) ?>
<?php endif; ?>
      <?= author_box() ?>
    </div>
  </div>
  <aside class="sidebar">
    <div class="side-card sticky"><?= lead_form('lead-tool', 'Get a real number', 'A licensed Houston public adjuster will review your claim for free.', true) ?></div>
    <div class="side-card">
      <h3>More claim tools</h3>
      <ul class="link-list">
<?php foreach (TOOLS as $slug => [$name]): if ($slug === $t['slug']) continue; ?>
        <li><a href="/tools/<?= $slug ?>/"><?= e($name) ?></a></li>
<?php endforeach; ?>
        <li><a href="/houston-weather/">Live Houston weather tracker</a></li>
      </ul>
    </div>
  </aside>
</div>
<?php
    page_end();
}
