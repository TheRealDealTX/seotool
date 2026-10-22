<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
$crumbs = [['Home', '/'], ['Sitemap', '/sitemap/']];
page_start(['title' => 'Sitemap | ' . SITE_NAME, 'description' => 'Every page on ' . SITE_NAME . ' in one place: under desk elliptical reviews, buying guides, comparisons, health questions and free interactive tools.', 'schema' => [schema_breadcrumbs($crumbs)]]);
?>
<section class="page-hero"><div class="wrap"><?= breadcrumbs_html($crumbs) ?><h1>Sitemap</h1></div></section>
<div class="wrap sitemap-cols">
<?php foreach (CATEGORIES as $cs => [$cn]): $in = array_filter(all_posts(), fn($p) => $p['category'] === $cs); if (!$in) continue; ?>
  <section><h2><a href="/topic/<?= e($cs) ?>/"><?= e($cn) ?></a></h2><ul>
<?php foreach ($in as $p): ?>    <li><a href="<?= e($p['url']) ?>"><?= e($p['h1']) ?></a></li>
<?php endforeach; ?>
  </ul></section>
<?php endforeach; ?>
  <section><h2><a href="/tools/">Free Tools</a></h2><ul>
<?php foreach (TOOLS as $s => $t): ?>    <li><a href="/tools/<?= e($s) ?>/"><?= e($t['h1']) ?></a></li>
<?php endforeach; ?>
  </ul></section>
  <section><h2>Site</h2><ul>
    <li><a href="/">Home</a></li><li><a href="/blog/">Blog</a></li><li><a href="/about-us/">About Us</a></li><li><a href="/contact/">Contact</a></li>
    <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-use/">Terms of Use</a></li>
  </ul></section>
</div>
<?php page_end();
