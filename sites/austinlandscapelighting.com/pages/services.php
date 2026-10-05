<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Services', '/services/']];
$items = array_map(fn($s) => [$s['name'], $s['path']], array_values(services()));
$page = [
    'title' => 'Landscape Lighting Services in Austin, TX',
    'description' => 'Every outdoor lighting service from Austin Landscape Lighting: uplighting, path and tree lighting, patios, pools, smart controls, LED retrofits and repair.',
    'path' => '/services/',
    'active' => '/services/',
    'image' => 'austin-landscape-lighting-service-1',
    'schema' => [schema_webpage(['title' => 'Landscape Lighting Services', 'description' => 'Austin Landscape Lighting services.', 'path' => '/services/'], 'CollectionPage'), schema_breadcrumb($crumbs), schema_itemlist($items, 'Austin Landscape Lighting services')],
];
ob_start();
echo sub_hero(['eyebrow' => 'Services', 'h1' => 'Landscape Lighting Services in Austin, TX', 'intro' => 'Twelve ways Austin Landscape Lighting brings a property to life after dark, from a single lit entry to a fully layered estate design. Every service uses low-voltage LED, solid brass fixtures and a night aiming visit.', 'image' => 'austin-landscape-lighting-service-1', 'image_alt' => 'Austin Landscape Lighting technician installing brass path lights', 'crumbs' => $crumbs]);
?>
<section class="section">
  <div class="container">
    <div class="grid grid--3">
      <?php foreach (array_values(services()) as $i => $s) echo service_card($s, $i); ?>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="container feature-split">
    <div data-reveal="left">
      <p class="eyebrow">How we work</p>
      <h2 class="display">One designer, one plan, one glow</h2>
      <p class="lede">Most Austin Landscape Lighting projects combine three or four of these services. We never sell fixtures by the box. A designer walks your property at dusk, proposes a layered plan and prices it line by line.</p>
      <ul class="checks">
        <li><?= icon('pencil') ?><div><strong>Design-first</strong><span>Techniques, beam spreads and color temperature chosen before a single fixture is ordered.</span></div></li>
        <li><?= icon('bolt') ?><div><strong>Low-voltage LED only</strong><span>12-volt systems: safe to bury, cheap to run and friendly to Austin's dark-sky sensibilities.</span></div></li>
        <li><?= icon('warranty') ?><div><strong>Two-year workmanship warranty</strong><span>Plus brass fixture warranties that outlast most roofs.</span></div></li>
      </ul>
      <div style="margin-top:24px"><a class="btn btn--primary" href="/contact/">Book a free consultation <?= icon('arrow') ?></a></div>
    </div>
    <div class="feature-split__media" data-reveal="right"><?= picture('professional-landscape-lighting-austin-1', 'Professional landscape lighting installation in Austin', ['width' => 1600, 'height' => 1200]) ?></div>
  </div>
</section>
<?= cta_band() ?>
<?php
render_page($page, ob_get_clean());
