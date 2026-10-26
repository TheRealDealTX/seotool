<?php
// Blog posts live in content/posts/<slug>.php, each returning an array (see README).

function all_posts(): array
{
    static $posts = null;
    if ($posts !== null) {
        return $posts;
    }
    $posts = [];
    foreach (glob(__DIR__ . '/../content/posts/*.php') as $file) {
        $p = require $file;
        $p['slug'] = basename($file, '.php');
        $p['path'] = '/' . $p['slug'] . '/';
        $p['words'] = str_word_count(strip_tags($p['body']));
        $p['minutes'] = max(1, (int)round($p['words'] / 230));
        $posts[$p['slug']] = $p;
    }
    uasort($posts, fn($a, $b) => strcmp($b['published'], $a['published']));
    return $posts;
}

function get_post(string $slug): ?array
{
    return all_posts()[$slug] ?? null;
}

function nice_date(string $ymd): string
{
    return date('F j, Y', strtotime($ymd));
}

/** [['id' => …, 'text' => …], …] from the post's <h2 id="…"> headings. */
function post_toc(string $body): array
{
    preg_match_all('#<h2 id="([^"]+)">(.*?)</h2>#s', $body, $m, PREG_SET_ORDER);
    return array_map(fn($x) => ['id' => $x[1], 'text' => html_entity_decode(strip_tags($x[2]), ENT_QUOTES, 'UTF-8')], $m);
}

function post_cta(): string
{
    return '<aside class="post-cta"><div class="post-cta__icon">' . icon('briefcase') . '</div><div>'
        . '<p class="post-cta__title">Looking for steady work in Texas?</p>'
        . '<p>Best Jobs Pro matches job seekers with office, warehouse, skilled-trade, driving and customer-service roles across Texas. Applying takes five minutes and there are no fees.</p>'
        . '<p class="post-cta__btns"><a class="btn btn--sm" href="/applications/">Apply now</a> <a class="btn btn--sm btn--outline" href="/job-postings/">See job postings</a></p>'
        . '</div></aside>';
}

function render_post_body(array $post): string
{
    $body = $post['body'];
    $tool = !empty($post['tool']) ? tool_widget($post['tool'], true) : '';
    // Callbacks, not replacement strings: widget HTML contains "$0", which preg_replace would expand.
    $body = preg_replace_callback('#<p>\s*\{\{tool\}\}\s*</p>|\{\{tool\}\}#', fn() => $tool, $body, 1);
    $body = preg_replace_callback('#<p>\s*\{\{cta\}\}\s*</p>|\{\{cta\}\}#', fn() => post_cta(), $body, 1);
    return $body;
}

function post_card(array $p, bool $lazy = true): string
{
    return '<article class="post-card reveal">'
        . '<a class="post-card__img" href="' . e($p['path']) . '" tabindex="-1" aria-hidden="true"><img src="' . e($p['image']) . '" alt="" width="' . (int)$p['image_w'] . '" height="' . (int)$p['image_h'] . '"' . ($lazy ? ' loading="lazy"' : '') . '></a>'
        . '<div class="post-card__body"><p class="post-card__meta"><time datetime="' . e($p['published']) . '">' . e(nice_date($p['published'])) . '</time> &middot; ' . $p['minutes'] . ' min read</p>'
        . '<h3><a href="' . e($p['path']) . '">' . e($p['title']) . '</a></h3>'
        . '<p>' . e($p['excerpt']) . '</p>'
        . '<a class="more" href="' . e($p['path']) . '">Read article ' . icon('arrow') . '</a></div></article>';
}
