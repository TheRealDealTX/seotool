<?php defined('M1S') || exit;
$lead = $articles[0] ?? null;
$rest = array_slice($articles, 1, 6);
?>
<section class="hero">
  <div>
    <p class="eyebrow">Blog + community forum</p>
    <h1>Real-life secrets for renters, homeowners &amp; Texans</h1>
    <p class="lede">Practical guides on apartment living, small-space design and insurance claims, plus a community where real people share the one tip they wish they had known sooner.</p>
    <div class="hero-actions">
      <a class="btn btn-accent" href="/blog/">Read the guides</a>
      <a class="btn btn-ghost" href="<?= current_user() ? '/submit/' : '/register/' ?>"><?= current_user() ? 'Share your secret' : 'Join the community' ?></a>
    </div>
  </div>
  <ul class="hero-stats" aria-label="Community stats">
    <li><strong><?= number_format($stats['articles']) ?></strong> in-depth guides</li>
    <li><strong><?= count(communities()) ?></strong> communities</li>
    <li><strong><?= number_format($stats['threads']) ?></strong> discussions</li>
  </ul>
</section>

<div class="layout">
  <div class="content">
    <?php if ($lead): ?>
    <section aria-labelledby="latest-h">
      <div class="section-head"><h2 id="latest-h">Latest from the blog</h2><a href="/blog/">All articles →</a></div>
      <?= article_card($lead, 'lg') ?>
      <div class="card-grid">
        <?php foreach ($rest as $a): ?><?= article_card($a) ?><?php endforeach; ?>
      </div>
    </section>
    <?php endif; ?>

    <section aria-labelledby="hot-h" class="block">
      <div class="section-head"><h2 id="hot-h">Hot in the community</h2><a href="/forum/">Browse the forum →</a></div>
      <div class="feed">
        <?php foreach ($hot as $t): ?><?= thread_row($t, $votes[(int)$t['id']] ?? 0) ?><?php endforeach; ?>
        <?php if (!$hot): ?><p class="empty">No discussions yet. <a href="/submit/">Start the first one.</a></p><?php endif; ?>
      </div>
    </section>
  </div>

  <aside class="sidebar">
    <section class="widget widget-accent">
      <h2>What's your one secret?</h2>
      <p>Everyone has one tip that changed everything. Post yours in <a href="/forum/one-secret/">One Secret</a> and vote up the ones that help you.</p>
      <?php foreach ($secrets as $s): ?>
        <a class="mini-thread" href="<?= e(thread_url($s)) ?>"><span class="mini-score">▲ <?= (int)$s['score'] ?></span><?= e($s['title']) ?></a>
      <?php endforeach; ?>
      <a class="btn btn-accent btn-block" href="/submit/?c=one-secret">Share a secret</a>
    </section>
    <?= communities_widget() ?>
    <?= topics_widget() ?>
  </aside>
</div>
