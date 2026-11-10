<h1>Dashboard</h1>
<div class="stat-grid">
  <div class="stat card"><span>Members</span><strong><?= number_format($stats['users']) ?></strong><small>+<?= $stats['new7'] ?> this week</small></div>
  <div class="stat card"><span>Active (7 days)</span><strong><?= number_format($stats['active7']) ?></strong><small><?= $stats['suspended'] ?> suspended</small></div>
  <div class="stat card"><span>Messages</span><strong><?= number_format($stats['messages']) ?></strong><small><?= number_format($stats['messages7']) ?> this week</small></div>
  <div class="stat card"><span>Friendships</span><strong><?= number_format($stats['friendships']) ?></strong><small><?= number_format($stats['posts']) ?> posts</small></div>
  <div class="stat card"><span>Properties</span><strong><?= number_format($stats['properties']) ?></strong><small><?= number_format($stats['interests']) ?> renter interests</small></div>
  <a class="stat card <?= $stats['pending'] ? 'stat-warn' : '' ?>" href="/admin/properties?status=pending"><span>Pending properties</span><strong><?= $stats['pending'] ?></strong><small>Review →</small></a>
  <a class="stat card <?= $stats['reports'] ? 'stat-danger' : '' ?>" href="/admin/reports"><span>Open reports</span><strong><?= $stats['reports'] ?></strong><small>Review →</small></a>
</div>
<section class="card">
  <h3 class="card-title">Sign-ups, last 30 days</h3>
  <?php $max = max(1, max(array_column($series, 'n'))); ?>
  <div class="bars" role="img" aria-label="Daily sign-ups">
    <?php foreach ($series as $s): ?><div class="bar" style="--v:<?= round($s['n'] / $max * 100) ?>%" title="<?= e(date('M j', strtotime($s['d']))) ?>: <?= $s['n'] ?>"><span><?= $s['n'] ?: '' ?></span></div><?php endforeach; ?>
  </div>
  <div class="bars-axis muted small"><span><?= e(date('M j', strtotime($series[0]['d']))) ?></span><span>Today</span></div>
</section>
<div class="layout-2 even">
  <section class="card">
    <h3 class="card-title">Newest members</h3>
    <table class="table"><tbody>
      <?php foreach ($recentUsers as $u): ?>
      <tr><td><a class="cell-user" href="/admin/users/<?= (int)$u['id'] ?>"><?= avatar($u, 'xs') ?> <?= e($u['name']) ?></a></td><td class="muted small">@<?= e($u['username']) ?></td><td class="muted small"><?= e(time_ago($u['created_at'])) ?></td></tr>
      <?php endforeach; ?>
    </tbody></table>
  </section>
  <section class="card">
    <h3 class="card-title">Most wanted properties</h3>
    <table class="table"><tbody>
      <?php foreach ($topProps as $p): ?>
      <tr><td><a href="/properties/<?= e($p['slug']) ?>"><?= e($p['name']) ?></a></td><td class="num"><?= (int)$p['n'] ?> renters</td></tr>
      <?php endforeach; ?>
      <?php if (!$topProps): ?><tr><td class="muted">No properties yet. <a href="/admin/properties/new">Add one</a>.</td></tr><?php endif; ?>
    </tbody></table>
  </section>
</div>
