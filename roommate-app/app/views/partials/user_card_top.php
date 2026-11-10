<a href="/u/<?= e($u['username']) ?>" class="user-card-top">
  <div class="avatar-wrap"><?= avatar($u, 'lg') ?><?php if (is_online($u)): ?><span class="online-dot"></span><?php endif; ?></div>
  <div class="user-card-id"><h3><?= e($u['name']) ?><?php if (age_of($u)): ?><span class="age">, <?= age_of($u) ?></span><?php endif; ?></h3><p class="muted small"><?= e(label('looking_for', $u['looking_for'])) ?><?= $u['city'] ? ' · ' . e($u['city']) : '' ?></p></div>
  <span class="score <?= score_class($match['score']) ?>"><?= $match['score'] ?>%</span>
</a>
