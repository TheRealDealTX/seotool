<?php
declare(strict_types=1);

use RT\Db;

$rows = Db::all('SELECT s.*, (SELECT COUNT(*) FROM source_records r WHERE r.source_id = s.id AND r.state = \'linked\') AS linked,
    (SELECT COUNT(*) FROM source_records r WHERE r.source_id = s.id) AS seen FROM sources s ORDER BY s.enabled DESC, s.access_status, s.name');
admin_header('Event sources');
?>
<p>Each source has its own adapter. Only sources with access status <strong>active</strong> and <strong>enabled</strong> run automatically.
  Sources awaiting permission use the manual CSV fallback. <a href="<?= e(admin_url('source', ['id' => 'new'])) ?>">+ Add a source</a></p>
<table class="table">
  <thead><tr><th>Source</th><th>Adapter</th><th>Access</th><th>Auto</th><th>Last success</th><th>Records (linked/seen)</th><th>Health</th></tr></thead>
  <tbody>
  <?php foreach ($rows as $s): ?>
    <tr>
      <td><a href="<?= e(admin_url('source', ['id' => $s['id']])) ?>"><?= e($s['name']) ?></a></td>
      <td><code><?= e($s['adapter']) ?></code></td>
      <td><?= status_pill($s['access_status']) ?></td>
      <td><?= $s['enabled'] ? 'On' . ($s['daily_check'] ? ' + daily' : '') : 'Off' ?></td>
      <td class="small nowrap"><?= e(fmt_dt($s['last_success_at'], 'M j, Y')) ?></td>
      <td><?= (int) $s['linked'] ?> / <?= (int) $s['seen'] ?></td>
      <td><?= $s['consecutive_failures'] > 0 ? '<span class="pill pill--failed">failing ×' . (int) $s['consecutive_failures'] . '</span>' : ($s['last_success_at'] ? '<span class="pill pill--success">ok</span>' : '—') ?></td>
    </tr>
  <?php endforeach; ?>
  </tbody>
</table>
<?php
admin_footer();
