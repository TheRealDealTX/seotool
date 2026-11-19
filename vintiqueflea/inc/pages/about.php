<?php
page_start([
    'title' => 'About Vintique Flea | Curated Indoor Vintage Market in Houston',
    'description' => 'Vintique Flea was founded by the creators of Rice Village Flea: a curated indoor market of vintage, mid-century, salvage and decor at Silver Street Studios.',
    'path' => '/about/',
]);
add_schema(['@type' => 'AboutPage', 'name' => 'About Vintique Flea', 'url' => abs_url('/about/')]);
?>
<div class="wrap">
  <?= breadcrumbs([['About', '/about/']]) ?>
  <header class="page-head">
    <h1>About Vintique Flea</h1>
    <p class="lede">The best curated indoor marketplace of interesting things in Houston, from the people who created Rice Village Flea.</p>
  </header>
  <div class="layout-2">
    <article class="prose">
      <h2>Our story</h2>
      <p>Vintique Flea was founded by the team behind Rice Village Flea. We wanted to build something bigger and more curated: an indoor market where every booth is worth stopping at. The result is a marketplace of interesting things, including <a href="/shop/mid-century-modern/">mid-century modern</a>, <a href="/shop/vintage-clothing/">vintage clothing</a>, <a href="/shop/architectural-salvage-industrial/">architectural salvage and industrial</a>, <a href="/shop/rustic-home-decor/">rustic home decor</a>, <a href="/food-trucks/">local food trucks</a>, and more.</p>
      <h2>Our home: Silver Street Studios</h2>
      <p>We're proud that our home has always been Silver Street Studios at 2000 Edwards Street, in the heart of Houston's <a href="/guides/washington-avenue-arts-district/">Washington Avenue Arts District</a>. The building's industrial bones, with high ceilings, concrete floors and working artist studios all around, make it the perfect backdrop for salvage, vintage and design.</p>
      <h2>What "curated" means to us</h2>
      <ul>
        <li><strong>Real vintage and real craft.</strong> We favor genuine vintage, antiques, salvage and handmade goods over mass-produced imports.</li>
        <li><strong>Variety in every aisle.</strong> We balance categories so you'll find furniture, fashion, records and decor at every edition.</li>
        <li><strong>Local first.</strong> Houston dealers, makers and food trucks are the heart of the market.</li>
        <li><strong>Community.</strong> Past editions have supported local causes like the Love, Molly Fund animal rescue.</li>
      </ul>
      <h2>Beyond the market</h2>
      <p>Between editions, this site is where the hunt continues: <a href="/shop/">curated finds you can shop online</a>, <a href="/guides/">guides to vintage shopping and decorating</a>, and <a href="/play/">games for vintage lovers</a>.</p>
    </article>
    <aside class="side">
      <div class="side-card">
        <h2>Come see us</h2>
        <address><?= e(VENUE['name']) ?><br><?= e(VENUE['street']) ?><br><?= e(VENUE['city']) ?>, <?= e(VENUE['region']) ?> <?= e(VENUE['postal']) ?></address>
        <a class="btn btn--primary btn--block" href="/events/">Market dates</a>
      </div>
      <div class="side-card">
        <h2>Join the market</h2>
        <a class="btn btn--ghost btn--block" href="/vendors/">Become a vendor</a>
      </div>
    </aside>
  </div>
</div>
<?php page_end();
