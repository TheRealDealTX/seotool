<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Sitemap', '/sitemap/']];
$page = [
    'title' => 'Sitemap | Austin Landscape Lighting',
    'description' => 'Every page on austinlandscapelighting.com: services, service areas, planning tools, blog articles and company pages from Austin Landscape Lighting.',
    'path' => '/sitemap/',
    'schema' => [schema_webpage(['title' => 'Sitemap', 'description' => 'HTML sitemap.', 'path' => '/sitemap/']), schema_breadcrumb($crumbs)],
];
$li = fn(string $label, string $path) => '<li><a href="' . e($path) . '">' . e($label) . '</a></li>';
ob_start();
echo sub_hero(['eyebrow' => 'Sitemap', 'h1' => 'Every Page on Austin Landscape Lighting', 'intro' => 'A complete index of the site. Looking for the XML version for search engines? It is at <a href="/sitemap.xml">/sitemap.xml</a>.', 'crumbs' => $crumbs, 'cta' => false]);
?>
<section class="section">
  <div class="container sitemap-cols">
    <div data-reveal>
      <h2>Company</h2>
      <ul>
        <?= $li('Home', '/') . $li('About us', '/about-us/') . $li('Reviews', '/reviews/') . $li('Project gallery', '/gallery/') . $li('FAQ', '/faq/') . $li('Contact / free estimate', '/contact/') . $li('Privacy policy', '/privacy-policy/') . $li('Terms of service', '/terms-of-service/') ?>
      </ul>
      <h2 style="margin-top:28px">Free tools</h2>
      <ul><?= $li('All tools', '/tools/'); foreach (tools() as $t) echo $li($t['name'], $t['path']); ?></ul>
    </div>
    <div data-reveal>
      <h2>Services</h2>
      <ul><?= $li('All services', '/services/'); foreach (services() as $s) echo $li($s['name'], $s['path']); ?></ul>
      <h2 style="margin-top:28px">Service areas</h2>
      <ul><?= $li('All service areas', '/service-areas/'); foreach (areas() as $a) echo $li($a['city'] . ', TX', $a['path']); ?></ul>
    </div>
    <div data-reveal>
      <h2>Blog</h2>
      <ul><?= $li('All articles', '/blog/'); foreach (posts() as $p) echo $li($p['h1'], $p['path']); ?></ul>
    </div>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
