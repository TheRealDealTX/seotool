<?php defined('SNW') || (http_response_code(404) && exit);
partial('page-hero', ['title' => 'Sell Your Home in Seattle', 'image' => photo('craftsman-home-twilight'), 'crumbs' => [['Sell Your Home', '']],
    'lead' => 'Get a free pricing review, a clear prep and marketing plan, and expert negotiation from a team that knows your neighborhood.']); ?>
<section class="section tight">
  <div class="wrap listing-layout">
    <div class="prose">
      <h2>Sell for the Best Price and Terms</h2>
      <p>Do you have a property you're thinking of selling? Our team and agent network will evaluate your home, recommend the right price and handle every part of the sale. You get our expertise, negotiation skills and market knowledge working to achieve the best possible price and terms — plus regular updates on market trends, pricing and competing listings so you always know where you stand.</p>
      <h3>Our selling process</h3>
      <ol>
        <li><strong>Pricing review.</strong> We study recent comparable sales and active competition around you to recommend a list price strategy. Read <a href="/blog/how-to-price-your-seattle-home-to-sell/">how we price Seattle homes</a>.</li>
        <li><strong>Prep that pays.</strong> Simple repairs, decluttering and <a href="/blog/home-staging-tips-increase-value/">staging</a> that help your home photograph and show beautifully — even in the rainy season.</li>
        <li><strong>Marketing.</strong> Professional photography, compelling listing copy and promotion to buyers and agents across the Seattle area.</li>
        <li><strong>Offers and negotiation.</strong> We help you compare price, financing strength, contingencies and timing — not just the top-line number.</li>
        <li><strong>Smooth closing.</strong> We coordinate inspections, appraisal and escrow through to closing day.</li>
      </ol>
      <p>Wondering when to list? See our guide to the <a href="/blog/best-time-to-sell-a-house-in-seattle/">best time to sell a house in Seattle</a>, or learn which <a href="/blog/renovations-that-increase-appraisal-value/">renovations increase appraisal value</a>.</p>
    </div>
    <aside class="sidebar">
      <div class="sticky-card">
        <h2 class="h3">Get Your Free Home Value Review</h2>
        <?php partial('form-sell') ?>
      </div>
    </aside>
  </div>
</section>
