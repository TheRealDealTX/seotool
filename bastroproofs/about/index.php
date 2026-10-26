<?php
require dirname(__DIR__) . '/includes/bootstrap.php';
$crumbs = [['Home', '/'], ['About', '/about/']];
page_start([
    'title'       => 'About Bastrop Roofing | Local Roofer in Bastrop, TX',
    'description' => 'Meet Bastrop Roofing, a local Bastrop, TX roofer focused on honest inspections, clear written estimates and roofs built for Lost Pines weather.',
    'path'        => '/about/',
    'image'       => 'ABOUT-BASTROP-ROOFING.webp',
    'schema'      => [breadcrumb_schema($crumbs), ['@type' => 'AboutPage', 'url' => abs_url('/about/'), 'about' => ['@id' => abs_url('/#business')]]],
]);
page_hero('About us', 'About Bastrop Roofing', 'A local roofing company built on a simple idea: inspect first, explain clearly, and recommend only the work the roof actually needs.', $crumbs, 'ABOUT-BASTROP-ROOFING.webp');
?>
<section class="section">
  <div class="container split">
    <div class="split-copy reveal">
      <span class="eyebrow">Who we are</span>
      <h2 class="section-title small">Roofing Help Built Around the Condition of Your Roof</h2>
      <p>Roof problems rarely arrive at a convenient time. A lifted shingle after a windy night, a stain spreading across the ceiling, a hailstorm that has the whole street talking about insurance claims — Bastrop Roofing exists to give property owners in Bastrop a clear, honest starting point.</p>
      <p>We are a local Bastrop roofer. We work in the same heat, the same hail season and under the same pines as our customers. That local focus shapes how we work: we are not here for one storm season, and our reputation travels by word of mouth from Tahitian Village to Hunters Crossing.</p>
    </div>
    <div class="split-media reveal"><img src="<?= img('Roofing-Help-Built-Around-the-Condition-of-Your-Roof.webp') ?>" alt="Bastrop Roofing reviewing a roof's condition in Bastrop, TX" width="1200" height="655" loading="lazy"></div>
  </div>
</section>
<section class="section section-tint">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">How we work</span><h2 class="section-title small">What You Can Count On</h2></div>
    <div class="value-grid">
      <div class="value-card reveal"><?= icon('search') ?><h3>Inspect before we recommend</h3><p>No quotes from the curb. We get on the roof and in the attic and show you photos of what we find.</p></div>
      <div class="value-card reveal"><?= icon('hammer') ?><h3>Repair when repair makes sense</h3><p>Not every problem means a new roof. If a targeted repair is the right answer, that is what we recommend.</p></div>
      <div class="value-card reveal"><?= icon('list') ?><h3>Written, itemized estimates</h3><p>Materials, scope and price spelled out clearly so you can compare and decide with confidence.</p></div>
      <div class="value-card reveal"><?= icon('shield') ?><h3>Respect for your property</h3><p>Landscaping protected, daily cleanup, magnetic nail sweeps and a final walkthrough on every job.</p></div>
      <div class="value-card reveal"><?= icon('layers') ?><h3>Shingle and metal expertise</h3><p>From architectural shingles to standing seam metal, we install the right system for the home and budget.</p></div>
      <div class="value-card reveal"><?= icon('phone') ?><h3>Responsive communication</h3><p>One point of contact, real answers by phone or text, and fast help when a storm hits.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container narrow prose">
    <h2>Roofing for the Lost Pines</h2>
    <p>Bastrop roofs deal with conditions most roofing brochures never mention: pine needles that pack valleys and gutters, tall loblolly pines that drop limbs in high wind, shaded roofs that grow algae, and a wildfire history that makes Class A roof coverings a smart choice. Add Central Texas heat and spring hail, and it is clear why local knowledge matters.</p>
    <p>Whether you need a <a href="/services/roof-repair-bastrop-tx/">roof repair</a>, a full <a href="/services/roof-replacement-bastrop-tx/">roof replacement</a>, a <a href="/services/metal-roofing-bastrop-tx/">metal roof</a> or a <a href="/services/roof-inspection-bastrop-tx/">free inspection</a> after a storm, Bastrop Roofing is ready to help. Call <a href="tel:+15122977580">(512) 297-7580</a> or <a href="/contact/">request an estimate online</a>.</p>
  </div>
</section>
<?php cta_band(); page_end();
