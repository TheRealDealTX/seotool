<?php
/** @var array $post */
$url = SITE_URL . '/blog/' . $post['slug'] . '/';
$meta['title'] = $post['title'];
$meta['description'] = $post['description'];
$meta['crumb'] = $post['title'];
$meta['og_type'] = 'article';
$meta['schema'][] = ['@type' => 'BlogPosting', 'headline' => $post['title'], 'description' => $post['description'], 'url' => $url,
    'mainEntityOfPage' => $url, 'datePublished' => $post['date'], 'dateModified' => $post['date'], 'keywords' => $post['keyword'],
    'articleSection' => $post['category'], 'image' => SITE_URL . '/assets/img/og.png',
    'author' => ['@type' => 'Person', 'name' => AUTHOR, 'jobTitle' => AUTHOR_ROLE, 'url' => SITE_URL . '/about/'],
    'publisher' => ['@id' => SITE_URL . '/#business']];
$faqs = array_map(fn($f) => [$f['q'], '<p>' . e($f['a']) . '</p>'], $post['faq'] ?? []);
$initials = implode('', array_map(fn($w) => $w[0], explode(' ', AUTHOR)));
$related = array_slice(array_values(array_filter(blog_posts(), fn($p) => $p['slug'] !== $post['slug'])), 0, 3);
?>
<section class="hero hero-sub">
  <div class="wrap narrow" style="position:relative;padding:56px 0 96px">
    <a href="/blog/" style="color:#9fc3dc;text-decoration:none">← All claim guides</a>
    <div class="post-meta" style="color:#cfe4f3;margin-top:14px"><span class="tag"><?= e($post['category']) ?></span><span><?= (int)$post['read_minutes'] ?> min read</span></div>
    <h1><?= e($post['title']) ?></h1>
    <div class="byline"><span class="avatar"><?= e($initials) ?></span><div>By <strong style="color:#fff"><?= AUTHOR ?></strong>, <?= AUTHOR_ROLE ?><br><time datetime="<?= e($post['date']) ?>"><?= fmt_date($post['date']) ?></time></div></div>
  </div>
  <?= wave_divider() ?>
</section>
<section class="section" style="padding-top:40px">
  <div class="wrap layout-side">
    <article class="prose">
      <?= $post['html'] ?>
      <?php if ($faqs): ?><h2>Frequently asked questions</h2><?= faq_block($faqs, $meta['schema']) ?><?php endif ?>
      <div class="author-box"><span class="avatar"><?= e($initials) ?></span><div><strong><?= AUTHOR ?></strong> is a <?= strtolower(AUTHOR_ROLE) ?> serving Galveston Island and Galveston County. Joseph represents policyholders on TWIA windstorm, hurricane, fire, flood and denied claims. <a href="/about/">More about Joseph</a> · <?= phone_link('', PHONE) ?></div></div>
      <?= banner('Want a second opinion on your claim? Call for an expert consultation.', 'Free review — no recovery, no fee.') ?>
      <p class="small muted">This article is general information, not legal advice. Every policy and claim is different.</p>
    </article>
    <aside class="sidebar">
      <div class="side-card dark"><h3>Talk to <?= explode(' ', AUTHOR)[0] ?></h3><p>Free expert consultation on your claim.</p><?= phone_link('btn btn-cta btn-block', icon('phone', 18) . ' ' . PHONE) ?></div>
      <div class="side-card"><h3>Free claim review</h3><?= lead_form('blog', true) ?></div>
      <?php if ($related): ?><div class="side-card"><h3>More guides</h3><ul><?php foreach ($related as $r): ?><li><a href="/blog/<?= e($r['slug']) ?>/"><?= e($r['title']) ?></a></li><?php endforeach ?></ul></div><?php endif ?>
    </aside>
  </div>
</section>
