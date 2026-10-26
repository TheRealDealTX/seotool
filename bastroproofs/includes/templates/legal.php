<?php
/** Legal/utility page template. Expects $legal = [title, description, path, h1, lead, html]. */
require_once dirname(__DIR__) . '/bootstrap.php';
$crumbs = [['Home', '/'], [$legal['h1'], $legal['path']]];
page_start([
    'title'       => $legal['title'],
    'description' => $legal['description'],
    'path'        => $legal['path'],
    'robots'      => $legal['robots'] ?? 'index, follow',
    'schema'      => [breadcrumb_schema($crumbs)],
]);
page_hero('Bastrop Roofing', $legal['h1'], $legal['lead'], $crumbs);
?>
<section class="section">
  <div class="container narrow prose">
    <?= $legal['html'] ?>
  </div>
</section>
<?php page_end();
