<?php
require dirname(__DIR__) . '/includes/layout.php';
$crumbs = [['Service Areas', '/service-areas/']];
page_start([
    'title' => 'Roofing Service Areas | Austin & Central Texas | Austin Roofing',
    'description' => 'Austin Roofing serves Austin, East & South Austin, Round Rock, Pflugerville, Cedar Park, Leander, Georgetown, Hutto, Kyle, San Marcos and more. Free quotes.',
    'path' => '/service-areas/', 'crumbs' => $crumbs, 'body_class' => 'page-areas',
]);
page_hero('Austin Roofing Service Areas', [
    'crumbs' => $crumbs,
    'eyebrow' => 'Travis · Williamson · Hays · Caldwell · Bastrop',
    'lead' => 'From East Austin bungalows to Hill Country homes in Dripping Springs and master-planned neighborhoods in Leander, Austin Roofing serves the whole Austin metro and surrounding Central Texas.',
]);
?>
<section class="section section--tight">
  <div class="container">
    <?php area_cards(); ?>
  </div>
</section>
<div class="container layout-sidebar">
  <article class="prose">
    <h2>An Austin Roofing Company That Covers Central Texas</h2>
    <p class="lead">Our home base is Austin, and our crews work every day across the surrounding cities and counties. Wherever your property is, you get the same free inspection, photo report and honest recommendation.</p>
    <p>Roofing needs change from one part of the metro to the next. Neighborhoods in <a href="/service-areas/east-austin/">East Austin</a> mix century-old bungalows with modern infill topped by low-slope and metal roofs. <a href="/service-areas/south-austin/">South Austin</a> is full of 1970s and ’80s ranch homes on their second or third roof. North of the river, <a href="/service-areas/round-rock-tx/">Round Rock</a>, <a href="/service-areas/pflugerville-tx/">Pflugerville</a>, <a href="/service-areas/georgetown-tx/">Georgetown</a> and <a href="/service-areas/hutto-tx/">Hutto</a> take the brunt of many spring hailstorms, while the Hill Country west of town — <a href="/service-areas/dripping-springs-tx/">Dripping Springs</a>, <a href="/service-areas/cedar-park-tx/">Cedar Park</a> and <a href="/service-areas/leander-tx/">Leander</a> — brings steep pitches, HOA material rules and wildfire-aware roofing choices. To the south and east, <a href="/service-areas/kyle-tx/">Kyle</a>, <a href="/service-areas/san-marcos-tx/">San Marcos</a>, <a href="/service-areas/lockhart-tx/">Lockhart</a> and <a href="/service-areas/bastrop-tx/">Bastrop</a> each have their own housing stock and weather patterns.</p>
    <h2>Services Available in Every Area</h2>
    <?php service_cards(['roof-repair', 'roof-replacement', 'hail-damage-repair', 'commercial-roofing', 'emergency-roof-repair', 'roof-inspection'], 'cards--compact'); ?>
    <p>Don’t see your town? We regularly work throughout the greater Austin area — <a href="/contact-us/">contact us</a> or call <?= phone_link() ?> and we will let you know.</p>
  </article>
  <?php sidebar(['links' => service_links(['roof-repair', 'roof-replacement', 'hail-damage-repair', 'roof-inspection'])]); ?>
</div>
<?php cta_band(); page_end();
