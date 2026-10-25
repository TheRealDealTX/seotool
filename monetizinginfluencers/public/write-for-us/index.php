<?php
require __DIR__ . '/../inc/layout.php';

$categories = [
    ['megaphone', 'Influencer Marketing', 'Campaign strategy, influencer outreach, measuring ROI, working with micro-influencers and how brands and creators build partnerships that last.'],
    ['globe', 'Creator Economy', 'Trends, business models, platform changes and data on how creators build sustainable, independent businesses.'],
    ['link', 'Affiliate Marketing', 'Affiliate programs for creators, link placement, conversion tactics, disclosure and turning content into commission.'],
    ['handshake', 'Brand Deals', 'Pitching, media kits, pricing sponsored posts, negotiating contracts, usage rights and long-term ambassador deals.'],
    ['play', 'Social Platforms', 'Growth and monetization on Pinterest, TikTok, YouTube, Instagram and Facebook, including algorithm updates.'],
    ['dollar', 'Creator Finance', 'Taxes, invoicing, budgeting irregular income, passive income and building a creator business that pays reliably.'],
];

$topics = [
    'How to land brand deals as a micro-influencer',
    'Crafting a winning media kit or outreach email',
    'Affiliate marketing for creators',
    'Monetizing short-form video (Reels, TikTok, Shorts)',
    'Tools influencers use to manage partnerships',
    'Starting a product line as an influencer (white labeling 101)',
    'Content strategy for multi-platform growth',
    'How to price sponsored posts and campaigns',
    'Passive income for creators',
    'Building your brand as a creator or influencer',
    'Navigating taxes and finances as a digital creator',
    'YouTube monetization and revenue breakdowns',
    'Pinterest influencer marketing strategies',
    'Creator case studies and success stories',
];

$faqs = [
    ['Do you accept guest posts about influencer marketing?', '<p>Yes. Monetizing Influencers accepts original guest posts on influencer marketing, the creator economy, affiliate marketing, brand deals, social platforms and creator finance. Send your pitch using the form on this page or email ' . e(SITE_EMAIL) . '.</p>'],
    ['Do you pay for guest posts?', '<p>The rate is provided once your pitch is approved, and the payment method is shared on acceptance.</p>'],
    ['Do you accept sponsored posts?', '<p>Yes, on relevant topics. Sponsored content must meet the same quality guidelines, rates are available on request, and sponsored articles are clearly labelled as sponsored.</p>'],
    ['How many links can I include?', '<p>Up to two relevant do-follow links to your own site or portfolio, placed naturally in the article or your author bio. Links must add value for the reader.</p>'],
    ['How long does the review take?', '<p>We review every submission within 5-7 business days and email you whether it is accepted, needs edits, or is not a fit.</p>'],
    ['Can I republish my article elsewhere?', '<p>No. Accepted articles require exclusive publishing rights and become the property of Monetizing Influencers, so they cannot be republished elsewhere.</p>'],
    ['What topics do you not accept?', '<p>We do not accept content about gambling, adult material or any prohibited industry, or anything that is mainly an advert with no practical value for creators.</p>'],
];

page_start([
    'title' => 'Influencer Marketing Write For Us: Submit a Guest Post',
    'description' => 'Write for us: submit influencer marketing, creator economy and affiliate marketing guest posts to Monetizing Influencers. Guidelines, topics and pitch form.',
    'path' => '/write-for-us/',
    'extra_css' => ['/assets/css/pages.css'],
]);

page_hero('Guest posts · Article submission',
    'Write For Us: <span class="grad-text">Influencer Marketing</span> &amp; Creator Economy Guest Posts',
    'Passionate about influencer marketing, brand deals, content creation or digital income streams? Monetizing Influencers helps creators get paid more from their audience, and we are inviting experts, marketers and creators like you to share what works with our growing global community.',
    [['Write For Us', '/write-for-us/']],
    '<div class="btn-row reveal"><a class="btn btn-glow btn-lg magnetic" href="#write-for-us">' . icon('pen') . ' Submit your pitch</a><a class="btn btn-ghost btn-lg" href="#guidelines">Read the guidelines</a></div><p class="small reveal" style="margin-top:16px">Prefer email? Send your pitch or article to <a href="mailto:' . e(SITE_EMAIL) . '?subject=Guest%20post%20pitch">' . e(SITE_EMAIL) . '</a></p>');
?>
<section class="section" style="padding-top:10px">
  <div class="wrap">
    <div class="stats">
      <div class="stat reveal"><b data-count="800" data-suffix="+">800+</b><span>Minimum words</span></div>
      <div class="stat reveal"><b data-count="2">2</b><span>Do-follow links allowed</span></div>
      <div class="stat reveal"><b data-count="7">7</b><span>Business days max review</span></div>
      <div class="stat reveal"><b data-count="6">6</b><span>Topic categories</span></div>
    </div>
  </div>
</section>

<section class="section" id="who" style="padding-top:20px">
  <div class="wrap split">
    <div>
      <span class="kicker reveal">Who we are</span>
      <h2 class="reveal">Write for an audience that wants to get paid</h2>
      <p class="reveal">Monetizing Influencers is dedicated to helping creators and influencers maximize their revenue potential. Our readers are influencers, content creators, social media strategists and marketers who want practical advice they can use today. Whether you are an influencer, brand strategist, content creator or digital entrepreneur, your voice belongs here.</p>
      <p class="reveal">Our mission is simple: give influencers the tools, insights and strategies they need to turn their passion into profit. We cover:</p>
      <ul class="check-list reveal">
        <li>Brand outreach strategies and paid partnership deals</li>
        <li>Ad placements and sponsored content</li>
        <li>White labeling and product launches</li>
        <li>Short-form content monetization and social media growth</li>
        <li>Creator business models and passive income</li>
      </ul>
    </div>
    <div class="glass-panel reveal">
      <h3><?= icon('star') ?> Content we love</h3>
      <ul class="check-list">
        <li>Actionable advice and real-world strategies</li>
        <li>Creator stories and behind-the-scenes lessons</li>
        <li>Data-driven insights and platform algorithm updates</li>
        <li>Trend reports on the creator economy</li>
        <li>Monetization tips based on personal experience</li>
      </ul>
      <p class="small" style="margin:0">We do <strong>not</strong> accept content related to gambling, adult material or prohibited industries.</p>
    </div>
  </div>
</section>

<section class="section alt-bg" id="categories">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">Topic categories</span>
      <h2 class="reveal">What we publish</h2>
      <p class="reveal">Pitch an article in one of these six categories. Specific, experience-led angles always beat broad overviews.</p>
    </div>
    <div class="card-grid cols-3">
<?php foreach ($categories as [$ic, $name, $txt]): ?>
      <article class="card tilt reveal"><span class="ico-badge"><?= icon($ic) ?></span><h3><?= e($name) ?> write for us</h3><p><?= e($txt) ?></p></article>
<?php endforeach; ?>
    </div>
    <div class="glass-panel reveal" style="margin-top:30px">
      <h3>Article ideas we would love to see</h3>
      <ul class="pill-list">
<?php foreach ($topics as $t): ?>
        <li><?= e($t) ?></li>
<?php endforeach; ?>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="generator">
  <div class="wrap tool-shell">
    <div class="tool-panel reveal">
      <span class="kicker">Free tool</span>
      <h2>Stuck for an angle? Generate pitch-ready headlines</h2>
      <p class="small">Pick a category and the readers you want to help. We will suggest headlines you can pitch to Monetizing Influencers (or adapt for any influencer marketing blog).</p>
      <div class="field"><label for="ig-cat">Category</label>
        <select id="ig-cat"><?php foreach ($categories as [, $name]): ?><option><?= e($name) ?></option><?php endforeach; ?></select></div>
      <div class="field" style="margin-top:14px"><label for="ig-aud">Who is it for?</label>
        <select id="ig-aud"><option value="micro-influencers">Micro-influencers</option><option value="new creators">New creators</option><option value="full-time creators">Full-time creators</option><option value="brands and marketers">Brands and marketers</option></select></div>
      <div class="btn-row" style="margin-top:20px"><button class="btn btn-glow" id="ig-go" type="button"><?= icon('sparkles') ?> Generate ideas</button></div>
    </div>
    <div class="tool-panel tool-output reveal gradient-border">
      <p class="small">Your headline ideas</p>
      <ul class="idea-list" id="ig-out" aria-live="polite"><li>Click "Generate ideas" to get five pitch-ready headlines.</li></ul>
    </div>
  </div>
</section>

<section class="section alt-bg" id="guidelines">
  <div class="wrap split" style="align-items:start">
    <div class="prose">
      <span class="kicker reveal">Submission guidelines</span>
      <h2 class="reveal" style="margin-top:0">How to write for Monetizing Influencers</h2>
      <p class="reveal">To make sure your influencer marketing article is a good fit for our audience, please follow these guidelines:</p>
      <ul class="reveal">
        <li><strong>Length:</strong> 800-2,500+ words.</li>
        <li><strong>Original:</strong> unpublished anywhere else and written by you (no AI-spun or rewritten content).</li>
        <li><strong>Formatting:</strong> clear headers, short paragraphs and bullet points.</li>
        <li><strong>Links:</strong> up to 2 relevant do-follow links to your site or portfolio.</li>
        <li><strong>Style:</strong> professional but conversational and encouraging.</li>
        <li><strong>Audience:</strong> influencers, creators, social media strategists and marketers.</li>
        <li><strong>Images (optional):</strong> 1-2 royalty-free images or infographics. We can source them if needed.</li>
      </ul>
      <h3 class="reveal">Payment and review process</h3>
      <ul class="reveal">
        <li><strong>Rate:</strong> provided upon pitch approval.</li>
        <li><strong>Payment method:</strong> shared upon acceptance.</li>
        <li><strong>Review:</strong> within 5-7 business days. Minor edits may be made for grammar, SEO or clarity.</li>
        <li><strong>Notification:</strong> you will hear from us on acceptance, with your publication date.</li>
      </ul>
      <h3 class="reveal">Republishing policy</h3>
      <p class="reveal">To keep content unique and high quality, we require exclusive publishing rights. Once accepted, your article becomes the property of Monetizing Influencers and cannot be republished elsewhere.</p>
    </div>
    <div class="glass-panel reveal">
      <h3><?= icon('check') ?> Pre-submission checklist</h3>
      <p class="small">Tick each item before you hit send.</p>
      <ul class="checklist" id="checklist">
<?php foreach (['My topic fits one of the six categories', 'The article is 800+ words and unpublished', 'It uses headers, short paragraphs and bullets', 'It includes real examples, data or experience', 'No more than 2 do-follow links', 'Nothing about gambling, adult or prohibited industries', 'Images (if any) are royalty-free', 'I agree to exclusive publishing rights'] as $i => $c): ?>
        <li><label><input type="checkbox"> <span><?= e($c) ?></span></label></li>
<?php endforeach; ?>
      </ul>
      <div class="check-score"><span>Ready to pitch</span><span id="ck-score">0 / 8</span></div>
      <div class="meter"><i id="ck-meter"></i></div>
    </div>
  </div>
</section>

<section class="section" id="pitch">
  <div class="wrap split" style="align-items:start">
    <div>
      <span class="kicker reveal">Example pitch</span>
      <h2 class="reveal">A pitch email that gets accepted</h2>
      <p class="reveal">Keep it short: who you are, the headline, why our readers need it, and an outline. Copy this template and make it yours.</p>
      <div class="template-box reveal" id="pitch-template">Subject: Guest post pitch: [Your headline]

Hi Monetizing Influencers team,

I'm [Name], a [role, e.g. UGC creator / influencer marketing manager] who has [one line of credibility, e.g. run 40+ creator campaigns for DTC brands].

I'd love to write "[Headline]" for your readers. It will show [audience] how to [specific outcome], with [examples, data or a case study] they can apply right away.

Outline:
1. [Section]
2. [Section]
3. [Section]

Recent writing: [link 1], [link 2]

Thanks for considering it!
[Name]
<button class="btn btn-ghost btn-sm copy-btn" type="button" data-copy="#pitch-template"><?= icon('copy') ?> Copy</button></div>
    </div>
    <div class="glass-panel gradient-border reveal" id="write-for-us">
      <h2 style="font-size:1.6rem">Submit your guest post pitch</h2>
      <?= form_flash('write-for-us') ?>
      <form class="form js-form" action="/api/form.php" method="post">
        <?= form_guard('write-for-us', '/write-for-us/') ?>
        <div class="form-row">
          <div class="field"><label for="wf-name">Name *</label><input id="wf-name" type="text" name="name" required autocomplete="name"></div>
          <div class="field"><label for="wf-email">Email *</label><input id="wf-email" type="email" name="email" required autocomplete="email"></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="wf-site">Website</label><input id="wf-site" type="url" name="website" placeholder="https://"></div>
          <div class="field"><label for="wf-cat">Category</label>
            <select id="wf-cat" name="category"><?php foreach ($categories as [, $name]): ?><option><?= e($name) ?></option><?php endforeach; ?></select></div>
        </div>
        <div class="field"><label for="wf-topic">Proposed headline *</label><input id="wf-topic" type="text" name="topic" required></div>
        <div class="field"><label for="wf-pitch">Your pitch and outline</label><textarea id="wf-pitch" name="pitch" placeholder="Why this article, who it helps, and a short outline"></textarea></div>
        <div class="field"><label for="wf-sample">Link to a writing sample</label><input id="wf-sample" type="url" name="sample_url" placeholder="https://"></div>
        <button class="btn btn-glow btn-lg" type="submit"><?= icon('pen') ?> Send my pitch</button>
      </form>
    </div>
  </div>
</section>

<?php faq_block($faqs, 'Write for us FAQ'); ?>
<?php cta_band('Ready to share your expertise?', 'If you are a creator, strategist, freelancer or marketer ready to help others monetize their influence, we want to hear from you. Let\'s help the next wave of creators get paid what they are worth.', 'Submit your pitch', '#write-for-us'); ?>

<script>
document.addEventListener('DOMContentLoaded', function () {
  var T = {
    'Influencer Marketing': ['How {A} Can Run an Influencer Campaign That Pays for Itself', 'The Influencer Marketing Brief Template That Gets Better Content From {A}', '7 Influencer Marketing Metrics {A} Should Track (and 3 to Ignore)', 'Micro vs Macro: Which Influencers Should {A} Work With in {Y}?', 'Influencer Marketing on Pinterest: A Practical Guide for {A}', 'How to Write to an Influencer: Outreach Lessons for {A}'],
    'Creator Economy': ['The Creator Economy in {Y}: What {A} Need to Know', 'Why {A} Are Building Owned Audiences (and How to Start)', 'From Side Hustle to Salary: A Creator Economy Roadmap for {A}', '5 Creator Economy Business Models {A} Can Copy', 'What the Creator Economy Gets Wrong About {A}'],
    'Affiliate Marketing': ['Affiliate Marketing for {A}: Where to Put Your Links in {Y}', 'How {A} Can Double Affiliate Clicks Without More Followers', 'The Affiliate Disclosure Guide {A} Actually Need', 'High-Ticket vs Low-Ticket Affiliate Programs for {A}', 'Building a Product Recommendation Page That Converts for {A}'],
    'Brand Deals': ['How {A} Can Land Their First Paid Brand Deal in 30 Days', 'The Media Kit Checklist Brands Want From {A}', 'How {A} Should Price Usage Rights and Whitelisting', 'Negotiating Brand Deals: Scripts for {A}', 'Turning One-Off Sponsorships Into Retainers: A Guide for {A}'],
    'Social Platforms': ['Pinterest Influencer Marketing: How {A} Can Drive Evergreen Sales', 'TikTok Shop for {A}: What Actually Sells', 'YouTube Shorts vs Long-Form: Monetization Math for {A}', 'Instagram Collabs: How {A} Can Grow Faster Together', 'Facebook Influencer Marketing in {Y}: Opportunities for {A}'],
    'Creator Finance': ['Taxes for {A}: A Plain-English Starter Guide', 'How {A} Can Budget Irregular Creator Income', 'Invoicing Brands: Payment Terms {A} Should Insist On', 'Building Passive Income Streams as {A}', 'The Creator Emergency Fund: Why {A} Need One'],
  };
  var out = document.getElementById('ig-out'), y = new Date().getFullYear();
  function cap(s) { return s.replace(/\b\w/g, function (c) { return c.toUpperCase(); }); }
  document.getElementById('ig-go').addEventListener('click', function () {
    var list = T[document.getElementById('ig-cat').value].slice(), aud = cap(document.getElementById('ig-aud').value);
    list.sort(function () { return Math.random() - .5; });
    out.innerHTML = '';
    list.slice(0, 5).forEach(function (h, i) {
      var li = document.createElement('li'), sp = document.createElement('span'), b = document.createElement('button');
      sp.id = 'idea-' + i; sp.textContent = h.replace(/\{A\}/g, aud).replace(/\{Y\}/g, y);
      b.type = 'button'; b.className = 'btn btn-ghost btn-sm'; b.textContent = 'Copy';
      b.addEventListener('click', function () { if (window.MI) MI.copy(sp.textContent, b); var t = document.getElementById('wf-topic'); if (t && !t.value) t.value = sp.textContent; });
      li.appendChild(sp); li.appendChild(b); out.appendChild(li);
    });
  });
  var boxes = document.querySelectorAll('#checklist input'), score = document.getElementById('ck-score'), meter = document.getElementById('ck-meter');
  function tally() {
    var n = 0; boxes.forEach(function (b) { if (b.checked) n++; });
    score.textContent = n + ' / ' + boxes.length;
    meter.style.width = (n / boxes.length * 100) + '%';
    if (n === boxes.length && window.MI) MI.confetti(120);
  }
  boxes.forEach(function (b) { b.addEventListener('change', tally); });
});
</script>
<?php page_end();
