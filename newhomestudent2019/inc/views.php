<?php defined('NHS') || exit;

/* ---------------- Blog post ---------------- */

function view_post(array $p): never {
    $cat = CATEGORIES[$p['category']] ?? ['name' => 'Blog'];
    $crumbs = [['Home', '/'], ['Blog', '/blog/'], [$cat['name'], '/category/' . $p['category'] . '/'], [$p['title'], $p['url']]];
    [$body, $toc] = add_toc(render_body($p['body']));
    $mins = reading_minutes($p['body']);

    $meta = '<p class="post-meta">By <a href="/author/jonathon/">' . e(SITE['author']) . '</a> · Updated <time datetime="' . e($p['updated']) . '">' . e(human_date($p['updated'])) . '</time> · ' . $mins . ' min read</p>';
    $h = page_hero($p['title'], '', $crumbs, $meta);
    $h .= '<div class="wrap post-layout"><article class="prose">';
    if ($p['image']) {
        $h .= '<figure class="post-figure"><img src="' . e($p['image']) . '" alt="' . e($p['image_alt']) . '" width="1200" height="675" fetchpriority="high"></figure>';
    }
    if (has_affiliate_links($p['body'])) {
        $h .= '<p class="disclosure">This guide contains affiliate links. As an Amazon Associate we earn from qualifying purchases, at no extra cost to you. <a href="/affiliate-disclosure/">Learn more</a>.</p>';
    }
    if (count($toc) >= 3) {
        $h .= '<details class="toc" open><summary>In this guide</summary><ol>';
        foreach ($toc as [$id, $t]) $h .= '<li><a href="#' . e($id) . '">' . e($t) . '</a></li>';
        $h .= '</ol></details>';
    }
    $h .= $body;
    if ($p['faq']) {
        $h .= '<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2>';
        foreach ($p['faq'] as [$q, $a]) $h .= '<details><summary>' . e($q) . '</summary><p>' . e($a) . '</p></details>';
        $h .= '</section>';
    }
    $h .= '<div class="author-box"><span class="author-avatar" aria-hidden="true">J</span><div><p class="author-name">Written by <a href="/author/jonathon/">' . e(SITE['author']) . '</a></p><p>Founder of New Home Investing Knowledge. Jonathon has spent more than a decade helping Texans plan, build and invest in new homes — including people acting as their own general contractor.</p></div></div>';
    $h .= '</article><aside class="sidebar">' . sidebar_widgets($p) . '</aside></div>';

    $rel = related_posts($p);
    if ($rel) {
        $h .= '<section class="section section-alt"><div class="wrap"><h2 class="section-title">Keep reading</h2><div class="card-grid">';
        foreach ($rel as $r) $h .= post_card($r);
        $h .= '</div></div></section>';
    }
    $h .= cta_band();

    $article = [
        '@type' => 'BlogPosting',
        '@id' => url($p['url'] . '#article'),
        'headline' => $p['title'],
        'description' => $p['description'],
        'datePublished' => $p['date'],
        'dateModified' => $p['updated'],
        'mainEntityOfPage' => url($p['url']),
        'author' => ['@id' => url('/author/jonathon/#person')],
        'publisher' => ['@id' => url('/#organization')],
        'articleSection' => $cat['name'],
        'keywords' => $p['keyword'] ?? '',
        'wordCount' => str_word_count(strip_tags($p['body'])),
    ];
    if ($p['image']) $article['image'] = url($p['image']);

    render_page([
        'title' => $p['seo_title'],
        'og_title' => $p['title'],
        'description' => $p['description'],
        'path' => $p['url'],
        'type' => 'article',
        'image' => $p['image'] ?? '/assets/img/og-default.jpg',
        'published' => $p['date'],
        'modified' => $p['updated'],
        'body' => $h,
        'schema' => [$article, person_schema(), breadcrumb_schema($crumbs), faq_schema($p['faq'])],
    ]);
}

function sidebar_widgets(?array $p = null): string {
    $h = '<div class="widget widget-cta"><p class="widget-title">Free owner-builder course</p><p>Six short lessons on designing and building your own home for less.</p><a class="btn" href="/free-training/">Get instant access</a></div>';
    $h .= '<div class="widget"><p class="widget-title">Start here</p><ul class="link-list">'
        . '<li><a href="/how-to-be-your-own-general-contractor/">How to be your own general contractor</a></li>'
        . '<li><a href="/how-much-does-it-cost-to-build-a-house-in-texas/">What it costs to build in Texas</a></li>'
        . '<li><a href="/new-home-construction-timeline/">The construction timeline, phase by phase</a></li>'
        . '<li><a href="/new-construction-inspection-checklist/">New construction inspection checklist</a></li>'
        . '<li><a href="/best-books-on-building-your-own-home/">Best books on building your own home</a></li>'
        . '</ul></div>';
    $h .= '<div class="widget"><p class="widget-title">Topics</p><ul class="link-list">';
    foreach (CATEGORIES as $slug => $c) $h .= '<li><a href="/category/' . e($slug) . '/">' . e($c['name']) . '</a> <span class="count">' . count(posts_in($slug)) . '</span></li>';
    $h .= '</ul></div>';
    $h .= '<div class="widget"><p class="widget-title">Owner-builder toolkit</p>' . product_grid(['laser_measure', 'moisture_meter', 'books_heldmann']) . '<a class="text-link" href="/our-products/">See every recommendation &rarr;</a></div>';
    return $h;
}

/* ---------------- Blog index & archives ---------------- */

function view_archive(string $path, string $h1, string $lead, string $title, string $desc, array $posts, int $page, array $crumbs, string $extra = ''): never {
    $per = SITE['per_page'];
    $pages = max(1, (int) ceil(count($posts) / $per));
    if ($page < 1 || $page > $pages) view_404();
    $slice = array_slice($posts, ($page - 1) * $per, $per);
    $h = page_hero($h1, $lead, $crumbs, $extra);
    $h .= '<section class="section"><div class="wrap"><div class="card-grid">';
    foreach ($slice as $p) $h .= post_card($p);
    $h .= '</div>' . pagination($page, $pages, $path) . '</div></section>' . cta_band();
    $canon = $page > 1 ? $path . 'page/' . $page . '/' : $path;
    $list = ['@type' => 'CollectionPage', 'name' => $h1, 'url' => url($canon), 'description' => $desc,
        'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => array_map(fn($p, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => url($p['url'])], $slice, array_keys($slice))]];
    render_page([
        'title' => $page > 1 ? "$title — Page $page" : $title,
        'description' => $desc,
        'path' => $canon,
        'body' => $h,
        'schema' => [$list, breadcrumb_schema($crumbs)],
    ]);
}

function view_blog(int $page): never {
    $chips = '<div class="chips">';
    foreach (CATEGORIES as $slug => $c) $chips .= '<a class="chip" href="/category/' . e($slug) . '/">' . e($c['name']) . '</a>';
    $chips .= '</div>';
    view_archive('/blog/', 'The New Home Builder\'s Blog',
        'Practical, plain-English guides on building, buying and investing in a home in Texas — plus the tools and books we recommend.',
        'New Home Building Blog: Tips, Guides & Checklists | NHIK',
        'Guides for owner-builders and future homeowners: budgeting, building codes, construction timelines, inspections, buying, moving and real estate investing.',
        all_posts(), $page, [['Home', '/'], ['Blog', '/blog/']], $chips);
}

function view_category(string $slug, int $page): never {
    $c = CATEGORIES[$slug];
    view_archive('/category/' . $slug . '/', $c['name'], e($c['intro']), $c['title'], $c['description'],
        posts_in($slug), $page, [['Home', '/'], ['Blog', '/blog/'], [$c['name'], '/category/' . $slug . '/']]);
}

function view_author(int $page): never {
    $lead = 'Jonathon founded New Home Investing Knowledge to share what he learned over more than a decade of helping people design, build and invest in new homes across Texas. He writes for owner-builders, families hiring a builder, and new real estate investors.';
    view_archive('/author/jonathon/', 'Articles by Jonathon', e($lead),
        'Jonathon — Founder & Author | New Home Investing Knowledge',
        'Guides on building a new home, owner-building, Texas building codes, buying and real estate investing by Jonathon, founder of New Home Investing Knowledge.',
        all_posts(), $page, [['Home', '/'], ['Authors', '/about-us/'], ['Jonathon', '/author/jonathon/']]);
}

/* ---------------- Generic content pages ---------------- */

function get_page(string $slug): ?array {
    if (!preg_match('/^[a-z0-9-]+$/', $slug)) return null;
    $f = APP_ROOT . '/content/pages/' . $slug . '.php';
    return is_file($f) ? require $f : null;
}

function view_page(string $slug, array $pg): never {
    $crumbs = [['Home', '/'], [$pg['crumb'] ?? $pg['title'], '/' . $slug . '/']];
    $h = page_hero($pg['title'], $pg['lead'] ?? '', $crumbs);
    $body = render_body($pg['body']);
    if (!empty($pg['image'])) {
        $body = '<figure class="post-figure"><img src="' . e($pg['image']) . '" alt="' . e($pg['image_alt'] ?? '') . '" width="1024" height="576" fetchpriority="high"></figure>' . $body;
    }
    if (!empty($pg['wide'])) {
        $h .= $body;
    } else {
        $h .= '<div class="wrap post-layout"><div class="prose">' . $body . '</div><aside class="sidebar">' . sidebar_widgets() . '</aside></div>';
    }
    if (empty($pg['no_cta'])) $h .= cta_band();
    render_page([
        'title' => $pg['seo_title'],
        'description' => $pg['description'],
        'path' => '/' . $slug . '/',
        'image' => $pg['image'] ?? '/assets/img/og-default.jpg',
        'body' => $h,
        'noindex' => $pg['noindex'] ?? false,
        'schema' => array_merge([breadcrumb_schema($crumbs)], $pg['schema'] ?? []),
    ]);
}

/* ---------------- 404 ---------------- */

function view_404(): never {
    $h = page_hero('Page not found', 'That page may have moved when we rebuilt the site. Try one of these instead:');
    $h .= '<section class="section"><div class="wrap"><div class="card-grid">';
    foreach (array_slice(all_posts(), 0, 6) as $p) $h .= post_card($p);
    $h .= '</div><p class="center"><a class="btn" href="/blog/">Browse all guides</a></p></div></section>';
    render_page(['title' => 'Page Not Found | ' . SITE['name'], 'description' => 'The page you were looking for could not be found.', 'path' => '/404', 'body' => $h, 'noindex' => true, 'status' => 404]);
}

/* ---------------- Feeds ---------------- */

function view_sitemap(): never {
    header('Content-Type: application/xml; charset=utf-8');
    $urls = [['/', date('Y-m-d')], ['/blog/', all_posts()[0]['updated'] ?? date('Y-m-d')]];
    foreach (['free-training', 'build-a-home-yourself', 'our-products', 'resources', 'about-us', 'contact', 'write-for-us', 'affiliate-disclosure', 'privacy-policy', 'terms-of-use'] as $s) {
        $f = APP_ROOT . '/content/pages/' . $s . '.php';
        $urls[] = ['/' . $s . '/', is_file($f) ? date('Y-m-d', filemtime($f)) : date('Y-m-d')];
    }
    foreach (array_keys(CATEGORIES) as $c) $urls[] = ['/category/' . $c . '/', posts_in($c)[0]['updated'] ?? date('Y-m-d')];
    $urls[] = ['/author/jonathon/', date('Y-m-d')];
    foreach (all_posts() as $p) $urls[] = [$p['url'], $p['updated'], $p['image']];
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
    foreach ($urls as $u) {
        echo '<url><loc>' . e(url($u[0])) . '</loc><lastmod>' . e($u[1]) . '</lastmod>';
        if (!empty($u[2])) echo '<image:image><image:loc>' . e(url($u[2])) . '</image:loc></image:image>';
        echo "</url>\n";
    }
    echo '</urlset>';
    exit;
}

function view_feed(): never {
    header('Content-Type: application/rss+xml; charset=utf-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>';
    echo '<title>' . e(SITE['name']) . '</title><link>' . e(url('/')) . '</link><description>' . e(SITE['tagline']) . '</description><language>en-us</language>';
    echo '<atom:link href="' . e(url('/feed/')) . '" rel="self" type="application/rss+xml"/>';
    foreach (array_slice(all_posts(), 0, 20) as $p) {
        echo '<item><title>' . e($p['title']) . '</title><link>' . e(url($p['url'])) . '</link><guid>' . e(url($p['url'])) . '</guid>'
            . '<pubDate>' . date(DATE_RSS, strtotime($p['date'])) . '</pubDate><description>' . e($p['excerpt']) . '</description></item>';
    }
    echo '</channel></rss>';
    exit;
}
