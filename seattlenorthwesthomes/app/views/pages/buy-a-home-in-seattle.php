<?php defined('SNW') || (http_response_code(404) && exit);
partial('page-hero', ['title' => 'Buy a Home in Seattle', 'image' => photo('farmhouse-wraparound-porch'), 'crumbs' => [['Buy a Home', '']],
    'lead' => 'Tell us about your dream home and we\'ll send a tailored list of Seattle homes — then guide you from first tour to closing day.']); ?>
<section class="section tight">
  <div class="wrap listing-layout">
    <div class="prose">
      <h2>Your Seattle Home Search, Simplified</h2>
      <p>Buying a home is one of the biggest financial decisions you'll make, and in Seattle the best homes can move quickly. Complete the form and one of our team members will review your goals, suggest neighborhoods that fit your budget and commute, and start sending homes that match — including new listings before they get buried on the big portals.</p>
      <h3>How we help buyers</h3>
      <ol>
        <li><strong>Plan your budget.</strong> We connect you with trusted local lenders for a solid pre-approval and explain the full cost of buying, from <a href="/blog/seattle-home-buying-costs-closing-costs/">closing costs</a> to HOA dues.</li>
        <li><strong>Narrow the map.</strong> Our <a href="/neighborhoods/">neighborhood guides</a> and on-the-ground knowledge help you compare Ballard vs. Wallingford, condo vs. townhome, city vs. suburbs.</li>
        <li><strong>Tour with an expert eye.</strong> We point out what matters in Seattle homes — drainage, roof moss, side sewers, older wiring — before you fall in love.</li>
        <li><strong>Write a winning offer.</strong> We read the room on review dates, escalation clauses and pre-inspections so your offer is competitive without overpaying.</li>
        <li><strong>Close with confidence.</strong> Inspection, appraisal, escrow and the final walk-through — we keep every deadline on track.</li>
      </ol>
      <p>New to buying? Start with our <a href="/blog/seattle-first-time-home-buyer-guide/">Seattle first-time home buyer guide</a>, see what to expect from a <a href="/blog/seattle-home-inspection-what-to-expect/">Seattle home inspection</a>, or <a href="/homes-for-sale/">browse homes for sale</a>.</p>
    </div>
    <aside class="sidebar">
      <div class="sticky-card">
        <h2 class="h3">Share Your Home Wish List</h2>
        <?php partial('form-buy') ?>
      </div>
    </aside>
  </div>
</section>
<?php partial('cta', ['title' => 'Already own a home?', 'text' => 'Buying and selling at the same time? We\'ll help you plan the timing so you only move once.']) ?>
