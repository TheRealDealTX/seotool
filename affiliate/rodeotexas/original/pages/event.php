<?php
/** Individual event page: /rodeos/<slug>/ */
defined('RT_APP') || exit;

use RT\Dates;
use RT\EventRepo;
use RT\Seo;
use RT\View;

$e = EventRepo::bySlug($slug);
if (!$e) {
    rt_not_found();
}
$perfs = EventRepo::performances((int) $e['id']);
$related = EventRepo::related($e);
$nearby = EventRepo::nearby($e);
$status = Dates::status($e);
$year = substr($e['start_date'], 0, 4);
$range = Dates::range($e['start_date'], $e['end_date'], true);
$placeLine = View::place($e);
$directions = View::mapsLink($e);
$url = '/rodeos/' . $e['slug'] . '/';
$parking = $e['parking_info'] ?: $e['venue_parking'];
$access = $e['accessibility_info'] ?: $e['venue_accessibility'];

$titleSeo = $e['title'] . (str_contains($e['title'], $year) ? '' : ' ' . $year) . ($e['city'] ? ' — ' . $e['city'] . ', TX' : '');
$descSeo = $e['title'] . ': ' . $range . ($e['city'] ? ' in ' . $e['city'] . ', Texas' : '') . '. '
    . ($perfs ? 'Show times, ' : '') . 'venue, directions and official links' . ($e['ticket_url'] && $e['ticket_url_verified'] ? ', tickets' : '') . '.';
$page = [
    'title' => $titleSeo,
    'description' => $status['key'] === 'canceled' ? 'CANCELED — ' . $descSeo : $descSeo,
    'canonical' => $url,
    // Old, unverified archive pages stay reachable but are kept out of search results.
    'robots' => ($e['is_legacy'] || $e['publish_state'] === 'archived') ? 'noindex,follow' : 'index,follow,max-image-preview:large',
    'og_image' => $e['image_url'] ?: '/assets/img/og-default.png',
    'jsonld' => array_filter([Seo::event($e, $perfs), Seo::breadcrumbs([['Home', '/'], ['Rodeos', '/rodeos/'], [$e['title'], $url]])]),
    'body_class' => 'page-event',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';

$notListed = '<span class="muted">Not listed — check the official website or contact the organizer.</span>';
?>
<article class="wrap event-page">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">›</span> <a href="/rodeos/">Rodeos</a> <span aria-hidden="true">›</span> <span><?= e($e['title']) ?></span></nav>

  <header class="event-hero">
    <div class="event-hero__tags">
      <?= View::statusBadge($e) ?>
      <?php if ($e['assoc_abbr']): ?><a class="tag tag--assoc" href="/rodeos/association/<?= e($e['assoc_slug']) ?>/" title="<?= e($e['assoc_name']) ?>"><?= e($e['assoc_abbr']) ?></a><?php endif; ?>
      <?php if ($e['type_name']): ?><a class="tag" href="/rodeos/type/<?= e($e['type_slug']) ?>/"><?= e($e['type_name']) ?></a><?php endif; ?>
      <?php if ($e['level']): ?><a class="tag tag--level" href="/rodeos/level/<?= e($e['level']) ?>/"><?= e(level_label($e['level'])) ?></a><?php endif; ?>
      <?php if ($e['region_name']): ?><a class="tag tag--region" href="/rodeos/region/<?= e($e['region_slug']) ?>/"><?= e($e['region_name']) ?></a><?php endif; ?>
    </div>
    <h1><?= e($e['title']) ?></h1>
    <p class="event-hero__when"><time datetime="<?= e($e['start_date']) ?>"><?= e($range) ?></time></p>
    <p class="event-hero__where"><?= e($placeLine) ?></p>
    <div class="event-actions">
      <button type="button" class="btn fav-btn fav-btn--wide" data-fav="<?= e($e['slug']) ?>" data-title="<?= e($e['title']) ?>" data-date="<?= e($e['start_date']) ?>" aria-pressed="false">
        <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z"/></svg><span data-fav-label>Save</span>
      </button>
      <a class="btn" href="<?= e($url) ?>calendar.ics" download>Add to calendar</a>
      <button type="button" class="btn" data-share data-share-title="<?= e($e['title']) ?>" data-share-url="<?= e(abs_url($url)) ?>">Share</button>
      <?php if ($e['ticket_url'] && $e['ticket_url_verified'] && in_array($status['key'], ['upcoming', 'ongoing'], true)): ?>
        <a class="btn btn--primary" href="<?= e($e['ticket_url']) ?>" rel="noopener" target="_blank">Tickets<span class="visually-hidden"> (opens the ticket seller's site)</span></a>
      <?php endif; ?>
    </div>
  </header>

  <?php if ($e['is_legacy']): ?>
    <div class="alert alert--info"><strong>Archived listing.</strong> <?= e($e['legacy_note']) ?> <a href="/rodeos/?q=<?= e(rawurlencode((string) $e['city'])) ?>">See upcoming rodeos<?= $e['city'] ? ' in ' . e($e['city']) : '' ?></a>.</div>
  <?php endif; ?>
  <?php if ($status['key'] === 'canceled'): ?>
    <div class="alert alert--danger" role="alert"><strong>This event has been canceled.</strong> <?= e($e['status_note']) ?></div>
  <?php elseif ($status['key'] === 'postponed'): ?>
    <div class="alert alert--warn" role="alert"><strong>This event has been postponed.</strong> <?= e($e['status_note'] ?: 'New dates have not been announced yet.') ?></div>
  <?php elseif ($status['key'] === 'completed' && !$e['is_legacy']): ?>
    <div class="alert alert--info">This event has ended. <a href="/rodeos/">Find upcoming rodeos</a>.</div>
  <?php endif; ?>

  <div class="event-layout">
    <div class="event-main">
      <section aria-labelledby="h-when">
        <h2 id="h-when">Dates &amp; show times</h2>
        <dl class="facts">
          <dt>Dates</dt><dd><?= e($range) ?></dd>
          <dt>Show times</dt>
          <dd>
            <?php if ($perfs): ?>
              <ul class="perf-list">
                <?php foreach ($perfs as $p): ?>
                  <li><time datetime="<?= e(Dates::iso($p['starts_at'], $e['timezone'])) ?>"><?= e(date('D, M j', strtotime($p['starts_at']))) ?> · <?= e(Dates::time($p['starts_at'], $e['timezone'])) ?></time><?= $p['ends_at'] ? ' – ' . e(Dates::time($p['ends_at'], $e['timezone'])) : '' ?><?= $p['label'] ? ' · ' . e($p['label']) : '' ?></li>
                <?php endforeach; ?>
              </ul>
              <?php if ($e['timezone'] !== 'America/Chicago'): ?><p class="fineprint">Times are local to the venue (Mountain Time).</p><?php endif; ?>
            <?php else: ?>
              <span class="muted">Performance times have not been published yet.</span>
            <?php endif; ?>
          </dd>
          <dt>Tickets &amp; prices</dt>
          <dd><?= $e['price_text'] ? e($e['price_text']) : $notListed ?>
            <?php if ($e['ticket_url'] && $e['ticket_url_verified']): ?><br><a href="<?= e($e['ticket_url']) ?>" rel="noopener" target="_blank">Official ticket link</a><?php endif; ?></dd>
        </dl>
      </section>

      <section aria-labelledby="h-where">
        <h2 id="h-where">Venue &amp; directions</h2>
        <dl class="facts">
          <dt>Venue</dt><dd><?= $e['venue_name'] ? e($e['venue_name']) : '<span class="muted">Venue not listed.</span>' ?></dd>
          <dt>Address</dt>
          <dd><?php if ($e['venue_address'] || $e['city']): ?>
              <address><?= $e['venue_address'] ? e($e['venue_address']) . '<br>' : '' ?><?= e(trim(($e['city'] ?? '') . ', TX ' . ($e['postal_code'] ?? ''))) ?></address>
            <?php else: ?><span class="muted">Not listed.</span><?php endif; ?></dd>
          <dt>Parking</dt><dd><?= $parking ? nl2br(e($parking)) : $notListed ?></dd>
          <dt>Accessibility</dt><dd><?= $access ? nl2br(e($access)) : $notListed ?></dd>
        </dl>
        <?php if ($directions && !$e['is_legacy']): ?><p><a class="btn" href="<?= e($directions) ?>" rel="noopener" target="_blank">Get directions</a></p><?php endif; ?>
        <?php if ($e['lat'] !== null && !$e['is_legacy']): ?>
          <div class="mini-map" data-mini-map data-lat="<?= e($e['lat']) ?>" data-lng="<?= e($e['lng']) ?>" data-precise="<?= $e['location_precision'] === 'address' ? '1' : '0' ?>"
               data-tiles="<?= e((string) cfg('map.tile_url')) ?>" data-attribution="<?= e((string) cfg('map.attribution')) ?>" data-label="<?= e($placeLine) ?>" role="img" aria-label="Map showing <?= e($placeLine) ?>"></div>
          <?php if ($e['location_precision'] !== 'address'): ?><p class="fineprint">Map shows the city center; the exact venue location is not listed.</p><?php endif; ?>
        <?php endif; ?>
      </section>

      <?php if ($e['description']): ?>
      <section aria-labelledby="h-about">
        <h2 id="h-about">About this event</h2>
        <div class="prose"><?= nl2br(e($e['description'])) ?></div>
      </section>
      <?php endif; ?>

      <?php if ($related): ?>
      <section aria-labelledby="h-related">
        <h2 id="h-related">Related competitions</h2>
        <p class="fineprint">Separate competitions held alongside this event.</p>
        <div class="event-list event-list--compact"><?php foreach ($related as $r) { echo View::eventCard($r, true); } ?></div>
      </section>
      <?php endif; ?>
    </div>

    <aside class="event-side">
      <div class="side-card">
        <h2>Official information</h2>
        <ul class="link-list">
          <li><?= $e['official_url'] ? '<a href="' . e($e['official_url']) . '" rel="noopener" target="_blank">Official website</a>' : '<span class="muted">Official website not listed</span>' ?></li>
          <?php if ($e['org_name']): ?>
            <li><strong>Organizer:</strong> <?= $e['org_website'] ? '<a href="' . e($e['org_website']) . '" rel="noopener" target="_blank">' . e($e['org_name']) . '</a>' : e($e['org_name']) ?>
              <?= $e['org_phone'] ? '<br><a href="tel:' . e(preg_replace('/[^0-9+]/', '', $e['org_phone'])) . '">' . e($e['org_phone']) . '</a>' : '' ?>
              <?= $e['org_email'] ? '<br><a href="mailto:' . e($e['org_email']) . '">' . e($e['org_email']) . '</a>' : '' ?></li>
          <?php else: ?>
            <li><span class="muted">Organizer not listed</span></li>
          <?php endif; ?>
        </ul>
      </div>
      <div class="side-card side-card--source">
        <h2>Source &amp; verification</h2>
        <p><strong>Information source:</strong>
          <?= $e['source_url'] ? '<a href="' . e($e['source_url']) . '" rel="noopener nofollow" target="_blank">' . e($e['source_label'] ?: 'Organizer listing') . '</a>' : e($e['source_label'] ?: 'Rodeo Texas editors') ?></p>
        <p><strong>Last verified:</strong>
          <?= $e['last_verified_at'] ? '<time datetime="' . e(gmdate('c', strtotime($e['last_verified_at'] . ' UTC'))) . '">' . e(date('M j, Y', strtotime($e['last_verified_at'] . ' UTC'))) . '</time>' : '<span class="muted">Not verified</span>' ?></p>
        <p class="fineprint">Rodeo schedules change. Please confirm with the organizer before you travel.</p>
        <p><a href="<?= e($url) ?>report/">Report a correction</a></p>
      </div>
    </aside>
  </div>

  <?php if ($nearby): ?>
  <section class="section" aria-labelledby="h-nearby">
    <h2 id="h-nearby">More upcoming rodeos nearby</h2>
    <div class="event-list"><?php foreach ($nearby as $n) { echo View::eventCard($n); } ?></div>
  </section>
  <?php endif; ?>
</article>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
