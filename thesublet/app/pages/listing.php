<?php defined('APP') || exit;

[$citySlug, $st, $slug, $id] = $params;
$l = listing_get((int)$id);
if (!$l) not_found('That listing doesn’t exist.');

$owner = current_owner();
$isOwner = $owner && (int)$l['owner_id'] === (int)$owner['id'];
$preview = $isOwner || is_admin();
if (!in_array($l['status'], ['active', 'rented'], true) && !$preview) {
    if (in_array($l['status'], ['expired', 'unavailable', 'rejected'], true)) {
        http_response_code(410);
        cache_public();
        page([
            'title' => 'This sublet is no longer available | The Sublet',
            'robots' => 'noindex, follow',
            'body' => '<div class="wrap narrow section"><h1>This sublet is no longer available</h1><p>“' . e($l['title']) . '” has expired or been taken down by the host.</p><p><a class="btn" href="' . e(city_url($l['state'], $l['city_slug'])) . '">More sublets in ' . e($l['city']) . '</a> <a class="btn btn-ghost" href="/sublets/">Browse all</a></p></div>',
        ]);
        exit;
    }
    not_found('That listing isn’t published yet.');
}
$canonical = listing_url($l);
if ($_SERVER['REQUEST_URI'] !== $canonical && strtok($_SERVER['REQUEST_URI'], '?') !== $canonical) redirect($canonical, 301);

$preview ? cache_private() : cache_public();
if (!$preview && ($_SERVER['REQUEST_METHOD'] ?? '') === 'GET') q('UPDATE listings SET views = views + 1 WHERE id = ?', [(int)$l['id']]);

$photos = listing_photos((int)$l['id']);
$types = property_types();
$amen = array_filter(explode(',', (string)$l['amenities']));
$showContact = contact_public($l);
$verified = is_verified($l);
$guide = city_guide($l['state'], $l['city_slug']);
$cityUrl = city_url($l['state'], $l['city_slug']);
$crumbs = [['The Sublet', '/'], ['Sublets', '/sublets/'], [state_name($l['state']), state_url($l['state'])], [$l['city'], $cityUrl], [$l['title'], $canonical]];
$similar = listing_card_data(array_values(array_filter(
    listing_search(['state' => $l['state'], 'city' => $l['city_slug']], 5)['items'], fn($x) => (int)$x['id'] !== (int)$l['id'])));
$similar = array_slice($similar, 0, 4);
$months = $l['available_from'] && $l['available_to'] ? max(1, (int)round((strtotime($l['available_to']) - strtotime($l['available_from'])) / (30.44 * 86400))) : null;
$bedsLabel = $l['beds'] === 'studio' ? 'Studio' : $l['beds'] . ' bed' . ($l['beds'] === '1' ? '' : 's');
$bathsLabel = $l['baths'] === 'shared' ? 'Shared bath' : $l['baths'] . ' bath' . ($l['baths'] === '1' ? '' : 's');

if (is_unclaimed($l)) {
    $body = view('listing_directory', compact('l', 'crumbs', 'guide', 'cityUrl', 'similar'));
    page([
        'title' => seo_title($l['title'], ' – ' . $l['city'] . ', ' . $l['state']),
        'description' => excerpt($l['title'] . ' in ' . $l['city'] . ', ' . $l['state'] . ': ' . (property_types()[$l['property_type']] ?? 'furnished housing') . ' for monthly stays. Address, phone, website and owner claim on The Sublet.', 150),
        'canonical' => $canonical,
        'robots' => 'index, follow',
        'body' => $body,
        'h_extra' => leaflet_head(),
        'schema' => [schema_breadcrumbs($crumbs), schema_business($l)],
    ]);
    exit;
}

ob_start(); ?>
<div class="wrap listing-page">
  <?= breadcrumbs_html($crumbs) ?>
  <?php if ($preview && $l['status'] !== 'active'): ?><div class="flash flash-warn">Preview — status: <strong><?= e(listing_status_label($l['status'])) ?></strong>. Only you can see this page.</div><?php endif; ?>
  <?php if ($l['status'] === 'rented'): ?><div class="flash flash-warn">This place has been rented. <a href="<?= e($cityUrl) ?>">See other sublets in <?= e($l['city']) ?></a>.</div><?php endif; ?>

  <header class="l-head">
    <div>
      <h1><?= e($l['title']) ?></h1>
      <p class="l-loc"><?= e(($l['neighborhood'] ? $l['neighborhood'] . ', ' : '') . $l['city'] . ', ' . $l['state'] . ($l['zip'] ? ' ' . $l['zip'] : '')) ?></p>
      <p class="l-badges">
        <?php if ($verified): ?><span class="badge badge-verified" title="Paid listing; host confirmed their email">✔ Verified host</span><?php endif; ?>
        <span class="badge"><?= e($types[$l['property_type']] ?? '') ?></span>
        <span class="badge"><?= $l['furnished'] ? 'Furnished' : 'Unfurnished' ?></span>
        <?php if ($l['pets'] !== 'no'): ?><span class="badge">🐾 <?= e(pet_options()[$l['pets']]) ?></span><?php endif; ?>
      </p>
    </div>
    <div class="l-actions">
      <button class="btn btn-ghost btn-sm fav-btn-lg" type="button" data-fav="<?= (int)$l['id'] ?>" aria-pressed="false">♡ Save</button>
      <label class="btn btn-ghost btn-sm"><input type="checkbox" data-compare="<?= (int)$l['id'] ?>"> Compare</label>
    </div>
  </header>

  <div class="l-layout">
    <div class="l-main">
      <div class="gallery<?= count($photos) > 2 ? ' gallery-multi' : (count($photos) === 2 ? ' gallery-two' : '') ?>">
        <?php if ($photos): foreach ($photos as $i => $p): ?>
          <a href="<?= photo_src((int)$p['id']) ?>" class="g-item" target="_blank" rel="noopener"><img src="<?= photo_src((int)$p['id']) ?>" alt="<?= e($l['title']) ?> — photo <?= $i + 1 ?>" width="<?= (int)$p['width'] ?>" height="<?= (int)$p['height'] ?>" <?= $i ? 'loading="lazy"' : 'fetchpriority="high"' ?>></a>
        <?php endforeach; else: ?>
          <div class="g-empty">
            <?= placeholder_svg($l['property_type'], false, (int)$l['id']) ?>
            <p>The host hasn’t added photos yet. Ask for a live video tour before you commit.</p>
            <a class="btn btn-sm" href="/manage/<?= (int)$l['id'] ?>/">📷 Add Photos</a> <span class="small muted">(for the host)</span>
          </div>
        <?php endif; ?>
      </div>

      <section class="facts">
        <div><span>Rent</span><strong><?= $l['rent'] > 0 ? money($l['rent']) . '/mo' : 'On request' ?></strong><?= $l['utilities_included'] ? '<small>Utilities included</small>' : '<small>Utilities extra</small>' ?></div>
        <div><span>Deposit</span><strong><?= $l['deposit'] ? money($l['deposit']) : 'None stated' ?></strong></div>
        <div><span>Available</span><strong><?= $l['available_from'] ? e(fmt_date($l['available_from'])) : 'Now' ?></strong><small>until <?= $l['available_to'] ? e(fmt_date($l['available_to'])) : 'flexible' ?></small></div>
        <div><span>Minimum stay</span><strong><?= (int)$l['min_stay'] ?> month<?= $l['min_stay'] > 1 ? 's' : '' ?></strong><?= $months ? '<small>up to ~' . $months . ' months</small>' : '' ?></div>
        <div><span>Space</span><strong><?= e($bedsLabel) ?></strong><small><?= e($bathsLabel) ?></small></div>
      </section>

      <section class="l-sec">
        <h2>About this place</h2>
        <?= nl2p($l['description']) ?>
      </section>
      <?php if ($amen): ?>
      <section class="l-sec">
        <h2>Amenities</h2>
        <ul class="amen"><?php foreach ($amen as $a): if (!isset(amenity_options()[$a])) continue; ?><li><?= e(amenity_options()[$a]) ?></li><?php endforeach; ?></ul>
      </section>
      <?php endif; ?>
      <section class="l-sec">
        <h2>House rules</h2>
        <?= $l['house_rules'] ? nl2p($l['house_rules']) : '<p class="muted">No specific rules listed — ask the host.</p>' ?>
        <p><strong>Pets:</strong> <?= e(pet_options()[$l['pets']] ?? 'Ask host') ?></p>
      </section>
      <?php if ($l['lat'] !== null): ?>
      <section class="l-sec">
        <h2>Approximate location</h2>
        <div id="lmap" class="map map-sm" data-lat="<?= e($l['lat']) ?>" data-lng="<?= e($l['lng']) ?>" aria-label="Map showing the approximate area"></div>
        <p class="small muted">The circle shows the general area only. The host shares the exact address once you’ve been in touch.</p>
      </section>
      <?php endif; ?>
      <?php if ($guide): ?>
      <section class="l-sec">
        <h2>About <?= e($l['city']) ?></h2>
        <p><?= e(html_entity_decode($guide['tagline'], ENT_QUOTES, 'UTF-8')) ?> <a href="<?= e($cityUrl) ?>">Read our <?= e($l['city']) ?> sublet guide →</a></p>
      </section>
      <?php endif; ?>
      <?= amazon_block(listing_amazon_items($l), 'Packing & furnished-room essentials') ?>
    </div>

    <aside class="l-side">
      <div class="side-card">
        <p class="side-price"><?= $l['rent'] > 0 ? '<strong>' . money($l['rent']) . '</strong> / month' : '<strong>Rates on request</strong>' ?></p>
        <?php if ($showContact): ?>
          <div class="contact-direct">
            <h2 class="h4">Contact <?= e($l['contact_name'] ?: 'the host') ?></h2>
            <p>✉️ <a href="mailto:<?= e($l['contact_email']) ?>"><?= e($l['contact_email']) ?></a></p>
            <?php if ($l['contact_phone']): ?><p>📞 <a href="tel:<?= e(preg_replace('/[^0-9+]/', '', $l['contact_phone'])) ?>"><?= e($l['contact_phone']) ?></a></p><?php endif; ?>
            <p class="small muted">Or send a message below.</p>
          </div>
        <?php endif; ?>
        <?php if ($l['status'] === 'active'): ?>
        <form class="js-form" method="post" action="/listing/<?= (int)$l['id'] ?>/contact/" data-csrf>
          <h2 class="h4"><?= $showContact ? 'Message the host' : 'Contact the host' ?></h2>
          <?php if (!$showContact): ?><p class="small muted">Your message is relayed by The Sublet; the host’s email stays private. The host can reply to you directly.</p><?php endif; ?>
          <input type="hidden" name="_csrf" value="">
          <?= honeypot_field() ?>
          <label>Your name<input type="text" name="name" required maxlength="120" autocomplete="name"></label>
          <label>Your email<input type="email" name="email" required maxlength="190" autocomplete="email"></label>
          <label>Message<textarea name="message" rows="5" required minlength="20" maxlength="3000" placeholder="Hi! I’m interested from <?= e(fmt_date($l['available_from'] ?: date('Y-m-d'), 'M j')) ?>. A bit about me…"></textarea></label>
          <button class="btn btn-block" type="submit">Send message</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>
        <?php endif; ?>
      </div>
      <div class="side-card scam-tips">
        <h2 class="h4">🛡️ Scam-awareness tips</h2>
        <ul>
          <li><strong>Never wire money</strong> or pay with gift cards, crypto or payment apps to someone you haven’t met.</li>
          <li><strong>Tour first</strong> — in person or by live video — before paying anything.</li>
          <li>Ask to see the lease or the landlord’s written OK to sublet.</li>
          <li>Be wary of prices far below similar places, or “I’m overseas, I’ll mail the keys.”</li>
        </ul>
        <a href="/safety/">More safety tips →</a>
      </div>
      <details class="side-card report">
        <summary>🚩 Report listing</summary>
        <form class="js-form" method="post" action="/listing/<?= (int)$l['id'] ?>/report/" data-csrf>
          <input type="hidden" name="_csrf" value="">
          <?= honeypot_field() ?>
          <label>Reason<select name="reason" required>
            <option value="scam">Looks like a scam</option><option value="wrong">Wrong or misleading details</option>
            <option value="unavailable">No longer available</option><option value="discrimination">Discriminatory language</option>
            <option value="illegal">Possibly illegal rental</option><option value="other">Other</option></select></label>
          <label>Details (optional)<textarea name="details" rows="3" maxlength="2000"></textarea></label>
          <label>Your email (optional)<input type="email" name="email" maxlength="190"></label>
          <button class="btn btn-sm btn-ghost" type="submit">Send report</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>
      </details>
      <p class="small muted">Listing #<?= (int)$l['id'] ?> · posted <?= e(fmt_date($l['published_at'] ?: $l['created_at'])) ?><?= $isOwner ? ' · <a href="/account/listing/' . (int)$l['id'] . '/">Edit</a>' : '' ?></p>
    </aside>
  </div>

  <?php if ($similar): ?>
  <section class="section">
    <h2>More sublets in <?= e($l['city']) ?></h2>
    <div class="grid cards"><?php foreach ($similar as $c) echo listing_card_html($c); ?></div>
  </section>
  <?php endif; ?>
  <p class="small muted fh">The Sublet supports fair housing. Hosts must follow federal, state and local fair housing laws and their area’s short-term-rental rules.</p>
</div>
<?php
$body = ob_get_clean();
page([
    'title' => seo_title($l['title'], ' – ' . $l['city'] . ', ' . $l['state']),
    'description' => excerpt(($types[$l['property_type']] ?? '') . ' in ' . $l['city'] . ', ' . $l['state'] . ' for ' . money($l['rent']) . '/month' . ($l['available_from'] ? ', available ' . fmt_date($l['available_from']) : '') . '. ' . $l['description'], 150),
    'canonical' => $canonical,
    'robots' => $l['status'] === 'active' && !$preview ? 'index, follow, max-image-preview:large' : 'noindex, follow',
    'og_image' => $photos ? base_url(photo_src((int)$photos[0]['id'])) : null,
    'body' => $body,
    'h_extra' => leaflet_head(),
    'schema' => [schema_breadcrumbs($crumbs), schema_accommodation($l, $photos)],
]);
