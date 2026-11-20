<?php defined('WCA') || exit; ?>
<div class="wrap section-tight admin-page">
  <h1 class="h2">Admin dashboard</h1>
  <?php if (!stripe_ready()): ?><div class="alert alert-info">Stripe is not connected yet, so claims and paid listings can't be purchased. <a href="/admin/settings/">Add your Stripe keys</a>.</div><?php endif; ?>
  <div class="admin-stats">
    <a href="/admin/listings/?status=published" class="card"><b><?= $stats['published'] ?></b><span>Published listings</span></a>
    <a href="/admin/listings/?status=pending" class="card <?= $stats['pending'] ? 'hot' : '' ?>"><b><?= $stats['pending'] ?></b><span>Pending review</span></a>
    <a href="/admin/listings/" class="card"><b><?= $stats['claimed'] ?></b><span>Claimed by owners</span></a>
    <a href="/admin/users/" class="card"><b><?= $stats['users'] ?></b><span>Owner accounts</span></a>
    <a href="/admin/payments/" class="card"><b><?= money($stats['revenue']) ?></b><span>Revenue</span></a>
    <a href="/admin/messages/" class="card <?= $stats['messages'] ? 'hot' : '' ?>"><b><?= $stats['messages'] ?></b><span>Unread messages</span></a>
  </div>
  <div class="grid-2">
    <div class="card">
      <h2 class="h4">Pending submissions</h2>
      <?php if (!$pending): ?><p class="muted">Nothing waiting for review.</p><?php endif; ?>
      <?php foreach ($pending as $l): ?>
        <div class="pending-row">
          <div><strong><?= e($l['name']) ?></strong><br><span class="small muted"><?= e($l['address']) ?> · by <?= e($l['submitter_name']) ?> (<?= e($l['submitter_email']) ?>)</span></div>
          <div class="row-actions">
            <a class="btn btn-ghost btn-sm" href="/admin/listings/edit/?id=<?= (int)$l['id'] ?>">Review</a>
            <form method="post" action="/admin/listings/action/"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$l['id'] ?>"><button class="btn btn-sm" name="action" value="approve">Approve</button></form>
            <form method="post" action="/admin/listings/action/" onsubmit="return confirm('Reject this listing?')"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$l['id'] ?>"><button class="btn btn-ghost btn-sm" name="action" value="reject">Reject</button></form>
          </div>
        </div>
      <?php endforeach; ?>
    </div>
    <div class="card">
      <h2 class="h4">Recent payments</h2>
      <?php if (!$payments): ?><p class="muted">No payments yet.</p><?php else: ?>
      <table class="table small"><tbody><?php foreach ($payments as $p): ?><tr><td><?= e(time_ago($p['created_at'])) ?></td><td><?= e($p['listing_name']) ?></td><td><?= money($p['amount'] / 100) ?></td><td><?= e($p['status']) ?></td></tr><?php endforeach; ?></tbody></table>
      <?php endif; ?>
      <h2 class="h4 mt">Most viewed listings</h2>
      <table class="table small"><tbody><?php foreach ($top as $t): ?><tr><td><a href="/apartments/<?= e($t['slug']) ?>/" target="_blank"><?= e($t['name']) ?></a></td><td><?= (int)$t['views'] ?> views</td></tr><?php endforeach; ?></tbody></table>
    </div>
  </div>
</div>
