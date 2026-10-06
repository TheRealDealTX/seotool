<?php defined('SLT') || exit;
$slug = $GLOBALS['SLUG']; $p = POSTS[$slug]; $cat = CATEGORIES[$p['cat']];
ob_start(); include APP . '/posts/' . $slug . '.php'; [$content, $toc] = with_toc(ob_get_clean());
$mins = reading_time($content);
add_schema(['@type' => 'BlogPosting', '@id' => abs_url('/' . $slug . '/') . '#article', 'headline' => $p['title'], 'description' => $p['desc'],
    'image' => abs_url('/assets/img/' . $p['img']), 'datePublished' => $p['date'] . 'T08:00:00-05:00', 'dateModified' => ($p['updated'] ?? $p['date']) . 'T08:00:00-05:00',
    'author' => ['@type' => 'Organization', 'name' => BRAND, 'url' => SITE_URL . '/'], 'publisher' => ['@id' => SITE_URL . '/#business'],
    'mainEntityOfPage' => abs_url('/' . $slug . '/'), 'articleSection' => $cat['name'], 'wordCount' => str_word_count(strip_tags($content)), 'inLanguage' => 'en-US']);
page_hero(['title' => e($p['title']), 'img' => $p['img'], 'eyebrow' => $cat['name'],
    'meta' => '<span>' . icon('calendar') . fmt_date($p['date']) . '</span>' . (!empty($p['updated']) ? '<span>' . icon('sparkles') . 'Updated ' . fmt_date($p['updated']) . '</span>' : '') . '<span>' . icon('clock') . $mins . ' min read</span><span>' . icon('lightbulb') . e(BRAND) . '</span>',
    'crumbs' => [['Home', '/'], ['Blog', '/blog/'], [$p['title'], null]]]);
$related = array_filter(POSTS, fn($k) => $k !== $slug, ARRAY_FILTER_USE_KEY);
uksort($related, fn($a, $b) => (POSTS[$b]['cat'] === $p['cat']) <=> (POSTS[$a]['cat'] === $p['cat']));
?>
<section class="sec" style="padding-top:30px">
  <div class="wrap article">
    <article class="prose">
      <?= $content ?>
      <div class="author"><img src="/assets/img/icon-192.webp" alt="" width="64" height="64" loading="lazy"><p><strong><?= e(BRAND) ?></strong><br>Landscape lighting designers serving Spring, Klein, The Woodlands and North Houston. Questions about your property? <a href="/contact/">Get in touch</a>.</p></div>
      <div class="share">Share:
        <a href="https://www.facebook.com/sharer/sharer.php?u=<?= rawurlencode(abs_url('/' . $slug . '/')) ?>" target="_blank" rel="noopener" aria-label="Share on Facebook">f</a>
        <a href="https://twitter.com/intent/tweet?url=<?= rawurlencode(abs_url('/' . $slug . '/')) ?>&amp;text=<?= rawurlencode($p['title']) ?>" target="_blank" rel="noopener" aria-label="Share on X">𝕏</a>
        <a href="mailto:?subject=<?= rawurlencode($p['title']) ?>&amp;body=<?= rawurlencode(abs_url('/' . $slug . '/')) ?>" aria-label="Share by email"><?= icon('mail') ?></a>
        <button type="button" data-copy aria-label="Copy link"><?= icon('layers') ?></button>
      </div>
    </article>
    <aside class="aside">
      <?php if (count($toc) > 2): ?><nav class="toc" aria-label="Table of contents"><h4>In this article</h4><ol><?php foreach ($toc as [$id, $t]) echo '<li><a href="#' . $id . '">' . e($t) . '</a></li>'; ?></ol></nav><?php endif; ?>
      <div class="side-cta"><span class="eyebrow eyebrow--glow">Free consultation</span><h4>Want a plan for your home?</h4><p>Spring Landscape Lighting designs and installs custom LED systems.</p><a class="btn btn--glow" href="/quote/">Request a quote</a></div>
    </aside>
  </div>
</section>
<section class="sec sec--forest">
  <div class="wrap">
    <?php section_head('Keep reading', 'Related articles'); ?>
    <div class="grid-3"><?php $i = 0; foreach ($related as $k => $r) { if ($i++ >= 3) break; echo post_card($k, $r); } ?></div>
  </div>
</section>
<?php cta_band(); ?>
