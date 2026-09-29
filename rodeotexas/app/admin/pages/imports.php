<?php
declare(strict_types=1);

use RT\Db;

$id = (int) ($_GET['id'] ?? 0);
if ($id) {
    $run = Db::one('SELECT * FROM import_runs WHERE id = ?', [$id]);
    if (!$run) {
        redirect(admin_url('imports'));
    }
    $level = in_array($_GET['level'] ?? '', ['info', 'warning', 'error'], true) ? $_GET['level'] : '';
    $logs = Db::all('SELECT l.*, s.name AS source FROM import_logs l LEFT JOIN sources s ON s.id = l.source_id WHERE l.run_id = :rid'
        . ($level ? ' AND l.level = :lvl' : '') . ' ORDER BY l.id', $level ? ['rid' => $id, 'lvl' => $level] : ['rid' => $id]);
    admin_header('Import run #' . $id);
    $stats = json_decode((string) $run['stats'], true) ?: [];
    ?>
    <p><a href="<?= e(admin_url('imports')) ?>">← All runs</a></p>
    <section class="card">
      <p><?= status_pill($run['status']) ?> · <?= e($run['trigger_type']) ?> / <?= e($run['mode']) ?> · started <?= e(fmt_dt($run['started_at'])) ?> · finished <?= e(fmt_dt($run['finished_at'])) ?><?= $run['started_by'] ? ' · by ' . e($run['started_by']) : '' ?></p>
      <p><?= e($run['message']) ?></p>
      <?php if ($stats): ?><div class="stats small"><?php foreach ($stats as $k => $n): ?><div class="stat"><span class="stat__n"><?= (int) $n ?></span><span class="stat__l"><?= e(str_replace('_', ' ', $k)) ?></span></div><?php endforeach; ?></div><?php endif; ?>
    </section>
    <nav class="tabs"><?php foreach (['' => 'All', 'info' => 'Info', 'warning' => 'Warnings', 'error' => 'Errors'] as $k => $l): ?><a href="<?= e(admin_url('imports', array_filter(['id' => $id, 'level' => $k]))) ?>"<?= $level === $k ? ' aria-current="page"' : '' ?>><?= $l ?></a><?php endforeach; ?></nav>
    <table class="table small"><thead><tr><th>Time</th><th>Level</th><th>Source</th><th>Message</th></tr></thead><tbody>
    <?php foreach ($logs as $l): ?><tr class="log--<?= e($l['level']) ?>"><td class="nowrap"><?= e(fmt_dt($l['created_at'], 'g:i:s A')) ?></td><td><?= e($l['level']) ?></td><td><?= e($l['source']) ?></td><td><?= e($l['message']) ?></td></tr><?php endforeach; ?>
    </tbody></table>
    <?php
    admin_footer();
    return;
}
$runs = Db::all('SELECT * FROM import_runs ORDER BY id DESC LIMIT 100');
admin_header('Import history');
?>
<form method="post" action="<?= e(admin_url('dashboard')) ?>" data-confirm="Run the import for all enabled sources now?">
  <?= RT\Auth::csrfField() ?><input type="hidden" name="action" value="run_import"><button class="btn btn--primary" type="submit"<?= RT\Importer::isRunning() ? ' disabled' : '' ?>>Run import now</button>
</form>
<table class="table"><thead><tr><th>#</th><th>Started (Central)</th><th>Trigger</th><th>Status</th><th>Summary</th></tr></thead><tbody>
<?php foreach ($runs as $r): ?><tr><td><a href="<?= e(admin_url('imports', ['id' => $r['id']])) ?>"><?= (int) $r['id'] ?></a></td><td class="nowrap"><?= e(fmt_dt($r['started_at'])) ?></td><td><?= e($r['trigger_type'] . ' / ' . $r['mode']) ?></td><td><?= status_pill($r['status']) ?></td><td class="small"><?= e(excerpt($r['message'], 220)) ?></td></tr><?php endforeach; ?>
</tbody></table>
<?php
admin_footer();
