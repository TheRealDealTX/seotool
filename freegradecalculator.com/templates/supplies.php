<?php
$groups = [
  ['Calculators approved for class & exams', 'calc', ['ti-84-plus-ce', 'ti-30xs', 'casio-fx-991ex', 'casio-fx-115es', 'ti-nspire-cx-ii']],
  ['Test prep books', 'book', ['sat-study-guide', 'act-prep-guide']],
  ['Study smarter', 'sparkle', ['straight-a-book', 'make-it-stick-book', 'index-cards', 'highlighters', 'sticky-notes', 'academic-planner']],
  ['Your study space', 'lamp', ['noise-cancelling-headphones', 'desk-lamp', 'laptop-stand', 'desk-whiteboard', 'visual-timer']],
  ['For teachers', 'apple', ['teacher-gradebook', 'grading-pens']],
];
page_start(['title' => 'Best Study Supplies & Calculators for Students (2026)', 'description' => 'Hand-picked calculators, test prep books and study gear for high school and college students, plus grading supplies for teachers.', 'path' => '/study-supplies', 'schema' => [breadcrumb_schema([['Home', '/'], ['Study supplies', '/study-supplies']])], 'image' => 'desk-with-books']);
?>
<section class="page-hero"><div class="hero-bg" aria-hidden="true"><div class="blob blob-1"></div><div class="blob blob-2"></div></div><div class="wrap"><?= breadcrumbs_html([['Home', '/'], ['Study supplies', '/study-supplies']]) ?><h1>Study supplies that actually help</h1><p class="lead">Our short list of calculators, books and gear that students and teachers rely on — no fluff, no filler.</p></div></section>
<div class="wrap" style="padding-bottom:40px">
  <?php foreach ($groups as [$title, $ic, $keys]): ?>
  <section class="cat-block"><div class="cat-title"><?= icon($ic) ?><h2><?= e($title) ?></h2></div><?= product_grid($keys) ?></section>
  <?php endforeach; ?>
  <div class="callout callout-info prose"><strong>Which calculator do I need?</strong><p>Check your syllabus first. Most high school algebra through precalculus classes use a TI-84 Plus CE; chemistry and physics often only need a scientific calculator like the TI-30XS. The SAT includes a built-in graphing calculator, and the ACT publishes its own calculator policy — check act.org before test day.</p></div>
</div>
<?php page_end();
