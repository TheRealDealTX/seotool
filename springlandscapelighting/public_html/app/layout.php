<?php
defined('SLT') || exit;

function render_page(array $m, string $body): void {
    $title = $m['title'] ?? BRAND;
    $desc  = $m['desc'] ?? '';
    $path  = $m['path'] ?? '/';
    $canon = abs_url($path);
    $img   = abs_url('/assets/img/' . ($m['image'] ?? 'Spring-Landscape-Lighting-Site-Image.webp'));
    $type  = $m['og_type'] ?? 'website';

    $graph = [
        [
            '@type' => ['LocalBusiness', 'HomeAndConstructionBusiness'],
            '@id' => SITE_URL . '/#business',
            'name' => BRAND,
            'url' => SITE_URL . '/',
            'telephone' => PHONE_TEL,
            'email' => EMAIL,
            'logo' => abs_url('/assets/img/Spring-Landscape-Lighting-Logo.webp'),
            'image' => abs_url('/assets/img/Spring-Landscape-Lighting-Site-Image.webp'),
            'description' => 'Custom landscape lighting design, installation, repair and LED upgrades for homes in Spring, Texas and nearby North Houston communities.',
            'areaServed' => array_map(fn($a) => ['@type' => 'Place', 'name' => $a['name']], array_values(AREAS)),
            'knowsAbout' => ['Landscape lighting', 'Architectural lighting', 'Low-voltage LED lighting', 'Outdoor lighting design'],
            'hasOfferCatalog' => [
                '@type' => 'OfferCatalog', 'name' => 'Landscape lighting services',
                'itemListElement' => array_map(fn($s, $k) => ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Service', 'name' => $s['name'], 'url' => abs_url('/services/' . $k . '/')]], SERVICES, array_keys(SERVICES)),
            ],
        ],
        ['@type' => 'WebSite', '@id' => SITE_URL . '/#website', 'url' => SITE_URL . '/', 'name' => BRAND, 'publisher' => ['@id' => SITE_URL . '/#business'], 'inLanguage' => 'en-US'],
        ['@type' => $m['page_type'] ?? 'WebPage', '@id' => $canon . '#webpage', 'url' => $canon, 'name' => $title, 'description' => $desc, 'isPartOf' => ['@id' => SITE_URL . '/#website'], 'about' => ['@id' => SITE_URL . '/#business'], 'inLanguage' => 'en-US'],
    ];
    foreach ($GLOBALS['SCHEMA'] as $n) $graph[] = $n;
    if ($GLOBALS['FAQ']) $graph[] = ['@type' => 'FAQPage', '@id' => $canon . '#faq', 'mainEntity' => $GLOBALS['FAQ']];
    $ld = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
    $cur = '/' . explode('/', trim($path, '/'))[0] . '/';
    ?>
<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XTLNWBFJWH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XTLNWBFJWH');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<?php if (!empty($m['noindex'])): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<?php endif; ?>
<meta name="theme-color" content="#07100c">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($type) ?>">
<meta property="og:site_name" content="<?= e(BRAND) ?>">
<meta property="og:title" content="<?= e($m['og_title'] ?? $title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:image" content="<?= e($img) ?>">
<?php if (!empty($m['published'])): ?><meta property="article:published_time" content="<?= e($m['published']) ?>T08:00:00-05:00">
<meta property="article:modified_time" content="<?= e($m['modified'] ?? $m['published']) ?>T08:00:00-05:00">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($m['og_title'] ?? $title) ?>">
<meta name="twitter:description" content="<?= e($desc) ?>">
<meta name="twitter:image" content="<?= e($img) ?>">
<meta name="geo.region" content="US-TX"><meta name="geo.placename" content="Spring, Texas">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/webp" href="/assets/img/icon-192.webp" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="<?= e(BRAND) ?> Blog" href="<?= SITE_URL ?>/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="<?= asset('css/main.css') ?>">
<?php if (!empty($m['preload'])): ?><link rel="preload" as="image" href="<?= e($m['preload']) ?>"><?php endif; ?>
<script type="application/ld+json"><?= $ld ?></script>
</head>
<body class="<?= e($m['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<div class="cursor-glow" aria-hidden="true"></div>
<header class="hdr" data-hdr>
  <div class="wrap hdr__in">
    <a class="hdr__logo" href="/" aria-label="<?= e(BRAND) ?> home">
      <img src="/assets/img/Spring-Landscape-Lighting-Logo-White.webp" alt="<?= e(BRAND) ?>" width="600" height="142">
    </a>
    <nav class="nav" aria-label="Main">
      <ul class="nav__list">
      <?php foreach (NAV as [$label, $href, $menu]): $active = $cur === $href ? ' is-active' : ''; ?>
        <li class="nav__item<?= $menu ? ' has-menu' : '' ?>">
          <a class="nav__link<?= $active ?>" href="<?= $href ?>"><?= e($label) ?><?= $menu ? icon('chevron-down', 'nav__chev') : '' ?></a>
          <?php if ($menu === 'services'): ?>
          <div class="mega"><div class="mega__grid">
            <?php foreach (SERVICES as $k => $s): ?><a class="mega__link" href="/services/<?= $k ?>/"><?= icon($s['icon']) ?><span><strong><?= e($s['name']) ?></strong><small><?= e(mb_strimwidth($s['blurb'], 0, 74, '…')) ?></small></span></a><?php endforeach; ?>
          </div><a class="mega__all" href="/services/">All landscape lighting services <?= icon('arrow-right') ?></a></div>
          <?php elseif ($menu === 'tools'): ?>
          <div class="mega"><div class="mega__grid">
            <?php foreach (TOOLS as $k => $t): ?><a class="mega__link" href="/tools/<?= $k ?>/"><?= icon($t['icon']) ?><span><strong><?= e($t['name']) ?></strong><small><?= e(mb_strimwidth($t['desc'], 0, 74, '…')) ?></small></span></a><?php endforeach; ?>
          </div><a class="mega__all" href="/tools/">All free lighting tools <?= icon('arrow-right') ?></a></div>
          <?php elseif ($menu === 'areas'): ?>
          <div class="mega mega--sm"><div class="mega__grid mega__grid--1">
            <?php foreach (AREAS as $k => $a): ?><a class="mega__link" href="/service-areas/<?= $k ?>/"><?= icon('map-pin') ?><span><strong><?= e($a['name']) ?></strong></span></a><?php endforeach; ?>
          </div></div>
          <?php endif; ?>
        </li>
      <?php endforeach; ?>
      </ul>
    </nav>
    <div class="hdr__cta">
      <a class="hdr__phone" href="tel:<?= PHONE_TEL ?>"><?= icon('phone') ?><span><?= PHONE ?></span></a>
      <a class="btn btn--glow btn--sm" href="/quote/" data-magnetic>Free Quote</a>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer__in">
    <ul>
      <li><a href="/">Home</a></li>
      <?php foreach (NAV as [$label, $href, $menu]): ?>
      <li><a href="<?= $href ?>"><?= e($label) ?></a>
        <?php if ($menu === 'services'): ?><ul class="drawer__sub"><?php foreach (SERVICES as $k => $s): ?><li><a href="/services/<?= $k ?>/"><?= e($s['name']) ?></a></li><?php endforeach; ?></ul><?php endif; ?>
        <?php if ($menu === 'tools'): ?><ul class="drawer__sub"><?php foreach (TOOLS as $k => $t): ?><li><a href="/tools/<?= $k ?>/"><?= e($t['name']) ?></a></li><?php endforeach; ?></ul><?php endif; ?>
      </li>
      <?php endforeach; ?>
      <li><a href="/faq/">FAQ</a></li><li><a href="/contact/">Contact</a></li>
    </ul>
    <div class="drawer__cta"><a class="btn btn--glow btn--block" href="/quote/">Get a Free Lighting Plan</a><a class="btn btn--ghost btn--block" href="tel:<?= PHONE_TEL ?>"><?= icon('phone') ?><?= PHONE ?></a></div>
  </div>
</div>

<main id="main">
<?= $body ?>
</main>

<footer class="ftr">
  <div class="ftr__horizon" aria-hidden="true"></div>
  <div class="wrap">
    <div class="ftr__top">
      <div class="ftr__brand">
        <a href="/" class="ftr__logo"><img src="/assets/img/Spring-Landscape-Lighting-Logo-White.webp" alt="<?= e(BRAND) ?>" width="600" height="142" loading="lazy"></a>
        <p>Custom landscape lighting design, installation, repair and LED upgrades for homes in Spring, Texas and nearby North Houston communities.</p>
        <div class="ftr__contact">
          <a href="tel:<?= PHONE_TEL ?>"><?= icon('phone') ?><?= PHONE ?></a>
          <a href="mailto:<?= EMAIL ?>"><?= icon('mail') ?><?= EMAIL ?></a>
          <span><?= icon('map-pin') ?>Serving Spring, Klein &amp; North Houston, TX</span>
        </div>
      </div>
      <div class="ftr__col"><h4>Services</h4><ul><?php foreach (SERVICES as $k => $s): ?><li><a href="/services/<?= $k ?>/"><?= e($s['name']) ?></a></li><?php endforeach; ?></ul></div>
      <div class="ftr__col"><h4>Free Tools</h4><ul><?php foreach (TOOLS as $k => $t): ?><li><a href="/tools/<?= $k ?>/"><?= e($t['name']) ?></a></li><?php endforeach; ?></ul></div>
      <div class="ftr__col"><h4>Service Areas</h4><ul><?php foreach (AREAS as $k => $a): ?><li><a href="/service-areas/<?= $k ?>/"><?= e($a['name']) ?></a></li><?php endforeach; ?></ul></div>
      <div class="ftr__col"><h4>Company</h4><ul>
        <li><a href="/about-us/">About Us</a></li><li><a href="/our-process/">Our Process</a></li><li><a href="/inspiration/">Inspiration</a></li>
        <li><a href="/blog/">Blog</a></li><li><a href="/faq/">FAQs</a></li><li><a href="/contact/">Contact</a></li><li><a href="/quote/">Request a Quote</a></li>
      </ul></div>
    </div>
    <div class="ftr__bottom">
      <p>&copy; <?= date('Y') ?> <?= e(BRAND) ?>. All rights reserved. Outdoor lighting for Spring, TX homes.</p>
      <p><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-service/">Terms of Service</a><a href="/sitemap_index.xml">Sitemap</a></p>
    </div>
  </div>
</footer>
<a class="mobile-call" href="tel:<?= PHONE_TEL ?>" aria-label="Call <?= e(BRAND) ?>"><?= icon('phone') ?></a>
<button class="totop" type="button" aria-label="Back to top"><?= icon('arrow-up-right') ?></button>
<script src="<?= asset('js/main.js') ?>" defer></script>
<?php if (!empty($m['tools_js'])): ?><script src="<?= asset('js/tools.js') ?>" defer></script><?php endif; ?>
</body>
</html>
<?php
}
