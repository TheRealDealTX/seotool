<?php
/** @var array $page */
$meta = $page;
require __DIR__ . '/header.php';
?>
<section class="err-hero">
  <div class="big">404</div>
  <h1>This side hustle doesn't exist (yet)</h1>
  <p>The page you're looking for has moved or never existed. Try one of these instead:</p>
  <div class="btn-row" style="justify-content:center">
    <a class="btn" href="/">Home</a>
    <a class="btn btn-outline" href="/blog/">All guides</a>
    <a class="btn btn-green" href="/tools/side-hustle-quiz/">Take the quiz</a>
  </div>
</section>
<?php require __DIR__ . '/footer.php'; ?>
