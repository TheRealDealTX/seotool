<?php defined('WCA') || exit; ?>
<section class="page-head"><div class="wrap">
  <h1>Compare West Carrollton apartments</h1>
  <p class="lead">Pick up to three communities to see rent, size, pets and amenities side by side. Your saved favorites (♥) appear below.</p>
</div></section>
<div class="wrap">
  <form class="compare-picker card" method="get" action="/compare/" data-compare-picker>
    <?php for ($i = 0; $i < 3; $i++): $cur = $items[$i]['id'] ?? ''; ?>
      <label>Community <?= $i + 1 ?>
        <select name="c<?= $i ?>"><option value="">— choose —</option>
          <?php foreach ($all as $o): ?><option value="<?= (int)$o['id'] ?>" <?= (int)$cur === (int)$o['id'] ? 'selected' : '' ?>><?= e($o['name']) ?></option><?php endforeach; ?>
        </select></label>
    <?php endfor; ?>
    <input type="hidden" name="ids" value="<?= e(implode(',', array_column($items, 'id'))) ?>">
    <button class="btn" type="submit">Compare</button>
  </form>

  <?php if ($items): $rows = [
      'Rent' => fn($l) => rent_label($l), 'Bedrooms' => fn($l) => beds_label($l), 'Size' => fn($l) => sqft_label($l) ?: '—',
      'Pets' => fn($l) => pets_label($l), 'Type' => fn($l) => LISTING_TYPES[$l['type']] ?? '', 'Year built' => fn($l) => $l['year_built'] ?: '—',
      'Units' => fn($l) => $l['units'] ?: '—', 'City' => fn($l) => $l['city'], 'Income-based' => fn($l) => $l['income_restricted'] ? 'Yes' : 'No',
      'Verified owner' => fn($l) => $l['claimed'] ? '✓ Yes' : 'Not yet']; ?>
  <div class="table-scroll">
  <table class="compare-table">
    <thead><tr><th></th><?php foreach ($items as $l): ?><th><img src="<?= e(photo_url($l['photos'][0], true)) ?>" alt="" width="200" height="133"><a href="<?= e($l['url']) ?>"><?= e($l['name']) ?></a></th><?php endforeach; ?></tr></thead>
    <tbody>
      <?php foreach ($rows as $label => $fn): ?><tr><th><?= e($label) ?></th><?php foreach ($items as $l): ?><td><?= e($fn($l)) ?></td><?php endforeach; ?></tr><?php endforeach; ?>
      <tr><th>Amenities</th><?php foreach ($items as $l): ?><td><ul class="tight"><?php foreach (array_slice($l['amenities'], 0, 12) as $a): ?><li><?= e($a) ?></li><?php endforeach; ?></ul></td><?php endforeach; ?></tr>
    </tbody>
  </table>
  </div>
  <?php endif; ?>

  <section class="section-tight">
    <h2>Your saved favorites</h2>
    <div class="card-grid" data-favorites><p class="muted">Tap the ♥ on any listing to save it here. Favorites are stored only in this browser.</p></div>
  </section>
</div>
<script>window.WCA_LISTINGS = <?= json_encode(array_map('listing_public_json', $all), JSON_HEX_TAG | JSON_UNESCAPED_SLASHES) ?>;</script>
