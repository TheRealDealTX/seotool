<?php defined('APP') || exit;
/** @var array $l; @var array $crumbs; @var ?array $guide; @var string $cityUrl; @var array $similar */
$types = property_types();
$typeLabel = $types[$l['property_type']] ?? 'Furnished housing';
$where = trim(($l['address_city'] && $l['address_city'] !== $l['city'] ? $l['address_city'] . ', ' : ($l['neighborhood'] ? $l['neighborhood'] . ', ' : '')) . $l['city'] . ', ' . $l['state']);
$site = $l['website'] ? preg_replace('#[?].*$#', '', $l['website']) : '';
$host = $site ? preg_replace('#^www\.#', '', (string)parse_url($site, PHP_URL_HOST)) : '';
$intro = [
    'furnished_community' => 'offers furnished apartments that can suit stays of a month or more — a common choice for travel nurses, relocating professionals, interns and visiting researchers.',
    'extended_stay' => 'is an extended-stay property with kitchen-equipped suites, often used for multi-week work assignments, relocations and stays between leases.',
    'student_housing' => 'is student-oriented housing near campus. Some properties offer summer, semester or individual leases, so it can be worth asking about shorter terms.',
][$l['property_type']] ?? 'offers housing that may suit medium-term stays.';
?>
<div class="wrap listing-page">
  <?= breadcrumbs_html($crumbs) ?>
  <header class="l-head reveal">
    <div>
      <p class="eyebrow"><?= e($typeLabel) ?></p>
      <h1><?= e($l['title']) ?></h1>
      <p class="l-loc">📍 <?= e($l['address_line'] ? $l['address_line'] . ', ' : '') ?><?= e($where) ?><?= $l['zip'] ? ' ' . e($l['zip']) : '' ?></p>
      <p class="l-badges"><span class="badge badge-glass">Property directory</span><span class="badge">Unclaimed</span></p>
    </div>
    <div class="l-actions">
      <button class="btn btn-ghost btn-sm fav-btn-lg" type="button" data-fav="<?= (int)$l['id'] ?>" aria-pressed="false">♡ Save</button>
    </div>
  </header>

  <div class="l-layout">
    <div class="l-main">
      <div class="g-empty g-dir reveal">
        <?= placeholder_svg($l['property_type'], false, (int)$l['id']) ?>
        <div class="g-dir-cta">
          <strong>Manage this property?</strong>
          <span>Claim the listing to add photos, rates and availability.</span>
          <a class="btn btn-sm btn-glow" href="/claim/<?= (int)$l['id'] ?>/">Claim this listing</a>
        </div>
      </div>

      <section class="l-sec reveal">
        <h2>About <?= e($l['title']) ?></h2>
        <p><?= e($l['title']) ?> in <?= e($where) ?> <?= e($intro) ?></p>
        <p>Rates, minimum stays, furnishing and availability haven’t been confirmed on The Sublet yet. Contact the property directly before making plans, and confirm whether short-term or month-to-month terms are offered.</p>
      </section>

      <section class="facts reveal">
        <div><span>Type</span><strong><?= e($typeLabel) ?></strong></div>
        <div><span>Rates</span><strong>On request</strong><small>Ask the property</small></div>
        <div><span>Pets</span><strong><?= e(pet_options()[$l['pets']] ?? 'Ask') ?></strong></div>
        <div><span>Listing</span><strong>Unclaimed</strong><small>Public business info</small></div>
      </section>

      <?php if ($l['lat'] !== null): ?>
      <section class="l-sec reveal">
        <h2>Location</h2>
        <div id="lmap" class="map map-sm" data-lat="<?= e($l['lat']) ?>" data-lng="<?= e($l['lng']) ?>" data-exact="1" aria-label="Map of the property location"></div>
      </section>
      <?php endif; ?>
      <?php if ($guide): ?>
      <section class="l-sec reveal">
        <h2>Living in <?= e($l['city']) ?></h2>
        <p><?= e(html_entity_decode($guide['tagline'], ENT_QUOTES, 'UTF-8')) ?> <a href="<?= e($cityUrl) ?>">Read the <?= e($l['city']) ?> sublet guide →</a></p>
      </section>
      <?php endif; ?>
      <div class="note small">This listing was created from publicly available business information so renters can find furnished and flexible housing in one place. It isn’t affiliated with or endorsed by the property. Details may be out of date — owners can <a href="/claim/<?= (int)$l['id'] ?>/">claim and update it</a> or <a href="/contact/">ask us to remove it</a>.</div>
      <?= amazon_block(listing_amazon_items($l), 'Packing & furnished-room essentials') ?>
    </div>

    <aside class="l-side">
      <div class="side-card side-glow reveal">
        <p class="side-price"><strong>Rates on request</strong></p>
        <h2 class="h4">Contact the property</h2>
        <?php if ($l['phone_public']): ?><p><a class="btn btn-block" href="tel:<?= e(preg_replace('/[^0-9+]/', '', $l['phone_public'])) ?>">📞 <?= e($l['phone_public']) ?></a></p><?php endif; ?>
        <?php if ($site): ?><p><a class="btn btn-ghost btn-block" href="<?= e($site) ?>" target="_blank" rel="nofollow ugc noopener">Visit <?= e($host) ?> ↗</a></p><?php endif; ?>
        <p class="small muted">Ask about furnished units, month-to-month or short-term leases, and corporate or travel-nurse rates.</p>
      </div>
      <div class="side-card owner-card reveal">
        <h2 class="h4">🏢 Is this your property?</h2>
        <p class="small">Claim it free, or verify instantly for <?= e(price_label()) ?>, to add photos, rates, availability and a direct contact form — and reach renters looking for 1–12 month stays.</p>
        <a class="btn btn-block btn-glow" href="/claim/<?= (int)$l['id'] ?>/">Claim this listing</a>
      </div>
      <div class="side-card scam-tips">
        <h2 class="h4">🛡️ Renter safety</h2>
        <ul><li>Book or pay only through the property’s official website or office.</li><li>Never wire money or pay with gift cards or crypto.</li><li>Tour first, in person or by live video.</li></ul>
        <a href="/safety/">More safety tips →</a>
      </div>
      <details class="side-card report">
        <summary>🚩 Report listing</summary>
        <form class="js-form" method="post" action="/listing/<?= (int)$l['id'] ?>/report/" data-csrf>
          <input type="hidden" name="_csrf" value="">
          <?= honeypot_field() ?>
          <label>Reason<select name="reason" required><option value="unavailable">Closed / no longer operating</option><option value="wrong">Wrong details</option><option value="scam">Looks like a scam</option><option value="other">Other</option></select></label>
          <label>Details (optional)<textarea name="details" rows="3" maxlength="2000"></textarea></label>
          <button class="btn btn-sm btn-ghost" type="submit">Send report</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>
      </details>
    </aside>
  </div>
  <?php if ($similar): ?>
  <section class="section">
    <h2>More places in <?= e($l['city']) ?></h2>
    <div class="grid cards"><?php foreach ($similar as $c) echo listing_card_html($c); ?></div>
  </section>
  <?php endif; ?>
</div>
