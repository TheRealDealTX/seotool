<?php defined('M1S') || exit; ?>
<div class="narrow center error-page">
  <p class="error-code"><?= (int)$code ?></p>
  <h1><?= e($heading) ?></h1>
  <p class="lede"><?= e($message) ?></p>
  <form class="search-big" action="/search/" method="get"><input type="search" name="q" placeholder="Search guides and discussions" aria-label="Search"><button class="btn btn-accent">Search</button></form>
  <p><a class="btn btn-ghost" href="/blog/">Read the blog</a> <a class="btn btn-ghost" href="/forum/">Visit the forum</a></p>
</div>
