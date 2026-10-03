<?php
/**
 * Page rendering: picks a template for a content item and wraps it in the layout.
 */

declare(strict_types=1);

/** Render head + header, call $body, then footer. */
function render_layout(array $page, callable $body): void
{
    if (!headers_sent()) {
        header('Content-Type: text/html; charset=utf-8');
    }
    include MPA_ROOT . '/templates/head.php';
    include MPA_ROOT . '/templates/header.php';
    $body($page);
    include MPA_ROOT . '/templates/footer.php';
}

/** Render a content item with its template. */
function render_page(array $page): void
{
    $template = $page['template'] ?? null;
    if (!$template) {
        $template = ['post' => 'post', 'service' => 'service'][$page['_type']] ?? 'page';
    }
    $page['template'] = $template;
    $file = MPA_ROOT . '/templates/' . $template . '.php';
    if (!is_file($file)) {
        $file = MPA_ROOT . '/templates/page.php';
    }
    // Templates may add scripts/head tags before the layout prints.
    $prepare = MPA_ROOT . '/templates/prepare/' . $template . '.php';
    if (is_file($prepare)) {
        $page = (function (array $page) use ($prepare) {
            include $prepare;
            return $page;
        })($page);
    }
    render_layout($page, function (array $page) use ($file) {
        include $file;
    });
}

/** Body HTML with shortcodes, heading ids, and table wrappers applied. */
function prepared_body(array $page, array &$toc = []): string
{
    $html = $page['body'] ?? '';
    $html = render_shortcodes($html, $page);
    $html = add_heading_ids($html, $toc);
    return wrap_tables($html);
}

function render_404(): void
{
    http_response_code(404);
    $page = [
        'path' => '/404/', 'title' => 'Page Not Found', 'description' => 'The page you were looking for could not be found.',
        'noindex' => true, '_type' => 'page', 'template' => '404', 'hide_hero_cta' => true, 'hero_compact' => true,
    ];
    render_layout($page, function (array $page) {
        include MPA_ROOT . '/templates/404.php';
    });
}
