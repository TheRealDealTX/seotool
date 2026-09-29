<?php
/**
 * End-to-end HTTP checks against a running site (local dev server or production).
 *
 *   php tests/http.php http://127.0.0.1:8080 [admin-email] [admin-password]
 *
 * Read-only against production EXCEPT: it submits one contact-form message
 * (clearly marked as a test) and signs in if credentials are given.
 * Old URLs are taken from app/data/redirects.json and articles.json.
 */
declare(strict_types=1);

$base = rtrim($argv[1] ?? 'http://127.0.0.1:8080', '/');
$email = $argv[2] ?? null;
$password = $argv[3] ?? null;
$root = dirname(__DIR__);
$pass = 0; $fail = 0;
function t(string $n, bool $ok, string $d = ''): void { global $pass, $fail; $ok ? $pass++ : $fail++; echo ($ok ? '  ✔ ' : '  ✘ ') . $n . ($ok || $d === '' ? '' : " — {$d}") . "\n"; }
function section(string $s): void { echo "\n■ {$s}\n"; }

$jar = tempnam(sys_get_temp_dir(), 'rtjar');
function req(string $url, array $o = []): array
{
    global $jar;
    $ch = curl_init($url);
    $h = [];
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => false, CURLOPT_TIMEOUT => 30,
        CURLOPT_COOKIEJAR => $jar, CURLOPT_COOKIEFILE => $jar, CURLOPT_USERAGENT => 'RodeoTexas-tests',
        CURLOPT_HEADERFUNCTION => static function ($c, $l) use (&$h) { $p = strpos($l, ':'); if ($p) { $h[strtolower(trim(substr($l, 0, $p)))] = trim(substr($l, $p + 1)); } return strlen($l); }]);
    if (isset($o['post'])) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($o['post']));
    }
    if (isset($o['headers'])) {
        curl_setopt($ch, CURLOPT_HTTPHEADER, $o['headers']);
    }
    $body = (string) curl_exec($ch);
    $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    return ['code' => $code, 'body' => $body, 'h' => $h];
}

section('Core pages');
foreach (['/', '/rodeos/', '/rodeos/?when=weekend', '/rodeos/?when=month', '/rodeos/?view=calendar', '/rodeos/?view=map', '/past-events/', '/blog/',
          '/about/', '/contact/', '/privacy-policy/', '/submit-event/', '/favorites/', '/sitemap.xml', '/sitemap-events.xml', '/sitemap-pages.xml', '/sitemap-articles.xml', '/robots.txt'] as $u) {
    $r = req($base . $u);
    t("GET {$u} → 200", $r['code'] === 200, (string) $r['code']);
}
$home = req($base . '/');
t('Homepage has <title>, description, canonical', (bool) preg_match('~<title>.+</title>~', $home['body']) && str_contains($home['body'], 'name="description"') && str_contains($home['body'], 'rel="canonical"'));
t('Open Graph + Twitter tags present', str_contains($home['body'], 'property="og:image"') && str_contains($home['body'], 'twitter:card'));
t('Site-wide analytics tag present on public pages', str_contains($home['body'], 'G-BYZKZGNG2D'));
t('Security headers', ($home['h']['x-content-type-options'] ?? '') === 'nosniff' && isset($home['h']['referrer-policy']));
t('Internals not reachable (/includes/head.php)', in_array(req($base . '/includes/head.php')['code'], [403, 404], true));
t('Internals not reachable (/pages/home.php)', in_array(req($base . '/pages/home.php')['code'], [403, 404], true));
t('Unknown page → 404', req($base . '/this-page-does-not-exist/')['code'] === 404);

section('Old URLs (SEO migration)');
$arts = json_decode((string) file_get_contents($root . '/app/data/articles.json'), true)['articles'];
$ok = 0; $bad = [];
foreach ($arts as $a) {
    $r = req($base . '/' . $a['slug'] . '/');
    if ($r['code'] === 200 && str_contains($r['body'], htmlspecialchars($a['title'], ENT_QUOTES | ENT_HTML5))) { $ok++; } else { $bad[] = $a['slug'] . ':' . $r['code']; }
}
t('All ' . count($arts) . ' articles live at their original URLs', $ok === count($arts), implode(', ', $bad));
$red = json_decode((string) file_get_contents($root . '/app/data/redirects.json'), true);
$ok = 0; $bad = [];
foreach ($red as $from => $to) {
    $r = req($base . $from);
    if ($r['code'] === 301 && str_ends_with((string) ($r['h']['location'] ?? ''), $to)) { $ok++; } else { $bad[] = $from . ':' . $r['code']; }
}
t('All ' . count($red) . ' retired URLs 301-redirect to the right place', $ok === count($red), implode(', ', array_slice($bad, 0, 5)));
$legacy = json_decode((string) file_get_contents($root . '/app/data/legacy_events.json'), true);
$ok = 0; $bad = [];
foreach ($legacy as $l) {
    $r = req($base . $l['legacy_url']);
    if ($r['code'] === 200 && str_contains($r['body'], 'noindex')) { $ok++; } else { $bad[] = $l['legacy_url'] . ':' . $r['code']; }
}
t('All ' . count($legacy) . ' Texas legacy event URLs kept (archived, noindex)', $ok === count($legacy), implode(', ', array_slice($bad, 0, 5)));
t('Missing trailing slash → 301', req($base . '/about')['code'] === 301);
t('Old WordPress feed → 301 /blog/', str_ends_with((string) (req($base . '/feed/')['h']['location'] ?? ''), '/blog/'));

section('Event pages');
$list = req($base . '/rodeos/');
preg_match('~href="/rodeos/([a-z0-9-]+)/"~', $list['body'], $m);
if ($m) {
    $ev = req($base . '/rodeos/' . $m[1] . '/');
    t('Event page loads', $ev['code'] === 200);
    preg_match_all('~<script type="application/ld\+json">(.*?)</script>~s', $ev['body'], $lds);
    $types = [];
    $valid = true;
    foreach ($lds[1] as $j) { $d = json_decode($j, true); if (!$d) { $valid = false; } else { $types[] = $d['@type'] ?? '?'; if (($d['@type'] ?? '') === 'Event') { $evLd = $d; } } }
    t('JSON-LD is valid JSON', $valid && $types);
    t('Event structured data present with location', isset($evLd['location']['address']['addressRegion']) && $evLd['location']['address']['addressRegion'] === 'TX');
    t('Event date includes the year', (bool) preg_match('~event-hero__when"><time[^>]*>[^<]*\b20\d\d\b~', $ev['body']));
    t('Source and last-verified shown', str_contains($ev['body'], 'Information source') && str_contains($ev['body'], 'Last verified'));
    $ics = req($base . '/rodeos/' . $m[1] . '/calendar.ics');
    t('Calendar download (text/calendar, VEVENT)', str_starts_with((string) ($ics['h']['content-type'] ?? ''), 'text/calendar') && str_contains($ics['body'], 'BEGIN:VEVENT'));
    $api = json_decode(req($base . '/api/events.json?slugs=' . $m[1])['body'], true);
    t('Favorites API returns the event', ($api['count'] ?? 0) === 1);
} else {
    t('At least one upcoming event listed', false, 'none found');
}
$xss = req($base . '/rodeos/?q=' . rawurlencode('<script>alert(1)</script>'));
t('Search input is escaped (no reflected XSS)', $xss['code'] === 200 && !str_contains($xss['body'], '<script>alert(1)</script>'));
t('Hostile filter values handled', req($base . "/rodeos/?region=x'%20OR%201=1--&from=2026-99-99&page=-4")['code'] === 200);

section('Forms (held for review, spam protection)');
$form = req($base . '/contact/');
preg_match('~name="_ft" value="([^"]+)"~', $form['body'], $tok);
t('Contact form has signed token + honeypot', isset($tok[1]) && str_contains($form['body'], 'company_website'));
$bot = req($base . '/contact/', ['post' => ['_ft' => $tok[1] ?? '', 'company_website' => 'http://spam.example', 'email' => 'bot@example.com', 'message' => 'buy now']]);
t('Honeypot submission silently discarded (303, no error shown)', $bot['code'] === 303);
sleep(5);
$real = req($base . '/contact/', ['post' => ['_ft' => $tok[1] ?? '', 'company_website' => '', 'first_name' => 'Automated', 'last_name' => 'Test',
    'email' => 'test@example.com', 'message' => '[AUTOMATED TEST] Please ignore — deployment verification.']]);
t('Valid contact message accepted (303 → thank-you)', $real['code'] === 303 && str_contains((string) ($real['h']['location'] ?? ''), 'sent=1'));
$tampered = req($base . '/submit-event/', ['post' => ['_ft' => '123.abc', 'title' => 'X', 'start_date' => '2030-01-01', 'city' => 'Austin', 'email' => 'a@b.co', 'confirm_texas' => '1']]);
t('Forged form token rejected', $tampered['code'] === 200 && str_contains($tampered['body'], 'expired'));

section('Admin security');
@unlink($jar);   // fresh session so the cookie is issued on this request
$a = req($base . '/admin/');
t('Admin requires login', $a['code'] === 302 && str_contains((string) ($a['h']['location'] ?? ''), 'page=login'));
$login = req($base . '/admin/?page=login');
t('Admin has strict CSP & noindex', str_contains((string) ($login['h']['content-security-policy'] ?? ''), "script-src 'self'") && str_contains((string) ($login['h']['x-robots-tag'] ?? ''), 'noindex'));
t('No public tracking scripts in admin', !str_contains($login['body'], 'googletagmanager'));
$ck = (string) ($a['h']['set-cookie'] ?? '');
t('Admin session cookie is HttpOnly + SameSite=Strict' . (str_starts_with($base, 'https') ? ' + Secure' : ''), stripos($ck, 'httponly') !== false && stripos($ck, 'samesite=strict') !== false && (!str_starts_with($base, 'https') || stripos($ck, 'secure') !== false), $ck);
t('Login without CSRF token rejected', req($base . '/admin/?page=login', ['post' => ['email' => 'x@example.com', 'password' => 'y']])['code'] === 400);
t('Admin page templates not web-reachable', req($base . '/app/admin/pages/dashboard.php')['code'] !== 200);
if ($email && $password) {
    preg_match('~name="_csrf" value="([^"]+)"~', $login['body'], $c);
    $in = req($base . '/admin/?page=login', ['post' => ['_csrf' => $c[1] ?? '', 'email' => $email, 'password' => $password]]);
    t('Admin login works', $in['code'] === 303);
    $dash = req($base . '/admin/?page=dashboard');
    t('Dashboard reachable after login', $dash['code'] === 200 && str_contains($dash['body'], 'Run import now'));
    t('POST without CSRF token rejected when logged in', req($base . '/admin/?page=redirects', ['post' => ['from_path' => '/x/', 'to_path' => '/']])['code'] === 400);
    t('Cross-origin POST rejected', req($base . '/admin/?page=redirects', ['post' => ['_csrf' => 'x'], 'headers' => ['Origin: https://evil.example']])['code'] === 400);
}
@unlink($jar);
echo "\n{$pass} passed, {$fail} failed\n";
exit($fail ? 1 : 0);
