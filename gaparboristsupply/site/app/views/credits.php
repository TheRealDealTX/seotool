<?php
defined('GAP') || exit;
$meta = ['title' => 'Image Credits', 'desc' => 'Credits and licenses for the photos used on Gap Arborist Supply.', 'canonical' => '/image-credits/'];
$all = [];
foreach ($CAT['images'] as $list) foreach ($list as $ph) $all[$ph['src']] = $ph;
?>
<section class="cat-hero"><div class="wrap narrow"><?= crumbs([['Image credits', '/image-credits/']]) ?><h1>Image credits</h1>
<p class="lede">Photos on this site are representative images of each type of gear, used under Creative Commons or public-domain terms. Thank you to the photographers below. Product listings at the retailer show the exact item.</p></div></section>
<section class="wrap credits-grid">
<?php foreach ($all as $ph): ?>
  <figure class="credit-item"><img src="<?= e($ph['sm']) ?>" alt="" loading="lazy" width="600" height="450"><figcaption><?= photo_credit($ph) ?></figcaption></figure>
<?php endforeach; ?>
</section>
