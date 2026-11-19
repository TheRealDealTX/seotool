<?php defined('M1S') || exit;
$name = $p['display_name'] ?: $p['username'];
?>
<header class="profile-head">
  <span class="avatar avatar-lg" style="--h:<?= crc32($p['username']) % 360 ?>"><?= e(strtoupper(substr($p['username'], 0, 1))) ?></span>
  <div>
    <h1><?= e($name) ?></h1>
    <p class="muted">u/<?= e($p['username']) ?><?= $p['role'] === 'admin' ? ' · <span class="badge badge-team">team</span>' : ($p['role'] === 'mod' ? ' · <span class="badge badge-mod">mod</span>' : '') ?> · <?= number_format((int)$p['karma']) ?> karma · joined <?= e(nice_date($p['created_at'])) ?></p>
    <?php if ($p['bio']): ?><p><?= e($p['bio']) ?></p><?php endif; ?>
    <?php if ($p['banned']): ?><p class="notice">This account is suspended.</p><?php endif; ?>
    <?php if ($counts['articles']): ?><p><a href="/author/<?= e($p['username']) ?>/">Read <?= plural($counts['articles'], 'article') ?> by <?= e($name) ?> →</a></p><?php endif; ?>
  </div>
</header>
<nav class="sort-tabs" aria-label="Profile">
  <a href="<?= e(user_url($p)) ?>"<?= $tab === 'posts' ? ' aria-current="true"' : '' ?>>Posts (<?= $counts['posts'] ?>)</a>
  <a href="<?= e(user_url($p)) ?>?tab=comments" rel="nofollow"<?= $tab === 'comments' ? ' aria-current="true"' : '' ?>>Comments (<?= $counts['comments'] ?>)</a>
</nav>
<div class="feed narrow-feed">
<?php if ($tab === 'posts'): ?>
  <?php foreach ($items as $t): ?><?= thread_row($t, $votes[(int)$t['id']] ?? 0) ?><?php endforeach; ?>
<?php else: ?>
  <?php foreach ($items as $c):
    $link = $c['target_type'] === 'thread'
      ? ($c['thread_id'] ? '/forum/' . $c['community_slug'] . '/' . $c['thread_id'] . '-' . $c['thread_slug'] . '/' : null)
      : ($c['article_slug'] ? '/blog/' . $c['article_slug'] . '/' : null);
    $on = $c['thread_title'] ?? $c['article_title'] ?? '';
  ?>
    <article class="comment-card">
      <div class="meta">Commented on <?= $link ? '<a href="' . e($link) . '">' . e($on) . '</a>' : e($on) ?> · <?= e(time_ago($c['created_at'])) ?> · <?= plural((int)$c['score'], 'point') ?></div>
      <div class="prose-sm"><?= $c['body_html'] ?></div>
      <?php if ($link): ?><a class="muted" href="<?= e($link) ?>#c<?= (int)$c['id'] ?>">View in context →</a><?php endif; ?>
    </article>
  <?php endforeach; ?>
<?php endif; ?>
<?php if (!$items): ?><p class="empty">Nothing here yet.</p><?php endif; ?>
</div>
<?= pager($page, $hasNext, user_url($p) . ($tab === 'comments' ? '?tab=comments' : '')) ?>
