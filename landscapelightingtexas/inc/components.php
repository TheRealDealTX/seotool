<?php
// Reusable page components. Content files call these directly.
defined('LLT') or die(http_response_code(404));

/** Inline stroke icons (24x24, currentColor). */
function icon(string $name, int $size = 20): string {
    static $paths = [
        'phone'    => '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
        'mail'     => '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
        'clock'    => '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        'pin'      => '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
        'calendar' => '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
        'check'    => '<path d="M20 6 9 17l-5-5"/>',
        'arrow'    => '<path d="M5 12h14M13 5l7 7-7 7"/>',
        'star'     => '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor" stroke="none"/>',
        'home'     => '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
        'tree'     => '<path d="M12 22v-7"/><path d="M12 15a6 6 0 0 0 6-6 6 6 0 0 0-3-5.2A4 4 0 0 0 9 3.8 6 6 0 0 0 6 9a6 6 0 0 0 6 6z"/>',
        'path'     => '<path d="M8 3c-2 6 4 12 0 18M16 3c2 6-4 12 0 18"/><path d="M12 6v1M12 11v2M12 17v1"/>',
        'water'    => '<path d="M2 16c2 0 2-1.5 4-1.5S8 16 10 16s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M2 20c2 0 2-1.5 4-1.5S8 20 10 20s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M12 3s4 4.5 4 7.5a4 4 0 0 1-8 0C8 7.5 12 3 12 3z"/>',
        'patio'    => '<path d="M3 7c3 2 6 2 9 0s6-2 9 0"/><circle cx="6" cy="9" r="1"/><circle cx="12" cy="8" r="1"/><circle cx="18" cy="9" r="1"/><path d="M5 21v-6h14v6M12 15v6"/>',
        'smart'    => '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/><path d="M9 9a4 4 0 0 1 6 0M10.5 11a2 2 0 0 1 3 0"/>',
        'shield'   => '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
        'wrench'   => '<path d="M14.7 6.3a4 4 0 0 0 5 5L22 14l-8 8-2.3-2.3a4 4 0 0 0-5-5L2 10l8-8z" transform="scale(.9) translate(1 1)"/>',
        'calc'     => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15v4M8 19h4"/>',
        'sliders'  => '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
        'sun'      => '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
        'bolt'     => '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
        'beam'     => '<path d="M12 21 5 4h14z"/><path d="M12 21v-4"/>',
        'leaf'     => '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.2-6"/>',
        'spark'    => '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>',
        'bulb'     => '<path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>',
        'award'    => '<circle cx="12" cy="8" r="6"/><path d="M8.2 13.9 7 22l5-3 5 3-1.2-8.1"/>',
        'users'    => '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
        'play'     => '<path d="m6 3 14 9-14 9z"/>',
        'moon'     => '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
    ];
    $p = $paths[$name] ?? $paths['spark'];
    return '<svg class="icon" viewBox="0 0 24 24" width="' . $size . '" height="' . $size . '" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}

/** Section heading block. */
function section_head(string $eyebrow, string $title, string $lead = '', string $align = 'center'): void {
    echo '<div class="section-head align-' . $align . '">';
    if ($eyebrow) echo '<p class="eyebrow reveal">' . e($eyebrow) . '</p>';
    echo '<h2 class="section-title reveal">' . $title . '</h2>';
    if ($lead) echo '<p class="section-lead reveal">' . $lead . '</p>';
    echo '</div>';
}

/** FAQ accordion. $items = [[question, answer-html], ...]. Also feeds FAQPage schema. */
function faqs(array $items, string $title = 'Frequently Asked Questions', string $eyebrow = 'FAQ'): void {
    foreach ($items as $it) $GLOBALS['FAQ_SCHEMA'][] = $it;
    echo '<section class="section faq-section"><div class="container narrow">';
    if ($title) section_head($eyebrow, e($title));
    echo '<div class="faq-list">';
    foreach ($items as $i => [$q, $a]) {
        echo '<details class="faq reveal"' . ($i === 0 ? ' open' : '') . '><summary><span>' . e($q) . '</span><i aria-hidden="true"></i></summary><div class="faq-a">' . (str_starts_with(trim($a), '<') ? $a : '<p>' . $a . '</p>') . '</div></details>';
    }
    echo '</div></div></section>';
}

/** Big call-to-action band used at the end of most pages. */
function cta_band(string $title = 'Ready to See Your Property in a New Light?', string $text = ''): void {
    $text = $text ?: 'Book a free dusk consultation. A ' . SITE_NAME . ' designer will walk your property at nightfall, show you what is possible and send a clear, itemized quote.';
    ?>
<section class="cta-band">
  <div class="cta-band-bg" data-parallax="0.15"><img src="/assets/img/oak-tree-uplighting-1600.webp" alt="" loading="lazy" width="1536" height="1024"></div>
  <div class="container cta-band-inner">
    <p class="eyebrow reveal">Free Consultation</p>
    <h2 class="reveal"><?= $title ?></h2>
    <p class="reveal"><?= $text ?></p>
    <div class="hero-actions reveal">
      <a class="btn btn-gold btn-lg magnetic" href="/quote/">Get My Free Quote</a>
      <a class="btn btn-ghost btn-lg" href="<?= PHONE_HREF ?>"><?= icon('phone') ?> <?= PHONE ?></a>
    </div>
  </div>
</section>
<?php
}

/** Grid of service cards. $exclude = slug to leave out. */
function service_cards(string $exclude = '', int $limit = 99): void {
    global $SERVICES;
    echo '<div class="card-grid services-grid">';
    $n = 0;
    foreach ($SERVICES as $slug => [$name, $blurb, $img, $ic]) {
        if ($slug === $exclude || $n++ >= $limit) continue;
        echo '<a class="svc-card reveal tilt" href="/services/' . $slug . '/">'
           . '<div class="svc-img"><img src="' . img_url($img, 800) . '" alt="' . e($name) . ' by ' . SITE_NAME . '" loading="lazy" width="800" height="533"></div>'
           . '<div class="svc-body"><span class="svc-icon">' . icon($ic, 22) . '</span><h3>' . e($name) . '</h3><p>' . e($blurb) . '</p>'
           . '<span class="link-arrow">Explore ' . icon('arrow', 16) . '</span></div></a>';
    }
    echo '</div>';
}

function tool_cards(string $exclude = ''): void {
    global $TOOLS;
    echo '<div class="card-grid tools-grid">';
    foreach ($TOOLS as $href => [$name, $blurb, $ic]) {
        if ($href === $exclude) continue;
        echo '<a class="tool-card reveal glow-card" href="' . $href . '"><span class="tool-icon">' . icon($ic, 26) . '</span><h3>' . e($name) . '</h3><p>' . e($blurb) . '</p><span class="link-arrow">Open tool ' . icon('arrow', 16) . '</span></a>';
    }
    echo '</div>';
}

function area_cards(string $exclude = ''): void {
    global $AREAS;
    echo '<div class="card-grid areas-grid">';
    foreach ($AREAS as $slug => [$name, $region, $cities]) {
        if ($slug === $exclude) continue;
        echo '<a class="area-card reveal glow-card" href="/areas/' . $slug . '/"><span class="area-region">' . e($region) . '</span><h3>' . e($name) . ' Landscape Lighting</h3><p>' . e(implode(' · ', array_slice($cities, 0, 5))) . '</p><span class="link-arrow">View area ' . icon('arrow', 16) . '</span></a>';
    }
    echo '</div>';
}

function post_card(array $p): string {
    return '<a class="post-card reveal" href="' . $p['path'] . '"><div class="post-card-img"><img src="' . img_url($p['image'], 800) . '" alt="' . e($p['h1']) . '" loading="lazy" width="800" height="533"></div>'
         . '<div class="post-card-body"><p class="post-card-meta">' . fmt_date($p['date']) . '</p><h3>' . e($p['h1']) . '</h3><p>' . e($p['description']) . '</p><span class="link-arrow">Read article ' . icon('arrow', 16) . '</span></div></a>';
}

function related_posts(string $exclude = '', int $n = 3, string $title = 'Keep Reading'): void {
    $posts = array_filter(posts(), fn($p) => $p['path'] !== $exclude);
    $posts = array_slice($posts, 0, $n);
    echo '<section class="section related"><div class="container">';
    section_head('From the blog', $title);
    echo '<div class="card-grid posts-grid">';
    foreach ($posts as $p) echo post_card($p);
    echo '</div></div></section>';
}

/** Checklist. */
function checklist(array $items, string $class = ''): string {
    $h = '<ul class="checklist ' . $class . '">';
    foreach ($items as $it) $h .= '<li>' . icon('check', 18) . '<span>' . $it . '</span></li>';
    return $h . '</ul>';
}

/** Animated number stats. $items = [[number, suffix, label], ...] */
function stats(array $items): void {
    echo '<div class="stats">';
    foreach ($items as [$num, $suffix, $label]) {
        echo '<div class="stat reveal"><p class="stat-num"><span data-count="' . e($num) . '">0</span>' . e($suffix) . '</p><p class="stat-label">' . e($label) . '</p></div>';
    }
    echo '</div>';
}

/** Image + text split section. */
function split(string $img, string $alt, string $html, bool $reverse = false, string $class = ''): void {
    echo '<div class="split ' . ($reverse ? 'is-reverse ' : '') . $class . '">'
       . '<figure class="split-media reveal"><img src="' . img_url($img, 1600) . '" alt="' . e($alt) . '" loading="lazy" width="1536" height="1024"></figure>'
       . '<div class="split-body">' . $html . '</div></div>';
}

/** Before/after slider using one photo: left side shows the property unlit. */
function before_after(string $img, string $alt): void {
    ?>
<div class="ba reveal" data-ba>
  <img class="ba-after" src="<?= img_url($img) ?>" alt="<?= e($alt) ?>" loading="lazy" width="1536" height="1024">
  <div class="ba-before" aria-hidden="true"><img src="<?= img_url($img) ?>" alt="" loading="lazy" width="1536" height="1024"></div>
  <span class="ba-tag ba-tag-l">Without lighting</span><span class="ba-tag ba-tag-r">With Landscape Lighting</span>
  <div class="ba-handle" aria-hidden="true"><span></span></div>
  <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Drag to compare unlit and lit">
</div>
<?php
}

/** Testimonials (from the original site). */
function testimonials(): void {
    $reviews = [
        ['The transformation was stunning. We had guests over the weekend after installation and every single one commented on how gorgeous our home looked at night. Worth every penny.', 'Michael R.', 'Austin, TX', 'Architectural Uplighting'],
        ['Professional from start to finish. They came at dusk to see how light behaved in our garden, designed a plan on the spot, and the install team was immaculate — not a single plant disturbed.', 'Sandra L.', 'Houston, TX', 'Garden & Path Lighting'],
        ['Our pool area went from functional to resort-like. The underwater lighting combined with the surrounding landscape lights creates an atmosphere we never imagined was possible in a Texas backyard.', 'James T.', 'Dallas, TX', 'Pool & Landscape Lighting'],
        ['The smart system they installed is phenomenal. I control everything from my phone — schedules, brightness, even color temperature for different moods.', 'Christine P.', 'San Antonio, TX', 'Smart Lighting System'],
        ['We\'ve had our system for three years now. Not a single issue — it just works beautifully every night. When one fixture needed adjusting, they came out same week, no charge.', 'Brian D.', 'Fort Worth, TX', 'Full Property Lighting'],
        ['Our live oak trees look absolutely spectacular at night. The uplighting creates this cathedral-like canopy effect that guests stop and photograph. Best investment we\'ve made in our property.', 'Angela R.', 'Plano, TX', 'Tree & Garden Lighting'],
    ];
    echo '<div class="reviews" data-carousel><div class="reviews-track">';
    foreach ($reviews as [$q, $n, $c, $s]) {
        $initials = implode('', array_map(fn($w) => $w[0], explode(' ', $n)));
        echo '<figure class="review glow-card"><div class="stars" aria-label="5 out of 5 stars">' . str_repeat(icon('star', 16), 5) . '</div>'
           . '<blockquote>“' . e($q) . '”</blockquote><figcaption><span class="avatar">' . e($initials) . '</span><span><strong>' . e($n) . '</strong><small>' . e($c) . ' · ' . e($s) . '</small></span></figcaption></figure>';
    }
    echo '</div><div class="reviews-nav"><button type="button" data-prev aria-label="Previous review">←</button><button type="button" data-next aria-label="Next review">→</button></div></div>';
}

/** The quote form. Posts to /quote/ (handled by inc/quote-handler.php). */
function quote_form(string $heading = 'Request Your Free Quote', string $source = ''): void {
    global $SERVICES;
    $t = time();
    ?>
<form class="quote-form glow-card" method="post" action="/quote/" data-quote-form novalidate>
  <div class="qf-head"><p class="qf-title"><?= e($heading) ?></p><p class="qf-sub">We respond within 1 business day</p></div>
  <div class="qf-grid">
    <label class="field"><span>First name</span><input name="first_name" autocomplete="given-name" required></label>
    <label class="field"><span>Last name</span><input name="last_name" autocomplete="family-name"></label>
    <label class="field"><span>Email</span><input type="email" name="email" autocomplete="email" required></label>
    <label class="field"><span>Phone</span><input type="tel" name="phone" autocomplete="tel" inputmode="tel" required></label>
    <label class="field"><span>City, TX</span><input name="city" autocomplete="address-level2" placeholder="e.g. Austin"></label>
    <label class="field"><span>Service interest</span>
      <select name="service">
        <option value="">Select a service…</option>
        <?php foreach ($SERVICES as $s) echo '<option>' . e($s[0]) . '</option>'; ?>
        <option>Full Property Package</option>
        <option>Not Sure — Help Me Decide</option>
      </select>
    </label>
    <label class="field field-full"><span>Tell us about your project</span><textarea name="message" rows="4" placeholder="Trees, facade, pool, pathways, budget, timing…"></textarea></label>
  </div>
  <div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="t" value="<?= $t ?>">
  <input type="hidden" name="source" value="<?= e($source) ?>">
  <button class="btn btn-gold btn-block magnetic" type="submit">Send My Free Quote Request <?= icon('arrow', 18) ?></button>
  <p class="qf-note">🔒 Your information is private. We never share or sell your data.</p>
  <div class="qf-status" role="status" aria-live="polite"></div>
</form>
<?php
}

/** Prose figure with caption. */
function figure(string $img, string $alt, string $caption = ''): string {
    return '<figure class="prose-figure reveal"><img src="' . img_url($img, 1600) . '" alt="' . e($alt) . '" loading="lazy" width="1536" height="1024">'
         . ($caption ? '<figcaption>' . $caption . '</figcaption>' : '') . '</figure>';
}

/** Call-out box inside prose. $kind = tip | note | warn */
function callout(string $html, string $kind = 'tip', string $title = ''): string {
    $titles = ['tip' => 'Pro tip', 'note' => 'Good to know', 'warn' => 'Watch out'];
    return '<aside class="callout callout-' . $kind . '"><p class="callout-title">' . icon($kind === 'warn' ? 'shield' : 'bulb', 18) . ' ' . e($title ?: $titles[$kind]) . '</p>' . $html . '</aside>';
}

/** Inline tool promo inside prose. */
function tool_promo(string $href): string {
    global $TOOLS;
    [$name, $blurb, $ic] = $TOOLS[$href];
    return '<a class="tool-promo" href="' . $href . '"><span class="tool-icon">' . icon($ic, 24) . '</span><span><strong>Try it: ' . e($name) . '</strong><small>' . e($blurb) . '</small></span>' . icon('arrow', 18) . '</a>';
}
