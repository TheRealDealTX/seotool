<?php
/** Service page template. Expects $slug; included from /services/<slug>/index.php. */
if (!isset($slug)) { http_response_code(404); exit; }
require_once dirname(__DIR__) . '/bootstrap.php';
$s = $SERVICES[$slug];
$path = "/services/$slug/";
$crumbs = [['Home', '/'], ['Services', '/services/'], [$s['name'], $path]];

page_start([
    'title'       => $s['title'],
    'description' => $s['description'],
    'path'        => $path,
    'image'       => $s['image'],
    'preload'     => $s['image'],
    'body'        => 'page-service',
    'schema'      => [
        service_schema($s['name'] . ' in Bastrop, TX', $s['description'], $path),
        breadcrumb_schema($crumbs),
        faq_schema($s['faqs']),
    ],
]);
page_hero('Bastrop Roofing · ' . $s['name'], $s['h1'], $s['lead'], $crumbs, $s['image']);
?>
<section class="section">
  <div class="container with-sidebar">
    <article class="prose">
      <figure class="prose-figure reveal">
        <img src="<?= img($s['image']) ?>" alt="<?= e($s['name']) ?> by Bastrop Roofing in Bastrop, TX" width="1200" height="655" loading="lazy">
      </figure>
<?php foreach ($s['sections'] as $sec): ?>
      <h2><?= e($sec['h2']) ?></h2>
      <?= $sec['html'] ?>
<?php endforeach; ?>

      <div class="signs-box reveal">
        <h2>Signs You May Need <?= e($s['name']) ?></h2>
        <ul class="check-list">
<?php foreach ($s['signs'] as $sign): ?>
          <li><?= icon('check') ?> <?= e($sign) ?></li>
<?php endforeach; ?>
        </ul>
      </div>
    </article>
    <?php sidebar(); ?>
  </div>
</section>

<section class="section section-tint">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Free interactive tool</span>
      <h2 class="section-title"><?= e($TOOLS[$s['tool']]['name']) ?></h2>
      <p class="section-copy"><?= e($TOOLS[$s['tool']]['lead']) ?></p>
    </div>
    <?php include dirname(__DIR__) . '/tools/' . $s['tool'] . '.php'; ?>
  </div>
</section>

<?php faq_block($s['faqs'], $s['name'] . ' Questions'); ?>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Related services</span>
      <h2 class="section-title small">More Roofing Services in Bastrop</h2>
    </div>
    <div class="card-grid card-grid-3"><?php service_cards($s['related']); ?></div>
  </div>
</section>
<?php
cta_band();
page_end();
