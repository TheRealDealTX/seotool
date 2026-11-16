<?php
declare(strict_types=1);

/**
 * Render a full page.
 * $m keys: title, description, path, image, schema (array of nodes), crumbs ([[name,url],...]),
 *          body_class, noindex (bool), og_type, head_extra, scripts (array of asset paths)
 */
function render_page(array $m, string $content): void
{
    $path   = $m['path'] ?? '/';
    $canon  = abs_url($path);
    $title  = $m['title'];
    $desc   = $m['description'];
    $image  = abs_url($m['image'] ?? SITE['og_default']);
    $robots = (!empty($m['noindex']) || !is_production()) ? 'noindex, nofollow' : 'index, follow, max-image-preview:large, max-snippet:-1';
    $schema = $m['schema'] ?? [];
    if (!empty($m['crumbs'])) {
        $schema[] = schema_breadcrumbs($m['crumbs']);
    }
    if (!is_production()) {
        header('X-Robots-Tag: noindex, nofollow');
    }
    header('Content-Type: text/html; charset=utf-8');
    ?><!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<!-- Google tag (GTM-5BXPCPWX) -->
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-5BXPCPWX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<meta name="robots" content="<?= $robots ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($m['og_type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:site_name" content="<?= e(SITE['name']) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($title) ?>">
<meta name="twitter:description" content="<?= e($desc) ?>">
<meta name="twitter:image" content="<?= e($image) ?>">
<meta name="theme-color" content="#1D4463">
<meta name="geo.region" content="US-TX">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/webp" href="<?= SITE['icon'] ?>">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap">
<link rel="stylesheet" href="<?= asset('/assets/css/site.css') ?>">
<?php if (!empty($m['preload'])): ?><link rel="preload" as="image" href="<?= e($m['preload']) ?>" fetchpriority="high"><?php endif; ?>
<?= $m['head_extra'] ?? '' ?>
<?= render_schema($schema) ?>
</head>
<body class="<?= e($m['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<?php site_header($path); ?>
<main id="main">
<?php if (!empty($m['crumbs'])) {
    echo breadcrumbs_html($m['crumbs']);
} ?>
<?= $content ?>
</main>
<?php site_footer(); ?>
<script src="<?= asset('/assets/js/site.js') ?>" defer></script>
<?php foreach ($m['scripts'] ?? [] as $s): ?><script src="<?= asset($s) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}

function site_header(string $path): void
{
    ?>
<div class="topbar">
  <div class="wrap topbar-in">
    <span class="tb-item"><?= icon('shield', 16) ?> Policyholder-side appraisers serving all of Texas</span>
    <span class="tb-item hide-sm"><?= icon('clock', 16) ?> <?= e(SITE['hours']) ?></span>
    <a class="tb-item tb-phone" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 16) ?> Call a Professional Now: <strong><?= e(SITE['phone']) ?></strong></a>
  </div>
</div>
<header class="site-header" id="top">
  <div class="wrap header-in">
    <a class="brand" href="/" aria-label="<?= e(SITE['name']) ?> home">
      <img src="<?= SITE['logo'] ?>" alt="TX Insurance Appraiser logo" width="150" height="60">
    </a>
    <nav class="nav" aria-label="Main navigation" id="nav">
      <ul class="nav-list">
      <?php foreach (NAV as [$label, $url, $kids]):
          $active = ($url === '/' ? $path === '/' : str_starts_with($path, $url)) ? ' is-active' : ''; ?>
        <li class="nav-item<?= $kids ? ' has-sub' : '' ?><?= $active ?>">
          <a href="<?= $url ?>"><?= e($label) ?><?= $kids ? icon('chev', 14) : '' ?></a>
          <?php if ($kids): ?>
          <ul class="sub">
            <?php foreach ($kids as [$kl, $ku]): ?><li><a href="<?= $ku ?>"><?= e($kl) ?></a></li><?php endforeach; ?>
          </ul>
          <?php endif; ?>
        </li>
      <?php endforeach; ?>
      </ul>
      <a class="btn btn-gold nav-cta" href="/contact-us/" data-popup>Free Claim Review</a>
    </nav>
    <a class="btn btn-gold header-cta" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 18) ?><span>Call Now</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><?= icon('menu', 28) ?></button>
  </div>
</header>
<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Menu" hidden>
  <div class="mnav-top">
    <a href="/" class="mnav-logo"><img src="<?= SITE['logo'] ?>" alt="TX Insurance Appraiser" width="140" height="56"></a>
    <button class="mnav-close" type="button" aria-label="Close menu"><?= icon('x', 26) ?><span>Close</span></button>
  </div>
  <nav class="mnav-body" aria-label="Mobile navigation">
    <ul class="mnav-list">
    <?php foreach (NAV as $i => [$label, $url, $kids]):
        $active = ($url === '/' ? $path === '/' : str_starts_with($path, $url)); ?>
      <li class="mnav-item<?= $active ? ' is-active' : '' ?>">
        <div class="mnav-row">
          <a href="<?= $url ?>"><?= e($label) ?></a>
          <?php if ($kids): ?><button type="button" class="mnav-toggle" aria-expanded="false" aria-controls="msub<?= $i ?>" aria-label="Show <?= e($label) ?> links"><?= icon('chev', 22) ?></button><?php endif; ?>
        </div>
        <?php if ($kids): ?>
        <ul class="mnav-sub" id="msub<?= $i ?>" hidden>
          <?php foreach ($kids as [$kl, $ku]): ?><li><a href="<?= $ku ?>"><?= e($kl) ?></a></li><?php endforeach; ?>
        </ul>
        <?php endif; ?>
      </li>
    <?php endforeach; ?>
    </ul>
  </nav>
  <div class="mnav-foot">
    <a class="btn btn-gold btn-block btn-lg" href="/contact-us/" data-popup>Free Claim Review</a>
    <div class="mnav-contact">
      <a class="btn btn-navy" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 18) ?> Call</a>
      <a class="btn btn-ghost" href="sms:<?= SITE['phone_href'] ?>"><?= icon('chat', 18) ?> Text</a>
    </div>
    <p><?= e(SITE['phone']) ?> · <?= e(SITE['hours']) ?></p>
  </div>
</div>
<?php
}

function breadcrumbs_html(array $crumbs): string
{
    $out = '<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>';
    $n = count($crumbs);
    foreach ($crumbs as $i => [$name, $url]) {
        $out .= $i === $n - 1
            ? '<li aria-current="page">' . e($name) . '</li>'
            : '<li><a href="' . e($url) . '">' . e($name) . '</a></li>';
    }
    return $out . '</ol></div></nav>';
}

function cta_band(string $heading = '', string $text = ''): string
{
    $heading = $heading ?: 'Disagree with your insurance settlement?';
    $text = $text ?: 'Get a free, no-pressure claim review from TX Insurance Appraiser. We’ll tell you honestly whether appraisal makes sense for your loss.';
    return '<section class="cta-band reveal"><div class="wrap cta-in"><div><h2>' . e($heading) . '</h2><p>' . e($text) . '</p></div>'
        . '<div class="cta-actions"><a class="btn btn-gold btn-lg" href="tel:' . SITE['phone_href'] . '">' . icon('phone', 20) . ' ' . e(SITE['phone']) . '</a>'
        . '<a class="btn btn-ghost-light btn-lg" href="/contact-us/">Request a Claim Review ' . icon('arrow', 18) . '</a></div></div></section>';
}

function site_footer(): void
{
    $c = cities();
    $top = ['houston', 'dallas', 'austin', 'san-antonio', 'fort-worth', 'el-paso', 'arlington', 'corpus-christi', 'plano', 'waco', 'lubbock', 'killeen'];
    ?>
<footer class="site-footer">
  <div class="footer-bg" aria-hidden="true"></div>
  <div class="wrap footer-grid">
    <div class="f-brand">
      <img src="<?= SITE['logo'] ?>" alt="TX Insurance Appraiser" width="170" height="67" loading="lazy" class="f-logo">
      <p class="f-tag"><?= e(SITE['blurb']) ?></p>
      <ul class="f-contact">
        <li><?= icon('phone', 18) ?> <a href="tel:<?= SITE['phone_href'] ?>"><?= e(SITE['phone']) ?></a></li>
        <li><?= icon('chat', 18) ?> <a href="sms:<?= SITE['phone_href'] ?>">Send a text message</a></li>
        <li><?= icon('mail', 18) ?> <a href="mailto:<?= SITE['email'] ?>"><?= e(SITE['email']) ?></a></li>
        <li><?= icon('clock', 18) ?> <?= e(SITE['hours']) ?></li>
        <li><?= icon('pin', 18) ?> Serving Austin, Waco, Dallas, Houston &amp; all of Texas</li>
      </ul>
    </div>
    <div>
      <h3 class="f-h">Services</h3>
      <ul class="f-links">
        <li><a href="/services/appraisal/">Insurance Appraisal</a></li>
        <li><a href="/services/umpire/">Umpire Services</a></li>
        <li><a href="/services/matterport/">Matterport 3D Scans</a></li>
        <li><a href="/services/xactimate-estimate/">Xactimate Estimates</a></li>
        <li><a href="/services/symbility-estimate/">Symbility Estimates</a></li>
        <li><a href="/what-is-an-appraisal/">What Is an Appraisal?</a></li>
      </ul>
    </div>
    <div>
      <h3 class="f-h">Top Service Areas</h3>
      <ul class="f-links f-cols">
        <?php foreach ($top as $s): if (!isset($c[$s])) continue; ?>
        <li><a href="<?= city_url($s) ?>"><?= e($c[$s]['name']) ?></a></li>
        <?php endforeach; ?>
        <li><a href="/areas/"><strong>All Texas cities →</strong></a></li>
      </ul>
    </div>
    <div>
      <h3 class="f-h">Resources</h3>
      <ul class="f-links">
        <li><a href="/about-us/">About Joseph Dittman</a></li>
        <li><a href="/tools/">Free Claim Tools</a></li>
        <li><a href="/tools/recoverable-depreciation-calculator/">Depreciation Calculator</a></li>
        <li><a href="/blog/">Insurance Claim Blog</a></li>
        <li><a href="/contact-us/">Contact Us</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-conditions/">Terms &amp; Conditions</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap f-bottom">
    <p>© <?= date('Y') ?> <?= e(SITE['copyright']) ?>. All rights reserved.</p>
    <p class="f-disclaimer">TX Insurance Appraiser is not a law firm and does not provide legal advice. Appraisal addresses the amount of loss under your policy’s appraisal provision; results depend on your policy and the facts of your claim.</p>
  </div>
</footer>
<div class="modal" id="lead-modal" role="dialog" aria-modal="true" aria-labelledby="lead-modal-title" hidden>
  <div class="modal-backdrop"></div>
  <div class="modal-box">
    <button class="modal-x" type="button" aria-label="Close"><?= icon('x', 22) ?></button>
    <div class="modal-head">
      <img src="<?= SITE['photo'] ?>" alt="Joseph Dittman" width="64" height="64" loading="lazy">
      <div><span class="eyebrow" style="margin:0 0 4px">Free claim review</span><h2 id="lead-modal-title">Was your claim underpaid?</h2></div>
    </div>
    <p class="modal-sub">Tell us about your claim and Joseph will personally review it — free, with no obligation.</p>
    <?= lead_form('compact', 'popup') ?>
  </div>
</div>
<div class="mobile-bar" role="navigation" aria-label="Quick contact">
  <a href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 20) ?> Call</a>
  <a href="sms:<?= SITE['phone_href'] ?>"><?= icon('chat', 20) ?> Text</a>
  <a href="/contact-us/" class="mb-gold" data-popup><?= icon('doc', 20) ?> Free Review</a>
</div>
<button class="to-top" aria-label="Back to top"><?= icon('chev', 22) ?></button>
<?php
}

/** Reusable FAQ accordion. */
function faq_html(array $faqs, string $heading = 'Frequently Asked Questions', string $id = 'faq'): string
{
    $out = '<section class="section faq-sec" id="' . e($id) . '"><div class="wrap narrow"><h2 class="sec-title reveal">' . e($heading) . '</h2><div class="faq-list">';
    foreach ($faqs as $i => $f) {
        $out .= '<details class="faq reveal"' . ($i === 0 ? ' open' : '') . '><summary>' . e($f['q']) . icon('chev', 20) . '</summary><div class="faq-a"><p>' . e($f['a']) . '</p></div></details>';
    }
    return $out . '</div></div></section>';
}

/** Lead form used on contact page and as a sidebar/inline widget. */
function lead_form(string $variant = 'full', string $source = ''): string
{
    $id = 'f' . substr(md5($variant . $source), 0, 6);
    ob_start(); ?>
<form class="lead-form <?= $variant === 'compact' ? 'compact' : '' ?>" method="post" action="/contact-submit/" data-ajax>
  <input type="hidden" name="source" value="<?= e($source) ?>">
  <div class="hp" aria-hidden="true"><label>Leave empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="ts" value="<?= time() ?>">
  <div class="fgrid">
    <label class="fl"><span>First name *</span><input name="first_name" required autocomplete="given-name"></label>
    <label class="fl"><span>Last name</span><input name="last_name" autocomplete="family-name"></label>
    <label class="fl"><span>Phone *</span><input name="phone" type="tel" required autocomplete="tel"></label>
    <label class="fl"><span>Email *</span><input name="email" type="email" required autocomplete="email"></label>
    <?php if ($variant !== 'compact'): ?>
    <label class="fl"><span>Property city</span><input name="city" autocomplete="address-level2" placeholder="e.g. Houston"></label>
    <label class="fl"><span>Type of loss</span>
      <select name="loss_type"><option value="">Select…</option><option>Hail</option><option>Wind / Tornado</option><option>Hurricane</option><option>Water / Plumbing</option><option>Fire / Smoke</option><option>Freeze</option><option>Other</option></select>
    </label>
    <?php endif; ?>
    <label class="fl full"><span>How can we help?</span><textarea name="message" rows="<?= $variant === 'compact' ? 3 : 4 ?>" placeholder="Briefly describe your claim and where it stands."></textarea></label>
  </div>
  <label class="consent"><input type="checkbox" name="sms_consent" value="yes"> <span>I agree to receive text messages from TX Insurance Appraisals LLC about my appraisal, including scheduling, status updates and invoices. Message frequency varies. Msg &amp; data rates may apply. Reply STOP to opt out, HELP for help. Consent is not a condition of service. See our <a href="/privacy-policy/">Privacy Policy</a> and <a href="/terms-conditions/">Terms &amp; Conditions</a>.</span></label>
  <button class="btn btn-gold btn-block" type="submit">Request My Free Claim Review <?= icon('arrow', 18) ?></button>
  <p class="form-msg" role="status" aria-live="polite"></p>
</form>
<?php
    return (string) ob_get_clean();
}
