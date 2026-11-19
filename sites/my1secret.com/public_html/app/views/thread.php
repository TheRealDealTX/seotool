<?php defined('M1S') || exit;
$me = current_user();
$own = $me && (int)$me['id'] === (int)$t['user_id'];
?>
<div class="layout">
  <div class="content">
    <article class="thread<?= $t['removed'] ? ' is-removed' : '' ?>">
      <?= vote_box('thread', (int)$t['id'], (int)$t['score'], $myVote) ?>
      <div class="thread-main">
        <div class="meta">
          <?= community_chip($t) ?> · Posted by <?= $t['deleted'] ? '<span class="muted">[deleted]</span>' : user_label($t) ?>
          · <time datetime="<?= e(iso_date($t['created_at'])) ?>" title="<?= e(nice_date($t['created_at'])) ?>"><?= e(time_ago($t['created_at'])) ?></time>
          <?php if ($t['edited_at'] && !$t['deleted']): ?><span class="muted">· edited</span><?php endif; ?>
          <?php if ($t['pinned']): ?><span class="badge badge-pin">pinned</span><?php endif; ?>
          <?php if ($t['locked']): ?><span class="badge">locked</span><?php endif; ?>
          <?php if ($t['removed']): ?><span class="badge badge-danger">removed</span><?php endif; ?>
        </div>
        <h1 class="thread-h1"><?= e($t['title']) ?></h1>
        <?php if ($t['link_url'] && !$t['deleted']): ?>
          <p><a class="link-card" href="<?= e($t['link_url']) ?>" rel="nofollow ugc noopener" target="_blank"><?= e(mb_strimwidth($t['link_url'], 0, 80, '…')) ?> ↗</a></p>
        <?php endif; ?>
        <?php if ($t['image'] && !$t['deleted']): ?>
          <figure class="thread-img"><img src="<?= e($t['image']) ?>" alt="<?= e($t['title']) ?>" width="<?= (int)$t['image_w'] ?>" height="<?= (int)$t['image_h'] ?>"></figure>
        <?php endif; ?>
        <div class="prose prose-sm">
          <?= $t['deleted'] ? '<p class="muted">The author deleted this post.</p>' : $t['body_html'] ?>
        </div>
        <div class="thread-actions">
          <a href="#comments">💬 <?= plural((int)$t['comment_count'], 'comment') ?></a>
          <button type="button" class="action linklike" data-share="<?= e(abs_url(thread_url($t))) ?>">Share</button>
          <?php if ($own && !$t['deleted']): ?>
            <a class="action" href="<?= e(thread_url($t)) ?>edit/">Edit</a>
            <form method="post" action="/thread/<?= (int)$t['id'] ?>/delete/" data-confirm="Delete this post? Comments stay visible."><?= csrf_field() ?><button class="action linklike">Delete</button></form>
          <?php elseif ($me && !$t['deleted']): ?>
            <a class="action" href="/report/?type=thread&amp;id=<?= (int)$t['id'] ?>" rel="nofollow">Report</a>
          <?php endif; ?>
          <?php if ($me && is_mod($me)): ?>
            <span class="mod-tools">
              <?php foreach ([$t['pinned'] ? 'unpin' : 'pin', $t['locked'] ? 'unlock' : 'lock', $t['removed'] ? 'restore' : 'remove'] as $act): ?>
                <form method="post" action="/thread/<?= (int)$t['id'] ?>/mod/"><?= csrf_field() ?><input type="hidden" name="action" value="<?= $act ?>"><button class="action linklike<?= $act === 'remove' ? ' danger' : '' ?>"><?= ucfirst($act) ?></button></form>
              <?php endforeach; ?>
              <?php if (!$own): ?><a class="action" href="<?= e(thread_url($t)) ?>edit/">Edit</a><?php endif; ?>
            </span>
          <?php endif; ?>
        </div>
      </div>
    </article>
    <?= comment_section($tree, $commentVotes, 'thread', (int)$t['id'], (int)$t['comment_count'], (bool)$t['locked'] || (bool)$t['deleted'], $sort) ?>
  </div>
  <aside class="sidebar">
    <section class="widget" style="--c:<?= e($c['color']) ?>">
      <h2><?= e($c['name']) ?></h2>
      <p><?= e($c['description']) ?></p>
      <a class="btn btn-ghost btn-block" href="<?= e(community_url($c)) ?>">View community</a>
      <a class="btn btn-accent btn-block" href="/submit/?c=<?= e($c['slug']) ?>">Create a post</a>
    </section>
    <?php if ($more): ?>
      <section class="widget">
        <h2>More in <?= e($c['name']) ?></h2>
        <?php foreach ($more as $m): ?>
          <a class="mini-thread" href="<?= e(thread_url($m)) ?>"><span class="mini-score">▲ <?= (int)$m['score'] ?></span><?= e($m['title']) ?></a>
        <?php endforeach; ?>
      </section>
    <?php endif; ?>
  </aside>
</div>
