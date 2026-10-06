<?php
defined('SLT') || exit;

function e($s): string { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

function abs_url(string $path): string { return SITE_URL . $path; }

function asset(string $path): string { return '/assets/' . $path . '?v=' . ASSET_VER; }

/** JSON-LD graph collected while a page renders. */
$GLOBALS['SCHEMA'] = [];
$GLOBALS['FAQ'] = [];
function add_schema(array $node): void { $GLOBALS['SCHEMA'][] = $node; }

function fmt_date(string $ymd): string { return date('F j, Y', strtotime($ymd)); }

function reading_time(string $html): int {
    return max(2, (int)round(str_word_count(strip_tags($html)) / 230));
}

function tel_link(string $cls = ''): string {
    return '<a class="' . e($cls) . '" href="tel:' . PHONE_TEL . '">' . icon('phone') . '<span>' . PHONE . '</span></a>';
}

/** Section eyebrow + heading block. */
function section_head(string $eyebrow, string $title, string $sub = '', string $align = 'center'): void {
    echo '<div class="sec-head sec-head--' . $align . '" data-reveal>';
    if ($eyebrow) echo '<span class="eyebrow">' . e($eyebrow) . '</span>';
    echo '<h2 class="sec-title">' . $title . '</h2>';
    if ($sub) echo '<p class="sec-sub">' . $sub . '</p>';
    echo '</div>';
}

/** Breadcrumbs: [['Home','/'], ['Blog','/blog/'], ['Post', null]] */
function breadcrumbs(array $items): string {
    $list = [];
    $html = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    foreach ($items as $i => [$name, $href]) {
        $last = $i === count($items) - 1;
        $html .= '<li>' . ($last || !$href ? '<span aria-current="page">' . e($name) . '</span>' : '<a href="' . e($href) . '">' . e($name) . '</a>') . '</li>';
        $node = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name];
        if ($href) $node['item'] = abs_url($href);
        $list[] = $node;
    }
    add_schema(['@type' => 'BreadcrumbList', 'itemListElement' => $list]);
    return $html . '</ol></nav>';
}

/** Inner-page hero. */
function page_hero(array $o): void {
    $img = $o['img'] ?? 'Spring-Landscape-Lighting-BG-1.webp';
    echo '<section class="phero' . (!empty($o['tall']) ? ' phero--tall' : '') . '" data-spotlight>';
    echo '<div class="phero__bg" data-parallax="0.25"><img src="/assets/img/' . e($img) . '" alt="" fetchpriority="high"></div>';
    echo '<div class="phero__shade"></div><canvas class="fireflies" data-count="26" aria-hidden="true"></canvas>';
    echo '<div class="wrap phero__inner">';
    if (!empty($o['crumbs'])) echo breadcrumbs($o['crumbs']);
    if (!empty($o['eyebrow'])) echo '<span class="eyebrow eyebrow--glow" data-reveal>' . e($o['eyebrow']) . '</span>';
    echo '<h1 class="phero__title" data-split>' . $o['title'] . '</h1>';
    if (!empty($o['sub'])) echo '<p class="phero__sub" data-reveal data-delay="2">' . $o['sub'] . '</p>';
    if (!empty($o['meta'])) echo '<div class="phero__meta" data-reveal data-delay="3">' . $o['meta'] . '</div>';
    if (!empty($o['cta'])) {
        echo '<div class="btn-row" data-reveal data-delay="3"><a class="btn btn--glow" href="/quote/" data-magnetic>' . icon('sparkles') . 'Get a Free Lighting Plan</a>';
        echo '<a class="btn btn--ghost" href="tel:' . PHONE_TEL . '">' . icon('phone') . PHONE . '</a></div>';
    }
    echo '</div><div class="phero__fade"></div></section>';
}

function cta_box(string $h = 'Get a lighting plan for your property', string $t = 'Tell us about your home and what you would like to see after dark. We will follow up to schedule a complimentary consultation.'): void {
    echo '<aside class="cta-box" data-reveal><div class="cta-box__glow"></div><div class="cta-box__body">';
    echo '<span class="eyebrow">' . e(BRAND) . '</span><h3>' . e($h) . '</h3><p>' . e($t) . '</p>';
    echo '<div class="btn-row"><a class="btn btn--glow" href="/quote/">' . icon('sparkles') . 'Request a Free Consultation</a>';
    echo '<a class="btn btn--ghost" href="tel:' . PHONE_TEL . '">' . icon('phone') . PHONE . '</a></div></div></aside>';
}

function faq_block(array $items, string $title = 'Frequently asked questions', bool $heading = true): void {
    if ($heading) echo '<h2 id="faq">' . e($title) . '</h2>';
    echo '<div class="faq" data-reveal>';
    foreach ($items as [$q, $a]) {
        echo '<details class="faq__item"><summary><span>' . e($q) . '</span><i class="faq__icon" aria-hidden="true"></i></summary><div class="faq__a"><p>' . e($a) . '</p></div></details>';
        $GLOBALS['FAQ'][] = ['@type' => 'Question', 'name' => $q, 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $a]];
    }
    echo '</div>';
}

/** Embed an interactive tool widget (markup in app/tools/{slug}.php, behaviour in tools.js). */
function tool_embed(string $slug, bool $framed = true): void {
    $f = APP . '/tools/' . $slug . '.php';
    if (!is_file($f)) return;
    $GLOBALS['USES_TOOLS'] = true;
    if ($framed) echo '<div class="tool-embed" data-reveal><div class="tool-embed__head">' . icon(TOOLS[$slug]['icon'] ?? 'sparkles') . '<span>Interactive tool</span><strong>' . e(TOOLS[$slug]['name'] ?? '') . '</strong></div>';
    include $f;
    if ($framed) echo '</div>';
}

function img_small(string $img): string {
    $sm = str_replace('.webp', '-960.webp', $img);
    return '/assets/img/' . (is_file(PUB . '/assets/img/' . $sm) ? $sm : $img);
}

function post_url(string $slug): string { return '/' . $slug . '/'; }

/** Blog card. */
function post_card(string $slug, array $p, string $cls = ''): string {
    $cat = CATEGORIES[$p['cat']]['name'] ?? '';
    return '<article class="pcard ' . $cls . '" data-reveal data-tilt><a class="pcard__img" href="' . post_url($slug) . '" tabindex="-1" aria-hidden="true"><img src="' . img_small($p['img']) . '" alt="" loading="lazy" width="960" height="640"></a>'
        . '<div class="pcard__body"><div class="pcard__meta"><a href="/category/' . e($p['cat']) . '/">' . e($cat) . '</a><span>' . fmt_date($p['date']) . '</span></div>'
        . '<h3><a href="' . post_url($slug) . '">' . e($p['title']) . '</a></h3><p>' . e($p['excerpt']) . '</p>'
        . '<a class="link-arrow" href="' . post_url($slug) . '">Read article ' . icon('arrow-right') . '</a></div></article>';
}

function service_card(string $slug, array $s, int $i = 0): string {
    return '<a class="scard" href="/services/' . $slug . '/" data-reveal data-delay="' . ($i % 3) . '" data-tilt>'
        . '<span class="scard__num">' . str_pad((string)($i + 1), 2, '0', STR_PAD_LEFT) . '</span>'
        . '<span class="scard__icon">' . icon($s['icon']) . '</span><h3>' . e($s['name']) . '</h3><p>' . e($s['blurb']) . '</p>'
        . '<span class="link-arrow">Explore ' . icon('arrow-up-right') . '</span><span class="scard__glow"></span></a>';
}

function tool_card(string $slug, array $t, int $i = 0): string {
    return '<a class="tcard" href="/tools/' . $slug . '/" data-reveal data-delay="' . ($i % 3) . '" data-tilt>'
        . '<span class="tcard__icon">' . icon($t['icon']) . '</span><div><h3>' . e($t['name']) . '</h3><p>' . e($t['desc']) . '</p></div>'
        . '<span class="tcard__go">' . icon('arrow-up-right') . '</span></a>';
}

/** Quote form. $compact for sidebars. */
function quote_form(string $id = 'quote', bool $compact = false): void {
    $ts = time();
    $sig = hash_hmac('sha256', (string)$ts, form_secret());
    ?>
<form class="qform<?= $compact ? ' qform--compact' : '' ?>" id="<?= e($id) ?>-form" method="post" action="/quote/" data-qform novalidate>
  <input type="hidden" name="ts" value="<?= $ts ?>"><input type="hidden" name="sig" value="<?= $sig ?>">
  <input type="hidden" name="source" value="<?= e($_SERVER['REQUEST_URI'] ?? '/') ?>">
  <div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <div class="qform__grid">
    <label class="fld"><span>Full name</span><input type="text" name="name" required autocomplete="name" placeholder="Jane Smith"></label>
    <label class="fld"><span>Phone</span><input type="tel" name="phone" required autocomplete="tel" placeholder="(281) 555-0123"></label>
    <label class="fld"><span>Email</span><input type="email" name="email" required autocomplete="email" placeholder="you@example.com"></label>
    <label class="fld"><span>Project type</span><select name="project">
      <option value="">Select a service</option>
      <?php foreach (SERVICES as $s) echo '<option>' . e($s['name']) . '</option>'; ?>
      <option>Complete new lighting system</option><option>Not sure yet</option></select></label>
    <?php if (!$compact): ?>
    <label class="fld"><span>Neighborhood / city</span><input type="text" name="area" placeholder="e.g. Gleannloch Farms"></label>
    <label class="fld"><span>Best time to reach you</span><select name="time"><option>Any time</option><option>Morning</option><option>Afternoon</option><option>Evening</option></select></label>
    <?php endif; ?>
    <label class="fld fld--full"><span>Project details</span><textarea name="message" rows="<?= $compact ? 3 : 4 ?>" placeholder="What would you like to light? Front elevation, trees, patio, pool, repairs…"></textarea></label>
  </div>
  <button class="btn btn--glow btn--block" type="submit" data-magnetic><?= icon('sparkles') ?><span>Request My Free Consultation</span></button>
  <p class="qform__note"><?= icon('shield-check') ?> No obligation. We never share your details. Or call <a href="tel:<?= PHONE_TEL ?>"><?= PHONE ?></a>.</p>
  <div class="qform__status" role="status" aria-live="polite"></div>
</form>
<?php
}

function form_secret(): string {
    $f = APP . '/data/secret.php';
    if (is_file($f)) { $s = include $f; if (is_string($s) && strlen($s) > 20) return $s; }
    $s = bin2hex(random_bytes(24));
    // If the data dir isn't writable, fall back to a stable per-install value.
    if (@file_put_contents($f, "<?php return '" . $s . "';\n") === false) $s = hash('sha256', __DIR__ . SITE_URL . 'slt-form');
    return $s;
}

/** Process steps used on several pages. */
const PROCESS = [
    ['Consultation',        'compass',        'We talk through your goals, budget and how you actually use each outdoor space after dark.'],
    ['Property walkthrough','footprints',     'We study architecture, trees, beds, viewing angles, power access, drainage and irrigation.'],
    ['Custom lighting plan','layers',         'Techniques, fixture locations, beam spreads, color temperature, zones and controls, all mapped out.'],
    ['Clear proposal',      'clipboard-list', 'A straightforward scope and recommendation for the planned system, with no surprises.'],
    ['Clean installation',  'hammer',         'Professional low-voltage components, concealed wire, protected beds and a tidy site.'],
    ['Night review',        'moon',           'We return after dark to fine-tune aim, brightness and glare until the balance is right.'],
];

function process_strip(bool $compact = false): void {
    echo '<ol class="process' . ($compact ? ' process--compact' : '') . '">';
    foreach (PROCESS as $i => [$t, $ic, $d]) {
        echo '<li class="process__step" data-reveal data-delay="' . ($i % 3) . '"><span class="process__n">' . str_pad((string)($i + 1), 2, '0', STR_PAD_LEFT) . '</span><span class="process__ic">' . icon($ic) . '</span><h3>' . e($t) . '</h3><p>' . e($d) . '</p></li>';
    }
    echo '</ol>';
}

/** Big closing CTA band. */
function cta_band(string $title = 'Ready to see your home in a new light?', string $sub = 'Let’s design an outdoor space you’ll love after dark.'): void {
    ?>
<section class="ctaband" data-spotlight>
  <div class="ctaband__bg" data-parallax="0.18"><img src="/assets/img/Spring-Landscape-Lighting-BG-2.webp" alt="" loading="lazy"></div>
  <div class="ctaband__shade"></div><canvas class="fireflies" data-count="34" aria-hidden="true"></canvas>
  <div class="wrap ctaband__inner">
    <span class="eyebrow eyebrow--glow" data-reveal>Complimentary consultation</span>
    <h2 class="ctaband__title" data-split><?= $title ?></h2>
    <p data-reveal data-delay="1"><?= $sub ?></p>
    <div class="btn-row btn-row--center" data-reveal data-delay="2">
      <a class="btn btn--glow btn--lg" href="/quote/" data-magnetic><?= icon('sparkles') ?>Get a Free Lighting Plan</a>
      <a class="btn btn--ghost btn--lg" href="tel:<?= PHONE_TEL ?>"><?= icon('phone') ?><?= PHONE ?></a>
    </div>
  </div>
</section>
<?php
}

/** Insert ids on h2s and return [html, toc]. */
function with_toc(string $html): array {
    $toc = []; $used = [];
    $html = preg_replace_callback('#<h2(?: id="([^"]*)")?>(.*?)</h2>#s', function ($m) use (&$toc, &$used) {
        $text = trim(strip_tags($m[2]));
        $id = $m[1] ?: trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($text)), '-');
        $base = $id; $n = 2; while (isset($used[$id])) $id = $base . '-' . $n++;
        $used[$id] = 1; $toc[] = [$id, $text];
        return '<h2 id="' . $id . '">' . $m[2] . '</h2>';
    }, $html);
    return [$html, $toc];
}
