<?php defined('APP') || exit;

function blog_posts(): array
{
    static $posts = null;
    if ($posts !== null) return $posts;
    $posts = [];
    foreach (glob(APPDIR . '/content/blog/*.php') ?: [] as $f) {
        $p = require $f;
        if (is_array($p) && !empty($p['slug'])) $posts[$p['slug']] = $p;
    }
    uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
    return $posts;
}

function blog_post(string $slug): ?array
{
    return blog_posts()[$slug] ?? null;
}

function blog_category_icon(string $cat): string
{
    return ['Guides' => '🧭', 'Renters' => '🔑', 'Hosts' => '🏠', 'Travel Nurses' => '🩺', 'Interns' => '💼', 'Students' => '🎓', 'Safety' => '🛡️'][$cat] ?? '📝';
}

function blog_card(array $p): string
{
    $img = photo_img('blog.' . $p['slug'], 'post-card-img');
    return '<article class="post-card reveal"><a href="/blog/' . e($p['slug']) . '/">'
        . ($img ? '<span class="post-card-media">' . $img . '</span>' : '')
        . '<span class="post-card-body"><span class="post-cat">' . blog_category_icon($p['category']) . ' ' . e($p['category']) . '</span>'
        . '<h3>' . e($p['title']) . '</h3><p>' . e(excerpt($p['description'], 130)) . '</p>'
        . '<span class="small muted">' . e(fmt_date($p['date'])) . ' · ' . (int)($p['read_min'] ?? 6) . ' min read</span></span></a></article>';
}

function tools_list(): array
{
    return [
        'cost-calculator' => ['title' => 'Sublet Cost Calculator', 'icon' => '🧮', 'short' => 'Add up rent, deposit and fees — prorated for a mid-month move-in.'],
        'compare' => ['title' => 'Sublet vs. Short-Term Lease vs. Extended-Stay Hotel', 'icon' => '⚖️', 'short' => 'Compare the true cost of three ways to live somewhere for a few months.'],
        'proration' => ['title' => 'Move-In Date Proration Calculator', 'icon' => '📅', 'short' => 'Work out partial-month rent three common ways.'],
        'packing-checklist' => ['title' => 'Sublet Packing Checklist', 'icon' => '🧳', 'short' => 'A tick-as-you-go list that saves on your device.'],
        'room-planner' => ['title' => 'Room Planner', 'icon' => '📐', 'short' => 'Sketch a room to scale and check what fits.'],
        'city-quiz' => ['title' => 'City Match Quiz', 'icon' => '🗺️', 'short' => 'Six questions to suggest cities worth a short-term stay.'],
    ];
}
