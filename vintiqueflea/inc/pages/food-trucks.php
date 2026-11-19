<?php
page_start([
    'title' => 'Houston Food Trucks at Vintique Flea | Eat, Drink & Shop',
    'description' => 'Local Houston food trucks, beer and wine at Vintique Flea in the Washington Avenue Arts District. Plus how food trucks can apply for a spot at the market.',
    'path' => '/food-trucks/',
]);
$picks = [
    ['name' => 'Insulated Picnic Backpack', 'q' => 'insulated picnic backpack', 'note' => 'Pack drinks for a day of market-hopping.', 'icon' => '🎒', 'tier' => '$'],
    ['name' => 'Retro Enamel Camp Mugs', 'q' => 'enamel camp mugs retro', 'note' => 'Vintage-style mugs for coffee on the go.', 'icon' => '☕', 'tier' => '$'],
    ['name' => 'Texas Hot Sauce Sampler', 'q' => 'texas hot sauce gift set', 'note' => 'Bring the food truck heat home.', 'icon' => '🌶️', 'tier' => '$'],
    ['name' => 'Insulated Tumbler', 'q' => 'insulated tumbler with lid', 'note' => 'Iced drinks that survive a Houston afternoon.', 'icon' => '🥤', 'tier' => '$'],
];
$faq = [
    ['q' => 'Are there food trucks at Vintique Flea?', 'a' => 'Yes. Local food trucks are part of every Vintique Flea, along with beer and wine, so you can shop, eat and hang out all afternoon.'],
    ['q' => 'Can my food truck apply?', 'a' => 'Absolutely. Fill out the vendor application, choose "Food truck" as your category, and include your menu or Instagram link.'],
    ['q' => 'Is the market kid friendly?', 'a' => 'Yes. Families are welcome, and children 16 and under have historically been admitted free.'],
];
?>
<div class="wrap">
  <?= breadcrumbs([['Food Trucks', '/food-trucks/']]) ?>
  <header class="page-head page-head--icon">
    <span class="page-head__icon" aria-hidden="true">🚚</span>
    <div>
      <h1>Local food trucks, beer &amp; wine</h1>
      <p class="lede">Treasure hunting works up an appetite. Every Vintique Flea brings local Houston food trucks to Silver Street Studios, plus beer and wine, so you can refuel and keep shopping.</p>
    </div>
  </header>
  <div class="layout-2">
    <article class="prose">
      <h2>Houston's food truck culture</h2>
      <p>Houston is one of the most diverse food cities in the country, and its food trucks prove it. On any given weekend you can find Gulf Coast seafood, Viet-Cajun mashups, smoked brisket, tacos al pastor, Korean barbecue, wood-fired pizza and inventive desserts parked side by side. That variety is exactly what we look for when we line up trucks for the market.</p>
      <h2>What to expect at the market</h2>
      <ul>
        <li><strong>A rotating lineup.</strong> Trucks change from edition to edition, so there's always something new to try.</li>
        <li><strong>Beer &amp; wine.</strong> Sip while you browse (21+ with ID).</li>
        <li><strong>Something for everyone.</strong> We aim for savory, sweet, vegetarian-friendly and kid-friendly options.</li>
      </ul>
      <div class="tip"><strong>Tip:</strong> Lunch lines peak around noon to 1pm. Eat early or late, and shop the big furniture first while it's still there.</div>
      <h2>Food truck owners: join us</h2>
      <p>We love featuring local trucks. <a href="/vendors/">Apply through our vendor form</a>, pick "Food truck" and tell us about your menu.</p>
      <h2>Make a day of it</h2>
      <p>Pair the market with a stroll through the <a href="/guides/washington-avenue-arts-district/">Washington Avenue Arts District</a> or use our <a href="/guides/things-to-do-in-houston-this-weekend/">Houston weekend guide</a> to plan the rest of your day.</p>
    </article>
    <aside class="side">
      <div class="side-card">
        <h2>Next market</h2>
        <a class="btn btn--primary btn--block" href="/events/">See dates</a>
      </div>
      <div class="side-card">
        <h2>Love vintage barware?</h2>
        <a class="btn btn--ghost btn--block" href="/shop/vintage-kitchen-barware/">Kitchen &amp; barware</a>
      </div>
    </aside>
  </div>
  <section class="section section--tight">
    <h2>Market-day essentials</h2>
    <?= product_grid($picks) ?>
    <?= disclosure() ?>
  </section>
  <?= faq_block($faq) ?>
</div>
<?php page_end();
