<?php
/** @var array $page */
$title = seo_title($page);
$desc = $page['description'] ?? '';
$canonical = url($page['path']);
$robots = !empty($page['noindex']) ? 'noindex, follow' : 'index, follow, max-image-preview:large, max-snippet:-1';
$ogType = ($page['_type'] ?? '') === 'post' ? 'article' : 'website';
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<?php if ($desc): ?><meta name="description" content="<?= e($desc) ?>">
<?php endif; ?>
<meta name="robots" content="<?= e($robots) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= $ogType ?>">
<meta property="og:title" content="<?= e($page['og_title'] ?? $title) ?>">
<?php if ($desc): ?><meta property="og:description" content="<?= e($desc) ?>">
<?php endif; ?>
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:site_name" content="<?= e(cfg('site_name')) ?>">
<meta property="og:image" content="<?= e(og_image($page)) ?>">
<?php if ($ogType === 'article'): ?>
<meta property="article:published_time" content="<?= e(iso_date($page['date'] ?? null)) ?>">
<meta property="article:modified_time" content="<?= e(iso_date($page['updated'] ?? $page['date'] ?? null)) ?>">
<meta property="article:author" content="<?= e(url('/author/joseph-dittman/')) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($page['og_title'] ?? $title) ?>">
<?php if ($desc): ?><meta name="twitter:description" content="<?= e($desc) ?>">
<?php endif; ?>
<meta name="twitter:image" content="<?= e(og_image($page)) ?>">
<meta name="theme-color" content="#10243A">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/img/logo-mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="<?= e(cfg('site_name')) ?> Blog" href="<?= e(url('/feed/')) ?>">
<link rel="preload" href="/assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v=<?= e(asset_version('css/site.css')) ?>">
<?php foreach ($page['head_extra'] ?? [] as $extra) echo $extra, "\n"; ?>
<?= json_ld($page) ?>

<?php if (cfg('analytics_id')): ?>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= e(cfg('analytics_id')) ?>"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','<?= e(cfg('analytics_id')) ?>',{anonymize_ip:true});</script>
<?php endif; ?>
</head>
