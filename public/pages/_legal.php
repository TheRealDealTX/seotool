<?php
defined('SCC') || exit;
function legal_page(string $path, string $title, string $h1, string $desc, string $html): void
{
    page_head(['title' => $title, 'description' => $desc, 'path' => $path,
        'schema' => [breadcrumb_schema([['Home', '/'], [$h1, $path]])]]);
    echo '<section class="page-hero"><div class="wrap">' . breadcrumbs_html([['Home', '/'], [$h1, $path]]) . '<h1>' . e($h1) . '</h1><p class="lede">Last updated ' . fmt_date(BUILD_DATE) . '</p></div></section>';
    echo '<div class="legal prose wrap">' . $html . '</div>';
    page_foot();
}
