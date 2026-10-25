<?php
require __DIR__ . '/../inc/layout.php';

$faqs = [
    ['How much does web design for influencers cost?', '<p>The Monetizing Influencers Fully Optimized Money Site is a one-time $500. That includes custom design, a responsive build, on-page SEO, content writing if you need it, Google Search Console and Google Analytics setup, plus domain and email hosting.</p>'],
    ['Do influencers really need a website?', '<p>Yes, if you want to own your audience. Social accounts can be restricted, hacked or throttled by algorithm changes. A website gives you a permanent home for your media kit, an email list, product and affiliate pages, and a way to be found on Google.</p>'],
    ['How long does it take to build an influencer website?', '<p>Most money sites go live within about two weeks of receiving your content and brand assets. If we write the content for you, allow a few extra days for your review.</p>'],
    ['Can I edit the website myself after launch?', '<p>Yes. We hand over the site with simple instructions, and you can always ask us to make updates for you.</p>'],
    ['Will my website help me get brand deals?', '<p>A professional site with a media kit page, clear audience stats and a contact form makes it easier for brands to evaluate you and say yes. It also shows you take your creator business seriously.</p>'],
    ['What do I need to provide?', '<p>Your social handles, logo or brand colours if you have them, photos, and a short note about your goals. If you do not have written content, our writers will draft it for you to proof.</p>'],
];

page_start([
    'title' => 'Web Design for Influencers | $500 Money Site',
    'description' => 'Web design for influencers: a fully optimized, mobile-first money site with SEO, content writing, analytics and hosting for a one-time $500.',
    'path' => '/website-design/',
    'extra_css' => ['/assets/css/pages.css'],
    'schema' => [[
        '@type' => 'Service',
        'name' => 'Web Design for Influencers - Fully Optimized Money Site',
        'serviceType' => 'Influencer website design',
        'provider' => ['@id' => SITE_URL . '/#org'],
        'areaServed' => 'Worldwide',
        'description' => 'Custom, responsive, SEO-optimized websites for influencers and creators, including content writing, Google Search Console, Google Analytics, domain and email hosting.',
        'offers' => ['@type' => 'Offer', 'price' => '500', 'priceCurrency' => 'USD', 'url' => SITE_URL . '/website-design/', 'availability' => 'https://schema.org/InStock'],
    ]],
]);

page_hero('Web design for influencers',
    'Web Design for Influencers That <span class="grad-text">Actually Earns</span>',
    'Your followers live on platforms you do not control. Monetizing Influencers builds fast, beautiful money sites that capture emails, sell products, showcase your media kit and rank on Google, all for a one-time <strong>$500</strong>.',
    [['Web Design', '/website-design/']],
    '<div class="btn-row reveal"><a class="btn btn-glow btn-lg magnetic" href="#web-design">' . icon('rocket') . ' Get my $500 money site</a><a class="btn btn-ghost btn-lg" href="#included">See what is included</a></div>');
?>
<section class="section" style="padding-top:10px">
  <div class="wrap split">
    <div class="reveal" aria-hidden="true">
      <div class="browser">
        <div class="browser-bar"><i></i><i></i><i></i><span>yourname.com</span></div>
        <div class="mock-site">
          <div class="mock-hero">
            <div><b>Hi, I'm Your Name.</b><div class="mock-line w80"></div><div class="mock-line w60"></div><span class="mock-btn">Work with me</span></div>
            <div class="mock-avatar"></div>
          </div>
          <div class="mock-cards">
            <div><b>Media kit</b>48K followers · 6.4% ER</div>
            <div><b>Shop</b>Presets &amp; merch</div>
            <div><b>Favourites</b>Affiliate picks</div>
          </div>
          <div class="mock-email"><span></span><em>Join the list</em></div>
        </div>
      </div>
    </div>
    <div>
      <span class="kicker reveal">Influencer website design</span>
      <h2 class="reveal">Why every influencer needs a website</h2>
      <p class="reveal">A link-in-bio page is a signpost. A website is a business. With your own site, every post can send followers somewhere you control: a page that collects their email, recommends products through your affiliate links, sells your own products and tells brands exactly why they should hire you.</p>
      <ul class="check-list reveal">
        <li><strong>Own your audience.</strong> An email list cannot be taken away by an algorithm update.</li>
        <li><strong>Get found on Google.</strong> Searchers become followers, buyers and clients.</li>
        <li><strong>Close more brand deals.</strong> A professional media kit page builds instant trust.</li>
        <li><strong>Earn while you sleep.</strong> Product, shop and affiliate pages keep selling.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section alt-bg" id="features">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">What you get</span>
      <h2 class="reveal">Built to grow your influence and your income</h2>
      <p class="reveal">Every Monetizing Influencers website is designed around one goal: turning visitors into revenue.</p>
    </div>
    <div class="card-grid cols-3">
      <article class="card tilt reveal"><span class="ico-badge"><?= icon('pen') ?></span><h3>Customized Design</h3><p>Our designers create a visually appealing, professional site that matches your brand identity and resonates with your audience. No cookie-cutter templates.</p></article>
      <article class="card tilt reveal"><span class="ico-badge"><?= icon('layout') ?></span><h3>Responsive and User-Friendly</h3><p>Most of your traffic comes from phones. Your site adapts seamlessly to mobile, tablet and desktop, so every visitor gets a fast, smooth experience.</p></article>
      <article class="card tilt reveal"><span class="ico-badge"><?= icon('search') ?></span><h3>Search Engine Optimization</h3><p>Keyword research, on-page optimization, meta tags and XML sitemaps so your site can rank higher on Google and attract organic traffic.</p></article>
      <article class="card tilt reveal"><span class="ico-badge"><?= icon('sparkles') ?></span><h3>Engaging Content</h3><p>Our writers craft copy that tells your story, highlights what you offer and persuades visitors to subscribe, buy or book, with keywords built in.</p></article>
      <article class="card tilt reveal"><span class="ico-badge"><?= icon('chart') ?></span><h3>Analytics Integration</h3><p>Google Analytics shows who visits, where they come from and what they click, so you can make smart decisions and prove your reach to brands.</p></article>
      <article class="card tilt reveal"><span class="ico-badge"><?= icon('zap') ?></span><h3>Fast and Secure</h3><p>Lightweight code, compressed images and HTTPS keep your site quick to load, which helps both your visitors and your search rankings.</p></article>
    </div>
  </div>
</section>

<section class="section" id="pages">
  <div class="wrap split reverse">
    <div class="reveal"><img src="/assets/img/portfolio-responsive-websites.webp" width="1200" height="717" loading="lazy" alt="Influencer website design shown on desktop, laptop, tablet and phone"></div>
    <div>
      <span class="kicker reveal">What pages a website for influencers needs</span>
      <h2 class="reveal">The money site blueprint</h2>
      <p class="reveal">We plan your site around the pages that make creators money. A typical influencer website includes:</p>
      <ul class="check-list reveal">
        <li><strong>Home</strong> with a clear hook, your best content and an email signup</li>
        <li><strong>About</strong> that tells your story and builds trust</li>
        <li><strong>Media kit / Work with me</strong> with audience stats, past collaborations and a brand enquiry form</li>
        <li><strong>Shop or favourites</strong> for your products and affiliate recommendations</li>
        <li><strong>Blog</strong> to rank on Google and repurpose your social content</li>
        <li><strong>Contact</strong> so brands and fans can reach you easily</li>
      </ul>
      <p class="reveal">Each page gets its own target keyword, title and description, so your influencer website can start ranking for your name, your niche and the questions your audience searches. Over time your blog posts become a second source of followers that does not depend on any social algorithm.</p>
    </div>
  </div>
</section>

<section class="section alt-bg" id="included">
  <div class="wrap split">
    <div>
      <span class="kicker reveal">Money site inclusions</span>
      <h2 class="reveal">Everything included for one price</h2>
      <div class="card-grid cols-2" style="margin-top:24px">
        <div class="card reveal"><h3><?= icon('globe') ?> Domain &amp; Email Hosting</h3><p>Get your domain and a professional email address with no extra charge.</p></div>
        <div class="card reveal"><h3><?= icon('layout') ?> Website Design</h3><p>Modern, visually captivating layouts that elevate your online presence.</p></div>
        <div class="card reveal"><h3><?= icon('pen') ?> Content Writing</h3><p>No content yet? Our writers draft it for you to proof and approve.</p></div>
        <div class="card reveal"><h3><?= icon('search') ?> On-Page SEO</h3><p>Optimized titles, headings, meta descriptions and internal links on every page.</p></div>
        <div class="card reveal"><h3><?= icon('chart') ?> Google Search Console</h3><p>Set up and verified so you can see how your site appears in Google.</p></div>
        <div class="card reveal"><h3><?= icon('trending') ?> Google Analytics</h3><p>Track visitors, traffic sources and conversions from day one.</p></div>
      </div>
    </div>
    <div class="reveal">
      <div class="card price-card gradient-border">
        <span class="badge">Fully Optimized Money Site</span>
        <div class="price">$500 <small>one-time</small></div>
        <p>No monthly design fees. No surprise add-ons.</p>
        <ul class="check-list">
          <li>Custom design for your brand</li>
          <li>Mobile-first responsive build</li>
          <li>On-page SEO and XML sitemap</li>
          <li>Content writing included</li>
          <li>Search Console and Analytics setup</li>
          <li>Domain and email hosting</li>
        </ul>
        <a class="btn btn-glow btn-lg magnetic" href="#web-design">Request my site <?= icon('arrow') ?></a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="process">
  <div class="wrap">
    <div class="section-head"><span class="kicker reveal">How it works</span><h2 class="reveal">From idea to live site in four steps</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Tell us your goals</h3><p>Fill in the short quote form with your handles, niche and what you want the site to do.</p></div>
      <div class="step reveal"><h3>Plan and write</h3><p>We map your pages and keywords, and draft content if you need it.</p></div>
      <div class="step reveal"><h3>Design and build</h3><p>You review a custom design and request changes before we finalise.</p></div>
      <div class="step reveal"><h3>Launch and grow</h3><p>We go live, connect Search Console and Analytics, and show you the ropes.</p></div>
    </div>
  </div>
</section>

<section class="section alt-bg" id="compare">
  <div class="wrap narrow">
    <div class="section-head"><span class="kicker reveal">Done-for-you vs DIY</span><h2 class="reveal">Why not just use a DIY website builder?</h2>
      <p class="reveal">DIY builders are a fine option if you enjoy design and SEO. If you would rather spend that time creating content, here is how the two approaches compare.</p></div>
    <div class="table-scroll reveal">
      <table class="data-table compare">
        <thead><tr><th>What you get</th><th>Monetizing Influencers money site</th><th>Typical DIY builder</th></tr></thead>
        <tbody>
          <tr><td>Custom design for your brand</td><td class="yes">Included</td><td class="part">You design it</td></tr>
          <tr><td>Content written for you</td><td class="yes">Included</td><td class="no">No</td></tr>
          <tr><td>Keyword research and on-page SEO</td><td class="yes">Included</td><td class="part">You set it up</td></tr>
          <tr><td>Search Console and Analytics setup</td><td class="yes">Included</td><td class="part">You set it up</td></tr>
          <tr><td>Built around creator income pages</td><td class="yes">Yes</td><td class="part">Depends on template</td></tr>
          <tr><td>Pricing model</td><td class="yes">One-time $500</td><td class="part">Usually a monthly plan</td></tr>
          <tr><td>Your time investment</td><td class="yes">A short brief and review</td><td class="part">Many hours</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section" id="quote">
  <div class="wrap split" style="align-items:start">
    <div>
      <span class="kicker reveal">Get started</span>
      <h2 class="reveal">Request your influencer website</h2>
      <p class="reveal">Tell us a little about your channel and goals. We will reply within 1-2 business days with next steps and any questions. There is no payment until you are happy with the plan.</p>
      <div class="callout reveal"><?= icon('shield') ?><p>Prefer email? Write to <a href="mailto:<?= e(SITE_EMAIL) ?>"><?= e(SITE_EMAIL) ?></a> or call <a href="tel:<?= e(SITE_PHONE_HREF) ?>"><?= e(SITE_PHONE) ?></a>.</p></div>
    </div>
    <div class="glass-panel reveal" id="web-design">
      <?= form_flash('web-design') ?>
      <form class="form js-form" action="/api/form.php" method="post">
        <?= form_guard('web-design', '/website-design/') ?>
        <div class="form-row">
          <div class="field"><label for="wd-name">Name *</label><input id="wd-name" type="text" name="name" required autocomplete="name"></div>
          <div class="field"><label for="wd-email">Email *</label><input id="wd-email" type="email" name="email" required autocomplete="email"></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="wd-handle">Main social handle</label><input id="wd-handle" type="text" name="social_handle" placeholder="@yourname"></div>
          <div class="field"><label for="wd-niche">Niche</label><input id="wd-niche" type="text" name="niche" placeholder="Fitness, fashion, finance..."></div>
        </div>
        <div class="field"><label for="wd-budget">Package</label>
          <select id="wd-budget" name="budget"><option>Fully Optimized Money Site ($500)</option><option>Money site plus extras (let's talk)</option><option>Not sure yet</option></select></div>
        <div class="field"><label for="wd-goals">What should your website do for you?</label><textarea id="wd-goals" name="goals" placeholder="Get brand deals, sell presets, grow my email list..."></textarea></div>
        <button class="btn btn-glow btn-lg" type="submit"><?= icon('rocket') ?> Send my request</button>
      </form>
    </div>
  </div>
</section>

<?php faq_block($faqs, 'Web design for influencers FAQ'); ?>
<?php cta_band('Own your audience. Launch your money site.', 'A one-time $500 website from Monetizing Influencers, built to collect emails, sell products and land brand deals.', 'Request my site', '#web-design'); ?>
<?php page_end();
