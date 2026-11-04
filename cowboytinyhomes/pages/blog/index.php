<?php
$posts = blog_posts();
$GLOBALS['schema'][] = [
    '@type' => 'Blog', '@id' => abs_url('/blog/') . '#blog', 'name' => SITE_NAME . ' Blog', 'url' => abs_url('/blog/'),
    'publisher' => ['@id' => SITE_URL . '/#business'],
    'blogPost' => array_map(function ($p, $m) {
        return ['@type' => 'BlogPosting', 'headline' => $m['title'], 'url' => abs_url($p), 'datePublished' => $m['published'], 'image' => abs_url(img_url($m['image']))];
    }, array_keys($posts), $posts),
];
hero([
    'eyebrow' => 'The Cowboy Tiny Homes Blog',
    'h1' => 'Tiny Home Blog: Ideas &amp; Advice for Texas Tiny Living',
    'lead' => 'Design ideas, building tips and honest advice from the Cowboy Tiny Homes team — for anyone dreaming about, planning or living in a tiny home, casita or small house in Texas.',
    'image' => 'Cowboy-Tiny-Homes-Home-BG.webp',
    'cta' => false,
]);
$first = array_key_first($posts);
$fm = $posts[$first];
?>
<section class="section">
  <div class="wrap">
    <article class="grid-2 card" style="padding:0;overflow:hidden;align-items:center;gap:0;margin-bottom:48px;grid-template-columns:1.15fr .85fr">
      <a href="<?= e($first) ?>" tabindex="-1" aria-hidden="true" style="display:block;background:var(--ink-3)"><img src="<?= e(img_url($fm['image'])) ?>" alt="<?= e($fm['crumb']) ?> — featured image" width="1200" height="675" style="width:100%;height:auto"></a>
      <div style="padding:36px">
        <span class="card-kicker">Latest · <?= e($fm['category']) ?> · <time datetime="<?= e($fm['published']) ?>"><?= nice_date($fm['published']) ?></time></span>
        <h2 style="margin-top:10px"><a href="<?= e($first) ?>" style="color:inherit;text-decoration:none"><?= e($fm['title']) ?></a></h2>
        <p><?= e($fm['desc']) ?></p>
        <a class="btn btn--ink" href="<?= e($first) ?>">Read the Article</a>
      </div>
    </article>
    <h2>All Articles</h2>
    <?php post_cards(); ?>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap grid-2">
    <div>
      <h2>Looking for In-Depth Guides?</h2>
      <p>Our blog covers ideas and inspiration. For the nuts and bolts — permits, costs, financing and choosing a builder — see the Cowboy Tiny Homes <a href="/guides/">Texas tiny home guides</a>, or run your own numbers with our <a href="/tools/">free planning tools</a>.</p>
    </div>
    <div class="cards cards--links">
      <a class="card card--link" href="/guides/tiny-house-laws-texas/"><span class="card-kicker">Guide</span><strong>Tiny House Laws in Texas</strong><span>Permits, zoning and codes explained.</span></a>
      <a class="card card--link" href="/guides/cost-to-build-a-tiny-house-in-texas/"><span class="card-kicker">Guide</span><strong>Cost to Build a Tiny House</strong><span>Real Texas cost ranges.</span></a>
    </div>
  </div>
</section>
<?php cta_band('Have a Tiny Home Idea?', 'Turn inspiration into a plan. Cowboy Tiny Homes offers free design consultations for tiny homes, casitas and small houses across Texas.');
