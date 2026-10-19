<?php
defined('PGF') || exit;

$t = TOOLS[$slug];
$tool = include APP . "/tools/$slug.php";
$crumbs = [['Home', '/'], ['Tools', '/tools/'], [$t['name'], "/tools/$slug/"]];
$schema = [schema_tool($slug, $t)];
if (!empty($tool['faq'])) {
    $schema[] = schema_faq($tool['faq']);
}
$page = [
    'path'     => "/tools/$slug/",
    'title'    => $tool['title'],
    'desc'     => $tool['desc'],
    'crumbs'   => $crumbs,
    'schema'   => $schema,
    'tools_js' => true,
    'body_class' => 'page-tool',
];
ob_start();
?>
<section class="page-hero page-hero--tool">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span></div>
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow reveal"><span class="eyebrow__icon"><?= icon($t['icon']) ?></span> Free tool</p>
    <h1 class="reveal"><?= e($t['name']) ?></h1>
    <p class="page-hero__lead reveal"><?= $tool['intro'] ?></p>
  </div>
</section>
<section class="section section--tight">
  <div class="container tool-wrap">
    <div class="tool reveal" data-tool="<?= e($slug) ?>">
      <?= $tool['widget'] ?>
    </div>
  </div>
</section>
<section class="section section--sand">
  <div class="container post-layout post-layout--tool">
    <div class="prose">
      <?= $tool['how'] ?>
<?php if (!empty($tool['faq'])): ?>
      <?= faq_html($tool['faq'], 'FAQs') ?>
<?php endif; ?>
      <p class="muted small">This tool provides general estimates for planning and education. It is not a substitute for advice from your veterinarian or a livestock nutritionist.</p>
    </div>
    <aside class="post-side">
      <div class="side-card">
        <p class="side-card__kicker">Read the guide</p>
        <ul class="side-links">
<?php foreach ($tool['posts'] as $ps): ?>
          <li><a href="/<?= $ps ?>/"><?= icon('book') ?> <?= e(POSTS[$ps]['title']) ?></a></li>
<?php endforeach; ?>
        </ul>
      </div>
      <div class="side-card">
        <p class="side-card__kicker">More tools</p>
        <ul class="side-links">
<?php foreach (TOOLS as $s => $tt): if ($s === $slug) continue; ?>
          <li><a href="/tools/<?= $s ?>/"><?= icon($tt['icon']) ?> <?= e($tt['name']) ?></a></li>
<?php endforeach; ?>
        </ul>
      </div>
    </aside>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
