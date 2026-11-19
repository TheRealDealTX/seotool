<?php defined('SNW') || (http_response_code(404) && exit);
partial('page-hero', ['title' => 'Seattle Neighborhood Guide', 'crumbs' => [['Neighborhoods', '/neighborhoods/']],
    'lead' => 'Where should you buy in Seattle? Compare housing, commutes and lifestyle across the city\'s most popular neighborhoods.']);
$counts = array_count_values(array_map(fn($l) => $l['neighborhood'], array_filter(listings(), fn($l) => $l['status'] !== 'Sold'))); ?>
<section class="section tight">
  <div class="wrap">
    <div class="grid-3">
<?php foreach (neighborhoods() as $s => $h): ?>
      <article class="card hood-card">
        <a class="card-media" href="/neighborhoods/<?= $s ?>/"><img src="<?= photo($h['image'], true) ?>" alt="Homes in <?= e($h['name']) ?>, Seattle" width="720" height="480" loading="lazy"></a>
        <div class="card-body">
          <p class="eyebrow"><?= e($h['area']) ?></p>
          <h2 class="card-title"><a href="/neighborhoods/<?= $s ?>/"><?= e($h['name']) ?></a></h2>
          <p class="muted"><?= e(excerpt($h['intro'], 150)) ?></p>
          <p class="meta"><?= ($counts[$s] ?? 0) ?> featured <?= ($counts[$s] ?? 0) === 1 ? 'home' : 'homes' ?> · ZIP <?= e($h['zip']) ?></p>
        </div>
      </article>
<?php endforeach ?>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="wrap prose narrow">
    <h2>How to Choose a Seattle Neighborhood</h2>
    <p>Start with your daily routine. If you commute downtown or to South Lake Union, neighborhoods along the Link light rail line — Capitol Hill, the U District, Roosevelt and Columbia City — can make car-light living realistic. If space and a yard matter most, look at Lake City, West Seattle or Magnolia, where lots tend to be larger.</p>
    <p>Then think about housing style. North Seattle's Ballard, Wallingford and Green Lake are known for early-1900s Craftsman homes; Fremont and Columbia City have plenty of newer townhomes; and condo buyers will find the most choice in Capitol Hill and South Lake Union. Our guide to the <a href="/blog/best-seattle-neighborhoods-to-buy-a-home/">best Seattle neighborhoods to buy a home</a> goes deeper, or <a href="/contact-seattle-real-estate-agents/">ask us</a> for a personalized shortlist.</p>
  </div>
</section>
<?php partial('cta') ?>
