<?php
/** expects $L = [title, description, path, updated, html] */
page_start(['title' => $L[0] . ' | ' . SITE_NAME, 'description' => $L[1], 'path' => $L[2], 'schema' => [breadcrumb_schema([['Home', '/'], [$L[0], $L[2]]])]]);
?>
<section class="page-hero"><div class="wrap"><?= breadcrumbs_html([['Home', '/'], [$L[0], $L[2]]]) ?><h1><?= e($L[0]) ?></h1><p class="lead">Last updated <?= e($L[3]) ?></p></div></section>
<div class="wrap"><div class="prose legal" style="padding-bottom:40px"><?= $L[4] ?></div></div>
<?php page_end();
