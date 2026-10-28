<?php
defined('HA_ROOT') || exit;
$d = $p['d'];
$isNew = !$p['id'];
$title = $isNew ? 'Add a listing' : 'Edit: ' . $p['name'];
$actions = $isNew ? '' : ($p['status'] === 'publish'
    ? '<a class="btn ghost" href="' . e(listing_url($p['slug'])) . '" target="_blank" rel="noopener">View on website ↗</a>'
    : '<a class="btn ghost" href="/admin/listings/' . $p['id'] . '/preview/" target="_blank" rel="noopener">Preview (not public) ↗</a>');
$plans = $d['floorplans'] ?? [];
$prices = $d['prices'] ?? [];
$faqs = $d['faqs'] ?? [];
$schools = $d['schools'] ?? [];
$bedOpts = [0 => 'Studio', 1 => '1 bed', 2 => '2 beds', 3 => '3 beds', 4 => '4+ beds'];
?>
<form class="edit-form" method="post" enctype="multipart/form-data" data-dirty-check>
  <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">

  <?php if ($p['status'] === 'review'): ?>
    <div class="note note-review"><div>
      <strong>Hidden until rewritten.</strong> This listing was imported with riseapartments.com’s description, which Google would treat as duplicate content.
      Rewrite the <a href="#about-text">About this property</a> section in your own words and save – it goes live automatically once the text is clearly different
      (less than <?= ADMIN_REWRITE_MAX_OVERLAP * 100 ?>% matching phrases).
      <?php if (($d['rise_about'] ?? []) && $d['about'] ?? []): ?><br>Right now about <strong><?= round(Listings::aboutOverlap($d['about'], $d['rise_about']) * 100) ?>%</strong> still matches the original.<?php endif ?>
    </div></div>
  <?php endif ?>
  <?php if ($p['source'] === 'rise'): ?>
    <div class="note">
      This listing was imported from riseapartments.com.
      <?= $p['locked'] ? '<strong>It has been edited here, so the Rise sync no longer changes it.</strong>' : 'Right now it updates automatically when Rise changes. Saving this form stops that so your edits stick.' ?>
      <label class="inline"><input type="checkbox" name="keep_sync" value="1"> Keep updating it from Rise anyway (my changes below may be overwritten)</label>
    </div>
  <?php endif ?>

  <section class="card">
    <h2><span class="step">1</span> Basic details</h2>
    <div class="fields">
      <label class="span2"><span>Property name <b class="req">*</b></span><input name="name" value="<?= e($p['name']) ?>" required placeholder="e.g. Camden Heights"></label>
      <label>Show on website
        <select name="status"><option value="publish"<?= $p['status'] === 'publish' ? ' selected' : '' ?>>Yes – live</option><?php if ($p['status'] === 'review'): ?><option value="review" selected>Awaiting rewrite – goes live when About is rewritten</option><?php endif ?><option value="hidden"<?= $p['status'] === 'hidden' ? ' selected' : '' ?>>Hidden (draft / full)</option></select>
      </label>
      <label class="span2"><span>Street address <b class="req">*</b></span><input name="street" value="<?= e($p['street']) ?>" required placeholder="404 Oxford St" data-addr></label>
      <label>City<input name="city" value="<?= e($p['city'] ?: 'Houston') ?>" data-addr></label>
      <label>ZIP code<input name="zip" value="<?= e($p['zip']) ?>" inputmode="numeric" maxlength="5" data-addr></label>
      <label>Area
        <select name="area"><option value="">— Other / none —</option><?php foreach (AREAS as $k => $a): ?><option value="<?= $k ?>"<?= $areaKey === $k ? ' selected' : '' ?>><?= e($a['name']) ?></option><?php endforeach ?></select>
        <small>Puts the listing on that area’s page.</small>
      </label>
      <label>Neighborhood name<input name="neighborhood" value="<?= e($p['neighborhood']) ?>" placeholder="Optional, e.g. Washington Ave"></label>
    </div>
    <div class="map-box">
      <div class="map-head"><strong>Map pin</strong> <button type="button" class="btn small" data-find>📍 Find address on map</button> <small>Drag the pin or click the map to fine-tune.</small></div>
      <div id="pin-map" class="pin-map" data-lat="<?= e($p['lat']) ?>" data-lng="<?= e($p['lng']) ?>"></div>
      <input type="hidden" name="lat" value="<?= e($p['lat']) ?>"><input type="hidden" name="lng" value="<?= e($p['lng']) ?>">
    </div>
  </section>

  <section class="card">
    <h2><span class="step">2</span> Photos</h2>
    <p class="muted">The first photo is the cover. Drag photos to reorder them (or use the arrows), and click × to remove one.</p>
    <div class="photos" data-photos>
      <?php foreach ($d['photos'] ?? [] as $ph): ?>
        <figure class="ph" draggable="true" data-path="<?= e($ph) ?>"><img src="<?= e($ph) ?>" alt=""><span class="ph-tools"><button type="button" data-move="-1" aria-label="Move left">‹</button><button type="button" data-move="1" aria-label="Move right">›</button><button type="button" data-remove aria-label="Remove">×</button></span></figure>
      <?php endforeach ?>
    </div>
    <input type="hidden" name="photos_keep" value="">
    <label class="drop">
      <input type="file" name="photos_new[]" accept="image/*" multiple data-new-photos>
      <span><strong>Click to add photos</strong> or drag them here<br><small>JPG, PNG or WebP · large photos are resized automatically</small></span>
    </label>
    <div class="photos new" data-new-preview></div>
  </section>

  <section class="card">
    <h2><span class="step">3</span> Starting prices &amp; specials</h2>
    <p class="muted">🔒 These prices are <strong>never shown to visitors</strong> – the website says “Check for availability”. They’re only used so the price filters on the search page work. Leave a box empty if you don’t know it.</p>
    <div class="fields prices">
      <?php foreach ($bedOpts as $b => $label): ?>
        <label><?= $label ?><span class="money-in"><i>$</i><input name="price[<?= $b ?>]" value="<?= e($prices[$b] ?? '') ?>" inputmode="numeric" placeholder="—"></span></label>
      <?php endforeach ?>
      <label class="span3">Move-in special <small>(optional – shows a “Special” badge)</small><input name="special" value="<?= e($d['special'] ?? '') ?>" placeholder="e.g. 6 weeks free on 14-month leases"></label>
    </div>
  </section>

  <section class="card">
    <h2><span class="step">4</span> Floor plans</h2>
    <div class="plans-list" data-repeater="plans">
      <?php foreach ($plans as $i => $pl): ?>
        <div class="plan-row">
          <?php if ($pl['image']): ?><img class="plan-thumb" src="<?= e($pl['image']) ?>" alt=""><?php else: ?><span class="plan-thumb empty">No image</span><?php endif ?>
          <label>Bedrooms<select name="plans[<?= $i ?>][beds]"><?php foreach ($bedOpts as $b => $l): ?><option value="<?= $b ?>"<?= (int) $pl['beds'] === $b ? ' selected' : '' ?>><?= $l ?></option><?php endforeach ?></select></label>
          <label>Baths<input name="plans[<?= $i ?>][baths]" value="<?= e($pl['baths']) ?>" inputmode="decimal"></label>
          <label>Sq ft<input name="plans[<?= $i ?>][sqft]" value="<?= e($pl['sqft']) ?>" inputmode="numeric"></label>
          <label>Available<input name="plans[<?= $i ?>][available]" value="<?= e($pl['available']) ?>" placeholder="Now"></label>
          <label>Plan image<input type="file" name="plan_img[<?= $i ?>]" accept="image/*"></label>
          <input type="hidden" name="plans[<?= $i ?>][image]" value="<?= e($pl['image']) ?>">
          <label class="rm"><input type="checkbox" name="plans[<?= $i ?>][remove]" value="1"> Remove</label>
        </div>
      <?php endforeach ?>
    </div>
    <template data-template="plans">
      <div class="plan-row new">
        <span class="plan-thumb empty">New</span>
        <label>Bedrooms<select name="plans[__i__][beds]"><?php foreach ($bedOpts as $b => $l): ?><option value="<?= $b ?>"<?= $b === 1 ? ' selected' : '' ?>><?= $l ?></option><?php endforeach ?></select></label>
        <label>Baths<input name="plans[__i__][baths]" value="1" inputmode="decimal"></label>
        <label>Sq ft<input name="plans[__i__][sqft]" inputmode="numeric"></label>
        <label>Available<input name="plans[__i__][available]" placeholder="Now"></label>
        <label>Plan image<input type="file" name="plan_img[__i__]" accept="image/*"></label>
        <button type="button" class="btn small ghost" data-remove-row>Remove</button>
      </div>
    </template>
    <button type="button" class="btn" data-add="plans">＋ Add a floor plan</button>
  </section>

  <section class="card">
    <h2><span class="step">5</span> Features &amp; amenities</h2>
    <div class="checks big">
      <label><input type="checkbox" name="pets" value="1"<?= $p['pets'] ? ' checked' : '' ?>> 🐾 Pets allowed</label>
      <label><input type="checkbox" name="parking" value="1"<?= $p['parking'] ? ' checked' : '' ?>> 🚗 Parking included</label>
      <label><input type="checkbox" name="furnished" value="1"<?= $p['furnished'] ? ' checked' : '' ?>> 🛋 Furnished</label>
      <label><input type="checkbox" name="essential" value="1"<?= $p['essential'] ? ' checked' : '' ?>> Income-restricted / essential housing</label>
    </div>
    <h3>Inside the apartment</h3>
    <div class="checks"><?php foreach (ADMIN_UNIT_AMENITIES as $a): ?><label><input type="checkbox" name="amen_unit[]" value="<?= e($a) ?>"<?= in_array($a, $have, true) ? ' checked' : '' ?>> <?= e($a) ?></label><?php endforeach ?></div>
    <h3>Community</h3>
    <div class="checks"><?php foreach (ADMIN_COMMUNITY_AMENITIES as $a): ?><label><input type="checkbox" name="amen_comm[]" value="<?= e($a) ?>"<?= in_array($a, $have, true) ? ' checked' : '' ?>> <?= e($a) ?></label><?php endforeach ?></div>
    <label class="block">Other amenities <small>(one per line or separated by commas)</small><textarea name="amen_other" rows="3"><?= e(implode("\n", $other)) ?></textarea></label>
  </section>

  <section class="card">
    <h2><span class="step">6</span> Description &amp; details</h2>
    <label class="block" id="about-text">About this property <small>(leave a blank line between paragraphs)</small><textarea name="about" rows="8"><?= e(implode("\n\n", $d['about'] ?? [])) ?></textarea></label>
    <div class="fields">
      <label>Year built<input name="year_built" value="<?= e($p['year_built']) ?>" inputmode="numeric"></label>
      <label>Number of units<input name="units" value="<?= e($p['units']) ?>" inputmode="numeric"></label>
      <label>Stories<input name="stories" value="<?= e($p['stories']) ?>" inputmode="numeric"></label>
      <label>Google rating<input name="rating" value="<?= e($p['rating']) ?>" inputmode="decimal" placeholder="e.g. 4.3"></label>
      <label class="span2">Office hours<input name="hours" value="<?= e($d['hours'] ?? '') ?>" placeholder="e.g. 9 - 6 PM"></label>
    </div>
    <h3>Schools</h3>
    <div class="fields">
      <label>School district<input name="school_district" value="<?= e($schools['District'] ?? '') ?>"></label>
      <label>Elementary<input name="school_elem" value="<?= e($schools['Elementary School'] ?? '') ?>"></label>
      <label>Middle<input name="school_middle" value="<?= e($schools['Middle School'] ?? '') ?>"></label>
      <label>High<input name="school_high" value="<?= e($schools['High School'] ?? '') ?>"></label>
    </div>
  </section>

  <section class="card">
    <h2><span class="step">7</span> FAQs <small class="muted">(optional – shown on the property page and to Google)</small></h2>
    <div data-repeater="faqs">
      <?php foreach ($faqs as $i => $f): ?>
        <div class="faq-row"><label>Question<input name="faqs[<?= $i ?>][q]" value="<?= e($f['q']) ?>"></label><label>Answer<textarea name="faqs[<?= $i ?>][a]" rows="2"><?= e(implode("\n", $f['a'])) ?></textarea></label><button type="button" class="btn small ghost" data-remove-row>Remove</button></div>
      <?php endforeach ?>
    </div>
    <template data-template="faqs"><div class="faq-row"><label>Question<input name="faqs[__i__][q]"></label><label>Answer<textarea name="faqs[__i__][a]" rows="2"></textarea></label><button type="button" class="btn small ghost" data-remove-row>Remove</button></div></template>
    <button type="button" class="btn" data-add="faqs">＋ Add a question</button>
  </section>

  <div class="save-bar">
    <button class="btn primary big" type="submit">💾 Save listing</button>
    <a class="btn ghost" href="/admin/listings/">Cancel</a>
    <?php if (!$isNew): ?><span class="muted">Last updated <?= $p['updated_at'] ? e(date('M j, Y g:ia', strtotime($p['updated_at']))) . ' by ' . e($p['updated_by'] ?: 'Rise sync') : 'by Rise sync' ?></span><?php endif ?>
  </div>
</form>
<?php if (!$isNew): ?>
<form class="danger-zone" method="post" action="/admin/listings/<?= $p['id'] ?>/delete/" onsubmit="return confirm('Delete “<?= e(addslashes($p['name'])) ?>”? This removes it from the website.');">
  <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
  <button class="btn danger" type="submit">Delete this listing</button>
  <small class="muted">Tip: to take it off the site temporarily, set “Show on website” to Hidden instead.</small>
</form>
<?php endif ?>
