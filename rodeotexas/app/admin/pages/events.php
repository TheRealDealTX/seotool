<?php
declare(strict_types=1);

use RT\Dates;
use RT\Db;

$q = clean_str($_GET['q'] ?? null, 100);
$state = in_array($_GET['state'] ?? '', ['draft', 'published', 'archived'], true) ? $_GET['state'] : '';
$when = in_array($_GET['when'] ?? '', ['upcoming', 'past', 'all'], true) ? $_GET['when'] : 'upcoming';
$legacy = ($_GET['legacy'] ?? '') === '1';
$pageNo = max(1, (int) ($_GET['p'] ?? 1));
$per = 50;

// Bulk actions
if (is_post() && in_array($_POST['bulk'] ?? '', ['publish', 'draft', 'archive'], true)) {
    $ids = array_values(array_filter(array_map('intval', (array) ($_POST['ids'] ?? []))));
    $newState = ['publish' => 'published', 'draft' => 'draft', 'archive' => 'archived'][$_POST['bulk']];
    foreach ($ids as $id) {
        $cur = Db::one('SELECT id, publish_state, locked_fields FROM events WHERE id = ?', [$id]);
        if ($cur && $cur['publish_state'] !== $newState) {
            $locked = json_decode((string) $cur['locked_fields'], true) ?: [];
            $locked[] = 'publish_state';
            Db::update('events', ['publish_state' => $newState, 'locked_fields' => json_encode(array_values(array_unique($locked))), 'updated_at' => now_utc()], 'id = :id', ['id' => $id]);
            RT\Importer::history($id, 'admin:' . $admin['id'], 'publish_state', $cur['publish_state'], $newState);
        }
    }
    flash(count($ids) . ' event(s) set to ' . $newState . '.');
    redirect($_SERVER['REQUEST_URI'], 303);
}

$w = ['1=1'];
$p = [];
$today = Dates::today();
if ($when === 'upcoming') { $w[] = 'e.end_date >= :today'; $p['today'] = $today; }
if ($when === 'past') { $w[] = 'e.end_date < :today'; $p['today'] = $today; }
if ($state) { $w[] = 'e.publish_state = :state'; $p['state'] = $state; }
if (!$legacy) { $w[] = 'e.is_legacy = 0'; }
if ($q) {
    $w[] = '(e.title LIKE :q1 OR v.city LIKE :q2 OR v.name LIKE :q3 OR e.slug LIKE :q4)';
    $like = '%' . addcslashes($q, '%_\\') . '%';
    $p += ['q1' => $like, 'q2' => $like, 'q3' => $like, 'q4' => $like];
}
$where = implode(' AND ', $w);
$total = (int) Db::val("SELECT COUNT(*) FROM events e LEFT JOIN venues v ON v.id = e.venue_id WHERE {$where}", $p);
$rows = Db::all("SELECT e.id, e.slug, e.title, e.start_date, e.end_date, e.status, e.publish_state, e.is_legacy, e.source_label, e.last_verified_at, e.locked_fields, v.city
    FROM events e LEFT JOIN venues v ON v.id = e.venue_id WHERE {$where} ORDER BY e.start_date " . ($when === 'past' ? 'DESC' : 'ASC') . " LIMIT {$per} OFFSET " . (($pageNo - 1) * $per), $p);

admin_header('Events');
?>
<form class="toolbar" method="get">
  <input type="hidden" name="page" value="events">
  <input type="search" name="q" value="<?= e($q) ?>" placeholder="Search title, city, venue" aria-label="Search">
  <select name="when" aria-label="When"><?php foreach (['upcoming' => 'Upcoming & ongoing', 'past' => 'Past', 'all' => 'All dates'] as $k => $l): ?><option value="<?= $k ?>"<?= $when === $k ? ' selected' : '' ?>><?= $l ?></option><?php endforeach; ?></select>
  <select name="state" aria-label="State"><option value="">Any state</option><?php foreach (['published', 'draft', 'archived'] as $s): ?><option<?= $state === $s ? ' selected' : '' ?>><?= $s ?></option><?php endforeach; ?></select>
  <label class="check"><input type="checkbox" name="legacy" value="1"<?= $legacy ? ' checked' : '' ?>> include legacy</label>
  <button class="btn" type="submit">Filter</button>
  <a class="btn btn--primary" href="<?= e(admin_url('event', ['id' => 'new'])) ?>">+ New event</a>
</form>
<p class="small"><?= $total ?> event(s)</p>
<form method="post">
  <?= RT\Auth::csrfField() ?>
  <table class="table">
    <thead><tr><th><span class="visually-hidden">Select</span></th><th>Dates</th><th>Event</th><th>City</th><th>State</th><th>Status</th><th>Source</th><th>Verified</th></tr></thead>
    <tbody>
    <?php foreach ($rows as $r): ?>
      <tr>
        <td><input type="checkbox" name="ids[]" value="<?= (int) $r['id'] ?>" aria-label="Select <?= e($r['title']) ?>"></td>
        <td class="nowrap"><?= e($r['start_date']) ?><?= $r['end_date'] !== $r['start_date'] ? '<br><span class="small">to ' . e($r['end_date']) . '</span>' : '' ?></td>
        <td><a href="<?= e(admin_url('event', ['id' => $r['id']])) ?>"><?= e($r['title']) ?></a><?= $r['is_legacy'] ? ' <span class="pill">legacy</span>' : '' ?><?= $r['locked_fields'] && $r['locked_fields'] !== '[]' ? ' <span class="pill" title="Has manually locked fields">🔒</span>' : '' ?></td>
        <td><?= e($r['city']) ?></td>
        <td><?= status_pill($r['publish_state']) ?></td>
        <td><?= status_pill($r['status']) ?></td>
        <td class="small"><?= e($r['source_label']) ?></td>
        <td class="small nowrap"><?= e(fmt_dt($r['last_verified_at'], 'M j, Y')) ?></td>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table>
  <div class="toolbar">
    <label for="bulk">With selected:</label>
    <select id="bulk" name="bulk"><option value="">—</option><option value="publish">Publish</option><option value="draft">Unpublish (draft)</option><option value="archive">Archive</option></select>
    <button class="btn" type="submit">Apply</button>
  </div>
</form>
<?php if ($total > $per): ?>
<nav class="pager"><?php for ($i = 1; $i <= (int) ceil($total / $per); $i++): ?><a<?= $i === $pageNo ? ' aria-current="page"' : '' ?> href="<?= e(admin_url('events', array_filter(['q' => $q, 'when' => $when, 'state' => $state, 'legacy' => $legacy ? 1 : null, 'p' => $i]))) ?>"><?= $i ?></a><?php endfor; ?></nav>
<?php endif; ?>
<?php
admin_footer();
