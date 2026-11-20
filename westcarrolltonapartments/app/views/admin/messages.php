<?php defined('WCA') || exit; ?>
<div class="wrap section-tight admin-page">
  <h1 class="h2">Contact messages</h1>
  <p class="small muted">Messages are also emailed to <?= e(cfg('admin_email')) ?>.</p>
  <?php if (!$messages): ?><p class="muted">No messages yet.</p><?php endif; ?>
  <?php foreach ($messages as $m): ?>
    <div class="card message-card <?= $m['is_read'] ? '' : 'unread' ?>">
      <div class="section-head"><strong><?= e($m['subject'] ?: '(no subject)') ?></strong><span class="small muted"><?= e(date('M j, Y g:ia', strtotime($m['created_at']))) ?></span></div>
      <p class="small"><?= e($m['name']) ?> · <a href="mailto:<?= e($m['email']) ?>?subject=<?= rawurlencode('Re: ' . $m['subject']) ?>"><?= e($m['email']) ?></a></p>
      <p><?= nl2br(e($m['body'])) ?></p>
      <form method="post" onsubmit="return confirm('Delete message?')"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$m['id'] ?>"><button class="linklike small" name="action" value="delete">Delete</button></form>
    </div>
  <?php endforeach; ?>
</div>
