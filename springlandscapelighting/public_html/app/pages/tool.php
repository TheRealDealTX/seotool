<?php defined('SLT') || exit;
$slug = $GLOBALS['SLUG']; $t = TOOLS[$slug];
add_schema(['@type' => 'WebApplication', 'name' => $t['name'], 'description' => $t['meta'], 'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any',
    'url' => abs_url('/tools/' . $slug . '/'), 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'publisher' => ['@id' => SITE_URL . '/#business']]);
page_hero(['title' => e($t['name']), 'eyebrow' => 'Free tool by Spring Landscape Lighting', 'sub' => e($t['desc']),
    'crumbs' => [['Home', '/'], ['Tools', '/tools/'], [$t['name'], null]]]);
?>
<section class="sec" style="padding-top:20px">
  <div class="wrap">
    <div data-reveal="zoom"><?php tool_embed($slug, false); ?></div>
  </div>
</section>
<section class="sec" style="padding-top:0">
  <div class="wrap article">
    <div class="prose"><?php include APP . '/tools/' . $slug . '-guide.php'; ?></div>
    <aside class="aside">
      <div class="side-cta"><span class="eyebrow eyebrow--glow">Want it done right?</span><h4>Get a professional plan</h4><p>Our tools give planning estimates. A walkthrough turns them into a real design.</p><a class="btn btn--glow" href="/quote/">Free consultation</a></div>
      <div class="toc"><h4>More free tools</h4><ol><?php foreach (TOOLS as $k => $o) if ($k !== $slug) echo '<li><a href="/tools/' . $k . '/">' . e($o['name']) . '</a></li>'; ?></ol></div>
    </aside>
  </div>
</section>
<?php cta_band(); ?>
