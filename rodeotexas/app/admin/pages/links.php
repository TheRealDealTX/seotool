<?php
declare(strict_types=1);

use RT\Dates;
use RT\Db;
use RT\LinkChecker;

if (is_post() && ($_POST['action'] ?? '') === 'check') {
    @set_time_limit(300);
    $r = LinkChecker::run(25, 24);
    flash("Checked {$r['checked']} link(s); {$r['broken']} broken. Run again to continue.");
    redirect(admin_url('links'), 303);
}
$today = Dates::today();
$events = Db::all("SELECT e.id, e.title, e.start_date, e.official_url, e.ticket_url, e.ticket_url_verified, e.price_text,
        COALESCE(e.parking_info, v.parking_info) AS parking, COALESCE(e.accessibility_info, v.accessibility_info) AS access,
        e.organizer_id, e.last_verified_at, v.address, v.city,
        (SELECT COUNT(*) FROM performances p WHERE p.event_id = e.id) AS perfs
    FROM events e LEFT JOIN venues v ON v.id = e.venue_id
    WHERE e.publish_state = 'published' AND e.end_date >= ? ORDER BY e.start_date LIMIT 300", [$today]);
$checks = [];
foreach (Db::all('SELECT url, ok, http_status, error, last_checked_at FROM link_checks') as $c) {
    $checks[$c['url']] = $c;
}
$broken = array_filter($checks, static fn($c) => !(int) $c['ok']);
$stale = gmdate('Y-m-d H:i:s', time() - 86400 * 45);
admin_header('Links & missing information');
?>
<section class="card">
  <h2>Link check</h2>
  <p class="small">Checks official and ticket links of upcoming events (25 per click; results cached for 24 h). <?= count($checks) ?> links checked so far, <?= count($broken) ?> broken.</p>
  <form method="post"><?= RT\Auth::csrfField() ?><input type="hidden" name="action" value="check"><button class="btn btn--primary">Check links now</button></form>
  <?php if ($broken): ?>
    <table class="table small"><thead><tr><th>Broken URL</th><th>Result</th><th>Checked</th></tr></thead><tbody>
      <?php foreach ($broken as $u => $c): ?><tr><td><a href="<?= e($u) ?>" rel="noopener noreferrer" target="_blank"><?= e(excerpt($u, 80)) ?></a></td><td><?= e($c['http_status'] ?: $c['error']) ?></td><td><?= e(fmt_dt($c['last_checked_at'], 'M j')) ?></td></tr><?php endforeach; ?>
    </tbody></table>
  <?php endif; ?>
</section>

<section class="card">
  <h2>Upcoming events: what's missing</h2>
  <p class="small">✗ = not listed (shown publicly as “Not listed”). Never fill these in without an official source.</p>
  <table class="table small">
    <thead><tr><th>Date</th><th>Event</th><th>Address</th><th>Times</th><th>Official</th><th>Tickets</th><th>Price</th><th>Parking</th><th>Access.</th><th>Organizer</th><th>Verified</th></tr></thead>
    <tbody>
    <?php
    $mark = static fn($ok) => $ok ? '✓' : '<span class="bad">✗</span>';
    foreach ($events as $ev):
        $linkState = static function (?string $u) use ($checks, $mark): string {
            if (!$u) { return $mark(false); }
            if (isset($checks[$u]) && !(int) $checks[$u]['ok']) { return '<span class="bad" title="Link is broken">broken</span>'; }
            return $mark(true);
        };
    ?>
      <tr>
        <td class="nowrap"><?= e($ev['start_date']) ?></td>
        <td><a href="<?= e(admin_url('event', ['id' => $ev['id']])) ?>"><?= e($ev['title']) ?></a></td>
        <td><?= $mark((bool) $ev['address']) ?></td>
        <td><?= $mark($ev['perfs'] > 0) ?></td>
        <td><?= $linkState($ev['official_url']) ?></td>
        <td><?= $ev['ticket_url'] ? ($ev['ticket_url_verified'] ? $linkState($ev['ticket_url']) : '<span class="warn" title="Not verified, hidden publicly">unverified</span>') : $mark(false) ?></td>
        <td><?= $mark((bool) $ev['price_text']) ?></td>
        <td><?= $mark((bool) $ev['parking']) ?></td>
        <td><?= $mark((bool) $ev['access']) ?></td>
        <td><?= $mark((bool) $ev['organizer_id']) ?></td>
        <td class="nowrap"><?= $ev['last_verified_at'] && $ev['last_verified_at'] > $stale ? e(fmt_dt($ev['last_verified_at'], 'M j')) : '<span class="warn">' . e(fmt_dt($ev['last_verified_at'], 'M j')) . '</span>' ?></td>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table>
</section>
<?php
admin_footer();
