<?php
/** Service-area page template. Expects $slug; included from /service-areas/<slug>/index.php. */
if (!isset($slug)) { http_response_code(404); exit; }
require_once dirname(__DIR__) . '/bootstrap.php';
$a = $AREAS[$slug];
$path = "/service-areas/$slug/";
$crumbs = [['Home', '/'], ['Service Areas', '/service-areas/'], ['Roofing ' . $a['name'] . ', TX', $path]];

page_start([
    'title'       => $a['title'],
    'description' => $a['description'],
    'path'        => $path,
    'image'       => 'LOCAL-ROOFING-IN-BASTROP-TEXAS.webp',
    'body'        => 'page-area',
    'schema'      => [
        service_schema('Roofing in ' . $a['name'] . ', TX', $a['description'], $path, $a['name'] . ', TX'),
        breadcrumb_schema($crumbs),
        faq_schema($a['faqs']),
    ],
]);
page_hero('Bastrop Roofing serves ' . $a['name'], $a['h1'], $a['lead'], $crumbs, 'LOCAL-ROOFING-IN-BASTROP-TEXAS.webp');
?>
<section class="section">
  <div class="container with-sidebar">
    <article class="prose">
      <div class="area-facts reveal">
        <div><?= icon('pin') ?><span><strong><?= e($a['name']) ?>, TX <?= e($a['zip']) ?></strong><?= e($a['county']) ?></span></div>
        <div><?= icon('clock') ?><span><strong>From our Bastrop base</strong><?= e($a['distance']) ?></span></div>
      </div>
<?php foreach ($a['sections'] as $sec): ?>
      <h2><?= e($sec['h2']) ?></h2>
      <?= $sec['html'] ?>
<?php endforeach; ?>
      <div class="two-lists reveal">
        <div>
          <h2>Neighborhoods &amp; Areas</h2>
          <ul class="check-list">
<?php foreach ($a['neighborhoods'] as $n): ?>
            <li><?= icon('home') ?> <?= e($n) ?></li>
<?php endforeach; ?>
          </ul>
        </div>
        <div>
          <h2>Local Landmarks</h2>
          <ul class="check-list">
<?php foreach ($a['landmarks'] as $l): ?>
            <li><?= icon('pin') ?> <?= e($l) ?></li>
<?php endforeach; ?>
          </ul>
        </div>
      </div>
    </article>
    <?php sidebar('Roofing in ' . $a['name'] . '? Call Us'); ?>
  </div>
</section>

<section class="section section-tint">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Services in <?= e($a['name']) ?></span>
      <h2 class="section-title small">Roofing Services Available in <?= e($a['name']) ?>, TX</h2>
    </div>
    <div class="card-grid"><?php service_cards(); ?></div>
  </div>
</section>

<?php faq_block($a['faqs'], 'Roofing in ' . $a['name'] . ': FAQ'); ?>
<?php
cta_band('Need a Roofer in ' . $a['name'] . ', TX?');
page_end();
