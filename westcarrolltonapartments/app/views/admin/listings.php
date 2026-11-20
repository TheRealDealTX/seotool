<?php defined('WCA') || exit; ?>
<div class="wrap section-tight admin-page">
  <div class="section-head"><h1 class="h2">Listings</h1><a class="btn btn-sm" href="/admin/listings/edit/">+ New listing</a></div>
  <form class="admin-filter" method="get">
    <input type="search" name="q" value="<?= e($q) ?>" placeholder="Search name or address">
    <select name="status"><option value="">All statuses</option><?php foreach (['published', 'pending', 'awaiting_payment', 'draft', 'rejected'] as $s): ?><option <?= $status === $s ? 'selected' : '' ?>><?= $s ?></option><?php endforeach; ?></select>
    <button class="btn btn-sm">Filter</button>
  </form>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th>Name</th><th>Status</th><th>Source</th><th>Owner</th><th>Contact</th><th>Views</th><th></th></tr></thead>
    <tbody>
    <?php foreach ($rows as $l): ?>
      <tr>
        <td><a href="/admin/listings/edit/?id=<?= (int)$l['id'] ?>"><strong><?= e($l['name']) ?></strong></a><br><span class="small muted"><?= e($l['address']) ?>, <?= e($l['city']) ?></span></td>
        <td><span class="status status-<?= e($l['status']) ?>"><?= e($l['status']) ?></span><?= $l['featured'] ? ' ★' : '' ?></td>
        <td><?= e($l['source']) ?></td>
        <td class="small"><?= e($l['owner_email'] ?? '—') ?></td>
        <td><?= $l['show_contact'] ? 'Shown' : 'Hidden' ?></td>
        <td><?= (int)$l['views'] ?></td>
        <td class="row-actions">
          <a class="btn btn-ghost btn-sm" href="<?= e($l['url']) ?>" target="_blank">View</a>
          <?php if ($l['status'] === 'pending'): ?><form method="post" action="/admin/listings/action/"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$l['id'] ?>"><button class="btn btn-sm" name="action" value="approve">Approve</button></form><?php endif; ?>
        </td>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table>
  </div>
</div>
