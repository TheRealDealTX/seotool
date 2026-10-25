<?php
require __DIR__ . '/../_common.php';

$slug = 'influencer-earnings-calculator';
$name = 'Influencer Earnings Calculator';
$desc = 'Free influencer earnings calculator: estimate your sponsored post rate and monthly income on Instagram, TikTok, YouTube, Facebook and Pinterest.';

page_start([
    'title' => 'Influencer Earnings Calculator: Rate Per Post (Free)',
    'description' => $desc,
    'path' => '/tools/' . $slug . '/',
    'extra_css' => ['/assets/css/tools.css'],
    'extra_js' => ['/assets/js/tools/earnings.js'],
    'schema' => [tool_schema($slug, $name, $desc)],
]);

page_hero(
    'Free tool · influencer rate calculator',
    'Influencer <span class="grad-text">Earnings Calculator</span>',
    'How much do influencers make per post? Enter your platform, followers and engagement to estimate a fair sponsored post rate, plus your monthly and yearly earning potential.',
    [['Free Tools', '/tools/'], [$name, '/tools/' . $slug . '/']]
);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap tool-shell" id="calc">
    <form class="tool-panel" id="ec-form" onsubmit="return false">
      <h2>Your channel</h2>
      <div class="field"><label for="ec-platform">Platform</label>
        <select id="ec-platform">
          <option value="instagram">Instagram</option><option value="tiktok">TikTok</option><option value="youtube">YouTube</option><option value="facebook">Facebook</option><option value="pinterest">Pinterest</option>
        </select></div>
      <div class="field num-with-range">
        <label for="ec-followers"><span id="ec-flabel">Followers</span></label>
        <input id="ec-followers" type="number" min="100" max="50000000" step="100" value="25000" inputmode="numeric">
        <input id="ec-fslider" type="range" min="0" max="100" step="0.1" aria-label="Followers slider">
      </div>
      <div class="field">
        <span class="sr-only" id="ec-emode-l">Engagement input method</span>
        <div class="mode-toggle" role="group" aria-labelledby="ec-emode-l">
          <button type="button" data-emode="rate" aria-pressed="true">I know my engagement rate</button>
          <button type="button" data-emode="counts" aria-pressed="false">Use average likes &amp; comments</button>
        </div>
        <div id="ec-rate-box" class="range-row"><div class="top"><label for="ec-er">Average engagement rate</label><output id="ec-er-o">3.0%</output></div><input id="ec-er" type="range" min="0.2" max="15" step="0.1" value="3"></div>
        <div id="ec-count-box" class="inline-pair" hidden>
          <div><label for="ec-likes" id="ec-likes-l">Avg likes per post</label><input id="ec-likes" type="number" min="0" value="700"></div>
          <div><label for="ec-comments">Avg comments per post</label><input id="ec-comments" type="number" min="0" value="45"></div>
        </div>
      </div>
      <div class="inline-pair">
        <div class="field"><label for="ec-niche">Niche</label>
          <select id="ec-niche">
            <option value="1.35">Finance / investing</option><option value="1.3">Tech / software</option><option value="1.3">Business / B2B</option>
            <option value="1.1">Beauty / skincare</option><option value="1.1" selected>Fashion</option><option value="1.1">Fitness / health</option><option value="1.1">Travel</option><option value="1.05">Food / cooking</option><option value="1.05">Parenting / family</option>
            <option value="1">Lifestyle</option><option value="0.9">Gaming</option><option value="0.85">Entertainment / comedy</option>
          </select></div>
        <div class="field"><label for="ec-type">Content type</label><select id="ec-type"></select></div>
      </div>
      <div class="range-row"><div class="top"><label for="ec-posts">Sponsored posts per month</label><output id="ec-posts-o">2</output></div><input id="ec-posts" type="range" min="0" max="20" step="1" value="2"></div>
      <div class="inline-pair">
        <div class="field"><label for="ec-aff">Affiliate sales / month <span class="hint">(optional)</span></label><input id="ec-aff" type="number" min="0" value="0"></div>
        <div class="field"><label for="ec-comm">Avg commission per sale ($)</label><input id="ec-comm" type="number" min="0" step="0.5" value="8"></div>
      </div>
    </form>

    <div class="tool-panel tool-output gradient-border" aria-live="polite">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap">
        <p class="small" style="margin:0">Estimated rate per sponsored post</p>
        <span class="tier-badge" id="ec-tier"><?= icon('star') ?> <span>Micro-influencer</span></span>
      </div>
      <div class="big-num" id="ec-rate">$0</div>
      <p class="small" id="ec-mid">Suggested asking price: $0</p>
      <div class="out-grid">
        <div class="out-box"><small>Monthly estimate</small><b id="ec-month">$0</b></div>
        <div class="out-box"><small>Yearly estimate</small><b id="ec-year">$0</b></div>
      </div>
      <p class="small" style="margin:0">Same audience, rate per post on each platform</p>
      <div class="bars-chart" id="ec-bars" aria-hidden="true"></div>
      <ul class="result-rows" id="ec-break"></ul>
      <p class="disclaimer">All figures are estimates based on public industry benchmarks, not guaranteed earnings. Real offers vary with usage rights, exclusivity, deliverables and brand budget.</p>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap narrow prose">
    <h2 id="how-it-works">How this influencer rate calculator works</h2>
    <p>There is no official price list for sponsored content, so brands and agencies price creators from benchmarks. This influencer earnings calculator starts from the most commonly cited ones and adjusts them for the things that actually change what a brand will pay.</p>
    <div class="table-scroll"><table>
      <thead><tr><th>Platform</th><th>Starting benchmark</th><th>"Average" engagement used</th></tr></thead>
      <tbody>
        <tr><td>Instagram</td><td>$10 per 1,000 followers (feed post)</td><td>3%</td></tr>
        <tr><td>TikTok</td><td>$7 per 1,000 followers (video)</td><td>5%</td></tr>
        <tr><td>YouTube</td><td>$20 per 1,000 subscribers (60-90s integration)</td><td>4% (likes + comments vs subscribers)</td></tr>
        <tr><td>Facebook</td><td>$6 per 1,000 followers (post)</td><td>1.5%</td></tr>
        <tr><td>Pinterest</td><td>$5 per 1,000 followers (Pin)</td><td>1%</td></tr>
      </tbody>
    </table></div>
    <p>The formula is: <strong>followers ÷ 1,000 × platform benchmark × engagement multiplier × niche multiplier × content-type multiplier</strong>. The engagement multiplier compares your rate with the platform average (capped between 0.5x and 2.2x, with diminishing returns), so a creator with double the average engagement earns noticeably more, but not infinitely more. Niche multipliers run from 0.85x (entertainment) to 1.35x (finance), reflecting how much advertisers in each category pay per customer. Content-type multipliers price a Story below a feed post and a dedicated YouTube video at a little over twice an integration.</p>
    <p>The range shown is 75% to 135% of that midpoint, and no rate falls below a $50 floor. Monthly earnings multiply the midpoint by your sponsored posts per month and add any affiliate commission you enter. Yearly is simply monthly × 12.</p>

    <h2>How to read your results</h2>
    <p>Quote near the <strong>top</strong> of the range when the brand wants usage rights (running your content as ads), exclusivity in your category, a fast turnaround, or a package of several posts. Quote near the <strong>bottom</strong> for a first collaboration with a brand you genuinely want in your portfolio, or when the product itself is high value. Never go below the range without getting something tangible in return, such as a long-term contract or affiliate commission on top.</p>
    <p>The bar chart compares what the same audience size would earn on every platform. It is a useful gut check when deciding where to grow next: YouTube integrations usually pay the most per follower because videos keep earning views for months, while Stories and Pins pay less per piece but are faster to produce.</p>

    <h2>How much do influencers make, really?</h2>
    <p>Per-post rates are only half of the answer. Most full-time creators earn from several streams at once: brand deals, affiliate commission, platform ad revenue and their own products. A micro-influencer doing two sponsored posts a month at $400 earns about $800, but adding affiliate links and a small digital product can double that without more brand work. Model the full picture with the <a href="/tools/income-stream-simulator/">income stream simulator</a>, and read the <a href="/how-much-should-influencers-charge/">influencer rate guide</a> for negotiation scripts.</p>
    <div class="callout"><?= icon('zap') ?><p><strong>Tip from Monetizing Influencers:</strong> brands will ask for your engagement rate. Calculate it precisely across your last 10 posts with the <a href="/tools/engagement-rate-calculator/">engagement rate calculator</a> and put it in your <a href="/tools/media-kit-builder/">media kit</a>.</p></div>
  </div>
</section>

<?php
faq_block([
    ['How much do influencers make per post?', '<p>As a rough benchmark, Instagram creators charge around $10 per 1,000 followers for a feed post, so a 25K-follower account would start near $250. TikTok tends to be a little lower per follower and YouTube integrations higher. Engagement, niche and usage rights move the number up or down.</p>'],
    ['Is this influencer rate calculator accurate?', '<p>It gives a reasoned starting range, not a guarantee. Rates are private and negotiated, so we use public industry benchmarks and show every assumption in the "How it works" section above.</p>'],
    ['Should I charge more for usage rights?', '<p>Yes. If a brand wants to run your content as paid ads or on its own channels, add 20-50% (or more for long terms and exclusivity). Usage rights are one of the most common reasons creators undercharge.</p>'],
    ['Do micro-influencers get paid?', '<p>Yes. Micro-influencers (10K-100K followers) are in high demand because their engagement is usually stronger. Many brands prefer five micro-influencers to one celebrity.</p>'],
]);
more_tools($slug);
cta_band('Turn your rate into a real offer', 'Monetizing Influencers can help you package your numbers, build a rate card and pitch the brands that fit your audience.');
page_end();
