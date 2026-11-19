<?php
declare(strict_types=1);
defined('M1S') || exit;

function home_page(): void
{
    [$articles] = article_list(null, 1, 7);
    [$hot] = thread_list(null, 'hot', 1, 8);
    $secrets = all(THREAD_SELECT . " WHERE t.removed = 0 AND t.status = 'live' AND t.pinned = 0 AND c.slug = 'one-secret' ORDER BY t.score DESC, t.created_at DESC LIMIT 5");
    $stats = [
        'members' => (int)val('SELECT COUNT(*) FROM users WHERE banned = 0'),
        'threads' => (int)val('SELECT COUNT(*) FROM threads WHERE removed = 0 AND status = \'live\''),
        'articles' => (int)val("SELECT COUNT(*) FROM articles WHERE status = 'published'"),
    ];
    $votes = my_votes('thread', array_merge(array_column($hot, 'id'), array_column($secrets, 'id')));

    $itemList = ['@type' => 'ItemList', 'name' => 'Latest guides', 'itemListElement' => array_map(fn($a, $i) => [
        '@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url(article_url($a)), 'name' => $a['title'],
    ], $articles, array_keys($articles))];

    render('home', compact('articles', 'hot', 'secrets', 'stats', 'votes'), [
        'title' => null,
        'description' => M1S_DEFAULT_DESC,
        'canonical' => abs_url('/'),
        'jsonld' => [org_schema(), website_schema(), $itemList],
        'body_class' => 'page-home',
    ]);
}

function blog_index(): void
{
    $page = page_num();
    [$articles, $hasNext] = article_list(null, $page, 12);
    if (!$articles && $page > 1) {
        not_found();
    }
    render('blog_list', [
        'heading' => 'The My 1 Secret Blog',
        'intro' => 'In-depth guides on apartment living, small-space design, renters and homeowners insurance claims, Texas living and everyday life. Every article is open for discussion.',
        'articles' => $articles, 'page' => $page, 'hasNext' => $hasNext, 'base' => '/blog/', 'activeTopic' => null,
    ], [
        'title' => $page > 1 ? "Blog: Apartment Living, Renting & Home Guides (Page $page)" : 'Blog: Apartment Living, Renting & Home Guides',
        'description' => 'Guides for renters, homeowners and Texans: apartment living tips, small-space design, insurance claim help, Texas cities and lifestyle advice.',
        'jsonld' => [breadcrumb_schema([['Blog', '/blog/']]), ['@type' => 'CollectionPage', 'name' => 'My 1 Secret Blog', 'url' => abs_url('/blog/')]],
        'breadcrumbs' => [['Blog', null]],
    ]);
}

function blog_topic(string $slug): void
{
    $topic = one('SELECT * FROM topics WHERE slug = ?', [$slug]) ?? not_found();
    $page = page_num();
    [$articles, $hasNext] = article_list((int)$topic['id'], $page, 12);
    if (!$articles && $page > 1) {
        not_found();
    }
    $community = find_community(topic_community_slug($slug));
    render('blog_list', [
        'heading' => $topic['seo_title'] ?: $topic['name'],
        'intro' => $topic['description'],
        'articles' => $articles, 'page' => $page, 'hasNext' => $hasNext, 'base' => topic_url($topic),
        'activeTopic' => $topic['slug'], 'community' => $community,
    ], [
        'title' => ($topic['seo_title'] ?: $topic['name']) . ($page > 1 ? " (Page $page)" : ''),
        'description' => $topic['description'],
        'jsonld' => [
            breadcrumb_schema([['Blog', '/blog/'], [$topic['name'], topic_url($topic)]]),
            ['@type' => 'CollectionPage', 'name' => $topic['seo_title'] ?: $topic['name'], 'url' => abs_url(topic_url($topic)), 'description' => $topic['description']],
        ],
        'breadcrumbs' => [['Blog', '/blog/'], [$topic['name'], null]],
    ]);
}

/** Which forum community discusses a blog topic. */
function topic_community_slug(string $topicSlug): string
{
    return ['renting' => 'renting', 'home-design' => 'small-space-living', 'insurance-claims' => 'insurance-claims',
        'texas-living' => 'texas', 'lifestyle' => 'lifestyle'][$topicSlug] ?? 'one-secret';
}

function article_page(string $slug): void
{
    $a = one(ARTICLE_SELECT . ' WHERE a.slug = ?', [$slug]);
    if (!$a) {
        $renamed = val('SELECT slug FROM articles WHERE legacy_slug = ?', [$slug]);
        $renamed ? redirect('/blog/' . $renamed . '/', 301) : not_found();
    }
    if ($a['status'] !== 'published' && !is_admin()) {
        not_found();
    }
    $url = article_url($a);
    $sort = in_array($_GET['sort'] ?? '', ['new', 'old'], true) ? $_GET['sort'] : 'best';
    $tree = comment_tree('article', (int)$a['id'], $url, $sort);
    $commentVotes = my_votes('comment', flatten_ids($tree));
    $myVote = my_votes('article', [(int)$a['id']])[(int)$a['id']] ?? 0;
    $related = all(ARTICLE_SELECT . " WHERE a.status = 'published' AND a.id <> ? AND a.topic_id = ? ORDER BY a.published_at DESC LIMIT 3",
        [(int)$a['id'], (int)$a['topic_id']]);
    if (count($related) < 3) {
        $more = all(ARTICLE_SELECT . " WHERE a.status = 'published' AND a.id <> ? AND (a.topic_id IS NULL OR a.topic_id <> ?) ORDER BY a.published_at DESC LIMIT " . (3 - count($related)),
            [(int)$a['id'], (int)$a['topic_id']]);
        $related = array_merge($related, $more);
    }
    $community = find_community(topic_community_slug((string)$a['topic_slug']));
    $communityThreads = $community ? thread_list((int)$community['id'], 'hot', 1, 4, 'all', false)[0] : [];

    [$bodyHtml, $toc] = article_toc($a['body_html']);

    $budget = 20;
    $posting = [
        '@type' => 'BlogPosting',
        '@id' => abs_url($url) . '#article',
        'headline' => $a['title'],
        'description' => $a['meta_description'] ?: $a['excerpt'],
        'url' => abs_url($url),
        'mainEntityOfPage' => abs_url($url),
        'datePublished' => iso_date($a['published_at']),
        'dateModified' => iso_date($a['updated_at']),
        'author' => ['@type' => 'Person', 'name' => $a['author_name'] ?: 'My 1 Secret', 'url' => abs_url('/author/' . ($a['author_username'] ?: 'meagan') . '/')],
        'publisher' => ['@id' => abs_url('/#organization')],
        'isPartOf' => ['@id' => abs_url('/#website')],
        'articleSection' => $a['topic_name'],
        'wordCount' => str_word_count(strip_tags($a['body_html'])),
        'commentCount' => (int)$a['comment_count'],
        'interactionStatistic' => interaction_stats((int)$a['upvotes'], (int)$a['comment_count']),
    ];
    if ($a['image']) {
        $posting['image'] = ['@type' => 'ImageObject', 'url' => abs_url($a['image']), 'width' => (int)$a['image_w'], 'height' => (int)$a['image_h']];
    }
    if ($tree) {
        $posting['comment'] = comments_schema($tree, $budget);
    }

    render('article', compact('a', 'tree', 'commentVotes', 'myVote', 'related', 'community', 'communityThreads', 'bodyHtml', 'toc', 'sort'), [
        'title' => $a['seo_title'] ?: $a['title'],
        'description' => $a['meta_description'] ?: excerpt($a['excerpt'] ?? '', 155),
        'canonical' => abs_url($url),
        'robots' => $a['status'] === 'published' ? null : 'noindex',
        'image' => $a['image'] ? abs_url($a['image']) : null,
        'type' => 'article',
        'published' => iso_date($a['published_at']),
        'modified' => iso_date($a['updated_at']),
        'jsonld' => [$posting, breadcrumb_schema([['Blog', '/blog/'], [$a['topic_name'] ?: 'Articles', $a['topic_slug'] ? topic_url($a['topic_slug']) : '/blog/'], [$a['title'], null]])],
        'breadcrumbs' => [['Blog', '/blog/'], [$a['topic_name'] ?: 'Articles', $a['topic_slug'] ? topic_url($a['topic_slug']) : '/blog/']],
    ]);
}

/** Add ids to h2s and build a table of contents. */
function article_toc(string $html): array
{
    $toc = [];
    $used = [];
    $html = preg_replace_callback('#<h2>(.*?)</h2>#s', function ($m) use (&$toc, &$used) {
        $text = trim(html_entity_decode(strip_tags($m[1]), ENT_QUOTES));
        $id = slugify(preg_replace('/^\d+\.\s*/', '', $text), 50);
        while (isset($used[$id])) {
            $id .= '-2';
        }
        $used[$id] = true;
        $toc[] = [$id, $text];
        return '<h2 id="' . e($id) . '">' . $m[1] . '</h2>';
    }, $html);
    return [$html, count($toc) >= 3 ? $toc : []];
}

function author_page(string $username): void
{
    $u = one('SELECT * FROM users WHERE username = ?', [$username]) ?? not_found();
    $page = page_num();
    [$articles, $hasNext] = article_list(null, $page, 12, (int)$u['id']);
    if (!$articles) {
        redirect(user_url($u), 302);
    }
    $name = $u['display_name'] ?: $u['username'];
    render('blog_list', [
        'heading' => "Articles by $name",
        'intro' => $u['bio'] ?: '',
        'articles' => $articles, 'page' => $page, 'hasNext' => $hasNext, 'base' => '/author/' . $u['username'] . '/', 'activeTopic' => null,
    ], [
        'title' => "$name, Author at My 1 Secret" . ($page > 1 ? " (Page $page)" : ''),
        'description' => "Guides by $name on My 1 Secret: apartment living, renting in Texas, small-space design and insurance claims.",
        'jsonld' => [
            ['@type' => 'ProfilePage', 'url' => abs_url('/author/' . $u['username'] . '/'),
             'mainEntity' => ['@type' => 'Person', 'name' => $name, 'description' => $u['bio'], 'url' => abs_url('/author/' . $u['username'] . '/')]],
            breadcrumb_schema([['Blog', '/blog/'], [$name, null]]),
        ],
        'breadcrumbs' => [['Blog', '/blog/'], [$name, null]],
    ]);
}
