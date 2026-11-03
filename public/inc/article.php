<?php
/**
 * Article renderer. Content files (content/*.php) return an array:
 *   title, description, h1, kicker, lede, published, updated, image, image_alt,
 *   takeaways[] , body (HTML), faq[[q,a]], related[] (paths), affiliate (bool),
 *   tool (tool id shown above the body), schema_extra[] (extra graph nodes)
 * Inside body, <!--tool:ID--> embeds an interactive tool widget.
 */
defined('SCC') || (http_response_code(404) && exit);

function tool_widget(string $id, array &$scripts): string
{
    $f = ROOT . "/pages/tools/$id.widget.php";
    if (!is_file($f)) return '';
    $scripts[] = 'js/tools/common.js';
    $scripts[] = "js/tools/$id.js";
    ob_start();
    include $f;
    return '<div class="tool-embed reveal" id="tool">' . ob_get_clean() . '</div>';
}

/** Adds ids to h2/h3 and returns [html, toc]. */
function prepare_body(string $html): array
{
    $toc = [];
    $seen = [];
    $html = preg_replace_callback('#<h([23])(\s[^>]*)?>(.*?)</h\1>#s', function ($m) use (&$toc, &$seen) {
        $attrs = $m[2] ?? '';
        if (preg_match('/id="([^"]+)"/', $attrs, $idm)) {
            $id = $idm[1];
        } else {
            $id = slugify($m[3]) ?: 'section';
            $base = $id; $i = 2;
            while (isset($seen[$id])) $id = $base . '-' . $i++;
            $attrs .= ' id="' . $id . '"';
        }
        $seen[$id] = true;
        if ($m[1] === '2') $toc[] = [$id, trim(strip_tags($m[3]))];
        return "<h{$m[1]}$attrs>{$m[3]}</h{$m[1]}>";
    }, $html);
    return [$html, $toc];
}

function reading_minutes(string $html): int
{
    return max(3, (int) round(str_word_count(strip_tags($html)) / 230));
}

function render_article(string $path, string $source, string $section, array $opt = []): void
{
    $a = article($source);
    if (!$a) { not_found(); }
    $scripts = [];
    $body = $a['body'] ?? '';
    // Embeds
    $body = preg_replace_callback('/<!--tool:([a-z0-9-]+)-->/', function ($m) use (&$scripts) {
        return tool_widget($m[1], $scripts);
    }, $body);
    [$body, $toc] = prepare_body($body);
    $minutes = reading_minutes($body . ($a['lede'] ?? ''));

    [$secName, $secUrl] = SECTIONS[$section] ?? ['', '/'];
    $crumbs = [['Home', '/']];
    if ($section === 'tools') {
        $crumbs[] = ['Tools', '/tools/'];
    } elseif ($secName) {
        $crumbs[] = ['Guides', '/solar-camera-guides/'];
    }
    $crumbs[] = [$a['crumb'] ?? $a['h1'], $path];

    $published = $a['published'] ?? BUILD_DATE;
    $updated = $a['updated'] ?? BUILD_DATE;
    $image = $a['image'] ?? 'og-default';

    $schema = [];
    $schema[] = breadcrumb_schema($crumbs);
    $schema[] = [
        '@type' => $section === 'tools' ? 'WebPage' : 'Article',
        '@id' => abs_url($path) . '#main',
        'headline' => $a['h1'],
        'description' => $a['description'],
        'image' => img_url($image),
        'datePublished' => $published . 'T08:00:00+00:00',
        'dateModified' => $updated . 'T08:00:00+00:00',
        'author' => ['@type' => 'Organization', 'name' => 'Solar CCTV Camera Editorial Team', 'url' => abs_url('/about-us/')],
        'publisher' => ['@id' => SITE_ORIGIN . '/#organization'],
        'mainEntityOfPage' => abs_url($path),
        'isPartOf' => ['@id' => SITE_ORIGIN . '/#website'],
        'inLanguage' => 'en-US',
    ] + (!empty($a['keyword']) ? ['keywords' => $a['keyword']] : []);
    if (!empty($a['faq'])) {
        $schema[] = [
            '@type' => 'FAQPage',
            'mainEntity' => array_map(fn($f) => [
                '@type' => 'Question', 'name' => $f[0],
                'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f[1], '<a><b><strong><em><br>')],
            ], $a['faq']),
        ];
    }
    foreach ($a['schema_extra'] ?? [] as $node) $schema[] = $node;
    if (!empty($opt['schema'])) foreach ($opt['schema'] as $node) $schema[] = $node;

    $topTool = '';
    if (!empty($opt['tool'])) $topTool = tool_widget($opt['tool'], $scripts);
    elseif (!empty($a['tool'])) $topTool = tool_widget($a['tool'], $scripts);

    page_head([
        'title' => $a['title'],
        'description' => $a['description'],
        'path' => $path,
        'image' => img_url($image),
        'type' => $section === 'tools' ? 'website' : 'article',
        'schema' => $schema,
        'published' => $published,
        'updated' => $updated,
        'body_class' => 'is-article' . ($section === 'tools' ? ' is-tool' : ''),
    ]);
    ?>
<section class="article-hero<?= $section === 'tools' ? ' tool-hero' : '' ?>">
  <div class="hero-sky" aria-hidden="true"><span class="hero-sun"></span></div>
  <div class="wrap article-hero-inner">
    <?= breadcrumbs_html($crumbs) ?>
    <span class="kicker"><?= icon($a['icon'] ?? ($section === 'tools' ? 'calc' : 'sun'), 16) ?> <?= e($a['kicker'] ?? $secName) ?></span>
    <h1><?= e($a['h1']) ?></h1>
    <p class="lede"><?= $a['lede'] ?? '' ?></p>
    <div class="meta-row">
      <span><?= icon('clock', 16) ?> <?= $section === 'tools' ? 'Free · runs in your browser' : $minutes . ' min read' ?></span>
      <span><?= icon('refresh', 16) ?> Updated <time datetime="<?= e($updated) ?>"><?= e(fmt_date($updated)) ?></time></span>
      <span><?= icon('shield', 16) ?> Independent · no paid placements</span>
    </div>
  </div>
</section>
<?php if ($topTool): ?>
<section class="wrap tool-top"><?= $topTool ?></section>
<?php endif; ?>
<div class="wrap article-layout">
  <aside class="toc-col">
<?php if (count($toc) > 2): ?>
    <nav class="toc" aria-label="On this page">
      <p class="toc-title">On this page</p>
      <ol>
<?php foreach ($toc as [$id, $label]): ?>
        <li><a href="#<?= e($id) ?>"><?= e($label) ?></a></li>
<?php endforeach; ?>
      </ol>
    </nav>
<?php endif; ?>
    <div class="side-tools">
      <p class="toc-title">Free tools</p>
<?php foreach (array_slice(tools_meta(), 0, 4) as $t): ?>
      <a href="<?= e($t['path']) ?>"><?= icon($t['icon'], 16) ?> <?= e($t['short']) ?></a>
<?php endforeach; ?>
    </div>
  </aside>
  <article class="prose">
<?php if (empty($topTool) && !empty($a['image']) && $section !== 'tools'): ?>
    <figure class="hero-figure"><?= img($a['image'], $a['image_alt'] ?? $a['h1'], ['eager' => true, 'sizes' => '(max-width: 900px) 100vw, 760px']) ?></figure>
<?php endif; ?>
<?php if (!empty($a['affiliate'])): ?>
    <p class="disclosure"><?= icon('alert', 16) ?> Some links on this page are affiliate links. If you buy through them we may earn a commission at no extra cost to you. <a href="/affiliate-disclosure/">How we stay independent</a>.</p>
<?php endif; ?>
<?php if (!empty($a['takeaways'])): ?>
    <div class="takeaways reveal">
      <p class="takeaways-title"><?= icon('zap', 18) ?> Quick answer</p>
      <ul>
<?php foreach ($a['takeaways'] as $t): ?>
        <li><?= $t ?></li>
<?php endforeach; ?>
      </ul>
    </div>
<?php endif; ?>
    <?= $body ?>
<?php if (!empty($a['faq'])): ?>
    <section class="faq" aria-labelledby="faq">
      <h2 id="faq">Frequently asked questions</h2>
<?php foreach ($a['faq'] as [$q, $ans]): ?>
      <details class="reveal">
        <summary><?= e($q) ?></summary>
        <div><p><?= $ans ?></p></div>
      </details>
<?php endforeach; ?>
    </section>
<?php endif; ?>
    <div class="author-box">
      <span class="brand-mark"><?= icon('sun', 22) ?></span>
      <div>
        <p><strong>Solar CCTV Camera Editorial Team</strong></p>
        <p>We research solar security cameras full-time: manufacturer specs, solar irradiance data, installer documentation and owner reports. We do not accept paid placements. <a href="/about-us/">How we work</a>.</p>
      </div>
    </div>
  </article>
</div>
<?php
    $related = [];
    foreach ($a['related'] ?? [] as $rp) {
        $r = routes()[$rp] ?? null;
        if ($r && $r[0] === 'article') {
            $x = article($r[1]); $x['path'] = $rp; $x['section'] = $r[2]; $related[] = $x;
        }
    }
    if (count($related) < 3) {
        foreach (articles() as $p => $x) {
            if ($p === $path || in_array($p, $a['related'] ?? [], true)) continue;
            if ($x['section'] === $section || count($related) < 3) $related[] = $x;
            if (count($related) >= 3) break;
        }
    }
    ?>
<section class="related">
  <div class="wrap">
    <h2 class="section-title">Keep reading</h2>
    <div class="card-grid">
<?php foreach (array_slice($related, 0, 3) as $x) echo article_card($x); ?>
    </div>
  </div>
</section>
<?php
    cta_band();
    page_foot(array_unique($scripts));
}

function cta_band(): void
{
    ?>
<section class="cta-band">
  <div class="wrap cta-inner reveal">
    <div>
      <h2>Size your solar camera before you buy</h2>
      <p>Seven free calculators: panel angle for your latitude, battery days without sun, 4G data use, coverage, camera count and true 5-year cost.</p>
    </div>
    <a class="btn btn-sun btn-lg" href="/tools/"><?= icon('calc', 20) ?> Open the tools</a>
  </div>
</section>
<?php
}
