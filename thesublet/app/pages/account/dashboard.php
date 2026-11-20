<?php defined('APP') || exit;

cache_private();
$o = require_owner();
$ls = rows('SELECT * FROM listings WHERE owner_id = ? ORDER BY created_at DESC', [(int)$o['id']]);
$photos = [];
foreach (rows('SELECT listing_id, COUNT(*) n FROM photos WHERE listing_id IN (SELECT id FROM listings WHERE owner_id = ?) GROUP BY listing_id', [(int)$o['id']]) as $r) $photos[(int)$r['listing_id']] = (int)$r['n'];
$msgs = (int)val('SELECT COUNT(*) FROM messages m JOIN listings l ON l.id = m.listing_id WHERE l.owner_id = ?', [(int)$o['id']]);
ob_start(); ?>
<div class="wrap section">
  <div class="section-head"><h1>Your listings</h1><span><a class="btn btn-sm" href="/account/new/">+ New listing</a> <a class="btn btn-sm btn-ghost" href="/logout/">Sign out</a></span></div>
  <p class="muted">Signed in as <?= e($o['email']) ?> · <?= $msgs ?> renter message<?= $msgs == 1 ? '' : 's' ?> relayed to your inbox</p>
  <?= flashes() ?>
  <?php if (!$ls): ?><p>You don’t have any listings yet. <a href="/account/new/">Create one</a>.</p><?php endif; ?>
  <div class="dash-list">
  <?php foreach ($ls as $l): $pc = $photos[(int)$l['id']] ?? 0; ?>
    <article class="dash-item">
      <div>
        <h2 class="h4"><a href="<?= e(listing_url($l)) ?>"><?= e($l['title']) ?></a></h2>
        <p class="small"><span class="status status-<?= e($l['status']) ?>"><?= e(listing_status_label($l['status'])) ?></span>
          <?= $l['tier'] === 'paid' ? '<span class="badge badge-verified">✔ Verified</span>' : '<span class="badge">Free</span>' ?>
          · <?= money($l['rent']) ?>/mo · <?= e($l['city'] . ', ' . $l['state']) ?> · <?= (int)$l['views'] ?> views · <?= $pc ?> photo<?= $pc == 1 ? '' : 's' ?>
          <?= $l['expires_at'] && $l['status'] === 'active' ? ' · expires ' . e(fmt_date($l['expires_at'])) : '' ?></p>
        <?php if (!$pc): ?><p class="small warn-text">No photos yet — listings with photos get far more messages. <a href="/account/listing/<?= (int)$l['id'] ?>/#photos">Add photos</a></p><?php endif; ?>
      </div>
      <div class="dash-actions">
        <a class="btn btn-sm" href="/account/listing/<?= (int)$l['id'] ?>/">Edit</a>
        <form method="post" action="/account/listing/<?= (int)$l['id'] ?>/action/"><?= csrf_field() ?>
          <?php if ($l['status'] === 'pending_payment' || $l['tier'] !== 'paid'): ?>
            <button class="btn btn-sm" formaction="/checkout/start/<?= (int)$l['id'] ?>/" name="kind" value="<?= $l['status'] === 'pending_payment' ? 'new' : 'upgrade' ?>">Pay <?= e(price_label()) ?> &amp; publish</button>
          <?php endif; ?>
          <?php if ($l['status'] === 'active'): ?>
            <button class="btn btn-sm btn-ghost" name="do" value="rented">Mark rented</button>
            <button class="btn btn-sm btn-ghost" name="do" value="unavailable">Mark unavailable</button>
            <button class="btn btn-sm btn-ghost" name="do" value="renew">Renew</button>
          <?php elseif (in_array($l['status'], ['rented', 'unavailable', 'expired'], true) && $l['tier'] === 'paid'): ?>
            <button class="btn btn-sm btn-ghost" name="do" value="activate">Re-activate</button>
          <?php endif; ?>
          <button class="btn btn-sm btn-danger" name="do" value="delete" data-confirm="Delete this listing permanently?">Delete</button>
        </form>
      </div>
    </article>
  <?php endforeach; ?>
  </div>
</div>
<?php
page(['title' => 'Your listings | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean()]);
