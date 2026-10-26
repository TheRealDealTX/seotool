<?php defined('BO') || exit;
// Tools hub.
$crumbs = [['Home', '/'], ['Tools', '/tools/']];
$items = [];
$i = 1;
foreach ($TOOLS as $ts => $t) $items[] = ['@type' => 'ListItem', 'position' => $i++, 'url' => SITE_URL . '/tools/' . $ts . '/', 'name' => $t['h1']];
page_head([
    'title' => 'Free Archery Calculators & Bowhunting Tools | Better Outdoors',
    'desc'  => 'Free archery tools: draw length, arrow speed and kinetic energy calculators, a bow finder quiz and a printable bowhunting checklist.',
    'path'  => '/tools/',
    'schema' => [breadcrumb_schema($crumbs), ['@type' => 'ItemList', 'name' => 'Better Outdoors archery tools', 'itemListElement' => $items]],
]);
?>
<section class="page-hero mist-after">
  <div class="wrap">
    <?= breadcrumbs_html($crumbs) ?>
    <span class="eyebrow"><i class="fa-solid fa-screwdriver-wrench" aria-hidden="true"></i> 100% free, no sign-up</span>
    <h1>Free Archery &amp; Bowhunting Tools</h1>
    <p>Turn specs into decisions. These Better Outdoors calculators run right in your browser and work on any phone, so you can use them at the range, in the pro shop or in the stand.</p>
  </div>
</section>
<section class="section-mist" style="padding:10px 0 90px">
  <div class="wrap">
    <div class="tools-grid">
<?php $d = 0; foreach ($TOOLS as $ts => $t): ?>
      <a class="tool-card reveal reveal-d<?= $d++ % 4 ?>" href="/tools/<?= e($ts) ?>/"><div class="ico"><i class="fa-solid <?= e($t['icon']) ?>" aria-hidden="true"></i></div><h2 style="font-size:1.25rem"><?= e($t['h1']) ?></h2><p><?= e($t['desc']) ?></p><span class="go">Open tool <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span></a>
<?php endforeach; ?>
    </div>
    <div class="prose" style="max-width:860px;margin:60px auto 0">
      <h2 id="which-tool">Which Tool Should You Start With?</h2>
      <p>If you are buying or adjusting a bow, start with the <a href="/tools/draw-length-calculator/">draw length calculator</a>: fit comes first. Then use the <a href="/tools/bow-finder/">bow finder quiz</a> to see which compound bows we&rsquo;ve reviewed suit your draw length and hunting style. Already own your bow? The <a href="/tools/arrow-speed-calculator/">arrow speed calculator</a> and <a href="/tools/kinetic-energy-calculator/">kinetic energy calculator</a> tell you what your setup really delivers, and the <a href="/tools/bowhunting-checklist/">bowhunting checklist</a> makes sure nothing gets left in the truck.</p>
    </div>
  </div>
</section>
<?php page_foot(); ?>
