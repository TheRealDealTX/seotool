<?php
$slug = trim($path, '/');
$title = $slug === 'privacy-policy' ? 'Privacy Policy' : 'Terms of Use';
[$crumbs, $crumb_schema] = breadcrumbs([['Home', '/'], [$title, null]]);
layout_start(['title' => $title, 'description' => $title . ' for ' . cfg('name') . '.', 'path' => $path, 'schema' => [$crumb_schema]]);
?>
<section class="page-hero page-hero-sm"><div class="wrap narrow"><?= $crumbs ?><h1><?= e($title) ?></h1></div></section>
<section class="section section-tight"><div class="wrap narrow prose"><?= file_get_contents(APP . "/data/pages/$slug.html") ?></div></section>
<?php layout_end();
