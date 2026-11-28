<?php page_start(['title' => 'Page Not Found | Free Grade Calculator', 'description' => 'This page could not be found.', 'path' => '/404', 'noindex' => true]); ?>
<section class="err-hero"><div class="wrap"><div class="big">404</div><h1 style="font-size:1.8rem">This page dropped the class.</h1><p class="muted">The page you’re looking for doesn’t exist or has moved. Try one of these instead:</p>
<div class="hero-cta" style="justify-content:center;margin:20px 0 36px"><a class="btn btn-primary" href="/"><?= icon('home') ?> Grade calculator</a><button class="btn btn-ghost search-open" type="button"><?= icon('search') ?> Search tools</button></div>
<div class="tool-grid" style="text-align:left"><?php foreach (array_slice(array_filter(tools(), fn($t) => $t[4]), 0, 6, true) as $s => $t) include ROOT . '/templates/partials/tool-card.php'; ?></div></div></section>
<?php page_end();
