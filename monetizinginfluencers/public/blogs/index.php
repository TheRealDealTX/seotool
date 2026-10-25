<?php
require __DIR__ . '/../inc/layout.php';

$posts = site_posts();
$featured = $posts[0];
$cats = ['All', 'Outreach', 'Pricing', 'Brand Deals', 'Income Streams', 'Pinterest', 'Strategy'];
$catIcons = ['Outreach' => 'mail', 'Pricing' => 'dollar', 'Brand Deals' => 'handshake', 'Income Streams' => 'trending', 'Pinterest' => 'pinterest', 'Strategy' => 'rocket'];

$items = [];
foreach ($posts as $i => [$url, $title]) {
    $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'url' => SITE_URL . $url, 'name' => $title];
}

page_start([
    'title' => 'Influencer Marketing Blog | Monetizing Influencers',
    'description' => 'The Monetizing Influencers blog: influencer marketing guides on brand deals, rates, outreach templates, affiliate income and Pinterest for creators.',
    'path' => '/blogs/',
    'extra_css' => ['/assets/css/blog.css'],
    'schema' => [
        [
            '@type' => 'Blog',
            '@id' => SITE_URL . '/blogs/#blog',
            'name' => SITE_NAME . ' Blog',
            'url' => SITE_URL . '/blogs/',
            'publisher' => ['@id' => SITE_URL . '/#org'],
            'inLanguage' => 'en-US',
        ],
        ['@type' => 'ItemList', 'name' => 'Influencer marketing guides', 'itemListElement' => $items],
    ],
]);

page_hero(
    'Influencer marketing news & guides',
    'The <span class="grad-text">Monetizing Influencers</span> Blog',
    'Practical influencer marketing guides for creators who want to get paid: how to price sponsored posts, write to brands and influencers, build a media kit and stack income streams that last.',
    [['Blog', '/blogs/']]
);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap">
    <article class="card featured-post gradient-border reveal">
      <a href="<?= e($featured[0]) ?>">
        <div class="featured-art" aria-hidden="true"><i></i><i></i><i></i><?= icon($catIcons[$featured[2]] ?? 'sparkles') ?></div>
        <div class="featured-body">
          <div><span class="chip">Featured · <?= e($featured[2]) ?></span></div>
          <h2><?= e($featured[1]) ?></h2>
          <p><?= e($featured[4]) ?></p>
          <span class="more">Read the guide <?= icon('arrow') ?></span>
        </div>
      </a>
    </article>

    <div class="blog-tools">
      <div class="filter-chips" role="group" aria-label="Filter guides by topic">
<?php foreach ($cats as $c):
        $n = $c === 'All' ? count($posts) : count(array_filter($posts, fn($p) => $p[2] === $c)); ?>
        <button type="button" data-cat="<?= e($c) ?>" aria-pressed="<?= $c === 'All' ? 'true' : 'false' ?>"><?= e($c) ?><span class="count"><?= $n ?></span></button>
<?php endforeach; ?>
      </div>
      <div class="blog-search">
        <?= icon('search') ?>
        <label class="sr-only" for="blog-q">Search guides</label>
        <input id="blog-q" type="search" placeholder="Search guides…" autocomplete="off">
      </div>
    </div>

    <div class="card-grid cols-3 post-grid" id="post-grid">
<?php foreach ($posts as [$url, $title, $cat, $date, $excerpt]): ?>
      <article class="card post-card tilt reveal" data-cat="<?= e($cat) ?>" data-title="<?= e(strtolower($title . ' ' . $excerpt)) ?>">
        <a href="<?= e($url) ?>">
          <div class="meta"><span class="chip"><?= e($cat) ?></span><time datetime="<?= e($date) ?>"><?= e(date('M j, Y', strtotime($date))) ?></time></div>
          <h3><?= e($title) ?></h3>
          <p><?= e($excerpt) ?></p>
          <span class="more">Read the guide <?= icon('arrow') ?></span>
        </a>
      </article>
<?php endforeach; ?>
    </div>
    <p class="no-results" id="no-results" hidden>No guides match that search yet. Try another topic, or <a href="/write-for-us/">pitch us the article</a>.</p>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap split">
    <div>
      <span class="kicker reveal">Got something to teach?</span>
      <h2 class="reveal">Write for the Monetizing Influencers blog</h2>
      <p class="reveal">We publish original, practical articles on influencer marketing, the creator economy and affiliate marketing from people who do the work. Pitch us a topic and share what you know with creators worldwide.</p>
      <a class="btn btn-glow reveal" href="/write-for-us/">See the guidelines <?= icon('pen') ?></a>
    </div>
    <div class="glass-panel reveal">
      <h3>Free tools to use with these guides</h3>
      <ul class="check-list">
        <li><a href="/tools/influencer-earnings-calculator/">Influencer earnings calculator</a></li>
        <li><a href="/tools/influencer-email-generator/">Influencer email generator</a></li>
        <li><a href="/tools/media-kit-builder/">Media kit builder</a></li>
        <li><a href="/tools/engagement-rate-calculator/">Engagement rate calculator</a></li>
      </ul>
    </div>
  </div>
</section>

<?php cta_band(); ?>

<script>
document.addEventListener('DOMContentLoaded', function () {
  var chips = document.querySelectorAll('.filter-chips button'), q = document.getElementById('blog-q');
  var cards = document.querySelectorAll('#post-grid .post-card'), none = document.getElementById('no-results');
  var cat = 'All';
  function apply() {
    var term = q.value.trim().toLowerCase(), shown = 0;
    cards.forEach(function (c) {
      var ok = (cat === 'All' || c.dataset.cat === cat) && (!term || c.dataset.title.indexOf(term) !== -1);
      c._show = ok;
      if (ok) {
        shown++;
        if (c.hidden || c.classList.contains('is-hiding')) {
          c.hidden = false; c.classList.add('is-hiding');
          requestAnimationFrame(function () { requestAnimationFrame(function () { if (c._show) c.classList.remove('is-hiding'); }); });
        }
      } else if (!c.hidden) {
        c.classList.add('is-hiding');
        setTimeout(function () { if (!c._show) c.hidden = true; }, 330);
      }
    });
    none.hidden = shown > 0;
  }
  chips.forEach(function (b) {
    b.addEventListener('click', function () {
      chips.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      cat = b.dataset.cat;
      apply();
    });
  });
  q.addEventListener('input', apply);
});
</script>
<?php page_end();
