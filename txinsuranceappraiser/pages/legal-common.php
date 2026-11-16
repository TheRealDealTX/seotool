<?php
/** Shared renderer for privacy / terms. */
function render_legal(string $file, string $h1, string $title, string $desc, string $path): void
{
    $body = (string) file_get_contents(ROOT . '/content/legal/' . $file . '.html');
    $body = preg_replace_callback('#<h2>(.*?)</h2>#', function ($m) {
        $id = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower(strip_tags($m[1]))), '-');
        return '<h2 id="' . $id . '">' . rtrim($m[1], ':') . '</h2>';
    }, $body);
    ob_start(); ?>
<section class="hero hero-sm"><div class="orb orb-1"></div><div class="wrap hero-in"><div>
  <span class="eyebrow anim">Legal</span><h1 class="anim"><?= e($h1) ?></h1>
  <p class="lead anim">TX Insurance Appraisals LLC · Last updated <?= date('F j, Y', filemtime(ROOT . '/content/legal/' . $file . '.html')) ?></p>
</div></div></section>
<div class="wrap narrow section"><article class="prose"><?= $body ?>
<h2 id="contact">Contact</h2><p>Questions? Email <a href="mailto:<?= SITE['email'] ?>"><?= SITE['email'] ?></a> or call <a href="tel:<?= SITE['phone_href'] ?>"><?= e(SITE['phone']) ?></a>.</p></article></div>
<?php
    render_page(['title' => $title, 'description' => $desc, 'path' => $path,
        'crumbs' => [['Home', '/'], [$h1, $path]], 'schema' => [schema_webpage('WebPage', $title, $desc, $path)]], (string) ob_get_clean());
}
