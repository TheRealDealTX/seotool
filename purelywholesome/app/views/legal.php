<?php /** @var array $doc @var array $crumbs */
$heroTitle = $doc['title']; $heroLede = '';
include __DIR__ . '/partials/page-hero.php'; ?>
<section class="section section--tight"><div class="wrap wrap--narrow prose"><?= $doc['html'] ?></div></section>
