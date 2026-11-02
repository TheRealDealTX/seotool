<?php
// Blog and weather-event data access.
//
// Blog: data/blog-queue/*.json holds written-but-unpublished posts (deployed with the site, never
// edited at runtime). data/published.json maps slug => publish date and is the runtime state the
// weekly cron appends to. data/posts-generated/*.json holds posts the cron wrote itself once the
// queue ran out (only when an Anthropic API key is configured).
//
// Weather: data/weather-events.json is the list of 70+ mph wind days found by the weekly check;
// data/weather-status.json records the last check.

function read_json($file, $default = []) {
    if (!is_file($file)) return $default;
    $d = json_decode((string)file_get_contents($file), true);
    return is_array($d) ? $d : $default;
}

function write_json($file, $data) {
    if (!is_dir(dirname($file))) mkdir(dirname($file), 0755, true);
    $tmp = $file . '.tmp';
    file_put_contents($tmp, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE));
    rename($tmp, $file);
}

/** All posts that exist on disk (queued or generated), keyed by slug. */
function all_post_sources() {
    static $all = null;
    if ($all !== null) return $all;
    $all = [];
    foreach (array_merge(glob(DATA . '/blog-queue/*.json') ?: [], glob(DATA . '/posts-generated/*.json') ?: []) as $f) {
        $p = read_json($f);
        if (!empty($p['slug'])) { $p['_file'] = basename($f); $all[$p['slug']] = $p; }
    }
    uksort($all, fn($a, $b) => strcmp($all[$a]['_file'], $all[$b]['_file']));
    return $all;
}

/** Published posts, newest first, each with 'date'. */
function blog_posts() {
    $pub = read_json(DATA . '/published.json');
    $src = all_post_sources();
    $out = [];
    foreach ($pub as $slug => $date) {
        if (isset($src[$slug])) $out[] = $src[$slug] + ['date' => $date, 'author' => AUTHOR];
    }
    usort($out, fn($a, $b) => strcmp($b['date'], $a['date']) ?: strcmp($b['_file'], $a['_file']));
    return $out;
}

function blog_post($slug) {
    foreach (blog_posts() as $p) if ($p['slug'] === $slug) return $p;
    return null;
}

/** Next unpublished queued post, or null. */
function next_queued_post() {
    $pub = read_json(DATA . '/published.json');
    foreach (all_post_sources() as $slug => $p) if (!isset($pub[$slug])) return $p;
    return null;
}

function weather_events() {
    $ev = read_json(DATA . '/weather-events.json');
    usort($ev, fn($a, $b) => strcmp($b['date'], $a['date']));
    return $ev;
}

function weather_status() { return read_json(DATA . '/weather-status.json'); }

function fmt_date($ymd) { return date('F j, Y', strtotime($ymd)); }
