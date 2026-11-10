<div class="narrow">
  <h1>Notifications</h1>
  <?php if (!$items): ?><div class="card empty-state"><?= icon('bell') ?><h3>You're all caught up</h3></div><?php else: ?>
  <ul class="card notif-list">
    <?php foreach ($items as $n): [$text, $link] = notification_text($n); ?>
    <li class="<?= $n['is_read'] ? '' : 'unread' ?>"><a href="<?= e($link) ?>">
      <?= $n['actor_id'] ? avatar($n, 'md') : '<span class="avatar avatar-md avatar-initials" style="--h:240">' . icon('bell') . '</span>' ?>
      <span class="grow"><?= $text ?><small class="muted"><?= e(time_ago($n['created_at'])) ?></small></span>
    </a></li>
    <?php endforeach; ?>
  </ul>
  <?php endif; ?>
</div>
