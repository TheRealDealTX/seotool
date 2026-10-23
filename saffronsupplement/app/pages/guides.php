<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Everything you need to use saffron well: how much to take, how to stay safe, and how to pick a product that actually contains what it claims.', 'Guides');
?>
<div class="wrap section">
  <h2 style="margin-top:0">Dosage, Safety &amp; Buying</h2>
  <div class="grid g2">
    <?= card('/saffron-dosage/', 'Saffron Supplement Dosage Guide', 'The exact doses used in clinical trials for each goal, plus timing and safe upper limits.', '⚖️') ?>
    <?= card('/saffron-side-effects/', 'Side Effects, Safety & Interactions', 'Who should avoid saffron, the drug interactions that matter, and what side effects to expect.', '🛡️') ?>
    <?= card('/how-to-choose-a-saffron-supplement/', 'How to Choose a Saffron Supplement', 'A 7-point label checklist and the red flags that point to a poor-quality product.', '✅') ?>
    <?= card('/affron-vs-satiereal/', 'affron® vs Satiereal® vs Generic', 'The two branded extracts compared, and when a generic is good enough.', '🔬') ?>
  </div>
  <h2>Benefits, by Goal</h2>
  <div class="grid g3">
    <?= card('/saffron-benefits/', 'All Saffron Benefits', 'Seven research-backed uses, ranked by the strength of the evidence.', '🌼') ?>
    <?= card('/saffron-for-depression-and-mood/', 'Saffron for Mood', 'What 20+ trials found about saffron and low mood.', '🌤️') ?>
    <?= card('/saffron-for-sleep/', 'Saffron for Sleep', 'Dose, timing and how saffron compares with melatonin.', '🌙') ?>
    <?= card('/saffron-for-eye-health/', 'Saffron for Eye Health', 'The macular degeneration trials and how saffron fits with AREDS2.', '👁️') ?>
    <?= card('/saffron-for-weight-loss/', 'Saffron for Appetite', 'An honest look at Satiereal® and snacking.', '🍽️') ?>
    <?= card('/saffron-for-pms/', 'Saffron for PMS', 'The 15 mg twice-daily protocol, explained.', '🌸') ?>
  </div>
  <h2>From the Blog</h2>
  <div class="grid g3">
    <?php foreach (blog_posts() as $bp => $br) echo card($bp, $br['h1'], $br['desc'], '📝'); ?>
  </div>
  <h2>Reviews</h2>
  <div class="grid g2">
    <?= card('/best-saffron-supplements/', 'Best Saffron Supplements of ' . SITE_YEAR, '12 products compared on dose, standardization, testing and value.', '⭐') ?>
    <?= card('/faq/', 'Saffron Supplement FAQ', 'Twenty common questions, answered briefly.', '❓') ?>
  </div>
</div>
