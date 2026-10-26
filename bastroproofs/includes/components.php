<?php
/** Shared layout (head, header, footer) and reusable page sections. */

/**
 * Open the document. $p keys:
 *   title, description, path (canonical, e.g. "/services/"),
 *   schema (array of JSON-LD nodes), image (og image file), robots,
 *   body (body class), type (og:type), published (ISO date, articles).
 */
function page_start(array $p): void
{
    global $SERVICES, $AREAS, $TOOLS;
    $canonical = abs_url($p['path']);
    $ogImage   = abs_url(img($p['image'] ?? 'A-Stronger-Roof-Starts-With-a-Clear-Plan.webp'));
    $schema    = array_merge([business_schema(), website_schema()], $p['schema'] ?? []);
    $here      = current_path();
    ?>
<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= GA_ID ?>"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '<?= GA_ID ?>');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($p['title']) ?></title>
<meta name="description" content="<?= e($p['description']) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<meta name="robots" content="<?= e($p['robots'] ?? 'index, follow, max-image-preview:large') ?>">
<meta name="theme-color" content="#0a2540">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Bastrop">
<meta name="geo.position" content="<?= SITE['latitude'] ?>;<?= SITE['longitude'] ?>">
<meta property="og:type" content="<?= e($p['type'] ?? 'website') ?>">
<meta property="og:site_name" content="<?= e(SITE['name']) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="<?= e($p['title']) ?>">
<meta property="og:description" content="<?= e($p['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($ogImage) ?>">
<?php if (!empty($p['published'])): ?>
<meta property="article:published_time" content="<?= e($p['published']) ?>T08:00:00-05:00">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($p['title']) ?>">
<meta name="twitter:description" content="<?= e($p['description']) ?>">
<meta name="twitter:image" content="<?= e($ogImage) ?>">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="icon" type="image/png" href="/favicon-48x48.png" sizes="48x48">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="apple-mobile-web-app-title" content="Bastrop Roofing">
<meta name="application-name" content="Bastrop Roofing">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css?v=<?= filemtime(ROOT . '/assets/css/style.css') ?>">
<?php if (!empty($p['preload'])): ?>
<link rel="preload" as="image" href="<?= e(img($p['preload'])) ?>">
<?php endif; ?>
<?= json_ld($schema) ?>

</head>
<body class="<?= e($p['body'] ?? '') ?>">
<a class="skip-link" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span></span></div>

<div class="topbar">
  <div class="container topbar-inner">
    <span class="topbar-msg"><?= icon('pin') ?> Local roofing for Bastrop, TX &amp; Bastrop County</span>
    <span class="topbar-links">
      <a href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone') ?> <?= SITE['phone_short'] ?></a>
      <a href="mailto:<?= SITE['email'] ?>"><?= icon('mail') ?> <?= SITE['email'] ?></a>
    </span>
  </div>
</div>

<header class="site-header" id="top">
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="Bastrop Roofing home">
      <img src="<?= img('Bastrop-Roofing-Logo.webp') ?>" alt="Bastrop Roofing logo" width="210" height="47">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>
<?php foreach (NAV as $item):
        $active = $item['href'] !== '/' && str_starts_with($here, $item['href']) ? ' is-active' : '';
        $kids = match ($item['children'] ?? '') {
            'services' => array_map(fn($s, $k) => [$s['name'], "/services/$k/"], $SERVICES, array_keys($SERVICES)),
            'areas'    => array_merge([['Bastrop, TX', '/']], array_map(fn($a, $k) => [$a['name'] . ', TX', "/service-areas/$k/"], $AREAS, array_keys($AREAS))),
            'tools'    => array_map(fn($t, $k) => [$t['name'], "/roofing-tools/$k/"], $TOOLS, array_keys($TOOLS)),
            default    => [],
        };
?>
        <li class="<?= $kids ? 'has-drop' : '' ?><?= $active ?>">
          <a href="<?= $item['href'] ?>"><?= e($item['label']) ?></a>
<?php if ($kids): ?>
          <button class="drop-toggle" type="button" aria-expanded="false" aria-label="Show <?= e($item['label']) ?> menu"><?= icon('chevron') ?></button>
          <ul class="dropdown">
<?php foreach ($kids as [$label, $href]): ?>
            <li><a href="<?= $href ?>"><?= e($label) ?></a></li>
<?php endforeach; ?>
          </ul>
<?php endif; ?>
        </li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn-primary nav-cta-mobile" href="/contact/">Free Roof Estimate</a>
    </nav>
    <div class="header-actions">
      <a class="header-phone" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone') ?><span><?= SITE['phone_short'] ?></span></a>
      <a class="btn btn-primary btn-sm" href="/contact/">Free Estimate</a>
      <button class="menu-btn" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><?= icon('menu', 'icon i-open') ?><?= icon('x', 'icon i-close') ?></button>
    </div>
  </div>
</header>

<main id="main">
<?php
}

function page_end(): void
{
    global $SERVICES, $AREAS, $TOOLS;
    ?>
</main>

<footer class="site-footer">
  <div class="footer-roofline" aria-hidden="true"></div>
  <div class="container footer-grid">
    <div class="footer-brand">
      <img src="<?= img('Bastrop-Roofing-Logo-Alt.webp') ?>" alt="Bastrop Roofing" width="210" height="47" loading="lazy">
      <p>Bastrop Roofing is a local roofer serving Bastrop, TX and Bastrop County with roof repair, roof replacement, metal roofing, inspections and storm damage repair for homes and businesses.</p>
      <ul class="footer-contact">
        <li><a href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone') ?> <?= SITE['phone_display'] ?></a></li>
        <li><a href="mailto:<?= SITE['email'] ?>"><?= icon('mail') ?> <?= SITE['email'] ?></a></li>
        <li><?= icon('pin') ?> Bastrop, TX <?= SITE['zip'] ?></li>
        <li><?= icon('clock') ?> <?= SITE['hours'] ?></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-title">Roofing Services</h2>
      <ul>
<?php foreach ($SERVICES as $slug => $s): ?>
        <li><a href="/services/<?= $slug ?>/"><?= e($s['name']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2 class="footer-title">Service Areas</h2>
      <ul>
        <li><a href="/">Bastrop, TX</a></li>
<?php foreach ($AREAS as $slug => $a): ?>
        <li><a href="/service-areas/<?= $slug ?>/">Roofing <?= e($a['name']) ?>, TX</a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2 class="footer-title">Roof Tools &amp; Help</h2>
      <ul>
<?php foreach ($TOOLS as $slug => $t): ?>
        <li><a href="/roofing-tools/<?= $slug ?>/"><?= e($t['name']) ?></a></li>
<?php endforeach; ?>
        <li><a href="/blog/">Roofing Blog</a></li>
        <li><a href="/faq/">Roofing FAQ</a></li>
        <li><a href="/about/">About Us</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; <?= date('Y') ?> Bastrop Roofing. All rights reserved. Serving <?= SERVING ?>.</p>
    <p><a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms-of-use/">Terms of Use</a> · <a href="/sitemap/">Sitemap</a></p>
  </div>
</footer>

<div class="mobile-bar">
  <a href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone') ?> Call Now</a>
  <a href="/contact/" class="is-accent"><?= icon('calc') ?> Free Estimate</a>
</div>
<button class="to-top" type="button" aria-label="Back to top"><?= icon('arrow') ?></button>

<script src="/assets/js/main.js?v=<?= filemtime(ROOT . '/assets/js/main.js') ?>" defer></script>
</body>
</html>
<?php
}

/** Interior-page hero with breadcrumbs. $crumbs = [[label, path], ...] ending with the current page. */
function page_hero(string $eyebrow, string $h1, string $lead, array $crumbs, ?string $image = null, array $actions = []): void
{
    ?>
<section class="page-hero<?= $image ? ' has-image' : '' ?>">
<?php if ($image): ?>
  <img class="page-hero-bg" src="<?= img($image) ?>" alt="" width="1200" height="655" fetchpriority="high">
<?php endif; ?>
  <canvas class="weather-canvas" data-weather="rain" aria-hidden="true"></canvas>
  <div class="container page-hero-inner">
    <nav class="breadcrumbs" aria-label="Breadcrumb">
      <ol>
<?php foreach ($crumbs as $i => [$label, $path]): ?>
<?php if ($i === count($crumbs) - 1): ?>
        <li aria-current="page"><?= e($label) ?></li>
<?php else: ?>
        <li><a href="<?= $path ?>"><?= e($label) ?></a></li>
<?php endif; ?>
<?php endforeach; ?>
      </ol>
    </nav>
    <span class="eyebrow eyebrow-light"><?= e($eyebrow) ?></span>
    <h1><?= e($h1) ?></h1>
    <p class="page-hero-lead"><?= e($lead) ?></p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone') ?> Call <?= SITE['phone_short'] ?></a>
      <?php foreach ($actions as [$label, $href]): ?><a class="btn btn-outline" href="<?= $href ?>"><?= e($label) ?> <?= icon('arrow') ?></a><?php endforeach; ?>
      <?php if (!$actions): ?><a class="btn btn-outline" href="/contact/">Request an Estimate <?= icon('arrow') ?></a><?php endif; ?>
    </div>
  </div>
  <div class="hero-shingles" aria-hidden="true"></div>
</section>
<?php
}

function faq_block(array $faqs, string $title = 'Frequently Asked Questions', string $eyebrow = 'FAQ'): void
{
    ?>
<section class="section faq-section">
  <div class="container narrow">
    <div class="section-head center reveal">
      <span class="eyebrow"><?= e($eyebrow) ?></span>
      <h2 class="section-title"><?= e($title) ?></h2>
    </div>
    <div class="faq-list">
<?php foreach ($faqs as $f): ?>
      <details class="faq-item reveal">
        <summary><?= e($f['q']) ?><span class="faq-icon" aria-hidden="true"></span></summary>
        <div class="faq-answer"><p><?= e($f['a']) ?></p></div>
      </details>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php
}

function cta_band(string $title = 'Talk With a Bastrop Roofer Today', string $text = 'Tell us what you are seeing on your roof. We will inspect it, explain what we find in plain language, and give you a clear written estimate.'): void
{
    ?>
<section class="cta-band">
  <canvas class="weather-canvas" data-weather="rain" aria-hidden="true"></canvas>
  <div class="container cta-inner reveal">
    <div>
      <h2><?= e($title) ?></h2>
      <p><?= e($text) ?></p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-primary btn-lg" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone') ?> <?= SITE['phone_short'] ?></a>
      <a class="btn btn-outline btn-lg" href="/contact/">Get a Free Estimate</a>
    </div>
  </div>
</section>
<?php
}

/** The estimate form. Posts to /contact/send.php (PHP mail handler). */
function estimate_form(string $context = ''): void
{
    global $SERVICES;
    $sent = $_GET['sent'] ?? '';
    ?>
<form class="estimate-form" action="/contact/send.php" method="post" novalidate>
<?php if ($sent === '1'): ?>
  <div class="form-alert is-success" role="status"><?= icon('check') ?> Thanks — your request was sent. A Bastrop Roofing team member will call you shortly.</div>
<?php elseif ($sent === '0'): ?>
  <div class="form-alert is-error" role="alert">Something went wrong sending your request. Please call <?= SITE['phone_short'] ?> or email <?= SITE['email'] ?>.</div>
<?php endif; ?>
  <input type="hidden" name="context" value="<?= e($context) ?>">
  <div class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <div class="form-row">
    <label>Full name<input type="text" name="name" required autocomplete="name" placeholder="Jane Smith"></label>
    <label>Phone<input type="tel" name="phone" required autocomplete="tel" placeholder="(512) 555-0123"></label>
  </div>
  <div class="form-row">
    <label>Email<input type="email" name="email" autocomplete="email" placeholder="you@example.com"></label>
    <label>Property address or ZIP<input type="text" name="address" autocomplete="street-address" placeholder="Bastrop, TX 78602"></label>
  </div>
  <label>What do you need?
    <select name="service">
      <option value="">Choose a service…</option>
<?php foreach ($SERVICES as $s): ?>
      <option><?= e($s['name']) ?></option>
<?php endforeach; ?>
      <option>Not sure — need an inspection</option>
    </select>
  </label>
  <label>Tell us about the roof<textarea name="message" rows="4" placeholder="Leak over the kitchen after last week's storm, roof is about 15 years old…"></textarea></label>
  <button class="btn btn-primary btn-block" type="submit">Send My Estimate Request <?= icon('arrow') ?></button>
  <p class="form-note"><?= icon('shield') ?> No obligation. We never share your information.</p>
</form>
<?php
}

function service_cards(array $only = []): void
{
    global $SERVICES;
    $i = 0;
    foreach ($SERVICES as $slug => $s) {
        if ($only && !in_array($slug, $only, true)) continue;
        $i++;
        ?>
    <a class="service-card reveal" href="/services/<?= $slug ?>/" style="--d:<?= ($i % 4) * 70 ?>ms">
      <span class="service-icon"><?= icon($s['icon']) ?></span>
      <h3><?= e($s['name']) ?></h3>
      <p><?= e($s['card']) ?></p>
      <span class="card-link">Learn more <?= icon('arrow') ?></span>
    </a>
<?php
    }
}

function tool_cards(array $skip = []): void
{
    global $TOOLS;
    foreach ($TOOLS as $slug => $t) {
        if (in_array($slug, $skip, true)) continue;
        ?>
    <a class="tool-card reveal" href="/roofing-tools/<?= $slug ?>/">
      <span class="tool-icon"><?= icon($t['icon']) ?></span>
      <span><strong><?= e($t['name']) ?></strong><small><?= e($t['card']) ?></small></span>
      <?= icon('arrow', 'icon tool-arrow') ?>
    </a>
<?php
    }
}

/** Prose + sticky sidebar wrapper used by service, area and legal pages. */
function sidebar(string $heading = 'Get a Free Roof Estimate'): void
{
    global $TOOLS;
    ?>
<aside class="sidebar">
  <div class="side-card side-cta">
    <h2><?= e($heading) ?></h2>
    <p>Same-week inspections across Bastrop County. Storm calls answered 24/7.</p>
    <a class="btn btn-primary btn-block" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone') ?> <?= SITE['phone_short'] ?></a>
    <a class="btn btn-dark btn-block" href="/contact/">Request Online</a>
  </div>
  <div class="side-card">
    <h2>Free Roof Tools</h2>
    <ul class="side-links">
<?php foreach ($TOOLS as $slug => $t): ?>
      <li><a href="/roofing-tools/<?= $slug ?>/"><?= icon($t['icon']) ?> <?= e($t['name']) ?></a></li>
<?php endforeach; ?>
    </ul>
  </div>
</aside>
<?php
}
