<?php
/**
 * Content loaders. Each content/<type>/<slug>.php returns an array.
 */
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

function load_dir(string $dir): array
{
    static $cache = [];
    if (isset($cache[$dir])) {
        return $cache[$dir];
    }
    $out = [];
    foreach (glob(SITE_ROOT . '/content/' . $dir . '/*.php') ?: [] as $file) {
        $data = require $file;
        if (is_array($data) && isset($data['slug'])) {
            $out[$data['slug']] = $data;
        }
    }
    return $cache[$dir] = $out;
}

/** All services in SERVICES_ORDER (unknown slugs skipped, extras appended). */
function services(): array
{
    $all = load_dir('services');
    $ordered = [];
    foreach (SERVICES_ORDER as $slug) {
        if (isset($all[$slug])) {
            $ordered[$slug] = $all[$slug] + ['path' => "/services/{$slug}/", 'icon' => SERVICE_ICONS[$slug] ?? 'sparkle'];
        }
    }
    foreach ($all as $slug => $s) {
        if (!isset($ordered[$slug])) {
            $ordered[$slug] = $s + ['path' => "/services/{$slug}/", 'icon' => 'sparkle'];
        }
    }
    return $ordered;
}

function service(string $slug): ?array
{
    return services()[$slug] ?? null;
}

function areas(): array
{
    $all = load_dir('areas');
    $ordered = [];
    foreach (AREAS_ORDER as $slug) {
        if (isset($all[$slug])) {
            $ordered[$slug] = $all[$slug] + ['path' => "/service-areas/{$slug}/"];
        }
    }
    foreach ($all as $slug => $a) {
        if (!isset($ordered[$slug])) {
            $ordered[$slug] = $a + ['path' => "/service-areas/{$slug}/"];
        }
    }
    return $ordered;
}

function area(string $slug): ?array
{
    return areas()[$slug] ?? null;
}

/** Posts, newest first. Post URLs are root-level (/<slug>/), matching the previous site. */
function posts(): array
{
    $all = load_dir('posts');
    foreach ($all as $slug => &$p) {
        $p['path'] = "/{$slug}/";
        $p['reading'] = reading_time($p['body'] ?? '');
        $p['words'] = word_count($p['body'] ?? '');
    }
    unset($p);
    uasort($all, fn($a, $b) => strcmp($b['published'] . $b['slug'], $a['published'] . $a['slug']));
    return $all;
}

function post(string $slug): ?array
{
    return posts()[$slug] ?? null;
}

function post_categories(): array
{
    $cats = [];
    foreach (posts() as $p) {
        $cats[$p['category']] = ($cats[$p['category']] ?? 0) + 1;
    }
    ksort($cats);
    return $cats;
}

function tools(): array
{
    $out = [];
    foreach (TOOLS as $slug => [$name, $desc, $icon]) {
        $out[$slug] = ['slug' => $slug, 'name' => $name, 'description' => $desc, 'icon' => $icon, 'path' => "/tools/{$slug}/"];
    }
    return $out;
}

/** Gallery items: every photo in assets/img grouped into a category by filename. */
function gallery_items(): array
{
    static $items = null;
    if ($items !== null) {
        return $items;
    }
    $items = [];
    $map = [
        'tree' => 'Trees', 'pool' => 'Pools', 'backyard' => 'Backyards', 'front-yard' => 'Front Yards',
        'commercial' => 'Commercial', 'modern' => 'Modern', 'path' => 'Paths', 'design' => 'Design',
        'repair' => 'Service', 'maintenance' => 'Service', 'led' => 'LED', 'low-voltage' => 'LED',
        'installation' => 'Installation', 'solar' => 'Ideas', 'ideas' => 'Ideas',
    ];
    foreach (glob(SITE_ROOT . '/assets/img/*.webp') ?: [] as $file) {
        $name = basename($file, '.webp');
        if (in_array($name, ['how-many-landscape-lights-do-i-need', 'best-front-yard-landscape-lighting-ideas'], true)) {
            continue;
        }
        $cat = 'Residential';
        foreach ($map as $needle => $label) {
            if (str_contains($name, $needle)) {
                $cat = $label;
                break;
            }
        }
        $alt = ucfirst(str_replace('-', ' ', preg_replace('/-\d+(-\d+)?$/', '', $name)));
        $alt = preg_replace('/\baustin\b/i', 'Austin', $alt);
        $alt = preg_replace('/\btx\b/i', 'TX', $alt);
        $alt = preg_replace('/\bled\b/i', 'LED', $alt);
        $items[] = ['name' => $name, 'cat' => $cat, 'alt' => $alt . ' by Austin Landscape Lighting'];
    }
    return $items;
}

/** Site-wide FAQ used on the homepage and /faq/. */
function site_faqs(): array
{
    return [
        ['q' => 'How much does landscape lighting cost in Austin?',
         'a' => 'Most residential systems designed and installed by Austin Landscape Lighting land in a planning range of $3,500 to $12,000, driven mostly by fixture count and fixture grade. A focused front elevation with 8 to 12 fixtures sits at the low end; a layered front-and-back design with 30 or more fixtures, smart controls and tree moonlighting sits at the high end. Every written estimate is itemized, and the price we quote is the price you pay.'],
        ['q' => 'How long does installation take?',
         'a' => 'Most residential projects are installed in a single day. Low-voltage wiring is buried a few inches below mulch or turf, so there is no trenching through hardscape and no permits for the 12-volt side. We return after dark for a night aiming session, which typically takes one to two hours.'],
        ['q' => 'Do you use LED fixtures?',
         'a' => 'Yes. Every new system uses integrated or lamp-based LED fixtures in solid brass or copper. LEDs draw roughly 80 percent less power than the halogen fixtures common in older Austin systems, run cool, and are rated for 40,000 hours or more. We also retrofit existing halogen systems to LED.'],
        ['q' => 'What color temperature do you recommend?',
         'a' => 'For most Austin homes we recommend 2700K warm white. It flatters limestone, brick and wood, reads as natural rather than commercial, and is friendly to the dark-sky sensibilities of the Hill Country. We use 3000K on some modern architecture and cool-toned stone, and occasionally 2400K for a candlelit feel on patios.'],
        ['q' => 'Will the lights run up my electric bill?',
         'a' => 'A typical 20-fixture LED system draws about 100 watts in total, less than two old incandescent bulbs. Running it six hours a night costs roughly $2 to $4 a month at Austin Energy rates. You can check your own numbers with our LED savings calculator.'],
        ['q' => 'Is the system weatherproof and deer-proof?',
         'a' => 'Fixtures are solid brass or copper with marine-grade seals and they are rated for direct burial and wet locations. Wire connections are made with waterproof, gel-filled connectors. Brass stakes and ground-mounted fixtures hold up to deer traffic far better than the aluminum fixtures sold at big-box stores.'],
        ['q' => 'What does the warranty cover?',
         'a' => 'Austin Landscape Lighting backs every installation with a two-year workmanship warranty covering wiring, connections, aiming and transformer setup. Fixtures carry their manufacturer warranties, which range from 10 years to lifetime on the brass bodies. If anything is not right, we come back and fix it.'],
        ['q' => 'Which areas do you serve?',
         'a' => 'We serve Austin and the surrounding communities: Round Rock, Cedar Park, Pflugerville, Georgetown, Bee Cave, Lakeway, Westlake Hills, Rollingwood, Kyle, Buda and Dripping Springs. If you are nearby and do not see your city listed, call us; we are usually glad to make the drive.'],
    ];
}
