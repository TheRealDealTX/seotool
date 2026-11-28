<?php
$schema = [breadcrumb_schema([['Home', '/'], ['All calculators', '/tools']]), ['@type' => 'ItemList', 'itemListElement' => array_values(array_map(fn($s, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url('/' . $s), 'name' => tools()[$s][0]], array_keys(tools()), range(0, count(tools()) - 1)))]];
page_start(['title' => 'All Free Grade, GPA & Study Calculators (29 Tools)', 'description' => 'Browse 29 free calculators for students and teachers: weighted grades, final exam, GPA, grade curves, ACT/SAT scores, percentages, fractions and study timers.', 'path' => '/tools', 'schema' => $schema]);
?>
<section class="page-hero"><div class="hero-bg" aria-hidden="true"><div class="blob blob-1"></div><div class="blob blob-2"></div></div>
  <div class="wrap" style="text-align:center">
    <?= breadcrumbs_html([['Home', '/'], ['All calculators', '/tools']]) ?>
    <h1>Every calculator a student needs</h1>
    <p class="lead" style="margin:0 auto 22px">29 free tools for grades, GPA, test scores, math and studying. Filter by category or start typing.</p>
    <div class="tool-search"><?= icon('search') ?><input id="tool-filter" type="search" placeholder="Search calculators… (e.g. final, gpa, curve)" aria-label="Filter calculators"></div>
    <div class="filter-bar" role="group" aria-label="Category" style="justify-content:center"><button type="button" data-cat="all" aria-pressed="true">All</button><?php foreach (tool_categories() as $k => $c): ?><button type="button" data-cat="<?= e($k) ?>" aria-pressed="false"><?= e($c[0]) ?></button><?php endforeach; ?></div>
  </div>
</section>
<div class="wrap" style="padding-bottom:40px">
<?php foreach (tool_categories() as $ck => [$cname, $cdesc, $cic]): ?>
  <section class="cat-block" id="<?= e($ck) ?>">
    <div class="cat-title"><?= icon($cic) ?><div><h2><?= e($cname) ?></h2><p class="muted" style="margin:0"><?= e($cdesc) ?></p></div></div>
    <div class="tool-grid"><?php foreach (tools() as $s => $t) if ($t[1] === $ck) include ROOT . '/templates/partials/tool-card.php'; ?></div>
  </section>
<?php endforeach; ?>
</div>
<?php page_end();
