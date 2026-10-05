<?php
/**
 * Page shell: <head>, header, footer, scripts. render_page($page, $content).
 *
 * $page keys: title, description, path, (optional) image, og_type, robots,
 * schema (array of JSON-LD nodes), active (nav path), body_class, nav_dark.
 */
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

/** Google tag (gtag.js) emitted in the <head> of every page and post. */
const GTAG_SNIPPET = <<<'HTML'
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5E1J8F43T7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-5E1J8F43T7');
</script>

HTML;

function render_page(array $page, string $content): void
{
    $title = $page['title'];
    if (!str_contains($title, SITE_NAME) && empty($page['title_raw'])) {
        $title .= ' | ' . SITE_NAME;
    }
    $canonical = url($page['path']);
    $ogImage = url(!empty($page['image']) ? img($page['image']) : '/assets/img/brand/austin-landscape-lighting-site-image.webp');
    $robots = $page['robots'] ?? 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1';
    $graph = array_merge([schema_org(), schema_website()], $page['schema'] ?? []);
    $jsonld = schema_encode($graph);
    $bodyClass = e($page['body_class'] ?? '');
    $ogType = e($page['og_type'] ?? 'website');
    $articleMeta = '';
    if (!empty($page['published'])) {
        $articleMeta = '<meta property="article:published_time" content="' . e($page['published']) . '">' . "\n"
            . '<meta property="article:modified_time" content="' . e($page['modified'] ?? $page['published']) . '">' . "\n";
    }

    header('Content-Type: text/html; charset=utf-8');
    echo '<!DOCTYPE html>' . "\n";
    echo '<html lang="en-US">' . "\n<head>\n";
    echo '<meta charset="utf-8">' . "\n";
    echo '<meta name="viewport" content="width=device-width, initial-scale=1">' . "\n";
    echo '<title>' . e($title) . '</title>' . "\n";
    echo '<meta name="description" content="' . e($page['description']) . '">' . "\n";
    echo '<link rel="canonical" href="' . e($canonical) . '">' . "\n";
    echo '<meta name="robots" content="' . e($robots) . '">' . "\n";
    echo '<meta name="theme-color" content="#070b14">' . "\n";
    echo GTAG_SNIPPET;
    echo '<meta property="og:locale" content="en_US">' . "\n";
    echo '<meta property="og:type" content="' . $ogType . '">' . "\n";
    echo '<meta property="og:site_name" content="' . e(SITE_NAME) . '">' . "\n";
    echo '<meta property="og:title" content="' . e($title) . '">' . "\n";
    echo '<meta property="og:description" content="' . e($page['description']) . '">' . "\n";
    echo '<meta property="og:url" content="' . e($canonical) . '">' . "\n";
    echo '<meta property="og:image" content="' . e($ogImage) . '">' . "\n";
    echo $articleMeta;
    echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
    echo '<meta name="twitter:title" content="' . e($title) . '">' . "\n";
    echo '<meta name="twitter:description" content="' . e($page['description']) . '">' . "\n";
    echo '<meta name="twitter:image" content="' . e($ogImage) . '">' . "\n";
    echo '<link rel="icon" href="/favicon.ico" sizes="32x32">' . "\n";
    echo '<link rel="icon" href="/favicon.svg" type="image/svg+xml">' . "\n";
    echo '<link rel="apple-touch-icon" href="/apple-touch-icon.png">' . "\n";
    echo '<link rel="manifest" href="/site.webmanifest">' . "\n";
    echo '<link rel="preconnect" href="https://fonts.googleapis.com">' . "\n";
    echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
    echo '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Manrope:wght@400;500;600;700;800&display=swap">' . "\n";
    echo '<link rel="stylesheet" href="/assets/css/site.css?v=' . ASSET_VERSION . '">' . "\n";
    echo '<script type="application/ld+json">' . $jsonld . '</script>' . "\n";
    echo "</head>\n";
    echo '<body class="' . $bodyClass . '">' . "\n";
    echo '<a class="skip" href="#main">Skip to content</a>' . "\n";
    echo '<div class="progress" aria-hidden="true"><span data-progress></span></div>' . "\n";
    echo site_header($page['active'] ?? null);
    echo '<main id="main">' . "\n" . $content . "\n</main>\n";
    echo site_footer();
    echo '<a class="to-top" href="#top" aria-label="Back to top" data-totop>' . icon('chevron') . '</a>' . "\n";
    echo '<script src="/assets/js/site.js?v=' . ASSET_VERSION . '" defer></script>' . "\n";
    if (!empty($page['tools_js'])) {
        echo '<script src="/assets/js/tools.js?v=' . ASSET_VERSION . '" defer></script>' . "\n";
    }
    echo "</body>\n</html>\n";
}

function site_header(?string $active): string
{
    $links = '';
    foreach (NAV as [$label, $path]) {
        $is = $active !== null && str_starts_with($active, $path) ? ' aria-current="page"' : '';
        $links .= '<li><a href="' . e($path) . '"' . $is . '>' . e($label) . '</a></li>';
    }
    $phone = e(BIZ['phone_display']);
    $tel = BIZ['phone_href'];
    $logo = '/assets/img/brand/austin-landscape-lighting-logo.webp';
    return str_replace(['{pin}', '{clock}', '{hours}', '{phone_i}', '{menu}', '{close}'], [icon('pin', 'ico ico--sm'), icon('clock', 'ico ico--sm'), e(BIZ['hours']), icon('phone', 'ico ico--sm'), icon('menu', 'ico menu-btn__open'), icon('close', 'ico menu-btn__close')], <<<HTML
<header class="site-header" id="top" data-header>
  <div class="topbar">
    <div class="container topbar__inner">
      <span>{pin} Austin, TX · Serving the greater Austin metro</span>
      <span>{clock} {hours}</span>
      <a href="{$tel}">{phone_i} {$phone}</a>
    </div>
  </div>
  <div class="container nav">
    <a class="brand" href="/" aria-label="Austin Landscape Lighting home">
      <img src="{$logo}" alt="Austin Landscape Lighting logo" width="250" height="41" decoding="async">
    </a>
    <nav class="nav__links" aria-label="Primary" data-nav>
      <ul>{$links}</ul>
      <div class="nav__mobile-cta">
        <a class="btn btn--primary" href="/contact/">Get a Free Estimate</a>
        <a class="btn btn--ghost" href="{$tel}">{phone_i} {$phone}</a>
      </div>
    </nav>
    <div class="nav__actions">
      <button class="lights-toggle" type="button" data-lights-toggle aria-pressed="false" title="Flip the switch">
        <span class="lights-toggle__track"><span class="lights-toggle__knob"></span></span>
        <span class="lights-toggle__label">Lights</span>
      </button>
      <a class="btn btn--primary nav__cta" href="/contact/">Free Estimate</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Open navigation" data-menu>{menu}{close}</button>
    </div>
  </div>
</header>
HTML);
}

function site_footer(): string
{
    $svc = '';
    foreach (services() as $s) {
        $svc .= '<li><a href="' . e($s['path']) . '">' . e($s['name']) . '</a></li>';
    }
    $ar = '';
    foreach (areas() as $a) {
        $ar .= '<li><a href="' . e($a['path']) . '">' . e($a['city']) . ', TX</a></li>';
    }
    $tl = '';
    foreach (tools() as $t) {
        $tl .= '<li><a href="' . e($t['path']) . '">' . e($t['name']) . '</a></li>';
    }
    $year = year();
    $phone = e(BIZ['phone_display']);
    $tel = BIZ['phone_href'];
    $email = e(BIZ['email']);
    $hours = e(BIZ['hours']);
    return str_replace(['{phone_i}', '{mail_i}', '{clock_i}', '{pin_i}'], [icon('phone', 'ico ico--sm'), icon('mail', 'ico ico--sm'), icon('clock', 'ico ico--sm'), icon('pin', 'ico ico--sm')], <<<HTML
<footer class="site-footer">
  <div class="site-footer__glow" aria-hidden="true"></div>
  <div class="container footer-grid">
    <div class="footer-brand">
      <img src="/assets/img/brand/austin-landscape-lighting-logo.webp" alt="Austin Landscape Lighting" width="250" height="41" loading="lazy" decoding="async">
      <p>Austin Landscape Lighting is Austin's trusted landscape lighting design and installation company since 2020. Low-voltage LED systems, brass fixtures and night-aimed designs that make Central Texas homes glow after dark.</p>
      <ul class="footer-contact">
        <li>{phone_i}<a href="{$tel}">{$phone}</a></li>
        <li>{mail_i}<a href="mailto:{$email}">{$email}</a></li>
        <li>{clock_i}<span>{$hours}</span></li>
        <li>{pin_i}<span>Austin, TX · Serving the greater Austin metro</span></li>
      </ul>
    </div>
    <nav class="footer-col" aria-label="Services"><h3>Services</h3><ul>{$svc}</ul></nav>
    <nav class="footer-col" aria-label="Service areas"><h3>Areas served</h3><ul>{$ar}</ul></nav>
    <nav class="footer-col" aria-label="Tools and company"><h3>Free tools</h3><ul>{$tl}</ul>
      <h3>Company</h3>
      <ul>
        <li><a href="/about-us/">About us</a></li>
        <li><a href="/gallery/">Project gallery</a></li>
        <li><a href="/reviews/">Reviews</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/contact/">Get an estimate</a></li>
      </ul>
    </nav>
  </div>
  <div class="container footer-bottom">
    <p>© {$year} Austin Landscape Lighting. All rights reserved. Licensed &amp; insured · 2-year workmanship warranty.</p>
    <ul>
      <li><a href="/privacy-policy/">Privacy Policy</a></li>
      <li><a href="/terms-of-service/">Terms of Service</a></li>
      <li><a href="/sitemap/">Sitemap</a></li>
    </ul>
  </div>
</footer>
HTML);
}
