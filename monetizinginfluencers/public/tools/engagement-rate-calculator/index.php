<?php
require __DIR__ . '/../_common.php';

$slug = 'engagement-rate-calculator';
$name = 'Engagement Rate Calculator';
$desc = 'Free engagement rate calculator for Instagram, TikTok, YouTube, Facebook and Pinterest. Average up to 10 posts and compare with benchmarks for your tier.';

page_start([
    'title' => 'Engagement Rate Calculator for Influencers (Free)',
    'description' => $desc,
    'path' => '/tools/' . $slug . '/',
    'extra_css' => ['/assets/css/tools.css'],
    'extra_js' => ['/assets/js/tools/engagement.js'],
    'schema' => [tool_schema($slug, $name, $desc)],
]);

page_hero(
    'Free tool · engagement benchmarks',
    'Engagement Rate <span class="grad-text">Calculator</span>',
    'Calculate your true engagement rate by followers and by reach, averaged across up to 10 posts, then see exactly how it stacks up against creators your size on the same platform.',
    [['Free Tools', '/tools/'], [$name, '/tools/' . $slug . '/']]
);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap tool-shell">
    <form class="tool-panel" id="er-form" onsubmit="return false">
      <h2>Your posts</h2>
      <div class="inline-pair">
        <div class="field"><label for="er-platform">Platform</label>
          <select id="er-platform"><option value="instagram">Instagram</option><option value="tiktok">TikTok</option><option value="youtube">YouTube</option><option value="facebook">Facebook</option><option value="pinterest">Pinterest</option></select></div>
        <div class="field"><label for="er-followers">Followers / subscribers</label><input id="er-followers" type="number" min="1" value="18500" inputmode="numeric"></div>
      </div>
      <p class="small">Enter the numbers for your recent posts. Reach / views is optional and powers the reach-based rate.</p>
      <div class="row-head" aria-hidden="true"><span>#</span><span>Likes</span><span>Comments</span><span>Shares + saves</span><span>Reach / views</span><span></span></div>
      <div class="post-rows" id="er-rows"></div>
      <div class="btn-row">
        <button type="button" class="btn btn-ghost btn-sm" id="er-add"><?= icon('sparkles') ?> Add post</button>
        <button type="button" class="btn btn-ghost btn-sm" id="er-sample">Fill sample data</button>
      </div>
    </form>

    <div class="tool-panel tool-output gradient-border" aria-live="polite">
      <p class="small" style="margin:0">Engagement rate by followers (average of <span id="er-n">0</span> posts)</p>
      <div class="big-num" id="er-rate">0.00%</div>
      <svg class="gauge" viewBox="0 0 320 200" role="img" aria-labelledby="er-gauge-t">
        <title id="er-gauge-t">Engagement gauge compared with benchmark</title>
        <defs><linearGradient id="gaugeGrad" x1="0" x2="1"><stop offset="0" stop-color="#ff3d9a"/><stop offset=".5" stop-color="#8b5cf6"/><stop offset="1" stop-color="#2ee59d"/></linearGradient></defs>
        <path class="track" d="M30 170 A130 130 0 0 1 290 170"/>
        <path class="val" id="er-arc" d="M30 170 A130 130 0 0 1 290 170" stroke-dasharray="408.4" stroke-dashoffset="408.4"/>
        <g class="needle" id="er-needle" style="transform:rotate(-90deg)"><line x1="160" y1="170" x2="160" y2="62" stroke="#fff" stroke-width="4" stroke-linecap="round"/><circle cx="160" cy="170" r="10" fill="#fff"/></g>
        <text x="24" y="192">Low</text><text x="146" y="28" id="er-bench-t">Avg</text><text x="268" y="192">High</text>
      </svg>
      <div class="gauge-read"><span class="tier-badge" id="er-badge">Average</span></div>
      <div class="out-grid">
        <div class="out-box"><small>Rate by reach / views</small><b id="er-reach">-</b></div>
        <div class="out-box"><small>Benchmark for your tier</small><b id="er-bench">-</b></div>
        <div class="out-box"><small>Avg interactions / post</small><b id="er-avg">0</b></div>
        <div class="out-box"><small>Your tier</small><b id="er-tier" style="font-size:1.05rem">-</b></div>
      </div>
      <p class="verdict" id="er-verdict">Add your posts to see how you compare.</p>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap narrow prose">
    <h2 id="how-it-works">How engagement rate is calculated</h2>
    <p>Engagement rate measures how many people actively interact with your content compared with how many could have seen it. This calculator gives you both standard versions:</p>
    <ul>
      <li><strong>Engagement rate by followers</strong> = (likes + comments + shares + saves) ÷ followers × 100, averaged across your posts. This is the number most brands and media kits use because anyone can check it.</li>
      <li><strong>Engagement rate by reach (or views)</strong> = total interactions ÷ total reach × 100. It is usually higher and more honest about how compelling your content is, because it ignores followers who never saw the post. Pull reach from Instagram Insights, TikTok Analytics or YouTube Studio.</li>
    </ul>
    <p>Averaging at least 5-10 recent posts matters. One viral post can make a single-post rate look three times better than reality, and brands that dig into your profile will notice the gap.</p>

    <h2>Engagement benchmarks by platform and tier</h2>
    <p>Engagement naturally falls as accounts grow, so a 1% rate can be excellent for a mega-influencer and weak for a nano creator. The gauge compares you with these approximate benchmarks (engagement by followers), compiled from public industry reports. They are rounded starting points, not hard rules.</p>
    <div class="table-scroll"><table>
      <thead><tr><th>Platform</th><th>Nano &lt;10K</th><th>Micro 10-100K</th><th>Mid 100-500K</th><th>Macro 500K-1M</th><th>Mega 1M+</th></tr></thead>
      <tbody>
        <tr><td>Instagram</td><td>4.0%</td><td>2.5%</td><td>1.6%</td><td>1.2%</td><td>1.0%</td></tr>
        <tr><td>TikTok</td><td>9.0%</td><td>6.5%</td><td>5.0%</td><td>4.5%</td><td>4.0%</td></tr>
        <tr><td>YouTube</td><td>4.0%</td><td>2.5%</td><td>1.8%</td><td>1.5%</td><td>1.2%</td></tr>
        <tr><td>Facebook</td><td>1.5%</td><td>0.8%</td><td>0.5%</td><td>0.4%</td><td>0.3%</td></tr>
        <tr><td>Pinterest</td><td>1.5%</td><td>1.0%</td><td>0.7%</td><td>0.5%</td><td>0.4%</td></tr>
      </tbody>
    </table></div>
    <p>The gauge runs from zero to three times your benchmark. Below half the benchmark reads as low, around the benchmark is healthy, and anything above 2x is exceptional and worth highlighting in every pitch.</p>

    <p>Brands increasingly ask for screenshots of your analytics, so report the same method every time and say which one you used.</p>
    <h2>How to improve your engagement rate</h2>
    <ul>
      <li><strong>Ask a specific question.</strong> "Which one would you pick, A or B?" earns more comments than "Thoughts?"</li>
      <li><strong>Make content worth saving.</strong> Checklists, tutorials and carousels drive saves and shares, which most algorithms weight heavily.</li>
      <li><strong>Reply in the first hour.</strong> Early conversation signals that a post is worth pushing to more people.</li>
      <li><strong>Prune inactive followers carefully.</strong> Giveaway and follow-for-follow audiences drag your rate down permanently.</li>
      <li><strong>Post less, but better.</strong> Three strong posts a week usually beat seven rushed ones.</li>
    </ul>
    <div class="callout"><?= icon('zap') ?><p>Engagement is the biggest lever on your rate. Plug your new number into the <a href="/tools/influencer-earnings-calculator/">influencer earnings calculator</a> to see what it is worth, and add it to your <a href="/tools/media-kit-builder/">media kit</a>. More growth tactics are in the Monetizing Influencers <a href="/social-platforms/">platform playbooks</a>.</p></div>
  </div>
</section>

<?php
faq_block([
    ['What is a good engagement rate?', '<p>It depends on platform and audience size. On Instagram, 1-3% is typical for most accounts and above 3% is strong for micro-influencers. TikTok rates run higher, often 4-9%. Compare yourself with creators of a similar size using the benchmark table above.</p>'],
    ['Should I count saves and shares?', '<p>Yes. Saves and shares are high-intent interactions and many brands value them more than likes. If you only have likes and comments, enter zero in the shares + saves column.</p>'],
    ['Why is my reach-based rate higher?', '<p>Reach only counts people who actually saw the post, while follower-based rates include inactive followers. Reach-based rates are typically 1.5-3x higher.</p>'],
    ['How many posts should I average?', '<p>Use your last 5-10 regular posts. Leave out giveaways and paid boosts, which inflate results and will not match what brands see on a normal post.</p>'],
]);
more_tools($slug);
cta_band('Got great engagement? Get paid for it.', 'Monetizing Influencers helps creators turn strong engagement into higher rates and better brand partnerships.');
page_end();
