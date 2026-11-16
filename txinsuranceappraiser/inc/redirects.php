<?php
declare(strict_types=1);

/**
 * Old WordPress-only URLs → their new home. Every page URL of the WordPress site is served at the
 * same address by the new router, so this list only covers WP machinery, feeds, sitemaps, typo URLs
 * that Google picked up, and media files.
 */
function legacy_redirect(string $path): ?string
{
    static $exact = [
        '/category/blog/'                              => '/blog/',
        '/category/blog'                               => '/blog/',
        '/feed/'                                       => '/blog/',
        '/comments/feed/'                              => '/blog/',
        '/sitemap_index.xml'                           => '/sitemap.xml',
        '/post-sitemap.xml'                            => '/sitemap.xml',
        '/page-sitemap.xml'                            => '/sitemap.xml',
        '/category-sitemap.xml'                        => '/sitemap.xml',
        '/wp-sitemap.xml'                              => '/sitemap.xml',
        // URLs seen in Search Console that never existed or were renamed
        '/can-you-su-after-insurance-appraisal/'       => '/can-you-sue-after-insurance-appraisal/',
        '/how-long-does-an-insurance-appraiser-take/'  => '/how-long-does-an-insurance-appraisal-take/',
        '/insurance-loss-reported/'                    => '/insurance-loss-reported-meaning/',
        '/what-does-insurance-loss-reported/'          => '/what-does-insurance-loss-reported-mean/',
        '/invoking-the-appraisal-clause/'              => '/what-happens-after-invoking-the-appraisal-clause-in-texas/',
        '/invoking-the-appraisal-clause'               => '/what-happens-after-invoking-the-appraisal-clause-in-texas/',
        '/terms-of-use/'                               => '/terms-conditions/',
        '/terms-and-conditions/'                       => '/terms-conditions/',
        '/contact/'                                    => '/contact-us/',
        '/about/'                                      => '/about-us/',
        '/home/'                                       => '/',
        '/index.php'                                   => '/',
    ];
    if (isset($exact[$path])) {
        return $exact[$path];
    }
    if (preg_match('#^/(feed|.+/feed)/?$#', $path)) {
        return '/blog/';
    }
    if (preg_match('#^/(category|tag|author)/#', $path)) {
        return '/blog/';
    }
    if (preg_match('#^/blog/page/\d+/?$#', $path)) {
        return '/blog/';
    }
    if (preg_match('#^/(wp-admin|wp-login\.php|wp-json|wp-includes|xmlrpc\.php)(/|$)#', $path)) {
        return '/';
    }
    // Old media: /wp-content/uploads/YYYY/MM/Name-800x420.webp → /assets/img/...
    if (preg_match('#^/wp-content/uploads/.*/([^/]+?)(?:-\d+x\d+)?\.(webp|png|jpe?g|gif)$#i', $path, $m)) {
        return media_redirect($m[1], strtolower($m[2]));
    }
    return null;
}

function media_redirect(string $base, string $ext): ?string
{
    $base = preg_replace('/-[a-z0-9]{40,}$/', '', $base); // WP "scaled/hash" suffixes
    foreach (['site', 'blog'] as $dir) {
        if (is_file(ROOT . "/assets/img/$dir/$base.webp")) {
            return "/assets/img/$dir/$base.webp";
        }
    }
    if (preg_match('/^(.+)-Insurance-Appraiser$/i', $base, $m)) {
        $slug = strtolower($m[1]);
        if (is_file(ROOT . "/assets/img/cities/$slug.webp")) {
            return "/assets/img/cities/$slug.webp";
        }
    }
    if (stripos($base, 'TX-Insurance-Appraiser-Icon') !== false) {
        return SITE['icon'];
    }
    return null; // falls through to a 404
}
