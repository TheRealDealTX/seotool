<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$s = service($slug);
[$body, $toc] = with_heading_ids($s['body']);
$crumbs = [['Home', '/'], ['Services', '/services/'], [$s['name'], $s['path']]];
$related = [];
foreach ($s['related'] ?? [] as $r) {
    if ($rs = service($r)) {
        $related[] = [$rs['name'], $rs['path']];
    }
}
$otherLinks = [];
foreach (services() as $o) {
    if ($o['slug'] !== $slug) {
        $otherLinks[] = [$o['name'], $o['path']];
    }
}
$page = [
    'title' => $s['title'],
    'description' => $s['description'],
    'path' => $s['path'],
    'image' => $s['image'],
    'active' => '/services/',
    'schema' => [schema_webpage(['title' => $s['title'], 'description' => $s['description'], 'path' => $s['path'], 'image' => $s['image']]), schema_breadcrumb($crumbs), schema_service($s), schema_faq($s['faqs'])],
];
$hl = '';
foreach ($s['highlights'] as $h) {
    $hl .= '<li>' . icon('check', 'ico ico--sm') . e($h) . '</li>';
}
ob_start();
echo sub_hero(['eyebrow' => $s['eyebrow'], 'h1' => e($s['h1']), 'intro' => e($s['intro']), 'image' => $s['image'], 'image_alt' => $s['image_alt'], 'crumbs' => $crumbs]);
?>
<section class="section">
  <div class="container layout">
    <article class="prose" data-reveal>
      <ul class="highlights"><?= $hl ?></ul>
      <?php if (!empty($s['range'])): ?>
      <div class="range-card"><strong><?= e($s['range']) ?></strong><span><?= e($s['range_note'] ?? 'Typical planning range. Your written estimate is exact.') ?> <a href="/tools/cost-estimator/">Try the cost estimator</a>.</span></div>
      <?php endif; ?>
      <?= $body ?>
      <?php if (!empty($s['gallery'])): ?>
      <h2 id="recent-work">Recent <?= e(strtolower($s['name'])) ?> work</h2>
      <div class="gallery-strip" data-lightbox>
        <?php foreach ($s['gallery'] as $g) echo picture($g, $s['name'] . ' project in Austin by Austin Landscape Lighting', ['width' => 1600, 'height' => 1200, 'sizes' => '(max-width: 760px) 100vw, 25vw']); ?>
      </div>
      <?php endif; ?>
      <h2 id="faq"><?= e($s['name']) ?> FAQ</h2>
      <?= faq_list($s['faqs'], 'svc-faq') ?>
    </article>
    <?= sidebar(['toc' => $toc, 'links' => $related ?: array_slice($otherLinks, 0, 4), 'links_title' => 'Related services']) ?>
  </div>
</section>
<section class="section section--alt section--tight">
  <div class="container">
    <?= section_head('More from Austin Landscape Lighting', 'Explore other services', '', 'left') ?>
    <div class="grid grid--4">
      <?php $i = 0; foreach (services() as $o) { if ($o['slug'] === $slug) continue; if ($i++ >= 4) break; echo service_card($o, $i); } ?>
    </div>
  </div>
</section>
<?= contact_section('Free design consultation', 'Get ' . strtolower($s['name']) . ' designed for your home', $slug) ?>
<?php
render_page($page, ob_get_clean());
