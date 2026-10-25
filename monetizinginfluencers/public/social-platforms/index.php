<?php
require __DIR__ . '/../inc/layout.php';
require __DIR__ . '/_platform.php';

$path  = '/social-platforms/';
$title = 'Social Media Monetization by Platform: Where to Earn';
$desc  = 'Compare social media monetization on YouTube, TikTok, Instagram, Facebook and Pinterest, and use our free picker to find the platform that pays best for you.';

$plats = [
    'youtube'   => ['YouTube', 'Ad revenue share, sponsorships, memberships and search traffic that earns for years.'],
    'tiktok'    => ['TikTok', 'Explosive reach, Creator Rewards, TikTok Shop affiliate, LIVE gifts and brand deals.'],
    'instagram' => ['Instagram', 'The home of brand partnerships: Reels, collabs, subscriptions and affiliate Stories.'],
    'facebook'  => ['Facebook', 'Community-driven income from Groups, lives, Stars and an older, high-spending audience.'],
    'pinterest' => ['Pinterest', 'A visual search engine that sends buyers to your affiliate links, products and site.'],
];

page_start([
    'title' => $title,
    'description' => $desc,
    'path' => $path,
    'extra_css' => ['/assets/css/platforms.css'],
    'schema' => [[
        '@type' => 'ItemList',
        'name' => 'Social media monetization playbooks',
        'itemListElement' => array_values(array_map(
            fn($slug, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => SITE_URL . '/social-platforms/' . $slug . '/', 'name' => PLATFORMS[$slug] . ' monetization'],
            array_keys(PLATFORMS), array_keys(array_keys(PLATFORMS))
        )),
    ]],
]);

page_hero(
    'Platform playbooks',
    'Social Media Monetization <span class="grad-text">by Platform</span>',
    'Every platform pays creators differently. YouTube shares ad revenue, TikTok rewards reach, Instagram runs on brand deals, Facebook pays for community and Pinterest sends buyers. Use the picker to find where you should focus first, then dive into the playbook for each platform.',
    [['Social Platforms', $path]]
);
?>
<section class="section" style="padding-top:10px" id="picker">
  <div class="wrap">
    <div class="tool-panel gradient-border reveal">
      <span class="kicker">Free tool · instant</span>
      <h2>Which platform pays best for you?</h2>
      <p class="small">Pick your niche, content style and audience size. The Monetizing Influencers picker scores each platform on income potential for your situation. Scores are a guide, not a guarantee.</p>
      <div class="picker picker-row">
        <div class="field"><label for="pk-niche">Your niche</label>
          <select id="pk-niche">
            <option value="fashion">Fashion &amp; beauty</option>
            <option value="fitness">Fitness &amp; wellness</option>
            <option value="finance">Finance &amp; business</option>
            <option value="tech">Tech &amp; gaming</option>
            <option value="home">Home, DIY &amp; food</option>
            <option value="travel">Travel &amp; luxury</option>
            <option value="education">Education &amp; how-to</option>
            <option value="entertainment">Comedy &amp; entertainment</option>
          </select></div>
        <div class="field"><label for="pk-style">Content you enjoy making</label>
          <select id="pk-style">
            <option value="short">Short vertical video</option>
            <option value="long">Long-form video</option>
            <option value="photo">Photos &amp; visuals</option>
            <option value="live">Live streams &amp; community</option>
            <option value="tutorial">Tutorials &amp; guides</option>
          </select></div>
        <div class="field"><label for="pk-size">Current audience</label>
          <select id="pk-size">
            <option value="start">Just starting (under 1K)</option>
            <option value="small" selected>Small (1K - 10K)</option>
            <option value="mid">Growing (10K - 100K)</option>
            <option value="big">Large (100K+)</option>
          </select></div>
      </div>
      <div class="picker-results" id="pk-results">
<?php foreach ($plats as $slug => [$name]): ?>
        <a class="pick-card p-<?= $slug ?>" data-p="<?= $slug ?>" href="/social-platforms/<?= $slug ?>/"><span class="rank">Best fit</span><span class="p-ico"><?= icon($slug) ?></span><b><?= $name ?></b><span class="score">0</span><span class="why"></span></a>
<?php endforeach; ?>
      </div>
    </div>
  </div>
</section>

<section class="section" id="playbooks">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">The playbooks</span>
      <h2 class="reveal">Five platforms, five ways to get paid</h2>
      <p class="reveal">Each guide covers the platform's monetization programs, what brands pay, and the growth tactics that make you more bookable.</p>
    </div>
    <div class="card-grid cols-3">
<?php foreach ($plats as $slug => [$name, $txt]): ?>
      <article class="card platform-card p-<?= $slug ?> tilt reveal"><a href="/social-platforms/<?= $slug ?>/"><span class="p-ico"><?= icon($slug) ?></span><h3><?= $name ?> monetization</h3><p><?= e($txt) ?></p><span class="more">Read the <?= $name ?> playbook <?= icon('arrow') ?></span></a></article>
<?php endforeach; ?>
      <article class="card platform-card tilt reveal gradient-border"><a href="/website-design/"><span class="p-ico" style="background:var(--grad)"><?= icon('globe') ?></span><h3>Your own website</h3><p>The platform you own. Capture emails, sell products and rank on Google without an algorithm in the way.</p><span class="more">Web design for influencers <?= icon('arrow') ?></span></a></article>
    </div>
  </div>
</section>

<section class="section alt-bg" id="compare">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">Side by side</span>
      <h2 class="reveal">Social media monetization compared</h2>
      <p class="reveal">Programs and thresholds change often and vary by country, so confirm details in each app. Rates are rough planning estimates for one sponsored post or video from a micro-influencer (10K-100K followers).</p>
    </div>
    <div class="table-scroll reveal"><table class="data-table">
      <thead><tr><th>Platform</th><th>Native monetization</th><th>Typical entry requirements</th><th>Best-paying formats</th><th>Est. sponsored rate (micro)</th></tr></thead>
      <tbody>
        <tr><td><a href="/social-platforms/youtube/"><strong>YouTube</strong></a></td><td>Ad revenue share, memberships, Super Thanks/Chat, Shopping</td><td>500-1,000 subscribers plus watch hours or Shorts views</td><td>Long-form integrations, dedicated reviews</td><td>$500 - $3,000<small>Priced on average views</small></td></tr>
        <tr><td><a href="/social-platforms/tiktok/"><strong>TikTok</strong></a></td><td>Creator Rewards, TikTok Shop affiliate, LIVE gifts, subscriptions</td><td>10K followers and 100K monthly views for Creator Rewards</td><td>Native-style sponsored videos, Shop demos</td><td>$150 - $1,000<small>Volatile reach</small></td></tr>
        <tr><td><a href="/social-platforms/instagram/"><strong>Instagram</strong></a></td><td>Subscriptions, gifts, badges, partnership ads</td><td>Professional account; feature-specific thresholds</td><td>Reels, carousels, Story link sets</td><td>$100 - $1,500<small>~$10 per 1K followers baseline</small></td></tr>
        <tr><td><a href="/social-platforms/facebook/"><strong>Facebook</strong></a></td><td>Content monetization, Stars, subscriptions</td><td>Professional mode or Page; eligibility checks</td><td>Lives, Reels, Group placements</td><td>$100 - $1,000<small>Higher for Groups and lives</small></td></tr>
        <tr><td><a href="/social-platforms/pinterest/"><strong>Pinterest</strong></a></td><td>Paid partnership label; earnings come off-platform</td><td>Business account; no follower minimum</td><td>Pin sets, video pins, affiliate roundups</td><td>$100 - $800<small>Long-tail traffic adds value</small></td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<section class="section" id="choose">
  <div class="wrap narrow prose">
    <span class="kicker reveal">How to choose</span>
    <h2 class="reveal" style="margin-top:.2em">How to choose the right platform to monetize</h2>
    <p>Social media monetization is not one-size-fits-all. The platform that makes a comedy creator rich can be a dead end for a financial planner. Before you spread yourself thin, weigh these four factors.</p>
    <h3>1. Where your buyers already spend time</h3>
    <p>Money follows audiences with purchasing power and intent. Pinterest users are planning purchases. YouTube viewers search for reviews and tutorials before they buy. Facebook skews toward adults with established incomes. TikTok and Instagram reach younger audiences at enormous scale. Match the platform to the people who buy the products in your niche, because that is who brands want to reach.</p>
    <h3>2. The content you can make consistently</h3>
    <p>The best platform is the one you will actually post on every week. If you love talking to a camera for twenty minutes, YouTube will reward you. If you think in quick hooks and trends, TikTok and Reels fit. If you are a natural photographer or designer, Instagram carousels and Pinterest pins play to your strengths. Consistency beats optimisation every time.</p>
    <h3>3. How the platform pays</h3>
    <p>Some platforms pay you directly (YouTube ad revenue, TikTok Creator Rewards, Facebook content monetization). Others mostly create value you capture elsewhere (Pinterest traffic, Instagram brand deals, affiliate clicks). Direct payouts are steady but usually small per view; brand deals and your own products are where most creators make serious money, on any platform.</p>
    <h3>4. How long your content keeps earning</h3>
    <p>A TikTok or Story is mostly seen within days. A YouTube tutorial or a keyword-rich pin can earn for years. Mixing fast, high-reach platforms with slow, evergreen ones gives you both growth today and income that compounds. Monetizing Influencers recommends at least one evergreen channel in every creator's mix, and a website as the place all of it points back to.</p>
  </div>
</section>

<section class="section" id="strategy">
  <div class="wrap split">
    <div>
      <span class="kicker reveal">Strategy</span>
      <h2 class="reveal">One home base, several outposts</h2>
      <p class="reveal">The creators who earn the most pick one primary platform where they make their best content, then repurpose it everywhere else. A YouTube video becomes Shorts, Reels, TikToks and pins. A TikTok series becomes a YouTube compilation. Monetizing Influencers calls this the hub-and-spoke model, and it multiplies the income from every hour you spend creating.</p>
      <ul class="check-list reveal">
        <li>Choose a primary platform that fits the content you enjoy making</li>
        <li>Repurpose to two or three secondary platforms</li>
        <li>Point every bio link to a website and email list you own</li>
        <li>Stack brand deals, affiliate and products on top of native payouts</li>
      </ul>
      <a class="btn btn-glow reveal" href="/monetization/">Read the monetization guide <?= icon('arrow') ?></a>
    </div>
    <div class="glass-panel reveal">
      <h3>Free tools for every platform</h3>
      <ul class="result-rows">
        <li><a href="/tools/influencer-earnings-calculator/">Influencer earnings calculator</a> <b><?= icon('calc') ?></b></li>
        <li><a href="/tools/engagement-rate-calculator/">Engagement rate calculator</a> <b><?= icon('heart') ?></b></li>
        <li><a href="/tools/media-kit-builder/">Media kit builder</a> <b><?= icon('file') ?></b></li>
        <li><a href="/tools/influencer-email-generator/">Influencer email generator</a> <b><?= icon('mail') ?></b></li>
        <li><a href="/tools/income-stream-simulator/">Income stream simulator</a> <b><?= icon('pie') ?></b></li>
      </ul>
    </div>
  </div>
</section>

<?php
faq_block([
    ['Which social media platform pays creators the most?', '<p>YouTube pays the most directly because it shares ad revenue at scale. For brand deals, Instagram and YouTube usually command the highest rates, while TikTok offers the fastest growth. The best platform for you depends on your niche and content style; try the picker above.</p>'],
    ['Can you make money on every social platform?', '<p>Yes, but in different ways. YouTube, TikTok, Instagram and Facebook have native programs; Pinterest mostly earns through affiliate links, sponsorships and traffic to your own products or site.</p>'],
    ['Should I focus on one platform or many?', '<p>Focus on one primary platform for your best content, then repurpose to two or three others. This spreads risk without doubling your workload.</p>'],
    ['Do I need a website as an influencer?', '<p>It is the one channel you fully own. A website lets you capture emails, sell products, host a media kit and rank on Google. See our <a href="/website-design/">web design for influencers</a> package.</p>'],
], 'Social media monetization FAQ');
?>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><span class="kicker reveal">Keep learning</span><h2 class="reveal">Latest monetization guides</h2></div>
    <?php post_cards(3); ?>
  </div>
</section>
<?php cta_band('Not sure where to start?', 'Tell Monetizing Influencers about your content and audience, and we will recommend the platforms and income streams that fit.'); ?>
<script>
document.addEventListener('DOMContentLoaded', function () {
  // Base income potential per platform (0-10), then niche, style and size modifiers.
  var base = { youtube: 7, tiktok: 6, instagram: 6.5, facebook: 5, pinterest: 5 };
  var niche = {
    fashion:       { instagram: 2.5, tiktok: 1.5, pinterest: 2, youtube: .5, facebook: 0 },
    fitness:       { instagram: 2, youtube: 1.5, tiktok: 1.5, facebook: .5, pinterest: .5 },
    finance:       { youtube: 3, facebook: 1, instagram: .5, tiktok: .5, pinterest: .5 },
    tech:          { youtube: 3, tiktok: 1, instagram: 0, facebook: 0, pinterest: -1 },
    home:          { pinterest: 3, youtube: 1.5, facebook: 1.5, instagram: 1, tiktok: .5 },
    travel:        { instagram: 2.5, youtube: 1.5, pinterest: 1.5, tiktok: 1, facebook: .5 },
    education:     { youtube: 3, facebook: 1, tiktok: 1, pinterest: 1, instagram: .5 },
    entertainment: { tiktok: 3, youtube: 2, facebook: 1, instagram: 1, pinterest: -1.5 }
  };
  var style = {
    short:    { tiktok: 2.5, instagram: 2, youtube: 1, facebook: 1, pinterest: .5 },
    long:     { youtube: 3, facebook: 1.5, instagram: -.5, tiktok: -.5, pinterest: -.5 },
    photo:    { instagram: 2.5, pinterest: 2.5, facebook: .5, tiktok: -1, youtube: -1.5 },
    live:     { facebook: 2.5, tiktok: 2, youtube: 1.5, instagram: 1, pinterest: -1.5 },
    tutorial: { youtube: 2.5, pinterest: 2, tiktok: 1, instagram: 1, facebook: .5 }
  };
  var size = {
    start: { tiktok: 1.5, pinterest: 1, youtube: -1, facebook: -.5, instagram: 0 },
    small: { tiktok: 1, pinterest: .5, instagram: .5, youtube: 0, facebook: 0 },
    mid:   { instagram: 1, youtube: 1, tiktok: .5, facebook: .5, pinterest: .5 },
    big:   { youtube: 1.5, instagram: 1, facebook: 1, tiktok: .5, pinterest: 0 }
  };
  var why = {
    youtube: 'Ad revenue + evergreen search',
    tiktok: 'Fastest reach + Shop affiliate',
    instagram: 'Biggest brand-deal market',
    facebook: 'Community, lives and Stars',
    pinterest: 'Buyers with search intent'
  };
  var n = document.getElementById('pk-niche'), s = document.getElementById('pk-style'), z = document.getElementById('pk-size');
  var cards = document.querySelectorAll('.pick-card');
  function run() {
    var scores = {};
    Object.keys(base).forEach(function (p) {
      scores[p] = Math.max(1, Math.min(10, (base[p] + niche[n.value][p] + style[s.value][p] + size[z.value][p]) / 1.6));
    });
    var best = Object.keys(scores).sort(function (a, b) { return scores[b] - scores[a]; });
    cards.forEach(function (c) {
      var p = c.dataset.p, sc = c.querySelector('.score');
      sc.textContent = scores[p].toFixed(1) + '/10';
      c.querySelector('.why').textContent = why[p];
      c.classList.toggle('top', p === best[0]);
      c.classList.toggle('dim', best.indexOf(p) >= 3);
      c.style.order = best.indexOf(p);
    });
  }
  [n, s, z].forEach(function (el) { el.addEventListener('change', run); });
  run();
});
</script>
<?php page_end();
