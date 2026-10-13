<?php
/**
 * Shared layout: <head>, header, footer, lead popup and reusable components.
 *
 * Usage in a page:
 *   require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';
 *   page_start([...]);  ...page HTML...  page_end();
 */

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/posts.php';

const ASSET_VER = '20261013';

/** Base JSON-LD nodes shared by every page. */
function base_schema(): array
{
    $o = SITE['origin'];
    return [
        [
            '@type' => 'WebSite',
            '@id' => $o . '/#website',
            'url' => $o . '/',
            'name' => SITE['name'],
            'publisher' => ['@id' => $o . '/#business'],
            'inLanguage' => 'en-US',
        ],
        [
            '@type' => ['ProfessionalService', 'LocalBusiness'],
            '@id' => $o . '/#business',
            'name' => SITE['name'],
            'alternateName' => ['Sugar Land Public Adjusters', 'Public Adjuster Sugar Land'],
            'description' => 'Sugar Land Public Adjuster is a licensed public adjuster in Sugar Land, TX representing homeowners and business owners—not insurance companies—on hurricane, hail, wind, water, flood and fire insurance claims.',
            'url' => $o . '/',
            'telephone' => SITE['phone_href'],
            'email' => SITE['email'],
            'logo' => abs_url(SITE['logo']),
            'image' => abs_url(SITE['og_image']),
            'address' => [
                '@type' => 'PostalAddress',
                'addressLocality' => 'Sugar Land',
                'addressRegion' => 'TX',
                'addressCountry' => 'US',
            ],
            'geo' => ['@type' => 'GeoCoordinates', 'latitude' => SITE['lat'], 'longitude' => SITE['lng']],
            'areaServed' => array_map(fn($c) => ['@type' => 'City', 'name' => $c . ', TX'],
                ['Sugar Land', 'Missouri City', 'Stafford', 'Richmond', 'Rosenberg', 'Fulshear', 'Katy', 'Pearland', 'Houston']),
            'knowsAbout' => ['Public adjusting', 'Property insurance claims', 'Hurricane damage claims', 'Hail damage claims', 'Water damage claims', 'Fire damage claims', 'Flood insurance claims', 'Commercial property claims'],
            'employee' => ['@id' => $o . '/#joseph-dittman'],
            'parentOrganization' => ['@type' => 'Organization', 'name' => SITE['firm'], 'url' => 'https://txpublicadjusting.com/'],
            'contactPoint' => [
                '@type' => 'ContactPoint',
                'telephone' => SITE['phone_href'],
                'email' => SITE['email'],
                'contactType' => 'customer service',
                'areaServed' => 'US-TX',
                'availableLanguage' => 'English',
            ],
        ],
        [
            '@type' => 'Person',
            '@id' => $o . '/#joseph-dittman',
            'name' => AUTHOR['name'],
            'jobTitle' => AUTHOR['title'],
            'url' => $o . AUTHOR['url'],
            'image' => abs_url(AUTHOR['image']),
            'description' => AUTHOR['short'],
            'worksFor' => ['@id' => $o . '/#business'],
            'knowsAbout' => ['Texas property insurance claims', 'Public adjusting', 'Xactimate estimating', 'Storm damage claims'],
            'sameAs' => AUTHOR['sameAs'],
        ],
    ];
}

function page_start(array $m): void
{
    $o = SITE['origin'];
    $path = $m['path'] ?? '/';
    $canonical = $o . $path;
    $title = $m['title'];
    $desc = $m['description'];
    $image = abs_url($m['image'] ?? SITE['og_image']);
    $type = $m['type'] ?? 'website';
    $crumbs = $m['breadcrumbs'] ?? null;

    $graph = base_schema();
    $webpage = [
        '@type' => $m['page_type'] ?? 'WebPage',
        '@id' => $canonical . '#webpage',
        'url' => $canonical,
        'name' => $title,
        'description' => $desc,
        'isPartOf' => ['@id' => $o . '/#website'],
        'about' => ['@id' => $o . '/#business'],
        'primaryImageOfPage' => ['@type' => 'ImageObject', 'url' => $image],
        'inLanguage' => 'en-US',
    ];
    if (!empty($m['main_entity'])) {
        $webpage['mainEntity'] = ['@id' => $m['main_entity']];
    }
    if (!empty($m['modified'])) {
        $webpage['dateModified'] = $m['modified'];
    }
    if ($crumbs) {
        $items = [];
        $i = 1;
        foreach ($crumbs as [$name, $href]) {
            $items[] = ['@type' => 'ListItem', 'position' => $i++, 'name' => $name, 'item' => $o . $href];
        }
        $graph[] = ['@type' => 'BreadcrumbList', '@id' => $canonical . '#breadcrumb', 'itemListElement' => $items];
        $webpage['breadcrumb'] = ['@id' => $canonical . '#breadcrumb'];
    }
    $graph[] = $webpage;
    foreach ($m['schema'] ?? [] as $node) {
        $graph[] = $node;
    }
    $ld = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
    $bodyClass = $m['body_class'] ?? '';
    ?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<meta name="robots" content="<?= e($m['robots'] ?? 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1') ?>">
<meta name="author" content="<?= e($m['author'] ?? SITE['name']) ?>">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Sugar Land, Texas">
<meta name="geo.position" content="<?= SITE['lat'] ?>;<?= SITE['lng'] ?>">
<meta name="ICBM" content="<?= SITE['lat'] ?>, <?= SITE['lng'] ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($type) ?>">
<meta property="og:title" content="<?= e($m['og_title'] ?? $title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:site_name" content="<?= e(SITE['name']) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<?php if ($type === 'article'): ?>
<meta property="article:published_time" content="<?= e($m['published']) ?>">
<meta property="article:modified_time" content="<?= e($m['modified'] ?? $m['published']) ?>">
<meta property="article:author" content="<?= e($o . AUTHOR['url']) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($m['og_title'] ?? $title) ?>">
<meta name="twitter:description" content="<?= e($desc) ?>">
<meta name="twitter:image" content="<?= e($image) ?>">
<meta name="theme-color" content="#2E073F">
<link rel="icon" href="/wp-content/uploads/2026/02/cropped-Sugar-Land-Public-Adjuster-Site-Icon-32x32.webp" sizes="32x32">
<link rel="icon" href="/wp-content/uploads/2026/02/cropped-Sugar-Land-Public-Adjuster-Site-Icon-192x192.webp" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&family=Roboto+Slab:wght@500;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= ASSET_VER ?>">
<?php if (!empty($m['preload'])): ?>
<link rel="preload" as="image" href="<?= e($m['preload']) ?>" fetchpriority="high">
<?php endif; ?>
<script type="application/ld+json"><?= $ld ?></script>
<?= $m['head_extra'] ?? '' ?>
</head>
<body class="<?= e($bodyClass) ?>">
<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container topbar-inner">
    <span class="topbar-note">Licensed public adjusters for Sugar Land &amp; Fort Bend County policyholders</span>
    <span class="topbar-links">
      <a href="tel:<?= SITE['phone_href'] ?>"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>Call <?= e(SITE['phone_display']) ?></a>
      <a href="sms:<?= SITE['phone_href'] ?>"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2z"/></svg>Text Us</a>
      <a href="mailto:<?= e(SITE['email']) ?>" class="hide-sm"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/></svg><?= e(SITE['email']) ?></a>
    </span>
  </div>
</div>
<header class="site-header" id="top">
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="<?= e(SITE['name']) ?> home">
      <img src="<?= e(SITE['logo']) ?>" alt="Sugar Land Public Adjuster logo" width="300" height="54">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
<?php $cur = $path; foreach (NAV as [$label, $href, $kids]):
    $active = ($href === '/' ? $cur === '/' : strpos($cur, $href) === 0);
    if (!$active && $kids) { foreach ($kids as [, $kh]) { if ($kh !== '/' && strpos($cur, $kh) === 0) { $active = true; } } }
?>
        <li class="<?= $kids ? 'has-sub' : '' ?><?= $active ? ' active' : '' ?>">
          <a href="<?= e($href) ?>"<?= $active ? ' aria-current="page"' : '' ?>><?= e($label) ?></a>
<?php if ($kids): ?>
          <button class="sub-toggle" aria-label="Show <?= e($label) ?> menu" aria-expanded="false"></button>
          <ul class="sub">
<?php foreach ($kids as [$kl, $kh]): ?>
            <li><a href="<?= e($kh) ?>"><?= e($kl) ?></a></li>
<?php endforeach; ?>
          </ul>
<?php endif; ?>
        </li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn-primary nav-cta" href="tel:<?= SITE['phone_href'] ?>"><?= e(SITE['phone_display']) ?></a>
    </nav>
  </div>
</header>
<main id="main">
<?php
}

function page_end(array $opts = []): void
{
    $year = date('Y');
    if (empty($opts['no_cta'])) {
        cta_band();
    }
    ?>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-about">
      <a href="/"><img src="<?= e(SITE['logo_white']) ?>" alt="Sugar Land Public Adjuster logo in white" width="300" height="54" loading="lazy"></a>
      <p>Sugar Land Public Adjuster helps homeowners and businesses across Sugar Land navigate insurance claims after property damage. Our licensed public adjusters work on your behalf to document losses, challenge low settlements, and pursue the full compensation your policy allows.</p>
      <p class="license">Texas public adjusting firm: <?= e(SITE['firm']) ?> &middot; License #<?= e(SITE['firm_license']) ?></p>
    </div>
    <div>
      <h2 class="footer-h">Claim Services</h2>
      <ul>
        <li><a href="/services/hurricane-wind-damage-claims/">Hurricane &amp; Wind Claims</a></li>
        <li><a href="/services/hail-damage-claims/">Hail Damage Claims</a></li>
        <li><a href="/services/water-damage-claims/">Water Damage Claims</a></li>
        <li><a href="/services/fire-smoke-damage-claims/">Fire &amp; Smoke Claims</a></li>
        <li><a href="/services/flood-damage-claims/">Flood Claims</a></li>
        <li><a href="/services/commercial-property-claims/">Commercial Claims</a></li>
        <li><a href="/services/denied-underpaid-claims/">Denied &amp; Underpaid Claims</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Tools &amp; Resources</h2>
      <ul>
        <li><a href="/tools/insurance-claim-settlement-calculator/">Settlement Calculator</a></li>
        <li><a href="/tools/depreciation-calculator/">Depreciation Calculator</a></li>
        <li><a href="/tools/public-adjuster-fee-calculator/">Fee Calculator</a></li>
        <li><a href="/tools/claim-deadline-calculator/">Claim Deadline Calculator</a></li>
        <li><a href="/sugar-land-weather/">Live Sugar Land Weather</a></li>
        <li><a href="/sugar-land-storm-history/">Sugar Land Storm History</a></li>
        <li><a href="/faq/">Public Adjuster FAQ</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Contact</h2>
      <ul class="footer-contact">
        <li>Serving Sugar Land, Fort Bend County &amp; surrounding areas</li>
        <li>Call: <?= tel_link() ?></li>
        <li>Text: <?= sms_link(SITE['phone_display']) ?></li>
        <li><a href="mailto:<?= e(SITE['email']) ?>"><?= e(SITE['email']) ?></a></li>
      </ul>
      <a class="btn btn-light" href="/contact/">Free Claim Review</a>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; <?= $year ?> <?= e(SITE['name']) ?>. All rights reserved. We are public adjusters, not attorneys; nothing on this site is legal advice.</p>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about-us/">About Us</a></li>
      <li><a href="/services/">Services</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/contact/">Contact</a></li>
      <li><a href="/privacy-policy/">Privacy Policy</a></li>
      <li><a href="/terms-of-use/">Terms of Use</a></li>
      <li><a href="/sitemap/">Sitemap</a></li>
    </ul>
  </div>
</footer>

<div class="mobile-bar" aria-label="Quick contact">
  <a href="tel:<?= SITE['phone_href'] ?>" class="mb-call">Call Now</a>
  <a href="sms:<?= SITE['phone_href'] ?>" class="mb-text">Text Us</a>
  <button type="button" class="mb-form" data-open-popup>Free Review</button>
</div>

<?php if (empty($opts['no_popup'])): ?>
<div class="popup" id="lead-popup" role="dialog" aria-modal="true" aria-labelledby="popup-title" hidden>
  <div class="popup-backdrop" data-close-popup></div>
  <div class="popup-card">
    <button type="button" class="popup-close" data-close-popup aria-label="Close">&times;</button>
    <div class="popup-head">
      <p class="eyebrow">Free, no-obligation claim review</p>
      <h2 id="popup-title">Was your claim denied, delayed or underpaid?</h2>
      <p>Tell a Sugar Land public adjuster what happened. We'll review it and call you back—no upfront fees.</p>
    </div>
    <?php lead_form('popup', 'Popup'); ?>
    <p class="popup-alt">Prefer to talk now? <?= tel_link('Call') ?> or <?= sms_link('text') ?> <?= e(SITE['phone_display']) ?></p>
  </div>
</div>
<?php endif; ?>
<script src="/assets/js/site.js?v=<?= ASSET_VER ?>" defer></script>
<?= $opts['scripts'] ?? '' ?>
</body>
</html>
<?php
}

/** Lead form. Posts to /lead.php (JSON via fetch, or a normal POST that redirects to /thank-you/). */
function lead_form(string $id, string $source, bool $full = false): void
{
    $t = time();
    ?>
<form class="lead-form<?= $full ? ' lead-form-full' : '' ?>" action="/lead.php" method="post" data-lead-form>
  <input type="hidden" name="source" value="<?= e($source) ?>">
  <input type="hidden" name="page" value="<?= e(current_path()) ?>">
  <input type="hidden" name="ts" value="<?= $t ?>">
  <div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <div class="field-row">
    <label class="field"><span>Full name *</span><input type="text" name="name" required autocomplete="name" maxlength="100"></label>
    <label class="field"><span>Phone *</span><input type="tel" name="phone" required autocomplete="tel" maxlength="40" inputmode="tel"></label>
  </div>
  <div class="field-row">
    <label class="field"><span>Email</span><input type="email" name="email" autocomplete="email" maxlength="150"></label>
    <label class="field"><span>Type of damage</span>
      <select name="damage">
        <option value="">Select one…</option>
<?php foreach (DAMAGE_TYPES as $d): ?>
        <option><?= e($d) ?></option>
<?php endforeach; ?>
      </select>
    </label>
  </div>
<?php if ($full): ?>
  <div class="field-row">
    <label class="field"><span>Property address or ZIP</span><input type="text" name="address" autocomplete="street-address" maxlength="200"></label>
    <label class="field"><span>Claim status</span>
      <select name="status">
        <option value="">Select one…</option>
        <option>Haven't filed yet</option>
        <option>Filed — waiting on insurer</option>
        <option>Offer received — seems low</option>
        <option>Claim denied</option>
        <option>Claim closed / paid — want a second look</option>
      </select>
    </label>
  </div>
<?php endif; ?>
  <label class="field"><span>What happened?</span><textarea name="message" rows="<?= $full ? 5 : 3 ?>" maxlength="3000" placeholder="e.g. Hail damaged our roof in May; insurer paid for a repair, contractor says it needs replacement."></textarea></label>
  <label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted by phone, text or email about my claim.</label>
  <button type="submit" class="btn btn-primary btn-block">Get My Free Claim Review</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>
<?php
}

function cta_band(): void
{
    ?>
<section class="cta-band">
  <div class="container cta-inner">
    <div>
      <h2>Property damage? The clock is already ticking.</h2>
      <p>Start with a free consultation and protect your claim before mistakes cost you money.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-light" href="tel:<?= SITE['phone_href'] ?>">Call: <?= e(SITE['phone_display']) ?></a>
      <a class="btn btn-outline-light" href="sms:<?= SITE['phone_href'] ?>">Text Us</a>
    </div>
  </div>
</section>
<?php
}

/** Interior page hero with breadcrumbs. */
function page_hero(string $h1, string $lead = '', array $crumbs = [], string $eyebrow = ''): void
{
    ?>
<section class="page-hero">
  <div class="container">
<?php if ($crumbs) breadcrumb_nav($crumbs); ?>
<?php if ($eyebrow): ?>    <p class="eyebrow"><?= e($eyebrow) ?></p>
<?php endif; ?>
    <h1><?= $h1 ?></h1>
<?php if ($lead): ?>    <p class="lead"><?= $lead ?></p>
<?php endif; ?>
  </div>
</section>
<?php
}

function breadcrumb_nav(array $crumbs): void
{
    echo '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>';
    $n = count($crumbs);
    foreach ($crumbs as $i => [$name, $href]) {
        if ($i === $n - 1) {
            echo '<li aria-current="page">' . e($name) . '</li>';
        } else {
            echo '<li><a href="' . e($href) . '">' . e($name) . '</a></li>';
        }
    }
    echo '</ol></nav>';
}

function author_box(): void
{
    ?>
<aside class="author-box">
  <img src="<?= e(AUTHOR['image']) ?>" alt="Joseph Dittman, licensed Texas public adjuster" width="120" height="120" loading="lazy">
  <div>
    <p class="eyebrow">About the author</p>
    <p class="author-name"><a href="<?= e(AUTHOR['url']) ?>"><?= e(AUTHOR['name']) ?></a> &middot; <?= e(AUTHOR['title']) ?></p>
    <p><?= e(AUTHOR['short']) ?></p>
    <p class="author-links"><a href="<?= e(AUTHOR['url']) ?>">More from Joseph</a> &middot; <?= tel_link('Call ' . SITE['phone_display']) ?></p>
  </div>
</aside>
<?php
}

function post_card(array $p): void
{
    ?>
<article class="post-card">
  <a href="/<?= e($p['slug']) ?>/" class="post-card-img"><img src="<?= e($p['thumb']) ?>" alt="<?= e($p['title']) ?>" width="300" height="200" loading="lazy"></a>
  <div class="post-card-body">
    <p class="post-meta"><time datetime="<?= e(substr($p['date'], 0, 10)) ?>"><?= e(date('F j, Y', strtotime($p['date']))) ?></time> &middot; By <?= e(AUTHOR['name']) ?></p>
    <h3><a href="/<?= e($p['slug']) ?>/"><?= e($p['title']) ?></a></h3>
    <p><?= e($p['excerpt']) ?></p>
    <a class="read-more" href="/<?= e($p['slug']) ?>/" aria-label="Read <?= e($p['title']) ?>">Read article &rarr;</a>
  </div>
</article>
<?php
}

/** Build an FAQPage schema node from [[q, a_html], ...]. */
function faq_schema(array $faqs, string $path): array
{
    return [
        '@type' => 'FAQPage',
        '@id' => SITE['origin'] . $path . '#faq',
        'mainEntity' => array_map(fn($f) => [
            '@type' => 'Question',
            'name' => $f[0],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => trim(strip_tags($f[1]))],
        ], $faqs),
    ];
}

function faq_list(array $faqs, bool $openFirst = false): void
{
    echo '<div class="faq-list">';
    foreach ($faqs as $i => [$q, $a]) {
        echo '<details class="faq-item"' . ($openFirst && $i === 0 ? ' open' : '') . '><summary>' . e($q) . '</summary><div>' . $a . '</div></details>';
    }
    echo '</div>';
}

/** Service schema node. */
function service_schema(string $name, string $desc, string $path): array
{
    return [
        '@type' => 'Service',
        '@id' => SITE['origin'] . $path . '#service',
        'name' => $name,
        'serviceType' => 'Public adjusting',
        'description' => $desc,
        'provider' => ['@id' => SITE['origin'] . '/#business'],
        'areaServed' => ['@type' => 'City', 'name' => 'Sugar Land, TX'],
        'url' => SITE['origin'] . $path,
    ];
}

/** Sidebar used on service and tool pages. */
function sidebar_cta(): void
{
    ?>
<aside class="sidebar">
  <div class="side-card side-card-dark">
    <h2>Free Claim Review</h2>
    <p>Talk with a licensed public adjuster in Sugar Land. No upfront fees—and in Texas, public adjuster fees are capped by law.</p>
    <a class="btn btn-light btn-block" href="tel:<?= SITE['phone_href'] ?>">Call <?= e(SITE['phone_display']) ?></a>
    <a class="btn btn-outline-light btn-block" href="sms:<?= SITE['phone_href'] ?>">Text Us</a>
    <button type="button" class="btn btn-accent btn-block" data-open-popup>Request a Callback</button>
  </div>
  <div class="side-card">
    <h2>Claim Tools</h2>
    <ul class="side-links">
      <li><a href="/tools/insurance-claim-settlement-calculator/">Claim settlement calculator</a></li>
      <li><a href="/tools/depreciation-calculator/">Depreciation (ACV) calculator</a></li>
      <li><a href="/tools/hurricane-deductible-calculator/">Hurricane deductible calculator</a></li>
      <li><a href="/tools/claim-deadline-calculator/">Texas claim deadline calculator</a></li>
      <li><a href="/sugar-land-weather/">Live Sugar Land weather &amp; alerts</a></li>
    </ul>
  </div>
  <div class="side-card side-author">
    <img src="<?= e(AUTHOR['image']) ?>" alt="Joseph Dittman, public adjuster" width="88" height="88" loading="lazy">
    <p><strong><a href="<?= e(AUTHOR['url']) ?>"><?= e(AUTHOR['name']) ?></a></strong><br><?= e(AUTHOR['title']) ?></p>
  </div>
</aside>
<?php
}
