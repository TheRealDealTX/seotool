<?php defined('SS_APP') || exit; ?>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="kicker">Updated <?= UPDATED_HUMAN ?> &middot; Independent &amp; research-based</p>
      <h1>Saffron Supplement Guide: <em>What Works, How Much, and What to Buy</em></h1>
      <p class="lede">Saffron Supplement is a free, independent guide to saffron extract. We read the clinical trials so you don't have to, then turn them into plain-English advice on benefits, dosage and safety, plus free tools and honest reviews of the best saffron supplements on Amazon.</p>
      <div class="hero-cta">
        <a class="btn" href="/best-saffron-supplements/">See the Best Saffron Supplements</a>
        <a class="btn btn-ghost" href="/tools/saffron-supplement-quiz/">Take the 60-Second Quiz</a>
      </div>
      <ul class="trust">
        <li>Every claim cited to a clinical trial</li>
        <li>12 products compared label by label</li>
        <li>5 free interactive tools</li>
      </ul>
    </div>
    <div class="hero-card mini-calc">
      <h2>Quick Dose Finder</h2>
      <p class="small">Pick a goal to see the dose used in clinical studies.</p>
      <label for="mini-goal">What do you want saffron to help with?</label>
      <select id="mini-goal">
        <option value="mood">Low mood &amp; emotional balance</option>
        <option value="stress">Stress &amp; everyday anxiety</option>
        <option value="sleep">Sleep quality</option>
        <option value="eyes">Eye health (macular)</option>
        <option value="appetite">Snacking &amp; appetite</option>
        <option value="pms">PMS symptoms</option>
      </select>
      <div class="mini-out" id="mini-out" aria-live="polite"></div>
      <p style="margin:14px 0 0"><a href="/tools/saffron-dosage-calculator/">Open the full dosage calculator &rarr;</a></p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="stat-row">
      <div class="stat"><b>30 mg</b><span>Most-studied daily dose of saffron extract</span></div>
      <div class="stat"><b>20+</b><span>Randomized trials on saffron and mood</span></div>
      <div class="stat"><b>4–8 wks</b><span>Typical time to notice results</span></div>
      <div class="stat"><b>~150,000</b><span>Crocus flowers to make 1 kg of saffron</span></div>
    </div>
    <div class="grid g2" style="align-items:center;gap:40px">
      <div>
        <h2 style="margin-top:0">What Is a Saffron Supplement?</h2>
        <p>A saffron supplement is a capsule, tablet, softgel or gummy containing a concentrated extract of the stigmas of the saffron crocus, <em>Crocus sativus</em>. Those red threads are the world's most expensive spice, and they contain three compounds researchers care about: <strong>crocins</strong> (the pigments), <strong>safranal</strong> (the aroma) and <strong>picrocrocin</strong> (the bitter taste).</p>
        <p>Because extract is standardized, one 30 mg saffron supplement capsule delivers a consistent amount of those compounds. A pinch of kitchen saffron does not. That consistency is why nearly every clinical trial uses an extract, and why Saffron Supplement focuses on extract products rather than threads.</p>
        <p><a href="/saffron-benefits/">Read the full breakdown of saffron's benefits &rarr;</a></p>
      </div>
      <div class="keyfacts" style="margin:0">
        <h2>Key facts at a glance</h2>
        <ul>
          <li><strong>Best-supported use:</strong> mild-to-moderate low mood</li>
          <li><strong>Typical dose:</strong> 20–30 mg extract daily (176 mg for Satiereal®)</li>
          <li><strong>Time to work:</strong> 2–8 weeks depending on the goal</li>
          <li><strong>Safety:</strong> well tolerated at studied doses; avoid high doses in pregnancy</li>
          <li><strong>Upper limit in trials:</strong> up to 100 mg/day used safely short-term</li>
          <li><strong>Watch out for:</strong> antidepressant, blood-thinner and blood-pressure interactions</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <h2>Saffron Supplement Benefits, Ranked by Evidence</h2>
      <p>Not every claim about saffron is equally solid. Here is how Saffron Supplement rates the research behind each benefit, from several meta-analyses down to a handful of small pilot trials.</p>
    </div>
    <div class="evidence">
      <div class="ev-row"><span>Low mood</span><span class="ev-bar"><i style="width:88%"></i></span><span>Strong</span></div>
      <div class="ev-row"><span>Stress &amp; anxiety</span><span class="ev-bar"><i style="width:66%"></i></span><span>Moderate</span></div>
      <div class="ev-row"><span>Sleep quality</span><span class="ev-bar"><i style="width:60%"></i></span><span>Moderate</span></div>
      <div class="ev-row"><span>Macular eye health</span><span class="ev-bar"><i style="width:56%"></i></span><span>Moderate</span></div>
      <div class="ev-row"><span>PMS symptoms</span><span class="ev-bar"><i style="width:50%"></i></span><span>Promising</span></div>
      <div class="ev-row"><span>Libido &amp; sexual function</span><span class="ev-bar"><i style="width:45%"></i></span><span>Promising</span></div>
      <div class="ev-row"><span>Snacking &amp; appetite</span><span class="ev-bar"><i style="width:40%"></i></span><span>Limited</span></div>
      <div class="ev-row"><span>Memory &amp; cognition</span><span class="ev-bar"><i style="width:32%"></i></span><span>Early</span></div>
    </div>
    <div class="grid g3" style="margin-top:30px">
      <?= card('/saffron-for-depression-and-mood/', 'Saffron for Mood', 'Saffron has the most evidence for low mood, with several trials finding effects similar to standard medication in mild-to-moderate cases.', '🌤️') ?>
      <?= card('/saffron-for-sleep/', 'Saffron for Sleep', 'A 28 mg daily dose of affron® improved sleep quality scores in adults with self-reported poor sleep.', '🌙') ?>
      <?= card('/saffron-for-eye-health/', 'Saffron for Eye Health', '20 mg a day improved retinal function in early macular degeneration trials.', '👁️') ?>
      <?= card('/saffron-for-weight-loss/', 'Saffron for Appetite', 'Satiereal® reduced snacking in a study of mildly overweight women. Useful for cravings, but don\'t expect dramatic weight loss.', '🍽️') ?>
      <?= card('/saffron-for-pms/', 'Saffron for PMS', '15 mg twice daily cut PMS symptom scores in a randomized trial.', '🌸') ?>
      <?= card('/saffron-dosage/', 'Saffron Dosage Guide', 'How much to take for each goal, when to take it, and the safe upper limits.', '⚖️') ?>
    </div>
  </div>
</section>

<section class="section section-alt" id="top-picks">
  <div class="wrap">
    <div class="sec-head">
      <h2>Best Saffron Supplements of <?= SITE_YEAR ?>: Our Top 5</h2>
      <p>The Saffron Supplement team compared 12 popular products on Amazon by dose, extract standardization, brand testing and value. These five came out on top. <?= a('/best-saffron-supplements/', 'See all 12 reviews and the full comparison table') ?>.</p>
    </div>
    <?= aff_note() ?>
    <div class="grid g2" style="gap:24px">
      <?php foreach (TOP_PICKS as $i => $id) echo product_card($id, $i + 1); ?>
      <div class="card" style="display:flex;flex-direction:column;justify-content:center;background:var(--plum-soft)">
        <h3>Not sure which one fits you?</h3>
        <p>Answer five quick questions and the Saffron Supplement Finder matches you to the right extract, dose and budget.</p>
        <p><a class="btn" href="/tools/saffron-supplement-quiz/">Start the Quiz</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <h2>Free Saffron Tools</h2>
      <p>Saffron Supplement built these tools to answer the questions readers ask most: how much to take, which product, is it safe for me, and is it working?</p>
    </div>
    <div class="grid g3">
      <?= card('/tools/saffron-dosage-calculator/', 'Dosage Calculator', 'Get a research-matched daily dose, capsule count and timing for your goal.', '🧮') ?>
      <?= card('/tools/saffron-supplement-quiz/', 'Supplement Finder Quiz', 'Five questions, one personalized product match.', '🎯') ?>
      <?= card('/tools/cost-per-dose-calculator/', 'Cost-Per-Dose Calculator', 'Compare bottles by what an effective daily dose actually costs.', '💲') ?>
      <?= card('/tools/saffron-safety-checker/', 'Safety Checker', 'Flags medications and conditions to raise with your doctor before starting.', '🛡️') ?>
      <?= card('/tools/saffron-mood-sleep-tracker/', '12-Week Mood & Sleep Tracker', 'Log how you feel and chart your progress, saved privately in your browser.', '📈') ?>
      <?= card('/how-to-choose-a-saffron-supplement/', 'Label Checklist', 'Seven things to check on any saffron label before you buy.', '✅') ?>
    </div>
  </div>
</section>

<section class="section section-plum">
  <div class="wrap grid g2" style="gap:40px;align-items:center">
    <div>
      <h2 style="margin-top:0">How to Choose a Saffron Supplement in 3 Steps</h2>
      <ol class="steps">
        <li><strong>Match the dose to your goal.</strong> 28–30 mg for mood, stress and sleep; 20 mg for eyes; about 176 mg of Satiereal® for appetite.</li>
        <li><strong>Look for standardization.</strong> The label should state crocin and/or safranal percentages, or use a branded extract such as affron® or Satiereal®.</li>
        <li><strong>Buy from a tested brand.</strong> Saffron is one of the most adulterated spices on earth. Pick brands that publish third-party testing.</li>
      </ol>
      <p><a class="btn btn-light" href="/how-to-choose-a-saffron-supplement/">Read the full buying guide</a></p>
    </div>
    <div>
      <div class="table-wrap" style="color:var(--ink)">
        <table>
          <thead><tr><th>Goal</th><th>Daily dose in trials</th><th>Results in</th></tr></thead>
          <tbody>
            <tr><td>Low mood</td><td>30 mg (15 mg × 2)</td><td>4–8 weeks</td></tr>
            <tr><td>Stress / anxiety</td><td>28–30 mg</td><td>4–8 weeks</td></tr>
            <tr><td>Sleep</td><td>28 mg (14 mg × 2)</td><td>2–4 weeks</td></tr>
            <tr><td>Eye health</td><td>20 mg</td><td>~3 months</td></tr>
            <tr><td>PMS</td><td>30 mg (15 mg × 2)</td><td>2 cycles</td></tr>
            <tr><td>Appetite</td><td>176.5 mg Satiereal®</td><td>4–8 weeks</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid g2" style="gap:40px">
    <div>
      <h2 style="margin-top:0">Is a Saffron Supplement Safe?</h2>
      <p>At the doses used in research, saffron is well tolerated. The side effects reported most often are mild: nausea, dry mouth, headache or a change in appetite. Short-term studies have used up to 100 mg a day without serious problems, while toxic effects have only been reported at several grams, far more than any capsule contains.</p>
      <p>A few groups should take extra care. Saffron Supplement recommends speaking to a doctor first if you are pregnant, have bipolar disorder, or take SSRIs, blood thinners or blood-pressure medication.</p>
      <p><a class="btn btn-ghost" href="/tools/saffron-safety-checker/">Run the Safety Checker</a> &nbsp; <a href="/saffron-side-effects/">Read the full safety guide</a></p>
    </div>
    <div>
      <h2 style="margin-top:0">Why Trust Saffron Supplement?</h2>
      <p>Saffron Supplement is a small, independent publication, not a supplement brand. We don't sell our own product, and no company can pay for a ranking. Every health claim on Saffron Supplement links to the peer-reviewed study behind it, and we say plainly when the evidence is thin.</p>
      <p>We earn a small commission when you buy through our Amazon links, which keeps the site free. That commission is the same whichever product you choose, so it doesn't change our rankings. <a href="/about/">Read how we research and rate products</a>.</p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="sec-head"><h2>Popular Saffron Guides</h2></div>
    <div class="grid g4">
      <?= card('/saffron-dosage/', 'Saffron Dosage', 'How much saffron to take, by goal.') ?>
      <?= card('/saffron-side-effects/', 'Side Effects & Interactions', 'Who should avoid saffron and why.') ?>
      <?= card('/affron-vs-satiereal/', 'affron® vs Satiereal®', 'The two branded extracts compared.') ?>
      <?= card('/how-to-choose-a-saffron-supplement/', 'How to Choose', 'A 7-point label checklist.') ?>
    </div>
    <h2>Pair Your Saffron Supplement With…</h2>
    <p>Readers often combine saffron with these. Each link opens an Amazon search.</p>
    <ul class="related">
      <?php foreach (RELATED as [$label, $q]) echo '<li>' . amz($q, e($label)) . '</li>'; ?>
    </ul>
  </div>
</section>

<section class="section">
  <div class="narrow">
    <?= faq_block([
      ['What does a saffron supplement do?', '<p>A saffron supplement delivers standardized saffron extract, mainly crocins and safranal. Clinical trials link it most strongly to better mood, with moderate evidence for stress, sleep quality and early macular degeneration, and smaller studies on PMS, appetite and libido.</p>'],
      ['How long does it take for saffron to work?', '<p>Sleep improvements have appeared within 2–4 weeks in trials. Mood benefits usually take 4–8 weeks, and eye studies measured changes after about 3 months. Give any saffron supplement at least 6 weeks at a consistent dose before judging it.</p>'],
      ['What is the best time of day to take saffron?', '<p>For mood, most trials split the dose between morning and evening. For sleep, take it in the evening or split it. Taking saffron with food can reduce mild nausea.</p>'],
      ['Can I take saffron with antidepressants?', '<p>Only with your doctor\'s approval. Saffron appears to affect serotonin, so combining it with SSRIs, SNRIs or MAOIs could in theory add to their effects. Some trials have used saffron alongside SSRIs under medical supervision.</p>'],
      ['Is saffron extract better than saffron spice?', '<p>For supplement use, yes. Extract delivers a known amount of active compounds in a small dose, while the strength of kitchen saffron varies widely and is often adulterated. The spice is still wonderful for cooking.</p>'],
      ['Which saffron supplement is best?', '<p>For most people, Saffron Supplement\'s top pick is a 28–30 mg standardized extract such as ' . amz('B0B69MGMFW', 'Nootropics Depot Saffron 30 mg') . ' or an affron® product. For appetite, choose a Satiereal® product such as ' . amz('B003UGS4T0', 'Life Extension Optimized Saffron') . '. See the <a href="/best-saffron-supplements/">full rankings</a>.</p>'],
    ]) ?>
    <div class="cta-band">
      <div>
        <h2>Find the right saffron supplement in 60 seconds</h2>
        <p>Answer five questions and get a personalized product and dose match.</p>
      </div>
      <a class="btn btn-amz" href="/tools/saffron-supplement-quiz/">Start the Quiz &rarr;</a>
    </div>
    <?= med_note() ?>
  </div>
</section>
