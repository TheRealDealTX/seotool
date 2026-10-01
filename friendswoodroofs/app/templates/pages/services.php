<?php defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
partial('page-hero', [
    'eyebrow' => 'What we do',
    'title'   => 'Roofing Services in Friendswood, TX',
    'lead'    => 'Residential roofing services for Friendswood homeowners, each starting with a careful assessment and a written estimate.',
]); ?>

<section class="section">
  <div class="container">
    <div class="section-head" data-reveal>
      <h2>Choose a service</h2>
      <p>Not sure which service fits? Start with a <a href="/services/roof-inspections/">roof inspection</a> or describe your concern in the <a href="/roofing-project-planner/">Roofing Project Planner</a>.</p>
    </div>
    <?php partial('service-cards'); ?>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head" data-reveal>
      <h2>Which service do I need?</h2>
      <p>A quick guide to matching what you are seeing with the right starting point.</p>
    </div>
    <div class="table-wrap" data-reveal>
      <table class="guide-table">
        <caption class="sr-only">Situations and suggested starting services</caption>
        <thead><tr><th scope="col">If you are seeing&hellip;</th><th scope="col">A good place to start</th></tr></thead>
        <tbody>
          <tr><th scope="row">A ceiling stain or drip during rain</th><td><a href="/services/roof-repair/">Roof Repair</a></td></tr>
          <tr><th scope="row">Missing shingles or debris after a storm</th><td><a href="/services/storm-damage-roof-repair/">Storm Damage Roof Repair</a></td></tr>
          <tr><th scope="row">Widespread curling, cracking or repeated leaks</th><td><a href="/services/roof-replacement/">Roof Replacement</a></td></tr>
          <tr><th scope="row">No obvious problem, but the roof is older or its history is unknown</th><td><a href="/services/roof-inspections/">Roof Inspections</a></td></tr>
          <tr><th scope="row">You want to choose or compare roofing materials</th><td><a href="/services/asphalt-shingle-roofing/">Asphalt Shingle Roofing</a> or <a href="/services/metal-roofing/">Metal Roofing</a></td></tr>
          <tr><th scope="row">You want to keep a sound roof in good shape</th><td><a href="/services/roof-maintenance/">Roof Maintenance</a></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split split--even">
    <div class="prose" data-reveal>
      <h2>What every service includes</h2>
      <ul class="check-list">
        <li>A conversation about what you have noticed and what you want to achieve</li>
        <li>An assessment of the relevant parts of the roof, with photos</li>
        <li>A plain-language explanation of what we found</li>
        <li>A written estimate with scope, materials and price before any work begins</li>
        <li>Clean-up and a review of the completed work</li>
      </ul>
    </div>
    <div class="prose" data-reveal>
      <h2>Helpful reading</h2>
      <ul class="link-list">
        <li><a href="/blog/roof-repair-or-replacement-friendswood/">Roof Repair or Replacement? A Guide for Friendswood Homeowners</a></li>
        <li><a href="/blog/asphalt-shingles-vs-metal-roofing-friendswood-tx/">Asphalt Shingles vs. Metal Roofing for Homes in Friendswood, TX</a></li>
        <li><a href="/blog/how-to-choose-a-roofing-contractor-friendswood/">Friendswood Roofers: How to Choose a Roofing Contractor</a></li>
        <li><a href="/faqs/">Roofing FAQs</a></li>
      </ul>
    </div>
  </div>
</section>

<?php partial('cta-band'); ?>
