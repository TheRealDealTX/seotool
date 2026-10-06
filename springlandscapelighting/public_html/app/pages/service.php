<?php defined('SLT') || exit;
$slug = $GLOBALS['SLUG']; $s = SERVICES[$slug];
add_schema(['@type' => 'Service', 'name' => $s['name'], 'serviceType' => $s['name'], 'description' => $s['desc'],
    'provider' => ['@id' => SITE_URL . '/#business'], 'areaServed' => array_map(fn($a) => $a['name'], array_values(AREAS)), 'url' => abs_url('/services/' . $slug . '/')]);
ob_start(); include APP . '/services/' . $slug . '.php'; $content = ob_get_clean();
page_hero(['title' => e($s['name']) . ' in Spring, TX', 'eyebrow' => 'Spring Landscape Lighting services', 'sub' => e($s['blurb']), 'cta' => true, 'tall' => true,
    'img' => in_array($slug, ['tree-garden-lighting', 'pathway-driveway-lighting']) ? 'Spring-Landscape-Lighting-BG-1.webp' : ($slug === 'patio-pool-lighting' ? 'How-Much-Electricity-Does-Landscape-Lighting-Use.webp' : 'Spring-Landscape-Lighting-BG-2.webp'),
    'crumbs' => [['Home', '/'], ['Services', '/services/'], [$s['name'], null]]]);
?>
<section class="sec">
  <div class="wrap article">
    <div class="prose"><?= $content ?></div>
    <aside class="aside">
      <div class="side-cta"><span class="eyebrow eyebrow--glow">Free consultation</span><h4>Plan your <?= e(strtolower($s['short'])) ?> lighting</h4><p>Get a custom plan from Spring Landscape Lighting.</p><a class="btn btn--glow" href="/quote/">Request a quote</a><a class="btn btn--ghost" href="tel:<?= PHONE_TEL ?>"><?= icon('phone') ?><?= PHONE ?></a></div>
      <div class="toc"><h4>Other services</h4><ol><?php foreach (SERVICES as $k => $o) if ($k !== $slug) echo '<li><a href="/services/' . $k . '/">' . e($o['name']) . '</a></li>'; ?></ol></div>
      <div class="toc"><h4>Free tools</h4><ol><li><a href="/tools/lighting-visualizer/">Lighting visualizer</a></li><li><a href="/tools/fixture-estimator/">Fixture estimator</a></li><li><a href="/tools/energy-cost-calculator/">Energy cost calculator</a></li></ol></div>
    </aside>
  </div>
</section>
<section class="sec sec--forest">
  <div class="wrap">
    <?php section_head('How we work', 'Six steps from first call to final glow', 'Every ' . e(strtolower($s['name'])) . ' project follows the same clear, collaborative process.'); ?>
    <?php process_strip(); ?>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <?php section_head('Complete the picture', 'Pair it with these services', 'The best results come from layering techniques across the whole property.'); ?>
    <div class="grid-3"><?php $i = 0; foreach (SERVICES as $k => $o) { if ($k === $slug || $i >= 3) continue; echo service_card($k, $o, $i++); } ?></div>
  </div>
</section>
<?php cta_band('Ready for ' . e(strtolower($s['name'])) . ' that looks intentional?'); ?>
