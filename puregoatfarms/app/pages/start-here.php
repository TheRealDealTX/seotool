<?php
defined('PGF') || exit;

$crumbs = [['Home', '/'], ['Start Here', '/start-here/']];
$page = [
    'path'   => '/start-here/',
    'title'  => 'Start Here: Beginner\'s Guide to Dairy Goats | Pure Goat Farms',
    'desc'   => 'New to dairy goats? Start here: a step-by-step path through choosing breeds, milk expectations, milking routines, feeding and kidding — with free planning tools.',
    'crumbs' => $crumbs,
    'schema' => [
        ['@type' => 'WebPage', '@id' => SITE_URL . '/start-here/#webpage', 'url' => SITE_URL . '/start-here/', 'name' => 'Start Here: Beginner\'s Guide to Dairy Goats', 'isPartOf' => ['@id' => SITE_URL . '/#website']],
    ],
];
$steps = [
    ['Decide what you want from your goats', 'Milk for the house, cheese, soap, brush clearing or simply good company? Your goal decides your breed, herd size and setup. Most families who want milk start with two dairy does.', [['Dairy Goat Breed Finder', '/tools/dairy-goat-breed-finder/'], ['Best dairy goat breeds for milk', '/best-dairy-goat-breeds-for-milk/']]],
    ['Set realistic milk expectations', 'A full-size dairy doe averages roughly three-quarters of a gallon a day across her lactation; a Nigerian Dwarf about a quart. Knowing this keeps you from buying too many — or too few — goats.', [['How much milk does a goat produce per day', '/how-much-milk-does-a-goat-produce-per-day/'], ['How much milk can a goat give at once', '/how-much-milk-can-a-goat-really-give-at-once/']]],
    ['Understand the lactation cycle', 'Goats only start producing milk after kidding, peak around six to eight weeks, and need a dry period before the next kidding. Plan breeding around when you want milk.', [['Do goats produce milk without being pregnant?', '/do-goats-produce-milk-without-being-pregnant/'], ['Goat Gestation Calculator', '/tools/goat-gestation-calculator/']]],
    ['Build a milking routine you can keep', 'Twice a day, about 12 hours apart, every day. Set up a milking stand, a stainless pail and a way to chill milk fast before your first doe freshens.', [['How often do you milk a goat', '/how-often-do-you-milk-a-goat/'], ['Goat Milk Yield Calculator', '/tools/goat-milk-yield-calculator/']]],
    ['Feed for health and milk', 'Good hay first, clean water always, loose goat minerals free-choice, and a dairy ration on the stand for milkers.', [['Goat Feed & Hay Calculator', '/tools/goat-feed-calculator/'], ['How to increase goat milk production', '/how-to-increase-goat-milk-production/']]],
    ['Turn surplus milk into something that keeps', 'Spring milk is abundant. Fresh chevre, aged cheese and frozen milk carry you through the dry months.', [['How many goats do you need to make cheese', '/how-many-goats-do-you-need-to-make-cheese/'], ['Goat Cheese Herd Calculator', '/tools/goat-cheese-herd-calculator/']]],
];
ob_start();
?>
<section class="page-hero">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span></div>
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow reveal">Start here</p>
    <h1 class="reveal">New to dairy goats? Start here.</h1>
    <p class="page-hero__lead reveal">A step-by-step path through everything Pure Goat Farms has published, in the order we wish we had learned it — from choosing a breed to your first wheel of cheese.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="container narrow">
    <ol class="path">
<?php foreach ($steps as $i => [$h, $p, $links]): ?>
      <li class="path__step reveal">
        <span class="path__n"><?= str_pad((string) ($i + 1), 2, '0', STR_PAD_LEFT) ?></span>
        <div class="path__body">
          <h2><?= e($h) ?></h2>
          <p><?= e($p) ?></p>
          <ul class="path__links">
<?php foreach ($links as [$l, $href]): ?>
            <li><a href="<?= e($href) ?>"><?= str_starts_with($href, '/tools/') ? icon('chart') : icon('book') ?> <?= e($l) ?></a></li>
<?php endforeach; ?>
          </ul>
        </div>
      </li>
<?php endforeach; ?>
    </ol>
  </div>
</section>
<section class="section section--sand">
  <div class="container narrow">
    <div class="checklist-card reveal" data-checklist>
      <h2>Before your first goats come home</h2>
      <p class="muted">Tick them off as you go — your progress is saved on this device.</p>
      <ul>
        <li><label><input type="checkbox"> Secure fencing at least 4 ft high (no gaps!)</label></li>
        <li><label><input type="checkbox"> Dry, draft-free shelter with bedding</label></li>
        <li><label><input type="checkbox"> Hay supply and feeder that limits waste</label></li>
        <li><label><input type="checkbox"> Water buckets or trough you can scrub daily</label></li>
        <li><label><input type="checkbox"> Loose goat minerals and a mineral feeder</label></li>
        <li><label><input type="checkbox"> A local vet who treats goats</label></li>
        <li><label><input type="checkbox"> Hoof trimmers and a basic first-aid kit</label></li>
        <li><label><input type="checkbox"> At least two goats — never just one</label></li>
      </ul>
      <p class="checklist-card__score"><strong data-done>0</strong> of 8 ready</p>
    </div>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
