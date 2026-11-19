<?php defined('SNW') || (http_response_code(404) && exit); ?>
<section class="hero">
  <picture>
    <source media="(max-width: 700px)" srcset="/assets/img/brand/seattle-skyline-hero-sm.webp">
    <img class="hero-bg" src="/assets/img/brand/seattle-skyline-hero.webp" alt="Seattle skyline and Space Needle at dusk" width="1920" height="972" fetchpriority="high">
  </picture>
  <div class="wrap hero-inner">
    <p class="eyebrow light">Seattle Real Estate</p>
    <h1>Seattle Homes for Sale, Guided by Local Experts</h1>
    <p class="lead">From Ballard Craftsmans to Capitol Hill condos, find the right home — or the right buyer — with a team that knows every Seattle neighborhood.</p>
    <form class="hero-search" action="/homes-for-sale/" method="get" role="search">
      <label class="sr" for="hs-q">Search homes</label>
      <input id="hs-q" type="search" name="q" placeholder="Neighborhood, ZIP or keyword">
      <label class="sr" for="hs-type">Property type</label>
      <select id="hs-type" name="type"><option value="">All types</option><option>Single Family</option><option>Condo</option><option>Townhome</option></select>
      <label class="sr" for="hs-max">Max price</label>
      <select id="hs-max" name="max"><option value="">Any price</option><option value="750000">Up to $750K</option><option value="1000000">Up to $1M</option><option value="1500000">Up to $1.5M</option><option value="2500000">Up to $2.5M</option></select>
      <button class="btn btn-accent" type="submit">Search Homes</button>
    </form>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Featured Listings</p><h2>Homes for Sale in Seattle</h2></div>
      <a class="link-arrow" href="/homes-for-sale/">View all homes</a>
    </div>
    <div class="grid-3">
<?php foreach ($featured as $l) partial('listing-card', ['l' => $l]); ?>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap split">
    <div class="split-media"><img src="<?= photo('craftsman-home-twilight') ?>" alt="Seattle Craftsman home at twilight" width="1400" height="933" loading="lazy"></div>
    <div>
      <p class="eyebrow">Why Seattle Northwest Homes</p>
      <h2>A Seattle Real Estate Team That Puts You First</h2>
      <p>Buying or selling a home in Seattle moves fast. You deserve a team that answers quickly, explains every option in plain English and knows the difference between a Wallingford Craftsman and a West Seattle view home.</p>
      <ul class="checks">
        <li><strong>Local expertise</strong> — we live, work and play in the neighborhoods we sell.</li>
        <li><strong>Personalized approach</strong> — your goals shape the plan, not a script.</li>
        <li><strong>Transparent communication</strong> — clear updates on pricing, offers and timelines.</li>
        <li><strong>Extensive network</strong> — lenders, inspectors, stagers and contractors we trust.</li>
        <li><strong>Hassle-free experience</strong> — we coordinate the details so you can focus on the move.</li>
      </ul>
      <a class="btn btn-primary" href="/about-seattle-northwest-homes/">Meet the Team</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap two-up">
    <article class="panel">
      <img src="/assets/img/blog/for-buyers-sm.webp" alt="Couple touring a home for sale in Seattle" width="720" height="480" loading="lazy">
      <div class="panel-body">
        <p class="eyebrow">For Buyers</p>
        <h2>Find the Seattle Home That Fits Your Life</h2>
        <p>Buying a home is one of the biggest financial decisions you'll make. Share your wish list and we'll send a tailored list of homes, flag the neighborhoods that match your commute and budget, and guide you from offer to keys.</p>
        <a class="btn btn-primary" href="/buy-a-home-in-seattle/">Tell Us Your Dream Home</a>
      </div>
    </article>
    <article class="panel">
      <img src="/assets/img/blog/for-sellers-sm.webp" alt="Seattle home sold by Seattle Northwest Homes" width="720" height="480" loading="lazy">
      <div class="panel-body">
        <p class="eyebrow">For Sellers</p>
        <h2>Sell Your Seattle Home with Confidence</h2>
        <p>Timing, pricing and presentation decide your result. We'll review recent sales near you, recommend the prep that pays off and market your home to the buyers most likely to pay top dollar.</p>
        <a class="btn btn-primary" href="/sell-your-home-seattle/">Get a Free Home Value Review</a>
      </div>
    </article>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Neighborhood Guides</p><h2>Explore Seattle Neighborhoods</h2></div>
      <a class="link-arrow" href="/neighborhoods/">All neighborhoods</a>
    </div>
    <div class="hood-grid">
<?php foreach (array_slice(neighborhoods(), 0, 8, true) as $s => $h): ?>
      <a class="hood-tile" href="/neighborhoods/<?= $s ?>/">
        <img src="<?= photo($h['image'], true) ?>" alt="Homes in <?= e($h['name']) ?>, Seattle" width="720" height="480" loading="lazy">
        <span><strong><?= e($h['name']) ?></strong><small><?= e($h['area']) ?></small></span>
      </a>
<?php endforeach ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">From the Blog</p><h2>Latest Seattle Real Estate Advice</h2></div>
      <a class="link-arrow" href="/blog/">Read the blog</a>
    </div>
    <div class="grid-3">
<?php foreach ($latest as $p) partial('post-card', ['p' => $p]); ?>
    </div>
  </div>
</section>
<?php partial('cta') ?>
