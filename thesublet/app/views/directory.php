<?php defined('APP') || exit;
/** @var array $f current filters; @var array $locked; @var array $res; @var array $cards; @var array $pg; @var string $basePath; @var array|null $center */
$types = property_types();
$sel = fn($a, $b) => (string)$a === (string)$b ? ' selected' : '';
$centerAttr = $center ? ' data-lat="' . e($center[0]) . '" data-lng="' . e($center[1]) . '" data-zoom="' . e($center[2] ?? 11) . '"' : '';
?>
<section class="directory" data-api="/api/listings" data-locked='<?= e(json_encode($locked)) ?>'<?= $centerAttr ?>>
  <form class="filters" method="get" action="<?= e($basePath) ?>" role="search" aria-label="Filter sublets">
    <?php if (!empty($showQ)): ?>
    <label class="f-q"><span>City or keyword</span><input type="search" name="q" value="<?= e($f['q'] ?? '') ?>" placeholder="e.g. Boston, Capitol Hill"></label>
    <?php endif; ?>
    <label><span>Min $</span><input type="number" name="min" inputmode="numeric" min="0" step="50" value="<?= e($f['min'] ?? '') ?>" placeholder="0"></label>
    <label><span>Max $</span><input type="number" name="max" inputmode="numeric" min="0" step="50" value="<?= e($f['max'] ?? '') ?>" placeholder="Any"></label>
    <label><span>Move in</span><input type="date" name="from" value="<?= e($f['from'] ?? '') ?>"></label>
    <label><span>Move out</span><input type="date" name="to" value="<?= e($f['to'] ?? '') ?>"></label>
    <label><span>Type</span><select name="type"><option value="">Any type</option><?php foreach ($types as $k => $v): ?><option value="<?= e($k) ?>"<?= $sel($f['type'] ?? '', $k) ?>><?= e($v) ?></option><?php endforeach; ?></select></label>
    <label class="chk"><input type="checkbox" name="furnished" value="1"<?= !empty($f['furnished']) ? ' checked' : '' ?>> Furnished</label>
    <label class="chk"><input type="checkbox" name="pets" value="1"<?= !empty($f['pets']) ? ' checked' : '' ?>> Pets OK</label>
    <label class="chk"><input type="checkbox" name="verified" value="1"<?= !empty($f['verified']) ? ' checked' : '' ?>> Verified hosts</label>
    <label><span>Sort</span><select name="sort"><option value="">Newest</option><option value="price_asc"<?= $sel($f['sort'] ?? '', 'price_asc') ?>>Price: low to high</option><option value="price_desc"<?= $sel($f['sort'] ?? '', 'price_desc') ?>>Price: high to low</option><option value="available"<?= $sel($f['sort'] ?? '', 'available') ?>>Available soonest</option></select></label>
    <div class="f-actions"><button class="btn btn-sm" type="submit">Apply</button> <a class="btn btn-sm btn-ghost" href="<?= e($basePath) ?>">Reset</a></div>
  </form>

  <div class="dir-bar">
    <p class="dir-count" aria-live="polite"><strong data-count><?= (int)$res['total'] ?></strong> <span data-count-label><?= $res['total'] == 1 ? 'sublet' : 'sublets' ?></span> available</p>
    <div class="view-toggle" role="group" aria-label="View">
      <button type="button" class="vt-btn is-on" data-view="list" aria-pressed="true">List</button>
      <button type="button" class="vt-btn" data-view="map" aria-pressed="false">Map</button>
    </div>
  </div>
  <div class="map-wrap" hidden><div id="map" class="map" aria-label="Map of approximate listing locations"></div><p class="small muted">Pins are approximate (within a few blocks). Exact addresses are shared by the host directly.</p></div>
  <div class="grid cards" data-results>
    <?php foreach ($cards as $c) echo listing_card_html($c); ?>
  </div>
  <div class="empty-state" data-empty<?= $cards ? ' hidden' : '' ?>>
    <?= $emptyHtml ?? '<h3>No sublets match those filters yet</h3><p>Try widening your budget or dates — or be the first to list a place here.</p><p><a class="btn" href="/post-a-sublet/">List your place</a></p>' ?>
  </div>
  <?php if ($pg['pages'] > 1): ?>
  <nav class="pager" aria-label="Pages">
    <?php for ($i = 1; $i <= $pg['pages']; $i++):
        $qs = http_build_query(array_filter($f + ['page' => $i > 1 ? $i : null], fn($v) => $v !== '' && $v !== null && $v !== 0)); ?>
      <a href="<?= e($basePath . ($qs ? '?' . $qs : '')) ?>"<?= $i === $pg['page'] ? ' aria-current="page" class="is-on"' : '' ?>><?= $i ?></a>
    <?php endfor; ?>
  </nav>
  <?php endif; ?>
  <div class="compare-bar" hidden><span><strong data-cmp-count>0</strong> selected to compare</span> <a class="btn btn-sm" href="/compare/" data-cmp-link>Compare</a> <button type="button" class="btn btn-sm btn-ghost" data-cmp-clear>Clear</button></div>
</section>
