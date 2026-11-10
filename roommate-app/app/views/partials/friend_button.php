<?php $id = (int)$u['id']; ?>
<?php if ($fstatus === 'friends'): ?>
  <form method="post" action="/friend/<?= $id ?>/remove" data-confirm="Remove <?= e($u['name']) ?> from your friends?"><?= csrf_field() ?><button class="btn btn-soft" type="submit"><?= icon('check') ?> Friends</button></form>
<?php elseif ($fstatus === 'sent'): ?>
  <form method="post" action="/friend/<?= $id ?>/cancel"><?= csrf_field() ?><button class="btn btn-outline" type="submit">Request sent · Cancel</button></form>
<?php elseif ($fstatus === 'received'): ?>
  <form method="post" action="/friend/<?= $id ?>/accept"><?= csrf_field() ?><button class="btn btn-primary" type="submit"><?= icon('check') ?> Accept request</button></form>
  <form method="post" action="/friend/<?= $id ?>/decline"><?= csrf_field() ?><button class="btn btn-outline" type="submit">Decline</button></form>
<?php else: ?>
  <form method="post" action="/friend/<?= $id ?>/add"><?= csrf_field() ?><button class="btn btn-outline" type="submit"><?= icon('plus') ?> Add friend</button></form>
<?php endif; ?>
