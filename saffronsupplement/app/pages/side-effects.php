<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Saffron is well tolerated at the doses used in research, but it isn\'t right for everyone. Here are the side effects to expect, the drug interactions that matter, and who should avoid saffron supplements.', 'Guides &middot; Safety');
?>
<div class="wrap layout">
  <article class="prose">
    <div class="keyfacts">
      <h2>Key takeaways</h2>
      <ul>
        <li>Side effects at 20–30 mg/day are <strong>uncommon and mild</strong>: nausea, dry mouth, headache, appetite changes.</li>
        <li><strong>Avoid high doses in pregnancy</strong>; large amounts may stimulate the uterus.</li>
        <li>Use caution with <strong>antidepressants, blood thinners, blood-pressure and diabetes medication</strong>.</li>
        <li>People with <strong>bipolar disorder</strong> should avoid saffron unless a psychiatrist approves.</li>
      </ul>
    </div>
    <?= toc(['common' => 'Common side effects', 'serious' => 'Rare & serious effects', 'who' => 'Who should avoid saffron', 'interactions' => 'Drug interactions', 'quality' => 'Adulteration risk', 'checker' => 'Safety checker', 'faq' => 'FAQ']) ?>

    <h2 id="common">Common Side Effects</h2>
    <p>Across trials at 20–30 mg/day, side effects occurred at rates similar to placebo. When they do occur, they are usually mild:</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Side effect</th><th>How common</th><th>Tip</th></tr></thead>
      <tbody>
        <tr><td>Nausea or upset stomach</td><td>Occasional</td><td>Take with food</td></tr>
        <tr><td>Dry mouth</td><td>Occasional</td><td>Stay hydrated</td></tr>
        <tr><td>Headache</td><td>Occasional</td><td>Try a lower dose</td></tr>
        <tr><td>Change in appetite</td><td>Occasional</td><td>Usually reduced appetite</td></tr>
        <tr><td>Drowsiness or restlessness</td><td>Uncommon</td><td>Adjust timing (evening vs morning)</td></tr>
        <tr><td>Allergic reaction</td><td>Rare</td><td>Stop and seek care; more likely if allergic to <em>Lolium</em>, <em>Olea</em> or <em>Salsola</em> pollens</td></tr>
      </tbody>
    </table></div>

    <h2 id="serious">Rare and Serious Effects</h2>
    <p>At very high doses (several grams, far beyond any supplement), saffron can cause vomiting, bleeding, dizziness, numbness and yellowing of the skin and eyes. Doses of 5 g or more have been described as toxic. A one-week study found minor changes in some blood measures at 400 mg/day (Modaghegh 2008). Stick to research doses.</p>

    <h2 id="who">Who Should Avoid Saffron Supplements?</h2>
    <div class="flag flag-red"><strong>Pregnancy:</strong> large amounts of saffron have historically been used to stimulate the uterus. Culinary amounts are considered fine, but avoid supplements unless your obstetrician approves.</div>
    <div class="flag flag-red"><strong>Bipolar disorder:</strong> saffron's mood-lifting effect could, in theory, trigger mania or hypomania.</div>
    <div class="flag flag-amber"><strong>Breastfeeding:</strong> not enough safety data. Stick to food amounts.</div>
    <div class="flag flag-amber"><strong>Low blood pressure:</strong> saffron may lower blood pressure slightly.</div>
    <div class="flag flag-amber"><strong>Bleeding disorders or upcoming surgery:</strong> high doses may affect platelets. Stop 2 weeks before surgery.</div>
    <div class="flag flag-amber"><strong>Children and teens:</strong> one affron® trial included 12–16-year-olds under supervision. Only use under a doctor's guidance.</div>

    <h2 id="interactions">Saffron Drug Interactions</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>Medication type</th><th>Examples</th><th>Concern</th></tr></thead>
      <tbody>
        <tr><td>Antidepressants (SSRIs, SNRIs, MAOIs, TCAs)</td><td>Sertraline, fluoxetine, venlafaxine</td><td>Possible additive serotonin effect. Some trials combined them under supervision.</td></tr>
        <tr><td>Blood thinners &amp; antiplatelets</td><td>Warfarin, apixaban, clopidogrel, aspirin</td><td>May increase bleeding risk at high doses</td></tr>
        <tr><td>Blood-pressure medication</td><td>Amlodipine, lisinopril</td><td>May add to blood-pressure lowering</td></tr>
        <tr><td>Diabetes medication</td><td>Metformin, insulin</td><td>May slightly lower blood sugar; monitor levels</td></tr>
        <tr><td>Sedatives</td><td>Benzodiazepines, sleep aids</td><td>Possible additive drowsiness</td></tr>
        <tr><td>Other serotonergic supplements</td><td>5-HTP, St John's wort, SAMe</td><td>Avoid stacking without medical advice</td></tr>
      </tbody>
    </table></div>
    <p>This list isn't complete. Always show your pharmacist the supplement bottle.</p>

    <h2 id="quality">The Hidden Risk: Adulteration</h2>
    <p>Saffron is so expensive that fake and "cut" saffron is common in the spice trade. Bulking agents have included safflower, marigold, turmeric, dyed corn silk and synthetic dyes. With supplements, the safest approach is to buy branded extracts (affron®, Satiereal®) or products from manufacturers with third-party testing. See our <a href="/how-to-choose-a-saffron-supplement/">buying checklist</a>.</p>

    <h2 id="checker">Check Your Situation</h2>
    <p>Use the free <a href="/tools/saffron-safety-checker/">saffron safety checker</a> to see which of these points apply to you, then take the results to your doctor or pharmacist.</p>
    <p><a class="btn" href="/tools/saffron-safety-checker/">Open the Safety Checker</a></p>

    <?= faq_block([
      ['What are the negative effects of saffron?', '<p>At normal supplement doses, side effects are uncommon and mild: nausea, dry mouth, headache, appetite changes and occasionally drowsiness. Serious effects have only been reported at doses many times higher than supplements contain.</p>'],
      ['Is saffron hard on the liver or kidneys?', '<p>Studies at normal doses have not shown liver or kidney harm, and some animal research suggests protective effects. If you have liver or kidney disease, ask your doctor first.</p>'],
      ['Can saffron cause anxiety?', '<p>It is uncommon. Trials more often found saffron reduced anxiety. A few people report restlessness. Taking it earlier in the day may help.</p>'],
      ['Is saffron safe to take with sertraline?', '<p>Only with your doctor\'s approval. Saffron may affect serotonin, so combining it with sertraline or other SSRIs needs medical supervision.</p>'],
      ['Can saffron cause bleeding?', '<p>Only at very high doses. If you take blood thinners or have a bleeding disorder, discuss saffron with your doctor.</p>'],
    ]) ?>
    <?= sources([
      'Modaghegh MH, et al. Safety evaluation of saffron (Crocus sativus) tablets in healthy volunteers. <em>Phytomedicine.</em> 2008;15(12):1032-1037.',
      'Schmidt M, Betti G, Hensel A. Saffron in phytotherapy: pharmacology and clinical uses. <em>Wien Med Wochenschr.</em> 2007;157(13-14):315-319.',
      'Marx W, et al. Effect of saffron supplementation on symptoms of depression and anxiety. <em>Nutr Rev.</em> 2019;77(8):557-571.',
      'Lopresti AL, et al. Affron® for youth anxiety and depressive symptoms. <em>J Affect Disord.</em> 2018;232:349-357.',
    ]) ?>
    <?= med_note() ?>
  </article>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
