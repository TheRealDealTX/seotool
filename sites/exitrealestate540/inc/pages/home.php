<?php
defined('ERE') or exit;
$posts = array_values(all_posts());
$c = cfg();
page_head([
    'title' => 'Exit Real Estate 540: Texas Real Estate Guides & Tools',
    'description' => 'Houston and Texas real estate made simple: buying, selling, investing, property taxes and claims, with free mortgage and affordability tools.',
    'path' => '/',
    'body_class' => 'home',
    'schema' => [[
        '@type' => 'CollectionPage', '@id' => abs_url('/#webpage'), 'url' => abs_url('/'),
        'name' => $c['name'], 'isPartOf' => ['@id' => abs_url('/#website')], 'about' => 'Texas residential real estate',
    ]],
]);
?>
<section class="hero<?= has_photo('home') ? ' hero--photo' : '' ?>">
  <?= picture('home', '100vw', 'hero__bg', true, '') ?>
  <div class="wrap hero__inner">
    <div class="hero__copy">
      <p class="eyebrow">Houston &amp; Texas real estate, explained</p>
      <h1>Buy, sell, invest and protect your home with real numbers</h1>
      <p class="lead">Straight-talk guides and free calculators for Texas buyers, sellers, investors and homeowners - including what to do when a fire, flood or hurricane turns your house into an insurance claim.</p>
      <div class="hero__cta">
        <a class="btn btn--primary" href="/tools/">Try the free calculators <?= icon('arrow') ?></a>
        <a class="btn btn--ghost" href="/blog/">Read the guides</a>
      </div>
    </div>
    <div class="hero__panel" aria-label="Popular tools">
      <p class="hero__panel-title">Most-used tools</p>
<?php foreach (['mortgage-calculator', 'home-affordability-calculator', 'texas-property-tax-calculator', 'insurance-claim-depreciation-calculator'] as $t) echo tool_card($t); ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head"><h2>Explore by topic</h2><p>Pick the move you are making.</p></div>
    <div class="topics">
<?php foreach ($c['categories'] as $slug => $cat): $n = count(posts_in($slug)); ?>
      <a class="topic cat-<?= $slug ?>" href="/category/<?= $slug ?>/">
        <span class="topic__icon"><?= icon($cat['icon']) ?></span>
        <strong><?= e($cat['name']) ?></strong>
        <span><?= $n ?> guide<?= $n === 1 ? '' : 's' ?></span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>

<?php if ($posts): ?>
<section class="section section--tint">
  <div class="wrap">
    <div class="section__head"><h2>Latest guides</h2><a class="more" href="/blog/">All articles <?= icon('arrow') ?></a></div>
    <div class="grid grid--feature">
      <?= post_card($posts[0], true) ?>
<?php foreach (array_slice($posts, 1, 6) as $p) echo post_card($p); ?>
    </div>
  </div>
</section>
<?php endif; ?>

<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Property damage &amp; claims</p>
      <h2>House fire, flood or hurricane damage? Start here.</h2>
      <p>Disasters turn homeowners into insurance experts overnight. Our claim guides walk through the first 24 hours, how Texas claim deadlines work, how depreciation is calculated, and when it makes sense to bring in a licensed public adjuster - or sell the property as-is.</p>
      <ul class="ticks">
        <li><?= icon('check') ?><a href="/blog/what-to-do-after-a-house-fire/">What to do after a house fire</a></li>
        <li><?= icon('check') ?><a href="/blog/hurricane-damage-insurance-claim-texas/">Filing a hurricane claim in Texas</a></li>
        <li><?= icon('check') ?><a href="/blog/water-damage-claim-denied/">Water damage claim denied?</a></li>
        <li><?= icon('check') ?><a href="/blog/sell-fire-damaged-house-texas/">Selling a fire-damaged house</a></li>
      </ul>
    </div>
    <div class="split__aside">
      <?= tool_card('insurance-claim-depreciation-calculator', 'tool-card tool-card--big') ?>
      <?= tool_card('hurricane-prep-checklist', 'tool-card tool-card--big') ?>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section__head"><h2><?= count(tools()) ?> free real estate calculators &amp; tools</h2><a class="more" href="/tools/">See all tools <?= icon('arrow') ?></a></div>
    <div class="tool-grid">
<?php foreach (tools() as $slug => $t) echo tool_card($slug); ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head"><h2>Gear every Texas homeowner should own</h2><a class="more" href="/recommended-products/">See all picks <?= icon('arrow') ?></a></div>
    <div class="products">
<?php foreach (['govee-water-sensor', 'midland-weather-radio', 'first-alert-smoke-co', 'sentrysafe-fireproof'] as $k) echo product_card($k); ?>
    </div>
    <p class="fine">As an Amazon Associate we earn from qualifying purchases, at no extra cost to you.</p>
  </div>
</section>
<?php page_foot(['scripts' => []]);
