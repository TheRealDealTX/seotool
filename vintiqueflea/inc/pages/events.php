<?php
defined('INC') || exit;
page_start([
    'title' => 'Houston Flea Market Dates | Vintique Flea at Silver Street Studios',
    'description' => 'Vintique Flea market dates, hours, admission and directions. A curated indoor vintage flea market at Silver Street Studios, 2000 Edwards St, Houston TX.',
    'path' => '/events/',
]);
foreach (UPCOMING_EVENTS as $ev) {
    $s = [
        '@type' => 'Event',
        'name' => $ev['name'],
        'startDate' => $ev['start'],
        'endDate' => $ev['end'],
        'eventStatus' => 'https://schema.org/EventScheduled',
        'eventAttendanceMode' => 'https://schema.org/OfflineEventAttendanceMode',
        'location' => ['@type' => 'Place', 'name' => VENUE['name'], 'address' => venue_address()],
        'organizer' => ['@type' => 'Organization', 'name' => SITE_NAME, 'url' => SITE_URL . '/'],
        'description' => 'A curated indoor marketplace of mid-century modern, vintage clothing, architectural salvage and industrial, rustic home decor, local food trucks and more.',
        'image' => SITE_URL . '/assets/img/og-image.png',
    ];
    if (isset($ev['price_online'])) {
        $s['offers'] = ['@type' => 'Offer', 'price' => $ev['price_online'], 'priceCurrency' => 'USD', 'url' => $ev['tickets_url'] ?: abs_url('/events/'), 'availability' => 'https://schema.org/InStock'];
    }
    add_schema($s);
}
$mapQ = rawurlencode(VENUE['name'] . ', ' . VENUE['street'] . ', ' . VENUE['city'] . ', ' . VENUE['region'] . ' ' . VENUE['postal']);
?>
<div class="wrap">
  <?= breadcrumbs([['Events', '/events/']]) ?>
  <header class="page-head">
    <h1>Vintique Flea market dates &amp; visitor info</h1>
    <p class="lede">A curated indoor flea market in Houston's Washington Avenue Arts District, with mid-century modern, vintage clothing, architectural salvage, antiques, rustic decor, food trucks, beer and wine.</p>
  </header>

<?php if (UPCOMING_EVENTS): ?>
  <div class="event-list">
<?php foreach (UPCOMING_EVENTS as $ev): ?>
    <article class="event-card">
      <h2><?= e($ev['name']) ?></h2>
      <ul><?php foreach ($ev['hours'] ?? [] as $h): ?><li><?= e($h) ?></li><?php endforeach; ?></ul>
<?php if (isset($ev['price_online'])): ?>
      <p>Admission: $<?= e((string) $ev['price_online']) ?> online · $<?= e((string) ($ev['price_door'] ?? $ev['price_online'])) ?> at the door</p>
<?php endif; ?>
<?php if (!empty($ev['tickets_url'])): ?><a class="btn btn--primary" href="<?= e($ev['tickets_url']) ?>">Get tickets</a><?php endif; ?>
    </article>
<?php endforeach; ?>
  </div>
<?php else: ?>
  <div class="notice">
    <h2>Next market dates coming soon</h2>
    <p>We announce each seasonal edition to our email list first. Sign up and you'll hear about dates, vendors and early-bird admission before anyone else.</p>
    <?= newsletter_form('events') ?>
  </div>
<?php endif; ?>

  <section class="section section--tight">
    <h2>Seasonal editions</h2>
    <div class="edition-grid">
<?php foreach (EDITIONS as $slug => $ed): ?>
      <a class="edition" href="/events/<?= $slug ?>/">
        <span class="edition__icon" aria-hidden="true"><?= $ed['icon'] ?></span>
        <span class="edition__name"><?= e($ed['name']) ?></span>
        <span class="edition__lede"><?= e(mb_strimwidth($ed['lede'], 0, 140, '…')) ?></span>
      </a>
<?php endforeach; ?>
    </div>
  </section>

  <div class="layout-2">
    <article class="prose">
      <h2>Getting there</h2>
      <p>Vintique Flea takes place at <strong>Silver Street Studios, 2000 Edwards Street, Houston, TX 77007</strong>, in the heart of the Washington Avenue Arts District, just west of downtown. The building is a converted warehouse full of working artist studios, which gives the market its industrial, creative feel.</p>
      <p><a href="https://www.google.com/maps/search/?api=1&amp;query=<?= $mapQ ?>" target="_blank" rel="noopener">Open in Google Maps</a></p>
      <h2>What to expect</h2>
      <ul>
        <li><strong>Curated vendors:</strong> mid-century modern furniture, vintage clothing, architectural salvage and industrial pieces, antiques, rustic home decor, records and more.</li>
        <li><strong>Food trucks, beer &amp; wine:</strong> local food trucks park on site. See our <a href="/food-trucks/">food truck page</a>.</li>
        <li><strong>Indoors:</strong> rain, shine or August heat.</li>
        <li><strong>Family friendly:</strong> children 16 and under have historically been admitted free.</li>
        <li><strong>Giving back:</strong> past editions have supported local nonprofits like the Love, Molly Fund animal rescue.</li>
      </ul>
      <h2>Tips for market day</h2>
      <p>Arrive early for the best furniture, bring measurements and small bills, and plan how you'll get big pieces home. Our <a href="/guides/how-to-shop-a-flea-market/">flea market tips guide</a> covers everything, and you can practice bargaining in <a href="/play/haggle-hero/">Haggle Hero</a>.</p>
    </article>
    <aside class="side">
      <div class="side-card">
        <h2>Want a booth?</h2>
        <p>We're always looking for vintage dealers, salvage pros, makers and food trucks.</p>
        <a class="btn btn--primary btn--block" href="/vendors/">Vendor application</a>
      </div>
      <div class="side-card">
        <h2>Pack for the hunt</h2>
        <p>Folding wagon, tape measure, loupe: the picker's kit.</p>
        <a class="btn btn--ghost btn--block" href="/shop/flea-market-gear/">Flea market gear</a>
      </div>
    </aside>
  </div>
</div>
<?php page_end();
