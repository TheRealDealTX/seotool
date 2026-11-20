<?php defined('WCA') || exit; ?>
<div class="wrap section-tight admin-page">
  <h1 class="h2">Payments</h1>
  <p class="small muted">Refunds are issued from your Stripe dashboard. Use "Revoke owner" on the listing if access should be removed.</p>
  <div class="table-scroll"><table class="table">
    <thead><tr><th>Date</th><th>Listing</th><th>Type</th><th>Name / email</th><th>Amount</th><th>Status</th><th>Stripe session</th></tr></thead>
    <tbody><?php foreach ($payments as $p): ?><tr>
      <td><?= e(date('M j, Y g:ia', strtotime($p['created_at']))) ?></td>
      <td><a href="/admin/listings/edit/?id=<?= (int)$p['listing_id'] ?>"><?= e($p['listing_name'] ?? '#' . $p['listing_id']) ?></a></td>
      <td><?= e($p['purpose']) ?></td><td><?= e($p['name']) ?><br><span class="small muted"><?= e($p['email']) ?></span></td>
      <td><?= money($p['amount'] / 100) ?></td><td><span class="status status-<?= e($p['status']) ?>"><?= e($p['status']) ?></span></td>
      <td class="small muted"><?= e(substr((string)$p['session_id'], 0, 24)) ?>…</td>
    </tr><?php endforeach; ?></tbody>
  </table></div>
</div>
