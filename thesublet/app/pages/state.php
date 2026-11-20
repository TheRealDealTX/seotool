<?php defined('APP') || exit;

$st = strtolower($params[0]);
if (!isset(states()[strtoupper($st)])) not_found('We don’t recognise that state.');
cache_public();
$name = state_name($st);
$cities = known_cities($st);
$dir = directory_section(['state' => $st], state_url($st), null, [],
    '<h3>No sublets listed in ' . e($name) . ' yet</h3><p>Hosts in ' . e($name) . ' can be the first — free listings are reviewed within a day or two, and verified listings go live instantly.</p><p><a class="btn" href="/post-a-sublet/">List your place in ' . e($name) . '</a></p>');
$crumbs = [['The Sublet', '/'], ['Sublets', '/sublets/'], [$name, state_url($st)]];
$hasContent = $cities || $dir['total'] > 0;

ob_start(); ?>
<div class="wrap">
  <?= breadcrumbs_html($crumbs) ?>
  <header class="page-head">
    <h1>Sublets in <?= e($name) ?></h1>
    <p class="lead">Furnished rooms, apartments and houses for short stays of one to twelve months across <?= e($name) ?>, posted by hosts on The Sublet.</p>
  </header>
  <?php if ($cities): ?>
  <section class="section-sm">
    <h2 class="h3">Cities in <?= e($name) ?></h2>
    <p class="chips"><?php foreach ($cities as $k => $c): [$s, $slug] = explode('/', $k); ?><a href="<?= e(city_url($s, $slug)) ?>"><?= e($c['name']) ?><?= $c['n'] ? ' <span class="muted">(' . (int)$c['n'] . ')</span>' : '' ?></a><?php endforeach; ?></p>
  </section>
  <?php endif; ?>
  <?= $dir['html'] ?>
  <section class="section narrow">
    <h2>Subletting in <?= e($name) ?>: the basics</h2>
    <p>Whether you can sublet, and on what terms, depends first on your lease and then on state and local law. Many leases require the landlord’s written consent before you sublet, and some cities regulate stays shorter than 30 days separately from monthly rentals. Read <a href="/blog/how-to-sublet-your-apartment-legally/">how to sublet legally</a> and <a href="/blog/short-term-rental-laws-what-hosts-should-know/">what hosts should know about short-term rental rules</a>, and check with your city or county before you list.</p>
    <p>Renters: tour before paying, ask for a written <a href="/blog/sublease-agreement-what-to-include/">sublease agreement</a>, and review our <a href="/safety/">scam-awareness tips</a>.</p>
  </section>
</div>
<?php
$body = ob_get_clean();
page([
    'title' => 'Sublets in ' . $name . ' — Furnished Short-Term Rentals | The Sublet',
    'description' => 'Find furnished sublets and 1–12 month rentals in ' . $name . ' on The Sublet: rooms, apartments and houses for interns, travel nurses, students and relocations.',
    'canonical' => state_url($st),
    'robots' => (!$hasContent || $dir['filtered']) ? 'noindex, follow' : 'index, follow',
    'body' => $body,
    'h_extra' => leaflet_head(),
    'schema' => array_values(array_filter([schema_breadcrumbs($crumbs), schema_itemlist($dir['cards'], 'Sublets in ' . $name)])),
]);
