<h1>Reports</h1>
<nav class="tabs">
  <?php foreach (['open', 'resolved', 'dismissed'] as $st): ?><a href="?status=<?= $st ?>" class="<?= $status === $st ? 'active' : '' ?>"><?= ucfirst($st) ?></a><?php endforeach; ?>
</nav>
<?php if (!$reports): ?><div class="card empty-state"><?= icon('check') ?><h3>No <?= e($status) ?> reports</h3></div><?php endif; ?>
<?php foreach ($reports as $r): ?>
<article class="card report">
  <div class="report-head">
    <span class="tag"><?= e($r['target_type']) ?></span>
    <strong><?php if ($r['target']['link']): ?><a href="<?= e($r['target']['link']) ?>" target="_blank"><?= e($r['target']['label']) ?></a><?php else: ?><?= e($r['target']['label']) ?><?php endif; ?></strong>
    <span class="muted small">reported by @<?= e($r['reporter'] ?? 'deleted') ?> · <?= e(time_ago($r['created_at'])) ?></span>
  </div>
  <p class="report-reason">“<?= e($r['reason']) ?>”</p>
  <?php if ($r['target']['text']): ?><blockquote class="report-content"><?= e(mb_strimwidth($r['target']['text'], 0, 500, '…')) ?></blockquote><?php endif; ?>
  <?php if ($r['admin_note']): ?><p class="small muted">Note: <?= e($r['admin_note']) ?></p><?php endif; ?>
  <form method="post" class="report-actions"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$r['id'] ?>">
    <input type="text" name="note" placeholder="Internal note (optional)" class="input-sm">
    <?php if ($status === 'open'): ?>
      <?php if ($r['target_type'] !== 'user'): ?><button class="btn btn-outline btn-xs" name="action" value="remove_content">Remove content</button><?php endif; ?>
      <button class="btn btn-outline btn-xs danger" name="action" value="suspend_user" data-confirm="Suspend the member responsible?">Suspend member</button>
      <button class="btn btn-primary btn-xs" name="action" value="resolved">Mark resolved</button>
      <button class="btn btn-ghost btn-xs" name="action" value="dismissed">Dismiss</button>
    <?php else: ?>
      <button class="btn btn-ghost btn-xs" name="action" value="open">Reopen</button>
    <?php endif; ?>
  </form>
</article>
<?php endforeach; ?>
