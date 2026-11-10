<h1>Audit log</h1>
<p class="muted">Every administrative action is recorded here.</p>
<div class="card table-card"><div class="table-wrap"><table class="table">
  <thead><tr><th>When</th><th>Admin</th><th>Action</th><th>Details</th></tr></thead>
  <tbody>
  <?php foreach ($rows as $r): ?>
  <tr><td class="small muted"><?= e(date('M j, Y g:i A', strtotime($r['created_at']))) ?></td><td class="small">@<?= e($r['username'] ?? 'system') ?></td><td><code><?= e($r['action']) ?></code></td><td class="small"><?= e($r['details']) ?></td></tr>
  <?php endforeach; ?>
  <?php if (!$rows): ?><tr><td colspan="4" class="muted">Nothing logged yet.</td></tr><?php endif; ?>
  </tbody>
</table></div></div>
<?php partial('partials/pager', ['page' => $page, 'pages' => $pages]); ?>
