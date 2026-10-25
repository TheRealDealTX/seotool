<?php
require __DIR__ . '/inc/layout.php';

$faqs = [
    ['What is Monetizing Influencers?',
     '<p>Monetizing Influencers is a resource hub and service studio for creators. We publish influencer monetization guides for every major platform, build free tools like the earnings calculator and media kit builder, and design websites that help influencers sell, capture emails and land brand deals.</p>'],
    ['How do influencers make money?',
     '<p>Most influencers earn from a mix of sponsored posts and brand partnerships, affiliate commissions, platform ad revenue (YouTube, Facebook and TikTok programs), selling their own digital or physical products, memberships and paid communities, and freelance services like UGC. The <a href="/monetization/">influencer monetization guide</a> breaks down each one.</p>'],
    ['How many followers do you need to monetize?',
     '<p>You can start earning with as few as 1,000 engaged followers through affiliate links, UGC and small paid collaborations. Brands care more about engagement rate and audience fit than raw follower count, which is why micro-influencers (10K-100K) often get more deals per follower than celebrities.</p>'],
    ['How much should I charge for a sponsored post?',
     '<p>A common starting point is about $100 per 10,000 followers on Instagram, adjusted for engagement, niche, usage rights and deliverables. Try the free <a href="/tools/influencer-earnings-calculator/">influencer earnings calculator</a> for a personalised range, and read the <a href="/how-much-should-influencers-charge/">influencer rate guide</a>.</p>'],
    ['Does Monetizing Influencers build websites for creators?',
     '<p>Yes. Our <a href="/website-design/">web design for influencers</a> package is a fully optimised money site for a one-time $500: custom design, mobile-first build, on-page SEO, content writing, Google Search Console and Google Analytics setup.</p>'],
    ['Can I write a guest post for Monetizing Influencers?',
     '<p>Yes. We accept original articles on influencer marketing, the creator economy, brand deals and affiliate marketing. See the <a href="/write-for-us/">write for us guidelines</a> to pitch.</p>'],
];

page_start([
    'title' => 'Monetizing Influencers | Get Paid More From Your Audience',
    'description' => 'Monetizing Influencers shows creators how to turn followers into income: brand deals, rate guides, free earnings calculators and websites built to earn.',
    'path' => '/',
    'body_class' => 'home',
]);
?>
<section class="hero">
  <canvas id="hero-canvas" aria-hidden="true"></canvas>
  <div class="wrap hero-inner">
    <div>
      <p class="eyebrow reveal"><?= icon('sparkles') ?> The creator income playbook</p>
      <h1 class="reveal"><span class="grad-text">Monetizing Influencers:</span> Get Paid More From Your Audience</h1>
      <p class="lead reveal">Turn your followers into <strong class="grad-text typer" data-words='["brand deals","affiliate income","sponsored posts","product sales","ad revenue","memberships"]'>brand deals</strong>. Monetizing Influencers gives creators the strategy, pricing data and free tools to earn more from every post, on every platform.</p>
      <div class="btn-row reveal">
        <a class="btn btn-glow btn-lg magnetic" href="/get-started/"><?= icon('rocket') ?> Get Started Free</a>
        <a class="btn btn-ghost btn-lg" href="/tools/influencer-earnings-calculator/"><?= icon('calc') ?> What am I worth?</a>
      </div>
      <div class="hero-proof reveal">
        <span><?= icon('check') ?> 6 free creator tools</span>
        <span><?= icon('check') ?> 5 platform playbooks</span>
        <span><?= icon('check') ?> No sign-up needed</span>
      </div>
    </div>
    <div class="phone-stage reveal" aria-hidden="true">
      <div class="float-badge fb-1"><?= icon('handshake') ?><div>New brand deal<small>Skincare collab · $1,200</small></div></div>
      <div class="float-badge fb-2"><?= icon('trending') ?><div>Engagement 6.4%<small>3x the average</small></div></div>
      <div class="float-badge fb-3"><?= icon('dollar') ?><div>Affiliate payout<small>+$486 this week</small></div></div>
      <div class="phone">
        <div class="phone-screen">
          <div class="phone-notch"></div>
          <div class="ph-profile"><div class="ph-avatar"><i></i></div><div><div class="ph-name">@yourchannel</div><div class="ph-handle">Creator · Lifestyle</div></div></div>
          <div class="ph-stats"><div><b>48.2K</b><small>Followers</small></div><div><b>6.4%</b><small>Engage</small></div><div><b>12</b><small>Deals</small></div></div>
          <div class="ph-earn"><small>Earned this month</small><b data-count="8420" data-prefix="$">$8,420</b>
            <div class="ph-bars"><i style="height:40%"></i><i style="height:65%"></i><i style="height:50%"></i><i style="height:80%"></i><i style="height:60%"></i><i style="height:95%"></i><i style="height:75%"></i></div>
          </div>
          <div class="ph-deal"><span class="dot"><?= icon('handshake') ?></span> Brand partnership <b>+$1,200</b></div>
          <div class="ph-deal"><span class="dot"><?= icon('link') ?></span> Affiliate sales <b>+$486</b></div>
          <div class="ph-deal"><span class="dot"><?= icon('play') ?></span> Ad revenue <b>+$312</b></div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="platform-strip" aria-label="Platforms we cover">
  <div class="marquee">
<?php for ($i = 0; $i < 2; $i++): ?>
    <span><?= icon('youtube') ?> YouTube</span><span><?= icon('tiktok') ?> TikTok</span><span><?= icon('instagram') ?> Instagram</span><span><?= icon('facebook') ?> Facebook</span><span><?= icon('pinterest') ?> Pinterest</span><span><?= icon('globe') ?> Your Website</span>
<?php endfor; ?>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <div class="stats">
      <div class="stat reveal"><b data-count="12">12</b><span>Income streams mapped</span></div>
      <div class="stat reveal"><b data-count="5">5</b><span>Platform playbooks</span></div>
      <div class="stat reveal"><b data-count="6">6</b><span>Free interactive tools</span></div>
      <div class="stat reveal"><b data-count="500" data-prefix="$">$500</b><span>Done-for-you money site</span></div>
    </div>
  </div>
</section>

<section class="section" id="what">
  <div class="wrap split">
    <div>
      <span class="kicker reveal">Influencer monetization, explained</span>
      <h2 class="reveal">Followers are attention. <span class="grad-text">Monetizing Influencers</span> turns attention into income.</h2>
      <p class="reveal">Influencer monetization is the business of earning money from the audience you have built. The creators who earn the most rarely rely on one source. They stack brand partnerships, affiliate links, ad revenue and their own products so no single algorithm change can wipe out their income.</p>
      <p class="reveal">Monetizing Influencers exists to make that stack simple. Every guide on this site answers one practical question, from how to price a sponsored post to how to pitch a brand that has never heard of you, and every tool gives you a number you can act on today.</p>
      <ul class="check-list reveal">
        <li>Know your worth with real rate formulas, not guesses</li>
        <li>Pitch brands with templates that get replies</li>
        <li>Diversify so one platform never controls your income</li>
        <li>Own your audience with a website and email list</li>
      </ul>
      <a class="btn btn-glow reveal" href="/monetization/">Read the monetization guide <?= icon('arrow') ?></a>
    </div>
    <div class="reveal" aria-hidden="true">
      <div class="orbit">
        <div class="orbit-ring"></div><div class="orbit-ring r2"></div>
        <?php
        $orbit = [['handshake', 'Brand deals'], ['link', 'Affiliate'], ['play', 'Ad revenue'], ['box', 'Products'], ['users', 'Memberships'], ['camera', 'UGC'], ['tag', 'White label'], ['film', 'Shorts']];
        foreach ($orbit as $i => [$ic, $lb]):
            $a = $i / count($orbit) * 2 * M_PI; $x = round(cos($a) * 44, 2); $y = round(sin($a) * 44, 2); ?>
        <div class="orbit-item" style="left:<?= 50 + $x ?>%;top:<?= 50 + $y ?>%;animation-delay:-<?= $i * 0.6 ?>s"><span><?= icon($ic) ?> <?= e($lb) ?></span></div>
        <?php endforeach; ?>
        <div class="orbit-core">Your<br>Audience</div>
      </div>
    </div>
  </div>
</section>

<section class="section alt-bg" id="methods">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">Monetization methods</span>
      <h2 class="reveal">Five proven ways Monetizing Influencers helps you earn</h2>
      <p class="reveal">These are the core revenue channels we cover in depth. Start with the one that fits your audience size, then stack the rest.</p>
    </div>
    <div class="card-grid cols-3">
      <article class="card tilt reveal"><a href="/monetization/#brand-outreach"><span class="ico-badge"><?= icon('megaphone') ?></span><h3>Brand Outreach</h3><p>Stop waiting for brands to find you. Pitch the companies your audience already buys from with outreach emails that convert.</p><span class="more">Learn brand outreach <?= icon('arrow') ?></span></a></article>
      <article class="card tilt reveal"><a href="/monetization/#partnership-deals"><span class="ico-badge"><?= icon('handshake') ?></span><h3>Partnership Deals</h3><p>Turn one-off sponsored posts into retainers, ambassador programs and revenue-share partnerships that pay every month.</p><span class="more">Land partnership deals <?= icon('arrow') ?></span></a></article>
      <article class="card tilt reveal"><a href="/monetization/#ad-placements"><span class="ico-badge"><?= icon('play') ?></span><h3>Ad Placements</h3><p>Earn from YouTube, Facebook and TikTok creator programs, plus direct ad placements in your videos, newsletter and site.</p><span class="more">Maximise ad revenue <?= icon('arrow') ?></span></a></article>
      <article class="card tilt reveal"><a href="/monetization/#white-labeling"><span class="ico-badge"><?= icon('box') ?></span><h3>White Labeling Products</h3><p>Launch your own branded product line without factories or inventory risk, and keep the margin brands used to keep.</p><span class="more">Launch a product <?= icon('arrow') ?></span></a></article>
      <article class="card tilt reveal"><a href="/monetization/#short-content"><span class="ico-badge"><?= icon('film') ?></span><h3>Short Content Distribution</h3><p>Repurpose one video into Reels, Shorts, TikToks and Pins so every piece of content earns on five platforms, not one.</p><span class="more">Distribute short content <?= icon('arrow') ?></span></a></article>
      <article class="card tilt reveal gradient-border"><a href="/website-design/"><span class="ico-badge"><?= icon('layout') ?></span><h3>Your Own Money Site</h3><p>A website you own captures emails, sells products and ranks on Google. It is the one platform no algorithm can take away.</p><span class="more">Web design for influencers <?= icon('arrow') ?></span></a></article>
    </div>
  </div>
</section>

<section class="section" id="platforms">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">Platform playbooks</span>
      <h2 class="reveal">Monetize every platform you post on</h2>
      <p class="reveal">Each platform pays creators differently. Monetizing Influencers has a dedicated growth and income playbook for all five.</p>
    </div>
    <div class="card-grid cols-3">
      <?php
      $plats = [
          ['youtube', 'YouTube', 'Partner Program requirements, RPM by niche, sponsorship pricing and how to make Shorts pay.'],
          ['tiktok', 'TikTok', 'Creator Rewards, TikTok Shop affiliate, LIVE gifts and pitching brands on the fastest-growing platform.'],
          ['instagram', 'Instagram', 'Sponsored Reels, collabs, subscriptions and the rate formula brands use for Instagram creators.'],
          ['facebook', 'Facebook', 'Facebook influencer marketing, content monetization, Stars and how brands find Facebook influencers.'],
          ['pinterest', 'Pinterest', 'Pinterest influencer marketing, affiliate pins and turning evergreen pins into steady traffic and sales.'],
      ];
      foreach ($plats as [$slug, $name, $txt]): ?>
      <article class="card platform-card p-<?= $slug ?> tilt reveal"><a href="/social-platforms/<?= $slug ?>/"><span class="p-ico"><?= icon($slug) ?></span><h3><?= $name ?> Monetization</h3><p><?= $txt ?></p><span class="more">Open the <?= $name ?> playbook <?= icon('arrow') ?></span></a></article>
      <?php endforeach; ?>
      <article class="card platform-card tilt reveal"><a href="/social-platforms/"><span class="p-ico" style="background:var(--grad)"><?= icon('globe') ?></span><h3>Compare All Platforms</h3><p>Side-by-side: which platform pays best for your niche, audience size and content style.</p><span class="more">See the comparison <?= icon('arrow') ?></span></a></article>
    </div>
  </div>
</section>

<section class="section alt-bg" id="calculator">
  <div class="wrap tool-shell">
    <div class="tool-panel reveal">
      <span class="kicker">Free tool · live preview</span>
      <h2>How much could you earn per sponsored post?</h2>
      <p class="small">Move the sliders. This quick estimate uses the same benchmarks as the full Monetizing Influencers earnings calculator.</p>
      <div class="range-row"><div class="top"><label for="hc-f">Followers</label><output id="hc-fo">25K</output></div><input id="hc-f" type="range" min="1" max="100" value="45"></div>
      <div class="range-row"><div class="top"><label for="hc-e">Engagement rate</label><output id="hc-eo">3.5%</output></div><input id="hc-e" type="range" min="0.5" max="12" step="0.1" value="3.5"></div>
      <div class="field"><label for="hc-p">Platform</label>
        <select id="hc-p"><option value="instagram">Instagram</option><option value="tiktok">TikTok</option><option value="youtube">YouTube</option><option value="facebook">Facebook</option><option value="pinterest">Pinterest</option></select></div>
    </div>
    <div class="tool-panel tool-output reveal gradient-border">
      <p class="small">Estimated rate per sponsored post</p>
      <div class="big-num" id="hc-out">$250 - $400</div>
      <div class="meter"><i id="hc-meter"></i></div>
      <p class="small" id="hc-tier">Micro-influencer tier</p>
      <a class="btn btn-glow" href="/tools/influencer-earnings-calculator/">Open the full calculator <?= icon('arrow') ?></a>
    </div>
  </div>
</section>

<section class="section" id="tools">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">Free creator tools</span>
      <h2 class="reveal">Tools that do the math (and the writing) for you</h2>
      <p class="reveal">Built by Monetizing Influencers for creators who would rather create than crunch numbers. Free, instant and no account required.</p>
    </div>
    <div class="card-grid cols-3">
      <?php
      $tools = [
          ['calc', 'influencer-earnings-calculator', 'Influencer Earnings Calculator', 'Estimate your per-post rate and monthly income by platform, niche and engagement.'],
          ['heart', 'engagement-rate-calculator', 'Engagement Rate Calculator', 'Find your true engagement rate and see how it compares with your follower tier.'],
          ['mail', 'influencer-email-generator', 'Influencer Email Generator', 'Write a brand pitch, or an email to an influencer, in seconds. Copy, tweak, send.'],
          ['file', 'media-kit-builder', 'Media Kit Builder', 'Fill in your stats and get a polished, printable one-page media kit.'],
          ['pie', 'income-stream-simulator', 'Income Stream Simulator', 'Mix brand deals, affiliate, ads and products to see your monthly income grow.'],
          ['quiz', 'monetization-readiness-quiz', 'Monetization Readiness Quiz', 'Ten quick questions to find the best income stream for you right now.'],
      ];
      foreach ($tools as [$ic, $slug, $name, $txt]): ?>
      <article class="card tool-card tilt reveal"><a href="/tools/<?= $slug ?>/"><span class="ico-badge"><?= icon($ic) ?></span><h3><?= $name ?></h3><p><?= $txt ?></p><span class="more">Try it free <?= icon('arrow') ?></span></a></article>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section alt-bg" id="how">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">How it works</span>
      <h2 class="reveal">From followers to a creator business in four steps</h2>
    </div>
    <div class="steps">
      <div class="step reveal"><h3>Audit</h3><p>Use our calculators to measure engagement and find what your audience is worth to brands.</p></div>
      <div class="step reveal"><h3>Package</h3><p>Build a media kit and rate card so brands can say yes quickly.</p></div>
      <div class="step reveal"><h3>Pitch</h3><p>Send outreach that gets replies using proven Monetizing Influencers templates.</p></div>
      <div class="step reveal"><h3>Stack</h3><p>Add affiliate, products and a money site so income keeps growing between deals.</p></div>
    </div>
  </div>
</section>

<section class="section" id="niches">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">Niches we know</span>
      <h2 class="reveal">Monetizing Influencers works across niches</h2>
      <p class="reveal">Every niche has its own brands, budgets and best-paying formats. Here is where our creators earn.</p>
    </div>
    <div class="card-grid cols-3 niche-grid">
      <?php
      $niches = [
          ['fashion', 'Fashion', 'Fashion influencers earn from seasonal campaigns, affiliate hauls and capsule collections. Lookbooks and try-on Reels are the highest-paying formats.'],
          ['fitness', 'Fitness', 'Fitness creators monetize with supplement and apparel partnerships, workout programs, coaching and app affiliate deals.'],
          ['motorcross', 'Motocross', 'Motocross riders land gear, parts and energy-drink sponsorships. Helmet-cam content and race-day vlogs drive the deals.'],
          ['mountain-biking', 'Mountain Biking', 'Mountain biking influencers partner with bike, component and outdoor brands, and earn affiliate income on high-ticket gear.'],
          ['luxury', 'Luxury & Travel', 'Luxury creators command premium rates from hotels, jewellery and lifestyle brands that pay for polished, aspirational content.'],
          ['finance', 'Finance', 'Finance influencers earn some of the highest RPMs and affiliate payouts online, from fintech apps to investing platforms.'],
      ];
      foreach ($niches as [$img, $name, $txt]): ?>
      <article class="card niche-card reveal"><img src="/assets/img/niche-<?= $img ?>.webp" width="500" height="333" loading="lazy" alt="<?= e($name) ?> influencer content example"><div class="body"><h3><?= e($name) ?> influencers</h3><p><?= e($txt) ?></p></div></article>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section alt-bg" id="web-design">
  <div class="wrap split reverse">
    <div class="reveal">
      <img src="/assets/img/portfolio-responsive-websites.webp" width="1200" height="717" loading="lazy" alt="Influencer website shown on desktop, tablet and phone">
    </div>
    <div>
      <span class="kicker reveal">Web design for influencers</span>
      <h2 class="reveal">Own your audience with a website that earns</h2>
      <p class="reveal">Social platforms rent you an audience. A website lets you own it. Monetizing Influencers designs fast, mobile-first money sites for creators, with a media kit page, email capture, affiliate-ready product pages and the SEO to rank on Google.</p>
      <ul class="check-list reveal">
        <li>Custom design that matches your personal brand</li>
        <li>On-page SEO, Search Console and Analytics set up</li>
        <li>Content writing included if you need it</li>
        <li>One-time <strong>$500</strong>, domain and email hosting included</li>
      </ul>
      <a class="btn btn-glow reveal" href="/website-design/">See the $500 money site <?= icon('arrow') ?></a>
    </div>
  </div>
</section>

<section class="section" id="latest">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">From the Monetizing Influencers blog</span>
      <h2 class="reveal">Fresh guides for creators who want to earn more</h2>
    </div>
    <?php post_cards(3); ?>
    <p style="text-align:center;margin-top:34px"><a class="btn btn-ghost" href="/blogs/">See all guides <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section alt-bg" id="write">
  <div class="wrap split">
    <div>
      <span class="kicker reveal">Write for us</span>
      <h2 class="reveal">Share your creator economy expertise</h2>
      <p class="reveal">Monetizing Influencers accepts guest posts on influencer marketing, brand deals, affiliate marketing and the creator economy. If you have real, practical experience helping creators get paid, we want to publish it.</p>
      <a class="btn btn-glow reveal" href="/write-for-us/">Read the guidelines <?= icon('pen') ?></a>
    </div>
    <div class="glass-panel reveal">
      <h3>Topics we are looking for</h3>
      <ul class="pill-list">
        <li>Influencer marketing</li><li>Brand deals</li><li>Creator economy</li><li>Affiliate marketing</li><li>UGC</li><li>Pinterest marketing</li><li>Short-form video</li><li>Creator finances</li><li>Media kits</li><li>Case studies</li>
      </ul>
    </div>
  </div>
</section>

<?php faq_block($faqs, 'Monetizing Influencers FAQ'); ?>

<?php cta_band('Start monetizing your influence today', 'Tell Monetizing Influencers about your channel and get a free outline of the income streams that fit your niche, platform and audience size.'); ?>

<script>
document.addEventListener('DOMContentLoaded', function () {
  var f = document.getElementById('hc-f'), en = document.getElementById('hc-e'), p = document.getElementById('hc-p');
  // slider 1-100 maps logarithmically to 1K-5M followers
  function followers() { return Math.round(1000 * Math.pow(5000, (f.value - 1) / 99)); }
  var base = { instagram: 10, tiktok: 7, youtube: 20, facebook: 6, pinterest: 5 }; // $ per 1K followers at 3% engagement
  function update() {
    var n = followers(), er = parseFloat(en.value), mult = Math.max(.4, Math.min(2.2, er / 3));
    var mid = n / 1000 * base[p.value] * mult, lo = Math.max(25, mid * .75), hi = Math.max(60, mid * 1.3);
    document.getElementById('hc-fo').textContent = window.MI ? MI.fmtNum(n) : n;
    document.getElementById('hc-eo').textContent = er.toFixed(1) + '%';
    document.getElementById('hc-out').textContent = '$' + Math.round(lo).toLocaleString() + ' - $' + Math.round(hi).toLocaleString();
    var tier = n < 10000 ? 'Nano-influencer' : n < 100000 ? 'Micro-influencer' : n < 500000 ? 'Mid-tier influencer' : n < 1000000 ? 'Macro-influencer' : 'Mega-influencer';
    document.getElementById('hc-tier').textContent = tier + ' tier · ' + (er >= 3 ? 'above' : 'below') + '-average engagement';
    document.getElementById('hc-meter').style.width = Math.min(100, (f.value / 100) * 70 + mult * 14) + '%';
  }
  [f, en, p].forEach(function (el) { el.addEventListener('input', update); });
  update();
});
</script>
<?php page_end();
