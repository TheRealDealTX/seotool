<?php
defined('TR_ROOT') || exit;
$crumbs = [['Sitemap', '/sitemap/']];
layout_start([
    'title' => 'Sitemap', 'description' => 'Every page on the Temple Roofers website: services, service areas, roofing tools, weather, blog articles and company pages.',
    'path' => '/sitemap/', 'crumbs' => $crumbs,
]);
page_hero(['h1' => 'Website Sitemap', 'lead' => 'A complete list of pages on templeroofs.com.', 'crumbs' => $crumbs, 'actions' => false, 'compact' => true]);
?>
<section class="section">
  <div class="container sitemap-grid">
    <div><h2>Main pages</h2><ul class="sitemap-list">
      <li><a href="/">Home</a></li><li><a href="/about/">About Temple Roofers</a></li><li><a href="/free-roof-inspection/">Free Roof Inspection</a></li>
      <li><a href="/services/">Roofing Services</a></li><li><a href="/service-areas/">Service Areas</a></li><li><a href="/tools/">Roofing Tools</a></li>
      <li><a href="/weather/">Temple Weather</a></li><li><a href="/blog/">Roofing Blog</a></li><li><a href="/contact/">Contact</a></li>
      <li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-use/">Terms of Use</a></li>
    </ul></div>
    <div><h2>Roofing services</h2><ul class="sitemap-list">
      <?php foreach (services() as $s): ?><li><a href="<?= e($s['url']) ?>"><?= e($s['name']) ?></a></li><?php endforeach; ?>
    </ul></div>
    <div><h2>Service areas</h2><ul class="sitemap-list">
      <?php foreach (areas() as $a): ?><li><a href="<?= e($a['url']) ?>"><?= e($a['city']) ?>, TX</a></li><?php endforeach; ?>
    </ul>
    <h2>Roofing tools</h2><ul class="sitemap-list">
      <?php foreach (catalog('tools') as $slug => $t): ?><li><a href="/tools/<?= e($slug) ?>/"><?= e($t['name']) ?></a></li><?php endforeach; ?>
    </ul></div>
    <div><h2>Blog articles</h2><ul class="sitemap-list">
      <?php foreach (posts() as $p): ?><li><a href="<?= e($p['url']) ?>"><?= e($p['title']) ?></a> <small><?= e(format_date($p['date'])) ?></small></li><?php endforeach; ?>
    </ul>
    <h2>Blog categories</h2><ul class="sitemap-list">
      <?php $used = array_unique(array_column(posts(), 'category')); foreach (catalog('blog_categories') as $slug => $name): if (!in_array($slug, $used, true)) continue; ?><li><a href="/blog/category/<?= e($slug) ?>/"><?= e($name) ?></a></li><?php endforeach; ?>
    </ul></div>
  </div>
</section>
<?php layout_end();
