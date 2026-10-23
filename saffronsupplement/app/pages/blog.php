<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Research roundups, comparisons and practical advice on using saffron well, from the Saffron Supplement editorial team.', 'Blog');
?>
<div class="wrap section">
  <div class="grid g3">
  <?php foreach (blog_posts() as $bp => $br): ?>
    <a class="card" href="<?= e($bp) ?>">
      <p class="small" style="margin:0 0 6px"><time datetime="<?= e($br['date']) ?>"><?= human_date($br['date']) ?></time></p>
      <h3><?= e($br['h1']) ?></h3>
      <p><?= e($br['desc']) ?></p>
      <span class="card-more">Read article &rarr;</span>
    </a>
  <?php endforeach; ?>
  </div>
  <div class="narrow" style="margin-top:40px">
    <h2>Looking for the essentials?</h2>
    <p>Start with our <a href="/saffron-dosage/">dosage guide</a>, the <a href="/saffron-side-effects/">safety guide</a> and our ranking of the <a href="/best-saffron-supplements/">best saffron supplements</a>, or see every guide on the <a href="/guides/">guides page</a>.</p>
  </div>
</div>
