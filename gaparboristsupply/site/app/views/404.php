<?php
defined('GAP') || exit;
$meta = ['title' => 'Page not found', 'noindex' => true];
?>
<section class="notfound wrap">
  <svg viewBox="0 0 300 200" class="nf-art" aria-hidden="true"><path class="nf-rope" d="M150 0 V120"/><circle cx="150" cy="132" r="12"/><path d="M60 190 Q150 150 240 190" class="nf-ground"/></svg>
  <h1>This branch doesn't hold weight</h1>
  <p>The page you were looking for has moved or never existed. Try a search, or head back down to solid ground.</p>
  <form class="search search-lg" action="/search/" method="get" role="search"><label class="sr" for="q404">Search</label><input id="q404" name="q" type="search" placeholder="Search gear"><button type="submit" aria-label="Search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg></button></form>
  <p><a class="btn btn-chain" href="/">Back to the homepage</a></p>
</section>
