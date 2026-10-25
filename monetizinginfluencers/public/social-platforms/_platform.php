<?php
/**
 * Helpers shared by the /social-platforms/ pages. Included after inc/layout.php.
 * Outputs nothing on its own.
 */
if (!defined('SITE_NAME')) {
    http_response_code(404);
    exit;
}

const PLATFORMS = [
    'youtube'   => 'YouTube',
    'tiktok'    => 'TikTok',
    'instagram' => 'Instagram',
    'facebook'  => 'Facebook',
    'pinterest' => 'Pinterest',
];

/** Platform icon badge + meta line for page_hero()'s $extraHtml. */
function plat_hero_extra(string $slug, string $label, string $readMins): string
{
    return '<div class="plat-hero-badge reveal p-' . $slug . '"><span class="p-ico">' . icon($slug) . '</span>'
        . '<span class="lbl">' . e($label) . '</span></div>'
        . '<div class="hero-meta reveal"><span>' . icon('clock') . ' ' . e($readMins) . ' min read</span>'
        . '<span>' . icon('pen') . ' By the ' . e(SITE_NAME) . ' team</span>'
        . '<span>' . icon('check') . ' Updated October 2026</span></div>';
}

/** Sticky table of contents + sidebar CTA. $items = [id => label] */
function plat_toc(array $items, string $ctaTitle, string $ctaText, string $ctaHref, string $ctaBtn): void
{
    echo '<aside><nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>';
    foreach ($items as $id => $label) {
        echo '<li><a href="#' . e($id) . '">' . e($label) . '</a></li>';
    }
    echo '</ol></nav><div class="side-cta"><h3>' . e($ctaTitle) . '</h3><p>' . e($ctaText) . '</p>'
        . '<a class="btn btn-light btn-sm" href="' . e($ctaHref) . '">' . e($ctaBtn) . ' ' . icon('arrow') . '</a></div></aside>';
}

/** Row of links to every platform playbook. */
function platform_nav(string $current = ''): void
{
    echo '<section class="section"><div class="wrap"><div class="section-head"><span class="kicker reveal">More platform playbooks</span>'
        . '<h2 class="reveal">Monetize every channel you post on</h2></div><div class="platform-nav">';
    foreach (PLATFORMS as $slug => $name) {
        $cur = $slug === $current ? ' current' : '';
        echo '<article class="card tilt reveal p-' . $slug . $cur . '"><a href="/social-platforms/' . $slug . '/">'
            . '<span class="p-ico">' . icon($slug) . '</span><h3>' . e($name) . '</h3></a></article>';
    }
    echo '</div></div></section>';
}

/** Article JSON-LD node for page_start()'s 'schema'. */
function plat_article_schema(string $path, string $headline, string $desc): array
{
    return [
        '@type' => 'Article',
        '@id' => SITE_URL . $path . '#article',
        'headline' => $headline,
        'description' => $desc,
        'datePublished' => '2023-07-06',
        'dateModified' => '2026-10-25',
        'author' => ['@type' => 'Organization', 'name' => SITE_NAME, 'url' => SITE_URL . '/'],
        'publisher' => ['@id' => SITE_URL . '/#org'],
        'mainEntityOfPage' => SITE_URL . $path,
        'image' => SITE_URL . '/assets/img/og-default.png',
    ];
}
