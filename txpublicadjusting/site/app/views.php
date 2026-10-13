<?php
/** Layout and shared components. */

function tools_registry(): array
{
    return [
        'claim-settlement-calculator'     => ['Claim settlement calculator', 'See what your claim should pay after depreciation and your deductible, and what you net with or without a public adjuster.', 'calc'],
        'texas-claim-deadline-calculator' => ['Texas claim deadline calculator', 'Turn your claim dates into the insurer\'s Chapter 542 deadlines to acknowledge, decide and pay.', 'calendar'],
        'claim-documentation-checklist'   => ['Claim documentation checklist', 'An interactive, printable checklist for hail, water, fire and wind claims. Progress saves in your browser.', 'clipboard'],
        'contents-inventory-builder'      => ['Contents inventory builder', 'Build a room-by-room list of damaged belongings with ages and prices, then export it as a spreadsheet.', 'list'],
        'storm-report-lookup'             => ['Storm report lookup', 'Find NOAA hail and wind reports for a date and place to pin down your date of loss.', 'radar'],
        'do-i-need-a-public-adjuster'     => ['Do I need a public adjuster?', 'Seven honest questions that tell you whether your claim needs outside help, or whether you can handle it yourself.', 'quiz'],
    ];
}

function render_head(array $m): void
{
    $base = $m['title'] ?? BIZ['name'];
    $suffix = ' | ' . BIZ['name'];
    $title = $m['title_full'] ?? (mb_strlen($base . $suffix) <= 65 ? $base . $suffix : $base);
    $desc = $m['description'] ?? '';
    $path = $m['path'] ?? '/';
    $og = $m['og_image'] ?? '/assets/img/og-default.jpg';
    $robots = (!is_production() || !empty($m['noindex'])) ? 'noindex, nofollow' : 'index, follow, max-image-preview:large, max-snippet:-1';
    ?>
<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.remove('no-js')</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= h($title) ?></title>
<meta name="description" content="<?= h($desc) ?>">
<meta name="robots" content="<?= $robots ?>">
<link rel="canonical" href="<?= h(canonical($path)) ?>">
<?php if (GOOGLE_SITE_VERIFICATION): ?><meta name="google-site-verification" content="<?= h(GOOGLE_SITE_VERIFICATION) ?>"><?php endif; ?>
<meta property="og:type" content="<?= h($m['og_type'] ?? 'website') ?>">
<meta property="og:site_name" content="<?= h(BIZ['name']) ?>">
<meta property="og:title" content="<?= h($m['title'] ?? $title) ?>">
<meta property="og:description" content="<?= h($desc) ?>">
<meta property="og:url" content="<?= h(canonical($path)) ?>">
<meta property="og:image" content="<?= h(CANONICAL_ORIGIN . $og) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#051d40">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap">
<link rel="stylesheet" href="<?= asset('/assets/css/site.css') ?>">
<?= $m['schema'] ?? schema_graph([]) ?>
<?php if (GA4_ID && is_production()): ?>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= h(GA4_ID) ?>"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','<?= h(GA4_ID) ?>');</script>
<?php endif; ?>
</head>
<body class="<?= h($m['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<?php
}

function render_header(string $path): void
{
    ?>
<div class="topbar">
  <div class="wrap topbar__in">
    <span><?= icon('license') ?> Licensed Texas public adjuster · TDI license #<?= h(BIZ['license']) ?></span>
    <span class="topbar__right"><?= icon('pin') ?> Serving all 254 Texas counties from <?= h(BIZ['city']) ?>, TX</span>
  </div>
</div>
<header class="header" data-header>
  <div class="wrap header__in">
    <a class="brand" href="/" aria-label="<?= h(BIZ['name']) ?> home">
      <img src="/assets/img/TX-Public-Adjusting-Logo.webp" width="200" height="50" alt="<?= h(BIZ['name']) ?>">
    </a>
    <nav class="nav" aria-label="Main">
      <ul class="nav__list">
      <?php foreach (NAV as [$label, $href, $children]):
          $active = $href !== '/' && strpos($path, $href) === 0 ? ' is-active' : ''; ?>
        <li class="nav__item<?= $children ? ' has-menu' : '' ?>">
          <a class="nav__link<?= $active ?>" href="<?= h($href) ?>"><?= h($label) ?><?= $children ? icon('chevron', 'icon nav__chev') : '' ?></a>
          <?php if ($children): ?>
          <div class="menu">
            <?php foreach ($children as [$cl, $ch]): ?>
            <a href="<?= h($ch) ?>"><?= h($cl) ?></a>
            <?php endforeach; ?>
          </div>
          <?php endif; ?>
        </li>
      <?php endforeach; ?>
      </ul>
    </nav>
    <div class="header__cta">
      <a class="btn btn--ghost btn--sm header__phone" href="<?= tel_link() ?>"><?= icon('phone') ?><span><?= h(BIZ['phone_display']) ?></span></a>
      <a class="btn btn--primary btn--sm" href="/contact-us/">Free claim review</a>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" data-burger><?= icon('menu') ?></button>
    </div>
  </div>
</header>
<div class="drawer" data-drawer hidden>
  <div class="drawer__panel">
    <div class="drawer__top">
      <img src="/assets/img/TX-Public-Adjusting-Logo.webp" width="160" height="40" alt="">
      <button class="burger" type="button" aria-label="Close menu" data-drawer-close><?= icon('close') ?></button>
    </div>
    <nav aria-label="Mobile">
      <?php foreach (NAV as [$label, $href, $children]): ?>
        <a class="drawer__link" href="<?= h($href) ?>"><?= h($label) ?></a>
        <?php if ($children): foreach ($children as [$cl, $ch]): ?>
          <a class="drawer__sub" href="<?= h($ch) ?>"><?= h($cl) ?></a>
        <?php endforeach; endif; ?>
      <?php endforeach; ?>
      <a class="drawer__link" href="/contact-us/">Contact</a>
    </nav>
    <div class="drawer__cta">
      <a class="btn btn--primary btn--block" href="<?= tel_link() ?>"><?= icon('phone') ?> Call <?= h(BIZ['phone_display']) ?></a>
      <a class="btn btn--ghost btn--block" href="<?= sms_link() ?>"><?= icon('message') ?> Send a text</a>
    </div>
  </div>
</div>
<?php if (!is_production()): ?>
<div class="preview-pill" title="This preview domain is hidden from search engines">Preview site · not indexed</div>
<?php endif; ?>
<main id="main">
<?php
}

function render_footer(): void
{
    $year = date('Y');
    ?>
</main>
<footer class="footer">
  <div class="footer__glow" aria-hidden="true"></div>
  <div class="wrap footer__cta">
    <div>
      <h2>Not sure your claim was paid fairly?</h2>
      <p>Send us the estimate. Joseph will review it at no cost and tell you plainly whether it's worth disputing.</p>
    </div>
    <div class="footer__cta-btns">
      <a class="btn btn--primary btn--lg" href="/contact-us/">Request a free review <?= icon('arrow') ?></a>
      <a class="btn btn--light btn--lg" href="<?= tel_link() ?>"><?= icon('phone') ?> <?= h(BIZ['phone_display']) ?></a>
    </div>
  </div>
  <div class="wrap footer__grid">
    <div class="footer__about">
      <img src="/assets/img/TX-Public-Adjusting-Logo-White.webp" width="200" height="50" alt="<?= h(BIZ['name']) ?>" loading="lazy">
      <p><?= h(BIZ['name']) ?> is the public adjusting practice of <?= h(BIZ['legal_name']) ?>. We represent policyholders, never insurance companies.</p>
      <p class="footer__lic"><?= icon('license') ?> <?= h(BIZ['adjuster']) ?>, Texas public adjuster license #<?= h(BIZ['license']) ?></p>
      <p><a href="<?= tel_link() ?>"><?= icon('phone') ?> <?= h(BIZ['phone_display']) ?></a> · <a href="<?= sms_link() ?>">Text us</a></p>
      <p><?= icon('pin') ?> Based in <?= h(BIZ['city']) ?>, Texas · Statewide service</p>
    </div>
    <div>
      <h3>Claims we handle</h3>
      <a href="/services/roof-hail-damage-claims/">Roof &amp; hail damage</a>
      <a href="/services/water-damage-claims/">Water damage</a>
      <a href="/services/fire-smoke-damage-claims/">Fire &amp; smoke damage</a>
      <a href="/services/hurricane-windstorm-claims/">Hurricane &amp; windstorm</a>
      <a href="/services/denied-underpaid-claims/">Denied &amp; underpaid claims</a>
      <a href="/commercial-claims/">Commercial property</a>
    </div>
    <div>
      <h3>Free tools</h3>
      <?php foreach (tools_registry() as $slug => [$t]): ?>
      <a href="/tools/<?= h($slug) ?>/"><?= h($t) ?></a>
      <?php endforeach; ?>
    </div>
    <div>
      <h3>Company</h3>
      <a href="/about-us/">About Joseph Dittman</a>
      <a href="/areas/">Service areas</a>
      <a href="/blog/">Claim guides</a>
      <a href="/contact-us/">Contact</a>
      <a href="/privacy-policy/">Privacy policy</a>
      <a href="/terms-of-use/">Terms of use</a>
    </div>
  </div>
  <div class="wrap footer__legal">
    <p>&copy; <?= $year ?> <?= h(BIZ['legal_name']) ?>. Public adjusters are licensed by the Texas Department of Insurance. We are not a law firm and do not give legal advice. Information on this site is general and isn't a substitute for reading your policy.</p>
  </div>
</footer>
<a class="totop" href="#main" aria-label="Back to top" data-totop><?= icon('up') ?></a>
<div class="mobilebar">
  <a href="<?= tel_link() ?>"><?= icon('phone') ?> Call</a>
  <a href="<?= sms_link() ?>"><?= icon('message') ?> Text</a>
  <a class="mobilebar__main" href="/contact-us/">Free review</a>
</div>
<script src="<?= asset('/assets/js/site.js') ?>" defer></script>
</body>
</html>
<?php
}

function render_page(array $meta, callable $content): void
{
    render_head($meta);
    render_header($meta['path'] ?? '/');
    $content();
    render_footer();
}

function breadcrumbs_html(array $crumbs): string
{
    $out = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $last = count($crumbs) - 1;
    foreach ($crumbs as $i => [$name, $path]) {
        $out .= $i === $last
            ? '<li aria-current="page">' . h($name) . '</li>'
            : '<li><a href="' . h($path) . '">' . h($name) . '</a></li>';
    }
    return $out . '</ol></nav>';
}

function cta_box(): string
{
    return '<aside class="cta-box" data-reveal>
  <div class="cta-box__icon">' . icon('shield') . '</div>
  <div class="cta-box__text">
    <p class="cta-box__title">Get a second set of eyes on your claim</p>
    <p>Free review of your estimate, denial letter or policy. If we can\'t add value, we\'ll tell you.</p>
  </div>
  <div class="cta-box__btns">
    <a class="btn btn--primary" href="/contact-us/">Free claim review</a>
    <a class="btn btn--ghost" href="' . tel_link() . '">' . icon('phone') . ' ' . h(BIZ['phone_display']) . '</a>
  </div>
</aside>';
}

function tool_card(string $slug, string $extra = ''): string
{
    $reg = tools_registry();
    if (!isset($reg[$slug])) {
        return '';
    }
    [$title, $desc, $ic] = $reg[$slug];
    return '<a class="tool-card ' . h($extra) . '" href="/tools/' . h($slug) . '/" data-reveal>
  <span class="tool-card__icon">' . icon($ic) . '</span>
  <span class="tool-card__body"><span class="tool-card__kicker">Free tool</span><span class="tool-card__title">' . h($title) . '</span><span class="tool-card__desc">' . h($desc) . '</span></span>
  <span class="tool-card__go">' . icon('arrow') . '</span>
</a>';
}

function process_shortcodes(string $html): string
{
    $html = preg_replace('#<p>\s*(\[\[[a-z:-]+\]\])\s*</p>#', '$1', $html);
    $html = str_replace('[[cta]]', cta_box(), $html);
    return preg_replace_callback('#\[\[tool:([a-z0-9-]+)\]\]#', fn($m) => tool_card($m[1]), $html);
}

/** Wrap bare <table> in .table-wrap if a writer forgot. */
function normalize_body(string $html): string
{
    $html = preg_replace('#(?<!<div class="table-wrap">)\s*<table>#', '<div class="table-wrap"><table>', $html);
    $html = preg_replace('#</table>(?!\s*</div>)#', '</table></div>', $html);
    // External links open safely.
    return preg_replace_callback('#<a href="(https?://[^"]+)"(?![^>]*target=)#', fn($m) => '<a href="' . $m[1] . '" target="_blank" rel="noopener"', $html);
}

function faq_html(array $faqs, string $title = 'Frequently asked questions'): string
{
    if (!$faqs) {
        return '';
    }
    $out = '<section class="faqs" id="faq"><h2>' . h($title) . '</h2>';
    foreach ($faqs as $i => $f) {
        $out .= '<details class="faq"' . ($i === 0 ? ' open' : '') . '><summary>' . h(strip_tags($f['q'])) . icon('chevron', 'icon faq__chev') . '</summary><div class="faq__a"><p>' . $f['a'] . '</p></div></details>';
    }
    return $out . '</section>';
}

function author_box(): string
{
    return '<div class="author-box" data-reveal>
  <img src="/assets/img/Joseph-Dittman-TX-Public-Adjusting.webp" width="96" height="96" alt="Joseph Dittman" loading="lazy">
  <div>
    <p class="author-box__kicker">Written by</p>
    <p class="author-box__name"><a href="/about-us/">Joseph Dittman</a></p>
    <p class="author-box__role">Licensed Texas public adjuster · License #' . h(BIZ['license']) . ' · ' . h(BIZ['legal_name']) . '</p>
    <p>Joseph inspects, documents and negotiates residential and commercial property claims across Texas, working only for policyholders.</p>
  </div>
</div>';
}

function card_for(array $p): string
{
    $url = $p['_url'] ?? url_for($p['_type'], $p['_slug']);
    $img = $p['_type'] === 'posts' ? '/assets/img/blog/' . $p['_slug'] . '-600.webp' : null;
    $kicker = $p['category'] ?? ($p['eyebrow'] ?? '');
    if ($p['_type'] === 'tools') {
        return tool_card($p['_slug']);
    }
    $out = '<a class="card" href="' . h($url) . '" data-reveal>';
    if ($img && is_file(SITE_ROOT . $img)) {
        $out .= '<span class="card__img"><img src="' . h($img) . '" alt="" loading="lazy" width="600" height="400"></span>';
    } elseif (!empty($p['icon'])) {
        $out .= '<span class="card__icon">' . icon($p['icon']) . '</span>';
    }
    $out .= '<span class="card__body"><span class="card__kicker">' . h($kicker) . '</span><span class="card__title">' . h($p['h1'] ?? $p['title']) . '</span><span class="card__desc">' . h($p['description'] ?? '') . '</span><span class="card__more">Read more ' . icon('arrow') . '</span></span></a>';
    return $out;
}

function related_html(array $urls, string $title = 'Keep reading'): string
{
    $cards = '';
    foreach (array_slice($urls, 0, 6) as $u) {
        $p = page_for_url($u);
        if ($p) {
            $cards .= card_for($p);
        }
    }
    return $cards ? '<section class="related wrap"><h2 class="section-title">' . h($title) . '</h2><div class="grid grid--3">' . $cards . '</div></section>' : '';
}

function toc_html(array $toc): string
{
    if (count($toc) < 3) {
        return '';
    }
    $out = '<nav class="toc" aria-label="On this page"><p class="toc__title">On this page</p><ol>';
    foreach ($toc as [$id, $text]) {
        $out .= '<li><a href="#' . h($id) . '">' . h($text) . '</a></li>';
    }
    return $out . '</ol></nav>';
}

function aside_contact(): string
{
    return '<div class="aside-card">
  <p class="aside-card__title">Talk to a licensed adjuster</p>
  <p>Free claim review. No upfront fees. Texas caps public adjuster fees at 10%.</p>
  <a class="btn btn--primary btn--block" href="/contact-us/">Request a review</a>
  <a class="btn btn--ghost btn--block" href="' . tel_link() . '">' . icon('phone') . ' ' . h(BIZ['phone_display']) . '</a>
</div>';
}

/** Mini Texas map with highlighted metro(s). */
function texas_map(array $highlight = [], bool $labels = false, bool $links = false, string $class = 'txmap'): string
{
    $tx = require SITE_ROOT . '/app/texas.php';
    $out = '<svg class="' . h($class) . '" viewBox="0 0 ' . $tx['w'] . ' ' . $tx['h'] . '" role="img" aria-label="Map of Texas showing the cities we serve"><path class="txmap__state" d="' . $tx['path'] . '"/>';
    foreach ($tx['metros'] as $slug => [$name, $lat, $lng]) {
        $x = ($lng * $tx['k'] - $tx['minx']) * $tx['s'];
        $y = (-$lat - $tx['miny']) * $tx['s'];
        $hl = in_array($slug, $highlight, true);
        $isHome = $slug === 'belton';
        $dot = '<g class="txmap__pt' . ($hl ? ' is-hl' : '') . ($isHome ? ' is-home' : '') . '" transform="translate(' . round($x, 1) . ' ' . round($y, 1) . ')">'
            . ($hl || $isHome ? '<circle class="txmap__pulse" r="18"/>' : '')
            . '<circle class="txmap__dot" r="' . ($isHome ? 9 : 7) . '"/>'
            . ($labels || $hl ? '<text x="' . (in_array($slug, ['fort-worth', 'killeen', 'san-antonio', 'midland'], true) ? -13 : 13) . '" y="' . ($slug === 'belton' ? 16 : 5) . '"' . (in_array($slug, ['fort-worth', 'killeen', 'san-antonio', 'midland'], true) ? ' text-anchor="end"' : '') . '>' . h($isHome ? 'Belton (HQ)' : $name) . '</text>' : '')
            . '</g>';
        if ($links && !$isHome) {
            $dot = '<a href="/areas/public-insurance-adjuster-' . h($slug) . '/" aria-label="' . h($name) . '">' . $dot . '</a>';
        }
        $out .= $dot;
    }
    return $out . '</svg>';
}

/** Standard article-style page (services, commercial, posts, generic pages). */
function render_article(array $p, string $path, array $crumbs, array $opt = []): void
{
    $type = $p['_type'] ?? 'pages';
    [$body, $toc] = add_heading_ids(normalize_body(process_shortcodes($p['body'] ?? '')));
    $faqs = $p['faqs'] ?? [];
    $isPost = $type === 'posts';
    $img = $isPost ? '/assets/img/blog/' . $p['_slug'] . '.webp' : null;
    if ($img && !is_file(SITE_ROOT . $img)) {
        $img = null;
    }

    $nodes = [schema_breadcrumbs($crumbs), schema_faq($faqs)];
    if ($isPost) {
        $nodes[] = schema_article($p, $path);
    } elseif (in_array($type, ['services', 'commercial', 'areas'], true) && ($p['_slug'] ?? '') !== 'index') {
        $nodes[] = schema_service($p, $path);
    }

    render_page([
        'title'       => $p['title'],
        'description' => $p['description'] ?? '',
        'path'        => $path,
        'og_type'     => $isPost ? 'article' : 'website',
        'og_image'    => $img ?: '/assets/img/og-default.jpg',
        'schema'      => schema_graph($nodes),
        'body_class'  => 'page-' . $type . ($isPost ? ' has-progress' : ''),
    ], function () use ($p, $path, $crumbs, $body, $toc, $faqs, $isPost, $img, $opt, $type) {
        ?>
<?php if ($isPost): ?><div class="progress" aria-hidden="true"><span data-progress></span></div><?php endif; ?>
<section class="hero hero--page">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap hero__in<?= $img ? ' hero__in--split' : '' ?>">
    <div class="hero__copy">
      <?= breadcrumbs_html($crumbs) ?>
      <?php if (!empty($p['icon'])): ?><span class="hero__icon"><?= icon($p['icon']) ?></span><?php endif; ?>
      <?php if (!empty($p['eyebrow'])): ?><p class="eyebrow"><?= h($p['eyebrow']) ?></p><?php endif; ?>
      <h1><?= h($p['h1'] ?? $p['title']) ?></h1>
      <?php if (!empty($p['lead'])): ?><p class="hero__lead"><?= h($p['lead']) ?></p><?php endif; ?>
      <?php if ($isPost): ?>
      <div class="byline">
        <img src="/assets/img/Joseph-Dittman-TX-Public-Adjusting.webp" width="44" height="44" alt="">
        <div>
          <a href="/about-us/">Joseph Dittman</a>, licensed public adjuster #<?= h(BIZ['license']) ?><br>
          <span>Updated <?= h(fmt_date($p['updated'] ?? $p['published'] ?? null)) ?> · <?= read_minutes($p['body'] ?? '') ?> min read</span>
        </div>
      </div>
      <?php else: ?>
      <div class="hero__btns">
        <a class="btn btn--primary" href="/contact-us/">Free claim review <?= icon('arrow') ?></a>
        <a class="btn btn--light" href="<?= tel_link() ?>"><?= icon('phone') ?> <?= h(BIZ['phone_display']) ?></a>
      </div>
      <?php endif; ?>
    </div>
    <?php if ($img): ?>
    <figure class="hero__figure"><img src="<?= h($img) ?>" alt="<?= h($p['h1'] ?? $p['title']) ?>" width="1200" height="800" fetchpriority="high"></figure>
    <?php endif; ?>
  </div>
</section>
<?= $opt['before'] ?? '' ?>
<div class="wrap article-layout">
  <article class="prose">
    <?= $body ?>
    <?= faq_html($faqs) ?>
    <?= ($isPost || $type === 'services') ? author_box() : '' ?>
  </article>
  <aside class="article-aside">
    <div class="sticky">
      <?= toc_html($toc) ?>
      <?= aside_contact() ?>
    </div>
  </aside>
</div>
<?= $opt['after'] ?? '' ?>
<?= related_html($p['related'] ?? []) ?>
<?php
    });
}
