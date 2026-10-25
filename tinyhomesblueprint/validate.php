<?php
// Post-change checks against a running copy of the site.
//   php -S 127.0.0.1:8099 -t . dev-router.php &   (or any server running index.php)
//   php validate.php [base-url]
// Checks every route for: HTTP 200, no PHP errors, one <h1>, title/description length,
// canonical URL, valid JSON-LD, and that every internal link resolves.
require __DIR__ . '/inc/config.php';
$base = rtrim($argv[1] ?? 'http://127.0.0.1:8099', '/');
$problems = 0; $warnings = 0;
$fail = function ($path, $msg) use (&$problems) { $problems++; echo "FAIL $path: $msg\n"; };
$warn = function ($path, $msg) use (&$warnings) { $warnings++; echo "warn $path: $msg\n"; };
$fetch = function ($url) {
    $ctx = stream_context_create(['http' => ['ignore_errors' => true, 'follow_location' => 0, 'timeout' => 20]]);
    $body = @file_get_contents($url, false, $ctx);
    preg_match('#HTTP/\S+ (\d+)#', $http_response_header[0] ?? '', $m);
    return [(int)($m[1] ?? 0), (string)$body];
};
$linkOk = [];
foreach ($ROUTES as $path => $r) {
    [$code, $html] = $fetch($base . $path);
    if ($code !== 200) { $fail($path, "HTTP $code"); continue; }
    if (preg_match('#<b>(Warning|Notice|Fatal error|Deprecated)</b>|(Warning|Fatal error|Notice|Deprecated): .* in /#', $html)) $fail($path, 'PHP error in output');
    $h1 = preg_match_all('#<h1[\s>]#', $html);
    if ($h1 !== 1) $fail($path, "$h1 <h1> tags");
    preg_match('#<title>(.*?)</title>#s', $html, $t);
    $tl = mb_strlen(html_entity_decode($t[1] ?? '', ENT_QUOTES));
    if ($tl < 20 || $tl > 65) $warn($path, "title length $tl");
    preg_match('#<meta name="description" content="([^"]*)"#', $html, $d);
    $dl = mb_strlen(html_entity_decode($d[1] ?? '', ENT_QUOTES));
    if ($dl < 70 || $dl > 165) $warn($path, "description length $dl");
    if (strpos($html, '<link rel="canonical" href="' . SITE_URL . $path . '">') === false) $fail($path, 'canonical mismatch');
    preg_match_all('#<script type="application/ld\+json">(.*?)</script>#s', $html, $ld);
    foreach ($ld[1] as $j) if (json_decode($j) === null) $fail($path, 'invalid JSON-LD');
    preg_match_all('#href="(/[^"]*)"#', $html, $links);
    foreach (array_unique($links[1]) as $l) {
        $l = html_entity_decode($l);
        $p = strtok($l, '?#');
        if ($p === false || $p === '') continue;
        if (isset($ROUTES[$p]) || is_file(__DIR__ . $p)) continue;
        if (!isset($linkOk[$p])) { [$c] = $fetch($base . $p); $linkOk[$p] = $c; }
        if ($linkOk[$p] !== 200) $fail($path, "broken link $l ($linkOk[$p])");
        elseif (!isset($ROUTES[$p])) $warn($path, "link to non-route $l");
    }
}
foreach ($REDIRECTS as $from => $to) {
    $ctx = stream_context_create(['http' => ['ignore_errors' => true, 'follow_location' => 0]]);
    @file_get_contents($base . $from, false, $ctx);
    $loc = ''; foreach ($http_response_header ?? [] as $h) if (stripos($h, 'Location:') === 0) $loc = trim(substr($h, 9));
    if (strpos($http_response_header[0] ?? '', '301') === false || $loc !== SITE_URL . $to) $fail($from, "redirect expected to $to, got $loc");
    if (!isset($ROUTES[$to]) && $to !== '/sitemap.xml') $fail($from, "redirect target $to is not a route");
}
[$code, $xml] = $fetch($base . '/sitemap.xml');
if ($code !== 200 || substr_count($xml, '<url>') !== count($ROUTES)) $fail('/sitemap.xml', 'sitemap missing routes');
[$code] = $fetch($base . '/no-such-page/');
if ($code !== 404) $fail('/no-such-page/', "expected 404, got $code");
printf("\n%d routes, %d redirects checked: %d failures, %d warnings\n", count($ROUTES), count($REDIRECTS), $problems, $warnings);
exit($problems ? 1 : 0);
