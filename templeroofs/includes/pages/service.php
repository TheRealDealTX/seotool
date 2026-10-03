<?php
defined('TR_ROOT') || exit;
/** @var array $service */
$s = $service;
$crumbs = [['Roofing Services', '/services/'], [$s['name'], $s['url']]];
layout_start([
    'title'         => $s['seo_title'],
    'description'   => $s['meta_description'],
    'path'          => $s['url'],
    'crumbs'        => $crumbs,
    'image'         => $s['image'],
    'preload_image' => $s['image'],
    'body_class'    => 'page-service',
    'schema'        => [schema_service($s), schema_faq($s['faqs'] ?? [])],
]);
page_hero(['h1' => $s['h1'], 'lead' => $s['hero_lead'], 'image' => $s['image'], 'alt' => $s['image_alt'], 'crumbs' => $crumbs, 'eyebrow' => $s['name'] . ' · Temple, TX']);
?>
<div class="container content-layout">
  <article class="prose">
    <?= render_body($s['body'], 'Not sure what your roof needs? Start with a free inspection.') ?>
    <?= faq_html($s['faqs'] ?? [], $s['name'] . ' FAQs') ?>
  </article>
  <aside class="sidebar">
    <div class="sidebar__sticky">
      <div class="side-card side-card--form">
        <?php lead_form(['variant' => 'short', 'id' => 'side', 'title' => 'Free roof inspection', 'subtitle' => 'No cost, no obligation. Tell us what you are seeing.', 'concern' => service_concern($s['slug'])]); ?>
      </div>
      <div class="side-card">
        <p class="side-card__title">Other roofing services</p>
        <ul class="side-links">
          <?php foreach (services() as $o): if ($o['slug'] === $s['slug']) continue; ?>
          <li><a href="<?= e($o['url']) ?>"><?= icon($o['icon'] ?? 'home') ?> <?= e($o['name']) ?></a></li>
          <?php endforeach; ?>
        </ul>
      </div>
    </div>
  </aside>
</div>
<div class="container">
  <?= related_html($s['related_services'] ?? [], $s['related_posts'] ?? [], $s['slug']) ?>
</div>
<?php final_cta('Schedule Your Free Roof Inspection in Temple', '', $s['url']); ?>
<?php layout_end();
