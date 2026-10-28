<?php
require dirname(__DIR__) . '/includes/layout.php';
$crumbs = [['Sitemap', '/sitemap/']];
page_start([
    'title' => 'Sitemap | Austin Roofing',
    'description' => 'Every page on austinsroofing.com: Austin roofing services, service areas, free roofing calculators, blog guides and company information.',
    'path' => '/sitemap/', 'crumbs' => $crumbs,
]);
page_hero('Sitemap', ['crumbs' => $crumbs, 'cta' => false, 'lead' => 'Find any page on the Austin Roofing website.']);
$posts = POSTS;
uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
?>
<section class="section section--tight">
  <div class="container sitemap-cols">
    <section><h2>Company</h2><ul>
      <?php foreach (CORE_PAGES as $path => $p): ?><li><a href="<?= $path ?>"><?= e($p[0]) ?></a></li><?php endforeach; ?>
    </ul></section>
    <section><h2>Services</h2><ul>
      <?php foreach (SERVICES as $slug => $s): ?><li><a href="/services/<?= $slug ?>/"><?= e($s['h1']) ?></a></li><?php endforeach; ?>
    </ul></section>
    <section><h2>Service Areas</h2><ul>
      <?php foreach (AREAS as $slug => $a): ?><li><a href="/service-areas/<?= $slug ?>/"><?= e($a['h1']) ?></a></li><?php endforeach; ?>
    </ul></section>
    <section><h2>Roofing Tools</h2><ul>
      <?php foreach (TOOLS as $slug => $t): ?><li><a href="/roofing-tools/<?= $slug ?>/"><?= e($t['name']) ?></a></li><?php endforeach; ?>
    </ul></section>
    <section><h2>Blog</h2><ul>
      <?php foreach ($posts as $slug => $p): ?><li><a href="/blog/<?= $slug ?>/"><?= e($p['h1']) ?></a></li><?php endforeach; ?>
    </ul></section>
  </div>
</section>
<?php page_end();
