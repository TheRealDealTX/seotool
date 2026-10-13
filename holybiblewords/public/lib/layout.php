<?php
// Shared page chrome. render_page() prints a full HTML document.

function in_native_app(): bool {
    return str_contains($_SERVER['HTTP_USER_AGENT'] ?? '', 'HolyBibleWordsApp');
}

function icon(string $name, string $cls = ''): string {
    return '<svg class="ic ' . $cls . '" aria-hidden="true"><use href="#i-' . $name . '"/></svg>';
}

/**
 * $p keys: title, description, canonical (path), body, ver (current version or null),
 * switch (map ver => path for the version switcher), alternates (map ver => path),
 * noindex, jsonld (array of schema nodes), type (page type for app.js), og_image, data (extra data-* attrs)
 */
function render_page(array $p): void {
    $ver = $p['ver'] ?? null;
    $vers = versions();
    $canon = SITE_URL . ($p['canonical'] ?? '/');
    $title = $p['title'];
    $desc = $p['description'] ?? 'Read the Holy Bible online: King James Version (KJV) and Ang Pulong sa Dios, with easy chapter and verse navigation, search, and a daily verse.';
    $img = SITE_URL . ($p['og_image'] ?? '/assets/img/og-image.webp');
    $lang = $ver ? $vers[$ver]['lang'] : 'en';
    $app = in_native_app();
    header('Content-Type: text/html; charset=utf-8');
    ?>
<!doctype html>
<html lang="<?= e($lang) ?>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<?php if (!empty($p['noindex'])): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<?php endif ?>
<link rel="canonical" href="<?= e($canon) ?>">
<?php foreach (($p['alternates'] ?? []) as $av => $path): ?>
<link rel="alternate" hreflang="<?= e($vers[$av]['lang']) ?>" href="<?= e(SITE_URL . $path) ?>">
<?php endforeach ?>
<meta property="og:site_name" content="<?= SITE_NAME ?>">
<meta property="og:type" content="<?= isset($p['article']) ? 'article' : 'website' ?>">
<meta property="og:title" content="<?= e($title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:image" content="<?= e($img) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1b5e8f" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#11161c" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Holy Bible">
<script>
/* apply saved reading settings before first paint */
try{var s=JSON.parse(localStorage.getItem('hbw.settings')||'{}'),d=document.documentElement;
d.dataset.theme=s.theme||'auto';d.dataset.font=s.font||'serif';d.dataset.layout=s.layout||'verses';
d.dataset.nums=s.nums===false?'off':'on';if(s.size)d.style.setProperty('--reader-size',s.size+'px');
if(s.lh)d.style.setProperty('--reader-lh',s.lh);}catch(e){}
</script>
<link rel="stylesheet" href="/assets/css/app.css?v=<?= ASSET_VER ?>">
<?php if (!empty($p['jsonld'])): ?>
<script type="application/ld+json"><?= json_encode(['@context' => 'https://schema.org', '@graph' => $p['jsonld']], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?></script>
<?php endif ?>
<?php if (!$app): ?>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-WX37KX6GT4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-WX37KX6GT4');</script>
<meta name="google-adsense-account" content="ca-pub-3886800648957674">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3886800648957674" crossorigin="anonymous"></script>
<?php endif ?>
</head>
<body class="<?= $app ? 'native-app' : '' ?>">
<?= svg_sprite() ?>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="/" aria-label="<?= SITE_NAME ?> home">
    <img src="/assets/img/logo-64.png" width="32" height="32" alt="">
    <span>Holy Bible <b>Words</b></span>
  </a>
  <?= version_switch($ver, $p['switch'] ?? null) ?>
  <nav class="mainnav" aria-label="Main">
    <a href="/" data-nav="home"><?= icon('home') ?><span>Home</span></a>
    <a href="/ta/genesis/1/" data-nav="read" class="js-read-link"><?= icon('book') ?><span>Read</span></a>
    <a href="/search/" data-nav="search"><?= icon('search') ?><span>Search</span></a>
    <a href="/verse-of-the-day/" data-nav="votd"><?= icon('sun') ?><span>Daily</span></a>
    <a href="/plan/" data-nav="plan"><?= icon('calendar') ?><span>Plan</span></a>
    <a href="/saved/" data-nav="saved"><?= icon('bookmark') ?><span>Saved</span></a>
  </nav>
  <button class="icon-btn theme-btn" type="button" data-action="theme" aria-label="Dark mode" aria-pressed="false" title="Dark mode"><?= icon('moon', 'i-moon') ?><?= icon('sun', 'i-sun') ?></button>
  <button class="icon-btn" type="button" data-action="settings" aria-label="Reading settings"><?= icon('type') ?></button>
</header>
<div id="progress" aria-hidden="true"></div>
<main id="main" data-page="<?= e($p['type'] ?? 'page') ?>" data-title="<?= e($title) ?>"<?php
    foreach (($p['data'] ?? []) as $k => $v) echo ' data-' . e($k) . '="' . e((string)$v) . '"';
    if ($p['switch'] ?? null) echo " data-switch='" . e(json_encode($p['switch'])) . "'";
?>>
<?= $p['body'] ?>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-brand"><img src="/assets/img/logo-64.png" width="28" height="28" alt=""> <?= SITE_NAME ?> — Read the Bible online</div>
    <nav class="foot-links" aria-label="Footer">
      <a href="/ta/">King James Version (KJV)</a>
      <a href="/ceb/">Ang Pulong sa Dios</a>
      <a href="/blog/">Blog</a>
      <a href="/app/">Get the app</a>
      <a href="/privacy-policy/">Privacy Policy</a>
    </nav>
    <div class="copy"><?= credits(array_keys(versions())) ?></div>
  </div>
</footer>
<nav class="tabbar" aria-label="App">
  <a href="/" data-nav="home"><?= icon('home') ?><span>Home</span></a>
  <a href="/ta/genesis/1/" data-nav="read" class="js-read-link"><?= icon('book') ?><span>Read</span></a>
  <a href="/search/" data-nav="search"><?= icon('search') ?><span>Search</span></a>
  <a href="/plan/" data-nav="plan"><?= icon('calendar') ?><span>Plan</span></a>
  <a href="/saved/" data-nav="saved"><?= icon('bookmark') ?><span>Saved</span></a>
</nav>
<div id="sheet-root"></div>
<div id="toast" role="status" aria-live="polite"></div>
<script src="/assets/js/app.js?v=<?= ASSET_VER ?>" defer></script>
</body>
</html>
<?php
}

function version_switch(?string $ver, ?array $switch): string {
    $h = '<div class="ver-switch" role="group" aria-label="Bible version">';
    foreach (versions() as $k => $v) {
        $href = $switch[$k] ?? "/$k/";
        $on = $k === $ver ? ' aria-current="true" class="on"' : '';
        $h .= '<a href="' . e($href) . '" data-ver="' . $k . '" hreflang="' . e($v['lang']) . '" title="' . e($v['label']) . '"' . $on . '>'
            . e($v['short']) . '</a>';
    }
    return $h . '</div>';
}

function breadcrumbs(array $items): string {
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    foreach ($items as $i => [$label, $href]) {
        $h .= '<li>' . ($href && $i < count($items) - 1 ? '<a href="' . e($href) . '">' . e($label) . '</a>' : '<span>' . e($label) . '</span>') . '</li>';
    }
    return $h . '</ol></nav>';
}

function breadcrumb_ld(array $items): array {
    $list = [];
    foreach ($items as $i => [$label, $href]) {
        $list[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $label, 'item' => SITE_URL . ($href ?: '/')];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $list];
}

function svg_sprite(): string {
    $paths = [
        'home' => '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',
        'book' => '<path d="M2 4.5c3-1.3 6.3-1 10 1.2 3.7-2.2 7-2.5 10-1.2v15c-3-1.3-6.3-1-10 1.2-3.7-2.2-7-2.5-10-1.2zM12 5.7v15"/>',
        'search' => '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
        'moon' => '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
        'sun' => '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
        'calendar' => '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
        'bookmark' => '<path d="M6 3h12v18l-6-4-6 4z"/>',
        'type' => '<path d="M4 7V5h11v2M9.5 5v14M7 19h5M14 12v-1.5h7V12M17.5 10.5V19M16 19h3"/>',
        'left' => '<path d="m15 18-6-6 6-6"/>',
        'right' => '<path d="m9 18 6-6-6-6"/>',
        'down' => '<path d="m6 9 6 6 6-6"/>',
        'share' => '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>',
        'copy' => '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/>',
        'play' => '<path d="M7 4v16l13-8z"/>',
        'pause' => '<path d="M7 4h3v16H7zM14 4h3v16h-3z"/>',
        'columns' => '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M12 4v16"/>',
        'x' => '<path d="M18 6 6 18M6 6l12 12"/>',
        'pen' => '<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
        'image' => '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/>',
        'download' => '<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>',
        'check' => '<path d="M20 6 9 17l-5-5"/>',
        'compare' => '<path d="M8 3 4 7l4 4M4 7h16M16 21l4-4-4-4M20 17H4"/>',
        'highlight' => '<path d="m9 11-6 6v3h9l3-3M22 12l-4.6 4.6a2 2 0 0 1-2.8 0l-5.2-5.2a2 2 0 0 1 0-2.8L14 4"/>',
        'list' => '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    ];
    $h = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">';
    foreach ($paths as $id => $d) {
        $h .= '<symbol id="i-' . $id . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' . $d . '</symbol>';
    }
    return $h . '</svg>';
}
