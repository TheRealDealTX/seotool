<?php
defined('HA_ROOT') || exit;
$others = array_filter(TOOLS, fn ($k) => $k !== $slug, ARRAY_FILTER_USE_KEY);
?>
<section class="page-hero">
  <div class="page-hero-bg" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Houston Apartments</a><span>/</span><a href="<?= TOOLS_BASE ?>">Renter Tools</a><span>/</span><span aria-current="page"><?= e($tool['name']) ?></span></nav>
    <h1 class="fade-up"><?= e($tool['h1']) ?></h1>
    <p class="hero-sub fade-up d1"><?= e($tool['short']) ?></p>
  </div>
</section>
<section class="section tool-section">
  <div class="wrap">
    <div class="tool-app" data-tool="<?= e($slug) ?>"><?php require HA_APP . "/views/tools/$slug.php"; ?></div>
  </div>
</section>
<section class="section tool-info">
  <div class="wrap prose-grid">
    <article class="prose">
      <?= $tool['body'] ?>
      <h2>Frequently asked questions</h2>
      <div class="faq">
        <?php foreach ($tool['faqs'] as [$q, $a]): ?><details><summary><?= e($q) ?></summary><p><?= e($a) ?></p></details><?php endforeach ?>
      </div>
    </article>
    <aside class="side-card sticky">
      <h3>Want a second opinion?</h3>
      <p>Joseph and the Houston Apartments team can turn these numbers into a short list of apartments that fit – free.</p>
      <button class="btn btn-grad btn-block" type="button" data-lead data-lead-name="From the <?= e($tool['name']) ?>">Get my short list</button>
      <h4>More renter tools</h4>
      <ul class="side-tools">
        <?php foreach ($others as $k => $t): ?><li><a href="<?= TOOLS_BASE . $k ?>/"><span aria-hidden="true"><?= $t['icon'] ?></span> <?= e($t['name']) ?></a></li><?php endforeach ?>
      </ul>
    </aside>
  </div>
</section>
