<?php page_start(['title' => 'Sitemap | Free Grade Calculator', 'description' => 'Every page on FreeGradeCalculator: all calculators, guides and site information in one place.', 'path' => '/sitemap']); ?>
<section class="page-hero"><div class="wrap"><?= breadcrumbs_html([['Home', '/'], ['Sitemap', '/sitemap']]) ?><h1>Sitemap</h1></div></section>
<div class="wrap sitemap-cols prose" style="max-width:var(--wrap);padding-bottom:40px">
  <div><h2>Calculators</h2><ul><li><a href="/">Grade Calculator</a></li><?php foreach (tools() as $s => $t): ?><li><a href="/<?= e($s) ?>"><?= e($t[0]) ?></a></li><?php endforeach; ?></ul></div>
  <div><h2>Guides</h2><ul><?php foreach (articles() as $a): ?><li><a href="/blog/<?= e($a['slug']) ?>"><?= e($a['title']) ?></a></li><?php endforeach; ?></ul></div>
  <div><h2>Site</h2><ul><li><a href="/tools">All calculators</a></li><li><a href="/blog">Blog</a></li><li><a href="/study-supplies">Study supplies</a></li><li><a href="/about-us">About us</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy-policy">Privacy policy</a></li><li><a href="/terms-of-use">Terms of use</a></li><li><a href="/disclaimer">Disclaimer</a></li><li><a href="/affiliate-disclosure">Affiliate disclosure</a></li></ul></div>
</div>
<?php page_end();
