<?php
/** @var string $slug @var array $tool */
$crumbs = [['Home', '/'], ['Farm Tools', '/tools/'], [$tool['name'], '/tools/' . $slug . '/']];
$heroTitle = $tool['title']; $heroLede = e($tool['short']); $heroEyebrow = icon($tool['icon']) . ' Free tool from Purely Wholesome Farm';
include __DIR__ . '/partials/page-hero.php';
$guides = array_slice(array_values(topic_posts($tool['topic'])), 0, 4);
$others = array_slice(array_filter(tools(), fn($k) => $k !== $slug, ARRAY_FILTER_USE_KEY), 0, 3, true);
?>
<section class="section section--tight">
  <div class="wrap wrap--tool">
    <?= render_tool($slug) ?>
    <div class="tool-doc prose">
      <h2>How it works</h2>
      <?= $tool['intro'] ?>
      <h2>How to use the <?= e(strtolower($tool['name'])) ?></h2>
      <ol><?php foreach ($tool['how'] as $step): ?><li><?= e($step) ?></li><?php endforeach ?></ol>
      <?php if ($tool['faq']): ?>
        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq">
          <?php foreach ($tool['faq'] as $i => [$q, $a]): ?>
            <details class="faq__item" <?= $i === 0 ? 'open' : '' ?>><summary><?= e($q) ?><span class="faq__icon" aria-hidden="true"></span></summary><div class="faq__a"><p><?= e($a) ?></p></div></details>
          <?php endforeach ?>
        </div>
      <?php endif ?>
      <?php if ($tool['sources']): ?>
        <h2>Sources</h2>
        <ul class="sources"><?php foreach ($tool['sources'] as [$label, $url]): ?><li><a href="<?= e($url) ?>" target="_blank" rel="noopener"><?= e($label) ?></a></li><?php endforeach ?></ul>
      <?php endif ?>
      <p class="tool-disclaimer">Results are planning guides based on typical values. Always use a thermometer and follow tested recipes; for animal health questions, your veterinarian has the final word.</p>
    </div>
  </div>
</section>
<?php if ($guides): ?>
<section class="section section--cream">
  <div class="wrap">
    <header class="section__head"><p class="eyebrow">Related guides</p><h2>Read more on Purely Wholesome Farm</h2></header>
    <div class="cards cards--4"><?php foreach ($guides as $p): ?><?= card($p, 'reveal') ?><?php endforeach ?></div>
  </div>
</section>
<?php endif ?>
<section class="section">
  <div class="wrap">
    <header class="section__head"><p class="eyebrow">More tools</p><h2>Try another farm tool</h2></header>
    <div class="tool-cards tool-cards--3">
      <?php foreach ($others as $k => $t): ?><a class="tool-card tool-card--light" href="/tools/<?= $k ?>/"><span class="tool-card__icon tool-card__icon--<?= $t['color'] ?>"><?= icon($t['icon']) ?></span><strong><?= e($t['name']) ?></strong><small><?= e($t['short']) ?></small><span class="tool-card__go">Open tool <?= icon('arrow') ?></span></a><?php endforeach ?>
    </div>
  </div>
</section>
