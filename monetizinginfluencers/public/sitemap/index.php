<?php
require __DIR__ . '/../inc/layout.php';

$groups = [
    ['sparkles', 'Main pages', [
        ['Home', '/'],
        ['Influencer Monetization Guide', '/monetization/'],
        ['Web Design for Influencers', '/website-design/'],
        ['Get Started', '/get-started/'],
        ['Write For Us', '/write-for-us/'],
    ]],
    ['globe', 'Social platforms', [
        ['All Social Platforms', '/social-platforms/'],
        ['YouTube', '/social-platforms/youtube/'],
        ['TikTok', '/social-platforms/tiktok/'],
        ['Instagram', '/social-platforms/instagram/'],
        ['Facebook', '/social-platforms/facebook/'],
        ['Pinterest', '/social-platforms/pinterest/'],
    ]],
    ['calc', 'Free creator tools', [
        ['All Creator Tools', '/tools/'],
        ['Influencer Earnings Calculator', '/tools/influencer-earnings-calculator/'],
        ['Engagement Rate Calculator', '/tools/engagement-rate-calculator/'],
        ['Influencer Email Generator', '/tools/influencer-email-generator/'],
        ['Media Kit Builder', '/tools/media-kit-builder/'],
        ['Income Stream Simulator', '/tools/income-stream-simulator/'],
        ['Monetization Readiness Quiz', '/tools/monetization-readiness-quiz/'],
    ]],
    ['file', 'Blog', array_merge([['All Guides', '/blogs/']], array_map(fn($p) => [$p[1], $p[0]], site_posts()))],
    ['shield', 'Company and legal', [
        ['About', '/about/'],
        ['Contact', '/contact/'],
        ['Privacy Policy', '/privacy-policy/'],
        ['Terms of Use', '/terms/'],
    ]],
];

page_start([
    'title' => 'Sitemap | Monetizing Influencers',
    'description' => 'Every page on Monetizing Influencers in one place: monetization guides, platform playbooks, free creator tools, blog posts and company pages.',
    'path' => '/sitemap/',
    'extra_css' => ['/assets/css/pages.css'],
]);

page_hero('Sitemap', 'Sitemap', 'Find any guide, tool or page on Monetizing Influencers.', [['Sitemap', '/sitemap/']]);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap">
    <div class="card-grid cols-3">
<?php foreach ($groups as [$ic, $title, $links]): ?>
      <div class="card sitemap-group reveal">
        <h2><?= icon($ic) ?> <?= e($title) ?></h2>
        <ul>
<?php foreach ($links as [$label, $url]): ?>
          <li><a href="<?= e($url) ?>"><?= e($label) ?></a></li>
<?php endforeach; ?>
        </ul>
      </div>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php page_end();
