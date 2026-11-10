<?php /** @var array $p */ $mine = (int)$p['user_id'] === uid(); ?>
<article class="card post" id="post-<?= (int)$p['id'] ?>">
  <header class="post-head">
    <a href="/u/<?= e($p['username']) ?>"><?= avatar(['name' => $p['name'], 'avatar' => $p['avatar']], 'md') ?></a>
    <div class="post-id">
      <a class="post-author" href="/u/<?= e($p['username']) ?>"><?= e($p['name']) ?></a>
      <div class="muted small">
        <a href="/post/<?= (int)$p['id'] ?>"><?= e(time_ago($p['created_at'])) ?></a>
        <?php if (!empty($p['property_name'])): ?> · <a class="post-prop" href="/properties/<?= e($p['property_slug']) ?>"><?= icon('building') ?><?= e($p['property_name']) ?></a><?php endif; ?>
      </div>
    </div>
    <details class="menu menu-right">
      <summary class="iconbtn" aria-label="Post options"><?= icon('more') ?></summary>
      <div class="menu-pop">
        <?php if ($mine || is_admin()): ?>
        <form method="post" action="/post/<?= (int)$p['id'] ?>/delete" data-confirm="Delete this post?"><?= csrf_field() ?><button type="submit"><?= icon('trash') ?> Delete post</button></form>
        <?php endif; ?>
        <?php if (!$mine): ?>
        <button type="button" class="js-report" data-type="post" data-id="<?= (int)$p['id'] ?>"><?= icon('flag') ?> Report post</button>
        <?php endif; ?>
      </div>
    </details>
  </header>
  <div class="post-body"><?= linkify($p['body']) ?></div>
  <?php if ($p['image']): ?><a href="/uploads/posts/<?= e(rawurlencode($p['image'])) ?>" target="_blank" class="post-img"><img src="/uploads/posts/<?= e(rawurlencode($p['image'])) ?>" alt="" loading="lazy"></a><?php endif; ?>
  <footer class="post-actions">
    <form method="post" action="/post/<?= (int)$p['id'] ?>/like" class="js-like">
      <?= csrf_field() ?>
      <button type="submit" class="act <?= $p['liked'] ? 'liked' : '' ?>" aria-pressed="<?= $p['liked'] ? 'true' : 'false' ?>"><?= icon('heart') ?><span class="n"><?= (int)$p['likes'] ?: '' ?></span> Like</button>
    </form>
    <button type="button" class="act js-focus-comment" data-post="<?= (int)$p['id'] ?>"><?= icon('comment') ?><span><?= (int)$p['comments'] ?: '' ?></span> Comment</button>
  </footer>
  <div class="comments">
    <?php foreach ($p['comment_list'] ?? [] as $c): ?>
    <div class="comment" id="comment-<?= (int)$c['id'] ?>">
      <a href="/u/<?= e($c['username']) ?>"><?= avatar(['name' => $c['name'], 'avatar' => $c['avatar']], 'xs') ?></a>
      <div class="comment-bubble">
        <a class="comment-author" href="/u/<?= e($c['username']) ?>"><?= e($c['name']) ?></a>
        <span><?= linkify($c['body']) ?></span>
        <div class="comment-meta muted small"><?= e(time_ago($c['created_at'])) ?>
          <?php if ((int)$c['user_id'] === uid() || $mine || is_admin()): ?>
          · <form method="post" action="/comment/<?= (int)$c['id'] ?>/delete" class="inline" data-confirm="Delete this comment?"><?= csrf_field() ?><button type="submit" class="linkbtn">Delete</button></form>
          <?php elseif ((int)$c['user_id'] !== uid()): ?>
          · <button type="button" class="linkbtn js-report" data-type="comment" data-id="<?= (int)$c['id'] ?>">Report</button>
          <?php endif; ?>
        </div>
      </div>
    </div>
    <?php endforeach; ?>
    <?php if (($p['comments'] ?? 0) > count($p['comment_list'] ?? []) ): ?><a class="small more-comments" href="/post/<?= (int)$p['id'] ?>">View all <?= (int)$p['comments'] ?> comments</a><?php endif; ?>
    <form method="post" action="/post/<?= (int)$p['id'] ?>/comment" class="comment-form">
      <?= csrf_field() ?>
      <?= avatar(current_user(), 'xs') ?>
      <input type="text" name="body" placeholder="Write a comment…" maxlength="1000" required id="c-<?= (int)$p['id'] ?>">
      <button class="iconbtn" type="submit" aria-label="Send"><?= icon('send') ?></button>
    </form>
  </div>
</article>
