<?php
/** @var string $slug */
$pages = [
    'about-us' => ['h1' => 'About Us', 'title' => 'About Us - Thought Changer', 'desc' => 'Thought Changer exists for one simple reason:change begins with a thought. Not the loud, dramatic kind. The small ones.', 'type' => 'AboutPage'],
    'privacy-policy' => ['h1' => 'Privacy Policy', 'title' => 'Privacy Policy - Thought Changer', 'desc' => 'How Thought Changer collects, uses, and protects information when you visit thoughtchangerblog.com.', 'type' => 'WebPage'],
    'terms-of-use' => ['h1' => 'Terms of Use', 'title' => 'Terms of Use - Thought Changer', 'desc' => 'The terms that apply when you access or use thoughtchangerblog.com.', 'type' => 'WebPage'],
    'affiliate-disclosure' => ['h1' => 'Affiliate Disclosure', 'title' => 'Affiliate Disclosure - Thought Changer', 'desc' => 'How Thought Changer uses affiliate links, including the Amazon Associates program, and how we choose what to recommend.', 'type' => 'WebPage'],
];
$pg = $pages[$slug];
$url = '/' . $slug . '/';
view('head', ['meta' => [
    'title' => $pg['title'], 'description' => $pg['desc'], 'canonical' => $url, 'bodyClass' => 'page page-' . $slug,
    'schema' => [['@type' => $pg['type'], '@id' => SITE_URL . $url . '#webpage', 'url' => SITE_URL . $url, 'name' => $pg['title'], 'isPartOf' => ['@id' => SITE_URL . '/#website']],
                 ['@type' => 'BreadcrumbList', 'itemListElement' => [['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => SITE_URL . '/'], ['@type' => 'ListItem', 'position' => 2, 'name' => $pg['h1']]]]],
]]);
?>
<section class="page-hero">
  <div class="wrap-narrow"><h1 class="page-title reveal"><?= e($pg['h1']) ?></h1></div>
</section>
<section class="band band-tight">
  <div class="wrap-narrow prose reveal">
<?= file_get_contents(APP . '/pages/' . $slug . '.html') ?>
  </div>
</section>
<?php if ($slug === 'about-us'): ?>
<section class="band band-soft">
  <div class="wrap">
    <h2 class="section-title reveal">Start Here</h2>
    <div class="grid grid-3">
      <?php foreach (array_filter(array_map('post_by_slug', ['life-is-fleeting-5-ways-to-slow-it-down', 'heres-what-it-means-to-level-up', 'the-power-of-your-own-light'])) as $p) view('card', ['p' => $p]); ?>
    </div>
  </div>
</section>
<?php endif; ?>
<?php view('foot'); ?>
