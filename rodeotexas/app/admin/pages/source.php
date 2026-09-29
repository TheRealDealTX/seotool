<?php
declare(strict_types=1);

use RT\Db;
use RT\Importer;

$idParam = (string) ($_GET['id'] ?? 'new');
$id = ctype_digit($idParam) ? (int) $idParam : null;
$src = $id ? Db::one('SELECT * FROM sources WHERE id = ?', [$id]) : null;
if ($id && !$src) {
    redirect(admin_url('sources'));
}
$adapters = Importer::adapters();
$errors = [];

if (is_post()) {
    $action = (string) ($_POST['action'] ?? 'save');
    if ($action === 'run' && $src) {
        ignore_user_abort(true);
        @set_time_limit(600);
        $file = null;
        if ($src['adapter'] === 'csv') {
            $up = $_FILES['csv'] ?? null;
            if (!$up || $up['error'] !== UPLOAD_ERR_OK || $up['size'] > 5 * 1024 * 1024) {
                flash('Choose a CSV file (max 5 MB).', 'danger');
                redirect(admin_url('source', ['id' => $id]), 303);
            }
            $ext = strtolower(pathinfo((string) $up['name'], PATHINFO_EXTENSION));
            $head = (string) file_get_contents($up['tmp_name'], false, null, 0, 2048);
            if ($ext !== 'csv' || !mb_check_encoding($head, 'UTF-8') || str_contains($head, "\0")) {
                flash('The file must be a UTF-8 .csv file.', 'danger');
                redirect(admin_url('source', ['id' => $id]), 303);
            }
            $file = RT_STORAGE . '/imports/' . gmdate('Ymd-His') . '-' . bin2hex(random_bytes(4)) . '.csv';
            move_uploaded_file($up['tmp_name'], $file);
        }
        $r = Importer::run('manual', 'single', [$id], $file, $admin['email']);
        flash($r['status'] === 'locked' ? $r['message'] : 'Import #' . $r['run_id'] . ' (' . $r['status'] . '): ' . $r['message'], $r['status'] === 'success' ? 'success' : 'warning');
        redirect($r['run_id'] ? admin_url('imports', ['id' => $r['run_id']]) : admin_url('source', ['id' => $id]), 303);
    }
    $data = [
        'name' => post_str('name', 160),
        'slug' => post_str('slug', 60),
        'adapter' => array_key_exists($_POST['adapter'] ?? '', $adapters) ? $_POST['adapter'] : null,
        'config' => trim((string) ($_POST['config'] ?? '')) ?: '{}',
        'homepage' => valid_url($_POST['homepage'] ?? null),
        'access_status' => in_array($_POST['access_status'] ?? '', ['active', 'awaiting_permission', 'awaiting_credentials', 'manual_only', 'disabled'], true) ? $_POST['access_status'] : 'disabled',
        'access_note' => clean_text($_POST['access_note'] ?? null, 3000),
        'enabled' => !empty($_POST['enabled']) ? 1 : 0,
        'auto_publish' => !empty($_POST['auto_publish']) ? 1 : 0,
        'daily_check' => !empty($_POST['daily_check']) ? 1 : 0,
        'default_association_id' => post_int('default_association_id'),
        'default_level' => in_array($_POST['default_level'] ?? '', levels(), true) ? $_POST['default_level'] : null,
    ];
    if (!$data['name']) { $errors['name'] = 'Name is required.'; }
    if (!$data['slug'] || !preg_match('/^[a-z0-9-]+$/', $data['slug'])) { $errors['slug'] = 'Slug: lowercase letters, numbers, hyphens.'; }
    if (!$data['adapter']) { $errors['adapter'] = 'Choose an adapter.'; }
    $cfg = json_decode($data['config'], true);
    if (!is_array($cfg)) { $errors['config'] = 'Config must be valid JSON (an object).'; }
    else { $data['config'] = json_encode($cfg, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE); }
    if ($data['enabled'] && $data['access_status'] !== 'active') { $errors['enabled'] = 'Only sources with access status “active” can be enabled for automatic import.'; }
    if ($data['enabled'] && $data['adapter'] === 'csv') { $errors['enabled'] = 'CSV sources are manual; upload a file instead of enabling.'; }
    if (!$errors) {
        $data['updated_at'] = now_utc();
        if ($src) {
            Db::update('sources', $data, 'id = :id', ['id' => $id]);
        } else {
            $data['created_at'] = now_utc();
            $id = Db::insert('sources', $data);
        }
        flash('Source saved.');
        redirect(admin_url('source', ['id' => $id]), 303);
    }
}
$v = $src ?? ['name' => '', 'slug' => '', 'adapter' => 'ical', 'config' => '{}', 'homepage' => '', 'access_status' => 'awaiting_permission', 'access_note' => '',
    'enabled' => 0, 'auto_publish' => 1, 'daily_check' => 0, 'default_association_id' => null, 'default_level' => null];
if (is_post() && $errors) { $v = array_merge($v, $_POST); }
$records = $src ? Db::all('SELECT r.*, e.title AS ev_title FROM source_records r LEFT JOIN events e ON e.id = r.event_id WHERE r.source_id = ? ORDER BY r.last_changed_at DESC LIMIT 60', [$id]) : [];
$assocs = options_from("SELECT id, CONCAT(abbr, ' — ', name) AS label FROM associations ORDER BY sort");
$err = static fn(string $k): string => isset($errors[$k]) ? '<p class="field-error">' . e($errors[$k]) . '</p>' : '';

admin_header($src ? 'Source: ' . $src['name'] : 'New source');
?>
<?php if ($src): ?>
<section class="card">
  <h2>Run</h2>
  <p class="small">Last run <?= e(fmt_dt($src['last_run_at'])) ?> · last success <?= e(fmt_dt($src['last_success_at'])) ?> · <?= (int) $src['last_record_count'] ?> records last time
    <?= $src['last_error'] ? '<br><strong>Last error:</strong> ' . e($src['last_error']) : '' ?></p>
  <form method="post" enctype="multipart/form-data" data-confirm="Run this source now?">
    <?= RT\Auth::csrfField() ?><input type="hidden" name="action" value="run">
    <?php if ($src['adapter'] === 'csv'): ?>
      <div class="field"><label for="csv">CSV file</label><input id="csv" type="file" name="csv" accept=".csv,text/csv" required>
        <small>Columns: see <a href="/admin/csv-template.csv">csv-template.csv</a>. Rows are validated; only Texas events are imported. Re-uploading the same file is safe.</small></div>
      <button class="btn btn--primary" type="submit">Upload &amp; import</button>
    <?php else: ?>
      <button class="btn btn--primary" type="submit"<?= $src['access_status'] !== 'active' ? ' disabled title="Access status is not active"' : '' ?>>Run this source now</button>
    <?php endif; ?>
  </form>
</section>
<?php endif; ?>

<form method="post" class="card">
  <?= RT\Auth::csrfField() ?>
  <h2>Settings</h2>
  <div class="row2"><?= f_text('name', 'Name', $v['name'], ['required' => true]) ?><?= f_text('slug', 'Slug (for CLI: --source=slug)', $v['slug'], ['required' => true]) ?></div>
  <?= $err('name') . $err('slug') ?>
  <div class="row2"><?= f_select('adapter', 'Adapter', $v['adapter'], $adapters, false) ?><?= f_text('homepage', 'Homepage', $v['homepage'], ['type' => 'url']) ?></div>
  <?= f_area('config', 'Adapter configuration (JSON)', $v['config'] ? json_encode(json_decode((string) $v['config'], true), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?: $v['config'] : '{}', ['rows' => 9, 'mono' => true,
      'help' => 'Keys: base_url (tribe_rest), url (ical), urls / sitemap_url / url_pattern (jsonld), require_keywords, exclude_keywords, exclude_acts, title_strip_regex, title_replace, default_venue, unknown_location ("skip"|"review"), min_delay. See docs/SOURCES.md.']) ?><?= $err('config') ?>
  <div class="row2">
    <?= f_select('access_status', 'Access status', $v['access_status'], ['active' => 'active — automated access permitted', 'awaiting_permission' => 'awaiting permission', 'awaiting_credentials' => 'awaiting credentials / paid access', 'manual_only' => 'manual only (CSV)', 'disabled' => 'disabled'], false) ?>
    <div><?= f_check('enabled', 'Run automatically every week', (bool) $v['enabled']) ?><?= $err('enabled') ?>
      <?= f_check('daily_check', 'Also include in the optional daily 7-day check', (bool) $v['daily_check']) ?>
      <?= f_check('auto_publish', 'Publish complete, validated records automatically', (bool) $v['auto_publish'], 'Otherwise every new record is held as a draft for review.') ?></div>
  </div>
  <?= f_area('access_note', 'Access / permission notes (terms of use, robots.txt, contact)', $v['access_note'], ['rows' => 3]) ?>
  <div class="row2"><?= f_select('default_association_id', 'Default association (only if the source is that association’s own calendar)', $v['default_association_id'], $assocs) ?>
    <?= f_select('default_level', 'Default level', $v['default_level'], array_combine(levels(), array_map('level_label', levels()))) ?></div>
  <button class="btn btn--primary" type="submit">Save source</button>
</form>

<?php if ($records): ?>
<section class="card">
  <h2>Recent records from this source</h2>
  <table class="table small"><thead><tr><th>UID</th><th>State</th><th>Title</th><th>Event</th><th>Last seen</th></tr></thead><tbody>
  <?php foreach ($records as $r): $pl = json_decode((string) $r['payload'], true) ?: []; ?>
    <tr><td><code><?= e(excerpt($r['source_uid'], 40)) ?></code></td><td><?= status_pill($r['state']) ?><?= $r['skip_reason'] ? '<br>' . e($r['skip_reason']) : '' ?></td>
      <td><?= e($pl['title'] ?? '') ?><br><span class="muted"><?= e(($pl['start_date'] ?? '') . ' · ' . ($pl['venue']['city'] ?? '?')) ?></span></td>
      <td><?= $r['event_id'] ? '<a href="' . e(admin_url('event', ['id' => $r['event_id']])) . '">#' . (int) $r['event_id'] . '</a>' : '—' ?></td>
      <td class="nowrap"><?= e(fmt_dt($r['last_seen_at'], 'M j, Y')) ?></td></tr>
  <?php endforeach; ?>
  </tbody></table>
</section>
<?php endif; ?>
<?php
admin_footer();
