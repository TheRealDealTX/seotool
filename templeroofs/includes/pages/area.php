<?php
defined('TR_ROOT') || exit;
/** @var array $area */
$a = $area;
$crumbs = [['Service Areas', '/service-areas/'], [$a['city'] . ', TX', $a['url']]];
layout_start([
    'title'         => $a['seo_title'],
    'description'   => $a['meta_description'],
    'path'          => $a['url'],
    'crumbs'        => $crumbs,
    'image'         => $a['image'],
    'preload_image' => $a['image'],
    'body_class'    => 'page-area',
    'schema'        => [schema_faq($a['faqs'] ?? [])],
]);
page_hero([
    'h1' => $a['h1'], 'lead' => $a['hero_lead'], 'image' => $a['image'], 'alt' => $a['image_alt'], 'crumbs' => $crumbs,
    'eyebrow' => 'Service area · ' . $a['city'] . ', TX',
    'meta' => '<p class="hero-meta">' . icon('map-pin') . ' ' . e($a['distance_note']) . '</p>',
]);
?>
<div class="container content-layout">
  <article class="prose">
    <?= render_body($a['body'], 'Free roof inspections in ' . $a['city']) ?>
    <?= faq_html($a['faqs'] ?? [], 'Roofing Questions From ' . $a['city'] . ' Homeowners') ?>
  </article>
  <aside class="sidebar">
    <div class="sidebar__sticky">
      <div class="side-card side-card--form">
        <?php lead_form(['variant' => 'short', 'id' => 'side', 'title' => 'Free inspection in ' . $a['city'], 'subtitle' => 'No cost, no obligation.']); ?>
      </div>
      <div class="side-card">
        <p class="side-card__title">Other communities we serve</p>
        <ul class="side-links">
          <?php foreach (areas() as $o): if ($o['slug'] === $a['slug']) continue; ?>
          <li><a href="<?= e($o['url']) ?>"><?= icon('map-pin') ?> <?= e($o['city']) ?>, TX</a></li>
          <?php endforeach; ?>
        </ul>
      </div>
    </div>
  </aside>
</div>
<div class="container">
  <?= related_html($a['related_services'] ?? [], $a['related_posts'] ?? []) ?>
</div>
<?php final_cta('Need a Roofer in ' . $a['city'] . '? Start With a Free Inspection.', '', $a['url']); ?>
<?php layout_end();
