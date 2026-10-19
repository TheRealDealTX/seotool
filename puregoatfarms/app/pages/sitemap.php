<?php
defined('PGF') || exit;

$crumbs = [['Home', '/'], ['Sitemap', '/sitemap/']];
$page = [
    'path'   => '/sitemap/',
    'title'  => 'Sitemap — Pure Goat Farms',
    'desc'   => 'Every page on Pure Goat Farms: goat farming guides, categories, free goat calculators and site information.',
    'crumbs' => $crumbs,
];
ob_start();
?>
<section class="page-hero page-hero--slim">
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>Sitemap</h1>
    <p class="page-hero__lead">Everything on Pure Goat Farms in one place. Search engines can use the <a href="/sitemap_index.xml">XML sitemap</a>.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="container sitemap-grid">
    <div><h2>Pages</h2><ul>
      <li><a href="/">Home</a></li><li><a href="/about/">About</a></li><li><a href="/start-here/">Start Here</a></li><li><a href="/blog/">Blog</a></li><li><a href="/faq/">Goat FAQ</a></li><li><a href="/contact/">Contact</a></li>
    </ul></div>
    <div><h2>Guides</h2><ul>
<?php foreach (posts_sorted() as $s => $p): ?>
      <li><a href="/<?= $s ?>/"><?= e($p['title']) ?></a></li>
<?php endforeach; ?>
    </ul></div>
    <div><h2>Categories</h2><ul>
<?php foreach (CATEGORIES as $s => $c): ?>
      <li><a href="/category/<?= $s ?>/"><?= e($c['name']) ?></a></li>
<?php endforeach; ?>
    </ul></div>
    <div><h2>Tools</h2><ul>
      <li><a href="/tools/">All tools</a></li>
<?php foreach (TOOLS as $s => $t): ?>
      <li><a href="/tools/<?= $s ?>/"><?= e($t['name']) ?></a></li>
<?php endforeach; ?>
    </ul></div>
    <div><h2>Legal</h2><ul>
      <li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-use/">Terms of Use</a></li><li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
    </ul></div>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
