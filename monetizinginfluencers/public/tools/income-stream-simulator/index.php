<?php
require __DIR__ . '/../_common.php';

$slug = 'income-stream-simulator';
$name = 'Income Stream Simulator';
$desc = 'Free creator income simulator: mix brand deals, affiliate links, ad revenue, digital products, memberships and UGC to model your monthly influencer income.';

page_start([
    'title' => 'Creator Income Stream Simulator | Free Tool',
    'description' => $desc,
    'path' => '/tools/' . $slug . '/',
    'extra_css' => ['/assets/css/tools.css'],
    'extra_js' => ['/assets/js/tools/simulator.js'],
    'schema' => [tool_schema($slug, $name, $desc)],
]);

page_hero(
    'Free tool · diversify your income',
    'Creator Income <span class="grad-text">Stream Simulator</span>',
    'The highest-earning creators never rely on one income stream. Drag the sliders to build your own mix and see your monthly income, yearly total and how diversified (and safe) it really is.',
    [['Free Tools', '/tools/'], [$name, '/tools/' . $slug . '/']]
);

$groups = [
    ['brand', 'Brand deals', '#29b6f6', [['brand_n', 'Deals per month', 0, 12, 1, 2, ''], ['brand_r', 'Average rate per deal', 0, 5000, 50, 400, '$']]],
    ['aff', 'Affiliate links', '#8b5cf6', [['aff_c', 'Link clicks per month', 0, 50000, 250, 3000, ''], ['aff_cv', 'Conversion rate', 0, 10, 0.1, 3, '%'], ['aff_cm', 'Commission per sale', 0, 100, 1, 6, '$']]],
    ['ads', 'Ad revenue', '#ff3d9a', [['ads_v', 'Monetized views per month', 0, 5000000, 10000, 200000, ''], ['ads_rpm', 'RPM (earnings per 1,000 views)', 0, 30, 0.5, 3, '$']]],
    ['prod', 'Digital products', '#ffcc33', [['prod_s', 'Sales per month', 0, 1000, 5, 20, ''], ['prod_p', 'Price', 0, 300, 1, 29, '$']]],
    ['mem', 'Memberships', '#2ee59d', [['mem_n', 'Paying members', 0, 5000, 10, 50, ''], ['mem_p', 'Monthly price', 0, 50, 1, 5, '$']]],
    ['ugc', 'UGC videos', '#ff8a3d', [['ugc_n', 'Videos per month', 0, 30, 1, 2, ''], ['ugc_r', 'Rate per video', 0, 1500, 25, 200, '$']]],
];
?>
<section class="section" style="padding-top:10px">
  <div class="wrap tool-shell">
    <form class="tool-panel" id="sim-form" onsubmit="return false">
      <h2>Your income mix</h2>
      <div class="seg" role="group" aria-label="Presets" style="margin-bottom:16px">
        <button type="button" data-preset="starter" aria-pressed="true">Starter</button>
        <button type="button" data-preset="growing" aria-pressed="false">Growing</button>
        <button type="button" data-preset="pro" aria-pressed="false">Pro</button>
        <button type="button" data-preset="zero" aria-pressed="false">Clear</button>
      </div>
<?php foreach ($groups as [$key, $label, $color, $fields]): ?>
      <div class="sim-group" data-group="<?= $key ?>">
        <h3><i style="background:<?= $color ?>"></i><?= e($label) ?><b id="g-<?= $key ?>">$0</b></h3>
<?php foreach ($fields as [$id, $fl, $min, $max, $step, $val, $unit]): ?>
        <div class="range-row"><div class="top"><label for="<?= $id ?>"><?= e($fl) ?></label><output id="<?= $id ?>-o" data-unit="<?= $unit ?>"></output></div><input id="<?= $id ?>" type="range" min="<?= $min ?>" max="<?= $max ?>" step="<?= $step ?>" value="<?= $val ?>"></div>
<?php endforeach; ?>
      </div>
<?php endforeach; ?>
    </form>

    <div class="tool-panel tool-output gradient-border" aria-live="polite">
      <p class="small" style="margin:0">Estimated monthly income</p>
      <div class="big-num" id="sim-month">$0</div>
      <p class="small">That is <strong id="sim-year">$0</strong> a year (estimate).</p>
      <div class="donut-wrap">
        <div class="donut-center">
          <svg class="donut" viewBox="0 0 200 200" id="sim-donut" aria-hidden="true"><circle cx="100" cy="100" r="80" stroke="rgba(255,255,255,.07)"></circle></svg>
          <div class="lbl"><span><span id="sim-streams">0</span> streams<small>active</small></span></div>
        </div>
        <ul class="legend" id="sim-legend"></ul>
      </div>
      <p class="small" style="margin:0">Diversification score</p>
      <div class="score-bar"><div class="meter"><i id="sim-meter"></i></div><b id="sim-score" style="font-family:var(--font-d)">0/100</b></div>
      <p class="verdict" id="sim-verdict"></p>
      <p class="disclaimer">Estimates only. Ad RPMs, conversion rates and commissions vary widely by platform, niche and country.</p>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap narrow prose">
    <h2 id="how-it-works">How the simulator works</h2>
    <p>Each income stream is a simple, transparent formula. Nothing is hidden, so you can sanity-check every number against your own analytics:</p>
    <div class="table-scroll"><table>
      <thead><tr><th>Stream</th><th>Formula</th><th>Typical starting range</th></tr></thead>
      <tbody>
        <tr><td>Brand deals</td><td>deals per month × average rate</td><td>$100-$1,000 per deal for micro creators</td></tr>
        <tr><td>Affiliate</td><td>clicks × conversion rate × commission per sale</td><td>1-5% conversion, $2-$50 commission</td></tr>
        <tr><td>Ad revenue</td><td>monetized views ÷ 1,000 × RPM</td><td>$1-$5 RPM for most niches, higher for finance and tech</td></tr>
        <tr><td>Digital products</td><td>sales × price</td><td>$9-$99 guides, presets, templates, courses</td></tr>
        <tr><td>Memberships</td><td>paying members × monthly price</td><td>$3-$15 per month</td></tr>
        <tr><td>UGC</td><td>videos × rate per video</td><td>$100-$500 per video, no posting required</td></tr>
      </tbody>
    </table></div>
    <p>The <strong>diversification score</strong> measures how evenly your income is spread. It uses a normalised Herfindahl index: if 100% of your income comes from one stream the score is 0, and if it is spread perfectly evenly across all six streams the score is 100. A score above 60 means losing any single stream would hurt, but would not end your business.</p>

    <h2>Why diversification matters for creators</h2>
    <p>Platform payouts change, algorithms shift and brand budgets shrink in a bad quarter. Creators who earn only from sponsorships feel every dip. Creators who also earn from affiliate links, a digital product and a small membership keep getting paid between deals, and their owned income (products, memberships, email list) grows in value over time.</p>
    <p>A practical path for most creators: start with <strong>affiliate links and UGC</strong> (no minimum audience), add <strong>brand deals</strong> once you have an engaged niche audience, then launch a <strong>digital product</strong> that solves the question your followers ask most. Use the presets to see how each stage changes the picture.</p>

    <h2>Example: from $850 to $7,400 a month</h2>
    <p>The Starter preset models a newer creator with one brand deal, a few affiliate sales, some ad revenue and two UGC videos: roughly $850 a month, heavily weighted toward brand work. The Growing preset adds more deals at a higher rate, a $29 digital product and a small membership. Total income rises to around $7,400, and just as importantly, no single stream is more than about half of it. That is the shift from side hustle to resilient creator business.</p>
    <h2>Tips to grow each stream</h2>
    <ul>
      <li><strong>Brand deals:</strong> raise your rate with a strong engagement rate and a professional <a href="/tools/media-kit-builder/">media kit</a>.</li>
      <li><strong>Affiliate:</strong> put links where intent is high: tutorials, comparisons and "what I use" pages. See the <a href="/affiliate-marketing-for-influencers/">affiliate marketing playbook</a>.</li>
      <li><strong>Ad revenue:</strong> longer YouTube videos and evergreen topics earn the best RPMs.</li>
      <li><strong>Products and memberships:</strong> a website you own converts better than link-in-bio pages. Monetizing Influencers builds <a href="/website-design/">money sites for creators</a>.</li>
    </ul>
  </div>
</section>

<?php
faq_block([
    ['How many income streams should an influencer have?', '<p>Three to four active streams is a healthy target for most full-time creators. It is enough to smooth out bad months without spreading yourself too thin.</p>'],
    ['What is a good RPM for creators?', '<p>Many YouTube channels see $1-$5 per 1,000 monetized views, while finance, business and tech channels can earn $10 or more. Short-form video usually pays far less per view.</p>'],
    ['Which income stream is easiest to start?', '<p>Affiliate marketing and UGC have no follower minimums, so they are the easiest first streams. Take the <a href="/tools/monetization-readiness-quiz/">monetization readiness quiz</a> for a personalised recommendation.</p>'],
]);
more_tools($slug);
cta_band('Build a business, not a side hustle', 'Monetizing Influencers helps creators plan, launch and grow every income stream in this simulator.');
page_end();
