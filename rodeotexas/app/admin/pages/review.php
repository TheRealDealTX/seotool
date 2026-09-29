<?php
declare(strict_types=1);

use RT\Db;
use RT\Importer;

$kinds = ['submission' => 'Event submissions', 'correction' => 'Correction reports', 'contact' => 'Contact messages',
    'import_conflict' => 'Import conflicts', 'import_ambiguous' => 'Possible duplicates / unclear location', 'import_incomplete' => 'Incomplete imported events'];
$id = (int) ($_GET['id'] ?? 0);

if (is_post() && $id) {
    $item = Db::one('SELECT * FROM review_items WHERE id = ?', [$id]);
    if (!$item) {
        redirect(admin_url('review'));
    }
    $pl = json_decode((string) $item['payload'], true) ?: [];
    $note = post_str('note', 500);
    $action = (string) ($_POST['action'] ?? '');
    $resolve = static function (string $status, string $msg) use ($id, $admin, $note): void {
        Db::update('review_items', ['status' => $status, 'resolved_at' => now_utc(), 'resolved_by' => (int) $admin['id'], 'resolution_note' => $note ?? $msg], 'id = :id', ['id' => $id]);
        flash($msg);
    };
    switch ($action) {
        case 'create_event':          // submission → open a prefilled new-event form
            redirect(admin_url('event', ['id' => 'new', 'from_review' => $id]), 303);
        case 'apply_incoming':        // import conflict → accept the source's value (field stays locked)
            $ev = Db::one('SELECT * FROM events WHERE id = ?', [$item['event_id']]);
            if ($ev && isset($pl['field'])) {
                $f = $pl['field'];
                if ($f === 'performances') {
                    Importer::replacePerformances((int) $ev['id'], json_decode((string) $pl['incoming'], true) ?: []);
                } elseif (in_array($f, RT\EventAdmin::LOCKABLE, true) || $f === 'source_url') {
                    Db::update('events', [$f => $pl['incoming'], 'updated_at' => now_utc(), 'last_verified_at' => now_utc()], 'id = :id', ['id' => $ev['id']]);
                }
                Importer::history((int) $ev['id'], 'admin:' . $admin['id'], $f, is_scalar($pl['current']) ? (string) $pl['current'] : json_encode($pl['current']), is_scalar($pl['incoming']) ? (string) $pl['incoming'] : json_encode($pl['incoming']));
            }
            $resolve('approved', 'Incoming value applied.');
            break;
        case 'keep_current':
            $resolve('rejected', 'Kept the current value.');
            break;
        case 'link':                  // ambiguous import → link to a chosen existing event
            $target = post_int('event_id');
            if ($target && $item['source_record_id']) {
                Importer::linkSourceRecord((int) $item['source_record_id'], $target);
                Db::update('review_items', ['event_id' => $target], 'id = :id', ['id' => $id]);
                $resolve('approved', 'Linked to event #' . $target . '.');
            } else {
                flash('Enter a valid event ID.', 'danger');
            }
            break;
        case 'create_from_record':    // ambiguous/no-location import → new draft event
            if ($item['source_record_id']) {
                $newId = Importer::createDraftFromSourceRecord((int) $item['source_record_id']);
                Db::update('review_items', ['event_id' => $newId], 'id = :id', ['id' => $id]);
                $resolve('approved', 'Draft event #' . $newId . ' created — complete and publish it.');
                redirect(admin_url('event', ['id' => $newId]), 303);
            }
            break;
        case 'resolve':
            $resolve('resolved', 'Marked as resolved.');
            break;
        case 'reject':
            if ($item['source_record_id']) {
                Db::update('source_records', ['state' => 'skipped', 'skip_reason' => 'rejected by admin'], 'id = :id', ['id' => $item['source_record_id']]);
            }
            $resolve('rejected', 'Rejected.');
            break;
        case 'reopen':
            Db::update('review_items', ['status' => 'open', 'resolved_at' => null, 'resolved_by' => null], 'id = :id', ['id' => $id]);
            flash('Reopened.');
            break;
    }
    redirect(admin_url('review', ['id' => $id]), 303);
}

if ($id) {
    $item = Db::one('SELECT r.*, e.title AS event_title, e.slug AS event_slug FROM review_items r LEFT JOIN events e ON e.id = r.event_id WHERE r.id = ?', [$id]);
    if (!$item) {
        redirect(admin_url('review'));
    }
    $pl = json_decode((string) $item['payload'], true) ?: [];
    admin_header('Review: ' . ($kinds[$item['kind']] ?? $item['kind']));
    ?>
    <p><a href="<?= e(admin_url('review', ['kind' => $item['kind']])) ?>">← Back to the queue</a></p>
    <section class="card">
      <h2><?= e($item['summary']) ?></h2>
      <p><?= status_pill($item['status']) ?> · received <?= e(fmt_dt($item['created_at'])) ?>
        <?= $item['submitter_email'] ? ' · from ' . e($item['submitter_name'] ?: '') . ' &lt;<a href="mailto:' . e($item['submitter_email']) . '">' . e($item['submitter_email']) . '</a>&gt;' : '' ?></p>
      <?php if ($item['event_id']): ?><p>Event: <a href="<?= e(admin_url('event', ['id' => $item['event_id']])) ?>">#<?= (int) $item['event_id'] ?> <?= e($item['event_title']) ?></a> · <a href="/rodeos/<?= e($item['event_slug']) ?>/" target="_blank" rel="noopener">public page ↗</a></p><?php endif; ?>
      <?php if (!empty($pl['problem'])): ?><div class="alert alert--warning"><?= e($pl['problem']) ?></div><?php endif; ?>

      <?php if ($item['kind'] === 'import_conflict'): ?>
        <table class="table"><tr><th>Field</th><td><code><?= e($pl['field'] ?? '') ?></code></td></tr>
          <tr><th>Current value</th><td><pre><?= e(is_scalar($pl['current'] ?? null) ? (string) $pl['current'] : json_encode($pl['current'] ?? null, JSON_PRETTY_PRINT)) ?></pre></td></tr>
          <tr><th>Incoming (<?= e($pl['source'] ?? '') ?>)</th><td><pre><?= e(is_scalar($pl['incoming'] ?? null) ? (string) $pl['incoming'] : json_encode($pl['incoming'] ?? null, JSON_PRETTY_PRINT)) ?></pre></td></tr></table>
      <?php elseif (isset($pl['record'])): $r = $pl['record']; ?>
        <table class="table">
          <tr><th>Title</th><td><?= e($r['title']) ?></td></tr>
          <tr><th>Dates</th><td><?= e($r['start_date']) ?> – <?= e($r['end_date']) ?></td></tr>
          <tr><th>Venue</th><td><?= e(implode(', ', array_filter((array) ($r['venue'] ?? []), 'is_string'))) ?: '<em>not stated</em>' ?></td></tr>
          <tr><th>Links</th><td><?= e(implode(' · ', array_filter([$r['official_url'] ?? null, $r['source_url'] ?? null]))) ?></td></tr>
          <tr><th>Source</th><td><?= e($pl['source'] ?? '') ?></td></tr>
        </table>
        <?php if (!empty($pl['candidates'])): ?>
          <p>Possible existing matches:</p>
          <ul><?php foreach ($pl['candidates'] as $c): ?><li>#<?= (int) $c['id'] ?> <a href="<?= e(admin_url('event', ['id' => $c['id']])) ?>"><?= e($c['title']) ?></a> — <?= e($c['start_date']) ?>, <?= e($c['city'] ?? '?') ?></li><?php endforeach; ?></ul>
        <?php endif; ?>
      <?php else: ?>
        <table class="table"><?php foreach ($pl as $k => $v): if ($v === null || $v === '' || $v === []) { continue; } ?>
          <tr><th><?= e(ucfirst(str_replace('_', ' ', (string) $k))) ?></th><td><?= preg_match('~^https?://~', (string) (is_scalar($v) ? $v : '')) ? '<a href="' . e($v) . '" rel="noopener noreferrer" target="_blank">' . e($v) . '</a>' : nl2br(e(is_scalar($v) ? (string) $v : json_encode($v))) ?></td></tr>
        <?php endforeach; ?></table>
      <?php endif; ?>
    </section>

    <?php if ($item['status'] === 'open'): ?>
    <section class="card">
      <h2>Actions</h2>
      <form method="post" class="actions-row">
        <?= RT\Auth::csrfField() ?>
        <?= f_text('note', 'Note (optional, internal)', '') ?>
        <?php if ($item['kind'] === 'submission'): ?>
          <button class="btn btn--primary" name="action" value="create_event">Create event from this submission…</button>
          <button class="btn" name="action" value="reject" data-confirm="Reject this submission?">Reject</button>
        <?php elseif ($item['kind'] === 'import_conflict'): ?>
          <button class="btn btn--primary" name="action" value="apply_incoming">Apply incoming value</button>
          <button class="btn" name="action" value="keep_current">Keep current value</button>
        <?php elseif ($item['kind'] === 'import_ambiguous'): ?>
          <?= f_text('event_id', 'Same event as existing event ID', $pl['candidates'][0]['id'] ?? '') ?>
          <button class="btn btn--primary" name="action" value="link">Link to that event</button>
          <button class="btn" name="action" value="create_from_record">It's a different event — create draft</button>
          <button class="btn" name="action" value="reject">Ignore this record</button>
        <?php elseif ($item['kind'] === 'import_incomplete'): ?>
          <a class="btn btn--primary" href="<?= e(admin_url('event', ['id' => $item['event_id']])) ?>">Complete &amp; publish the event…</a>
          <button class="btn" name="action" value="resolve">Mark resolved</button>
          <button class="btn" name="action" value="reject">Not a Texas rodeo — reject</button>
        <?php else: ?>
          <?php if ($item['event_id']): ?><a class="btn btn--primary" href="<?= e(admin_url('event', ['id' => $item['event_id']])) ?>">Edit the event…</a><?php endif; ?>
          <button class="btn" name="action" value="resolve">Mark resolved</button>
          <button class="btn" name="action" value="reject">Dismiss</button>
        <?php endif; ?>
      </form>
    </section>
    <?php else: ?>
      <form method="post"><?= RT\Auth::csrfField() ?><p class="small">Resolved <?= e(fmt_dt($item['resolved_at'])) ?><?= $item['resolution_note'] ? ' — ' . e($item['resolution_note']) : '' ?></p><button class="btn" name="action" value="reopen">Reopen</button></form>
    <?php endif; ?>
    <?php
    admin_footer();
    return;
}

$kind = array_key_exists($_GET['kind'] ?? '', $kinds) ? $_GET['kind'] : '';
$status = in_array($_GET['status'] ?? 'open', ['open', 'approved', 'rejected', 'resolved', 'all'], true) ? ($_GET['status'] ?? 'open') : 'open';
$w = ['1=1']; $p = [];
if ($kind) { $w[] = 'kind = :kind'; $p['kind'] = $kind; }
if ($status !== 'all') { $w[] = 'status = :status'; $p['status'] = $status; }
$rows = Db::all('SELECT * FROM review_items WHERE ' . implode(' AND ', $w) . ' ORDER BY created_at DESC LIMIT 200', $p);
$counts = [];
foreach (Db::all("SELECT kind, COUNT(*) n FROM review_items WHERE status = 'open' GROUP BY kind") as $c) { $counts[$c['kind']] = (int) $c['n']; }

admin_header('Review queue');
?>
<nav class="tabs"><a href="<?= e(admin_url('review', ['status' => $status])) ?>"<?= !$kind ? ' aria-current="page"' : '' ?>>All</a>
  <?php foreach ($kinds as $k => $l): ?><a href="<?= e(admin_url('review', ['kind' => $k, 'status' => $status])) ?>"<?= $kind === $k ? ' aria-current="page"' : '' ?>><?= e($l) ?><?= !empty($counts[$k]) ? ' (' . $counts[$k] . ')' : '' ?></a><?php endforeach; ?></nav>
<form method="get" class="toolbar"><input type="hidden" name="page" value="review"><input type="hidden" name="kind" value="<?= e($kind) ?>">
  <select name="status" aria-label="Status"><?php foreach (['open', 'approved', 'rejected', 'resolved', 'all'] as $s): ?><option<?= $status === $s ? ' selected' : '' ?>><?= $s ?></option><?php endforeach; ?></select><button class="btn" type="submit">Show</button></form>
<?php if (!$rows): ?><p>No items.</p><?php else: ?>
<table class="table"><thead><tr><th>Received</th><th>Type</th><th>Summary</th><th>Status</th></tr></thead><tbody>
<?php foreach ($rows as $r): ?><tr><td class="nowrap small"><?= e(fmt_dt($r['created_at'], 'M j g:i A')) ?></td><td><?= e($kinds[$r['kind']] ?? $r['kind']) ?></td><td><a href="<?= e(admin_url('review', ['id' => $r['id']])) ?>"><?= e($r['summary']) ?></a></td><td><?= status_pill($r['status']) ?></td></tr><?php endforeach; ?>
</tbody></table>
<?php endif; ?>
<?php
admin_footer();
