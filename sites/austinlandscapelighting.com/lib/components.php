<?php
/**
 * Reusable page components. Each returns an HTML string.
 */
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

/** Fill {placeholders} in a template string. */
function fill(string $html, array $map): string
{
    return str_replace(array_keys($map), array_values($map), $html);
}

/** Compact page hero for interior pages. */
function sub_hero(array $o): string
{
    $eyebrow = $o['eyebrow'] ?? '';
    $h1 = $o['h1'];
    $intro = $o['intro'] ?? '';
    $image = $o['image'] ?? null;
    $alt = $o['image_alt'] ?? $h1;
    $crumbs = $o['crumbs'] ?? [];
    $meta = $o['meta'] ?? '';
    $cta = $o['cta'] ?? true;

    $crumbHtml = breadcrumbs($crumbs);
    $imgHtml = $image ? '<div class="sub-hero__media" data-parallax="0.12">' . picture($image, $alt, ['eager' => true, 'sizes' => '(max-width: 900px) 100vw, 46vw']) . '<span class="glow glow--amber"></span></div>' : '';
    $ctaHtml = $cta ? '<div class="sub-hero__actions"><a class="btn btn--primary" href="/contact/">Get a Free Design Consultation ' . icon('arrow') . '</a><a class="btn btn--ghost" href="' . BIZ['phone_href'] . '">' . icon('phone') . ' ' . e(BIZ['phone_short']) . '</a></div>' : '';
    $wide = $image ? '' : ' sub-hero__grid--wide';
    return <<<HTML
<section class="sub-hero spotlight" data-spotlight>
  <div class="stars" data-stars></div>
  <div class="container sub-hero__grid{$wide}">
    <div class="sub-hero__copy" data-reveal>
      {$crumbHtml}
      <p class="eyebrow">{$eyebrow}</p>
      <h1 class="display">{$h1}</h1>
      <p class="lede">{$intro}</p>
      {$meta}
      {$ctaHtml}
    </div>
    {$imgHtml}
  </div>
</section>
HTML;
}

function breadcrumbs(array $trail): string
{
    if (!$trail) {
        return '';
    }
    $li = '';
    $n = count($trail);
    foreach ($trail as $i => [$name, $path]) {
        $last = $i === $n - 1;
        $li .= $last
            ? '<li aria-current="page">' . e($name) . '</li>'
            : '<li><a href="' . e($path) . '">' . e($name) . '</a></li>';
    }
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' . $li . '</ol></nav>';
}

function section_head(string $eyebrow, string $title, string $text = '', string $align = 'center'): string
{
    $t = $text ? '<p class="section-head__text">' . $text . '</p>' : '';
    return <<<HTML
<div class="section-head section-head--{$align}" data-reveal>
  <p class="eyebrow">{$eyebrow}</p>
  <h2 class="display">{$title}</h2>
  {$t}
</div>
HTML;
}

function service_card(array $s, int $i = 0): string
{
    $delay = ($i % 4) * 80;
    $hl = '';
    foreach (array_slice($s['highlights'] ?? [], 0, 2) as $h) {
        $hl .= '<li>' . e($h) . '</li>';
    }
    $short = e($s['short'] ?? mb_strimwidth(strip_tags($s['intro'] ?? ''), 0, 120, '…'));
    return fill(<<<HTML
<a class="card card--service tilt" href="{$s['path']}" data-reveal style="--delay:{$delay}ms">
  <span class="card__glow"></span>
  <span class="card__icon">{icon}</span>
  <h3>{$s['name']}</h3>
  <p>{$short}</p>
  <ul class="card__list">{$hl}</ul>
  <span class="card__more">Explore {arrow}</span>
</a>
HTML, ['{icon}' => icon($s['icon']), '{arrow}' => icon('arrow')]);
}

function area_chip(array $a): string
{
    return '<a class="chip" href="' . e($a['path']) . '">' . icon('pin', 'ico ico--sm') . ' ' . e($a['city']) . '</a>';
}

function post_card(array $p, bool $big = false): string
{
    $cls = $big ? 'card card--post card--post-big' : 'card card--post';
    $date = nice_date($p['published']);
    $pic = picture($p['image'], $p['image_alt'] ?? $p['h1'], ['width' => 1600, 'height' => 900, 'sizes' => '(max-width: 760px) 100vw, 33vw']);
    return fill(<<<HTML
<a class="{$cls}" href="{$p['path']}" data-reveal>
  <span class="card__media">{picture}</span>
  <span class="card__body">
    <span class="card__meta"><span class="tag">{$p['category']}</span> <time datetime="{$p['published']}">{$date}</time> · {$p['reading']} min read</span>
    <h3>{$p['h1']}</h3>
    <p>{$p['excerpt']}</p>
    <span class="card__more">Read the guide {arrow}</span>
  </span>
</a>
HTML, ['{picture}' => $pic, '{arrow}' => icon('arrow')]);
}

function tool_card(array $t, int $i = 0): string
{
    $delay = ($i % 4) * 80;
    return fill(<<<HTML
<a class="card card--tool tilt" href="{$t['path']}" data-reveal style="--delay:{$delay}ms">
  <span class="card__glow"></span>
  <span class="card__icon card__icon--round">{icon}</span>
  <h3>{$t['name']}</h3>
  <p>{$t['description']}</p>
  <span class="card__more">Open tool {arrow}</span>
</a>
HTML, ['{icon}' => icon($t['icon']), '{arrow}' => icon('arrow')]);
}

/** Accordion FAQ list. */
function faq_list(array $faqs, string $id = 'faq'): string
{
    $out = '<div class="faq" id="' . e($id) . '">';
    foreach (array_values($faqs) as $i => $f) {
        $open = $i === 0 ? ' open' : '';
        $out .= '<details class="faq__item" data-reveal' . $open . '><summary><span>' . e($f['q']) . '</span>' . icon('chevron', 'ico faq__chev') . '</summary><div class="faq__a"><p>' . e($f['a']) . '</p></div></details>';
    }
    return $out . '</div>';
}

/** Full-width call to action band. */
function cta_band(string $title = 'Ready to see your property in a whole new light?', string $text = 'Consultations with Austin Landscape Lighting are free, fast and zero-pressure. Most homeowners are surprised how affordable a professional system can be.'): string
{
    return fill(<<<HTML
<section class="cta-band spotlight" data-spotlight>
  <div class="stars" data-stars></div>
  <div class="container cta-band__inner" data-reveal>
    <p class="eyebrow">Free design consultation</p>
    <h2 class="display">{$title}</h2>
    <p class="lede">{$text}</p>
    <div class="cta-band__actions">
      <a class="btn btn--primary btn--lg" href="/contact/">Schedule My Free Estimate {arrow}</a>
      <a class="btn btn--ghost btn--lg" href="{phone_href}">{phone_icon} Call {phone}</a>
    </div>
  </div>
</section>
HTML, ['{arrow}' => icon('arrow'), '{phone_href}' => BIZ['phone_href'], '{phone_icon}' => icon('phone'), '{phone}' => e(BIZ['phone_display'])]);
}

/** Contact / estimate form. Posts to /contact/send. */
function contact_form(string $heading = 'Request your free estimate', string $service = ''): string
{
    $opts = '<option value="">Select a service</option>';
    foreach (services() as $s) {
        $sel = $s['slug'] === $service ? ' selected' : '';
        $opts .= '<option value="' . e($s['name']) . '"' . $sel . '>' . e($s['name']) . '</option>';
    }
    $opts .= '<option value="Not sure yet">Not sure yet, need advice</option>';
    $areas = '<option value="">City</option>';
    foreach (areas() as $a) {
        $areas .= '<option value="' . e($a['city']) . '">' . e($a['city']) . '</option>';
    }
    $areas .= '<option value="Other">Other / nearby</option>';
    $ts = time();
    $status = '';
    if (isset($_GET['sent']) && $_GET['sent'] === '0') {
        $status = '<p class="form-status form-status--err" role="alert">Something went wrong sending your request. Please call us at ' . e(BIZ['phone_display']) . ' or email ' . e(BIZ['email']) . '.</p>';
    }
    return fill(<<<HTML
<form class="estimate-form" method="post" action="/contact/send" data-estimate-form novalidate>
  <h3>{$heading}</h3>
  <p class="estimate-form__note">A lighting designer replies within one business day. No spam, ever.</p>
  {$status}
  <div class="form-grid">
    <label class="field"><span>First name</span><input type="text" name="first_name" autocomplete="given-name" required maxlength="60"></label>
    <label class="field"><span>Last name</span><input type="text" name="last_name" autocomplete="family-name" required maxlength="60"></label>
    <label class="field"><span>Email</span><input type="email" name="email" autocomplete="email" required maxlength="120"></label>
    <label class="field"><span>Phone</span><input type="tel" name="phone" autocomplete="tel" required maxlength="30" placeholder="(512) 555-0100"></label>
    <label class="field"><span>Service</span><select name="service">{$opts}</select></label>
    <label class="field"><span>City</span><select name="city">{$areas}</select></label>
    <label class="field field--full"><span>Tell us about your property</span><textarea name="message" rows="4" maxlength="2000" placeholder="Front elevation, a few live oaks, a path to the front door..."></textarea></label>
  </div>
  <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="ts" value="{$ts}">
  <input type="hidden" name="page" value="">
  <button class="btn btn--primary btn--lg btn--block" type="submit">Request My Free Estimate {arrow}</button>
  <p class="estimate-form__fine">Or call <a href="{phone_href}">{phone}</a> · {hours}</p>
</form>
HTML, ['{arrow}' => icon('arrow'), '{phone_href}' => BIZ['phone_href'], '{phone}' => e(BIZ['phone_display']), '{hours}' => e(BIZ['hours'])]);
}

/** Two-column contact section used at the foot of most pages. */
function contact_section(string $eyebrow = 'Get started', string $title = 'Let\'s light up your Austin home', string $service = ''): string
{
    $form = contact_form('Request your free estimate', $service);
    return fill(<<<HTML
<section class="contact-section" id="contact">
  <div class="container contact-section__grid">
    <div class="contact-section__copy" data-reveal>
      <p class="eyebrow">{$eyebrow}</p>
      <h2 class="display">{$title}</h2>
      <p class="lede">Tell Austin Landscape Lighting a little about your property and we will schedule a free dusk walkthrough. You get a fixture-by-fixture design and a written, itemized estimate. The price we quote is the price you pay.</p>
      <ul class="contact-list">
        <li>{phone_icon}<div><strong>Call or text</strong><a href="{phone_href}">{phone}</a></div></li>
        <li>{mail_icon}<div><strong>Email</strong><a href="mailto:{email}">{email}</a></div></li>
        <li>{clock_icon}<div><strong>Hours</strong><span>{hours}</span></div></li>
        <li>{pin_icon}<div><strong>Based in Austin, TX</strong><span>Serving the greater Austin metro and Hill Country</span></div></li>
      </ul>
      <ul class="trust-row">
        <li>{shield} Licensed &amp; insured</li>
        <li>{warranty} 2-year workmanship warranty</li>
        <li>{star} 4.9 stars · 127 Google reviews</li>
      </ul>
    </div>
    <div class="contact-section__form" data-reveal style="--delay:120ms">{$form}</div>
  </div>
</section>
HTML, [
        '{phone_icon}' => icon('phone'), '{phone_href}' => BIZ['phone_href'], '{phone}' => e(BIZ['phone_display']),
        '{mail_icon}' => icon('mail'), '{email}' => e(BIZ['email']), '{clock_icon}' => icon('clock'), '{hours}' => e(BIZ['hours']),
        '{pin_icon}' => icon('pin'), '{shield}' => icon('shield', 'ico ico--sm'), '{warranty}' => icon('warranty', 'ico ico--sm'), '{star}' => icon('star', 'ico ico--sm'),
    ]);
}

/** "Lights off / lights on" comparison slider using one photo. */
function switch_compare(string $image, string $alt, string $caption = 'Drag to flip the switch'): string
{
    $pic = picture($image, $alt, ['sizes' => '(max-width: 900px) 100vw, 60vw']);
    $picOff = picture($image, '', ['sizes' => '(max-width: 900px) 100vw, 60vw']);
    return fill(<<<HTML
<div class="compare" data-compare>
  <div class="compare__after">{$pic}</div>
  <div class="compare__before" aria-hidden="true">{$picOff}<span class="compare__label compare__label--off">Lights off</span></div>
  <span class="compare__label compare__label--on">Lights on</span>
  <div class="compare__handle" aria-hidden="true"><span>{drag}</span></div>
  <input class="compare__range" type="range" min="0" max="100" value="38" aria-label="{$caption}">
  <p class="compare__hint">{$caption}</p>
</div>
HTML, ['{drag}' => icon('drag')]);
}

/** Horizontal scrolling marquee of served cities. */
function area_marquee(): string
{
    $items = '';
    foreach (areas() as $a) {
        $items .= '<a href="' . e($a['path']) . '">' . e($a['city']) . '</a><span class="dot">✦</span>';
    }
    return '<div class="marquee" aria-label="Cities served"><div class="marquee__track">' . $items . $items . '</div></div>';
}

/** Numbered stats row with count-up animation. */
function stats_row(): string
{
    return <<<HTML
<ul class="stats" data-reveal>
  <li><span class="stat__n"><span data-count="500">0</span>+</span><span class="stat__l">Projects lit across Austin</span></li>
  <li><span class="stat__n"><span data-count="4.9" data-decimals="1">0</span>★</span><span class="stat__l">Google rating · 127 reviews</span></li>
  <li><span class="stat__n"><span data-count="6">0</span> yrs</span><span class="stat__l">Designing light in Central Texas</span></li>
  <li><span class="stat__n"><span data-count="2">0</span>-year</span><span class="stat__l">Workmanship warranty</span></li>
</ul>
HTML;
}

function review_card(array $r, int $i = 0): string
{
    $delay = ($i % 3) * 90;
    $initial = strtoupper(substr($r['name'], 0, 1));
    return fill(<<<HTML
<figure class="review" data-reveal style="--delay:{$delay}ms">
  <div class="review__stars" aria-label="5 out of 5 stars">{stars}</div>
  <blockquote>{quote}<p>{$r['text']}</p></blockquote>
  <figcaption><span class="review__avatar">{$initial}</span><span><strong>{$r['name']}</strong><br><small>{$r['place']} · {$r['service']}</small></span></figcaption>
</figure>
HTML, ['{stars}' => str_repeat(icon('star', 'ico ico--star'), 5), '{quote}' => icon('quote', 'ico review__q')]);
}

function process_steps(): string
{
    $out = '<ol class="process" data-process>';
    foreach (PROCESS_STEPS as $i => [$t, $d]) {
        $n = $i + 1;
        $out .= '<li class="process__step" data-reveal style="--delay:' . ($i * 100) . 'ms"><span class="process__n">' . $n . '</span><div><h3>' . e($t) . '</h3><p>' . e($d) . '</p></div></li>';
    }
    return $out . '<span class="process__line"><span class="process__fill"></span></span></ol>';
}

/** Sidebar used on service, area and post pages. */
function sidebar(array $o = []): string
{
    $links = '';
    foreach (($o['links'] ?? []) as [$label, $path]) {
        $links .= '<li><a href="' . e($path) . '">' . e($label) . '</a></li>';
    }
    $linksBlock = $links ? '<div class="side-card"><h3>' . e($o['links_title'] ?? 'Related') . '</h3><ul class="side-links">' . $links . '</ul></div>' : '';
    $toc = '';
    foreach (($o['toc'] ?? []) as $t) {
        $toc .= '<li><a href="#' . e($t['id']) . '">' . e($t['text']) . '</a></li>';
    }
    $tocBlock = $toc ? '<div class="side-card side-card--toc" data-toc><h3>On this page</h3><ol>' . $toc . '</ol></div>' : '';
    $cta = fill(<<<HTML
<div class="side-card side-card--cta">
  <p class="eyebrow">Free consultation</p>
  <h3>Talk to a lighting designer</h3>
  <p>Austin Landscape Lighting walks your property at dusk, designs fixture by fixture and gives you a written estimate. No pressure.</p>
  <a class="btn btn--primary btn--block" href="/contact/">Get My Free Estimate {arrow}</a>
  <a class="side-card__phone" href="{phone_href}">{phone_icon} {phone}</a>
  <ul class="side-card__trust"><li>{check} Licensed &amp; insured</li><li>{check} 2-year workmanship warranty</li><li>{check} 4.9★ on Google (127 reviews)</li></ul>
</div>
HTML, ['{arrow}' => icon('arrow'), '{phone_href}' => BIZ['phone_href'], '{phone_icon}' => icon('phone', 'ico ico--sm'), '{phone}' => e(BIZ['phone_display']), '{check}' => icon('check', 'ico ico--sm')]);
    return '<aside class="sidebar">' . $tocBlock . $cta . $linksBlock . '</aside>';
}
