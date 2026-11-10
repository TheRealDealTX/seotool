<div class="narrow-lg">
  <div class="page-head"><div><h1>Friends</h1><p class="muted">Your roommate network.</p></div><a class="btn btn-primary" href="/discover"><?= icon('search') ?> Find people</a></div>
  <nav class="tabs">
    <a href="/friends?tab=all" class="<?= $tab === 'all' ? 'active' : '' ?>">Friends <span class="count"><?= count($friends) ?></span></a>
    <a href="/friends?tab=requests" class="<?= $tab === 'requests' ? 'active' : '' ?>">Requests <?php if ($incoming): ?><span class="count hot"><?= count($incoming) ?></span><?php endif; ?></a>
    <a href="/friends?tab=sent" class="<?= $tab === 'sent' ? 'active' : '' ?>">Sent <span class="count"><?= count($outgoing) ?></span></a>
  </nav>

  <?php if ($tab === 'requests'): ?>
    <?php if (!$incoming): ?><div class="card empty-state"><?= icon('users') ?><h3>No pending requests</h3></div><?php endif; ?>
    <ul class="card people-list big">
      <?php foreach ($incoming as $u): ?>
      <li>
        <a href="/u/<?= e($u['username']) ?>"><?= avatar($u, 'md') ?></a>
        <div class="grow"><a class="strong" href="/u/<?= e($u['username']) ?>"><?= e($u['name']) ?></a><small class="muted"><?= e(label('looking_for', $u['looking_for'])) ?> · requested <?= e(time_ago($u['requested_at'])) ?></small></div>
        <span class="score sm <?= score_class($u['_match']['score']) ?>"><?= $u['_match']['score'] ?>%</span>
        <div class="pl-actions">
          <form method="post" action="/friend/<?= (int)$u['id'] ?>/accept"><?= csrf_field() ?><button class="btn btn-primary btn-sm" type="submit">Accept</button></form>
          <form method="post" action="/friend/<?= (int)$u['id'] ?>/decline"><?= csrf_field() ?><button class="btn btn-outline btn-sm" type="submit">Decline</button></form>
        </div>
      </li>
      <?php endforeach; ?>
    </ul>
  <?php elseif ($tab === 'sent'): ?>
    <?php if (!$outgoing): ?><div class="card empty-state"><?= icon('send') ?><h3>No sent requests</h3></div><?php endif; ?>
    <ul class="card people-list big">
      <?php foreach ($outgoing as $u): ?>
      <li>
        <a href="/u/<?= e($u['username']) ?>"><?= avatar($u, 'md') ?></a>
        <div class="grow"><a class="strong" href="/u/<?= e($u['username']) ?>"><?= e($u['name']) ?></a><small class="muted">Sent <?= e(time_ago($u['requested_at'])) ?></small></div>
        <div class="pl-actions"><form method="post" action="/friend/<?= (int)$u['id'] ?>/cancel"><?= csrf_field() ?><button class="btn btn-outline btn-sm" type="submit">Cancel</button></form></div>
      </li>
      <?php endforeach; ?>
    </ul>
  <?php else: ?>
    <?php if (!$friends): ?><div class="card empty-state"><?= icon('users') ?><h3>No friends yet</h3><p class="muted">Find renters interested in your properties and send a friend request.</p><a class="btn btn-primary" href="/discover">Discover roommates</a></div><?php endif; ?>
    <div class="grid grid-3">
      <?php foreach ($friends as $u) partial('partials/user_card', ['u' => $u, 'match' => $u['_match']]); ?>
    </div>
  <?php endif; ?>
</div>
