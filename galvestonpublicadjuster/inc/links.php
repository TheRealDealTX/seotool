<?php
// Internal linking. One topic map drives everything: the "Related" sidebars, the "Keep reading"
// sections under every hub page, the "Read next" block under every blog post, the visible
// breadcrumbs, and the auto-linker that turns recurring phrases in blog posts into links. Blog
// posts publish weekly, so nothing here is hard-coded to a post that may not be live yet: a post
// is linked only once blog_post() can find it.

// Hub pages (the static, always-live pages). key => path, nav-style label, card title, blurb, icon.
const HUBS = [
    'twia'            => ['/twia-claims-expert/',      'TWIA claims help',            'TWIA Claims Expert',             'Deadlines, wind-vs-water disputes, appraisal and what to do after a TWIA denial or low offer.', 'wind'],
    'fire'            => ['/galveston-fire-claims/',   'Galveston fire claims',       'Fire & Smoke Claims',            'Structure, smoke, soot, contents and living expenses — the items fire estimates leave out.', 'fire'],
    'calculators'     => ['/calculators/',             'wind & claim calculators',    'Wind & Claim Calculators',       'See what a given wind speed does to shingles, and what your claim nets after deductible and fee.', 'calc'],
    'windstorm-rules' => ['/texas-windstorm-rules/',   'Texas windstorm rules',       'Texas Windstorm Rules',          'TWIA eligibility, WPI-8 certificates, claim deadlines, appraisal and public adjuster rules.', 'scale'],
    'local-code'      => ['/galveston-local-code/',    'Galveston local code',        'Galveston Local Code',           'Design wind speeds, shingle class, underlayment and floodplain rules that belong in your estimate.', 'building'],
    'storm-history'   => ['/galveston-storm-history/', 'Galveston storm history',     'Galveston Storm History',        'From the 1900 Storm to Ike and Beryl — and what each taught the island about insurance.', 'hurricane'],
    'weather-events'  => ['/weather-events/',          'weather events log',          'Weather Events: 70+ mph Winds',  'Updated weekly: every day Galveston winds reached 70 mph, the level where roof damage begins.', 'wind'],
    'blog'            => ['/blog/',                    'claim guides',                'Claim Guides & Blog',            'Weekly, practical guides on TWIA, hurricane, fire, flood and denied claims.', 'file'],
    'about'           => ['/about/',                   'about Joseph Dittman',        'About Your Adjuster',            'Who handles your file, how we document a loss, and what Texas law requires of us.', 'user'],
    'contact'         => ['/contact/',                 'free claim review',           'Free Claim Review',              'Send your policy, photos and any offer or denial letter. We call back the same day.', 'phone'],
];

// Hub pages each blog category leans on, in order. Drives the "Related resources" list on posts,
// the hub links under each category on /blog/, and the hub cards under a post's "Read next".
const CATEGORY_HUBS = [
    'TWIA & Windstorm'   => ['twia', 'windstorm-rules', 'calculators', 'weather-events'],
    'Fire & Smoke'       => ['fire', 'local-code', 'calculators', 'about'],
    'Flood & Water'      => ['local-code', 'twia', 'storm-history', 'windstorm-rules'],
    'Denied & Underpaid' => ['twia', 'calculators', 'windstorm-rules', 'about'],
    'Claim Process'      => ['windstorm-rules', 'calculators', 'twia', 'about'],
];

// Blog categories each hub page pulls guides from (first category first), and the other hubs it
// points to. Used by related_section() and related_list().
const HUB_TOPICS = [
    'twia'            => [['TWIA & Windstorm', 'Denied & Underpaid'], ['windstorm-rules', 'calculators', 'weather-events', 'local-code']],
    'fire'            => [['Fire & Smoke'],                           ['local-code', 'calculators', 'windstorm-rules', 'about']],
    'calculators'     => [['TWIA & Windstorm', 'Denied & Underpaid'], ['local-code', 'twia', 'weather-events', 'windstorm-rules']],
    'windstorm-rules' => [['TWIA & Windstorm', 'Claim Process'],      ['twia', 'local-code', 'calculators', 'weather-events']],
    'local-code'      => [['TWIA & Windstorm', 'Fire & Smoke'],       ['windstorm-rules', 'calculators', 'twia', 'fire']],
    'storm-history'   => [['TWIA & Windstorm', 'Flood & Water'],      ['weather-events', 'twia', 'windstorm-rules', 'local-code']],
    'weather-events'  => [['TWIA & Windstorm'],                       ['calculators', 'twia', 'storm-history', 'windstorm-rules']],
    'about'           => [['Claim Process'],                          ['twia', 'fire', 'calculators', 'blog']],
    'contact'         => [['Claim Process', 'Denied & Underpaid'],    ['calculators', 'windstorm-rules', 'twia', 'blog']],
];

// Blog auto-linker: phrase => target. The first match of each phrase in a post's body becomes a
// link, once per target, never inside an existing link or heading, never to the post itself, never
// to a target the post already links by hand, and never to a post that isn't published yet.
// Longer phrases are listed before the shorter phrases they contain.
const AUTO_LINKS = [
    'sworn proof of loss'       => '/blog/sworn-proof-of-loss-texas/',
    'proof of loss'             => '/blog/sworn-proof-of-loss-texas/',
    'additional living expense' => '/blog/fire-damage-insurance-claim-help-galveston/',
    'flood insurance'           => '/blog/flood-insurance-claims-process-galveston/',
    'NFIP'                      => '/blog/flood-insurance-claims-process-galveston/',
    'water damage'              => '/blog/does-homeowners-insurance-cover-water-damage/',
    'mortgage company'          => '/blog/mortgage-company-insurance-claim-check/',
    'smoke damage'              => '/blog/smoke-damage-claims/',
    'house fire'                => '/blog/how-to-deal-with-insurance-adjuster-after-house-fire/',
    'roof claim'                => '/blog/public-adjuster-for-roof-claim/',
    'denial letter'             => '/blog/how-to-successfully-appeal-an-insurance-denial/',
    'appeal'                    => '/blog/how-to-successfully-appeal-an-insurance-denial/',
    'commercial property'       => '/blog/commercial-public-adjuster-galveston/',
    'insurance adjuster'        => '/blog/public-adjuster-vs-insurance-adjuster/',
    'WPI-8'                     => '/blog/wpi-8-certificate-twia/',
    'hurricane'                 => '/blog/hurricane-damage-claim-galveston/',
    'denied'                    => '/blog/why-would-insurance-deny-a-claim/',
    'appraisal'                 => '/texas-windstorm-rules/#disputes',
    'Prompt Payment'            => '/texas-windstorm-rules/#private',
    'building code'             => '/galveston-local-code/',
    'code upgrade'              => '/galveston-local-code/',
    'deductible'                => '/calculators/#claim-calc',
    'wind speed'                => '/calculators/',
    'TWIA'                      => '/twia-claims-expert/',
];

function hub_path(string $key): string { return HUBS[$key][0]; }

/** Inline link to a hub page: hub_link('twia') or hub_link('twia', 'custom anchor text'). */
function hub_link(string $key, ?string $text = null, string $fragment = ''): string {
    return '<a href="' . hub_path($key) . $fragment . '">' . ($text ?? e(HUBS[$key][1])) . '</a>';
}

/** Inline link to a blog post if it is published; otherwise just the text (or $fallback_path if given). */
function post_link(string $slug, string $text, ?string $fallback_path = null): string {
    if (blog_post($slug)) return '<a href="/blog/' . e($slug) . '/">' . $text . '</a>';
    return $fallback_path ? '<a href="' . e($fallback_path) . '">' . $text . '</a>' : $text;
}

/** URL of a blog post if published, else $fallback. For cards whose target should upgrade as posts go live. */
function post_url(string $slug, string $fallback): string {
    return blog_post($slug) ? '/blog/' . $slug . '/' : $fallback;
}

/** Published posts in $cats (newest first), topped up from other categories; never $exclude. */
function related_posts(array $cats, int $n, ?string $exclude = null): array {
    $out = []; $seen = [];
    foreach ([true, false] as $match) {
        foreach (blog_posts() as $p) {
            if (count($out) >= $n) break;
            if ($p['slug'] === $exclude || isset($seen[$p['slug']])) continue;
            if ($match !== in_array($p['category'], $cats, true)) continue;
            $out[] = $p; $seen[$p['slug']] = true;
        }
    }
    return $out;
}

/** Card linking to a hub page (same look as the homepage resource cards). */
function hub_card(string $key): string {
    [$path, , $title, $blurb, $ico] = HUBS[$key];
    return '<a class="card reveal" href="' . $path . '" style="text-decoration:none"><div class="badge-ico">' . icon($ico, 30) . '</div><h3>' . e($title) . '</h3><p>' . e($blurb) . '</p></a>';
}

/** Sidebar "Related" list: the hub's sibling pages plus up to $n_posts guides from its categories. */
function related_list(string $key, int $n_posts = 3): string {
    [$cats, $hubs] = HUB_TOPICS[$key];
    $h = '<div class="side-card"><h3>Related</h3><ul>';
    foreach ($hubs as $k) $h .= '<li><a href="' . hub_path($k) . '">' . e(HUBS[$k][2]) . '</a></li>';
    foreach (related_posts($cats, $n_posts) as $p) $h .= '<li><a href="/blog/' . e($p['slug']) . '/">' . e($p['title']) . '</a></li>';
    return $h . '</ul></div>';
}

/** Full-width "Keep reading" section for a hub page: guides from its categories, then sibling hubs. */
function related_section(string $key, int $n_posts = 3, int $n_hubs = 3): string {
    [$cats, $hubs] = HUB_TOPICS[$key];
    $posts = related_posts($cats, $n_posts);
    $h = '<section class="section alt related"><div class="wrap">';
    if ($posts) {
        $h .= '<div class="section-head"><span class="kicker">Keep reading</span><h2>Related claim guides</h2><p>Written by ' . AUTHOR . ' from questions Galveston owners actually ask. <a href="/blog/">All guides →</a></p></div><div class="grid g3">';
        foreach ($posts as $i => $p) $h .= post_card($p, $i);
        $h .= '</div>';
    }
    $h .= '<div class="section-head' . ($posts ? ' mt-lg' : '') . '"><span class="kicker">More resources</span><h2>Tools and references we use on real claims</h2></div><div class="grid g3">';
    foreach (array_slice($hubs, 0, $n_hubs) as $k) $h .= hub_card($k);
    return $h . '</div></div></section>';
}

/** "Read next" block for the end of a blog post: two guides from the same category, then its hubs. */
function read_next(array $post): string {
    $posts = related_posts([$post['category']], 2, $post['slug']);
    $hubs = CATEGORY_HUBS[$post['category']] ?? ['twia', 'calculators', 'windstorm-rules'];
    $h = '<div class="read-next"><h2>Read next</h2>';
    if ($posts) { $h .= '<div class="grid g2">'; foreach ($posts as $i => $p) $h .= post_card($p, $i); $h .= '</div>'; }
    $h .= '<p class="read-next-hubs"><strong>Related resources:</strong> ';
    $h .= implode(' · ', array_map(fn($k) => '<a href="' . hub_path($k) . '">' . e(HUBS[$k][2]) . '</a>', array_slice($hubs, 0, 4)));
    return $h . ' · <a href="/blog/">all claim guides</a></p></div>';
}

/** Sidebar list of the hub pages behind a post's category. */
function category_resources(string $category): string {
    $h = '<div class="side-card"><h3>Related resources</h3><ul>';
    foreach (CATEGORY_HUBS[$category] ?? ['twia', 'calculators', 'windstorm-rules'] as $k) {
        $h .= '<li><a href="' . hub_path($k) . '">' . e(HUBS[$k][2]) . '</a></li>';
    }
    return $h . '</ul></div>';
}

/** Hub pages that belong with a blog category, as inline links (for the category headings on /blog/). */
function category_hub_links(string $category): string {
    return implode(' · ', array_map(fn($k) => '<a href="' . hub_path($k) . '">' . e(HUBS[$k][2]) . '</a>', CATEGORY_HUBS[$category] ?? []));
}

/**
 * Visible breadcrumb trail. $trail is [[label, path], ...] for the parents (Home is implied);
 * $current is the page's own label. The matching BreadcrumbList schema is built in render_page().
 */
function breadcrumbs(array $trail, string $current): string {
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol><li><a href="/">Home</a></li>';
    foreach ($trail as [$label, $path]) $h .= '<li><a href="' . e($path) . '">' . e($label) . '</a></li>';
    return $h . '<li aria-current="page">' . e($current) . '</li></ol></div></nav>';
}

/**
 * Link recurring phrases in a blog post's body (see AUTO_LINKS). $self is the post's own path.
 * Text inside <a> and <h1>–<h4> is left alone. At most $max links are added.
 */
function auto_link_html(string $html, string $self, int $max = 6): string {
    // Targets this post already links by hand (fragments ignored), plus itself.
    $have = [$self => true];
    if (preg_match_all('/href="([^"#]+)/', $html, $mm)) foreach ($mm[1] as $u) $have[$u] = true;

    $targets = [];
    foreach (AUTO_LINKS as $phrase => $path) {
        $bare = strtok($path, '#');
        if (isset($have[$bare])) continue;
        if (str_starts_with($bare, '/blog/') && !blog_post(trim(substr($bare, 6), '/'))) continue; // not published yet
        $targets[] = ['/(?<![\w-])' . preg_quote($phrase, '/') . '(?![\w-])/iu', $path, $bare];
    }
    if (!$targets) return $html;

    $parts = preg_split('/(<[^>]+>)/', $html, -1, PREG_SPLIT_DELIM_CAPTURE);
    $depth = 0; $n = 0; $used = [];
    foreach ($parts as $i => $part) {
        if ($part === '') continue;
        if ($part[0] === '<') {
            if (preg_match('#^<(/?)(a|h[1-4])\b#i', $part, $m)) $depth += $m[1] === '' ? 1 : -1;
            continue;
        }
        if ($depth > 0 || $n >= $max) continue;
        // Find non-overlapping matches against the original text, then splice links in from the end.
        $hits = [];
        foreach ($targets as [$re, $path, $bare]) {
            if (isset($used[$bare]) || !preg_match($re, $part, $m, PREG_OFFSET_CAPTURE)) continue;
            [$text, $off] = $m[0]; $end = $off + strlen($text);
            foreach ($hits as $h) if ($off < $h[1] && $end > $h[0]) continue 2;
            $hits[] = [$off, $end, $path]; $used[$bare] = true;
            if (++$n >= $max) break;
        }
        usort($hits, fn($a, $b) => $b[0] <=> $a[0]);
        foreach ($hits as [$off, $end, $path]) {
            $part = substr($part, 0, $off) . '<a href="' . e($path) . '">' . substr($part, $off, $end - $off) . '</a>' . substr($part, $end);
        }
        $parts[$i] = $part;
    }
    return implode('', $parts);
}
