<?php
// Blog hub: keyword-targeted posts (type 'post') newest first with category filters,
// then the long-form pillar guides (type 'guide').
page_start(['breadcrumbs' => [['Home', '/'], ['Blog', null]]]);
$byDate = function (array $items) {
    uasort($items, fn($a, $b) => strcmp($b['date'] ?? '', $a['date'] ?? ''));
    return $items;
};
$posts  = $byDate(array_filter($ROUTES, fn($r) => ($r['type'] ?? '') === 'post'));
$guides = $byDate(array_filter($ROUTES, fn($r) => ($r['type'] ?? '') === 'guide'));
$cats = array_values(array_unique(array_column($posts, 'cat')));
sort($cats);
$latestPath = array_key_first($posts);
$latest = $posts[$latestPath];
$fmt = fn($d) => date('M j, Y', strtotime($d));
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Tiny Homes Blueprint blog</p>
    <h1>Tiny House Blog</h1>
    <p class="lead">Straight answers to the questions people ask before they go tiny: what a tiny house is, where you can put one, how to buy or finance it, what it weighs and how long it takes to build. Plus long-form guides on cost, building, zoning and layouts.</p>
    <ul class="hero-facts">
      <li><?= count($posts) ?> articles</li>
      <li><?= count($guides) ?> in-depth guides</li>
      <li>Free calculators to run your own numbers</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div>
      <p class="eyebrow">Latest article &middot; <?= e($latest['cat']) ?></p>
      <h2><a href="<?= e($latestPath) ?>"><?= e($latest['title']) ?></a></h2>
      <p class="lead"><?= e($latest['description']) ?></p>
      <p class="muted"><time datetime="<?= e($latest['date']) ?>"><?= $fmt($latest['date']) ?></time></p>
      <p><a class="btn" href="<?= e($latestPath) ?>">Read the article <?= icon('arrow') ?></a></p>
    </div>
    <div class="panel">
      <h3>Start with the essentials</h3>
      <ul class="check-list">
        <li><a href="/blog/what-is-a-tiny-house/">What is a tiny house?</a></li>
        <li><a href="/blog/how-much-does-a-tiny-house-cost/">How much does a tiny house cost?</a></li>
        <li><a href="/blog/where-to-put-a-tiny-house/">Where to put a tiny house</a></li>
        <li><a href="/blog/how-to-buy-a-tiny-house/">How to buy a tiny house</a></li>
        <li><a href="/blog/how-to-build-a-tiny-house/">How to build a tiny house</a></li>
      </ul>
    </div>
  </div>
</section>

<section class="section section-alt" id="articles">
  <div class="wrap">
    <div class="section-head">
      <h2>All articles</h2>
      <p class="lead">Filter by topic. Every article links to the plans, guides and calculators that go with it.</p>
    </div>
    <div class="chip-row" role="group" aria-label="Filter articles by topic">
      <button type="button" class="chip" aria-pressed="true" data-cat="">All <span><?= count($posts) ?></span></button>
      <?php foreach ($cats as $c): $n = count(array_filter($posts, fn($r) => $r['cat'] === $c)); ?>
      <button type="button" class="chip" aria-pressed="false" data-cat="<?= e($c) ?>"><?= e($c) ?> <span><?= $n ?></span></button>
      <?php endforeach; ?>
    </div>
    <div class="post-grid" id="post-grid">
      <?php foreach ($posts as $path => $r): ?>
      <a class="post-card" href="<?= e($path) ?>" data-cat="<?= e($r['cat']) ?>">
        <span class="post-meta"><span class="tag"><?= e($r['cat']) ?></span> <time datetime="<?= e($r['date']) ?>"><?= $fmt($r['date']) ?></time></span>
        <strong><?= e($r['title']) ?></strong>
        <span><?= e($r['description']) ?></span>
        <span class="post-more">Read article <?= icon('arrow') ?></span>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section" id="guides">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">In-depth guides</p>
      <h2>Tiny house guides</h2>
      <p class="lead">Our longest, most detailed pages: full cost breakdowns, a 12-step build guide, zoning and trailer rules, layouts and plan buying advice.</p>
    </div>
    <div class="card-grid">
      <?php foreach ($guides as $path => $r): $d = $r['modified'] ?? $r['date']; ?>
      <a class="link-card" href="<?= e($path) ?>">
        <span class="link-ico"><?= icon('book') ?></span>
        <strong><?= e($r['nav'] ?? $r['title']) ?></strong>
        <span><?= e($r['description']) ?></span>
        <span><time datetime="<?= e($d) ?>"><?= isset($r['modified']) ? 'Updated ' : '' ?><?= $fmt($d) ?></time></span>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <h2>Free planning tools</h2>
      <p class="lead">Run your own numbers with Tiny Homes Blueprint calculators. No sign-up, and they run in your browser.</p>
    </div>
    <?php route_cards('tool', '', 3); ?>
    <p class="mt-2"><a href="/tools/">See all tiny house planning tools <?= icon('arrow') ?></a></p>
  </div>
</section>

<?php cta_band('Ready to plan your tiny home?', 'Browse ' . count($PLANS) . ' build-ready tiny house plans, or ask Tiny Homes Blueprint about a custom design.'); ?>
<script>
(function () {
  var chips = document.querySelectorAll('.chip-row .chip'), cards = document.querySelectorAll('#post-grid .post-card');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var cat = chip.dataset.cat;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
      cards.forEach(function (card) { card.hidden = cat !== '' && card.dataset.cat !== cat; });
    });
  });
})();
</script>
<?php page_end(); ?>
