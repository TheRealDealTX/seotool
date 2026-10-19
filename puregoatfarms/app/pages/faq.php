<?php
defined('PGF') || exit;

$groups = [
    'Goat milk' => [
        ['How much milk does a goat produce per day?', 'Most full-size dairy goats produce about 0.5 to 1.5 gallons (4–12 lb) per day. Nigerian Dwarfs give about 1–2 quarts.', '/how-much-milk-does-a-goat-produce-per-day/'],
        ['How much milk can a goat give at once?', 'Typically 2–4 lb (about 1–2 quarts) per milking on a twice-a-day schedule.', '/how-much-milk-can-a-goat-really-give-at-once/'],
        ['Do goats produce milk without being pregnant?', 'Normally no — a doe starts producing milk after she kids. Once in milk, many does can be milked through for 18 months or more without rebreeding.', '/do-goats-produce-milk-without-being-pregnant/'],
        ['Do goats give milk all the time?', 'No. A lactation lasts about 10 months after kidding, followed by a roughly two-month dry period before the next kidding.', '/do-goats-produce-milk-without-being-pregnant/'],
        ['How can I increase my goat\'s milk production?', 'Start with unlimited clean water, better forage (especially alfalfa), a balanced dairy ration, loose minerals and a steady milking schedule, then rule out parasites and mastitis.', '/how-to-increase-goat-milk-production/'],
    ],
    'Milking' => [
        ['How often do you milk a goat?', 'Most dairy goats are milked twice a day, about 12 hours apart. Once a day also works but yields roughly 15–25% less milk.', '/how-often-do-you-milk-a-goat/'],
        ['How long does it take to milk a goat?', 'About 5–10 minutes per doe for an experienced hand milker; beginners often take 15–20 minutes at first.', '/how-often-do-you-milk-a-goat/'],
        ['How much does a gallon of goat milk weigh?', 'About 8.6 pounds per US gallon.', '/tools/goat-milk-converter/'],
    ],
    'Breeds & herd planning' => [
        ['Which goat breed produces the most milk?', 'Saanens produce the most milk by volume, followed closely by Alpines.', '/best-dairy-goat-breeds-for-milk/'],
        ['Which goat breed has the richest milk?', 'Nigerian Dwarfs, at about 6–7% butterfat, followed by Nubians at 4.5–5%.', '/best-dairy-goat-breeds-for-milk/'],
        ['How many goats do you need to make cheese?', 'One good doe can supply small batches of fresh chevre; two or three does make regular firm-cheese making practical.', '/how-many-goats-do-you-need-to-make-cheese/'],
        ['Can you keep just one goat?', 'No — goats are herd animals and become stressed alone. Keep at least two, such as two does or a doe and a wether.', '/start-here/'],
    ],
    'Care & breeding' => [
        ['How long is a goat pregnant?', 'About 150 days on average, with 145–155 days considered normal.', '/tools/goat-gestation-calculator/'],
        ['How much hay does a goat eat per day?', 'Roughly 2.5–4% of body weight in forage per day — about 3–5 lb for a full-size goat.', '/tools/goat-feed-calculator/'],
        ['How much water does a goat need?', 'About 1 gallon per 100 lb of body weight for a dry goat, and 2–4 gallons or more for a milking doe.', '/tools/goat-feed-calculator/'],
    ],
];
$all = [];
foreach ($groups as $items) {
    foreach ($items as [$q, $a]) $all[] = [$q, $a];
}
$crumbs = [['Home', '/'], ['FAQ', '/faq/']];
$page = [
    'path'   => '/faq/',
    'title'  => 'Goat FAQ — Milk, Milking, Breeds & Care Answered | Pure Goat Farms',
    'desc'   => 'Quick answers to the goat questions we get asked most: how much milk goats produce, how often to milk, breeds, gestation, feed and water — from Pure Goat Farms.',
    'crumbs' => $crumbs,
    'schema' => [schema_faq($all)],
];
ob_start();
?>
<section class="page-hero">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span></div>
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow reveal">Goat FAQ</p>
    <h1 class="reveal">Straight answers to common goat questions.</h1>
    <p class="page-hero__lead reveal">The questions readers ask Pure Goat Farms most often, answered in a sentence or two — with a link to the full guide or tool when you want the detail.</p>
    <label class="search-field search-field--wide reveal"><?= icon('search') ?><span class="sr-only">Search questions</span><input type="search" placeholder="Search questions…" data-faq-search></label>
  </div>
</section>
<section class="section section--tight">
  <div class="container narrow">
<?php foreach ($groups as $g => $items): ?>
    <section class="faq faq--group" data-faq-group>
      <h2><?= e($g) ?></h2>
<?php foreach ($items as [$q, $a, $link]): ?>
      <details class="faq__item"><summary><?= e($q) ?><span class="faq__icon" aria-hidden="true"></span></summary><div class="faq__a"><p><?= e($a) ?></p><p><a class="link-arrow" href="<?= e($link) ?>">Learn more <?= icon('arrow') ?></a></p></div></details>
<?php endforeach; ?>
    </section>
<?php endforeach; ?>
    <p class="empty-state" hidden>No matching questions. <a href="/contact/">Ask us directly</a>.</p>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
