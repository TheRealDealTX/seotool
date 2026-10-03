<?php component('page-hero', ['page' => $page]); ?>
<section class="section">
  <div class="container narrow center">
    <p class="lead">Sorry&mdash;we couldn't find that page. It may have moved during our website update.</p>
    <form class="search-404" action="/blog/" method="get" role="search">
      <label for="q404" class="sr-only">Search articles</label>
      <input id="q404" type="search" name="q" placeholder="Search articles (e.g. hail, denied claim)">
      <button class="btn btn-gold" type="submit">Search</button>
    </form>
    <div class="chip-list chip-list-center">
      <a class="chip" href="/">Home</a>
      <a class="chip" href="/services/">Services</a>
      <a class="chip" href="/blog/">Blog</a>
      <a class="chip" href="/claim-tools/">Claim Tools</a>
      <a class="chip" href="/weather/">Live Weather</a>
      <a class="chip" href="/contact/">Contact</a>
    </div>
    <p><a class="btn btn-gold" href="/free-claim-review/">Get a Free Claim Review</a></p>
  </div>
</section>
