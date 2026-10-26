<?php
$meta = [
    'title' => 'Free Side Hustle Calculators & Tools | ' . SITE_NAME,
    'description' => 'Free side hustle tools: find your match with our quiz, then calculate income, gig driver pay, self-employment tax, freelance rates and product profit.',
    'url' => '/tools/',
    'schema' => [
        ['@type' => 'CollectionPage', 'name' => 'Free Side Hustle Tools', 'url' => SITE_URL . '/tools/'],
        schema_breadcrumbs([['Home', '/'], ['Free Tools', '/tools/']]),
    ],
];
require __DIR__ . '/header.php';
?>
<section class="page-hero">
  <canvas class="coin-canvas" data-density="0.4" aria-hidden="true"></canvas>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Free Tools</nav>
    <span class="pill">100% free · no sign-up</span>
    <h1>Free side hustle calculators</h1>
    <p class="dek">Pick a side hustle, price your work, see your true hourly pay and know exactly what to set aside for taxes.</p>
  </div>
</section>
<section class="section" style="padding-top:56px">
  <div class="wrap">
    <div class="grid grid-4">
      <?php foreach (TOOLS as $slug => [, $name, $desc, $ic]): ?>
      <a class="card tool-card glow reveal" href="/tools/<?= $slug ?>/"><span class="ti"><?= icon($ic) ?></span><h3><?= e($name) ?></h3><p><?= e($desc) ?></p><span class="more">Open tool <?= icon('arrow') ?></span></a>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section section-soft">
  <div class="wrap" style="max-width:860px"><?= tool_html('income-calculator', 'full') ?></div>
</section>
<?php require __DIR__ . '/footer.php'; ?>
