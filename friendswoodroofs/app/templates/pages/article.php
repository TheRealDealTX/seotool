<?php
/** @var array $page */
$a = $page['article'];
$c = article_content($a['slug']);
$others = array_filter(articles(), fn ($x) => $x['slug'] !== $a['slug']);
$words = str_word_count(strip_tags($c['body']));
$minutes = max(1, (int) round($words / 220));
?>
<article class="article" aria-labelledby="article-title">
  <header class="article-header">
    <div class="container narrow">
      <p class="card-meta"><a class="tag" href="/blog/?category=<?= e($a['category_slug']) ?>"><?= e($a['category']) ?></a></p>
      <h1 id="article-title"><?= e($a['title']) ?></h1>
      <p class="article-byline">
        By <a href="/about/">Friendswood Roofers Editorial Team</a>
        <span aria-hidden="true">&middot;</span>
        Published <time datetime="<?= e($a['date']) ?>"><?= e(display_date($a['date'])) ?></time>
        <span aria-hidden="true">&middot;</span>
        <?= $minutes ?> min read
      </p>
    </div>
  </header>

  <div class="container narrow">
    <figure class="article-figure">
      <?= photo($a['image'], '(min-width: 820px) 760px, 100vw', true) ?>
      <figcaption><?= photo_credit($a['image']) ?></figcaption>
    </figure>

    <div class="prose article-body">
      <?= $c['body'] /* trusted, authored HTML from content/articles */ ?>
    </div>

    <?php if (!empty($c['faqs'])): ?>
    <section class="article-faqs" aria-labelledby="article-faq-heading">
      <h2 id="article-faq-heading">Frequently asked questions</h2>
      <?php partial('faq-list', ['items' => $c['faqs']]); ?>
    </section>
    <?php endif; ?>

    <aside class="article-cta" aria-labelledby="article-cta-heading">
      <h2 id="article-cta-heading">Talk to Friendswood Roofers</h2>
      <p>Have a question about your own roof? Send an estimate request or give us a call. We will look at your roof and explain your options in plain language.</p>
      <div class="cta-actions">
        <a class="btn btn-accent" href="/contact/?service=<?= e(rawurlencode($a['services'][0] ?? 'not-sure')) ?>#estimate-form"><?= icon('clipboard') ?><span>Request an Estimate</span></a>
        <a class="btn btn-outline" href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span>Call <?= e(phone_display()) ?></span></a>
      </div>
    </aside>

    <div class="related-grid related-grid--two">
      <section aria-labelledby="rel-services">
        <h2 id="rel-services" class="h3">Related services</h2>
        <ul class="link-list">
          <?php foreach ($a['services'] as $slug): $s = service($slug); if (!$s) continue; ?>
          <li><a href="<?= e($s['url']) ?>"><?= e($s['name']) ?></a></li>
          <?php endforeach; ?>
        </ul>
      </section>
      <section aria-labelledby="rel-articles">
        <h2 id="rel-articles" class="h3">More roofing guides</h2>
        <ul class="link-list">
          <?php foreach ($others as $o): ?>
          <li><a href="<?= e($o['url']) ?>"><?= e($o['title']) ?></a></li>
          <?php endforeach; ?>
        </ul>
      </section>
    </div>
    <p class="article-disclaimer small">This article is general information for homeowners and is not a substitute for an inspection of your roof, legal advice or guidance from your insurance company.</p>
  </div>
</article>
