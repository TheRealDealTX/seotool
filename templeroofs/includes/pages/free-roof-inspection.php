<?php
defined('TR_ROOT') || exit;
$crumbs = [['Free Roof Inspection', '/free-roof-inspection/']];
$faqs = [
    ['q' => 'Is there really no cost or obligation?', 'a' => 'Correct. The inspection is free, and you are under no obligation to hire Temple Roofers for any work afterward. If the roof is in good shape, we will tell you so.'],
    ['q' => 'Do I need to be home for the inspection?', 'a' => 'It helps if someone can be there, especially if we need to look in the attic or at interior stains, and so we can walk you through the photos. If that is not possible, tell us when you book and we will discuss options for an exterior-only inspection.'],
    ['q' => 'How long does an inspection take?', 'a' => 'Most residential inspections take roughly 30 to 60 minutes depending on the size, pitch and complexity of the roof and whether the attic is accessible.'],
    ['q' => 'Will you get on my roof?', 'a' => 'When it is safe to do so, yes — our team uses proper fall-protection practices. If the roof is wet, very steep or otherwise unsafe that day, we will use other methods or reschedule. Homeowners should never climb onto the roof themselves.'],
    ['q' => 'Can the inspection help with an insurance claim?', 'a' => 'Our photos and written findings can help you decide whether to contact your insurer, and our estimate can support the repair scope. We are not public adjusters and cannot negotiate your claim or promise coverage — your insurance company makes that decision.'],
    ['q' => 'What happens after the inspection?', 'a' => 'We review the findings with you, explain what is urgent and what can wait, and provide a written estimate if work is recommended. There is no pressure to decide on the spot.'],
];
layout_start([
    'title'       => 'Free Roof Inspection in Temple, TX',
    'description' => 'Book a free, no-obligation roof inspection in Temple, TX. Photos, plain-language findings and honest repair or replacement advice.',
    'path'        => '/free-roof-inspection/',
    'crumbs'      => $crumbs,
    'image'       => 'roofer-inspecting-roof',
    'preload_image' => 'roofer-inspecting-roof',
    'schema'      => [schema_faq($faqs)],
    'body_class'  => 'page-inspection',
]);
?>
<section class="page-hero page-hero--image page-hero--form">
  <div class="page-hero__bg" data-parallax><?= img('roofer-inspecting-roof', 'Roofing professional inspecting a shingle roof', ['sizes' => '100vw', 'priority' => true, 'class' => 'page-hero__img']) ?></div>
  <div class="container page-hero__inner page-hero__inner--split">
    <div>
      <?= breadcrumbs_html($crumbs) ?>
      <p class="eyebrow eyebrow--light">No cost · No obligation</p>
      <h1 class="page-hero__title">Free Roof Inspection in Temple, TX</h1>
      <p class="page-hero__lead">Find out exactly what is happening on your roof. We inspect, photograph what we find and explain your options in plain language — free.</p>
      <ul class="hero__points">
        <li><?= icon('check') ?> Shingles, flashing, vents &amp; attic</li>
        <li><?= icon('check') ?> Photo documentation</li>
        <li><?= icon('check') ?> Written estimate if work is needed</li>
      </ul>
      <a class="btn btn--outline-light" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> Or call <?= e(cfg('phone_display')) ?></a>
    </div>
    <div class="hero__form" id="book">
      <?php lead_form(['variant' => 'full', 'id' => 'inspection', 'title' => 'Schedule your free roof inspection', 'subtitle' => 'Fields marked * are required. We usually reply by the next business day.', 'button' => 'Request My Free Inspection']); ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <?= section_head('What we check', 'What a Temple Roofers Inspection Covers', 'A real inspection is more than a glance from the driveway. Here is what we look at and why it matters in Central Texas.') ?>
    <div class="factor-grid factor-grid--3">
      <article class="factor reveal"><span class="factor__icon"><?= icon('shingle') ?></span><h3>Roof surface</h3><p>Missing, creased, cracked or curling shingles; hail bruises and granule loss; exposed fasteners and nail pops; signs of previous patchwork.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('layers') ?></span><h3>Flashing &amp; edges</h3><p>Step and counter flashing at walls and chimneys, valley metal, drip edge, and the rake and eave edges where wind uplift usually starts.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('pipe') ?></span><h3>Penetrations</h3><p>Plumbing pipe boots (a frequent leak source once UV cracks the rubber), exhaust caps, skylights, satellite mounts and other openings.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('fan') ?></span><h3>Ventilation</h3><p>Soffit intake, ridge and box vents, and attic signs of trapped heat or moisture that shorten shingle life and raise cooling costs.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('cloud-hail') ?></span><h3>Storm damage</h3><p>Hail impacts, wind-lifted tabs, debris strikes and dented soft metals — photographed and noted by slope so you have a clear record.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('gutter') ?></span><h3>Gutters &amp; drainage</h3><p>Clogs, sagging runs, overflowing downspouts and fascia rot that let Central Texas downpours back up under the roof edge.</p></article>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container split">
    <div class="split__copy reveal">
      <p class="eyebrow">When to book</p>
      <h2 class="section-title">When a Free Roof Inspection Makes Sense</h2>
      <ul class="check-list">
        <li><?= icon('check') ?><span><strong>After a storm:</strong> hail, high winds or a severe thunderstorm moved through Temple or your neighbors are getting roofs replaced.</span></li>
        <li><?= icon('check') ?><span><strong>You see a stain or drip:</strong> water marks on ceilings or walls, damp insulation or a musty attic.</span></li>
        <li><?= icon('check') ?><span><strong>Your roof is getting older:</strong> curling or balding shingles, or you are not sure how many years it has left.</span></li>
        <li><?= icon('check') ?><span><strong>Buying or selling:</strong> you want an independent view of a roof's condition before closing.</span></li>
        <li><?= icon('check') ?><span><strong>Planning ahead:</strong> spring storm season is coming and you would rather fix small issues now.</span></li>
      </ul>
      <p>Not sure? The <a href="/tools/storm-damage-checklist/">storm damage self-check</a> walks you through what you can safely look for from the ground.</p>
    </div>
    <div class="split__media reveal"><figure class="media-frame"><?= img('wind-damaged-roof', '', ['sizes' => '(max-width: 900px) 100vw, 50vw']) ?></figure></div>
  </div>
</section>

<section class="section process">
  <div class="container">
    <?= section_head('The process', 'How Your Free Inspection Works') ?>
    <ol class="steps steps--4">
      <li class="step reveal"><span class="step__num">1</span><span class="step__icon"><?= icon('calendar') ?></span><h3>Book a time</h3><p>Use the form above or call. We confirm a time that works for you.</p></li>
      <li class="step reveal"><span class="step__num">2</span><span class="step__icon"><?= icon('search') ?></span><h3>We inspect</h3><p>Roof surface, flashing, penetrations, ventilation, gutters and the attic where accessible.</p></li>
      <li class="step reveal"><span class="step__num">3</span><span class="step__icon"><?= icon('camera') ?></span><h3>See the photos</h3><p>We show you what we found and explain what it means for your roof.</p></li>
      <li class="step reveal"><span class="step__num">4</span><span class="step__icon"><?= icon('document') ?></span><h3>Get your options</h3><p>If work is needed, you get a written estimate. If not, you get peace of mind.</p></li>
    </ol>
    <div class="callout callout--warn reveal"><strong>Safety first:</strong> please do not climb onto your roof to look for damage — especially after a storm when shingles may be loose or wet. Look from the ground, take photos and let a professional with proper equipment handle the rest.</div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow">
    <?= faq_html($faqs, 'Free Roof Inspection FAQs') ?>
  </div>
</section>
<section class="section cta-slim">
  <div class="container cta-slim__inner reveal">
    <h2>Ready to book? It takes about a minute.</h2>
    <div class="btn-row"><a class="btn btn--gold" href="#book">Fill out the inspection form</a><a class="btn btn--ghost" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> <?= e(cfg('phone_display')) ?></a></div>
  </div>
</section>
<?php layout_end();
