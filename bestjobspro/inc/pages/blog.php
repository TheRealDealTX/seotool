<?php
// Serves /blog/ and the old /category/job-articles/ archive (kept live but noindexed: it duplicates /blog/).
$isCategory = $route === '/category/job-articles/';
$posts = array_values(all_posts());
$first = array_shift($posts);
page_start([
    'title'       => $isCategory ? 'Job Articles | Best Jobs Pro Blog' : 'Career Advice & Job Search Blog | Best Jobs Pro',
    'description' => 'Career advice from Best Jobs Pro: job search tips, freelancing, remote work skills, contractor taxes, flexible schedules and hiring insights.',
    'path'        => $route,
    'robots'      => $isCategory ? 'noindex, follow' : null,
    'crumbs'      => $isCategory ? [['Blog', '/blog/'], ['Job Articles', '/category/job-articles/']] : [['Blog', '/blog/']],
    'schema'      => [[
        '@type' => 'Blog', 'name' => 'Best Jobs Pro Blog', 'url' => url('/blog/'),
        'publisher' => ['@id' => SITE_URL . '/#organization'],
        'blogPost' => array_map(fn($p) => ['@type' => 'BlogPosting', 'headline' => $p['title'], 'url' => url($p['path']), 'datePublished' => $p['published']], array_values(all_posts())),
    ]],
]);
page_hero($isCategory ? 'Job Articles' : 'The Best Jobs Pro Career Blog', 'Practical advice on finding work, growing your career, freelancing and hiring well, from the recruiters at Best Jobs Pro.', $isCategory ? [['Blog', '/blog/'], ['Job Articles', '/category/job-articles/']] : [['Blog', '/blog/']], '', 'Insights &amp; advice');
?>
<section class="section">
  <div class="wrap">
<?php if ($first): ?>
    <article class="post-feature reveal">
      <a href="<?= e($first['path']) ?>" tabindex="-1" aria-hidden="true"><img src="<?= e($first['image']) ?>" alt="" width="<?= (int)$first['image_w'] ?>" height="<?= (int)$first['image_h'] ?>"></a>
      <div class="post-feature__body">
        <p class="post-card__meta">Latest &middot; <time datetime="<?= e($first['published']) ?>"><?= e(nice_date($first['published'])) ?></time> &middot; <?= $first['minutes'] ?> min read</p>
        <h2 style="font-size:1.7rem"><a href="<?= e($first['path']) ?>" style="color:inherit;text-decoration:none"><?= e($first['title']) ?></a></h2>
        <p><?= e($first['excerpt']) ?></p>
        <p><a class="btn btn--sm" href="<?= e($first['path']) ?>">Read the article <?= icon('arrow') ?></a></p>
      </div>
    </article>
<?php endif; ?>
    <div class="posts">
<?php foreach ($posts as $p) echo post_card($p); ?>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="wrap">
    <div class="section__head reveal"><p class="eyebrow">Free tools</p><h2>Put the advice to work</h2></div>
    <div class="cards cards--3 tool-cards stagger">
<?php foreach (TOOLS as $slug => [$title, $desc, $ic]): ?>
      <article class="card tilt"><div class="card__ico"><?= icon($ic) ?></div><h3><?= e($title) ?></h3><p><?= e($desc) ?></p><a class="card__link" href="/career-tools/<?= $slug ?>/">Use the tool <?= icon('arrow') ?></a></article>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?= cta_band() ?>
<?php page_end();
