<?php /** @var array $u  $match (optional) */ ?>
<article class="card user-card">
  <a href="/u/<?= e($u['username']) ?>" class="user-card-top">
    <div class="avatar-wrap"><?= avatar($u, 'lg') ?><?php if (is_online($u)): ?><span class="online-dot" title="Online"></span><?php endif; ?></div>
    <div class="user-card-id">
      <h3><?= e($u['name']) ?><?php if ($u['is_verified']): ?> <span class="verified" title="Verified"><?= icon('check') ?></span><?php endif; ?><?php if (age_of($u)): ?><span class="age">, <?= age_of($u) ?></span><?php endif; ?></h3>
      <p class="muted small"><?= e(label('looking_for', $u['looking_for'])) ?><?= $u['city'] ? ' · ' . e($u['city']) : '' ?></p>
    </div>
    <?php if (isset($match)): ?><span class="score <?= score_class($match['score']) ?>" title="Compatibility"><?= $match['score'] ?>%</span><?php endif; ?>
  </a>
  <?php if (!empty($u['quiz_type'])): ?><div><?= quiz_badge($u['quiz_type']) ?></div><?php endif; ?>
  <div class="chips">
    <?php if (budget_label($u)): ?><span class="chip"><?= icon('dollar') ?><?= e(budget_label($u)) ?></span><?php endif; ?>
    <?php if ($u['move_in_date']): ?><span class="chip"><?= icon('calendar') ?><?= e(date('M j', strtotime($u['move_in_date']))) ?></span><?php endif; ?>
    <span class="chip"><?= e(label('sleep_schedule', $u['sleep_schedule'])) ?></span>
    <span class="chip"><?= e(label('cleanliness', $u['cleanliness'])) ?></span>
  </div>
  <?php if (!empty($match['reasons'])): ?>
  <ul class="reasons"><?php foreach (array_slice($match['reasons'], 0, 3) as $r): ?><li><?= icon('check') ?><?= e($r) ?></li><?php endforeach; ?></ul>
  <?php endif; ?>
  <div class="user-card-actions">
    <a class="btn btn-sm btn-outline" href="/u/<?= e($u['username']) ?>">View profile</a>
    <a class="btn btn-sm btn-primary" href="/messages/<?= e($u['username']) ?>"><?= icon('chat') ?> Message</a>
  </div>
</article>
