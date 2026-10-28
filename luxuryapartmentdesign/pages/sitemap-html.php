<?php
$path = '/sitemap/';
$crumbs = [['Home', '/'], ['Sitemap', $path]];
page_head(['title' => 'Sitemap | ' . SITE_NAME, 'description' => 'Every page on Luxury Apartment Design: apartment design guides by topic, free interior design tools and site information.', 'path' => $path, 'schema' => [schema_breadcrumbs($crumbs)]]);
?>
<section class="page-hero"><div class="container"><?= breadcrumbs_html($crumbs) ?><h1>Sitemap</h1></div></section>
<section class="section"><div class="container sitemap-cols">
  <?php foreach (CATEGORIES as $s => $c): ?>
  <div><h2><a href="/category/<?= $s ?>/"><?= e($c['name']) ?></a></h2><ul>
    <?php foreach (articles_in($s) as $a): ?><li><a href="/<?= $a['slug'] ?>/"><?= e($a['h1']) ?></a></li><?php endforeach; ?>
  </ul></div>
  <?php endforeach; ?>
  <div><h2><a href="/tools/">Design Tools</a></h2><ul>
    <?php foreach (TOOLS as $s => $t): ?><li><a href="/tools/<?= $s ?>/"><?= e($t['name']) ?></a></li><?php endforeach; ?>
  </ul></div>
  <div><h2>Site</h2><ul>
    <li><a href="/">Home</a></li><li><a href="/blogs/">All Articles</a></li><li><a href="/about-us/">About Us</a></li><li><a href="/editorial-policy/">Editorial Policy</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-use/">Terms of Use</a></li>
  </ul></div>
</div></section>
<?php page_foot(); ?>
