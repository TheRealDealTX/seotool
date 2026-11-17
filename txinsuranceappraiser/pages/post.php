<?php
/** /{slug}/ — blog post. */
$p    = $post;
$path = '/' . $p['slug'] . '/';
$img  = post_image($p);
$mins = reading_minutes($p['body_html']);
$pub  = $p['published'] ?? '';
$upd  = $p['updated'] ?? $pub;
$cat  = $p['category'] ?? 'Insurance Basics';

// related: same category first, then others
$all = posts();
unset($all[$p['slug']]);
$same = array_filter($all, fn($x) => ($x['category'] ?? '') === $cat);
$related = array_slice(array_merge(array_values($same), array_values($all)), 0, 3);

ob_start(); ?>
<div class="progress" aria-hidden="true"></div>
<section class="hero post-hero">
  <div class="hero-bg" style="background-image:url(<?= e($img) ?>)"></div>
  <div class="orb orb-1"></div>
  <div class="wrap">
    <span class="eyebrow anim"><?= e($cat) ?></span>
    <h1 class="anim" style="max-width:920px"><?= e($p['h1']) ?></h1>
    <div class="post-meta anim">
      <span class="author-chip"><img class="av" src="<?= SITE['photo'] ?>" alt="Joseph Dittman" width="38" height="38"> <span>By <a href="/about-us/" style="color:#fff">Joseph Dittman</a></span></span>
      <span><?= icon('calendar', 16) ?> Published <time datetime="<?= e(substr($pub, 0, 10)) ?>"><?= e(nice_date($pub)) ?></time></span>
      <span><?= icon('clock', 16) ?> <?= $mins ?> min read</span>
    </div>
  </div>
</section>
<div class="wrap post-layout">
  <article>
    <figure class="post-feature" style="margin:0 0 34px"><img src="<?= e($img) ?>" alt="<?= e($p['h1']) ?>" width="1400" height="788" fetchpriority="high"></figure>
    <?php if (!empty($p['key_takeaways'])): ?>
    <div class="takeaways">
      <h2><?= icon('zap', 20) ?> Key takeaways</h2>
      <ul class="checks"><?php foreach ($p['key_takeaways'] as $t): ?><li><?= e($t) ?></li><?php endforeach; ?></ul>
    </div>
    <?php endif; ?>
    <div class="prose"><?= $p['body_html'] ?></div>
    <?php if (!empty($p['faqs'])): ?>
    <section class="prose" id="faq" style="margin-top:40px">
      <h2 id="faqs">Frequently asked questions</h2>
      <div class="faq-list">
      <?php foreach ($p['faqs'] as $i => $f): ?>
        <details class="faq"<?= $i === 0 ? ' open' : '' ?>><summary><?= e($f['q']) ?><?= icon('chev', 20) ?></summary><div class="faq-a"><p><?= e($f['a']) ?></p></div></details>
      <?php endforeach; ?>
      </div>
    </section>
    <?php endif; ?>
    <div class="author-box">
      <img class="av" src="<?= SITE['photo'] ?>" alt="Joseph Dittman" width="72" height="72" loading="lazy">
      <div>
        <h3>About the author: Joseph Dittman</h3>
        <p style="margin:0;color:var(--ink-2)">Joseph is the lead appraiser at TX Insurance Appraiser and a Texas-licensed public adjuster (Rise Public Adjusting LLC, TDI license #<?= SITE['appraiser']['license'] ?>). He has spent his career inspecting hail, wind, water and fire losses and negotiating property claims across Texas. <a href="/about-us/">More about Joseph</a>.</p>
      </div>
    </div>
    <div class="share">
      <a href="https://www.facebook.com/sharer/sharer.php?u=<?= rawurlencode(abs_url($path)) ?>" target="_blank" rel="noopener">Share on Facebook</a>
      <a href="https://www.linkedin.com/sharing/share-offsite/?url=<?= rawurlencode(abs_url($path)) ?>" target="_blank" rel="noopener">Share on LinkedIn</a>
      <a href="mailto:?subject=<?= rawurlencode($p['h1']) ?>&amp;body=<?= rawurlencode(abs_url($path)) ?>">Email</a>
      <button type="button" data-copy>Copy link</button>
    </div>
    <p style="font-size:.85rem;color:var(--ink-2);margin-top:22px">This article is general information about property insurance claims in Texas and is not legal advice. Policy language and facts vary; review your policy or consult a Texas attorney for legal questions.</p>
  </article>
  <aside class="sidebar">
    <div class="sticky">
      <nav class="toc" aria-label="Table of contents"><h2>In this article</h2><ol data-toc></ol></nav>
      <div class="side-cta">
        <h3>Underpaid claim?</h3>
        <p style="font-size:.95rem">Get a free review from TX Insurance Appraiser. We’ll tell you honestly whether appraisal makes sense.</p>
        <a class="btn btn-gold btn-block" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 18) ?> <?= e(SITE['phone_short']) ?></a>
        <a class="btn btn-ghost-light btn-block" style="margin-top:10px" href="/contact-us/">Request a review</a>
      </div>
      <div class="toc">
        <h2>Free tools</h2>
        <ol>
          <?php foreach (TOOLS as $slug => $t): ?><li><a href="/tools/<?= $slug ?>/"><?= e($t['title']) ?></a></li><?php endforeach; ?>
        </ol>
      </div>
    </div>
  </aside>
</div>
<?php if ($related): ?>
<section class="section bg-mist">
  <div class="wrap">
    <h2 class="sec-title reveal">Related articles</h2>
    <div class="grid g3">
      <?php foreach ($related as $r): ?>
      <article class="card card-img reveal">
        <a class="ci-media" href="/<?= $r['slug'] ?>/"><img src="<?= post_image($r) ?>" alt="<?= e($r['h1']) ?>" width="700" height="394" loading="lazy"></a>
        <div class="ci-body"><span class="pill"><?= e($r['category'] ?? '') ?></span><h3><a href="/<?= $r['slug'] ?>/" style="text-decoration:none;color:inherit"><?= e($r['h1']) ?></a></h3><p><?= e($r['excerpt'] ?? '') ?></p></div>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?php endif; ?>
<?= cta_band() ?>
<?php
$content = (string) ob_get_clean();
$article = [
    '@type' => 'BlogPosting',
    '@id' => abs_url($path) . '#article',
    'headline' => $p['h1'],
    'description' => $p['meta_description'],
    'image' => abs_url($img),
    'datePublished' => $pub,
    'dateModified' => $upd,
    'author' => ['@id' => SITE['origin'] . '/#joseph-dittman'],
    'publisher' => ['@id' => SITE['origin'] . '/#business'],
    'mainEntityOfPage' => abs_url($path),
    'articleSection' => $cat,
    'keywords' => implode(', ', array_merge([$p['primary_keyword'] ?? ''], $p['secondary_keywords'] ?? [])),
    'wordCount' => str_word_count(strip_tags($p['body_html'])),
    'inLanguage' => 'en-US',
];
$schema = [$article];
if (!empty($p['faqs'])) {
    $schema[] = schema_faq($p['faqs']);
}
render_page([
    'title' => $p['seo_title'], 'description' => $p['meta_description'], 'path' => $path,
    'image' => $img, 'og_type' => 'article',
    'head_extra' => '<meta property="article:published_time" content="' . e($pub) . '"><meta property="article:modified_time" content="' . e($upd) . '"><meta property="article:section" content="' . e($cat) . '">',
    'crumbs' => [['Home', '/'], ['Blog', '/blog/'], [$p['h1'], $path]],
    'schema' => $schema,
], $content);
