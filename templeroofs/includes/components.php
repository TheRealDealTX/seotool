<?php
/** Reusable page sections and cards. */
defined('TR_ROOT') || exit;

function breadcrumbs_html(array $crumbs): string
{
    if (!$crumbs) {
        return '';
    }
    $out = '<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>';
    $last = count($crumbs) - 1;
    foreach ($crumbs as $i => [$label, $path]) {
        $out .= $i === $last
            ? '<li><span aria-current="page">' . e($label) . '</span></li>'
            : '<li><a href="' . e($path) . '">' . e($label) . '</a></li>';
    }
    return $out . '</ol></nav>';
}

/**
 * Inner-page hero. Options: h1, lead, image, alt, crumbs, eyebrow,
 * actions (bool, default true), meta (raw HTML under the lead), compact.
 */
function page_hero(array $o): void
{
    $hasImg = !empty($o['image']);
    ?>
<section class="page-hero<?= $hasImg ? ' page-hero--image' : '' ?><?= !empty($o['compact']) ? ' page-hero--compact' : '' ?>">
  <?php if ($hasImg): ?>
  <div class="page-hero__bg" data-parallax><?= img($o['image'], $o['alt'] ?? '', ['sizes' => '100vw', 'priority' => true, 'class' => 'page-hero__img']) ?></div>
  <?php endif; ?>
  <div class="container page-hero__inner">
    <?= breadcrumbs_html($o['crumbs'] ?? []) ?>
    <?php if (!empty($o['eyebrow'])): ?><p class="eyebrow eyebrow--light"><?= e($o['eyebrow']) ?></p><?php endif; ?>
    <h1 class="page-hero__title"><?= e($o['h1']) ?></h1>
    <?php if (!empty($o['lead'])): ?><p class="page-hero__lead"><?= e($o['lead']) ?></p><?php endif; ?>
    <?= $o['meta'] ?? '' ?>
    <?php if ($o['actions'] ?? true): ?>
    <div class="btn-row">
      <a class="btn btn--gold" href="/free-roof-inspection/"><?= icon('clipboard-check') ?> Get My Free Roof Inspection</a>
      <a class="btn btn--outline-light" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> Call <?= e(cfg('phone_display')) ?></a>
    </div>
    <?php endif; ?>
  </div>
</section>
<?php
}

function cta_box(string $heading = 'Not sure what your roof needs?', string $text = ''): string
{
    $text = $text ?: 'Temple Roofers will inspect your roof for free, photograph what we find and explain your options in plain language. There is no cost and no obligation.';
    return '<aside class="cta-box reveal" aria-label="Free roof inspection">'
        . '<div class="cta-box__icon">' . icon('clipboard-check') . '</div>'
        . '<div class="cta-box__body"><p class="cta-box__title">' . e($heading) . '</p><p>' . e($text) . '</p></div>'
        . '<div class="cta-box__actions"><a class="btn btn--gold" href="/free-roof-inspection/">Book a Free Inspection</a>'
        . '<a class="cta-box__phone" href="' . e(tel_href()) . '">' . icon('phone') . ' ' . e(cfg('phone_display')) . '</a></div>'
        . '</aside>';
}

/** Body HTML from content files, with the mid-article CTA marker expanded. */
function render_body(string $html, string $ctaHeading = ''): string
{
    $cta = cta_box($ctaHeading ?: 'Want a professional set of eyes on your roof?');
    if (str_contains($html, '<!--cta-->')) {
        return preg_replace('/<!--cta-->/', $cta, $html, 1);
    }
    return $html;
}

function faq_html(array $faqs, string $heading = 'Frequently Asked Questions', string $intro = ''): string
{
    if (!$faqs) {
        return '';
    }
    static $n = 0;
    $out = '<section class="faq" aria-labelledby="faq-h-' . (++$n) . '"><h2 id="faq-h-' . $n . '">' . e($heading) . '</h2>';
    if ($intro) {
        $out .= '<p class="faq__intro">' . e($intro) . '</p>';
    }
    $out .= '<div class="faq__list">';
    foreach ($faqs as $i => $f) {
        $id = 'faq-' . $n . '-' . $i;
        $out .= '<div class="faq__item">'
            . '<h3 class="faq__q"><button type="button" aria-expanded="false" aria-controls="' . $id . '">'
            . '<span>' . e($f['q']) . '</span>' . icon('plus', 'faq__icon') . '</button></h3>'
            . '<div class="faq__a" id="' . $id . '" role="region" hidden><div class="faq__a-inner"><p>' . e($f['a']) . '</p></div></div>'
            . '</div>';
    }
    return $out . '</div></section>';
}

function service_card(array $s, bool $withImage = true): string
{
    $out = '<article class="card card--service reveal">';
    if ($withImage) {
        $out .= '<a class="card__media" href="' . e($s['url']) . '" tabindex="-1" aria-hidden="true">'
            . img($s['image'], '', ['sizes' => '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw', 'decorative' => true])
            . '</a>';
    }
    $out .= '<div class="card__body">' . ($withImage ? '<span class="card__badge" aria-hidden="true">' . icon($s['icon'] ?? 'home') . '</span>' : '') . '<h3 class="card__title"><a href="' . e($s['url']) . '">' . e($s['name']) . '</a></h3>'
        . '<p>' . e($s['card_summary']) . '</p>'
        . '<a class="card__link" href="' . e($s['url']) . '">Learn more<span class="sr-only"> about ' . e($s['name']) . '</span> ' . icon('arrow-right') . '</a></div></article>';
    return $out;
}

function post_card(array $p, string $headingTag = 'h3'): string
{
    return '<article class="card card--post reveal">'
        . '<a class="card__media" href="' . e($p['url']) . '" tabindex="-1" aria-hidden="true">'
        . img($p['image'], '', ['sizes' => '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw', 'decorative' => true]) . '</a>'
        . '<div class="card__body">'
        . '<p class="card__meta"><a class="tag" href="/blog/category/' . e($p['category']) . '/">' . e(category_name($p['category'])) . '</a>'
        . '<time datetime="' . e($p['date']->format('Y-m-d')) . '">' . e(format_date($p['date'])) . '</time></p>'
        . '<' . $headingTag . ' class="card__title"><a href="' . e($p['url']) . '">' . e($p['title']) . '</a></' . $headingTag . '>'
        . '<p>' . e($p['excerpt']) . '</p>'
        . '<p class="card__foot"><span>' . icon('clock') . ' ' . (int) $p['minutes'] . ' min read</span>'
        . '<a class="card__link" href="' . e($p['url']) . '">Read article<span class="sr-only">: ' . e($p['title']) . '</span> ' . icon('arrow-right') . '</a></p>'
        . '</div></article>';
}

function area_card(array $a): string
{
    return '<a class="area-card reveal" href="' . e($a['url']) . '">'
        . '<span class="area-card__pin">' . icon('map-pin') . '</span>'
        . '<span class="area-card__body"><span class="area-card__name">' . e($a['city']) . ', TX</span>'
        . '<span class="area-card__note">' . e($a['distance_note']) . '</span></span>'
        . icon('arrow-right', 'area-card__arrow') . '</a>';
}

function tool_card(string $slug, array $t): string
{
    return '<article class="tool-card reveal">'
        . '<span class="tool-card__icon">' . icon($t['icon']) . '</span>'
        . '<h3 class="tool-card__title"><a href="/tools/' . e($slug) . '/">' . e($t['name']) . '</a></h3>'
        . '<p>' . e($t['summary']) . '</p>'
        . '<a class="card__link" href="/tools/' . e($slug) . '/">Open the tool<span class="sr-only">: ' . e($t['name']) . '</span> ' . icon('arrow-right') . '</a>'
        . '</article>';
}

/** "Related services / related articles" block used by content pages. */
function related_html(array $serviceSlugs, array $postSlugs, string $exclude = ''): string
{
    $svc = [];
    foreach ($serviceSlugs as $slug) {
        if ($slug !== $exclude && ($s = service($slug))) {
            $svc[] = $s;
        }
    }
    $posts = [];
    foreach ($postSlugs as $slug) {
        if ($slug !== $exclude && ($p = post($slug))) {
            $posts[] = $p;
        }
    }
    if (!$svc && !$posts) {
        return '';
    }
    $out = '<section class="related" aria-label="Related roofing resources">';
    if ($svc) {
        $out .= '<div class="related__col"><h2 class="related__title">Related Services</h2><ul class="link-list">';
        foreach ($svc as $s) {
            $out .= '<li><a href="' . e($s['url']) . '">' . icon($s['icon'] ?? 'home') . '<span><strong>' . e($s['name']) . '</strong><small>' . e($s['card_summary']) . '</small></span></a></li>';
        }
        $out .= '</ul></div>';
    }
    if ($posts) {
        $out .= '<div class="related__col"><h2 class="related__title">Related Articles</h2><ul class="link-list">';
        foreach ($posts as $p) {
            $out .= '<li><a href="' . e($p['url']) . '">' . icon('book') . '<span><strong>' . e($p['title']) . '</strong><small>' . e(format_date($p['date'])) . ' · ' . (int) $p['minutes'] . ' min read</small></span></a></li>';
        }
        $out .= '</ul></div>';
    }
    return $out . '</section>';
}

/** Full-width closing CTA with the short lead form. */
function final_cta(string $heading = 'Concerned About Your Roof? Schedule a Free Inspection.', string $text = '', string $source = ''): void
{
    $text = $text ?: 'Tell us what is going on with your roof and we will set up a time to take a look. The inspection is free, there is no obligation, and you will get clear answers either way.';
    ?>
<section class="final-cta" id="get-inspection">
  <div class="container final-cta__inner">
    <div class="final-cta__copy reveal">
      <p class="eyebrow eyebrow--light">Free · No obligation</p>
      <h2><?= e($heading) ?></h2>
      <p><?= e($text) ?></p>
      <ul class="check-list check-list--light">
        <li><?= icon('check') ?> Photos of anything we find</li>
        <li><?= icon('check') ?> Repair-first, honest recommendations</li>
        <li><?= icon('check') ?> Written estimate if work is needed</li>
      </ul>
      <a class="final-cta__phone" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> <span>Prefer to talk? Call <strong><?= e(cfg('phone_intl')) ?></strong></span></a>
    </div>
    <div class="final-cta__form reveal">
      <?php lead_form(['variant' => 'short', 'id' => 'final', 'source' => $source, 'title' => 'Request your free inspection']); ?>
    </div>
  </div>
</section>
<?php
}

function section_head(string $eyebrow, string $title, string $intro = '', string $tag = 'h2', bool $center = true): string
{
    return '<div class="section-head' . ($center ? ' section-head--center' : '') . ' reveal">'
        . ($eyebrow ? '<p class="eyebrow">' . e($eyebrow) . '</p>' : '')
        . '<' . $tag . ' class="section-title">' . e($title) . '</' . $tag . '>'
        . ($intro ? '<p class="section-intro">' . e($intro) . '</p>' : '')
        . '</div>';
}

/** Pre-select the lead form concern that matches a service page. */
function service_concern(string $slug): string
{
    $map = [
        'roof-repair' => 'repair', 'roof-replacement' => 'replacement', 'storm-damage' => 'storm', 'hail-damage' => 'storm',
        'wind-damage' => 'storm', 'roof-insurance' => 'insurance', 'metal-roofing' => 'metal', 'asphalt-shingle' => 'replacement',
        'commercial-roofing' => 'commercial', 'roof-inspection' => 'inspection', 'emergency-roof-leak' => 'leak', 'gutters' => 'gutters',
    ];
    foreach ($map as $prefix => $concern) {
        if (str_starts_with($slug, $prefix)) {
            return $concern;
        }
    }
    return 'inspection';
}
