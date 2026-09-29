<?php
declare(strict_types=1);

use RT\Dates;
use RT\Db;
use RT\Importer;

// Manual "Run import" (all enabled automatic sources).
if (is_post() && ($_POST['action'] ?? '') === 'run_import') {
    ignore_user_abort(true);
    @set_time_limit(600);
    $r = Importer::run('manual', 'weekly', null, null, $admin['email']);
    if ($r['status'] === 'locked') {
        flash($r['message'], 'warning');
    } else {
        flash('Import #' . $r['run_id'] . ' finished (' . $r['status'] . '): ' . $r['message'], $r['status'] === 'success' ? 'success' : 'warning');
    }
    redirect(admin_url('imports', ['id' => $r['run_id']]), 303);
}

$today = Dates::today();
$stats = [
    'Upcoming published' => (int) Db::val("SELECT COUNT(*) FROM events WHERE publish_state = 'published' AND end_date >= ?", [$today]),
    'Drafts' => (int) Db::val("SELECT COUNT(*) FROM events WHERE publish_state = 'draft'"),
    'Open review items' => (int) Db::val("SELECT COUNT(*) FROM review_items WHERE status = 'open'"),
    'Articles' => (int) Db::val("SELECT COUNT(*) FROM articles WHERE status = 'published'"),
];
$byKind = Db::all("SELECT kind, COUNT(*) n FROM review_items WHERE status = 'open' GROUP BY kind");
$lastRun = Db::one('SELECT * FROM import_runs ORDER BY id DESC LIMIT 1');
$failing = Db::all("SELECT id, name, last_error, consecutive_failures FROM sources WHERE enabled = 1 AND consecutive_failures > 0");
$running = Importer::isRunning();
$soon = Db::all("SELECT slug, title, start_date, status FROM events WHERE publish_state = 'published' AND end_date >= ? AND start_date <= DATE_ADD(?, INTERVAL 14 DAY) ORDER BY start_date LIMIT 15", [$today, $today]);

admin_header('Dashboard');
?>
<div class="stats"><?php foreach ($stats as $k => $v): ?><div class="stat"><span class="stat__n"><?= $v ?></span><span class="stat__l"><?= e($k) ?></span></div><?php endforeach; ?></div>

<?php if ($failing): ?>
  <div class="alert alert--danger"><strong>Source problems:</strong>
    <ul><?php foreach ($failing as $s): ?><li><a href="<?= e(admin_url('source', ['id' => $s['id']])) ?>"><?= e($s['name']) ?></a> — failed <?= (int) $s['consecutive_failures'] ?>× in a row: <?= e(excerpt($s['last_error'], 200)) ?></li><?php endforeach; ?></ul>
    Existing events from these sources were left unchanged.</div>
<?php endif; ?>

<div class="grid2">
  <section class="card">
    <h2>Event import</h2>
    <p>Last run: <?= $lastRun ? '<a href="' . e(admin_url('imports', ['id' => $lastRun['id']])) . '">#' . (int) $lastRun['id'] . '</a> ' . status_pill($lastRun['status']) . ' ' . e(fmt_dt($lastRun['started_at'])) : 'never' ?></p>
    <?php if ($lastRun && $lastRun['message']): ?><p class="small"><?= e($lastRun['message']) ?></p><?php endif; ?>
    <p class="small">Automatic runs: Mondays at 7:00 AM Central (cron). Manual runs use the same safety checks and never overlap a running import.</p>
    <form method="post" data-confirm="Run the import for all enabled sources now? It can take a few minutes.">
      <?= RT\Auth::csrfField() ?><input type="hidden" name="action" value="run_import">
      <button class="btn btn--primary" type="submit"<?= $running ? ' disabled' : '' ?>><?= $running ? 'Import running…' : 'Run import now' ?></button>
    </form>
  </section>
  <section class="card">
    <h2>Review queue</h2>
    <?php if ($byKind): ?>
      <ul><?php foreach ($byKind as $k): ?><li><a href="<?= e(admin_url('review', ['kind' => $k['kind']])) ?>"><?= e(str_replace('_', ' ', $k['kind'])) ?></a>: <?= (int) $k['n'] ?></li><?php endforeach; ?></ul>
    <?php else: ?><p>Nothing waiting. 🎉</p><?php endif; ?>
  </section>
</div>

<section class="card">
  <h2>Next 14 days</h2>
  <?php if ($soon): ?>
    <table class="table"><thead><tr><th>Dates</th><th>Event</th><th>Status</th></tr></thead><tbody>
      <?php foreach ($soon as $ev): ?><tr><td><?= e($ev['start_date']) ?></td><td><a href="/rodeos/<?= e($ev['slug']) ?>/" target="_blank" rel="noopener"><?= e($ev['title']) ?></a></td><td><?= status_pill($ev['status']) ?></td></tr><?php endforeach; ?>
    </tbody></table>
  <?php else: ?><p>No published events in the next two weeks.</p><?php endif; ?>
  <p><a class="btn" href="<?= e(admin_url('event', ['id' => 'new'])) ?>">+ Add an event</a></p>
</section>
<?php
admin_footer();
