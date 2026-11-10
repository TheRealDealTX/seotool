<div class="card empty-state narrow">
  <?= avatar($u, 'xl') ?>
  <h1><?= e($u['name']) ?></h1>
  <?php if ($iBlocked): ?>
    <p class="muted">You've blocked this member.</p>
    <form method="post" action="/unblock/<?= (int)$u['id'] ?>"><?= csrf_field() ?><button class="btn btn-outline" type="submit">Unblock</button></form>
  <?php else: ?>
    <p class="muted">This profile isn't available.</p>
  <?php endif; ?>
</div>
