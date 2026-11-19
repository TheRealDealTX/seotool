<?php defined('M1S') || exit; ?>
<h1>Open reports</h1>
<?= view('admin/_nav') ?>
<?php if (!$reports): ?><p class="empty">No open reports. 🎉</p><?php endif; ?>
<?php foreach ($reports as $r): ?>
  <div class="card-pad report-item">
    <p class="meta"><?= e($r['target_type']) ?> by <strong><?= e((string)$r['author']) ?></strong> · reported by <?= e((string)$r['reporter']) ?> · <?= e(time_ago($r['created_at'])) ?></p>
    <p><strong><?= e($r['reason']) ?></strong></p>
    <blockquote><?= e($r['preview']) ?></blockquote>
    <div class="form-row">
      <?php if ($r['link']): ?><a href="<?= e($r['link']) ?>" target="_blank">Open ↗</a><?php endif; ?>
      <form method="post" action="/admin/reports/"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$r['id'] ?>"><input type="hidden" name="action" value="dismiss"><button class="btn btn-ghost btn-sm">Dismiss</button></form>
      <form method="post" action="/admin/reports/"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$r['id'] ?>"><input type="hidden" name="action" value="remove"><button class="btn btn-accent btn-sm">Remove content</button></form>
    </div>
  </div>
<?php endforeach; ?>
