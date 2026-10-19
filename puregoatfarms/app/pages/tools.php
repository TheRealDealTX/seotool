<?php
defined('PGF') || exit;

$crumbs = [['Home', '/'], ['Tools', '/tools/']];
$items = [];
$i = 1;
foreach (TOOLS as $slug => $t) {
    $items[] = ['@type' => 'ListItem', 'position' => $i++, 'url' => SITE_URL . "/tools/$slug/", 'name' => $t['name']];
}
$page = [
    'path'   => '/tools/',
    'title'  => 'Free Goat Calculators & Tools — Milk, Kidding, Feed | Pure Goat Farms',
    'desc'   => 'Free goat calculators from Pure Goat Farms: milk yield, lactation curve, cheese herd size, gestation and kidding dates, feed and hay, breed finder and milk converter.',
    'crumbs' => $crumbs,
    'schema' => [
        ['@type' => 'CollectionPage', '@id' => SITE_URL . '/tools/#webpage', 'url' => SITE_URL . '/tools/', 'name' => 'Free Goat Calculators & Tools', 'isPartOf' => ['@id' => SITE_URL . '/#website'], 'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => $items]],
    ],
];
ob_start();
?>
<section class="page-hero page-hero--tools">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="blob blob--3"></span></div>
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow reveal">Free goat tools</p>
    <h1 class="reveal">Goat calculators that do the math for you.</h1>
    <p class="page-hero__lead reveal">The planning tools we use around Pure Goat Farms — for milk, kidding, feed, cheese and choosing a breed. Free, no sign-up, and everything runs privately in your browser.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="container">
    <div class="tool-grid">
<?php foreach (TOOLS as $slug => $t): ?>
      <?= tool_card($slug, $t) ?>
<?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section section--sand">
  <div class="container narrow prose">
    <h2>How to use these goat tools</h2>
    <p>Each calculator gives a practical estimate based on typical numbers for healthy, well-managed goats. Use them to plan — how many does to keep, when kids are due, how much hay to buy — and then refine with your own records. Weighing milk and logging feed is still the best way to learn your herd.</p>
    <p>Looking for the reasoning behind the numbers? Each tool links to the in-depth guide it is based on, such as <a href="/how-much-milk-does-a-goat-produce-per-day/">how much milk does a goat produce per day</a> or <a href="/how-many-goats-do-you-need-to-make-cheese/">how many goats you need to make cheese</a>.</p>
    <p class="muted small">These tools are for general planning and education only. Always talk to your veterinarian about animal health, feeding changes and reproduction.</p>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
