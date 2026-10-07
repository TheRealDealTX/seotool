<?php
defined('GAP') || exit;
/** @var array $g */
$trail = [['Guides', '/guides/'], [$g['h1'], $g['path']]];
$related = [];
foreach ($g['related_paths'] ?? [] as $rp) if ($x = product($rp)) $related[] = $x;
$relCats = array_filter(array_map(fn($rp) => category($rp), $g['related_paths'] ?? []));
$meta = [
    'title' => $g['title'], 'desc' => $g['meta'], 'canonical' => $g['path'], 'og_type' => 'article',
    'jsonld' => array_filter([['@type' => 'Article', 'headline' => $g['h1'], 'description' => $g['meta'], 'url' => abs_url($g['path']), 'publisher' => ['@id' => abs_url('/#org')], 'dateModified' => $CAT['built']], crumbs_ld($trail), faq_ld($g['faq'] ?? [])]),
    'body_class' => 'is-guide',
];
?>
<article>
<section class="cat-hero guide-hero"><div class="wrap narrow">
  <?= crumbs($trail) ?>
  <p class="eyebrow"><?= (int)$g['read_minutes'] ?> min read</p>
  <h1><?= e($g['h1']) ?></h1>
  <p class="lede"><?= e($g['dek']) ?></p>
</div></section>
<div class="wrap guide-layout">
  <div class="prose">
    <nav class="toc" aria-label="In this guide"><h2>In this guide</h2><ol><?php foreach ($g['sections'] as $i => $s): ?><li><a href="#s<?= $i ?>"><?= e($s['h']) ?></a></li><?php endforeach; ?></ol></nav>
<?php foreach ($g['sections'] as $i => $s): ?>
    <h2 id="s<?= $i ?>"><?= e($s['h']) ?></h2>
<?php foreach ($s['p'] ?? [] as $para): ?>    <p><?= rich($para) ?></p>
<?php endforeach; ?>
<?php if (!empty($s['list'])): ?>    <ul><?php foreach ($s['list'] as $li): ?><li><?= rich($li) ?></li><?php endforeach; ?></ul>
<?php endif; ?>
<?php endforeach; ?>
    <?= faq_block($g['faq'] ?? []) ?>
  </div>
  <aside class="guide-side sticky-side">
<?php if ($relCats): ?><div class="aside-box"><h2>Shop this guide</h2><ul class="aside-links"><?php foreach ($relCats as $rc): ?><li><a href="<?= e($rc['path']) ?>"><?= e($rc['name']) ?></a></li><?php endforeach; ?></ul></div><?php endif; ?>
<?php foreach (array_slice($related, 0, 3) as $p) echo product_card($p, 'card-compact'); ?>
  </aside>
</div>
</article>
