<?php
defined('CPA') or exit;
$P['title'] = 'Page Not Found | CPA Calculator';
$P['description'] = 'The page you were looking for could not be found. Try one of our free tax and accounting calculators.';
$P['noindex'] = true;
$P['canonical'] = '/404/';
?>
<section class="page-hero"><div class="wrap err-hero" style="padding:60px 0">
  <div class="num mono">404</div>
  <h1>That page didn’t add up.</h1>
  <p class="lede" style="margin:0 auto 24px">The page may have moved. Here are the calculators people use most.</p>
  <a class="btn" href="/calculators/">Browse all calculators <?= icon('arrow') ?></a>
</div></section>
<section class="section-tight"><div class="wrap"><?= tool_cards(['federal-income-tax', '1099-tax-calculator', 'paycheck-calculator', 'quarterly-estimated-tax', 'self-employment-tax', 'tax-refund-calculator']) ?></div></section>
