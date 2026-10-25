<?php
require __DIR__ . '/_common.php';

$items = [];
$i = 0;
foreach (tool_list() as $slug => [$ic, $name, $txt]) {
    $items[] = ['@type' => 'ListItem', 'position' => ++$i, 'url' => SITE_URL . '/tools/' . $slug . '/', 'name' => $name];
}

page_start([
    'title' => 'Free Influencer Tools & Calculators | Monetizing Influencers',
    'description' => 'Free influencer tools: earnings and rate calculator, engagement rate calculator, email generator, media kit builder, income simulator and readiness quiz.',
    'path' => '/tools/',
    'extra_css' => ['/assets/css/tools.css'],
    'schema' => [[
        '@type' => 'CollectionPage',
        'name' => 'Free Influencer Tools & Calculators',
        'url' => SITE_URL . '/tools/',
        'isPartOf' => ['@id' => SITE_URL . '/#website'],
        'mainEntity' => ['@type' => 'ItemList', 'numberOfItems' => count($items), 'itemListElement' => $items],
    ]],
]);

page_hero(
    'Free creator tools',
    'Free Influencer Tools <span class="grad-text">&amp; Calculators</span>',
    'Six free tools that answer the questions every creator asks: what am I worth, is my engagement good, what do I say to brands, and which income stream should I start with? No sign-up, no paywall, instant results.',
    [['Free Tools', '/tools/']],
    '<div class="btn-row reveal" style="margin-top:22px"><a class="btn btn-glow btn-lg magnetic" href="/tools/influencer-earnings-calculator/">' . icon('calc') . ' Start with the earnings calculator</a></div>'
);

$tags = [
    'influencer-earnings-calculator' => ['Rate per post', 'Monthly income', '5 platforms'],
    'engagement-rate-calculator'     => ['By followers', 'By reach', 'Benchmarks'],
    'influencer-email-generator'     => ['Brand outreach', 'Creator pitch', 'DM version'],
    'media-kit-builder'              => ['Live preview', 'Print to PDF', 'Saves locally'],
    'income-stream-simulator'        => ['6 income streams', 'Donut chart', 'Presets'],
    'monetization-readiness-quiz'    => ['10 questions', 'Score', 'Next steps'],
];
?>
<section class="section" style="padding-top:20px">
  <div class="wrap">
    <div class="tool-hero-cards">
<?php $n = 0; foreach (tool_list() as $slug => [$ic, $name, $txt]): $n++; ?>
      <article class="card tool-big tilt reveal">
        <a href="/tools/<?= $slug ?>/">
          <span class="num" aria-hidden="true">0<?= $n ?></span>
          <span class="ico-badge"><?= icon($ic) ?></span>
          <h2><?= e($name) ?></h2>
          <div class="tags"><?php foreach ($tags[$slug] as $t): ?><span><?= e($t) ?></span><?php endforeach; ?></div>
          <p><?= e($txt) ?></p>
          <span class="more">Open the tool <?= icon('arrow') ?></span>
        </a>
      </article>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap narrow prose">
    <h2>Which influencer tool should you use first?</h2>
    <p>If you have never charged a brand before, start with the <a href="/tools/influencer-earnings-calculator/">influencer earnings calculator</a>. It gives you a defensible per-post rate range based on your platform, follower count, engagement and niche, so you never undersell yourself in a negotiation. Then run your last few posts through the <a href="/tools/engagement-rate-calculator/">engagement rate calculator</a>: brands look at engagement before follower count, and a strong rate is your best argument for higher fees.</p>
    <p>Once you know your numbers, package them. The <a href="/tools/media-kit-builder/">media kit builder</a> turns your stats, audience and services into a clean one-page PDF, and the <a href="/tools/influencer-email-generator/">influencer email generator</a> writes the pitch that goes with it. Brands can use the same generator in reverse to write to an influencer they want to work with.</p>
    <p>Finally, think long term. The <a href="/tools/income-stream-simulator/">income stream simulator</a> shows how adding affiliate links, a digital product or a membership changes your monthly income and how exposed you are to a single platform. Not sure where to start? The <a href="/tools/monetization-readiness-quiz/">monetization readiness quiz</a> recommends the two income streams that fit you best right now.</p>
    <div class="callout"><?= icon('shield') ?><p><strong>Private by design.</strong> Every Monetizing Influencers tool runs in your browser. The numbers you type are never sent to our server, and nothing is stored except your media kit draft, which stays on your own device.</p></div>
    <h2>How accurate are these calculators?</h2>
    <p>Influencer pricing is not public, so every rate calculator works from benchmarks. Ours use widely cited industry starting points (for example, roughly $10 per 1,000 Instagram followers for a feed post at average engagement) and adjust them for engagement, niche and content format. Treat the results as a well-reasoned starting range, then adjust for usage rights, exclusivity, turnaround time and how much the brand wants to work with you specifically. Each tool has a "How it works" section that lists its exact assumptions.</p>
  </div>
</section>

<?php
faq_block([
    ['Are these influencer tools really free?', '<p>Yes. All six tools are free to use with no account, no email and no usage limits.</p>'],
    ['Do the tools save my data?', '<p>No data is sent to Monetizing Influencers. The media kit builder saves your draft in your own browser (localStorage) so you can come back to it; clear your browser data to remove it.</p>'],
    ['Can brands use these tools too?', '<p>Yes. Brands and agencies use the earnings calculator to sanity-check quotes, the engagement calculator to vet creators, and the email generator to write to influencers.</p>'],
    ['Which platforms do the calculators support?', '<p>Instagram, TikTok, YouTube, Facebook and Pinterest. Each platform uses its own benchmark rate and engagement averages.</p>'],
]);
cta_band('Want a human to look at your numbers?', 'Send Monetizing Influencers your channel and we will outline the income streams and rates that fit your audience, free.');
page_end();
