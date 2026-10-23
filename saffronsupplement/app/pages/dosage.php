<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'The right saffron supplement dosage depends on your goal and the extract you buy. Here are the exact doses used in clinical trials for each benefit, the safe upper limits, and the best time of day to take saffron.', 'Guides &middot; Dosage');
?>
<div class="wrap layout">
  <article class="prose">
    <div class="keyfacts">
      <h2>Quick answer</h2>
      <ul>
        <li><strong>Most goals:</strong> 28–30 mg of standardized saffron extract per day.</li>
        <li><strong>Eye health:</strong> 20 mg per day.</li>
        <li><strong>Appetite:</strong> 176.5 mg per day of Satiereal®, split before two meals.</li>
        <li><strong>Upper limit:</strong> up to 100 mg/day has been used safely short-term; serious toxicity has only been reported at 5 g or more.</li>
      </ul>
    </div>
    <?= toc(['table' => 'Dosage by goal', 'extract' => 'Extract vs spice dosing', 'timing' => 'When to take saffron', 'how-long' => 'How long to take it', 'max' => 'Maximum safe dose', 'calc' => 'Dosage calculator', 'faq' => 'FAQ']) ?>

    <h2 id="table">Saffron Dosage by Goal</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>Goal</th><th>Daily dose used in trials</th><th>How it was taken</th><th>Trial length</th></tr></thead>
      <tbody>
        <tr><td><a href="/saffron-for-depression-and-mood/">Low mood / depression</a></td><td>30 mg</td><td>15 mg twice daily</td><td>6–8 weeks</td></tr>
        <tr><td>Low mood (healthy adults)</td><td>28 mg affron®</td><td>Once daily</td><td>4 weeks</td></tr>
        <tr><td>Stress &amp; anxiety</td><td>28–30 mg</td><td>Once or split</td><td>4–12 weeks</td></tr>
        <tr><td><a href="/saffron-for-sleep/">Sleep quality</a></td><td>28 mg affron®</td><td>14 mg twice daily</td><td>4 weeks</td></tr>
        <tr><td><a href="/saffron-for-eye-health/">Macular eye health</a></td><td>20 mg</td><td>Once daily</td><td>3+ months</td></tr>
        <tr><td><a href="/saffron-for-pms/">PMS</a></td><td>30 mg</td><td>15 mg twice daily</td><td>2 cycles</td></tr>
        <tr><td><a href="/saffron-for-weight-loss/">Snacking / appetite</a></td><td>176.5 mg Satiereal®</td><td>2 doses before meals</td><td>8 weeks</td></tr>
        <tr><td>SSRI sexual side effects</td><td>30 mg</td><td>15 mg twice daily</td><td>4 weeks</td></tr>
      </tbody>
    </table></div>
    <p class="note">More is not better. No trial has shown that doses above 30 mg (outside the Satiereal® protocol) work better for mood, and higher doses increase the chance of side effects.</p>

    <h2 id="extract">Why Satiereal® Is Dosed So Differently</h2>
    <p>Dosing numbers only make sense for the specific extract used. affron® is concentrated and standardized to ≥3.5% Lepticrosalides®, so 28 mg is enough. Satiereal® is prepared differently and was studied at 176.5 mg/day. A generic "saffron extract 88.5 mg" capsule with no stated standardization could contain more or less active compound than either. That's why we recommend products that disclose their extract. See <a href="/affron-vs-satiereal/">affron vs Satiereal</a>.</p>
    <h3>What about saffron threads?</h3>
    <p>Trials of kitchen saffron are rare, and potency varies hugely with grade and freshness. As a rough guide, 30 mg of threads is a generous pinch (about 15–20 threads). That is fine in food or tea, but you can't know its crocin content. For a consistent, research-matched dose, use an extract. For cooking, see <?= amz('grade 1 saffron threads', 'Grade I saffron threads on Amazon') ?>.</p>

    <h2 id="timing">When Is the Best Time to Take Saffron?</h2>
    <ul>
      <li><strong>Mood and PMS:</strong> split the dose, morning and evening, with food (as in most trials).</li>
      <li><strong>Sleep:</strong> split morning and evening, or take the full dose about an hour before bed.</li>
      <li><strong>Appetite:</strong> before lunch and before dinner.</li>
      <li><strong>Eyes:</strong> once a day with a meal, any time.</li>
    </ul>
    <p>Taking saffron with food reduces the chance of nausea and stomach upset.</p>

    <h2 id="how-long">How Long Should You Take Saffron?</h2>
    <p>Most trials ran 4–12 weeks; eye trials ran up to 14 months. Give saffron at least 6–8 weeks before deciding whether it works. If you take it long-term, review it with your doctor every few months and consider a short break to see whether you still need it.</p>

    <h2 id="max">What Is the Maximum Safe Dose of Saffron?</h2>
    <ul>
      <li><strong>Up to 30 mg/day</strong> (or 176.5 mg Satiereal®): the range used in most trials, well tolerated.</li>
      <li><strong>Up to 100 mg/day:</strong> used in some short-term studies without serious effects.</li>
      <li><strong>200–400 mg/day:</strong> a one-week safety study found minor changes in some blood measures at 400 mg (Modaghegh 2008). Not recommended.</li>
      <li><strong>5 g or more:</strong> reported toxic effects; 12–20 g has been cited as potentially lethal. No supplement comes close to this.</li>
    </ul>

    <h2 id="calc">Work Out Your Dose</h2>
    <p>Our free <a href="/tools/saffron-dosage-calculator/">saffron dosage calculator</a> turns your goal and your product's milligrams per capsule into a daily plan, with timing and an expected results window.</p>
    <p><a class="btn" href="/tools/saffron-dosage-calculator/">Open the Dosage Calculator</a></p>
    <?= aff_note() ?>
    <?= product_inline('nootropics-depot', '30 mg per capsule, the most common research dose for mood.') ?>
    <?= product_inline('source-naturals', '15 mg tablets for the twice-daily protocol.') ?>

    <?= faq_block([
      ['How many mg of saffron should I take a day?', '<p>For most goals, 28–30 mg of standardized saffron extract per day. Use 20 mg for eye health, and 176.5 mg of Satiereal® for appetite.</p>'],
      ['Is 100 mg of saffron too much?', '<p>100 mg/day has been used in short-term studies without serious problems, but it is more than most goals need. Stick to the studied dose for your goal unless your doctor advises otherwise.</p>'],
      ['Should saffron be taken morning or night?', '<p>For mood, split it morning and evening. For sleep, take it in the evening or split it. For appetite, take it before meals.</p>'],
      ['Can I take saffron on an empty stomach?', '<p>You can, but taking it with food reduces the chance of mild nausea.</p>'],
      ['How much saffron is in a cup of saffron tea?', '<p>It depends on how many threads you use. A typical cup uses 10–20 threads, roughly 20–40 mg of spice, but its active-compound content is unknown.</p>'],
    ]) ?>
    <?= sources([
      'Modaghegh MH, et al. Safety evaluation of saffron (Crocus sativus) tablets in healthy volunteers. <em>Phytomedicine.</em> 2008;15(12):1032-1037.',
      'Schmidt M, Betti G, Hensel A. Saffron in phytotherapy: pharmacology and clinical uses. <em>Wien Med Wochenschr.</em> 2007;157(13-14):315-319.',
      'Marx W, et al. Effect of saffron supplementation on symptoms of depression and anxiety. <em>Nutr Rev.</em> 2019;77(8):557-571.',
      'Kell G, et al. affron® improves mood in healthy adults over 4 weeks. <em>Complement Ther Med.</em> 2017;33:58-64.',
      'Gout B, et al. Satiereal reduces snacking and increases satiety. <em>Nutr Res.</em> 2010;30(5):305-313.',
    ]) ?>
    <?= med_note() ?>
  </article>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
