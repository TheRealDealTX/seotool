<?php
hero([
    'eyebrow' => 'Free Planning Tools',
    'h1'      => 'Free Tiny Home Calculators &amp; Planning Tools',
    'lead'    => 'Size it, price it, finance it and see what it could earn — before you ever call a builder. Every tool is free, runs in your browser and takes about a minute.',
    'image'   => 'Cowboy-Tiny-Homes-Home-BG.webp',
    'cta'     => false,
]);
$tools = [
    ['/tools/tiny-home-cost-calculator/', 'Calculator', 'Tiny Home Cost Calculator', 'Pick a home type, size, finish level and add-ons like septic, solar and utility hookups to get a low-to-high Texas budget with a line-by-line breakdown.', 'Estimate my cost'],
    ['/tools/which-tiny-home-is-right-for-me/', 'Quiz', 'Which Tiny Home Is Right for Me?', 'Six questions about your land, lifestyle, budget and financing match you with a tiny home on wheels, park model, ADU or custom foundation home.', 'Take the quiz'],
    ['/tools/tiny-house-size-planner/', 'Planner', 'Tiny House Size Planner', 'Add bedrooms, baths, lofts, kitchens and storage to see how many square feet you need and which home types can hold it.', 'Plan my space'],
    ['/tools/adu-rental-income-calculator/', 'Calculator', 'ADU Rental Income Calculator', 'Compare long-term and short-term rental income for a backyard casita and see monthly cash flow, cash-on-cash return and payback.', 'Run the numbers'],
    ['/tools/tiny-home-loan-calculator/', 'Calculator', 'Tiny Home Loan Calculator', 'Compare RV loans, personal loans, HELOCs, mortgages and construction loans with a monthly payment and year-by-year payoff schedule.', 'Estimate payments'],
];
?>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" style="color:var(--gold-dark)">Plan Smarter</p>
      <h2>Tools Built by Tiny Home Designers</h2>
      <p class="section-intro">Cowboy Tiny Homes built these calculators from the same planning numbers our designers use in first consultations. Use them in order — or jump to the one you need.</p>
    </div>
    <div class="cards cards--links">
<?php foreach ($tools as [$href, $kick, $title, $blurb, $more]): ?>
      <a class="card card--link" href="<?= $href ?>"><span class="card-kicker"><?= $kick ?></span><strong><?= e($title) ?></strong><span><?= e($blurb) ?></span><span class="card-more"><?= $more ?> →</span></a>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap grid-2">
    <div class="prose">
      <h2>How Our Estimates Work</h2>
      <p>Every cost figure across these tools comes from one shared model: Texas 2026 planning ranges per finished square foot for builder-built homes, adjusted for finish level, plus typical price ranges for site work such as foundations, septic systems, wells, utility hookups and solar. A tiny home on wheels, for example, is modeled at roughly $175 to $300 per square foot at standard finishes, and an ADU at roughly $190 to $340.</p>
      <p>The results are planning ranges, not bids. Land is never included, and real projects vary with design complexity, site conditions, material prices and local permit fees. Loan rates in the tools are illustrative examples — replace them with quotes from your lender.</p>
      <p>When your numbers look right, each tool's results button sends a summary straight into our contact form, so a Cowboy Tiny Homes designer can turn your estimate into a written quote.</p>
    </div>
    <div class="card">
      <h3>Suggested order</h3>
      <ol class="steps" style="grid-template-columns:1fr;margin-top:28px">
        <li><h3>Take the quiz</h3><p>Find the home type that fits your land and lifestyle.</p></li>
        <li><h3>Plan the size</h3><p>Add up the rooms you really need.</p></li>
        <li><h3>Price it</h3><p>Get a full budget with site costs.</p></li>
        <li><h3>Finance it</h3><p>See the monthly payment — and rental income for an ADU.</p></li>
      </ol>
    </div>
  </div>
</section>

<?php related([
    '/guides/cost-to-build-a-tiny-house-in-texas/',
    '/guides/tiny-house-laws-texas/',
    '/guides/tiny-home-financing-texas/',
], 'Read the Guides Behind the Numbers'); ?>

<?php cta_band(); ?>
