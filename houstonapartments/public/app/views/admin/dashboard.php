<?php
defined('HA_ROOT') || exit;
$title = 'Dashboard';
$actions = '<a class="btn primary" href="/admin/listings/new/">＋ Add a listing</a>';
?>
<div class="stat-row">
  <a class="stat" href="/admin/listings/?status=publish"><strong><?= number_format($stats['published']) ?></strong><span>Listings on the site</span></a>
  <a class="stat" href="/admin/listings/?status=hidden"><strong><?= number_format($stats['hidden']) ?></strong><span>Hidden listings</span></a>
  <a class="stat" href="/admin/listings/?source=manual"><strong><?= number_format($stats['manual']) ?></strong><span>Added by hand</span></a>
  <a class="stat hot" href="/admin/leads/?status=new"><strong><?= number_format($stats['leads_new']) ?></strong><span>New leads to call</span></a>
  <a class="stat" href="/admin/leads/"><strong><?= number_format($stats['leads_7d']) ?></strong><span>Leads this week</span></a>
</div>
<div class="grid-2">
  <section class="card">
    <div class="card-head"><h2>Latest leads</h2><a href="/admin/leads/">See all →</a></div>
    <?php if (!$leads): ?><p class="muted">No leads yet. They’ll show up here as soon as someone sends a request on the website.</p><?php endif ?>
    <ul class="simple-list">
      <?php foreach ($leads as $l): ?>
        <li><div><strong><?= e($l['name']) ?></strong> <span class="pill s-<?= e($l['status']) ?>"><?= e(LEAD_STATUSES[$l['status']] ?? $l['status']) ?></span><br>
          <small><?= e($l['phone']) ?> <?= e($l['email']) ?><?= $l['property'] ? ' · ' . e($l['property']) : '' ?></small></div>
          <small class="muted"><?= e(date('M j, g:ia', strtotime($l['created_at']))) ?></small></li>
      <?php endforeach ?>
    </ul>
  </section>
  <section class="card">
    <div class="card-head"><h2>Recently updated listings</h2><a href="/admin/listings/">All listings →</a></div>
    <ul class="simple-list">
      <?php foreach ($recent as $r): ?>
        <li><a class="row-link" href="/admin/listings/<?= $r['id'] ?>/"><img class="thumb" src="<?= e($r['photo'] ?: '/assets/img/Houston-High-Rise.webp') ?>" alt=""><span><strong><?= e($r['name']) ?></strong><br><small class="muted">by <?= e($r['updated_by'] ?: 'Rise sync') ?></small></span></a>
          <span class="pill <?= $r['status'] === 'publish' ? 's-leased' : 's-closed' ?>"><?= $r['status'] === 'publish' ? 'Live' : 'Hidden' ?></span></li>
      <?php endforeach ?>
    </ul>
  </section>
</div>
<section class="card help">
  <h2>Quick guide</h2>
  <ol>
    <li><strong>Add a listing</strong> – click “＋ Add a listing”, fill in the name and address, upload photos, add floor plans and starting prices, then click <em>Save listing</em>.</li>
    <li><strong>Edit a listing</strong> – go to <em>Listings</em>, search by name, click it, change anything, and save. Listings imported from Rise stop syncing once you edit them, so your changes are never overwritten.</li>
    <li><strong>Hide a listing</strong> – set <em>Show on website</em> to “Hidden” (useful when a property is full). It stays in the admin so you can turn it back on later.</li>
    <li><strong>Leads</strong> – every website request lands in <em>Leads</em> and is emailed to <?= e(config('lead_email') ?: 'the team') ?>. Update the status as you work them.</li>
  </ol>
</section>
