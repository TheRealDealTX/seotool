<?php
/** @var array $post @var string $html @var array $toc @var array $related @var array $crumbs @var string $topicLabel */
?>
<article class="article">
  <header class="article__hero">
    <div class="article__hero-bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grain"></span></div>
    <div class="wrap article__hero-grid">
      <div class="article__intro">
        <?= breadcrumbs_html($crumbs) ?>
        <?php if ($post['indexable'] && isset(TOPICS[$post['topic']])): ?>
          <a class="chip chip--<?= e($post['topic']) ?>" href="/topics/<?= e($post['topic']) ?>/"><?= e($topicLabel) ?></a>
        <?php endif ?>
        <h1><?= e($post['h1']) ?></h1>
        <p class="article__lede"><?= e($post['desc']) ?></p>
        <div class="byline">
          <span class="byline__who"><span class="byline__avatar" aria-hidden="true"><?= icon('sprout') ?></span><span><strong>Purely Wholesome Farm</strong> Kitchen &amp; Barn Team</span></span>
          <span class="byline__sep" aria-hidden="true"></span>
          <span><?= icon('calendar') ?> <?= $post['modified'] > $post['published'] ? 'Updated <time datetime="' . e($post['modified']) . '">' . fmt_date($post['modified']) . '</time>' : '<time datetime="' . e($post['published']) . '">' . fmt_date($post['published']) . '</time>' ?></span>
          <span><?= icon('clock') ?> <?= (int)$post['minutes'] ?> min read</span>
        </div>
        <?php if ($post['tools']): $t = tools()[$post['tools'][0]]; ?>
          <a class="tool-jump" href="#<?= e($post['tools'][0]) ?>"><span><?= icon($t['icon']) ?></span>Jump to the <?= e($t['name']) ?> <?= icon('arrow') ?></a>
        <?php endif ?>
      </div>
      <?php if ($post['image']): ?>
        <figure class="article__figure">
          <img src="<?= e($post['image']) ?>" alt="<?= e($post['h1']) ?>" width="<?= (int)$post['image_w'] ?>" height="<?= (int)$post['image_h'] ?>" fetchpriority="high">
        </figure>
      <?php endif ?>
    </div>
  </header>

  <div class="wrap article__layout">
    <aside class="article__aside">
      <?php if (count($toc) > 2): ?>
        <nav class="toc" aria-label="On this page" data-toc>
          <button class="toc__toggle" type="button" aria-expanded="false" data-toc-toggle><?= icon('book') ?> On this page <?= icon('chevron') ?></button>
          <ol class="toc__list">
            <?php foreach ($toc as [$id, $label]): ?><li><a href="#<?= e($id) ?>"><?= e($label) ?></a></li><?php endforeach ?>
            <?php if ($post['faq']): ?><li><a href="#faq">Frequently asked questions</a></li><?php endif ?>
          </ol>
        </nav>
      <?php endif ?>
      <div class="share">
        <span>Share</span>
        <a href="https://www.pinterest.com/pin/create/button/?url=<?= rawurlencode(canonical(post_url($post['slug']))) ?>&amp;description=<?= rawurlencode($post['h1']) ?>" target="_blank" rel="noopener" aria-label="Save to Pinterest">P</a>
        <a href="https://www.facebook.com/sharer/sharer.php?u=<?= rawurlencode(canonical(post_url($post['slug']))) ?>" target="_blank" rel="noopener" aria-label="Share on Facebook">f</a>
        <button type="button" data-copy-link aria-label="Copy link"><?= icon('link') ?></button>
        <button type="button" onclick="window.print()" aria-label="Print"><?= icon('print') ?></button>
      </div>
    </aside>

    <div class="article__main">
      <?php if ($post['sponsored'] && !$post['indexable']): ?>
        <p class="notice"><?= icon('sparkle') ?> This is a partner article from our archive. It is kept online for reference; outbound links are sponsored.</p>
      <?php elseif ($post['sponsored']): ?>
        <p class="notice"><?= icon('sparkle') ?> This article mentions products or services from partners. Links to them are marked as sponsored.</p>
      <?php endif ?>
      <div class="prose">
        <?= $html ?>
      </div>

      <?php if ($post['faq']): ?>
        <section class="article__faq" id="faq">
          <h2>Frequently asked questions</h2>
          <div class="faq">
            <?php foreach ($post['faq'] as $i => $f): ?>
              <details class="faq__item" <?= $i === 0 ? 'open' : '' ?>><summary><?= e($f['q']) ?><span class="faq__icon" aria-hidden="true"></span></summary><div class="faq__a"><p><?= $f['a'] ?></p></div></details>
            <?php endforeach ?>
          </div>
        </section>
      <?php endif ?>

      <?php if (count($post['tools']) > 1): ?>
        <div class="embed-tool"><?= render_tool($post['tools'][1]) ?></div>
      <?php endif ?>

      <aside class="author-box">
        <span class="author-box__mark" aria-hidden="true"><?= icon('sprout') ?></span>
        <div>
          <h2>From the Purely Wholesome Farm kitchen &amp; barn</h2>
          <p>We write from hands-on experience cooking from scratch and caring for goats and chickens, and we check food safety and animal health details against USDA, extension and veterinary sources. Spotted something we should fix? <a href="/contact-us/">Tell us</a>. Read our <a href="/editorial-policy/">editorial policy</a>.</p>
        </div>
      </aside>
    </div>
  </div>
</article>

<?php if ($related): ?>
<section class="section section--cream">
  <div class="wrap">
    <header class="section__head section__head--row">
      <div><p class="eyebrow">Keep reading</p><h2>More from <?= e($topicLabel) ?></h2></div>
      <?php if (isset(TOPICS[$post['topic']])): ?><a class="btn btn--ghost" href="/topics/<?= e($post['topic']) ?>/">See all <?= icon('arrow') ?></a><?php endif ?>
    </header>
    <div class="cards cards--4">
      <?php foreach ($related as $p): ?><?= card($p, 'reveal') ?><?php endforeach ?>
    </div>
  </div>
</section>
<?php endif ?>
