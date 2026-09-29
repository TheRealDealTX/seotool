<?php
declare(strict_types=1);

use RT\Db;
use RT\Geo;

if (is_post() && ($_POST['action'] ?? '') === 'geocode_missing') {
    Geo::$budget = 25;
    $n = Geo::backfillVenues(25);
    flash("Located {$n} venue(s) with OpenStreetMap.");
    redirect(admin_url('venues'), 303);
}
$q = clean_str($_GET['q'] ?? null, 80);
$p = [];
$where = '1=1';
if ($q) {
    $where = '(v.name LIKE :a OR v.city LIKE :b OR v.postal_code LIKE :c)';
    $like = '%' . addcslashes($q, '%_\\') . '%';
    $p = ['a' => $like, 'b' => $like, 'c' => $like];
}
$rows = Db::all("SELECT v.*, r.name AS region, (SELECT COUNT(*) FROM events e WHERE e.venue_id = v.id) AS n FROM venues v LEFT JOIN regions r ON r.id = v.region_id WHERE {$where} ORDER BY v.city, v.name LIMIT 300", $p);
$missing = (int) Db::val("SELECT COUNT(*) FROM venues WHERE location_precision = 'none'");
admin_header('Venues');
?>
<form class="toolbar" method="get"><input type="hidden" name="page" value="venues"><input type="search" name="q" value="<?= e($q) ?>" placeholder="Name, city or ZIP" aria-label="Search venues"><button class="btn">Search</button></form>
<?php if ($missing): ?>
<form method="post" class="toolbar"><?= RT\Auth::csrfField() ?><input type="hidden" name="action" value="geocode_missing"><span><?= $missing ?> venue(s) without map coordinates.</span><button class="btn">Locate up to 25 now</button></form>
<?php endif; ?>
<table class="table"><thead><tr><th>Venue</th><th>City</th><th>ZIP</th><th>Region</th><th>Time zone</th><th>Map</th><th>Events</th></tr></thead><tbody>
<?php foreach ($rows as $v): ?>
  <tr><td><a href="<?= e(admin_url('venue', ['id' => $v['id']])) ?>"><?= e($v['name'] ?: '(venue not listed)') ?></a><?= $v['manually_edited'] ? ' <span class="pill">edited</span>' : '' ?></td>
    <td><?= e($v['city']) ?></td><td><?= e($v['postal_code']) ?></td><td><?= e($v['region']) ?></td><td><?= e(str_replace('America/', '', $v['timezone'])) ?></td>
    <td><?= e($v['location_precision']) ?></td><td><?= (int) $v['n'] ?></td></tr>
<?php endforeach; ?>
</tbody></table>
<?php
admin_footer();
