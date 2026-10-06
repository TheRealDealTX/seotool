<?php defined('LLT') or die(http_response_code(404));
global $PAGES;
$P['lead'] = 'Every page on the Landscape Lighting Texas website.';
$P['hero_no_cta'] = true;
$groups = ['Company' => ['home', 'page', 'legal'], 'Services' => ['service'], 'Service Areas' => ['area'], 'Tools & Calculators' => ['tool'], 'Articles' => ['post']];
$order = ['/', '/about-us/', '/services/', '/areas/', '/tools/', '/gallery/', '/faq/', '/blog/', '/category/general/', '/quote/', '/privacy-policy/', '/terms-of-service/', '/sitemap/'];
?>
<section class="section">
  <div class="container sitemap-cols">
    <?php foreach ($groups as $label => $types):
        $items = array_filter($PAGES, fn($p) => in_array($p['type'], $types, true));
        if ($label === 'Company') { uksort($items, fn($a, $b) => array_search($a, $order) <=> array_search($b, $order)); }
        if ($label === 'Tools & Calculators') $items = ['/landscape-lighting-cost-calculator/' => $PAGES['/landscape-lighting-cost-calculator/']] + $items;
        if ($label === 'Articles') $items = posts(); ?>
    <section class="reveal"><h2><?= e($label) ?></h2><ul>
      <?php foreach ($items as $path => $p): ?><li><a href="<?= e($path) ?>"><?= e($path === '/' ? 'Home' : short_name($p)) ?></a></li><?php endforeach; ?>
    </ul></section>
    <?php endforeach; ?>
  </div>
</section>
