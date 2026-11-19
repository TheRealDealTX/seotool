<?php defined('M1S') || exit; ?>
<h1>Admin</h1>
<?= view('admin/_nav') ?>
<div class="stat-grid">
  <?php foreach ($stats as $k => $v): ?><div class="stat"><strong><?= number_format($v) ?></strong><span><?= e($k) ?></span></div><?php endforeach; ?>
</div>
<div class="layout">
  <section class="content">
    <h2>Newest posts</h2>
    <table class="table"><thead><tr><th>Post</th><th>By</th><th>Score</th><th>When</th></tr></thead><tbody>
    <?php foreach ($recentThreads as $t): ?>
      <tr<?= $t['removed'] ? ' class="muted"' : '' ?>><td><a href="<?= e(thread_url($t)) ?>"><?= e(mb_strimwidth($t['title'], 0, 70, '…')) ?></a> <span class="muted"><?= e($t['community_name']) ?></span></td><td><?= e((string)$t['username']) ?></td><td><?= (int)$t['score'] ?></td><td><?= e(time_ago($t['created_at'])) ?></td></tr>
    <?php endforeach; ?>
    </tbody></table>
  </section>
  <section class="sidebar">
    <h2>Newest comments</h2>
    <?php foreach ($recentComments as $c): ?>
      <p class="small"><strong><?= e((string)$c['username']) ?></strong>: <?= e(excerpt($c['body'], 90)) ?> <span class="muted"><?= e(time_ago($c['created_at'])) ?></span></p>
    <?php endforeach; ?>
  </section>
</div>
