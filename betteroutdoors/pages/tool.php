<?php defined('BO') || exit;
// Interactive tool template. Widget + explainer live in content/tools/{slug}.php.

$t = $TOOLS[$slug];
$GLOBALS['FAQS'] = [];
ob_start();
require __DIR__ . '/../content/tools/' . $slug . '.php';
$body = ob_get_clean();

$url    = '/tools/' . $slug . '/';
$crumbs = [['Home', '/'], ['Tools', '/tools/'], [$t['h1'], $url]];
$schema = [
    ['@type' => 'WebApplication', 'name' => $t['h1'], 'url' => SITE_URL . $url, 'description' => $t['desc'], 'applicationCategory' => 'SportsApplication', 'operatingSystem' => 'Any', 'browserRequirements' => 'Requires JavaScript', 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'publisher' => ['@id' => SITE_URL . '/#organization']],
    breadcrumb_schema($crumbs),
];
if ($GLOBALS['FAQS']) {
    $qa = [];
    foreach ($GLOBALS['FAQS'] as $q => $a) $qa[] = ['@type' => 'Question', 'name' => $q, 'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($a)]];
    $schema[] = ['@type' => 'FAQPage', 'mainEntity' => $qa];
}
page_head(['title' => $t['title'] . ' | Better Outdoors', 'desc' => $t['desc'], 'path' => $url, 'schema' => $schema, 'body_class' => 'is-tool']);
?>
<section class="page-hero mist-after">
  <div class="wrap">
    <?= breadcrumbs_html($crumbs) ?>
    <span class="eyebrow"><i class="fa-solid <?= e($t['icon']) ?>" aria-hidden="true"></i> Free Better Outdoors Tool</span>
    <h1><?= e($t['h1']) ?></h1>
    <p><?= e($t['desc']) ?></p>
  </div>
</section>
<div class="section-mist" style="padding-bottom:70px">
  <div class="wrap">
<?= $body ?>
    <div class="tool-content">
      <h2 class="section-title" style="margin-top:20px">More Free Archery Tools</h2>
      <div class="tools-grid">
<?php foreach ($TOOLS as $ts => $tt): if ($ts === $slug) continue; ?>
        <a class="tool-card reveal" href="/tools/<?= e($ts) ?>/"><div class="ico"><i class="fa-solid <?= e($tt['icon']) ?>" aria-hidden="true"></i></div><h3><?= e($tt['h1']) ?></h3><p><?= e($tt['short']) ?></p><span class="go">Open tool <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span></a>
<?php endforeach; ?>
      </div>
    </div>
  </div>
</div>
<script src="/assets/js/tools.js?v=<?= ASSET_VER ?>" defer></script>
<?php page_foot(); ?>
