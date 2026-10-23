<?php defined('SS_APP') || exit; ?>
<aside class="sidebar" aria-label="Sidebar">
  <div class="side-box side-cta">
    <h2>Find your match</h2>
    <p class="small" style="color:#e2d6ee">5 questions &rarr; your best saffron supplement and dose.</p>
    <a class="btn btn-amz" href="/tools/saffron-supplement-quiz/">Take the Quiz</a>
  </div>
  <div class="side-box">
    <h2>Top-rated picks</h2>
    <ul>
      <?php foreach (array_slice(TOP_PICKS, 0, 4) as $sid) { $sp = PRODUCTS[$sid]; ?>
      <li><span class="badge"><?= e($sp['badge']) ?></span><br><?= amz($sp['asin'], e($sp['name'])) ?></li>
      <?php } ?>
    </ul>
    <p style="margin:10px 0 0"><a href="/best-saffron-supplements/">All 12 reviews &rarr;</a></p>
  </div>
  <div class="side-box">
    <h2>Free tools</h2>
    <ul>
      <li><a href="/tools/saffron-dosage-calculator/">Dosage Calculator</a></li>
      <li><a href="/tools/cost-per-dose-calculator/">Cost-Per-Dose Calculator</a></li>
      <li><a href="/tools/saffron-safety-checker/">Safety Checker</a></li>
      <li><a href="/tools/saffron-mood-sleep-tracker/">Mood &amp; Sleep Tracker</a></li>
    </ul>
  </div>
  <div class="side-box">
    <h2>Popular guides</h2>
    <ul>
      <li><a href="/saffron-dosage/">Saffron Dosage</a></li>
      <li><a href="/saffron-side-effects/">Side Effects</a></li>
      <li><a href="/saffron-for-depression-and-mood/">Saffron for Mood</a></li>
      <li><a href="/saffron-for-sleep/">Saffron for Sleep</a></li>
    </ul>
  </div>
</aside>
