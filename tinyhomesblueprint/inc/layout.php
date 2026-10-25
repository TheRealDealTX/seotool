<?php
// Shared layout and component helpers. Page files call page_start() and page_end()
// around their markup; everything else here is an optional building block.

function e($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

function abs_url(string $path): string { return SITE_URL . $path; }

function asset(string $path): string { return $path . '?v=' . ASSET_VER; }

function money(int $n): string { return '$' . number_format($n); }

function json_ld(array $data): string {
    return '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . "</script>\n";
}

// Small inline icon set (stroke icons, 24x24, currentColor).
function icon(string $name, string $class = 'ico'): string {
    $p = [
        'aframe'    => '<path d="M12 3 3 21h18L12 3Z"/><path d="M12 11l-3 10M12 11l3 10"/><path d="M10 15h4"/>',
        'container' => '<rect x="2" y="7" width="20" height="11" rx="1"/><path d="M6 7v11M10 7v11M14 7v11M18 7v11"/>',
        'cottage'   => '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/><path d="M16 6V3h2v4.5"/>',
        'cabin'     => '<path d="M2 12 12 5l10 7"/><path d="M4 11v9h16v-9"/><path d="M4 14h16M4 17h16"/><path d="M10 20v-4h4v4"/>',
        'wheels'    => '<path d="M3 16V9l6-4 6 4v7"/><path d="M3 16h18"/><circle cx="7" cy="18.5" r="1.8"/><circle cx="12" cy="18.5" r="1.8"/><path d="M15 12h6v4"/>',
        'loft'      => '<path d="M3 10 12 3l9 7v11H3V10Z"/><path d="M3 13h11"/><path d="M15 13v8M15 15h3M15 18h3"/>',
        'shed'      => '<path d="M3 9 21 6v15H3V9Z"/><path d="M8 21v-7h5v7"/><rect x="15" y="11" width="3" height="3"/>',
        'farm'      => '<path d="M2 11 8 5l6 6"/><path d="M4 9.5V20h8v-9"/><path d="M12 20h9v-7l-3-3h-6"/><path d="M15 20v-4h3v4"/>',
        'adu'       => '<path d="M2 12 9 6l7 6"/><path d="M4 11v9h10v-9"/><path d="M15 15l3.5-3 3.5 3"/><path d="M16 14.5V20h5v-5.5"/>',
        'cost'      => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h2M12 10h2M16 10h0M8 14h2M12 14h2M8 18h2M12 18h2M16 14v4"/>',
        'layout'    => '<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M3 11h8V3M11 11v10M11 15h10"/>',
        'size'      => '<path d="M3 21 21 3"/><path d="M3 16v5h5M21 8V3h-5"/><path d="M7 3H3v4M17 21h4v-4"/>',
        'weight'    => '<path d="M6 8h12l2 13H4L6 8Z"/><circle cx="12" cy="5" r="2.5"/><path d="M10 14h4"/>',
        'solar'     => '<circle cx="12" cy="5" r="2.5"/><path d="M12 0.5v1M16.5 5h1M6.5 5h1"/><path d="M4 11h16l2 9H2l2-9Z"/><path d="M3 15.5h18M9 11l-1 9M15 11l1 9"/>',
        'quiz'      => '<circle cx="12" cy="12" r="9.5"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7v.5"/><path d="M12 17h.01"/>',
        'phone'     => '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2Z"/>',
        'mail'      => '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        'check'     => '<path d="m4 12 5 5L20 6"/>',
        'arrow'     => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'file'      => '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6Z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
        'ruler'     => '<path d="M3 17 17 3l4 4L7 21l-4-4Z"/><path d="m7 13 2 2M10 10l2 2M13 7l2 2"/>',
        'bed'       => '<path d="M2 18V7M2 13h20v5M22 18v-3a3 3 0 0 0-3-3h-8v1"/><circle cx="6.5" cy="10.5" r="1.8"/>',
        'bath'      => '<path d="M3 12h18v3a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5v-3Z"/><path d="M6 12V5a2 2 0 0 1 4 0"/><path d="M7 20l-1 2M17 20l1 2"/>',
        'stairs'    => '<path d="M3 21h5v-5h5v-5h5V6h3"/>',
        'menu'      => '<path d="M3 6h18M3 12h18M3 18h18"/>',
        'close'     => '<path d="M5 5l14 14M19 5 5 19"/>',
        'book'      => '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5v-17Z"/><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>',
        'leaf'      => '<path d="M5 21c0-9 5-15 16-17-1 11-7 16-16 17Z"/><path d="M5 21 14 12"/>',
        'shield'    => '<path d="M12 2 4 5v6c0 5 3.5 9.5 8 11 4.5-1.5 8-6 8-11V5l-8-3Z"/><path d="m9 12 2 2 4-4"/>',
        'tools'     => '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.5-.5-.5-2.5 2.5-2.5Z"/>',
    ][$name] ?? '';
    return '<svg class="' . e($class) . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}

function site_schema(): array {
    return [
        '@context' => 'https://schema.org',
        '@graph' => [
            [
                '@type' => 'Organization', '@id' => SITE_URL . '/#org', 'name' => SITE_NAME, 'url' => SITE_URL . '/',
                'logo' => abs_url('/assets/img/icon-512.png'), 'email' => SITE_EMAIL, 'telephone' => SITE_TEL,
                'contactPoint' => ['@type' => 'ContactPoint', 'telephone' => SITE_TEL, 'email' => SITE_EMAIL, 'contactType' => 'sales', 'areaServed' => 'US'],
            ],
            [
                '@type' => 'WebSite', '@id' => SITE_URL . '/#website', 'name' => SITE_NAME, 'url' => SITE_URL . '/',
                'publisher' => ['@id' => SITE_URL . '/#org'],
            ],
        ],
    ];
}

/**
 * Print <head>, header and opening <main>.
 * $o keys (all optional; defaults come from the current route):
 *   title, description, canonical, og_image, og_type, robots,
 *   breadcrumbs  list of [label, path]; the current page goes last with path null
 *   schema       list of extra JSON-LD objects
 *   styles       extra stylesheet paths (page_end takes 'scripts' the same way)
 *   body_class
 */
function page_start(array $o = []): void {
    global $ROUTE, $PATH;
    $title = $o['title'] ?? ($ROUTE['title'] ?? SITE_NAME);
    $desc  = $o['description'] ?? ($ROUTE['description'] ?? '');
    $canon = $o['canonical'] ?? abs_url($PATH);
    $img   = $o['og_image'] ?? abs_url('/assets/img/og-image.jpg');
    $type  = $o['og_type'] ?? (in_array($ROUTE['type'] ?? '', ['guide', 'post'], true) ? 'article' : 'website');
    $robots = $o['robots'] ?? 'index,follow,max-image-preview:large';
    $crumbs = $o['breadcrumbs'] ?? null;
    $schema = $o['schema'] ?? [];

    // Guides and blog posts get Article schema automatically.
    if (in_array($ROUTE['type'] ?? '', ['guide', 'post'], true)) {
        $schema[] = [
            '@context' => 'https://schema.org', '@type' => 'Article',
            'headline' => $ROUTE['nav'] ?? $title, 'description' => $desc,
            'datePublished' => $ROUTE['date'], 'dateModified' => $ROUTE['modified'] ?? $ROUTE['date'],
            'author' => ['@type' => 'Organization', 'name' => SITE_NAME, 'url' => SITE_URL . '/about/'],
            'publisher' => ['@id' => SITE_URL . '/#org'],
            'image' => $img, 'mainEntityOfPage' => $canon,
        ];
    }
    if ($crumbs) {
        $items = [];
        foreach ($crumbs as $i => [$label, $path]) {
            $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $label, 'item' => abs_url($path ?? $PATH)];
        }
        $schema[] = ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $items];
    }
    ?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= GA_ID ?>"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '<?= GA_ID ?>');
</script>
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<meta name="robots" content="<?= e($robots) ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:type" content="<?= e($type) ?>">
<meta property="og:title" content="<?= e($title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:image" content="<?= e($img) ?>">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f5f66">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="<?= asset('/assets/css/site.css') ?>">
<?php foreach ($o['styles'] ?? [] as $css): ?><link rel="stylesheet" href="<?= asset($css) ?>">
<?php endforeach; ?>
<?= json_ld(site_schema()) ?>
<?php foreach ($schema as $s) echo json_ld($s); ?>
</head>
<body class="<?= e($o['body_class'] ?? ('t-' . ($ROUTE['type'] ?? 'page'))) ?>">
<a class="skip" href="#main">Skip to content</a>
<?php site_header(); ?>
<main id="main">
<?php if ($crumbs) breadcrumbs($crumbs);
}

function page_end(array $o = []): void {
    ?>
</main>
<?php site_footer(); ?>
<script src="<?= asset('/assets/js/site.js') ?>" defer></script>
<?php foreach ($o['scripts'] ?? [] as $js): ?>
<script src="<?= asset($js) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}

function site_header(): void {
    global $NAV, $PATH;
    ?>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="/" aria-label="<?= e(SITE_NAME) ?> home">
      <img src="/assets/img/logo.webp" width="150" height="60" alt="<?= e(SITE_NAME) ?> logo">
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><?= icon('menu', 'ico ico-open') ?><?= icon('close', 'ico ico-close') ?><span class="sr">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
      <?php foreach ($NAV as $label => $item):
          $path = is_array($item) ? $item[0] : $item;
          $kids = is_array($item) ? $item[1] : null;
          $active = ($path === '/' ? $PATH === '/' : strpos($PATH, $path) === 0) ? ' class="active"' : '';
          if ($kids && !$active) foreach ($kids as $k) if ($k === $PATH) $active = ' class="active"'; ?>
        <li<?= $kids ? ' class="has-sub"' : '' ?>>
          <a href="<?= e($path) ?>"<?= $active ?>><?= e($label) ?></a>
          <?php if ($kids): ?>
          <button class="sub-toggle" type="button" aria-expanded="false" aria-label="Open <?= e($label) ?> menu"></button>
          <ul class="sub">
            <?php foreach ($kids as $kl => $kp): ?><li><a href="<?= e($kp) ?>"><?= e($kl) ?></a></li><?php endforeach; ?>
          </ul>
          <?php endif; ?>
        </li>
      <?php endforeach; ?>
      </ul>
      <a class="btn btn-sm nav-cta" href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> <?= SITE_PHONE ?></a>
    </nav>
  </div>
</header>
<?php
}

function site_footer(): void {
    global $ROUTES;
    $col = function (string $type) use ($ROUTES) {
        foreach ($ROUTES as $p => $r) if ($r['type'] === $type) echo '<li><a href="' . e($p) . '">' . e($r['nav'] ?? $r['title']) . '</a></li>';
    };
    ?>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="/assets/img/logo.webp" width="150" height="60" alt="<?= e(SITE_NAME) ?>" loading="lazy">
      <p><?= e(SITE_NAME) ?> designs build-ready tiny house plans and free planning tools for people who want more life in less space.</p>
      <p class="footer-contact">
        <a href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> <?= SITE_PHONE ?></a>
        <a href="mailto:<?= SITE_EMAIL ?>"><?= icon('mail') ?> <?= SITE_EMAIL ?></a>
      </p>
    </div>
    <div><h2 class="footer-h">House Plans</h2><ul><li><a href="/tiny-house-plans/">All Tiny House Plans</a></li><?php $col('style'); ?></ul></div>
    <div><h2 class="footer-h">Free Tools</h2><ul><?php $col('tool'); ?></ul></div>
    <div><h2 class="footer-h">Guides</h2><ul><?php $col('guide'); ?><li><a href="/blog/"><strong>All blog posts</strong></a></li></ul></div>
    <div><h2 class="footer-h">Company</h2><ul>
      <li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li>
      <li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-conditions/">Terms &amp; Conditions</a></li><li><a href="/sitemap/">Sitemap</a></li>
    </ul></div>
  </div>
  <div class="wrap footer-base">
    <p>&copy; <?= date('Y') ?> <?= e(SITE_NAME) ?>. All rights reserved.</p>
  </div>
</footer>
<?php
}

function breadcrumbs(array $crumbs): void {
    echo '<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>';
    foreach ($crumbs as [$label, $path]) {
        echo $path === null ? '<li aria-current="page">' . e($label) . '</li>' : '<li><a href="' . e($path) . '">' . e($label) . '</a></li>';
    }
    echo '</ol></nav>';
}

// FAQ accordion plus FAQPage schema. $faqs: list of [question, answer-html].
function faq_block(array $faqs, string $heading = 'Frequently Asked Questions'): void {
    $entities = [];
    echo '<section class="faq" id="faq"><h2>' . e($heading) . '</h2>';
    foreach ($faqs as [$q, $a]) {
        echo '<details><summary>' . e($q) . '</summary><div class="faq-a">' . $a . '</div></details>';
        $entities[] = ['@type' => 'Question', 'name' => $q, 'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($a)]];
    }
    echo '</section>';
    echo json_ld(['@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $entities]);
}

function plan_card(string $slug): void {
    global $PLANS;
    $p = $PLANS[$slug];
    ?>
<article class="plan-card" data-beds="<?= $p['beds'] ?>" data-sqft="<?= $p['sqft'] ?>" data-type="<?= $p['mobile'] ? 'wheels' : 'foundation' ?>" data-loft="<?= $p['has_loft'] ? 1 : 0 ?>" data-styles="<?= e(implode(' ', $p['styles'])) ?>" data-price="<?= $p['price'] ?>">
  <a class="plan-img" href="/plans/<?= e($slug) ?>/"><img src="<?= e($p['image']) ?>" width="800" height="430" alt="<?= e($p['name'] . (isset($p['rooms']) ? ' front elevation drawing' : ' exterior rendering') . ' - ' . $p['title']) ?>" loading="lazy"></a>
  <div class="plan-body">
    <p class="plan-no"><?= e($p['name']) ?></p>
    <h3><a href="/plans/<?= e($slug) ?>/"><?= e($p['title']) ?></a></h3>
    <ul class="plan-specs">
      <li><?= icon('ruler') ?> <?= number_format($p['sqft']) ?> sq ft</li>
      <li><?= icon('bed') ?> <?= $p['beds'] ?> bed</li>
      <li><?= icon('bath') ?> <?= $p['baths'] ?> bath</li>
      <li><?= icon($p['mobile'] ? 'wheels' : 'stairs') ?> <?= $p['mobile'] ? 'On wheels' : ($p['has_loft'] ? 'Loft' : ($p['floors'] > 1 ? $p['floors'] . ' floors' : '1 level')) ?></li>
    </ul>
    <div class="plan-foot"><span class="price"><?= money($p['price']) ?></span><a class="btn btn-sm" href="/plans/<?= e($slug) ?>/">View plan</a></div>
  </div>
</article>
<?php
}

// Grid of plan cards. $slugs null = all plans. $custom adds a "custom plan" card at the end.
function plan_grid(?array $slugs = null, bool $custom = true): void {
    global $PLANS;
    echo '<div class="plan-grid">';
    foreach ($slugs ?? array_keys($PLANS) as $s) plan_card($s);
    if ($custom) { ?>
<article class="plan-card plan-custom">
  <div class="plan-body">
    <span class="link-ico"><?= icon('ruler') ?></span>
    <p class="plan-no">Custom &amp; modified plans</p>
    <h3>Need a different size or layout?</h3>
    <p class="muted">Tell us your lot size, bedroom count and style. <?= e(SITE_NAME) ?> can modify an existing plan or quote a custom tiny house design.</p>
    <div class="plan-foot"><span class="muted">Free quote</span><a class="btn btn-sm btn-wood" href="/contact/">Request a plan</a></div>
  </div>
</article>
<?php }
    echo '</div>';
}

// Plans tagged with a style slug (e.g. 'small-cabin-plans').
function plans_for_style(string $style): array {
    global $PLANS;
    return array_keys(array_filter($PLANS, fn($p) => in_array($style, $p['styles'], true)));
}

// Card grid linking to routes of one type. $exclude = path to skip, $limit = 0 for all.
function route_cards(string $type, string $exclude = '', int $limit = 0): void {
    global $ROUTES;
    $n = 0;
    echo '<div class="card-grid">';
    foreach ($ROUTES as $p => $r) {
        if ($r['type'] !== $type || $p === $exclude) continue;
        if ($limit && $n++ >= $limit) break;
        echo '<a class="link-card" href="' . e($p) . '">';
        if (!empty($r['icon'])) echo '<span class="link-ico">' . icon($r['icon']) . '</span>';
        echo '<strong>' . e($r['nav'] ?? $r['title']) . '</strong><span>' . e($r['description']) . '</span></a>';
    }
    echo '</div>';
}

// Call-to-action band.
function cta_band(string $heading = 'Ready to build your tiny home?', string $text = '', string $btn = 'Browse tiny house plans', string $href = '/tiny-house-plans/'): void {
    if ($text === '') $text = 'Talk to ' . SITE_NAME . ' about a plan, a modification or a fully custom design. We answer every message within one business day.';
    ?>
<section class="cta-band">
  <div class="wrap cta-inner">
    <div><h2><?= e($heading) ?></h2><p><?= e($text) ?></p></div>
    <div class="cta-actions">
      <a class="btn btn-light" href="<?= e($href) ?>"><?= e($btn) ?></a>
      <a class="btn btn-ghost" href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> <?= SITE_PHONE ?></a>
    </div>
  </div>
</section>
<?php
}

// Byline for guides.
function guide_byline(): void {
    global $ROUTE;
    $pub = $ROUTE['date']; $mod = $ROUTE['modified'] ?? null;
    echo '<p class="byline">By <a href="/about/">' . e(SITE_NAME) . '</a> editorial team &middot; ';
    echo $mod ? 'Updated <time datetime="' . e($mod) . '">' . date('F j, Y', strtotime($mod)) . '</time>'
              : 'Published <time datetime="' . e($pub) . '">' . date('F j, Y', strtotime($pub)) . '</time>';
    echo '</p>';
}
