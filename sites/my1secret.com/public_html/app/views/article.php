<?php defined('M1S') || exit; ?>
<div class="layout layout-article">
  <article class="content article">
    <header class="article-head">
      <?php if ($a['topic_slug']): ?><a class="eyebrow" href="<?= e(topic_url($a['topic_slug'])) ?>"><?= e($a['topic_name']) ?></a><?php endif; ?>
      <h1><?= e($a['title']) ?></h1>
      <?php if ($a['status'] !== 'published'): ?><p class="notice">Draft: only admins can see this.</p><?php endif; ?>
      <div class="byline">
        <span>By <a href="/author/<?= e($a['author_username'] ?: 'meagan') ?>/" rel="author"><?= e($a['author_name'] ?: 'My 1 Secret') ?></a></span>
        <span>Published <time datetime="<?= e(iso_date($a['published_at'])) ?>"><?= e(nice_date($a['published_at'])) ?></time></span>
        <?php if (substr($a['updated_at'], 0, 10) > substr($a['published_at'], 0, 10)): ?><span>Updated <time datetime="<?= e(iso_date($a['updated_at'])) ?>"><?= e(nice_date($a['updated_at'])) ?></time></span><?php endif; ?>
        <span><?= (int)$a['reading_minutes'] ?> min read</span>
        <a href="#comments"><?= plural((int)$a['comment_count'], 'comment') ?></a>
      </div>
    </header>
    <?php if ($a['image']): ?>
      <figure class="hero-img"><img src="<?= e($a['image']) ?>" alt="<?= e($a['image_alt'] ?: $a['title']) ?>" width="<?= (int)$a['image_w'] ?>" height="<?= (int)$a['image_h'] ?>" fetchpriority="high"><?php if (!empty($a['image_credit'])): ?><figcaption class="credit"><?= !empty($a['image_credit_url']) ? '<a href="' . e($a['image_credit_url']) . '" target="_blank" rel="noopener nofollow">' . e($a['image_credit']) . '</a>' : e($a['image_credit']) ?></figcaption><?php endif; ?></figure>
    <?php endif; ?>
    <?php if ($toc): ?>
      <details class="toc" open>
        <summary>In this guide</summary>
        <ol><?php foreach ($toc as [$id, $text]): ?><li><a href="#<?= e($id) ?>"><?= e(preg_replace('/^\d+\.\s*/', '', $text)) ?></a></li><?php endforeach; ?></ol>
      </details>
    <?php endif; ?>
    <div class="prose">
      <?= $bodyHtml ?>
    </div>
    <?= product_box(products_for_article($a)) ?>
    <footer class="article-foot">
      <div class="helpful">
        <span>Was this guide helpful?</span>
        <?= vote_box('article', (int)$a['id'], (int)$a['score'], $myVote, true, 'vote-inline') ?>
      </div>
      <?php if ($community): ?>
        <div class="discuss-cta">
          <p><strong>Have a question this guide didn't answer?</strong> Ask the <a href="<?= e(community_url($community)) ?>"><?= e($community['name']) ?></a> community.</p>
          <a class="btn btn-accent btn-sm" href="/submit/?c=<?= e($community['slug']) ?>">Ask the community</a>
        </div>
      <?php endif; ?>
    </footer>
    <?= comment_section($tree, $commentVotes, 'article', (int)$a['id'], (int)$a['comment_count'], false, $sort) ?>
  </article>
  <aside class="sidebar">
    <section class="widget author-box">
      <h2>About the author</h2>
      <p><strong><a href="/author/<?= e($a['author_username'] ?: 'meagan') ?>/"><?= e($a['author_name'] ?: 'My 1 Secret') ?></a></strong></p>
      <?php $bio = val('SELECT bio FROM users WHERE id = ?', [$a['author_id']]); if ($bio): ?><p><?= e($bio) ?></p><?php endif; ?>
    </section>
    <?php if ($communityThreads): ?>
      <section class="widget">
        <h2>From the <?= e($community['name']) ?> community</h2>
        <?php foreach ($communityThreads as $t): ?>
          <a class="mini-thread" href="<?= e(thread_url($t)) ?>"><span class="mini-score">▲ <?= (int)$t['score'] ?></span><?= e($t['title']) ?></a>
        <?php endforeach; ?>
      </section>
    <?php endif; ?>
    <?php if ($related): ?>
      <section class="widget">
        <h2>Keep reading</h2>
        <?php foreach ($related as $r): ?><?= article_card($r, 'sm') ?><?php endforeach; ?>
      </section>
    <?php endif; ?>
  </aside>
</div>
