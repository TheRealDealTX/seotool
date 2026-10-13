<?php
// Blog post template. A post file calls post_open($slug), prints its article HTML, then post_close($slug).
// The body is buffered so headings can get ids, a table of contents and a mid-article call-to-action.

require_once __DIR__ . '/layout.php';

function slugify(string $s): string {
    return trim(preg_replace('/[^a-z0-9]+/', '-', strtolower(html_entity_decode(strip_tags($s), ENT_QUOTES, 'UTF-8'))), '-');
}

function post_open(string $slug): void {
    ob_start();
}

function post_close(string $slug): void {
    $body = ob_get_clean();
    $p = POSTS[$slug];
    $url = SITE_URL . '/' . $slug . '/';

    // Heading ids + table of contents.
    $toc = [];
    $seen = [];
    $body = preg_replace_callback('#<h2>(.*?)</h2>#s', function ($m) use (&$toc, &$seen) {
        $id = slugify($m[1]) ?: 'section';
        if (isset($seen[$id])) $id .= '-' . (++$seen[$id]); else $seen[$id] = 1;
        $toc[] = [$id, strip_tags($m[1])];
        return '<h2 id="' . $id . '">' . $m[1] . '</h2>';
    }, $body);

    // Mid-article call-to-action before the third H2.
    $n = 0;
    $cta = '<div class="inline-cta"><p><strong>Dealing with this right now?</strong> Houston Public Adjusters will review your claim for free and tell you plainly whether it was paid fairly.</p>'
        . '<p><a class="btn btn-accent" href="tel:' . PHONE_E164 . '">Call ' . PHONE_DISPLAY . '</a> <button class="btn btn-outline" type="button" data-open-lead>Request a Review</button></p></div>';
    $body = preg_replace_callback('#<h2 id=#', function ($m) use (&$n, $cta) {
        return (++$n === 3 ? $cta : '') . $m[0];
    }, $body);

    $minutes = max(1, (int)round($p['words'] / 225));
    $crumbs = [['Home', '/'], ['Blog', '/blog/'], [$p['h1'], '/' . $slug . '/']];

    page_start([
        'title' => $p['title'],
        'desc' => $p['desc'],
        'path' => '/' . $slug . '/',
        'image' => $p['image'],
        'type' => 'article',
        'published' => $p['published'],
        'modified' => $p['modified'],
        'crumbs' => $crumbs,
        'body_class' => 'post',
        'schema' => [[
            '@type' => 'BlogPosting',
            '@id' => $url . '#article',
            'headline' => $p['h1'],
            'description' => $p['desc'],
            'image' => abs_url($p['image']),
            'datePublished' => $p['published'],
            'dateModified' => $p['modified'],
            'wordCount' => $p['words'],
            'author' => ['@id' => SITE_URL . '/#joseph-dittman'],
            'publisher' => ['@id' => SITE_URL . '/#business'],
            'mainEntityOfPage' => ['@id' => $url . '#webpage'],
            'articleSection' => 'Insurance Claims',
            'inLanguage' => 'en-US',
        ]],
    ]);
    ?>
<section class="page-hero post-hero"><div class="wrap">
  <?= breadcrumbs_html($crumbs) ?>
  <p class="eyebrow">Claim Guide</p>
  <h1><?= e($p['h1']) ?></h1>
  <div class="byline">
    <img src="<?= AUTHOR['photo'] ?>" alt="<?= AUTHOR['name'] ?>" width="44" height="44">
    <p>By <a href="<?= AUTHOR['url'] ?>" rel="author"><?= AUTHOR['name'] ?></a>, <?= AUTHOR['title'] ?><br>
    <span>Published <time datetime="<?= e($p['published']) ?>"><?= date('F j, Y', strtotime($p['published'])) ?></time> &middot; Updated <time datetime="<?= e($p['modified']) ?>"><?= date('F j, Y', strtotime($p['modified'])) ?></time> &middot; <?= $minutes ?> min read</span></p>
  </div>
</div></section>
<div class="wrap layout-sidebar">
  <article class="prose">
    <img class="post-feature" src="<?= e($p['image']) ?>" alt="<?= e($p['h1']) ?>" width="1536" height="1024" fetchpriority="high">
<?php if (count($toc) > 2): ?>
    <nav class="toc" aria-label="In this article"><p class="toc-h">In this article</p><ol>
<?php foreach ($toc as [$id, $text]): ?>      <li><a href="#<?= $id ?>"><?= e($text) ?></a></li>
<?php endforeach; ?>
    </ol></nav>
<?php endif; ?>
    <?= $body ?>
    <p class="disclaimer">This article is general information from a licensed Texas public adjuster, not legal advice. Every policy and loss is different — <a href="/contact/">ask us to review yours</a>.</p>
    <?= author_box() ?>
  </article>
  <aside class="sidebar">
    <div class="side-card sticky">
      <?= lead_form('lead-sidebar', 'Free Claim Review', 'A licensed Houston public adjuster will call you back.', true) ?>
    </div>
    <div class="side-card">
      <h3>Free claim tools</h3>
      <ul class="link-list">
        <li><a href="/tools/claim-settlement-calculator/">Claim settlement calculator</a></li>
        <li><a href="/tools/public-adjuster-fee-calculator/">Public adjuster fee calculator</a></li>
        <li><a href="/tools/hurricane-deductible-calculator/">Hurricane deductible calculator</a></li>
        <li><a href="/tools/claim-deadline-calculator/">Texas claim deadline calculator</a></li>
        <li><a href="/houston-weather/">Live Houston weather &amp; alerts</a></li>
      </ul>
    </div>
  </aside>
</div>
<section class="section alt"><div class="wrap">
  <h2 class="section-title">More claim guides from Houston Public Adjusters</h2>
  <?= post_cards(array_slice(array_values(array_filter(array_keys(POSTS), fn($s) => $s !== $slug)), 0, 3)) ?>
</div></section>
<?php
    page_end();
}
