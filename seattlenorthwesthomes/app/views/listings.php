<?php defined('SNW') || (http_response_code(404) && exit);
$hoods = neighborhoods();
$sel = fn($a, $b) => (string) $a === (string) $b ? ' selected' : '';
partial('page-hero', ['title' => 'Seattle Homes for Sale', 'crumbs' => [['Homes for Sale', '/homes-for-sale/']],
    'lead' => 'Craftsman houses, modern townhomes and city condos across Seattle\'s favorite neighborhoods.']); ?>
<section class="section tight">
  <div class="wrap">
    <form class="filters" method="get" action="/homes-for-sale/" role="search">
      <label>Keyword<input type="search" name="q" value="<?= e($f['q']) ?>" placeholder="e.g. view, garage, 98107"></label>
      <label>Neighborhood<select name="hood"><option value="">All neighborhoods</option>
<?php foreach ($hoods as $s => $h): ?><option value="<?= $s ?>"<?= $sel($f['hood'], $s) ?>><?= e($h['name']) ?></option><?php endforeach ?>
      </select></label>
      <label>Type<select name="type"><option value="">All types</option>
<?php foreach (['Single Family', 'Condo', 'Townhome'] as $t): ?><option<?= $sel($f['type'], $t) ?>><?= $t ?></option><?php endforeach ?>
      </select></label>
      <label>Min price<select name="min"><option value="">No min</option>
<?php foreach ([500000, 750000, 1000000, 1500000] as $v): ?><option value="<?= $v ?>"<?= $sel($f['min'], $v) ?>><?= money($v) ?></option><?php endforeach ?>
      </select></label>
      <label>Max price<select name="max"><option value="">No max</option>
<?php foreach ([750000, 1000000, 1500000, 2000000, 3000000] as $v): ?><option value="<?= $v ?>"<?= $sel($f['max'], $v) ?>><?= money($v) ?></option><?php endforeach ?>
      </select></label>
      <label>Beds<select name="beds"><option value="">Any</option>
<?php foreach ([1, 2, 3, 4] as $v): ?><option value="<?= $v ?>"<?= $sel($f['beds'], $v) ?>><?= $v ?>+</option><?php endforeach ?>
      </select></label>
      <label>Status<select name="status"><option value="">All</option><option value="active"<?= $sel($f['status'], 'active') ?>>Active &amp; pending</option><option<?= $sel($f['status'], 'For Sale') ?>>For Sale</option><option<?= $sel($f['status'], 'Pending') ?>>Pending</option><option<?= $sel($f['status'], 'Sold') ?>>Sold</option></select></label>
      <label>Sort<select name="sort"><option value="newest">Newest</option><option value="price-asc"<?= $sel($f['sort'], 'price-asc') ?>>Price: low to high</option><option value="price-desc"<?= $sel($f['sort'], 'price-desc') ?>>Price: high to low</option><option value="sqft"<?= $sel($f['sort'], 'sqft') ?>>Largest</option></select></label>
      <div class="filter-actions"><button class="btn btn-primary" type="submit">Update Results</button><?php if ($filtered): ?> <a href="/homes-for-sale/">Clear</a><?php endif ?></div>
    </form>
    <p class="result-count"><?= count($results) ?> <?= count($results) === 1 ? 'home' : 'homes' ?> found</p>
<?php if ($results): ?>
    <div class="grid-3">
<?php foreach ($results as $l) partial('listing-card', ['l' => $l]); ?>
    </div>
<?php else: ?>
    <div class="empty"><p>No homes match those filters right now. Try widening your search — or <a href="/buy-a-home-in-seattle/">tell us what you're looking for</a> and we'll watch the market for you, including homes that never hit the public portals.</p></div>
<?php endif ?>
<?php if (cfg('listing_note')): ?><p class="disclaimer"><?= e(cfg('listing_note')) ?></p><?php endif ?>
  </div>
</section>
<section class="section alt">
  <div class="wrap prose narrow">
    <h2>Buying a Home in Seattle</h2>
    <p>Seattle's housing market is as varied as its neighborhoods. North Seattle neighborhoods like <a href="/neighborhoods/wallingford/">Wallingford</a>, <a href="/neighborhoods/green-lake/">Green Lake</a> and <a href="/neighborhoods/greenwood/">Greenwood</a> are rich in early-1900s Craftsman homes; <a href="/neighborhoods/capitol-hill/">Capitol Hill</a> and <a href="/neighborhoods/south-lake-union/">South Lake Union</a> offer walkable condo living near light rail and major employers; and <a href="/neighborhoods/west-seattle/">West Seattle</a> and <a href="/neighborhoods/magnolia/">Magnolia</a> trade a short bridge commute for space, beaches and big views.</p>
    <p>Well-priced homes can attract multiple offers, so it pays to be ready: get pre-approved, know your must-haves and review disclosures and pre-inspections early. Read our <a href="/blog/seattle-first-time-home-buyer-guide/">Seattle first-time buyer guide</a> or <a href="/buy-a-home-in-seattle/">share your wish list</a> and we'll send matching homes as soon as they come up.</p>
  </div>
</section>
