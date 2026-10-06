<?php defined('SLT') || exit;
$slug = $GLOBALS['SLUG']; $a = AREAS[$slug];
ob_start(); include APP . '/areas/' . $slug . '.php'; $content = ob_get_clean();
page_hero(['title' => 'Landscape Lighting in ' . e($a['name']), 'eyebrow' => 'Service area', 'sub' => 'Custom landscape lighting design, installation, repair and LED upgrades for homes in ' . e($a['name']) . ', from Spring Landscape Lighting.', 'cta' => true,
    'crumbs' => [['Home', '/'], ['Service Areas', '/service-areas/'], [$a['name'], null]]]);
?>
<section class="sec">
  <div class="wrap article">
    <div class="prose"><?= $content ?></div>
    <aside class="aside">
      <div class="formcard"><h3 style="font-size:1.35rem">Free consultation in <?= e($a['short']) ?></h3><?php quote_form('area', true); ?></div>
      <div class="toc"><h4>Other areas we serve</h4><ol><?php foreach (AREAS as $k => $o) if ($k !== $slug) echo '<li><a href="/service-areas/' . $k . '/">' . e($o['name']) . '</a></li>'; ?></ol></div>
    </aside>
  </div>
</section>
<section class="sec sec--forest">
  <div class="wrap">
    <?php section_head('Services in ' . e($a['short']), 'Landscape lighting services for ' . e($a['short']) . ' homes', 'Everything Spring Landscape Lighting offers is available throughout ' . e($a['name']) . '.'); ?>
    <div class="grid-3"><?php $i = 0; foreach (SERVICES as $k => $s) echo service_card($k, $s, $i++); ?></div>
  </div>
</section>
<?php cta_band('Light up your ' . e($a['short']) . ' home'); ?>
