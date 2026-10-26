<?php
/** @var string $toolSlug */
[$key, $name, $desc, $ic] = TOOLS[$toolSlug];
$copy = require BASE_DIR . '/data/tool-copy.php';
$c = $copy[$toolSlug];
$widget = tool_html($key, 'full');
[$cbody] = render_body($c['body']);
$meta = [
    'title' => $c['title'],
    'description' => $c['description'],
    'url' => "/tools/$toolSlug/",
    'schema' => [
        ['@type' => 'WebApplication', 'name' => $name, 'url' => SITE_URL . "/tools/$toolSlug/", 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any', 'description' => $desc, 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'publisher' => ['@id' => SITE_URL . '/#org']],
        schema_breadcrumbs([['Home', '/'], ['Free Tools', '/tools/'], [$name, "/tools/$toolSlug/"]]),
        schema_faq($c['faq']),
    ],
];
require __DIR__ . '/header.php';
?>
<section class="page-hero">
  <canvas class="coin-canvas" data-density="0.4" aria-hidden="true"></canvas>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/tools/">Free Tools</a><span>/</span><?= e($name) ?></nav>
    <span class="pill">Free tool</span>
    <h1><?= e($c['h1']) ?></h1>
    <p class="dek"><?= e($desc) ?></p>
  </div>
</section>
<div class="wrap article-layout">
  <div class="article-body">
    <?= $widget ?>
    <?= $cbody ?>
    <section class="article-faq">
      <h2 id="faq">Frequently asked questions</h2>
      <div class="faq">
        <?php foreach ($c['faq'] as $i => $f): ?>
        <details<?= $i === 0 ? ' open' : '' ?>><summary><?= e($f['q']) ?></summary><div><p><?= e($f['a']) ?></p></div></details>
        <?php endforeach; ?>
      </div>
    </section>
    <?= gear_box($c['gear'], 'Helpful gear') ?>
  </div>
  <aside class="sidebar">
    <div class="toc"><h2>More free tools</h2><ol>
      <?php foreach (TOOLS as $s => [, $n]) if ($s !== $toolSlug) echo '<li><a href="/tools/' . $s . '/">' . e($n) . '</a></li>'; ?>
    </ol></div>
    <div class="toc"><h2>Related guides</h2><ol>
      <?php foreach ($c['guides'] as $g) if ($p = content_load($g)) echo '<li><a href="' . e($p['url']) . '">' . e($p['h1']) . '</a></li>'; ?>
    </ol></div>
  </aside>
</div>
<?php require __DIR__ . '/footer.php'; ?>
