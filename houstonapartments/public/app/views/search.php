<?php
defined('HA_ROOT') || exit;
$center = $area ? [$area['lat'], $area['lng'], $area['zoom']] : [SITE['center'][0], SITE['center'][1], 10];
?>
<div class="search-app" id="search-app" data-center='<?= json_encode($center) ?>' data-area="<?= e($areaKey) ?>">
  <form class="filterbar" id="filters" role="search" onsubmit="return false">
    <div class="fb-search">
      <span class="ico ico-search" aria-hidden="true"></span>
      <input name="q" type="search" placeholder="Neighborhood, ZIP or community" aria-label="Search by neighborhood, ZIP or community" autocomplete="off">
    </div>
    <select name="area" aria-label="Area" class="fb-area">
      <option value="">All of Houston</option>
      <?php foreach (AREAS as $k => $a): ?><option value="<?= $k ?>"<?= $k === $areaKey ? ' selected' : '' ?>><?= e($a['name']) ?></option><?php endforeach ?>
    </select>

    <div class="dd" data-dd>
      <button type="button" class="dd-btn" aria-expanded="false"><span data-label="price">Price</span> <i class="caret"></i></button>
      <div class="dd-panel" hidden>
        <p class="dd-title">Monthly rent</p>
        <div class="range-row">
          <label>Min<select name="price_min"><option value="">No min</option><?php foreach ([800, 1000, 1200, 1400, 1600, 1800, 2000, 2500] as $p): ?><option value="<?= $p ?>">$<?= number_format($p) ?></option><?php endforeach ?></select></label>
          <span>–</span>
          <label>Max<select name="price_max"><option value="">No max</option><?php foreach ([1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000, 4000] as $p): ?><option value="<?= $p ?>">$<?= number_format($p) ?></option><?php endforeach ?></select></label>
        </div>
        <div class="price-presets">
          <button type="button" data-preset="0,1200">Under $1.2k</button>
          <button type="button" data-preset="1200,1600">$1.2k–1.6k</button>
          <button type="button" data-preset="1600,2200">$1.6k–2.2k</button>
          <button type="button" data-preset="2200,">$2.2k+</button>
        </div>
      </div>
    </div>

    <div class="dd" data-dd>
      <button type="button" class="dd-btn" aria-expanded="false"><span data-label="beds">Beds / Baths</span> <i class="caret"></i></button>
      <div class="dd-panel" hidden>
        <p class="dd-title">Bedrooms</p>
        <div class="seg" data-multi="beds">
          <?php foreach (['0' => 'Studio', '1' => '1', '2' => '2', '3' => '3', '4' => '4+'] as $v => $l): ?>
            <label><input type="checkbox" value="<?= $v ?>"><span><?= $l ?></span></label>
          <?php endforeach ?>
        </div>
        <p class="dd-title">Bathrooms</p>
        <div class="seg" data-single="baths">
          <?php foreach (['' => 'Any', '1' => '1+', '2' => '2+', '3' => '3+'] as $v => $l): ?>
            <label><input type="radio" name="baths" value="<?= $v ?>"<?= $v === '' ? ' checked' : '' ?>><span><?= $l ?></span></label>
          <?php endforeach ?>
        </div>
      </div>
    </div>

    <label class="toggle-chip"><input type="checkbox" name="pets" value="1"><span>🐾 Pets</span></label>

    <button type="button" class="dd-btn more-btn" data-more aria-expanded="false" aria-controls="more-panel">More filters <span class="count-badge" hidden>0</span></button>

    <select name="sort" aria-label="Sort" class="fb-sort">
      <option value="">Best match</option>
      <option value="price_asc">Price: low to high</option>
      <option value="price_desc">Price: high to low</option>
      <option value="newest">Newest builds</option>
      <option value="rating">Top rated</option>
      <option value="sqft">Largest</option>
    </select>
    <button type="button" class="fb-reset" data-reset>Reset</button>

    <div class="more-panel" id="more-panel" hidden>
      <div class="more-grid">
        <fieldset>
          <legend>Must-haves</legend>
          <label class="check"><input type="checkbox" name="parking" value="1"> Parking included</label>
          <label class="check"><input type="checkbox" name="special" value="1"> Move-in specials</label>
          <label class="check"><input type="checkbox" name="furnished" value="1"> Furnished</label>
          <label class="check"><input type="checkbox" name="essential" value="1"> Essential / income-restricted</label>
        </fieldset>
        <fieldset>
          <legend>Size &amp; age</legend>
          <label>Min. square feet<select name="sqft"><option value="">Any</option><?php foreach ([600, 800, 1000, 1200, 1500] as $s): ?><option value="<?= $s ?>"><?= number_format($s) ?>+ sqft</option><?php endforeach ?></select></label>
          <label>Built after<select name="year"><option value="">Any year</option><?php foreach ([2020, 2015, 2010, 2000, 1990] as $y): ?><option value="<?= $y ?>"><?= $y ?></option><?php endforeach ?></select></label>
        </fieldset>
        <fieldset class="amen-set">
          <legend>Amenities</legend>
          <div class="amen-grid" data-multi="amen">
            <?php foreach (Listings::AMENITIES as $k => [$label]): ?>
              <label class="check"><input type="checkbox" value="<?= $k ?>"> <?= e($label) ?></label>
            <?php endforeach ?>
          </div>
        </fieldset>
      </div>
      <div class="more-actions"><button type="button" class="btn btn-grad" data-more-done>Show results</button></div>
    </div>
  </form>

  <div class="results-layout">
    <div class="map-pane">
      <div id="search-map" class="search-map" aria-label="Map of matching apartments"></div>
      <div class="map-tools">
        <button type="button" class="map-tool draw-btn" data-draw><span class="ico ico-lasso" aria-hidden="true"></span> <span>Draw area</span></button>
        <button type="button" class="map-tool" data-clear-draw hidden>Clear shape</button>
        <label class="map-tool move-search"><input type="checkbox" data-move-search checked> Search as I move</label>
      </div>
      <div class="draw-hint" hidden>Click and drag to draw your search area · <kbd>Esc</kbd> to cancel</div>
    </div>
    <section class="list-pane" aria-live="polite">
      <div class="list-head">
        <div>
          <h1 class="list-title"><?= $area ? e($area['name']) . ' Apartments for Rent' : 'Houston Apartments for Rent' ?></h1>
          <p class="list-count"><span data-total>…</span> <span class="avg" data-avg></span></p>
        </div>
        <div class="active-chips" data-chips></div>
      </div>
      <div class="cards-grid" data-results>
        <?php for ($i = 0; $i < 6; $i++): ?><div class="card skeleton"><div class="sk-media"></div><div class="sk-line"></div><div class="sk-line short"></div></div><?php endfor ?>
      </div>
      <nav class="pager" data-pager aria-label="Results pages"></nav>
      <div class="list-cta">
        <p><strong>Not seeing the right fit?</strong> A Houston Apartments locator can check off-market availability and current specials for you.</p>
        <button class="btn btn-grad" type="button" data-lead>Ask a locator</button>
      </div>
    </section>
  </div>
  <button type="button" class="view-toggle" data-view-toggle><span class="ico ico-map" aria-hidden="true"></span> <span>Map</span></button>
</div>
