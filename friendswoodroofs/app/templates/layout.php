<?php
/** @var array $page  @var string $content */
$isHome    = $page['path'] === '/';
$noindex   = !empty($page['noindex']) || !config('indexable', true);
$canonical = empty($page['is_404']) ? abs_url($page['path']) : null;
$ogImage   = !empty($page['image']) ? abs_url('/assets/img/' . $page['image'] . '-1600.webp') : abs_url('/assets/img/og-default.jpg');
$ogImageW  = !empty($page['image']) ? 1600 : 1200;
$ogImageH  = !empty($page['image']) ? 1067 : 630;
$hasForm   = !empty($page['form']) && $page['template'] !== 'thank-you';
?>
<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($page['title']) ?></title>
<meta name="description" content="<?= e($page['description']) ?>">
<?php if ($noindex): ?>
<meta name="robots" content="noindex, follow">
<?php endif; ?>
<?php if ($canonical): ?>
<link rel="canonical" href="<?= e($canonical) ?>">
<?php endif; ?>
<meta property="og:site_name" content="<?= e(config('name')) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($page['og_type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($page['title']) ?>">
<meta property="og:description" content="<?= e($page['description']) ?>">
<?php if ($canonical): ?>
<meta property="og:url" content="<?= e($canonical) ?>">
<?php endif; ?>
<meta property="og:image" content="<?= e($ogImage) ?>">
<meta property="og:image:width" content="<?= $ogImageW ?>">
<meta property="og:image:height" content="<?= $ogImageH ?>">
<?php if (!empty($page['article'])): ?>
<meta property="article:published_time" content="<?= e($page['article']['date_iso']) ?>">
<meta property="article:section" content="<?= e($page['article']['category']) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($page['title']) ?>">
<meta name="twitter:description" content="<?= e($page['description']) ?>">
<meta name="twitter:image" content="<?= e($ogImage) ?>">
<meta name="theme-color" content="#0f2340">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<?php if ($isHome): ?>
<link rel="preload" as="image" href="/assets/img/hero-roofing-crew-960.webp" imagesrcset="/assets/img/hero-roofing-crew-480.webp 480w, /assets/img/hero-roofing-crew-960.webp 960w, /assets/img/hero-roofing-crew-1600.webp 1600w" imagesizes="100vw" fetchpriority="high">
<?php endif; ?>
<link rel="stylesheet" href="<?= e(asset('assets/css/site.css')) ?>">
<script src="<?= e(asset('assets/js/site.js')) ?>" defer></script>
<?= json_ld($page['schema'] ?? []) ?>
</head>
<body class="page-<?= e($page['template']) ?>">
<a class="skip-link" href="#main">Skip to main content</a>
<?php partial('header', ['page' => $page]); ?>
<main id="main" tabindex="-1">
<?php if (!empty($page['breadcrumbs'])) { partial('breadcrumbs', ['trail' => $page['breadcrumbs']]); } ?>
<?= $content ?>
</main>
<?php partial('footer', ['page' => $page]); ?>
<?php partial('mobile-bar', ['hasForm' => $hasForm]); ?>
</body>
</html>
