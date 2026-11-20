<?php defined('WCA') || exit;
$rents = array_filter(array_column($listings, 'rent_min'));
$avgMin = $rents ? (int)round(array_sum($rents) / count($rents) / 5) * 5 : null;
$lps = landing_pages();
?>
<section class="page-head">
  <div class="wrap">
    <h1><?= e($h1) ?></h1>
    <p class="lead"><?= $intro /* trusted copy */ ?></p>
    <div class="quick-links small-links">
      <?php if ($landing): ?><a href="/apartments/">All apartments</a><?php endif; ?>
      <?php foreach ($lps as $k => $lp): if ($k === $landing) continue; ?>
        <a href="/apartments/<?= $k ?>/"><?= e(str_replace([' in West Carrollton, OH', ' & Affordable Housing', ' & Townhomes'], '', $lp['h1'])) ?></a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="wrap directory" data-directory>
  <button type="button" class="btn btn-ghost filters-toggle" onclick="this.nextElementSibling.classList.toggle('open')">⚙ Filters</button>
  <aside class="filters card" aria-label="Filters">
    <h2 class="h4">Filter results</h2>
    <label>Search<input type="search" data-f="q" placeholder="Name, street, amenity"></label>
    <label>Bedrooms
      <select data-f="beds"><option value="">Any</option><option value="0">Studio</option><option value="1">1</option><option value="2">2</option><option value="3">3+</option></select>
    </label>
    <label>Max rent: <output data-out="max">Any</output>
      <input type="range" data-f="max" min="600" max="3000" step="50" value="3000">
    </label>
    <fieldset class="checks-list">
      <legend>Must have</legend>
      <label><input type="checkbox" data-f="pets"> Pets allowed</label>
      <label><input type="checkbox" data-f="am" value="pool"> Pool</label>
      <label><input type="checkbox" data-f="am" value="fitness"> Fitness center</label>
      <label><input type="checkbox" data-f="am" value="garage"> Garage</label>
      <label><input type="checkbox" data-f="am" value="washer"> Washer/dryer</label>
      <label><input type="checkbox" data-f="am" value="balcon|patio"> Balcony / patio</label>
      <label><input type="checkbox" data-f="income"> Income-based</label>
      <label><input type="checkbox" data-f="claimed"> Verified owner (contact shown)</label>
    </fieldset>
    <label>City
      <select data-f="city"><option value="">Any</option><?php $cities = array_unique(array_column($listings, 'city')); sort($cities); foreach ($cities as $c): ?><option><?= e($c) ?></option><?php endforeach; ?></select>
    </label>
    <label>Type
      <select data-f="type"><option value="">Any</option><?php foreach (LISTING_TYPES as $k => $n): ?><option value="<?= $k ?>"><?= e($n) ?></option><?php endforeach; ?></select>
    </label>
    <button class="btn btn-ghost btn-sm" type="button" data-reset>Reset filters</button>
  </aside>

  <div class="results">
    <div class="results-bar">
      <p><strong data-count><?= count($listings) ?></strong> communities</p>
      <div class="results-controls">
        <label class="sr" for="sort">Sort</label>
        <select id="sort" data-sort>
          <option value="rec">Recommended</option><option value="low">Rent: low to high</option><option value="high">Rent: high to low</option><option value="name">Name A–Z</option><option value="new">Newest built</option>
        </select>
        <div class="toggle" role="group" aria-label="View">
          <button type="button" class="active" data-view="grid">Grid</button><button type="button" data-view="map">Map</button>
        </div>
      </div>
    </div>
    <div id="map" class="dir-map" hidden></div>
    <div class="card-grid" data-grid>
      <?php foreach ($listings as $l) partial('partials/card', ['l' => $l]); ?>
    </div>
    <p class="empty" data-empty hidden>No communities match those filters. <button class="linklike" type="button" data-reset>Reset filters</button></p>
  </div>
</section>

<div class="compare-bar" data-compare-bar hidden>
  <div class="wrap"><span><strong data-compare-count>0</strong> selected to compare</span><a class="btn btn-sm" data-compare-go href="/compare/">Compare now</a><button type="button" class="linklike" data-compare-clear>Clear</button></div>
</div>

<section class="section">
  <div class="wrap narrow faq">
    <h2>Frequently asked questions</h2>
    <details><summary>How many apartment communities are in West Carrollton, OH?</summary><p>This page lists <?= count($listings) ?> communities<?= $landing ? ' that match this category' : ' in West Carrollton and nearby Moraine, Miamisburg, Miami Township and Kettering' ?>. We add new properties as owners submit them, and you can <a href="/list-your-property/">list a property</a> for free.</p></details>
    <?php if ($avgMin): ?><details><summary>What is a typical starting rent?</summary><p>Across these listings the average advertised starting rent is about <?= money($avgMin) ?> per month. Rents change often, so confirm current pricing and specials with the property.</p></details><?php endif; ?>
    <details><summary>Why are some phone numbers and websites hidden?</summary><p>Contact details appear once the owner or manager claims and verifies the listing. For unclaimed communities, search the community name to reach the leasing office, or <a href="/contact/">ask us</a> and we will point you in the right direction.</p></details>
    <details><summary>Are the photos real?</summary><p>Photos on listings are added by verified owners and managers. Listings without photos yet show a placeholder illustration.</p></details>
  </div>
</section>
<script>window.WCA_LISTINGS = <?= json_encode(array_map('listing_public_json', $listings), JSON_HEX_TAG | JSON_UNESCAPED_SLASHES) ?>;</script>
