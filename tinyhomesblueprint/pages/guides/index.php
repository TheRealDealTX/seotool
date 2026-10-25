<?php
page_start([
    'breadcrumbs' => [['Home', '/'], ['Guides', null]],
]);
$featured = '/blog/how-much-does-a-tiny-house-cost/';
$guides = array_filter($ROUTES, fn($r) => ($r['type'] ?? '') === 'guide');
// Newest first; keep registry order for guides sharing a date.
$order = array_flip(array_keys($guides));
uksort($guides, function ($a, $b) use ($guides, $order) {
    $d = strcmp($guides[$b]['date'] ?? '', $guides[$a]['date'] ?? '');
    return $d !== 0 ? $d : $order[$a] <=> $order[$b];
});
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Tiny house guides</p>
    <h1>Tiny House Guides</h1>
    <p class="lead">Straight answers on what a tiny house costs, how to build one, where you can legally put it and how to make a small floor plan work. Written by the Tiny Homes Blueprint team for owner-builders, families and small-home investors.</p>
    <ul class="hero-facts">
      <li><?= count($guides) ?> in-depth guides</li>
      <li>Real cost ranges, not wishful thinking</li>
      <li>Free calculators to run your own numbers</li>
    </ul>
  </div>
</section>

<?php if (isset($ROUTES[$featured])): $f = $ROUTES[$featured]; ?>
<section class="section">
  <div class="wrap two-col">
    <div>
      <p class="eyebrow">Featured guide</p>
      <h2><a href="<?= e($featured) ?>"><?= e($f['title']) ?></a></h2>
      <p class="lead"><?= e($f['description']) ?></p>
      <p>Most people start here. Before you pick a plan or a trailer, you need a realistic number for the whole project: the build itself, the land or parking spot, utilities, permits and the costs nobody puts on the brochure.</p>
      <p><a class="btn" href="<?= e($featured) ?>">Read the cost guide <?= icon('arrow') ?></a>
         <a class="btn btn-outline" href="/tools/tiny-house-cost-calculator/">Open the cost calculator</a></p>
    </div>
    <figure class="diagram">
      <svg viewBox="0 0 420 240" role="img" aria-label="Bar chart of typical tiny house cost per square foot: DIY basic 150 to 220 dollars, DIY high-end 240 to 330 dollars, builder basic 250 to 330 dollars, builder high-end 380 to 500 dollars">
        <g fill="none" stroke="#e8f2f2" stroke-width="1.5"><path d="M130 30v170h270"/></g>
        <g stroke="#e8f2f2" stroke-opacity=".25" stroke-width="1"><path d="M190 30v170M250 30v170M310 30v170M370 30v170"/></g>
        <g fill="#f2c58d">
          <rect x="160" y="44" width="42" height="18" rx="3"/>
          <rect x="214" y="84" width="54" height="18" rx="3"/>
          <rect x="220" y="124" width="48" height="18" rx="3"/>
          <rect x="298" y="164" width="72" height="18" rx="3"/>
        </g>
        <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12">
          <text x="122" y="57" text-anchor="end">DIY basic</text>
          <text x="122" y="97" text-anchor="end">DIY high-end</text>
          <text x="122" y="137" text-anchor="end">Builder basic</text>
          <text x="122" y="177" text-anchor="end">Builder high-end</text>
          <g text-anchor="middle"><text x="130" y="220">$100</text><text x="190" y="220">$200</text><text x="250" y="220">$300</text><text x="310" y="220">$400</text><text x="370" y="220">$500</text></g>
        </g>
      </svg>
      <figcaption>Typical cost per square foot by build path, before land and utilities.</figcaption>
    </figure>
  </div>
</section>
<?php endif; ?>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <h2>All tiny house guides</h2>
      <p class="lead">Cost, building, zoning, layouts, trailers and plans. Each guide links to the tools and plans that go with it.</p>
    </div>
    <div class="card-grid">
      <?php foreach ($guides as $p => $r):
          $d = $r['modified'] ?? $r['date'] ?? null; ?>
      <a class="link-card" href="<?= e($p) ?>">
        <span class="link-ico"><?= icon('book') ?></span>
        <strong><?= e($r['nav'] ?? $r['title']) ?></strong>
        <span><?= e($r['description']) ?></span>
        <?php if ($d): ?><span><time datetime="<?= e($d) ?>"><?= isset($r['modified']) ? 'Updated ' : '' ?><?= date('M j, Y', strtotime($d)) ?></time></span><?php endif; ?>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Popular planning tools</h2>
      <p class="lead">Free calculators from Tiny Homes Blueprint. No sign-up, and they run in your browser.</p>
    </div>
    <?php route_cards('tool', '', 3); ?>
    <p class="mt-2"><a href="/tools/">See all tiny house planning tools <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap two-col top">
    <div>
      <h2>Where to start</h2>
      <ol>
        <li><strong>Pick wheels or a foundation.</strong> It decides your zoning path, size limits and financing. The <a href="/blog/tiny-house-zoning-laws/">zoning guide</a> explains both.</li>
        <li><strong>Set a real budget.</strong> Use the <a href="/blog/how-much-does-a-tiny-house-cost/">cost guide</a> and <a href="/tools/tiny-house-cost-calculator/">calculator</a> before you shop.</li>
        <li><strong>Size it.</strong> The <a href="/tools/how-big-should-my-tiny-house-be/">size calculator</a> turns your household into square footage.</li>
        <li><strong>Choose a plan and build.</strong> Browse <a href="/tiny-house-plans/">tiny house plans</a>, then follow <a href="/blog/how-to-build-a-tiny-house/">how to build a tiny house</a>.</li>
      </ol>
    </div>
    <div>
      <h2>Browse by style</h2>
      <?php route_cards('style', '', 4); ?>
    </div>
  </div>
</section>

<?php cta_band('Have a question about your build?', 'Tiny Homes Blueprint answers questions about plans, modifications and custom designs. Send us your lot size and wish list.', 'Contact us', '/contact/'); ?>
<?php page_end(); ?>
