<?php
/**
 * Blog post wrapper. Each post is:
 *
 *   require __DIR__ . '/../inc/blog.php';
 *   blog_post_start(['path' => '/slug/', 'description' => '...', 'read' => 9, ...]);
 *   ...article HTML (h2 ids must match the toc)...
 *   blog_post_end($toc, $faqs, $sideCta);
 *
 * Title, category, date and excerpt come from site_posts() in config.php.
 */
require_once __DIR__ . '/layout.php';

function blog_find_post(string $path): array
{
    foreach (site_posts() as [$url, $title, $cat, $date, $excerpt]) {
        if ($url === $path) {
            return ['url' => $url, 'title' => $title, 'cat' => $cat, 'date' => $date, 'excerpt' => $excerpt];
        }
    }
    throw new RuntimeException('Post not in site_posts(): ' . $path);
}

function blog_post_start(array $o): void
{
    $post = blog_find_post($o['path']);
    $GLOBALS['__post'] = $post + $o;
    $modified = $o['modified'] ?? $post['date'];
    $headline = $o['h1_plain'] ?? $post['title'];

    page_start([
        'title' => $o['title'] ?? $post['title'],
        'description' => $o['description'] ?? $post['excerpt'],
        'path' => $post['url'],
        'type' => 'article',
        'published' => $post['date'],
        'modified' => $modified,
        'extra_css' => ['/assets/css/blog.css'],
        'schema' => [[
            '@type' => 'BlogPosting',
            '@id' => SITE_URL . $post['url'] . '#article',
            'headline' => $headline,
            'description' => $o['description'] ?? $post['excerpt'],
            'datePublished' => $post['date'],
            'dateModified' => $modified,
            'articleSection' => $post['cat'],
            'author' => ['@id' => SITE_URL . '/#org'],
            'publisher' => ['@id' => SITE_URL . '/#org'],
            'mainEntityOfPage' => ['@id' => SITE_URL . $post['url'] . '#webpage'],
            'image' => SITE_URL . '/assets/img/og-default.png',
            'inLanguage' => 'en-US',
        ]],
    ]);

    $dateFmt = date('F j, Y', strtotime($post['date']));
    $meta = '<div class="hero-meta reveal"><span class="chip">' . e($post['cat']) . '</span>'
        . '<span>' . icon('clock') . ' ' . (int) ($o['read'] ?? 8) . ' min read</span>'
        . '<span>' . icon('pen') . ' Published <time datetime="' . e($post['date']) . '">' . e($dateFmt) . '</time></span>';
    if ($modified !== $post['date']) {
        $meta .= '<span>' . icon('sparkles') . ' Updated <time datetime="' . e($modified) . '">' . e(date('F j, Y', strtotime($modified))) . '</time></span>';
    }
    $meta .= '</div>';

    page_hero($post['cat'], $o['h1'] ?? e($post['title']), $o['lead'] ?? e($post['excerpt']), [['Blog', '/blogs/'], [$post['title'], $post['url']]], $meta);
    echo "<section class=\"section article-section\">\n  <div class=\"wrap content-grid\">\n    <article class=\"prose\">\n";
}

/**
 * @param array $toc     [[id, label], ...]
 * @param array $faqs    [[question, answerHtml], ...]
 * @param array $sideCta [title, text, href, buttonLabel]
 */
function blog_post_end(array $toc, array $faqs, array $sideCta): void
{
    $post = $GLOBALS['__post'];
    echo "    </article>\n    <aside class=\"post-aside\">\n      <nav class=\"toc\" aria-label=\"In this guide\">\n        <h2>In this guide</h2>\n        <ol>\n";
    foreach ($toc as [$id, $label]) {
        echo '          <li><a href="#' . e($id) . '">' . e($label) . "</a></li>\n";
    }
    echo "        </ol>\n      </nav>\n";
    [$t, $txt, $href, $btn] = $sideCta;
    echo '      <div class="side-cta"><h3>' . e($t) . '</h3><p>' . e($txt) . '</p><a class="btn btn-light btn-sm" href="' . e($href) . '">' . e($btn) . ' ' . icon('arrow') . "</a></div>\n";
    echo "    </aside>\n  </div>\n</section>\n";

    faq_block($faqs);
    ?>
<section class="section related">
  <div class="wrap">
    <div class="section-head"><span class="kicker reveal">Keep reading</span><h2 class="reveal">Related guides</h2></div>
    <?php post_cards(3, $post['url']); ?>
  </div>
</section>
<?php
    cta_band();
    page_end();
}

/** Copyable template block. $text is plain text (escaped here); newlines are kept. */
function template_box(string $id, string $label, string $text): string
{
    return '<div class="template-box" id="' . e($id) . '">'
        . '<span class="tpl-label">' . e($label) . '</span>'
        . '<button type="button" class="btn btn-sm btn-ghost copy-btn" data-copy="#' . e($id) . '-text">' . icon('copy') . ' Copy</button>'
        . '<div class="tpl-text" id="' . e($id) . '-text">' . e(trim($text)) . '</div></div>';
}
