<?php
/**
 * SHARED <head> FOR EVERY PUBLIC PAGE.
 *
 * ▸ To add a site-wide tracking script, Meta Pixel, verification meta tag or any
 *   other <head> code, paste it in the "SITE-WIDE HEAD CODE" block below. It will
 *   appear on every public page (home, directory, events, articles, forms, 404).
 *   The admin area uses its own layout, so these scripts never load there.
 *
 * ▸ Pages set $page BEFORE including this file:
 *     $page = [
 *       'title'       => 'Page title',            // " | Rodeo Texas" is appended
 *       'title_full'  => false,                    // true = use title as-is
 *       'description' => 'Meta description',
 *       'canonical'   => '/path/',                 // absolute or site-relative
 *       'robots'      => 'index,follow',
 *       'og_type'     => 'website' | 'article',
 *       'og_image'    => '/assets/img/og-default.png',
 *       'og_image_alt'=> '…',
 *       'jsonld'      => [ [...schema...], … ],    // arrays, encoded safely here
 *       'head_extra'  => '<link …>',               // trusted, page-specific markup
 *       'body_class'  => 'page-event',
 *     ];
 */
defined('RT_APP') || exit;

$page = $page ?? [];
$siteName = (string) cfg('site_name', 'Rodeo Texas');
$__title = trim((string) ($page['title'] ?? ''));
$__fullTitle = $__title === '' ? $siteName . ' — Texas Rodeo Schedule & Event Directory'
    : (!empty($page['title_full']) ? $__title : $__title . ' | ' . $siteName);
$__desc = (string) ($page['description'] ?? 'Find upcoming rodeos across Texas — professional, amateur, youth and ranch rodeos with dates, venues, show times and official links.');
$__canonical = abs_url((string) ($page['canonical'] ?? request_path()));
$__robots = (string) ($page['robots'] ?? 'index,follow,max-image-preview:large');
$__ogImage = abs_url((string) ($page['og_image'] ?? '/assets/img/og-default.png'));
$__ogAlt = (string) ($page['og_image_alt'] ?? 'Rodeo Texas — find rodeos across the Lone Star State');
$__ogType = (string) ($page['og_type'] ?? 'website');
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($__fullTitle) ?></title>
<meta name="description" content="<?= e($__desc) ?>">
<link rel="canonical" href="<?= e($__canonical) ?>">
<meta name="robots" content="<?= e($__robots) ?>">
<meta name="theme-color" content="#7a3b1b">

<meta property="og:site_name" content="<?= e($siteName) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($__ogType) ?>">
<meta property="og:title" content="<?= e($__title !== '' ? $__title : $__fullTitle) ?>">
<meta property="og:description" content="<?= e($__desc) ?>">
<meta property="og:url" content="<?= e($__canonical) ?>">
<meta property="og:image" content="<?= e($__ogImage) ?>">
<meta property="og:image:alt" content="<?= e($__ogAlt) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($__title !== '' ? $__title : $__fullTitle) ?>">
<meta name="twitter:description" content="<?= e($__desc) ?>">
<meta name="twitter:image" content="<?= e($__ogImage) ?>">

<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/zilla-slab-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="<?= e(asset('assets/css/site.css')) ?>">
<?= $page['head_extra'] ?? '' ?>

<?php foreach ((array) ($page['jsonld'] ?? []) as $__ld): if (!$__ld) { continue; } ?>
<script type="application/ld+json"><?= json_encode($__ld, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP) ?></script>
<?php endforeach; ?>

<!-- ============ SITE-WIDE HEAD CODE (tracking, pixels, verification) ============ -->
<!-- Google Analytics 4 / Google tag (carried over from the previous site) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BYZKZGNG2D"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-BYZKZGNG2D');
  gtag('config', 'GT-MRQHZ43M');
</script>
<!-- Add more site-wide scripts or <meta name="…-verification"> tags here. -->
<!-- ============================================================================ -->
</head>
<body class="<?= e($page['body_class'] ?? '') ?>">
