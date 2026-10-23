<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Five free, private tools that answer the questions readers ask most: how much saffron to take, which product to buy, what it really costs, whether it\'s safe for you, and whether it\'s working.', 'Free Tools');
?>
<div class="wrap section">
  <div class="grid g3">
    <?= card('/tools/saffron-dosage-calculator/', 'Saffron Dosage Calculator', 'Turn your goal and capsule strength into a research-matched daily plan with timing and a results window.', '🧮') ?>
    <?= card('/tools/saffron-supplement-quiz/', 'Supplement Finder Quiz', 'Five questions match you to the extract, dose and product that fit your goal and budget.', '🎯') ?>
    <?= card('/tools/cost-per-dose-calculator/', 'Cost-Per-Dose Calculator', 'Compare bottles by the real cost of an effective daily dose, per month and per year.', '💲') ?>
    <?= card('/tools/saffron-safety-checker/', 'Saffron Safety Checker', 'Flags pregnancy, conditions and medications to raise with your doctor before you start.', '🛡️') ?>
    <?= card('/tools/saffron-mood-sleep-tracker/', '12-Week Mood & Sleep Tracker', 'Daily check-ins with a 7-day trend chart, stored privately in your browser.', '📈') ?>
    <?= card('/how-to-choose-a-saffron-supplement/', 'Label Checklist', 'Seven things to check on any saffron supplement label.', '✅') ?>
  </div>
  <div class="narrow" style="margin-top:40px">
    <h2>Suggested Order</h2>
    <ol class="steps">
      <li><a href="/tools/saffron-safety-checker/">Run the safety checker</a> to make sure saffron is a sensible fit.</li>
      <li><a href="/tools/saffron-supplement-quiz/">Take the quiz</a> to find a product.</li>
      <li><a href="/tools/saffron-dosage-calculator/">Use the dosage calculator</a> to plan how many capsules and when.</li>
      <li><a href="/tools/saffron-mood-sleep-tracker/">Track for 8–12 weeks</a> to see whether it's helping.</li>
    </ol>
    <p class="note">All tools run in your browser. Saffron Supplement doesn't collect or store anything you enter into them.</p>
  </div>
</div>
