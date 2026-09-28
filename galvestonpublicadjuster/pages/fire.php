<?php
$meta['title'] = 'Galveston Fire Claims | Fire & Smoke Damage Public Adjuster';
$meta['description'] = 'Galveston fire claims help from a licensed public adjuster: structure, smoke, soot, contents and living expenses. Free fire damage claim review — (832) 503-5866.';
$meta['crumb'] = 'Galveston Fire Claims';
$meta['schema'][] = ['@type' => 'Service', 'name' => 'Fire damage claim public adjuster', 'serviceType' => 'Fire and smoke damage insurance claims',
    'provider' => ['@id' => SITE_URL . '/#business'], 'areaServed' => 'Galveston County, TX'];
$faqs = [
    ['What should I do first after a house fire in Galveston?', '<p>Make sure everyone is safe, get the fire department report number, notify your insurer, and secure the property against weather and theft. Photograph everything before cleanup starts and keep every receipt for hotel, meals and emergency purchases — those are usually reimbursable under Additional Living Expense.</p>'],
    ['Does insurance cover smoke damage in rooms the fire never reached?', '<p>Usually, yes. Smoke and soot travel through HVAC ducts, attics and wall cavities. Smoke-damaged drywall, insulation, ductwork and contents are part of a fire loss, but they are often under-scoped unless someone documents them properly.</p>'],
    ['How long does a fire damage claim take?', '<p>Simple fires can resolve in weeks; total losses with contents inventories can take months. Texas\'s Prompt Payment of Claims Act (Insurance Code ch. 542) sets deadlines for insurers to acknowledge, decide and pay. We keep the claim moving.</p>'],
    ['Should I let the insurer\'s preferred contractor start work?', '<p>You have the right to choose your own contractor. Before any demolition, make sure the damage is fully documented — once it\'s torn out, it\'s much harder to prove.</p>'],
];
echo page_hero(icon('fire', 18) . ' Galveston fire claims', 'Galveston Fire Claims: Fire &amp; Smoke Damage Claim Help',
    'A fire claim is the most complex claim most families ever file. We document the structure, the smoke, the soot and every item you own — so the settlement covers what you actually lost.', art_fire());
?>
<section class="section">
  <div class="wrap layout-side">
    <article class="prose">
      <h2>Why fire damage claims get underpaid</h2>
      <p>Galveston fire claims involve more than the burned room. Heat, smoke, soot and the water used to put out the fire damage far more of the home than most initial estimates capture. Insurance company estimates tend to focus on what's visibly charred and miss the rest.</p>
      <div class="grid g2">
        <div class="card"><div class="badge-ico"><?= icon('fire', 28) ?></div><h3>Structure</h3><p>Framing, drywall, insulation, roofing, electrical and code upgrades required by the City of Galveston.</p></div>
        <div class="card"><div class="badge-ico"><?= icon('wind', 28) ?></div><h3>Smoke &amp; soot</h3><p>Soot migration through ductwork and attics, odor sealing, HVAC cleaning or replacement.</p></div>
        <div class="card"><div class="badge-ico"><?= icon('home', 28) ?></div><h3>Contents</h3><p>Room-by-room inventory of furniture, clothing, electronics and belongings at replacement cost.</p></div>
        <div class="card"><div class="badge-ico"><?= icon('dollar', 28) ?></div><h3>Living expenses</h3><p>Hotel or rental, extra food and mileage costs while the home is uninhabitable (ALE / Coverage D).</p></div>
      </div>

      <h2>Our fire damage claim process</h2>
      <ol>
        <li><strong>Emergency response.</strong> We help secure the property and get Additional Living Expense started.</li>
        <li><strong>Full documentation.</strong> Photos, measurements, soot and odor mapping in every room, including areas the fire never touched.</li>
        <li><strong>Complete estimate.</strong> A line-by-line reconstruction estimate including smoke remediation and code items.</li>
        <li><strong>Contents inventory.</strong> We build the inventory the insurer requires, with replacement values.</li>
        <li><strong>Negotiation.</strong> We meet the insurer's adjuster on site and negotiate every line.</li>
      </ol>

      <?= banner('House or business fire? Call for an expert consultation.', 'The sooner damage is documented, the stronger the claim.') ?>

      <h2>Smoke damage claims: the hidden half of the loss</h2>
      <p>Smoke is acidic and it keeps working after the fire is out. It discolors surfaces, corrodes electronics and settles into insulation and ducts. If your insurer's estimate only includes "clean and paint" in rooms beyond the fire, ask for a second look. Common missed items include HVAC duct cleaning or replacement, attic insulation, sealing primers, content cleaning (pack-out), and odor treatment.</p>

      <h2>What not to do after a fire</h2>
      <ul class="checks xs">
        <li>Don't throw away damaged items before they're photographed and inventoried.</li>
        <li>Don't sign a contractor's "direction to pay" or an insurer's release without reading it.</li>
        <li>Don't give a recorded statement before you understand your policy.</li>
        <li>Don't accept the first estimate as final — most fire estimates are revised.</li>
      </ul>

      <h2>Galveston fire claims FAQ</h2>
      <?= faq_block($faqs, $meta['schema']) ?>
      <p class="mt">Read more: <a href="/blog/">fire and smoke claim guides</a> by <?= AUTHOR ?>.</p>
    </article>
    <aside class="sidebar">
      <div class="side-card dark"><h3>Fire claim help now</h3><p>Talk to a licensed public adjuster about your fire loss.</p><?= phone_link('btn btn-cta btn-block', icon('phone', 18) . ' ' . PHONE) ?></div>
      <div class="side-card"><h3>Free claim review</h3><?= lead_form('fire', true) ?></div>
    </aside>
  </div>
</section>
