<?php defined('APP') || exit;

cache_public();
$tools = tools_list();
$slug = $params[0] ?? null;
if ($slug !== null && !isset($tools[$slug])) not_found();

if ($slug === null) {
    $crumbs = [['The Sublet', '/'], ['Tools', '/tools/']];
    ob_start(); ?>
<div class="wrap">
  <?= breadcrumbs_html($crumbs) ?>
  <header class="page-head"><h1>Free sublet tools</h1><p class="lead">Budget a short-term stay, compare your options and plan the move. Everything runs in your browser — nothing you type is sent to The Sublet.</p></header>
  <div class="grid three"><?php foreach ($tools as $k => $t): ?>
    <a class="tool-card" href="/tools/<?= e($k) ?>/"><span class="who-ico"><?= $t['icon'] ?></span><h2 class="h3"><?= e($t['title']) ?></h2><p><?= e($t['short']) ?></p></a>
  <?php endforeach; ?></div>
</div>
<?php
    page(['title' => 'Free Sublet Calculators & Planning Tools | The Sublet', 'description' => 'Free tools from The Sublet: sublet cost calculator, proration calculator, sublet vs. lease vs. hotel comparison, packing checklist, room planner and city quiz.',
        'canonical' => '/tools/', 'body' => ob_get_clean(), 'schema' => [schema_breadcrumbs($crumbs)]]);
    exit;
}

$t = $tools[$slug];
$crumbs = [['The Sublet', '/'], ['Tools', '/tools/'], [$t['title'], "/tools/$slug/"]];
$info = require APPDIR . '/content/tools.php';
$i = $info[$slug];
ob_start(); ?>
<div class="wrap">
  <?= breadcrumbs_html($crumbs) ?>
  <header class="page-head"><h1><?= e($t['title']) ?></h1><p class="lead"><?= e($i['lead']) ?></p></header>
  <div class="tool" data-tool="<?= e($slug) ?>"><?= $i['widget'] ?></div>
  <section class="narrow section-sm prose"><?= $i['body'] ?></section>
  <div class="narrow"><?= faq_html($i['faqs']) ?></div>
  <?php if (!empty($i['amazon'])) echo '<div class="narrow">' . amazon_block($i['amazon'], 'Handy for your move') . '</div>'; ?>
  <section class="section-sm"><h2 class="h3">More tools</h2><p class="chips"><?php foreach ($tools as $k => $x): if ($k === $slug) continue; ?><a href="/tools/<?= e($k) ?>/"><?= $x['icon'] ?> <?= e($x['title']) ?></a><?php endforeach; ?></p></section>
</div>
<?php
page([
    'title' => $t['title'] . ' | The Sublet',
    'description' => $i['meta'],
    'canonical' => "/tools/$slug/",
    'body' => ob_get_clean(),
    'scripts' => ['/assets/js/tools.js?v=' . ASSET_V],
    'schema' => array_values(array_filter([schema_breadcrumbs($crumbs), schema_faq($i['faqs']), [
        '@context' => 'https://schema.org', '@type' => 'WebApplication', 'name' => $t['title'], 'applicationCategory' => 'UtilitiesApplication',
        'operatingSystem' => 'Any', 'url' => base_url("/tools/$slug/"), 'offers' => ['@type' => 'Offer', 'price' => 0, 'priceCurrency' => 'USD'],
    ]])),
]);
