<?php
/** @var string $toolSlug */
$t = TOOLS[$toolSlug];
$path = "/tools/$toolSlug/";
$crumbs = [['Home', '/'], ['Tools', '/tools/'], [$t['short'], $path]];
$extra = is_file(ROOT . "/content/tools/$toolSlug.php") ? require ROOT . "/content/tools/$toolSlug.php" : ['body' => '', 'faq' => []];
$schema = [schema_breadcrumbs($crumbs), ['@type' => 'WebApplication', 'name' => $t['h1'], 'url' => SITE_URL . $path,
    'applicationCategory' => 'HealthApplication', 'operatingSystem' => 'Any', 'description' => $t['description'],
    'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'publisher' => ['@id' => SITE_URL . '/#org']]];
if (!empty($extra['faq'])) {
    $schema[] = schema_faq($extra['faq']);
}
page_start(['title' => $t['title'], 'description' => $t['description'], 'schema' => $schema, 'body_class' => 'is-tool']);
?>
<section class="page-hero"><div class="wrap narrow">
  <?= breadcrumbs_html($crumbs) ?>
  <h1><?= e($t['h1']) ?></h1>
  <p class="lead"><?= e($t['intro']) ?></p>
</div></section>
<div class="wrap narrow">
  <?= tool_widget($t['id']) ?>
  <div class="prose"><?php [$b] = add_heading_ids(render_shortcodes($extra['body'])); echo $b; ?></div>
<?php if (!empty($extra['faq'])): ?><?= faq_html($extra['faq']) ?><?php endif; ?>
  <h2>More free tools</h2>
  <div class="tool-grid">
<?php foreach (TOOLS as $s => $o): if ($s !== $toolSlug): ?>
    <a class="tool-tile" href="/tools/<?= e($s) ?>/"><strong><?= e($o['short']) ?></strong><span><?= e($o['description']) ?></span></a>
<?php endif; endforeach; ?>
  </div>
</div>
<?php page_end();
