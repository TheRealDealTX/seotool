<?php defined('WCA') || exit; ?>
<div class="wrap section-tight">
  <div class="section-head"><h1 class="h2">Welcome, <?= e($u['name']) ?></h1><a href="/account/logout/">Sign out</a></div>
  <p class="muted">Signed in as <?= e($u['email']) ?></p>
  <h2 class="h3">Your listings</h2>
  <?php if (!$listings): ?>
    <div class="card"><p>You don't manage any listings yet. <a href="/apartments/">Find your community and claim it</a>, or <a href="/list-your-property/">add a new property</a>.</p></div>
  <?php else: ?>
  <div class="owner-listings">
    <?php foreach ($listings as $l): ?>
    <div class="card owner-row">
      <img src="<?= e(photo_url($l['photos'][0], true)) ?>" alt="" width="160" height="107">
      <div>
        <h3><?= e($l['name']) ?></h3>
        <p class="small muted"><?= e($l['address']) ?>, <?= e($l['city']) ?> · <?= e(ucfirst($l['status'])) ?> · <?= (int)$l['views'] ?> views</p>
        <p class="small"><?= $l['show_contact'] ? '✓ Contact details visible' : 'Contact details hidden' ?></p>
      </div>
      <div class="owner-actions">
        <a class="btn btn-sm" href="/account/listings/edit/?id=<?= (int)$l['id'] ?>">Edit listing</a>
        <a class="btn btn-ghost btn-sm" href="<?= e($l['url']) ?>">View</a>
      </div>
    </div>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>
  <?php if ($payments): ?>
  <h2 class="h3">Payment history</h2>
  <div class="table-scroll"><table class="table"><thead><tr><th>Date</th><th>Listing</th><th>Type</th><th>Amount</th><th>Status</th></tr></thead><tbody>
    <?php foreach ($payments as $p): ?><tr><td><?= e(time_ago($p['created_at'])) ?></td><td><?= e($p['listing_name']) ?></td><td><?= e($p['purpose'] === 'claim' ? 'Claim' : 'New listing') ?></td><td><?= money($p['amount'] / 100) ?></td><td><?= e($p['status']) ?></td></tr><?php endforeach; ?>
  </tbody></table></div>
  <?php endif; ?>
</div>
