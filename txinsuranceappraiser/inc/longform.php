<?php
declare(strict_types=1);

/**
 * Long-form page: hero, prose body with sticky TOC + CTA sidebar, optional FAQ, CTA band.
 * $p: title, description, path, h1, eyebrow, lead, image, body (HTML), faqs, crumbs, schema, faq_heading, related (html)
 */
function render_longform(array $p): void
{
    ob_start(); ?>
<div class="progress" aria-hidden="true"></div>
<section class="hero hero-split">
  <div class="hero-bg" style="background-image:url(<?= e($p['image']) ?>)"></div>
  <div class="orb orb-1"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim"><?= e($p['eyebrow']) ?></span>
      <h1 class="anim"><?= e($p['h1']) ?></h1>
      <p class="lead anim"><?= e($p['lead']) ?></p>
      <div class="hero-actions anim">
        <a class="btn btn-gold btn-lg" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 20) ?> <?= e(SITE['phone_short']) ?></a>
        <a class="btn btn-ghost-light btn-lg" href="/contact-us/">Free claim review <?= icon('arrow', 18) ?></a>
      </div>
    </div>
    <div class="hero-img anim"><img src="<?= e($p['image']) ?>" alt="<?= e($p['image_alt'] ?? $p['h1']) ?>" width="800" height="420" fetchpriority="high"></div>
  </div>
</section>
<div class="wrap post-layout">
  <article class="prose">
    <?= $p['body'] ?>
  </article>
  <aside class="sidebar">
    <div class="sticky">
      <nav class="toc" aria-label="On this page"><h2>On this page</h2><ol data-toc></ol></nav>
      <div class="side-cta">
        <h3>Free claim review</h3>
        <p style="font-size:.95rem">Send us your carrier estimate — we’ll tell you honestly if appraisal can close the gap.</p>
        <a class="btn btn-gold btn-block" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 18) ?> <?= e(SITE['phone_short']) ?></a>
        <a class="btn btn-ghost-light btn-block" style="margin-top:10px" href="/contact-us/">Request a review</a>
      </div>
      <?= $p['side_extra'] ?? '' ?>
    </div>
  </aside>
</div>
<?= $p['related'] ?? '' ?>
<?php if (!empty($p['faqs'])) echo faq_html($p['faqs'], $p['faq_heading'] ?? 'Frequently Asked Questions'); ?>
<?= cta_band($p['cta_heading'] ?? '', $p['cta_text'] ?? '') ?>
<?php
    $content = (string) ob_get_clean();
    $schema = $p['schema'] ?? [];
    if (!empty($p['faqs'])) {
        $schema[] = schema_faq($p['faqs']);
    }
    render_page([
        'title' => $p['title'], 'description' => $p['description'], 'path' => $p['path'],
        'image' => $p['image'], 'crumbs' => $p['crumbs'], 'schema' => $schema,
    ], $content);
}

/** Card grid of other services (used at the foot of service pages). */
function services_strip(string $exclude = ''): string
{
    $all = [
        'appraisal' => ['scale', 'Insurance Appraisal', 'Your appraiser under the policy’s appraisal clause.'],
        'umpire' => ['gavel', 'Umpire Services', 'A neutral umpire when appraisers reach an impasse.'],
        'matterport' => ['cube', 'Matterport 3D Scans', 'Measurable 3D documentation of the damage.'],
        'xactimate-estimate' => ['calc', 'Xactimate Estimates', 'Line-item estimates in the carriers’ own format.'],
        'symbility-estimate' => ['doc', 'Symbility Estimates', 'Estimates for CoreLogic-based carriers.'],
    ];
    $out = '<section class="section bg-mist"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">More services</span><h2>Related services from TX Insurance Appraiser</h2></div><div class="grid g4">';
    foreach ($all as $slug => [$ic, $t, $d]) {
        if ($slug === $exclude) continue;
        $out .= '<a class="card tilt reveal" style="text-decoration:none" href="/services/' . $slug . '/"><div class="ic-badge">' . icon($ic, 26) . '</div><h3>' . e($t) . '</h3><p>' . e($d) . '</p><span class="link-arrow">Learn more ' . icon('arrow', 16) . '</span></a>';
    }
    return $out . '</div></div></section>';
}
