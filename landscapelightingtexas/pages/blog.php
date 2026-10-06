<?php defined('LLT') or die(http_response_code(404));
// Serves both /blog/ and /category/general/ (every post is in General).
$isCat = !empty($P['category']);
$P['eyebrow'] = $isCat ? 'Category' : 'The Landscape Lighting Texas blog';
$P['lead'] = $isCat
    ? 'Every general article from Landscape Lighting Texas: in-depth guides, design ideas, cost breakdowns and maintenance advice for Texas properties.'
    : 'Design ideas, cost guides and practical how-tos from the Landscape Lighting Texas design team — written for Texas homes, trees and weather.';
$P['hero_no_cta'] = true;
$all = posts();
$first = array_shift($all);
?>
<section class="section">
  <div class="container">
    <div class="blog-filter reveal"><input type="search" placeholder="Search articles…" aria-label="Search articles" data-blog-search></div>
    <a class="post-featured reveal" href="<?= $first['path'] ?>" data-post>
      <div class="post-card-img"><img src="<?= img_url($first['image']) ?>" alt="<?= e($first['h1']) ?>" width="1536" height="1024"></div>
      <div class="post-card-body"><p class="post-card-meta">Latest · <?= fmt_date($first['date']) ?></p><h2><?= e($first['h1']) ?></h2><p><?= e($first['description']) ?></p><span class="link-arrow">Read article <?= icon('arrow', 16) ?></span></div>
    </a>
    <div class="card-grid posts-grid">
      <?php foreach ($all as $p) echo str_replace('<a class="post-card reveal"', '<a class="post-card reveal" data-post', post_card($p)); ?>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <?php section_head('Free tools', 'Put the Guides Into Practice'); tool_cards(); ?>
  </div>
</section>
<?php cta_band();
