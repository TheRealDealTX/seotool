<?php
require __DIR__ . '/../inc/blog.php';

blog_post_start([
    'path' => '/how-much-should-influencers-charge/',
    'description' => 'How much should influencers charge? Estimated 2026 rates by platform and follower tier, the pricing formula brands use, and how to build a rate card.',
    'h1' => 'How Much Should Influencers Charge? <span class="grad-text">2026 Rate Guide</span>',
    'lead' => 'Per-post rate ranges by platform and follower tier, the formula behind them, and how to raise your rates without losing the brands you already work with.',
    'read' => 10,
]);
?>
<p><strong>How much should influencers charge</strong> for a sponsored post? There is no official price list, which is exactly why so many creators undercharge. Rates are negotiated deal by deal, but they follow patterns: follower count sets a baseline, engagement and niche move it up or down, and extras like usage rights and exclusivity can double the final number.</p>
<p>This guide gives you estimated ranges for each platform and tier, the simple formula most brands and agencies start from, and a step-by-step way to build your own rate card. Want a personalised number right now? Use the mini calculator below or the full <a href="/tools/influencer-earnings-calculator/">influencer earnings calculator</a>.</p>

<div class="callout"><?= icon('shield') ?><p><strong>About these numbers:</strong> every range on this page is an estimate based on commonly cited industry benchmarks, not a guarantee. Real rates vary widely by niche, region, audience quality and the brand's budget. Treat them as a starting point for negotiation.</p></div>

<h2 id="tiers">Influencer tiers explained</h2>
<p>Brands and agencies group creators into tiers by audience size. Knowing your tier tells you which rate bracket you are being compared against.</p>
<div class="tier-bars reveal">
  <div class="tier-bar"><b>Nano</b><span class="track"><i style="width:12%"></i></span><small>1K - 10K followers</small></div>
  <div class="tier-bar"><b>Micro</b><span class="track"><i style="width:30%"></i></span><small>10K - 100K</small></div>
  <div class="tier-bar"><b>Mid-tier</b><span class="track"><i style="width:52%"></i></span><small>100K - 500K</small></div>
  <div class="tier-bar"><b>Macro</b><span class="track"><i style="width:74%"></i></span><small>500K - 1M</small></div>
  <div class="tier-bar"><b>Mega</b><span class="track"><i style="width:100%"></i></span><small>1M+</small></div>
</div>
<p>Smaller tiers usually have higher engagement and tighter-knit communities, which is why micro-influencers are so popular with brands: they often deliver more trust per dollar. Bigger tiers sell reach and cultural visibility.</p>

<h2 id="rates">Estimated rates by platform</h2>
<p>The table below shows typical starting ranges for a single sponsored deliverable. Estimates only; strong engagement or a high-value niche can push you well above them.</p>
<div class="table-scroll"><table>
  <thead><tr><th>Tier</th><th>Instagram (post/Reel)</th><th>TikTok (video)</th><th>YouTube (integration)</th><th>Facebook (post)</th><th>Pinterest (pin set)</th></tr></thead>
  <tbody>
    <tr><td><strong>Nano</strong> 1K-10K</td><td>$10 - $100</td><td>$5 - $75</td><td>$20 - $200</td><td>$10 - $60</td><td>$10 - $50</td></tr>
    <tr><td><strong>Micro</strong> 10K-100K</td><td>$100 - $1,000</td><td>$75 - $700</td><td>$200 - $2,000</td><td>$60 - $600</td><td>$50 - $500</td></tr>
    <tr><td><strong>Mid-tier</strong> 100K-500K</td><td>$1,000 - $5,000</td><td>$700 - $3,500</td><td>$2,000 - $10,000</td><td>$600 - $3,000</td><td>$500 - $2,500</td></tr>
    <tr><td><strong>Macro</strong> 500K-1M</td><td>$5,000 - $10,000</td><td>$3,500 - $7,000</td><td>$10,000 - $20,000</td><td>$3,000 - $6,000</td><td>$2,500 - $5,000</td></tr>
    <tr><td><strong>Mega</strong> 1M+</td><td>$10,000+</td><td>$7,000+</td><td>$20,000+</td><td>$6,000+</td><td>$5,000+</td></tr>
  </tbody>
</table></div>
<p>YouTube commands the highest rates because videos are long, searchable and keep earning views for years. TikTok rates per follower are often lower because follower counts there grow faster and views swing more from video to video, so many brands price TikTok on average views instead.</p>

<h2 id="formula">The basic pricing formula</h2>
<p>Most negotiations start from a simple rule of thumb, then adjust:</p>
<div class="formula">Base rate = <em>(followers ÷ 1,000) × benchmark CPM</em> × engagement multiplier + extras</div>
<ul>
  <li><strong>Benchmark per 1,000 followers:</strong> roughly $10 on Instagram, $20 per 1,000 subscribers for a YouTube integration, and $5-$10 on TikTok, Facebook and Pinterest.</li>
  <li><strong>Engagement multiplier:</strong> around 1.0 at an average engagement rate (about 3% on Instagram). Push it up to 1.5-2x if you are well above average, down if you are below.</li>
  <li><strong>Extras:</strong> usage rights, exclusivity, whitelisting and extra deliverables are priced on top (see below).</li>
</ul>
<p>For video-first platforms, many brands prefer a <strong>view-based</strong> price: average views from your last 10-15 videos ÷ 1,000 × a CPM (often $15-$40 depending on niche). Pricing on views protects you when a big account has quiet weeks, and rewards you when your views outpace your follower count.</p>

<div class="glass-panel mini-calc" id="mini-calc">
  <h3>Quick rate estimator</h3>
  <div class="row">
    <div class="field"><label for="mc-f">Followers</label><input id="mc-f" type="number" min="500" step="500" value="25000"></div>
    <div class="field"><label for="mc-e">Engagement %</label><input id="mc-e" type="number" min="0.1" max="30" step="0.1" value="3"></div>
    <div class="field"><label for="mc-p">Platform</label><select id="mc-p"><option value="10">Instagram</option><option value="7">TikTok</option><option value="20">YouTube</option><option value="6">Facebook</option><option value="5">Pinterest</option></select></div>
  </div>
  <p class="small" style="margin:14px 0 0">Estimated starting rate per sponsored post</p>
  <div class="big-num" id="mc-out">$250</div>
  <p class="small" id="mc-range"></p>
  <a class="btn btn-glow btn-sm" href="/tools/influencer-earnings-calculator/">Get a detailed estimate <?= icon('arrow') ?></a>
</div>

<h2 id="other-deliverables">Pricing other deliverables</h2>
<p>Brands rarely buy a single feed post anymore. Here is how creators commonly price other deliverables relative to their base rate (the price of one main post or video):</p>
<div class="table-scroll"><table>
  <thead><tr><th>Deliverable</th><th>Typical price vs. base rate</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Instagram Story (per frame)</td><td>20% - 40%</td><td>Often sold in sets of 3 with a link sticker</td></tr>
    <tr><td>Reel / TikTok video</td><td>100% - 150%</td><td>More production time than a static post</td></tr>
    <tr><td>YouTube dedicated video</td><td>2x - 3x an integration</td><td>The whole video is about the brand</td></tr>
    <tr><td>Link in bio (per week or month)</td><td>10% - 30%</td><td>Add-on to a content package</td></tr>
    <tr><td>UGC (not posted on your account)</td><td>Flat fee per asset</td><td>Priced on production, not audience size</td></tr>
    <tr><td>Usage rights / whitelisting</td><td>+20% - 50% per month</td><td>Or a separate monthly licence fee</td></tr>
  </tbody>
</table></div>
<p class="small">Estimates for planning purposes; adjust for your niche and demand.</p>

<h2 id="factors">Factors that raise (or lower) your rate</h2>
<div class="card-grid cols-2">
  <div class="card"><span class="ico-badge"><?= icon('heart') ?></span><h3>Engagement rate</h3><p>High engagement signals a real, attentive audience. It is the single biggest reason two creators with the same following charge very different rates.</p></div>
  <div class="card"><span class="ico-badge"><?= icon('dollar') ?></span><h3>Niche</h3><p>Finance, tech, B2B and luxury audiences are worth more to advertisers than broad entertainment, so creators there can charge a premium.</p></div>
  <div class="card"><span class="ico-badge"><?= icon('file') ?></span><h3>Usage rights</h3><p>If a brand wants to reuse your content on its own channels, website or ads, charge extra, commonly 20-50% per month of usage or more for perpetual rights.</p></div>
  <div class="card"><span class="ico-badge"><?= icon('shield') ?></span><h3>Exclusivity</h3><p>Agreeing not to work with competitors for a period costs you future deals. Price it in, often 15-50% depending on length and category breadth.</p></div>
  <div class="card"><span class="ico-badge"><?= icon('megaphone') ?></span><h3>Whitelisting / paid ads</h3><p>When a brand runs ads through your handle, it borrows your credibility. Charge a separate monthly fee on top of the content fee.</p></div>
  <div class="card"><span class="ico-badge"><?= icon('layout') ?></span><h3>Deliverables &amp; effort</h3><p>Scripting, travel, props, multiple revisions and raw footage all add hours. Each extra deliverable should add to the price.</p></div>
</div>

<h2 id="rate-card">How to build your rate card</h2>
<p>A rate card is a simple price list you can send the moment a brand asks "what are your rates?". It makes you look professional and anchors the negotiation at your number, not theirs.</p>
<ol>
  <li><strong>Calculate your base rate</strong> for your main deliverable with the formula above.</li>
  <li><strong>Price each format</strong> relative to that base: Stories are often 20-40% of a feed post, a Reel or TikTok 100-150%, a dedicated YouTube video 2-3x an integration.</li>
  <li><strong>Build two or three packages</strong>, for example "Starter: 1 Reel + 3 Stories" and "Launch: 2 Reels + 6 Stories + link in bio for 30 days". Packages lift the average deal size.</li>
  <li><strong>List add-ons</strong> separately: usage rights per month, whitelisting, exclusivity, raw footage, rush delivery.</li>
  <li><strong>Add your terms</strong>: payment timing (for example 50% upfront), number of revisions included and cancellation policy.</li>
</ol>
<p>Put your rate card on the last page of your media kit. Our <a href="/influencer-media-kit/">media kit guide</a> and free <a href="/tools/media-kit-builder/">media kit builder</a> show you how.</p>

<h2 id="negotiate">How to negotiate without losing the deal</h2>
<ul class="check-list">
  <li><strong>Ask for the budget first.</strong> "Do you have a budget in mind for this campaign?" Sometimes it is higher than your rate.</li>
  <li><strong>Trade scope, not price.</strong> If the budget is lower, remove a deliverable or usage rights instead of discounting the same work.</li>
  <li><strong>Show proof.</strong> Share results from past campaigns: clicks, saves, conversions, codes redeemed.</li>
  <li><strong>Offer a package.</strong> Three posts across a month often perform better for the brand and earns you more than one.</li>
  <li><strong>Get it in writing.</strong> Deliverables, dates, payment terms and usage, before you film anything.</li>
</ul>

<h2 id="raise-rates">When to raise your rates</h2>
<p>Review your rates every three to six months. Raise them when you grow a full tier, when engagement climbs, when brands say yes instantly (a sign you are too cheap), or when you are booked out. Existing partners can keep their old rate for one more campaign as a thank-you, then move to the new card. Most brands expect it: growing creators cost more.</p>
<p>Once you know your number, the next step is filling your calendar. Read <a href="/how-to-get-brand-deals/">how to get brand deals as a micro-influencer</a>, then use our <a href="/how-to-write-to-an-influencer/">outreach templates</a> to pitch.</p>

<script>
document.addEventListener('DOMContentLoaded', function () {
  var f = document.getElementById('mc-f'), en = document.getElementById('mc-e'), p = document.getElementById('mc-p');
  function upd() {
    var n = Math.max(0, +f.value || 0), er = Math.max(0.1, +en.value || 0.1), mult = Math.max(.4, Math.min(2, er / 3));
    var mid = n / 1000 * (+p.value) * mult;
    document.getElementById('mc-out').textContent = '$' + Math.round(Math.max(20, mid)).toLocaleString();
    document.getElementById('mc-range').textContent = 'Typical negotiation range: $' + Math.round(Math.max(15, mid * .75)).toLocaleString() + ' - $' + Math.round(Math.max(40, mid * 1.35)).toLocaleString() + ' (estimate, before usage rights and exclusivity)';
  }
  [f, en, p].forEach(function (el) { el.addEventListener('input', upd); });
  upd();
});
</script>
<?php
blog_post_end(
    [
        ['tiers', 'Influencer tiers'],
        ['rates', 'Rates by platform'],
        ['formula', 'The pricing formula'],
        ['other-deliverables', 'Other deliverables'],
        ['factors', 'What moves your rate'],
        ['rate-card', 'Build a rate card'],
        ['negotiate', 'Negotiate the deal'],
        ['raise-rates', 'When to raise rates'],
    ],
    [
        ['How much should an influencer with 10K followers charge?', '<p>A common starting point is around $100 per sponsored Instagram post at 10,000 followers, adjusted for engagement and niche. A creator with strong engagement in a valuable niche can reasonably charge more.</p>'],
        ['Do influencers charge per post or per campaign?', '<p>Both. Many creators quote a per-deliverable rate and then offer campaign packages that bundle several posts, Stories and link placements at a better combined price.</p>'],
        ['Should I charge extra for usage rights?', '<p>Yes. If a brand wants to reuse your content in its ads, website or emails, that is additional value. Charge a monthly or one-off usage fee on top of your content fee.</p>'],
        ['Is it OK to accept free products instead of payment?', '<p>Gifted collaborations can make sense when you are starting out or genuinely want the product, but they should not come with guaranteed deliverables. If a brand needs a guaranteed post, it should pay.</p>'],
    ],
    ['What are you worth?', 'Get a personalised rate estimate by platform, niche and engagement.', '/tools/influencer-earnings-calculator/', 'Try the calculator']
);
