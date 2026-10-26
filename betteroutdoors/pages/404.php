<?php defined('BO') || exit;
header('Content-Type: text/html; charset=utf-8');
page_head(['title' => 'Page Not Found | Better Outdoors', 'desc' => 'This page could not be found. Browse Better Outdoors bow reviews, guides and free archery tools.', 'path' => '/404/', 'robots' => 'noindex, follow']);
?>
<section class="nf">
  <div class="wrap">
    <div class="big-num">404</div>
    <h1>Looks like this arrow missed the target</h1>
    <p>The page you were looking for has moved or doesn&rsquo;t exist. Try one of these instead:</p>
    <div class="btn-row" style="justify-content:center;margin-bottom:40px">
      <a class="btn btn-orange" href="/">Better Outdoors Home</a>
      <a class="btn btn-outline" href="/blog/">All Guides</a>
      <a class="btn btn-outline" href="/tools/">Free Tools</a>
    </div>
    <div class="post-grid" style="text-align:left">
<?php foreach (array_slice($POSTS, 0, 3, true) as $s => $p) echo post_card($s, $p); ?>
    </div>
  </div>
</section>
<?php page_foot(false); ?>
